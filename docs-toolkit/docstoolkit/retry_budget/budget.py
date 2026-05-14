"""SQLite-backed per-key retry budget tracker."""
import sqlite3
import threading
import time
from dataclasses import dataclass
from typing import Optional


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS retry_budget (
    key TEXT PRIMARY KEY,
    attempts INTEGER DEFAULT 0,
    first_attempt REAL,
    last_attempt REAL
)
"""


@dataclass
class BudgetConfig:
    """Configuration for a RetryBudget."""

    max_retries: int          # max retries per key
    window: float             # seconds; budget resets after this time passes since first attempt
    backoff_base: float = 1.0 # base sleep multiplier (not used for actual sleeping, just stored)


class RetryBudget:
    """SQLite-backed per-key retry budget tracker.

    Thread-safe via an in-process threading.Lock.  Supports both in-memory
    (db_path=":memory:") and file-based databases.  WAL mode is enabled for
    file databases so concurrent readers are not blocked by writers.

    Budget logic
    ------------
    Each key has an *attempts* counter and a *first_attempt* timestamp.
    The budget is valid for *config.window* seconds from *first_attempt*.
    Once that window has elapsed the record is replaced (new window starts).

    - ``attempt(key)`` → True while attempts < max_retries; False when
      the budget is exhausted (counter is NOT incremented after exhaustion).
    - ``remaining(key)`` → max_retries − attempts (0-clamped); full budget
      if there is no record or the window has expired.
    - ``is_exhausted(key)`` → remaining == 0.
    - ``reset(key)`` → deletes the row, restoring a fresh budget.
    - ``all_keys()`` → list of all tracked keys.
    """

    def __init__(self, config: BudgetConfig, db_path: str = ":memory:"):
        self._config = config
        self._db_path = db_path
        self._lock = threading.Lock()
        # Keep a single persistent connection so :memory: DBs are not lost
        # when the connection object is garbage-collected between calls.
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(_CREATE_TABLE)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def attempt(self, key: str, now: Optional[float] = None) -> bool:
        """Record an attempt for *key*.

        Returns True if the attempt is within budget, False if the budget is
        exhausted.  When the window has expired the budget resets and this
        call counts as the first attempt in the new window (returns True).
        """
        if now is None:
            now = time.time()

        with self._lock:
            row = self._conn.execute(
                "SELECT attempts, first_attempt FROM retry_budget WHERE key = ?",
                (key,),
            ).fetchone()

            if row is None or (now - row[1]) > self._config.window:
                # No record, or window has expired → start fresh window.
                if self._config.max_retries <= 0:
                    return False
                self._conn.execute(
                    """
                    INSERT OR REPLACE INTO retry_budget (key, attempts, first_attempt, last_attempt)
                    VALUES (?, 1, ?, ?)
                    """,
                    (key, now, now),
                )
                self._conn.commit()
                return True

            attempts, first_attempt = row
            if attempts < self._config.max_retries:
                self._conn.execute(
                    """
                    UPDATE retry_budget
                    SET attempts = attempts + 1, last_attempt = ?
                    WHERE key = ?
                    """,
                    (now, key),
                )
                self._conn.commit()
                return True

            # Budget exhausted — do NOT increment.
            return False

    def remaining(self, key: str, now: Optional[float] = None) -> int:
        """Return the number of attempts remaining for *key* in the current window.

        Returns *max_retries* if there is no record for the key or if the
        window has expired.
        """
        if now is None:
            now = time.time()

        with self._lock:
            row = self._conn.execute(
                "SELECT attempts, first_attempt FROM retry_budget WHERE key = ?",
                (key,),
            ).fetchone()

        if row is None or (now - row[1]) > self._config.window:
            return self._config.max_retries

        attempts, _ = row
        return max(0, self._config.max_retries - attempts)

    def is_exhausted(self, key: str, now: Optional[float] = None) -> bool:
        """Return True if *key* has no remaining budget."""
        return self.remaining(key, now=now) == 0

    def reset(self, key: str) -> None:
        """Delete the attempt record for *key*, restoring its full budget."""
        with self._lock:
            self._conn.execute(
                "DELETE FROM retry_budget WHERE key = ?",
                (key,),
            )
            self._conn.commit()

    def all_keys(self) -> list:
        """Return a list of all keys that have been tracked."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT key FROM retry_budget ORDER BY key"
            ).fetchall()
        return [row[0] for row in rows]

    def close(self) -> None:
        """Close the underlying SQLite connection."""
        with self._lock:
            self._conn.close()
