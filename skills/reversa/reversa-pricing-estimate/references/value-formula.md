### SOURCE:
# Value Scenario Formula (value-formula.md)

**Formula Version:** 2.0

Documents the deterministic calculation that the `reversa-pricing-estimate` agent applies to the Value scenario. Version 2 of the formula replaces the fixed multiple of 6 to 12 months with a percentage capture of the declared annual economic value.

## Source and Criterion

Value-based pricing uses the perceived or economic value to the customer as the basis for pricing, not just internal cost or competitor pricing.

References:

- Hinterhuber, A. (2008), *Customer value-based pricing strategies: why companies resist*, Journal of Business Strategy, 29(4), DOI 10.1108/02756660810887079
- Nagle, Hogan, and Zale, *The Strategy and Tactics of Pricing*, 5th ed., Routledge, 2016, especially Economic Value to the Customer

The range of 10% to 30% is a commercial heuristic for Reversa in B2B/freelance/agency settings. It should be described as capturing a portion of the annual value, not as a universal academic law.

## Step 1: Input Validation

```
if monthly_return_declared == 0 AND cost_of_not_doing == 0:
  available = false
  explanation_pt_br = "The Value scenario cannot be calculated: the customer did not declare measurable return."
```

`users_impacted` is a business context. It appears in estimate.md, but it does not enter the numerical calculation in version 2.

## Step 2: Annual Economic Value

```
annual_value =
  max(monthly_return_declared * 12, cost_of_not_doing)
```

The customer may declare:

- recurring monthly return
- annual cost of not doing
- both

When both exist, the formula uses the highest defensible economic value.

## Step 3: Value Capture

```
value_capture_min = 0.10
value_capture_recommended = 0.20
value_capture_max = 0.30

preco_minimo = round_currency(annual_value * value_capture_min)
preco_recomendado = round_currency(annual_value * value_capture_recommended)
preco_maximo = round_currency(annual_value * value_capture_max)
```

## Step 4: Explanatory Payback

If `monthly_return_declared > 0`, calculate payback as a secondary explanation:

```
payback_months_min = preco_minimo / monthly_return_declared
payback_months_max = preco_maximo / monthly_return_declared
```

If `monthly_return_declared == 0`, set `payback_months_min = null` and `payback_months_max = null`.

Payback does not define the price. It only helps the user explain the proposal.

## Examples

### Example 1: Clear monthly return

```
monthly_return_declared = 2000 BRL
cost_of_not_doing = 5000 BRL

annual_value = max(2000 * 12, 5000) = 24000
preco_minimo = 24000 * 0.10 = 2400
preco_recomendado = 24000 * 0.20 = 4800
preco_maximo = 24000 * 0.30 = 7200
payback_months_min = 1.2
payback_months_max = 3.6
```

### Example 2: Prevention of annual loss

```
monthly_return_declared = 0
cost_of_not_doing = 60000 BRL

annual_value = max(0, 60000) = 60000
preco_minimo = 6000
preco_recomendado = 12000
preco_maximo = 18000
payback_months_min = null
payback_months_max = null
```

### Example 3: No measurable data

```
monthly_return_declared = 0
cost_of_not_doing = 0

available = false
```

## Conversion to Billing Currency

Identical to Effort. When `profile.billing_currency` is populated:

```
preco_minimo_billing = round_currency(preco_minimo / exchange_rate_to_local)
preco_recomendado_billing = round_currency(preco_recomendado / exchange_rate_to_local)
preco_maximo_billing = round_currency(preco_maximo / exchange_rate_to_local)
```

## Limits and Assumptions

1. The return declared by the customer is not validated by the agent.
2. The 10% to 30% capture range is a documented heuristic.
3. `users_impacted` does not enter the numerical calculation in version 2.
4. Extreme values are not truncated.
5. The explanation may mention payback months, but it should not state that the price is "6 to 12 months."