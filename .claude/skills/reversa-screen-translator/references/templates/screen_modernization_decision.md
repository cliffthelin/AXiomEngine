```markdown
---
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: screen_modernization_decision
producedBy: screen-translator
decidedBy: <human-id or null when mode=skipped>
decidedAt: <ISO-8601 or null when mode=skipped>
mode: literal | modernized | hybrid | skipped
sourcePlatform: <slug or null when mode=skipped>
targetPlatform: <slug or null when mode=skipped>
hash: "sha256:<hash of the body below the front-matter>"
---

> When `mode: skipped`, this decision was **not reviewed by a human:** it was automatically issued by the Screen Translator because the legacy system has no UI. Only the "Context" and "Decision" sections are filled in, with the reason for the omission; the others remain as N/A. The Inspector reads `mode: skipped` in the front-matter and skips visual parity without prompting.

# Screen Modernization Decision

> A conscious decision on how to translate the screens of the legacy system: observable byte-for-byte or pixel-equivalent parity, idiomatic redesign for the target platform, or screen-by-screen combination.
> This artifact is essential reading for the Screen Translator itself (to generate `target_screens.md`), the Inspector (to build parity tests appropriate to the mode), and the coding agent.

## Context

- **Detected source platform**: <slug> (e.g., `cobol-ansi-tui`, `delphi-vcl`, `asp-classic`, `android-xml`)
- **Confidence**: 🟢 CONFIRMED | 🟡 INFERRED | 🔴 GAP | ⚠️ AMBIGUOUS
- **Target platform**: <slug> (e.g., `go-cli`, `web-spa`, `flutter`, `tauri`)
- **Screens inventoried**: <N>
- **Inventory source**: `_reversa_sdd/screens/inventory.json` + `_reversa_sdd/ui/inventory.md`
- **Adapter applied**: `<adapters/source__target>` (see `references/adapter-pairs.md`)

## Modes evaluated

### Mode: literal
- **Definition**: Observable byte-for-byte or pixel-equivalent parity between legacy and new.
- **Trade-offs**:
  - Implementation cost: <high | medium | low>
  - Visual fidelity: <high | medium | low>
  - Feasibility of constructive parity tests: <yes | partial | no>
  - Expected end-user acceptance: <high | medium | low>
  - Future technical debt: <high | medium | low>
- **Recommended**: <yes | no>
- **Justification**: <short text>

### Mode: modernized
- **Definition**: Idiomatic redesign for the target platform, preserving information and flow, but re-expressing hierarchy and interaction.
- **Trade-offs**:
  - Implementation cost: <high | medium | low>
  - Visual fidelity: <high | medium | low>
  - Feasibility of constructive parity tests: <yes | partial | no>
  - Expected end-user acceptance: <high | medium | low>
  - Future technical debt: <high | medium | low>
- **Recommended**: <yes | no>
- **Justification**: <short text>

### Mode: hybrid
- **Definition**: Some screens in literal mode, some in modernized mode, with explicit lists.
- **Trade-offs**:
  - Implementation cost: <high | medium | low>
  - Mixed visual fidelity: <description>
  - Feasibility of parity tests: <description per subset>
  - Cost of maintaining separation: <high | medium | low>
- **Recommended**: <yes | no>
- **Justification**: <short text>

## Decision

- **Chosen mode**: <literal | modernized | hybrid>
- **Human justification**: <text>
- **Discarded alternatives**: <brief list with reason>
- **Decided on**: <ISO-8601>
- **Decided by**: <name or identifier>

### In hybrid mode, explicit lists (mandatory)

**Screens in literal mode**:
- <screen 1>
- <screen 2>

**Screens in modernized mode**:
- <screen 3>
- <screen 4>

> Empty lists block Phase 2. The agent refuses to proceed.

## Pending implications for Phase 2

| Step | Implication | How to honor |
|---|---|---|
| Generation of `target_screens.md` | <implication> | <expected action> |
| Capture of golden files | <implication> | <expected action> |
| Design-system tokens | <implication> | <expected action> |
| Textual content | Preserve literal unless explicit approval for linguistic review | <expected action> |

## Implications for the Inspector

- **Parity strategy**:
  - Literal mode → observable byte-for-byte / pixel-equivalent parity, validated by golden files when the oracle executes.
  - Modernized mode → semantic contract (events, transitions, textual content, states), with no byte-for-byte visual comparison.
  - Hybrid mode → mixed strategy, declared by screen in `parity_specs.md`.
- **Known deviations to propagate**: see `screen_deviation_log.md`.

## Notes

<Additional points that the coder, the Inspector, and the agent need to know in order to honor the decision. This includes, for example, explicit approval for linguistic review, tolerance for approximate rendering, or marking of screens that cannot be modernized due to regulatory requirements.>
```