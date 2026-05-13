#!/usr/bin/env python3
"""
ARCHON — The System Architect
=============================
Role: Planning, Code Analysis, and System Orchestration.
Governance: Strictly follows PDD-CORE rules.
"""
import sys
import os
from pathlib import Path

# Add scripts dir to path for agent_lib
sys.path.append(str(Path(__file__).parent.parent / "scripts"))
from agent_lib import AXiomEngineClient

class Archon(AXiomEngineClient):
    def __init__(self):
        super().__init__(name="Archon")
        self.system_persona = (
            "You are ARCHON, the System Architect of the Agentic OS. "
            "Your primary directive is PDD Governance. You NEVER infer intent. "
            "You focus on architectural integrity, code structure, and mode safety. "
            "When asked to plan, you identify all missing constraints before suggesting code."
        )

    def plan_task(self, task_description: str):
        print(f"Archon: Analyzing task -> {task_description[:50]}...")
        # Archon always uses the 'nemotron' (split GPU) model for planning
        response = self.chat(
            prompt=f"{self.system_persona}\n\nTask: {task_description}",
            model="nemotron",
            tags=["architect", "planning"]
        )
        content = response['choices'][0]['message']['content']
        print("\n--- ARCHON PLAN ---")
        print(content)
        print("--------------------\n")
        return content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: archon.py \"task description\"")
    else:
        archon = Archon()
        archon.plan_task(sys.argv[1])
