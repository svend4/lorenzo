"""Feature extraction for passage re-ranking.

Pure stdlib — no sklearn, numpy, or ML libraries required.
"""
import hashlib
import math
import re
from dataclasses import dataclass


def _tokenize(text: str) -> list[str]:
    """Tokenize text into lowercase word tokens (latin + cyrillic, len >= 2)."""
    return re.findall(r'[а-яёa-z]{2,}', text.lower())


def _token_set(text: str) -> set[str]:
    """Return a set of lowercase tokens from text."""
    return set(_tokenize(text))


@dataclass
class PassageFeatures:
    """Feature vector for a single (query, passage) pair."""

    passage_id: str
    query_term_overlap: float
    bm25_score: float
    passage_length: int           # word count
    position_score: float         # 1.0 / rank
    title_match: bool
    exact_phrase_match: bool


class FeatureExtractor:
    """Extracts PassageFeatures for (query, passage, rank) triples.

    All computations are pure stdlib — no external dependencies.
    """

    # BM25 constants
    _K1: float = 1.5
    _B: float = 0.75
    _AVG_DL: int = 100  # assumed average document length in words

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(
        self,
        query: str,
        passage: str,
        rank: int,
        title: str = "",
    ) -> PassageFeatures:
        """Extract all features for a single (query, passage) pair.

        Parameters
        ----------
        query:
            The search query string.
        passage:
            The passage text to score.
        rank:
            1-based position of this passage in the original result list.
        title:
            Optional document title — used for title_match feature.

        Returns
        -------
        PassageFeatures
            Fully populated feature dataclass.
        """
        query_tokens = _token_set(query)
        passage_tokens = _tokenize(passage)
        passage_token_set = set(passage_tokens)

        pid = self.passage_id(passage, rank)
        overlap = self._query_term_overlap(query_tokens, passage_token_set)
        bm25 = self._bm25_score(query_tokens, passage_tokens)
        length = len(passage_tokens)
        pos_score = 1.0 / rank if rank > 0 else 0.0
        t_match = self._title_match(query_tokens, title)
        phrase_match = query.lower() in passage.lower() if query else False

        return PassageFeatures(
            passage_id=pid,
            query_term_overlap=overlap,
            bm25_score=bm25,
            passage_length=length,
            position_score=pos_score,
            title_match=t_match,
            exact_phrase_match=phrase_match,
        )

    # ------------------------------------------------------------------
    # Helper: passage_id
    # ------------------------------------------------------------------

    @staticmethod
    def passage_id(passage: str, rank: int) -> str:
        """Compute a short deterministic ID for a (rank, passage) pair.

        Uses SHA-256 of ``"{rank}:{passage[:50]}"`` truncated to 8 hex chars.
        """
        raw = f"{rank}:{passage[:50]}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8]

    # ------------------------------------------------------------------
    # Private feature computations
    # ------------------------------------------------------------------

    @staticmethod
    def _query_term_overlap(
        query_tokens: set[str],
        passage_token_set: set[str],
    ) -> float:
        """Fraction of query terms found in the passage.

        Formula: |query_tokens ∩ passage_tokens| / (|query_tokens| + 1)
        The +1 in the denominator avoids division-by-zero for empty queries.
        """
        if not query_tokens:
            return 0.0
        intersection = query_tokens & passage_token_set
        return len(intersection) / (len(query_tokens) + 1)

    @classmethod
    def _bm25_score(
        cls,
        query_tokens: set[str],
        passage_tokens: list[str],
    ) -> float:
        """Simplified BM25 score.

        For each query term t:
            tf = count of t in passage
            bm25_term = tf / (tf + K1) * log(1 + 1/df)

        where df = 1 for unknown terms (no corpus IDF available).
        The final score is the sum over all query terms.
        """
        if not query_tokens or not passage_tokens:
            return 0.0

        # Build term-frequency map for the passage
        tf_map: dict[str, int] = {}
        for token in passage_tokens:
            tf_map[token] = tf_map.get(token, 0) + 1

        score = 0.0
        for term in query_tokens:
            tf = tf_map.get(term, 0)
            if tf == 0:
                continue
            # Simplified BM25: no length normalisation component needed per spec
            bm25_term = (tf / (tf + cls._K1)) * math.log(1 + 1.0 / 1)
            score += bm25_term

        return score

    @staticmethod
    def _title_match(query_tokens: set[str], title: str) -> bool:
        """Return True if any query token appears in the title tokens."""
        if not title or not query_tokens:
            return False
        title_tokens = _token_set(title)
        return bool(query_tokens & title_tokens)
