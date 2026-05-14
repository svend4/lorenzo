"""Token-level and passage-level attribution for explainability."""
import re
from dataclasses import dataclass, field
from enum import Enum


class AttributionMethod(Enum):
    TOKEN_OVERLAP = "token_overlap"
    PASSAGE_SCORE = "passage_score"
    KEYWORD_FREQUENCY = "keyword_frequency"
    POSITION = "position"


@dataclass
class TokenAttribution:
    token: str
    score: float
    method: AttributionMethod


@dataclass
class PassageAttribution:
    passage_id: str
    passage_text: str
    attribution_score: float
    token_attributions: list[TokenAttribution]
    rank: int

    def top_tokens(self, n: int = 5) -> list[TokenAttribution]:
        """Return top-n token attributions sorted by score descending."""
        return sorted(self.token_attributions, key=lambda t: t.score, reverse=True)[:n]


def _tokenize(text: str) -> list[str]:
    """Lowercase words, strip punctuation, return list (preserving duplicates)."""
    return re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", text.lower())


def _token_frequency(tokens: list[str]) -> dict[str, int]:
    freq: dict[str, int] = {}
    for t in tokens:
        freq[t] = freq.get(t, 0) + 1
    return freq


class AttributionExplainer:
    """Explains passage relevance to a query using token-level attribution."""

    def explain_passage(
        self,
        query: str,
        passage: str,
        passage_id: str = "",
        rank: int = 1,
    ) -> PassageAttribution:
        """Compute token attributions for a single passage against the query.

        Token overlap: score each query token by frequency in passage, normalize.
        Passage attribution_score = overlap count / max(passage length, 1).
        """
        query_tokens = _tokenize(query)
        passage_tokens = _tokenize(passage)

        passage_freq = _token_frequency(passage_tokens)
        passage_len = len(passage_tokens)

        # Score each query token by its frequency in passage
        raw_scores: dict[str, float] = {}
        for token in query_tokens:
            raw_scores[token] = float(passage_freq.get(token, 0))

        # Normalize token scores so they sum to 1.0 (if any > 0)
        total = sum(raw_scores.values())
        normalized: dict[str, float] = {}
        for token, score in raw_scores.items():
            normalized[token] = score / total if total > 0 else 0.0

        # Build token attributions for unique query tokens (best score per token)
        seen: dict[str, float] = {}
        for token in query_tokens:
            if token not in seen or normalized[token] > seen[token]:
                seen[token] = normalized[token]

        token_attributions = [
            TokenAttribution(token=tok, score=sc, method=AttributionMethod.TOKEN_OVERLAP)
            for tok, sc in seen.items()
        ]

        # Passage-level score: number of query tokens found / passage length
        overlap_count = sum(1 for t in query_tokens if passage_freq.get(t, 0) > 0)
        attribution_score = overlap_count / max(passage_len, 1)

        return PassageAttribution(
            passage_id=passage_id,
            passage_text=passage,
            attribution_score=attribution_score,
            token_attributions=token_attributions,
            rank=rank,
        )

    def explain_all(
        self,
        query: str,
        passages: list[str],
    ) -> list[PassageAttribution]:
        """Explain all passages and return sorted by attribution_score descending."""
        attributions = [
            self.explain_passage(query, passage, passage_id=str(i), rank=i + 1)
            for i, passage in enumerate(passages)
        ]
        attributions.sort(key=lambda a: a.attribution_score, reverse=True)
        # Re-assign ranks after sorting
        for i, a in enumerate(attributions):
            a.rank = i + 1
        return attributions
