# Future-session guidance

## Commands

- Initial offline check: `python test/smoke.py`
- Backend tests (after M1): `python -m pytest`
- Frontend tests (after M3): `npm test`
- Frontend lint (after M3): `npm run lint`

## Rules

- Keep every record, label, and fixture synthetic; never add real company, person, marketplace, account, or secret data.
- Keep runtime offline. Do not add HTTP integrations, telemetry, remote fonts, CDNs, or cloud dependencies.
- Keep SQLite local and seed data idempotent.
- Update `SPEC.md` and `PLANS.md` when scope or milestone status changes.
- Add or update tests with behavior changes, and run the relevant command before handoff.
- Do not commit unless the user explicitly asks.
- Keep `.nightshift.json` commands within its allowed command prefixes and free of shell chaining/redirection.
