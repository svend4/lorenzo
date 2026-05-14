"""Document routing rules.

Routes documents (``dict`` payloads) to handlers based on metadata,
content patterns, or arbitrary predicates. Rules are evaluated in
priority order; by default a rule that matches stops further evaluation.

This is distinct from URL/path routing (see ``url_router``) — here we
match on document fields rather than URL path components.
"""
from __future__ import annotations

import re
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class RouteRule:
    """A single routing rule.

    Attributes:
        rule_id: Unique identifier (auto-generated when added).
        name: Human-friendly name.
        predicate: Callable taking the document dict, returns ``True`` to match.
        handler: Callable taking the document dict, returns any result.
        priority: Higher priority rules are evaluated first.
        stop_on_match: If True, routing stops after this rule matches.
        enabled: Disabled rules are skipped during routing.
    """

    rule_id: str
    name: str
    predicate: Callable[[dict], bool]
    handler: Callable[[dict], Any]
    priority: int = 0
    stop_on_match: bool = True
    enabled: bool = True


@dataclass
class RouteMatch:
    """Record of one rule matching a document and its handler's result."""

    rule_id: str
    rule_name: str
    result: Any
    matched_at: float


@dataclass
class RouterStats:
    """Aggregate router statistics."""

    total_rules: int
    total_routed: int
    total_matches: int
    total_unmatched: int
    by_rule: Dict[str, int] = field(default_factory=dict)


class DocRouting:
    """Document routing engine.

    Add rules with :meth:`add_rule` (each rule has a predicate and a
    handler). :meth:`route` evaluates rules against a document in
    priority order, runs handlers on matches, and returns ``RouteMatch``
    records. Helper builders (``match_by_metadata``, ``match_by_pattern``,
    ``match_all``, ``match_any``) make it easy to compose predicates.
    """

    def __init__(self) -> None:
        self._rules: Dict[str, RouteRule] = {}
        self._history: List[RouteMatch] = []
        self._total_routed: int = 0
        self._total_matches: int = 0
        self._total_unmatched: int = 0
        self._by_rule: Dict[str, int] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ rules

    def add_rule(
        self,
        name: str,
        predicate: Callable,
        handler: Callable,
        priority: int = 0,
        stop_on_match: bool = True,
    ) -> RouteRule:
        """Register a new rule and return it."""
        rule_id = uuid.uuid4().hex
        rule = RouteRule(
            rule_id=rule_id,
            name=name,
            predicate=predicate,
            handler=handler,
            priority=priority,
            stop_on_match=stop_on_match,
            enabled=True,
        )
        with self._lock:
            self._rules[rule_id] = rule
            self._by_rule[rule_id] = 0
        return rule

    def remove_rule(self, rule_id: str) -> bool:
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                self._by_rule.pop(rule_id, None)
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

    def get_rule(self, rule_id: str) -> Optional[RouteRule]:
        with self._lock:
            return self._rules.get(rule_id)

    def rules(self, enabled_only: bool = False) -> List[RouteRule]:
        with self._lock:
            items = list(self._rules.values())
        if enabled_only:
            items = [r for r in items if r.enabled]
        return items

    def rules_by_priority(self) -> List[RouteRule]:
        with self._lock:
            return sorted(
                self._rules.values(), key=lambda r: r.priority, reverse=True
            )

    @property
    def total_rules(self) -> int:
        with self._lock:
            return len(self._rules)

    # ------------------------------------------------------------------ route

    def route(self, doc: dict) -> List[RouteMatch]:
        """Route a document through the rule chain.

        Rules are evaluated in priority order (desc). Disabled rules are
        skipped. When a rule's predicate matches its handler is invoked
        and the result is recorded in a :class:`RouteMatch`. If
        ``stop_on_match`` is True for the matched rule, evaluation stops
        once the handler returns a non-``None`` result; ``None`` results
        do not short-circuit (treated as "soft" matches).
        """
        ordered = self.rules_by_priority()
        matches: List[RouteMatch] = []

        for rule in ordered:
            if not rule.enabled:
                continue
            try:
                ok = bool(rule.predicate(doc))
            except Exception:
                ok = False
            if not ok:
                continue

            now = time.time()
            try:
                result = rule.handler(doc)
                error = False
            except Exception as exc:  # noqa: BLE001 — exposing exception in result
                result = {"error": str(exc), "type": exc.__class__.__name__}
                error = True

            match = RouteMatch(
                rule_id=rule.rule_id,
                rule_name=rule.name,
                result=result,
                matched_at=now,
            )
            matches.append(match)

            with self._lock:
                self._total_matches += 1
                self._by_rule[rule.rule_id] = self._by_rule.get(rule.rule_id, 0) + 1
                self._history.append(match)

            if rule.stop_on_match and not error and result is not None:
                break

        with self._lock:
            self._total_routed += 1
            if not matches:
                self._total_unmatched += 1

        return matches

    def route_batch(self, docs: List[dict]) -> List[List[RouteMatch]]:
        return [self.route(d) for d in docs]

    def match_rules(self, doc: dict) -> List[RouteRule]:
        """Return rules whose predicates match without running handlers."""
        result: List[RouteRule] = []
        for rule in self.rules_by_priority():
            if not rule.enabled:
                continue
            try:
                if rule.predicate(doc):
                    result.append(rule)
            except Exception:
                continue
        return result

    # --------------------------------------------------------------- history

    def routing_history(self, limit: Optional[int] = None) -> List[RouteMatch]:
        with self._lock:
            hist = list(self._history)
        if limit is not None and limit >= 0:
            hist = hist[-limit:] if limit else []
        return hist

    def clear_history(self) -> int:
        with self._lock:
            n = len(self._history)
            self._history.clear()
            return n

    # ---------------------------------------------------------- predicate helpers

    @staticmethod
    def match_by_metadata(field: str, value: Any) -> Callable[[dict], bool]:
        """Predicate: doc[field] == value (supports dotted paths)."""
        parts = field.split(".")

        def _check(doc: dict) -> bool:
            current: Any = doc
            for p in parts:
                if isinstance(current, dict) and p in current:
                    current = current[p]
                else:
                    return False
            return current == value

        return _check

    @staticmethod
    def match_by_pattern(field: str, pattern: str) -> Callable[[dict], bool]:
        """Predicate: regex ``pattern`` searches doc[field] (string)."""
        regex = re.compile(pattern)
        parts = field.split(".")

        def _check(doc: dict) -> bool:
            current: Any = doc
            for p in parts:
                if isinstance(current, dict) and p in current:
                    current = current[p]
                else:
                    return False
            if not isinstance(current, str):
                return False
            return regex.search(current) is not None

        return _check

    @staticmethod
    def match_all(*predicates: Callable[[dict], bool]) -> Callable[[dict], bool]:
        """Predicate: True iff every sub-predicate returns True."""

        def _check(doc: dict) -> bool:
            for p in predicates:
                try:
                    if not p(doc):
                        return False
                except Exception:
                    return False
            return True

        return _check

    @staticmethod
    def match_any(*predicates: Callable[[dict], bool]) -> Callable[[dict], bool]:
        """Predicate: True if any sub-predicate returns True."""

        def _check(doc: dict) -> bool:
            for p in predicates:
                try:
                    if p(doc):
                        return True
                except Exception:
                    continue
            return False

        return _check

    # ----------------------------------------------------------------- stats

    def stats(self) -> RouterStats:
        with self._lock:
            return RouterStats(
                total_rules=len(self._rules),
                total_routed=self._total_routed,
                total_matches=self._total_matches,
                total_unmatched=self._total_unmatched,
                by_rule=dict(self._by_rule),
            )

    def clear(self) -> None:
        """Remove all rules, history, and reset counters."""
        with self._lock:
            self._rules.clear()
            self._history.clear()
            self._by_rule.clear()
            self._total_routed = 0
            self._total_matches = 0
            self._total_unmatched = 0
