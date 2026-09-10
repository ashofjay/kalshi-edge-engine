import sqlite3
from pathlib import Path
from typing import Any

SCHEMA = """
CREATE TABLE IF NOT EXISTS market_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    captured_at TEXT NOT NULL,
    ticker TEXT NOT NULL,
    event_ticker TEXT,
    title TEXT,
    yes_bid REAL,
    yes_ask REAL,
    no_bid REAL,
    no_ask REAL,
    volume REAL,
    volume_24h REAL,
    status TEXT
);
CREATE INDEX IF NOT EXISTS idx_snapshots_ticker_time
ON market_snapshots(ticker, captured_at);

CREATE TABLE IF NOT EXISTS shadow_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    captured_at TEXT NOT NULL,
    ticker TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    gross_cost REAL NOT NULL,
    buffer REAL NOT NULL,
    estimated_margin REAL NOT NULL,
    yes_ask REAL,
    no_ask REAL,
    note TEXT
);
CREATE INDEX IF NOT EXISTS idx_signals_time
ON shadow_signals(captured_at);
"""

def connect(db_path: str) -> sqlite3.Connection:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def initialize(db_path: str) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)

def insert_snapshot(db_path: str, row: dict[str, Any]) -> None:
    with connect(db_path) as conn:
        conn.execute(
            "INSERT INTO market_snapshots "
            "(captured_at,ticker,event_ticker,title,yes_bid,yes_ask,no_bid,no_ask,volume,volume_24h,status) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (
                row["captured_at"], row["ticker"], row.get("event_ticker"), row.get("title"),
                row.get("yes_bid"), row.get("yes_ask"), row.get("no_bid"), row.get("no_ask"),
                row.get("volume"), row.get("volume_24h"), row.get("status")
            ),
        )

def insert_signal(db_path: str, row: dict[str, Any]) -> None:
    with connect(db_path) as conn:
        conn.execute(
            "INSERT INTO shadow_signals "
            "(captured_at,ticker,signal_type,gross_cost,buffer,estimated_margin,yes_ask,no_ask,note) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (
                row["captured_at"], row["ticker"], row["signal_type"], row["gross_cost"],
                row["buffer"], row["estimated_margin"], row.get("yes_ask"), row.get("no_ask"),
                row.get("note")
            ),
        )

def query(db_path: str, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
    with connect(db_path) as conn:
        return [dict(r) for r in conn.execute(sql, params).fetchall()]
