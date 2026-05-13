import unittest
import json
import shutil
import tempfile
import hashlib
from pathlib import Path
from scripts.governance_manifest_verifier import verify_manifest

class TestGovernanceManifestVerifier(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.repo_dir = self.test_dir / "repo"
        self.repo_dir.mkdir()
        
        # Create a mock file
        self.file_path = self.repo_dir / "governance_closer.py"
        self.file_content = b"print('Hello Baseline')"
        self.file_path.write_bytes(self.file_content)
        self.file_hash = hashlib.sha256(self.file_content).hexdigest()
        
        # Create a mock manifest
        self.manifest_path = self.test_dir / "manifest.json"
        self.manifest_data = {
            "baseline_version": "1.3.1-TEST",
            "files": [
                {
                    "path": str(self.file_path),
                    "sha256": self.file_hash
                }
            ]
        }
        self.manifest_path.write_text(json.dumps(self.manifest_data))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_detect_unchanged(self):
        # Should exit 0
        try:
            # We need to change CWD or use absolute paths in manifest
            # For test, we use absolute paths in manifest data
            verify_manifest(self.manifest_path)
        except SystemExit as e:
            self.assertEqual(e.code, 0)

    def test_detect_modification(self):
        # Modify file
        self.file_path.write_bytes(b"MODIFIED")
        
        # Should exit 1
        with self.assertRaises(SystemExit) as cm:
            verify_manifest(self.manifest_path)
        self.assertEqual(cm.exception.code, 1)

    def test_detect_missing(self):
        # Delete file
        self.file_path.unlink()
        
        # Should exit 1
        with self.assertRaises(SystemExit) as cm:
            verify_manifest(self.manifest_path)
        self.assertEqual(cm.exception.code, 1)

    def test_allow_drift(self):
        # Modify file
        self.file_path.write_bytes(b"MODIFIED")
        
        # Should exit 0 with allow_drift
        try:
            verify_manifest(self.manifest_path, allow_drift=True)
        except SystemExit as e:
            self.assertEqual(e.code, 0)

    def test_real_baseline_integrity(self):
        # Verify our actual project baseline
        # This will fail if I (Antigravity) accidentally modified anything frozen
        try:
            verify_manifest("docs/audit/baseline_manifest_v1_3_1.json")
        except SystemExit as e:
            self.assertEqual(e.code, 0)

if __name__ == "__main__":
    unittest.main()
