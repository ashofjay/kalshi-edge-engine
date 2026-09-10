import asyncio

from .config import settings
from .db import save_signal, save_snapshot
from .kalshi_client import KalshiClient
from .strategy import find_two_leg_opportunity


class Scanner:
    def __init__(self):
        self.client = KalshiClient()

    async def scan_once(self):
        markets = await self.client.get_open_markets()
        signal_count = 0

        for market in markets:
            volume = market.get("volume") or 0

            try:
                volume = float(volume)
            except (TypeError, ValueError):
                volume = 0

            if volume < settings.min_volume:
                continue

            save_snapshot(market)

            signal = find_two_leg_opportunity(market)
            if signal:
                save_signal(signal)
                signal_count += 1

        return {
            "markets_seen": len(markets),
            "signals_found": signal_count,
        }

    async def run_forever(self):
        while True:
            try:
                result = await self.scan_once()
                print(
                    f"Scan complete: {result['markets_seen']} markets, "
                    f"{result['signals_found']} signals"
                )
            except Exception as exc:
                print(f"Scan failed: {exc}")

            await asyncio.sleep(settings.scan_interval_seconds)
