#!/usr/bin/env python3
import asyncio
import time
import sys
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from stitch import Stitch
from agent_lib import AsyncAXiomEngineClient

class BehaviorMonitor:
    """
    AXIOMENGINE BEHAVIOR MONITOR
    Inspired by @davidorex/pi-behavior-monitors.
    Continuously audits agent outputs for PDD drift and system health.
    """
    def __init__(self, check_interval=300): # Check every 5 mins
        self.stitch = Stitch()
        self.pi = AsyncAXiomEngineClient("BehaviorMonitor")
        self.interval = check_interval
        self.last_check_id = 0

    async def run(self):
        print("AXiomEngine Behavior Monitor Active")
        while True:
            try:
                # 1. Connect to Postgres (via Stitch or direct)
                import asyncpg
                PG_DSN = "postgresql://axiomengine:axiomengine_local_dev@localhost:5433/axiomengine"
                conn = await asyncpg.connect(PG_DSN)
                
                # 2. Fetch latest audit logs
                logs = await conn.fetch(
                    "SELECT id, agent_name, drift_flag, created_at FROM agent_audit WHERE id > $1 ORDER BY id ASC LIMIT 50",
                    self.last_check_id
                )
                
                if logs:
                    drift_count = sum(1 for l in logs if l['drift_flag'])
                    print(f"Monitor: Audited {len(logs)} turns. Detected {drift_count} drifts.")
                    
                    if drift_count > 0:
                        # Alert Pi/Archon via Stitch
                        self.stitch.publish("alerts", {
                            "type": "BEHAVIOR_DRIFT",
                            "severity": "high" if drift_count > 2 else "medium",
                            "message": f"Detected {drift_count} PDD rule violations in the last batch.",
                            "details": [l['id'] for l in logs if l['drift_flag']]
                        })
                    
                    self.last_check_id = logs[-1]['id']

                await conn.close()
                
                # 3. Update Status
                self.stitch.client.hset("stitch:agent_status", "behavior_monitor", "online")
                
            except Exception as e:
                print(f"Monitor Error: {e}")

            await asyncio.sleep(self.interval)

if __name__ == "__main__":
    monitor = BehaviorMonitor()
    asyncio.run(monitor.run())
