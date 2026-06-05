"""Sliding context window — pure stdlib."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.context_compression.scorer import RelevanceScore


def _word_count(text: str) -> int:
    """Return the number of whitespace-separated tokens in *text*."""
    return len(text.split())


@dataclass
class ContextWindow:
    """A fixed-capacity window that accumulates :class:`~scorer.RelevanceScore` objects.

    Capacity is measured in **word count** (a proxy for tokens).
    """

    max_tokens: int
    passages: list[RelevanceScore] = field(default_factory=list)
    current_tokens: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def can_fit(self, text: str) -> bool:
        """Return *True* if *text* fits without exceeding the budget."""
        return self.current_tokens + _word_count(text) <= self.max_tokens

    def add(self, rs: RelevanceScore) -> bool:
        """Add *rs* to this window if it fits.

        Returns
        -------
        bool
            ``True`` when the passage was added, ``False`` otherwise.
        """
        if not self.can_fit(rs.text):
            return False
        self.passages.append(rs)
        self.current_tokens += _word_count(rs.text)
        return True

    def utilization(self) -> float:
        """Return the fraction of the token budget consumed.

        Always returns 0.0 when *max_tokens* is 0 to avoid division by zero.
        """
        if self.max_tokens == 0:
            return 0.0
        return self.current_tokens / self.max_tokens

    def clear(self) -> None:
        """Reset the window to its initial (empty) state."""
        self.passages.clear()
        self.current_tokens = 0


class SlidingContextWindow:
    """Pack a list of scored passages into as many windows as needed.

    Passages are inserted greedily in the order given; a new window is opened
    whenever the current one cannot accommodate the next passage.  Passages
    that are individually larger than *max_tokens* are placed in their own
    over-full window so that no passage is silently dropped.
    """

    def __init__(self, max_tokens: int = 500) -> None:
        self.max_tokens = max_tokens

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fill(self, passages: list[RelevanceScore]) -> list[ContextWindow]:
        """Pack *passages* into windows and return the list of windows.

        An empty input produces an empty list.
        """
        if not passages:
            return []

        windows: list[ContextWindow] = []
        current = ContextWindow(max_tokens=self.max_tokens)

        for rs in passages:
            if not current.add(rs):
                # Current window is full — start a new one.
                windows.append(current)
                current = ContextWindow(max_tokens=self.max_tokens)
                # Force-add even if single passage exceeds budget so it isn't lost.
                if _word_count(rs.text) > self.max_tokens:
                    current.passages.append(rs)
                    current.current_tokens += _word_count(rs.text)
                else:
                    current.add(rs)

        # Don't forget the last window (even if partially filled).
        if current.passages:
            windows.append(current)

        return windows
