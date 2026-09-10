# Kalshi Edge Engine — V0 Shadow Scanner

A Railway-ready, **paper/shadow only** Kalshi market scanner.

## What V0 does
- Pulls open markets from Kalshi's public REST API.
- Stores market snapshots in SQLite.
- Detects a narrow, mechanically testable candidate:
  - `YES ask + NO ask < $1.00`, after a configurable safety/fee buffer.
- Logs those candidates as **shadow opportunities**.
- Exposes FastAPI endpoints for health, stats, recent snapshots, and recent shadow signals.
- Does **not** place live orders.
- Does **not** require Kalshi API credentials for public market data.

## Why start here
A price alone is not a forecast edge. A one-sided YES/NO trade needs an independent probability model.
V0 therefore avoids pretending that midpoint prices create alpha. It starts with data collection and a
book-consistency detector that can be measured before any live-trading module is considered.

## Local run

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn kalshi_edge_engine.app:app --host 0.0.0.0 --port 8000
```

Then open `/health`, `/stats`, `/signals`, or `/snapshots`.

## Railway
This project includes a `Procfile`, `railway.json`, and Dockerfile.

Recommended variables:
- `KALSHI_BASE_URL=https://external-api.kalshi.com/trade-api/v2`
- `SCAN_INTERVAL_SECONDS=60`
- `MARKET_LIMIT=200`
- `MIN_VOLUME=0`
- `FEE_SAFETY_BUFFER_CENTS=3`
- `DB_PATH=/data/kalshi_shadow.db`

For a persistent database on Railway, mount a volume at `/data`.

## Important
This is research software, not a promise of profit. V0 intentionally does not send orders.
Before any future execution module is enabled, validate fees, fills, latency, slippage, settlement rules,
position sizing, and Kalshi's current API/trading requirements.
