#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

class ReleaseManager:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.dist_dir = self.root_dir / "dist"

    def build_binary(self):
        print(f"Packaging AXiomEngine Pi...")
        self.dist_dir.mkdir(exist_ok=True)
        # Zip core directories to create a basic binary build bundle
        archive_path = self.dist_dir / "pi-agent-bundle"
        shutil.make_archive(str(archive_path), 'zip', self.root_dir, 'pi')
        print(f"Build complete: {archive_path}.zip")

    def sync_versions(self):
        import json
        pkg_path = self.root_dir / "package.json"
        if pkg_path.exists():
            with open(pkg_path, "r") as f:
                pkg = json.load(f)
            version = pkg.get("version", "1.0.0")
            print(f"Syncing version {version} across codebase...")
            # Example: write to a version file
            with open(self.root_dir / "VERSION", "w") as f:
                f.write(version)
        else:
            print("No package.json found, skipping version sync.")

if __name__ == "__main__":
    rm = ReleaseManager()
    rm.build_binary()
