"""PolicyEngine: evaluates multiple policies with DENY-precedence."""
from __future__ import annotations

import datetime

from docstoolkit.policy_engine.policy import Policy, PolicyDecision
from docstoolkit.policy_engine.rule import RuleEffect


class PolicyEngine:
    """Evaluates a collection of :class:`Policy` objects against a context.

    Precedence rules:
    - If **any** policy returns DENY → overall DENY.
    - If at least one policy returns ALLOW and none return DENY → ALLOW.
    - If all policies return AUDIT → AUDIT.
    - If there are no registered policies → ALLOW (open by default).
    """

    def __init__(self) -> None:
        self._policies: dict[str, Policy] = {}

    # ------------------------------------------------------------------
    # Policy registry
    # ------------------------------------------------------------------

    def add_policy(self, policy: Policy) -> None:
        self._policies[policy.policy_id] = policy

    def remove_policy(self, policy_id: str) -> bool:
        if policy_id in self._policies:
            del self._policies[policy_id]
            return True
        return False

    def policy_count(self) -> int:
        return len(self._policies)

    # ------------------------------------------------------------------
    # Evaluation
    # ------------------------------------------------------------------

    def evaluate(self, context: dict) -> PolicyDecision:
        """Evaluate *context* against all registered policies."""
        if not self._policies:
            return PolicyDecision(
                effect=RuleEffect.ALLOW,
                rule_id=None,
                rule_name=None,
                context=context,
                reason="No policies registered; open by default",
            )

        decisions: list[PolicyDecision] = [
            policy.evaluate(context) for policy in self._policies.values()
        ]

        # DENY takes precedence
        for decision in decisions:
            if decision.effect is RuleEffect.DENY:
                return PolicyDecision(
                    effect=RuleEffect.DENY,
                    rule_id=decision.rule_id,
                    rule_name=decision.rule_name,
                    context=context,
                    reason=f"DENY from policy decision: {decision.reason}",
                )

        # At least one ALLOW?
        for decision in decisions:
            if decision.effect is RuleEffect.ALLOW:
                return PolicyDecision(
                    effect=RuleEffect.ALLOW,
                    rule_id=decision.rule_id,
                    rule_name=decision.rule_name,
                    context=context,
                    reason=f"ALLOW from policy decision: {decision.reason}",
                )

        # All remaining decisions are AUDIT
        first = decisions[0]
        return PolicyDecision(
            effect=RuleEffect.AUDIT,
            rule_id=first.rule_id,
            rule_name=first.rule_name,
            context=context,
            reason="All policies returned AUDIT",
        )

    # ------------------------------------------------------------------
    # Audit logging
    # ------------------------------------------------------------------

    def audit_log(self, context: dict, decision: PolicyDecision) -> dict:
        """Return a structured audit-log entry for *context* and *decision*."""
        return {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "effect": decision.effect.value,
            "rule_id": decision.rule_id,
            "rule_name": decision.rule_name,
            "reason": decision.reason,
            "context": context,
            "policy_count": self.policy_count(),
        }
