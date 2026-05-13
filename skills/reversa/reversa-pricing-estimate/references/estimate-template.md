```markdown
# Price Estimation

**Feature:** `<feature_dir_relativa>`
**Generated on:** <created_at_local_legivel>
**Calculation Version:** Effort v<effort_formula_version>, Value v<value_formula_version>, Market v<market_table_version>

**Consumed Prerequisites:**
- Profile: `<output_folder>/_pricing/profile.json`
- Size: `<output_folder>/_pricing/<feature>/size.json` (complexity class `<complexity_class>`, auxiliary score `<size_score>`)

## Overview

| Scenario | Range | Comment |
|---|---|---|
| **Effort** | <esforco_str> | <horas_min> to <horas_max> h, cost + tax + markup |
| **Value** | <valor_str> | 10% to 30% of the declared annual value |
| **Market Range** | <mercado_str> | Hourly rate sourced by country and seniority |

## Effort Scenario

**What it is:** Price calculated from probable hours, hourly rate, approximate tax reserve, and project markup. It's the minimum defensible price to avoid subsidizing the client.

**When to use:** Always as a sanity check. Pricing below the Effort scenario means taking a loss or reducing the project's profit margin too much.

| Item | Value |
|---|---|
| Complexity class | <complexity_class> |
| Seniority | <seniority> |
| Seniority factor | <seniority_factor> |
| Estimated hours | <horas_min> to <horas_max> h |
| Midpoint | <horas_estimadas> h |
| Hourly rate | <hourly_rate> <currency>/h |
| Direct cost | <custo_direto_min> to <custo_direto_max> <currency> |
| Approximate tax reserve | <imposto_aproximado_min> to <imposto_aproximado_max> <currency> |
| Project markup (<margin_percent>%) | <markup_aplicado_min> to <markup_aplicado_max> <currency> |
| **Effort Range** | **<preco_minimo> to <preco_maximo> <currency>** |
| Midpoint | <preco_total> <currency> |

<aviso_vat_se_aplicavel>
<bloco_billing_currency_se_aplicavel>

## Value Scenario

**What it is:** Price based on a portion of the annual economic value that the feature generates or protects for the client. Reversa uses a capture rate of 10% to 30% of the declared annual value.

**When to use:** When the client can declare a return, savings, or the cost of not implementing the feature.

<se valor.available>

| Item | Value |
|---|---|
| Declared monthly return | <monthly_return_declared> <currency> |
| Users impacted | <users_impacted> |
| Cost of not doing | <cost_of_not_doing> <currency> |
| Annual value used | <annual_value> <currency> |
| Capture rate applied | 10% to 30% |
| Recommended price | <preco_recomendado> <currency> |
| **Value Range** | **<preco_minimo> to <preco_maximo> <currency>** |
| Approximate payback | <payback_str> |

<bloco_billing_currency_se_aplicavel>

<se NOT valor.available>

> **Value Scenario not available:** <razao_unavailable>

</se>

## Market Range Scenario

**What it is:** Range derived from benchmark hourly rates by country and seniority, multiplied by the same hour range as the Effort scenario.

**When to use:** As an external reference. Version 2 does not multiply by client profile because there is no reliable public dataset for this.

<se mercado.available>

| Item | Value |
|---|---|
| Country / Seniority | <country_nome> / <seniority> |
| Model / Client profile | <pricing_model> / <client_profile> |
| Complexity | <complexity_class> |
| Market hourly rate | <market_hourly_min> to <market_hourly_max> <currency>/h |
| Source type | <source_kind> |
| Reference year | <source_year> |
| Sources | <sources> |
| **Market Range** | **<preco_minimo_mercado> to <preco_maximo_mercado> <currency>** |

<se fallback aplicado>

> Fallback applied: <razao>

</se>

<bloco_billing_currency_se_aplicavel>

<se NOT mercado.available>

> **Market Scenario not available:** <razao_unavailable>

</se>

## How to choose between the three

<orientacao_pt_br_baseada_nos_cenarios>

General heuristic:

1. Client with no clear return: use Effort as the base and Market as an external reference.
2. Client with high and clear return: prefer Value, with Effort only as the minimum base.
3. Effort above Market: review profile, size, or client suitability.
4. Market above Effort: there is room to increase the markup or improve the proposal.

## Disclaimer

The numbers in this estimate are approximations for budgeting guidance, not a guarantee of a closed sale. The tax factor is an approximate reserve, not an exact legal rate. Actual tax validation is the responsibility of the user's accountant. The market range is static and based on the sources documented in `market-benchmarks.md`. The return declared by the client in the Value scenario is raw input, not validated. It is recommended to add `_reversa_sdd/_pricing/<feature>/estimate.{md,json}` to the `.gitignore` before committing.
```

## Billing currency

When `profile.billing_currency` is filled, each scenario receives an extra line:

```markdown
| In <billing_currency> | <valor_billing> <billing_currency> (exchange rate: 1 <billing_currency> = <exchange_rate_to_local> <currency>) |
```

## Short comments

| Scenario | Short comment |
|---|---|
| Effort | `<horas_min> to <horas_max> h, cost + tax + markup` |
| Value | `10% to 30% of the declared annual value` or `Not available` |
| Market | `hourly rate sourced by country and seniority` or `Not available` |
