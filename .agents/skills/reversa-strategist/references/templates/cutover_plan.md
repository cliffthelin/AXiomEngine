```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: cutover_plan
producedBy: strategist
hash: "sha256:<hash of the body below the front-matter>"
---

# Cutover Plan

> Plan to transition from the legacy system to the new system, aligned with the strategy chosen in `migration_strategy.md`.

## Baseline Strategy
- **Confirmed Strategy**: <reference to migration_strategy.md>

## Prerequisites
- [ ] <prerequisite 1: e.g., behavioral parity ≥ X% for N days>
- [ ] <prerequisite 2>
- [ ] <prerequisite 3>

## Cutover Window
- **Target Date**: <ISO-8601 or timeframe>
- **Estimated Duration**: <hours>
- **Affected Environment**: <production / staging / other>
- **Prior Communication**: <stakeholders notified, timeline>

## Cutover Steps

| # | Step | Owner | Duration | Reversible? |
|---|---|---|---|---|
| 1 | <e.g., freeze writes to legacy system> | | | |
| 2 | <e.g., final ETL of data> | | | |
| 3 | <e.g., DNS routing update> | | | |
| 4 | <e.g., smoke tests on the new system> | | | |

## Rollback Plan
- **Trigger Criteria**: <when rollback is decided>
- **Steps**:
  1. <step>
  2. <step>
- **Maximum Acceptable Time Until Rollback**: <minutes / hours>
- **Rollback Owner**: <name / role>

## Go / No-Go Criteria
- **Go**:
  - <criterion 1>
  - <criterion 2>
- **No-go**:
  - <criterion 1>
  - <criterion 2>

## Post-Cutover
- [ ] Extended monitoring for <period>
- [ ] Parity validation according to `parity_specs.md`
- [ ] Decommission legacy system on <date>

## Notes
<Additional observations.>
```