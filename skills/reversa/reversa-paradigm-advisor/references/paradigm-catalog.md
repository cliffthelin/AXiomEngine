### SOURCE:
> Local copy of the reference catalog. The canonical source is located at `templates/migration/catalogs/paradigm_catalog.md`.
> This copy is installed along with the agent so that it has access to the catalog within the user's project, without depending on the location of the npm package.

# Paradigm Catalog (local copy)

## Catalog of paradigms

### Procedural
- **Characteristics**: top-level functions, linear flow in controllers, absence of classes or ornamental use, data as dictionaries/structures, open side effects.
- **Examples in legacy**: classic PHP scripts, COBOL batch, pre-OO Perl systems, shell scripts.
- **Signals in `_reversa_sdd/`**: domain described as "functions", linear flows in `process_flows`, absence of explicit aggregates.

### Classic OO
- **Characteristics**: class hierarchy, strong inheritance, Active Record pattern, logic coupled to the models.
- **Examples in legacy**: monolithic Rails, traditional Django, pre-DI Java EE, .NET WebForms / classic.
- **Signals in `_reversa_sdd/`**: classes with broad responsibilities, inheritance in the domain model, anemic controllers calling model methods.

### OO with DI
- **Characteristics**: dependency injection containers, explicit interfaces, Repository / Service pattern, clear separation between layers.
- **Examples in legacy**: modern Spring, .NET 6+, NestJS, modern Symfony.
- **Signals in `_reversa_sdd/`**: explicit aggregates, repository interfaces, absence of Active Record.

### Functional
- **Characteristics**: dominant immutability, pure functions, composition, absence of implicit side effects, rich typing.
- **Examples in legacy**: Haskell, Elm, F#, functional Scala, Clojure.
- **Signals in `_reversa_sdd/`**: algebraic types, absence of classes, flow expressed as composition.

### Event-driven (asynchronous)
- **Characteristics**: queues / topics, decoupled handlers, absence of linear flow, eventual consistency, explicit idempotency.
- **Examples in legacy**: modern Node backends oriented towards queues, heavy SQS / Kafka systems, asynchronous microservices.
- **Signals in `_reversa_sdd/`**: events in the domain model, integrations via queue, long-running processes with retry.

### Actor model
- **Characteristics**: isolated actors with mailbox, supervision, state isolation.
- **Examples in legacy**: Erlang / Elixir / OTP, Akka.
- **Signals in `_reversa_sdd/`**: supervised processes, messages between actors.

### Dataflow
- **Characteristics**: declarative pipelines, transformations in flow, absence of imperative loops in the domain.
- **Examples in legacy**: classic ETLs, Spark, Flink.
- **Signals in `_reversa_sdd/`**: description in DAG, transformations in stages.

## Stack Mapping → Natural Paradigm

| Target Stack | Natural Paradigm | Viable Alternatives | Notes |
|---|---|---|---|
| Node.js 20 (Fastify, Express, NestJS) | event-driven asynchronous | OO with DI (NestJS), lightweight functional | runtime is async-first; heavy CPU blocking goes to worker threads |
| Go (net/http, Echo, Fiber) | CSP / goroutines (lightweight event-driven) | structured procedural | concurrency via channels; OO simulated via interfaces |
| Rust (axum, Actix, tokio) | ownership / async functional | event-driven | immutability by default, safety via types |
| Elixir / Phoenix | actor model (BEAM) | functional | supervision via OTP |
| Modern Python (FastAPI, Django 5) | OO with DI or rich procedural | event-driven (Celery, asyncio) | choice depends on the framework |
| Kotlin (Spring Boot, Ktor) | OO with DI | event-driven (Reactor) | coroutines enable ergonomic async |
| .NET 8 (ASP.NET Core, Minimal API) | OO with DI | event-driven (Channels, MediatR) | tradition of OO + first-class asynchronicity |
| Modern Java (Spring Boot 3, Quarkus) | OO with DI | event-driven (Project Reactor) | functional libraries possible but not dominant |
| Modern Ruby (Rails 7, Hanami) | classic OO (Rails) or OO with DI (Hanami) | lightweight functional (dry-rb) | Rails dictates Active Record; Hanami is DI-heavy |
| TypeScript serverless (AWS Lambda, Cloudflare Workers) | event-driven | functional | invocation by event; cold start influences design |

## Typical Gap Table by Pair

| From → To | Main Gap | Concrete Implications |
|---|---|---|
| procedural → event-driven | synchronicity → asynchronicity | response is no longer immediate; error handling becomes retry/DLQ; idempotency is required; order of events matters |
| procedural → OO with DI | data as dictionary → aggregates | invariants are inside aggregates; logic no longer lives in controllers; dependencies via interfaces |
| procedural → functional | open side effects → pure + isolated | mutability becomes an exception; composition replaces sequence; algebraic types for states |
| Classic OO → event-driven | synchronous flow → choreography | actions are no longer atomic; distributed transactions become sagas; strong consistency → eventual |
| Classic OO → OO with DI | inheritance → composition via interfaces | Active Record disappears; persistence becomes a repository; tests gain natural mocks |
| Classic OO → functional | mutable encapsulation → immutability | methods with effects become pure functions + explicit update; state expressed as a sequence of transformations |
| OO with DI → event-driven | synchronous command → event | return is no longer immediate; orchestration becomes choreography; order by key |
| OO with DI → functional | mocks → testable composition | DI stops being by interface, becomes by function argument |
| functional → event-driven | synchronous composition → messaging | latency increases; failure becomes a message in the DLQ; distributed state |
| event-driven → synchronous procedural | unnatural; only makes sense for small systems | collapse handlers into direct calls; loss of decoupling; strong consistency returns |
| dataflow → event-driven | declarative DAG → mutable choreography | control becomes less predictable; order must be guaranteed by key |
| actor model → OO with DI | messages between actors → synchronous calls | loss of failure isolation; supervision must become try/catch or orchestrated retry |
