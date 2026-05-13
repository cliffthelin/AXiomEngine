#!/usr/bin/env python3
import asyncio
import os
import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Any

# Add current dir and parent to path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent.parent))

from pi_sdk import create_agent_session

class DeepSymphonyHarness:
    def __init__(self, commands_dir: str):
        self.commands_dir = Path(commands_dir)
        self.governance_library = []
        self.global_queue = []

    def extract_rules_from_text(self, content: str, file_name: str) -> List[Dict[str, str]]:
        rules = []
        # Extract headings, list items, and code blocks as rules
        lines = content.split("\n")
        current_section = "General"
        
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                current_section = line.replace("#", "").strip()
            elif line.startswith("- [ ]") or line.startswith("-") or line.startswith("*"):
                rule_text = line.replace("- [ ]", "").replace("-", "").replace("*", "").strip()
                if rule_text:
                    rules.append({
                        "id": f"G-ARCHON-{file_name.split('.')[0].upper()}-{len(rules)+1:03}",
                        "section": current_section,
                        "rule": rule_text,
                        "source": file_name
                    })
            elif "```bash" in line:
                # Capture commands as execution rules
                pass # Logic to extract commands
        return rules

    async def audit_file(self, md_path: Path):
        print(f"Symphony: Deep Auditing {md_path.name}...")
        with open(md_path, "r") as f:
            content = f.read()

        rules = self.extract_rules_from_text(content, md_path.name)
        self.governance_library.extend(rules)
        
        # Create Active Checklist
        checklist_content = f"# Active Checklist: {md_path.name}\n\n"
        for r in rules:
            checklist_content += f"- [ ] {r['id']}: {r['rule']} (Section: {r['section']})\n"
            self.global_queue.append(f"{r['id']} | {md_path.name} | {r['rule']}")

        checklist_path = md_path.with_suffix(".checklist.md")
        with open(checklist_path, "w") as f:
            f.write(checklist_content)

    async def run(self):
        tasks = []
        for md_file in self.commands_dir.rglob("*.md"):
            if md_file.suffix == ".md" and not md_file.name.endswith(".checklist.md"):
                tasks.append(self.audit_file(md_file))
        
        await asyncio.gather(*tasks)
        
        # Write Governance Library
        lib_path = Path("/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/docs/Archon_Governance_Library.md")
        with open(lib_path, "w") as f:
            f.write("# Archon Deep Governance Library\n\n")
            f.write("| Rule ID | Section | Rule Description | Source File |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            for r in self.governance_library:
                f.write(f"| {r['id']} | {r['section']} | {r['rule']} | {r['source']} |\n")

        # Write Global Queue
        queue_path = Path("/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/docs/GLOBAL_IMPLEMENTATION_QUEUE.md")
        with open(queue_path, "w") as f:
            f.write("# Global Implementation Queue\n\n")
            f.write("| Rule ID | Source | Task Description |\n")
            f.write("| :--- | :--- | :--- |\n")
            for q in self.global_queue:
                f.write(f"| {q} |\n")

        print(f"Symphony: Deep Audit Complete. Generated {len(self.governance_library)} rules.")

if __name__ == "__main__":
    path = "/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/archon/.archon/commands"
    harness = DeepSymphonyHarness(path)
    asyncio.run(harness.run())
