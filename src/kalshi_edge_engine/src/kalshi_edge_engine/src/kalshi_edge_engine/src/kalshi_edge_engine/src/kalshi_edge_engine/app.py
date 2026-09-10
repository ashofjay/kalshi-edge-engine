import asyncio
import sqlite3
from contextlib import asynccontextmanager

from fastapi import FastAPI, Query

from .config import settings
from .db import init_db, get_stats, get_recent_signals
from .scanner import Scanner


scanner = Scanner()
scanner_task = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global scanner_task

    init_db()
    scanner_task = asyncio.create_task(scanner.run_forever())

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
    return {
        "name": "Kalshi Edge Engine",
        "mode": "shadow-only",
        "health": "/health",
        "stats": "/stats",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mode": "shadow-only",
    }


@app.post("/scan")
async def manual_scan():
    return await scanner.scan_once()


@app.get("/stats")
def stats():
    return get_stats()


@app.get("/signals")
def signals(limit: int = Query(50, ge=1, le=500)):
    return get_recent_signals(limit)


@app.get("/snapshots")
def snapshots(limit: int = Query(50, ge=1, le=500)):
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row

    try:
        rows = conn.execute(
            """
            SELECT *
            FROM snapshots
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [dict(row) for row in rows]
    finally:
        conn.close()
