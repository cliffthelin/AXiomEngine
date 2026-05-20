```markdown
### SOURCE:
> Local copy of the consulting catalog. The canonical source is located at `templates/migration/catalogs/paradigm_catalog.md`.
> This copy is installed along with the agent, so it has access to the catalog within the user's project, without relying on the location of the npm package.

# Paradigm Catalog (local copy)

## Catalog of Paradigms

### Procedural
- **Characteristics**: Top-level functions, linear flow in controllers, absence of classes or ornamental use, data as dicts/structs, open side effects.
- **Examples in legacy**: Classic PHP scripts, COBOL batch, pre-OO Perl systems, shell scripts.
- **Signals in `_reversa_sdd/`**: Domain described as "functions", linear flows in `process_flows`, absence of explicit aggregates.

### Classic OO
- **Characteristics**: Class hierarchy, strong inheritance, Active Record pattern, logic coupled to the models.
- **Examples in legacy**: Monolithic Rails, traditional Django, pre-DI Java EE, .NET WebForms / classic.
- **Signals in `_reversa_sdd/`**: Classes with broad responsibilities, inheritance in the domain model, anemic controllers calling model methods.

### OO with DI
- **Characteristics**: Dependency injection containers, explicit interfaces, Repository / Service pattern, clear separation between layers.
- **Examples in legacy**: Modern Spring, .NET 6+, NestJS, modern Symfony.
- **Signals in `_reversa_sdd/`**: Explicit aggregates, repository interfaces, absence of Active Record.

### Functional
- **Characteristics**: Dominant immutability, pure functions, composition, absence of implicit side effects, rich typing.
- **Examples in legacy**: Haskell, Elm, F#, functional Scala, Clojure.
- **Signals in `_reversa_sdd/`**: Algebraic types, absence of classes, flow expressed as composition.

### Event-driven (asynchronous)
- **Characteristics**: Queues / topics, decoupled handlers, absence of linear flow, eventual consistency, explicit idempotence.
- **Examples in legacy**: Modern Node backends oriented to queues, heavy SQS / Kafka systems, asynchronous microservices.
- **Signals in `_reversa_sdd/`**: Events in the domain model, integrations via queue, long-running processes with retry.

### Actor model
- **Characteristics**: Isolated actors with mailbox, supervision, state isolation.
- **Examples in legacy**: Erlang / Elixir / OTP, Akka.
- **Signals in `_reversa_sdd/`**: Supervised processes, messages between actors.

### Dataflow
- **Characteristics**: Declarative pipelines, transformations in flow, absence of imperative loops in the domain.
- **Examples in legacy**: Classic ETLs, Spark, Flink.
- **Signals in `_reversa_sdd/`**: Description in DAG, transformations in stages.

## Stack Mapping → Natural Paradigm

| Target Stack            | Natural Paradigm                         | Viable Alternatives         | Notes                                             |
|-------------------------|------------------------------------------|-----------------------------|---------------------------------------------------|
| Node.js 20 (Fastify, Express, NestJS) | Event-driven asynchronous              | OO with DI (NestJS), light functional | Runtime is async-first; heavy CPU blocking goes to worker threads |
| Go (net/http, Echo, Fiber)     | CSP / goroutines (light event-driven)  | Structured procedural       | Concurrency via channels; OO simulated via interfaces |
| Rust (axum, Actix, tokio)       | Ownership / async functional            | Event-driven               | Immutability by default, safety via types |
| Elixir / Phoenix        | Actor model (BEAM)                     | Functional                 | Supervision via OTP |
| Modern Python (FastAPI, Django 5) | OO with DI or rich procedural          | Event-driven (Celery, asyncio) | Choice depends on the framework |
| Kotlin (Spring Boot, Ktor)    | OO with DI                               | Event-driven (Reactor)           | Coroutines enable ergonomic async |
| .NET 8 (ASP.NET Core, Minimal API) | OO with DI                               | Event-driven (Channels, MediatR)  | Tradition OO + async first-class |
| Modern Java (Spring Boot 3, Quarkus) | OO with DI                               | Event-driven (Project Reactor)  | Functional libraries possible but not dominant |
| Modern Ruby (Rails 7, Hanami)   | Classic OO (Rails) or OO with DI (Hanami) | Light functional (dry-rb)        | Rails dictates Active Record; Hanami is DI-heavy |
| TypeScript serverless (AWS Lambda, Cloudflare Workers) | Event-driven     | Functional        | Invocation by event; cold start influences design |

## Typical Gap Table per Pair

| From → To           | Main Gap                    | Concrete Implications                                                                                                 |
|---------------------|-----------------------------|-------------------------------------------------------------------------------------------------------------------------|
| procedural → event-driven | synchronicity → asynchronicity | Response is no longer immediate; error handling becomes retry/DLQ; idempotence is mandatory; order of events matters |
| procedural → OO with DI    | data as dict → aggregates       | Invariants are inside aggregates; logic no longer lives in controllers; dependencies via interfaces                  |
| procedural → functional | open side effects → pure + isolated | Mutability becomes an exception; composition replaces sequence; algebraic types for states                      |
| classic OO → event-driven | synchronous flow → choreography | Actions are no longer atomic; distributed transactions become sagas; strong consistency → eventual            |
| classic OO → OO with DI    | inheritance → composition via interfaces | Active Record disappears; persistence becomes a repository; tests gain natural mocks                              |
| classic OO → functional    | mutable encapsulation → immutability | Methods with effect become pure functions + explicit update; state expressed as a sequence of transformations        |
| OO with DI → event-driven        | synchronous command → event     | Response is no longer immediate; orchestration becomes choreography; ordering by key                           |
| OO with DI → functional    | mocks → testable composition | DI is no longer by interface, it becomes by function argument |
| functional → event-driven      | synchronous composition → messaging | Latency increases; failure becomes a message in DLQ; distributed state |
| event-driven → synchronous procedural | Unnatural; only makes sense for small systems | Collapsing handlers into direct calls; loss of decoupling; strong consistency returns |
| dataflow → event-driven   | declarative DAG → mutable choreography | Control becomes less predictable; order must be guaranteed by key |
| actor model → OO with DI | messages between actors → synchronous calls | Loss of failure isolation; supervision becomes try/catch or orchestrated retry |
```