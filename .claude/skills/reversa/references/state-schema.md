### SOURCE:
# Schema — .reversa/state.json

This file persists the complete analysis state between sessions. Reversa reads from and writes to this file.

## Complete Structure

```json
{
  "version": "1.0.0",
  "project": "project-name",
  "user_name": "User Name",
  "chat_language": "pt-br",
  "doc_language": "Portuguese",
  "answer_mode": "chat",
  "doc_level": null,
  "output_folder": "_reversa_sdd",
  "phase": "reconhecimento",
  "completed": ["reconhecimento"],
  "pending": ["escavacao", "interpretacao", "geracao", "revisao"],
  "engines": ["claude-code"],
  "agents": ["reversa", "reversa-scout", "reversa-archaeologist"],
  "checkpoints": {
    "scout": {
      "completed_at": "2026-04-26T10:00:00Z",
      "files": [
        "_reversa_sdd/inventory.md",
        "_reversa_sdd/dependencies.md",
        ".reversa/context/surface.json"
      ]
    },
    "archaeologist": {
      "completed_at": "2026-04-26T11:00:00Z",
      "modules_analyzed": ["auth", "orders", "payments"],
      "files": [
        "_reversa_sdd/code-analysis.md",
        "_reversa_sdd/data-dictionary.md",
        ".reversa/context/modules.json"
      ]
    }
  },
  "created_files": [
    "CLAUDE.md",
    ".agents/skills/reversa/SKILL.md",
    ".reversa/state.json",
    ".reversa/plan.md"
  ]
}
```

## Fields

| Field | Type | Description |
|-------|------|-----------|
| `version` | string | Installed Reversa version |
| `project` | string | Legacy project name |
| `user_name` | string | User name (for interactions) |
| `chat_language` | string | Language of the interactions (e.g., pt-br, en-us) |
| `doc_language` | string | Language of the generated specs (e.g., Portuguese, English) |
| `answer_mode` | string | How the user responds to gaps: `chat` or `file` |
| `doc_level` | string \| null | Volume of documentation generated: `essencial`, `completo`, or `detalhado`. Starts as `null` — must be filled in via user choice after the Scout. |
| `output_folder` | string | Output folder for the specs (default: `_reversa_sdd`) |
| `phase` | string \| null | Current phase. `null` = not started |
| `completed` | string[] | Completed phases |
| `pending` | string[] | Pending phases |
| `checkpoints` | object | Record of the completion of each agent |
| `engines` | string[] | Configured engines (e.g., `["claude-code", "codex"]`) |
| `agents` | string[] | Installed agents |
| `created_files` | string[] | All files created by Reversa (for safe uninstall) |

## Valid Phases

`reconhecimento` → `escavacao` → `interpretacao` → `geracao` → `revisao`

## Rule when writing

Never remove existing fields. Only add or update them.

## Where NOT to write

The decision regarding the organization of the specs (granularity, custom folders, Scout's original suggestion, timestamp of the choice) **does not** go into `state.json`. It is persisted in `.reversa/config.toml`, in the `[specs]` section, as outlined in `references/step-03-specs-organization.md`. `state.json` is runtime state; `config.toml` is a long-term decision.
