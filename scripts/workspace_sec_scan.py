#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def scan_workspace(path):
    print(f"🛡️ Security: Scanning workspace {path}...")
    # Simulate a security scan (e.g., checking for exposed secrets)
    # In a real system, you'd run bandit -r . or similar.
    found_secrets = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith((".env", ".json", ".py")):
                with open(Path(root) / file, "r", errors="ignore") as f:
                    content = f.read()
                    if "sk-" in content or "API_KEY" in content:
                        found_secrets.append(file)
    
    if found_secrets:
        print(f"⚠️ Security Warning: Possible secrets found in {found_secrets}")
        return False
    
    print("✅ Security: Scan passed.")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        success = scan_workspace(sys.argv[1])
        sys.exit(0 if success else 1)
    else:
        print("Usage: python workspace_sec_scan.py <path>")
