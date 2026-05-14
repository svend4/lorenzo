"""E420 DocHealthMonitor — monitor document health metrics.

Pure stdlib implementation. Thread-safe via :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional

_VALID_SEVERITIES = ("info", "warning", "critical")


@dataclass
class HealthCheck:
    """A single health check definition.

    The ``check`` callable should accept ``(doc_id, content)`` and return
    ``True`` when the document is considered healthy for this check.
    """

    check_id: str
    name: str
    severity: str = "info"
    enabled: bool = True
    check: object = None  # Callable[[str, str], bool]


@dataclass
class HealthResult:
    """Outcome of a single check on a single doc."""

    doc_id: str
    check_id: str
    healthy: bool
    severity: str
    checked_at: float = 0.0
    message: str = ""


@dataclass
class MonitorStats:
    """Aggregate statistics from the monitor."""

    total_checks: int
    enabled_checks: int
    total_evaluations: int
    unhealthy_count: int


class DocHealthMonitor:
    """Monitor document health using registered checks.

    Thread-safe: all mutating and reading operations acquire an internal lock.
    """

    def __init__(self) -> None:
        self._checks: dict[str, HealthCheck] = {}
        self._results: dict[tuple, HealthResult] = {}
        self._total_evaluations: int = 0
        self._lock = threading.Lock()

    # ---- check management ---------------------------------------------------

    def register_check(self, check: HealthCheck) -> None:
        """Register (or replace) a health check by ``check_id``."""
        if not isinstance(check, HealthCheck):
            raise TypeError("check must be a HealthCheck instance")
        if not check.check_id:
            raise ValueError("check_id must be a non-empty string")
        if check.severity not in _VALID_SEVERITIES:
            raise ValueError(
                f"severity must be one of {_VALID_SEVERITIES}, got {check.severity!r}"
            )
        with self._lock:
            self._checks[check.check_id] = check

    def unregister_check(self, check_id: str) -> bool:
        """Remove a check and any related results. Returns True if removed."""
        with self._lock:
            if check_id not in self._checks:
                return False
            del self._checks[check_id]
            # Remove related results
            to_remove = [key for key in self._results if key[1] == check_id]
            for key in to_remove:
                del self._results[key]
            return True

    def enable_check(self, check_id: str) -> bool:
        with self._lock:
            check = self._checks.get(check_id)
            if check is None:
                return False
            check.enabled = True
            return True

    def disable_check(self, check_id: str) -> bool:
        with self._lock:
            check = self._checks.get(check_id)
            if check is None:
                return False
            check.enabled = False
            return True

    def get_check(self, check_id: str) -> Optional[HealthCheck]:
        with self._lock:
            return self._checks.get(check_id)

    def list_checks(self) -> list[HealthCheck]:
        """All registered checks, sorted by ``check_id``."""
        with self._lock:
            return sorted(self._checks.values(), key=lambda c: c.check_id)

    # ---- evaluation ---------------------------------------------------------

    def evaluate(
        self,
        doc_id: str,
        content: str,
        check_ids: Optional[list[str]] = None,
        now: Optional[float] = None,
    ) -> list[HealthResult]:
        """Apply enabled checks to ``content``.

        If ``check_ids`` is given, only those checks are considered (still
        skipping any that are disabled or unknown). Returns a list of
        :class:`HealthResult` in the order checks were executed (sorted by
        check_id for determinism). Exceptions from check callables are caught
        and produce an unhealthy result with the error message.
        """
        timestamp = now if now is not None else time.time()

        with self._lock:
            if check_ids is None:
                candidates = list(self._checks.values())
            else:
                candidates = [
                    self._checks[cid] for cid in check_ids if cid in self._checks
                ]
            # Filter enabled and sort
            selected = sorted(
                (c for c in candidates if c.enabled),
                key=lambda c: c.check_id,
            )
            # Snapshot to avoid running callbacks while holding the lock.
            snapshot = [
                (c.check_id, c.severity, c.check) for c in selected
            ]

        results: list[HealthResult] = []
        for check_id, severity, callback in snapshot:
            healthy = True
            message = ""
            if callback is None:
                healthy = True
                message = "no check callable; treated as healthy"
            else:
                try:
                    healthy = bool(callback(doc_id, content))
                except Exception as exc:  # noqa: BLE001
                    healthy = False
                    message = f"check raised: {type(exc).__name__}: {exc}"

            result = HealthResult(
                doc_id=doc_id,
                check_id=check_id,
                healthy=healthy,
                severity=severity,
                checked_at=timestamp,
                message=message,
            )
            results.append(result)

        # Persist results under lock
        with self._lock:
            for r in results:
                self._results[(r.doc_id, r.check_id)] = r
                self._total_evaluations += 1

        return results

    # ---- result access ------------------------------------------------------

    def latest_result(self, doc_id: str, check_id: str) -> Optional[HealthResult]:
        with self._lock:
            return self._results.get((doc_id, check_id))

    def results_for_doc(self, doc_id: str) -> list[HealthResult]:
        """All latest results for a doc, sorted by ``check_id``."""
        with self._lock:
            matching = [
                r for (did, _cid), r in self._results.items() if did == doc_id
            ]
        return sorted(matching, key=lambda r: r.check_id)

    def unhealthy_docs(self, severity: Optional[str] = None) -> list[str]:
        """Doc IDs with at least one unhealthy result.

        Optional ``severity`` filter restricts to results of that severity.
        Result is sorted alphabetically.
        """
        if severity is not None and severity not in _VALID_SEVERITIES:
            raise ValueError(
                f"severity must be one of {_VALID_SEVERITIES}, got {severity!r}"
            )
        with self._lock:
            doc_ids = set()
            for r in self._results.values():
                if r.healthy:
                    continue
                if severity is not None and r.severity != severity:
                    continue
                doc_ids.add(r.doc_id)
        return sorted(doc_ids)

    def health_score(self, doc_id: str) -> float:
        """Fraction of healthy results for ``doc_id``.

        Returns 1.0 when no checks have been evaluated for the doc.
        """
        with self._lock:
            doc_results = [
                r for (did, _cid), r in self._results.items() if did == doc_id
            ]
        if not doc_results:
            return 1.0
        passed = sum(1 for r in doc_results if r.healthy)
        return passed / len(doc_results)

    def clear_results(self) -> int:
        """Drop all stored results. Returns the number cleared."""
        with self._lock:
            count = len(self._results)
            self._results.clear()
            return count

    # ---- stats --------------------------------------------------------------

    def stats(self) -> MonitorStats:
        with self._lock:
            total_checks = len(self._checks)
            enabled_checks = sum(1 for c in self._checks.values() if c.enabled)
            unhealthy = sum(1 for r in self._results.values() if not r.healthy)
            return MonitorStats(
                total_checks=total_checks,
                enabled_checks=enabled_checks,
                total_evaluations=self._total_evaluations,
                unhealthy_count=unhealthy,
            )
