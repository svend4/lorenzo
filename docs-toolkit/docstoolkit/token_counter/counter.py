"""Lightweight token counting utilities with multiple tokenization strategies.

All implementations use the Python standard library only — no tiktoken,
no transformers, no external dependencies.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import List


class TokenStrategy(str, Enum):
    """Supported tokenization strategies."""

    WORD = "word"
    CHAR = "char"
    WHITESPACE = "whitespace"
    SENTENCE = "sentence"
    SUBWORD = "subword"


@dataclass
class TokenCount:
    """Result of a single tokenization operation."""

    text: str
    strategy: TokenStrategy
    count: int
    tokens: List[str]

    def __repr__(self) -> str:  # pragma: no cover
        preview = self.tokens[:5]
        return (
            f"TokenCount(strategy={self.strategy!r}, count={self.count}, "
            f"tokens={preview!r}{'...' if len(self.tokens) > 5 else ''})"
        )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_SENTENCE_PATTERN = re.compile(r"[.!?\n]+")


def _tokenize(text: str, strategy: TokenStrategy) -> List[str]:
    """Return the token list for *text* using *strategy*."""
    if strategy is TokenStrategy.WORD:
        return re.findall(r"\b\w+\b", text)

    if strategy is TokenStrategy.CHAR:
        return [ch for ch in text if not ch.isspace()]

    if strategy is TokenStrategy.WHITESPACE:
        return text.split()

    if strategy is TokenStrategy.SENTENCE:
        parts = _SENTENCE_PATTERN.split(text)
        return [p.strip() for p in parts if p.strip()]

    if strategy is TokenStrategy.SUBWORD:
        words = re.findall(r"\b\w+\b", text)
        chunks: List[str] = []
        for word in words:
            for i in range(0, len(word), 4):
                chunks.append(word[i : i + 4])
        return chunks

    raise ValueError(f"Unknown strategy: {strategy!r}")  # pragma: no cover


# ---------------------------------------------------------------------------
# TokenCounter
# ---------------------------------------------------------------------------


class TokenCounter:
    """Count, estimate and truncate tokens using configurable strategies."""

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def count(
        self,
        text: str,
        strategy: TokenStrategy = TokenStrategy.WORD,
    ) -> TokenCount:
        """Tokenise *text* with *strategy* and return a :class:`TokenCount`."""
        tokens = _tokenize(text, strategy)
        return TokenCount(
            text=text,
            strategy=strategy,
            count=len(tokens),
            tokens=tokens,
        )

    def count_batch(
        self,
        texts: List[str],
        strategy: TokenStrategy = TokenStrategy.WORD,
    ) -> List[TokenCount]:
        """Tokenise every string in *texts* and return a list of results."""
        return [self.count(t, strategy) for t in texts]

    # ------------------------------------------------------------------
    # Cost estimation
    # ------------------------------------------------------------------

    def estimate_cost(
        self,
        text: str,
        rate_per_1k: float = 0.002,
    ) -> float:
        """Estimate the cost of *text* at *rate_per_1k* dollars per 1 000 tokens.

        Token count is computed with the WORD strategy.
        """
        n = self.count(text, TokenStrategy.WORD).count
        return (n / 1000.0) * rate_per_1k

    # ------------------------------------------------------------------
    # Truncation helpers
    # ------------------------------------------------------------------

    def truncate(
        self,
        text: str,
        max_tokens: int,
        strategy: TokenStrategy = TokenStrategy.WORD,
    ) -> str:
        """Return a version of *text* containing at most *max_tokens* tokens.

        The returned string is reassembled by joining the first *max_tokens*
        tokens with a single space, so it may differ from the original
        whitespace layout.  For the CHAR strategy the characters are
        concatenated without a separator.
        """
        if max_tokens <= 0:
            return ""
        tokens = _tokenize(text, strategy)
        selected = tokens[:max_tokens]
        if strategy is TokenStrategy.CHAR:
            return "".join(selected)
        return " ".join(selected)

    def fits_in(
        self,
        text: str,
        max_tokens: int,
        strategy: TokenStrategy = TokenStrategy.WORD,
    ) -> bool:
        """Return ``True`` when *text* has at most *max_tokens* tokens."""
        return self.count(text, strategy).count <= max_tokens


# ---------------------------------------------------------------------------
# TokenBudget
# ---------------------------------------------------------------------------


@dataclass
class TokenBudget:
    """Track cumulative token usage against a hard limit.

    Parameters
    ----------
    limit:
        Maximum total tokens allowed.
    strategy:
        Tokenisation strategy used for counting each added text.
    """

    limit: int
    strategy: TokenStrategy = TokenStrategy.WORD

    _used: int = field(default=0, init=False, repr=False)
    _counter: TokenCounter = field(
        default_factory=TokenCounter, init=False, repr=False
    )

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add(self, text: str) -> bool:
        """Attempt to add *text* to the budget.

        Returns
        -------
        bool
            ``True`` when the text fits within the remaining budget and has
            been counted; ``False`` when it would exceed the limit (the
            budget is **not** modified in that case).
        """
        n = self._counter.count(text, self.strategy).count
        if self._used + n > self.limit:
            return False
        self._used += n
        return True

    def reset(self) -> None:
        """Reset the used-token counter to zero."""
        self._used = 0

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def used(self) -> int:
        """Tokens consumed so far."""
        return self._used

    @property
    def remaining(self) -> int:
        """Tokens still available (never negative)."""
        return max(0, self.limit - self._used)

    @property
    def is_exhausted(self) -> bool:
        """``True`` when no more tokens can be added."""
        return self._used >= self.limit
