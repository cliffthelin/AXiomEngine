#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

class AgentSandbox:
    """
    AXIOMENGINE SANDBOX (Phase 4)
    Implements resource capping via CGroups v2.
    """
    def __init__(self, agent_name: str, mode: str = "cgroup"):
        self.agent_name = agent_name
        self.mode = mode
        self.cgroup_path = f"/sys/fs/cgroup/axiomengine_{agent_name}"
        self.project_root = Path(__file__).parent.parent.absolute()

    def setup(self, mem_limit="512M", cpu_limit="50000 100000"): # 0.5 CPU
        """Creates the cgroup. Requires sudo or appropriate permissions."""
        try:
            os.makedirs(self.cgroup_path, exist_ok=True)
            
            # Set memory limit
            with open(f"{self.cgroup_path}/memory.max", "w") as f:
                f.write(mem_limit)
                
            # Set CPU limit (quota period)
            with open(f"{self.cgroup_path}/cpu.max", "w") as f:
                f.write(cpu_limit)
                
            print(f"Sandbox: Configured limits for {self.agent_name} ({mem_limit} RAM, {cpu_limit} CPU)")
        except PermissionError:
            print(f"Sandbox Error: Permission denied creating cgroup at {self.cgroup_path}. Run with sudo or set permissions.")

    def run_command(self, cmd_list: list):
        """Runs a command inside the chosen sandbox mode."""
        if self.mode == "microvm":
            self.run_microvm(cmd_list)
        else:
            self.run_cgroup(cmd_list)

    def run_cgroup(self, cmd_list: list):
        """Standard CGroup v2 isolation."""
        try:
            # Add current process to cgroup
            with open(f"{self.cgroup_path}/cgroup.procs", "w") as f:
                f.write(str(os.getpid()))
        except Exception as e:
            print(f"Sandbox (CGroup) Warning: Could not join cgroup: {e}")
            
        print(f"Sandbox: Executing command in {self.agent_name} CGroup...")
        subprocess.run(cmd_list)

    def run_microvm(self, cmd_list: list):
        """High-security MicroVM isolation."""
        print(f"Sandbox: Launching MicroVM for {self.agent_name}...")
        cmd_str = " ".join(cmd_list)
        
        # We override the -append to run the command and then halt
        launcher = self.project_root / "scripts" / "qemu_launcher.sh"
        
        # Read the launcher to get base params but we'll execute directly for control
        kernel = self.project_root / "vmlinux"
        rootfs = self.project_root / "rootfs.ext4"
        
        qemu_cmd = [
            "qemu-system-x86_64",
            "-M", "microvm,x-option-roms=off,pit=off,pic=off,rtc=off",
            "-enable-kvm", "-cpu", "host", "-m", "512m", "-smp", "2",
            "-kernel", str(kernel),
            "-append", f"console=ttyS0 root=/dev/vda rw init=/bin/sh -- -c '{cmd_str}'",
            "-drive", f"file={rootfs},format=raw,if=none,id=hd0,snapshot=on",
            "-device", "virtio-blk-device,drive=hd0",
            "-display", "none", "-serial", "stdio",
            "-no-reboot"
        ]
        
        subprocess.run(qemu_cmd)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("cmd", nargs="+")
    parser.add_argument("--mode", default="cgroup", choices=["cgroup", "microvm"])
    args = parser.parse_args()
    
    sb = AgentSandbox(args.name, mode=args.mode)
    if args.mode == "cgroup":
        sb.setup()
    sb.run_command(args.cmd)
