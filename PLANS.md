# Execution Plan

## Milestones

- [x] **M0 setup** - **stage: mvp** - Create the specification, project guidance, offline check, and a synthetic-domain skeleton. Acceptance: `python test/smoke.py`
- [x] **M1 API foundation** - **stage: mvp** - Create a FastAPI application with SQLite schema and idempotent synthetic seeding. Acceptance: `python -m pytest`
- [x] **M2 workflow API** - **stage: mvp** - Add read endpoints for requests, linked quotes/approvals/deliveries/payments, and computed margin/delay fields. Acceptance: `python -m pytest`
- [x] **M3 board UI** - **stage: mvp** - Create the Vite/React Kanban board with stage columns, search, and status indicators. Acceptance: `npm test`
- [x] **M4 table and details** - **stage: mvp** - Add TanStack Table filtering/sorting and a request-detail panel. Acceptance: `npm test`
- [x] **M5 usability polish** - **stage: polish** - Improve empty/loading/error states, keyboard focus, responsive layout, and visual hierarchy. Acceptance: `npm test`
- [ ] **M6 quality pass** - **stage: polish** - Add linting, API/UI regression coverage, and a concise demo seed reset flow. Acceptance: `python -m pytest`

## Progress log

- 2026-09-16 - M0 completed: documented product boundaries and added an offline smoke test for the synthetic workflow model.
- 2026-09-18 - M1 completed: added the local FastAPI application, SQLite workflow schema, idempotent synthetic seed data, and API foundation checks.
- 2026-09-20 - M2 completed: added local request list/detail reads, linked workflow records, and deterministic margin and delivery-delay indicators.
- 2026-09-21 - M3 completed: added the local Vite/React Kanban board, title/ID search, and margin/delivery status indicators.
- 2026-09-22 - M4 completed: added the TanStack request table with stage filtering and sortable columns, plus an on-demand linked-record detail panel.
- 2026-09-23 - M5 completed: added recovery actions and clear empty states, focus support, responsive scrolling, and stronger page hierarchy.

## Decision log

- 2026-09-16 - Keep runtime fully local: SQLite and local seed data, with no network-dependent features.
- 2026-09-16 - Start with a Node built-in test so repository checks work before dependencies are installed.
- 2026-09-16 - Use neutral synthetic labels such as `Request-Aster` rather than real-world identities.
- 2026-09-18 - Store money as integer cents in SQLite to keep later margin calculations exact and independent of floating-point rounding.
- 2026-09-20 - Use the latest-expiring quote as the current planning cost; when no quote exists, calculate projected margin from the original requested cost. Delivery delay is the greatest completed delivery lateness and is zero until a delivery is received.
- 2026-09-21 - Route board requests through Vite's `/api` development proxy so the browser contacts only the local companion API and the backend requires no CORS configuration.
- 2026-09-22 - Fetch detail records only after a user selects a request, keeping the board's initial local API read lightweight while still presenting all linked workflow records.
- 2026-09-23 - Keep all five stage columns visible as horizontally scrollable cards on narrow screens so stage context is retained instead of collapsing the workflow.
