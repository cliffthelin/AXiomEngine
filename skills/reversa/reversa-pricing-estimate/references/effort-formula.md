# Effort Scenario Formula (effort-formula.md)

**Formula Version:** 2.0

Documents the deterministic calculation that the `reversa-pricing-estimate` agent applies to the Effort scenario. Version 2 removes the old linear score-to-hours conversion and uses hourly ranges per T-shirt size, with a seniority factor inspired by the COCOMO II personnel capacity multipliers.

## Source and Criteria

COCOMO II is a parametric effort estimation model that uses size, product attributes, platform, personnel, and project characteristics. For Reversa's UX, using the complete model would be too complex. Version 2 only uses the defensible idea of personnel capacity multipliers, while maintaining simple hourly ranges per class.

Main reference:

- Barry Boehm et al., *Software Cost Estimation with COCOMO II*, Prentice Hall, 2000
- Carnegie Mellon SEI, overview of software cost estimation and COCOMO II: https://insights.sei.cmu.edu/blog/software-cost-estimation-explained/

## Step 1: Base hourly range for senior

```
hours_by_complexity_class_senior:
  S:   4 to 12 hours
  M:   12 to 32 hours
  L:   32 to 80 hours
  XL:  80 to 160 hours
  XXL: 160 to 320 hours, with mandatory recommendation to break down scope
```

These ranges are Reversa's heuristic, based on T-shirt sizing. They are more honest than a linear constant because software estimation has real uncertainty.

## Step 2: Seniority factor

```
seniority_factor:
  junior:      1.34
  mid:         1.15
  senior:      1.00
  staff_lead:  0.88
  principal:   0.76
```

Allowed aliases for compatibility:

```
pleno -> mid
especialista -> staff_lead
staff -> staff_lead
lead -> staff_lead
```

## Step 3: Estimated hours

```
horas_min = round(hours_min[complexity_class] * seniority_factor)
horas_max = round(hours_max[complexity_class] * seniority_factor)
horas_estimadas = round((horas_min + horas_max) / 2)
```

The `horas_estimadas` field is the midpoint for compatibility and summarization. The range `horas_min` to `horas_max` should be displayed in the estimate.md.

## Step 4: Direct cost

```
custo_direto_min = horas_min * profile.hourly_rate
custo_direto_max = horas_max * profile.hourly_rate
custo_direto = horas_estimadas * profile.hourly_rate
```

## Step 5: Approximate tax

```
imposto_aproximado_min = custo_direto_min * profile.tax_factor
imposto_aproximado_max = custo_direto_max * profile.tax_factor
imposto_aproximado = custo_direto * profile.tax_factor
```

When `profile.tax_regime == "outro"` or `tax_factor = 0`, the tax is not calculated and the estimate.md should display an explicit warning.

If the profile indicates that the factor includes VAT, GST, or tax itemized on the invoice, the estimate.md should warn that this value may be passed on to the client and does not necessarily reduce margin.

## Step 6: Project markup

The historical `margin_percent` field should be treated as **project markup over direct cost**, not as accounting net profit.

```
markup_min = custo_direto_min * (profile.margin_percent / 100)
markup_max = custo_direto_max * (profile.margin_percent / 100)
markup_aplicado = custo_direto * (profile.margin_percent / 100)
```

## Step 7: Total price

```
preco_minimo = round_currency(custo_direto_min + imposto_aproximado_min + markup_min)
preco_maximo = round_currency(custo_direto_max + imposto_aproximado_max + markup_max)
preco_total = round_currency(custo_direto + imposto_aproximado + markup_aplicado)
```

`preco_total` is the midpoint of the range and exists for compatibility. The estimate.md should highlight `preco_minimo` to `preco_maximo`.

## Example

```
profile:
  country = BR, currency = BRL, seniority = senior
  hourly_rate = 100.00, margin_percent = 35, tax_factor = 0.15

size:
  complexity_class = L

hours_by_complexity_class_senior[L] = 32 to 80
seniority_factor[senior] = 1.00
horas_min = 32
horas_max = 80
horas_estimadas = 56

custo_direto_min = 3200.00
custo_direto_max = 8000.00
imposto_min = 480.00
imposto_max = 1200.00
markup_min = 1120.00
markup_max = 2800.00

preco_minimo = 4800.00 BRL
preco_maximo = 12000.00 BRL
preco_total = 8400.00 BRL
```

## Conversion to billing currency

When `profile.billing_currency` and `profile.exchange_rate_to_local` are provided:

```
valor_billing = round_currency(valor_local / exchange_rate_to_local)
```

The estimate.md should print the rate used:

```
1 <billing_currency> = <exchange_rate_to_local> <currency>
```

## Limitations

1. The formula does not mix team seniorities.
2. XXL is still calculable, but should generate a strong recommendation to break down scope.
3. The hourly range is a heuristic, not a delivery promise.
4. `size_score` does not enter into the hours calculation.
