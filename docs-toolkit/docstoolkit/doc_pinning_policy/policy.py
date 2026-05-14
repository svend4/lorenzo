"""E365 DocPinningPolicy implementation."""

from __future__ import annotations

import fnmatch
import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PinPolicyRule:
    """A pinning policy rule."""

    rule_id: str
    pattern: str
    auto_pin: bool = False
    max_pinned: Optional[int] = None
    priority: int = 0
    description: str = ""


@dataclass
class PinPolicyResult:
    """Result of evaluating policy for a single doc."""

    doc_id: str
    matched_rule: Optional[str]
    auto_pin: bool
    max_pinned: Optional[int]
    reason: str


@dataclass
class PinPolicyStats:
    """Aggregate statistics for the policy."""

    total_rules: int
    auto_pin_rules: int
    unique_patterns: int


class DocPinningPolicy:
    """Main interface for pinning policy."""

    def __init__(self) -> None:
        self._rules: dict[str, PinPolicyRule] = {}
        self._lock = threading.Lock()

    def add_rule(self, rule: PinPolicyRule) -> None:
        """Add or replace a rule."""
        with self._lock:
            self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule. Returns True if removed, False if not found."""
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                return True
            return False

    def get_rule(self, rule_id: str) -> Optional[PinPolicyRule]:
        """Return rule by id, or None."""
        with self._lock:
            return self._rules.get(rule_id)

    def list_rules(self) -> list[PinPolicyRule]:
        """Return rules sorted by (-priority, rule_id)."""
        with self._lock:
            rules = list(self._rules.values())
        return sorted(rules, key=lambda r: (-r.priority, r.rule_id))

    def evaluate(self, doc_id: str) -> PinPolicyResult:
        """Evaluate policy for given doc_id.

        Finds highest-priority rule whose pattern matches doc_id
        (via :func:`fnmatch.fnmatch`). On ties, lower rule_id wins
        (deterministic via list_rules ordering).
        """
        for rule in self.list_rules():
            if fnmatch.fnmatch(doc_id, rule.pattern):
                return PinPolicyResult(
                    doc_id=doc_id,
                    matched_rule=rule.rule_id,
                    auto_pin=rule.auto_pin,
                    max_pinned=rule.max_pinned,
                    reason=f"matched rule {rule.rule_id!r} (pattern={rule.pattern!r})",
                )
        return PinPolicyResult(
            doc_id=doc_id,
            matched_rule=None,
            auto_pin=False,
            max_pinned=None,
            reason="no matching rule",
        )

    def auto_pin_candidates(self, doc_ids: list[str]) -> list[str]:
        """Return sorted list of doc_ids whose evaluate result has auto_pin=True."""
        candidates = [d for d in doc_ids if self.evaluate(d).auto_pin]
        return sorted(candidates)

    def clear(self) -> int:
        """Remove all rules. Return count of removed rules."""
        with self._lock:
            count = len(self._rules)
            self._rules.clear()
            return count

    def stats(self) -> PinPolicyStats:
        """Return aggregate statistics."""
        with self._lock:
            rules = list(self._rules.values())
        total = len(rules)
        auto = sum(1 for r in rules if r.auto_pin)
        unique_patterns = len({r.pattern for r in rules})
        return PinPolicyStats(
            total_rules=total,
            auto_pin_rules=auto,
            unique_patterns=unique_patterns,
        )
