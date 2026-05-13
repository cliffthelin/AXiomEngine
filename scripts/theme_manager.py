#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Dict, Any, Optional
from scripts.pi_config import get_agent_dir

class Theme:
    def __init__(self, name: str, data: Dict[str, Any]):
        self.name = name
        self.vars = data.get("vars", {})
        self.colors = data.get("colors", {})
        self._resolve_colors()

    def _resolve_colors(self):
        """Resolve variables in color values."""
        for k, v in self.colors.items():
            if v in self.vars:
                self.colors[k] = self.vars[v]

class ThemeManager:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.themes: Dict[str, Theme] = {
            "dark": Theme("dark", {"colors": {"accent": "#00aaff", "border": "#333333"}}),
            "light": Theme("light", {"colors": {"accent": "#0055ff", "border": "#dddddd"}})
        }

    def discover_themes(self):
        search_paths = [
            get_agent_dir() / "themes",
            self.project_dir / ".pi" / "themes"
        ]
        for path in search_paths:
            if not path.exists(): continue
            for theme_file in path.glob("*.json"):
                self.load_theme(theme_file)

    def load_theme(self, path: Path):
        try:
            with open(path, "r") as f:
                data = json.load(f)
                name = data.get("name", path.stem)
                self.themes[name] = Theme(name, data)
        except Exception as e:
            print(f"Failed to load theme {path}: {e}")

    def get_theme(self, name: str) -> Theme:
        return self.themes.get(name, self.themes["dark"])

_manager = None
def get_theme_manager():
    global _manager
    if _manager is None:
        _manager = ThemeManager()
        _manager.discover_themes()
    return _manager
