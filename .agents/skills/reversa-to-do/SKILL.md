```markdown
---
name: reverse-to-do
description: Decomposes the roadmap into atomic actions with sequential IDs, dependencies, and a parallelism marker. Use when the user types "/reverse-to-do", "reverse-to-do", "decompose into tasks", or asks to turn the roadmap into an executable list. This is the fourth skill in the forward cycle, following `/reverse-plan`.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reverse
  phase: forward
  stage: to-do
---

You are the decomposer. Your mission is to transform `roadmap.md` into an executable `actions.md`, with atomic tasks, stable IDs, and clear marking indicating what can run in parallel.

## Before You Begin

1.  Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`.
2.  Use the actual values in places where the text mentions `_reversa_sdd/` or `_reversa_forward/`.

## Initial Checks

1.  Read `.reversa/active-requirements.json`.
    1.1. If absent, abort and point to `/reversa-requirements`.
2.  Verify the existence of `feature-dir/roadmap.md`.
    2.1. If absent, abort with a clear message pointing to `/reversa-plan`. Do not attempt to fill in the roadmap here.
3.  Also load `feature-dir/data-delta.md` and `feature-dir/interfaces/*` if they exist.
4.  Apply `before-to-do` in the standard way.

## Decomposition Strategy

1.  Use the five standard phases in order:
    1.1. Preparation (setup, scaffolding, initial migrations, configuration).
    1.2. Tests (tests that need to exist before or shortly after the core, if the team practices TDD).
    1.3. Core (central logic of the feature).
    1.4. Integration (glue with other parts of the system, external contracts, hooks).
    1.5. Polishing (logs, telemetry, messages, short documentation).
2.  For each item in `roadmap.md`, derive one or more actions.
3.  Break down each action to the point where it can be executed in a single, coherent block, without needing to switch subjects.
4.  Assign ID `T001`, `T002`, ..., zero-padded to three digits.
5.  Mark with `[//]` at the beginning of the line for tasks that touch different files AND do not depend on each other.
6.  In an explicit column, record dependencies by ID (e.g., `T005 depends on T001, T003`).
7.  In an explicit column, record the main target file (e.g., `src/payments/pdf.js`).
8.  In the `confidence` column, inherit 🟢 / 🟡 / 🔴 from the corresponding decision in the roadmap.

## Criteria for "Atomic"

-   An action is atomic when it can be completed by an agent in one turn, without needing human feedback in the middle.
-   If an action has more than five logical sub-items, break it down.
-   If an action touches more than three unrelated files, break it down.
-   If an action includes "and also", "then", "next", break it down.

## Constructing `actions.md`

1.  Load the template `.reversa/templates/actions-template.md`.
2.  For each phase, create a table with columns: `ID | Description | Dependencies | Parallelism | Target File | Confidence | Status`.
3.  The Status always starts as `[ ]`.
4.  Before the first table, include a summary:
    4.1. Total number of actions.
    4.2. Total number of parallelizable actions.
    4.3. Longest dependency chain.

## Maintenance Rules

-   IDs are never recycled, even if an action is removed in a later review.
-   Renumbering only occurs when the document is generated for the first time.
-   Never insert actions for "configuring IDE", "running lint", "opening PR"; this is not the responsibility of Reversa.

## Persistence

-   Write `feature-dir/actions.md` with atomic writing.

## Post-Execution Hooks

-   Apply `after-to-do` in the standard way.

## Final Report

1.  Absolute path to `actions.md`.
2.  Total number of actions per phase.
3.  Total number marked with `[//]`.
4.  Suggestion for the next step, in order:
    4.1. `/reversa-audit` if you noticed an inconsistency during decomposition.
    4.2. `/reversa-coding` otherwise.

Finish with:

> Type **CONTINUE** to proceed as suggested above.
```