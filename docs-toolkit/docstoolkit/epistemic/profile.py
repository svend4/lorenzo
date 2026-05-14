"""Epistemic profile measurement: stance, hedging, citation density, lexical richness."""

import re
import math
from dataclasses import dataclass, field
from collections import Counter

# ---------------------------------------------------------------------------
# Marker lists
# ---------------------------------------------------------------------------

_STRONG_MARKERS = [
    "proven", "clearly", "definitely", "certainly", "undoubtedly",
    "always", "never", "must", "will", "is a fact",
    "доказано", "очевидно", "определённо", "безусловно", "всегда", "никогда",
]
_HEDGE_MARKERS = [
    "perhaps", "maybe", "possibly", "probably", "might", "could", "seems",
    "suggests", "appears", "likely", "unlikely", "arguably", "approximately",
    "возможно", "вероятно", "кажется", "похоже", "по-видимому", "примерно",
]
_CITATION_PATTERNS = [
    r'\[\d+\]',                       # [1], [23]
    r'\([A-Z][a-z]+\s+\d{4}\)',       # (Author 2023)
    r'см\.\s',                         # см. (Russian "see")
    r'source:',
]


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class EpistemicProfile:
    """Multidimensional epistemic style measurement."""

    # Stance
    strong_claim_rate: float = 0.0   # strong markers per 100 words
    hedge_rate: float = 0.0          # hedge markers per 100 words
    stance_ratio: float = 0.0        # hedge / (strong + hedge + 1), 0=assertive, 1=cautious

    # Structure
    avg_sentence_length: float = 0.0  # words per sentence
    citation_density: float = 0.0     # citation patterns per 100 words

    # Lexical richness
    ttr: float = 0.0                  # type-token ratio (unique/total)
    hapax_ratio: float = 0.0          # hapax legomena / total words

    # Derived
    sophistication: float = 0.0       # weighted combination (0-1)

    def to_vector(self) -> list[float]:
        """7-dim vector for distance calculation (excluding sophistication).

        All dimensions are normalised to [0, 1]:
        - strong_claim_rate: capped at 10 per-100-words (÷10, clipped)
        - hedge_rate:         capped at 10 per-100-words (÷10, clipped)
        - stance_ratio:       already in [0, 1]
        - avg_sentence_length/30: normalized so 30 words = 1.0, clipped
        - citation_density:  capped at 5 per-100-words (÷5, clipped)
        - ttr:                already in [0, 1]
        - hapax_ratio:        already in [0, 1]
        """
        def _clip(v: float) -> float:
            return max(0.0, min(1.0, v))

        return [
            _clip(self.strong_claim_rate / 10.0),
            _clip(self.hedge_rate / 10.0),
            self.stance_ratio,
            _clip(self.avg_sentence_length / 30.0),
            _clip(self.citation_density / 5.0),
            self.ttr,
            self.hapax_ratio,
        ]


# ---------------------------------------------------------------------------
# Core measurement
# ---------------------------------------------------------------------------

def _count_markers(text_lower: str, markers: list[str]) -> int:
    """Count how many marker phrases appear in text (case-insensitive, multi-word aware)."""
    count = 0
    for marker in markers:
        # Use word-boundary matching for single-word markers; substring for phrases
        if " " in marker:
            count += text_lower.count(marker)
        else:
            count += len(re.findall(r'\b' + re.escape(marker) + r'\b', text_lower))
    return count


def measure_profile(text: str) -> EpistemicProfile:
    """Measure epistemic profile of *text*.

    Steps
    -----
    1. Tokenise with ``re.findall(r'\\b\\w+\\b', text.lower())`` for word lists.
    2. Count strong/hedge markers (case-insensitive).
    3. Compute per-100-word rates and stance_ratio.
    4. Split sentences on ``[.!?]+`` to get avg_sentence_length.
    5. Count citation patterns for citation_density.
    6. Compute TTR and hapax_ratio from the word list.
    7. Compute sophistication = 0.3·ttr + 0.3·(1−stance_ratio)
       + 0.2·min(avg_sentence_length/30, 1) + 0.2·min(citation_density/5, 1).
    """
    if not text or not text.strip():
        return EpistemicProfile()

    text_lower = text.lower()

    # 1. Word list
    words_list = re.findall(r'\b\w+\b', text_lower)
    word_count = len(words_list)

    if word_count == 0:
        return EpistemicProfile()

    # 2. Stance markers
    strong_count = _count_markers(text_lower, _STRONG_MARKERS)
    hedge_count = _count_markers(text_lower, _HEDGE_MARKERS)

    # 3. Per-100-word rates and stance_ratio
    strong_claim_rate = 100.0 * strong_count / word_count
    hedge_rate = 100.0 * hedge_count / word_count
    stance_ratio = hedge_count / (strong_count + hedge_count + 1)

    # 4. Sentence splitting → avg_sentence_length
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    if sentences:
        sentence_lengths = [
            len(re.findall(r'\b\w+\b', s)) for s in sentences
        ]
        non_empty = [l for l in sentence_lengths if l > 0]
        avg_sentence_length = sum(non_empty) / len(non_empty) if non_empty else 0.0
    else:
        avg_sentence_length = 0.0

    # 5. Citation density
    citation_count = sum(
        len(re.findall(pattern, text, re.IGNORECASE))
        for pattern in _CITATION_PATTERNS
    )
    citation_density = 100.0 * citation_count / word_count

    # 6. Lexical richness
    freq = Counter(words_list)
    unique_words = len(freq)
    ttr = unique_words / word_count
    hapax = sum(1 for cnt in freq.values() if cnt == 1)
    hapax_ratio = hapax / word_count

    # 7. Sophistication (all sub-terms are in [0, 1])
    sent_norm = min(avg_sentence_length / 30.0, 1.0)
    cite_norm = min(citation_density / 5.0, 1.0)
    sophistication = (
        0.3 * ttr
        + 0.3 * (1.0 - stance_ratio)
        + 0.2 * sent_norm
        + 0.2 * cite_norm
    )
    # Clamp just in case of floating-point drift
    sophistication = max(0.0, min(1.0, sophistication))

    return EpistemicProfile(
        strong_claim_rate=strong_claim_rate,
        hedge_rate=hedge_rate,
        stance_ratio=stance_ratio,
        avg_sentence_length=avg_sentence_length,
        citation_density=citation_density,
        ttr=ttr,
        hapax_ratio=hapax_ratio,
        sophistication=sophistication,
    )


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate_profiles(profiles: list[EpistemicProfile]) -> EpistemicProfile:
    """Return the mean of *profiles* as a single corpus-level EpistemicProfile."""
    if not profiles:
        return EpistemicProfile()

    n = len(profiles)
    fields = [
        "strong_claim_rate", "hedge_rate", "stance_ratio",
        "avg_sentence_length", "citation_density",
        "ttr", "hapax_ratio", "sophistication",
    ]
    averages = {
        f: sum(getattr(p, f) for p in profiles) / n
        for f in fields
    }
    return EpistemicProfile(**averages)
