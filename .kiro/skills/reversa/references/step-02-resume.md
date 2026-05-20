###
###
# Step 2 — Session Resumption

## 0. Checking for Ongoing Migration

First, read `.reversa/state.json` solely to determine `output_folder` (default: `_reversa_sdd`).

Verify the existence of `<output_folder>/migration/.state.json`. If it doesn't exist, skip this section and proceed to section 1.

If it exists, read the file and determine the migration status:

| Condition                                          | State                |
|----------------------------------------------------|----------------------|
| `pendingAgents.length > 0` or `currentAgent.agent` is different from `null` | In progress         |
| `currentAgent.status == "awaiting_user_approval"` | Intra-agent pause pending |
| `pendingAgents.length == 0`, `currentAgent.agent == null` and `<output_folder>/migration/handoff.md` exists | Completed             |

If the state is **Completed**, skip this section (the migration is already finished, no need to ask further) and proceed to section 1.

If the state is **In progress** or **Intra-agent pause pending**, present the question to the user before anything else:

> "[Name], I have found an **ongoing migration** in `<output_folder>/migration/`.
>
> - Completed: <N> of 6 agents (<list of completedAgents>)
> - Pending: <list of pendingAgents>
> - Current state: <currentAgent.agent or "awaiting human approval">
>
> How would you like to proceed:
>
> 1. **Resume the migration**: go back to the Migration Team where you left off
> 2. **Resume the Reversa flow**: continue with discovery/forward, ignore migration for now
> 3. **Cancel**: end this session without making any changes
> 4. **Other**: describe what you would prefer to do
>
> Use the engine's interactive menu mechanism (in Claude Code, `AskUserQuestion`); in engines that do not support menus, ask the user to enter 1–4 or free text."

Wait for the response. Do NOT choose on your own.

- If **1**: end the `/reversa` session here with the final instruction:
  > "To resume the migration, type `/reversa-migrate`. It detects the saved state and offers the resumption options."
  
  Do NOT automatically activate `reversa-migrate`; let the user type it in (Reversa's explicit handoff default).
- If **2**: proceed with section 1 of this step as usual.
- If **3**: end without doing anything.
- If **4** (free text): interpret the user's intention and offer the best possible route, without inventing new flows. If the intention is ambiguous, rephrase the question once before deciding.

## 1. Reading the State

Read `.reversa/state.json` and `.reversa/plan.md`.

## 2. Version Check

Compare `.reversa/version` with the npm registry. If a newer version is available, discreetly inform:
> "💡 A new version is available. Run `npx reversa update` whenever you want to update."

## 3. Greeting

Say: "[Name], welcome back to Reversa! 🎼"

## 4. Progress Summary

Show:
- ✅ Completed phases (the `completed` field of `state.json`)
- 🔄 Current phase (the `phase` field) with the last task recorded in `checkpoints`
- ⏳ Next phases (the `pending` field)

Example:
> "Current progress:
> ✅ Recognition completed
> 🔄 Excavation in progress — `auth` and `orders` modules analyzed, `payments` and `users` pending
> ⏳ Interpretation, Generation, Revision"

## 5. Answering Gaps Mode

If `answer_mode` is `"file"`:
> "Remember: your answers to the questions must be filled in at `_reversa_sdd/questions.md`. Let me know when you are finished."

If `answer_mode` is `"chat"` (default):
> Continue as usual — I will ask the questions here in the chat.

## 6. Confirmation

Ask only: "Shall we continue where we left off? (CONTINUE to proceed)"

After confirmation, resume the next pending task in the plan (`.reversa/plan.md`).

**🚫 Do NOT offer `/clear` + `/reversa` at this time.** The user has just resumed the session; asking to clear and reopen now is redundant. The prompt for a pause between steps (described in `SKILL.md`, the "Preventive checkpoint between steps" section) only applies **after** an agent has completed work within this session, never in the resumption greeting itself.

Refer to `references/checkpoint-guide.md` for the rules for writing in `state.json`.
