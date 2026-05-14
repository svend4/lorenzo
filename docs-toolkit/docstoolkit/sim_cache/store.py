"""SQLite-backed store for SimilarityEntry objects."""
import sqlite3
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.sim_cache.fingerprint import Fingerprint, FingerprintMethod


def _new_entry_id() -> str:
    """Generate an 8-character UUID4-based entry ID."""
    return uuid.uuid4().hex[:8]


@dataclass
class SimilarityEntry:
    """A single cached similarity entry."""
    text: str
    fingerprint: Fingerprint
    result: str
    entry_id: str = field(default_factory=_new_entry_id)
    created_ts: float = field(default_factory=time.time)
    hit_count: int = 0


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS sim_entries (
    entry_id     TEXT PRIMARY KEY,
    text         TEXT NOT NULL,
    fp_method    TEXT NOT NULL,
    fp_value     TEXT NOT NULL,
    fp_text_len  INTEGER NOT NULL,
    result       TEXT NOT NULL,
    created_ts   REAL NOT NULL,
    hit_count    INTEGER NOT NULL DEFAULT 0
)
"""

# fp_value is stored as a hex string to avoid SQLite signed-int overflow for
# unsigned 64-bit fingerprint integers.


class SimCacheStore:
    """Thread-compatible SQLite store for SimilarityEntry objects."""

    def __init__(self, db_path: str = ":memory:"):
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(_CREATE_TABLE)
        self._conn.commit()

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------

    @staticmethod
    def _fp_value_to_db(value: int) -> str:
        """Encode fingerprint int as a hex string for safe SQLite storage."""
        return format(value, "016x")

    @staticmethod
    def _fp_value_from_db(hex_str: str) -> int:
        """Decode a hex-encoded fingerprint value back to int."""
        return int(hex_str, 16)

    def add(self, entry: SimilarityEntry) -> None:
        """Insert *entry* into the store (INSERT OR REPLACE)."""
        self._conn.execute(
            """
            INSERT OR REPLACE INTO sim_entries
                (entry_id, text, fp_method, fp_value, fp_text_len, result, created_ts, hit_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.entry_id,
                entry.text,
                entry.fingerprint.method.value,
                self._fp_value_to_db(entry.fingerprint.value),
                entry.fingerprint.text_len,
                entry.result,
                entry.created_ts,
                entry.hit_count,
            ),
        )
        self._conn.commit()

    def find_similar(
        self,
        fingerprint: Fingerprint,
        threshold: float = 0.9,
    ) -> list[SimilarityEntry]:
        """Return all entries whose fingerprint similarity >= *threshold*.

        Results are sorted by similarity descending.
        """
        rows = self._conn.execute(
            "SELECT entry_id, text, fp_method, fp_value, fp_text_len, result, created_ts, hit_count "
            "FROM sim_entries WHERE fp_method = ?",
            (fingerprint.method.value,),
        ).fetchall()

        results: list[tuple[float, SimilarityEntry]] = []
        for row in rows:
            stored_fp = Fingerprint(
                method=FingerprintMethod(row[2]),
                value=self._fp_value_from_db(row[3]),
                text_len=row[4],
            )
            sim = fingerprint.similarity(stored_fp)
            if sim >= threshold:
                entry = SimilarityEntry(
                    entry_id=row[0],
                    text=row[1],
                    fingerprint=stored_fp,
                    result=row[5],
                    created_ts=row[6],
                    hit_count=row[7],
                )
                results.append((sim, entry))

        results.sort(key=lambda t: t[0], reverse=True)
        return [entry for _, entry in results]

    def get(self, entry_id: str) -> Optional[SimilarityEntry]:
        """Return a SimilarityEntry by its ID, or None if not found."""
        row = self._conn.execute(
            "SELECT entry_id, text, fp_method, fp_value, fp_text_len, result, created_ts, hit_count "
            "FROM sim_entries WHERE entry_id = ?",
            (entry_id,),
        ).fetchone()
        if row is None:
            return None
        return SimilarityEntry(
            entry_id=row[0],
            text=row[1],
            fingerprint=Fingerprint(
                method=FingerprintMethod(row[2]),
                value=self._fp_value_from_db(row[3]),
                text_len=row[4],
            ),
            result=row[5],
            created_ts=row[6],
            hit_count=row[7],
        )

    def increment_hits(self, entry_id: str) -> None:
        """Increment the hit_count for *entry_id* by 1."""
        self._conn.execute(
            "UPDATE sim_entries SET hit_count = hit_count + 1 WHERE entry_id = ?",
            (entry_id,),
        )
        self._conn.commit()

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        """Return aggregate statistics: total, total_hits, avg_hits."""
        row = self._conn.execute(
            "SELECT COUNT(*), COALESCE(SUM(hit_count), 0), COALESCE(AVG(hit_count), 0.0) "
            "FROM sim_entries"
        ).fetchone()
        return {
            "total": row[0],
            "total_hits": row[1],
            "avg_hits": row[2],
        }

    def count(self) -> int:
        """Return the total number of stored entries."""
        return self._conn.execute(
            "SELECT COUNT(*) FROM sim_entries"
        ).fetchone()[0]

    def evict_lru(self, max_size: int) -> int:
        """Remove oldest entries (by created_ts) beyond *max_size*. Returns rows deleted."""
        total = self.count()
        excess = total - max_size
        if excess <= 0:
            return 0
        cursor = self._conn.execute(
            """
            DELETE FROM sim_entries
            WHERE entry_id IN (
                SELECT entry_id FROM sim_entries
                ORDER BY created_ts ASC
                LIMIT ?
            )
            """,
            (excess,),
        )
        self._conn.commit()
        return cursor.rowcount

    def evict_expired(self, ttl_seconds: float, now: float = None) -> int:
        """Remove entries older than *ttl_seconds*. Returns rows deleted."""
        if now is None:
            now = time.time()
        cursor = self._conn.execute(
            "DELETE FROM sim_entries WHERE (? - created_ts) >= ?",
            (now, ttl_seconds),
        )
        self._conn.commit()
        return cursor.rowcount
