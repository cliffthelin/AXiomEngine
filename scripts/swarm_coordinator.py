#!/usr/bin/env python3
import asyncio
import json
import sys
import uuid
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from stitch import Stitch
from agent_lib import AsyncAXiomEngineClient
from sync_state import SyncState
from propose_rule import propose_rule

class SwarmCoordinator:
    """
    AXIOMENGINE SWARM COORDINATOR (Phase 6)
    Manages multi-agent collaboration by decomposing high-level goals.
    """
    def __init__(self):
        self.stitch = Stitch()
        self.planner = AsyncAXiomEngineClient("Archon") # Using Archon for planning
        self.sync = SyncState()
        self.workers = {
            "coding": "Pi",
            "review": "Archon",
            "security": "Guardian" # Placeholder for future agent
        }

    async def decompose_goal(self, goal: str) -> list:
        """Use Archon to break down a goal into sub-tasks."""
        prompt = (
            "## GOAL DECOMPOSITION REQUEST\n"
            f"Goal: {goal}\n\n"
            "As the Architect (Archon), please break this goal down into 2-4 atomic sub-tasks. "
            "Return ONLY a JSON list of objects with 'title', 'intent' (coding, review, research), and 'payload'.\n"
            "Follow R-PDD-SWARM-001."
        )
        
        try:
            # We request 12GB VRAM for planning
            response = await self.planner.chat(prompt, model="nemotron", vram_mib=12000)
            content = response['choices'][0]['message']['content']
            # Basic JSON extraction
            start = content.find("[")
            end = content.rfind("]") + 1
            return json.loads(content[start:end])
        except Exception as e:
            print(f"Swarm: Planning failed: {e}")
            return []

    async def execute_swarm(self, goal: str):
        swarm_id = str(uuid.uuid4())[:8]
        print(f"🚀 Initializing Swarm {swarm_id} for goal: {goal}")
        
        # Initialize shared state for this swarm
        self.sync.namespace = f"axiomengine:swarm:{swarm_id}"
        self.sync.set("goal", goal, agent_id="Coordinator")
        self.sync.set("status", "planning", agent_id="Coordinator")
        
        # 1. Decomposition
        subtasks = await self.decompose_goal(goal)
        if not subtasks:
            print("❌ Swarm: Could not decompose goal. Aborting.")
            self.sync.set("status", "failed", agent_id="Coordinator")
            return

        self.sync.set("status", "executing", agent_id="Coordinator")
        self.sync.set("subtasks_count", len(subtasks), agent_id="Coordinator")
        print(f"Swarm {swarm_id}: Decomposed into {len(subtasks)} sub-tasks.")
        
        # 2. Dispatch
        for i, task in enumerate(subtasks):
            intent = task.get('intent', 'coding')
            target = self.workers.get(intent, "Pi")
            print(f"  [{i+1}] Dispatching '{task['title']}' to {target}...")
            
            self.stitch.send_task(target, "EXECUTE", {
                "swarm_id": swarm_id,
                "task_id": f"{swarm_id}-{i}",
                "instruction": task['payload'],
                "pdd_rules": ["R-PDD-SWARM-001"],
                "sync_namespace": self.sync.namespace
            }, sender=f"Swarm-{swarm_id}")

        print(f"✅ Swarm {swarm_id} dispatched. Monitoring channels...")
        
        # In a real system, we would wait for 'COMPLETED' events on Stitch.
        # For this implementation, we wait a bit and then finalize.
        await asyncio.sleep(5) 
        await self.finalize_and_document(goal, swarm_id)

    async def finalize_and_document(self, goal: str, swarm_id: str):
        """Final phase: Archon documents changes and updates governance."""
        print(f"🧐 Swarm {swarm_id}: Archon is finalizing and documenting...")
        
        # 1. ARCHON ANALYSIS
        prompt = (
            "## FINALIZATION & DOCUMENTATION REQUEST\n"
            f"Goal: {goal}\n"
            "The execution phase is complete. Please:\n"
            "1. Generate a brief markdown summary of the work done.\n"
            "2. Identify if any new governance rules (PDD) are needed based on this work.\n"
            "3. Provide a 'Proposed Rule' if applicable.\n"
            "Return JSON: {'summary': '...', 'new_rule': {'rule_id': '...', 'content': '...', 'rationale': '...'}}"
        )
        
        try:
            response = await self.planner.chat(prompt, model="nemotron", vram_mib=8192)
            content = response['choices'][0]['message']['content']
            # Extraction logic...
            start = content.find("{")
            end = content.rfind("}") + 1
            data = json.loads(content[start:end])
            
            # 2. UPDATE PROJECT ARTIFACTS
            ws_path = Path(f"./workspaces/swarm_{swarm_id}")
            ws_path.mkdir(parents=True, exist_ok=True)
            ctx_path = ws_path / ".context"
            ctx_path.mkdir(exist_ok=True)
            
            with open(ctx_path / "GOVERNANCE_DELTA.md", "w") as f:
                f.write(f"# Swarm {swarm_id} Summary\n\n{data.get('summary', 'No summary provided.')}")
            
            # 3. PROPOSE PDD RULE
            if data.get('new_rule'):
                rule = data['new_rule']
                await propose_rule(
                    rule_id=rule['rule_id'],
                    agent_name="Archon",
                    change_type="new",
                    content=rule['content'],
                    rationale=rule['rationale'],
                    title=f"Auto-generated rule from Swarm {swarm_id}"
                )
            
            self.sync.set("status", "completed", agent_id="Coordinator")
            print(f"✅ Swarm {swarm_id} fully documented and refined.")
            
        except Exception as e:
            print(f"Swarm: Finalization failed: {e}")
            self.sync.set("status", "finalization_error", agent_id="Coordinator")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        goal = " ".join(sys.argv[1:])
        coord = SwarmCoordinator()
        asyncio.run(coord.execute_swarm(goal))
    else:
        print("Usage: python swarm_coordinator.py <high-level goal>")
