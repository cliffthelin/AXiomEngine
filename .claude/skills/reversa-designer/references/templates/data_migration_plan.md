```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: data_migration_plan
producedBy: designer
hash: "sha256:<hash of the body below the front-matter>"
---

# Data Migration Plan

> Plan for migrating data from the legacy system to the new system: mapping, transformations, ETL, data cutover, and validation.

## Summary
- Estimated volume: <rows / GB per primary entity>
- Migration window: <see `cutover_plan.md`>
- Strategy: pre-backfill + delta + cutover | single bulk | continuous replication

## Legacy → New Mapping

| Source | Destination | Type | Notes |
|---|---|---|---|
| `<legacy schema>.tb_pedidos` | `pedidos` | rename | type normalization |
| `<legacy schema>.tb_pedido_item` | `pedido_itens` | rename | adjusted FK |
| `<legacy schema>.usr_x` | `usuarios` (partial) + `perfis` | split | extracts profile data |

## Transformations

### Transformation T-01: <name>
- **Applies to**: <column or table>
- **Rule**: <explicit text>
- **Invalid data handling**: <discard | reject | fill with default>
- **Rule Origin**: <reference to `target_business_rules.md` or `discard_log.md`>

<repeat per transformation>

## ETL Strategy

- **Tool**: <e.g., SQL scripts, dbt, Airbyte, custom>
- **Flow**:
  1. <extraction>
  2. <transformation>
  3. <load>
- **Idempotency**: <how the ETL is safe for re-execution>
- **Expected throughput**: <e.g., 50k rows/s>

## Backfill and Delta

- **Backfill**: <initial date, scope, duration>
- **Delta Capture**:
  - **Mechanism**: CDC | log mining | timestamps | replication | trigger
  - **Acceptable latency**: <seconds>
- **Periodic Reconciliation**: <frequency, scope>

## Data Cutover

> Also see `cutover_plan.md`. This section focuses only on the data-specific aspects.

- **Window**: <ISO-8601>
- **Cutover sequence**:
  1. <step>
  2. <step>
- **Post-cutover verification**:
  - **Counts**: <which tables, tolerance>
  - **Checksums**: <critical columns>

## Quality Validation

| Metric | Target | Measurement Source |
|---|---|---|
| Count per entity | equal ± 0% | direct comparison |
| Sum of monetary values | equal ± 0.01% | financial reconciliation |
| Referential integrity | 0 orphans | audit scripts |

## Data-Specific Risks
- <RISK-XXX: see `risk_register.md`>

## Notes
<Additional notes.>
```