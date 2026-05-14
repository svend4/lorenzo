"""Document Health Monitoring module (E271).

Configurable health checks with status aggregation, intervals, and history.
Different from doc_health_check (E212): this is for ongoing monitoring.

Usage:
    from docstoolkit.doc_health import (
        DocHealth, HealthCheck, CheckResult, HealthReport, HealthStatus,
    )

    dh = DocHealth()

    def index_check():
        return CheckResult(
            check_name="index",
            status=HealthStatus.HEALTHY,
            message="Index ok",
        )

    dh.register_check("index", index_check, interval_seconds=30.0)
    report = dh.run_all()
    print(report.overall_status, report.healthy_count)
"""
from docstoolkit.doc_health.health import (
    CheckResult,
    DocHealth,
    HealthCheck,
    HealthReport,
    HealthStatus,
)

__all__ = [
    "CheckResult",
    "DocHealth",
    "HealthCheck",
    "HealthReport",
    "HealthStatus",
]
