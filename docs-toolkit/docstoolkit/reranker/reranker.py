"""High-level PassageReranker — the main entry point for E25 re-ranking.

Pure stdlib — no sklearn, numpy, or ML libraries required.
"""
from dataclasses import dataclass, field

from docstoolkit.reranker.features import FeatureExtractor, PassageFeatures
from docstoolkit.reranker.scorer import PassageScore, PassageScorer, ScoringWeights


@dataclass
class RerankerConfig:
    """Configuration for PassageReranker.

    Parameters
    ----------
    weights:
        Scoring weights used when ranking passages.
    top_k:
        Maximum number of passages to return after re-ranking.
        If the input list is shorter, all passages are returned.
    """

    weights: ScoringWeights = field(default_factory=ScoringWeights)
    top_k: int = 10


@dataclass
class RerankResult:
    """Result of a single re-ranking operation.

    Attributes
    ----------
    query:
        The original query string.
    passages:
        PassageScore list in *original* order (rank 1 first).
    reranked:
        PassageScore list sorted by ``rerank_score`` descending,
        truncated to ``top_k``.
    """

    query: str
    passages: list[PassageScore]
    reranked: list[PassageScore]

    def improvement(self, n: int = 5) -> float:
        """Compute average position improvement for the top-n re-ranked passages.

        For each of the top-n passages in ``reranked`` (by rerank_score), the
        position improvement is ``original_rank - new_rank`` where
        ``new_rank`` is the 1-based position in the ``reranked`` list.

        A positive value means the passage moved *up* (closer to the front).

        Parameters
        ----------
        n:
            How many top re-ranked passages to consider.

        Returns
        -------
        float
            Average position change.  Returns 0.0 if there are no passages.
        """
        if not self.reranked:
            return 0.0

        top = self.reranked[:n]
        total_change = 0.0
        for new_rank_zero_based, ps in enumerate(top):
            new_rank = new_rank_zero_based + 1
            total_change += ps.original_rank - new_rank

        return total_change / len(top)


class PassageReranker:
    """Re-ranks a list of plain text passages for a given query.

    Uses FeatureExtractor to compute feature vectors and PassageScorer to
    produce a combined relevance score, then sorts by that score.

    Example::

        reranker = PassageReranker()
        result = reranker.rerank(
            query="neural network training",
            passages=["deep learning ...", "cooking recipes ..."],
        )
        for ps in result.reranked:
            print(ps.original_rank, "->", ps.rerank_score)
    """

    def __init__(self, config: RerankerConfig | None = None) -> None:
        self._config = config if config is not None else RerankerConfig()
        self._extractor = FeatureExtractor()
        self._scorer = PassageScorer()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def rerank(
        self,
        query: str,
        passages: list[str],
        titles: list[str] | None = None,
    ) -> RerankResult:
        """Re-rank *passages* for *query*.

        Parameters
        ----------
        query:
            Search query string.
        passages:
            Ordered list of passage texts.  Index 0 is rank 1 (highest
            original confidence).
        titles:
            Optional list of document titles parallel to *passages*.  When
            provided, the title_match feature is populated for each passage.

        Returns
        -------
        RerankResult
            Contains original-order scores and a re-ranked list (up to
            ``config.top_k`` entries).
        """
        if titles is None:
            titles = [""] * len(passages)

        # Pad / truncate titles to match passages length
        if len(titles) < len(passages):
            titles = list(titles) + [""] * (len(passages) - len(titles))

        # 1. Extract features for every passage (rank is 1-based)
        feature_list: list[PassageFeatures] = []
        for idx, (passage, title) in enumerate(zip(passages, titles)):
            rank = idx + 1
            feat = self._extractor.extract(query, passage, rank, title)
            feature_list.append(feat)

        # 2. Score all features
        scored: list[PassageScore] = self._scorer.score_all(
            feature_list, self._config.weights
        )

        # 3. Sort by rerank_score descending, then take top_k
        reranked = sorted(scored, key=lambda ps: ps.rerank_score, reverse=True)
        reranked = reranked[: self._config.top_k]

        return RerankResult(
            query=query,
            passages=scored,
            reranked=reranked,
        )
