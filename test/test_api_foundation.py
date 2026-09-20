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


def test_requests_list_exposes_computed_workflow_indicators(tmp_path: Path) -> None:
    database_path = tmp_path / "flow.sqlite3"
    with TestClient(create_app(database_path)) as client:
        response = client.get("/requests")

    assert response.status_code == 200
    requests = response.json()
    aster = next(request for request in requests if request["id"] == "req-aster")
    cinder = next(request for request in requests if request["id"] == "req-cinder")
    assert aster["cost_basis_cents"] == 48000
    assert aster["margin_cents"] == 24000
    assert aster["margin_percent"] == 33.33
    assert aster["delivery_delay_days"] == 0
    assert aster["is_delivery_delayed"] is False
    assert cinder["cost_basis_cents"] == 36000
    assert cinder["margin_cents"] == 23000


def test_request_detail_exposes_all_linked_records_and_not_found(tmp_path: Path) -> None:
    database_path = tmp_path / "flow.sqlite3"
    with TestClient(create_app(database_path)) as client:
        response = client.get("/requests/req-birch")
        missing = client.get("/requests/req-missing")

    assert response.status_code == 200
    request = response.json()
    assert request["id"] == "req-birch"
    assert request["quotes"] == [
        {"id": "quote-birch", "request_id": "req-birch", "quoted_cost_cents": 121000, "valid_until": "2030-02-04"}
    ]
    assert request["approvals"][0]["state"] == "approved"
    assert request["deliveries"][0]["state"] == "pending"
    assert request["payments"][0]["state"] == "scheduled"
    assert missing.status_code == 404


def test_completed_late_delivery_sets_delay_indicator(tmp_path: Path) -> None:
    database_path = tmp_path / "flow.sqlite3"
    with TestClient(create_app(database_path)) as client:
        with sqlite3.connect(database_path) as connection:
            connection.execute(
                "UPDATE deliveries SET state = ?, delivered_on = ? WHERE id = ?",
                ("late", "2030-01-20", "delivery-aster"),
            )
        response = client.get("/requests/req-aster")

    assert response.status_code == 200
    assert response.json()["delivery_delay_days"] == 5
    assert response.json()["is_delivery_delayed"] is True
