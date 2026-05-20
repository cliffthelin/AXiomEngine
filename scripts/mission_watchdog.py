#!/usr/bin/env python3
import os
import subprocess
import time
import json
import psutil
from pathlib import Path

# --- CONFIGURATION ---
ROOT_DIR = Path(__file__).resolve().parents[1]
MISSION_SCRIPT = str(ROOT_DIR / "scripts" / "DataCatalogFactory.py")
MISSION_LOG = str(ROOT_DIR / "MISSION_ROI_TELEMETRY.log")
STATS_FILE = str(ROOT_DIR / "MISSION_STATS.json")
CHECK_INTERVAL = 60  # Check every minute
STALL_TIMEOUT = 900  # 15 minutes
RAM_BUFFER = 8 * 1024 * 1024 * 1024  # 8 GB
VRAM_BUFFER = 500 * 1024 * 1024      # 500 MB (for RTX 3070)

def get_3070_vram_free():
    try:
        cmd = "nvidia-smi --query-gpu=index,memory.free --format=csv,noheader,nounits -i 0"
        output = subprocess.check_output(cmd, shell=True).decode()
        for line in output.strip().split('\n'):
            idx, free = line.split(',')
            if idx.strip() == '0':
                return int(free.strip()) * 1024 * 1024
    except:
        pass
    return 0

def get_system_ram_free():
    return psutil.virtual_memory().available

def kill_stalled_processes():
    print("🚨 STALL DETECTED: Killing mission and Ollama processes...")
    # Kill DataCatalogFactory
    subprocess.run("pkill -f DataCatalogFactory.py", shell=True)
    # Kill any defunct or stalled ollama processes
    subprocess.run("pkill -f ollama", shell=True)
    time.sleep(5)

def restart_services():
    print("♻️ RESTARTING SERVICES...")
    # Try to restart the snap service if it exists
    subprocess.run("snap restart ollama", shell=True)
    # Start our own managed nodes if needed (to be implemented)
    time.sleep(10)

def resume_mission():
    print("🚀 RESUMING MISSION...")
    cmd = f"nohup python3 {MISSION_SCRIPT} >> /tmp/mission_output.log 2>&1 &"
    subprocess.Popen(cmd, shell=True)

def monitor_loop():
    last_progress_time = time.time()
    last_completed_count = 0
    
    if os.path.exists(STATS_FILE):
        try:
            stats = json.loads(Path(STATS_FILE).read_text())
            last_completed_count = stats.get("rules_completed", 0)
        except:
            pass

    while True:
        # 1. Check Resources
        ram_free = get_system_ram_free()
        vram_free = get_3070_vram_free()
        
        print(f"[{time.strftime('%H:%M:%S')}] RAM Free: {ram_free/1e9:.2f}GB | VRAM Free: {vram_free/1e6:.2f}MB")
        
        if ram_free < RAM_BUFFER:
            print("⚠️ RAM BUFFER CRITICAL!")
            # Throttling logic would go here
        
        if vram_free < VRAM_BUFFER:
            print("⚠️ VRAM BUFFER CRITICAL!")

        # 2. Check Progress
        current_completed_count = 0
        if os.path.exists(STATS_FILE):
            try:
                stats = json.loads(Path(STATS_FILE).read_text())
                current_completed_count = stats.get("rules_completed", 0)
            except:
                pass
        
        if current_completed_count > last_completed_count:
            print(f"✅ Progress detected: {current_completed_count} rules completed.")
            last_completed_count = current_completed_count
            last_progress_time = time.time()
        else:
            elapsed_stall = time.time() - last_progress_time
            if elapsed_stall > STALL_TIMEOUT:
                print(f"🛑 STALL DETECTED ({elapsed_stall/60:.1f} mins since last progress)")
                kill_stalled_processes()
                restart_services()
                resume_mission()
                last_progress_time = time.time()
            elif elapsed_stall > 300:
                print(f"⏳ Warning: No progress for {elapsed_stall/60:.1f} mins.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("🛡️ MISSION WATCHDOG STARTED")
    monitor_loop()
