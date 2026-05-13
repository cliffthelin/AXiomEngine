#!/usr/bin/env python3
import json
import time
import redis
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add current dir to path for imports
sys.path.append(str(Path(__file__).parent))

from stitch import Stitch

class SyncState:
    """
    AXIOMENGINE GLOBAL STATE SYNC (Phase 6)
    Implements a Last-Write-Wins (LWW) Register/Map for shared agent context.
    Uses Valkey (Redis) as the shared backbone.
    """
    def __init__(self, namespace: str = "axiomengine:global_state"):
        self.stitch = Stitch()
        self.client = self.stitch.client
        self.namespace = namespace

    def _get_key(self, key: str) -> str:
        return f"{self.namespace}:{key}"

    def set(self, key: str, value: Any, agent_id: str = "system"):
        """Set a value with LWW semantics."""
        if not self.client: return
        
        full_key = self._get_key(key)
        payload = {
            "value": value,
            "timestamp": time.time(),
            "agent_id": agent_id
        }
        
        # Atomically check timestamp before setting (or use a simple hash)
        # For simplicity, we'll use a HASH where field is the key
        # and value is the serialized payload.
        self.client.hset(self.namespace, key, json.dumps(payload))
        print(f"SyncState: Set '{key}' = {value} (by {agent_id})")

    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from the shared state."""
        if not self.client: return None
        
        data = self.client.hget(self.namespace, key)
        if data:
            payload = json.loads(data)
            return payload.get("value")
        return None

    def get_all(self) -> Dict[str, Any]:
        """Retrieve the entire shared state."""
        if not self.client: return {}
        
        raw_data = self.client.hgetall(self.namespace)
        state = {}
        for key, val in raw_data.items():
            payload = json.loads(val)
            state[key] = payload.get("value")
        return state

    def update(self, updates: Dict[str, Any], agent_id: str = "system"):
        """Batch update the shared state."""
        if not self.client: return
        
        # Prepare batch hash set
        pipeline = self.client.pipeline()
        for key, value in updates.items():
            payload = {
                "value": value,
                "timestamp": time.time(),
                "agent_id": agent_id
            }
            pipeline.hset(self.namespace, key, json.dumps(payload))
        pipeline.execute()
        print(f"SyncState: Batch update of {len(updates)} keys (by {agent_id})")

def test_sync():
    print("🚀 Testing Global State Sync...")
    ss = SyncState(namespace="axiomengine:test_sync")
    
    # Simulate two agents updating the same state
    ss.set("weather_api", "openweathermap", agent_id="Archon")
    ss.set("status", "planning", agent_id="Archon")
    
    time.sleep(0.1)
    ss.set("status", "executing", agent_id="Pi")
    
    # Retrieve
    state = ss.get_all()
    print(f"Shared State: {state}")
    
    assert state["status"] == "executing"
    assert state["weather_api"] == "openweathermap"
    print("✅ Sync Test Passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test_sync":
        test_sync()
    else:
        ss = SyncState()
        print("Global State Snapshot:")
        print(json.dumps(ss.get_all(), indent=2))
