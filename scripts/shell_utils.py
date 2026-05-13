#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

def get_bash_path() -> str:
    """
    Official PI shell detection logic.
    """
    from scripts.settings_manager import get_settings_manager
    custom = get_settings_manager().get("shellPath")
    if custom and os.path.exists(custom):
        return custom

    if sys.platform != "win32":
        return "/bin/bash"

    # 1. Custom path from settings (Placeholder: we'll check ~/.pi/agent/settings.json)
    # 2. Git Bash default location
    git_bash = Path("C:/Program Files/Git/bin/bash.exe")
    if git_bash.exists():
        return str(git_bash)

    # 3. Path search
    bash_on_path = shutil.which("bash.exe")
    if bash_on_path:
        return bash_on_path

    # Fallback
    return "bash.exe"

def get_shell_aliases() -> str:
    from scripts.pi_config import get_agent_dir
    alias_path = get_agent_dir() / "aliases"
    if alias_path.exists():
        try:
            with open(alias_path, "r") as f:
                return f.read().strip()
        except: pass
    return ""

def run_in_shell(command: str):
    """Executes a command using the detected bash shell."""
    bash = get_bash_path()
    aliases = get_shell_aliases()
    full_cmd = f"{aliases}\n{command}" if aliases else command
    # Logic to run subprocess with bash -c
    pass
