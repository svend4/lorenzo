"""Multi-signal document ranker.

Combines configurable signals (relevance, recency, popularity, length,
authority, freshness) with min-max normalization and weighted aggregation.

Stdlib only.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum


class RankSignal(Enum):
    """Available ranking signals."""

    RELEVANCE = "relevance"
    RECENCY = "recency"
    POPULARITY = "popularity"
    LENGTH = "length"
    AUTHORITY = "authority"
    FRESHNESS = "freshness"


@dataclass
class SignalScore:
    """Score for a single signal applied to a document."""

    signal: RankSignal
    raw_value: float
    normalized: float


@dataclass
class RankedDoc:
    """Result for one document after ranking."""

    doc_id: str
    final_score: float
    signal_scores: dict[RankSignal, SignalScore]
    rank: int


@dataclass
class RankConfig:
    """Configuration for the ranker."""

    weights: dict[RankSignal, float] = field(
        default_factory=lambda: {RankSignal.RELEVANCE: 1.0}
    )
    normalize_scores: bool = True
    boost_recent_days: int = 30


@dataclass
class DocInfo:
    """Per-document input information for ranking."""

    doc_id: str
    relevance: float = 0.0
    created_at: float = 0.0
    popularity: int = 0
    length: int = 0
    authority: float = 0.0


class DocRanker:
    """Rank documents by combining multiple signals."""

    def __init__(self, config: RankConfig = None) -> None:
        self.config = config if config is not None else RankConfig()

    # ------------------------------------------------------------------
    # Signal computation
    # ------------------------------------------------------------------

    @staticmethod
    def _raw_signal(doc: DocInfo, signal: RankSignal, now: float, boost_recent_days: int) -> float:
        """Compute raw signal value for a single document."""
        if signal == RankSignal.RELEVANCE:
            return float(doc.relevance)
        if signal == RankSignal.RECENCY:
            age_days = (now - doc.created_at) / 86400.0
            if age_days < 0:
                age_days = 0.0
            return 1.0 / (1.0 + age_days)
        if signal == RankSignal.POPULARITY:
            pop = doc.popularity if doc.popularity >= 0 else 0
            return math.log(1.0 + pop)
        if signal == RankSignal.LENGTH:
            val = 1.0 - abs(doc.length - 1000) / 1000.0
            if val < 0.0:
                val = 0.0
            if val > 1.0:
                val = 1.0
            return val
        if signal == RankSignal.AUTHORITY:
            return float(doc.authority)
        if signal == RankSignal.FRESHNESS:
            age_days = (now - doc.created_at) / 86400.0
            if age_days < 0:
                age_days = 0.0
            return 1.0 if age_days < boost_recent_days else 0.0
        return 0.0

    def score_signal(
        self,
        docs: list[DocInfo],
        signal: RankSignal,
        now: float = 0.0,
    ) -> list[SignalScore]:
        """Compute SignalScore for all docs for one signal."""
        raws = [
            self._raw_signal(doc, signal, now, self.config.boost_recent_days)
            for doc in docs
        ]
        if self.config.normalize_scores:
            norms = self.normalize_signals(raws)
        else:
            norms = list(raws)
        return [
            SignalScore(signal=signal, raw_value=raw, normalized=norm)
            for raw, norm in zip(raws, norms)
        ]

    # ------------------------------------------------------------------
    # Normalization & combination
    # ------------------------------------------------------------------

    @staticmethod
    def normalize_signals(scores: list[float]) -> list[float]:
        """Min-max normalize values into [0, 1]."""
        if not scores:
            return []
        lo = min(scores)
        hi = max(scores)
        if hi == lo:
            return [1.0] * len(scores)
        span = hi - lo
        return [(v - lo) / span for v in scores]

    @staticmethod
    def combine_scores(
        scores: dict[RankSignal, float],
        weights: dict[RankSignal, float],
    ) -> float:
        """Compute weighted sum over signals that appear in weights."""
        total = 0.0
        matched = False
        for signal, weight in weights.items():
            if signal in scores:
                total += scores[signal] * weight
                matched = True
        if not matched:
            return 0.0
        return total

    # ------------------------------------------------------------------
    # Ranking
    # ------------------------------------------------------------------

    def rank(self, docs: list[DocInfo], now: float = 0.0) -> list[RankedDoc]:
        """Rank all docs using all signals present in config.weights."""
        if not docs:
            return []

        weights = self.config.weights
        # Build per-doc signal score map.
        per_signal: dict[RankSignal, list[SignalScore]] = {}
        for signal in weights:
            per_signal[signal] = self.score_signal(docs, signal, now=now)

        ranked: list[RankedDoc] = []
        for idx, doc in enumerate(docs):
            signal_scores: dict[RankSignal, SignalScore] = {}
            score_map: dict[RankSignal, float] = {}
            for signal, scores in per_signal.items():
                ss = scores[idx]
                signal_scores[signal] = ss
                score_map[signal] = ss.normalized
            final = self.combine_scores(score_map, weights)
            ranked.append(
                RankedDoc(
                    doc_id=doc.doc_id,
                    final_score=final,
                    signal_scores=signal_scores,
                    rank=0,
                )
            )

        ranked.sort(key=lambda r: r.final_score, reverse=True)
        for i, r in enumerate(ranked):
            r.rank = i + 1
        return ranked

    def top_k(
        self,
        docs: list[DocInfo],
        k: int,
        now: float = 0.0,
    ) -> list[RankedDoc]:
        """Return only the top-k ranked documents."""
        if k <= 0:
            return []
        return self.rank(docs, now=now)[:k]

    def rerank(
        self,
        ranked: list[RankedDoc],
        boost_ids: set[str],
        boost_factor: float = 1.5,
    ) -> list[RankedDoc]:
        """Multiply final score by boost_factor for docs whose id is in boost_ids."""
        boosted: list[RankedDoc] = []
        for r in ranked:
            new_score = r.final_score * boost_factor if r.doc_id in boost_ids else r.final_score
            boosted.append(
                RankedDoc(
                    doc_id=r.doc_id,
                    final_score=new_score,
                    signal_scores=dict(r.signal_scores),
                    rank=0,
                )
            )
        boosted.sort(key=lambda x: x.final_score, reverse=True)
        for i, r in enumerate(boosted):
            r.rank = i + 1
        return boosted
