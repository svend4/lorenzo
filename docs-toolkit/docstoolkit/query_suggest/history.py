"""SQLite-backed query history store."""
from __future__ import annotations

import sqlite3


class QueryHistory:
    """Persistent (or in-memory) query history backed by SQLite.

    Args:
        db_path: Path to the SQLite database file.  Defaults to ``":memory:"``
                 which keeps everything in RAM for the lifetime of this object.
    """

    _CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS query_log (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            query        TEXT    NOT NULL,
            result_count INTEGER NOT NULL DEFAULT 0,
            selected     INTEGER NOT NULL DEFAULT 0,
            recorded_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        )
    """

    _CREATE_IDX_QUERY = (
        "CREATE INDEX IF NOT EXISTS idx_query_log_query ON query_log(query)"
    )

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(self._CREATE_TABLE)
        self._conn.execute(self._CREATE_IDX_QUERY)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Normalisation
    # ------------------------------------------------------------------

    @staticmethod
    def _normalize(query: str) -> str:
        return query.lower().strip()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def record(self, query: str, result_count: int = 0, selected: bool = False) -> None:
        """Append one query event to the history log.

        Each call always creates a new row so that temporal ordering is
        preserved and ``recent_queries`` works correctly.
        """
        normalized = self._normalize(query)
        if not normalized:
            return
        self._conn.execute(
            "INSERT INTO query_log (query, result_count, selected) VALUES (?, ?, ?)",
            (normalized, result_count, int(selected)),
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def top_queries(self, n: int = 20) -> list[tuple[str, int]]:
        """Return the *n* most frequently recorded queries.

        Returns a list of ``(query, count)`` tuples sorted by count descending.
        """
        cur = self._conn.execute(
            """
            SELECT query, COUNT(*) AS cnt
            FROM query_log
            GROUP BY query
            ORDER BY cnt DESC, query
            LIMIT ?
            """,
            (n,),
        )
        return [(row[0], row[1]) for row in cur.fetchall()]

    def recent_queries(self, n: int = 10) -> list[str]:
        """Return the last *n* **distinct** queries in reverse chronological order."""
        # Fetch enough rows to collect n distinct values without loading everything.
        # We use a subquery that keeps the most recent row per distinct query, then
        # orders by that row's id descending.
        cur = self._conn.execute(
            """
            SELECT query
            FROM (
                SELECT query, MAX(id) AS last_id
                FROM query_log
                GROUP BY query
            )
            ORDER BY last_id DESC
            LIMIT ?
            """,
            (n,),
        )
        return [row[0] for row in cur.fetchall()]

    def popular_for_prefix(self, prefix: str, n: int = 5) -> list[tuple[str, int]]:
        """Return queries matching *prefix* sorted by frequency descending.

        Returns a list of ``(query, count)`` tuples.
        """
        normalized_prefix = self._normalize(prefix)
        like_pattern = normalized_prefix + "%"
        cur = self._conn.execute(
            """
            SELECT query, COUNT(*) AS cnt
            FROM query_log
            WHERE query LIKE ?
            GROUP BY query
            ORDER BY cnt DESC, query
            LIMIT ?
            """,
            (like_pattern, n),
        )
        return [(row[0], row[1]) for row in cur.fetchall()]

    def total_queries(self) -> int:
        """Return the total number of recorded query events (rows in the log)."""
        cur = self._conn.execute("SELECT COUNT(*) FROM query_log")
        return cur.fetchone()[0]

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()

    def __del__(self) -> None:  # pragma: no cover
        try:
            self._conn.close()
        except Exception:
            pass
