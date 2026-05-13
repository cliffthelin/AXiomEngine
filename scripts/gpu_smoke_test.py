#!/usr/bin/env python3
import subprocess
import json
import os
from datetime import datetime

REPORT_PATH = "docs/audit/gpu_smoke_report.json"

def run_command(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def get_gpu_data():
    query = "index,name,memory.total,memory.used,utilization.gpu,temperature.gpu"
    raw = run_command(["nvidia-smi", f"--query-gpu={query}", "--format=csv,noheader,nounits"])
    
    if not raw:
        return None, None, []

    gpus = []
    lines = raw.split("\n")
    for line in lines:
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split(",")]
        gpus.append({
            "index": int(parts[0]),
            "name": parts[1],
            "memory_total_mb": int(parts[2]),
            "memory_used_mb": int(parts[3]),
            "utilization_gpu_percent": int(parts[4]),
            "temperature_c": int(parts[5])
        })
    
    raw_versions = run_command(["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"])
    driver_version = raw_versions.split("\n")[0] if raw_versions else "UNKNOWN"
    
    # Simple extraction of CUDA version from standard nvidia-smi output
    raw_smi = run_command(["nvidia-smi"])
    cuda_version = "UNKNOWN"
    if raw_smi:
        for line in raw_smi.split("\n"):
            if "CUDA Version:" in line:
                cuda_version = line.split("CUDA Version:")[1].split("|")[0].strip()
                break

    return driver_version, cuda_version, gpus

def get_active_processes():
    query = "gpu_index,pid,process_name,used_memory"
    raw = run_command(["nvidia-smi", f"--query-compute-apps={query}", "--format=csv,noheader,nounits"])
    
    processes = []
    if raw:
        lines = raw.split("\n")
        for line in lines:
            if not line.strip():
                continue
            parts = [p.strip() for p in line.split(",")]
            processes.append({
                "gpu_index": int(parts[0]),
                "pid": int(parts[1]),
                "process_name": parts[2],
                "used_memory_mb": int(parts[3])
            })
    return processes

def get_ollama_status():
    ollama_list = run_command(["ollama", "list"])
    if ollama_list is None:
        return {"detected": False, "models": [], "status": "OLLAMA_NOT_AVAILABLE"}
    
    models = []
    lines = ollama_list.split("\n")
    # Skip header
    for line in lines[1:]:
        if line.strip():
            models.append(line.split()[0])
            
    return {
        "detected": True,
        "models": models,
        "status": "READY" if models else "NO_MODELS_FOUND"
    }

def run_inference_probe(model_name="qwen3.6:27b"):
    print(f"📡 Running inference probe with {model_name}...")
    start_time = datetime.utcnow()
    # A simple, very short prompt to test responsiveness
    probe_cmd = ["ollama", "run", model_name, "echo 'ready'"]
    output = run_command(probe_cmd)
    end_time = datetime.utcnow()
    
    duration = (end_time - start_time).total_seconds()
    
    if output and "ready" in output.lower():
        return {
            "status": "SUCCESS",
            "model": model_name,
            "duration_seconds": duration,
            "response": output.strip()
        }
    else:
        return {
            "status": "FAILED",
            "model": model_name,
            "error": "Model failed to respond correctly or is not installed."
        }

def main():
    print("🚀 AXiomEngine GPU Smoke Test...")
    
    driver, cuda, gpus = get_gpu_data()
    processes = get_active_processes()
    ollama = get_ollama_status()
    
    probe_result = {"status": "SKIPPED", "reason": "No NVIDIA GPUs or Ollama unavailable"}
    if gpus and ollama["detected"]:
        # Check if qwen3.6:27b is in models
        target_model = "qwen3.6:27b"
        if target_model in ollama["models"]:
            probe_result = run_inference_probe(target_model)
        else:
            probe_result = {"status": "FAILED", "reason": f"Required model {target_model} not found in Ollama."}
    
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "detected_gpu_count": len(gpus),
        "driver_version": driver,
        "cuda_version": cuda,
        "gpus": gpus,
        "active_processes": processes,
        "ollama": ollama,
        "inference_probe": probe_result,
        "report_status": "STABLE" if gpus and probe_result.get("status") == "SUCCESS" else "WARNING"
    }
    
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"✅ Report generated: {REPORT_PATH}")
    if not gpus:
        print("⚠️  Warning: No NVIDIA GPUs detected via nvidia-smi.")
    else:
        print(f"✨ Found {len(gpus)} GPU(s). Driver: {driver}, CUDA: {cuda}")
        print(f"📊 Probe Status: {probe_result.get('status')}")

if __name__ == "__main__":
    main()
