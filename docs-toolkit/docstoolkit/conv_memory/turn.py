"""ConversationTurn — a single message in a conversation."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum

# Question words (English + Russian)
_EN_QUESTION_WORDS = {"what", "who", "where", "when", "why", "how"}
_RU_QUESTION_WORDS = {"что", "кто", "где", "когда", "почему", "как"}
_ALL_QUESTION_WORDS = _EN_QUESTION_WORDS | _RU_QUESTION_WORDS


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


def _auto_turn_id() -> str:
    return uuid.uuid4().hex[:8]


def _auto_ts() -> float:
    return time.time()


@dataclass
class ConversationTurn:
    role: Role
    content: str
    turn_id: str = field(default_factory=_auto_turn_id)
    ts: float = field(default_factory=_auto_ts)
    metadata: dict = field(default_factory=dict)

    def word_count(self) -> int:
        """Return the number of whitespace-separated words in content."""
        return len(self.content.split())

    def is_question(self) -> bool:
        """Return True if the turn looks like a question.

        A turn is a question if:
        - its content ends with "?", OR
        - any word (lowercased) in the content matches a known question word.
        """
        text = self.content.strip()
        if text.endswith("?"):
            return True
        words = {w.strip(".,;:!\"'()[]{}").lower() for w in text.split()}
        return bool(words & _ALL_QUESTION_WORDS)
