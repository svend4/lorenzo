"""E342 DocAlertManager — document alert/condition manager.

Pure stdlib, thread-safe via :class:`threading.Lock`, dataclasses throughout.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AlertRule:
    """A single alert rule definition."""

    rule_id: str
    name: str
    severity: str = "info"
    condition: str = ""
    cooldown_seconds: float = 0.0
    enabled: bool = True


@dataclass
class AlertOccurrence:
    """A recorded alert firing."""

    occurrence_id: int
    rule_id: str
    doc_id: str
    message: str = ""
    fired_at: float = 0.0
    acknowledged: bool = False
    metadata: dict = field(default_factory=dict)


@dataclass
class AlertStats:
    """Aggregate statistics."""

    total_rules: int
    enabled_rules: int
    total_occurrences: int
    unacknowledged_count: int


class DocAlertManager:
    """Manages alert rules and their firings against documents."""

    def __init__(self) -> None:
        self._rules: dict[str, AlertRule] = {}
        self._occurrences: list[AlertOccurrence] = []
        self._last_fired: dict[tuple, float] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ rules

    def define_rule(self, rule: AlertRule) -> None:
        """Register a new rule or replace an existing one with the same id."""
        with self._lock:
            self._rules[rule.rule_id] = rule

    def undefine_rule(self, rule_id: str) -> bool:
        """Remove a rule. Past occurrences are kept. Returns True if existed."""
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                return True
            return False

    def enable_rule(self, rule_id: str) -> bool:
        """Set rule.enabled = True. Returns True if found."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = True
            return True

    def disable_rule(self, rule_id: str) -> bool:
        """Set rule.enabled = False. Returns True if found."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = False
            return True

    def get_rule(self, rule_id: str) -> Optional[AlertRule]:
        """Return the rule or None."""
        with self._lock:
            return self._rules.get(rule_id)

    def list_rules(self) -> list[AlertRule]:
        """Return all rules sorted by rule_id."""
        with self._lock:
            return sorted(self._rules.values(), key=lambda r: r.rule_id)

    # ------------------------------------------------------------------ fire

    def fire(
        self,
        rule_id: str,
        doc_id: str,
        message: str = "",
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> Optional[AlertOccurrence]:
        """Fire an alert for the given rule and document.

        Returns ``None`` if the rule is unknown, disabled, or still within
        its cooldown window. Otherwise creates and records a new occurrence.
        """
        ts = time.time() if now is None else now
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None or not rule.enabled:
                return None
            key = (rule_id, doc_id)
            if rule.cooldown_seconds > 0.0:
                last = self._last_fired.get(key)
                if last is not None and (ts - last) < rule.cooldown_seconds:
                    return None
            occ = AlertOccurrence(
                occurrence_id=self._next_id,
                rule_id=rule_id,
                doc_id=doc_id,
                message=message,
                fired_at=ts,
                acknowledged=False,
                metadata=dict(metadata) if metadata else {},
            )
            self._next_id += 1
            self._occurrences.append(occ)
            self._last_fired[key] = ts
            return occ

    # ------------------------------------------------------------ acknowledge

    def acknowledge(self, occurrence_id: int) -> bool:
        """Mark an occurrence as acknowledged. Returns True if found."""
        with self._lock:
            for occ in self._occurrences:
                if occ.occurrence_id == occurrence_id:
                    occ.acknowledged = True
                    return True
            return False

    def acknowledge_all_for_doc(self, doc_id: str) -> int:
        """Acknowledge all unack occurrences for a doc. Returns count."""
        with self._lock:
            count = 0
            for occ in self._occurrences:
                if occ.doc_id == doc_id and not occ.acknowledged:
                    occ.acknowledged = True
                    count += 1
            return count

    # ----------------------------------------------------------- occurrences

    def occurrences_for_doc(
        self, doc_id: str, unacknowledged_only: bool = False
    ) -> list[AlertOccurrence]:
        """Return occurrences for a doc sorted by fired_at descending."""
        with self._lock:
            items = [o for o in self._occurrences if o.doc_id == doc_id]
            if unacknowledged_only:
                items = [o for o in items if not o.acknowledged]
            items.sort(key=lambda o: o.fired_at, reverse=True)
            return items

    def occurrences_for_rule(
        self, rule_id: str, unacknowledged_only: bool = False
    ) -> list[AlertOccurrence]:
        """Return occurrences for a rule sorted by fired_at descending."""
        with self._lock:
            items = [o for o in self._occurrences if o.rule_id == rule_id]
            if unacknowledged_only:
                items = [o for o in items if not o.acknowledged]
            items.sort(key=lambda o: o.fired_at, reverse=True)
            return items

    def occurrences_by_severity(self, severity: str) -> list[AlertOccurrence]:
        """Return occurrences whose rule has the given severity."""
        with self._lock:
            items = []
            for occ in self._occurrences:
                rule = self._rules.get(occ.rule_id)
                if rule is not None and rule.severity == severity:
                    items.append(occ)
            items.sort(key=lambda o: o.fired_at, reverse=True)
            return items

    # ---------------------------------------------------------------- misc

    def clear_occurrences(self) -> int:
        """Remove all occurrences. Returns number removed."""
        with self._lock:
            count = len(self._occurrences)
            self._occurrences.clear()
            self._last_fired.clear()
            return count

    def stats(self) -> AlertStats:
        """Return aggregate statistics."""
        with self._lock:
            total_rules = len(self._rules)
            enabled_rules = sum(1 for r in self._rules.values() if r.enabled)
            total_occurrences = len(self._occurrences)
            unack = sum(1 for o in self._occurrences if not o.acknowledged)
            return AlertStats(
                total_rules=total_rules,
                enabled_rules=enabled_rules,
                total_occurrences=total_occurrences,
                unacknowledged_count=unack,
            )
