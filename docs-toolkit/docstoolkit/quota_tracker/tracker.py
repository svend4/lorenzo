"""QuotaTracker — tracks consumption against quotas per-key with reset windows.

Stdlib-only (`threading`). Time is provided externally via `now=` to keep
behavior deterministic and testable.
"""
from __future__ import annotations

import math
import threading
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Tuple


class QuotaPeriod(Enum):
    """Window periods for quotas."""

    SECOND = "second"
    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    FOREVER = "forever"


_PERIOD_SECONDS: Dict[QuotaPeriod, float] = {
    QuotaPeriod.SECOND: 1.0,
    QuotaPeriod.MINUTE: 60.0,
    QuotaPeriod.HOUR: 3600.0,
    QuotaPeriod.DAY: 86400.0,
    QuotaPeriod.WEEK: 604800.0,
    QuotaPeriod.MONTH: 2592000.0,  # 30 days
    QuotaPeriod.FOREVER: math.inf,
}


def _period_seconds(period: QuotaPeriod) -> float:
    return _PERIOD_SECONDS[period]


class QuotaError(Exception):
    """Raised on quota-related errors."""


@dataclass
class QuotaLimit:
    """Defines the quota for one key."""

    key: str
    period: QuotaPeriod
    max_units: int


@dataclass
class QuotaStatus:
    """Current consumption snapshot for a quota key."""

    key: str
    period: QuotaPeriod
    used: int
    remaining: int
    max_units: int
    reset_at: float

    @property
    def is_exhausted(self) -> bool:
        return self.used >= self.max_units

    @property
    def utilization(self) -> float:
        if self.max_units <= 0:
            # No-budget bucket: treat as fully utilized when anything used,
            # otherwise zero.
            return 1.0 if self.used > 0 else 0.0
        return self.used / self.max_units


class QuotaTracker:
    """Tracks usage per key against per-period limits.

    State stored as: {key: [used, window_start, limit]}.
    Thread-safe via a single re-entrant lock.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # key -> [used, window_start, QuotaLimit]
        self._state: Dict[str, List] = {}

    # ------------------------------------------------------------------ #
    # Limit management
    # ------------------------------------------------------------------ #
    def set_limit(
        self,
        key: str,
        period: QuotaPeriod,
        max_units: int,
    ) -> QuotaLimit:
        """Set or replace the limit for a key. Resets the window."""
        if not isinstance(period, QuotaPeriod):
            raise QuotaError(f"period must be QuotaPeriod, got {type(period)!r}")
        if max_units < 0:
            raise QuotaError(f"max_units must be >= 0, got {max_units}")
        limit = QuotaLimit(key=key, period=period, max_units=max_units)
        with self._lock:
            self._state[key] = [0, 0.0, limit]
        return limit

    # ------------------------------------------------------------------ #
    # Window helpers (must be called under lock)
    # ------------------------------------------------------------------ #
    def _maybe_reset_window(self, entry: List, now: float) -> None:
        """Reset window if it expired. Mutates `entry` in place."""
        limit: QuotaLimit = entry[2]
        if limit.period == QuotaPeriod.FOREVER:
            return
        window_start = entry[1]
        period_s = _period_seconds(limit.period)
        if now - window_start >= period_s:
            entry[0] = 0
            entry[1] = now

    def _status_locked(self, entry: List, now: float) -> QuotaStatus:
        limit: QuotaLimit = entry[2]
        used: int = entry[0]
        window_start: float = entry[1]
        if limit.period == QuotaPeriod.FOREVER:
            reset_at = math.inf
        else:
            reset_at = window_start + _period_seconds(limit.period)
        remaining = max(0, limit.max_units - used)
        return QuotaStatus(
            key=limit.key,
            period=limit.period,
            used=used,
            remaining=remaining,
            max_units=limit.max_units,
            reset_at=reset_at,
        )

    # ------------------------------------------------------------------ #
    # Consume / check
    # ------------------------------------------------------------------ #
    def consume(self, key: str, units: int = 1, now: float = 0.0) -> bool:
        """Consume `units` from the bucket. Returns True if allowed."""
        if units < 0:
            raise QuotaError(f"units must be >= 0, got {units}")
        with self._lock:
            entry = self._state.get(key)
            if entry is None:
                # No limit configured → not allowed by quota system.
                return False
            self._maybe_reset_window(entry, now)
            limit: QuotaLimit = entry[2]
            if entry[0] + units > limit.max_units:
                return False
            entry[0] += units
            return True

    def check(self, key: str, units: int = 1, now: float = 0.0) -> bool:
        """Non-mutating check. Does not advance the window either."""
        if units < 0:
            raise QuotaError(f"units must be >= 0, got {units}")
        with self._lock:
            entry = self._state.get(key)
            if entry is None:
                return False
            limit: QuotaLimit = entry[2]
            # Compute view that would be after potential reset, but don't mutate.
            used = entry[0]
            window_start = entry[1]
            if limit.period != QuotaPeriod.FOREVER:
                if now - window_start >= _period_seconds(limit.period):
                    used = 0
            return used + units <= limit.max_units

    def try_consume(
        self,
        key: str,
        units: int = 1,
        now: float = 0.0,
    ) -> Tuple[bool, QuotaStatus]:
        """Attempt to consume and return (success, current_status).

        Status reflects state AFTER the attempt (whether or not it succeeded).
        Raises QuotaError if the key has no limit set.
        """
        if units < 0:
            raise QuotaError(f"units must be >= 0, got {units}")
        with self._lock:
            entry = self._state.get(key)
            if entry is None:
                raise QuotaError(f"no quota set for key {key!r}")
            self._maybe_reset_window(entry, now)
            limit: QuotaLimit = entry[2]
            success = entry[0] + units <= limit.max_units
            if success:
                entry[0] += units
            return success, self._status_locked(entry, now)

    # ------------------------------------------------------------------ #
    # Read-only helpers
    # ------------------------------------------------------------------ #
    def status(self, key: str, now: float = 0.0) -> Optional[QuotaStatus]:
        with self._lock:
            entry = self._state.get(key)
            if entry is None:
                return None
            self._maybe_reset_window(entry, now)
            return self._status_locked(entry, now)

    def total_used(self, key: str, now: float = 0.0) -> int:
        """Used count for current window (after possible reset)."""
        with self._lock:
            entry = self._state.get(key)
            if entry is None:
                return 0
            self._maybe_reset_window(entry, now)
            return entry[0]

    def all_keys(self) -> List[str]:
        with self._lock:
            return list(self._state.keys())

    # ------------------------------------------------------------------ #
    # Reset
    # ------------------------------------------------------------------ #
    def reset(self, key: str) -> bool:
        """Reset usage for a single key. Returns False if key unknown."""
        with self._lock:
            entry = self._state.get(key)
            if entry is None:
                return False
            entry[0] = 0
            entry[1] = 0.0
            return True

    def reset_all(self) -> int:
        """Reset all keys. Returns number of keys reset."""
        with self._lock:
            n = 0
            for entry in self._state.values():
                entry[0] = 0
                entry[1] = 0.0
                n += 1
            return n
