#!/usr/bin/env python3
import json
import time
import redis
from typing import Optional, Any

class Stitch:
    """
    Stitch Messaging System
    Inter-agent communication via Valkey (Redis-compatible).
    """
    def __init__(self, host='127.0.0.1', port=6379):
        try:
            self.client = redis.Redis(host=host, port=port, decode_responses=True)
            self.client.ping()
        except Exception as e:
            print(f"Stitch: Failed to connect to Valkey at {host}:{port} - {e}")
            self.client = None

    def publish(self, channel: str, message: Any, sender: str = 'system'):
        """Broadcast a message to a channel."""
        if not self.client: return
        payload = {
            'sender': sender,
            'message': message,
            'timestamp': time.time()
        }
        self.client.publish(f"stitch:chan:{channel}", json.dumps(payload))

    def send_task(self, agent: str, task_name: str, data: dict, sender: str = 'system'):
        """Send a direct task to an agent's queue."""
        if not self.client: return
        payload = {
            'sender': sender,
            'task': task_name,
            'data': data,
            'timestamp': time.time()
        }
        self.client.lpush(f"stitch:tasks:{agent}", json.dumps(payload))

    def get_task(self, agent: str, timeout: int = 5) -> Optional[dict]:
        """Wait for and retrieve a task from the queue."""
        if not self.client: return None
        res = self.client.brpop(f"stitch:tasks:{agent}", timeout=timeout)
        if res:
            return json.loads(res[1])
        return None

    def set_status(self, agent: str, status: str):
        """Set agent status in the registry."""
        if not self.client: return
        self.client.hset("stitch:agent_status", agent, status)
        self.client.hset("stitch:agent_last_seen", agent, time.time())

    def get_agent_statuses(self) -> dict:
        """Get all agent statuses."""
        if not self.client: return {}
        return self.client.hgetall("stitch:agent_status")

if __name__ == "__main__":
    # Simple test
    s = Stitch()
    if s.client:
        print("Stitch connected to Valkey.")
        s.set_status("stitch_test", "online")
        print("Status set. Current statuses:", s.get_agent_statuses())
    else:
        print("Stitch test failed: No connection.")
