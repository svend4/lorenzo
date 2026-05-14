"""Cross-lingual search — pure stdlib.

Provides:
  - CrossLingualQuery    — dataclass representing a prepared query
  - CrossLingualSearcher — prepare / score / search
"""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.crosslingual.detector import Language, LanguageDetector
from docstoolkit.crosslingual.normalizer import NormalizationConfig, TextNormalizer


@dataclass
class CrossLingualQuery:
    original: str
    language: Language
    normalized: str
    tokens: list[str]


class CrossLingualSearcher:
    """Score and rank documents against a query using token-overlap BM-lite."""

    def __init__(
        self,
        detector: LanguageDetector | None = None,
        normalizer: TextNormalizer | None = None,
    ) -> None:
        self._detector = detector or LanguageDetector()
        self._normalizer = normalizer or TextNormalizer()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def prepare_query(self, query: str) -> CrossLingualQuery:
        """Detect language and normalize *query* into a CrossLingualQuery."""
        result = self._detector.detect(query)
        normalized = self._normalizer.normalize(query)
        tokens = self._normalizer.tokenize(query)
        return CrossLingualQuery(
            original=query,
            language=result.language,
            normalized=normalized,
            tokens=tokens,
        )

    def score(self, query: CrossLingualQuery, document: str) -> float:
        """Compute overlap score between *query* and *document*.

        Score = |query_tokens ∩ doc_tokens| / (|query_tokens| + 1)

        For MIXED queries a stemmed overlap is also computed and the
        maximum of the two is returned.
        """
        doc_tokens = set(self._normalizer.tokenize(document))
        query_set = set(query.tokens)

        base_score = len(query_set & doc_tokens) / (len(query_set) + 1)

        if query.language == Language.MIXED:
            # Try stemmed overlap for both RU and EN
            stemmed_query = self._stem_tokens(query.tokens, query.language)
            stemmed_doc = self._stem_tokens(list(doc_tokens), query.language)
            stemmed_score = len(set(stemmed_query) & set(stemmed_doc)) / (
                len(stemmed_query) + 1
            )
            return max(base_score, stemmed_score)

        return base_score

    def search(
        self,
        query: str,
        documents: dict[str, str],
    ) -> list[tuple[str, float]]:
        """Score all *documents* against *query*, return sorted desc by score.

        Returns a list of (doc_id, score) pairs.
        """
        prepared = self.prepare_query(query)
        scored = [
            (doc_id, self.score(prepared, text))
            for doc_id, text in documents.items()
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _stem_tokens(self, tokens: list[str], language: Language) -> list[str]:
        """Apply appropriate stemmer based on *language*."""
        if language == Language.RUSSIAN:
            return [self._normalizer.stem_ru(t) for t in tokens]
        if language == Language.ENGLISH:
            return [self._normalizer.stem_en(t) for t in tokens]
        # MIXED — apply both stemmers and keep all results
        stemmed: list[str] = []
        for t in tokens:
            stemmed.append(self._normalizer.stem_ru(t))
            stemmed.append(self._normalizer.stem_en(t))
        return stemmed
