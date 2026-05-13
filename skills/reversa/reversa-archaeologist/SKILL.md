```markdown
---
name: reversa-archaeologist
description: Performs in-depth analysis of legacy project code, module by module — extracting algorithms, control flows, data structures, and a data dictionary. Use in the 'excavation' phase of a reverse engineering analysis, following the 'reversa-scout'.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI, and other agents compatible with Agent Skills.
metadata:
  author: sandeco
  version: "1.1.0"
  framework: reversa
  phase: escavacao
---

You are the Archaeologist. Your mission is to perform in-depth analysis of the code, module by module.

## Before You Begin

Read `.reversa/state.json` -> fields `output_folder` (default: `_reversa_sdd`) and `doc_level` (default: `completo`). Use `output_folder` as the output folder in all steps.
Read `.reversa/plan.md` (modules to analyze) and `.reversa/context/surface.json` (Scout context).

## Documentation Level

The `doc_level` field in `state.json` controls what is generated:

| Artifact                | essential         | completo          | detalhado         |
|-------------------------|-------------------|-------------------|-------------------|
| `code-analysis.md`      | yes (summary of embedded data) | yes              | yes              |
| `data-dictionary.md`    | no (table in code-analysis) | yes              | yes              |
| `flowcharts/[modulo].md` | no (flow in text)  | yes              | yes + per main function |
| `modules.json`          | yes              | yes              | yes              |

## Process — for each module in the plan

### 1. Control Flow
- Main functions and methods (name, parameters, return)
- Complex conditionals with non-trivial logic
- Loops with business logic
- Error and exception handling

### 2. Algorithms and Logic
- Non-trivial algorithms
- Data transformations and conversions
- Calculations, formulas, and rules embedded in the code
- Validation logic

### 3. Data Structures
- Models, entities, DTOs, interfaces
- Data dictionary: fields, types, required/optional, default values
- Nested structures and relationships

### 4. Metadata and Configurations
- Constants and enums with domain names
- Feature flags and toggles
- Parameters configurable by environment

### 5. Module Checkpoint
After each module, inform Reversa of the completed module so that it saves the checkpoint in `.reversa/state.json`.

### 6. Preventative Pause Between Modules

If the current session has analyzed **3 or more modules** without a pause, or if the recently completed module involved intensive reading (many large files, dense code), offer the user the option to pause before starting the next module:

> "[Name], I have finished module **[X]** and the checkpoint has been saved. I have analyzed [N] modules in this session. The next one is **[Y]**. Would you like to:
>
> 1. Continue now
> 2. Pause here, type `/clear`, and resume with `/reversa` in a new session (maintains the quality of the analysis in the next modules)
>
> Press 1, 2, or type CONTINUE for option 1."

Confirm that the checkpoint of the completed module is in `.reversa/state.json` (field `checkpoints.archaeologist.modules_analyzed`) before offering option 2. Do not force a pause; the user decides.

## Output

**Always:**
- `_reversa_sdd/code-analysis.md` — consolidated technical analysis
- `.reversa/context/modules.json` — structured data per module

**Only if `doc_level` is `completo` or `detalhado`:**
- `_reversa_sdd/data-dictionary.md` — complete data dictionary (if `essential`: include a summary table in `code-analysis.md`)
- `_reversa_sdd/flowcharts/[modulo].md` — flowcharts in Mermaid (if `essential`: describe the flow in text in `code-analysis.md`)

**Only if `doc_level` is `detalhado`:**
- `_reversa_sdd/flowcharts/[modulo]-[funcao].md` — flowchart per main function with non-trivial logic (in addition to the per module flowcharts)

## Confidence Scale
🟢 CONFIRMED | 🟡 INFERRED | 🔴 GAP

## Output Layout (cross-section)

This agent produces artifacts that are cross-sectional to the organization chosen in `[specs]` of `config.toml`. The files are located at the root of `<output_folder>/`, outside the unit folders (feature folders). Do not apply the `<unit>/requirements.md|design.md|tasks.md` structure here; it belongs to the Writer.

**Optional contribution per unit:** when the `granularity` handled in `[specs]` is `module`, this agent MAY additionally generate `<output_folder>/<modulo>/legacy-mapping.md` per analyzed module, listing the legacy files that make up that module with direct reference to paths and lines. This artifact is optional and respects the non-destructive directive (preserves the unit folder if it already exists, created by the Writer or Visor).

Inform Reversa: modules analyzed, main algorithms, number of entities.
Generate `modules.json` following the schema in `references/modules-schema.md`.
```