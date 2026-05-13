#!/usr/bin/env python3
import asyncio
import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add current dir and parent to path
sys.path.append(str(Path(__file__).parent))

class ArchonExtendedHarness:
    def __init__(self, target_dirs: List[str]):
        self.target_dirs = [Path(d) for d in target_dirs]
        self.governance_library = []
        self.global_queue = []

    def extract_rules_from_text(self, content: str, file_name: str, prefix: str) -> List[Dict[str, str]]:
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
                        "id": f"G-{prefix}-{file_name.split('.')[0].upper()}-{len(rules)+1:03}",
                        "section": current_section,
                        "rule": rule_text,
                        "source": file_name
                    })
        return rules

    async def audit_file(self, md_path: Path):
        # Determine prefix based on parent folder
        parent_name = md_path.parent.name.upper().replace(".", "")
        prefix = f"ARCHON-{parent_name}"
        
        print(f"Symphony: Deep Auditing {prefix} File: {md_path.name}...")
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                content = f.read()
        except:
            return

        rules = self.extract_rules_from_text(content, md_path.name, prefix)
        self.governance_library.extend(rules)
        
        # Create Active Checklist
        checklist_content = f"# Active {prefix} Checklist: {md_path.name}\n\n"
        for r in rules:
            checklist_content += f"- [ ] {r['id']}: {r['rule']} (Section: {r['section']})\n"
            self.global_queue.append(f"{r['id']} | {md_path.name} | {r['rule']}")

        checklist_path = md_path.with_suffix(".checklist.md")
        with open(checklist_path, "w") as f:
            f.write(checklist_content)

    async def run(self):
        tasks = []
        for d in self.target_dirs:
            if not d.exists(): continue
            for md_file in d.rglob("*.md"):
                if md_file.suffix == ".md" and not md_file.name.endswith(".checklist.md"):
                    tasks.append(self.audit_file(md_file))
        
        await asyncio.gather(*tasks)
        
        # Append to Archon Governance Library
        lib_path = Path("/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/docs/Archon_Governance_Library.md")
        with open(lib_path, "a") as f:
            f.write(f"\n## Extended Archon Governance (Sub-Folders)\n\n")
            for r in self.governance_library:
                f.write(f"| {r['id']} | {r['section']} | {r['rule']} | {r['source']} |\n")

        # Update Global Queue
        queue_path = Path("/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/docs/GLOBAL_IMPLEMENTATION_QUEUE.md")
        with open(queue_path, "a") as f:
            f.write(f"\n## Archon Extended Queue\n\n")
            for q in self.global_queue:
                f.write(f"| {q} |\n")

        print(f"Symphony: Extended Audit Complete. Generated {len(self.governance_library)} rules.")

if __name__ == "__main__":
    dirs = [
        "/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/archon/.archon/maintainer-standup",
        "/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/archon/.claude",
        "/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects/axiomengine/archon/.github"
    ]
    harness = ArchonExtendedHarness(dirs)
    asyncio.run(harness.run())
