#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def get_config_dir():
    """Mirroring PI's configDir resolution."""
    env_dir = os.getenv("PI_CODING_AGENT_DIR")
    if env_dir: return Path(env_dir).expanduser()
    return Path.home() / ".pi"

def get_agent_dir():
    return get_config_dir() / "agent"

def is_offline() -> bool:
    return os.getenv("PI_OFFLINE") in ["1", "true", "yes"]

def skip_version_check() -> bool:
    return os.getenv("PI_SKIP_VERSION_CHECK") in ["1", "true", "yes"] or is_offline()

def get_cache_retention() -> str:
    return os.getenv("PI_CACHE_RETENTION", "default")

def get_debug_log_path():
    return get_agent_dir() / "pi-debug.log"

def setup_dirs():
    get_agent_dir().mkdir(parents=True, exist_ok=True)

def debug_log(message: str):
    """Hidden /debug command backend."""
    with open(get_debug_log_path(), "a") as f:
        f.write(f"[{os.getpid()}] {message}\n")

def get_keybindings() -> Dict[str, Any]:
    """Load user keybindings from ~/.pi/agent/keybindings.json."""
    kb_path = get_agent_dir() / "keybindings.json"
    defaults = {
        "tui.editor.cursorUp": ["up", "ctrl+p"],
        "tui.editor.cursorDown": ["down", "ctrl+n"],
        "tui.submit": ["enter"],
        "tui.cancel": ["ctrl+c"]
    }
    if kb_path.exists():
        try:
            with open(kb_path, "r") as f:
                user_kb = json.load(f)
                defaults.update(user_kb)
        except Exception:
            pass
    return defaults
