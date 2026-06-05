"""Combined throttling + quota system per user/per-action with multiple windows.

Stdlib-only (``threading`` + ``dataclasses``). Deterministic via explicit
``now=`` argument on all time-sensitive methods.

Combines concepts from ``quota_tracker`` (E158) and ``doc_throttler`` (E268).
This adds per-action quotas with cascading windows (minute/hour/day/week/month).
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TimeWindow(Enum):
    """Time window granularities for cascading quotas."""

    MINUTE = "minute"
    HOUR = "hour"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"


_WINDOW_SECONDS = {
    TimeWindow.MINUTE: 60,
    TimeWindow.HOUR: 3600,
    TimeWindow.DAY: 86400,
    TimeWindow.WEEK: 604800,
    TimeWindow.MONTH: 2592000,
}


@dataclass
class QuotaSpec:
    """Specification of a per-action quota for a particular window."""

    action: str
    window: TimeWindow
    limit: int


@dataclass
class UsageRecord:
    """Mutable usage record for a (user, action, window) tuple."""

    user_id: str
    action: str
    window: TimeWindow
    count: int = 0
    window_start: float = 0.0
    last_op_at: float = 0.0


@dataclass
class QuotaCheckResult:
    """Result of checking a single quota for a (user, action, window)."""

    allowed: bool
    user_id: str
    action: str
    window: TimeWindow
    count: int
    limit: int
    remaining: int
    reset_at: float
    reason: Optional[str] = None


class DocThrottleQuota:
    """Per-user / per-action quotas with cascading time windows.

    Quotas are configured via :py:meth:`set_quota`. For each ``action`` you may
    register multiple windows (e.g. 10/minute and 100/hour). On :py:meth:`consume`
    *all* registered windows for the action are checked atomically and updated
    only if all are within their limits.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # quotas[action][window] = QuotaSpec
        self._quotas: dict[str, dict[TimeWindow, QuotaSpec]] = {}
        # usage[(user_id, action, window)] = UsageRecord
        self._usage: dict[tuple[str, str, TimeWindow], UsageRecord] = {}

    # ------------------------------------------------------------------ quotas

    def set_quota(self, action: str, window: TimeWindow, limit: int) -> QuotaSpec:
        """Register or replace a quota for ``(action, window)``."""
        if limit < 0:
            raise ValueError("limit must be >= 0")
        spec = QuotaSpec(action=action, window=window, limit=limit)
        with self._lock:
            self._quotas.setdefault(action, {})[window] = spec
        return spec

    def remove_quota(self, action: str, window: TimeWindow) -> bool:
        """Remove the quota for ``(action, window)``. Returns True if removed."""
        with self._lock:
            action_map = self._quotas.get(action)
            if not action_map or window not in action_map:
                return False
            del action_map[window]
            if not action_map:
                del self._quotas[action]
            return True

    def quotas_for_action(self, action: str) -> list[QuotaSpec]:
        """Return all :class:`QuotaSpec` configured for ``action``."""
        with self._lock:
            action_map = self._quotas.get(action, {})
            return list(action_map.values())

    def all_actions(self) -> list[str]:
        """Return all actions with at least one configured quota."""
        with self._lock:
            return list(self._quotas.keys())

    @property
    def total_quotas(self) -> int:
        """Total number of (action, window) quota entries."""
        with self._lock:
            return sum(len(m) for m in self._quotas.values())

    # ----------------------------------------------------------------- internal

    @staticmethod
    def _resolve_now(now: Optional[float]) -> float:
        return time.time() if now is None else float(now)

    def _maybe_reset(self, rec: UsageRecord, now: float) -> None:
        """Reset the usage record if its window has elapsed."""
        window_seconds = _WINDOW_SECONDS[rec.window]
        if (now - rec.window_start) >= window_seconds:
            rec.count = 0
            rec.window_start = now

    def _get_or_create_usage(
        self, user_id: str, action: str, window: TimeWindow, now: float
    ) -> UsageRecord:
        key = (user_id, action, window)
        rec = self._usage.get(key)
        if rec is None:
            rec = UsageRecord(
                user_id=user_id,
                action=action,
                window=window,
                count=0,
                window_start=now,
                last_op_at=0.0,
            )
            self._usage[key] = rec
        else:
            self._maybe_reset(rec, now)
        return rec

    def _build_result(
        self,
        rec: UsageRecord,
        spec: QuotaSpec,
        allowed: bool,
        reason: Optional[str],
    ) -> QuotaCheckResult:
        remaining = max(0, spec.limit - rec.count)
        reset_at = rec.window_start + _WINDOW_SECONDS[rec.window]
        return QuotaCheckResult(
            allowed=allowed,
            user_id=rec.user_id,
            action=rec.action,
            window=rec.window,
            count=rec.count,
            limit=spec.limit,
            remaining=remaining,
            reset_at=reset_at,
            reason=reason,
        )

    # ------------------------------------------------------------ check/consume

    def check(
        self,
        user_id: str,
        action: str,
        now: Optional[float] = None,
    ) -> list[QuotaCheckResult]:
        """Return a result per configured quota for ``action`` (no mutation).

        If no quotas are configured for the action, returns an empty list.
        """
        t = self._resolve_now(now)
        results: list[QuotaCheckResult] = []
        with self._lock:
            action_map = self._quotas.get(action, {})
            for window, spec in action_map.items():
                rec = self._get_or_create_usage(user_id, action, window, t)
                allowed = rec.count < spec.limit
                reason = None if allowed else "quota_exceeded"
                results.append(self._build_result(rec, spec, allowed, reason))
        return results

    def consume(
        self,
        user_id: str,
        action: str,
        now: Optional[float] = None,
    ) -> tuple[bool, list[QuotaCheckResult]]:
        """Try to consume one op against all quotas of ``action`` (all-or-nothing).

        - If the action has no configured quotas, returns ``(True, [])``.
        - If any quota would be exceeded, returns ``(False, results)`` without
          incrementing any counter.
        - Otherwise increments all counters and returns ``(True, results)``.
        """
        t = self._resolve_now(now)
        with self._lock:
            action_map = self._quotas.get(action, {})
            if not action_map:
                return True, []

            records: list[tuple[UsageRecord, QuotaSpec]] = []
            blocking: Optional[QuotaSpec] = None
            for window, spec in action_map.items():
                rec = self._get_or_create_usage(user_id, action, window, t)
                records.append((rec, spec))
                if rec.count >= spec.limit and blocking is None:
                    blocking = spec

            if blocking is not None:
                results = [
                    self._build_result(
                        rec,
                        spec,
                        allowed=rec.count < spec.limit,
                        reason=None if rec.count < spec.limit else "quota_exceeded",
                    )
                    for rec, spec in records
                ]
                return False, results

            # All within limits — increment.
            for rec, _spec in records:
                rec.count += 1
                rec.last_op_at = t

            results = [
                self._build_result(
                    rec,
                    spec,
                    allowed=rec.count <= spec.limit,
                    reason=None,
                )
                for rec, spec in records
            ]
            return True, results

    # ----------------------------------------------------------------- queries

    def usage(
        self,
        user_id: str,
        action: str,
        window: TimeWindow,
        now: Optional[float] = None,
    ) -> Optional[UsageRecord]:
        """Return a snapshot of the (user, action, window) usage record.

        Returns ``None`` if no record exists yet. Applies window reset before
        returning. Returns a copy, not the live record.
        """
        t = self._resolve_now(now)
        with self._lock:
            key = (user_id, action, window)
            rec = self._usage.get(key)
            if rec is None:
                return None
            self._maybe_reset(rec, t)
            return UsageRecord(
                user_id=rec.user_id,
                action=rec.action,
                window=rec.window,
                count=rec.count,
                window_start=rec.window_start,
                last_op_at=rec.last_op_at,
            )

    def reset_user(self, user_id: str, action: str = None) -> int:
        """Remove usage records for ``user_id``. If ``action`` is None, remove all.

        Returns the number of records removed.
        """
        with self._lock:
            to_remove = [
                key
                for key in self._usage
                if key[0] == user_id and (action is None or key[1] == action)
            ]
            for key in to_remove:
                del self._usage[key]
            return len(to_remove)

    def users_at_limit(
        self,
        action: str,
        window: TimeWindow,
        now: Optional[float] = None,
    ) -> list[str]:
        """Return user_ids currently at or above the configured limit.

        If the quota is not configured, returns an empty list.
        """
        t = self._resolve_now(now)
        with self._lock:
            spec = self._quotas.get(action, {}).get(window)
            if spec is None:
                return []
            result: list[str] = []
            for (uid, act, win), rec in self._usage.items():
                if act != action or win != window:
                    continue
                # Apply window reset to give an accurate "current" snapshot.
                self._maybe_reset(rec, t)
                if rec.count >= spec.limit:
                    result.append(uid)
            return result

    def top_users(
        self,
        action: str,
        top_k: int = 10,
        now: Optional[float] = None,
    ) -> list[tuple[str, int]]:
        """Return ``(user_id, count)`` pairs ranked by total count across windows.

        The count aggregates the user's records for ``action`` across all
        configured windows.
        """
        t = self._resolve_now(now)
        with self._lock:
            totals: dict[str, int] = {}
            for (uid, act, _win), rec in self._usage.items():
                if act != action:
                    continue
                self._maybe_reset(rec, t)
                totals[uid] = totals.get(uid, 0) + rec.count
            ranked = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
            return ranked[: max(0, int(top_k))]

    # ----------------------------------------------------------- maintenance

    def cleanup(self, now: Optional[float] = None) -> int:
        """Remove usage records whose window has expired and which are empty.

        A record is removed when its window has elapsed and ``count == 0`` after
        the implicit reset (i.e., truly idle). Returns the number of records
        removed.
        """
        t = self._resolve_now(now)
        removed = 0
        with self._lock:
            to_remove: list[tuple[str, str, TimeWindow]] = []
            for key, rec in self._usage.items():
                window_seconds = _WINDOW_SECONDS[rec.window]
                # If the window has elapsed, the next call would reset to 0,
                # so the record is effectively empty.
                if (t - rec.window_start) >= window_seconds:
                    to_remove.append(key)
            for key in to_remove:
                del self._usage[key]
                removed += 1
        return removed

    def clear(self) -> None:
        """Remove all quotas and all usage records."""
        with self._lock:
            self._quotas.clear()
            self._usage.clear()
