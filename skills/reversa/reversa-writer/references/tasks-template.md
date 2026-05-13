### SOURCE:
# [Unit Name], Implementation Tasks

> This is a template for the `tasks.md` file. It focuses on a sequence of executable tasks to reimplement the unit from the legacy code, with traceability to the original code.

## Prerequisites
- [ ] Dependencies for the unit, listed in `design.md`, are available.
- [ ] Database schema/migrations are compatible (if applicable).
- [ ] Necessary environment variables/configurations are documented.

## Tasks

> Each task references the legacy file from which the behavior was extracted.

- [ ] T-01, [Task Description]
  - Origin in legacy code: `path/file.ext:line`
  - Completion criterion: [how to validate]
  - Confidence: 🟢 / 🟡 / 🔴

- [ ] T-02, [Task Description]
  - Origin in legacy code: `path/file.ext:line`
  - Completion criterion: [how to validate]
  - Confidence: 🟢 / 🟡 / 🔴

## Testing Tasks
- [ ] TT-01, Test the happy path of the main flow (see `requirements.md`, Acceptance Criteria)
- [ ] TT-02, Test the main error case
- [ ] TT-03, [Other relevant scenarios]

## Data Migration Tasks (if applicable)
- [ ] TM-01, [Data migration X, with reference to the legacy schema]

## Suggested Order
1. [Which tasks should be done first and why]
2. [Dependencies between tasks]

## Pending Gaps (🔴)
[List here the decisions that depend on human validation before implementation]
