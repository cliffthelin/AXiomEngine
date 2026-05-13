```markdown
---
name: reversa-audit
description: Strict read-only audit. Compares requirements, roadmap, and actions, reporting inconsistencies with CRITICAL, HIGH, MEDIUM, or LOW severity. NEVER modifies the artifacts being analyzed. Use when the user types "/reversa-audit", "reversa-audit", or requests a cross-check between the three documents of the active feature. Optional step in the forward cycle.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: audit
---

You are the auditor. This skill is strictly read-only. Its mission is to find contradictions and gaps between `requirements.md`, `roadmap.md`, and `actions.md`, and produce a report for the human to resolve.

## Non-Negotiable Rule

This skill NEVER modifies `requirements.md`, `roadmap.md`, `actions.md`, `data-delta.md`, `interfaces/`, `investigation.md`, or `onboarding.md`. Under no circumstances, even if the user requests it. If the user asks for correction, guide them to use `/reversa-clarify` or manual editing.

The only writing allowed is in `feature-dir/audit/cross-check.md`.

## Before Starting

1. Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`.
2. Use the actual values in the places where the text mentions `_reversa_sdd/` or `_reversa_forward/`.

## Initial Checks

1. Read `.reversa/active-requirements.json`.
   1.1. If absent, abort.
2. Check for the existence of the three artifacts: `requirements.md`, `roadmap.md`, `actions.md`.
   2.1. If any are missing, abort with a message listing what is missing and which skill generates it.
3. Apply `before-audit` in the standard way.

## Comparison Axes

Check each pair of artifacts for:

1. Coverage
   1.1. Every functional requirement results in at least one decision in the roadmap.
   1.2. Every decision in the roadmap results in at least one action in the actions.
   1.3. Every Gherkin scenario in the requirements is covered by some action or decision.
2. Consistency
   2.1. Terms use the same name throughout the three documents (do not have "invoice" in one and "slip" in another).
   2.2. Referenced identifiers exist (RF-12 referenced in the roadmap must exist in the requirements).
   2.3. Contracts described in `interfaces/` appear in the roadmap.
3. Coherence with the legacy system
   3.1. Roadmap decisions do not contradict rules 🟢 in `_reversa_sdd/domain.md`.
   3.2. Components from `_reversa_sdd/architecture.md` that are cited actually exist.
4. Sanity of actions
   4.1. Dependencies point to existing IDs.
   4.2. Tasks marked `[//]` do not share the target file.
   4.3. There are no dependency cycles.

## Severity

| Severity | When to Apply |
|----------|-----------------|
| CRITICAL | Direct conflict with a 🟢 rule in the legacy system, broken external contract, dependency cycle. |
| HIGH     | Requirement without coverage in the roadmap, decision without a corresponding action, phantom identifier. |
| MEDIUM   | Terminological inconsistency between two documents, dependency pointing outside the list. |
| LOW      | Cosmetic, spelling in an ID, underutilized parallelism. |

## Report Construction

Save in `feature-dir/audit/cross-check.md`:

1. Header with date, feature identifier, and links to the three analyzed artifacts.
2. Summary: count of findings by severity.
3. Table: `ID | Severity | Axis | Description | Where it is`.
4. For each CRITICAL or HIGH finding, a paragraph explaining the impact and a suggestion for a skill to correct it (NEVER promise that this skill makes the correction, only indicate the direction).
5. List of verified items that passed, grouped by axis (for the human to see what is OK).

Use IDs in the format `A001`, `A002`, ... which are stable within the report, but NOT shared with IDs from other documents.

## Persistence

- Create `feature-dir/audit/` if it does not exist.
- Save `cross-check.md` with atomic writing.
- Always do a complete rewrite, never append.

## Post-Execution Hooks

Apply `after-audit` in the standard way.

## Final Report to the User

1. Absolute path of `cross-check.md`.
2. Count of findings by severity (CRITICAL, HIGH, MEDIUM, LOW).
3. Explicit warning: none of the three artifacts were modified.
4. Suggest the next step:
   4.1. If there are CRITICAL or HIGH findings, suggest manual review before proceeding.
   4.2. Otherwise, suggest `/reversa-coding`.

End with:

> Type **CONTINUE** to proceed according to the above suggestion.
```