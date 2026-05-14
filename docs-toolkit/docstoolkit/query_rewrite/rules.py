"""Rewrite rules: pattern-based substring replacement for query rewriting."""
import re
from dataclasses import dataclass, field


@dataclass
class RewriteRule:
    """A single rewrite rule that matches a substring pattern and replaces it.

    Attributes:
        rule_id:     Unique identifier for this rule.
        pattern:     Substring to match (case-insensitive).
        replacement: String to substitute for every match.
        priority:    Higher value → applied first when multiple rules apply.
        description: Human-readable explanation of the rule.
    """

    rule_id: str
    pattern: str
    replacement: str
    priority: int = 0
    description: str = ""

    def applies_to(self, query: str) -> bool:
        """Return True if *pattern* is found anywhere in *query* (case-insensitive)."""
        return bool(re.search(re.escape(self.pattern), query, re.IGNORECASE))

    def apply(self, query: str) -> str:
        """Replace all case-insensitive occurrences of *pattern* with *replacement*."""
        return re.sub(re.escape(self.pattern), self.replacement, query, flags=re.IGNORECASE)


class RuleSet:
    """An ordered collection of :class:`RewriteRule` objects."""

    def __init__(self) -> None:
        self._rules: dict[str, RewriteRule] = {}

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add(self, rule: RewriteRule) -> None:
        """Add *rule* to the set (overwrites any existing rule with the same id)."""
        self._rules[rule.rule_id] = rule

    def remove(self, rule_id: str) -> bool:
        """Remove the rule with *rule_id*.

        Returns True if a rule was removed, False if the id was not found.
        """
        if rule_id in self._rules:
            del self._rules[rule_id]
            return True
        return False

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get(self, rule_id: str) -> "RewriteRule | None":
        """Return the rule with *rule_id*, or None if not present."""
        return self._rules.get(rule_id)

    def rules_for(self, query: str) -> list[RewriteRule]:
        """Return all rules whose pattern is found in *query*, sorted by priority desc."""
        applicable = [r for r in self._rules.values() if r.applies_to(query)]
        applicable.sort(key=lambda r: r.priority, reverse=True)
        return applicable

    def all_rules(self) -> list[RewriteRule]:
        """Return all registered rules (insertion order preserved)."""
        return list(self._rules.values())
