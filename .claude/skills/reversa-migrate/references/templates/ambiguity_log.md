```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: ambiguity_log
producedBy: orchestrator
hash: "sha256:<hash do corpo abaixo do front-matter>"
---

# Ambiguity Log

> Consolidation of all ⚠️ AMBIGUOUS or pending items detected by the agents throughout the pipeline.
> Expected final status when the pipeline completes: no PENDING items.

## Summary
- Total items: <N>
- PENDING: <n>
- RESOLVED WITH HUMAN DECISION: <n>
- REFERRED TO CODIFICATION: <n>

## Items

### AMB-001
- **Description**: <text>
- **Detected by**: paradigm_advisor | curator | strategist | designer | screen_translator | inspector
- **Origin**: <reference to the artifact and section>
- **Status**: PENDING | RESOLVED WITH HUMAN DECISION | REFERRED TO CODIFICATION
- **Decision taken** (if applicable):
  - **Choice**: <text>
  - **Decider**: <name>
  - **When**: <ISO-8601>
  - **Justification**: <text>

<repeat for each item>

## Items referred to codification
> Lists only items with the status `REFERRED TO CODIFICATION`. They will appear highlighted in `handoff.md`.

- AMB-XXX: <short description>

## Notes
<Final notes from the orchestrator.>
```