#!/usr/bin/env python3
"""
AXIOMENGINE NON-BLOCKING GOVERNOR (Phase 7)

Pre-checks an agent's proposal against PDD rules WITHOUT blocking execution.
The caller's action proceeds immediately; the compliance verdict is resolved
in the background and, on rejection, is routed to one of:

  - a PDD rule-mutation proposal (pdd_proposals table) when the proposal
    looks like it should change/extend governance itself, or
  - an isolated git worktree/branch (via git_worker.sh) so the
    non-compliant change can be reviewed in isolation instead of landing
    on the working branch.

This complements Governor (scripts/governor.py), which is a synchronous,
blocking PASS/REJECT gate. Use NonBlockingGovernor when the caller wants to
keep moving and have drift handled asynchronously.
"""
import asyncio
import subprocess
import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT / "scripts"))

from governor import Governor
from propose_rule import propose_rule
from system_one import SystemOneClient

GIT_WORKER = PROJECT_ROOT / "scripts" / "git_worker.sh"
QUARANTINE_ROOT = PROJECT_ROOT / ".quarantine"


class NonBlockingGovernor:
    """
    Wraps Governor.validate_proposal so governance checks never stall the
    calling agent. `precheck` schedules validation as a background task and
    returns immediately with a handle; callers that care about the outcome
    can await the returned task, but nothing requires them to.
    """

    def __init__(self, session_id: str = "nb_gov_session"):
        self._governor = Governor(session_id=session_id)
        self._system_one = SystemOneClient(name="NonBlockingGovernor", session_id=session_id)

    def precheck(self, agent_name: str, task: str, proposal: str) -> asyncio.Task:
        """Fire-and-forget: kicks off validation + routing, returns the Task."""
        return asyncio.create_task(
            self._check_and_route(agent_name, task, proposal)
        )

    async def _check_and_route(self, agent_name: str, task: str, proposal: str) -> dict:
        verdict = await self._governor.validate_proposal(agent_name, task, proposal)
        compliant = verdict.strip().upper().startswith("PASS")

        result = {"agent_name": agent_name, "task": task, "verdict": verdict, "compliant": compliant}

        if compliant:
            return result

        reason = verdict.split(":", 1)[1].strip() if ":" in verdict else verdict
        route = await self._route_noncompliant(agent_name, task, proposal, reason)
        result["route"] = route
        return result

    async def _route_noncompliant(self, agent_name: str, task: str, proposal: str, reason: str) -> dict:
        """
        Decide how to handle a rejected proposal without blocking the caller:
        - If the reason implies a governance gap (no rule covers this case),
          file a PDD rule proposal for human review.
        - Otherwise, isolate the change on its own branch/worktree so it
          never lands directly on the active branch.

        This classification used to be a keyword-substring guess ("no rule"
        in reason.lower()), which misses phrasing the model didn't happen to
        use. It's exactly the kind of atomic, bounded choice a System One
        model is suited for: not deterministic (no fixed vocabulary of
        rejection reasons exists), but far simpler than a full chat
        completion. If the classifier degrades (model unreachable, bad
        output), fall back to the original keyword heuristic rather than
        blocking or guessing worse.
        """
        classification = self._system_one.choice(
            state=f"Governance rejection reason from {agent_name}'s task '{task}': {reason}",
            question=(
                "Is this rejection reason a governance COVERAGE GAP (no existing rule "
                "addresses this situation at all), or a POLICY VIOLATION (an existing "
                "rule was broken)?"
            ),
            options=["coverage_gap", "policy_violation"],
        )

        if classification["degraded"]:
            looks_like_gap = any(
                phrase in reason.lower()
                for phrase in ("no rule", "not covered", "undefined", "no applicable", "no matching rule")
            )
        else:
            looks_like_gap = classification["best"] == "coverage_gap"

        if looks_like_gap:
            pid = await propose_rule(
                rule_id=f"R-AUTO-{uuid.uuid4().hex[:8].upper()}",
                agent_name=agent_name,
                change_type="new",
                title=f"Coverage gap surfaced by {agent_name}",
                content=f"Task: {task}\nProposal:\n{proposal}",
                rationale=f"Non-blocking governor detected an uncovered case: {reason}",
            )
            return {"action": "rule_proposal", "proposal_id": pid, "classification": classification}

        branch = f"quarantine/{agent_name.lower()}-{uuid.uuid4().hex[:8]}"
        target = QUARANTINE_ROOT / branch.replace("/", "-")
        try:
            subprocess.run(
                ["bash", str(GIT_WORKER), branch, str(target)],
                check=True, capture_output=True, text=True, cwd=str(PROJECT_ROOT),
            )
            return {"action": "quarantine_branch", "branch": branch, "path": str(target), "classification": classification}
        except subprocess.CalledProcessError as e:
            return {"action": "quarantine_branch_failed", "branch": branch, "error": e.stderr}


async def main():
    nbg = NonBlockingGovernor()

    print("Dispatching non-compliant proposal (should NOT block)...")
    task_handle = nbg.precheck(
        "TestAgent",
        "Run intensive training on Tesla P40",
        "Start fine-tuning with 100% load on P40 without temperature checks.",
    )
    print("Caller proceeds immediately; governance resolves in background.")

    outcome = await task_handle
    print(f"Background verdict: {outcome}")


if __name__ == "__main__":
    asyncio.run(main())
