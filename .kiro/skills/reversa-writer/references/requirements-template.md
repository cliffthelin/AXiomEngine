```markdown
# [Unit Name]

> Template for the `requirements.md` file. Focuses on WHAT the unit does, not HOW.

## Overview
[What it is, what problem it solves, 2-3 lines]

## Responsibilities
- [Responsibility 1]
- [Responsibility 2]

## Business Rules
- [Rule 1] 🟢
- [Rule 2] 🟡
- [Unknown behavior] 🔴

## Functional Requirements

| ID    | Requirement | Priority | Acceptance Criteria |
|-------|-------------|----------|----------------------|
| RF-01 | [Description] | Must     | [How to validate]    |
| RF-02 | [Description] | Should   | [How to validate]    |

## Non-Functional Requirements

| Type          | Inferred Requirement              | Evidence in Code        | Confidence |
|---------------|-----------------------------------|-------------------------|------------|
| Performance   | [e.g., 30s timeout on external calls] | `path/file.ext:line`     | 🟢         |
| Security      | [e.g., mandatory authentication on route] | `path/file.ext:line`     | 🟡         |
| Scalability   | [e.g., use of Redis cache]      | `path/file.ext:line`     | 🟢         |
| Availability  | [e.g., automatic retry on failure]   | `path/file.ext:line`     | 🟡         |

> Inferred from the code. Validate with the operations team.

## Acceptance Criteria

```gherkin
Given [pre-condition]
When [action]
Then [expected result]

Given [error condition]
When [invalid action]
Then [expected failure behavior]
```

## Priority (MoSCoW)

| Requirement              | MoSCoW | Justification                      |
|--------------------------|--------|-------------------------------------|
| [Core responsibility]    | Must   | Critical path, called in every flow |
| [Central business rule] | Must   | Business rule without fallback      |
| [Secondary functionality] | Should | Important but with an alternative   |
| [Edge case]             | Could  | Rarely triggered                   |

> Priority inferred by call frequency and position in the dependency chain.

## Code Traceability

| File                  | Function / Class | Coverage |
|-----------------------|------------------|----------|
| `path/file.ext`        | `ClassName`       | 🟢        |
```