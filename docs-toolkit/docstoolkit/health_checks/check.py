"""Health check primitives: HealthStatus, CheckResult, HealthCheck, FunctionCheck."""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Tuple, Union


class HealthStatus(str, Enum):
    """Overall status of a single health check."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class CheckResult:
    """Result of running one health check."""
    name: str
    status: HealthStatus
    message: str = ""
    duration_ms: float = 0.0
    details: dict = field(default_factory=dict)

    def is_healthy(self) -> bool:
        """Return True if status is HEALTHY."""
        return self.status == HealthStatus.HEALTHY

    def is_degraded(self) -> bool:
        """Return True if status is DEGRADED."""
        return self.status == HealthStatus.DEGRADED


class HealthCheck(ABC):
    """Abstract base class for health checks."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name for this check."""

    @abstractmethod
    def run(self) -> CheckResult:
        """Execute the check and return a CheckResult."""


class FunctionCheck(HealthCheck):
    """A HealthCheck backed by a plain callable.

    The callable may return:
    - ``True``  → HEALTHY
    - ``False`` → UNHEALTHY
    - ``(HealthStatus, message: str)`` tuple → use directly
    - Any exception raised → UNHEALTHY with the exception message
    """

    def __init__(
        self,
        name: str,
        func: Callable,
        timeout_ms: float = 5000.0,
    ) -> None:
        self._name = name
        self._func = func
        self._timeout_ms = timeout_ms

    @property
    def name(self) -> str:
        return self._name

    def run(self) -> CheckResult:
        """Call func(), measure duration, interpret return value."""
        start = time.perf_counter()
        try:
            result = self._func()
        except Exception as exc:
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            return CheckResult(
                name=self._name,
                status=HealthStatus.UNHEALTHY,
                message=str(exc),
                duration_ms=elapsed_ms,
            )
        elapsed_ms = (time.perf_counter() - start) * 1000.0

        if isinstance(result, tuple) and len(result) == 2:
            status, message = result
            return CheckResult(
                name=self._name,
                status=status,
                message=str(message),
                duration_ms=elapsed_ms,
            )

        if isinstance(result, bool):
            status = HealthStatus.HEALTHY if result else HealthStatus.UNHEALTHY
            return CheckResult(
                name=self._name,
                status=status,
                duration_ms=elapsed_ms,
            )

        # Fallback: treat as truthy/falsy
        status = HealthStatus.HEALTHY if result else HealthStatus.UNHEALTHY
        return CheckResult(
            name=self._name,
            status=status,
            duration_ms=elapsed_ms,
        )
