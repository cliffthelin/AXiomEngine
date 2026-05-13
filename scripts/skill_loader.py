#!/usr/bin/env python3
import os
import yaml
import re
from pathlib import Path
from typing import List, Dict, Optional

class Skill:
    def __init__(self, name: str, description: str, file_path: str, disable_model_invocation: bool = False):
        self.name = name
        self.description = description
        self.file_path = file_path
        self.disable_model_invocation = disable_model_invocation

class SkillLoader:
    """
    Python port of the PI Skills System.
    Loads .md skill files with YAML frontmatter.
    """
    def __init__(self, skills_dirs: List[str]):
        self.skills_dirs = [Path(d) for d in skills_dirs]
        self.skills: Dict[str, Skill] = {}

    def load_all(self):
        self.skills = {}
        for s_dir in self.skills_dirs:
            if not s_dir.exists():
                continue
            self._scan_dir(s_dir)
        return self.skills

    def _scan_dir(self, directory: Path):
        # Discovery rules:
        # - if a directory contains SKILL.md, treat it as a skill root
        # - otherwise, load direct .md children
        
        skill_md = directory / "SKILL.md"
        if skill_md.exists():
            self._load_skill_file(skill_md)
            return

        for entry in directory.iterdir():
            if entry.is_dir():
                if entry.name.startswith("."): continue
                self._scan_dir(entry)
            elif entry.suffix == ".md":
                self._load_skill_file(entry)

    def _load_skill_file(self, file_path: Path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Extract frontmatter
            match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
            if not match:
                return

            frontmatter = yaml.safe_load(match.group(1))
            if not frontmatter or not isinstance(frontmatter, dict):
                return

            name = frontmatter.get("name") or file_path.parent.name
            description = frontmatter.get("description")
            
            if not description:
                return

            # Validation (subset of PI spec)
            if not re.match(r"^[a-z0-9-]+$", name):
                return

            skill = Skill(
                name=name,
                description=description,
                file_path=str(file_path),
                disable_model_invocation=frontmatter.get("disable-model-invocation", False)
            )
            self.skills[name] = skill
        except Exception as e:
            print(f"Error loading skill {file_path}: {e}")

    def format_for_prompt(self) -> str:
        visible_skills = [s for s in self.skills.values() if not s.disable_model_invocation]
        if not visible_skills:
            return ""

        lines = [
            "\n\nThe following skills provide specialized instructions for specific tasks.",
            "Use the read tool to load a skill's file when the task matches its description.",
            "",
            "<available_skills>"
        ]
        
        for skill in visible_skills:
            lines.append("  <skill>")
            lines.append(f"    <name>{skill.name}</name>")
            lines.append(f"    <description>{skill.description}</description>")
            lines.append(f"    <location>{skill.file_path}</location>")
            lines.append("  </skill>")
            
        lines.append("</available_skills>")
        return "\n".join(lines)

if __name__ == "__main__":
    # Test
    import sys
    root = Path(__file__).parent.parent
    loader = SkillLoader([str(root / "skills")])
    skills = loader.load_all()
    print(f"Loaded {len(skills)} skills.")
    print(loader.format_for_prompt())
