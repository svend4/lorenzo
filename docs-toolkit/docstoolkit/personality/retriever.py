"""Personality-aware retrieval: re-ranking passages by cognitive style."""
import re
from dataclasses import dataclass
from docstoolkit.personality.profile import CognitiveProfile

# Style-to-passage markers
_SKEPTIC_MARKERS = [
    "however", "but", "contradicts", "challenges", "disputes",
    "however,", "on the other hand", "critics", "против", "однако",
]
_SYNTHESIS_MARKERS = [
    "overview", "in general", "broadly", "pattern", "trend",
    "across", "в целом", "обзор", "закономерность",
]
_VERIFICATION_MARKERS = [
    "[", "source", "cite", "citation", "reference", "study",
    "research", "evidence", "proof", "источник", "ссылка",
]
_PRAGMATISM_MARKERS = [
    "how to", "step", "install", "run", "example", "usage",
    "implement", "configure", "как ", "шаг", "установить",
]


def _contains_any(text: str, markers: list) -> bool:
    """Return True if text (lowercased) contains any of the given markers."""
    tl = text.lower()
    return any(m in tl for m in markers)


@dataclass
class StyleModifier:
    """Score modifiers applied per style dimension."""
    skepticism_boost: float = 0.2
    synthesis_boost: float = 0.2
    exploration_penalty: float = 0.05  # small penalty for already-seen topics
    verification_boost: float = 0.15
    pragmatism_boost: float = 0.2


class PersonalRetriever:
    """Re-ranks passages based on CognitiveProfile."""

    def __init__(
        self,
        profile: CognitiveProfile,
        modifier: StyleModifier | None = None,
    ):
        self._profile = profile
        self._mod = modifier or StyleModifier()

    def rerank(
        self,
        passages: list,
        query: str = "",
        *,
        seen_doc_ids: set | None = None,
    ) -> list:
        """Re-score passages by adding style bonuses/penalties.

        For each passage:
        1. base_score = passage.score (or 0.5 if no score attr)
        2. If profile.skepticism > 0.6 and passage contains _SKEPTIC_MARKERS:
           score += modifier.skepticism_boost * profile.skepticism
        3. If profile.synthesis > 0.6 and passage contains _SYNTHESIS_MARKERS:
           score += modifier.synthesis_boost * profile.synthesis
        4. If profile.verification > 0.6 and passage contains _VERIFICATION_MARKERS:
           score += modifier.verification_boost * profile.verification
        5. If profile.pragmatism > 0.6 and passage contains _PRAGMATISM_MARKERS:
           score += modifier.pragmatism_boost * profile.pragmatism
        6. If profile.exploration > 0.7 and passage.doc_id in seen_doc_ids:
           score -= modifier.exploration_penalty  (diversity penalty)

        Sort by final score descending.
        Return list of passages with updated scores (create new objects or update in-place).
        """
        if not passages:
            return []

        if seen_doc_ids is None:
            seen_doc_ids = set()

        profile = self._profile
        mod = self._mod

        scored = []
        for passage in passages:
            base_score = getattr(passage, "score", 0.5)
            score = base_score

            if profile.skepticism > 0.6 and _contains_any(passage.text, _SKEPTIC_MARKERS):
                score += mod.skepticism_boost * profile.skepticism

            if profile.synthesis > 0.6 and _contains_any(passage.text, _SYNTHESIS_MARKERS):
                score += mod.synthesis_boost * profile.synthesis

            if profile.verification > 0.6 and _contains_any(passage.text, _VERIFICATION_MARKERS):
                score += mod.verification_boost * profile.verification

            if profile.pragmatism > 0.6 and _contains_any(passage.text, _PRAGMATISM_MARKERS):
                score += mod.pragmatism_boost * profile.pragmatism

            if profile.exploration > 0.7 and getattr(passage, "doc_id", None) in seen_doc_ids:
                score -= mod.exploration_penalty

            scored.append((score, passage))

        scored.sort(key=lambda x: -x[0])

        result = []
        for new_score, passage in scored:
            try:
                from dataclasses import replace
                p = replace(passage, score=new_score)
            except TypeError:
                # Fallback for non-dataclass passage-like objects
                from docstoolkit.rag.types import Passage as _Passage
                p = _Passage(
                    text=passage.text,
                    doc_id=passage.doc_id,
                    title=getattr(passage, "title", ""),
                    score=new_score,
                )
            result.append(p)

        return result

    def top_style(self) -> str:
        return self._profile.dominant_style()
