"""Implementation of the E380 DocEventFilter module."""

from __future__ import annotations

import fnmatch
import threading
from dataclasses import dataclass, field
from typing import Optional


_VALID_ACTIONS = ("allow", "block")


@dataclass
class FilterRule:
    """A single filter rule applied to document events."""

    rule_id: str
    event_type_pattern: str = "*"
    doc_id_pattern: str = "*"
    action: str = "allow"
    priority: int = 0
    enabled: bool = True


@dataclass
class FilterResult:
    """Outcome of applying the filter chain to a single event."""

    allowed: bool
    matched_rule: Optional[str] = None
    reason: str = ""


@dataclass
class FilterStats:
    """Aggregate statistics about rules and evaluations."""

    total_rules: int
    enabled_rules: int
    total_evaluations: int
    allowed_count: int
    blocked_count: int


class DocEventFilter:
    """Filter chain for document event streams.

    Rules are evaluated in priority order (highest first, then by rule_id).
    The first enabled rule whose patterns match decides the outcome.
    If no rule matches, the default action is applied.
    """

    def __init__(self, default_action: str = "allow") -> None:
        if default_action not in _VALID_ACTIONS:
            raise ValueError(
                f"default_action must be one of {_VALID_ACTIONS!r}, got {default_action!r}"
            )
        self._rules: dict[str, FilterRule] = {}
        self._total_evaluations: int = 0
        self._allowed_count: int = 0
        self._blocked_count: int = 0
        self._default_action: str = default_action
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ rules
    def add_rule(self, rule: FilterRule) -> None:
        """Add or replace a rule."""
        if not isinstance(rule, FilterRule):
            raise TypeError("rule must be a FilterRule instance")
        if rule.action not in _VALID_ACTIONS:
            raise ValueError(
                f"rule.action must be one of {_VALID_ACTIONS!r}, got {rule.action!r}"
            )
        with self._lock:
            self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule. Returns True if removed, False if not found."""
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                return True
            return False

    def enable_rule(self, rule_id: str) -> bool:
        """Enable a rule. Returns True if found, False otherwise."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = True
            return True

    def disable_rule(self, rule_id: str) -> bool:
        """Disable a rule. Returns True if found, False otherwise."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = False
            return True

    def get_rule(self, rule_id: str) -> Optional[FilterRule]:
        """Return rule by id or None."""
        with self._lock:
            return self._rules.get(rule_id)

    def list_rules(self) -> list[FilterRule]:
        """Return all rules sorted by (-priority, rule_id)."""
        with self._lock:
            rules = list(self._rules.values())
        rules.sort(key=lambda r: (-r.priority, r.rule_id))
        return rules

    def clear_rules(self) -> int:
        """Remove all rules. Returns the number removed."""
        with self._lock:
            count = len(self._rules)
            self._rules.clear()
            return count

    # ------------------------------------------------------------------ config
    def set_default_action(self, action: str) -> None:
        """Set default action when no rule matches."""
        if action not in _VALID_ACTIONS:
            raise ValueError(
                f"action must be one of {_VALID_ACTIONS!r}, got {action!r}"
            )
        with self._lock:
            self._default_action = action

    # -------------------------------------------------------------- evaluation
    def evaluate(self, event_type: str, doc_id: str) -> FilterResult:
        """Apply enabled rules in priority order, return FilterResult."""
        with self._lock:
            # Snapshot enabled rules in priority order under the lock.
            candidates = [r for r in self._rules.values() if r.enabled]
            candidates.sort(key=lambda r: (-r.priority, r.rule_id))
            default_action = self._default_action

            matched: Optional[FilterRule] = None
            for rule in candidates:
                if fnmatch.fnmatchcase(event_type, rule.event_type_pattern) and \
                        fnmatch.fnmatchcase(doc_id, rule.doc_id_pattern):
                    matched = rule
                    break

            self._total_evaluations += 1

            if matched is not None:
                allowed = matched.action == "allow"
                reason = (
                    f"matched rule {matched.rule_id!r} (action={matched.action})"
                )
                result = FilterResult(
                    allowed=allowed, matched_rule=matched.rule_id, reason=reason
                )
            else:
                allowed = default_action == "allow"
                reason = f"no rule matched; default_action={default_action}"
                result = FilterResult(
                    allowed=allowed, matched_rule=None, reason=reason
                )

            if result.allowed:
                self._allowed_count += 1
            else:
                self._blocked_count += 1

            return result

    def filter_events(self, events: list[tuple]) -> list[tuple]:
        """Return only events whose evaluation is allowed.

        Each event is expected to be a ``(event_type, doc_id, payload)`` tuple.
        """
        out: list[tuple] = []
        for event in events:
            if not isinstance(event, tuple) or len(event) < 2:
                raise ValueError(
                    "each event must be a tuple of (event_type, doc_id, payload)"
                )
            event_type, doc_id = event[0], event[1]
            if self.evaluate(event_type, doc_id).allowed:
                out.append(event)
        return out

    # ------------------------------------------------------------------- stats
    def stats(self) -> FilterStats:
        """Return aggregate statistics."""
        with self._lock:
            total = len(self._rules)
            enabled = sum(1 for r in self._rules.values() if r.enabled)
            return FilterStats(
                total_rules=total,
                enabled_rules=enabled,
                total_evaluations=self._total_evaluations,
                allowed_count=self._allowed_count,
                blocked_count=self._blocked_count,
            )
