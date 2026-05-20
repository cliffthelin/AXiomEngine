#!/usr/bin/env python3
"""
Governance Mission Orchestrator v5 — PROMPT FILE MODE
=====================================================
Role: Queues sharded tasks using --prompt-file to avoid shell arg limits.
"""
import os
import time
import subprocess
import glob
from pathlib import Path

# Paths
ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT_DIR / "scripts"
VENV_PYTHON = "/run/media/cane/f2a4492f-959f-4385-b87a-134ac4769088/home/cane/.axiomengine_venv/bin/python3"

SHARDS = [
    {
        "name": "orchestration",
        "targets": ["scripts/*.py", "core/*.ts"],
        "skill": "reversa-strategist",
        "prompt": "Extract orchestration & lifecycle rules. Focus on venv, heartbeat, and task routing."
    },
    {
        "name": "resource",
        "targets": ["scripts/gpu_*.py", "scripts/mission_*.py", "start_axiomengine.sh"],
        "skill": "reversa-visor",
        "prompt": "Extract hardware & resource constraints. Focus on P40 power, VRAM, and thermal limits."
    },
    {
        "name": "security",
        "targets": ["scripts/auth_manager.py", "scripts/reversa_to_pdd.py"],
        "skill": "reversa-strategist",
        "prompt": "Extract security & identity rules. Focus on PII, audit trails, and secret resolution."
    }
]

def log_mission(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] 🚀 {msg}")

def run_task(name, command):
    log_mission(f"Starting Task: {name}")
    start_time = time.time()
    try:
        subprocess.run(command, shell=True, check=True)
        duration = time.time() - start_time
        log_mission(f"✅ Completed Task: {name} (Duration: {duration:.1f}s)")
        return True
    except subprocess.CalledProcessError as e:
        log_mission(f"❌ Failed Task: {name}. Error: {e}")
        return False

def get_file_context(targets):
    context = ""
    for pattern in targets:
        full_pattern = str(ROOT_DIR / pattern)
        files = glob.glob(full_pattern)
        for f in files:
            try:
                with open(f, 'r') as file:
                    context += f"\n--- FILE: {os.path.basename(f)} ---\n"
                    context += file.read()[:5000] # Increased context per file
            except:
                pass
    return context

def main():
    log_mission("Initializing Sharded Governance Mission v5 (PROMPT FILE)...")

    for shard in SHARDS:
        log_mission(f"--- SHARD: {shard['name'].upper()} ---")
        
        out_file = ROOT_DIR / "_reversa_sdd" / f"{shard['name']}.md"
        # Skip if already exists and non-empty (to save time, or remove to re-run)
        # if out_file.exists() and out_file.stat().st_size > 0:
        #     log_mission(f"⏩ Shard {shard['name']} already exists. Skipping.")
        #     continue

        # 1. Gather Context
        context = get_file_context(shard['targets'])
        if not context:
            log_mission(f"⚠️ No files found for {shard['name']}. Skipping.")
            continue

        out_file.parent.mkdir(exist_ok=True)
        full_prompt = f"{shard['prompt']}\n\n### SOURCE CODE CONTEXT:\n{context}"
        
        prompt_file = ROOT_DIR / f"temp_prompt_{shard['name']}.txt"
        with open(prompt_file, 'w') as f:
            f.write(full_prompt)

        # Run with --prompt-file
        run_task(f"Extract {shard['name']}", 
                 f"{VENV_PYTHON} {SCRIPTS_DIR}/reversa_runner.py {shard['skill']} "
                 f"--prompt-file {prompt_file} --output {out_file}")
        
        os.remove(prompt_file)

        # 2. Association (Low-level mapping)
        run_task(f"Associate {shard['name']}", 
                 f"{VENV_PYTHON} {SCRIPTS_DIR}/association_agent.py --shard {shard['name']}")

    # Phase 4: Final Refresh
    log_mission("Finalizing Governance Stack Refresh...")
    run_task("Intent Index Refresh", f"{VENV_PYTHON} {SCRIPTS_DIR}/intent_index_builder.py --project-root {ROOT_DIR}")
    run_task("MDG Build", f"{VENV_PYTHON} {SCRIPTS_DIR}/mdg_builder.py --project-root {ROOT_DIR}")
    run_task("Drift Report Update", f"{VENV_PYTHON} {SCRIPTS_DIR}/drift_detector.py --project-root {ROOT_DIR}")

    log_mission("MISSION COMPLETE. All shards processed.")

if __name__ == "__main__":
    main()
