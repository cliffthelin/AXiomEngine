# Price Estimate

**Feature:** `_reversa_sdd/forward/042-pagamento-pix`
**Generated on:** 2026-05-06 16:42 UTC
**Calculation Version:** Effort v2.0, Value v2.0, Market v2.0

**Consumed Prerequisites:**
- Profile: `_reversa_sdd/_pricing/profile.json`
- Size: `_reversa_sdd/_pricing/042-pagamento-pix/size.json` (complexity class `L`, auxiliary score `60`)

## Overview

| Scenario | Range | Comment |
|---|---|---|
| **Effort** | 4,800.00 to 12,000.00 BRL | 32 to 80h, cost + tax + markup |
| **Value** | 2,400.00 to 7,200.00 BRL | 10% to 30% of the declared annual value |
| **Market Range** | 3,200.00 to 16,000.00 BRL | hourly rate sourced by country and seniority |

## Effort Scenario

**What it is:** price calculated from probable hours, hourly rate, approximate tax reserve, and project markup. It represents the lowest defendable price to avoid subsidizing the client.

**When to use:** always as a sanity check. Quoting below the Effort level means taking a loss or significantly reducing the project's profit.

| Item | Value |
|---|---|
| Complexity class | L |
| Seniority | senior |
| Seniority factor | 1.00 |
| Estimated hours | 32 to 80 h |
| Midpoint | 56 h |
| Hourly rate | 100.00 BRL/h |
| Direct cost | 3,200.00 to 8,000.00 BRL |
| Approximate tax reserve | 480.00 to 1,200.00 BRL |
| Project markup (35%) | 1,120.00 to 2,800.00 BRL |
| **Effort Range** | **4,800.00 to 12,000.00 BRL** |
| Midpoint | 8,400.00 BRL |

Warning: part of the tax factor may be highlighted as tax and passed on to the client. Validate with an accountant.

## Value Scenario

**What it is:** price based on a portion of the annual economic value that the feature generates or protects for the client. Reversa uses a capture rate of 10% to 30% of the declared annual value.

**When to use:** when the client can declare a return, savings, or cost of not implementing the feature.

| Item | Value |
|---|---|
| Declared monthly return | 2,000.00 BRL |
| Users impacted | 500 |
| Cost of not implementing | 5,000.00 BRL |
| Annual value used | 24,000.00 BRL |
| Applied capture rate | 10% to 30% |
| Recommended price | 4,800.00 BRL |
| **Value Range** | **2,400.00 to 7,200.00 BRL** |
| Approximate Payback | 1.2 to 3.6 months |

## Market Range Scenario

**What it is:** range derived from hourly benchmarking by country and seniority, multiplied by the same hour range as the Effort scenario.

**When to use:** as external reference. V2 does not multiply by client profile because there is no reliable public dataset for this.

| Item | Value |
|---|---|
| Country / Seniority | Brazil / senior |
| Model / Client profile | fixed_scope / small_business |
| Complexity | L |
| Market hourly rate | 100.00 to 200.00 BRL/h |
| Source type | salary_derived_freelance_estimate |
| Reference year | 2025-2026 |
| Sources | Portal Salario CAGED, Glassdoor Brazil |
| **Market Range** | **3,200.00 to 16,000.00 BRL** |

## How to Choose Between the Three

The declared Value generates a smaller range than the average Effort. Use Effort as the lowest defensible price and Market as an external reference. For this client, only quote below 4,800 BRL if there is a clear strategic reason.

General heuristic:

1.  Client without a clear return: use Effort as the minimum and Market as an external reference
2.  Client with a high and clear return: prefer Value, with Effort only as a minimum
3.  Effort above Market: review profile, size, or client suitability
4.  Market above Effort: there is room to increase the markup or improve the proposal

## Disclaimer

The numbers in this estimate are approximations for budget guidance, not a guarantee of a closed sale. The tax factor is an approximate reserve, not an exact legal rate. Actual tax validation is the responsibility of the user's accountant. The market range is static and based on the sources documented in `market-benchmarks.md`. The value declared by the client in the Value scenario is a raw input, not validated. It is recommended to add `_reversa_sdd/_pricing/<feature>/estimate.{md,json}` to the `.gitignore` before committing.
