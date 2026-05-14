"""HealthReport and HealthRegistry for managing and running health checks."""
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.health_checks.check import CheckResult, HealthCheck, HealthStatus


@dataclass
class HealthReport:
    """Aggregate result of running one or more health checks."""
    timestamp: float
    checks: list[CheckResult] = field(default_factory=list)

    def overall_status(self) -> HealthStatus:
        """UNHEALTHY if any check is UNHEALTHY, DEGRADED if any DEGRADED, else HEALTHY."""
        if any(c.status == HealthStatus.UNHEALTHY for c in self.checks):
            return HealthStatus.UNHEALTHY
        if any(c.status == HealthStatus.DEGRADED for c in self.checks):
            return HealthStatus.DEGRADED
        return HealthStatus.HEALTHY

    def healthy_count(self) -> int:
        return sum(1 for c in self.checks if c.status == HealthStatus.HEALTHY)

    def unhealthy_count(self) -> int:
        return sum(1 for c in self.checks if c.status == HealthStatus.UNHEALTHY)

    def degraded_count(self) -> int:
        return sum(1 for c in self.checks if c.status == HealthStatus.DEGRADED)

    def to_dict(self) -> dict:
        """Return a JSON-serialisable summary."""
        return {
            "timestamp": self.timestamp,
            "overall_status": self.overall_status().value,
            "total": len(self.checks),
            "healthy": self.healthy_count(),
            "degraded": self.degraded_count(),
            "unhealthy": self.unhealthy_count(),
            "checks": [
                {
                    "name": c.name,
                    "status": c.status.value,
                    "message": c.message,
                    "duration_ms": c.duration_ms,
                    "details": c.details,
                }
                for c in self.checks
            ],
        }


class HealthRegistry:
    """Stores named health checks and runs them on demand."""

    def __init__(self) -> None:
        self._checks: dict[str, HealthCheck] = {}

    def register(self, check: HealthCheck) -> None:
        """Register a check; silently overwrites any existing check with the same name."""
        self._checks[check.name] = check

    def unregister(self, name: str) -> bool:
        """Remove a check by name. Returns True if it existed, False otherwise."""
        if name in self._checks:
            del self._checks[name]
            return True
        return False

    def get(self, name: str) -> Optional[HealthCheck]:
        """Return the check with the given name, or None."""
        return self._checks.get(name)

    def names(self) -> list[str]:
        """Return a sorted list of registered check names."""
        return sorted(self._checks.keys())

    def run_one(self, name: str) -> CheckResult:
        """Run a single check by name. Raises KeyError if not found."""
        if name not in self._checks:
            raise KeyError(f"No health check registered with name {name!r}")
        return self._checks[name].run()

    def run_all(self, parallel: bool = False) -> HealthReport:
        """Run all registered checks and return a HealthReport.

        If ``parallel=True`` uses a ThreadPoolExecutor to run checks
        concurrently; results are collected in registration order.
        """
        timestamp = time.time()
        checks_list = list(self._checks.values())

        if not checks_list:
            return HealthReport(timestamp=timestamp, checks=[])

        if parallel:
            results: dict[str, CheckResult] = {}
            with ThreadPoolExecutor() as executor:
                future_to_name = {
                    executor.submit(check.run): check.name
                    for check in checks_list
                }
                for future in as_completed(future_to_name):
                    name = future_to_name[future]
                    try:
                        results[name] = future.result()
                    except Exception as exc:
                        results[name] = CheckResult(
                            name=name,
                            status=HealthStatus.UNHEALTHY,
                            message=str(exc),
                        )
            # Preserve deterministic ordering
            ordered = [results[check.name] for check in checks_list]
        else:
            ordered = [check.run() for check in checks_list]

        return HealthReport(timestamp=timestamp, checks=ordered)
