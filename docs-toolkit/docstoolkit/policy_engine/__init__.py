"""Policy engine module for docs-toolkit (E44).

Provides a pure-stdlib, composable policy engine with:
- Fine-grained ``Condition`` predicates (9 operators, dot-notation fields).
- ``PolicyRule`` objects grouped into ``Policy`` instances with priority ordering.
- ``PolicyEngine`` that combines multiple policies with DENY-precedence.

Quick start::

    from docstoolkit.policy_engine import (
        Condition, PolicyRule, RuleEffect,
        Policy, PolicyDecision,
        PolicyEngine,
    )

    engine = PolicyEngine()

    allow_admins = Policy(name="AllowAdmins", default_effect=RuleEffect.DENY)
    allow_admins.add_rule(PolicyRule(
        name="admin-access",
        conditions=[Condition("user.role", "eq", "admin")],
        effect=RuleEffect.ALLOW,
        priority=10,
    ))
    engine.add_policy(allow_admins)

    decision = engine.evaluate({"user": {"role": "admin"}, "action": "delete"})
    decision.is_allowed()   # True
"""

from docstoolkit.policy_engine.rule import (
    RuleEffect,
    Condition,
    PolicyRule,
)
from docstoolkit.policy_engine.policy import (
    PolicyDecision,
    Policy,
)
from docstoolkit.policy_engine.engine import PolicyEngine

__all__ = [
    "RuleEffect",
    "Condition",
    "PolicyRule",
    "PolicyDecision",
    "Policy",
    "PolicyEngine",
]
