"""Cross-lingual support for docs-toolkit — pure stdlib, no ML dependencies.

Modules:
  - detector   — Language enum, LangDetectionResult, LanguageDetector
  - normalizer — NormalizationConfig, TextNormalizer (normalize/tokenize/stem)
  - search     — CrossLingualQuery, CrossLingualSearcher

Quickstart::

    from docstoolkit.crosslingual import (
        LanguageDetector, Language,
        TextNormalizer, NormalizationConfig,
        CrossLingualSearcher,
    )

    detector = LanguageDetector()
    result = detector.detect("Привет мир")
    assert result.language == Language.RUSSIAN

    searcher = CrossLingualSearcher()
    ranking = searcher.search("memory agent", {"doc1": "...", "doc2": "..."})
"""
from docstoolkit.crosslingual.detector import (
    Language,
    LangDetectionResult,
    LanguageDetector,
)
from docstoolkit.crosslingual.normalizer import (
    NormalizationConfig,
    TextNormalizer,
)
from docstoolkit.crosslingual.search import (
    CrossLingualQuery,
    CrossLingualSearcher,
)

__all__ = [
    # detector
    "Language",
    "LangDetectionResult",
    "LanguageDetector",
    # normalizer
    "NormalizationConfig",
    "TextNormalizer",
    # search
    "CrossLingualQuery",
    "CrossLingualSearcher",
]
