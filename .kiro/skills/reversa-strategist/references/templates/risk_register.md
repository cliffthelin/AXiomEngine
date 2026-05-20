```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: risk_register
producedBy: strategist
hash: "sha256:<hash of the body below the front-matter>"
---

# Risk Register

> A register of migration risks, including probability, impact, mitigation, and responsible party.

## Risks

### RISK-001
- **Description**: <text>
- **Category**: technical | operational | organizational | regulatory | financial
- **Probability**: low | medium | high
- **Impact**: low | medium | high | critical
- **Combined Severity**: <calculated from the two above>
- **Trigger / Early Warning Sign**: <what would indicate that the risk is materializing>
- **Mitigation**: <concrete actions>
- **Contingency Plan**: <if mitigation fails>
- **Owner**: <name / role>
- **Status**: open | mitigating | accepted | closed

<repeat for each risk>

## Summary by Severity

| Severity | Quantity | IDs |
|---|---|---|
| Critical | | |
| High | | |
| Medium | | |
| Low | | |

## Risks Related to the Target Paradigm

> Sub-section dedicated to scenarios where a paradigm shift occurs. List only risks whose direct origin is the gap recorded in `paradigm_decision.md`.

- <RISK-XXX: description>
```