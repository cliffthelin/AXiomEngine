#!/usr/bin/env python3
import json
from typing import AsyncGenerator, Dict, Any, List

class FauxProvider:
    def __init__(self):
        self.responses: Dict[str, str] = {}
        self.call_history: List[str] = []

    def set_response(self, prompt: str, response: str):
        self.responses[prompt] = response

    async def stream(self, prompt: str, **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        self.call_history.append(prompt)
        content = self.responses.get(prompt, "Faux response for: " + prompt)
        
        # Simulate thinking
        yield {"type": "thinking_delta", "thinking": "Thinking..."}
        
        # Simulate text deltas
        for char in content:
            yield {"type": "text_delta", "delta": char}
        
        yield {"type": "turn_end"}
