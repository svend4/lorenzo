"""Search backends for hybrid search: BM25 and Keyword (Jaccard)."""
from __future__ import annotations

import math
from abc import ABC, abstractmethod
from collections import Counter


def _tokenize(text: str) -> list[str]:
    """Lowercase and split on whitespace/punctuation."""
    import re
    return re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", text.lower())


class SearchBackend(ABC):
    """Abstract base class for search backends."""

    @abstractmethod
    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """Search for documents matching the query.

        Returns list of (doc_id, score) sorted descending by score.
        """

    @abstractmethod
    def doc_count(self) -> int:
        """Return the number of indexed documents."""


class BM25Backend(SearchBackend):
    """BM25 search backend with TF-IDF weighting.

    Parameters
    ----------
    k1:
        Term frequency saturation parameter (default 1.5).
    b:
        Field length normalization parameter (default 0.75).
    """

    def __init__(self, documents: dict[str, str] = None, k1: float = 1.5, b: float = 0.75):
        self._k1 = k1
        self._b = b
        self._doc_ids: list[str] = []
        # tf[doc_id][term] = raw term frequency
        self._tf: dict[str, Counter] = {}
        # idf[term] = log((N - df + 0.5) / (df + 0.5) + 1)
        self._idf: dict[str, float] = {}
        self._doc_lengths: dict[str, int] = {}
        self._avg_dl: float = 0.0
        self._n_docs: int = 0

        if documents:
            self.index(documents)

    def index(self, documents: dict[str, str]) -> None:
        """Build BM25 index from documents.

        Args:
            documents: mapping of doc_id -> text content.
        """
        self._doc_ids = list(documents.keys())
        self._n_docs = len(self._doc_ids)
        self._tf = {}
        self._doc_lengths = {}

        for doc_id, text in documents.items():
            tokens = _tokenize(text)
            self._tf[doc_id] = Counter(tokens)
            self._doc_lengths[doc_id] = len(tokens)

        total_length = sum(self._doc_lengths.values())
        self._avg_dl = total_length / self._n_docs if self._n_docs > 0 else 0.0

        # Compute IDF for all terms
        df: dict[str, int] = Counter()
        for tf in self._tf.values():
            for term in tf:
                df[term] += 1

        self._idf = {}
        n = self._n_docs
        for term, freq in df.items():
            self._idf[term] = math.log((n - freq + 0.5) / (freq + 0.5) + 1)

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """BM25 search.

        Returns list of (doc_id, score) sorted descending, top_k results.
        """
        if not self._doc_ids:
            return []

        query_terms = _tokenize(query)
        scores: dict[str, float] = {}

        for doc_id in self._doc_ids:
            dl = self._doc_lengths.get(doc_id, 0)
            tf_doc = self._tf.get(doc_id, Counter())
            score = 0.0
            for term in query_terms:
                if term not in self._idf:
                    continue
                idf = self._idf[term]
                tf = tf_doc.get(term, 0)
                numerator = tf * (self._k1 + 1)
                denominator = tf + self._k1 * (1 - self._b + self._b * dl / (self._avg_dl or 1))
                score += idf * numerator / denominator if denominator != 0 else 0.0
            if score > 0:
                scores[doc_id] = score

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def doc_count(self) -> int:
        """Return number of indexed documents."""
        return self._n_docs


class KeywordBackend(SearchBackend):
    """Keyword search backend using exact token overlap (Jaccard similarity).

    Scores documents by Jaccard similarity between query token set
    and document token set.
    """

    def __init__(self, documents: dict[str, str] = None):
        self._doc_ids: list[str] = []
        self._doc_tokens: dict[str, set[str]] = {}
        self._n_docs: int = 0

        if documents:
            self.index(documents)

    def index(self, documents: dict[str, str]) -> None:
        """Build keyword index from documents.

        Args:
            documents: mapping of doc_id -> text content.
        """
        self._doc_ids = list(documents.keys())
        self._n_docs = len(self._doc_ids)
        self._doc_tokens = {}

        for doc_id, text in documents.items():
            tokens = _tokenize(text)
            self._doc_tokens[doc_id] = set(tokens)

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """Keyword search using Jaccard similarity.

        score = |query_tokens ∩ doc_tokens| / |query_tokens ∪ doc_tokens|

        Returns list of (doc_id, score) sorted descending, top_k results.
        """
        if not self._doc_ids:
            return []

        query_tokens = set(_tokenize(query))
        if not query_tokens:
            return []

        scores: dict[str, float] = {}
        for doc_id, doc_tokens in self._doc_tokens.items():
            if not doc_tokens:
                continue
            intersection = len(query_tokens & doc_tokens)
            if intersection == 0:
                continue
            union = len(query_tokens | doc_tokens)
            scores[doc_id] = intersection / union if union > 0 else 0.0

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return ranked[:top_k]

    def doc_count(self) -> int:
        """Return number of indexed documents."""
        return self._n_docs
