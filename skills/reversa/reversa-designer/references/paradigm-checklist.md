# Honor Checklist for the Target Paradigm

A quick checklist that the Designer applies before closing `target_architecture.md` and `target_domain_model.md`.

## Event-driven

- [ ] Events are named in the past tense (`OrderCreated`, not `CreateOrder`).
- [ ] Each event has an explicit schema with versioning.
- [ ] Commands and events are distinct.
- [ ] Idempotency is guaranteed by design (event ID, deduplication key).
- [ ] Message order is handled by partitioning key.
- [ ] Saga / orchestrator for distributed transactions, with compensation.
- [ ] Outbox table for at-least-once guarantee between database and queue.
- [ ] DLQ defined for terminal failures.

## OO with DI

- [ ] Explicit interfaces for external dependencies.
- [ ] Dependency injection container configured per bounded context.
- [ ] Aggregates do not depend on infrastructure (no persistence within the aggregate).
- [ ] Concrete repositories live in the infrastructure layer.
- [ ] Active Record is explicitly prohibited.

## Functional

- [ ] Immutable types in the domain.
- [ ] Pure functions in the core; side effects at the edge.
- [ ] State is a sequence of transformations, not mutation.
- [ ] Composition is used to build flows.
- [ ] Algebraic types (sum types) for disjoint states.

## Actor model

- [ ] Each actor has a mailbox and isolated state.
- [ ] Hierarchical supervision is defined.
- [ ] Messages between actors are immutable.
- [ ] Persistence via event sourcing or snapshot.

## Procedural / dataflow

- [ ] Flow expressed as a pipeline of transformations.
- [ ] No shared mutable state.
- [ ] Independent and isolated, testable stages.

## General (any paradigm)

- [ ] Each element points to its origin in the legacy system or to `discard_log.md`.
- [ ] Bounded contexts are justified by cohesion, not by legacy structure.
- [ ] Mermaid diagram renders without error.
- [ ] Architectural decisions are documented in a summarized ADR format.
