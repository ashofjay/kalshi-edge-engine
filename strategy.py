from typing import Optional

def _price(market: dict, dollar_key: str, cents_key: str) -> Optional[float]:
    value = market.get(dollar_key)
    if value not in (None, ""):
        try:
            return float(value)
        except (TypeError, ValueError):
            pass
    value = market.get(cents_key)
    if value not in (None, ""):
        try:
            return float(value) / 100.0
        except (TypeError, ValueError):
            pass
    return None

def normalize_market(market: dict) -> dict:
    return {
        "ticker": market.get("ticker"),
        "event_ticker": market.get("event_ticker"),
        "title": market.get("title") or market.get("subtitle"),
        "yes_bid": _price(market, "yes_bid_dollars", "yes_bid"),
        "yes_ask": _price(market, "yes_ask_dollars", "yes_ask"),
        "no_bid": _price(market, "no_bid_dollars", "no_bid"),
        "no_ask": _price(market, "no_ask_dollars", "no_ask"),
        "volume": float(market.get("volume_fp") or market.get("volume") or 0),
        "volume_24h": float(market.get("volume_24h_fp") or market.get("volume_24h") or 0),
        "status": market.get("status"),
    }

def detect_two_leg_candidate(market: dict, fee_safety_buffer_cents: int) -> Optional[dict]:
    yes_ask = market.get("yes_ask")
    no_ask = market.get("no_ask")
    if yes_ask is None or no_ask is None:
        return None

    gross_cost = yes_ask + no_ask
    buffer = fee_safety_buffer_cents / 100.0
    estimated_margin = 1.0 - gross_cost - buffer

    if estimated_margin <= 0:
        return None

    return {
        "signal_type": "two_leg_book_inconsistency",
        "gross_cost": round(gross_cost, 4),
        "buffer": round(buffer, 4),
        "estimated_margin": round(estimated_margin, 4),
        "yes_ask": yes_ask,
        "no_ask": no_ask,
        "note": "Shadow-only candidate. Buffer is a placeholder, not an exact Kalshi fee calculation."
    }
