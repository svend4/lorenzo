"""Document health monitoring core (E271).

Configurable health checks with status aggregation, intervals, and history.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional


class HealthStatus(str, Enum):
    """Status of a health check or overall system."""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class CheckResult:
    """Result of a single health check execution."""

    check_name: str
    status: HealthStatus
    message: str
    details: dict = field(default_factory=dict)
    timestamp: float = 0.0
    duration_ms: float = 0.0


@dataclass
class HealthCheck:
    """Registered health check configuration."""

    name: str
    check_func: Callable[[], CheckResult]
    interval_seconds: float = 60.0
    enabled: bool = True
    critical: bool = True


@dataclass
class HealthReport:
    """Aggregate report from running all health checks."""

    overall_status: HealthStatus
    checks: list
    timestamp: float
    degraded_count: int
    unhealthy_count: int
    healthy_count: int


class DocHealth:
    """Health monitor with configurable checks and status aggregation."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._checks: dict[str, HealthCheck] = {}
        self._last_results: dict[str, CheckResult] = {}
        self._history: dict[str, list[CheckResult]] = {}
        self._last_run: dict[str, float] = {}

    # ---- Registration -------------------------------------------------
    def register_check(
        self,
        name: str,
        check_func: Callable[[], CheckResult],
        interval_seconds: float = 60.0,
        critical: bool = True,
    ) -> HealthCheck:
        """Register a new health check."""
        check = HealthCheck(
            name=name,
            check_func=check_func,
            interval_seconds=interval_seconds,
            enabled=True,
            critical=critical,
        )
        with self._lock:
            self._checks[name] = check
            self._history.setdefault(name, [])
        return check

    def unregister_check(self, name: str) -> bool:
        """Remove a registered check. Returns True if removed."""
        with self._lock:
            if name not in self._checks:
                return False
            del self._checks[name]
            self._last_results.pop(name, None)
            self._history.pop(name, None)
            self._last_run.pop(name, None)
            return True

    def enable_check(self, name: str) -> bool:
        """Enable a registered check."""
        with self._lock:
            check = self._checks.get(name)
            if check is None:
                return False
            check.enabled = True
            return True

    def disable_check(self, name: str) -> bool:
        """Disable a registered check."""
        with self._lock:
            check = self._checks.get(name)
            if check is None:
                return False
            check.enabled = False
            return True

    # ---- Execution ----------------------------------------------------
    def run_check(
        self, name: str, now: Optional[float] = None
    ) -> Optional[CheckResult]:
        """Run a single check by name. Returns None if not registered."""
        with self._lock:
            check = self._checks.get(name)
        if check is None:
            return None

        ts = time.time() if now is None else now
        start = time.perf_counter()
        try:
            result = check.check_func()
            if not isinstance(result, CheckResult):
                # Defensive: coerce
                result = CheckResult(
                    check_name=name,
                    status=HealthStatus.UNKNOWN,
                    message="check_func did not return CheckResult",
                )
        except Exception as exc:  # noqa: BLE001
            result = CheckResult(
                check_name=name,
                status=HealthStatus.UNKNOWN,
                message=str(exc),
            )
        duration_ms = (time.perf_counter() - start) * 1000.0

        # Fill in metadata
        result.check_name = name
        result.timestamp = ts
        result.duration_ms = duration_ms

        with self._lock:
            self._last_results[name] = result
            self._history.setdefault(name, []).append(result)
            self._last_run[name] = ts

        return result

    def run_all(self, now: Optional[float] = None) -> HealthReport:
        """Run all enabled checks and return aggregate report."""
        ts = time.time() if now is None else now
        with self._lock:
            names = [n for n, c in self._checks.items() if c.enabled]

        results: list[CheckResult] = []
        for name in names:
            res = self.run_check(name, now=ts)
            if res is not None:
                results.append(res)

        healthy = sum(1 for r in results if r.status == HealthStatus.HEALTHY)
        degraded = sum(1 for r in results if r.status == HealthStatus.DEGRADED)
        unhealthy = sum(1 for r in results if r.status == HealthStatus.UNHEALTHY)

        overall = self._aggregate_status(results)

        return HealthReport(
            overall_status=overall,
            checks=results,
            timestamp=ts,
            degraded_count=degraded,
            unhealthy_count=unhealthy,
            healthy_count=healthy,
        )

    # ---- Aggregation helpers -----------------------------------------
    def _aggregate_status(self, results: list[CheckResult]) -> HealthStatus:
        """Compute overall status from check results."""
        if not results:
            return HealthStatus.HEALTHY

        any_critical_unhealthy = False
        any_degraded = False
        for r in results:
            check = self._checks.get(r.check_name)
            critical = check.critical if check else True
            if r.status == HealthStatus.UNHEALTHY and critical:
                any_critical_unhealthy = True
            if r.status == HealthStatus.DEGRADED:
                any_degraded = True
            if r.status == HealthStatus.UNHEALTHY and not critical:
                # Non-critical unhealthy degrades overall
                any_degraded = True

        if any_critical_unhealthy:
            return HealthStatus.UNHEALTHY
        if any_degraded:
            return HealthStatus.DEGRADED
        return HealthStatus.HEALTHY

    def overall_status(self) -> HealthStatus:
        """Return aggregated status from last results."""
        with self._lock:
            results = list(self._last_results.values())
        return self._aggregate_status(results)

    # ---- Query --------------------------------------------------------
    def last_result(self, name: str) -> Optional[CheckResult]:
        """Return last result for a check, or None."""
        with self._lock:
            return self._last_results.get(name)

    def history(self, name: str, limit: Optional[int] = None) -> list[CheckResult]:
        """Return history of results for a check (most recent last)."""
        with self._lock:
            entries = list(self._history.get(name, []))
        if limit is not None and limit >= 0:
            return entries[-limit:] if limit > 0 else []
        return entries

    def checks(self, enabled_only: bool = False) -> list[HealthCheck]:
        """Return registered checks."""
        with self._lock:
            items = list(self._checks.values())
        if enabled_only:
            items = [c for c in items if c.enabled]
        return items

    def unhealthy_checks(self) -> list[CheckResult]:
        """Return last results where status is UNHEALTHY."""
        with self._lock:
            return [
                r for r in self._last_results.values()
                if r.status == HealthStatus.UNHEALTHY
            ]

    def degraded_checks(self) -> list[CheckResult]:
        """Return last results where status is DEGRADED."""
        with self._lock:
            return [
                r for r in self._last_results.values()
                if r.status == HealthStatus.DEGRADED
            ]

    def should_run(self, name: str, now: Optional[float] = None) -> bool:
        """Return True if check is due based on interval."""
        with self._lock:
            check = self._checks.get(name)
            if check is None:
                return False
            last = self._last_run.get(name)
        if last is None:
            return True
        ts = time.time() if now is None else now
        return (ts - last) > check.interval_seconds

    # ---- Properties / lifecycle --------------------------------------
    @property
    def total_checks(self) -> int:
        """Number of registered checks."""
        with self._lock:
            return len(self._checks)

    def clear(self) -> None:
        """Remove all checks and state."""
        with self._lock:
            self._checks.clear()
            self._last_results.clear()
            self._history.clear()
            self._last_run.clear()
