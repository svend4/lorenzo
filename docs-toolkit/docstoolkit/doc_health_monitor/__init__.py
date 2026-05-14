"""E420 DocHealthMonitor — monitor document health metrics.

Public API
----------
:class:`HealthCheck`      — a single health check definition
:class:`HealthResult`     — outcome of a check on a doc
:class:`MonitorStats`     — aggregate statistics
:class:`DocHealthMonitor` — main interface for health monitoring
"""

from .monitor import HealthCheck, HealthResult, MonitorStats, DocHealthMonitor

__all__ = ["HealthCheck", "HealthResult", "MonitorStats", "DocHealthMonitor"]
