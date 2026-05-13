#!/usr/bin/env python3
import os
import subprocess
import time
import httpx
import socket
import sys
from pathlib import Path

# Configuration
AXIOMENGINE_ROOT = Path(__file__).parent.parent.absolute()
ROUTER_URL = "http://localhost:9001"
N8N_URL = "http://localhost:5678"
KERNEL_URL = "https://github.com/firecracker-microvm/firecracker/raw/main/resources/tests/vmlinux"
ROOTFS_URL = "https://github.com/firecracker-microvm/firecracker/raw/main/resources/tests/ubuntu-22.04.ext4"

def is_port_open(port, host="127.0.0.1"):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def run_cmd(cmd, cwd=None, shell=False):
    print(f"🚀 Running: {cmd}")
    try:
        res = subprocess.run(cmd, cwd=cwd, shell=shell, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ Error: {res.stderr}")
        return res
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def check_services():
    print("\n── 🏥 System Health Check ──────────────────────")
    
    # 1. Valkey
    if not is_port_open(6379):
        print("⚠️  Valkey is DOWN. Attempting to start...")
        # Try systemctl first (will likely fail in this environment)
        run_cmd(["sudo", "systemctl", "start", "valkey-server"])
        time.sleep(1)
        
        if not is_port_open(6379):
            print("🔄 System Valkey failed. Trying local Valkey instance...")
            run_cmd(["valkey-server", str(AXIOMENGINE_ROOT / "valkey_local.conf")])
            time.sleep(2)
            
        if is_port_open(6379):
            print("✅ Valkey is now UP.")
        else:
            print("❌ Failed to start Valkey. Please run: sudo systemctl start valkey-server")
    else:
        print("✅ Valkey is UP.")

    # 2. Router
    if not is_port_open(9001):
        print("⚠️  Router is DOWN. Attempting to start...")
        # Start in background using nohup or similar if needed, 
        # but for this harness we might just trigger the script.
        # Note: 01_start_router.sh uses exec, so we might need to spawn it.
        subprocess.Popen(["bash", str(AXIOMENGINE_ROOT / "scripts" / "01_start_router.sh")], 
                         cwd=AXIOMENGINE_ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        if is_port_open(9001):
            print("✅ Router is now UP.")
        else:
            print("❌ Failed to start Router.")
    else:
        print("✅ Router is UP.")

def fix_n8n_permissions():
    print("\n── 🔌 Phase 2: n8n Workflow Automation ─────────")
    print("Checking Docker snap interfaces...")
    
    docker_dir = AXIOMENGINE_ROOT / "docker"
    if not is_port_open(5678):
        print("Attempting to start n8n...")
        res = run_cmd(["docker", "compose", "up", "-d"], cwd=docker_dir)
        if res and "permission denied" in res.stderr.lower():
            print("❌ Permission Denied by Docker Snap.")
            print("👉 ACTION REQUIRED: Please run the following commands in your terminal:")
            print("   sudo snap connect docker:removable-media")
            print("   cd " + str(docker_dir) + " && docker compose up -d")
        else:
            time.sleep(5)
            if is_port_open(5678):
                print("✅ n8n is now UP at http://localhost:5678")
            else:
                print("❌ n8n failed to start.")
    else:
        print("✅ n8n is UP.")

def setup_microvm():
    print("\n── 🛡️ Phase 4: MicroVM Sandboxing ──────────────")
    kernel_path = AXIOMENGINE_ROOT / "vmlinux"
    rootfs_path = AXIOMENGINE_ROOT / "rootfs.ext4"

    if not kernel_path.exists():
        print(f"Downloading kernel from {KERNEL_URL}...")
        run_cmd(["curl", "-L", KERNEL_URL, "-o", str(kernel_path)])
    
    if not rootfs_path.exists():
        print(f"Downloading rootfs from {ROOTFS_URL}...")
        run_cmd(["curl", "-L", ROOTFS_URL, "-o", str(rootfs_path)])
    
    if kernel_path.exists() and rootfs_path.exists():
        print("✅ MicroVM assets ready.")
        print("Testing MicroVM launcher...")
        # We might not want to run it fully in a non-interactive harness if it blocks
        # but let's see if we can at least verify the command exists.
        if run_cmd(["which", "qemu-system-x86_64"]).returncode == 0:
            print("✅ QEMU is installed.")
        else:
            print("❌ QEMU not found. Install with: sudo apt install qemu-system-x86")

def main():
    print("============================================")
    print(" AXiomEngine Master Harness — Phase Completion")
    print("============================================")
    
    check_services()
    fix_n8n_permissions()
    setup_microvm()
    
    print("\n============================================")
    print(" ✅ Harness Run Complete!")
    print(" Next: Run 'python scripts/full_system_test.py'")
    print("============================================")

if __name__ == "__main__":
    main()
