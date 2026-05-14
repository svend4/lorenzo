"""DocAlerts — alerting rules engine for document events."""
from __future__ import annotations

import enum
import threading
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional


class AlertSeverity(enum.Enum):
    """Severity levels for alerts."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertState(enum.Enum):
    """Lifecycle state of an alert."""

    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    EXPIRED = "expired"


@dataclass
class AlertRule:
    """Definition of an alerting rule."""

    rule_id: str
    name: str
    condition: Callable[[dict], bool]
    severity: AlertSeverity = AlertSeverity.MEDIUM
    enabled: bool = True
    cooldown_seconds: float = 60.0
    expires_after: Optional[float] = None
    last_triggered: float = 0.0


@dataclass
class Alert:
    """A fired alert instance."""

    alert_id: str
    rule_id: str
    triggered_at: float
    state: AlertState
    payload: dict
    severity: AlertSeverity
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[float] = None
    resolved_at: Optional[float] = None
    expires_at: Optional[float] = None


@dataclass
class AlertStats:
    """Aggregate statistics over the alert store."""

    total: int = 0
    active: int = 0
    acknowledged: int = 0
    resolved: int = 0
    by_severity: dict = field(default_factory=dict)


class DocAlerts:
    """In-memory alert engine with thread-safe rule evaluation."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._rules: dict[str, AlertRule] = {}
        self._alerts: dict[str, Alert] = {}
        # rule_ids that have ever fired (so cooldown applies even at now=0.0)
        self._ever_fired: set = set()

    # ----- rule management -----

    def add_rule(
        self,
        name: str,
        condition: Callable[[dict], bool],
        severity: AlertSeverity = AlertSeverity.MEDIUM,
        cooldown_seconds: float = 60.0,
        expires_after: Optional[float] = None,
    ) -> AlertRule:
        """Register a new alert rule and return it."""
        rule_id = uuid.uuid4().hex
        rule = AlertRule(
            rule_id=rule_id,
            name=name,
            condition=condition,
            severity=severity,
            enabled=True,
            cooldown_seconds=cooldown_seconds,
            expires_after=expires_after,
            last_triggered=0.0,
        )
        with self._lock:
            self._rules[rule_id] = rule
        return rule

    def remove_rule(self, rule_id: str) -> bool:
        """Remove the rule. Returns True if removed."""
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                self._ever_fired.discard(rule_id)
                return True
            return False

    def enable_rule(self, rule_id: str) -> bool:
        """Enable the rule. Returns True if found."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = True
            return True

    def disable_rule(self, rule_id: str) -> bool:
        """Disable the rule. Returns True if found."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = False
            return True

    def list_rules(self, enabled_only: bool = False) -> list:
        """Return a list of rules."""
        with self._lock:
            rules = list(self._rules.values())
        if enabled_only:
            rules = [r for r in rules if r.enabled]
        return rules

    # ----- evaluation -----

    def evaluate(self, payload: dict, now: float = 0.0) -> list:
        """Evaluate every enabled rule against the payload.

        Fires Alerts for rules whose condition returns True and which are
        outside their cooldown window. Returns the list of new Alerts.
        """
        fired: list = []
        with self._lock:
            for rule in self._rules.values():
                if not rule.enabled:
                    continue
                # cooldown check — only applies after the rule has fired once
                if (
                    rule.rule_id in self._ever_fired
                    and (now - rule.last_triggered) < rule.cooldown_seconds
                ):
                    continue
                try:
                    matched = bool(rule.condition(payload))
                except Exception:
                    matched = False
                if not matched:
                    continue
                expires_at: Optional[float] = None
                if rule.expires_after is not None:
                    expires_at = now + rule.expires_after
                alert = Alert(
                    alert_id=uuid.uuid4().hex,
                    rule_id=rule.rule_id,
                    triggered_at=now,
                    state=AlertState.ACTIVE,
                    payload=dict(payload),
                    severity=rule.severity,
                    expires_at=expires_at,
                )
                self._alerts[alert.alert_id] = alert
                rule.last_triggered = now
                self._ever_fired.add(rule.rule_id)
                fired.append(alert)
        return fired

    # ----- lifecycle -----

    def acknowledge(self, alert_id: str, by: str, now: float = 0.0) -> bool:
        """Mark an active alert as acknowledged. Returns True on success."""
        with self._lock:
            alert = self._alerts.get(alert_id)
            if alert is None:
                return False
            if alert.state != AlertState.ACTIVE:
                return False
            alert.state = AlertState.ACKNOWLEDGED
            alert.acknowledged_by = by
            alert.acknowledged_at = now
            return True

    def resolve(self, alert_id: str, now: float = 0.0) -> bool:
        """Mark an alert as resolved. Allowed from ACTIVE or ACKNOWLEDGED."""
        with self._lock:
            alert = self._alerts.get(alert_id)
            if alert is None:
                return False
            if alert.state not in (AlertState.ACTIVE, AlertState.ACKNOWLEDGED):
                return False
            alert.state = AlertState.RESOLVED
            alert.resolved_at = now
            return True

    def expire_overdue(self, now: float = 0.0) -> int:
        """Transition overdue ACTIVE/ACKNOWLEDGED alerts to EXPIRED.

        Returns the number of expired alerts.
        """
        count = 0
        with self._lock:
            for alert in self._alerts.values():
                if alert.expires_at is None:
                    continue
                if alert.state not in (
                    AlertState.ACTIVE,
                    AlertState.ACKNOWLEDGED,
                ):
                    continue
                if now >= alert.expires_at:
                    alert.state = AlertState.EXPIRED
                    count += 1
        return count

    # ----- queries -----

    def get_alert(self, alert_id: str) -> Optional[Alert]:
        with self._lock:
            return self._alerts.get(alert_id)

    def active_alerts(self) -> list:
        with self._lock:
            return [
                a for a in self._alerts.values() if a.state == AlertState.ACTIVE
            ]

    def acknowledged_alerts(self) -> list:
        with self._lock:
            return [
                a
                for a in self._alerts.values()
                if a.state == AlertState.ACKNOWLEDGED
            ]

    def resolved_alerts(self) -> list:
        with self._lock:
            return [
                a
                for a in self._alerts.values()
                if a.state == AlertState.RESOLVED
            ]

    def alerts_by_severity(self, severity: AlertSeverity) -> list:
        with self._lock:
            return [
                a for a in self._alerts.values() if a.severity == severity
            ]

    def alerts_for_rule(self, rule_id: str) -> list:
        with self._lock:
            return [
                a for a in self._alerts.values() if a.rule_id == rule_id
            ]

    def stats(self) -> AlertStats:
        with self._lock:
            total = len(self._alerts)
            active = 0
            acknowledged = 0
            resolved = 0
            by_severity: dict = {s.value: 0 for s in AlertSeverity}
            for alert in self._alerts.values():
                if alert.state == AlertState.ACTIVE:
                    active += 1
                elif alert.state == AlertState.ACKNOWLEDGED:
                    acknowledged += 1
                elif alert.state == AlertState.RESOLVED:
                    resolved += 1
                by_severity[alert.severity.value] = (
                    by_severity.get(alert.severity.value, 0) + 1
                )
        return AlertStats(
            total=total,
            active=active,
            acknowledged=acknowledged,
            resolved=resolved,
            by_severity=by_severity,
        )

    @property
    def rule_count(self) -> int:
        with self._lock:
            return len(self._rules)

    @property
    def alert_count(self) -> int:
        with self._lock:
            return len(self._alerts)

    def clear(self) -> None:
        """Remove all rules and alerts."""
        with self._lock:
            self._rules.clear()
            self._alerts.clear()
            self._ever_fired.clear()
