"""Text normalizer v2 — advanced unicode and whitespace normalization."""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class NormalizationRule(Enum):
    """Supported normalization rules."""

    NFC = "NFC"
    NFKC = "NFKC"
    NFD = "NFD"
    NFKD = "NFKD"
    LOWERCASE = "LOWERCASE"
    UPPERCASE = "UPPERCASE"
    STRIP_ACCENTS = "STRIP_ACCENTS"
    COLLAPSE_WHITESPACE = "COLLAPSE_WHITESPACE"
    NORMALIZE_QUOTES = "NORMALIZE_QUOTES"
    NORMALIZE_DASHES = "NORMALIZE_DASHES"
    REMOVE_ZWSP = "REMOVE_ZWSP"


@dataclass
class NormalizationConfig:
    """Configuration for text normalization pipeline."""

    unicode_form: str = "NFC"
    lowercase: bool = False
    strip_accents: bool = False
    collapse_whitespace: bool = True
    normalize_quotes: bool = True
    normalize_dashes: bool = True
    remove_zero_width: bool = True
    preserve_newlines: bool = True


@dataclass
class NormalizationResult:
    """Result of applying normalization to a text."""

    original: str
    normalized: str
    rules_applied: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        """True when the normalized text differs from the original."""
        return self.original != self.normalized

    @property
    def char_diff(self) -> int:
        """Absolute character-length difference between original and normalized."""
        return abs(len(self.original) - len(self.normalized))


# --- character tables -------------------------------------------------------

_SMART_QUOTES_DOUBLE = {
    "“": '"',  # LEFT DOUBLE QUOTATION MARK
    "”": '"',  # RIGHT DOUBLE QUOTATION MARK
    "„": '"',  # DOUBLE LOW-9 QUOTATION MARK
    "‟": '"',  # DOUBLE HIGH-REVERSED-9 QUOTATION MARK
    "«": '"',  # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    "»": '"',  # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
}

_SMART_QUOTES_SINGLE = {
    "‘": "'",  # LEFT SINGLE QUOTATION MARK
    "’": "'",  # RIGHT SINGLE QUOTATION MARK
    "‚": "'",  # SINGLE LOW-9 QUOTATION MARK
    "‛": "'",  # SINGLE HIGH-REVERSED-9 QUOTATION MARK
}

_SMART_DASHES = {
    "—": "-",  # EM DASH
    "–": "-",  # EN DASH
    "‒": "-",  # FIGURE DASH
    "―": "-",  # HORIZONTAL BAR
}

_ZERO_WIDTH_CHARS = {
    "​",  # ZERO WIDTH SPACE
    "‌",  # ZERO WIDTH NON-JOINER
    "‍",  # ZERO WIDTH JOINER
    "﻿",  # ZERO WIDTH NO-BREAK SPACE (BOM)
}

_QUOTE_TRANSLATE = str.maketrans({**_SMART_QUOTES_DOUBLE, **_SMART_QUOTES_SINGLE})
_DASH_TRANSLATE = str.maketrans(_SMART_DASHES)
_ZWSP_TRANSLATE = str.maketrans({c: None for c in _ZERO_WIDTH_CHARS})

_RE_INLINE_WS = re.compile(r"[ \t\f\v\r ]+")
_RE_ANY_WS = re.compile(r"\s+")
_RE_NEWLINES = re.compile(r"\n+")


class TextNormalizer:
    """Apply a configurable pipeline of normalization rules."""

    def __init__(self, config: Optional[NormalizationConfig] = None) -> None:
        self.config = config or NormalizationConfig()

    # --- individual rules --------------------------------------------------

    def unicode_normalize(self, text: str, form: str = "NFC") -> str:
        """Apply unicode normalization (NFC/NFKC/NFD/NFKD)."""
        if not form:
            return text
        if form not in ("NFC", "NFKC", "NFD", "NFKD"):
            raise ValueError(f"Unsupported unicode form: {form!r}")
        return unicodedata.normalize(form, text)

    def strip_accents(self, text: str) -> str:
        """Remove combining diacritical marks (e.g. café -> cafe)."""
        decomposed = unicodedata.normalize("NFD", text)
        return "".join(c for c in decomposed if unicodedata.category(c) != "Mn")

    def collapse_whitespace(self, text: str, preserve_newlines: bool = True) -> str:
        """Collapse runs of whitespace into a single space."""
        if preserve_newlines:
            # Collapse inline whitespace (space, tab, NBSP, ...) but keep newlines.
            collapsed = _RE_INLINE_WS.sub(" ", text)
            # Collapse multiple consecutive newlines into one.
            collapsed = _RE_NEWLINES.sub("\n", collapsed)
            # Trim spaces around newlines.
            collapsed = re.sub(r" *\n *", "\n", collapsed)
            return collapsed
        return _RE_ANY_WS.sub(" ", text)

    def normalize_quotes(self, text: str) -> str:
        """Replace smart quotes with their ASCII equivalents."""
        return text.translate(_QUOTE_TRANSLATE)

    def normalize_dashes(self, text: str) -> str:
        """Replace em/en/figure dashes with hyphen-minus."""
        return text.translate(_DASH_TRANSLATE)

    def remove_zero_width(self, text: str) -> str:
        """Strip zero-width characters (ZWSP, ZWNJ, ZWJ, BOM)."""
        return text.translate(_ZWSP_TRANSLATE)

    def lowercase(self, text: str) -> str:
        """Return lowercased text."""
        return text.lower()

    # --- pipeline ----------------------------------------------------------

    def normalize(self, text: str) -> NormalizationResult:
        """Apply the configured normalization pipeline to `text`."""
        cfg = self.config
        original = text
        rules_applied: list[str] = []
        current = text

        if cfg.unicode_form:
            new = self.unicode_normalize(current, cfg.unicode_form)
            if new != current:
                rules_applied.append(cfg.unicode_form)
                current = new

        if cfg.remove_zero_width:
            new = self.remove_zero_width(current)
            if new != current:
                rules_applied.append(NormalizationRule.REMOVE_ZWSP.value)
                current = new

        if cfg.normalize_quotes:
            new = self.normalize_quotes(current)
            if new != current:
                rules_applied.append(NormalizationRule.NORMALIZE_QUOTES.value)
                current = new

        if cfg.normalize_dashes:
            new = self.normalize_dashes(current)
            if new != current:
                rules_applied.append(NormalizationRule.NORMALIZE_DASHES.value)
                current = new

        if cfg.strip_accents:
            new = self.strip_accents(current)
            if new != current:
                rules_applied.append(NormalizationRule.STRIP_ACCENTS.value)
                current = new

        if cfg.lowercase:
            new = self.lowercase(current)
            if new != current:
                rules_applied.append(NormalizationRule.LOWERCASE.value)
                current = new

        if cfg.collapse_whitespace:
            new = self.collapse_whitespace(current, cfg.preserve_newlines)
            if new != current:
                rules_applied.append(NormalizationRule.COLLAPSE_WHITESPACE.value)
                current = new

        return NormalizationResult(
            original=original,
            normalized=current,
            rules_applied=rules_applied,
        )

    def normalize_batch(self, texts: list[str]) -> list[NormalizationResult]:
        """Normalize a batch of texts."""
        return [self.normalize(t) for t in texts]
