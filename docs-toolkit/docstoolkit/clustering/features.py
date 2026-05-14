"""TF-IDF feature extraction for document clustering (E20)."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field


@dataclass
class DocumentFeatures:
    """TF-IDF feature vector for a single document."""

    doc_id: str
    tokens: list[str]
    tfidf: dict[str, float]


_NON_ALPHA = re.compile(r"[^a-zA-ZЀ-ӿ]+")


def _tokenize(text: str) -> list[str]:
    """Lowercase and split on non-alphabetic characters (Latin + Cyrillic)."""
    return [t for t in _NON_ALPHA.split(text.lower()) if t]


class FeatureExtractor:
    """Fits IDF from a corpus and transforms documents into TF-IDF vectors."""

    def __init__(self) -> None:
        self._idf: dict[str, float] = {}
        self._n_docs: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fit(self, docs: dict[str, str]) -> None:
        """Compute IDF weights from *docs* mapping doc_id -> text.

        IDF formula: log((N + 1) / (df + 1)) + 1
        where N is the number of documents and df is the document frequency
        of the term.
        """
        n = len(docs)
        self._n_docs = n

        # Count document frequency for every term.
        df: dict[str, int] = {}
        for text in docs.values():
            seen = set(_tokenize(text))
            for token in seen:
                df[token] = df.get(token, 0) + 1

        self._idf = {
            term: math.log((n + 1) / (count + 1)) + 1
            for term, count in df.items()
        }

    def transform(self, doc_id: str, text: str) -> DocumentFeatures:
        """Return TF-IDF features for a single document.

        TF is raw term frequency divided by document length (L1-normalised).
        Unknown terms (not in the fitted vocabulary) receive IDF = log(2) + 1
        (as if df = N, i.e. present in every document).
        """
        tokens = _tokenize(text)
        if not tokens:
            return DocumentFeatures(doc_id=doc_id, tokens=[], tfidf={})

        # Raw term counts -> TF (relative frequency).
        tf_raw: dict[str, int] = {}
        for t in tokens:
            tf_raw[t] = tf_raw.get(t, 0) + 1
        total = len(tokens)

        # Fallback IDF for out-of-vocabulary terms.
        n = max(self._n_docs, 1)
        fallback_idf = math.log((n + 1) / (n + 1)) + 1  # = log(1) + 1 = 1.0

        tfidf: dict[str, float] = {}
        for term, count in tf_raw.items():
            tf = count / total
            idf = self._idf.get(term, fallback_idf)
            tfidf[term] = tf * idf

        return DocumentFeatures(doc_id=doc_id, tokens=tokens, tfidf=tfidf)

    def fit_transform(self, docs: dict[str, str]) -> list[DocumentFeatures]:
        """Fit on *docs* then return feature vectors for all documents."""
        self.fit(docs)
        return [self.transform(doc_id, text) for doc_id, text in docs.items()]

    def vocabulary_size(self) -> int:
        """Number of terms in the fitted vocabulary."""
        return len(self._idf)
