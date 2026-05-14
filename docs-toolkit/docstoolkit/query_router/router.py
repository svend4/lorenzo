"""QueryRouter: routes queries through prioritized RouteRule list."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.query_router.route import RouteAction, RouteRule


@dataclass
class RouteResult:
    """Result of routing a single query.

    Attributes:
        query: The (potentially transformed) query after routing.
        original_query: The query as received before any transformation.
        action: The RouteAction that was applied.
        target: The destination/handler name.
        rule_name: Name of the rule that matched (empty string if none).
        matched: True if a rule was matched; False for the default fallback.
    """
    query: str
    original_query: str
    action: RouteAction
    target: str
    rule_name: str
    matched: bool


class QueryRouter:
    """Routes queries through an ordered list of RouteRules.

    Rules are evaluated in descending priority order; the first match wins.
    """

    def __init__(self) -> None:
        self._rules: list[RouteRule] = []

    def add_rule(self, rule: RouteRule) -> None:
        """Add a RouteRule to the router."""
        self._rules.append(rule)

    def remove_rule(self, name: str) -> bool:
        """Remove the rule with the given name.

        Returns True if a rule was removed, False if the name was not found.
        """
        for i, rule in enumerate(self._rules):
            if rule.name == name:
                del self._rules[i]
                return True
        return False

    def rules(self) -> list[RouteRule]:
        """Return all rules sorted by priority descending (highest first)."""
        return sorted(self._rules, key=lambda r: r.priority, reverse=True)

    def route(self, query: str) -> RouteResult:
        """Route a single query.

        Evaluates rules in descending priority order.  The first matching rule
        determines the action:

        * TRANSFORM — ``rule.transform_fn(query)`` is called and the result
          becomes the routed query.
        * REJECT — query is unchanged, action is REJECT.
        * FORWARD / CACHE — query is unchanged.

        If no rule matches, returns a default result with
        action=FORWARD, target="default", matched=False.
        """
        original = query
        for rule in self.rules():
            if rule.matches(query):
                routed_query = query
                if rule.action is RouteAction.TRANSFORM and rule.transform_fn is not None:
                    routed_query = rule.transform_fn(query)
                return RouteResult(
                    query=routed_query,
                    original_query=original,
                    action=rule.action,
                    target=rule.target,
                    rule_name=rule.name,
                    matched=True,
                )

        # No rule matched — return a safe default.
        return RouteResult(
            query=query,
            original_query=original,
            action=RouteAction.FORWARD,
            target="default",
            rule_name="",
            matched=False,
        )

    def route_batch(self, queries: list[str]) -> list[RouteResult]:
        """Route a list of queries and return a list of RouteResults."""
        return [self.route(q) for q in queries]
