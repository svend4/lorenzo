"""Relevance scoring for context compression — pure stdlib."""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field


def _tokenize(text: str) -> set[str]:
    """Return lowercase word token set from *text*."""
    return set(re.findall(r"[a-zA-Zа-яёА-ЯЁ0-9]+", text.lower()))


@dataclass
class RelevanceScore:
    """A passage paired with its relevance metrics."""

    passage_id: str
    text: str
    score: float
    query_coverage: float  # fraction of query tokens covered


class RelevanceScorer:
    """Score passages against a query using token-overlap heuristics."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def score(
        self,
        query: str,
        passage: str,
        passage_id: str = "",
    ) -> RelevanceScore:
        """Compute a :class:`RelevanceScore` for *passage* w.r.t. *query*.

        ``query_coverage``
            |query_tokens ∩ passage_tokens| / (|query_tokens| + 1)

        ``score``
            query_coverage × (1 + log(word_count + 1) / 10)
        """
        query_tokens = _tokenize(query)
        passage_tokens = _tokenize(passage)

        intersection = query_tokens & passage_tokens
        query_coverage = len(intersection) / (len(query_tokens) + 1)

        word_count = len(passage.split())
        score = query_coverage * (1 + math.log(word_count + 1) / 10)

        return RelevanceScore(
            passage_id=passage_id,
            text=passage,
            score=score,
            query_coverage=query_coverage,
        )

    def score_all(
        self,
        query: str,
        passages: list[str],
    ) -> list[RelevanceScore]:
        """Score all passages and return them sorted by score descending."""
        results = [
            self.score(query, p, passage_id=str(i))
            for i, p in enumerate(passages)
        ]
        results.sort(key=lambda rs: -rs.score)
        return results
