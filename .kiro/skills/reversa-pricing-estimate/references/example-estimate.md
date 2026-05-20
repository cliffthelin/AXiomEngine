### SOURCE:
### SOURCE:
# Price Estimate

**Feature:** `_reversa_sdd/forward/042-pagamento-pix`
**Generated on:** 2026-05-06 16:42 UTC
**Calculation Version:** Effort v2.0, Value v2.0, Market v2.0

**Consumed Prerequisites:**
- Profile: `_reversa_sdd/_pricing/profile.json`
- Size: `_reversa_sdd/_pricing/042-pagamento-pix/size.json` (class `L`, auxiliary score `60`)

## Overview

| Scenario | Range | Comment |
|---|---|---|
| **Effort** | 4,800.00 to 12,000.00 BRL | 32 to 80h, cost + tax + markup |
| **Value** | 2,400.00 to 7,200.00 BRL | 10% to 30% of the declared annual value |
| **Market Range** | 3,200.00 to 16,000.00 BRL | hourly rate sourced by country and seniority |

## Effort Scenario

**What it is:** Price calculated based on likely hours, hourly rate, approximate tax reserve, and project markup. It is the defensible lower limit to avoid subsidizing the client.

**When to use:** Always as a sanity check. Charging below the Effort means accepting a loss or reducing the project profit too much.

| Item | Value |
|---|---|
| Complexity Class | L |
| Seniority | senior |
| Seniority Factor | 1.00 |
| Estimated Hours | 32 to 80 h |
| Midpoint | 56 h |
| Hourly Rate | 100.00 BRL/h |
| Direct Cost | 3,200.00 to 8,000.00 BRL |
| Approximate Tax Reserve | 480.00 to 1,200.00 BRL |
| Project Markup (35%) | 1,120.00 to 2,800.00 BRL |
| **Effort Range** | **4,800.00 to 12,000.00 BRL** |
| Midpoint | 8,400.00 BRL |

Note: part of the tax factor may be a highlighted tax and passed on to the client. Validate with an accountant.

## Value Scenario

**What it is:** Price based on a portion of the annual economic value that the feature generates or protects for the client. Reversa uses a 10% to 30% capture of the declared annual value.

**When to use:** When the client can declare a return, saving, or cost of not implementing it.

| Item | Value |
|---|---|
| Declared Monthly Return | 2,000.00 BRL |
| Users Impacted | 500 |
| Cost of Not Implementing | 5,000.00 BRL |
| Annual Value Used | 24,000.00 BRL |
| Capture Applied | 10% to 30% |
| Recommended Price | 4,800.00 BRL |
| **Value Range** | **2,400.00 to 7,200.00 BRL** |
| Approximate Payback | 1.2 to 3.6 months |

## Market Range Scenario

**What it is:** Range derived from hourly benchmarking by country and seniority, multiplied by the same hour range as the Effort scenario.

**When to use:** As external reference. v2 does not multiply by client profile because there is no reliable public dataset for this.

| Item | Value |
|---|---|
| Country / Seniority | Brazil / senior |
| Model / Client Profile | closed_scope / small_business |
| Complexity | L |
| Market Hourly Rate | 100.00 to 200.00 BRL/h |
| Source Type | salary_derived_freelance_estimate |
| Reference Year | 2025-2026 |
| Sources | Portal Salario CAGED, Glassdoor Brazil |
| **Market Range** | **3,200.00 to 16,000.00 BRL** |

## How to choose between the three

The declared Value generates a smaller range than the average Effort. Use Effort as a defensible lower limit and Market as external reference. For this client, only charge below 4,800 BRL if there is a clear strategic reason.

General Heuristic:

1. Client with no clear return: use Effort as the lower limit and Market as external reference.
2. Client with high and clear return: prefer Value, with Effort only as the minimum lower limit.
3. Effort above Market: review profile, size, or client suitability.
4. Market above Effort: there is room to increase markup or improve the proposal.

## Disclaimer

The numbers in this estimate are approximations for budget guidance, not a guarantee of closing the sale. The tax factor is an approximate reserve, not an exact legal rate. Actual tax validation is the responsibility of the user's accountant. The market range is static and based on the sources documented in `market-benchmarks.md`. The return declared by the client in the Value scenario is raw input, not validated. It is recommended to add `_reversa_sdd/_pricing/<feature>/estimate.{md,json}` to the `.gitignore` before committing.
