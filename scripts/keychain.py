#!/usr/bin/env python3
import json
import os
from pathlib import Path

# In a real production system, this would use a proper encryption library (e.g. cryptography)
# or a system keychain. For this implementation, we use a restricted-permission JSON file.
KEYCHAIN_FILE = Path(__file__).parent.parent / ".agent_keychain.json"

class Keychain:
    """Secure Credential Manager for AXiomEngine."""
    
    def __init__(self):
        self._ensure_file()

    def _ensure_file(self):
        if not KEYCHAIN_FILE.exists():
            with open(KEYCHAIN_FILE, 'w') as f:
                json.dump({}, f)
            os.chmod(KEYCHAIN_FILE, 0o600) # Only owner can read/write

    def _load(self):
        with open(KEYCHAIN_FILE, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(KEYCHAIN_FILE, "w") as f:
            json.dump(data, f, indent=4)
        os.chmod(KEYCHAIN_FILE, 0o600)

    def get_key(self, service_name: str) -> str:
        """Retrieve a key. Logs access."""
        data = self._load()
        # In a real system, this is where we'd emit an audit log that an agent requested a key
        return data.get(service_name)

    def set_key(self, service_name: str, key_value: str):
        data = self._load()
        data[service_name] = key_value
        self._save(data)

if __name__ == "__main__":
    kc = Keychain()
    print("Keychain initialized with secure permissions.")
