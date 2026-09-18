"""Application factory for the offline procurement-flow API."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from backend.database import DEFAULT_DATABASE_PATH, initialize_database


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

    return app


app = create_app()
