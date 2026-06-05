"""Decision tokens for Self-RAG reflection."""
from enum import Enum


class DecisionToken(Enum):
    NEED_RETRIEVAL = "NEED_RETRIEVAL"
    NO_RETRIEVAL = "NO_RETRIEVAL"
    REFLECT = "REFLECT"
    ANSWER_OK = "ANSWER_OK"
    ANSWER_INSUFFICIENT = "ANSWER_INSUFFICIENT"


# Convenience aliases
NEED_RETRIEVAL = DecisionToken.NEED_RETRIEVAL
NO_RETRIEVAL = DecisionToken.NO_RETRIEVAL
REFLECT = DecisionToken.REFLECT
ANSWER_OK = DecisionToken.ANSWER_OK
ANSWER_INSUFFICIENT = DecisionToken.ANSWER_INSUFFICIENT


def parse_decision(text: str) -> DecisionToken:
    """Parse decision token from text.

    Looks for [NEED_RETRIEVAL], [NO_RETRIEVAL], [REFLECT], [ANSWER_OK],
    [ANSWER_INSUFFICIENT] in text (case-insensitive, brackets optional).

    Fallback rules if no token found:
    - If text is short (<20 chars): NEED_RETRIEVAL (needs more info)
    - Otherwise: REFLECT (has answer, needs checking)
    """
    normalized = text.upper()

    # Try bracket-wrapped tokens first (longest match wins for ambiguity)
    _ORDER = [
        "ANSWER_INSUFFICIENT",
        "ANSWER_OK",
        "NEED_RETRIEVAL",
        "NO_RETRIEVAL",
        "REFLECT",
    ]

    for token_name in _ORDER:
        # Accept both [TOKEN] and bare TOKEN
        if f"[{token_name}]" in normalized or token_name in normalized:
            return DecisionToken[token_name]

    # Fallback
    if len(text) < 20:
        return DecisionToken.NEED_RETRIEVAL
    return DecisionToken.REFLECT
