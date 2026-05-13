#!/usr/bin/env python3
"""
AXiomEngine Governance Closer (Phase 7B) — HARDENED PROMOTION NODE
============================================================
Role: Safely promotes human-reviewed findings into formal determinations.
v1.3.0: Operational excellence, exit codes, and historical reports.
"""
import argparse
import json
import uuid
import shutil
import tempfile
import sys
from pathlib import Path
from datetime import datetime

CLOSER_VERSION = "1.3.0"

def log_action(msg):
    print(f"🏛️ [CLOSER] {msg}")

class GovernanceCloser:
    def __init__(self, project_root, export_path, dry_run=True, strict=True):
        self.project_root = Path(project_root)
        self.export_path = Path(export_path)
        self.dry_run = dry_run
        self.strict = strict
        
        if not self.export_path.exists():
            raise FileNotFoundError(f"Global Decisions export not found: {export_path}")
            
        # Artifact Collection
        self.artifact_dir = self.export_path.parent
        self.files = {
            "decisions": self.export_path,
            "report": self.artifact_dir / "global_mission_report.json",
            "findings": self.artifact_dir / "global_findings.json",
            "evidence": self.artifact_dir / "global_evidence.json"
        }
        
        self.data = {}
        self.load_artifacts()
        
    def load_artifacts(self):
        for key, path in self.files.items():
            if not path.exists():
                raise FileNotFoundError(f"Required mission artifact missing: {path}")
            self.data[key] = json.loads(path.read_text())
        log_action(f"Artifacts loaded and parsed: {list(self.files.keys())}")

    def validate_traceability(self):
        log_action("Validating mission traceability...")
        report = self.data["report"]
        decisions = self.data["decisions"]
        
        # 1. Global ID Match
        if report["mission_pack_id"] != decisions["mission_pack_id"]:
            raise ValueError("Mission Pack ID mismatch between report and decisions export.")
        if report["manager_run_id"] != decisions["manager_run_id"]:
            raise ValueError("Manager Run ID mismatch between report and decisions export.")
            
        # 2. Findings Consistency
        finding_map = {f["finding_id"]: f for f in self.data["findings"].get("findings", [])}
        evidence_map = {e["evidence_id"]: e for e in self.data["evidence"].get("evidence", [])}
        
        accepted_ids = [fid for fid, status in decisions["decisions"].items() if status == "ACCEPTED"]
        log_action(f"Found {len(accepted_ids)} findings marked ACCEPTED for promotion.")
        
        valid_promotions = []
        rejected_ids = []

        for fid in accepted_ids:
            if fid not in finding_map:
                rejected_ids.append(f"Finding {fid} not found in global_findings.json")
                continue
            
            f_item = finding_map[fid]
            
            # 1. Finding Metadata Consistency
            if f_item.get("manager_run_id") != report["manager_run_id"]:
                rejected_ids.append(f"Finding {fid} manager_run_id mismatch.")
                continue

            # 2. Evidence Consistency
            missing_evidence = []
            mismatched_evidence = []
            for eid in f_item.get("evidence_refs", []):
                if eid not in evidence_map:
                    missing_evidence.append(eid)
                    continue
                
                e_item = evidence_map[eid]
                if e_item.get("mission_pack_id") != report["mission_pack_id"]:
                    mismatched_evidence.append(f"{eid} mission_pack_id mismatch")
                if e_item.get("manager_run_id") != report["manager_run_id"]:
                    mismatched_evidence.append(f"{eid} manager_run_id mismatch")
                if e_item.get("worker_run_id") != f_item.get("worker_run_id"):
                    mismatched_evidence.append(f"{eid} worker_run_id mismatch")

            if missing_evidence:
                rejected_ids.append(f"Finding {fid} is missing evidence: {missing_evidence}")
                continue
            if mismatched_evidence:
                rejected_ids.append(f"Finding {fid} has inconsistent evidence metadata: {mismatched_evidence}")
                continue
                
            valid_promotions.append(f_item)
            
        return valid_promotions, rejected_ids

    def promote(self, decisions_file, authority="Human Governor", force=False):
        dec_path = Path(decisions_file)
        report_path = self.artifact_dir / "closer_report.json"
        
        status = {
            "closer_version": CLOSER_VERSION,
            "timestamp": datetime.now().isoformat(),
            "export_path": str(self.export_path),
            "decisions_file": str(dec_path),
            "mission_pack_id": self.data["report"].get("mission_pack_id"),
            "manager_run_id": self.data["report"].get("manager_run_id"),
            "dry_run": self.dry_run,
            "strict": self.strict,
            "force": force,
            "requested_accept_count": 0,
            "valid_promotion_count": 0,
            "skipped_duplicate_count": 0,
            "rejected_count": 0,
            "validation_errors": [],
            "promoted_decision_ids": []
        }

        try:
            decisions_map = self.data["decisions"].get("decisions", {})
            status["requested_accept_count"] = sum(1 for s in decisions_map.values() if s == "ACCEPTED")
            
            promotions, rejected_errors = self.validate_traceability()
            status["validation_errors"].extend(rejected_errors)
            status["rejected_count"] = len(rejected_errors)
            
            if rejected_errors:
                for err in rejected_errors:
                    log_action(f"❌ ERROR: {err}")
                if self.strict:
                    self.write_report(report_path, status)
                    raise ValueError(f"Strict Mode: Aborting promotion due to validation errors: {rejected_errors}")

            if not promotions:
                log_action("No valid findings to promote.")
                status["rejected_count"] = status["requested_accept_count"]
                self.write_report(report_path, status)
                return

            if not dec_path.exists():
                auth_data = {"decisions": []}
            else:
                auth_data = json.loads(dec_path.read_text())

            # Idempotency Check
            existing_keys = {
                (d["prompted_by"]["mission_pack_id"], d["prompted_by"]["manager_run_id"], d["prompted_by"]["finding_ref"])
                for d in auth_data["decisions"]
                if "prompted_by" in d
            }

            evidence_map = {e["evidence_id"]: e for e in self.data["evidence"].get("evidence", [])}
            new_entries = []
            for f in promotions:
                key = (self.data["report"]["mission_pack_id"], self.data["report"]["manager_run_id"], f["finding_id"])
                if key in existing_keys and not force:
                    log_action(f"⏭️ Skipping duplicate: {f['finding_id']} (Already promoted)")
                    status["skipped_duplicate_count"] += 1
                    continue

                # Build Evidence Snapshots
                ev_snapshots = []
                for eid in f.get("evidence_refs", []):
                    ev = evidence_map.get(eid, {})
                    ev_snapshots.append({
                        "evidence_id": eid,
                        "source_file": ev.get("source_file"),
                        "source_hash": ev.get("source_hash"),
                        "line_range": [ev.get("line_start"), ev.get("line_end")],
                        "excerpt": ev.get("excerpt")
                    })

                decision = {
                    "decision_id": f"DEC-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}",
                    "decision_type": "SecurityDetermination",
                    "status": "promoted",
                    "promotion_policy": {
                        "strict": self.strict,
                        "force": force,
                        "dry_run": self.dry_run,
                        "allow_partial": not self.strict
                    },
                    "prompted_by": {
                        "context_type": "mission_audit",
                        "mission_pack_id": self.data["report"]["mission_pack_id"],
                        "manager_run_id": self.data["report"]["manager_run_id"],
                        "finding_ref": f["finding_id"],
                        "shard_name": f["shard_name"],
                        "worker_run_id": f["worker_run_id"]
                    },
                    "evidence_context": {
                        "source_file": f["file"],
                        "line_range": [f["line_start"], f["line_end"]],
                        "finding_snapshot": f,
                        "evidence_refs": f["evidence_refs"],
                        "evidence_snapshots": ev_snapshots,
                        "pack_hash": self.data["report"]["pack_hash"]
                    },
                    "statement": f["rationale"],
                    "authority": authority,
                    "reviewed_at": self.data["decisions"].get("reviewed_at"),
                    "promoted_at": datetime.now().isoformat(),
                    "closer_version": CLOSER_VERSION
                }
                new_entries.append(decision)
                status["promoted_decision_ids"].append(decision["decision_id"])

            status["valid_promotion_count"] = len(new_entries)
            
            if self.dry_run:
                log_action(f"🔍 [DRY RUN] Would promote {len(new_entries)} decisions to {dec_path}")
                self.write_report(report_path, status)
                return

            # ATOMIC SAFE WRITE
            if new_entries:
                log_action(f"Promoting {len(new_entries)} decisions...")
                if dec_path.exists():
                    backup_path = dec_path.with_suffix(".json.bak")
                    shutil.copy(dec_path, backup_path)
                    log_action(f"Backup created: {backup_path}")
                auth_data["decisions"].extend(new_entries)
                with tempfile.NamedTemporaryFile('w', delete=False, dir=dec_path.parent) as tf:
                    json.dump(auth_data, tf, indent=2)
                    temp_name = tf.name
                Path(temp_name).replace(dec_path)
                log_action(f"✅ Successfully promoted decisions to {dec_path}")
            
            self.write_report(report_path, status)

        except Exception as e:
            if not status["validation_errors"]:
                status["validation_errors"].append(str(e))
            self.write_report(report_path, status)
            raise e

    def write_report(self, path, status):
        # Latest
        with open(path, "w") as f:
            json.dump(status, f, indent=2)
            
        # Historical
        history_dir = self.artifact_dir / "closer_reports"
        history_dir.mkdir(exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        hist_path = history_dir / f"closer_report_{ts}_{uuid.uuid4().hex[:4]}.json"
        with open(hist_path, "w") as f:
            json.dump(status, f, indent=2)
            
        log_action(f"📊 Closer report written to {path} (Historical copy preserved)")

def main():
    parser = argparse.ArgumentParser(description="AXiomEngine Governance Closer (Phase 7B)")
    parser.add_argument("export", help="Path to global_decisions.json")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--decisions-file", help="Path to data/decisions.json (overrides root/data/decisions.json)")
    parser.add_argument("--authority", default="Human Governor", help="Signing authority")
    parser.add_argument("--commit", action="store_true", help="Actually write changes (default is DRY RUN)")
    parser.add_argument("--allow-partial", action="store_true", help="Allow partial promotion if some findings are invalid")
    parser.add_argument("--force", action="store_true", help="Force promotion of duplicate entries")
    args = parser.parse_args()

    # Resolve decisions file
    if args.decisions_file:
        dec_file = Path(args.decisions_file)
    else:
        dec_file = Path(args.project_root) / "data" / "decisions.json"

    closer = GovernanceCloser(args.project_root, args.export, dry_run=not args.commit, strict=not args.allow_partial)
    try:
        closer.promote(dec_file, authority=args.authority, force=args.force)
    except Exception as e:
        log_action(f"❌ FATAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
