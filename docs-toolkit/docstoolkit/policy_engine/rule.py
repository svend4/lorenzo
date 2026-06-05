"""Policy rule primitives: conditions and rules."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class RuleEffect(Enum):
    ALLOW = "allow"
    DENY = "deny"
    AUDIT = "audit"


def _get_nested(context: dict, dotted_key: str) -> Any:
    """Resolve a dot-notation key against *context*.

    Examples::

        _get_nested({"user": {"role": "admin"}}, "user.role") -> "admin"
        _get_nested({"action": "read"}, "action") -> "read"

    Raises ``KeyError`` if any segment is missing.
    """
    parts = dotted_key.split(".")
    node: Any = context
    for part in parts:
        if not isinstance(node, dict):
            raise KeyError(dotted_key)
        node = node[part]
    return node


@dataclass
class Condition:
    """A single predicate evaluated against a request context."""

    field: str
    operator: str  # eq | ne | gt | lt | gte | lte | in | contains | startswith
    value: Any

    # Supported operators
    _OPERATORS = frozenset(
        {"eq", "ne", "gt", "lt", "gte", "lte", "in", "contains", "startswith"}
    )

    def __post_init__(self) -> None:
        if self.operator not in self._OPERATORS:
            raise ValueError(
                f"Unknown operator {self.operator!r}. "
                f"Must be one of: {sorted(self._OPERATORS)}"
            )

    def evaluate(self, context: dict) -> bool:
        """Return True when the condition holds for *context*."""
        try:
            actual = _get_nested(context, self.field)
        except KeyError:
            return False

        op = self.operator
        expected = self.value

        if op == "eq":
            return actual == expected
        if op == "ne":
            return actual != expected
        if op == "gt":
            return actual > expected
        if op == "lt":
            return actual < expected
        if op == "gte":
            return actual >= expected
        if op == "lte":
            return actual <= expected
        if op == "in":
            return actual in expected
        if op == "contains":
            return expected in actual
        if op == "startswith":
            return str(actual).startswith(str(expected))

        # Should never reach here due to __post_init__ check
        raise ValueError(f"Unhandled operator: {op!r}")  # pragma: no cover


@dataclass
class PolicyRule:
    """A named rule with one or more conditions and an effect."""

    name: str
    conditions: list[Condition]
    effect: RuleEffect
    priority: int = 0
    description: str = ""
    rule_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def matches(self, context: dict) -> bool:
        """Return True when ALL conditions evaluate to True."""
        return all(c.evaluate(context) for c in self.conditions)

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "effect": self.effect.value,
            "priority": self.priority,
            "description": self.description,
            "conditions": [
                {
                    "field": c.field,
                    "operator": c.operator,
                    "value": c.value,
                }
                for c in self.conditions
            ],
        }
