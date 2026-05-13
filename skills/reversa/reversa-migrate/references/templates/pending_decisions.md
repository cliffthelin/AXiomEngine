```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: pending_decisions
producedBy: orchestrator
hash: "sha256:<hash of the body below the front-matter>"
---

# Pending Decisions

> A transient file used during human pauses. Each item describes an open decision with context and options.
> After the user responds, the item is moved to `ambiguity_log.md` (or to the artifact that owns the decision), and this file can be deleted.

## Open Decisions

### PD-001
- **Requesting Agent**: paradigm_advisor | curator | strategist | designer | screen_translator | inspector
- **Topic**: <short title>
- **Context**:
  <text explaining why this decision is needed here>
- **Options**:
  1. <option 1>
  2. <option 2>
  3. <option 3>
- **Proposed Default** (used in `--auto`): <option number>
- **Impact if decided incorrectly**: <text>
- **Where the decision will be recorded**: <e.g., `paradigm_decision.md § User Decision`>

<repeat for each decision>

## How to Respond

- In chat: by responding directly to the agent with the option number and justification.
- In file: by editing this `pending_decisions.md` file, adding a `Response:` field to each item.
```