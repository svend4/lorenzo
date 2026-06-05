"""TF-IDF document classifier — stdlib only, no external dependencies.

Groups documents by section (first subdir name), builds per-section centroid
TF-IDF vectors, then classifies new documents by cosine similarity.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Stopwords (mirrored from embeddings/tfidf.py)
# ---------------------------------------------------------------------------
_STOP_WORDS: frozenset[str] = frozenset({
    # ru
    "и", "в", "на", "что", "как", "это", "для", "или", "но", "не", "по", "с", "из",
    "к", "у", "о", "за", "от", "до", "же", "ли", "бы",
    # en
    "the", "a", "an", "of", "in", "to", "is", "are", "for", "and", "or", "but",
    "with", "on", "at", "by", "as", "be", "this", "that",
})


def _tokenize(text: str) -> list[str]:
    """Same tokenizer used in embeddings/tfidf.py."""
    words = re.findall(r"[a-zа-яё][a-zа-яё\-]{2,}", text.lower())
    return [w for w in words if w not in _STOP_WORDS]


def _cosine_sparse(a: dict[str, float], b: dict[str, float]) -> float:
    if not a or not b:
        return 0.0
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[t] * b[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return dot / (norm_a * norm_b)


# ---------------------------------------------------------------------------
# Public dataclass
# ---------------------------------------------------------------------------
@dataclass
class ClassificationResult:
    """Result of classifying a single document."""
    suggested_section: str
    confidence: float
    alternatives: list[tuple[str, float]] = field(default_factory=list)
    top_terms: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------
class TfidfClassifier:
    """Per-section centroid TF-IDF classifier.

    1. ``fit`` computes IDF over all docs, then builds per-section centroid
       vectors (average of individual TF-IDF vectors for that section).
    2. ``classify`` computes TF-IDF of query against the corpus IDF, then
       returns cosine similarity to each centroid.
    3. ``explain`` shows top-5 terms driving similarity for each section.
    """

    def __init__(self, min_docs_per_section: int = 3) -> None:
        self.min_docs_per_section = min_docs_per_section
        # {term: idf_value}
        self._idf: dict[str, float] = {}
        # {section: {term: centroid_weight}}
        self._centroids: dict[str, dict[str, float]] = {}
        self._fitted = False

    # ------------------------------------------------------------------
    # fit / fit_from_docs_dir
    # ------------------------------------------------------------------
    def fit(self, corpus: dict[str, list[str]]) -> None:
        """Fit on *corpus* = {section_name: [doc_text, ...]}.

        Sections with fewer than ``min_docs_per_section`` docs are skipped.
        """
        # Filter sections
        valid: dict[str, list[str]] = {
            sec: docs
            for sec, docs in corpus.items()
            if len(docs) >= self.min_docs_per_section
        }
        if not valid:
            raise ValueError(
                f"No section has >= {self.min_docs_per_section} documents."
            )

        # Build flat list for IDF
        all_texts: list[str] = [t for docs in valid.values() for t in docs]
        n_docs = len(all_texts)

        # Document frequency
        df: Counter = Counter()
        for text in all_texts:
            tokens = set(_tokenize(text))
            for t in tokens:
                df[t] += 1

        self._idf = {
            t: math.log((n_docs + 1) / (cnt + 1)) + 1.0
            for t, cnt in df.items()
        }

        # Build per-section centroids
        self._centroids = {}
        for section, docs in valid.items():
            vecs = [self._tfidf_vec(doc) for doc in docs]
            centroid = self._average_vecs(vecs)
            if centroid:
                self._centroids[section] = centroid

        self._fitted = True

    @classmethod
    def fit_from_docs_dir(
        cls,
        docs_dir: Path,
        min_docs_per_section: int = 3,
    ) -> "TfidfClassifier":
        """Walk *docs_dir*, group .md files by first subdir name, and fit.

        Example layout::

            docs_dir/
              section-a/file1.md
              section-a/subdir/file2.md
              section-b/file3.md
        """
        corpus: dict[str, list[str]] = {}
        docs_dir = Path(docs_dir)
        for md_file in sorted(docs_dir.rglob("*.md")):
            # Relative to docs_dir → first part is the section name
            try:
                rel = md_file.relative_to(docs_dir)
            except ValueError:
                continue
            parts = rel.parts
            if len(parts) < 2:
                # file directly in docs_dir — skip or assign to root
                section = "__root__"
            else:
                section = parts[0]
            text = md_file.read_text(encoding="utf-8", errors="replace")
            corpus.setdefault(section, []).append(text)

        obj = cls(min_docs_per_section=min_docs_per_section)
        obj.fit(corpus)
        return obj

    # ------------------------------------------------------------------
    # classify / explain
    # ------------------------------------------------------------------
    def classify(self, text: str) -> ClassificationResult:
        """Classify *text* against fitted centroids."""
        self._check_fitted()
        query_vec = self._tfidf_vec(text)

        scores: list[tuple[str, float]] = []
        for section, centroid in self._centroids.items():
            sim = _cosine_sparse(query_vec, centroid)
            scores.append((section, sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        best_section, best_score = scores[0]
        alternatives = scores[1:]

        top_terms = self._top_contributing_terms(query_vec, self._centroids[best_section])

        return ClassificationResult(
            suggested_section=best_section,
            confidence=best_score,
            alternatives=alternatives,
            top_terms=top_terms,
        )

    def explain(self, text: str) -> dict[str, list[tuple[str, float]]]:
        """For each section return top-5 terms with their similarity contribution."""
        self._check_fitted()
        query_vec = self._tfidf_vec(text)
        result: dict[str, list[tuple[str, float]]] = {}
        for section, centroid in self._centroids.items():
            result[section] = self._top_contributing_terms(
                query_vec, centroid, n=5, with_scores=True
            )
        return result

    # ------------------------------------------------------------------
    # save / load
    # ------------------------------------------------------------------
    def save(self, path: Path) -> None:
        """Serialize centroids + idf to JSON."""
        path = Path(path)
        data = {
            "idf": self._idf,
            "centroids": self._centroids,
            "min_docs_per_section": self.min_docs_per_section,
        }
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def load(self, path: Path) -> None:
        """Load centroids + idf from JSON (in-place)."""
        path = Path(path)
        data = json.loads(path.read_text(encoding="utf-8"))
        self._idf = data["idf"]
        self._centroids = data["centroids"]
        self.min_docs_per_section = data.get(
            "min_docs_per_section", self.min_docs_per_section
        )
        self._fitted = True

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------
    def _tfidf_vec(self, text: str) -> dict[str, float]:
        tokens = _tokenize(text)
        if not tokens:
            return {}
        tf = Counter(tokens)
        total = sum(tf.values())
        vec: dict[str, float] = {}
        for t, cnt in tf.items():
            tf_norm = cnt / total
            idf = self._idf.get(t, 1.0)
            vec[t] = tf_norm * idf
        return vec

    @staticmethod
    def _average_vecs(vecs: list[dict[str, float]]) -> dict[str, float]:
        if not vecs:
            return {}
        acc: Counter = Counter()
        for v in vecs:
            for t, w in v.items():
                acc[t] += w
        n = len(vecs)
        return {t: w / n for t, w in acc.items()}

    @staticmethod
    def _top_contributing_terms(
        query_vec: dict[str, float],
        centroid: dict[str, float],
        n: int = 5,
        with_scores: bool = False,
    ):
        """Return terms that contribute most to the dot product (cosine numerator)."""
        contributions: list[tuple[str, float]] = []
        for t in set(query_vec) & set(centroid):
            score = query_vec[t] * centroid[t]
            contributions.append((t, score))
        contributions.sort(key=lambda x: x[1], reverse=True)
        top = contributions[:n]
        if with_scores:
            return top
        return [t for t, _ in top]

    def _check_fitted(self) -> None:
        if not self._fitted:
            raise RuntimeError("TfidfClassifier must be fitted before use.")
