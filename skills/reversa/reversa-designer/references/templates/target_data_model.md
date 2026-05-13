```
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: target_data_model
producedBy: designer
hash: "sha256:<hash of the body below the front-matter>"
---

# Target Data Model

> Data model for the new system. Schema, relationships, and constraints.

## Overview
<Short text: main database type, division by bounded context, roles (OLTP / OLAP / event store).>

## Data Entities

| Entity | Table / collection | Owner Aggregate | PK | Bounded context |
|---|---|---|---|---|
| <name> | <ref> | <AGG> | <field> | <BC> |

## Schema (DDL or equivalent)

```sql
-- Replace with the actual DDL of the target system.
CREATE TABLE pedidos (
    id UUID PRIMARY KEY,
    cliente_id UUID NOT NULL,
    status TEXT NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

## Relationships

| Source | Target | Cardinality | Integrity | Notes |
|---|---|---|---|---|
| pedidos.cliente_id | clientes.id | N:1 | FK ON DELETE RESTRICT | |

## Constraints

- **Uniqueness**: <list>
- **Referential integrity**: <enabled / disabled and why>
- **Partitioning / sharding** (if applicable): <description>
- **Critical indexes**: <list>

## Target Paradigm-Specific Considerations

> Section dedicated to when the target paradigm is event-driven, functional, or other with a direct implication on the data model.

- <e.g., event-driven → outbox table for at-least-once guarantee>
- <e.g., event sourcing → events store as the source of truth, derived projections>
- <e.g., immutability → immutable events / snapshots, no updates>

## Origin in Legacy System

| New Table / collection | Origin in legacy | Transformation |
|---|---|---|
| pedidos | `<legacy schema>.tb_pedidos` | renaming + normalized types |

## Notes
<Additional notes about the data model.>
```