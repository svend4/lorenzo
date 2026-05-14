"""Text normalizer for cross-lingual processing — pure stdlib.

Provides:
  - NormalizationConfig  — options dataclass
  - TextNormalizer       — normalize / tokenize / stem_ru / stem_en
"""
from __future__ import annotations

import re
import string
from dataclasses import dataclass, field


@dataclass
class NormalizationConfig:
    lowercase: bool = True
    strip_punctuation: bool = False
    strip_numbers: bool = False
    collapse_whitespace: bool = True


# Russian suffixes to strip (longest first so more-specific rules win)
_RU_SUFFIXES = (
    # Genitive / dative long forms
    "ого", "его", "ому", "ему",
    # Short adjective endings
    "ый", "ий", "ой",
    # Feminine / neuter adj endings
    "ая", "яя", "ое", "ее", "ые", "ие",
    # Instrumental / prepositional plural
    "ами", "ями", "ах", "ях",
    # Genitive plural
    "ов", "ев", "ей",
    # Soft-sign forms
    "ью", "ьи",
)

# English suffixes to strip (longest first)
_EN_SUFFIXES = (
    "tion", "ness", "ment",
    "ing", "est", "ed", "er", "ly",
)


class TextNormalizer:
    """Normalize and tokenize text; includes lightweight stemmers."""

    def normalize(
        self,
        text: str,
        config: NormalizationConfig | None = None,
    ) -> str:
        """Apply normalization steps defined in *config* to *text*."""
        if config is None:
            config = NormalizationConfig()

        if config.lowercase:
            text = text.lower()

        if config.strip_punctuation:
            text = text.translate(str.maketrans("", "", string.punctuation))

        if config.strip_numbers:
            text = re.sub(r"\d+", "", text)

        if config.collapse_whitespace:
            text = re.sub(r"\s+", " ", text).strip()

        return text

    def tokenize(self, text: str) -> list[str]:
        """Normalize *text* (default config) then split on whitespace."""
        normalized = self.normalize(text)
        return [t for t in normalized.split(" ") if t]

    def stem_ru(self, token: str) -> str:
        """Strip common Russian suffixes from *token* if len > 4."""
        if len(token) <= 4:
            return token
        lower = token.lower()
        for suffix in _RU_SUFFIXES:
            if lower.endswith(suffix) and len(lower) - len(suffix) >= 2:
                return lower[: len(lower) - len(suffix)]
        return lower

    def stem_en(self, token: str) -> str:
        """Strip common English suffixes from *token* if len > 4."""
        if len(token) <= 4:
            return token
        lower = token.lower()
        for suffix in _EN_SUFFIXES:
            if lower.endswith(suffix) and len(lower) - len(suffix) >= 2:
                return lower[: len(lower) - len(suffix)]
        return lower
