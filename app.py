import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from .config import settings
from .db import initialize, query
from .scanner import scan_once, scan_forever

scanner_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global scanner_task
    initialize(settings.db_path)
    scanner_task = asyncio.create_task(scan_forever())
    yield
    if scanner_task:
        scanner_task.cancel()

app = FastAPI(
    title="Kalshi Edge Engine",
    version="0.1.0",
    description="Shadow-only Kalshi market scanner and research logger.",
    lifespan=lifespan,
)

@app.get("/")
def root():
    return {"name": "Kalshi Edge Engine", "mode": "shadow-only", "docs": "/docs", "health": "/health"}

@app.get("/health")
def health():
    return {"status": "ok", "mode": "shadow-only"}

@app.post("/scan")
async def manual_scan():
    return await scan_once()

@app.get("/stats")
def stats():
    snapshots = query(settings.db_path, "SELECT COUNT(*) AS n FROM market_snapshots")[0]["n"]
    signals = query(settings.db_path, "SELECT COUNT(*) AS n FROM shadow_signals")[0]["n"]
    unique_markets = query(settings.db_path, "SELECT COUNT(DISTINCT ticker) AS n FROM market_snapshots")[0]["n"]
    return {"snapshots": snapshots, "signals": signals, "unique_markets": unique_markets}

@app.get("/signals")
def signals(limit: int = Query(50, ge=1, le=500)):
    return query(settings.db_path, "SELECT * FROM shadow_signals ORDER BY id DESC LIMIT ?", (limit,))

@app.get("/snapshots")
def snapshots(limit: int = Query(50, ge=1, le=500)):
    return query(settings.db_path, "SELECT * FROM market_snapshots ORDER BY id DESC LIMIT ?", (limit,))
