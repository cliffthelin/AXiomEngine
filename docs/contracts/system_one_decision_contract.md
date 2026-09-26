# System One Decision Contract (v1.0.0)

This document defines `scripts/system_one.py`'s `SystemOneClient` — a small,
self-hosted "System One" primitive set (fast, structured **Choice** and
**Score** decisions) for call sites that are currently either a hand-rolled
heuristic or a full free-text chat completion doing something much simpler.

## What this is not

This is **not** a client for any third-party hosted decision API. It runs
entirely over AXiomEngine's own governed router (`AXiomEngineClient.chat`),
using models already declared in `model_registry`
(`scripts/00_install_base.sh`). No new external service, package, or model
weight is required. If you've seen marketing content for hosted "System One"
decision products, treat it as inspiration for the *interface shape*
(Choice/Score, not open-ended generation) — not as something to install.

## When to reach for it

Use `SystemOneClient` when a decision:
- Has a **small, enumerable option set** (Choice) or produces a **single
  scalar match/confidence value** (Score).
- Is **not deterministic** — no fixed rule or lookup table can answer it — so
  a plain `if`/keyword check would be guessing, not computing.
- Doesn't need open-ended reasoning, multi-turn context, or tool use — i.e.
  it would be wasteful to route through a full chat completion just to get
  one word or one float back out.

Do **not** use it for anything `Governor` already does end-to-end (PASS/REJECT
with a free-text rationale) — that's intentionally a richer, explainable
verdict, not a bounded choice. Do not use it to replace a check that actually
is deterministic (e.g. a numeric threshold, a file existence check) — those
belong in code, not a model call.

## Interface

```python
from scripts.system_one import SystemOneClient

client = SystemOneClient(name="MyAgent", session_id="...")

result = client.choice(
    state="<context the decision needs>",
    question="<the single question being asked>",
    options=["option_a", "option_b", "..."],
)
# {"options": [...], "probabilities": [...], "best": "option_a",
#  "confidence": 0.83, "degraded": false}

result = client.score(
    state="<context>",
    question="<the single question being asked>",
)
# {"score": 0.71, "degraded": false}
```

## Design Invariants

- **Never blocks worse than a chat call already would**: both primitives are
  synchronous HTTP calls through the same governed router path `Governor`
  already uses; they carry no additional latency risk class.
- **Never raises**: any parse failure, network error, or malformed model
  output degrades to a neutral answer (uniform distribution for `choice`,
  `0.5` for `score`) with `degraded: true` set, rather than propagating an
  exception into the caller's control flow.
- **Callers must check `degraded`**: a degraded result means "the model
  didn't answer usefully," not "the answer is uniform/neutral." Callers with
  an existing deterministic-ish fallback (e.g. a keyword heuristic) should
  use it only in the degraded case, never as the primary path — see
  `NonBlockingGovernor._route_noncompliant` for the reference pattern.
- **No hidden state**: each call is independent; there is no session memory
  inside `SystemOneClient` itself (use `conversation_memory.py` if a decision
  genuinely needs prior-turn context).

## Current call sites

- `scripts/nonblocking_governor.py` (`_route_noncompliant`): classifies a
  Governor rejection reason as `coverage_gap` vs `policy_violation` to decide
  whether to file a PDD rule proposal or quarantine the change on its own
  branch. Previously a keyword-substring guess; now a bounded `choice` call
  with the old heuristic kept only as the `degraded` fallback.

## Candidate future call sites (not yet wired)

- `scripts/skill_harvester.py`: a `score` call on "how novel/reusable is this
  harvested workflow" could pre-rank candidates before a human reviews them
  (never replacing the human `--approve` gate).
- `scripts/dispatcher.py` / `scripts/swarm_coordinator.py`: a `choice` call
  over the registered subagent roster for "which agent should handle this
  task" is a textbook fit, if/when routing there stops being purely
  keyword/tag based.
- Any future OCR/evidence reconciliation step that needs "which of N
  candidate values is correct" — the exact use case this pattern is suited
  for, per the design note in `docs/roadmap/`.
