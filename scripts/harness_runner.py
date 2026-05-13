#!/usr/bin/env python3
"""
AXiomEngine Harness Runner (Track B) — STABLE EVIDENCE UPGRADE
========================================================
Role: Produces stable, hash-verified, audit-defensible evidence packs.
"""
import argparse
import json
import os
import re
import hashlib
import uuid
from pathlib import Path
from datetime import datetime

RUNNER_VERSION = "1.1.0"

class HarnessRunner:
    def __init__(self, config_path, json_mode=False):
        self.config_path = Path(config_path)
        self.start_time = datetime.now()
        self.run_id = str(uuid.uuid4())[:8]
        self.json_mode = json_mode
        self.error_data = None
        self.failure_stage = "init"
        
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {config_path}")
        
        self.config_raw = self.config_path.read_text()
        self.config = json.loads(self.config_raw)
        self.config_hash = hashlib.sha256(self.config_raw.encode()).hexdigest()
        
        self.timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        self.sim_dir = Path(f"./temp_sim_{self.timestamp}_{self.run_id}")
        self.log_file = self.sim_dir / "harness.log"
        self.findings_file = self.sim_dir / "findings.json"
        self.evidence_file = self.sim_dir / "evidence.json"
        
        self.findings = []
        self.evidence = []
        self.status = "PENDING"
        self.target_hashes = {}

        # Ensure directory exists before logging
        self.sim_dir.mkdir(exist_ok=True, parents=True)

    def log(self, msg, force_print=False):
        timestamp = datetime.now().isoformat()
        entry = f"[{timestamp}] {msg}\n"
        with open(self.log_file, "a") as f:
            f.write(entry)
        if not self.json_mode or force_print:
            print(f"  {msg}")

    def validate_config(self):
        self.log("Validating mission config...")
        required = ["goal", "type", "scope", "flags"]
        for field in required:
            if field not in self.config:
                self.status = "BLOCKED"
                raise ValueError(f"Missing required field: {field}")
        
        # Hard Type Guard
        if self.config["type"] != "worker":
            self.status = "BLOCKED"
            self.log(f"⚠️ Harness type '{self.config['type']}' is recognized but NOT_IMPLEMENTED in this runner.")
            raise NotImplementedError(f"Runner only supports 'worker' missions currently.")
        
        self.log(f"Config Validated. Run ID: {self.run_id}")

    def resolve_scope(self):
        # Use config-rooted pathing if available, otherwise fallback to CWD
        project_root_path = self.config.get("project_root", os.getcwd())
        project_root = Path(project_root_path).resolve()
        
        scope_path = Path(self.config["scope"])
        
        # If scope is relative, resolve it against project_root
        if not scope_path.is_absolute():
            full_path = (project_root / scope_path).resolve()
        else:
            full_path = scope_path.resolve()
            
        self.log(f"Resolving Scope: {full_path} (Project Root: {project_root})")
        
        if not full_path.exists():
            self.status = "FAILED"
            raise FileNotFoundError(f"Scope target does not exist: {full_path}")
            
        # Path Jail: Ensure target is within the project_root
        if project_root not in full_path.parents and full_path != project_root:
            self.status = "BLOCKED"
            raise PermissionError(f"Access denied: Target '{full_path}' is outside project root '{project_root}'.")
            
        # Hash the target file for the manifest
        content = full_path.read_text()
        self.target_hashes[str(scope_path)] = hashlib.sha256(content.encode()).hexdigest()
        
        self.log(f"Scope Verified: {full_path}")
        return full_path

    def execute_worker_mission(self, target_path):
        self.log(f"Executing Worker Mission: {self.config['goal']}")
        
        if "Audit" in self.config["goal"]:
            self.run_security_audit(target_path)
        else:
            self.log("No specific logic for this mission goal. Marking SUCCESS_NO_FINDINGS.")
            self.status = "SUCCESS_NO_FINDINGS"

    def run_security_audit(self, target_path):
        content = target_path.read_text()
        lines = content.splitlines()
        target_hash = self.target_hashes[str(self.config["scope"])]

        patterns = {
            "SHELL_EXEC": r"(subprocess\..*shell=True|os\.system|os\.popen)",
            "UNSAFE_EVAL": r"(eval\(|exec\()",
            "DYNAMIC_CMD": r"(\.format\(|f[\"'].*\{.*\}[\"']).*\.run\(|.*\.Popen\("
        }

        for i, line in enumerate(lines, 1):
            for p_name, p_regex in patterns.items():
                if re.search(p_regex, line):
                    finding_id = f"FND-{uuid.uuid4().hex[:6]}"
                    evidence_id = f"EVD-{uuid.uuid4().hex[:6]}"
                    
                    # Create Finding
                    self.findings.append({
                        "finding_id": finding_id,
                        "type": p_name,
                        "severity": "HIGH" if p_name != "DYNAMIC_CMD" else "MEDIUM",
                        "candidate_only": True, # Enforced: Security Audit findings are always candidates
                        "file": str(self.config["scope"]),
                        "line_start": i,
                        "line_end": i,
                        "snippet": line.strip(),
                        "rationale": f"Detected {p_name} pattern during automated security audit.",
                        "evidence_refs": [evidence_id],
                        "confidence": 0.9,
                        "review_status": "proposed"
                    })
                    
                    # Create Evidence
                    self.evidence.append({
                        "evidence_id": evidence_id,
                        "source_file": str(self.config["scope"]),
                        "source_hash": target_hash,
                        "line_start": i,
                        "line_end": i,
                        "excerpt": line.strip(),
                        "extraction_method": "regex_pattern_match",
                        "collected_at": datetime.now().isoformat()
                    })

        self.status = "SUCCESS_WITH_FINDINGS" if self.findings else "SUCCESS_NO_FINDINGS"
        self.log(f"Audit complete. Findings: {len(self.findings)}")

    def finalize(self):
        end_time = datetime.now()
        
        # Write Artifacts
        with open(self.findings_file, "w") as f:
            json.dump({"findings": self.findings}, f, indent=2)
        with open(self.evidence_file, "w") as f:
            json.dump({"evidence": self.evidence}, f, indent=2)
            
        manifest = {
            "mission_id": self.config.get("mission_id", "MSN-UNKNOWN"),
            "run_id": self.run_id,
            "timestamp_start": self.start_time.isoformat(),
            "timestamp_end": end_time.isoformat(),
            "status": self.status,
            "config_hash": self.config_hash,
            "target_hashes": self.target_hashes,
            "findings_count": len(self.findings),
            "evidence_count": len(self.evidence),
            "runner_version": RUNNER_VERSION
        }
        manifest_path = self.sim_dir / "manifest.json"
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
            
        # Report
        report = f"# Mission Validation Report: {self.config['goal']}\n\n"
        report += f"| Metric | Value |\n|---|---|\n"
        report += f"| Status | {self.status} |\n| Run ID | {self.run_id} |\n"
        report += f"| Findings | {len(self.findings)} |\n\n"
        report += "## Findings Table\n"
        if self.findings:
            report += "| ID | Type | Line | Snippet |\n|---|---|---|---|\n"
            for f in self.findings:
                report += f"| {f['finding_id']} | {f['type']} | {f['line_start']} | `{f['snippet']}` |\n"
        else:
            report += "*No findings identified.*\n"
            
        with open(self.sim_dir / "validation_report.md", "w") as f:
            f.write(report)

        if self.json_mode:
            summary = {
                "status": self.status,
                "run_id": self.run_id,
                "sim_dir": str(self.sim_dir),
                "manifest_path": str(manifest_path),
                "findings_path": str(self.findings_file),
                "evidence_path": str(self.evidence_file),
                "findings_count": len(self.findings),
                "error": self.error_data
            }
            print(json.dumps(summary))
        else:
            self.log(f"📁 Results in: {self.sim_dir}")
            
        return self.status

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to harness.json")
    parser.add_argument("--json-output", action="store_true", help="Emit machine-readable JSON summary")
    args = parser.parse_args()

    runner = HarnessRunner(args.config, json_mode=args.json_output)
    try:
        runner.failure_stage = "validate_config"
        runner.validate_config()
        
        runner.failure_stage = "resolve_scope"
        target = runner.resolve_scope()
        
        runner.failure_stage = "execute_worker"
        runner.execute_worker_mission(target)
    except Exception as e:
        runner.status = "FAILED" if runner.status == "PENDING" else runner.status
        runner.error_data = {
            "type": type(e).__name__,
            "message": str(e),
            "stage": runner.failure_stage
        }
        if not args.json_output:
            runner.log(f"❌ ERROR: [{runner.failure_stage}] {e}")
    finally:
        status = runner.finalize()
        if not args.json_output:
            print(f"✨ [RUNNER] Complete. Status: {status}")

if __name__ == "__main__":
    main()
