#!/usr/bin/env python3
"""
MCP (Model Context Protocol) Bridge
===================================
Standardizes tool discovery and execution for AXiomEngine.
Bridges Archon's logic to Ollama's native tool-calling JSON API over the Stitch messaging bus.
"""

import sys
import os
import json
import inspect
import asyncio
import traceback
from typing import Callable, Dict, Any, List
from pathlib import Path

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from scripts.stitch import Stitch
from scripts.sync_state import SyncState
from scripts.ollama_controller import OllamaController

class MCPBridge:
    def __init__(self, name: str = "mcp_bridge"):
        self.name = name
        self.stitch = Stitch()
        self.sync = SyncState()
        self.ollama = OllamaController()
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: List[Dict[str, Any]] = []

    def register_tool(self, func: Callable):
        """
        Registers a Python function as an MCP tool.
        Auto-generates the JSON schema required by Ollama/OpenAI tool calling.
        """
        name = func.__name__
        self.tools[name] = func
        
        # Build the JSON Schema for the tool based on its docstring and type hints
        sig = inspect.signature(func)
        doc = inspect.getdoc(func) or "No description provided."
        
        properties = {}
        required = []
        
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
                
            param_type = "string"  # Default
            if param.annotation == int:
                param_type = "integer"
            elif param.annotation == float:
                param_type = "number"
            elif param.annotation == bool:
                param_type = "boolean"
            elif param.annotation == list or param.annotation == List:
                param_type = "array"
            elif param.annotation == dict or param.annotation == Dict:
                param_type = "object"
                
            properties[param_name] = {
                "type": param_type,
                "description": f"Parameter {param_name}"
            }
            
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
                
        schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": doc,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }
        
        self.tool_schemas.append(schema)
        print(f"[{self.name}] Registered tool: {name}")

    def execute_tool(self, tool_name: str, kwargs: dict) -> Any:
        """Executes a registered tool safely."""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found."
            
        try:
            print(f"[{self.name}] Executing {tool_name}({kwargs})...")
            result = self.tools[tool_name](**kwargs)
            return result
        except Exception as e:
            err = traceback.format_exc()
            print(f"[{self.name}] Tool {tool_name} failed: {e}")
            return f"Error executing {tool_name}: {err}"

    async def run(self):
        print(f"[{self.name}] MCP Bridge active. Listening for tool execution requests...")
        while True:
            try:
                # Listen for tool execution tasks targeting the MCP bridge
                task_envelope = self.stitch.get_task(self.name, timeout=2)
                if task_envelope:
                    await self.handle_task(task_envelope)
            except Exception as e:
                print(f"[{self.name}] Error in loop: {e}")
            await asyncio.sleep(0.1)

    async def handle_task(self, envelope: dict):
        """
        Handles requests from Archon or other agents that need to use tools.
        """
        task_data = envelope.get("data", {})
        task_id = task_data.get("task_id", "unknown")
        action = task_data.get("action")
        sender = envelope.get("sender", "unknown")
        
        print(f"[{self.name}] Received Request {task_id} from {sender}: {action}")
        self.sync.set(f"mcp:{task_id}:status", "running", agent_id=self.name)
        
        try:
            if action == "get_schemas":
                # Agent is requesting what tools are available
                self.sync.set(f"mcp:{task_id}:schemas", json.dumps(self.tool_schemas), agent_id=self.name)
                self.sync.set(f"mcp:{task_id}:status", "completed", agent_id=self.name)
                
            elif action == "execute":
                # Agent is requesting to execute a specific tool
                tool_name = task_data.get("tool_name")
                tool_args = task_data.get("tool_args", {})
                
                # --- EXTENSION EVENT BUS ---
                from scripts.extension_manager import get_manager
                mgr = get_manager()
                event_data = {
                    "toolName": tool_name,
                    "input": tool_args
                }
                modifiers = await mgr.emit("tool_call", event_data)
                
                if modifiers.get("block", False):
                    reason = modifiers.get("reason", "Blocked by extension")
                    result = f"Error: {reason}"
                else:
                    result = self.execute_tool(tool_name, tool_args)
                
                # Format as an MCP response
                mcp_response = {
                    "role": "tool",
                    "content": str(result),
                    "name": tool_name
                }
                
                self.sync.set(f"mcp:{task_id}:result", json.dumps(mcp_response), agent_id=self.name)
                self.sync.set(f"mcp:{task_id}:status", "completed", agent_id=self.name)
                
            else:
                self.sync.set(f"mcp:{task_id}:status", "failed", agent_id=self.name)
                self.sync.set(f"mcp:{task_id}:error", f"Unknown action: {action}", agent_id=self.name)
                
        except Exception as e:
            print(f"[{self.name}] Task {task_id} failed: {e}")
            self.sync.set(f"mcp:{task_id}:status", "failed", agent_id=self.name)
            self.sync.set(f"mcp:{task_id}:error", str(e), agent_id=self.name)


# ---------------------------------------------------------------------------
# Example Native Tools Registry
# ---------------------------------------------------------------------------

def read_workspace_file(filepath: str) -> str:
    """Reads the contents of a file from the workspace directory."""
    workspace_root = "/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects"
    full_path = os.path.join(workspace_root, filepath.lstrip('/'))
    
    # Security check to prevent directory traversal
    if not os.path.abspath(full_path).startswith(workspace_root):
        return "Error: Access denied. Path is outside the workspace."
        
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def list_workspace_dir(directory: str = "") -> list:
    """Lists files and directories in the workspace."""
    workspace_root = "/mnt/usb-Seagate_Backup+_Hub_BK_NA9R7TTV-0:0-part2/Projects"
    full_path = os.path.join(workspace_root, directory.lstrip('/'))
    
    if not os.path.abspath(full_path).startswith(workspace_root):
        return ["Error: Access denied. Path is outside the workspace."]
        
    try:
        return os.listdir(full_path)
    except Exception as e:
        return [f"Error listing directory: {str(e)}"]

def get_system_time(timezone: str = "UTC") -> str:
    """Gets the current system time."""
    from datetime import datetime
    return f"Current time ({timezone}): {datetime.now().isoformat()}"


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    bridge = MCPBridge()
    
    # Register core standard tools
    bridge.register_tool(read_workspace_file)
    bridge.register_tool(list_workspace_dir)
    bridge.register_tool(get_system_time)
    
    asyncio.run(bridge.run())
