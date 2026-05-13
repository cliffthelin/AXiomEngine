#!/usr/bin/env python3
import os
import subprocess
import json
import sys
from pathlib import Path

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from stitch import Stitch
from sync_state import SyncState

class AtlasBridge:
    """
    AXIOMENGINE ATLAS BRIDGE
    Integrates @wizdear/atlas-code into the AXiomEngine multi-agent swarm.
    """
    def __init__(self):
        self.stitch = Stitch()
        self.sync = SyncState()
        self.nvm_dir = os.path.expanduser("~/.nvm")
        self.node_setup = rf'export NVM_DIR="{self.nvm_dir}" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && nvm use 22 > /dev/null'

    def _run_acode(self, cmd: str, project_path: str = None):
        """Execute acode command with Node.js environment."""
        cwd = project_path or os.getcwd()
        full_cmd = f"{self.node_setup} && acode {cmd}"
        
        # Inject Router as OpenAI endpoint
        env = os.environ.copy()
        env["OPENAI_API_BASE"] = "http://localhost:9001/v1"
        env["OPENAI_API_KEY"] = "axiomengine-atlas-internal"
        
        print(f"Atlas: Executing 'acode {cmd}' in {cwd}...")
        return subprocess.run(full_cmd, shell=True, cwd=cwd, env=env, capture_output=True, text=True)

    def setup(self):
        """Run acode setup."""
        print("Atlas: Running global setup...")
        res = self._run_acode("setup")
        return res.returncode == 0

    def start_engineering(self, goal: str, project_path: str):
        """Start a multi-agent engineering pipeline for a goal."""
        # For non-interactive integration, we might need a specific 'acode' flag 
        # or use a generated 'acode.json' config.
        # As per README, 'acode' usually launches an interactive session.
        # We will attempt to pass the goal via stdin or a flag if supported.
        print(f"Atlas: Starting engineering pipeline for: {goal}")
        
        # We'll use the 'swarm_coordinator' to track this.
        swarm_id = f"atlas-{os.urandom(4).hex()}"
        self.sync.namespace = f"axiomengine:swarm:{swarm_id}"
        self.sync.set("goal", goal, agent_id="AtlasBridge")
        self.sync.set("status", "running", agent_id="AtlasBridge")
        
        # Launch acode (simulating user input for the goal)
        # Note: If acode requires TTY, this might need 'pexpect' or similar.
        res = self._run_acode(f"--goal '{goal}'", project_path=project_path)
        
        if res.returncode == 0:
            self.sync.set("status", "completed", agent_id="AtlasBridge")
        else:
            self.sync.set("status", "failed", agent_id="AtlasBridge")
            print(f"Atlas Error: {res.stderr}")
        
        return res.stdout

if __name__ == "__main__":
    bridge = AtlasBridge()
    if len(sys.argv) > 2:
        bridge.start_engineering(sys.argv[1], sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "setup":
        bridge.setup()
    else:
        print("Usage: python atlas_bridge.py <goal> <project_path>")
