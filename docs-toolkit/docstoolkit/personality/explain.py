"""Personalization explanation: what changed and why."""
from dataclasses import dataclass, field
from docstoolkit.personality.profile import CognitiveProfile


@dataclass
class PersonalizationExplanation:
    dominant_style: str
    applied_boosts: list   # e.g. ["skepticism +0.14", "verification +0.12"]
    default_ranking: list  # doc_ids in default order
    personal_ranking: list # doc_ids after personalization
    rank_changes: dict     # {doc_id: +/-N positions changed}


def explain_personalization(
    profile: CognitiveProfile,
    default_passages: list,
    personal_passages: list,
) -> PersonalizationExplanation:
    """Explain what the personalization changed.

    1. dominant_style = profile.dominant_style()
    2. applied_boosts: for each dim > 0.6, add "{dim} +{value:.2f}"
    3. default_ranking = [p.doc_id for p in default_passages]
    4. personal_ranking = [p.doc_id for p in personal_passages]
    5. rank_changes: for each doc_id, compute new_rank - old_rank
       (negative = moved up, positive = moved down)
    """
    dominant_style = profile.dominant_style()

    # Collect applied boosts for dims exceeding threshold
    _DIM_NAMES = ["skepticism", "synthesis", "exploration", "verification", "pragmatism"]
    applied_boosts = []
    for dim in _DIM_NAMES:
        value = getattr(profile, dim)
        if value > 0.6:
            applied_boosts.append(f"{dim} +{value:.2f}")

    default_ranking = [p.doc_id for p in default_passages]
    personal_ranking = [p.doc_id for p in personal_passages]

    # Build rank-change map: new_rank - old_rank (negative = moved up)
    old_rank = {doc_id: i for i, doc_id in enumerate(default_ranking)}
    new_rank = {doc_id: i for i, doc_id in enumerate(personal_ranking)}

    all_ids = set(default_ranking) | set(personal_ranking)
    rank_changes: dict = {}
    for doc_id in all_ids:
        if doc_id in old_rank and doc_id in new_rank:
            rank_changes[doc_id] = new_rank[doc_id] - old_rank[doc_id]

    return PersonalizationExplanation(
        dominant_style=dominant_style,
        applied_boosts=applied_boosts,
        default_ranking=default_ranking,
        personal_ranking=personal_ranking,
        rank_changes=rank_changes,
    )
