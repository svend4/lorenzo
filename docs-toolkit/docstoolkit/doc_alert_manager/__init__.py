"""E342 DocAlertManager — document alert/condition manager.

Public API
----------
:class:`AlertRule`        — a single alert rule definition
:class:`AlertOccurrence`  — a recorded alert firing
:class:`AlertStats`       — aggregate statistics
:class:`DocAlertManager`  — main interface for alert management
"""

from .manager import AlertRule, AlertOccurrence, AlertStats, DocAlertManager

__all__ = ["AlertRule", "AlertOccurrence", "AlertStats", "DocAlertManager"]
