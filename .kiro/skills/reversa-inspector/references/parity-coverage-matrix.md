### SOURCE:
### TARGET:

# Parity Coverage Matrix

Reference table for defining the minimum set of `.feature` scenarios per flow, according to the paradigm shift.

## Coverage by Transition

| Transition | Minimum Scenarios per Flow |
|---|---|
| No change | `@parity` (input → expected output) |
| Procedural → OO | `@parity` + `@invariant` (aggregate invariant validated) |
| Procedural → Event-driven | `@parity` + `@idempotency` + `@order` + `@dlq` (behavior under queue failure) |
| Classic OO → OO with DI | `@parity` + `@composition` (no Active Record dependency) |
| Classic OO → Event-driven | `@parity` + `@idempotency` + `@order` + `@saga` (compensation upon failure) |
| Classic OO → Functional | `@parity` + `@immutability` + `@composition` |
| OO with DI → Event-driven | `@parity` + `@idempotency` + `@order` |
| Functional → Event-driven | `@parity` + `@idempotency` + `@order` |
| Any → Actor model | `@parity` + `@supervision` (recovery after failure) |

## Conventional Tags

- `@parity`: always present; main equivalence.
- `@critical`: critical flow (regulatory, financial, sensitive data).
- `@regulatory`: when there is an external formal requirement.
- `@idempotency`: reprocessing does not duplicate effect.
- `@order`: order by key respected.
- `@dlq`: behavior upon arrival in the dead letter queue.
- `@saga`: compensation in distributed transaction.
- `@invariant`: aggregate invariant validated.
- `@composition`: equivalent behavior under functional composition.
- `@immutability`: no shared mutation.
- `@supervision`: supervisor recovers failed actor.

## Typical "accepted parity" criteria

| System Type | Primary Metric |
|---|---|
| Web app with no strong regulation | functional divergence < 1% over 7 days |
| Public API | functional divergence < 0.1% over 30 days + zero divergence in public contracts |
| Fiscal / regulatory system | functional divergence < 0.01% over 60 days + zero divergence in regulated fields |
| Financial system | financial divergence per monetary value < 0.001% + zero divergence in totals |
| Internal system with low criticality | functional divergence < 5% over 7 days |

## Re-use of `characterization_specs`

When `_reversa_sdd/characterization_specs/` exists:

1. For each spec, derive the corresponding `.feature`, adapting inputs/outputs to the new system.
2. Maintain the original `spec-id` in the traceability.
3. Add extra scenarios according to the "Minimum Scenarios per Flow" table.

When it does not exist:

1. Infer critical flows from `code-analysis.md` + `sequences/` + `BR-MIGRAR` rules marked as critical.
2. Document the gap in `parity_specs.md § Re-use of characterization_specs`.
