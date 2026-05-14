"""FeedbackSignal — typed signal for the E19 feedback loop."""
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum


class FeedbackType(Enum):
    THUMBS_UP = "thumbs_up"
    THUMBS_DOWN = "thumbs_down"
    RATING = "rating"
    CORRECTION = "correction"
    SKIP = "skip"


def _normalize_value(feedback_type: FeedbackType, raw_value: float) -> float:
    """Return a normalised scalar value for a feedback signal.

    Rules:
      THUMBS_UP   → 1.0
      THUMBS_DOWN → -1.0
      SKIP        → 0.0
      RATING      → (raw_value - 1) / 4  clamped to [0.0, 1.0]
                    (maps 1→0.0, 3→0.5, 5→1.0)
      CORRECTION  → raw_value if already provided, else 0.0
    """
    if feedback_type == FeedbackType.THUMBS_UP:
        return 1.0
    if feedback_type == FeedbackType.THUMBS_DOWN:
        return -1.0
    if feedback_type == FeedbackType.SKIP:
        return 0.0
    if feedback_type == FeedbackType.RATING:
        # Normalise 1-5 scale to 0-1
        return max(0.0, min(1.0, (raw_value - 1.0) / 4.0))
    # CORRECTION — keep whatever the caller supplied, default 0.0
    return raw_value


@dataclass
class FeedbackSignal:
    """A single structured feedback event.

    Parameters
    ----------
    query:
        The user query or prompt that triggered this feedback.
    feedback_type:
        Type of feedback (from :class:`FeedbackType`).
    doc_id:
        Optional document/result identifier the feedback relates to.
    value:
        Raw input value; normalised automatically by ``__post_init__``.
        For THUMBS_UP/DOWN/SKIP the caller may pass anything — the final
        stored value is always fixed.  For RATING, pass 1–5.
        For CORRECTION, pass an explicit scalar (e.g. -1.0 … 1.0) or leave
        0.0 for neutral.
    note:
        Free-text annotation.
    signal_id:
        Auto-generated UUID4 hex string; override only for testing.
    ts:
        Unix timestamp (float seconds); auto-set to ``time.time()`` if 0.
    """

    query: str
    feedback_type: FeedbackType
    doc_id: str | None = None
    value: float = 0.0
    note: str = ""
    signal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ts: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        # Normalise value according to the feedback type
        self.value = _normalize_value(self.feedback_type, self.value)

    # ------------------------------------------------------------------
    # Convenience predicates
    # ------------------------------------------------------------------

    def is_positive(self) -> bool:
        """Return True when the signal carries a positive value (> 0)."""
        return self.value > 0.0

    def is_negative(self) -> bool:
        """Return True when the signal carries a negative value (< 0)."""
        return self.value < 0.0
