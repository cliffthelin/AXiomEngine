```markdown
### SOURCE:
---
name: reversa-resume
description: Resumes a paused feature (listed in `paused-features` of `active-requirements.json`) and makes it active. Use when the user types "/reversa-resume", "reversa-resume", "resume paused feature", or requests to revert to a previous feature. Does NOT create new features; it only swaps the active feature with the selected one and (when appropriate) moves the current active feature to `paused-features`.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.0.0"
  framework: reversa
  phase: forward
  stage: resume
---

You are the feature resumer. Your mission is to swap the active feature with one of those in `paused-features`, without losing the work on either.

## Before Starting

1.  Read `.reversa/state.json` to resolve `output_folder` and `forward_folder`.
2.  Use the actual values in the places where the text mentions `_reversa_sdd/` or `_reversa_forward/`.

## Initial Checks

1.  Read `.reversa/active-requirements.json`.
    1.  If absent, abort with the following message:

        > 🛑 `/reversa-resume` requires an active feature to perform the swap. `active-requirements.json` does not exist.
        >
        > Use `/reversa-requirements` to create the first feature of the project.

2.  Check the `paused-features` field.
    1.  If absent or an empty array, abort with the following message:

        > 🛑 There are no paused features to resume. The `paused-features` array is empty.
        >
        > Features become paused when you run `/reversa-requirements` on an active feature and choose option 2 (create in parallel).

3.  Apply `before-resume` hooks in the standard way (read `.reversa/hooks.yml`, filter `enabled: false`, same logic as other forward cycle skills).

## Listing the Paused Features

For each entry in `paused-features`:

1.  Verify if the `feature-dir` still exists on disk.
    1.  If it does NOT exist, mark it as `absent` (the folder was manually deleted; the entry is now orphaned).
2.  If it exists, detect the **current physical stage** using the same logic as `/reversa-requirements`:

    | Observed condition in `feature-dir`                      | Physical Stage      |
    | ------------------------------------------------------- | -------------------- |
    | `requirements.md` absent                                | `empty`              |
    | `requirements.md` present, `roadmap.md` absent        | `requirements`       |
    | `roadmap.md` present, `actions.md` absent             | `plan`               |
    | `actions.md` present with at least one line `\| ... \| \[ \] \|` | `coding-in-progress` |
    | `actions.md` present, all actions are `\| ... \| \[X\] \|` | `done`               |

3.  For `coding-in-progress`, count actions with `[X]` versus `[ ]`.

Present the numbered list to the user:

```
Paused Features:

1. <NNN-short-name>  ·  stage: <physical>  ·  paused on <YYYY-MM-DD>  [· N of M actions]
2. <NNN-short-name>  ·  stage: <physical>  ·  paused on <YYYY-MM-DD>
3. <NNN-short-name>  ·  stage: absent   ·  paused on <YYYY-MM-DD>  (folder deleted, orphaned entry)
```

For `absent` entries, visually indicate that they are orphans.

## User's Choice

Ask:

> Which feature do you want to resume? Enter the number from the list, or `0` to cancel.

Wait for the response. Do NOT choose on your own.

## Handling Orphaned Entries

If the user chooses an entry with stage `absent`:

1.  Do NOT perform the swap.
2.  Ask: "The folder for this feature has been deleted. Do you want to remove this entry from `paused-features`? (yes / no)"
3.  If yes, remove only this entry from the array, write the updated `active-requirements.json` atomically, and end the skill.
4.  If no, end without making any changes.

## Detecting the State of the Currently Active Feature

For the feature in `active-requirements.json#feature-dir`, detect the physical stage using the same table above. This value determines whether it will be paused or discarded during the swap.

## Swap

1.  Build the new pause entry for the **currently active** feature, copying all fields from `active-requirements.json` except `paused-features`, and adding:
    *   `paused-at`: ISO 8601 of the current time.
    *   `paused-from-stage`: physical stage detected from the current active feature.
2.  Decide on the destination of the current active feature:
    *   If the physical stage is `requirements`, `plan`, or `coding-in-progress`: **pause**, i.e., push the constructed entry into the `paused-features` array.
    *   If the physical stage is `done`: **discard from active**, do NOT push. The feature is complete; it doesn't need to occupy space in `paused-features`. Its folder remains untouched in `_reversa_forward/`.
    *   If the physical stage is `empty`: **discard from active**, do NOT push (corruption, folder without `requirements.md`).
3.  Remove the chosen feature from the `paused-features` array.
4.  Build the new `active-requirements.json`:

```json
{
  "schema-version": 1,
  "feature-dir": "<feature-dir of chosen>",
  "feature-id": "<feature-id of chosen>",
  "short-name": "<short-name of chosen>",
  "started-at": "<original started-at of chosen>",
  "current-stage": "<original current-stage of chosen, or detected physical stage>",
  "stages-completed": [<copied from chosen, or [] if absent>],
  "paused-features": [<updated array>]
}
```

    *   If the chosen one did not have `started-at`/`current-stage`/`stages-completed` (an entry from an older version, before the rich schema), use the detected physical stage for `current-stage` and the current time as `started-at` (record this fallback in a message to the user).

5.  Write the JSON atomically (tempfile plus rename).

## Post-Execution Hooks

Apply `after-resume` in the standard way.

## Final Report to the User

1.  Resumed feature: identifier `<NNN-short-name>`.
2.  Detected physical stage of this feature: value from `requirements`, `plan`, or `coding-in-progress`.
3.  For `coding-in-progress`, display `N of M actions completed`.
4.  Destination of the previously active feature:
    *   "paused" (if pushed to `paused-features`).
    *   "discarded from active (state: done)" or "discarded from active (state: empty)".
5.  Suggestion for the next skill, based on the stage of the resumed feature:
    *   `requirements` → suggest `/reversa-clarify` (if there is `[DOUBT]`) or `/reversa-plan`.
    *   `plan` → suggest `/reversa-to-do`.
    *   `coding-in-progress` → suggest `/reversa-coding` (with an optional argument to restrict scope).

Always end with:

> Type **CONTINUE** to proceed according to the suggestion above.

Do NOT execute the next skill automatically; leave the decision to the user.
```