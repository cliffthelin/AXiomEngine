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

class PiDeepGovernanceHarness:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir)
        self.governance_library = []
        self.global_queue = []

    def extract_rules_from_text(self, content: str, file_name: str) -> List[Dict[str, str]]:
        rules = []
        lines = content.split("\n")
        current_section = "General"
        
        for line in lines:
            line = line.strip()
            if line.startswith("#"):
                current_section = line.replace("#", "").strip()
            elif line.startswith("- [ ]") or line.startswith("-") or line.startswith("*"):
                rule_text = line.replace("- [ ]", "").replace("-", "").replace("*", "").strip()
                if rule_text and len(rule_text) > 5:
                    rules.append({
                        "id": f"G-PI-{file_name.split('.')[0].upper()}-{len(rules)+1:03}",
                        "section": current_section,
                        "rule": rule_text,
                        "source": file_name
                    })
            elif "```" in line:
                # Capture code blocks as implementation patterns
                pass
        return rules

    async def audit_file(self, md_path: Path):
        print(f"Symphony: Deep Auditing PI File: {md_path.name}...")
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            return

        rules = self.extract_rules_from_text(content, md_path.name)
        self.governance_library.extend(rules)
        
        # Create Active Checklist
        checklist_content = f"# Active PI Checklist: {md_path.name}\n\n"
        for r in rules:
            checklist_content += f"- [ ] {r['id']}: {r['rule']} (Section: {r['section']})\n"
            self.global_queue.append(f"{r['id']} | {md_path.name} | {r['rule']}")

        checklist_path = md_path.with_suffix(".checklist.md")
        with open(checklist_path, "w") as f:
            f.write(checklist_content)

    async def run(self):
        tasks = []
        for md_file in self.target_dir.rglob("*.md"):
            if md_file.suffix == ".md" and not md_file.name.endswith(".checklist.md"):
                tasks.append(self.audit_file(md_file))
        
        await asyncio.gather(*tasks)
        
        # Write PI Governance Library
        lib_path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/docs/PI_Governance_Library.md")
        with open(lib_path, "w") as f:
            f.write("# PI Deep Governance Library\n\n")
            f.write("| Rule ID | Section | Rule Description | Source File |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            for r in self.governance_library:
                f.write(f"| {r['id']} | {r['section']} | {r['rule']} | {r['source']} |\n")

        # Update Global Queue
        queue_path = Path("/mnt/UBUNTU_8TB/Projects/axiomengine/docs/GLOBAL_IMPLEMENTATION_QUEUE.md")
        with open(queue_path, "a") as f:
            f.write("\n## PI Implementation Queue\n\n")
            for q in self.global_queue:
                f.write(f"| {q} |\n")

        print(f"Symphony: PI Deep Audit Complete. Generated {len(self.governance_library)} PI rules.")

if __name__ == "__main__":
    path = "/mnt/UBUNTU_8TB/Projects/axiomengine/pi"
    harness = PiDeepGovernanceHarness(path)
    asyncio.run(harness.run())
