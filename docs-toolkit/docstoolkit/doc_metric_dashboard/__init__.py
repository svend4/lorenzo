"""E382 DocMetricDashboard — dashboard for aggregated document metrics.

Public API
----------
:class:`MetricCard`         — a single dashboard card with aggregate value
:class:`DashboardSnapshot`  — a snapshot of all cards at one time
:class:`DashboardStats`     — aggregate statistics
:class:`DocMetricDashboard` — main interface for dashboard management
"""

from .dashboard import MetricCard, DashboardSnapshot, DashboardStats, DocMetricDashboard

__all__ = ["MetricCard", "DashboardSnapshot", "DashboardStats", "DocMetricDashboard"]
