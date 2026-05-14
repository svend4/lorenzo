"""TextNormalizer and NormalizerConfig."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.text_normalizer.rules import (
    NormRule,
    case_rules,
    number_rules,
    punctuation_rules,
    whitespace_rules,
)


@dataclass
class NormalizerConfig:
    """Configuration flags that control which rule sets are applied."""

    apply_whitespace: bool = True
    apply_punctuation: bool = False
    apply_case: bool = False
    apply_numbers: bool = False
    custom_rules: list[NormRule] = field(default_factory=list)


class TextNormalizer:
    """Apply a configurable sequence of normalization rules to text.

    Parameters
    ----------
    config:
        A :class:`NormalizerConfig` instance.  Defaults to
        ``NormalizerConfig()`` (whitespace normalization only).
    """

    def __init__(self, config: NormalizerConfig | None = None) -> None:
        self._config = config if config is not None else NormalizerConfig()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def normalize(self, text: str) -> str:
        """Return *text* with all enabled rule sets applied in order.

        Rule application order:
        whitespace → punctuation → case → numbers → custom
        """
        for rule in self.active_rules():
            text = rule.apply(text)
        return text

    def normalize_batch(self, texts: list[str]) -> list[str]:
        """Return a new list with :meth:`normalize` applied to every element."""
        return [self.normalize(t) for t in texts]

    def add_rule(self, rule: NormRule) -> None:
        """Append *rule* to the custom rules list."""
        self._config.custom_rules.append(rule)

    def active_rules(self) -> list[NormRule]:
        """Return all rules that will be applied, in application order."""
        rules: list[NormRule] = []
        if self._config.apply_whitespace:
            rules.extend(whitespace_rules())
        if self._config.apply_punctuation:
            rules.extend(punctuation_rules())
        if self._config.apply_case:
            rules.extend(case_rules())
        if self._config.apply_numbers:
            rules.extend(number_rules())
        rules.extend(self._config.custom_rules)
        return rules
