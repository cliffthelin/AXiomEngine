import unittest
import json
import shutil
import tempfile
import io
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from scripts.release_verifier import main

class TestReleaseVerifier(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.project_root = self.test_dir / "project"
        self.project_root.mkdir()
        
        # Setup required files
        (self.project_root / "scripts").mkdir()
        (self.project_root / "data").mkdir()
        (self.project_root / "docs/audit").mkdir(parents=True)
        (self.project_root / "tests").mkdir()
        
        for f in [
            "scripts/governance_cli.py",
            "scripts/governance_dashboard_server.py",
            "governance_dashboard_v1_4.html",
            "docs/audit/AXIOMENGINE_GOVERNANCE_V1_4_0_COMPLETION_RECORD.md",
            "docs/audit/baseline_manifest_v1_3_1.json",
            "scripts/release_verifier.py",
            "data/decisions.json"
        ]:
            (self.project_root / f).write_text("mock")
            
        # Valid manifest content for build_manifest_verification_result
        (self.project_root / "docs/audit/baseline_manifest_v1_3_1.json").write_text(json.dumps({
            "baseline_version": "1.3.1-TEST",
            "files": []
        }))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def run_verifier(self, args):
        old_cwd = os.getcwd()
        try:
            with patch("sys.argv", ["release_verifier.py"] + args):
                with patch("sys.stdout", new=io.StringIO()) as fake_out:
                    try:
                        main()
                        return fake_out.getvalue(), 0
                    except SystemExit as e:
                        return fake_out.getvalue(), e.code
        finally:
            os.chdir(old_cwd)

    @patch("subprocess.run")
    def test_release_stable(self, mock_run):
        # Mock successful unittest run with exact expected count
        # (Assuming TESTS_EXPECTED = 46 in the implementation)
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="Ran 46 tests in 0.1s\n\nOK")
        
        output, code = self.run_verifier(["--project-root", str(self.project_root), "--json"])
        self.assertEqual(code, 0)
        data = json.loads(output)
        self.assertEqual(data["release_status"], "STABLE")
        self.assertEqual(data["tests_observed"], 46)
        self.assertEqual(data["tests_expected"], 46)
        self.assertTrue(data["tests_passed"])

    @patch("subprocess.run")
    def test_insufficient_tests_fails(self, mock_run):
        # Even if all pass, if we only ran 10 but expected 46, it should be UNSTABLE
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="Ran 10 tests\n\nOK")
        
        output, code = self.run_verifier(["--project-root", str(self.project_root), "--json"])
        self.assertEqual(code, 1)
        data = json.loads(output)
        self.assertEqual(data["release_status"], "UNSTABLE")
        self.assertEqual(data["tests_observed"], 10)

    @patch("subprocess.run")
    def test_missing_file_fails(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="Ran 46 tests\n\nOK")
        # Remove a required file
        (self.project_root / "governance_dashboard_v1_4.html").unlink()
        
        output, code = self.run_verifier(["--project-root", str(self.project_root), "--json"])
        self.assertEqual(code, 1)
        data = json.loads(output)
        self.assertEqual(data["release_status"], "UNSTABLE")
        self.assertIn("governance_dashboard_v1_4.html", data["missing_files"])

    @patch("subprocess.run")
    def test_test_failure_fails(self, mock_run):
        # Mock failing unittest
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="Ran 46 tests\n\nFAILED (failures=1)")
        
        output, code = self.run_verifier(["--project-root", str(self.project_root), "--json"])
        self.assertEqual(code, 1)
        data = json.loads(output)
        self.assertEqual(data["release_status"], "UNSTABLE")
        self.assertFalse(data["tests_passed"])

    @patch("scripts.release_verifier.build_manifest_verification_result")
    @patch("subprocess.run")
    def test_baseline_drift_fails(self, mock_run, mock_build):
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="Ran 46 tests\n\nOK")
        mock_build.return_value = {"drift_detected": True, "baseline_version": "1.3.1-DRIFTED"}
        
        output, code = self.run_verifier(["--project-root", str(self.project_root), "--json"])
        self.assertEqual(code, 1)
        data = json.loads(output)
        self.assertEqual(data["release_status"], "UNSTABLE")
        self.assertTrue(data["baseline_drift_detected"])

if __name__ == "__main__":
    unittest.main()
