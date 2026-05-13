#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from scripts.pi_config import get_agent_dir

class PackageManager:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.global_dir = get_agent_dir()
        self.packages_dir = self.global_dir / "packages"
        self.git_dir = self.global_dir / "git"
        self.npm_dir = self.global_dir / "npm"
        self.setup_dirs()

    def setup_dirs(self):
        self.packages_dir.mkdir(parents=True, exist_ok=True)
        self.git_dir.mkdir(parents=True, exist_ok=True)
        self.npm_dir.mkdir(parents=True, exist_ok=True)

    async def install(self, source: str, local: bool = False):
        """
        Mirroring pi install logic.
        """
        print(f"Installing package from {source}...")
        
        if source.startswith("npm:"):
            await self._install_npm(source[4:], local)
        elif source.startswith("git:") or "github.com" in source:
            await self._install_git(source, local)
        elif source.startswith("/") or source.startswith("./"):
            await self._install_local(source, local)
        else:
            print(f"Unknown package source: {source}")

    async def _install_npm(self, pkg_spec: str, local: bool):
        # In python, we'll just shell out to npm
        cmd = ["npm", "install"]
        if not local:
            cmd.append("-g")
        cmd.append(pkg_spec)
        
        try:
            subprocess.run(cmd, check=True)
            self._update_settings(f"npm:{pkg_spec}", local)
            print(f"Successfully installed {pkg_spec} via npm")
        except subprocess.CalledProcessError as e:
            print(f"npm install failed: {e}")

    async def _install_git(self, git_url: str, local: bool):
        # Normalize git: shorthand
        clean_url = git_url.replace("git:", "")
        if not clean_url.startswith(("http", "ssh")):
            clean_url = f"https://{clean_url}"
        
        repo_name = clean_url.split("/")[-1].replace(".git", "")
        dest = (self.project_dir / ".pi" / "git" / repo_name) if local else (self.git_dir / repo_name)
        
        try:
            if dest.exists():
                subprocess.run(["git", "-C", str(dest), "pull"], check=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["git", "clone", clean_url, str(dest)], check=True)
            
            # Post-clone npm install if package.json exists
            if (dest / "package.json").exists():
                subprocess.run(["npm", "install"], cwd=str(dest), check=True)
                
            self._update_settings(git_url, local)
            print(f"Successfully installed {repo_name} from git")
        except subprocess.CalledProcessError as e:
            print(f"git operation failed: {e}")

    def _install_local(self, path: str, local: bool):
        abs_path = str(Path(path).resolve())
        self._update_settings(abs_path, local)
        print(f"Added local package path: {abs_path}")

    def _update_settings(self, source: str, local: bool):
        settings_path = (self.project_dir / ".pi" / "settings.json") if local else (self.global_dir / "settings.json")
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        
        settings = {}
        if settings_path.exists():
            with open(settings_path, "r") as f:
                settings = json.load(f)
        
        packages = settings.get("packages", [])
        if source not in packages:
            packages.append(source)
            settings["packages"] = packages
            with open(settings_path, "w") as f:
                json.dump(settings, f, indent=2)

    def list_packages(self):
        # Load from both global and local settings
        pass
