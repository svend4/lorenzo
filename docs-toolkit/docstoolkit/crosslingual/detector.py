"""Language detector — pure stdlib, no ML dependencies.

Detects language based on character ratios (Cyrillic vs Latin).

Supported languages:
  - RUSSIAN  — Cyrillic dominates (ru_ratio > 0.7)
  - ENGLISH  — Latin dominates (en_ratio > 0.7)
  - MIXED    — both scripts present (both > 0.2)
  - UNKNOWN  — text too short or indeterminate
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Language(Enum):
    RUSSIAN = "russian"
    ENGLISH = "english"
    MIXED = "mixed"
    UNKNOWN = "unknown"


@dataclass
class LangDetectionResult:
    language: Language
    confidence: float  # 0–1
    ru_ratio: float
    en_ratio: float

    def is_confident(self, threshold: float = 0.7) -> bool:
        """Return True if confidence >= threshold."""
        return self.confidence >= threshold


class LanguageDetector:
    """Detect language of text using character-ratio heuristics.

    Algorithm:
      1. Count Cyrillic chars (U+0400–U+04FF) and ASCII Latin chars (a-z A-Z).
      2. ru_ratio = cyrillic / (cyrillic + latin + 1)
      3. en_ratio = 1 - ru_ratio
      4. Classify based on thresholds.
    """

    def detect(self, text: str) -> LangDetectionResult:
        """Detect language of *text* and return a LangDetectionResult."""
        cyrillic = sum(1 for ch in text if "Ѐ" <= ch <= "ӿ")
        latin = sum(
            1 for ch in text if ("a" <= ch <= "z") or ("A" <= ch <= "Z")
        )

        total = cyrillic + latin
        # Use +1 denominator to avoid div-by-zero and dampen short texts
        ru_ratio = cyrillic / (total + 1)
        en_ratio = 1.0 - ru_ratio
        confidence = max(ru_ratio, en_ratio)

        # Too short — not enough signal
        if total < 10:
            return LangDetectionResult(
                language=Language.UNKNOWN,
                confidence=confidence,
                ru_ratio=ru_ratio,
                en_ratio=en_ratio,
            )

        if ru_ratio > 0.7:
            language = Language.RUSSIAN
        elif en_ratio > 0.7:
            language = Language.ENGLISH
        elif ru_ratio > 0.2 and en_ratio > 0.2:
            language = Language.MIXED
        else:
            language = Language.UNKNOWN

        return LangDetectionResult(
            language=language,
            confidence=confidence,
            ru_ratio=ru_ratio,
            en_ratio=en_ratio,
        )

    def detect_batch(self, texts: list[str]) -> list[LangDetectionResult]:
        """Detect language for each text in *texts*."""
        return [self.detect(t) for t in texts]
