#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import shlex
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
from scripts.pi_config import get_agent_dir

CREDENTIALS_MODE = 0o600

class AuthManager:
    def __init__(self):
        self.auth_path = get_agent_dir() / "auth.json"
        self.cache: Dict[str, str] = {}

    def get_api_key(self, provider_id: str) -> Optional[str]:
        """
        Resolution Order:
        1. auth.json entry
        2. Environment variable
        """
        # 1. Check auth.json
        if self.auth_path.exists():
            try:
                with open(self.auth_path, "r") as f:
                    auth_data = json.load(f)
                    provider_data = auth_data.get(provider_id)
                    if provider_data and provider_data.get("type") == "api_key":
                        return self.resolve_key(provider_data["key"])
            except (json.JSONDecodeError, PermissionError) as e:
                print(f"Auth: Error reading credentials: {e}")
            except Exception as e:
                print(f"Auth: Unexpected error: {e}")

        # 2. Check Environment Variables
        env_map = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "google": "GEMINI_API_KEY",
            "mistral": "MISTRAL_API_KEY",
            "groq": "GROQ_API_KEY"
        }
        env_var = env_map.get(provider_id)
        if env_var and os.getenv(env_var):
            return os.getenv(env_var)

        return None

    def resolve_key(self, key_spec: str) -> str:
        """
        Mirroring PI key resolution logic:
        - "!command" -> execute and use stdout
        - "VAR_NAME" -> use environment variable
        - Literal value
        """
        if key_spec.startswith("!"):
            cmd = key_spec[1:]
            if cmd in self.cache: return self.cache[cmd]
            try:
                # CWE-78 Fix: Avoid shell=True, use shlex.split for safe arguments
                args = shlex.split(cmd)
                res = subprocess.check_output(args, shell=False, timeout=10).decode("utf-8").strip()
                self.cache[cmd] = res
                return res
            except Exception as e:
                print(f"Auth: Command resolution failed for '{cmd}': {e}")
                return key_spec
        
        if key_spec in os.environ:
            return os.environ[key_spec]
            
        return key_spec

    def login(self, provider_id: str, key: str):
        """Store key in auth.json using an atomic write pattern."""
        auth_data = {}
        if self.auth_path.exists():
            try:
                with open(self.auth_path, "r") as f:
                    auth_data = json.load(f)
            except json.JSONDecodeError:
                print(f"Auth: auth.json was corrupted. Resetting for {provider_id}.")

        auth_data[provider_id] = {"type": "api_key", "key": key}
        self.auth_path.parent.mkdir(parents=True, exist_ok=True)

        # Atomic Write Pattern: Write to temp, then rename
        with tempfile.NamedTemporaryFile('w', dir=self.auth_path.parent, delete=False) as tf:
            json.dump(auth_data, tf, indent=2)
            tempname = tf.name

        try:
            os.chmod(tempname, CREDENTIALS_MODE)
            os.replace(tempname, self.auth_path)
            print(f"Logged in to {provider_id}. Credentials saved to {self.auth_path}")
        except Exception as e:
            if os.path.exists(tempname):
                os.unlink(tempname)
            print(f"Auth: Failed to save credentials: {e}")

_manager = None
def get_auth_manager():
    global _manager
    if _manager is None:
        _manager = AuthManager()
    return _manager
