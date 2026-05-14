"""Policy and decision types."""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.policy_engine.rule import PolicyRule, RuleEffect


@dataclass
class PolicyDecision:
    """Result of evaluating a policy (or the whole engine) against a context."""

    effect: RuleEffect
    rule_id: Optional[str]
    rule_name: Optional[str]
    context: dict
    reason: str = ""

    def is_allowed(self) -> bool:
        return self.effect is RuleEffect.ALLOW

    def is_denied(self) -> bool:
        return self.effect is RuleEffect.DENY


@dataclass
class Policy:
    """An ordered collection of rules with a fallback default effect."""

    name: str
    rules: list[PolicyRule] = field(default_factory=list)
    default_effect: RuleEffect = RuleEffect.DENY
    policy_id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def add_rule(self, rule: PolicyRule) -> None:
        self.rules.append(rule)

    def evaluate(self, context: dict) -> PolicyDecision:
        """Evaluate *context* against all rules; first match wins.

        Rules are tried in descending priority order (highest priority first).
        If no rule matches the *default_effect* applies.
        """
        sorted_rules = sorted(self.rules, key=lambda r: r.priority, reverse=True)

        for rule in sorted_rules:
            if rule.matches(context):
                return PolicyDecision(
                    effect=rule.effect,
                    rule_id=rule.rule_id,
                    rule_name=rule.name,
                    context=context,
                    reason=f"Matched rule '{rule.name}' (id={rule.rule_id})",
                )

        return PolicyDecision(
            effect=self.default_effect,
            rule_id=None,
            rule_name=None,
            context=context,
            reason=f"No rule matched; applied default effect '{self.default_effect.value}'",
        )
