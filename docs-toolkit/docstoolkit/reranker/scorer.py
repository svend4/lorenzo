"""Scoring and weight management for passage re-ranking.

Pure stdlib — no sklearn, numpy, or ML libraries required.
"""
from dataclasses import dataclass, field

from docstoolkit.reranker.features import PassageFeatures


@dataclass
class ScoringWeights:
    """Weights for each feature dimension used in passage scoring.

    All weights must be non-negative.  Call ``normalize()`` to ensure they
    sum to exactly 1.0 before scoring.
    """

    overlap: float = 0.3
    bm25: float = 0.3
    position: float = 0.2
    title: float = 0.1
    phrase: float = 0.1

    def normalize(self) -> "ScoringWeights":
        """Return a new ScoringWeights scaled so that all weights sum to 1.0.

        If the total is 0 (all weights are 0), returns the original object
        unchanged to avoid division by zero.
        """
        total = self.overlap + self.bm25 + self.position + self.title + self.phrase
        if total == 0.0:
            return ScoringWeights(
                overlap=self.overlap,
                bm25=self.bm25,
                position=self.position,
                title=self.title,
                phrase=self.phrase,
            )
        return ScoringWeights(
            overlap=self.overlap / total,
            bm25=self.bm25 / total,
            position=self.position / total,
            title=self.title / total,
            phrase=self.phrase / total,
        )


@dataclass
class PassageScore:
    """Scored passage combining original rank, rerank score, and features."""

    passage_id: str
    original_rank: int
    rerank_score: float
    features: PassageFeatures


class PassageScorer:
    """Computes weighted relevance scores for PassageFeatures objects.

    Usage::

        scorer = PassageScorer()
        score = scorer.score(features)
        all_scores = scorer.score_all(feature_list)
    """

    _default_weights: ScoringWeights = ScoringWeights()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def score(
        self,
        features: PassageFeatures,
        weights: ScoringWeights | None = None,
    ) -> float:
        """Compute a single weighted relevance score for *features*.

        The BM25 score is normalised via ``bm25 / (bm25 + 1)`` to map it into
        [0, 1) before weighting.  Boolean features (title_match,
        exact_phrase_match) are cast to 1.0/0.0.

        Parameters
        ----------
        features:
            Feature vector for one passage.
        weights:
            Optional custom weights.  Defaults to ``ScoringWeights()``.

        Returns
        -------
        float
            Weighted score in [0, +inf).
        """
        w = weights if weights is not None else self._default_weights

        bm25_norm = features.bm25_score / (features.bm25_score + 1.0)
        title_val = 1.0 if features.title_match else 0.0
        phrase_val = 1.0 if features.exact_phrase_match else 0.0

        return (
            features.query_term_overlap * w.overlap
            + bm25_norm * w.bm25
            + features.position_score * w.position
            + title_val * w.title
            + phrase_val * w.phrase
        )

    def score_all(
        self,
        feature_list: list[PassageFeatures],
        weights: ScoringWeights | None = None,
    ) -> list[PassageScore]:
        """Score every PassageFeatures in *feature_list*.

        Parameters
        ----------
        feature_list:
            List of feature vectors; list index 0 corresponds to rank 1.
        weights:
            Optional custom weights forwarded to ``score()``.

        Returns
        -------
        list[PassageScore]
            One PassageScore per input feature, in the same order as the input.
            ``original_rank`` is derived from the feature's ``position_score``
            via ``round(1.0 / position_score)`` when position_score > 0,
            otherwise falls back to ``list index + 1``.
        """
        result: list[PassageScore] = []
        for idx, feat in enumerate(feature_list):
            s = self.score(feat, weights)
            if feat.position_score > 0.0:
                original_rank = round(1.0 / feat.position_score)
            else:
                original_rank = idx + 1
            result.append(
                PassageScore(
                    passage_id=feat.passage_id,
                    original_rank=original_rank,
                    rerank_score=s,
                    features=feat,
                )
            )
        return result
