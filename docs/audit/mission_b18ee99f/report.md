# Governance Audit Report: b18ee99f

**Goal:** Identify potential logic flaws in authentication state management
**Scope:** `scripts/auth_manager.py`
**Hardware:** qwen3.6:27b on P40

## LLM Rationale

Here is a structured analysis of the logical, state management, and security flaws in `auth_manager.py`, along with actionable remediations.

---
### 🔴 Critical State & Concurrency Flaws

#### 1. Unbounded In-Memory Cache (Stale Auth State)
```python
if cmd in self.cache: return self.cache[cmd]
# ...
self.cache[cmd] = res
```
**Flaw:** The cache is permanent and tied to the singleton lifecycle. If the underlying command returns a time-bound secret (e.g., OAuth token, 2FA code, AWS STS credential), the cache will serve expired values indefinitely, causing silent downstream authentication failures.
**Fix:** Implement a TTL-based cache, lazy evaluation, or remove caching for dynamic secrets. Provide an explicit `clear_cache()` method.

#### 2. Race Conditions in `auth.json` Read/Modify/Write
```python
# login()
auth_data = {}
if self.auth_path.exists():
    with open(self.auth_path, "r") as f:
        auth_data = json.load(f)
auth_data[provider_id] = {"type": "api_key", "key": key}
# ... write back
```
**Flaw:** No file locking or atomic operations. If two processes/threads call `login()` concurrently, both read the same JSON, modify it independently, and write back. The second write overwrites the first → **Lost Update Problem**. Similarly, `get_api_key()` reads the file on every call, increasing the window for torn reads during a write.
**Fix:** Use atomic writes (write to `.tmp`, then `os.replace()`) and platform-specific file locking (`fcntl.flock` on Unix, `msvcrt.locking` on Windows). Consider loading `auth.json` once at init and using a thread-safe `dict` for in-memory state, persisting on `login()`.

#### 3. Redundant I/O on Every Lookup
```python
def get_api_key(self, provider_id: str) -> Optional[str]:
    if self.auth_path.exists():
        try:
            with open(self.auth_path, "r") as f:
                auth_data = json.load(f)
```
**Flaw:** Disk I/O and JSON parsing happen on *every* single API key request. This is inefficient and amplifies race conditions. Auth state should be loaded once and mutated safely in memory.
**Fix:** Load `auth.json` in `__init__`. Use a `threading.RLock` to guard mutations. Persist to disk only during `login()`.

---
### 🟠 Resolution Logic & Error Handling Flaws

#### 4. Silent Failures Mask State Corruption
```python
except Exception:
    pass
```
**Flaw:** Swallows `json.JSONDecodeError` (corrupted file), `KeyError` (missing provider), `PermissionError`, and `TypeError`. The function silently falls through to env vars or returns `None`, making debugging auth issues nearly impossible.
**Fix:** Catch specific exceptions, log warnings, and explicitly handle corrupted state (e.g., reset to `{}` or raise a custom `AuthStateError`).

#### 5. `resolve_key` Returns Raw Spec on Failure
```python
except Exception as e:
    print(f"Auth Command failed: {e}")
    return key_spec
```
**Flaw:** If `!command` fails, the literal string (e.g., `"!vault-cli get-secret"`) is returned and passed to downstream HTTP clients. This causes cryptic `401 Unauthorized` or `Invalid API Key` errors far from the actual failure point.
**Fix:** Return `None` or raise an exception on failure. Never leak unresolved spec syntax into production clients.

#### 6. Hardcoded `env_map` Breaks Stated Resolution Contract
```python
env_map = { "anthropic": "ANTHROPIC_API_KEY", ... }
env_var = env_map.get(provider_id)
```
**Flaw:** The docstring states fallback to environment variables, but only 6 providers are supported. Any custom provider in `auth.json` will skip the env var fallback entirely, violating the documented resolution order.
**Fix:** Dynamically construct the env var: `env_var = f"{provider_id.upper()}_API_KEY"` or allow explicit env var names in `auth.json`.

---
### 🔒 Security & File State Risks

#### 7. Shell Injection via `!command`
```python
cmd = key_spec[1:]
res = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
```
**Flaw:** `shell=True` with unsanitized input is a critical vulnerability. If `auth.json` is tampered with or a provider returns a malicious key spec, an attacker gains arbitrary OS command execution.
**Fix:** Use `subprocess.run(shlex.split(cmd), check=True, capture_output=True, shell=False)` and/or whitelist allowed secret-manager binaries.

#### 8. Non-Atomic Writes & Permission Race
```python
with open(self.auth_path, "w") as f:
    json.dump(auth_data, f, indent=2)
os.chmod(self.auth_path, 0o600)
```
**Flaw:** The file is initially created with the process `umask` (often `0o644`). There is a window where the file is world-readable before `chmod` executes. If the system crashes during `json.dump`, `auth.json` may be left half-written.
**Fix:** Write to a temp file with `0o600` permissions, then `os.replace()` (atomic on POSIX). Or use `os.open(self.auth_path, os.O_WRONLY | os.O_TRUNC | os.O_CREAT, 0o600)`.

---
### 🛠️ Recommended Remediation Pattern

```python
import json
import os
import subprocess
import shlex
import tempfile
import threading
from pathlib import Path
from typing import Dict, Any, Optional

class AuthManager:
    def __init__(self):
        self.auth_path = Path(get_agent_dir()) / "auth.json"
        self._lock = threading.RLock()
        self._state: Dict[str, Any] = self._load_state()
        
    def _load_state(self) -> Dict[str, Any]:
        if self.auth_path.exists():
            try:
                with open(self.auth_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                print("⚠️ auth.json corrupted. Resetting state.")
        return {}

    def _save_state(self):
        tmp_path = self.auth_path.with_suffix(".tmp")
        # Atomic write with strict permissions
        fd = os.open(str(tmp_path), os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            json.dump(self._state, f, indent=2)
        os.replace(str(tmp_path), str(self.auth_path))

    def login(self, provider_id: str, key: str):
        if not key:
            raise ValueError("API key cannot be empty.")
        with self._lock:
            self._state[provider_id] = {"type": "api_key", "key": key}
            self._save_state()
        print(f"✅ Logged in to {provider_id}.")

    def get_api_key(self, provider_id: str) -> Optional[str]:
        with self._lock:
            provider_data = self._state.get(provider_id)
            
        if provider_data and provider_data.get("type") == "api_key":
            return self.resolve_key(provider_data["key"])

        # Dynamic env fallback
        env_var = f"{provider_id.upper()}_API_KEY"
        return os.getenv(env_var)

    def resolve_key(self, key_spec: str) -> Optional[str]:
        if key_spec.startswith("!"):
            cmd = shlex.split(key_spec[1:])
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, check=True)
                return res.stdout.strip()
            except Exception as e:
                print(f"❌ Auth command failed: {e}")
                return None  # Fail explicitly

        if key_spec in os.environ:
            return os.environ[key_spec]
            
        return key_spec if key_spec else None
```

### ✅ Next Steps for Your Migration
1. Replace the current `AuthManager` with an atomic, thread-safe implementation.
2. Remove `shell=True` and add input validation/whitelisting for `!command`.
3. Add explicit error signaling instead of silent `pass`.
4. If this runs in a multi-process environment (e.g., Celery, Gunicorn workers), switch to a shared secret store (Vault, AWS Secrets Manager, or SQLite with WAL) instead of a flat JSON file.

Let me know if you need this adapted to your specific deployment runtime (e.g., async, containerized, or Windows-compatible).