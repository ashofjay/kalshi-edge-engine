import httpx

from .config import settings


class KalshiClient:
    def __init__(self):
        self.base_url = settings.kalshi_base_url.rstrip("/")

    async def get_open_markets(self):
        params = {
            "status": "open",
            "limit": settings.market_limit,
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/markets",
                params=params,
            )
            response.raise_for_status()
            data = response.json()

        return data.get("markets", [])
