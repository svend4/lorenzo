"""Document Alerts module (E210).

Alerting rules engine for document events with thresholds, cooldowns,
acknowledgements, and auto-expiration.

Usage:
    from docstoolkit.doc_alerts import DocAlerts, AlertSeverity

    da = DocAlerts()
    rule = da.add_rule(
        name="large_doc",
        condition=lambda p: p.get("size", 0) > 1_000_000,
        severity=AlertSeverity.HIGH,
        cooldown_seconds=60.0,
    )

    alerts = da.evaluate({"size": 2_000_000}, now=100.0)
    da.acknowledge(alerts[0].alert_id, by="alice", now=110.0)
    da.resolve(alerts[0].alert_id, now=120.0)
"""
from docstoolkit.doc_alerts.alerts import (
    Alert,
    AlertRule,
    AlertSeverity,
    AlertState,
    AlertStats,
    DocAlerts,
)

__all__ = [
    "Alert",
    "AlertRule",
    "AlertSeverity",
    "AlertState",
    "AlertStats",
    "DocAlerts",
]
