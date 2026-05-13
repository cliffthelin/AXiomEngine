#!/usr/bin/env python3
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from scripts.pi_config import get_agent_dir

class SettingsManager:
    def __init__(self, project_dir: str = "."):
        self.global_path = get_agent_dir() / "settings.json"
        self.project_path = Path(project_dir) / ".pi" / "settings.json"
        self.settings: Dict[str, Any] = self._load_and_merge()

    def _load_and_merge(self) -> Dict[str, Any]:
        global_settings = self._load_file(self.global_path)
        project_settings = self._load_file(self.project_path)
        return self._deep_merge(global_settings, project_settings)

    def _load_file(self, path: Path) -> Dict[str, Any]:
        if not path.exists(): return {}
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load settings from {path}: {e}")
            return {}

    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        result = base.copy()
        for k, v in override.items():
            if k in result and isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = self._deep_merge(result[k], v)
            else:
                result[k] = v
        return result

    def get(self, key: str, default: Any = None) -> Any:
        parts = key.split(".")
        val = self.settings
        for part in parts:
            if isinstance(val, dict) and part in val:
                val = val[part]
            else:
                return default
        return val

    def set(self, key: str, value: Any, local: bool = False):
        path = self.project_path if local else self.global_path
        path.parent.mkdir(parents=True, exist_ok=True)
        
        current = self._load_file(path)
        # Simplified: handle nested sets if needed
        current[key] = value
        
        with open(path, "w") as f:
            json.dump(current, f, indent=2)
        self.settings = self._load_and_merge()

_manager = None
def get_settings_manager():
    global _manager
    if _manager is None:
        _manager = SettingsManager()
    return _manager
