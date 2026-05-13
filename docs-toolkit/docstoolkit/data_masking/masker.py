"""Masker implementation for the E103 Data Masking module."""
import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MaskStrategy(str, Enum):
    """Strategy used to mask a field value."""
    REDACT = "redact"    # replace with "***"
    PARTIAL = "partial"  # show first N and last N chars, mask middle with "*"
    HASH = "hash"        # replace with SHA-256 hex (first 16 chars)
    NULLIFY = "nullify"  # replace with None
    FIXED = "fixed"      # replace with a fixed string


@dataclass
class MaskRule:
    """A rule that matches fields by regex pattern and specifies how to mask them."""
    field_pattern: str
    strategy: MaskStrategy = MaskStrategy.REDACT
    partial_show: int = 2          # chars to show at each end for PARTIAL
    fixed_value: str = "REDACTED"  # value used for FIXED strategy


@dataclass
class MaskConfig:
    """Configuration for a DataMasker instance."""
    rules: list[MaskRule]
    recursive: bool = True   # apply to nested dicts
    mask_keys: bool = False  # if True, also mask the key names matching rules


class DataMasker:
    """Apply field-level data masking/redaction to dicts.

    Rules are evaluated in order; the **first** matching rule wins.
    The original dict is never modified — a new dict is always returned.

    Example::

        from docstoolkit.data_masking import (
            DataMasker, MaskConfig, MaskRule, MaskStrategy,
        )

        masker = DataMasker(MaskConfig(rules=[
            MaskRule("password", MaskStrategy.REDACT),
            MaskRule(".*_token", MaskStrategy.HASH),
        ]))

        result = masker.mask({"password": "s3cr3t", "auth_token": "abc123"})
        # {"password": "***", "auth_token": "<sha256-hex[:16]>"}
    """

    def __init__(self, config: MaskConfig) -> None:
        self._config = config
        # Pre-compile all patterns for efficiency
        self._compiled: list[tuple[re.Pattern, MaskRule]] = [
            (re.compile(rule.field_pattern), rule)
            for rule in config.rules
        ]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def mask(self, data: dict) -> dict:
        """Return a new dict with fields masked per config rules.

        Does not modify the original dict.
        Rules are applied in order; first matching rule wins.
        Recurses into nested dict values when ``config.recursive`` is True.
        """
        result: dict = {}
        for key, value in data.items():
            # Optionally recurse before masking so nested values are handled
            if self._config.recursive and isinstance(value, dict):
                value = self.mask(value)

            rule = self.matched_rule(str(key))
            if rule is not None:
                masked_value = self._apply_rule(value, rule)
                masked_key = self._mask_key(str(key), rule) if self._config.mask_keys else key
            else:
                masked_value = value
                masked_key = key

            result[masked_key] = masked_value
        return result

    def mask_value(self, field_name: str, value: Any) -> Any:
        """Apply masking to a single field value.

        Returns the value unchanged if no rule matches *field_name*.
        """
        rule = self.matched_rule(field_name)
        if rule is None:
            return value
        return self._apply_rule(value, rule)

    def mask_string(
        self,
        value: str,
        strategy: MaskStrategy,
        partial_show: int = 2,
        fixed_value: str = "REDACTED",
    ) -> str:
        """Apply a specific masking strategy to a string value.

        Always returns a string (NULLIFY returns the string ``"None"`` — use
        ``mask_value`` if you need the actual ``None`` sentinel).
        """
        if strategy == MaskStrategy.REDACT:
            return "***"
        if strategy == MaskStrategy.PARTIAL:
            return self._partial(value, partial_show)
        if strategy == MaskStrategy.HASH:
            return hashlib.sha256(value.encode()).hexdigest()[:16]
        if strategy == MaskStrategy.NULLIFY:
            return str(None)
        if strategy == MaskStrategy.FIXED:
            return fixed_value
        return value  # pragma: no cover

    def should_mask(self, field_name: str) -> bool:
        """Return True if any rule matches *field_name*."""
        return self.matched_rule(field_name) is not None

    def matched_rule(self, field_name: str) -> "MaskRule | None":
        """Return the first matching rule for *field_name*, or None."""
        for pattern, rule in self._compiled:
            if pattern.fullmatch(field_name):
                return rule
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _apply_rule(self, value: Any, rule: MaskRule) -> Any:
        """Apply *rule* to an arbitrary value."""
        strategy = rule.strategy

        # NULLIFY always returns None regardless of type
        if strategy == MaskStrategy.NULLIFY:
            return None

        # For dict values, if recursive is already handled in mask(); but
        # mask_value may be called independently — leave dicts as-is here.
        if isinstance(value, str):
            return self.mask_string(
                value,
                strategy,
                partial_show=rule.partial_show,
                fixed_value=rule.fixed_value,
            )

        # Non-string types
        if strategy == MaskStrategy.REDACT:
            return "***"
        if strategy == MaskStrategy.FIXED:
            return rule.fixed_value
        if strategy == MaskStrategy.HASH:
            return hashlib.sha256(str(value).encode()).hexdigest()[:16]
        if strategy == MaskStrategy.PARTIAL:
            return self._partial(str(value), rule.partial_show)

        return value  # pragma: no cover

    @staticmethod
    def _partial(value: str, partial_show: int) -> str:
        """Return *value* with middle characters replaced by ``*``s.

        If ``partial_show == 0`` or ``len(value) <= 2 * partial_show``,
        the entire string is replaced with ``*``s of the same length.
        """
        n = len(value)
        if partial_show <= 0 or n <= 2 * partial_show:
            return "*" * n
        return value[:partial_show] + "*" * (n - 2 * partial_show) + value[n - partial_show:]

    @staticmethod
    def _mask_key(key: str, rule: MaskRule) -> str:
        """Return a masked version of a dict key using the same strategy as the value."""
        strategy = rule.strategy
        if strategy == MaskStrategy.REDACT:
            return "***"
        if strategy == MaskStrategy.FIXED:
            return rule.fixed_value
        if strategy == MaskStrategy.HASH:
            return hashlib.sha256(key.encode()).hexdigest()[:16]
        if strategy == MaskStrategy.NULLIFY:
            return str(None)
        if strategy == MaskStrategy.PARTIAL:
            return DataMasker._partial(key, rule.partial_show)
        return key  # pragma: no cover
