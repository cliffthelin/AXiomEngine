import unittest
import json
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch
from scripts.governance_closer import GovernanceCloser

class TestGovernanceCloserHardened(unittest.TestCase):
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
            "mission_pack_id": "MPK-TEST",
            "manager_run_id": "MGR-TEST",
            "pack_hash": "HASH-123"
        }
        self.findings_data = {"findings": [
            {
                "finding_id": "FND-VALID",
                "mission_pack_id": "MPK-TEST",
                "manager_run_id": "MGR-TEST",
                "worker_run_id": "WRK-1",
                "file": "target.py",
                "line_start": 1, "line_end": 1,
                "shard_name": "shard_1",
                "rationale": "Valid issue",
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
                "mission_pack_id": "MPK-TEST",
                "manager_run_id": "MGR-TEST",
                "worker_run_id": "WRK-1"
            }
        ]}
        self.export_data = {
            "mission_pack_id": "MPK-TEST",
            "manager_run_id": "MGR-TEST",
            "reviewed_at": "2026-05-12T18:00:00Z",
            "decisions": {"FND-VALID": "ACCEPTED"}
        }
        
        self.write_artifacts()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def write_artifacts(self):
        (self.artifact_dir / "global_mission_report.json").write_text(json.dumps(self.report_data))
        (self.artifact_dir / "global_findings.json").write_text(json.dumps(self.findings_data))
        (self.artifact_dir / "global_evidence.json").write_text(json.dumps(self.evidence_data))
        (self.artifact_dir / "global_decisions.json").write_text(json.dumps(self.export_data))

    def test_rejected_count_incremented(self):
        # Trigger validation failure
        self.export_data["decisions"]["FND-MISSING"] = "ACCEPTED"
        self.write_artifacts()
        
        closer = GovernanceCloser(self.project_root, self.artifact_dir / "global_decisions.json", dry_run=False, strict=False)
        closer.promote(self.decisions_file)
        
        report_path = self.artifact_dir / "closer_report.json"
        status = json.loads(report_path.read_text())
        self.assertEqual(status["rejected_count"], 1)

    def test_historical_reports_created(self):
        closer = GovernanceCloser(self.project_root, self.artifact_dir / "global_decisions.json", dry_run=True)
        closer.promote(self.decisions_file)
        
        history_dir = self.artifact_dir / "closer_reports"
        self.assertTrue(history_dir.exists())
        self.assertEqual(len(list(history_dir.glob("closer_report_*.json"))), 1)

    @patch("sys.exit")
    def test_exit_code_on_failure(self, mock_exit):
        from scripts.governance_closer import main
        # Force a failure by corrupting the export file
        self.export_data["mission_pack_id"] = "WRONG-ID"
        self.write_artifacts()
        
        with patch("sys.argv", ["governance_closer.py", str(self.artifact_dir / "global_decisions.json"), "--commit"]):
            main()
            mock_exit.assert_called_with(1)

    def test_policy_accuracy(self):
        closer = GovernanceCloser(self.project_root, self.artifact_dir / "global_decisions.json", dry_run=False, strict=True)
        closer.promote(self.decisions_file)
        
        data = json.loads(self.decisions_file.read_text())
        dec = data["decisions"][0]
        self.assertEqual(dec["promotion_policy"]["strict"], True)
        self.assertEqual(dec["promotion_policy"]["allow_partial"], False)

if __name__ == "__main__":
    unittest.main()
