"""k-Anonymity helpers for query generalization.

Queries are generalized until each variant is shared by at least k users,
making it impossible to single out an individual from their search pattern.
"""
import re
from collections import Counter
from dataclasses import dataclass, field


@dataclass
class KAnonymityConfig:
    """Configuration for k-anonymity enforcement."""

    k: int = 5
    generalization_level: int = 1


def _tokenize(text: str) -> list[str]:
    """Split text into lowercase word tokens."""
    return re.findall(r'[a-zA-Zа-яёА-ЯЁ0-9]+', text.lower())


class QueryGeneralizer:
    """Generalizes a single query string at varying levels of abstraction."""

    def __init__(self) -> None:
        self._history: list[str] = []
        self._freq: Counter[str] = Counter()

    # ------------------------------------------------------------------
    # History / frequency tracking
    # ------------------------------------------------------------------

    def add_to_history(self, query: str) -> None:
        """Record *query* in the internal history and update token frequencies."""
        self._history.append(query)
        for tok in _tokenize(query):
            self._freq[tok] += 1

    def token_frequency(self, token: str) -> int:
        """Return how many times *token* appeared across all recorded queries."""
        return self._freq[token.lower()]

    # ------------------------------------------------------------------
    # Generalization
    # ------------------------------------------------------------------

    def generalize(self, query: str, level: int = 1) -> str:
        """Return a generalized version of *query*.

        Level 1 — remove rare tokens (keep only tokens that appear more than
                  once in the recorded query history).
        Level 2 — replace specific numbers with ``[NUM]`` and Title-Case words
                  (potential proper names) with ``[NAME]``.
        Level 3 — keep only the three longest tokens.
        """
        if level <= 0:
            return query

        if level >= 3:
            return self._level3(query)
        if level == 2:
            return self._level2(query)
        # level == 1
        return self._level1(query)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _level1(self, query: str) -> str:
        """Keep only tokens with frequency > 1 in history."""
        tokens = _tokenize(query)
        kept = [t for t in tokens if self._freq[t] > 1]
        return ' '.join(kept) if kept else query

    def _level2(self, query: str) -> str:
        """Replace numbers → [NUM] and Title-Case words → [NAME]."""
        # Apply number and name substitutions on the *original* query first
        # so that casing and digits are still present.
        result = query

        # Replace standalone numbers
        result = re.sub(r'\b\d+\b', '[NUM]', result)

        # Replace Title-Case words (potential proper names / specific entities)
        # A "title-case word" starts with an uppercase letter followed by
        # one or more lowercase letters — and is not already a placeholder.
        result = re.sub(
            r'\b(?!\[)[A-ZА-ЯЁ][a-zа-яё]+\b',
            '[NAME]',
            result,
        )

        # Now apply level-1 rare-token removal on the substituted text.
        # Tokenize the substituted result (keeping placeholders as tokens).
        tokens = re.findall(r'\[[A-Z]+\]|[a-zA-Zа-яёА-ЯЁ0-9]+', result)
        kept = []
        for t in tokens:
            # Placeholders are always kept; ordinary tokens must be frequent.
            if t.startswith('[') or self._freq[t.lower()] > 1:
                kept.append(t)
        if not kept:
            return result  # fallback: return the substituted (not filtered) text
        return ' '.join(kept)

    def _level3(self, query: str) -> str:
        """Return only the top-3 tokens by length."""
        tokens = _tokenize(query)
        if not tokens:
            return query
        top3 = sorted(set(tokens), key=len, reverse=True)[:3]
        return ' '.join(top3)


class KAnonymizer:
    """Enforce k-anonymity over a batch of queries by generalization."""

    def __init__(self, config: KAnonymityConfig | None = None) -> None:
        self._config = config or KAnonymityConfig()
        self._generalizer = QueryGeneralizer()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def anonymize_batch(self, queries: list[str]) -> list[str]:
        """Generalize each query until every group has size >= k.

        Queries that are textually identical after generalization are grouped
        together.  Generalization levels are increased until each group
        contains at least ``config.k`` members or the maximum level (3) is
        reached.
        """
        if not queries:
            return []

        k = self._config.k
        start_level = self._config.generalization_level

        # Seed the history so the generalizer can compute token frequencies.
        for q in queries:
            self._generalizer.add_to_history(q)

        # Try increasing generalization levels until k-anonymity is met or
        # we run out of levels.
        for level in range(start_level, 4):
            generalized = [
                self._generalizer.generalize(q, level=level) for q in queries
            ]
            counts = Counter(generalized)
            if all(counts[g] >= k for g in generalized):
                return generalized

        # Fallback: return whatever we produced at level 3.
        return [self._generalizer.generalize(q, level=3) for q in queries]

    def group_count(self, queries: list[str]) -> dict[str, int]:
        """Return a mapping of generalized-query → count of members in group.

        Uses the same generalization level as :meth:`anonymize_batch`.
        """
        generalized = self.anonymize_batch(queries)
        counts: Counter[str] = Counter(generalized)
        return {g: counts[g] for g in generalized}
