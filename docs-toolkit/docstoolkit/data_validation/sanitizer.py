"""Sanitizer primitives for the E71 Data Validation module."""
import re
from dataclasses import dataclass
from typing import Callable


@dataclass
class SanitizeRule:
    """A named transformation applied to a string value."""
    name: str
    transform: Callable[[str], str]
    description: str = ""


class DataSanitizer:
    """Apply an ordered sequence of SanitizeRules to string values."""

    def __init__(self, rules: list[SanitizeRule] | None = None) -> None:
        self._rules: list[SanitizeRule] = list(rules) if rules else []

    def add_rule(self, rule: SanitizeRule) -> None:
        """Append *rule* to the end of the sanitization pipeline."""
        self._rules.append(rule)

    def sanitize(self, value: str) -> str:
        """Apply every registered transform in order to *value*."""
        for rule in self._rules:
            value = rule.transform(value)
        return value

    def sanitize_dict(self, data: dict, fields: list[str] | None = None) -> dict:
        """Return a copy of *data* with string fields sanitized.

        If *fields* is given, only those keys are processed; otherwise all
        keys whose current value is a ``str`` are sanitized.
        """
        result = dict(data)
        keys = fields if fields is not None else [k for k, v in data.items() if isinstance(v, str)]
        for key in keys:
            if key in result and isinstance(result[key], str):
                result[key] = self.sanitize(result[key])
        return result


# ---------------------------------------------------------------------------
# Built-in sanitizer factories
# ---------------------------------------------------------------------------

def strip_whitespace() -> SanitizeRule:
    """Return a rule that strips leading and trailing whitespace."""
    return SanitizeRule(
        name="strip_whitespace",
        transform=str.strip,
        description="Strip leading and trailing whitespace",
    )


def lowercase() -> SanitizeRule:
    """Return a rule that converts the string to lower-case."""
    return SanitizeRule(
        name="lowercase",
        transform=str.lower,
        description="Convert to lowercase",
    )


def truncate(max_len: int) -> SanitizeRule:
    """Return a rule that truncates the string to *max_len* characters."""
    return SanitizeRule(
        name=f"truncate:{max_len}",
        transform=lambda s: s[:max_len],
        description=f"Truncate to {max_len} characters",
    )


def remove_html_tags() -> SanitizeRule:
    """Return a rule that strips HTML tags (``<...>``) via regex."""
    _pattern = re.compile(r"<[^>]*>")
    return SanitizeRule(
        name="remove_html_tags",
        transform=lambda s: _pattern.sub("", s),
        description="Remove HTML tags",
    )
