"""SQLite-backed store for CacheEntry objects."""
import sqlite3
import time
from typing import Optional

from docstoolkit.response_cache.entry import CacheEntry


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS cache_entries (
    cache_key    TEXT PRIMARY KEY,
    value        TEXT NOT NULL,
    created_ts   REAL NOT NULL,
    ttl_seconds  REAL NOT NULL,
    hit_count    INTEGER NOT NULL DEFAULT 0,
    last_accessed REAL NOT NULL DEFAULT 0.0
)
"""


class ResponseCacheStore:
    """Thread-compatible SQLite store for cache entries."""

    def __init__(self, db_path: str = ":memory:"):
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(_CREATE_TABLE)
        self._conn.commit()

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    def set(self, entry: CacheEntry) -> None:
        """INSERT OR REPLACE the entry in the store."""
        self._conn.execute(
            """
            INSERT OR REPLACE INTO cache_entries
                (cache_key, value, created_ts, ttl_seconds, hit_count, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                entry.cache_key,
                entry.value,
                entry.created_ts,
                entry.ttl_seconds,
                entry.hit_count,
                entry.last_accessed,
            ),
        )
        self._conn.commit()

    def get(self, cache_key: str) -> Optional[CacheEntry]:
        """Return the CacheEntry for cache_key, or None if not found."""
        row = self._conn.execute(
            "SELECT cache_key, value, created_ts, ttl_seconds, hit_count, last_accessed "
            "FROM cache_entries WHERE cache_key = ?",
            (cache_key,),
        ).fetchone()
        if row is None:
            return None
        return CacheEntry(
            cache_key=row[0],
            value=row[1],
            created_ts=row[2],
            ttl_seconds=row[3],
            hit_count=row[4],
            last_accessed=row[5],
        )

    def delete(self, cache_key: str) -> bool:
        """Delete entry by key. Returns True if a row was removed."""
        cursor = self._conn.execute(
            "DELETE FROM cache_entries WHERE cache_key = ?", (cache_key,)
        )
        self._conn.commit()
        return cursor.rowcount > 0

    # ------------------------------------------------------------------
    # Eviction
    # ------------------------------------------------------------------

    def evict_expired(self, now: float = None) -> int:
        """Remove all expired entries. Returns the number of rows deleted."""
        if now is None:
            now = time.time()
        # An entry is expired when (now - created_ts) >= ttl_seconds,
        # i.e. created_ts <= now - ttl_seconds
        cursor = self._conn.execute(
            "DELETE FROM cache_entries WHERE (? - created_ts) >= ttl_seconds",
            (now,),
        )
        self._conn.commit()
        return cursor.rowcount

    def evict_lru(self, max_size: int) -> int:
        """Remove least-recently-used entries beyond max_size. Returns rows deleted."""
        total = self._conn.execute(
            "SELECT COUNT(*) FROM cache_entries"
        ).fetchone()[0]
        excess = total - max_size
        if excess <= 0:
            return 0
        # Delete the `excess` entries with the smallest last_accessed value.
        cursor = self._conn.execute(
            """
            DELETE FROM cache_entries
            WHERE cache_key IN (
                SELECT cache_key FROM cache_entries
                ORDER BY last_accessed ASC
                LIMIT ?
            )
            """,
            (excess,),
        )
        self._conn.commit()
        return cursor.rowcount

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        """Return aggregate statistics for the store."""
        row = self._conn.execute(
            "SELECT COUNT(*), COALESCE(SUM(hit_count), 0) FROM cache_entries"
        ).fetchone()
        total_entries = row[0]
        total_hits = row[1]
        # hit_rate: proportion of entries that have been accessed at least once,
        # expressed as total_hits / (total_entries + total_hits) where total_entries
        # counts "misses" (initial sets).  A simpler and more useful definition:
        # total_hits / total_requests, but we only track hits here, so we compute
        # total_hits / (total_entries + total_hits) as an approximation.
        if (total_entries + total_hits) == 0:
            hit_rate = 0.0
        else:
            hit_rate = total_hits / (total_entries + total_hits)
        return {
            "total_entries": total_entries,
            "total_hits": total_hits,
            "hit_rate": hit_rate,
        }
