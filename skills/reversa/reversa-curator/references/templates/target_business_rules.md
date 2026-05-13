```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: target_business_rules
producedBy: curator
hash: "sha256:<hash of the body below the front-matter>"
---

# Target Business Rules

> Catalog of legacy business rules with migration decision: MIGRATE, DISCARD, or HUMAN DECISION.
> Each item traces back to its origin in `_reversa_sdd/` and adheres to `paradigm_decision.md`.

## Summary
- Total rules analyzed: <N>
- MIGRATE: <n>
- DISCARD: <n> (details in `discard_log.md`)
- HUMAN DECISION: <n>

## Rules to MIGRATE

### BR-MIGRATE-001
- **Origin**: `_reversa_sdd/<unit>/{requirements,design}.md` § <section>
- **Original Confidence**: 🟢 | 🟡 | 🔴 | ⚠️
- **Description**: <rule>
- **Migration Justification**: <why to migrate>
- **Compatibility with Target Paradigm**: <note; e.g., needs to be expressed as an event>

<repeat for each rule>

## Rules to DISCARD (summary)

| ID | Origin | Short Reason | Linked to Paradigm? |
|---|---|---|---|
| BR-DISCARD-001 | <ref> | <reason> | yes/no |

> Full details in `discard_log.md`.

## Rules requiring HUMAN DECISION

### BR-HUMAN-001
- **Origin**: <ref>
- **Type of Ambiguity**: ⚠️ AMBIGUOUS | 🔴 GAP | stakeholder dependency
- **Description**: <rule>
- **Options**: <clear options>
- **Curator Recommendation**: <suggested option and why>
- **Status**: PENDING | RESOLVED (choice + decision-maker + date)

<repeat for each item>

## Notes
<General Curator's notes. Items to be consolidated in `ambiguity_log.md`.>
```