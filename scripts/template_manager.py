#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml
from scripts.pi_config import get_agent_dir

class PromptTemplate:
    def __init__(self, name: str, content: str, description: str = "", arg_hint: str = ""):
        self.name = name
        self.content = content
        self.description = description
        self.arg_hint = arg_hint

    def expand(self, args: List[str]) -> str:
        """
        Mirroring PI expansion logic: $1, $@, etc.
        """
        full_args = " ".join(args)
        expanded = self.content
        
        # Replace $@ or $ARGUMENTS
        expanded = expanded.replace("$@", full_args)
        expanded = expanded.replace("$ARGUMENTS", full_args)
        
        # Replace $1, $2, ...
        for i, val in enumerate(args, 1):
            expanded = expanded.replace(f"${i}", val)
            
        return expanded

class TemplateManager:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.templates: Dict[str, PromptTemplate] = {}

    def discover_templates(self):
        search_paths = [
            get_agent_dir() / "prompts",
            self.project_dir / ".pi" / "prompts"
        ]
        
        # Also check packages (simplified: check git/ for now)
        git_global = get_agent_dir() / "git"
        if git_global.exists():
            for pkg_dir in git_global.iterdir():
                if pkg_dir.is_dir():
                    search_paths.append(pkg_dir / "prompts")

        for path in search_paths:
            if not path.exists(): continue
            for md_file in path.glob("*.md"):
                self.load_template(md_file)

    def load_template(self, path: Path):
        try:
            with open(path, "r") as f:
                raw = f.read()
            
            # Parse Frontmatter
            frontmatter = {}
            content = raw
            if raw.startswith("---"):
                parts = raw.split("---", 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1]) or {}
                        content = parts[2].strip()
                    except:
                        pass
            
            name = path.stem
            self.templates[name] = PromptTemplate(
                name=name,
                content=content,
                description=frontmatter.get("description", content.split("\n")[0]),
                arg_hint=frontmatter.get("argument-hint", "")
            )
        except Exception as e:
            print(f"Failed to load template {path}: {e}")

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        return self.templates.get(name)

_manager = None
def get_template_manager():
    global _manager
    if _manager is None:
        _manager = TemplateManager()
        _manager.discover_templates()
    return _manager
