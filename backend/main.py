"""Application factory for the offline procurement-flow API."""

from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path
import sqlite3
from typing import Any

from fastapi import FastAPI, HTTPException

from backend.database import DEFAULT_DATABASE_PATH, connect, initialize_database


def _rows_for_request(
    connection: sqlite3.Connection, table: str, request_id: str
) -> list[dict[str, Any]]:
    """Return linked records in a stable order for a single request."""

    connection.row_factory = sqlite3.Row
    rows = connection.execute(
        f"SELECT * FROM {table} WHERE request_id = ? ORDER BY id", (request_id,)
    ).fetchall()
    return [dict(row) for row in rows]


def _request_payload(
    connection: sqlite3.Connection, request: sqlite3.Row, *, include_links: bool
) -> dict[str, Any]:
    """Serialize a request and its deterministic, local workflow indicators."""

    request_id = request["id"]
    quotes = _rows_for_request(connection, "supplier_quotes", request_id)
    deliveries = _rows_for_request(connection, "deliveries", request_id)

    # Quotes have no selection flag in the MVP schema. The latest-expiring quote is
    # therefore the current planning cost; a request without a quote uses its budget.
    current_quote = max(
        quotes, key=lambda quote: (quote["valid_until"], quote["id"]), default=None
    )
    cost_basis_cents = (
        current_quote["quoted_cost_cents"]
        if current_quote is not None
        else request["requested_cost_cents"]
    )
    margin_cents = request["expected_revenue_cents"] - cost_basis_cents
    delivery_delay_days = max(
        (
            max(
                0,
                (
                    date.fromisoformat(delivery["delivered_on"])
                    - date.fromisoformat(delivery["due_on"])
                ).days,
            )
            for delivery in deliveries
            if delivery["delivered_on"] is not None
        ),
        default=0,
    )

    payload: dict[str, Any] = {
        "id": request_id,
        "title": request["title"],
        "stage": request["stage"],
        "requested_cost_cents": request["requested_cost_cents"],
        "expected_revenue_cents": request["expected_revenue_cents"],
        "created_on": request["created_on"],
        "cost_basis_cents": cost_basis_cents,
        "margin_cents": margin_cents,
        "margin_percent": round((margin_cents / request["expected_revenue_cents"]) * 100, 2)
        if request["expected_revenue_cents"]
        else None,
        "delivery_delay_days": delivery_delay_days,
        "is_delivery_delayed": delivery_delay_days > 0,
    }
    if include_links:
        payload.update(
            {
                "quotes": quotes,
                "approvals": _rows_for_request(connection, "approvals", request_id),
                "deliveries": deliveries,
                "payments": _rows_for_request(connection, "payments", request_id),
            }
        )
    return payload


def create_app(database_path: str | Path = DEFAULT_DATABASE_PATH) -> FastAPI:
    """Build an app backed only by the supplied local SQLite database."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        initialize_database(database_path)
        yield

    app = FastAPI(
        title="Procurement Flow Board API",
        version="0.1.0",
        lifespan=lifespan,
    )
    app.state.database_path = Path(database_path)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "storage": "local-sqlite"}

    @app.get("/requests")
    def list_requests() -> list[dict[str, Any]]:
        """List synthetic purchase requests with planning indicators."""

        with connect(app.state.database_path) as connection:
            connection.row_factory = sqlite3.Row
            requests = connection.execute(
                "SELECT * FROM purchase_requests ORDER BY created_on, id"
            ).fetchall()
            return [
                _request_payload(connection, request, include_links=False)
                for request in requests
            ]

    @app.get("/requests/{request_id}")
    def get_request(request_id: str) -> dict[str, Any]:
        """Return a request together with every linked local workflow record."""

        with connect(app.state.database_path) as connection:
            connection.row_factory = sqlite3.Row
            request = connection.execute(
                "SELECT * FROM purchase_requests WHERE id = ?", (request_id,)
            ).fetchone()
            if request is None:
                raise HTTPException(status_code=404, detail="Purchase request not found")
            return _request_payload(connection, request, include_links=True)

    return app


app = create_app()
