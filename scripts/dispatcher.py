#!/usr/bin/env python3
import asyncio
import json
import sys
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from stitch import Stitch
from agent_lib import AsyncAXiomEngineClient

class PiDispatcher:
    """
    AXIOMENGINE PI DISPATCHER
    Inspired by @codewithkenzo/pi-dispatch.
    Intelligently routes tasks to specialized subagents.
    """
    def __init__(self):
        self.stitch = Stitch()
        self.router = AsyncAXiomEngineClient("Dispatcher")
        self.agent_registry = {
            "coding": "Pi",
            "planning": "Archon",
            "research": "Pi", # Can be scaled to 'Researcher' later
            "review": "Archon"
        }

    async def route_task(self, task_data: dict):
        """Determine the best agent for the task and dispatch it."""
        task_id = task_data.get('id', 'unknown')
        intent = task_data.get('intent', 'general')
        payload = task_data.get('payload', '')
        
        print(f"Dispatcher: Routing Task {task_id} (Intent: {intent})")
        
        # Simple intent-based routing
        target_agent = self.agent_registry.get(intent, "Pi")
        
        # Publish to the agent's specific channel in Stitch
        self.stitch.send_task(target_agent, "EXECUTE", {
            "task_id": task_id,
            "instruction": payload,
            "origin": task_data.get('sender', 'system')
        }, sender="Dispatcher")
        
        print(f"Dispatcher: Task {task_id} sent to {target_agent}")

    async def run(self):
        print("AXiomEngine Pi Dispatcher Active. Listening on 'stitch:tasks:system'...")
        while True:
            try:
                # Listen for system-wide tasks
                task = self.stitch.get_task("system", timeout=10)
                if task:
                    await self.route_task(task)
            except Exception as e:
                print(f"Dispatcher Error: {e}")
                await asyncio.sleep(5)

if __name__ == "__main__":
    dispatcher = PiDispatcher()
    asyncio.run(dispatcher.run())
