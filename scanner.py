import asyncio
from datetime import datetime, timezone
from .config import settings
from .kalshi_client import KalshiPublicClient
from .strategy import normalize_market, detect_two_leg_candidate
from .db import insert_snapshot, insert_signal

client = KalshiPublicClient(settings.kalshi_base_url)

async def scan_once() -> dict:
    raw_markets = await client.get_open_markets(settings.market_limit)
    captured_at = datetime.now(timezone.utc).isoformat()
    scanned = stored = signals = 0

    for raw in raw_markets:
        scanned += 1
        m = normalize_market(raw)
        if not m.get("ticker") or m.get("volume", 0) < settings.min_volume:
            continue

        m["captured_at"] = captured_at
        insert_snapshot(settings.db_path, m)
        stored += 1

        signal = detect_two_leg_candidate(m, settings.fee_safety_buffer_cents)
        if signal:
            signal.update({"captured_at": captured_at, "ticker": m["ticker"]})
            insert_signal(settings.db_path, signal)
            signals += 1

    return {"scanned": scanned, "stored": stored, "signals": signals, "captured_at": captured_at}

async def scan_forever() -> None:
    while True:
        try:
            await scan_once()
        except Exception as exc:
            print(f"scanner error: {exc}", flush=True)
        await asyncio.sleep(max(settings.scan_interval_seconds, 5))
