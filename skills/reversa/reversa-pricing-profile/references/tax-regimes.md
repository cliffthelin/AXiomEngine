### SOURCE:
# Tax Regime Catalog

An extensible catalog used by the `reversa-pricing-profile` agent to map the tax regime declared by the user to an approximate `tax_factor`. The factors are didactic reserves for budgeting, not exact legal rates.

## How to Read This File

Each regime has:

- `key`: canonical key stored in `profile.json`
- `country`: ISO 3166-1 alpha-2 code or `INTL`
- `name_pt_br`: user-friendly name used in the chat
- `tax_factor`: approximate factor applied to direct costs
- `tax_factor_kind`: `effective_reserve_estimate`, `statutory_proxy`, or `not_computed`
- `includes_vat`: whether it combines income tax/contribution with VAT/IVA/ISS
- `vat_pass_through_warning`: whether the estimate should warn that part of the tax may be passed on to the client
- `tax_factor_source`: public source or base description
- `notes_pt_br`: short note for the user

## Mandatory Disclaimer

The factors listed here are didactic approximations based on publicly known references from 2026-05. They do not replace accounting advice. Accuracy depends on deductibles, municipality, revenue range, CNAE, classification, withholding taxes, international treaties, and the rules in effect at the time of invoice issuance.

The agent must repeat the disclaimer during the interview and in the footer of the `profile.md`.

## Brazil (BR)

| key | name_pt_br | tax_factor | tax_factor_kind | includes_vat | vat_pass_through_warning | tax_factor_source | notes_pt_br |
|---|---|---:|---|---|---|---|---|
| MEI | Individual Micro-Entrepreneur (MEI) | 0.06 | effective_reserve_estimate | true | true | Portal do Empreendedor and public rules of DAS-MEI | Simplified reserve. MEI usually has a fixed DAS and a revenue limit. Software activity may require validation of eligibility. |
| simples_servicos | Simplified National Regime, IT services | 0.15 | effective_reserve_estimate | true | true | Federal Revenue Service, Simplified National Regime, annexes, and R factor | Average reserve. The actual rate depends on the annex, RBT12, R factor, ISS, and withholding taxes. |
| lucro_presumido | Presumed Profit Regime, services | 0.165 | effective_reserve_estimate | true | true | Federal Revenue Service, IRPJ, CSLL, PIS, COFINS, and ISS | Combined reserve for services. Validate municipal ISS and withholding taxes. |
| autonomo_pf | Self-employed individual, carnê-leão | 0.275 | effective_reserve_estimate | false | false | Federal Revenue Service, progressive IRPF and INSS | Reserve for senior professionals. Effective rate varies by deductions and social security contributions. |

## United States (US)

| key | name_pt_br | tax_factor | tax_factor_kind | includes_vat | vat_pass_through_warning | tax_factor_source | notes_pt_br |
|---|---|---:|---|---|---|---|---|
| self_employed_1099 | Self-Employed, 1099, sole proprietor | 0.30 | effective_reserve_estimate | false | false | IRS, self-employment tax and federal income tax | Combined reserve. Does not include state tax or specific deductions. |
| s_corp_llc | S-Corp or LLC with S-Corp election | 0.22 | effective_reserve_estimate | false | false | IRS, payroll tax, reasonable salary and distributions | Simplified reserve. Requires an accountant for reasonable salary and distributions. |

## Portugal (PT)

| key | name_pt_br | tax_factor | tax_factor_kind | includes_vat | vat_pass_through_warning | tax_factor_source | notes_pt_br |
|---|---|---:|---|---|---|---|---|
| pt_simplificado | Category B, simplified regime | 0.21 | effective_reserve_estimate | true | true | Tax Authority, IRS Category B, VAT, and Social Security | Combined reserve. VAT can be itemized and passed on to the client. |
| pt_organizada | Category B, organized accounting | 0.18 | effective_reserve_estimate | true | true | Tax Authority, organized accounting | Simplified reserve. Actual costs can reduce the tax base. |

## Mexico (MX)

| key | name_pt_br | tax_factor | tax_factor_kind | includes_vat | vat_pass_through_warning | tax_factor_source | notes_pt_br |
|---|---|---:|---|---|---|---|---|
| mx_resico | Simplified Trust Regime (RESICO) | 0.10 | effective_reserve_estimate | true | true | SAT, RESICO Individual and VAT | Combined reserve. ISR can be low, but VAT may apply as appropriate. |
| mx_actividad_empresarial | Business and Professional Activity (Individual) | 0.20 | effective_reserve_estimate | true | true | SAT, progressive ISR and VAT | Simplified reserve for independent professionals. |

## International (INTL)

| key | name_pt_br | tax_factor | tax_factor_kind | includes_vat | vat_pass_through_warning | tax_factor_source | notes_pt_br |
|---|---|---:|---|---|---|---|---|
| intl_freelance_no_withhold | International freelance, client with no withholding | 0.00 | not_computed | false | false | Depends on the provider's country | Client pays in full. Use the provider's national regime for actual tax. |
| intl_freelance_with_withhold | International freelance, client with withholding | 0.15 | effective_reserve_estimate | false | false | Bilateral treaties and local rules | Actual withholding depends on the treaty and the client's country. |

## Other

| key | name_pt_br | tax_factor | tax_factor_kind | includes_vat | vat_pass_through_warning | tax_factor_source | notes_pt_br |
|---|---|---:|---|---|---|---|---|
| outro | Other regime, not listed | 0.00 | not_computed | false | false | User reported a non-cataloged regime | Tax not computed. Estimate should warn that the calculation is the responsibility of the accountant. |

## Essential Regimes for Future Regions

Do not enable these countries as supported in the Market scenario without cataloging minimum regimes:

| country | essential regimes |
|---|---|
| GB | sole_trader_self_assessment, limited_company |
| DE | freiberufler, gewerbe_einzelunternehmen, gmbh |
| ES | autonomo_estimacion_directa_simplificada, autonomo_estimacion_directa_normal, sociedad_limitada |
| AR | monotributo, responsable_inscripto |
| CO | regimen_simple, regimen_ordinario_persona_natural, sociedad |

Verified official sources:

- UK GOV.UK, sole trader and limited company: https://www.gov.uk/set-up-business/sole-trader.html
- Germany, federal administrative portal, fiscal registration: https://verwaltung.bund.de/leistungsverzeichnis/EN/leistung/99102019120000/herausgeber/HH-S1000020010000009790/region/020000000000
- Spain, Tax Agency, income determination regimes: https://sede.agenciatributaria.gob.es/Sede/irpf/empresarios-individuales-profesionales/regimenes-determinar-rendimiento-actividad.html
- Argentina ARCA, Monotributo: https://www.afip.gob.ar/monotributo/
- Colombia DIAN, Simplified Tax Regime: https://micrositios.dian.gov.co/regimen-simple-tributacion/

## Suggested Default Regime per Country

When the user answers "I don't know," the agent suggests the following default and sets `tax_regime_confidence = "low"`:

| country | suggested default regime |
|---|---|
| BR | simples_servicos |
| US | self_employed_1099 |
| PT | pt_simplificado |
| MX | mx_resico |
| Other country | no suggestion, request explicit choice |

## How to Extend

1. Add the country section with the same table
2. Cite a public source
3. Indicate whether the factor includes VAT, IVA, or itemized tax
4. Do not call `tax_factor` a legal rate
5. Update the schema if new fields are needed
