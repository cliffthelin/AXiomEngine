```markdown
# Billing Profile

**Created on:** 2026-05-06 14:32 UTC
**Schema version:** 1.1

## Identification

| Field | Value |
|---|---|
| Country | Brazil (BR) |
| Local currency | Brazilian Real (BRL) |
| Seniority | senior |

## Direct Cost

| Field | Value |
|---|---|
| Hourly rate mode | Derived |
| Desired net monthly income | 12,000.00 BRL |
| Billable hours per month | 120 |
| Calculated hourly rate | 100.00 BRL/h |

## Markup and Taxes

| Field | Value |
|---|---|
| Project markup | 35% |
| Tax regime | Simplified National Tax System, IT services |
| Approximate factor | 15% |
| Factor type | effective_reserve_estimate |
| Factor source | Federal Revenue, Simplified National Tax System, annexes and factor R |
| Includes highlighted tax | Yes |
| Pass-through notice | Yes |
| Confidence in regime | High, explicit choice |

## Business Model

| Field | Value |
|---|---|
| Billing models | fixed_scope, time_and_materials |
| Customer profile | small_business |
| Billing in foreign currency | No |

## Disclaimer

The registered tax factor is an approximate reserve for budgeting, not an exact legal rate. Actual tax validation is the responsibility of the user's accountant. This file contains sensitive financial data. It is recommended to add `_reversa_sdd/_pricing/profile.json` and `_reversa_sdd/_pricing/profile.md` to `.gitignore` before committing.
```