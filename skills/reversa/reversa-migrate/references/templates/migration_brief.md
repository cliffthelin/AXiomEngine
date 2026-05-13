```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: migration_brief
producedBy: orchestrator
hash: "sha256:<hash of the body below the front-matter>"
---

# Migration Brief

> Migration criteria document collected during the interview at the beginning of `/reversa-migrate`.
> Consumed by the six agents of the Migration Team. Does not inquire about paradigms (responsibility of the Paradigm Advisor) or appetite (derived in `paradigm_decision.md`).

## Migration Objective
<Why does this migration exist? What changes in the business if it happens or does not happen?>

## Success Metrics
- <metric 1, with a clear numerical or qualitative target>
- <metric 2>
- <metric 3>

## Constraints
- **Deadline**: <date or window>
- **Budget**: <range, team size, hiring involved>
- **Technical**: <external APIs that cannot change, contracts, regulatory rules>
- **Operational**: <maintenance windows, SLAs during the migration>

## Known Risk Factors
- <risk 1: short description>
- <risk 2>

## Stakeholders
| Name / Role | Responsibility in the migration |
|---|---|
| <name> | <responsibility> |

## Target Stack
- **Language**: <e.g., Node.js 20>
- **Framework**: <e.g., Fastify>
- **Database**: <e.g., PostgreSQL 16>
- **Messaging** (if applicable): <e.g., SQS, Kafka, none>
- **Infrastructure**: <e.g., AWS Lambda, Kubernetes, on-premise>
- **Other relevant components**: <cache, observability, gateway>

## Declared Scope
- **Included**: <legacy modules that are included>
- **Excluded**: <modules that are excluded or will be discontinued>

## Free Notes
<Any context that the user wants to leave recorded for the agents to read.>
```