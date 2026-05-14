"""E381 DocKeywordAlert implementation.

Pure stdlib, thread-safe, dataclasses throughout.
"""

from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class KeywordRule:
    """A keyword alert rule."""

    rule_id: str
    keyword: str
    case_sensitive: bool = False
    whole_word: bool = False
    severity: str = "info"
    enabled: bool = True


@dataclass
class KeywordMatch:
    """A single match instance."""

    rule_id: str
    doc_id: str
    keyword: str
    position: int
    severity: str
    detected_at: float = 0.0


@dataclass
class AlertStats:
    """Aggregate statistics for the alert system."""

    total_rules: int
    enabled_rules: int
    total_matches: int
    matches_by_severity: dict = field(default_factory=dict)


class DocKeywordAlert:
    """Main interface for keyword alerts on document content."""

    def __init__(self) -> None:
        self._rules: dict[str, KeywordRule] = {}
        self._matches: list[KeywordMatch] = []
        self._lock = threading.Lock()

    # ---------- Rule management ----------

    def add_rule(self, rule: KeywordRule) -> None:
        with self._lock:
            self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> bool:
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                return True
            return False

    def enable_rule(self, rule_id: str) -> bool:
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = True
            return True

    def disable_rule(self, rule_id: str) -> bool:
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = False
            return True

    def get_rule(self, rule_id: str) -> Optional[KeywordRule]:
        with self._lock:
            return self._rules.get(rule_id)

    def list_rules(self) -> list[KeywordRule]:
        with self._lock:
            return sorted(self._rules.values(), key=lambda r: r.rule_id)

    # ---------- Scanning ----------

    @staticmethod
    def _build_pattern(rule: KeywordRule) -> "re.Pattern[str]":
        escaped = re.escape(rule.keyword)
        if rule.whole_word:
            escaped = r"\b" + escaped + r"\b"
        flags = 0 if rule.case_sensitive else re.IGNORECASE
        return re.compile(escaped, flags)

    def scan(
        self,
        doc_id: str,
        content: str,
        now: Optional[float] = None,
    ) -> list[KeywordMatch]:
        """Scan content with all enabled rules; record and return matches."""
        ts = now if now is not None else time.time()
        new_matches: list[KeywordMatch] = []
        with self._lock:
            # Iterate rules in deterministic order
            for rule_id in sorted(self._rules.keys()):
                rule = self._rules[rule_id]
                if not rule.enabled:
                    continue
                pattern = self._build_pattern(rule)
                for m in pattern.finditer(content):
                    new_matches.append(
                        KeywordMatch(
                            rule_id=rule.rule_id,
                            doc_id=doc_id,
                            keyword=rule.keyword,
                            position=m.start(),
                            severity=rule.severity,
                            detected_at=ts,
                        )
                    )
            self._matches.extend(new_matches)
        return new_matches

    # ---------- Match queries ----------

    def matches_for_doc(self, doc_id: str) -> list[KeywordMatch]:
        with self._lock:
            filtered = [m for m in self._matches if m.doc_id == doc_id]
        return sorted(filtered, key=lambda m: m.detected_at)

    def matches_for_rule(self, rule_id: str) -> list[KeywordMatch]:
        with self._lock:
            filtered = [m for m in self._matches if m.rule_id == rule_id]
        return sorted(filtered, key=lambda m: m.detected_at)

    def matches_by_severity(self, severity: str) -> list[KeywordMatch]:
        with self._lock:
            filtered = [m for m in self._matches if m.severity == severity]
        return sorted(filtered, key=lambda m: m.detected_at)

    # ---------- Clearing ----------

    def clear_matches(self) -> int:
        with self._lock:
            count = len(self._matches)
            self._matches.clear()
            return count

    def clear_rules(self) -> int:
        with self._lock:
            count = len(self._rules)
            self._rules.clear()
            return count

    # ---------- Stats ----------

    def stats(self) -> AlertStats:
        with self._lock:
            total_rules = len(self._rules)
            enabled_rules = sum(1 for r in self._rules.values() if r.enabled)
            total_matches = len(self._matches)
            by_sev: dict = {}
            for m in self._matches:
                by_sev[m.severity] = by_sev.get(m.severity, 0) + 1
        return AlertStats(
            total_rules=total_rules,
            enabled_rules=enabled_rules,
            total_matches=total_matches,
            matches_by_severity=by_sev,
        )
