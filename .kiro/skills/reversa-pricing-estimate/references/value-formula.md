```markdown
# Value Scenario Formula (value-formula.md)

**Formula Version:** 2.0

This document details the deterministic calculation that the `reversa-pricing-estimate` agent applies to the Value scenario. Version 2 of the formula replaces the fixed multiple of 6 to 12 months with a percentage capture of the declared annual economic value.

## Source and Criteria

Value-based pricing uses the perceived or economic value to the customer as the basis for price, not just internal cost or competitor pricing.

References:

- Hinterhuber, A. (2008), *Customer value-based pricing strategies: why companies resist*, Journal of Business Strategy, 29(4), DOI 10.1108/02756660810887079
- Nagle, Hogan, and Zale, *The Strategy and Tactics of Pricing*, 5th ed., Routledge, 2016, especially Economic Value to the Customer

The range of 10% to 30% is a commercial heuristic for Reversa for B2B/freelance/agency. It should be described as capturing a portion of the annual value, not as a universal academic law.

## Step 1: Input Validation

```
if monthly_return_declared == 0 AND cost_of_not_doing == 0:
  available = false
  explanation_pt_br = "The Value scenario cannot be calculated: the client has not declared measurable return."
```

`users_impacted` is business context. It appears in estimate.md but does not enter the numerical v2 calculation.

## Step 2: Annual Economic Value

```
annual_value =
  max(monthly_return_declared * 12, cost_of_not_doing)
```

The client may declare:

- recurring monthly return
- annual cost of not doing
- both

When both exist, the formula uses the highest defensible economic value.

## Step 3: Value Capture

```
value_capture_min = 0.10
value_capture_recommended = 0.20
value_capture_max = 0.30

price_min = round_currency(annual_value * value_capture_min)
price_recommended = round_currency(annual_value * value_capture_recommended)
price_max = round_currency(annual_value * value_capture_max)
```

## Step 4: Explanatory Payback

If `monthly_return_declared > 0`, calculate payback as a secondary explanation:

```
payback_months_min = price_min / monthly_return_declared
payback_months_max = price_max / monthly_return_declared
```

If `monthly_return_declared == 0`, set `payback_months_min = null` and `payback_months_max = null`.

Payback does not define the price. It only helps the user explain the proposal.

## Examples

### Example 1: Clear Monthly Return

```
monthly_return_declared = 2000 BRL
cost_of_not_doing = 5000 BRL

annual_value = max(2000 * 12, 5000) = 24000
price_min = 24000 * 0.10 = 2400
price_recommended = 24000 * 0.20 = 4800
price_max = 24000 * 0.30 = 7200
payback_months_min = 1.2
payback_months_max = 3.6
```

### Example 2: Preventing Annual Loss

```
monthly_return_declared = 0
cost_of_not_doing = 60000 BRL

annual_value = max(0, 60000) = 60000
price_min = 6000
price_recommended = 12000
price_max = 18000
payback_months_min = null
payback_months_max = null
```

### Example 3: No Measurable Data

```
monthly_return_declared = 0
cost_of_not_doing = 0

available = false
```

## Conversion to Billing Currency

Identical to Effort. When `profile.billing_currency` is filled in:

```
price_min_billing = round_currency(price_min / exchange_rate_to_local)
price_recommended_billing = round_currency(price_recommended / exchange_rate_to_local)
price_max_billing = round_currency(price_max / exchange_rate_to_local)
```

## Limitations and Assumptions

1. The return declared by the client is not validated by the agent.
2. The 10% to 30% capture range is a documented heuristic.
3. `users_impacted` does not enter the numerical v2 calculation.
4. Extreme values are not truncated.
5. The explanation may mention payback months, but it must not state that the price is "6 to 12 months."
```