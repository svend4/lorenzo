"""ContentScorer — computes recommendation scores for documents."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from docstoolkit.recommender.profile import UserProfile


def _tokenize(text: str) -> set[str]:
    """Return a set of lowercase word tokens from *text*."""
    return set(re.findall(r"[a-zA-Zа-яёА-ЯЁ0-9]+", text.lower()))


def _jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard similarity between two token sets."""
    if not a and not b:
        return 0.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union if union else 0.0


@dataclass
class RecommendationScore:
    """Score details for a single document recommendation.

    Attributes:
        doc_id: Identifier of the scored document.
        score: Combined recommendation score (higher = more relevant).
        reasons: Human-readable strings explaining the score components.
    """

    doc_id: str
    score: float
    reasons: list[str] = field(default_factory=list)


class ContentScorer:
    """Scores documents against a :class:`UserProfile`.

    Scoring components
    ------------------
    * **tag_match** — fraction of the document's tags that align with the
      user's tag interests, weighted by interest scores.
    * **query_overlap** — average Jaccard similarity between the user's last
      3 queries and the document text tokens.
    * **dislike_penalty** — subtracts 0.5 when the document was disliked.
    """

    def score_for_profile(
        self,
        profile: UserProfile,
        doc_id: str,
        doc_text: str,
        doc_tags: list[str] | None = None,
    ) -> RecommendationScore:
        """Compute a recommendation score for a single document.

        Parameters
        ----------
        profile:
            The user profile to score against.
        doc_id:
            Identifier for the document being scored.
        doc_text:
            Full text content of the document (used for query overlap).
        doc_tags:
            Optional list of tags associated with the document.

        Returns
        -------
        RecommendationScore
            Score and human-readable reason strings.
        """
        doc_tags = doc_tags or []
        reasons: list[str] = []

        # ---- Tag match -------------------------------------------------------
        tag_sum = sum(profile.tags.get(tag, 0.0) for tag in doc_tags)
        tag_match = tag_sum / (len(doc_tags) + 1)
        if tag_match > 0:
            reasons.append(f"tag_match:{tag_match:.4g}")

        # ---- Query overlap ---------------------------------------------------
        recent_queries = profile.query_history[-3:]
        doc_tokens = _tokenize(doc_text)
        if recent_queries and doc_tokens:
            jaccard_scores = [
                _jaccard(_tokenize(q), doc_tokens) for q in recent_queries
            ]
            query_overlap = sum(jaccard_scores) / len(jaccard_scores)
        else:
            query_overlap = 0.0
        if query_overlap > 0:
            reasons.append(f"query_overlap:{query_overlap:.4g}")

        # ---- Combine ---------------------------------------------------------
        combined = tag_match + query_overlap

        # ---- Dislike penalty -------------------------------------------------
        if doc_id in profile.disliked_docs:
            combined -= 0.5
            reasons.append("dislike_penalty:-0.5")

        return RecommendationScore(doc_id=doc_id, score=combined, reasons=reasons)

    def score_all(
        self,
        profile: UserProfile,
        docs: dict[str, str],
        doc_tags: dict[str, list[str]] | None = None,
    ) -> list[RecommendationScore]:
        """Score every document in *docs* and return results sorted descending.

        Parameters
        ----------
        profile:
            The user profile to score against.
        docs:
            Mapping of ``doc_id → doc_text``.
        doc_tags:
            Optional mapping of ``doc_id → list[tag]``.

        Returns
        -------
        list[RecommendationScore]
            All scores, sorted by score descending.
        """
        doc_tags = doc_tags or {}
        scores = [
            self.score_for_profile(
                profile, doc_id, doc_text, doc_tags.get(doc_id, [])
            )
            for doc_id, doc_text in docs.items()
        ]
        scores.sort(key=lambda s: s.score, reverse=True)
        return scores
