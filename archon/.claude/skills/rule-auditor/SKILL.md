# Rule Auditor Skill

Skill for performing atomic scrutiny audits on governance rules, aligning them with codebase implementation, and generating metadata (summaries, keywords).

## Protocol

1. **Alignment**: Search the codebase for the specific Rule ID or associated logic.
2. **Metadata Generation**:
   - Create a detailed summary (max 500 chars).
   - Extract a JSON array of tags/keywords.
3. **Interface Audit**:
   - Check if the rule is exposed in CLI (pi.py/scripts), TUI (pi_tui.py), or GUI (remote_gateway.py).
   - Mark as "Missing" if not found.
4. **JSON Export**: Write the result to a hierarchical JSON structure.
