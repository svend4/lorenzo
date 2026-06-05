"""TrustScorer: aggregate trust signals into a single TrustScore."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.trust_scoring.signals import (
    SignalScore,
    TrustSignal,
    TrustSignalExtractor,
)


@dataclass
class TrustWeights:
    """Per-signal weights used to compute the overall trust score."""

    source: float = 0.25
    recency: float = 0.20
    citations: float = 0.20
    author: float = 0.15
    consistency: float = 0.10
    cross_val: float = 0.10

    def normalize(self) -> "TrustWeights":
        """Return a new TrustWeights scaled so that all weights sum to 1.0."""
        total = (
            self.source
            + self.recency
            + self.citations
            + self.author
            + self.consistency
            + self.cross_val
        )
        if total == 0:
            raise ValueError("Sum of weights must not be zero.")
        return TrustWeights(
            source=self.source / total,
            recency=self.recency / total,
            citations=self.citations / total,
            author=self.author / total,
            consistency=self.consistency / total,
            cross_val=self.cross_val / total,
        )


@dataclass
class TrustScore:
    """Aggregated trust score for a single document."""

    doc_id: str
    overall: float  # 0-1
    grade: str      # A / B / C / D / F
    signals: list[SignalScore] = field(default_factory=list)

    def dominant_signal(self) -> TrustSignal:
        """Return the signal with the highest weighted_score."""
        if not self.signals:
            raise ValueError("No signals available.")
        return max(self.signals, key=lambda s: s.weighted_score()).signal

    def weak_signals(self, threshold: float = 0.3) -> list[TrustSignal]:
        """Return signals whose *normalized* value is below *threshold*."""
        return [s.signal for s in self.signals if s.normalized < threshold]


class TrustScorer:
    """Compute TrustScore objects from document metadata and content."""

    def __init__(
        self,
        weights: TrustWeights | None = None,
        extractor: TrustSignalExtractor | None = None,
    ) -> None:
        self._weights = (weights or TrustWeights()).normalize()
        self._extractor = extractor or TrustSignalExtractor()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def score(
        self,
        doc_id: str,
        content: str,
        source_url: str = "",
        days_old: float = 0,
        citation_count: int = 0,
        author_score: float = 0.5,
    ) -> TrustScore:
        """Compute a TrustScore for the given document.

        Parameters
        ----------
        doc_id:
            Unique identifier for the document.
        content:
            Full text of the document (used for consistency analysis).
        source_url:
            URL from which the document originated.
        days_old:
            Age of the document in days.
        citation_count:
            Number of times the document has been cited.
        author_score:
            Pre-computed author reputation score in [0, 1].
        """
        w = self._weights
        ex = self._extractor

        # --- Extract raw values ----------------------------------------
        sq_raw = ex.source_quality(source_url)
        re_raw = ex.recency(days_old)
        ci_raw = ex.citation_count(citation_count)
        au_raw = float(max(0.0, min(1.0, author_score)))
        co_raw = ex.content_consistency(content)
        cv_raw = 0.0  # CROSS_VALIDATION — no automatic extractor; use default

        # --- Build SignalScore list ------------------------------------
        signals = [
            SignalScore(TrustSignal.SOURCE_QUALITY,      sq_raw, sq_raw, w.source),
            SignalScore(TrustSignal.RECENCY,             re_raw, re_raw, w.recency),
            SignalScore(TrustSignal.CITATION_COUNT,      ci_raw, ci_raw, w.citations),
            SignalScore(TrustSignal.AUTHOR_REPUTATION,   au_raw, au_raw, w.author),
            SignalScore(TrustSignal.CONTENT_CONSISTENCY, co_raw, co_raw, w.consistency),
            SignalScore(TrustSignal.CROSS_VALIDATION,    cv_raw, cv_raw, w.cross_val),
        ]

        overall = sum(s.weighted_score() for s in signals)
        overall = max(0.0, min(1.0, overall))

        return TrustScore(
            doc_id=doc_id,
            overall=overall,
            grade=self._grade(overall),
            signals=signals,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _grade(score: float) -> str:
        """Convert a 0-1 score to a letter grade."""
        if score >= 0.8:
            return "A"
        if score >= 0.6:
            return "B"
        if score >= 0.4:
            return "C"
        if score >= 0.2:
            return "D"
        return "F"
