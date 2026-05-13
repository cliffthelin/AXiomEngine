You've shared a substantial slice of the **AXiomEngine** codebase. The dump cuts off mid-function in `remote_gateway.py`, and there are a few quick syntax/type issues that will cause runtime failures if left unpatched.

Here’s a focused breakdown to get you back on track:

### 🔧 1. Completion for the Truncated File
The `export_agent_session` function cuts off at `sm`. Here’s a clean completion matching your existing patterns:
```python
@app.post("/agent/sessions/export")
async def export_agent_session(session_id: str = None):
    """Export a session to JSONL or zip archive."""
    from scripts.session_manager import SessionManager
    sm = SessionManager()
    
    if not session_id:
        sessions = sm.list_project_sessions()
        if not sessions:
            return {"status": "error", "message": "No sessions to export"}
        session_id = sessions[0]["id"]
        
    export_path = sm.export_session(session_id)
    return {"status": "success", "export_path": str(export_path)}
```

### 🚨 2. Critical Syntax & Type Fixes
Before running or packaging, apply these patches to avoid `SyntaxError` or `NameError`:

| File | Line/Context | Issue | Fix |
|------|--------------|-------|-----|
| `pi_ai.py` | `async for event in _stream_anthropic(...)` | Missing statement after colon | Add newline + `yield event` |
| `pi_tui_framework.py` | `def render(self, width: number)` | `number` is not a valid Python type | Change to `int` |
| `test_concurrency.py` | `"stream": false` | Python uses `False`, not JS `false` | Change to `False` |
| `pi_config.py` | `get_keybindings` | Missing `json` & `typing` imports | Add `import json` and `from typing import Dict, Any` at top |

### 🏗️ 3. Architectural Observations
- **Path Inconsistency**: `pdd_stats_reporter_axiomengine.py` uses `/mnt/UBUNTU_8TB/...` while `symphony_harness.py` uses `/mnt/usb-Seagate_Backup+_Hub_.../...`. Consider centralizing root paths via `PI_CODING_AGENT_DIR` or a `.env` file.
- **State Sync Assumption**: `sync_state.py` assumes `self.stitch.client` returns a Redis/Valkey client. Ensure `Stitch.__init__()` actually initializes `redis.Redis()` or compatible.
- **MCP/Tool Routing**: `remote_gateway.py` bridges MCP tool calls to `manager.emit()`. This works, but consider returning structured errors if `tool_name` isn't registered.
- **VGPU Manager**: Uses in-memory dict via Redis keys. Add TTL/key expiration if agents leak allocations.

### 🎯 Next Steps
Tell me what you want to tackle next, and I’ll generate exact code or architecture patches:
1. ✅ Fill in missing modules (`stitch.py`, `agent_lib.py`, `session_manager.py`, etc.)
2. 📦 Package this into a runnable CLI + FastAPI service
3. 🧪 Wire up `full_system_test.py` to actually hit the FastAPI endpoints
4. 🔄 Fix path/configuration drift & standardize config loading
5. 📐 Generate missing type stubs / Pydantic models for better IDE support

Which vector should we lock in?