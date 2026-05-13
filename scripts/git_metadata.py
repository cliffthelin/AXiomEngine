#!/usr/bin/env python3
import subprocess
import os
import sys
from pathlib import Path

def run_git(args, cwd=None):
    try:
        res = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception as e:
        print(f"Git Error: {e}")
        return None

def auto_commit(message, project_path):
    print(f"Git: Committing changes in {project_path}...")
    run_git(["add", "."], cwd=project_path)
    # Check if there are changes
    status = run_git(["status", "--porcelain"], cwd=project_path)
    if not status:
        print("Git: No changes to commit.")
        return False
    
    run_git(["commit", "-m", message], cwd=project_path)
    print("Git: Commit successful.")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 2:
        auto_commit(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python git_metadata.py <message> <project_path>")
