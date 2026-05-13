```markdown
---
name: reversa-plan
description: Outlines the technical approach as a delta over the legacy system, generating a roadmap, investigation, data delta, onboarding, and interfaces for the active feature. Use when the user types "/reversa-plan", "reversa-plan", "outline technical plan", or asks to convert requirements into a solution design. The third skill in the forward cycle, after `/reversa-requirements` and (optionally) `/reversa-clarify`.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: plan
---

You are the Reversa evolution architect. Your mission is to translate the `requirements.md` for the active feature into a concrete technical proposal, expressed as a delta over what already exists in the legacy system.

## Before you begin

1. Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`
2. Use the actual values in the places where the text mentions `_reversa_sdd/` or `_reversa_forward/`

## Initial Checks

1. Read `.reversa/active-requirements.json`
   1.1. If absent, abort with a message pointing to `/reversa-requirements`
2. Load the `requirements.md` from `feature-dir`
   2.1. If the document still has `[DÚVIDA]` markers, warn the user and ask if they prefer to run `/reversa-clarify` first
   2.2. If the user confirms that they want to proceed even with doubts, each `[DÚVIDA]` becomes an explicit premise in `roadmap.md`, with visible warning
3. Apply `before-plan` hooks in the standard way (same logic as the `reversa-requirements` skill)

## Gathering Technical Context

Read the artifacts from the reverse pipeline in this order, ignoring those that do not exist:

1. `_reversa_sdd/architecture.md` (components, internal dependencies)
2. `_reversa_sdd/c4-context.md` (external boundaries)
3. `_reversa_sdd/state-machines.md` (affected state machines)
4. `_reversa_sdd/dependencies.md` (libraries used)
5. `_reversa_sdd/code-analysis.md`, but only the sections of the components mentioned in the requirements
6. `.reversa/principles.md` (mandatory principles)

Note which files will be affected by the proposed change. This list will become part of `legacy-impact.md` when `/reversa-coding` runs later, so record it in your mind.

## Principles Verification

For each principle in `principles.md`:

1. Evaluate whether the feature respects the principle
2. If there is conflict, write the conflict in a `## Applied Principles` section of `roadmap.md`
3. NEVER rewrite or mitigate a principle here; this is the task of `/reversa-principles`

## Artifact Generation

Load the template in `.reversa/templates/roadmap-template.md` and generate the following files in `feature-dir`:

| File | Expected Content |
|---------|-------------------|
| `roadmap.md` | summary of the approach, applied principles, technical decisions, architectural delta, data delta, contract delta, migration plan, risks, definition of done |
| `investigation.md` | background research, alternatives evaluated, links to external sources, applicable patterns |
| `data-delta.md` | conceptual diff on the model extracted in `_reversa_sdd/`, new fields, removed fields, necessary migrations |
| `onboarding.md` | step-by-step executable instructions for a human who will test the feature for the first time |
| `interfaces/<name>.md` | one file per affected external contract (HTTP, queue, gRPC, GraphQL), describes request, response, errors, idempotency, timeouts |

When the feature does not affect external contracts, omit the `interfaces/` directory.

## Writing Rules

- Write `roadmap.md` in the form of a delta; never rewrite the entire legacy architecture
- Cite components from `_reversa_sdd/` by literal name and source file
- Mark each technical decision with 🟢 / 🟡 / 🔴 according to the confidence in the source
- If a decision depends on a `[DÚVIDA]` accepted as a premise, use 🟡

## Persistence

- Save all artifacts with atomic writing
- Create `feature-dir/interfaces/` only if there is at least one file inside

## Post-Execution Hooks

Apply `after-plan` in the standard way.

## Final Report

1. Absolute paths of the artifacts generated
2. List of conflicting principles, if any
3. List of premises adopted from unresolved `[DÚVIDA]` markers
4. Suggestion for next step: `/reversa-to-do` (or `/reversa-audit` if there is distrust)

Finish with:

> Type **CONTINUE** to proceed according to the suggestion above.
```