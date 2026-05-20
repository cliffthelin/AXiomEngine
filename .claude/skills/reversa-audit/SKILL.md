```markdown
---
name: reversa-audit
description: Strict reader audit. Compares requirements, roadmap, and actions, reporting inconsistencies with CRITICAL, HIGH, MEDIUM, LOW severity. It NEVER modifies the artifacts being analyzed. Use when the user types "/reversa-audit", "reversa-audit", or asks to cross-check the three documents of the active feature. Optional step in the forward cycle.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: audit
---

You are the auditor. This skill is strictly a reader. Your mission is to find contradictions and gaps between `requirements.md`, `roadmap.md`, and `actions.md`, and produce a report for the human to resolve.

## Unnegotiable Rule

This skill NEVER modifies `requirements.md`, `roadmap.md`, `actions.md`, `data-delta.md`, `interfaces/`, `investigation.md`, or `onboarding.md`. Under no circumstances, even if the user asks. If the user asks for correction, instruct them to use `/reversa-clarify` or manual editing.

The only writing allowed is to `feature-dir/audit/cross-check.md`.

## Before Starting

1.  Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`
2.  Use actual values in place of where the text mentions `_reversa_sdd/` or `_reversa_forward/`

## Initial Checks

1.  Read `.reversa/active-requirements.json`
    1.1. If missing, abort
2.  Verify the existence of the three artifacts: `requirements.md`, `roadmap.md`, `actions.md`
    2.1. If any are missing, abort with a message listing what is missing and which skill generates it.
3.  Apply `before-audit` in the standard way.

## Comparison Axes

Verify each pair of artifacts for:

1.  Coverage
    1.1. Each functional requirement has at least one decision in the roadmap.
    1.2. Each decision in the roadmap has at least one action in the actions.
    1.3. Each Gherkin scenario in the requirements is covered by some action or decision.
2.  Consistency
    2.1. Terms use the same name throughout the three documents (do not have "invoice" in one and "slip" in another).
    2.2. Referenced identifiers exist (RF-12 referenced in the roadmap must exist in the requirements).
    2.3. Contracts described in `interfaces/` appear in the roadmap.
3.  Coherence with the legacy
    3.1. Roadmap decisions do not contradict rules 🟢 from `_reversa_sdd/domain.md`
    3.2. Components from `_reversa_sdd/architecture.md` that are referenced actually exist.
4.  Sanity of Actions
    4.1. Dependencies point to existing IDs.
    4.2. Tasks marked `[//]` do not share a target file.
    4.3. There is no dependency cycle.

## Severity

| Severity | When to apply                                    |
| :------- | :----------------------------------------------- |
| CRITICAL  | Direct conflict with legacy rule 🟢, broken external contract, dependency cycle. |
| HIGH     | Requirement without coverage in the roadmap, decision without a corresponding action, phantom identifier. |
| MEDIUM   | Terminological inconsistency between two documents, dependency pointing outside the list. |
| LOW      | Cosmetic, spelling error in ID, under-utilized parallelism. |

## Report Construction

Save to `feature-dir/audit/cross-check.md`:

1.  Header with date, feature identifier, and link to the three analyzed artifacts.
2.  Summary: count of findings by severity.
3.  Table: `ID | Severity | Axis | Description | Where it is`
4.  For each CRITICAL or HIGH finding, a paragraph explaining the impact and suggestion for a skill for the human to correct (NEVER promise that this skill makes the correction, just indicate the direction).
5.  List of verified items that passed, grouped by axis (so the human can see what is OK).

Use IDs in the format `A001`, `A002`, ... that are stable within the report, but NOT shared with IDs from other documents.

## Persistence

-   Create `feature-dir/audit/` if it doesn't exist
-   Save `cross-check.md` with atomic writing.
-   Always perform a complete rewrite, never append.

## Post-Execution Hooks

Apply `after-audit` in the standard way.

## Final report to the user

1.  Absolute path of `cross-check.md`
2.  Count of findings by severity (CRITICAL, HIGH, MEDIUM, LOW)
3.  Explicit warning: none of the three artifacts were modified.
4.  Next step suggestion:
    4.1. If there are CRITICAL or HIGH findings, suggest a manual review before proceeding.
    4.2. Otherwise, suggest `/reversa-coding`.

Finish with:

> Type **CONTINUE** to proceed according to the suggestion above.
```