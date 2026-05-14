"""Voice distance: compare two EpistemicProfiles."""

import math
from dataclasses import dataclass
from docstoolkit.epistemic.profile import EpistemicProfile

# Dimension names matching to_vector() order
_DIM_NAMES = [
    "strong_claim_rate",
    "hedge_rate",
    "stance_ratio",
    "avg_sentence_length_norm",
    "citation_density",
    "ttr",
    "hapax_ratio",
]


@dataclass
class VoiceComparison:
    distance: float           # 0-1: 0=identical voice, 1=maximally different
    similarity: float         # 1 - distance
    dominant_difference: str  # which dimension differs most
    assessment: str           # "same_voice" | "similar" | "different" | "opposite"


def _euclidean(v1: list[float], v2: list[float]) -> float:
    """Normalised Euclidean distance between two vectors, clipped to [0, 1].

    Normalise by dividing the raw Euclidean distance by ``sqrt(len(v1))``
    so that the theoretical maximum (each dimension differs by 1) maps to 1.0.
    """
    raw = math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))
    n = len(v1)
    normalised = raw / math.sqrt(n) if n > 0 else 0.0
    return max(0.0, min(1.0, normalised))


def voice_distance(
    profile_a: EpistemicProfile,
    profile_b: EpistemicProfile,
) -> VoiceComparison:
    """Compare two epistemic profiles.

    Parameters
    ----------
    profile_a, profile_b:
        The profiles to compare.

    Returns
    -------
    VoiceComparison
        ``distance`` is the normalised Euclidean distance (clipped to [0, 1]).
        ``similarity`` = 1 − distance.
        ``dominant_difference`` is the name of the vector dimension where
        ``|a[i] − b[i]|`` is largest.
        ``assessment`` is one of:

        * ``"same_voice"`` — distance < 0.15
        * ``"similar"`` — distance < 0.35
        * ``"different"`` — distance < 0.60
        * ``"opposite"`` — distance ≥ 0.60
    """
    vec_a = profile_a.to_vector()
    vec_b = profile_b.to_vector()

    distance = _euclidean(vec_a, vec_b)
    similarity = 1.0 - distance

    # Dominant difference: dimension index with largest absolute delta
    deltas = [abs(a - b) for a, b in zip(vec_a, vec_b)]
    dom_idx = deltas.index(max(deltas))
    dominant_difference = _DIM_NAMES[dom_idx]

    # Assessment thresholds
    if distance < 0.15:
        assessment = "same_voice"
    elif distance < 0.35:
        assessment = "similar"
    elif distance < 0.60:
        assessment = "different"
    else:
        assessment = "opposite"

    return VoiceComparison(
        distance=distance,
        similarity=similarity,
        dominant_difference=dominant_difference,
        assessment=assessment,
    )
