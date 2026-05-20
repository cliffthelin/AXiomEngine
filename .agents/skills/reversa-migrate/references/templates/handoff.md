```
schemaVersion: 1
generatedAt: <ISO-8601>
reversa:
  version: "x.y.z"
kind: handoff
producedBy: orchestrator
hash: "sha256:<hash of the body below the front-matter>"
---

# Handoff for the Coding Agent

> This document serves as the entry point for the coding agent (Claude Code, Codex, Cursor, Antigravity, etc.) that will develop the new system based on the specifications.

## ⚠️ Mandatory Reading First

1. **`paradigm_decision.md`**, non-negotiable reading. The target paradigm shapes how all coding should be done.
2. **`topology_decision.md`**, non-negotiable reading. The chosen topology (preserve/modernize/hybrid) defines the folder tree and the boundaries between modules.
3. **`screen_modernization_decision.md`**, non-negotiable reading when the legacy system has a UI. The chosen mode (literal/modernized/hybrid) defines how the coder will materialize the screens.

## Recommended Reading Order

1. `paradigm_decision.md` (mandatory, first)
2. `topology_decision.md` (mandatory, second)
3. `screen_modernization_decision.md` (mandatory when there's a UI; skip if the Screen Translator ran in skipped mode)
4. `migration_brief.md`
5. `target_business_rules.md`
6. `migration_strategy.md`
7. `target_architecture.md`
8. `target_domain_model.md`
9. `target_data_model.md`
10. `data_migration_plan.md`
11. `target_screens.md` (when there's a UI)
12. `parity_specs.md` + `parity_tests/`
13. `screen_deviation_log.md` (for reference, when there's a UI)
14. `risk_register.md` + `cutover_plan.md`
15. `discard_log.md` (for reference)
16. `ambiguity_log.md` (for reference)

## List of Produced Artifacts

| Artifact                    | Produced By       | Status   |
| --------------------------- | ----------------- | -------- |
| `migration_brief.md`        | `orchestrator`    | created  |
| `paradigm_decision.md`      | `paradigm_advisor` | created  |
| `target_business_rules.md`  | `curator`         | created  |
| `discard_log.md`            | `curator`         | created  |
| `migration_strategy.md`     | `strategist`      | created  |
| `risk_register.md`          | `strategist`      | created  |
| `cutover_plan.md`           | `strategist`      | created  |
| `topology_decision.md`     | `designer (Phase 1)` | created  |
| `target_architecture.md`    | `designer`        | created  |
| `target_domain_model.md`    | `designer`        | created  |
| `target_data_model.md`      | `designer`        | created  |
| `data_migration_plan.md`    | `designer`        | created  |
| `screen_modernization_decision.md` | `screen_translator (Phase 1)` | created / skipped |
| `target_screens.md`         | `screen_translator` | created / skipped |
| `screen_deviation_log.md`   | `screen_translator` | created / empty |
| `_reversa_sdd/screens/inventory.json` | `screen_translator` | created / empty |
| `_reversa_sdd/screens/golden/manifest.yaml` | `screen_translator` | created / optional |
| `parity_specs.md`           | `inspector`       | created  |
| `parity_tests/*.feature`   | `inspector`       | <N> files |
| `ambiguity_log.md`          | `orchestrator`    | consolidated |

## Blocking Issues Before Implementation Can Start
> Items that require human decision before the coding agent starts.

- <AMB-XXX: short description + where to decide>
- <or: no blocking issues, proceed>

## Next Steps for the Coding Agent

1. **Read `paradigm_decision.md` and internalize**: the target paradigm is <from `paradigm_decision.md`>. All code choices must adhere to this paradigm.
2. **Read `topology_decision.md` and internalize**: the chosen topology is <preserve | modernize | hybrid>. Use the outline of the tree recorded in this artifact as the basis for creating the folder structure of the new repository.
3. **Read `screen_modernization_decision.md` and internalize** (when there's a UI): the screen translation mode is <literal | modernized | hybrid>. In literal mode, materialize the contents of `target_screens.md` byte-by-byte (or pixel-equivalent); in modernized mode, adhere to the component hierarchy, tokens, and the 4 states (idle, loading, error, success).
4. **Set up the new repository** with the stack declared in `migration_brief.md` and the decided topology.
5. **Implement bottom-up** following `target_architecture.md` and `target_domain_model.md`:
    - infrastructure → data → domain → application → edges.
6. **Implement the screens** using `target_screens.md` as the literal contract. In literal mode with golden files present in `_reversa_sdd/screens/golden/`, the result of the implementation should match the golden file within the `normalizationRules` declared in `manifest.yaml`.
7. **Write the tests** based on `parity_specs.md` and `parity_tests/*.feature` from the start. Adhere to the § Exceptions section, which reflects the approved deviations in `screen_deviation_log.md`.
8. **For each component**, validate that it respects the chosen paradigm (explicit signals in `target_architecture.md § Adherence to the chosen paradigm`) and the chosen topology (explicit signals in `target_architecture.md § Adherence to the chosen topology`).
9. **For the data migration**, follow `data_migration_plan.md`.
10. **For the cutover**, follow `cutover_plan.md` and the go/no-go criteria.

## Items Auto-Decided (only if run in --auto mode)
> List here items whose default was applied without human confirmation. Recommended to review before the cutover.

- <or: the pipeline ran in interactive mode, no items were auto-decided>

## Final Notes
<Observations from the orchestrator for the coding agent.>
```