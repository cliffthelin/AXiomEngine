## Checkpoints Guide — `.reversa/state.json`

Reversa is the only agent that **writes** to the `state.json` file. All other agents only read from it.

## Absolute Rules

1.  **Never remove existing fields.** Only add or update.
2.  **Always read the file before writing** – another agent may have updated `checkpoints`.
3.  **Save after each phase is completed**, not just at the end.
4.  **In case of context overflow**, save immediately before pausing.

## What to Save at Each Phase

### When Starting a Phase
```json
{
  "phase": "reconhecimento"
}
```

### When an Agent Completes a Task
```json
{
  "checkpoints": {
    "scout": {
      "completed_at": "2026-04-26T10:30:00Z",
      "files": [
        "_reversa_sdd/inventory.md",
        "_reversa_sdd/dependencies.md",
        ".reversa/context/surface.json"
      ]
    }
  }
}
```

### When an Entire Phase is Completed
```json
{
  "phase": "escavacao",
  "completed": ["reconhecimento"],
  "pending": ["escavacao", "interpretacao", "geracao", "revisao"]
}
```

### When Marking a Partial Task of the Archaeologist
```json
{
  "checkpoints": {
    "archaeologist": {
      "modules_analyzed": ["auth", "orders"],
      "modules_pending": ["payments", "users"]
    }
  }
}
```

## Phase Sequence

```
null → reconhecimento → escavacao → interpretacao → geracao → revisao
```

When moving from one phase to the next:
- Remove the completed phase from `pending` and add it to `completed`.
- Update `phase` to the next phase.

## Example of `state.json` with Analysis in Progress

```json
{
  "version": "1.0.0",
  "project": "meu-sistema",
  "user_name": "Ana",
  "chat_language": "pt-br",
  "doc_language": "Português",
  "answer_mode": "chat",
  "output_folder": "_reversa_sdd",
  "phase": "escavacao",
  "completed": ["reconhecimento"],
  "pending": ["escavacao", "interpretacao", "geracao", "revisao"],
  "checkpoints": {
    "scout": {
      "completed_at": "2026-04-26T10:30:00Z",
      "files": [
        "_reversa_sdd/inventory.md",
        "_reversa_sdd/dependencies.md",
        ".reversa/context/surface.json"
      ]
    },
    "archaeologist": {
      "modules_analyzed": ["auth", "orders"],
      "modules_pending": ["payments", "users"]
    }
  },
  "engines": ["claude-code"],
  "agents": ["reversa", "reversa-scout", "reversa-archaeologist"],
  "created_files": []
}
```

## Pause Message Due to Context Overflow

If the context is running out, save the current checkpoint and say:

> "[Name], I will pause here to preserve the context. Everything is saved in `.reversa/state.json`. Type `reversa` in a new session to continue where we left off."
