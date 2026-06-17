"""
Layer 5 (Persistence) — Signal storage.

Stores generated signals as JSON rows in SQLite by default (zero setup).
Set DB_URL to a postgresql:// string and install psycopg2 to use Postgres;
the same SQL works on both via SQLAlchemy if you choose to extend it.
"""
import json
import sqlite3
from datetime import datetime, timezone
from config import config

_DB_FILE = config.DB_URL.replace("sqlite:///", "") if config.DB_URL.startswith("sqlite") else "signals.db"


def _conn():
    c = sqlite3.connect(_DB_FILE)
    c.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT, ticker TEXT, action TEXT,
            confidence REAL, payload TEXT
        )""")
    return c


def save_signal(sig):
    c = _conn()
    c.execute(
        "INSERT INTO signals (created_at, ticker, action, confidence, payload) VALUES (?,?,?,?,?)",
        (datetime.now(timezone.utc).isoformat(), sig["ticker"], sig["action"],
         sig["confidence"], json.dumps(sig)),
    )
    c.commit()
    c.close()


def recent_signals(limit=50):
    c = _conn()
    rows = c.execute(
        "SELECT payload FROM signals ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    c.close()
    return [json.loads(r[0]) for r in rows]
