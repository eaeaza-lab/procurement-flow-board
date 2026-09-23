"""M6 regression coverage for the demo seed reset flow."""

from pathlib import Path
import sqlite3

from fastapi.testclient import TestClient

from backend.database import SEED_ROWS, initialize_database, reset_demo_data
from backend.main import create_app
from backend.reset_demo import main


def _counts(database_path: Path) -> dict[str, int]:
    with sqlite3.connect(database_path) as connection:
        return {
            table: connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in SEED_ROWS
        }


def test_reset_restores_seed_after_edits_and_extra_rows(tmp_path: Path) -> None:
    database_path = tmp_path / "flow.sqlite3"
    initialize_database(database_path)
    with sqlite3.connect(database_path) as connection:
        connection.execute("UPDATE purchase_requests SET stage = 'paid' WHERE id = 'req-aster'")
        connection.execute("DELETE FROM payments WHERE id = 'payment-aster'")
        connection.execute(
            "INSERT INTO purchase_requests VALUES ('req-extra', 'Request-Extra', 'requested', 1, 2, '2030-03-01')"
        )

    reset_demo_data(database_path)

    assert _counts(database_path) == {table: len(rows) for table, rows in SEED_ROWS.items()}
    with sqlite3.connect(database_path) as connection:
        stage = connection.execute(
            "SELECT stage FROM purchase_requests WHERE id = 'req-aster'"
        ).fetchone()[0]
    assert stage == "quoted"


def test_reset_works_on_a_new_database_and_is_repeatable(tmp_path: Path) -> None:
    database_path = tmp_path / "nested" / "flow.sqlite3"
    reset_demo_data(database_path)
    reset_demo_data(database_path)

    assert _counts(database_path) == {table: len(rows) for table, rows in SEED_ROWS.items()}


def test_cli_resets_given_database_and_api_serves_it(tmp_path: Path, capsys) -> None:
    database_path = tmp_path / "flow.sqlite3"

    assert main([str(database_path)]) == 0
    assert "synthetic records" in capsys.readouterr().out

    with TestClient(create_app(database_path)) as client:
        response = client.get("/requests")
    assert [item["id"] for item in response.json()] == ["req-aster", "req-birch", "req-cinder"]
