"""SQLite schema and repeatable demo data for the local application."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DEFAULT_DATABASE_PATH = Path(__file__).resolve().parent / "procurement_flow.db"

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS purchase_requests (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    stage TEXT NOT NULL CHECK (stage IN ('requested', 'quoted', 'approved', 'delivered', 'paid')),
    requested_cost_cents INTEGER NOT NULL CHECK (requested_cost_cents >= 0),
    expected_revenue_cents INTEGER NOT NULL CHECK (expected_revenue_cents >= 0),
    created_on TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS supplier_quotes (
    id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL REFERENCES purchase_requests(id),
    quoted_cost_cents INTEGER NOT NULL CHECK (quoted_cost_cents >= 0),
    valid_until TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS approvals (
    id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL REFERENCES purchase_requests(id),
    state TEXT NOT NULL CHECK (state IN ('pending', 'approved', 'rejected')),
    decided_on TEXT
);

CREATE TABLE IF NOT EXISTS deliveries (
    id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL REFERENCES purchase_requests(id),
    due_on TEXT NOT NULL,
    delivered_on TEXT,
    state TEXT NOT NULL CHECK (state IN ('pending', 'received', 'late'))
);

CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL REFERENCES purchase_requests(id),
    amount_cents INTEGER NOT NULL CHECK (amount_cents >= 0),
    state TEXT NOT NULL CHECK (state IN ('unpaid', 'scheduled', 'paid')),
    paid_on TEXT
);
"""

# Stable identifiers make the local sample set safe to insert again after any restart.
SEED_ROWS = {
    "purchase_requests": [
        ("req-aster", "Request-Aster", "quoted", 48000, 72000, "2030-01-02"),
        ("req-birch", "Request-Birch", "approved", 125000, 178000, "2030-01-05"),
        ("req-cinder", "Request-Cinder", "requested", 36000, 59000, "2030-01-08"),
    ],
    "supplier_quotes": [
        ("quote-aster", "req-aster", 48000, "2030-02-01"),
        ("quote-birch", "req-birch", 121000, "2030-02-04"),
    ],
    "approvals": [
        ("approval-aster", "req-aster", "pending", None),
        ("approval-birch", "req-birch", "approved", "2030-01-06"),
    ],
    "deliveries": [
        ("delivery-aster", "req-aster", "2030-01-15", None, "pending"),
        ("delivery-birch", "req-birch", "2030-01-18", None, "pending"),
    ],
    "payments": [
        ("payment-aster", "req-aster", 48000, "unpaid", None),
        ("payment-birch", "req-birch", 121000, "scheduled", None),
    ],
}


def connect(database_path: str | Path = DEFAULT_DATABASE_PATH) -> sqlite3.Connection:
    """Return a local SQLite connection with foreign-key protection enabled."""

    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def reset_demo_data(database_path: str | Path = DEFAULT_DATABASE_PATH) -> None:
    """Discard all local records and restore the fixed synthetic sample set."""

    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with connect(database_path) as connection:
        connection.executescript(SCHEMA)
        # Children first so foreign keys stay satisfied while clearing.
        for table in reversed(list(SEED_ROWS)):
            connection.execute(f"DELETE FROM {table}")
    initialize_database(database_path)


def initialize_database(database_path: str | Path = DEFAULT_DATABASE_PATH) -> None:
    """Create the schema and insert the fixed synthetic sample set exactly once."""

    database_path = Path(database_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)
    with connect(database_path) as connection:
        connection.executescript(SCHEMA)
        for table, rows in SEED_ROWS.items():
            placeholders = ", ".join("?" for _ in rows[0])
            connection.executemany(
                f"INSERT OR IGNORE INTO {table} VALUES ({placeholders})", rows
            )
