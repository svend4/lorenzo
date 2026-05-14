"""SQLite-backed storage for quota usage counters."""
from __future__ import annotations

import math
import sqlite3
import time
from typing import Optional

_SCHEMA = """
CREATE TABLE IF NOT EXISTS quota_usage (
    quota_key TEXT NOT NULL,
    owner TEXT NOT NULL,
    window_start REAL NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (quota_key, owner, window_start)
);
CREATE INDEX IF NOT EXISTS idx_quota_window
    ON quota_usage(quota_key, owner, window_start);
CREATE INDEX IF NOT EXISTS idx_quota_window_start
    ON quota_usage(window_start);
"""


def _floor_window(now: float, period_seconds: float) -> float:
    """Compute the start of the current window for an event at `now`."""
    if period_seconds <= 0:
        raise ValueError("period_seconds must be > 0")
    return math.floor(now / period_seconds) * period_seconds


class QuotaStore:
    """Persistent counter for current-window quota usage."""

    def __init__(self, db_path: str = ":memory:"):
        self._path = str(db_path) if db_path else ":memory:"
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    # ------------------------------------------------------------------ #
    def record(
        self,
        quota_key: str,
        owner: str,
        period_seconds: float,
        now: Optional[float] = None,
        amount: int = 1,
    ) -> int:
        """Increment the current window counter, return new count."""
        if now is None:
            now = time.time()
        window_start = _floor_window(now, period_seconds)

        cur = self._conn.execute(
            "SELECT count FROM quota_usage "
            "WHERE quota_key=? AND owner=? AND window_start=?",
            (quota_key, owner, window_start),
        )
        row = cur.fetchone()
        if row is None:
            new_count = int(amount)
            self._conn.execute(
                "INSERT INTO quota_usage (quota_key, owner, window_start, count) "
                "VALUES (?, ?, ?, ?)",
                (quota_key, owner, window_start, new_count),
            )
        else:
            new_count = int(row[0]) + int(amount)
            self._conn.execute(
                "UPDATE quota_usage SET count=? "
                "WHERE quota_key=? AND owner=? AND window_start=?",
                (new_count, quota_key, owner, window_start),
            )
        self._conn.commit()
        return new_count

    # ------------------------------------------------------------------ #
    def get_count(
        self,
        quota_key: str,
        owner: str,
        period_seconds: float,
        now: Optional[float] = None,
    ) -> int:
        """Return count for current window (0 if missing)."""
        if now is None:
            now = time.time()
        window_start = _floor_window(now, period_seconds)
        row = self._conn.execute(
            "SELECT count FROM quota_usage "
            "WHERE quota_key=? AND owner=? AND window_start=?",
            (quota_key, owner, window_start),
        ).fetchone()
        if row is None:
            return 0
        return int(row[0])

    # ------------------------------------------------------------------ #
    def reset(
        self,
        quota_key: Optional[str] = None,
        owner: Optional[str] = None,
    ) -> int:
        """Delete matching rows. Returns deleted row count."""
        if quota_key is None and owner is None:
            cur = self._conn.execute("DELETE FROM quota_usage")
        elif quota_key is not None and owner is not None:
            cur = self._conn.execute(
                "DELETE FROM quota_usage WHERE quota_key=? AND owner=?",
                (quota_key, owner),
            )
        elif quota_key is not None:
            cur = self._conn.execute(
                "DELETE FROM quota_usage WHERE quota_key=?",
                (quota_key,),
            )
        else:  # owner only
            cur = self._conn.execute(
                "DELETE FROM quota_usage WHERE owner=?",
                (owner,),
            )
        self._conn.commit()
        return cur.rowcount if cur.rowcount is not None else 0

    # ------------------------------------------------------------------ #
    def cleanup(self, older_than: float) -> int:
        """Delete rows with window_start < older_than."""
        cur = self._conn.execute(
            "DELETE FROM quota_usage WHERE window_start < ?",
            (older_than,),
        )
        self._conn.commit()
        return cur.rowcount if cur.rowcount is not None else 0

    # ------------------------------------------------------------------ #
    def close(self) -> None:
        self._conn.close()
