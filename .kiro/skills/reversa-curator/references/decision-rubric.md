### Curator Decision Rubric

A quick reference table for applying the decision policy.

## Decision Table

| Observed signal in the rule | Default decision | Notes |
|---|---|---|
| 🟢 CONFIRMED, compatible with the target paradigm, no pain point | MIGRATE | no reservations |
| 🟡 INFERRED, compatible with the target paradigm | MIGRATE | add note "validate in the coding agent" |
| 🔴 GAP | HUMAN DECISION | optional recommendation |
| ⚠️ AMBIGUOUS | HUMAN DECISION | mandatory to list interpretations |
| Rule cited as a pain point | HUMAN DECISION | default recommendation: replace with X in the new one |
| Rule incompatible with brief (out of scope) | DISCARD | justification: "out of scope as declared in migration_brief.md" |
| Rule incompatible with brief (technical) | DISCARD | justification: "technical constraint of the brief prevents it" |
| Rule is a mechanism of the legacy paradigm, paradigm has changed | DISCARD (linked to paradigm) | indicate a substitute in the target paradigm |
| Rule is a mechanism of the legacy paradigm, paradigm is the same | MIGRATE | no reservations |

## List of typical paradigm mechanisms (discardable when the paradigm changes)

### Procedural → event-driven
- Pessimistic lock (`SELECT ... FOR UPDATE`)
- Entire ACID transaction around the flow
- Synchronous response to the user with inline side effect
- Retry implemented as `for` in the controller

### Classic OO → OO with DI
- Active Record that mixes persistence and domain
- Inheritance used for behavior reuse (prefer composition)
- Manual Singleton (prefer scoped DI)

### Classic OO → functional
- Mutable encapsulation (prefer immutable types)
- Void methods with side effect (prefer return + pure function)

### OO with DI → event-driven
- Synchronous commands with immediate return (prefer event + ack)
- Centralized orchestration (prefer choreography)
- 2PC / distributed transaction (prefer saga)

### Synchronous → asynchronous in general
- Timeout configured in the controller (goes to the consumer's retry policy)
- Error handling as a propagated exception (becomes DLQ)

## What to NEVER discard based on paradigm

- Pure business rules (calculations, conditions, derivations).
- Regulatory rules.
- Domain invariants.
- Rights / permissions.

These rules change **location** in the new paradigm, but they don't disappear.