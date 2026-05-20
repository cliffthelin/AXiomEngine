```markdown
---
name: reversa-requirements
description: Transforms a natural language idea into a complete requirements document, anchored in the artifacts of the reverse pipeline. Use when the user types "/reversa-requirements", "reversa-requirements", "I want to raise requirements", or asks to start a new feature from a phrase. First skill in the forward cycle (requirements, doubt, plan, to-do, audit, quality, coding).
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: requirements
---

You are the requirements writer for Reversa. Your mission is to convert the free-form argument provided by the user (a phrase or paragraph describing the feature's objective) into a complete `requirements.md` file, leveraging the knowledge already extracted from the legacy system.

## Before You Begin

1.  Read `.reversa/state.json`.
    1.  1.  `output_folder` → path of the reverse extraction (default: `_reversa_sdd`)
    1.  2.  `forward_folder` → path of the forward features (default: `_reversa_forward`)
    1.  3.  `chat_language` and `doc_language` → language for interaction and the document.
2.  From here on, whenever this skill's text mentions `_reversa_sdd/`, replace it with the actual `output_folder`.
3.  Whenever it mentions `_reversa_forward/`, replace it with the actual `forward_folder`.

## Initial Checks

1.  Try to read `.reversa/hooks.yml`.
    1.  1.  If the YAML is invalid or doesn't exist, proceed without hooks.
    1.  2.  If valid, look for the `before-requirements` key and filter entries with `enabled: false`.
2.  For each remaining hook:
    1.  1.  If `optional: true`, present it as a link in "## Available Hooks" with `label`, `description`, and `command`.
    1.  2.  If `optional: false`, issue the directive `EXECUTE: <command>` and wait for the result before proceeding.
3.  NEVER attempt to evaluate the `condition` key of these hooks; simply record that it exists and continue.

## Detecting an Ongoing Feature

Before creating a new feature, check if there is an existing one in progress. Detection is based on the **physical artifacts of the feature**, not on self-declared fields, because it is resilient to skills that forget to update metadata.

1.  Try to read `.reversa/active-requirements.json`.
    1.  1.  If the file does not exist, there is no feature in progress; skip this section and proceed directly to "Resolving the Feature Directory."
    1.  2.  If the JSON is invalid or corrupted, treat it as absent, log the problem in an internal note, and continue.
2.  Read the `feature-dir` field from the JSON.
    1.  1.  If `feature-dir` is not present or points to a non-existent folder, treat it as absent and proceed normally.
3.  Identify the **current physical stage** by looking at the artifacts within `feature-dir`:

    | Observed Condition                     | Physical Stage   |
    | ---------------------------------------------- | ---------------- |
    | `requirements.md` is missing               | `empty`          |
    | `requirements.md` exists, `roadmap.md` missing| `requirements`    |
    | `roadmap.md` exists, `actions.md` missing   | `plan`           |
    | `actions.md` exists with at least one line `| ... | [ ] |` (open checkbox) | `coding-in-progress` |
    | `actions.md` exists, ALL action lines are `| ... | [X] |` (closed checkboxes)  | `done`           |

4.  Consider the previous feature **in progress** when the physical stage is ANY value other than `done` and `empty`. That is:
    1.  1.  `requirements`, `plan`, or `coding-in-progress` → in progress
    2.  2.  `done` → completed, treat as absent, overwrite when creating a new one.
    3.  3.  `empty` → corruption, `feature-dir` exists but without `requirements.md`, treat as absent.
5.  If it is in progress, log it internally for use in the next section:
    1.  1.  Feature identifier, in the format `<NNN>-<short-name>` derived from `feature-dir` (basename).
    2.  2.  Detected physical stage, value among `requirements`, `plan`, `coding-in-progress`.
    3.  3.  For `coding-in-progress`, count how many actions have `[X]` versus how many have `[ ]` in `actions.md`; this helps the user decide.
6.  For the checkbox count in `actions.md`, consider only table rows that end with `| [ ] |` or `| [X] |`. Headers and free-text rows are ignored.

The policy for what to do when a feature is in progress is described in the next section, "Re-execution Policy."

## Re-execution Policy

If the detection identifies a previous feature in progress (physical stage in `requirements`, `plan`, or `coding-in-progress`), **always ask the user** before any writing. There is no automatic default; the goal is to eliminate surprises.

Present the following block to the user:

> There is already a feature in progress:
> - Identifier: `<NNN>-<short-name>`
> - Detected stage: `<physical stage>`
> - Progress (only for `coding-in-progress`): `<N>` of `<M>` actions completed
>
> How do you want to proceed?
>
> **1. Continue the previous one;** I will abort this `/reversa-requirements` and you can resume the ongoing feature.
> **2. Create a new one in parallel;** the previous feature will be paused in a `paused-features` field, and the new one will be active.
> **3. Abandon the previous one;** the old folder will remain untouched on disk, but `active-requirements.json` will point to the new one.
>
> Enter 1, 2, or 3.

Wait for the response. DO NOT choose on your own; DO NOT interpret silence as confirmation of any option.

### Option 1, Continue the previous one

1.  Do not write to `active-requirements.json`.
2.  Do not create a new folder in `_reversa_forward/`.
3.  Suggest the appropriate next skill for the physical stage:
    1.  1.  `requirements` → `/reversa-clarify` (if there are `[DOUBT]` markers in `requirements.md`) or `/reversa-plan`.
    2.  2.  `plan` → `/reversa-to-do`.
    3.  3.  `coding-in-progress` → `/reversa-coding` (can receive a free-form argument restricting the scope, e.g., "T010-T015").
4.  End this skill with a clear message informing that nothing was written; DO NOT execute the next sections.

### Option 2, Create a new one in parallel

1.  Read the current `active-requirements.json` and the `paused-features` field.
    1.  1.  If the field does not exist, consider it to be `paused-features: []`.
2.  Create a pause entry for the previous feature, copying the fields from the current `active-requirements.json` and adding the two pause fields:

```json
{
  "feature-dir": "<relative feature-dir>",
  "feature-id": "<NNN>",
  "short-name": "<short-name>",
  "started-at": "<ISO 8601 from the current active-requirements.json>",
  "current-stage": "<current field value, even if it's merely informative metadata>",
  "stages-completed": [],
  "paused-at": "<ISO 8601 of the current time>",
  "paused-from-stage": "<detected stage: requirements | plan | coding-in-progress>"
}
```

    1.  1.  The `started-at`, `current-stage`, and `stages-completed` fields allow `/reversa-resume` to resume this feature later without losing original data.
3.  Add this entry to the end of the `paused-features` array (push, chronological order).
4.  Proceed normally to "Resolving the Feature Directory." When writing the new `active-requirements.json` (step 5 in that section), INCLUDE the updated `paused-features` array in the JSON.

### Option 3, Abandon the previous one

1.  Read the current `active-requirements.json` and the `paused-features` field.
    1.  1.  If the field does not exist, consider it to be `paused-features: []`.
2.  DO NOT add the newly abandoned feature to the `paused-features` array (it remains orphaned in the `_reversa_forward/` folder, without active registration, recoverable only by manual listing).
3.  Proceed normally. When writing the new `active-requirements.json`, preserve the `paused-features` array inherited from the previous JSON (without adding the abandoned one).

The **non-destructive** guideline applies here: in none of the three options is the folder of the previous feature in `_reversa_forward/` deleted or modified. Only the `active-requirements.json` (managed by Reversa) is rewritten.

## Resolving the Feature Directory

1.  Read `.reversa/setup.json`.
    1.  1.  If `prefix-format` is missing or is `sequential`, calculate the next `NNN` by listing the subfolders of `_reversa_forward/` in the format `NNN-*` and adding 1 to the largest.
    2.  2.  If `prefix-format` is `timestamp`, use `YYYYMMDD-HHMMSS` from the current time.
2.  Generate a `short-name` in kebab-case ASCII from the free-form argument, up to thirty characters.
3.  Define `feature-dir = _reversa_forward/<NNN>-<short-name>` (or `_reversa_forward/<TIMESTAMP>-<short-name>`).
4.  Create `feature-dir` if it does not exist.
5.  Update `.reversa/active-requirements.json` with the content below, using atomic writing (tempfile plus rename):

```json
{
  "schema-version": 1,
  "feature-dir": "<project relative path>",
  "feature-id": "<NNN>",
  "short-name": "<short>",
  "started-at": "<ISO 8601>",
  "current-stage": "requirements",
  "stages-completed": [],
  "paused-features": [...]
}
```

    1.  1.  The `paused-features` field comes from the array updated according to the option chosen in "Re-execution Policy" (empty if it was the first feature in the project).
    2.  2.  The `current-stage` and `stages-completed` fields are informative metadata, not authoritative; the actual stage detection is done by physical artifacts.

Re-execution policy: if `active-requirements.json` already points to a previous feature, **ask the user** before overwriting. Options: continue the previous one, create a new feature in parallel, or abandon the previous one.

## Collecting Context from Reverse Extraction

Before writing the requirements, read, in order (skipping what doesn't exist):

1.  `_reversa_sdd/architecture.md` (overview of the components).
2.  `_reversa_sdd/domain.md` (confirmed business rules).
3.  `_reversa_sdd/inventory.md` (code surface).
4.  `_reversa_sdd/code-analysis.md` ONLY in the sections of the components that the free-form argument seems to refer to.
5.  `.reversa/principles.md` (project principles, if it exists).

Identify the relevant files. Each citation within the requirements must point to these sources in the format `_reversa_sdd/<file>#<section>`.

## Constructing the `requirements.md`

1.  Load the template in `.reversa/templates/requirements-template.md`.
2.  Preserve the order of the mandatory sections.
3.  Fill in each section, respecting the inline guiding comments.
4.  Mark with `[DOUBT]` any point where the information is missing or ambiguous.
5.  Limit the total number of `[DOUBT]` markers in the initial document to a maximum of three.
    1.  1.  Prioritize, in order: scope, security, and privacy, user experience, technical.
6.  Use the 🟢 / 🟡 / 🔴 markers for items according to the confidence of the original source.

## Iterative Auto-validation

1.  After writing `requirements.md`, read the `quality-template.md` template.
2.  Mentally apply the checklist.
3.  If there are failed items, rewrite the affected sections.
4.  Repeat this cycle a maximum of three times.
5.  If problems persist after three iterations, log them in a final section `## Quality Pending Items` and continue.

## Persistence

-   Save `requirements.md` in `feature-dir/`.
-   The writing should be atomic (tempfile plus rename).
-   Use UTF-8 without BOM.

## Post-execution Hooks

1.  Search for `after-requirements` in `.reversa/hooks.yml`.
2.  Apply the same filtering rule (`enabled: false` is discarded).
3.  For `optional: true`, present links in "## Available Hooks".
4.  For `optional: false`, issue `EXECUTE: <command>` and wait.

## Final Report

At the end of the execution, show the user:

1.  Absolute path of `feature-dir`.
2.  Absolute path of `requirements.md`.
3.  Number of `[DOUBT]` markers in the document.
4.  Suggestion for the next step:
    1.  1.  If there are `[DOUBT]`, suggest `/reversa-clarify`.
    2.  2.  Otherwise, suggest `/reversa-plan`.

Always end with:

> Type **CONTINUE** to proceed with `/reversa-clarify` or `/reversa-plan` as suggested above.

NEVER automatically proceed to the next command; let the user decide.
```