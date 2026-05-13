```markdown
---
name: reversa-resume
description: Resumes a paused feature (listed in the `paused-features` of `active-requirements.json`) and makes it active. Use when the user types `/reversa-resume`, `reversa-resume`, `resume paused feature`, or asks to go back to a previous feature. This does NOT create new features; it simply swaps the active feature with the chosen one and, when appropriate, moves the current active feature to `paused-features`.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: resume
---

You are the feature resumer. Your mission is to swap the active feature with one of the features in `paused-features`, without losing the work of either feature.

## Before You Begin

1.  Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`.
2.  Use the actual values in the places where the text mentions `_reversa_sdd/` or `_reversa_forward/`.

## Initial Checks

1.  Read `.reversa/active-requirements.json`.
    1.1. If it's missing, abort with the message:

        > 🛑 `/reversa-resume` requires an active feature to perform the swap. `active-requirements.json` does not exist.
        >
        > Use `/reversa-requirements` to create the first feature of the project.

2.  Check the `paused-features` field.
    2.1. If it's missing or an empty array, abort with the message:

        > 🛑 There are no paused features to resume. The `paused-features` array is empty.
        >
        > Features are paused when you run `/reversa-requirements` on an active feature and choose option 2 (create a parallel feature).

3.  Apply the `before-resume` hooks in the standard way (read `.reversa/hooks.yml`, filter `enabled: false`, same logic as other skills in the forward cycle).

## Listing the Paused Features

For each entry in `paused-features`:

1.  Verify that the `feature-dir` still exists on disk.
    1.1. If it doesn't exist, mark it as `absent` (the folder was deleted manually, and the entry has become obsolete).
2.  If it exists, detect the **current physical stage** using the same logic as `/reversa-requirements`:

    | Condition Observed in `feature-dir` | Physical Stage    |
    | -------------------------------------- | ----------------- |
    | `requirements.md` absent               | `empty`           |
    | `requirements.md` present, `roadmap.md` absent   | `requirements` |
    | `roadmap.md` present, `actions.md` absent      | `plan`          |
    | `actions.md` present with at least one line `\| ... \| \[ \] \|`  | `coding-in-progress` |
    | `actions.md` present, all actions as `\| ... \| \[X\] \|`   | `done`            |

3.  For `coding-in-progress`, count actions `[X]` versus `[ ]`.

Present the numbered list to the user:

```
Paused features:

1.  <NNN-short-name>  ·  stage: <physical>  ·  paused on <YYYY-MM-DD>  [· N of M actions]
2.  <NNN-short-name>  ·  stage: <physical>  ·  paused on <YYYY-MM-DD>
3.  <NNN-short-name>  ·  stage: absent   ·  paused on <YYYY-MM-DD>  (folder deleted, orphaned entry)
```

For `absent` entries, visually indicate that they are orphaned.

## User Choice

Ask:

> Which feature do you want to resume? Enter the number from the list, or `0` to cancel.

Wait for the response. Do NOT choose on your own.

## Handling Orphaned Entry

If the user chooses an entry with stage `absent`:

1.  Do NOT perform the swap.
2.  Ask: "The folder for this feature has been deleted. Do you want to remove this entry from `paused-features`? (yes / no)"
3.  If yes, remove only that entry from the array, write the updated `active-requirements.json` (atomically), and end the skill.
4.  If no, end without making any changes.

## Detecting the State of the Currently Active Feature

For the feature in `active-requirements.json#feature-dir`, detect the physical stage using the same table as above. This value determines whether it will be paused or discarded during the swap.

## Swap

1.  Construct the new pause entry for the **currently active feature**, copying all fields from `active-requirements.json` except `paused-features`, and adding:
    *   `paused-at`: ISO 8601 of the current time.
    *   `paused-from-stage`: the detected physical stage of the current active feature.
2.  Decide on the destination of the current active feature:
    *   2.1. If the physical stage is `requirements`, `plan`, or `coding-in-progress`: **pause**, i.e., push the constructed entry into the `paused-features` array.
    *   2.2. If the physical stage is `done`: **discard from active**, do NOT push (the feature is complete; it doesn't make sense to occupy space in `paused-features`). The folder remains untouched in `_reversa_forward/`.
    *   2.3. If the physical stage is `empty`: **discard from active**, do NOT push (corruption, folder without `requirements.md`).
3.  Remove the chosen feature from the `paused-features` array.
4.  Construct the new `active-requirements.json`:

```json
{
  "schema-version": 1,
  "feature-dir": "<feature-dir of the chosen one>",
  "feature-id": "<feature-id of the chosen one>",
  "short-name": "<short-name of the chosen one>",
  "started-at": "<original started-at of the chosen one>",
  "current-stage": "<original current-stage of the chosen one, or detected physical stage>",
  "stages-completed": [<copied from the chosen one, or [] if absent>],
  "paused-features": [<updated array>]
}
```

    4.1. If the chosen one didn't have `started-at`/`current-stage`/`stages-completed` (an entry from an older version, before the rich schema), use the detected physical stage for `current-stage` and the current time as `started-at` (record this fallback in a message to the user).
5.  Write the JSON atomically (tempfile plus rename).

## Post-Execution Hooks

Apply the `after-resume` hooks in the standard way.

## Final Report to the User

1.  Feature resumed: identifier `<NNN-short-name>`.
2.  Detected physical stage of this feature: value among `requirements` / `plan` / `coding-in-progress`.
3.  For `coding-in-progress`, show `N of M actions completed`.
4.  Destination of the previously active feature:
    4.1. "paused" (if pushed to paused-features)
    4.2. "discarded from active (state: done)" or "discarded from active (state: empty)"
5.  Suggestion for the next skill based on the stage of the resumed feature:
    5.1. `requirements` → suggest `/reversa-clarify` (if there's `[DÚVIDA]`) or `/reversa-plan`
    5.2. `plan` → suggest `/reversa-to-do`
    5.3. `coding-in-progress` → suggest `/reversa-coding` (with an optional argument to restrict scope)

Always end with:

> Type **CONTINUE** to proceed according to the above suggestion.

Do NOT execute the next skill automatically; leave the decision to the user.
```