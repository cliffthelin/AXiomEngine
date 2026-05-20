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

> Complete record of what was discarded from the migration and why. Each item has traceability to its origin in the legacy system.

## Discarded Items

### BR-DESCARTAR-001
- **Origin**: `_reversa_sdd/<unit>/{requirements,design}.md` § <section>
- **Description**: <rule or behavior discarded>
- **Justification**: <text>
- **Linked to Paradigm**: yes | no
  - If yes: <which paradigm and how the target paradigm absorbs the case>
- **Replacement in the new system**: <none | replaced by X>
- **Risk of discarding**: low | medium | high, with explanatory note

<repeat for each item>

## Items Discarded Due to Paradigm Shift (dedicated subsection)

> List of only those items where `Linked to Paradigm = yes`. Explicit audit for the coding agent.

| ID | Origin | Legacy Paradigm | Substitute in Target Paradigm |
|---|---|---|---|
| BR-DESCARTAR-XXX | <ref> | <e.g., synchronous pessimistic lock> | <e.g., idempotency via event ID> |

## Notes
<Curator's final remarks on the discarded set.>
```