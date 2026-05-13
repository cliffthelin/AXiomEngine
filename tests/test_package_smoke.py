import unittest
import subprocess
import sys
import os
from pathlib import Path

class TestPackageSmoke(unittest.TestCase):
    def setUp(self):
        self.project_root = Path(__file__).parent.parent.absolute()

    def test_entrypoint_discovery(self):
        # Verify that scripts/__init__.py exists for packaging
        init_path = self.project_root / "scripts" / "__init__.py"
        self.assertTrue(init_path.exists(), "scripts/__init__.py missing (required for packaging)")

    def test_cli_version_v1_5_0(self):
        # Run the CLI directly from the source to check version
        env = os.environ.copy()
        env["PYTHONPATH"] = str(self.project_root)
        
        proc = subprocess.run(
            [sys.executable, str(self.project_root / "scripts/governance_cli.py"), "--version"],
            capture_output=True,
            text=True,
            env=env
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("1.5.0", proc.stdout)

    def test_package_metadata(self):
        # Check setup.py for correct metadata
        setup_py = self.project_root / "setup.py"
        self.assertTrue(setup_py.exists())
        content = setup_py.read_text()
        self.assertIn('name="axiomengine-governance"', content)
        self.assertIn('version="1.5.0"', content)
        self.assertIn('gov = scripts.governance_cli:main', content)

if __name__ == "__main__":
    unittest.main()
