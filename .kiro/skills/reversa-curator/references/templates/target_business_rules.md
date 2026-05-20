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
> Each item tracks back to its origin in `_reversa_sdd/` and adheres to `paradigm_decision.md`.

## Summary
- Total rules analyzed: <N>
- MIGRATE: <n>
- DISCARD: <n> (details in `discard_log.md`)
- HUMAN DECISION: <n>

## MIGRATE Rules

### BR-MIGRATE-001
- **Origin**: `_reversa_sdd/<unit>/{requirements,design}.md` § <section>
- **Original Confidence**: 🟢 | 🟡 | 🔴 | ⚠️
- **Description**: <rule>
- **Migration Justification**: <why to migrate>
- **Target Paradigm Compatibility**: <note; e.g., needs to be expressed as an event>

<repeat for each rule>

## DISCARD Rules (summary)

| ID | Origin | Short Reason | Linked to Paradigm? |
|---|---|---|---|
| BR-DISCARD-001 | <ref> | <reason> | yes/no |

> Full details in `discard_log.md`.

## HUMAN DECISION Rules

### BR-HUMAN-001
- **Origin**: <ref>
- **Type of Ambiguity**: ⚠️ AMBIGUOUS | 🔴 GAP | stakeholder dependency
- **Description**: <rule>
- **Options**: <clear options>
- **Curator's Recommendation**: <suggested option and why>
- **Status**: PENDING | RESOLVED (choice + decision-maker + date)

<repeat for each item>

## Notes
<General notes from the Curator. Items that will be consolidated in `ambiguity_log.md`.>
```