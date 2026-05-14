"""Health checks module — pure-stdlib health check primitives and registry."""
from docstoolkit.health_checks.check import (
    HealthStatus,
    CheckResult,
    HealthCheck,
    FunctionCheck,
)
from docstoolkit.health_checks.registry import (
    HealthReport,
    HealthRegistry,
)

__all__ = [
    "HealthStatus",
    "CheckResult",
    "HealthCheck",
    "FunctionCheck",
    "HealthReport",
    "HealthRegistry",
]
