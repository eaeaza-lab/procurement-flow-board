# Execution Plan

## Milestones

- [x] **M0 setup** — **stage: mvp** — Create the specification, project guidance, offline check, and a synthetic-domain skeleton. Acceptance: `python test/smoke.py`
- [x] **M1 API foundation** — **stage: mvp** — Create a FastAPI application with SQLite schema and idempotent synthetic seeding. Acceptance: `python -m pytest`
- [ ] **M2 workflow API** — **stage: mvp** — Add read endpoints for requests, linked quotes/approvals/deliveries/payments, and computed margin/delay fields. Acceptance: `python -m pytest`
- [ ] **M3 board UI** — **stage: mvp** — Create the Vite/React Kanban board with stage columns, search, and status indicators. Acceptance: `npm test`
- [ ] **M4 table and details** — **stage: mvp** — Add TanStack Table filtering/sorting and a request-detail panel. Acceptance: `npm test`
- [ ] **M5 usability polish** — **stage: polish** — Improve empty/loading/error states, keyboard focus, responsive layout, and visual hierarchy. Acceptance: `npm test`
- [ ] **M6 quality pass** — **stage: polish** — Add linting, API/UI regression coverage, and a concise demo seed reset flow. Acceptance: `python -m pytest`

## Progress log

- 2026-09-16 — M0 completed: documented product boundaries and added an offline smoke test for the synthetic workflow model.
- 2026-09-18 — M1 completed: added the local FastAPI application, SQLite workflow schema, idempotent synthetic seed data, and API foundation checks.

## Decision log

- 2026-09-16 — Keep runtime fully local: SQLite and local seed data, with no network-dependent features.
- 2026-09-16 — Start with a Node built-in test so repository checks work before dependencies are installed.
- 2026-09-16 — Use neutral synthetic labels such as `Request-Aster` rather than real-world identities.
- 2026-09-18 — Store money as integer cents in SQLite to keep later margin calculations exact and independent of floating-point rounding.
