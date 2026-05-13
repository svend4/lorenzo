"""Distance and similarity metrics for sparse TF-IDF vectors (E20)."""

from __future__ import annotations

import math


def cosine_similarity(a: dict[str, float], b: dict[str, float]) -> float:
    """Cosine similarity between two sparse TF-IDF vectors.

    Returns 0.0 if either vector is empty or has zero magnitude.
    """
    if not a or not b:
        return 0.0

    # Dot product (only over shared keys for efficiency).
    dot = sum(a[k] * b[k] for k in a if k in b)
    if dot == 0.0:
        return 0.0

    mag_a = math.sqrt(sum(v * v for v in a.values()))
    mag_b = math.sqrt(sum(v * v for v in b.values()))

    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0

    return dot / (mag_a * mag_b)


def cosine_distance(a: dict[str, float], b: dict[str, float]) -> float:
    """Cosine distance: 1 - cosine_similarity(a, b)."""
    return 1.0 - cosine_similarity(a, b)


def jaccard_similarity(a: set, b: set) -> float:
    """Jaccard similarity: |intersection| / |union|.

    Returns 0.0 if both sets are empty.
    """
    if not a and not b:
        return 0.0
    intersection = len(a & b)
    union = len(a | b)
    if union == 0:
        return 0.0
    return intersection / union
