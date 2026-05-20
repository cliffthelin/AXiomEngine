```
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: target_architecture
producedBy: designer
hash: "sha256:<hash do corpo abaixo do front-matter>"
---

# Target Architecture

> Target architecture for the new system, respecting the paradigm chosen in `paradigm_decision.md` and the strategy confirmed in `migration_strategy.md`.

## Overview
<Summary in 3 to 6 lines: what is the new system, what paradigm does it follow, and what are its boundaries with the legacy system during migration.>

## Diagram (Mermaid)

```mermaid
flowchart LR
    %% Substitute with the actual diagram
    Client -->|HTTP| API
    API --> Service
    Service --> DB[(DB)]
    Service -.events.-.-> Queue[[Messaging]]
```

## Components

| Component | Type | Responsibility | Origin (legacy / new / merged) |
|---|---|---|---|
| <name> | API / Service / Worker / DB / Queue | <text> | <ref to legacy or "new"> |

## Bounded contexts

### BC-01: <name>
- **Responsibility**: <text>
- **Justification for grouping / separation**: <why this context was not decomposed 1-to-1 from the legacy>
- **Internal components**: <list>
- **Events published** (if event-driven paradigm): <list>
- **Events consumed**: <list>

<repeat for each context>

## Architectural Decisions (ADR-style summarized)

### AD-01: <title>
- **Decision**: <text>
- **Discarded alternatives**: <list>
- **Justification**: <text, linking to paradigm, strategy, and appetite>
- **Traceability**: <reference to the legacy or the discard_log>

## Honoring the Chosen Paradigm

> Mandatory section when there is a paradigm shift. Demonstrates that the architecture honors the decision from `paradigm_decision.md`.

- **Target Paradigm**: <from `paradigm_decision.md`>
- **How the architecture honors this paradigm**:
  - <ex: event-driven → explicit events, message schemas, eventual consistency strategy>
  - <ex: OO with DI → interfaces, dependency injection container, clear boundaries between layers>
  - <ex: functional → immutable types, composition, absence of side effects in the domain>

## Boundaries with the Legacy During Migration
- <ex: during the Strangler Fig pattern, the new API re-routes calls from legacy system X until phase Y>

## Notes
<Additional design notes.>
```