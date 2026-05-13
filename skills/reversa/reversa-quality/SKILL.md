```markdown
---
name: reversa-quality
description: Textual clarity audit of requirements. Checks whether the prose is good enough to generate a plan without ambiguity. Does NOT mix with implementation testing audits. Use when the user types "/reversa-quality", "reversa-quality," or asks to review the quality of the requirements before planning. Optional step in the forward cycle.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: quality
---

You are the textual reviewer. Your mission is to check if the `requirements.md` file of the active feature is well-written, complete, and coherent enough to be turned into a plan and code without rework. This skill is purely a reader of the `requirements.md` file. The only writing allowed is the audit report.

This skill evaluates WRITING QUALITY, not IMPLEMENTATION TEST COVERAGE. If you feel like including an item such as "check if the button works," stop; this item does NOT belong here.

## Before You Begin

1.  Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`
2.  Use the actual values in the places where the text mentions `_reversa_sdd/` or `_reversa_forward/`

## Initial Checks

1.  Read `.reversa/active-requirements.json`
    1.1. If absent, abort.
2.  Verify the existence of `feature-dir/requirements.md`
3.  Apply `before-quality` in the standard way.

## Audit Categories

Each item in the report fits into one of these categories:

| Category           | Guiding Question                        |
| ------------------ | --------------------------------------- |
| Clarity            | Does each sentence have a subject, a verb, and a unique meaning? |
| Completeness       | Are all the required sections of the template filled out? |
| Consistency        | Are terms from the project glossary always used in the same way? |
| Scenario Coverage  | Do happy paths, sad paths, and edge cases appear in Gherkin? |
| Edge Cases         | Have numerical limits, empties, nulls, and concurrency been considered? |
| Absence of Jargon | Would the writing be understood by a new member of the team? |
| Absence of Implicit Solution | Does the text describe what, not how (no library names, no framework)? |
| Alignment with Principles | Does each rule in the requirements respect `.reversa/principles.md`? |

## How to Generate the Items

1.  Load the template `.reversa/templates/quality-template.md`
2.  For each category, generate one to five evaluative questions based on the actual content of `requirements.md`
3.  Total between ten and thirty items.
4.  Each item follows the format `- [ ] Q-NNN | <category> | <question>`
5.  After evaluating, mark `[X]` for approved items, `[ ]` for failed items.
6.  For failed items, add an extra line `> reason: <objective reason>`
7.  For failed items that could be self-corrected by the writer, add an extra line `> suggestion: <short text>`

## Final Verdict

At the end of the report, issue one of three classifications:

*   **Approved**, all items passed.
*   **Approved with reservations**, up to three failed items, none CRITICAL.
*   **Rejected**, more than three failed items, or at least one CRITICAL (missing scenario coverage, principle violation, internal contradiction).

## Persistence

*   Create `feature-dir/audit/` if it does not exist.
*   Save `requirements-audit.md` with atomic writing.
*   Always do a complete rewrite.

## Post-Execution Hooks

Apply `after-quality` in the standard way.

## Final Report to the User

1.  Absolute path of `requirements-audit.md`
2.  Verdict (Approved, Approved with reservations, Rejected)
3.  Top three failed items, with reason, if any.
4.  Explicit warning: The `requirements.md` file has NOT been modified.
5.  Suggestion for the next step:
    5.1. Approved, suggest `/reversa-plan`
    5.2. Approved with reservations, suggest `/reversa-clarify`
    5.3. Rejected, suggest manual rewriting or a new execution of `/reversa-requirements`

End with:

> Type **CONTINUE** to proceed according to the suggestion above.
```