import unittest
import json
import threading
import time
import urllib.request
import urllib.error
import shutil
import tempfile
import hashlib
from pathlib import Path
from scripts.governance_dashboard_server import GovernanceServer, GovernanceDiscoveryHandler

class TestGovernanceDashboardServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path(tempfile.mkdtemp())
        cls.project_root = cls.test_dir / "project"
        cls.project_root.mkdir()
        
        # Additional mission dir
        cls.mission_dir = cls.test_dir / "mission_ext"
        cls.mission_dir.mkdir()
        
        # Setup mock files in project root
        (cls.project_root / "data").mkdir()
        (cls.project_root / "data" / "decisions.json").write_text(json.dumps({"decisions": []}))
        
        (cls.project_root / "docs/audit").mkdir(parents=True)
        (cls.project_root / "docs/audit/baseline_manifest_v1_3_1.json").write_text(json.dumps({
            "baseline_version": "1.3.1-TEST",
            "files": []
        }))
        
        # Report in project root (older)
        (cls.project_root / "closer_report.json").write_text(json.dumps({
            "timestamp": "2026-05-12T10:00:00Z",
            "valid_promotion_count": 5,
            "dry_run": False,
            "validation_errors": []
        }))

        # Report in external mission dir (newer)
        (cls.mission_dir / "closer_report.json").write_text(json.dumps({
            "timestamp": "2026-05-12T18:00:00Z",
            "valid_promotion_count": 10,
            "dry_run": False,
            "validation_errors": []
        }))
        
        # Malformed artifact
        (cls.project_root / "global_findings.json").write_text("{ malformed json }")

        cls.host = "127.0.0.1"
        cls.port = 8767
        cls.server = GovernanceServer((cls.host, cls.port), GovernanceDiscoveryHandler, cls.project_root, [cls.mission_dir])
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        shutil.rmtree(cls.test_dir)

    def get_url(self, path):
        return f"http://{self.host}:{self.port}{path}"

    def test_latest_report_timestamp_selection(self):
        # Should pick the 10-count report from mission_ext
        with urllib.request.urlopen(self.get_url("/api/governance/latest-report")) as r:
            data = json.load(r)
            self.assertEqual(data["valid_promotion_count"], 10)

    def test_mission_artifacts_malformed_handling(self):
        with urllib.request.urlopen(self.get_url("/api/governance/mission-artifacts")) as r:
            data = json.load(r)
            self.assertEqual(data["global_findings"]["status"], "PRESENT")
            self.assertIn("parse_error", data["global_findings"]["data"])

    def test_cors_allowed_local(self):
        req = urllib.request.Request(self.get_url("/health"), headers={"Origin": "http://localhost:3000"})
        with urllib.request.urlopen(req) as r:
            self.assertEqual(r.headers.get("Access-Control-Allow-Origin"), "http://localhost:3000")

    def test_cors_rejected_non_local(self):
        req = urllib.request.Request(self.get_url("/health"), headers={"Origin": "http://malicious.com"})
        with urllib.request.urlopen(req) as r:
            self.assertIsNone(r.headers.get("Access-Control-Allow-Origin"))

    def test_baseline_status_uses_logic(self):
        # Verify that it reports our mock manifest correctly
        with urllib.request.urlopen(self.get_url("/api/governance/baseline/status")) as r:
            data = json.load(r)
            self.assertEqual(data["baseline_version"], "1.3.1-TEST")
            self.assertFalse(data["drift_detected"])

    def test_summary_aggregates_multiple_dirs(self):
        with urllib.request.urlopen(self.get_url("/api/governance/summary")) as r:
            data = json.load(r)
            # 5 from root + 10 from ext = 15
            self.assertEqual(data["total_promoted"], 15)
            self.assertEqual(data["historical_report_count"], 2)

    def test_no_duplicate_definitions(self):
        # Hygiene check: ensure no duplicate class definitions (prevents agent maintenance drift)
        path = Path("scripts/governance_dashboard_server.py")
        content = path.read_text()
        matches = content.count("class GovernanceDiscoveryHandler")
        self.assertEqual(matches, 1, f"Found {matches} definitions of GovernanceDiscoveryHandler (Expected 1)")

if __name__ == "__main__":
    unittest.main()
