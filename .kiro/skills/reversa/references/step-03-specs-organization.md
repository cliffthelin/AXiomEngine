```markdown
### Step 3, Specs Organization

This step occurs immediately after the user selects the `doc_level` (Essential / Complete / Detailed) and before the Archaeologist is invoked. It's when Reversa determines and persists the structure in which the specifications will be generated.

## 1. Decide whether the menu should be displayed

Read, in this order, and merge key by key (full precedence given to `config.user.toml`):

1. `.reversa/config.toml`, section `[specs]` (Reversa-managed configuration)
2. `.reversa/config.user.toml`, section `[specs]` (user's manual override)

The merge is evaluated key by key: each key present in `config.user.toml` replaces the corresponding one in `config.toml`. Missing keys remain from `config.toml`.

The section is considered **decided** when, after the merge, `granularity` is set to one of the valid values: `module`, `use-case`, `endpoint`, `hybrid`, `feature`, `custom`.

- **If decided:** Skip this entire step. Proceed directly to the Archaeologist invocation.
- **If not decided** (section is missing, or `granularity` is empty): Present the menu (step 2 below).

### Special Case, RF-18

If `granularity` is empty in `config.toml` (or the section has been removed) **and** the `[specs]` section exists in `config.user.toml` with any key filled, notify the user before displaying the menu. Use exactly this format:

> "I've detected that `.reversa/config.toml` does not have a decision for the specs organization, but `.reversa/config.user.toml` contains an override in `[specs]`. The override will continue to be active after your choice and may overwrite fields that you decide now.
>
> Current override in `config.user.toml`:
> [list keys and values]
>
> Do you want to proceed with the menu anyway? (y/N)"

Wait for an explicit affirmative response before proceeding to the menu. An empty or negative response aborts without persisting anything.

## 2. Present the menu

Read `.reversa/context/surface.json` → `organization_suggestion`. Use the `granularity` field to pre-select the suggested option, and the `rationale` field to show the reason.

If `surface.json` does not have `organization_suggestion` filled (Scout did not run or failed), display the menu without a default and ask the user to choose manually, as per EC-01 of the organization specification.

Use exactly this format (language follows `chat_language` from `state.json`, example below in pt-br):

```
How do you want to organize the specifications for this project?

Scout analyzed the legacy code and suggests: [translated suggested granularity].
Reason: [organization_suggestion.rationale]

  [1] [marker] By code module
  [2] [marker] By use case
  [3] [marker] By endpoint/contract
  [4] [marker] Hybrid (module at the root, nested use cases)
  [5] [marker] By features (Scout lists the discovered features)
  [6] [marker] Custom

Choose (Enter accepts the suggested one):
```

Where `[marker]` is `*` (asterisk) on the pre-selected option and a space on the others. Add `(suggested)` next to the pre-selected option.

Mapping of the 6 options to the `granularity` value:

| Option | `granularity` |
|-------|---------------|
| 1 | `module` |
| 2 | `use-case` |
| 3 | `endpoint` |
| 4 | `hybrid` |
| 5 | `feature` |
| 6 | `custom` |

### Accept the input

- Pressing Enter without typing: accepts the pre-selected option.
- Entering a number from 1 to 6: accepts the corresponding option.
- Any other input: ask again without persisting anything.
- Pressing Ctrl+C / ESC / cancel: abort execution and do not persist anything (EC-02).

### Option 6, custom

If the user chooses 6, display the following prompt:

> "What are the names of the first-level folders? List them separated by a comma or one per line (minimum 1)."

Accept the input, sanitize each name (remove characters prohibited by the operating system's file system, discard empty names). If the list results in being empty, repeat the prompt (EC-07). The names are stored in `custom_folders`.

## 3. Detect conflict with existing structure on disk (RF-11)

Before persisting the decision, check if a specification structure is already present in `<output_folder>/` (defined in `state.json`).

If the output folder contains subfolders that correspond to a granularity different from the one chosen now (for example, `endpoint` was chosen but the disk contains folders that look like `module`), display a warning comparing the two structures and ask for confirmation:

> "I've detected that specifications are already generated with the **[old]** structure in `<output_folder>/`. You chose **[new]** now, which differs from the previous one.
>
> I will create the new structure in parallel, without touching the previous one. Existing specifications will be preserved.
>
> Confirm? (y/N)"

Wait for an explicit affirmative response. A negative response aborts without persisting.

The detection is heuristic and best-effort: compare the names of top-level subfolders with the modules identified by Scout (`module`), with URIs/routes (`endpoint`), with features (`feature`), etc. When the heuristic cannot decide clearly, **do not** display the warning (avoids false positives).

## 4. Persist the decision (RNF-03, atomic write)

Update `.reversa/config.toml`, section `[specs]`, with:

```toml
[specs]
layout = "feature-folder"
granularity = "<user's choice>"
custom_folders = [<list>]   # only when granularity == "custom", otherwise []
scout_suggestion = "<organization_suggestion.granularity from surface.json>"
decided_at = "<ISO 8601 UTC timestamp, example 2026-05-03T14:32:00Z>"
```

Rules:

- **Atomic write:** write to a temporary file in the same directory (`config.toml.tmp`) and perform an atomic rename to `config.toml`. Failure during writing must not leave `config.toml` corrupted.
- **scout_suggestion is immutable** (RF-14): if the `[specs]` section already existed but was with `granularity` empty and `scout_suggestion` filled, preserve `scout_suggestion`. On the first execution, copy the current value of `organization_suggestion.granularity` from `surface.json`.
- **Non-destructive:** preserve any key/section that you are not explicitly updating. Do not touch `[project]`, `[user]`, `[output]`, `[agents]`, `[engines]`, `[analysis]` or other sections.
- **Do not touch `.reversa/config.user.toml`.** This file belongs to the user.
- **I/O failure** (disk full, no permission, EC-06): display a clear error, do not create specification folders, do not consider the choice as confirmed. The user can try again on the next execution.

## 5. Continue the flow

After successful persistence, continue with the Archaeologist invocation as described in the `plan.md`. The decision is available to all agents that write specifications.

## 6. Manual re-presentation (RF-17)

There is no dedicated CLI flag to reconfigure. The user can re-present the menu by manually removing the `[specs]` section from `.reversa/config.toml` (or emptying `granularity`). On the next execution, this step detects the "undecided" state and runs again.

## Language of the folders (RF-10)

The names that Reversa uses for the feature folders follow `doc_language` from `state.json`. Do not ask for the language in this step. In a `pt-br` installation, the folders are named in `pt-br`; in `en`, in English.

## List of checks before proceeding

- [ ] Read `[specs]` from `config.toml` and merge with `config.user.toml` key by key
- [ ] If already decided, skip the step
- [ ] If there is an override in `config.user.toml` but `config.toml` is empty, display warning RF-18
- [ ] Read `organization_suggestion` from `surface.json`
- [ ] Display the menu with a suggested option pre-selected
- [ ] Accept Enter, a number from 1 to 6, or cancellation
- [ ] If option 6, collect `custom_folders`
- [ ] Detect conflict with existing structure on disk and ask for confirmation
- [ ] Atomic write in `config.toml`
- [ ] Preserve `scout_suggestion` in re-executions with a partial section
- [ ] Proceed to the Archaeologist
```