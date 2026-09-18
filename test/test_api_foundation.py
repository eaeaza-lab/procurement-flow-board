"""M1 regression coverage for the entirely local API foundation."""

from pathlib import Path
import sqlite3

from fastapi.testclient import TestClient

from backend.database import SEED_ROWS, initialize_database
from backend.main import create_app


def test_schema_exposes_every_workflow_record_type(tmp_path: Path) -> None:
    database_path = tmp_path / "flow.sqlite3"
    initialize_database(database_path)

    with sqlite3.connect(database_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert {
            "purchase_requests",
            "supplier_quotes",
            "approvals",
            "deliveries",
            "payments",
        } <= tables


def test_seed_is_idempotent_and_synthetic(tmp_path: Path) -> None:
    database_path = tmp_path / "flow.sqlite3"
    initialize_database(database_path)
    initialize_database(database_path)

    with sqlite3.connect(database_path) as connection:
        for table, rows in SEED_ROWS.items():
            count = connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            assert count == len(rows)
        titles = connection.execute("SELECT title FROM purchase_requests").fetchall()

    assert titles == [("Request-Aster",), ("Request-Birch",), ("Request-Cinder",)]


def test_app_starts_with_local_database_and_health_check(tmp_path: Path) -> None:
    database_path = tmp_path / "flow.sqlite3"
    with TestClient(create_app(database_path)) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "storage": "local-sqlite"}
    assert database_path.exists()
