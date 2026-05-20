#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def scan_workspace(path):
    import re
    print(f"🛡️ Security: Scanning workspace {path}...")
    
    # Real regex patterns for common secrets
    patterns = [
        re.compile(r"sk-[a-zA-Z0-9]{20,}"),  # OpenAI, Anthropic, etc.
        re.compile(r"AKIA[0-9A-Z]{16}"),    # AWS Access Key
        re.compile(r"-----BEGIN RSA PRIVATE KEY-----"),
        re.compile(r"ghp_[a-zA-Z0-9]{36}")  # GitHub Personal Access Token
    ]
    
    found_secrets = []
    for root, dirs, files in os.walk(path):
        if '.git' in dirs: dirs.remove('.git') # Skip .git
        for file in files:
            file_path = Path(root) / file
            try:
                with open(file_path, "r", errors="ignore") as f:
                    content = f.read()
                    for pattern in patterns:
                        if pattern.search(content):
                            found_secrets.append(str(file_path))
                            break
            except Exception:
                pass
    
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
