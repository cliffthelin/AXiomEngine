```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: target_domain_model
producedBy: designer
hash: "sha256:<hash do corpo abaixo do front-matter>"
---

# Target Domain Model

> Domain model for the new system. Explicit traceability to the legacy system (in `_reversa_sdd/domain.md` or equivalent).

## Aggregates

### AGG-Order
- **Aggregate root**: Order
- **Invariants**:
  - <invariant 1>
  - <invariant 2>
- **Accepted commands**: <list>
- **Events published** (if event-driven paradigm): <list>
- **Origin in the legacy system**: <ref to `domain.md` or equivalent>

<repeat for each aggregate>

## Entities

| Entity | Owning aggregate | Key attributes | Origin in the legacy system |
|---|---|---|---|
| <name> | <agg> | <summarized list> | <ref> |

## Value objects

| Value object | Attributes | Validations | Origin |
|---|---|---|---|
| <name> | <list> | <rules> | <ref> |

## Domain events
> Mandatory section if the paradigm is event-driven or hybrid.

| Event | Published by | Consumed by | Schema (summarized) |
|---|---|---|---|
| <OrderCreated> | AGG-Order | Payment, Inventory | <fields> |

## Domain rules
> Mapping of rules from `target_business_rules.md` (only the ones to be MIGRATED) to the aggregates / services where they now reside.

| Rule (ID) | Location in the new domain | Origin (target_business_rules.md) |
|---|---|---|
| BR-MIGRATE-001 | AGG-Order.invariant <name> | BR-MIGRATE-001 |

## Traceability to the legacy system

| New element | Origin in the legacy system | Mapping type |
|---|---|---|
| AGG-Order | `domain.md § Order` + `sdd/orders.md` | merged |
| <new> | <ref> | 1-to-1 / merged / split / new |

## Notes
<Additional modeling notes.>
```