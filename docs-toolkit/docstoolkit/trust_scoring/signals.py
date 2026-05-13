"""Trust signal extraction: source quality, recency, citations, consistency."""
import math
import re
from dataclasses import dataclass, field
from enum import Enum


class TrustSignal(Enum):
    SOURCE_QUALITY = "source_quality"
    RECENCY = "recency"
    CITATION_COUNT = "citation_count"
    AUTHOR_REPUTATION = "author_reputation"
    CONTENT_CONSISTENCY = "content_consistency"
    CROSS_VALIDATION = "cross_validation"


@dataclass
class SignalScore:
    signal: TrustSignal
    raw_value: float
    normalized: float  # 0-1
    weight: float = 1.0

    def weighted_score(self) -> float:
        """Return normalized * weight."""
        return self.normalized * self.weight


# Trusted domains that receive full 1.0 score
_TRUSTED_DOMAINS: frozenset[str] = frozenset(
    ["github.com", "arxiv.org", "wikipedia.org", "docs.python.org"]
)

# Regex to extract the netloc / suffix from a URL
_URL_RE = re.compile(r'^https?://([^/]+)', re.IGNORECASE)

# Sentence-boundary split: split on '. ', '! ', '? ' or end-of-string
_SENTENCE_RE = re.compile(r'(?<=[.!?])\s+')


class TrustSignalExtractor:
    """Extract individual trust signals from document metadata and content."""

    # ------------------------------------------------------------------
    # Public signal extractors
    # ------------------------------------------------------------------

    def source_quality(self, source_url: str) -> float:
        """Return a quality score based on the domain of *source_url*.

        Rules:
        - Known trusted list (github.com / arxiv.org / wikipedia.org /
          docs.python.org): 1.0
        - .edu or .gov TLD: 0.7
        - .com or .org TLD: 0.5
        - anything else (unknown / empty): 0.3
        """
        if not source_url:
            return 0.3

        m = _URL_RE.match(source_url.strip())
        if not m:
            return 0.3

        host = m.group(1).lower()
        # Strip port if present
        host = host.split(":")[0]

        # Exact domain match (also handle www. prefix)
        bare = host[4:] if host.startswith("www.") else host
        if bare in _TRUSTED_DOMAINS:
            return 1.0
        # Also match sub-domains, e.g. subdomain.github.com
        for trusted in _TRUSTED_DOMAINS:
            if host.endswith("." + trusted):
                return 1.0

        # TLD-based rules
        parts = host.rsplit(".", 1)
        tld = parts[-1] if len(parts) == 2 else ""
        if tld in ("edu", "gov"):
            return 0.7
        if tld in ("com", "org"):
            return 0.5

        return 0.3

    def recency(self, days_old: float) -> float:
        """Return exp(-days_old / 365). Range: (0, 1], where 1 = today."""
        if days_old < 0:
            days_old = 0.0
        return math.exp(-days_old / 365.0)

    def citation_count(self, count: int) -> float:
        """Return min(count / 100, 1.0)."""
        if count < 0:
            count = 0
        return min(count / 100.0, 1.0)

    def content_consistency(self, text: str) -> float:
        """Measure sentence-length consistency as a proxy for content quality.

        Heuristic:
          1. Split text into sentences.
          2. Compute the coefficient of variation (std / mean) of sentence
             lengths (in words).
          3. Return 1 - min(cv, 1.0) so that uniform texts score close to 1
             and highly variable texts score close to 0.

        Edge cases:
          - Empty text or single sentence → 1.0 (cannot measure variance).
        """
        if not text or not text.strip():
            return 1.0

        sentences = [s.strip() for s in _SENTENCE_RE.split(text) if s.strip()]
        if len(sentences) <= 1:
            return 1.0

        lengths = [len(s.split()) for s in sentences]
        n = len(lengths)
        mean = sum(lengths) / n
        if mean == 0:
            return 1.0

        variance = sum((l - mean) ** 2 for l in lengths) / n
        std = math.sqrt(variance)
        cv = std / mean  # coefficient of variation

        return 1.0 - min(cv, 1.0)
