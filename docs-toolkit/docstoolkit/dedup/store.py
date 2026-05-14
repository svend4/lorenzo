"""SQLite-backed deduplication store."""
import sqlite3
import time
from dataclasses import dataclass
from typing import Optional

from docstoolkit.dedup.key import DeduplicationStrategy


@dataclass
class DedupEntry:
    """A single stored deduplication record."""
    request_id: str
    key_hash: str
    strategy: DeduplicationStrategy
    result: Optional[str]       # None until complete() is called
    created_ts: float
    ttl_seconds: float          # 0 means never expires


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS dedup_entries (
    key_hash    TEXT NOT NULL PRIMARY KEY,
    request_id  TEXT NOT NULL,
    strategy    TEXT NOT NULL,
    result      TEXT,
    created_ts  REAL NOT NULL,
    ttl_seconds REAL NOT NULL
);
"""

_CREATE_RESULT_IDX = """
CREATE INDEX IF NOT EXISTS idx_request_id ON dedup_entries (request_id);
"""


class DedupStore:
    """Thread-safe deduplication store backed by SQLite.

    Parameters
    ----------
    db_path: SQLite database path.  Use ``":memory:"`` (default) for
             an in-process store that is lost when the object is garbage
             collected.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute(_CREATE_TABLE)
        self._conn.execute(_CREATE_RESULT_IDX)
        self._conn.commit()
        self._stats: dict = {
            "total": 0,
            "expired_evicted": 0,
            "duplicate_hits": 0,
        }

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def put(self, entry: DedupEntry) -> None:
        """Insert or replace a DedupEntry keyed by *key_hash*."""
        self._conn.execute(
            """
            INSERT OR REPLACE INTO dedup_entries
                (key_hash, request_id, strategy, result, created_ts, ttl_seconds)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                entry.key_hash,
                entry.request_id,
                entry.strategy.value,
                entry.result,
                entry.created_ts,
                entry.ttl_seconds,
            ),
        )
        self._conn.commit()
        self._stats["total"] += 1

    def update_result(self, request_id: str, result: str) -> None:
        """Persist the completed result for *request_id*."""
        self._conn.execute(
            "UPDATE dedup_entries SET result = ? WHERE request_id = ?",
            (result, request_id),
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get(self, key_hash: str) -> Optional[DedupEntry]:
        """Return the DedupEntry for *key_hash*, or None if absent/expired."""
        row = self._conn.execute(
            "SELECT * FROM dedup_entries WHERE key_hash = ?", (key_hash,)
        ).fetchone()
        if row is None:
            return None
        entry = self._row_to_entry(row)
        if self._is_expired(entry):
            return None
        return entry

    def get_by_request_id(self, request_id: str) -> Optional[DedupEntry]:
        """Look up an entry by its *request_id* (for result retrieval)."""
        row = self._conn.execute(
            "SELECT * FROM dedup_entries WHERE request_id = ?", (request_id,)
        ).fetchone()
        if row is None:
            return None
        return self._row_to_entry(row)

    def is_duplicate(self, key_hash: str) -> bool:
        """Return True if a live (non-expired) entry exists for *key_hash*."""
        entry = self.get(key_hash)
        if entry is None:
            return False
        self._stats["duplicate_hits"] += 1
        return True

    # ------------------------------------------------------------------
    # Eviction
    # ------------------------------------------------------------------

    def evict_expired(self, now: float = None) -> int:
        """Delete all TTL-expired entries.

        Parameters
        ----------
        now: Reference timestamp (``time.time()``).  Defaults to the
             current wall-clock time; pass an explicit value in tests to
             avoid real sleeping.

        Returns
        -------
        Number of rows removed.
        """
        if now is None:
            now = time.time()
        # expires_at = created_ts + ttl_seconds; ttl_seconds=0 means immortal
        cursor = self._conn.execute(
            """
            DELETE FROM dedup_entries
            WHERE ttl_seconds > 0
              AND (created_ts + ttl_seconds) < ?
            """,
            (now,),
        )
        self._conn.commit()
        removed = cursor.rowcount
        self._stats["expired_evicted"] += removed
        return removed

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        """Return a snapshot of store statistics.

        Keys: ``total``, ``expired_evicted``, ``duplicate_hits``.
        """
        return dict(self._stats)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_entry(row: sqlite3.Row) -> DedupEntry:
        return DedupEntry(
            request_id=row["request_id"],
            key_hash=row["key_hash"],
            strategy=DeduplicationStrategy(row["strategy"]),
            result=row["result"],
            created_ts=row["created_ts"],
            ttl_seconds=row["ttl_seconds"],
        )

    @staticmethod
    def _is_expired(entry: DedupEntry, now: float = None) -> bool:
        if entry.ttl_seconds <= 0:
            return False
        if now is None:
            now = time.time()
        return (entry.created_ts + entry.ttl_seconds) < now
