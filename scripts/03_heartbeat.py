#!/usr/bin/env python3
import asyncio
import time
import sys
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from stitch import Stitch
from task_lib import get_pending_tasks, update_task_status
from agent_lib import AsyncAXiomEngineClient

class HeartbeatManager:
    """
    AXIOMENGINE HEARTBEAT (Phase 3+)
    Inspired by ArgentOS Always-On Loop.
    This script runs proactively to handle background tasks and system health.
    """
    def __init__(self, interval=60):
        self.stitch = Stitch()
        self.pi = AsyncAXiomEngineClient("Pi") 
        self.interval = interval

    async def run(self):
        print(f"AXiomEngine Heartbeat Active (Interval: {self.interval}s)")
        print("Monitoring tasks and system state...")
        
        while True:
            t_start = time.time()
            
            try:
                # 1. Fetch pending tasks from Postgres
                tasks = await get_pending_tasks(limit=5)
                
                if tasks:
                    print(f"Heartbeat: Found {len(tasks)} pending tasks. Initiating Pi contemplation...")
                    
                    task_summary = ""
                    for t in tasks:
                        task_summary += f"- [{t['id']}] {t['title']}: {t['description'] or 'No description'}\n"
                        # Mark as in_progress so we don't repeat immediately
                        await update_task_status(t['id'], 'in_progress')
                    
                    # Proactive Context Assembly
                    prompt = (
                        "## HEARTBEAT CONTEMPLATION\n"
                        "I have detected the following tasks in the system queue:\n\n"
                        f"{task_summary}\n"
                        "As Pi (Personal Intelligence), please review these tasks. "
                        "If any task can be addressed immediately, provide the solution. "
                        "If you need more information, ask. "
                        "If these are background tasks, acknowledge them and state their current priority."
                    )
                    
                    # Trigger Pi turn
                    # We use qwen3.6 for quick analysis
                    try:
                        response = await self.pi.chat(prompt, model="qwen3.6:35b", tags=["heartbeat", "proactive"])
                        content = response['choices'][0]['message']['content']
                        print(f"\n--- Pi's Heartbeat Response ---\n{content[:500]}...\n")
                    except Exception as chat_err:
                        print(f"Heartbeat: Pi Chat Error: {chat_err}")
                    
                    # Log to Valkey that we processed tasks
                    self.stitch.client.set("axiomengine:heartbeat:last_action", f"Processed {len(tasks)} tasks")
                
                else:
                    # Optional: Low-frequency system health check
                    pass

                # 2. Update 'Last Tick' in Valkey
                self.stitch.client.set("axiomengine:heartbeat:last_tick", time.time())
                
            except Exception as e:
                print(f"Heartbeat Error: {e}")

            # 3. Calculate wait time
            elapsed = time.time() - t_start
            wait = max(1, self.interval - elapsed)
            await asyncio.sleep(wait)

async def main():
    manager = HeartbeatManager(interval=60)
    await manager.run()

if __name__ == "__main__":
    asyncio.run(main())
