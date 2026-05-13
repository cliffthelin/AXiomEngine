import asyncio
import json
import websockets
from typing import Optional, Callable

class WebSocketTransport:
    """
    AXIOMENGINE WEBSOCKET TRANSPORT
    Handles persistent, bidirectional communication with the Router.
    """
    def __init__(self, uri: str):
        self.uri = uri
        self.connection = None
        self.on_message_callback: Optional[Callable] = None

    async def connect(self):
        try:
            self.connection = await websockets.connect(self.uri)
            print(f"WS Transport: Connected to {self.uri}")
            return True
        except Exception as e:
            print(f"WS Transport: Connection failed: {e}")
            return False

    async def send(self, data: dict):
        if not self.connection:
            raise ConnectionError("Not connected")
        await self.connection.send(json.dumps(data))

    async def send_and_wait(self, data: dict, timeout: int = 120) -> dict:
        """Send data and wait for the next response on the websocket."""
        await self.send(data)
        # In a real system, we'd correlate by request_id.
        # For simplicity, we just wait for the next message.
        return await asyncio.wait_for(self.connection.recv(), timeout=timeout)

    async def listen(self):
        """Main receive loop for the websocket."""
        if not self.connection:
            return
        try:
            async for message in self.connection:
                data = json.loads(message)
                if self.on_message_callback:
                    await self.on_message_callback(data)
        except websockets.exceptions.ConnectionClosed:
            print("WS Transport: Connection closed")
        finally:
            self.connection = None

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
