"""E25 Passage re-ranking module.

Pure stdlib implementation — no sklearn, numpy, or ML libraries required.

Quick start::

    from docstoolkit.reranker import PassageReranker

    reranker = PassageReranker()
    result = reranker.rerank(
        query="neural network training",
        passages=["deep learning tutorial ...", "cooking recipes ..."],
    )
    for ps in result.reranked:
        print(ps.original_rank, "->", round(ps.rerank_score, 4))

Public names
------------
features:
    PassageFeatures, FeatureExtractor

scorer:
    ScoringWeights, PassageScore, PassageScorer

reranker:
    RerankerConfig, RerankResult, PassageReranker
"""

from docstoolkit.reranker.features import FeatureExtractor, PassageFeatures
from docstoolkit.reranker.scorer import PassageScore, PassageScorer, ScoringWeights
from docstoolkit.reranker.reranker import (
    PassageReranker,
    RerankResult,
    RerankerConfig,
)

__all__ = [
    # features
    "PassageFeatures",
    "FeatureExtractor",
    # scorer
    "ScoringWeights",
    "PassageScore",
    "PassageScorer",
    # reranker
    "RerankerConfig",
    "RerankResult",
    "PassageReranker",
]
