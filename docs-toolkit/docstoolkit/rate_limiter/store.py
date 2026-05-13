import sqlite3
import time
from docstoolkit.rate_limiter.limiter import RateLimitResult

_SCHEMA = """
CREATE TABLE IF NOT EXISTS rate_limit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT NOT NULL,
    allowed INTEGER NOT NULL,
    ts_monotonic REAL NOT NULL,
    remaining INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_key_ts ON rate_limit_log(key, ts_monotonic DESC);
"""


class RateLimitStore:
    """Persistent log of rate limit decisions (for audit)."""

    def __init__(self, db_path=None):
        self._path = str(db_path) if db_path else ":memory:"
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def record(self, result: RateLimitResult) -> None:
        """Log a rate limit decision."""
        self._conn.execute(
            "INSERT INTO rate_limit_log (key, allowed, ts_monotonic, remaining) "
            "VALUES (?, ?, ?, ?)",
            (result.key, int(result.allowed), time.monotonic(), result.remaining),
        )
        self._conn.commit()

    def denied_count(self, key: str) -> int:
        """Count denied requests for a key."""
        return self._conn.execute(
            "SELECT COUNT(*) FROM rate_limit_log WHERE key=? AND allowed=0",
            (key,)
        ).fetchone()[0]

    def allowed_count(self, key: str) -> int:
        """Count allowed requests for a key."""
        return self._conn.execute(
            "SELECT COUNT(*) FROM rate_limit_log WHERE key=? AND allowed=1",
            (key,)
        ).fetchone()[0]

    def total_count(self, key: str) -> int:
        """Count all requests for a key."""
        return self._conn.execute(
            "SELECT COUNT(*) FROM rate_limit_log WHERE key=?",
            (key,)
        ).fetchone()[0]

    def close(self):
        self._conn.close()
