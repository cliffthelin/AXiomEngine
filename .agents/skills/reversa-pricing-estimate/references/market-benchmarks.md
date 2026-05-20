###
###
# Market Benchmarks (market-benchmarks.md)

**Table Version:** 2.0
**Benchmark Reference Date:** 2026-05

This document outlines the static references used by the `reversa-pricing-estimate` agent for the Market Range scenario. Version 2 removes the total ranges created through combination and now uses hourly benchmarks per country and seniority, deriving the total from the number of hours in the `effort-formula.md`.

## Mandatory Disclaimer

The figures presented are didactic approximations based on public and commercial sources available in May 2026. They should not be used as a substitute for updated, regionalized research. Many public sources provide monthly or annual salary data, not direct freelance rates. When a freelance rate is derived from a salary, the `source_kind` field must explicitly indicate this.

## How to Calculate the Market Scenario

Each line in the table contains the following information:

```
country | seniority | currency | min_hourly | max_hourly | source_kind | source_year | sources
```

The total cost per feature is derived as follows:

```
market_min = horas_min[complexity_class][seniority] * min_hourly
market_max = horas_max[complexity_class][seniority] * max_hourly
```

`pricing_model` only affects the presentation of the data:

- `time_and_materials`: displays the hourly rate and estimated total cost per hour.
- `fixed_scope`, `sprint`, `fixed_price_per_delivery`: displays the total cost per feature, calculated based on the estimated hours.
- `retainer`: displays the "equivalent range per feature within the retainer."

`client_profile` does not change the numerical values in version 2. Without a dataset per profile, introducing multipliers based on client type would be arbitrary. `estimate.md` can provide a qualitative alert indicating whether the client is a microenterprise, small business, or enterprise.

## Version 2 Table

| country | seniority | currency | min_hourly | max_hourly | source_kind | source_year | sources |
|---|---|---|---|---|---|---|---|
| BR | junior | BRL | 40 | 80 | salary_derived_freelance_estimate | 2025-2026 | Portal Salario CAGED, Glassdoor Brasil |
| BR | mid | BRL | 70 | 130 | salary_derived_freelance_estimate | 2025-2026 | Portal Salario CAGED, Glassdoor Brasil |
| BR | senior | BRL | 100 | 200 | salary_derived_freelance_estimate | 2025-2026 | Portal Salario CAGED, Glassdoor Brasil |
| BR | staff_lead | BRL | 160 | 300 | salary_derived_freelance_estimate | 2025-2026 | Portal Salario CAGED, Glassdoor Brasil |
| BR | principal | BRL | 220 | 420 | salary_derived_freelance_estimate | 2025-2026 | Portal Salario CAGED, Glassdoor Brasil |
| US | junior | USD | 20 | 40 | freelance_platform_and_public_wage | 2024-2025 | Upwork, O*NET/BLS |
| US | mid | USD | 40 | 70 | freelance_platform_and_public_wage | 2024-2025 | Upwork, O*NET/BLS |
| US | senior | USD | 70 | 150 | freelance_platform_and_public_wage | 2024-2025 | Upwork, O*NET/BLS |
| US | staff_lead | USD | 120 | 200 | freelance_platform_and_public_wage | 2024-2025 | Upwork, O*NET/BLS |
| US | principal | USD | 160 | 260 | freelance_platform_and_public_wage | 2024-2025 | Upwork, O*NET/BLS |
| PT | junior | EUR | 25 | 45 | salary_derived_contractor_estimate | 2024-2026 | Landing.Jobs, Hays Portugal |
| PT | mid | EUR | 40 | 70 | salary_derived_contractor_estimate | 2024-2026 | Landing.Jobs, Hays Portugal |
| PT | senior | EUR | 60 | 100 | salary_derived_contractor_estimate | 2024-2026 | Landing.Jobs, Hays Portugal |
| PT | staff_lead | EUR | 90 | 140 | salary_derived_contractor_estimate | 2024-2026 | Landing.Jobs, Hays Portugal |
| PT | principal | EUR | 120 | 180 | salary_derived_contractor_estimate | 2024-2026 | Landing.Jobs, Hays Portugal |
| MX | junior | MXN | 200 | 400 | salary_derived_freelance_estimate | 2025 | Glassdoor Mexico, Computrabajo Mexico |
| MX | mid | MXN | 350 | 650 | salary_derived_freelance_estimate | 2025 | Glassdoor Mexico, Computrabajo Mexico |
| MX | senior | MXN | 600 | 1000 | salary_derived_freelance_estimate | 2025 | Glassdoor Mexico, Computrabajo Mexico |
| MX | staff_lead | MXN | 900 | 1500 | salary_derived_freelance_estimate | 2025 | Glassdoor Mexico, Computrabajo Mexico |
| MX | principal | MXN | 1200 | 2000 | salary_derived_freelance_estimate | 2025 | Glassdoor Mexico, Computrabajo Mexico |

## Seniority Aliases

```
pleno -> mid
especialista -> staff_lead
staff -> staff_lead
lead -> staff_lead
```

## Sources

- Portal Salario, Information Systems Programmer, CBO 317110, CAGED/eSocial/Employer Web data, updated in 2026: https://www.salario.com.br/profissao/programador-de-sistemas-de-informacao-cbo-317110/
- Glassdoor Brasil, Software Developer, monthly range, updated in 2025: https://www.glassdoor.com/Salaries/br%C3%A9sil-software-developer-salary-SRCH_IL.0%2C6_IN36_KO7%2C25.htm
- O*NET Online, Software Developers 15-1252.00, local salaries with BLS source 2024: https://www.onetonline.org/link/localwages/15-1252.00
- Upwork, Software Developer hourly cost guide, entry, intermediate, and expert ranges: https://www.upwork.com/hire/software-developers/cost/
- Landing.Jobs Global Tech Talent Trends 2024: https://campaign.landing.jobs/gttt-2024
- Hays Portugal Salary Guide 2026: https://www.hays.pt/en/salary-guide/overview
- Glassdoor Mexico, Software Developer, monthly range, updated in 2025: https://www.glassdoor.com/Salaries/mexico-software-developer-salary-SRCH_IL.0%2C6_IN169_KO7%2C25.htm
- Computrabajo Mexico, salaries for Developer and IT Developer, updated in 2025: https://mx.computrabajo.com/salarios/desarrollador-it

## Fallback Rules

1.  If `country` is not in the table, the Market scenario becomes `unavailable: true`.
2.  If `seniority` is provided in an alias, normalize it and calculate.
3.  If `pricing_model` is not among the known models, use the presentation of `fixed_scope` and log the fallback.
4.  `client_profile` does not change the price in version 2.
5.  `complexity_class` should always exist within the size parameters; if absent, the process should fail with a message instructing the user to recalculate in the Sizer.

## Countries Not Covered in v2

For `country` values other than `[BR, US, PT, MX]`, the Market scenario becomes unavailable, displaying the following explanation:

"Market range for `<country>` is not yet documented in this version of Reversa. Covered in v2: BR, US, PT, MX."

## How to Extend

To add a country:

1.  Prioritize using a public source of direct freelance rates.
2.  If using salary data, specify `source_kind = salary_derived_freelance_estimate`.
3.  Cite the source and year for each data point.
4.  Avoid adding multipliers for `client_profile` unless there is supporting data.
5.  Update the `formula_version` in the `market` calculation.