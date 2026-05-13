import unittest
import json
import shutil
import tempfile
import io
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from scripts.governance_cli import main

class TestGovernanceCLI(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_root = self.test_dir / "project"
        self.project_root.mkdir()
        
        # Setup minimal project structure
        (self.project_root / "data").mkdir()
        (self.project_root / "data" / "decisions.json").write_text(json.dumps({"decisions": []}))
        (self.project_root / "docs/audit").mkdir(parents=True)
        self.manifest_path = self.project_root / "docs/audit/baseline_manifest_v1_3_1.json"
        self.manifest_path.write_text(json.dumps({
            "baseline_version": "1.3.1-TEST",
            "files": [
                {"path": "data/decisions.json", "sha256": "mock"}
            ]
        }))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def run_cli(self, args):
        with patch("sys.argv", ["governance_cli.py"] + args):
            with patch("sys.stdout", new=io.StringIO()) as fake_out:
                try:
                    main()
                    return fake_out.getvalue(), 0
                except SystemExit as e:
                    return fake_out.getvalue(), e.code

    def test_help_output(self):
        output, code = self.run_cli(["--help"])
        self.assertIn("verify-baseline", output)
        self.assertIn("server", output)
        self.assertIn("close", output)
        self.assertIn("summary", output)
        self.assertIn("audit-package", output)

    def test_verify_baseline_project_root(self):
        # Move decisions.json to subroot to test project-root resolution
        subroot = self.project_root / "sub"
        subroot.mkdir()
        (subroot / "data").mkdir()
        (subroot / "data" / "decisions.json").write_text(json.dumps({"decisions": []}))
        
        # Run verify pointing to subroot
        output, code = self.run_cli([
            "verify-baseline", 
            "--manifest", str(self.manifest_path),
            "--project-root", str(subroot)
        ])
        # Note: manifest has sha256: "mock", so it might detect drift, but it shouldn't be MISSING
        self.assertNotIn("MISSING", output)

    def test_summary_comprehensive(self):
        output, code = self.run_cli(["summary", "--project-root", str(self.project_root), "--json"])
        self.assertEqual(code, 0)
        data = json.loads(output)
        required = [
            "baseline_version", "baseline_drift_detected", "decision_count",
            "latest_report_status", "historical_report_count", "total_promoted",
            "total_rejected", "total_duplicate_skips", "timestamp"
        ]
        for field in required:
            self.assertIn(field, data)

    def test_audit_package_comprehensive(self):
        out_dir = self.test_dir / "audit_out"
        output, code = self.run_cli(["audit-package", "--project-root", str(self.project_root), "--output-dir", str(out_dir)])
        self.assertEqual(code, 0)
        
        files = list(out_dir.glob("audit_inventory_*.json"))
        data = json.loads(files[0].read_text())
        
        self.assertEqual(data["baseline_manifest"], str(self.manifest_path))
        # Should source frozen components from manifest (we added data/decisions.json in setUp)
        self.assertIn("data/decisions.json", data["frozen_components"])
        self.assertIn("verification_result", data)
        self.assertIn("known_limitations", data)

    @patch("scripts.governance_cli.GovernanceCloser")
    def test_close_delegation_shape_v1_3_1(self, mock_closer_class):
        mock_closer = MagicMock()
        mock_closer_class.return_value = mock_closer
        mock_closer.promote.return_value = True
        
        # Scenario: commit=True (dry_run=False), allow-partial=True (strict=False)
        output, code = self.run_cli([
            "close", "mock_export", 
            "--commit", "--allow-partial", 
            "--authority", "Test Authority",
            "--force"
        ])
        
        self.assertEqual(code, 0)
        # Verify constructor args (v1.3.1 shape)
        mock_closer_class.assert_called_once_with(
            project_root=".",
            export_path="mock_export",
            dry_run=False,
            strict=False
        )
        # Verify promote args (v1.3.1 shape)
        mock_closer.promote.assert_called_once_with(
            "data/decisions.json",
            authority="Test Authority",
            force=True
        )

    @patch("scripts.governance_cli.GovernanceCloser")
    def test_close_delegation_defaults(self, mock_closer_class):
        mock_closer = MagicMock()
        mock_closer_class.return_value = mock_closer
        mock_closer.promote.return_value = True
        
        # Scenario: default (dry_run=True, strict=True)
        output, code = self.run_cli(["close", "mock_export"])
        
        self.assertEqual(code, 0)
        mock_closer_class.assert_called_once_with(
            project_root=".",
            export_path="mock_export",
            dry_run=True,
            strict=True
        )

    @patch("scripts.governance_dashboard_server.main")
    def test_server_delegation(self, mock_server_main):
        output, code = self.run_cli(["server", "--port", "9999"])
        self.assertEqual(code, 0)
        mock_server_main.assert_called_once()

if __name__ == "__main__":
    unittest.main()
