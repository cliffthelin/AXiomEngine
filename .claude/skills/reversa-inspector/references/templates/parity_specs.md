```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: parity_specs
producedBy: inspector
hash: "sha256:<hash of the body below the front-matter>"
---

# Parity Specifications

> Strategy for validating behavioral equivalence between the legacy and new system, adapted to the paradigm chosen in `paradigm_decision.md`.

## General Strategy
- **Applicable validation modes** (mark the ones used):
  - [ ] Shadow mode (traffic mirroring with asynchronous comparison)
  - [ ] Characterization tests (suite derived from the current legacy behavior)
  - [ ] Contract tests (external interfaces)
  - [ ] Data parity (snapshots and checksums)
  - [ ] Other: <specify>

## Criteria for "accepted parity"
- **Primary metric**: <e.g., functional divergence index < 0.01% over N consecutive days>
- **Observation window**: <evaluation period>
- **Blocking criterion**: <when insufficient parity blocks the cutover>

## Coverage adapted to the paradigm

> This section changes based on the target paradigm confirmed in `paradigm_decision.md`.

### No paradigm change
- Standard functional equivalence: same input → same output → same observable side effect.

### Synchronous → Event-driven change
- **Message order**: <acceptance criterion per channel / partition>
- **Idempotency**: <proof that reprocessing does not duplicate the effect>
- **Eventual consistency**: <maximum acceptable propagation window>
- **Behavior under queue failure**: <retry, DLQ, replay>

### Procedural → OO change
- **Invariants in aggregates**: <set to be validated>
- **Validation in factories / constructors**: <critical cases>

### OO → Functional change
- **Immutability**: <critical points to observe>
- **Absence of expected side effects**: <where the legacy had implicit side effects>
- **Equivalence under composition**: <composed functions are equivalent to the legacy flow>

## Types of tests to be applied
- **Functional**: <description, tool>
- **Contract**: <description, tool>
- **Load / performance**: <description, targets>
- **Resilience** (if applicable): <queue failure, unavailable external dependency>

## Reuse of characterization_specs from the discovery team
- **Origin**: `_reversa_sdd/characterization_specs/` or equivalent available.
- **Adaptations needed for the new system**: <text>

## Outputs
- `parity_tests/*.feature`: scenarios in Gherkin for the critical flows.

## Notes
<Additional notes.>
```