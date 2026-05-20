### SOURCE:
# `--auto` Defaults

When the user invokes `/reversa-migrate --auto`, the orchestrator skips human pauses and applies these defaults. Before starting, a warning is displayed to the user listing each of them. Each auto-applied item is logged in `ambiguity_log.md` with the tag `auto-decided` for later review.

## Paradigm Advisor
- Choose **option 1: adopt the natural paradigm of the target stack**.
- `derived_appetite` = `transformational`.

## Curator
- Items requiring HUMAN DECISION are marked as pending in `ambiguity_log.md` and do not block the pipeline.
- Items 🟡 INFERRED → MIGRATE (with note "validate in the code generation agent").
- Items 🔴 GAP and ⚠️ AMBIGUOUS → DISCARD with explicit note "auto-discarded, requires review."

## Strategist
- Adopts the strategy marked as **recommended**.
- Risks with `critical` severity that would depend on a human owner remain with `owner = "to be defined"` in `risk_register.md`.

## Designer
- **Topology (Phase 1)**: accepts the proposed modern topology (option 2). Justification logged in `topology_decision.md` is the Designer's own; the `auto-decided` tag is added to `ambiguity_log.md` for later review. Rationale: `--auto` is for users who want the recommended path; refusing to decide would stop the pipeline and violate the `--auto` contract.
- **Architecture (Phase 2)**: approves the first proposal without iteration.
- Bounded contexts, events, and ADRs are accepted as proposed.

## Screen Translator
- **Mode (Phase 1)**: adopts the mode recommended by the agent for the detected source→target pair (literal for text pairs; modernized for platform changes; hybrid only with an explicit listing, therefore never in `--auto`).
- **Generation (Phase 2)**: accepts the generated `target_screens.md` and propagates deviations as `pending`. `--auto` does not approve deviations on its own; they are placed in `ambiguity_log.md` as `auto-decided` for later review, without blocking the handoff (exception to `--auto`: if a deviation is `type=correction` in literal mode, the agent refuses and requests human approval even in `--auto`, because changing text without review is unacceptable).
- **Golden files capture**: does not automate in `--auto` (oracle driver is OQ-02). It only outputs `manifest.yaml` with suggested commands.
- **Legacy without UI**: automatically marks the status as `skipped`, without prompting.
- **Missing Discovery Prerequisites** (`_reversa_sdd/design-system/` or `_reversa_sdd/ui/inventory.md`): creates a minimal `tokens-derived.md` and builds the inventory only from the source code; alerts in `ambiguity_log.md`.

## Inspector
- Uses parity criteria derived directly from the chosen paradigm (see `parity-coverage-matrix.md` in the agent).
- Does not negotiate the "accepted parity" criterion with the user.

## Detected manual modifications
- Adopts **option (a)**: preserve the manually modified version and abort regeneration of that artifact. Never destroys human work.

## Mandatory warning

Always before starting `--auto`, display:

> "⚠️ `--auto` mode activated. The following defaults will be applied without a pause for confirmation:
> - Paradigm Advisor: adopt the natural paradigm of the stack (transformational).
> - Curator: ⚠️/🔴 items will be DISCARDED with a note; 🟡 items will be MIGRATED with a note.
> - Strategist: the recommended strategy will be adopted.
> - Designer (topology): the proposed modern topology will be adopted (option 2).
> - Designer (architecture): the first architecture proposal will be accepted.
> - Screen Translator (mode): adopts the recommended mode for the source→target pair. Hybrid mode never in `--auto`. In legacy without UI, status `skipped`.
> - Screen Translator (generation): deviations will be pending in `ambiguity_log.md` (not approved). Golden files capture not automated (only manifest).
> - Inspector: parity criteria derived from the paradigm, without interactive adjustment.
>
> The final `handoff.md` will highlight all auto-decided items for later review.
> Confirm? (y/N)"
