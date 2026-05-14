"""Cognitive profile: dimensions, survey, and heuristic inference."""
import re
from dataclasses import dataclass


@dataclass
class CognitiveProfile:
    """5-dimensional cognitive style (all floats in [0, 1])."""
    skepticism: float = 0.5     # prefers counterarguments / contradictions
    synthesis: float = 0.5      # prefers high-level patterns / connections
    exploration: float = 0.5    # prefers diverse results over focused
    verification: float = 0.5   # prefers cited / authoritative sources
    pragmatism: float = 0.5     # prefers action-oriented / how-to passages
    confidence: float = 0.5     # how calibrated this profile is (0=guess, 1=certain)

    def dominant_style(self) -> str:
        """Return name of highest-scoring dimension."""
        dims = {
            "skepticism": self.skepticism,
            "synthesis": self.synthesis,
            "exploration": self.exploration,
            "verification": self.verification,
            "pragmatism": self.pragmatism,
        }
        return max(dims, key=lambda k: dims[k])

    def to_dict(self) -> dict:
        return {
            "skepticism": self.skepticism,
            "synthesis": self.synthesis,
            "exploration": self.exploration,
            "verification": self.verification,
            "pragmatism": self.pragmatism,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CognitiveProfile":
        return cls(
            skepticism=float(d.get("skepticism", 0.5)),
            synthesis=float(d.get("synthesis", 0.5)),
            exploration=float(d.get("exploration", 0.5)),
            verification=float(d.get("verification", 0.5)),
            pragmatism=float(d.get("pragmatism", 0.5)),
            confidence=float(d.get("confidence", 0.5)),
        )

    def blend(self, other: "CognitiveProfile", weight: float = 0.5) -> "CognitiveProfile":
        """Weighted blend: self * (1-weight) + other * weight."""
        w = weight
        v = 1.0 - weight
        return CognitiveProfile(
            skepticism=self.skepticism * v + other.skepticism * w,
            synthesis=self.synthesis * v + other.synthesis * w,
            exploration=self.exploration * v + other.exploration * w,
            verification=self.verification * v + other.verification * w,
            pragmatism=self.pragmatism * v + other.pragmatism * w,
            confidence=self.confidence * v + other.confidence * w,
        )


@dataclass
class ProfileSurvey:
    """Forced-choice survey for cold-start profiling."""

    QUESTIONS: list = None  # list[tuple[str, str, str]]

    def __post_init__(self):
        self.QUESTIONS = [
            (
                "When reading a claim, you prefer to:",
                "Find supporting evidence",
                "Find counterarguments",
            ),
            (
                "You prefer answers that are:",
                "Broad overview",
                "Deep detail on one aspect",
            ),
            (
                "When searching, you value:",
                "Finding the most relevant result",
                "Discovering unexpected results",
            ),
            (
                "You trust sources that have:",
                "Many citations",
                "Clear practical examples",
            ),
            (
                "Your goal is usually:",
                "Understand the concept",
                "Know what to do next",
            ),
        ]

    def score_answer(self, question_idx: int, chose_b: bool) -> dict:
        """Map answer to profile dimension delta.

        Q0: chose_b → skepticism += 0.2
        Q1: chose_a → synthesis += 0.2 (broad)
        Q2: chose_b → exploration += 0.2 (unexpected)
        Q3: chose_a → verification += 0.2 (citations)
        Q4: chose_b → pragmatism += 0.2 (what to do)
        Returns {dim: delta}
        """
        mapping = {
            0: ("skepticism", True),    # chose_b triggers
            1: ("synthesis", False),    # chose_a triggers
            2: ("exploration", True),   # chose_b triggers
            3: ("verification", False), # chose_a triggers
            4: ("pragmatism", True),    # chose_b triggers
        }
        if question_idx not in mapping:
            return {}
        dim, trigger_b = mapping[question_idx]
        if chose_b == trigger_b:
            return {dim: 0.2}
        return {}

    def build_profile(self, answers: list) -> CognitiveProfile:
        """answers[i] = True if chose option_b for question i.
        Start with all 0.3 (below neutral), add deltas.
        confidence = len(answers) / len(QUESTIONS)
        """
        dims = {
            "skepticism": 0.3,
            "synthesis": 0.3,
            "exploration": 0.3,
            "verification": 0.3,
            "pragmatism": 0.3,
        }
        for i, chose_b in enumerate(answers):
            delta = self.score_answer(i, chose_b)
            for dim, val in delta.items():
                dims[dim] = min(1.0, dims[dim] + val)

        confidence = len(answers) / len(self.QUESTIONS)
        return CognitiveProfile(
            skepticism=dims["skepticism"],
            synthesis=dims["synthesis"],
            exploration=dims["exploration"],
            verification=dims["verification"],
            pragmatism=dims["pragmatism"],
            confidence=confidence,
        )


def infer_profile(queries: list) -> CognitiveProfile:
    """Heuristic profile inference from query history.

    skepticism: fraction of queries containing ("but", "however", "contra", "against", "wrong")
    synthesis: fraction containing ("overview", "compare", "vs", "difference", "relation")
    exploration: fraction that are short (<4 words) — explorers browse
    verification: fraction containing ("source", "cite", "evidence", "proof", "reference")
    pragmatism: fraction containing ("how to", "how do", "implement", "use", "example")
    confidence = min(len(queries) / 20, 1.0)

    All values clipped to [0, 1].
    """
    if not queries:
        return CognitiveProfile(
            skepticism=0.5,
            synthesis=0.5,
            exploration=0.5,
            verification=0.5,
            pragmatism=0.5,
            confidence=0.0,
        )

    n = len(queries)

    _SKEPTIC_WORDS = {"but", "however", "contra", "against", "wrong"}
    _SYNTHESIS_WORDS = {"overview", "compare", "vs", "difference", "relation"}
    _VERIFICATION_WORDS = {"source", "cite", "evidence", "proof", "reference"}
    _PRAGMATISM_PHRASES = {"how to", "how do", "implement", "use", "example"}

    skepticism_count = 0
    synthesis_count = 0
    exploration_count = 0
    verification_count = 0
    pragmatism_count = 0

    for q in queries:
        ql = q.lower()
        words = set(re.findall(r'\b\w+\b', ql))

        if words & _SKEPTIC_WORDS:
            skepticism_count += 1

        if words & _SYNTHESIS_WORDS:
            synthesis_count += 1

        if len(q.split()) < 4:
            exploration_count += 1

        if words & _VERIFICATION_WORDS:
            verification_count += 1

        if any(phrase in ql for phrase in _PRAGMATISM_PHRASES):
            pragmatism_count += 1

    def _clip(v: float) -> float:
        return max(0.0, min(1.0, v))

    return CognitiveProfile(
        skepticism=_clip(skepticism_count / n),
        synthesis=_clip(synthesis_count / n),
        exploration=_clip(exploration_count / n),
        verification=_clip(verification_count / n),
        pragmatism=_clip(pragmatism_count / n),
        confidence=min(n / 20, 1.0),
    )
