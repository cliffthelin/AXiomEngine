import unittest
import json
import os
import shutil
import tempfile
import sys
import hashlib
from unittest.mock import patch, MagicMock
from pathlib import Path
from scripts.harness_manager import HarnessManager

class TestHarnessManagerStabilized(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.project_root = Path(self.test_dir) / "project"
        self.project_root.mkdir()
        
        # Create target files
        (self.project_root / "scripts").mkdir()
        self.target_a = self.project_root / "scripts/auth.py"
        self.target_a.write_text("subprocess.run('ls', shell=True)") # Finding
        self.target_b = self.project_root / "scripts/intent.py"
        self.target_b.write_text("print('clean')") # No Finding
        
        # Base Pack
        self.pack_data = {
            "mission_pack_id": "MPK-STABILIZED-001",
            "project_root": str(self.project_root),
            "shards": []
        }
        self.pack_path = self.project_root / "mission_pack.json"

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def write_pack(self, shards):
        self.pack_data["shards"] = shards
        self.pack_path.write_text(json.dumps(self.pack_data))

    def test_all_clean_completed(self):
        self.write_pack([
            {"name": "clean_1", "goal": "Audit", "type": "worker", "scope": "scripts/intent.py", "flags": []}
        ])
        manager = HarnessManager(self.pack_path)
        manager.run()
        self.assertEqual(manager.status, "COMPLETED")
        self.assertEqual(manager.global_findings, [])

    def test_all_failed_failed(self):
        self.write_pack([
            {"name": "fail_1", "goal": "Audit", "type": "worker", "scope": "missing.py", "flags": []}
        ])
        manager = HarnessManager(self.pack_path)
        manager.run()
        self.assertEqual(manager.status, "FAILED")
        
        # Check error reporting
        with open(manager.mission_dir / "global_mission_report.json") as f:
            report = json.load(f)
            self.assertEqual(report["shard_counts"]["failed_shards"], 1)
            self.assertEqual(report["worker_runs"][0]["error"]["type"], "FileNotFoundError")

    def test_blocked_dominates_status(self):
        # One success, one blocked
        outside_file = Path(self.test_dir) / "evil.py"
        outside_file.write_text("danger")
        
        self.write_pack([
            {"name": "success", "goal": "Audit", "type": "worker", "scope": "scripts/intent.py", "flags": []},
            {"name": "blocked", "goal": "Audit", "type": "worker", "scope": str(outside_file), "flags": []}
        ])
        manager = HarnessManager(self.pack_path)
        manager.run()
        self.assertEqual(manager.status, "BLOCKED")

    def test_finding_metadata_enrichment(self):
        self.write_pack([
            {"name": "auth_shard", "goal": "Audit", "type": "worker", "scope": "scripts/auth.py", "flags": []}
        ])
        manager = HarnessManager(self.pack_path)
        manager.run()
        
        self.assertEqual(len(manager.global_findings), 1)
        finding = manager.global_findings[0]
        self.assertEqual(finding["shard_name"], "auth_shard")
        self.assertIn("worker_run_id", finding)
        self.assertIn("manager_run_id", finding)
        self.assertEqual(finding["mission_pack_id"], "MPK-STABILIZED-001")

    def test_malformed_json_handling(self):
        # Mock subprocess.run to return malformed JSON
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="This is not JSON",
                stderr="Segmentation Fault",
                returncode=139
            )
            
            self.write_pack([
                {"name": "crash_shard", "goal": "Audit", "type": "worker", "scope": "scripts/auth.py", "flags": []}
            ])
            manager = HarnessManager(self.pack_path)
            manager.run()
            
            self.assertEqual(manager.status, "FAILED")
            self.assertEqual(len(manager.global_errors), 1)
            error = manager.global_errors[0]
            self.assertEqual(error["shard_name"], "crash_shard")
            self.assertEqual(error["error_type"], "JSONDecodeError")
            self.assertEqual(error["failure_stage"], "dispatcher")

    def test_accurate_shard_counts(self):
        self.write_pack([
            {"name": "s1", "goal": "Audit", "type": "worker", "scope": "scripts/intent.py", "flags": []},
            {"name": "f1", "goal": "Audit", "type": "worker", "scope": "missing.py", "flags": []}
        ])
        manager = HarnessManager(self.pack_path)
        manager.run()
        
        with open(manager.mission_dir / "global_mission_report.json") as f:
            report = json.load(f)
            counts = report["shard_counts"]
            self.assertEqual(counts["reported_shards"], 2)
            self.assertEqual(counts["successful_shards"], 1)
            self.assertEqual(counts["failed_shards"], 1)
            self.assertEqual(report["global_status"], "PARTIAL")

if __name__ == "__main__":
    unittest.main()
