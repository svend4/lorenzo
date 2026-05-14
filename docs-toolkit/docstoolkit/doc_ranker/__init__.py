"""Multi-signal document ranker for docs-toolkit.

Ranks documents by combining multiple configurable signals
(relevance, recency, popularity, length, authority, freshness)
using weighted sum aggregation.

Usage:
    from docstoolkit.doc_ranker import (
        DocRanker, DocInfo, RankedDoc, RankConfig,
        RankSignal, SignalScore,
    )

    config = RankConfig(weights={
        RankSignal.RELEVANCE: 0.6,
        RankSignal.RECENCY: 0.4,
    })
    ranker = DocRanker(config)
    docs = [DocInfo(doc_id="a", relevance=0.9, created_at=now)]
    ranked = ranker.rank(docs, now=now)
"""
from docstoolkit.doc_ranker.ranker import (
    DocInfo,
    DocRanker,
    RankConfig,
    RankedDoc,
    RankSignal,
    SignalScore,
)

__all__ = [
    "DocInfo",
    "DocRanker",
    "RankConfig",
    "RankedDoc",
    "RankSignal",
    "SignalScore",
]
