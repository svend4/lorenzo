"""Content recommendation module for docs-toolkit.

Provides a three-layer recommendation stack:

* :mod:`~docstoolkit.recommender.profile` — user interest modelling
* :mod:`~docstoolkit.recommender.scorer` — per-document scoring
* :mod:`~docstoolkit.recommender.engine` — end-to-end pipeline with diversity

Quickstart::

    from docstoolkit.recommender import (
        UserProfile, ContentScorer, RecommendationEngine,
        RecommendationConfig, Recommendation, RecommendationScore,
    )

    profile = UserProfile(user_id="alice")
    profile.tags["python"] = 0.9
    profile.query_history.append("memory agent")

    engine = RecommendationEngine(RecommendationConfig(top_k=5))
    recs = engine.recommend(
        profile,
        docs={"doc1": "python memory agent article", "doc2": "java web framework"},
        doc_tags={"doc1": ["python", "agent"], "doc2": ["java", "web"]},
    )
    for r in recs:
        print(r.rank, r.doc_id, r.score, r.reasons)
"""
from docstoolkit.recommender.profile import UserProfile
from docstoolkit.recommender.scorer import RecommendationScore, ContentScorer
from docstoolkit.recommender.engine import (
    RecommendationConfig,
    Recommendation,
    RecommendationEngine,
)

__all__ = [
    # profile
    "UserProfile",
    # scorer
    "RecommendationScore",
    "ContentScorer",
    # engine
    "RecommendationConfig",
    "Recommendation",
    "RecommendationEngine",
]
