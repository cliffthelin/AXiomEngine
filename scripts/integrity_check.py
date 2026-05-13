#!/usr/bin/env python3
import asyncio
import os
import sys
import json
import httpx
from pathlib import Path
from datetime import datetime

# Add scripts dir to path for imports
sys.path.append(str(Path(__file__).parent))

from agent_lib import AsyncAXiomEngineClient
from swarm_coordinator import SwarmCoordinator

class SystemIntegrityCheck:
    def __init__(self):
        self.router_url = "http://localhost:9001"
        self.results = []

    def log(self, stage, status, details=""):
        res = {"timestamp": datetime.now().isoformat(), "stage": stage, "status": status, "details": details}
        self.results.append(res)
        icon = "✅" if status == "PASS" else "❌"
        print(f"{icon} [{stage}] {status}: {details}")

    async def check_router(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.router_url}/health")
                if resp.status_code == 200:
                    self.log("ROUTER", "PASS", "Health endpoint responded OK")
                else:
                    self.log("ROUTER", "FAIL", f"HTTP {resp.status_code}")
        except Exception as e:
            self.log("ROUTER", "FAIL", str(e))

    async def check_pdd(self):
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self.router_url}/admin/audit?limit=1")
                if resp.status_code == 200:
                    self.log("PDD_GOVERNANCE", "PASS", "Postgres Audit logs accessible")
                else:
                    self.log("PDD_GOVERNANCE", "FAIL", f"HTTP {resp.status_code}")
        except Exception as e:
            self.log("PDD_GOVERNANCE", "FAIL", str(e))

    async def run_swarm_test(self):
        print("🚀 Starting Swarm Integrity Check...")
        coord = SwarmCoordinator()
        goal = "Run a system-wide integrity check including security and documentation hooks."
        try:
            await coord.execute_swarm(goal)
            self.log("SWARM_LIFECYCLE", "PASS", "Full swarm cycle completed successfully")
        except Exception as e:
            self.log("SWARM_LIFECYCLE", "FAIL", str(e))

    async def run_maintenance_test(self):
        try:
            # Import and run pruner
            from kg_pruner import prune_kg
            prune_kg()
            self.log("MAINTENANCE", "PASS", "KG Pruner executed successfully")
        except Exception as e:
            self.log("MAINTENANCE", "FAIL", str(e))

    async def run_all(self):
        print("=== AXIOMENGINE SYSTEM INTEGRITY CHECK ===")
        await self.check_router()
        await self.check_pdd()
        await self.run_maintenance_test()
        await self.run_swarm_test()
        
        print("\n=== FINAL REPORT ===")
        all_pass = all(r['status'] == "PASS" for r in self.results)
        if all_pass:
            print("🌟 SYSTEM INTEGRITY VERIFIED 🌟")
        else:
            print("⚠️ SYSTEM INTEGRITY COMPROMISED ⚠️")

if __name__ == "__main__":
    checker = SystemIntegrityCheck()
    asyncio.run(checker.run_all())
