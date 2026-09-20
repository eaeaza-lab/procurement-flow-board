# Procurement Flow Board

Status: **work in progress**

An offline procurement-workflow demo: synthetic purchase requests move through supplier quotes, approvals, delivery, and payment on a searchable Kanban board. It is intended as a showcase, practical tool experiment, learning project, and possible SaaS foundation.

Built by a supervised autonomous agent pipeline (nightshift).

## Run

Install the local Python and Node dependencies, then run the complete local check suite:

```powershell
python -m pip install -r requirements.txt
npm install
python -m pytest
npm test
```

Start the entirely local API in one terminal:

```powershell
python -m uvicorn backend.main:app --reload
```

Then start the Vite board in another:

```powershell
npm run dev
```

Open the local address Vite prints (normally `http://127.0.0.1:5173`). The board fetches from the companion API through Vite's local-only proxy. It groups requests by stage, supports title/ID search, and flags late deliveries or low projected margins.

The health check is available at `http://127.0.0.1:8000/health`; the API initializes a local SQLite database with repeatable synthetic seed data on startup. `GET /requests` lists the requests with local margin and delivery-delay indicators, while `GET /requests/{request_id}` also returns its quotes, approvals, deliveries, and payments.

All demo records are synthetic. The finished app will run locally with SQLite and will not make runtime network calls.
