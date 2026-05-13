#!/usr/bin/env python3
import os
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from scripts.pi_config import get_agent_dir

class Skill:
    def __init__(self, name: str, description: str, path: Path, content: str):
        self.name = name
        self.description = description
        self.path = path
        self.content = content

class SkillManager:
    def __init__(self, project_dir: str = "."):
        self.project_dir = Path(project_dir)
        self.skills: Dict[str, Skill] = {}

    def discover_skills(self):
        search_paths = [
            get_agent_dir() / "skills",
            self.project_dir / ".pi" / "skills"
        ]
        
        # Add packages (simplified: check git/ for now)
        git_global = get_agent_dir() / "git"
        if git_global.exists():
            for pkg_dir in git_global.iterdir():
                if pkg_dir.is_dir():
                    search_paths.append(pkg_dir / "skills")

        for path in search_paths:
            if not path.exists(): continue
            # Recursive search for SKILL.md
            for skill_file in path.rglob("SKILL.md"):
                self.load_skill(skill_file)

    def load_skill(self, path: Path):
        try:
            with open(path, "r") as f:
                raw = f.read()
            
            # Parse Frontmatter
            if not raw.startswith("---"): return
            parts = raw.split("---", 2)
            if len(parts) < 3: return
            
            frontmatter = yaml.safe_load(parts[1]) or {}
            name = frontmatter.get("name")
            description = frontmatter.get("description")
            disable_invocation = frontmatter.get("disable-model-invocation", False)
            
            # Validation: Missing description skips load
            if not description:
                print(f"Skill {path} missing description, skipping.")
                return

            # Validation: Name mismatch warning
            if name != path.parent.name:
                print(f"Warning: Skill name '{name}' does not match directory '{path.parent.name}'")

            self.skills[name] = Skill(
                name=name,
                description=description,
                path=path.parent,
                content=parts[2].strip()
            )
            self.skills[name].disable_invocation = disable_invocation
        except Exception as e:
            print(f"Failed to load skill {path}: {e}")

    def get_skill_registry_xml(self) -> str:
        """Standardized PI Skill Registry XML."""
        visible_skills = {k: v for k, v in self.skills.items() if not getattr(v, 'disable_invocation', False)}
        if not visible_skills: return ""
        xml = "<available_skills>\n"
        for name, skill in visible_skills.items():
            xml += f'  <skill name="{name}">\n'
            xml += f"    <description>{skill.description}</description>\n"
            xml += "  </skill>\n"
        xml += "</available_skills>"
        return xml

_manager = None
def get_skill_manager():
    global _manager
    if _manager is None:
        _manager = SkillManager()
        _manager.discover_skills()
    return _manager
