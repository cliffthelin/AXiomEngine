#!/usr/bin/env python3
import asyncio
import json
import sys
import os
from pathlib import Path

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from scripts.stitch import Stitch
from scripts.agent_lib import AsyncAXiomEngineClient
from scripts.sync_state import SyncState
from scripts.ollama_controller import OllamaController

# Default model for all agents — can be overridden per-task
DEFAULT_MODEL = os.environ.get("AXIOMENGINE_MODEL", "qwen3.6:27b")

class AgentDaemon:
    def __init__(self, name: str, model: str = DEFAULT_MODEL):
        self.name = name
        self.model = model
        self.stitch = Stitch()
        self.client = AsyncAXiomEngineClient(name)
        self.sync = SyncState()
        self.ollama = OllamaController()

    async def run(self):
        print(f"[{self.name}] Daemon started. Listening for tasks...")
        while True:
            try:
                # Use get_task as implemented in stitch.py
                task_envelope = self.stitch.get_task(self.name, timeout=2)
                if task_envelope:
                    await self.handle_task(task_envelope)
            except Exception as e:
                print(f"[{self.name}] Error in loop: {e}")
            await asyncio.sleep(0.1)

    async def handle_task(self, envelope: dict):
        # Stitch.get_task returns {sender, task, data, timestamp}
        task_data = envelope.get("data", {})
        task_id = task_data.get("task_id", "unknown")
        instruction = task_data.get("instruction", "No instruction")
        task_model = task_data.get("model", self.model)  # per-task model override
        
        print(f"[{self.name}] Received Task {task_id}: {instruction[:50]}...")
        
        # Switch model if the task requests a different one
        if task_model != self.model:
            print(f"[{self.name}] Switching model: {self.model} → {task_model}")
            try:
                self.ollama.switch_model(self.model, task_model, keep_alive="-1")
                self.model = task_model
            except Exception as e:
                print(f"[{self.name}] Model switch failed: {e}, keeping {self.model}")
                task_model = self.model
        
        # Update SyncState
        self.sync.namespace = task_data.get("sync_namespace", "default")
        self.sync.set(f"task:{task_id}:status", "running", agent_id=self.name)
        
        try:
            # Ensure model is loaded
            self.ollama.ensure_model_loaded(task_model, keep_alive="-1")
            
            # Execute via OllamaController (direct Ollama API, bypasses router)
            messages = [
                {"role": "system", "content": f"You are {self.name}, an AXiomEngine agent. Execute tasks precisely."},
                {"role": "user", "content": instruction},
            ]
            
            # Use thinking for complex tasks
            use_thinking = task_data.get("think", False)
            
            result = self.ollama.chat(
                model=task_model,
                messages=messages,
                stream=False,
                think=use_thinking if use_thinking else None,
                options=task_data.get("options"),  # allow per-task runtime options
            )
            
            summary = result.get("message", {}).get("content", "")
            thinking = result.get("message", {}).get("thinking", "")
            
            # Log timing stats
            total_ns = result.get("total_duration", 0)
            eval_count = result.get("eval_count", 0)
            if total_ns > 0:
                total_s = total_ns / 1e9
                tps = eval_count / (result.get("eval_duration", 1) / 1e9) if result.get("eval_duration") else 0
                print(f"[{self.name}] Task {task_id} done in {total_s:.1f}s ({eval_count} tokens, {tps:.1f} tok/s)")
            
            self.sync.set(f"task:{task_id}:status", "completed", agent_id=self.name)
            self.sync.set(f"task:{task_id}:output", summary, agent_id=self.name)
            if thinking:
                self.sync.set(f"task:{task_id}:thinking", thinking, agent_id=self.name)
            
        except Exception as e:
            print(f"[{self.name}] Task {task_id} failed: {e}")
            self.sync.set(f"task:{task_id}:status", "failed", agent_id=self.name)
            self.sync.set(f"task:{task_id}:error", str(e), agent_id=self.name)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        agent_name = sys.argv[1]
        model = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL
        daemon = AgentDaemon(agent_name, model=model)
        asyncio.run(daemon.run())
    else:
        print("Usage: python agent_daemon.py <agent_name> [model_name]")
