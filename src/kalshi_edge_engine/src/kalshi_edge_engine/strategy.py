from .config import settings


def find_two_leg_opportunity(market):
    yes_ask = market.get("yes_ask")
    no_ask = market.get("no_ask")

    if yes_ask is None or no_ask is None:
        return None

    try:
        yes_ask = int(yes_ask)
        no_ask = int(no_ask)
    except (TypeError, ValueError):
        return None

    total_cost = yes_ask + no_ask
    threshold = 100 - settings.fee_safety_buffer_cents

    if total_cost < threshold:
        return {
            "ticker": market.get("ticker"),
            "title": market.get("title"),
            "yes_ask": yes_ask,
            "no_ask": no_ask,
            "total_cost": total_cost,
            "gross_edge_cents": 100 - total_cost,
            "buffer_cents": settings.fee_safety_buffer_cents,
        }

    return None
