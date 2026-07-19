# Remote Compute Scoping (Phase 7, long-term)

> Status: **SCOPED, NOT IMPLEMENTED**. This document turns the roadmap's
> one-liner ("Consider off-host execution via Modal or SSH sandboxes") into a
> concrete first step. It does not ship code.

## Why this is separate from Phase 4 sandboxing

`scripts/sandbox.py` (`AgentSandbox`) already isolates *where on this host* an
agent's command runs — CGroups for resource capping, MicroVM (`qemu-microvm`)
for hard security isolation. Both modes assume the RTX 3070 / Tesla P40 / USB
hub described in `docs/ROADMAP.md`'s hardware table are always available
locally. Remote Compute is about the case where they aren't: a job that needs
more VRAM than the local rig has, or needs to run while the host is powered
down, or needs to run somewhere with different compliance boundaries.

## Goals

1. Let an agent task run on off-host compute (a Modal function, or an SSH'd
   remote machine) using the **same governance contract** as local execution:
   the job is still subject to PDD rule injection, still writes to
   `agent_audit`, still respects the thermal/VRAM invariants that apply to
   *its* hardware.
2. Make remote execution an *additional* `AgentSandbox` mode, not a parallel
   system — callers should not need to know or care whether `mode="remote"`
   dispatches to Modal, SSH, or stays local.
3. Fail closed: if remote dispatch can't be governed (no audit sink reachable,
   no PDD context available), it must not silently fall back to ungoverned
   execution.

## Two backends considered

| | Modal | SSH Sandbox |
|---|---|---|
| **Model** | Serverless function calls; AXiomEngine submits a job, Modal provisions ephemeral compute | Long-lived remote host reachable via SSH; AXiomEngine dispatches a command over an established connection |
| **Auth** | Modal API token (needs a secrets path — see `scripts/keychain.py`) | SSH key already managed by the operator; reuse existing key material, don't mint new secrets |
| **Isolation** | Provider-managed container per invocation | Whatever the remote host provides (its own cgroup/microvm) — AXiomEngine can't fully guarantee this |
| **Cost model** | Pay-per-invocation, no idle cost | Idle cost if the box is dedicated; free if it's spare hardware the operator already owns |
| **Best fit** | Bursty jobs (e.g. one-off fine-tune) needing GPU classes bigger than the local rig | Recurring jobs, or when the operator has a specific known second machine (e.g. a homelab node) |

Recommendation: **prototype SSH sandbox first.** It reuses infrastructure
this repo already has opinions about (`git_worker.sh` worktree isolation,
existing key-based auth patterns in `keychain.py`) and needs no new billing
relationship. Modal is the natural second backend once the `AgentSandbox`
interface has a real second mode to generalize from.

## Proposed interface (not yet implemented)

```python
class AgentSandbox:
    def __init__(self, agent_name: str, mode: str = "cgroup"):
        # mode: "cgroup" | "microvm" | "remote_ssh" | "remote_modal"
        ...

    def run_command(self, cmd_list: list):
        if self.mode == "remote_ssh":
            return self.run_remote_ssh(cmd_list)
        if self.mode == "remote_modal":
            return self.run_remote_modal(cmd_list)
        ...  # existing local modes unchanged
```

`run_remote_ssh` / `run_remote_modal` would each:
1. Resolve remote credentials via `scripts/keychain.py` (never inline in code
   or config).
2. Attach the same PDD rule context the local path would (`get_pdd_rules`)
   to whatever prompt/command is dispatched.
3. Stream results back into `agent_audit` with `backend` set to
   `"remote_ssh"` / `"remote_modal"` so the audit trail distinguishes
   off-host runs from local ones.
4. Surface hardware telemetry if the remote side can report it (GPU temp,
   VRAM) so `vgpu_manager.py` and the thermal monitor stay meaningful; if it
   can't, the run must be flagged `telemetry_unavailable: true` rather than
   silently omitting the check the way `docs/ROADMAP.md`'s Phase 0 thermal
   safety work assumed.

## Open questions to resolve before implementation starts

- **Audit sink reachability**: if the remote box can't reach the local
  Postgres/Valkey audit stack, does the job block, buffer locally and
  replay, or refuse to run? (Recommend: refuse to run — matches the
  "fail closed" goal above.)
- **Cost governance**: does the Governor (`scripts/governor.py` /
  `scripts/nonblocking_governor.py`) need a new rule scope for
  "spend real money" actions (Modal billing) before this ships? Likely yes.
- **Secrets**: does `keychain.py` already support a remote-host credential
  type, or does that need its own small extension first?

## Suggested first implementation slice

A single `run_remote_ssh` path behind `AgentSandbox(mode="remote_ssh")`,
targeting one operator-configured host, with:
- No new billing relationship (defers the Modal question entirely).
- Audit writes required, not optional, before the run is considered started.
- A single new test asserting a job with unreachable audit sink refuses to
  run rather than executing ungoverned.

This is intentionally the smallest slice that proves the governance contract
holds off-host, before generalizing to a second (Modal) backend.
