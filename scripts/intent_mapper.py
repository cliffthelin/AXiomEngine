#!/usr/bin/env python3
import re
import json
from pathlib import Path

class IntentMapper:
    """
    AXIOMENGINE INTENT MAPPER (Phase 3)
    Extracts goals from Markdown files and maps them to agent tasks.
    """
    def __init__(self, root_dir="."):
        self.root_dir = Path(root_dir)
        self.intent_map = {}

    def scan_roadmap(self):
        """Parses ROADMAP.md for uncompleted [ ] items."""
        roadmap_path = self.root_dir / "ROADMAP.md"
        if not roadmap_path.exists():
            return []
        
        with open(roadmap_path, "r") as f:
            content = f.read()
            
        # Match uncompleted tasks: - [ ] **Task Name**: Description
        matches = re.findall(r"- \[ \] \*\*(.*?)\*\*: (.*)", content)
        return [{"intent": m[0], "description": m[1], "source": "ROADMAP.md"} for m in matches]

    def map_to_agent(self, task):
        """Maps an intent to a specific agent (Pi or Archon)."""
        intent = task['intent'].lower()
        if any(w in intent for w in ["sandbox", "vm", "resource", "cgroup", "gpu"]):
            return "Archon" # System/Architecture tasks
        return "Pi" # General/User tasks

    def generate_task_payloads(self):
        tasks = self.scan_roadmap()
        payloads = []
        for t in tasks:
            t['assigned_agent'] = self.map_to_agent(t)
            payloads.append(t)
        return payloads

if __name__ == "__main__":
    mapper = IntentMapper()
    payloads = mapper.generate_task_payloads()
    print(json.dumps(payloads, indent=2))
