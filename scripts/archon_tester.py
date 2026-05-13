#!/usr/bin/env python3
import asyncio
import json
import subprocess
import sys
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from agent_lib import AsyncAXiomEngineClient
from stitch import Stitch

class ArchonTestHarness:
    """
    ARCHON TEST HARNESS
    System-level health and integration testing orchestrated by Archon.
    """
    def __init__(self):
        self.archon = AsyncAXiomEngineClient("Archon")
        self.stitch = Stitch()
        self.results = []

    async def run_unit_test(self, name: str, cmd: list):
        """Runs a subprocess test and captures result."""
        print(f"Archon: Testing {name}...")
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            success = process.returncode == 0
            self.results.append({
                "test": name,
                "status": "PASS" if success else "FAIL",
                "output": stdout.decode() if success else stderr.decode()
            })
            return success
        except Exception as e:
            self.results.append({"test": name, "status": "ERROR", "output": str(e)})
            return False

    async def run_all_tests(self):
        print("Archon: Initiating Full System Integration Test...")
        
        # 1. Test TOON (Token-efficient Object Notation)
        await self.run_unit_test("TOON Encoder/Decoder", [sys.executable, "scripts/test_toon.py"])
        
        # 2. Test Smart Fetch (Network Driver)
        # Testing a local-ish or reliable site to avoid hang
        await self.run_unit_test("Smart Fetch", [sys.executable, "scripts/smart_fetch.py", "https://example.com"])
        
        # 3. Test Knowledge Graph / AST Indexer
        await self.run_unit_test("AST Indexer", [sys.executable, "scripts/ast_indexer.py"])
        await self.run_unit_test("Knowledge Graph", [sys.executable, "scripts/knowledge_graph.py"])
        
        # 4. Test Security (UAC & Sandbox)
        await self.run_unit_test("UAC Logic", [sys.executable, "scripts/uac.py", "ls -l"])
        await self.run_unit_test("CGroup Sandbox", [sys.executable, "scripts/sandbox.py", "test_agent", "ls"])
        
        # 5. Test Intent Mapper
        await self.run_unit_test("Intent Mapper", [sys.executable, "scripts/intent_mapper.py"])

        # 6. Test Keychain
        await self.run_unit_test("Keychain Init", [sys.executable, "scripts/keychain.py"])

        # 6. Report to Stitch
        self.stitch.client.set("axiomengine:test_harness:last_results", json.dumps(self.results))
        self.stitch.client.set("axiomengine:test_harness:last_run", str(asyncio.get_event_loop().time()))
        
        print(f"Archon: Testing complete. {sum(1 for r in self.results if r['status'] == 'PASS')}/{len(self.results)} passed.")
        return self.results

if __name__ == "__main__":
    harness = ArchonTestHarness()
    asyncio.run(harness.run_all_tests())
