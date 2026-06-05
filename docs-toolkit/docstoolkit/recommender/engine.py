"""RecommendationEngine — orchestrates scoring, filtering and diversity."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.recommender.profile import UserProfile
from docstoolkit.recommender.scorer import ContentScorer, RecommendationScore


@dataclass
class RecommendationConfig:
    """Configuration for :class:`RecommendationEngine`.

    Attributes:
        top_k: Maximum number of recommendations to return.
        exclude_seen: When *True*, documents already in the user's
            :meth:`~UserProfile.seen_docs` set are excluded.
        diversity_factor: Penalty weight applied to documents that share more
            than 50 % of their tags with already-selected documents.
    """

    top_k: int = 10
    exclude_seen: bool = True
    diversity_factor: float = 0.1


@dataclass
class Recommendation:
    """A single ranked recommendation result.

    Attributes:
        doc_id: Identifier of the recommended document.
        score: Final score after diversity adjustment.
        rank: 1-based rank within the recommendation list.
        reasons: Human-readable explanation strings from the scorer.
    """

    doc_id: str
    score: float
    rank: int
    reasons: list[str] = field(default_factory=list)


def _tag_overlap_ratio(tags_a: list[str], tags_b: list[str]) -> float:
    """Fraction of *tags_a* that also appear in *tags_b*."""
    if not tags_a:
        return 0.0
    set_b = set(tags_b)
    overlap = sum(1 for t in tags_a if t in set_b)
    return overlap / len(tags_a)


class RecommendationEngine:
    """End-to-end recommendation pipeline.

    1. Scores all documents with :class:`~docstoolkit.recommender.scorer.ContentScorer`.
    2. Optionally excludes documents the user has already seen.
    3. Applies a diversity penalty to avoid tag-homogeneous result lists.
    4. Returns the top-*k* results as :class:`Recommendation` objects.
    """

    def __init__(
        self,
        config: RecommendationConfig | None = None,
        scorer: ContentScorer | None = None,
    ) -> None:
        self.config = config or RecommendationConfig()
        self.scorer = scorer or ContentScorer()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def recommend(
        self,
        profile: UserProfile,
        docs: dict[str, str],
        doc_tags: dict[str, list[str]] | None = None,
    ) -> list[Recommendation]:
        """Generate ranked recommendations for *profile*.

        Parameters
        ----------
        profile:
            The user whose interests drive the recommendations.
        docs:
            Mapping of ``doc_id → doc_text`` representing the candidate pool.
        doc_tags:
            Optional mapping of ``doc_id → list[tag]``.

        Returns
        -------
        list[Recommendation]
            Up to :attr:`RecommendationConfig.top_k` recommendations,
            sorted by final score descending, with ranks starting at 1.
        """
        doc_tags = doc_tags or {}

        # Step 1: score all candidates
        scored: list[RecommendationScore] = self.scorer.score_all(
            profile, docs, doc_tags
        )

        # Step 2: exclude seen documents when configured
        if self.config.exclude_seen:
            seen = profile.seen_docs()
            scored = [s for s in scored if s.doc_id not in seen]

        # Step 3: diversity-aware selection
        selected: list[RecommendationScore] = []
        selected_tags: list[list[str]] = []

        for candidate in scored:
            if len(selected) >= self.config.top_k:
                break

            tags = doc_tags.get(candidate.doc_id, [])

            # Compute max tag-overlap with already-selected documents
            max_overlap = 0.0
            for sel_tags in selected_tags:
                overlap = _tag_overlap_ratio(tags, sel_tags)
                if overlap > max_overlap:
                    max_overlap = overlap

            # Apply penalty only when overlap exceeds 50 %
            adjusted_score = candidate.score
            if max_overlap > 0.5:
                adjusted_score -= max_overlap * self.config.diversity_factor

            selected.append(
                RecommendationScore(
                    doc_id=candidate.doc_id,
                    score=adjusted_score,
                    reasons=candidate.reasons,
                )
            )
            selected_tags.append(tags)

        # Step 4: sort by final score (diversity may have reordered)
        selected.sort(key=lambda s: s.score, reverse=True)

        return [
            Recommendation(
                doc_id=s.doc_id,
                score=s.score,
                rank=i + 1,
                reasons=s.reasons,
            )
            for i, s in enumerate(selected)
        ]
