#!/usr/bin/env python3
import json
import os
from pathlib import Path

SETTINGS_FILE = Path(__file__).parent.parent / "agent_settings.json"

class SettingsRegistry:
    """Centralized configuration manager for AXiomEngine extensions."""
    
    def __init__(self):
        self.settings = self._load()

    def _load(self):
        if SETTINGS_FILE.exists():
            try:
                with open(SETTINGS_FILE, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, extension: str, key: str, default=None):
        return self.settings.get(extension, {}).get(key, default)

    def set(self, extension: str, key: str, value):
        if extension not in self.settings:
            self.settings[extension] = {}
        self.settings[extension][key] = value
        self._save()

if __name__ == "__main__":
    registry = SettingsRegistry()
    registry.set("core", "version", "1.0.0")
    print("Settings Registry Initialized.")
