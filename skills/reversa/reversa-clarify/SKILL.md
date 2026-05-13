```markdown
---
name: reversa-clarify
description: Generates up to five targeted questions to resolve ambiguities in the requirements and integrates the answers into the document. Use when the user types "/reversa-clarify", "reversa-clarify", "clarify doubts", or asks to address open points in the requirements before planning. Optional step in the forward cycle, between `/reversa-requirements` and `/reversa-plan`.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: clarify
---

You are the clarifier. Your mission is to identify what information is missing before the planning phase and return the answers to the `requirements.md` file of the active feature.

## Before You Begin

1.  Read the `.reversa/state.json` file to determine `output_folder` (reverse extraction) and `forward_folder` (forward features).
2.  Whenever this skill mentions `_reversa_sdd/` or `_reversa_forward/`, use the actual values from the `state.json` file.

## Initial Checks

1.  Read the `.reversa/active-requirements.json` file.
    1.1. If the file does not exist, abort with a clear message guiding the user to `/reversa-requirements`.
2.  Load the `requirements.md` file from the indicated `feature-dir`.
3.  Apply the default hook rule `before-clarify` read from `.reversa/hooks.yml` (same logic as the `reversa-requirements` skill).

## Question Generation

1.  Examine the `requirements.md` file for:
    1.1. Explicit `[DÚVIDA]` markers.
    1.2. Vague phrases ("probably", "maybe", "if possible", "some").
    1.3. Open terms with no definition (numerical limits, user profiles, expected formats).
    1.4. Obvious coverage gaps (missing negative scenario, implicit edge case).
2.  Cross-reference with the internal taxonomy below to select candidates.
3.  Select a maximum of five questions, ranked by their impact on the plan.
4.  Each question should be either multiple choice or short answer, never open-ended without options.

### Taxonomy for Prioritization

1.  Functional scope and behavior.
2.  Domain model and data.
3.  Interaction flow and experience.
4.  Non-functional attributes (performance, security, observability).
5.  Integrations and external dependencies.
6.  Permissions and authentication.
7.  Data persistence and migration.
8.  Auditing, logging, and telemetry.
9.  Internationalization and localization.
10. Failures and recovery.
11. Compatibility with the legacy system mapped in `_reversa_sdd/`.

## Presentation to the User

Present the questions in the following format:

```
1. <question>
   a) <option>
   b) <option>
   c) <option>
   d) <option>
   e) Free-form answer

2. ...
```

If a question is a short answer, omit the options block and use the format `Expected answer: <hint of the type of value>`.

Wait for the user to respond. If they only answer some questions, proceed only with the answered ones.

## Integration into requirements.md

1.  Locate or create the `## Esclarecimentos` section.
2.  Within it, create or update `### Sessão YYYY-MM-DD`.
3.  For each answered question:
    3.1. Add an item in the format `- **Q:** <question>` followed by `**R:** <answer>`.
    3.2. Locate the section of the requirements document where the doubt existed.
    3.3. Rewrite the section in place, removing the corresponding `[DÚVIDA]` marker.
4.  Update the `## Lacunas` section, removing resolved entries and keeping unresolved ones.

## Persistence

-   Atomically save the modified `requirements.md` file.
-   The `## Esclarecimentos` section should appear immediately before the `## Lacunas` section.

## Post-Execution Hooks

Apply the default rule for `after-clarify` (same logic as the `reversa-requirements` skill).

## Final Report

1.  Absolute path of the `requirements.md` file.
2.  Number of doubts resolved in this session.
3.  Number of remaining `[DÚVIDA]` markers.
4.  Suggestion for the next step:
    4.1. If there are still `[DÚVIDA]` markers, suggest another execution of `/reversa-clarify`.
    4.2. If there are none, suggest `/reversa-plan`.

Finish with:

> Type **CONTINUAR** to proceed with the suggestion above.
```