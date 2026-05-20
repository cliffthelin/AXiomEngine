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

> Migration criteria document gathered during interviews at the beginning of the `/reversa-migrate` process.
> Used by the six agents of the Migration Team. Does not address paradigm (responsibility of the Paradigm Advisor) or appetite (defined in `paradigm_decision.md`).

## Migration Goal
<Why does this migration exist? What business changes would result from its completion or failure?>

## Success Metrics
- <metric 1, with a clear numerical or qualitative target>
- <metric 2>
- <metric 3>

## Constraints
- **Deadline**: <date or time window>
- **Budget**: <range, team, and resources involved>
- **Technical**: <external APIs that cannot be changed, contracts, regulatory requirements>
- **Operational**: <maintenance windows, SLAs during the migration>

## Known Risk Factors
- <risk 1: brief description>
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
<Any context the user wants to leave for the agents to review.>
```