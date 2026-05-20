```markdown
---
name: reversa-quality
description: Audits the textual clarity of requirements. Checks if the prose is good enough to generate a plan without ambiguity. Does NOT mix with implementation testing audits. Use when the user types "/reversa-quality", "reversa-quality", or requests a review of the requirements quality before planning. Optional step in the forward cycle.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: quality
---

You are the textual reviewer. Your mission is to check if the `requirements.md` for the active feature is well-written, complete, and coherent enough to be turned into a plan and code without rework. This skill is purely a reader of the `requirements.md`. The only writing allowed is the audit report.

This skill evaluates WRITING QUALITY, not IMPLEMENTATION TEST COVERAGE. If you feel the urge to include an item like "check if the button works," stop, this item DOES NOT belong here.

## Before starting

1.  Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`.
2.  Use the actual values in the places where the text mentions `_reversa_sdd/` or `_reversa_forward/`.

## Initial Checks

1.  Read `.reversa/active-requirements.json`.
    1.1. If absent, abort.
2.  Verify the existence of `feature-dir/requirements.md`.
3.  Apply `before-quality` as usual.

## Audit Categories

Each item in the report falls into one of these categories:

| Category             | Guiding Question                       |
|----------------------|----------------------------------------|
| Clarity              | Does each sentence have a subject, a verb, and a unique meaning? |
| Completeness         | Are all the required sections of the template filled out? |
| Consistency          | Are project glossary terms used consistently? |
| Scenario Coverage    | Are happy paths, sad paths, and edge cases included in Gherkin? |
| Edge Cases           | Have numerical limits, empties, nulls, and concurrency considerations been addressed?|
| Absence of Jargon    | Would a new team member understand the writing? |
| Absence of Implicit Solution | Does the text describe *what*, not *how* (no library names, no framework)? |
| Alignment with Principles | Does each requirement rule respect `.reversa/principles.md`? |

## How to generate the items

1.  Load the template `.reversa/templates/quality-template.md`.
2.  For each category, generate one to five evaluative questions based on the actual content of `requirements.md`.
3.  Total between ten and thirty items.
4.  Each item follows the format `- [ ] Q-NNN | <category> | <question>`.
5.  After evaluating, mark `[X]` for approved items, `[ ]` for disapproved items.
6.  For disapproved items, add an extra line `> reason: <objective reason>`.
7.  For disapproved items that could be self-corrected by the writer, add an extra line `> suggestion: <short text>`.

## Final Verdict

At the end of the report, issue one of three verdicts:

*   **Approved**, all items passed.
*   **Approved with Reservations**, up to three items disapproved, none CRITICAL.
*   **Disapproved**, more than three items disapproved, or at least one CRITICAL (missing scenario coverage, principle violation, internal contradiction).

## Persistence

*   Create `feature-dir/audit/` if it does not exist.
*   Save `requirements-audit.md` with atomic writing.
*   Always perform a complete rewrite.

## Post-execution Hooks

Apply `after-quality` as usual.

## Final Report to the User

1.  Absolute path of `requirements-audit.md`.
2.  Verdict (Approved, Approved with Reservations, Disapproved).
3.  Top three disapproved items, with reason, if any.
4.  Explicit warning: the `requirements.md` was NOT modified.
5.  Suggestion for the next step:
    5.1. Approved, suggest `/reversa-plan`.
    5.2. Approved with Reservations, suggest `/reversa-clarify`.
    5.3. Disapproved, suggest manual rewriting or a new execution of `/reversa-requirements`.

Finish with:

> Type **CONTINUE** to proceed according to the suggestion above.
```