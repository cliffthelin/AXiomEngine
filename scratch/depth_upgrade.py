import sys
from pathlib import Path

path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/scripts/DataCatalogFactory.py")
content = path.read_text()

# Upgrade the dissertation prompt for maximum depth
old_prompt = """        GOVERNANCE ARCHITECT REPORT: {rule['id']}
        CONTEXT: {rule['text']}
        STRUCTURAL ANCHOR: {graph_context.get('related_files', [])[:3]}
        IMPLEMENTATION STATUS: {code_found if code_found else 'Not physically anchored'}
        
        Write an exhaustive 5000-character technical dissertation.
        Include Philosophical Intent, Architectural Necessity, Control Specifications, and Security Impact."""

new_prompt = """        GOVERNANCE ARCHITECT REPORT: {rule['id']}
        CONTEXT: {rule['text']}
        STRUCTURAL ANCHOR: {graph_context.get('related_files', [])[:10]}
        IMPLEMENTATION STATUS: {code_found if code_found else 'Not physically anchored'}
        
        ### MANDATE: DONE RIGHT > DONE NOW ###
        Write an EXHAUSTIVE 5000+ character technical dissertation including:
        I. PHILOSOPHICAL INTENT: The deeper 'Why' and the logical sovereignty this rule provides.
        II. ARCHITECTURAL NECESSITY: How this specific rule prevents entropy across the related files.
        III. SECURITY THREAT MODEL: Potential vulnerabilities if this rule is bypassed.
        IV. TDD VERIFICATION: Precise RED/GREEN test scenarios for CLI, TUI, and GUI.
        V. COMPLIANCE ANCHOR: How this rule maps to the global PDD Axioms.
        
        Be precise, technical, and encyclopedic."""

content = content.replace(old_prompt, new_prompt)

path.write_text(content)
print("Governance Depth Upgrade applied: Prompt now enforces 'Done Right' mantra.")
