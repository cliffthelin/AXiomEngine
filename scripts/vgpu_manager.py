#!/usr/bin/env python3
import time
import sys
import json
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from stitch import Stitch

class VGPUManager:
    """
    AXIOMENGINE VGPU MANAGER (Phase 4 Enhancement)
    Logically partitions VRAM between concurrent agents to prevent OOM.
    Total VRAM: 32,000 MiB (8192 + 23040 roughly)
    """
    TOTAL_VRAM = 31000 # Safety margin
    
    def __init__(self):
        self.stitch = Stitch()
        self.key = "axiomengine:vgpu:allocation"

    def get_allocation(self):
        if not self.stitch.client:
            return {}
        data = self.stitch.client.get(self.key)
        if data:
            return json.loads(data)
        return {}

    def save_allocation(self, alloc):
        if not self.stitch.client:
            return
        self.stitch.client.set(self.key, json.dumps(alloc))

    def reserve(self, agent_name: str, amount_mib: int):
        alloc = self.get_allocation()
        used = sum(alloc.values())
        
        if used + amount_mib > self.TOTAL_VRAM:
            print(f"VGPU: Reservation failed for {agent_name}. Request: {amount_mib}MiB, Available: {self.TOTAL_VRAM - used}MiB")
            return False
        
        alloc[agent_name] = amount_mib
        self.save_allocation(alloc)
        print(f"VGPU: Reserved {amount_mib}MiB for {agent_name}. Total used: {used + amount_mib}MiB")
        return True

    def release(self, agent_name: str):
        alloc = self.get_allocation()
        if agent_name in alloc:
            amount = alloc.pop(agent_name)
            self.save_allocation(alloc)
            print(f"VGPU: Released {amount}MiB from {agent_name}")
            return True
        return False

    def status(self):
        alloc = self.get_allocation()
        used = sum(alloc.values())
        print("\n── 🎮 VGPU Allocation Status ──────────────────")
        print(f"  Total VRAM: {self.TOTAL_VRAM} MiB")
        print(f"  Used:       {used} MiB")
        print(f"  Available:  {self.TOTAL_VRAM - used} MiB")
        print("───────────────────────────────────────────────")
        for agent, amt in alloc.items():
            print(f"  - {agent:15}: {amt} MiB")
        print("───────────────────────────────────────────────\n")

if __name__ == "__main__":
    mgr = VGPUManager()
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "reserve" and len(sys.argv) > 3:
            mgr.reserve(sys.argv[2], int(sys.argv[3]))
        elif cmd == "release" and len(sys.argv) > 2:
            mgr.release(sys.argv[2])
        elif cmd == "status":
            mgr.status()
    else:
        mgr.status()
        print("Usage: python vgpu_manager.py [reserve <agent> <mib> | release <agent> | status]")
