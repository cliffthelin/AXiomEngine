#!/usr/bin/env python3
"""
AXiomEngine GPU Provider Registry v0.1
======================================
Role: Read-only inventory layer for GPU hardware and local model services.
"""

import json
import subprocess
import os
import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

def run_cmd(cmd: List[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.stdout.strip()
    except Exception:
        return ""

class GPUProviderRegistry:
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.report = {
            "version": "0.1.0",
            "collected_at": self.timestamp,
            "hardware": {
                "gpus": [],
                "active_profile": None
            },
            "providers": {
                "ollama": {"active": False, "models": [], "running": []},
                "llama_server": {"active": False, "instances": []}
            }
        }

    def detect_gpus(self):
        """Parse nvidia-smi CSV output for NVIDIA hardware."""
        query = (
            "index,name,uuid,memory.total,memory.used,memory.free,"
            "utilization.gpu,utilization.memory,power.draw,power.limit,"
            "temperature.gpu,persistence_mode,display_active"
        )
        output = run_cmd(["nvidia-smi", f"--query-gpu={query}", "--format=csv,noheader,nounits"])
        
        if not output:
            return

        for line in output.splitlines():
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 13:
                continue
            
            gpu = {
                "index": int(parts[0]),
                "name": parts[1],
                "uuid": parts[2],
                "memory": {
                    "total_mib": int(parts[3]),
                    "used_mib": int(parts[4]),
                    "free_mib": int(parts[5])
                },
                "utilization": {
                    "gpu_pct": int(parts[6]),
                    "memory_pct": int(parts[7])
                },
                "power": {
                    "draw_w": float(parts[8]),
                    "limit_w": float(parts[9])
                },
                "temperature_c": int(parts[10]),
                "persistence_mode": parts[11],
                "display_active": parts[12]
            }
            self.report["hardware"]["gpus"].append(gpu)

    def detect_hardware_profile(self):
        """Detect the active GPU Switcher profile."""
        # Try a few common locations for the switcher
        switcher_paths = [
            Path("/mnt/UBUNTU_8TB/Projects/GPU_Switcher/gpu-orchestrator"),
            Path(__file__).parent.parent.parent / "GPU_Switcher" / "gpu-orchestrator"
        ]
        
        for path in switcher_paths:
            manifest_path = path / "active" / "manifest.env"
            if manifest_path.exists():
                content = manifest_path.read_text()
                match = re.search(r'PROFILE_NAME="([^"]+)"', content)
                if match:
                    self.report["hardware"]["active_profile"] = match.group(1)
                    return

    def detect_ollama(self):
        """Detect Ollama status and models."""
        # Check if ollama is installed
        if not run_cmd(["which", "ollama"]):
            return

        self.report["providers"]["ollama"]["active"] = True
        
        # 1. List installed models
        list_output = run_cmd(["ollama", "list"])
        if list_output:
            lines = list_output.splitlines()
            if len(lines) > 1: # Skip header
                for line in lines[1:]:
                    parts = re.split(r'\s{2,}', line) # Split by multiple spaces
                    if len(parts) >= 3:
                        self.report["providers"]["ollama"]["models"].append({
                            "name": parts[0],
                            "id": parts[1],
                            "size": parts[2]
                        })

        # 2. List running models
        ps_output = run_cmd(["ollama", "ps"])
        if ps_output:
            lines = ps_output.splitlines()
            if len(lines) > 1: # Skip header
                for line in lines[1:]:
                    parts = re.split(r'\s{2,}', line)
                    if len(parts) >= 6:
                        self.report["providers"]["ollama"]["running"].append({
                            "name": parts[0],
                            "id": parts[1],
                            "size": parts[2],
                            "processor": parts[3],
                            "context": parts[4],
                            "until": parts[5]
                        })

    def detect_llama_server(self):
        """Detect llama-server processes via ps."""
        ps_output = run_cmd(["ps", "aux"])
        if not ps_output:
            return

        # Pattern for llama-server
        for line in ps_output.splitlines():
            if "llama-server" in line and "grep" not in line:
                self.report["providers"]["llama_server"]["active"] = True
                
                # Extract PID and command line
                parts = line.split()
                pid = parts[1]
                cmdline = " ".join(parts[10:])
                
                instance = {
                    "pid": pid,
                    "cmdline": cmdline,
                    "port": "8080", # Default
                    "host": "127.0.0.1", # Default
                    "model_path": None,
                    "alias": None
                }
                
                # Parse cmdline for arguments
                port_match = re.search(r'--port\s+(\d+)', cmdline)
                if port_match: instance["port"] = port_match.group(1)
                
                host_match = re.search(r'--host\s+([^\s]+)', cmdline)
                if host_match: instance["host"] = host_match.group(1)
                
                model_match = re.search(r'--model\s+([^\s]+)', cmdline)
                if model_match: instance["model_path"] = model_match.group(1)
                
                alias_match = re.search(r'--alias\s+([^\s]+)', cmdline)
                if alias_match: instance["alias"] = alias_match.group(1)
                
                self.report["providers"]["llama_server"]["instances"].append(instance)

    def run_discovery(self):
        self.detect_gpus()
        self.detect_hardware_profile()
        self.detect_ollama()
        self.detect_llama_server()
        return self.report

def main():
    parser = argparse.ArgumentParser(description="AXiomEngine GPU Provider Registry")
    parser.add_argument("--write-report", help="Path to save the JSON report")
    parser.add_argument("--json", action="store_true", help="Print only JSON to stdout")
    args = parser.parse_args()

    registry = GPUProviderRegistry()
    report = registry.run_discovery()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        # User-friendly summary
        print(f"🚀 AXiomEngine GPU Provider Registry v0.1")
        print(f"📅 Collected at: {report['collected_at']}")
        print("-" * 40)
        
        gpus = report["hardware"]["gpus"]
        profile = report["hardware"]["active_profile"]
        print(f"📡 Hardware: {len(gpus)} GPU(s) detected [Profile: {profile or 'Standard'}]")
        for g in gpus:
            print(f"  [{g['index']}] {g['name']} ({g['memory']['total_mib']} MiB)")
            print(f"      Util: {g['utilization']['gpu_pct']}% GPU, {g['utilization']['memory_pct']}% VRAM")
            print(f"      Power: {g['power']['draw_w']}W / {g['power']['limit_w']}W")
        
        print("-" * 40)
        ollama = report["providers"]["ollama"]
        print(f"🦙 Provider: Ollama ({'ACTIVE' if ollama['active'] else 'DOWN'})")
        if ollama["active"]:
            print(f"  Installed: {len(ollama['models'])} models")
            print(f"  Running:   {len(ollama['running'])} model(s)")
            for m in ollama["running"]:
                print(f"      • {m['name']} ({m['size']}) - {m['processor']}, ctx={m['context']}")

        print("-" * 40)
        llama = report["providers"]["llama_server"]
        print(f"🦙 Provider: llama-server ({'ACTIVE' if llama['active'] else 'DOWN'})")
        for inst in llama["instances"]:
            print(f"  PID {inst['pid']} on {inst['host']}:{inst['port']}")
            print(f"      Model: {inst['alias'] or inst['model_path']}")

    if args.write_report:
        report_path = Path(args.write_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2)
        if not args.json:
            print(f"\n✅ Report saved to: {args.write_report}")

if __name__ == "__main__":
    main()
