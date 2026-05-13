```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: discard_log
producedBy: curator
hash: "sha256:<hash of the body below the front-matter>"
---

# Discard Log

> A complete record of what was discarded from the migration and why. Each item has traceability back to its origin in the legacy system.

## Discarded Items

### BR-DESCARTAR-001
- **Origin**: `_reversa_sdd/<unit>/{requirements,design}.md` § <section>
- **Description**: <discarded rule or behavior>
- **Justification**: <text>
- **Linked to paradigm**: yes | no
  - If yes: <which paradigm and how the target paradigm absorbs the case>
- **Replacement in the new system**: <none | replaced by X>
- **Risk of discarding**: low | medium | high, with explanatory note

<repeat for each item>

## Discarded Items due to Paradigm Shift (dedicated subsection)

> Lists only the items where `Linked to paradigm = yes`. Explicit audit for the coding agent.

| ID | Origin | Legacy Paradigm | Substitute in Target Paradigm |
|---|---|---|---|
| BR-DESCARTAR-XXX | <ref> | <ex: synchronous pessimistic lock> | <ex: idempotency via event ID> |

## Notes
<Final notes from the Curator regarding the discarded set.>
```