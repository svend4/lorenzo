"""KeywordExtractor — TF-IDF based keyword extraction, stdlib only."""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Keyword:
    """A single extracted keyword with scoring metadata."""

    term: str
    score: float
    frequency: int
    doc_frequency: int


@dataclass
class ExtractionConfig:
    """Configuration for keyword extraction."""

    max_keywords: int = 10
    min_freq: int = 1
    min_length: int = 3
    max_length: int = 50
    use_bigrams: bool = False
    stop_words: set[str] = field(default_factory=set)


class KeywordExtractor:
    """TF-IDF based keyword extractor using stdlib only.

    Workflow:
        1. Optionally call :meth:`fit` with a list of documents to build an IDF
           table.  Without fitting, :meth:`extract` falls back to TF-only scoring.
        2. Call :meth:`extract` on any text to get a ranked list of
           :class:`Keyword` objects.

    Parameters
    ----------
    config:
        An :class:`ExtractionConfig` instance.  Defaults to
        ``ExtractionConfig()`` when *None* is supplied.
    """

    def __init__(self, config: Optional[ExtractionConfig] = None) -> None:
        self._config: ExtractionConfig = config if config is not None else ExtractionConfig()
        # Maps term -> number of corpus documents that contain the term.
        self._df: dict[str, int] = {}
        # Total number of documents seen during fit.
        self._n_docs: int = 0

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_fitted(self) -> bool:
        """True after :meth:`fit` has been called with at least one document."""
        return self._n_docs > 0

    @property
    def vocabulary_size(self) -> int:
        """Number of distinct terms in the IDF vocabulary."""
        return len(self._df)

    @property
    def top_keywords(self) -> list[str]:
        """Top terms ordered by IDF score descending (most discriminative first).

        Returns an empty list when the extractor has not been fitted.
        """
        if not self.is_fitted:
            return []
        scored = [
            (term, self._idf(term))
            for term in self._df
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [t for t, _ in scored[: self._config.max_keywords]]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fit(self, documents: list[str]) -> None:
        """Build the IDF table from *documents*.

        Repeated calls replace the previous IDF table entirely.

        Parameters
        ----------
        documents:
            A list of raw text strings forming the reference corpus.
        """
        self._df = {}
        self._n_docs = len(documents)
        for doc in documents:
            tokens = set(self._tokenize(doc))
            for token in tokens:
                self._df[token] = self._df.get(token, 0) + 1

    def extract(self, text: str, top_k: Optional[int] = None) -> list[Keyword]:
        """Extract keywords from *text* sorted by TF-IDF score descending.

        Parameters
        ----------
        text:
            The document to extract keywords from.
        top_k:
            Maximum number of keywords to return.  When *None*, falls back to
            ``config.max_keywords``.

        Returns
        -------
        list[Keyword]
            Keywords sorted by score descending.
        """
        limit = top_k if top_k is not None else self._config.max_keywords
        tokens = self._tokenize(text)
        if not tokens:
            return []

        # Raw term counts
        tf_counts: dict[str, int] = {}
        for t in tokens:
            tf_counts[t] = tf_counts.get(t, 0) + 1

        total = len(tokens)
        cfg = self._config

        results: list[Keyword] = []
        for term, count in tf_counts.items():
            if count < cfg.min_freq:
                continue
            tf = count / total
            idf = self._idf(term)
            score = tf * idf
            doc_freq = self._df.get(term, 0) if self.is_fitted else 0
            results.append(
                Keyword(
                    term=term,
                    score=score,
                    frequency=count,
                    doc_frequency=doc_freq,
                )
            )

        results.sort(key=lambda k: k.score, reverse=True)
        return results[:limit]

    def extract_batch(
        self, texts: list[str], top_k: Optional[int] = None
    ) -> list[list[Keyword]]:
        """Apply :meth:`extract` to every element of *texts*.

        Parameters
        ----------
        texts:
            A list of documents to process.
        top_k:
            Forwarded to :meth:`extract`.

        Returns
        -------
        list[list[Keyword]]
            One list of keywords per input document, in the same order.
        """
        return [self.extract(text, top_k=top_k) for text in texts]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _tokenize(self, text: str) -> list[str]:
        """Return tokens from *text* after applying all config filters."""
        cfg = self._config
        pattern = rf"[a-zа-яё]{{{cfg.min_length},{cfg.max_length}}}"
        tokens = re.findall(pattern, text.lower())
        # Apply stop words filter
        if cfg.stop_words:
            tokens = [t for t in tokens if t not in cfg.stop_words]
        if cfg.use_bigrams:
            unigrams = tokens
            bigrams = [f"{unigrams[i]}_{unigrams[i + 1]}" for i in range(len(unigrams) - 1)]
            tokens = unigrams + bigrams
        return tokens

    def _idf(self, term: str) -> float:
        """Return IDF for *term*.

        Formula: ``log((1 + N) / (1 + df)) + 1``

        When the extractor is not fitted returns 1.0 so that TF-IDF
        degrades gracefully to plain TF.
        """
        if not self.is_fitted:
            return 1.0
        df = self._df.get(term, 0)
        return math.log((1 + self._n_docs) / (1 + df)) + 1
