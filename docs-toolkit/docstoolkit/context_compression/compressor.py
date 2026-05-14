"""Context compressor — greedy token-budget selection — pure stdlib."""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from docstoolkit.context_compression.scorer import RelevanceScore, RelevanceScorer


def _word_count(text: str) -> int:
    """Return the number of whitespace-separated tokens in *text*."""
    return len(text.split())


def _tokenize_set(text: str) -> set[str]:
    """Lowercase word tokens as a set."""
    return set(re.findall(r"[a-zA-Zа-яёА-ЯЁ0-9]+", text.lower()))


@dataclass
class CompressionConfig:
    """Tunable knobs for :class:`ContextCompressor`."""

    max_tokens: int = 500
    min_coverage: float = 0.3
    overlap_penalty: float = 0.1


@dataclass
class CompressedContext:
    """Result of a compression run."""

    query: str
    passages: list[RelevanceScore]
    total_tokens: int
    compression_ratio: float

    def texts(self) -> list[str]:
        """Return the plain text of every included passage."""
        return [rs.text for rs in self.passages]

    def coverage(self) -> float:
        """Average query_coverage of the included passages.

        Returns 0.0 when no passages were selected.
        """
        if not self.passages:
            return 0.0
        return sum(rs.query_coverage for rs in self.passages) / len(self.passages)


class ContextCompressor:
    """Greedily select passages that fit within a token budget.

    Algorithm
    ---------
    1. Score all passages with :class:`~scorer.RelevanceScorer`.
    2. Iterate from highest score to lowest:
       a. Skip if ``query_coverage < min_coverage``.
       b. Apply ``overlap_penalty`` to the *current* effective score if the
          passage has >50 % token overlap with any already-selected passage.
       c. Add if there is still token budget left.
    """

    def __init__(self, config: CompressionConfig | None = None) -> None:
        self._config = config or CompressionConfig()
        self._scorer = RelevanceScorer()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def compress(
        self,
        query: str,
        passages: list[str],
    ) -> CompressedContext:
        """Compress *passages* to fit within ``config.max_tokens``."""
        cfg = self._config
        scored = self._scorer.score_all(query, passages)

        total_input_tokens = sum(_word_count(p) for p in passages)

        selected: list[RelevanceScore] = []
        selected_token_sets: list[set[str]] = []
        used_tokens = 0

        for rs in scored:
            # --- coverage gate -------------------------------------------
            if rs.query_coverage < cfg.min_coverage:
                continue

            # --- overlap penalty -----------------------------------------
            effective_score = rs.score
            passage_tokens = _tokenize_set(rs.text)
            for sel_tokens in selected_token_sets:
                if not passage_tokens:
                    break
                overlap = len(passage_tokens & sel_tokens) / len(passage_tokens)
                if overlap > 0.5:
                    effective_score -= cfg.overlap_penalty
                    break  # apply penalty at most once

            if effective_score <= 0:
                continue

            # --- token budget gate ---------------------------------------
            wc = _word_count(rs.text)
            if used_tokens + wc > cfg.max_tokens:
                continue

            selected.append(rs)
            selected_token_sets.append(passage_tokens)
            used_tokens += wc

        compression_ratio = (
            used_tokens / total_input_tokens if total_input_tokens else 0.0
        )

        return CompressedContext(
            query=query,
            passages=selected,
            total_tokens=used_tokens,
            compression_ratio=compression_ratio,
        )
