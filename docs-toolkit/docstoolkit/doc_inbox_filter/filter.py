"""E193 DocInboxFilter — declarative rules engine for the document inbox.

A rule consists of:
- one or more :class:`Condition` (field/operator/value)
- one or more :class:`Action` (action_type + args)
- a ``match_mode`` ("all" or "any") that decides how conditions combine
- a ``priority`` (higher = applied first)
- an ``enabled`` flag

Evaluating a document yields a :class:`MatchResult` with the list of matched
rule ids and the concatenated list of actions to apply.

Field lookups support dotted paths (``metadata.tags`` → ``doc["metadata"]["tags"]``).
Missing fields make a condition fail.

Thread-safe: every mutation is protected by an internal :class:`threading.Lock`.
"""
from __future__ import annotations

import re
import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class Operator(str, Enum):
    """Comparison operators usable in :class:`Condition`."""

    EQ = "eq"
    NE = "ne"
    CONTAINS = "contains"
    STARTSWITH = "startswith"
    ENDSWITH = "endswith"
    MATCHES = "matches"
    GT = "gt"
    LT = "lt"
    IN = "in"


class ActionType(str, Enum):
    """Actions that may be performed when a rule matches."""

    TAG = "tag"
    MOVE = "move"
    FLAG = "flag"
    ARCHIVE = "archive"
    DELETE = "delete"
    ASSIGN = "assign"
    NOTIFY = "notify"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Condition:
    """Single condition: ``doc[field] <operator> value``."""

    field: str
    operator: Operator
    value: Any = None


@dataclass
class Action:
    """Action that should be performed when a rule matches."""

    action_type: ActionType
    args: dict = field(default_factory=dict)


@dataclass
class FilterRule:
    """Rule binding a set of conditions to a set of actions."""

    rule_id: str
    name: str
    conditions: list[Condition]
    actions: list[Action]
    match_mode: str = "all"  # "all" or "any"
    enabled: bool = True
    priority: int = 0


@dataclass
class MatchResult:
    """Result of evaluating one document against the rule set."""

    doc_id: str
    matched_rules: list[str] = field(default_factory=list)
    applied_actions: list[Action] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Internal sentinel for "missing field"
# ---------------------------------------------------------------------------


_MISSING = object()


def _get_field(doc: dict, dotted: str) -> Any:
    """Look up ``dotted`` path inside ``doc``; return ``_MISSING`` if absent."""
    if not isinstance(doc, dict):
        return _MISSING
    current: Any = doc
    for part in dotted.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return _MISSING
    return current


# ---------------------------------------------------------------------------
# Main engine
# ---------------------------------------------------------------------------


class DocInboxFilter:
    """Declarative rules engine for the document inbox."""

    def __init__(self) -> None:
        self._rules: dict[str, FilterRule] = {}
        self._lock = threading.Lock()

    # ---- rule management -------------------------------------------------

    def add_rule(
        self,
        name: str,
        conditions: list[Condition],
        actions: list[Action],
        match_mode: str = "all",
        priority: int = 0,
    ) -> FilterRule:
        """Create and register a new rule. Returns the stored :class:`FilterRule`."""
        if match_mode not in ("all", "any"):
            raise ValueError(f"match_mode must be 'all' or 'any', got {match_mode!r}")
        rule_id = uuid.uuid4().hex
        rule = FilterRule(
            rule_id=rule_id,
            name=name,
            conditions=list(conditions),
            actions=list(actions),
            match_mode=match_mode,
            enabled=True,
            priority=priority,
        )
        with self._lock:
            self._rules[rule_id] = rule
        return rule

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule by id. Returns ``True`` if it existed."""
        with self._lock:
            return self._rules.pop(rule_id, None) is not None

    def update_rule(self, rule_id: str, **kwargs: Any) -> Optional[FilterRule]:
        """Patch fields of an existing rule. Unknown keys are ignored."""
        allowed = {
            "name",
            "conditions",
            "actions",
            "match_mode",
            "enabled",
            "priority",
        }
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return None
            for key, value in kwargs.items():
                if key not in allowed:
                    continue
                if key == "match_mode" and value not in ("all", "any"):
                    raise ValueError(
                        f"match_mode must be 'all' or 'any', got {value!r}"
                    )
                setattr(rule, key, value)
            return rule

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

    # ---- condition matching ---------------------------------------------

    def match_single(self, doc: dict, condition: Condition) -> bool:
        """Evaluate one condition against ``doc``."""
        actual = _get_field(doc, condition.field)
        op = condition.operator
        expected = condition.value

        # NE is special: a missing field is considered "not equal" to any
        # non-None expected value.
        if actual is _MISSING:
            if op is Operator.NE:
                return True
            return False

        try:
            if op is Operator.EQ:
                return actual == expected
            if op is Operator.NE:
                return actual != expected
            if op is Operator.CONTAINS:
                if isinstance(actual, str):
                    return isinstance(expected, str) and expected in actual
                if isinstance(actual, (list, tuple, set)):
                    return expected in actual
                return False
            if op is Operator.STARTSWITH:
                return (
                    isinstance(actual, str)
                    and isinstance(expected, str)
                    and actual.startswith(expected)
                )
            if op is Operator.ENDSWITH:
                return (
                    isinstance(actual, str)
                    and isinstance(expected, str)
                    and actual.endswith(expected)
                )
            if op is Operator.MATCHES:
                if not isinstance(actual, str) or not isinstance(expected, str):
                    return False
                return re.search(expected, actual) is not None
            if op is Operator.GT:
                return actual > expected
            if op is Operator.LT:
                return actual < expected
            if op is Operator.IN:
                if not isinstance(expected, (list, tuple, set)):
                    return False
                return actual in expected
        except (TypeError, ValueError, re.error):
            return False
        return False

    def match_conditions(
        self,
        doc: dict,
        conditions: list[Condition],
        mode: str = "all",
    ) -> bool:
        """Combine ``conditions`` according to ``mode`` ("all" or "any")."""
        if mode not in ("all", "any"):
            raise ValueError(f"mode must be 'all' or 'any', got {mode!r}")
        if not conditions:
            # Vacuous truth for "all", definite false for "any"
            return mode == "all"
        if mode == "all":
            return all(self.match_single(doc, c) for c in conditions)
        return any(self.match_single(doc, c) for c in conditions)

    # ---- evaluation ------------------------------------------------------

    def evaluate(self, doc: dict, doc_id: Optional[str] = None) -> MatchResult:
        """Evaluate ``doc`` against all enabled rules in priority order."""
        if doc_id is None:
            doc_id = str(doc.get("id", "")) if isinstance(doc, dict) else ""

        with self._lock:
            rules_snapshot = [r for r in self._rules.values() if r.enabled]
        # Higher priority first; stable on ties.
        rules_snapshot.sort(key=lambda r: r.priority, reverse=True)

        result = MatchResult(doc_id=doc_id, matched_rules=[], applied_actions=[])
        for rule in rules_snapshot:
            if self.match_conditions(doc, rule.conditions, rule.match_mode):
                result.matched_rules.append(rule.rule_id)
                result.applied_actions.extend(rule.actions)
        return result

    def evaluate_batch(self, docs: list[dict]) -> list[MatchResult]:
        """Evaluate a list of documents; each gets its own :class:`MatchResult`."""
        return [self.evaluate(d) for d in docs]

    # ---- introspection ---------------------------------------------------

    def list_rules(self, enabled_only: bool = False) -> list[FilterRule]:
        with self._lock:
            rules = list(self._rules.values())
        if enabled_only:
            rules = [r for r in rules if r.enabled]
        rules.sort(key=lambda r: r.priority, reverse=True)
        return rules

    @property
    def rule_count(self) -> int:
        with self._lock:
            return len(self._rules)

    @property
    def enabled_count(self) -> int:
        with self._lock:
            return sum(1 for r in self._rules.values() if r.enabled)

    def clear(self) -> None:
        with self._lock:
            self._rules.clear()

    # ---- (de)serialization ----------------------------------------------

    def import_rules(self, rules: list[dict]) -> int:
        """Load rules from a list of dicts. Returns the number imported.

        Each dict may contain: ``rule_id``, ``name``, ``conditions``, ``actions``,
        ``match_mode``, ``enabled``, ``priority``. Missing ``rule_id`` is generated.
        """
        count = 0
        for entry in rules:
            if not isinstance(entry, dict):
                continue
            try:
                conditions = [
                    Condition(
                        field=c["field"],
                        operator=Operator(c["operator"]),
                        value=c.get("value"),
                    )
                    for c in entry.get("conditions", [])
                ]
                actions = [
                    Action(
                        action_type=ActionType(a["action_type"]),
                        args=dict(a.get("args", {})),
                    )
                    for a in entry.get("actions", [])
                ]
            except (KeyError, ValueError):
                continue
            match_mode = entry.get("match_mode", "all")
            if match_mode not in ("all", "any"):
                continue
            rule_id = entry.get("rule_id") or uuid.uuid4().hex
            rule = FilterRule(
                rule_id=rule_id,
                name=entry.get("name", ""),
                conditions=conditions,
                actions=actions,
                match_mode=match_mode,
                enabled=bool(entry.get("enabled", True)),
                priority=int(entry.get("priority", 0)),
            )
            with self._lock:
                self._rules[rule_id] = rule
            count += 1
        return count

    def export_rules(self) -> list[dict]:
        """Serialize all rules to a list of plain dicts."""
        with self._lock:
            rules = list(self._rules.values())
        out: list[dict] = []
        for rule in rules:
            out.append(
                {
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "conditions": [
                        {
                            "field": c.field,
                            "operator": c.operator.value,
                            "value": c.value,
                        }
                        for c in rule.conditions
                    ],
                    "actions": [
                        {
                            "action_type": a.action_type.value,
                            "args": dict(a.args),
                        }
                        for a in rule.actions
                    ],
                    "match_mode": rule.match_mode,
                    "enabled": rule.enabled,
                    "priority": rule.priority,
                }
            )
        return out
