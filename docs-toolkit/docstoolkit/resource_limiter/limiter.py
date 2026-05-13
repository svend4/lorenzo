"""Resource limiter: track and enforce per-namespace usage limits (E112).

SQLite-backed, thread-safe, supports time-windowed limits for any resource
type (API calls, bytes, CPU time, custom units).
"""
import sqlite3
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional

# --------------------------------------------------------------------------- #
#  Public types                                                                 #
# --------------------------------------------------------------------------- #

class LimitResult(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    WARNING = "warning"   # usage >= warn_threshold but < limit


@dataclass
class ResourceLimit:
    """Configuration for a single resource limit."""
    resource: str          # e.g. "api_calls", "bytes", "cpu_ms"
    limit: float           # hard limit per window
    window: float          # window duration in seconds
    warn_threshold: float | None = None   # optional warning level


@dataclass
class UsageRecord:
    """Result of a consume() call."""
    namespace: str
    resource: str
    used: float
    limit: float
    window_start: float
    result: LimitResult


# --------------------------------------------------------------------------- #
#  SQLite schema                                                                #
# --------------------------------------------------------------------------- #

_SCHEMA = """
CREATE TABLE IF NOT EXISTS usage (
    namespace   TEXT NOT NULL,
    resource    TEXT NOT NULL,
    used        REAL DEFAULT 0,
    window_start REAL,
    PRIMARY KEY (namespace, resource)
);
"""


# --------------------------------------------------------------------------- #
#  ResourceLimiter                                                              #
# --------------------------------------------------------------------------- #

class ResourceLimiter:
    """Thread-safe, SQLite-backed resource usage limiter.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``":memory:"`` (default) for an
        in-process, in-memory database.
    now_fn:
        Callable that returns the current timestamp as a float (seconds).
        Defaults to :func:`time.time`.  Inject a virtual clock in tests.
    """

    def __init__(
        self,
        db_path: str = ":memory:",
        now_fn: Callable[[], float] | None = None,
    ) -> None:
        self._now = now_fn if now_fn is not None else time.time
        self._lock = threading.Lock()
        self._limits: dict[str, ResourceLimit] = {}

        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    # ---------------------------------------------------------------------- #
    #  Configuration                                                           #
    # ---------------------------------------------------------------------- #

    def add_limit(self, limit: ResourceLimit) -> None:
        """Register or update a resource limit."""
        with self._lock:
            self._limits[limit.resource] = limit

    # ---------------------------------------------------------------------- #
    #  Core API                                                                #
    # ---------------------------------------------------------------------- #

    def consume(
        self,
        namespace: str,
        resource: str,
        amount: float = 1.0,
    ) -> UsageRecord:
        """Record consumption of *amount* units of *resource* for *namespace*.

        Behaviour
        ---------
        * If no limit is registered for *resource*, returns ALLOWED with
          ``used=amount`` (usage is still tracked so ``usage()`` returns it).
        * Window resets when ``now > window_start + window``.
        * Returns DENIED if ``used + amount > limit`` — usage is **not**
          updated.
        * Returns WARNING if ``warn_threshold`` is set and
          ``used + amount >= warn_threshold``.
        * Returns ALLOWED otherwise.
        """
        with self._lock:
            now = self._now()
            cfg = self._limits.get(resource)
            limit_val = cfg.limit if cfg is not None else float("inf")

            row = self._conn.execute(
                "SELECT used, window_start FROM usage "
                "WHERE namespace = ? AND resource = ?",
                (namespace, resource),
            ).fetchone()

            # Determine whether we are in an active window
            if row is None:
                current_used = 0.0
                window_start = now
            else:
                current_used, window_start = row
                # Window expired?
                if cfg is not None and now > window_start + cfg.window:
                    current_used = 0.0
                    window_start = now

            # Enforce hard limit (only when a limit is configured)
            if cfg is not None and current_used + amount > limit_val:
                # Do NOT update usage
                return UsageRecord(
                    namespace=namespace,
                    resource=resource,
                    used=current_used,
                    limit=limit_val,
                    window_start=window_start,
                    result=LimitResult.DENIED,
                )

            # Commit the consumption
            new_used = current_used + amount
            self._conn.execute(
                "INSERT INTO usage (namespace, resource, used, window_start) "
                "VALUES (?, ?, ?, ?) "
                "ON CONFLICT(namespace, resource) DO UPDATE SET "
                "used = excluded.used, window_start = excluded.window_start",
                (namespace, resource, new_used, window_start),
            )
            self._conn.commit()

            # Determine result level
            if (
                cfg is not None
                and cfg.warn_threshold is not None
                and new_used >= cfg.warn_threshold
            ):
                result = LimitResult.WARNING
            else:
                result = LimitResult.ALLOWED

            return UsageRecord(
                namespace=namespace,
                resource=resource,
                used=new_used,
                limit=limit_val,
                window_start=window_start,
                result=result,
            )

    def usage(self, namespace: str, resource: str) -> float:
        """Return current usage for *namespace*/*resource* in the current window.

        Returns ``0.0`` if no record exists or the window has expired.
        """
        with self._lock:
            now = self._now()
            cfg = self._limits.get(resource)
            row = self._conn.execute(
                "SELECT used, window_start FROM usage "
                "WHERE namespace = ? AND resource = ?",
                (namespace, resource),
            ).fetchone()
            if row is None:
                return 0.0
            used, window_start = row
            if cfg is not None and now > window_start + cfg.window:
                return 0.0
            return used

    def reset(self, namespace: str, resource: str) -> None:
        """Reset usage for *namespace*/*resource* to zero."""
        with self._lock:
            self._conn.execute(
                "DELETE FROM usage WHERE namespace = ? AND resource = ?",
                (namespace, resource),
            )
            self._conn.commit()

    def reset_namespace(self, namespace: str) -> int:
        """Reset all resources for *namespace*.

        Returns the number of rows deleted.
        """
        with self._lock:
            cur = self._conn.execute(
                "DELETE FROM usage WHERE namespace = ?",
                (namespace,),
            )
            self._conn.commit()
            return cur.rowcount

    def remaining(self, namespace: str, resource: str) -> float:
        """Return remaining allowance for *namespace*/*resource*.

        Returns the full limit if no usage row exists, if the window has
        expired, or if no limit is defined for *resource*.
        """
        with self._lock:
            now = self._now()
            cfg = self._limits.get(resource)
            if cfg is None:
                return float("inf")

            row = self._conn.execute(
                "SELECT used, window_start FROM usage "
                "WHERE namespace = ? AND resource = ?",
                (namespace, resource),
            ).fetchone()

            if row is None:
                return cfg.limit
            used, window_start = row
            if now > window_start + cfg.window:
                return cfg.limit
            return max(0.0, cfg.limit - used)

    # ---------------------------------------------------------------------- #
    #  Lifecycle                                                               #
    # ---------------------------------------------------------------------- #

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()
