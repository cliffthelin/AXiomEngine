### SOURCE:
### SOURCE:
# \[Unit Name], Implementation Tasks

> Template for the `tasks.md` file. Focuses on a sequence of executable tasks for reimplementing the unit from the legacy code, with traceability to the original code.

## Prerequisites
- \[ ] Unit dependencies listed in `design.md` are available
- \[ ] Compatible schema/migrations for the database (if applicable)
- \[ ] Required environment variables / configurations are documented

## Tasks

> Each task references the legacy file from which the behavior was extracted.

- \[ ] T-01, \[Task Description]
  - Origin in legacy code: `path/file.ext:line`
  - Completion criterion: \[how to validate]
  - Confidence: 🟢 / 🟡 / 🔴

- \[ ] T-02, \[Task Description]
  - Origin in legacy code: `path/file.ext:line`
  - Completion criterion: \[how to validate]
  - Confidence: 🟢 / 🟡 / 🔴

## Test Tasks

- \[ ] TT-01, Test of the happy path of the main flow (see `requirements.md`, Acceptance Criteria)
- \[ ] TT-02, Test of the main error case
- \[ ] TT-03, \[Other relevant scenarios]

## Data Migration Tasks (if applicable)

- \[ ] TM-01, \[Data migration X, with reference to the legacy schema]

## Suggested Order
1. \[Which tasks should be done first and why]
2. \[Dependencies between tasks]

## Pending Gaps (🔴)
\[List here the decisions that depend on human validation before implementation]
