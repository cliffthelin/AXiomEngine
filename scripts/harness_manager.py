#!/usr/bin/env python3
"""
AXiomEngine Harness Manager (Phase 5C) — GLOBAL REVIEW PACK STABILIZATION
===================================================================
Role: Produces enriched, indexed, and review-grade global governance artifacts.
"""
import argparse
import json
import subprocess
import sys
import hashlib
import uuid
from pathlib import Path
from datetime import datetime

MANAGER_VERSION = "1.2.1"

class HarnessManager:
    def __init__(self, pack_path):
        self.pack_path = Path(pack_path)
        self.start_time = datetime.now()
        self.manager_run_id = f"MGR-{uuid.uuid4().hex[:6]}"
        
        if not self.pack_path.exists():
            raise FileNotFoundError(f"Mission Pack not found: {pack_path}")
        
        self.pack_raw = self.pack_path.read_text()
        self.pack = json.loads(self.pack_raw)
        self.pack_hash = hashlib.sha256(self.pack_raw.encode()).hexdigest()
        
        self.timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        self.mission_dir = Path(f"./mission_pack_{self.timestamp}_{self.manager_run_id}")
        self.log_file = self.mission_dir / "manager.log"
        
        self.worker_summaries = []
        self.global_findings = []
        self.global_evidence = []
        self.global_errors = []
        
        # Indexes for Track A
        self.finding_index = {}
        self.evidence_index = {}
        self.shard_index = {}
        self.error_index = {}
        
        self.status = "PENDING"

    def log(self, msg):
        timestamp = datetime.now().isoformat()
        entry = f"[{timestamp}] [MANAGER] {msg}\n"
        self.mission_dir.mkdir(exist_ok=True, parents=True)
        with open(self.log_file, "a") as f:
            f.write(entry)
        print(f"🛰️ {msg}")

    def validate_pack(self):
        required = ["mission_pack_id", "project_root", "shards"]
        for field in required:
            if field not in self.pack:
                raise ValueError(f"Missing required pack field: {field}")
        self.log(f"Pack Validated: {self.pack['mission_pack_id']}")

    def execute_shard(self, shard):
        shard_name = shard.get("name", "unnamed")
        self.log(f"Dispatching Shard: {shard_name}")
        
        # Inject project_root
        shard["project_root"] = self.pack["project_root"]
        shard["mission_pack_id"] = self.pack["mission_pack_id"]
        
        temp_config = self.mission_dir / f"config_{shard_name}.json"
        with open(temp_config, "w") as f:
            json.dump(shard, f, indent=2)
            
        try:
            cmd = [sys.executable, "scripts/harness_runner.py", str(temp_config), "--json-output"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=False)
            
            # Parse machine-readable output
            try:
                summary = json.loads(result.stdout.strip())
                summary["shard_name"] = shard_name # Enrich summary
                self.worker_summaries.append(summary)
                
                status_icon = "✅" if summary["status"].startswith("SUCCESS") else "⚠️"
                self.log(f"{status_icon} Shard {shard_name} finished. Status: {summary['status']}")
                
                if summary["status"].startswith("SUCCESS"):
                    self.aggregate_worker_data(summary, shard_name)
                else:
                    self.log_shard_error(summary, shard_name)
                    
            except json.JSONDecodeError:
                self.log(f"❌ Malformed worker output for {shard_name}")
                error_summary = {
                    "status": "FAILED", 
                    "shard_name": shard_name, 
                    "error": {
                        "type": "JSONDecodeError", 
                        "message": "Failed to parse runner stdout", 
                        "stage": "dispatcher",
                        "returncode": result.returncode,
                        "stdout_excerpt": result.stdout[:500] if result.stdout else "",
                        "stderr_excerpt": result.stderr[:500] if result.stderr else ""
                    }
                }
                self.worker_summaries.append(error_summary)
                self.log_shard_error(error_summary, shard_name)
                
        except Exception as e:
            self.log(f"❌ Process error for shard {shard_name}: {e}")

    def aggregate_worker_data(self, summary, shard_name):
        self.shard_index[shard_name] = summary
        
        # Aggregate Findings
        if Path(summary["findings_path"]).exists():
            with open(summary["findings_path"]) as f:
                data = json.load(f)
                findings = data.get("findings", [])
                for f_item in findings:
                    # Enrich with Traceability Metadata
                    f_item["mission_pack_id"] = self.pack["mission_pack_id"]
                    f_item["manager_run_id"] = self.manager_run_id
                    f_item["shard_name"] = shard_name
                    f_item["worker_run_id"] = summary["run_id"]
                    f_item["source_manifest_path"] = summary["manifest_path"]
                    
                    self.global_findings.append(f_item)
                    self.finding_index[f_item["finding_id"]] = f_item
        
        # Aggregate Evidence
        if Path(summary["evidence_path"]).exists():
            with open(summary["evidence_path"]) as f:
                data = json.load(f)
                evidence = data.get("evidence", [])
                for e_item in evidence:
                    # Enrich with full Traceability metadata
                    e_item["mission_pack_id"] = self.pack["mission_pack_id"]
                    e_item["manager_run_id"] = self.manager_run_id
                    e_item["shard_name"] = shard_name
                    e_item["worker_run_id"] = summary["run_id"]
                    e_item["source_manifest_path"] = summary.get("manifest_path")
                    
                    self.global_evidence.append(e_item)
                    self.evidence_index[e_item["evidence_id"]] = e_item

    def log_shard_error(self, summary, shard_name):
        error_info = summary.get("error") or {"type": "Unknown", "message": "No error details available"}
        error_entry = {
            "shard_name": shard_name,
            "status": summary["status"],
            "error_type": error_info.get("type"),
            "error_message": error_info.get("message"),
            "failure_stage": error_info.get("stage"),
            "returncode": error_info.get("returncode"),
            "stdout_excerpt": error_info.get("stdout_excerpt"),
            "stderr_excerpt": error_info.get("stderr_excerpt"),
            "worker_run_id": summary.get("run_id"),
            "mission_pack_id": self.pack["mission_pack_id"],
            "manager_run_id": self.manager_run_id
        }
        self.global_errors.append(error_entry)
        self.error_index[shard_name] = error_entry

    def compute_global_status(self):
        statuses = [s["status"] for s in self.worker_summaries]
        if not statuses: return "FAILED"
        
        if any(s == "BLOCKED" for s in statuses): return "BLOCKED"
        
        has_success = any(s.startswith("SUCCESS") for s in statuses)
        has_failure = any(s == "FAILED" for s in statuses)
        if has_success and has_failure: return "PARTIAL"
        
        if all(s == "FAILED" for s in statuses): return "FAILED"
        
        if any(s == "SUCCESS_WITH_FINDINGS" for s in statuses): return "COMPLETED_WITH_FINDINGS"
        if all(s == "SUCCESS_NO_FINDINGS" for s in statuses): return "COMPLETED"
        
        return "UNKNOWN"

    def finalize(self):
        self.status = self.compute_global_status()
        end_time = datetime.now()
        
        # Shard Stats
        successful = [s for s in self.worker_summaries if s["status"].startswith("SUCCESS")]
        failed = [s for s in self.worker_summaries if s["status"] == "FAILED"]
        blocked = [s for s in self.worker_summaries if s["status"] == "BLOCKED"]
        
        # Global Report
        report = {
            "mission_pack_id": self.pack["mission_pack_id"],
            "manager_run_id": self.manager_run_id,
            "pack_hash": self.pack_hash,
            "project_root": self.pack["project_root"],
            "global_status": self.status,
            "timestamps": {
                "started_at": self.start_time.isoformat(),
                "ended_at": end_time.isoformat()
            },
            "shard_counts": {
                "reported_shards": len(self.worker_summaries),
                "successful_shards": len(successful),
                "failed_shards": len(failed),
                "blocked_shards": len(blocked)
            },
            "aggregate_counts": {
                "total_findings": len(self.global_findings),
                "total_evidence": len(self.global_evidence),
                "total_errors": len(self.global_errors)
            },
            "indexes": {
                "finding_index": self.finding_index,
                "evidence_index": self.evidence_index,
                "shard_index": self.shard_index,
                "error_index": self.error_index
            },
            "worker_runs": self.worker_summaries,
            "manager_version": MANAGER_VERSION
        }
        
        # Write Global Pack
        with open(self.mission_dir / "global_findings.json", "w") as f:
            json.dump({"findings": self.global_findings}, f, indent=2)
        with open(self.mission_dir / "global_evidence.json", "w") as f:
            json.dump({"evidence": self.global_evidence}, f, indent=2)
        with open(self.mission_dir / "global_errors.json", "w") as f:
            json.dump({"errors": self.global_errors}, f, indent=2)
        with open(self.mission_dir / "global_mission_report.json", "w") as f:
            json.dump(report, f, indent=2)
            
        self.log(f"✨ Global Mission Pack Stabilized. Status: {self.status}")
        self.log(f"📁 Global Report: {self.mission_dir}/global_mission_report.json")

    def run(self):
        self.validate_pack()
        for shard in self.pack["shards"]:
            self.execute_shard(shard)
        self.finalize()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pack", help="Path to mission_pack.json")
    args = parser.parse_args()

    manager = HarnessManager(args.pack)
    manager.run()

if __name__ == "__main__":
    main()
