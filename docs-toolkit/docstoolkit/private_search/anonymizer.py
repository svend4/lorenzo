"""Query anonymizer: redacts PII from search queries before processing.

Supports email, phone, IP address, and credit card patterns by default.
Custom rules can be added via add_rule().
"""
import re
from dataclasses import dataclass, field


@dataclass
class AnonymizationRule:
    """A single regex-based anonymization rule."""

    pattern: str
    replacement: str
    label: str


_DEFAULT_RULES: list[AnonymizationRule] = [
    AnonymizationRule(
        pattern=r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}',
        replacement='[EMAIL]',
        label='EMAIL',
    ),
    AnonymizationRule(
        pattern=r'\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b',
        replacement='[PHONE]',
        label='PHONE',
    ),
    AnonymizationRule(
        pattern=r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
        replacement='[IP]',
        label='IP',
    ),
    AnonymizationRule(
        pattern=r'\b\d{4}[\s-]\d{4}[\s-]\d{4}[\s-]\d{4}\b',
        replacement='[CARD]',
        label='CARD',
    ),
]


class QueryAnonymizer:
    """Redacts PII from search queries using configurable regex rules."""

    def __init__(self) -> None:
        self._rules: list[AnonymizationRule] = list(_DEFAULT_RULES)
        # Pre-compile patterns for performance
        self._compiled: list[tuple[re.Pattern[str], str, str]] = [
            (re.compile(r.pattern), r.replacement, r.label)
            for r in self._rules
        ]

    def add_rule(self, rule: AnonymizationRule) -> None:
        """Append a custom anonymization rule."""
        self._rules.append(rule)
        self._compiled.append(
            (re.compile(rule.pattern), rule.replacement, rule.label)
        )

    def anonymize(self, query: str) -> tuple[str, list[str]]:
        """Redact PII from *query*.

        Returns:
            (anonymized_query, list_of_redacted_labels)
        """
        result = query
        redacted: list[str] = []
        for pattern, replacement, label in self._compiled:
            new_result, n = pattern.subn(replacement, result)
            if n > 0:
                if label not in redacted:
                    redacted.append(label)
                result = new_result
        return result, redacted

    def is_sensitive(self, query: str) -> bool:
        """Return True if *query* matches any anonymization rule."""
        for pattern, _replacement, _label in self._compiled:
            if pattern.search(query):
                return True
        return False
