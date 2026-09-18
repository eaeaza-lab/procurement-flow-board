# Procurement Flow Board

Status: **work in progress**

An offline procurement-workflow demo: synthetic purchase requests move through supplier quotes, approvals, delivery, and payment on a searchable Kanban board. It is intended as a showcase, practical tool experiment, learning project, and possible SaaS foundation.

Built by a supervised autonomous agent pipeline (nightshift).

## Run

Install the local Python dependencies, then run the API test suite:

```powershell
python -m pip install -r requirements.txt
python -m pytest
```

Start the entirely local API with:

```powershell
python -m uvicorn backend.main:app --reload
```

The health check is available at `http://127.0.0.1:8000/health`; the API initializes a local SQLite database with repeatable synthetic seed data on startup. The board UI is planned for M3.

All demo records are synthetic. The finished app will run locally with SQLite and will not make runtime network calls.
