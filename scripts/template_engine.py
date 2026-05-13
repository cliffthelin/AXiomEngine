#!/usr/bin/env python3
import os
import re
from pathlib import Path
from typing import Dict, List, Optional

class TemplateEngine:
    """
    Implements PI Prompt Templates.
    Loads .md templates and performs variable replacement using {{var}} syntax.
    """
    def __init__(self, template_dirs: List[str]):
        self.template_dirs = [Path(os.path.expanduser(d)) for d in template_dirs]
        self.templates: Dict[str, str] = {}

    def load_all(self):
        self.templates = {}
        for t_dir in self.template_dirs:
            if not t_dir.exists():
                continue
            self._scan_dir(t_dir)
        return self.templates

    def _scan_dir(self, directory: Path):
        for entry in directory.iterdir():
            if entry.is_dir():
                if entry.name.startswith("."): continue
                self._scan_dir(entry)
            elif entry.suffix == ".md":
                name = entry.stem
                with open(entry, "r", encoding="utf-8") as f:
                    self.templates[name] = f.read()

    def render(self, template_name: str, variables: Dict[str, str]) -> Optional[str]:
        template = self.templates.get(template_name)
        if not template:
            return None
        
        # Replace {{var}}
        rendered = template
        for key, val in variables.items():
            rendered = rendered.replace(f"{{{{{key}}}}}", val)
            
        # Clean up unmatched variables? (PI spec usually leaves them or prompts user)
        return rendered

if __name__ == "__main__":
    # Test
    engine = TemplateEngine(["./test_templates"])
    engine.templates["review"] = "Review this code: {{code}}"
    print(engine.render("review", {"code": "print('hello')"}))
