import json
from typing import Optional
from .websocket_transport import WebSocketTransport
from .http_transport import HttpTransport

class TransportSelector:
    """
    AXIOMENGINE TRANSPORT SELECTOR
    Determines the best available transport mode for the current session.
    """
    def __init__(self, ws_uri: str, http_url: str):
        self.ws = WebSocketTransport(ws_uri)
        self.http = HttpTransport(http_url)
        self.active_mode = "http"

    async def initialize(self) -> str:
        """Attempt to connect via WebSocket, fallback to HTTP."""
        success = await self.ws.connect()
        if success:
            self.active_mode = "websocket"
        else:
            self.active_mode = "http"
            print("Selector: Falling back to HTTP mode.")
        return self.active_mode

    async def send_turn(self, payload: dict, headers: dict = None):
        """Execute a single agent turn using the active transport."""
        if self.active_mode == "websocket":
            try:
                raw_res = await self.ws.send_and_wait(payload)
                res = json.loads(raw_res)
                return {**res, "mode": "websocket"}
            except Exception as e:
                print(f"Selector: WS Send failed ({e}), switching to HTTP.")
                self.active_mode = "http"
        
        # HTTP Fallback
        res = await self.http.post("/v1/chat/completions", payload, headers=headers)
        return {**res, "mode": "http"}
