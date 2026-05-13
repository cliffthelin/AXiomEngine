```
### SOURCE:
# Checkpoints Guide — .reversa/state.json

Reversa is the only agent that **writes** to the state.json file. All other agents only read from it.

## Absolute Rules

1.  **Never remove existing fields.** Only add or update them.
2.  **Always read the file before writing** – another agent may have updated `checkpoints`.
3.  **Save after each completed phase**, not just at the end.
4.  **In case of context exhaustion**, save immediately before pausing.

## What to Save in Each Phase

### When starting a phase
```json
{
  "phase": "reconhecimento"
}
```

### When completing an agent
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

### When completing an entire phase
```json
{
  "phase": "escavacao",
  "completed": ["reconhecimento"],
  "pending": ["escavacao", "interpretacao", "geracao", "revisao"]
}
```

### When marking a partial task of the Archaeologist
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

When moving from one phase to another:
- Remove the completed phase from `pending` and add it to `completed`.
- Update `phase` to the next phase.

## Example of state.json with analysis in progress

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

## Context Exhaustion Pause Message

If the context is running out, save the current checkpoint and say:

> "[Name], I'm going to pause here to preserve the context. Everything is saved in `.reversa/state.json`. Type `reversa` in a new session to continue from where we left off."
```