import os
import sqlite3
from datetime import datetime, timezone

from .config import settings


def _connect():
    directory = os.path.dirname(settings.db_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                ticker TEXT,
                title TEXT,
                yes_bid INTEGER,
                yes_ask INTEGER,
                no_bid INTEGER,
                no_ask INTEGER,
                volume REAL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                ticker TEXT,
                title TEXT,
                yes_ask INTEGER,
                no_ask INTEGER,
                total_cost INTEGER,
                gross_edge_cents INTEGER,
                buffer_cents INTEGER
            )
        """)


def save_snapshot(market):
    timestamp = datetime.now(timezone.utc).isoformat()

    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO snapshots (
                timestamp, ticker, title,
                yes_bid, yes_ask, no_bid, no_ask, volume
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                market.get("ticker"),
                market.get("title"),
                market.get("yes_bid"),
                market.get("yes_ask"),
                market.get("no_bid"),
                market.get("no_ask"),
                market.get("volume"),
            ),
        )


def save_signal(signal):
    timestamp = datetime.now(timezone.utc).isoformat()

    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO signals (
                timestamp, ticker, title,
                yes_ask, no_ask, total_cost,
                gross_edge_cents, buffer_cents
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                signal.get("ticker"),
                signal.get("title"),
                signal.get("yes_ask"),
                signal.get("no_ask"),
                signal.get("total_cost"),
                signal.get("gross_edge_cents"),
                signal.get("buffer_cents"),
            ),
        )


def get_stats():
    with _connect() as conn:
        snapshots = conn.execute(
            "SELECT COUNT(*) AS count FROM snapshots"
        ).fetchone()["count"]

        signals = conn.execute(
            "SELECT COUNT(*) AS count FROM signals"
        ).fetchone()["count"]

    return {
        "snapshots": snapshots,
        "signals": signals,
    }


def get_recent_signals(limit=50):
    with _connect() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM signals
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]
