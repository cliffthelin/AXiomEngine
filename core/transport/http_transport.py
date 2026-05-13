import httpx
from typing import Dict, Any

class HttpTransport:
    """
    AXIOMENGINE HTTP TRANSPORT (Fallback)
    Standard stateless request/response communication.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def post(self, endpoint: str, data: dict, headers: dict = None) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=120.0) as client:
            url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            response = await client.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
