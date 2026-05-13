### SOURCE:
# Parity Coverage Matrix

Reference table to define the minimum set of `.feature` scenarios per flow, as per paradigm shift.

## Coverage per Transition

| Transition | Minimum Scenarios per Flow |
|---|---|
| No change | `@parity` (input → expected output) |
| Procedural → OO | `@parity` + `@invariant` (aggregate invariant validated) |
| Procedural → Event-Driven | `@parity` + `@idempotency` + `@order` + `@dlq` (behavior under queue failure) |
| Classic OO → OO with DI | `@parity` + `@composition` (no Active Record dependency) |
| Classic OO → Event-Driven | `@parity` + `@idempotency` + `@order` + `@saga` (compensation on failure) |
| Classic OO → Functional | `@parity` + `@immutability` + `@composition` |
| OO with DI → Event-Driven | `@parity` + `@idempotency` + `@order` |
| Functional → Event-Driven | `@parity` + `@idempotency` + `@order` |
| Any → Actor Model | `@parity` + `@supervision` (recovery after failure) |

## Conventioned Tags

- `@parity`: always present; primary equivalence.
- `@critical`: critical flow (regulatory, financial, sensitive data).
- `@regulatory`: when there is a formal external requirement.
- `@idempotency`: reprocessing does not duplicate effect.
- `@order`: order by key respected.
- `@dlq`: behavior when arriving in the dead letter queue.
- `@saga`: compensation in distributed transaction.
- `@invariant`: aggregate invariant validated.
- `@composition`: equivalent behavior under functional composition.
- `@immutability`: no shared mutation.
- `@supervision`: supervisor recovers failed actor.

## Typical "accepted parity" criteria

| System Type | Primary Metric |
|---|---|
| Web app without strong regulation | functional divergence < 1% per 7 days |
| Public API | functional divergence < 0.1% per 30 days + zero divergence in public contracts |
| Fiscal / Regulatory System | functional divergence < 0.01% per 60 days + zero divergence in regulated fields |
| Financial System | financial divergence by monetary value < 0.001% + zero divergence in totals |
| Internal System, Low Criticality | functional divergence < 5% per 7 days |

## Reuse of `characterization_specs`

When `_reversa_sdd/characterization_specs/` exists:

1. For each spec → derive the corresponding `.feature`, adapting inputs/outputs to the new system.
2. Keep the original `spec-id` in the traceability.
3. Add extra scenarios according to the "Minimum Scenarios per Flow" table.

When it does not exist:

1. Infer critical flows from `code-analysis.md` + `sequences/` + `BR-MIGRAR` rules marked as critical.
2. Document the gap in `parity_specs.md § Reuse of characterization_specs`.