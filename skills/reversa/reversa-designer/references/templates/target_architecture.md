```
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: target_architecture
producedBy: designer
hash: "sha256:<hash of the body below the front-matter>"
---

# Target Architecture

> Target architecture for the new system, respecting the paradigm chosen in `paradigm_decision.md` and the strategy confirmed in `migration_strategy.md`.

## Overview
<Summary in 3 to 6 lines: what is the new system, what paradigm does it follow, what boundaries does it have with the legacy system during migration.>

## Diagram (Mermaid)

```mermaid
flowchart LR
    %% Replace with the actual diagram
    Client -->|HTTP| API
    API --> Service
    Service --> Database[(DB)]
    Service -.events.-.> Queue[[Messaging]]
```

## Components

| Component | Type | Responsibility | Origin (legacy / new / merged) |
|---|---|---|---|
| <name> | API / Service / Worker / DB / Queue | <text> | <ref to legacy or "new"> |

## Bounded contexts

### BC-01: <name>
- **Responsibility**: <text>
- **Justification for grouping / separation**: <why this context was not decomposed 1-to-1 from the legacy system>
- **Internal components**: <list>
- **Events published** (if event-driven paradigm): <list>
- **Events consumed**: <list>

<repeat for each context>

## Architectural Decisions (ADR-style summarized)

### AD-01: <title>
- **Decision**: <text>
- **Alternatives discarded**: <list>
- **Justification**: <text, linking to paradigm, strategy, and risk appetite>
- **Traceability**: <reference to the legacy system or the `discard_log`>

## Honoring the chosen paradigm

> Mandatory section when there is a paradigm shift. Demonstrates that the architecture honors the decision in `paradigm_decision.md`.

- **Target paradigm**: <from `paradigm_decision.md`>
- **How the architecture honors this paradigm**:
  - <e.g., event-driven → explicit events, message schemas, eventual consistency strategy>
  - <e.g., OO with DI → interfaces, dependency injection container, clear boundaries between layers>
  - <e.g., functional → immutable types, composition, absence of side effects in the domain>

## Boundaries with the legacy system during migration
- <e.g., during the Strangler Fig pattern, the new API re-routes calls from legacy X until phase Y>

## Notes
<Additional design notes.>
```