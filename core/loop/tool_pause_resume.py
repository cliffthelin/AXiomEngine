import asyncio
from typing import Dict, Any, Callable
from core.transport.websocket_transport import WebSocketTransport

class ToolPauseResume:
    """
    AXIOMENGINE TOOL PAUSE/RESUME LOOP
    Orchestrates the lifecycle of a tool call within a persistent session.
    """
    def __init__(self, transport: WebSocketTransport):
        self.transport = transport
        self.tool_handler: Optional[Callable] = None

    async def handle_model_response(self, response: dict):
        """Processes model output, checking for tool calls."""
        choices = response.get("choices", [])
        if not choices:
            return response

        message = choices[0].get("message", {})
        tool_calls = message.get("tool_calls", [])

        if not tool_calls:
            return response

        print(f"Loop: Model requested {len(tool_calls)} tools. Pausing sampling...")
        
        results = []
        for call in tool_calls:
            tool_name = call.get("function", {}).get("name")
            tool_args = call.get("function", {}).get("arguments")
            
            # Emit tool request event
            if self.tool_handler:
                result = await self.tool_handler(tool_name, tool_args)
                results.append({
                    "role": "tool",
                    "tool_call_id": call.get("id"),
                    "name": tool_name,
                    "content": str(result)
                })

        # Resume by sending tool results back over the same transport
        print("Loop: Resuming with tool results...")
        await self.transport.send({"messages": results})
        return None # Signal that the turn is continuing
