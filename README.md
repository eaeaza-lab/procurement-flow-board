# Procurement Flow Board

Status: **work in progress**

An offline procurement-workflow demo: synthetic purchase requests move through supplier quotes, approvals, delivery, and payment on a searchable Kanban board. It is intended as a showcase, practical tool experiment, learning project, and possible SaaS foundation.

Built by a supervised autonomous agent pipeline (nightshift).

## Run

The repository starts with a dependency-free smoke check:

```powershell
python test/smoke.py
```

Planned application commands (after M1–M3):

```powershell
python -m pytest
npm install
npm run dev
```

All demo records are synthetic. The finished app will run locally with SQLite and will not make runtime network calls.
