"""text_similarity.similarity — core similarity algorithms (stdlib only)."""
from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple


def _tokenize(text: str) -> List[str]:
    """Tokenize text into lowercase words."""
    return re.findall(r'\b\w+\b', text.lower())


class SimilarityMethod(Enum):
    JACCARD = "jaccard"
    COSINE = "cosine"
    OVERLAP = "overlap"
    LEVENSHTEIN = "levenshtein"
    DICE = "dice"


@dataclass
class SimilarityResult:
    """Result of a similarity computation."""
    method: SimilarityMethod
    score: float  # 0.0–1.0
    text_a: str
    text_b: str

    def __post_init__(self) -> None:
        if not (0.0 <= self.score <= 1.0):
            raise ValueError(f"score must be in [0.0, 1.0], got {self.score}")


class TextSimilarity:
    """Computes similarity between texts using multiple algorithms."""

    # ------------------------------------------------------------------
    # Individual methods
    # ------------------------------------------------------------------

    @staticmethod
    def jaccard(a: str, b: str) -> float:
        """Jaccard similarity on word sets: |A ∩ B| / |A ∪ B|."""
        set_a = set(_tokenize(a))
        set_b = set(_tokenize(b))
        if not set_a and not set_b:
            return 0.0
        intersection = set_a & set_b
        union = set_a | set_b
        return len(intersection) / len(union)

    @staticmethod
    def cosine(a: str, b: str) -> float:
        """Cosine similarity on TF word vectors."""
        tokens_a = _tokenize(a)
        tokens_b = _tokenize(b)
        if not tokens_a or not tokens_b:
            return 0.0
        freq_a = Counter(tokens_a)
        freq_b = Counter(tokens_b)
        # dot product
        dot = sum(freq_a[t] * freq_b[t] for t in freq_a if t in freq_b)
        # magnitudes
        mag_a = math.sqrt(sum(v * v for v in freq_a.values()))
        mag_b = math.sqrt(sum(v * v for v in freq_b.values()))
        if mag_a == 0.0 or mag_b == 0.0:
            return 0.0
        return dot / (mag_a * mag_b)

    @staticmethod
    def overlap(a: str, b: str) -> float:
        """Overlap coefficient: |A ∩ B| / min(|A|, |B|) on word sets."""
        set_a = set(_tokenize(a))
        set_b = set(_tokenize(b))
        if not set_a or not set_b:
            return 0.0
        intersection = set_a & set_b
        return len(intersection) / min(len(set_a), len(set_b))

    @staticmethod
    def levenshtein(a: str, b: str) -> float:
        """Character-level Levenshtein similarity: 1 - edit_distance / max(len(a), len(b))."""
        if not a and not b:
            return 1.0
        max_len = max(len(a), len(b))
        if max_len == 0:
            return 1.0
        # DP edit distance
        m, n = len(a), len(b)
        # Use two rows to save memory
        prev = list(range(n + 1))
        curr = [0] * (n + 1)
        for i in range(1, m + 1):
            curr[0] = i
            for j in range(1, n + 1):
                if a[i - 1] == b[j - 1]:
                    cost = 0
                else:
                    cost = 1
                curr[j] = min(
                    prev[j] + 1,      # deletion
                    curr[j - 1] + 1,  # insertion
                    prev[j - 1] + cost,  # substitution
                )
            prev, curr = curr, prev
        edit_dist = prev[n]
        return 1.0 - edit_dist / max_len

    @staticmethod
    def dice(a: str, b: str) -> float:
        """Dice coefficient on word sets: 2|A ∩ B| / (|A| + |B|)."""
        set_a = set(_tokenize(a))
        set_b = set(_tokenize(b))
        if not set_a and not set_b:
            return 0.0
        if not set_a or not set_b:
            return 0.0
        intersection = set_a & set_b
        return 2 * len(intersection) / (len(set_a) + len(set_b))

    # ------------------------------------------------------------------
    # High-level API
    # ------------------------------------------------------------------

    def similarity(
        self,
        a: str,
        b: str,
        method: SimilarityMethod = SimilarityMethod.JACCARD,
    ) -> SimilarityResult:
        """Compute similarity using the specified method and return a SimilarityResult."""
        dispatch = {
            SimilarityMethod.JACCARD: self.jaccard,
            SimilarityMethod.COSINE: self.cosine,
            SimilarityMethod.OVERLAP: self.overlap,
            SimilarityMethod.LEVENSHTEIN: self.levenshtein,
            SimilarityMethod.DICE: self.dice,
        }
        fn = dispatch[method]
        score = fn(a, b)
        return SimilarityResult(method=method, score=score, text_a=a, text_b=b)

    def most_similar(
        self,
        query: str,
        candidates: List[str],
        method: SimilarityMethod = SimilarityMethod.COSINE,
        top_k: int = 5,
    ) -> List[Tuple[int, float]]:
        """Return (index, score) pairs sorted descending by score, up to top_k."""
        dispatch = {
            SimilarityMethod.JACCARD: self.jaccard,
            SimilarityMethod.COSINE: self.cosine,
            SimilarityMethod.OVERLAP: self.overlap,
            SimilarityMethod.LEVENSHTEIN: self.levenshtein,
            SimilarityMethod.DICE: self.dice,
        }
        fn = dispatch[method]
        scored = [(i, fn(query, c)) for i, c in enumerate(candidates)]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def all_similarities(self, a: str, b: str) -> dict:
        """Compute similarity using all methods and return a dict keyed by SimilarityMethod."""
        return {
            SimilarityMethod.JACCARD: self.jaccard(a, b),
            SimilarityMethod.COSINE: self.cosine(a, b),
            SimilarityMethod.OVERLAP: self.overlap(a, b),
            SimilarityMethod.LEVENSHTEIN: self.levenshtein(a, b),
            SimilarityMethod.DICE: self.dice(a, b),
        }
