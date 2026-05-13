#!/usr/bin/env python3
"""
Archon Execution Harness
========================
Role: Policy-Driven Monitoring and Autonomous Recovery.
Pattern: Reads L3 Policies -> Monitors L1 Reality -> Resolves Drift.
"""
import os
import time
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Paths
ROOT_DIR = Path("/mnt/UBUNTU_8TB/Projects/axiomengine")
SCRIPTS_DIR = ROOT_DIR / "scripts"
POLICIES_FILE = ROOT_DIR / "data" / "archon_policies.json"
ORCHESTRATOR_LOG = ROOT_DIR / "mission_orchestrator.log"
INTENT_INDEX = ROOT_DIR / "INTENT_INDEX.json"
VENV_PYTHON = "/run/media/cane/f2a4492f-959f-4385-b87a-134ac4769088/home/cane/.axiomengine_venv/bin/python3"

class ArchonHarness:
    def __init__(self):
        self.load_policies()
        self.last_log_mtime = 0
        if ORCHESTRATOR_LOG.exists():
            self.last_log_mtime = ORCHESTRATOR_LOG.stat().st_mtime

    def load_policies(self):
        with open(POLICIES_FILE, 'r') as f:
            self.policies = json.load(f)["monitoring_policies"]

    def log_event(self, policy_id, action, status):
        """Writes a Layer 13 Process Record for the event."""
        record = {
            "timestamp": datetime.now().isoformat(),
            "policy_id": policy_id,
            "action_taken": action,
            "status": status,
            "provenance": "Archon Autonomous Harness"
        }
        # Append to a dedicated process log
        proc_log = ROOT_DIR / "data" / "governance_process_history.jsonl"
        with open(proc_log, 'a') as f:
            f.write(json.dumps(record) + "\n")
        print(f"🛡️ [ARCHON] Policy {policy_id} -> {action} ({status})")

    def get_gpu_util(self):
        try:
            cmd = "nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits -i 1"
            return int(subprocess.check_output(cmd, shell=True).decode().strip())
        except: return 0

    def check_and_enforce(self):
        gpu_util = self.get_gpu_util()
        is_running = "mission_orchestrator.py" in subprocess.check_output(["ps", "aux"]).decode()

        for pol in self.policies:
            if pol["name"] == "Saturation Enforcement":
                if is_running and gpu_util < pol["threshold"]:
                    # Check if idle for too long (simplified here, in reality we'd track duration)
                    self.log_event(pol["id"], "STALL_DETECTED", "RESTARTING")
                    subprocess.run("pkill -f mission_orchestrator.py", shell=True)
                    self.relaunch()

            if pol["name"] == "Heartbeat Continuity":
                if ORCHESTRATOR_LOG.exists():
                    mtime = ORCHESTRATOR_LOG.stat().st_mtime
                    if (time.time() - mtime) > pol["threshold_seconds"]:
                        self.log_event(pol["id"], "LOG_STALE", "RECOVERY")
                        subprocess.run("pkill -f mission_orchestrator.py", shell=True)
                        self.relaunch()

            if pol["name"] == "Service Availability":
                ollama_active = "ollama" in subprocess.check_output(["ps", "aux"]).decode()
                if not ollama_active:
                    self.log_event(pol["id"], "SERVICE_DOWN", "RESTARTING_OLLAMA")
                    subprocess.run("snap restart ollama", shell=True)

        if not is_running:
            self.log_event("SYS-AUTO", "MISSION_NOT_RUNNING", "RELAUNCHING")
            self.relaunch()

    def relaunch(self):
        cmd = f"nohup {VENV_PYTHON} {SCRIPTS_DIR}/mission_orchestrator.py > {ORCHESTRATOR_LOG} 2>&1 &"
        subprocess.Popen(cmd, shell=True)

    def run(self):
        print("🏛️ Archon Execution Harness Active (Policy-Driven).")
        while True:
            try:
                self.check_and_enforce()
            except Exception as e:
                print(f"Error in harness: {e}")
            time.sleep(60)

if __name__ == "__main__":
    harness = ArchonHarness()
    harness.run()
