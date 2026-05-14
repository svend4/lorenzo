"""Route rules: conditions, actions, and RouteRule dataclass."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class RouteCondition(Enum):
    """Condition type used to decide whether a rule matches a query."""
    KEYWORD_MATCH = "keyword_match"
    LENGTH_THRESHOLD = "length_threshold"
    REGEX_MATCH = "regex_match"
    ALWAYS = "always"


class RouteAction(Enum):
    """Action to take when a rule matches."""
    FORWARD = "forward"
    TRANSFORM = "transform"
    REJECT = "reject"
    CACHE = "cache"


@dataclass
class RouteRule:
    """A single routing rule with a condition and action.

    Attributes:
        name: Unique name for the rule.
        condition: Which condition to evaluate.
        action: What to do when the condition is met.
        priority: Higher value = evaluated first.
        keywords: Keywords to look for (KEYWORD_MATCH).
        min_length: Minimum query length inclusive (LENGTH_THRESHOLD).
        max_length: Maximum query length inclusive (LENGTH_THRESHOLD).
        pattern: Regex pattern string (REGEX_MATCH); compiled on first use.
        transform_fn: Callable(query: str) -> str for TRANSFORM action.
        target: Destination/handler name used when routing.
    """
    name: str
    condition: RouteCondition
    action: RouteAction
    priority: int = 0
    keywords: list[str] = field(default_factory=list)
    min_length: int = 0
    max_length: int = 10_000
    pattern: str = ""
    transform_fn: Callable[[str], str] | None = None
    target: str = "default"

    # Internal cache for compiled regex — not exposed as a dataclass field.
    _compiled_pattern: re.Pattern | None = field(default=None, init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        # Reset compiled pattern so it is lazily compiled on first use.
        object.__setattr__(self, "_compiled_pattern", None)

    def _get_compiled_pattern(self) -> re.Pattern:
        """Compile and cache the regex pattern."""
        if self._compiled_pattern is None:
            object.__setattr__(self, "_compiled_pattern", re.compile(self.pattern))
        return self._compiled_pattern

    def matches(self, query: str) -> bool:
        """Evaluate the rule's condition against *query*.

        Returns True if the condition is satisfied.
        """
        if self.condition is RouteCondition.ALWAYS:
            return True

        if self.condition is RouteCondition.KEYWORD_MATCH:
            query_lower = query.lower()
            return any(kw.lower() in query_lower for kw in self.keywords)

        if self.condition is RouteCondition.LENGTH_THRESHOLD:
            length = len(query)
            return self.min_length <= length <= self.max_length

        if self.condition is RouteCondition.REGEX_MATCH:
            compiled = self._get_compiled_pattern()
            return compiled.search(query) is not None

        return False  # Unknown condition — conservative default.
