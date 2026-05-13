#!/usr/bin/env python3
import os
from pathlib import Path
from typing import List, Optional

class ContextLoader:
    """
    Implements PI Context File Discovery.
    Loads AGENTS.md, CLAUDE.md, and SYSTEM.md from global and local paths.
    """
    def __init__(self, cwd: str, agent_dir: str = "~/.pi/agent"):
        self.cwd = Path(cwd).resolve()
        self.agent_dir = Path(os.path.expanduser(agent_dir)).resolve()

    def get_context_files(self) -> List[Path]:
        """Finds all AGENTS.md / CLAUDE.md files in the hierarchy."""
        files = []
        
        # 1. Global config
        global_agents = self.agent_dir / "AGENTS.md"
        if global_agents.exists():
            files.append(global_agents)
            
        # 2. Walk up from CWD
        current = self.cwd
        while True:
            for name in ["AGENTS.md", "CLAUDE.md"]:
                p = current / name
                if p.exists() and p not in files:
                    files.append(p)
            
            if current == current.parent:
                break
            current = current.parent
            
        return files

    def get_system_prompt(self) -> str:
        """Loads and concatenates the system prompt hierarchy."""
        # 1. Find SYSTEM.md or APPEND_SYSTEM.md
        prompt = ""
        
        # Base system prompt from global or local
        system_md = self.cwd / ".pi" / "SYSTEM.md"
        if not system_md.exists():
            system_md = self.agent_dir / "SYSTEM.md"
            
        if system_md.exists():
            with open(system_md, "r") as f:
                prompt = f.read()
        
        # Append logic
        append_md = self.cwd / ".pi" / "APPEND_SYSTEM.md"
        if append_md.exists():
            with open(append_md, "r") as f:
                prompt += "\n\n" + f.read()
                
        return prompt

    def load_context_text(self) -> str:
        """Concatenates all AGENTS.md content."""
        files = self.get_context_files()
        content = []
        for f in files:
            with open(f, "r") as handle:
                content.append(f"--- Context from {f} ---\n" + handle.read())
        return "\n\n".join(content)

if __name__ == "__main__":
    loader = ContextLoader(os.getcwd())
    print(f"System Prompt Length: {len(loader.get_system_prompt())}")
    print(f"Context Files Found: {len(loader.get_context_files())}")
    print(loader.load_context_text())
