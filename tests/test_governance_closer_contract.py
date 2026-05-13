import unittest
import json
import shutil
import tempfile
from pathlib import Path
from scripts.governance_closer import GovernanceCloser

class TestGovernanceCloserContract(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_root = self.test_dir / "project"
        self.project_root.mkdir()
        self.decisions_file = self.project_root / "data" / "decisions.json"
        self.decisions_file.parent.mkdir()
        self.decisions_file.write_text(json.dumps({"decisions": []}))
        
        # Mock Artifacts
        self.artifact_dir = self.test_dir / "mission_pack"
        self.artifact_dir.mkdir()
        
        self.report_data = {
            "mission_pack_id": "MPK-CONTRACT-TEST",
            "manager_run_id": "MGR-CONTRACT-TEST",
            "pack_hash": "HASH-CONTRACT-123"
        }
        self.findings_data = {"findings": [
            {
                "finding_id": "FND-1",
                "mission_pack_id": "MPK-CONTRACT-TEST",
                "manager_run_id": "MGR-CONTRACT-TEST",
                "worker_run_id": "WRK-1",
                "file": "target.py",
                "line_start": 1, "line_end": 1,
                "shard_name": "shard_1",
                "rationale": "Contract Test Finding",
                "evidence_refs": ["EVD-1"]
            }
        ]}
        self.evidence_data = {"evidence": [
            {
                "evidence_id": "EVD-1", 
                "source_file": "target.py",
                "source_hash": "SHA-EVD-1",
                "line_start": 10, "line_end": 15,
                "excerpt": "danger()",
                "mission_pack_id": "MPK-CONTRACT-TEST",
                "manager_run_id": "MGR-CONTRACT-TEST",
                "worker_run_id": "WRK-1"
            }
        ]}
        self.export_data = {
            "mission_pack_id": "MPK-CONTRACT-TEST",
            "manager_run_id": "MGR-CONTRACT-TEST",
            "reviewed_at": "2026-05-12T18:00:00Z",
            "decisions": {"FND-1": "ACCEPTED"}
        }
        
        self.write_artifacts()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def write_artifacts(self):
        (self.artifact_dir / "global_mission_report.json").write_text(json.dumps(self.report_data))
        (self.artifact_dir / "global_findings.json").write_text(json.dumps(self.findings_data))
        (self.artifact_dir / "global_evidence.json").write_text(json.dumps(self.evidence_data))
        (self.artifact_dir / "global_decisions.json").write_text(json.dumps(self.export_data))

    def test_closer_report_dashboard_fields(self):
        closer = GovernanceCloser(self.project_root, self.artifact_dir / "global_decisions.json", dry_run=False)
        closer.promote(self.decisions_file)
        
        report_path = self.artifact_dir / "closer_report.json"
        status = json.loads(report_path.read_text())
        
        required_fields = [
            "closer_version", "timestamp", "mission_pack_id", "manager_run_id",
            "dry_run", "strict", "force", "requested_accept_count",
            "valid_promotion_count", "skipped_duplicate_count", "rejected_count",
            "validation_errors", "promoted_decision_ids"
        ]
        for field in required_fields:
            self.assertIn(field, status, f"Missing required dashboard field: {field}")

    def test_historical_report_integrity(self):
        closer = GovernanceCloser(self.project_root, self.artifact_dir / "global_decisions.json", dry_run=True)
        closer.promote(self.decisions_file)
        
        history_dir = self.artifact_dir / "closer_reports"
        hist_files = list(history_dir.glob("closer_report_*.json"))
        self.assertTrue(len(hist_files) > 0)
        
        status = json.loads(hist_files[0].read_text())
        self.assertIn("timestamp", status)
        self.assertEqual(status["dry_run"], True)

    def test_promoted_decision_snapshot_integrity(self):
        closer = GovernanceCloser(self.project_root, self.artifact_dir / "global_decisions.json", dry_run=False)
        closer.promote(self.decisions_file)
        
        decisions = json.loads(self.decisions_file.read_text())["decisions"]
        self.assertEqual(len(decisions), 1)
        dec = decisions[0]
        
        # Verify evidence_snapshots structure
        ev_snapshots = dec["evidence_context"].get("evidence_snapshots", [])
        self.assertEqual(len(ev_snapshots), 1)
        self.assertEqual(ev_snapshots[0]["source_hash"], "SHA-EVD-1")
        self.assertEqual(ev_snapshots[0]["excerpt"], "danger()")

    def test_duplicate_promotion_accounting(self):
        closer = GovernanceCloser(self.project_root, self.artifact_dir / "global_decisions.json", dry_run=False)
        closer.promote(self.decisions_file)
        
        # Run again to trigger duplicate skip
        closer.promote(self.decisions_file)
        
        status = json.loads((self.artifact_dir / "closer_report.json").read_text())
        self.assertEqual(status["skipped_duplicate_count"], 1)
        self.assertEqual(status["valid_promotion_count"], 0)

    def test_dry_run_non_mutating_report_accounting(self):
        closer = GovernanceCloser(self.project_root, self.artifact_dir / "global_decisions.json", dry_run=True)
        closer.promote(self.decisions_file)
        
        # Verify decisions file remains empty
        decisions = json.loads(self.decisions_file.read_text())["decisions"]
        self.assertEqual(len(decisions), 0)
        
        # Verify report shows dry_run=True
        status = json.loads((self.artifact_dir / "closer_report.json").read_text())
        self.assertEqual(status["dry_run"], True)
        self.assertEqual(status["valid_promotion_count"], 1)

    def test_allow_partial_preserves_errors(self):
        # Add invalid finding to export
        self.export_data["decisions"]["FND-MISSING"] = "ACCEPTED"
        self.write_artifacts()
        
        closer = GovernanceCloser(self.project_root, self.artifact_dir / "global_decisions.json", dry_run=False, strict=False)
        closer.promote(self.decisions_file)
        
        status = json.loads((self.artifact_dir / "closer_report.json").read_text())
        self.assertEqual(status["rejected_count"], 1)
        self.assertTrue(len(status["validation_errors"]) > 0)
        self.assertEqual(status["valid_promotion_count"], 1)

    def test_strict_mode_aborts_on_invalid_accepted(self):
        self.export_data["decisions"]["FND-MISSING"] = "ACCEPTED"
        self.write_artifacts()
        
        closer = GovernanceCloser(self.project_root, self.artifact_dir / "global_decisions.json", dry_run=False, strict=True)
        with self.assertRaises(ValueError):
            closer.promote(self.decisions_file)
        
        # Verify no decisions were written
        decisions = json.loads(self.decisions_file.read_text())["decisions"]
        self.assertEqual(len(decisions), 0)

if __name__ == "__main__":
    unittest.main()
