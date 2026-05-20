```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: screen_deviation_log
producedBy: screen-translator
mode: append-only
hash: "sha256:<hash of the body below the front-matter>"
---

# Screen Deviation Log

> A record of all divergences between the legacy system and the specification generated in `target_screens.md`. Append-only. Pending deviations block handoff to the Inspector.
> Approved deviations are propagated to `parity_specs.md § Exceptions` when the Inspector runs.

## Conventions

- **ID**: `DEV-NNN` (sequential, three digits).
- **Type**:
  - `technical`: technical limitation of the target system (e.g., a Windows terminal without UTF-8 support, requiring `chcp 65201`).
  - `modernization`: intentional divergence resulting from the modernized approach.
  - `platform`: divergence forced by platform incompatibility (e.g., Win16 → web).
  - `correction`: visual bug in the legacy system that the target system corrects (e.g., a typo in a label).
- **Approval**: `pending` | `approved` | `rejected`.
- Approved Deviation → also listed in `parity_specs.md § Exceptions`.
- Pending Deviation → blocks handoff to the Inspector.
- Rejected Deviation → archived with an explicit note; the agent regenerates the screen in a compliant mode.

## Summary

- **Total**: <N>
- **Pending**: <N>
- **Approved**: <N>
- **Rejected**: <N>

## Entries

### DEV-001

| Field | Value |
|---|---|
| Affected Screen | <canonical-name> |
| Type | `technical` \| `modernization` \| `platform` \| `correction` |
| Description | <what diverges between legacy and new> |
| Reason | <why the divergence is necessary or acceptable> |
| Origin in Legacy | <file:line> |
| Implication for parity tests | <e.g., false byte-by-byte comparison, use semantic comparison> |
| Approval | `pending` \| `approved` \| `rejected` |
| Approved by | <name or identifier, when approved> |
| Approved on | <ISO-8601, when approved> |
| Propagates to `parity_specs.md § Exceptions` | yes \| no |

### DEV-002

(repeat the above block for each deviation)

## Screens with more than one deviation

| Screen | IDs |
|---|---|
| <screen X> | DEV-001, DEV-007 |

## Notes

<General observations about the set of deviations: patterns, lessons learned that apply to future migrations in the same source→target pair, suggestions for improved adapter for v2.>
```