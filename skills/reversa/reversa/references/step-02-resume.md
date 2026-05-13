### SOURCE:
# Step 2 — Session Resumption

## 0. Check for Ongoing Migration

First, read `.reversa/state.json` solely to resolve `output_folder` (default: `_reversa_sdd`).

Check if `<output_folder>/migration/.state.json` exists. If not, skip this section and proceed to section 1.

If it exists, read the file and categorize the migration status:

| Condition | Status |
|----------|--------|
| `pendingAgents.length > 0` or `currentAgent.agent` is different from `null` | ongoing |
| `currentAgent.status == "awaiting_user_approval"` | intra-agent pause pending |
| `pendingAgents.length == 0`, `currentAgent.agent == null` and `<output_folder>/migration/handoff.md` exists | completed |

If the status is **completed**, skip this section (the migration has already finished, no need to ask anything) and proceed to section 1.

If the status is **ongoing** or **intra-agent pause pending**, present the question to the user before anything else:

> "[Name], I found an **ongoing migration** in `<output_folder>/migration/`.
>
> - Completed: <N> of 6 agents (<list of completedAgents>)
> - Pending: <list of pendingAgents>
> - Current status: <currentAgent.agent or "awaiting human approval">
>
> How would you like to proceed:
>
> 1. **Resume migration**: returns to the Migration Team from where it stopped
> 2. **Resume the Reversa flow**: continues discovery/forward, ignores migration for now
> 3. **Cancel**: ends this session without making any changes
> 4. **Other**: describe what you would prefer to do
>
> Use the interactive menu mechanism of the engine (in Claude Code, `AskUserQuestion`); in engines without menu support, ask the user to type the number 1–4 or free text."

Wait for the answer. DO NOT choose for yourself.

- If **1**: end `/reversa` here with the final instruction:
  > "To resume the migration, type `/reversa-migrate`. It detects the saved state and offers the resumption options."
  
  Do NOT activate `reversa-migrate` automatically, let the user type (Reversa's explicit handoff default).
- If **2**: proceed with section 1 of this step normally.
- If **3**: end without doing anything.
- If **4** (free text): interpret the user's intention and offer the best possible route, without inventing new flows. If the intention is ambiguous, rephrase the question once before deciding.

## 1. State Reading

Read `.reversa/state.json` and `.reversa/plan.md`.

## 2. Version Check

Compare `.reversa/version` with the npm registry. If a newer version is available, discreetly inform:
> "💡 A new version is available. Run `npx reversa update` when you want to update."

## 3. Greeting

Say: "[Name], welcome back to Reversa! 🎼"

## 4. Progress Summary

Show:
- ✅ Completed phases (field `completed` of state.json)
- 🔄 Current phase (field `phase`) with the last task recorded in `checkpoints`
- ⏳ Next phases (field `pending`)

Example:
> "Current progress:
> ✅ Recognition completed
> 🔄 Excavation in progress — `auth` and `orders` modules analyzed, `payments` and `users` pending
> ⏳ Interpretation, Generation, Review"

## 5. Answering Gaps Mode

If `answer_mode` is `"file"`:
> "Remember: your answers to the questions must be filled in `_reversa_sdd/questions.md`. Let me know when you're done."

If `answer_mode` is `"chat"` (default):
> Continue normally — I will ask the questions here in the chat.

## 6. Confirmation

Ask only: "Shall we continue where we left off? (CONTINUE to proceed)"

After confirmation, resume the next pending task in the plan (`.reversa/plan.md`).

**🚫 Do not offer `/clear` + `/reversa` at this time.** The user has just resumed the session; asking to clear and reopen now is redundant. The prompt for a pause between steps (described in `SKILL.md`, section "Preventive checkpoint between steps") applies only **after** an agent has completed work within this session, never in the resumption greeting itself.

Consult `references/checkpoint-guide.md` for the rules for writing in the state.json.
