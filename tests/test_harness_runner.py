import unittest
import json
import os
import shutil
import tempfile
from pathlib import Path
from scripts.harness_runner import HarnessRunner

class TestHarnessRunner(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.workspace = Path(self.test_dir) / "project"
        self.workspace.mkdir()
        
        # Create a dummy target file
        self.target = self.workspace / "target.py"
        self.target.write_text("print('hello')\nsubprocess.run('ls', shell=True)")
        
        # Create a dummy config
        self.config_data = {
            "goal": "Audit target.py",
            "type": "worker",
            "scope": "target.py",
            "flags": ["candidate-only"]
        }
        self.config_path = self.workspace / "harness.json"
        self.config_path.write_text(json.dumps(self.config_data))
        
        # Change to workspace dir for relative path testing
        self.old_cwd = os.getcwd()
        os.chdir(self.workspace)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir)

    def test_missing_fields(self):
        config = {"goal": "Only goal"}
        self.config_path.write_text(json.dumps(config))
        
        runner = HarnessRunner(self.config_path)
        with self.assertRaisesRegex(ValueError, "Missing required field"):
            runner.validate_config()

    def test_unsupported_type(self):
        config = {"goal": "G", "type": "alien", "scope": "S", "flags": []}
        self.config_path.write_text(json.dumps(config))
        
        runner = HarnessRunner(self.config_path)
        with self.assertRaisesRegex(ValueError, "Unsupported harness type"):
            runner.validate_config()

    def test_missing_scope(self):
        config = {"goal": "G", "type": "worker", "scope": "missing.py", "flags": []}
        self.config_path.write_text(json.dumps(config))
        
        runner = HarnessRunner(self.config_path)
        runner.validate_config()
        with self.assertRaises(FileNotFoundError):
            runner.resolve_scope()

    def test_path_outside_root(self):
        # Create a file outside the workspace
        outside_file = Path(self.test_dir) / "evil.py"
        outside_file.write_text("dangerous")
        
        config = {"goal": "G", "type": "worker", "scope": str(outside_file), "flags": []}
        self.config_path.write_text(json.dumps(config))
        
        runner = HarnessRunner(self.config_path)
        runner.validate_config()
        with self.assertRaises(PermissionError):
            runner.resolve_scope()

    def test_security_audit_detection(self):
        runner = HarnessRunner(self.config_path)
        runner.validate_config()
        target_path = runner.resolve_scope()
        runner.execute_worker_mission(target_path)
        status = runner.finalize()
        
        # Verify Findings
        with open(runner.findings_file) as f:
            findings = json.load(f)["findings"]
        
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["type"], "SHELL_EXEC")
        self.assertEqual(status, "SUCCESS_WITH_FINDINGS")

    def test_no_findings(self):
        self.target.write_text("print('clean code')")
        
        runner = HarnessRunner(self.config_path)
        runner.validate_config()
        target_path = runner.resolve_scope()
        runner.execute_worker_mission(target_path)
        status = runner.finalize()
        
        self.assertEqual(status, "SUCCESS_NO_FINDINGS")
        with open(runner.findings_file) as f:
            self.assertEqual(len(json.load(f)["findings"]), 0)

    def test_manifest_structure(self):
        runner = HarnessRunner(self.config_path)
        runner.validate_config()
        target_path = runner.resolve_scope()
        runner.execute_worker_mission(target_path)
        runner.finalize()
        
        with open(runner.sim_dir / "manifest.json") as f:
            manifest = json.load(f)
            
        self.assertIn("run_id", manifest)
        self.assertIn("config_hash", manifest)
        self.assertIn("target_hashes", manifest)
        self.assertEqual(manifest["status"], "SUCCESS_WITH_FINDINGS")
        self.assertEqual(manifest["runner_version"], "1.1.0")

if __name__ == "__main__":
    unittest.main()
