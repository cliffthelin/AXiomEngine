#!/usr/bin/env python3
"""
Governance Inference Worker v1.0
===============================
Role: Governed execution of LLM-based governance missions.
Enforces hardware checks before starting heavy inference on P40.
"""

import json
import subprocess
import os
import sys
import uuid
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

# Add scripts dir to path for imports
sys.path.append(str(Path(__file__).parent))

from gpu_provider_registry import GPUProviderRegistry

class GovernanceInferenceWorker:
    def __init__(self, model="qwen3.6:27b"):
        self.model = model
        self.registry = GPUProviderRegistry()
        self.run_id = str(uuid.uuid4())[:8]

    def log(self, msg):
        print(f"[{datetime.now().isoformat()}] 🧠 [WORKER] {msg}")

    def pre_flight_check(self) -> bool:
        """Check if hardware is ready for 27B inference."""
        self.log("Performing GPU pre-flight check...")
        report = self.registry.run_discovery()
        
        # 1. Find P40
        p40 = next((g for g in report["hardware"]["gpus"] if "P40" in g["name"]), None)
        if not p40:
            self.log("❌ CRITICAL: Tesla P40 not detected. Mission aborted.")
            return False
        
        if p40["utilization"]["gpu_pct"] > 80:
            self.log(f"⚠️ P40 is heavily utilized ({p40['utilization']['gpu_pct']}%). Waiting or aborting.")
            return False
        
        # 2. Check Ollama
        ollama = report["providers"]["ollama"]
        if not ollama["active"]:
            self.log("❌ CRITICAL: Ollama provider is DOWN.")
            return False
            
        self.log(f"✅ Hardware Ready: P40 ({p40['memory']['free_mib']} MiB free), Ollama ACTIVE.")
        return True

    def run_mission(self, skill_name: str, scope_path: str, goal: str):
        if not self.pre_flight_check():
            return {"status": "BLOCKED", "reason": "Hardware/Provider not ready"}

        scope = Path(scope_path)
        if not scope.exists():
            self.log(f"❌ Scope path not found: {scope_path}")
            return {"status": "FAILED", "reason": "Scope not found"}

        self.log(f"Starting Mission: {goal}")
        self.log(f"Applying Skill: {skill_name} to {scope.name}")

        # 1. Prepare Context
        source_code = scope.read_text()
        source_hash = hashlib.sha256(source_code.encode()).hexdigest()

        # 2. Load Skill
        skill_path = Path(__file__).parent.parent / "skills" / "reversa" / skill_name / "SKILL.md"
        if not skill_path.exists():
            self.log(f"❌ Skill not found: {skill_name}")
            return {"status": "FAILED", "reason": "Skill not found"}
        skill_content = skill_path.read_text()

        # 3. Execute Inference (via Ollama)
        prompt = f"GOAL: {goal}\n\n### SOURCE CODE CONTEXT ({scope.name}):\n{source_code}"
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": skill_content},
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "options": {
                "num_ctx": 32768
            }
        }

        self.log(f"Executing Deep Reasoning via {self.model} (Timeout: 600s)...")
        start_time = datetime.now()
        
        try:
            # We use curl or httpx if available. Since I saw httpx in the venv, I'll try to import it.
            import httpx
            with httpx.Client(timeout=600.0) as client:
                response = client.post("http://127.0.0.1:11434/v1/chat/completions", json=payload)
                response.raise_for_status()
                data = response.json()
                content = data['choices'][0]['message']['content']
        except Exception as e:
            self.log(f"❌ Inference failed: {e}")
            return {"status": "FAILED", "reason": str(e)}

        duration = (datetime.now() - start_time).total_seconds()
        self.log(f"✅ Inference Complete ({duration:.1f}s)")

        # 4. Generate Evidence Pack
        evidence = {
            "mission_id": self.run_id,
            "timestamp_start": start_time.isoformat(),
            "timestamp_end": datetime.now().isoformat(),
            "status": "SUCCESS",
            "scope": str(scope),
            "source_hash": source_hash,
            "skill": skill_name,
            "model": self.model,
            "gpu_metrics": {
                "hardware": "Tesla P40",
                "duration_seconds": duration
            },
            "llm_rationale": content
        }

        # Save artifacts
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        audit_dir = Path("docs/audit")
        audit_dir.mkdir(parents=True, exist_ok=True)
        
        evidence_path = audit_dir / f"mission_evidence_{ts}.json"
        with open(evidence_path, "w") as f:
            json.dump(evidence, f, indent=2)

        report_path = audit_dir / f"mission_report_{ts}.md"
        with open(report_path, "w") as f:
            f.write(f"# Governance Audit Report: {self.run_id}\n\n")
            f.write(f"- **Goal**: {goal}\n")
            f.write(f"- **Scope**: `{scope_path}`\n")
            f.write(f"- **Skill**: `{skill_name}`\n")
            f.write(f"- **Model**: `{self.model}` on P40\n\n")
            f.write("## LLM Rationale\n\n")
            f.write(content)

        self.log(f"📁 Evidence saved to: {evidence_path}")
        return evidence

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AXiomEngine Governance Inference Worker")
    parser.add_argument("--skill", required=True, help="Reversa skill name")
    parser.add_argument("--scope", required=True, help="File path to audit")
    parser.add_argument("--goal", default="Perform high-rationale governance extraction.", help="Mission goal")
    parser.add_argument("--model", default="qwen3.6:27b", help="Model name")
    args = parser.parse_args()

    worker = GovernanceInferenceWorker(model=args.model)
    worker.run_mission(args.skill, args.scope, args.goal)
