"""MemoryWindow — windowing strategies for conversation context."""
from __future__ import annotations

from enum import Enum

from docstoolkit.conv_memory.turn import ConversationTurn

_TOKENS_PER_WORD = 1.3


class WindowStrategy(str, Enum):
    LAST_N = "last_n"
    TOKEN_LIMIT = "token_limit"
    SLIDING = "sliding"
    SUMMARY = "summary"


class MemoryWindow:
    """Apply a windowing strategy to a list of ConversationTurns."""

    def __init__(
        self,
        strategy: WindowStrategy = WindowStrategy.LAST_N,
        size: int = 10,
        token_limit: int = 2000,
    ) -> None:
        self.strategy = strategy
        self.size = size
        self.token_limit = token_limit

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def apply(self, turns: list[ConversationTurn]) -> list[ConversationTurn]:
        """Return the subset of *turns* selected by the current strategy."""
        if not turns:
            return []

        if self.strategy == WindowStrategy.LAST_N:
            return self._last_n(turns)
        if self.strategy == WindowStrategy.TOKEN_LIMIT:
            return self._token_limit(turns)
        if self.strategy == WindowStrategy.SLIDING:
            return self._sliding(turns)
        # SUMMARY — summarisation happens at store level; return all
        return list(turns)

    def estimated_tokens(self, turns: list[ConversationTurn]) -> int:
        """Estimate token count as sum(word_count) * 1.3, rounded to int."""
        total_words = sum(t.word_count() for t in turns)
        return int(total_words * _TOKENS_PER_WORD)

    # ------------------------------------------------------------------
    # Strategy implementations
    # ------------------------------------------------------------------

    def _last_n(self, turns: list[ConversationTurn]) -> list[ConversationTurn]:
        return turns[-self.size :]

    def _token_limit(self, turns: list[ConversationTurn]) -> list[ConversationTurn]:
        """Walk backwards accumulating word counts; stop before exceeding token_limit."""
        selected: list[ConversationTurn] = []
        cumulative = 0
        for turn in reversed(turns):
            wc = turn.word_count()
            if cumulative + int(wc * _TOKENS_PER_WORD) > self.token_limit:
                break
            selected.append(turn)
            cumulative += int(wc * _TOKENS_PER_WORD)
        selected.reverse()
        return selected

    def _sliding(self, turns: list[ConversationTurn]) -> list[ConversationTurn]:
        """Return the last complete window of *size* turns."""
        if len(turns) <= self.size:
            return list(turns)
        # Number of complete windows
        start = len(turns) - self.size
        return turns[start : start + self.size]
