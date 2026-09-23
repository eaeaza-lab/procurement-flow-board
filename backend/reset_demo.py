"""Restore the local demo database to its synthetic seed data.

Usage: python -m backend.reset_demo [database_path]
"""

from __future__ import annotations

import sys

from backend.database import DEFAULT_DATABASE_PATH, SEED_ROWS, reset_demo_data


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    database_path = args[0] if args else DEFAULT_DATABASE_PATH
    reset_demo_data(database_path)
    total = sum(len(rows) for rows in SEED_ROWS.values())
    print(f"Reset {database_path} with {total} synthetic records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
