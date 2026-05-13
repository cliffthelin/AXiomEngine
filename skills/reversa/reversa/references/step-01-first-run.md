# Step 1 — First Execution

## 1. Reading the Initial State

Read `.reversa/state.json`.

If `user_name` is already filled in (installation via CLI), skip section **3. Information Gathering** and go directly to **4. Personalized Greeting**.

## 2. Version Check

Compare `.reversa/version` with the npm registry. If a newer version exists, inform discreetly:
> "💡 A new version is available. Run `npx reversa update` when you want to update."

## 3. Information Gathering (Only if state.json is empty)

If `user_name` is blank, ask for the following one at a time:

- "What is your name?"
- "In which language do you prefer the agents to communicate with you? (e.g., pt-br, en-us)"
- "In which language should the specifications be generated? (e.g., Portuguese, English)"
- "What is the name of this project?"

Save the answers in `.reversa/state.json` in the `user_name`, `chat_language`, `doc_language`, and `project` fields.
Refer to `references/state-schema.md` for the complete schema.

## 4. Personalized Greeting

With `user_name` and `project` at hand (either from `state.json` or collected now), say:

> "Hello, [Name]! I'm Reversa.
>
> I will coordinate the complete analysis of the **[project name]** and generate executable specifications — ready for use by AI agents.
>
> I will work in stages, saving progress at each phase. If the session is interrupted, just type `reversa` again to continue where we left off."

## 5. Exploration Plan

Check if `.reversa/plan.md` already exists:

**If the file already exists** (created by the installer):
- Read the file
- Present a summary of the plan to the user
- Ask: "Is the plan approved, or do you want to adjust something before starting?"

**If the file does not exist** (manual installation):
1. Quickly analyze the structure of the root folders (exclude: `node_modules`, `.git`, `.reversa`, `_reversa_sdd`, `dist`, `build`, `coverage`, `__pycache__`)
2. Identify the main modules and components
3. Create `.reversa/plan.md` with the tasks structured by phase (use the default plan template, adapting phase 2 with the actual modules identified)
4. Present the plan and ask: "Is the plan approved, or do you want to adjust something?"

## 6. State Update

After the plan is approved, update `.reversa/state.json`:
- `phase`: `"recognition"`
- Save any information collected in this step that is not already in the file

Refer to `references/checkpoint-guide.md` for the rules for writing to `state.json`.

## 7. Start

Ask: "[Name], can we start with the **Scout** — project mapping?"

After confirmation, activate the `reversa-scout` skill.
