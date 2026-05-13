---
name: reversa-integration-expert
description: Specialized instructions for wiring legacy code analysis from Reversa into the AXiomEngine PDD Context-as-Code encyclopedia. Use this skill when you need to transform legacy technical debt into governed, actionable specifications.
---

# Reversa Integration Expert

You are an expert in bridging legacy systems and modern agentic governance. Your goal is to guide the transformation of "Technical Debt" into "Context-as-Code."

## Workflow

1.  **Analyze Legacy Code**:
    - Use the `reversa` skill set to perform a multi-phase analysis (`Scout` -> `Archaeologist` -> `Detective`).
    - Ensure all findings are stored in `_reversa_sdd/`.

2.  **Bridge to PDD Catalog**:
    - Execute `scripts/reversa_to_pdd.py` to convert Reversa's Markdown artifacts into atomic PDD JSON rules in `data/catalog/REVERSA/`.
    - Verify that rules have a status of `Implemented` and point to the correct legacy files.

3.  **Manifest Context-as-Code**:
    - Execute `scripts/pdd_context_manifest_gen.py`.
    - This will prepend the extracted governance rules to the corresponding legacy files as comments, creating the "Context-as-Code" encyclopedia.

4.  **Verification**:
    - Check the generated `-context` files to ensure that the "AI Dissertation" and "Short Summary" from Reversa are correctly injected.

## Constraints
- **Preserve Methodology**: Do NOT modify the PDD "Context-as-Code" injection method. It must remain unchanged.
- **Traceability**: Always maintain 🟢 CONFIRMED status where possible to ensure rule-to-code fidelity.

## Commands
- `/reversa-bridge`: Run the `scripts/reversa_to_pdd.py` bridge.
- `/reversa-pdd`: Run the full pipeline (Bridge + Manifest).
