#!/usr/bin/env python3
import sys
import json
import asyncio
from typing import Dict, Any, Optional

class RPCHandler:
    def __init__(self, pi_instance):
        self.pi = pi_instance
        self.running = True

    async def run_loop(self):
        """
        Mirroring the PI RPC protocol: JSONL over stdin/stdout.
        """
        print(json.dumps({"type": "session_start", "status": "online"}), flush=True)
        
        while self.running:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line: break
            
            try:
                cmd = json.loads(line.strip())
                req_id = cmd.get("id")
                cmd_type = cmd.get("type")
                
                res = await self.handle_command(cmd)
                
                # Send response
                response = {
                    "type": "response",
                    "command": cmd_type,
                    "success": res.get("success", True),
                    "data": res.get("data")
                }
                if req_id: response["id"] = req_id
                print(json.dumps(response), flush=True)
                
            except Exception as e:
                print(json.dumps({"type": "error", "message": str(e)}), flush=True)

    async def handle_command(self, cmd: Dict[str, Any]) -> Dict[str, Any]:
        ctype = cmd.get("type")
        
        if ctype == "prompt":
            msg = cmd.get("message")
            # Run prompt asynchronously (events stream to stdout)
            asyncio.create_task(self._run_prompt(msg))
            return {"success": True}
            
        elif ctype == "get_state":
            state = self.pi.agent.state
            return {
                "success": True,
                "data": {
                    "sessionId": state.session_id,
                    "model": state.model,
                    "messageCount": len(state.messages),
                    "isStreaming": state.is_streaming
                }
            }
            
        elif ctype == "set_model":
            model_id = f"{cmd.get('provider')}/{cmd.get('modelId')}"
            self.pi.agent.state.model = model_id
            return {"success": True, "data": {"model": model_id}}

        elif ctype == "abort":
            self.pi.agent.state.is_streaming = False
            return {"success": True}

        return {"success": False, "error": f"Unknown command: {ctype}"}

    async def _run_prompt(self, text: str):
        async for event in self.pi.agent.prompt(text):
            print(event.json(), flush=True)
