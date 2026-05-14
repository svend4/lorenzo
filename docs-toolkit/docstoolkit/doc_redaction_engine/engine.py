"""E327 DocRedactionEngine — implementation."""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RedactionRule:
    """A single redaction rule."""

    rule_id: str
    pattern: str
    replacement: str = "[REDACTED]"
    description: str = ""
    enabled: bool = True


@dataclass
class RedactionResult:
    """The result of applying redactions."""

    original_length: int
    redacted_length: int
    redacted_text: str
    applied_rules: list = field(default_factory=list)
    match_counts: dict = field(default_factory=dict)


@dataclass
class RedactionStats:
    """Aggregate statistics for the engine."""

    total_rules: int
    enabled_rules: int
    total_redactions_performed: int


class DocRedactionEngine:
    """Pattern-based content redaction for documents."""

    def __init__(self) -> None:
        self._rules: dict = {}
        self._compiled: dict = {}
        self._total_redactions: int = 0
        self._lock = threading.Lock()

    def add_rule(self, rule: RedactionRule) -> None:
        """Register or replace a rule; compiles regex eagerly."""
        compiled = re.compile(rule.pattern)
        with self._lock:
            self._rules[rule.rule_id] = rule
            self._compiled[rule.rule_id] = compiled

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule; return True if it existed."""
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                self._compiled.pop(rule_id, None)
                return True
            return False

    def enable_rule(self, rule_id: str) -> bool:
        """Enable a rule; return True if found."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = True
            return True

    def disable_rule(self, rule_id: str) -> bool:
        """Disable a rule; return True if found."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = False
            return True

    def get_rule(self, rule_id: str) -> Optional[RedactionRule]:
        """Return a rule by id, or None."""
        with self._lock:
            return self._rules.get(rule_id)

    def list_rules(self) -> list:
        """Return all rules, sorted by rule_id."""
        with self._lock:
            return [self._rules[rid] for rid in sorted(self._rules)]

    def redact(self, text: str, rule_ids: Optional[list] = None) -> RedactionResult:
        """Apply enabled rules to text and return a RedactionResult."""
        with self._lock:
            if rule_ids is None:
                candidate_ids = list(self._rules.keys())
            else:
                candidate_ids = [rid for rid in rule_ids if rid in self._rules]

            # Snapshot rules + compiled regex while holding lock
            work = []
            for rid in candidate_ids:
                rule = self._rules[rid]
                if not rule.enabled:
                    continue
                work.append((rid, self._compiled[rid], rule.replacement))

            self._total_redactions += 1

        original_length = len(text)
        current = text
        match_counts: dict = {}
        applied: list = []

        for rid, compiled, replacement in work:
            matches = compiled.findall(current)
            count = len(matches)
            match_counts[rid] = count
            if count > 0:
                applied.append(rid)
                current = compiled.sub(replacement, current)

        applied.sort()

        return RedactionResult(
            original_length=original_length,
            redacted_length=len(current),
            redacted_text=current,
            applied_rules=applied,
            match_counts=match_counts,
        )

    def test_pattern(self, rule_id: str, text: str) -> int:
        """Return the number of matches for a rule's pattern without modifying text."""
        with self._lock:
            compiled = self._compiled.get(rule_id)
        if compiled is None:
            return 0
        return len(compiled.findall(text))

    def clear_rules(self) -> int:
        """Remove all rules; return the number removed."""
        with self._lock:
            count = len(self._rules)
            self._rules.clear()
            self._compiled.clear()
            return count

    def stats(self) -> RedactionStats:
        """Return aggregate stats."""
        with self._lock:
            total = len(self._rules)
            enabled = sum(1 for r in self._rules.values() if r.enabled)
            return RedactionStats(
                total_rules=total,
                enabled_rules=enabled,
                total_redactions_performed=self._total_redactions,
            )
