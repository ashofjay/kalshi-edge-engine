from typing import Any
import httpx

class KalshiPublicClient:
    def __init__(self, base_url: str, timeout: float = 20.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    async def get_open_markets(self, limit: int = 200) -> list[dict[str, Any]]:
        params = {"status": "open", "limit": min(max(limit, 1), 1000)}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/markets", params=params)
            response.raise_for_status()
            return response.json().get("markets", [])
