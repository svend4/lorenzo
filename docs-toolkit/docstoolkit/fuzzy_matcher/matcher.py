"""Fuzzy string matching with multiple algorithms.

Implements Levenshtein distance/ratio, Jaro, Jaro-Winkler, n-gram Dice,
difflib ratio (with partial/token variants) — all pure stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from difflib import SequenceMatcher
from enum import Enum
from typing import List, Optional


class FuzzyAlgo(Enum):
    """Supported fuzzy matching algorithms."""

    LEVENSHTEIN = "levenshtein"
    JARO = "jaro"
    JARO_WINKLER = "jaro_winkler"
    NGRAM = "ngram"
    RATIO = "ratio"
    PARTIAL_RATIO = "partial_ratio"
    TOKEN_SORT = "token_sort"
    TOKEN_SET = "token_set"


@dataclass
class FuzzyMatch:
    """Result of a fuzzy match operation."""

    query: str
    target: str
    score: float
    algo: FuzzyAlgo
    meets_threshold: bool = False


@dataclass
class FuzzyConfig:
    """Configuration for FuzzyMatcher."""

    algo: FuzzyAlgo = FuzzyAlgo.RATIO
    threshold: float = 0.7
    case_sensitive: bool = False
    ngram_size: int = 2


class FuzzyMatcher:
    """Fuzzy string matcher with pluggable algorithms."""

    def __init__(self, config: Optional[FuzzyConfig] = None) -> None:
        self.config = config if config is not None else FuzzyConfig()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _prep(self, s: str) -> str:
        if not self.config.case_sensitive:
            return s.lower()
        return s

    def _compute(self, a: str, b: str, algo: FuzzyAlgo) -> float:
        if algo is FuzzyAlgo.LEVENSHTEIN:
            return self.levenshtein_ratio(a, b)
        if algo is FuzzyAlgo.JARO:
            return self.jaro_similarity(a, b)
        if algo is FuzzyAlgo.JARO_WINKLER:
            return self.jaro_winkler(a, b)
        if algo is FuzzyAlgo.NGRAM:
            return self.ngram_similarity(a, b, self.config.ngram_size)
        if algo is FuzzyAlgo.RATIO:
            return self.ratio(a, b)
        if algo is FuzzyAlgo.PARTIAL_RATIO:
            return self.partial_ratio(a, b)
        if algo is FuzzyAlgo.TOKEN_SORT:
            return self.token_sort_ratio(a, b)
        if algo is FuzzyAlgo.TOKEN_SET:
            return self.token_set_ratio(a, b)
        raise ValueError(f"Unknown algorithm: {algo}")

    # ------------------------------------------------------------------
    # Algorithm primitives
    # ------------------------------------------------------------------
    def levenshtein_distance(self, a: str, b: str) -> int:
        """Standard Levenshtein edit distance via dynamic programming."""
        if a == b:
            return 0
        if not a:
            return len(b)
        if not b:
            return len(a)

        # Two-row DP for memory efficiency
        prev = list(range(len(b) + 1))
        curr = [0] * (len(b) + 1)
        for i, ca in enumerate(a, 1):
            curr[0] = i
            for j, cb in enumerate(b, 1):
                cost = 0 if ca == cb else 1
                curr[j] = min(
                    prev[j] + 1,        # deletion
                    curr[j - 1] + 1,    # insertion
                    prev[j - 1] + cost,  # substitution
                )
            prev, curr = curr, prev
        return prev[len(b)]

    def levenshtein_ratio(self, a: str, b: str) -> float:
        """Normalized Levenshtein similarity in [0, 1]."""
        if not a and not b:
            return 1.0
        max_len = max(len(a), len(b))
        if max_len == 0:
            return 1.0
        dist = self.levenshtein_distance(a, b)
        return 1.0 - (dist / max_len)

    def jaro_similarity(self, a: str, b: str) -> float:
        """Jaro similarity in [0, 1]."""
        if a == b:
            return 1.0
        if not a or not b:
            return 0.0

        len_a, len_b = len(a), len(b)
        match_distance = max(len_a, len_b) // 2 - 1
        if match_distance < 0:
            match_distance = 0

        a_matches = [False] * len_a
        b_matches = [False] * len_b

        matches = 0
        for i in range(len_a):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len_b)
            for j in range(start, end):
                if b_matches[j]:
                    continue
                if a[i] != b[j]:
                    continue
                a_matches[i] = True
                b_matches[j] = True
                matches += 1
                break

        if matches == 0:
            return 0.0

        # Count transpositions
        k = 0
        transpositions = 0
        for i in range(len_a):
            if not a_matches[i]:
                continue
            while not b_matches[k]:
                k += 1
            if a[i] != b[k]:
                transpositions += 1
            k += 1
        transpositions //= 2

        m = float(matches)
        return (m / len_a + m / len_b + (m - transpositions) / m) / 3.0

    def jaro_winkler(self, a: str, b: str, prefix_scale: float = 0.1) -> float:
        """Jaro-Winkler similarity favoring matching prefixes."""
        if a == b:
            return 1.0
        if not a or not b:
            return 0.0
        jaro = self.jaro_similarity(a, b)
        # Common prefix length, max 4
        prefix_len = 0
        for ca, cb in zip(a, b):
            if ca == cb:
                prefix_len += 1
                if prefix_len == 4:
                    break
            else:
                break
        return jaro + prefix_len * prefix_scale * (1.0 - jaro)

    def ngram_similarity(self, a: str, b: str, n: int = 2) -> float:
        """Dice coefficient on character n-gram multisets."""
        if n <= 0:
            raise ValueError("n must be positive")
        if a == b:
            return 1.0
        if not a or not b:
            return 0.0
        if len(a) < n or len(b) < n:
            # Fall back to character set
            n = 1

        def grams(s: str) -> List[str]:
            return [s[i:i + n] for i in range(len(s) - n + 1)]

        ga = grams(a)
        gb = grams(b)
        if not ga or not gb:
            return 0.0

        # Multiset intersection
        from collections import Counter
        ca = Counter(ga)
        cb = Counter(gb)
        intersection = sum((ca & cb).values())
        return 2.0 * intersection / (len(ga) + len(gb))

    def ratio(self, a: str, b: str) -> float:
        """difflib SequenceMatcher ratio."""
        if a == b:
            return 1.0
        if not a and not b:
            return 1.0
        if not a or not b:
            return 0.0
        return SequenceMatcher(None, a, b).ratio()

    def partial_ratio(self, a: str, b: str) -> float:
        """Best substring match — slide the shorter string across the longer."""
        if a == b:
            return 1.0
        if not a and not b:
            return 1.0
        if not a or not b:
            return 0.0

        if len(a) <= len(b):
            shorter, longer = a, b
        else:
            shorter, longer = b, a

        if len(shorter) == 0:
            return 0.0

        # Use difflib to find best matching block, then score substrings
        sm = SequenceMatcher(None, shorter, longer)
        blocks = sm.get_matching_blocks()
        best = 0.0
        for block in blocks:
            i, j, size = block
            # Substring of longer aligned to shorter
            start = max(0, j - i)
            end = start + len(shorter)
            if end > len(longer):
                end = len(longer)
                start = max(0, end - len(shorter))
            substr = longer[start:end]
            r = SequenceMatcher(None, shorter, substr).ratio()
            if r > best:
                best = r
        return best

    def token_sort_ratio(self, a: str, b: str) -> float:
        """Sort tokens, then compute ratio."""
        if a == b:
            return 1.0
        if not a and not b:
            return 1.0
        if not a or not b:
            return 0.0
        sa = " ".join(sorted(a.split()))
        sb = " ".join(sorted(b.split()))
        if not sa and not sb:
            return 1.0
        if not sa or not sb:
            return 0.0
        return SequenceMatcher(None, sa, sb).ratio()

    def token_set_ratio(self, a: str, b: str) -> float:
        """Token set ratio: intersection vs differences (max of three ratios)."""
        if a == b:
            return 1.0
        if not a and not b:
            return 1.0
        if not a or not b:
            return 0.0

        tokens_a = set(a.split())
        tokens_b = set(b.split())
        if not tokens_a and not tokens_b:
            return 1.0
        if not tokens_a or not tokens_b:
            return 0.0

        intersection = tokens_a & tokens_b
        diff_ab = tokens_a - tokens_b
        diff_ba = tokens_b - tokens_a

        sorted_inter = " ".join(sorted(intersection))
        sorted_ab = (sorted_inter + " " + " ".join(sorted(diff_ab))).strip()
        sorted_ba = (sorted_inter + " " + " ".join(sorted(diff_ba))).strip()

        def _r(x: str, y: str) -> float:
            if not x and not y:
                return 1.0
            if not x or not y:
                return 0.0
            return SequenceMatcher(None, x, y).ratio()

        scores = [
            _r(sorted_inter, sorted_ab),
            _r(sorted_inter, sorted_ba),
            _r(sorted_ab, sorted_ba),
        ]
        return max(scores)

    # ------------------------------------------------------------------
    # High-level API
    # ------------------------------------------------------------------
    def match(
        self,
        query: str,
        target: str,
        algo: Optional[FuzzyAlgo] = None,
    ) -> FuzzyMatch:
        """Match query against a single target."""
        algo = algo if algo is not None else self.config.algo
        a = self._prep(query)
        b = self._prep(target)
        score = self._compute(a, b, algo)
        # Clamp to [0, 1] to defend against floating-point creep
        if score < 0.0:
            score = 0.0
        elif score > 1.0:
            score = 1.0
        return FuzzyMatch(
            query=query,
            target=target,
            score=score,
            algo=algo,
            meets_threshold=score >= self.config.threshold,
        )

    def match_many(
        self,
        query: str,
        targets: List[str],
        algo: Optional[FuzzyAlgo] = None,
        threshold: Optional[float] = None,
    ) -> List[FuzzyMatch]:
        """Match query against many targets, filtered by threshold."""
        algo = algo if algo is not None else self.config.algo
        thr = threshold if threshold is not None else self.config.threshold
        results: List[FuzzyMatch] = []
        for target in targets:
            a = self._prep(query)
            b = self._prep(target)
            score = self._compute(a, b, algo)
            if score < 0.0:
                score = 0.0
            elif score > 1.0:
                score = 1.0
            if score >= thr:
                results.append(
                    FuzzyMatch(
                        query=query,
                        target=target,
                        score=score,
                        algo=algo,
                        meets_threshold=True,
                    )
                )
        results.sort(key=lambda m: m.score, reverse=True)
        return results

    def find_best(
        self,
        query: str,
        targets: List[str],
        algo: Optional[FuzzyAlgo] = None,
    ) -> Optional[FuzzyMatch]:
        """Return the single best match, or None if `targets` empty."""
        if not targets:
            return None
        algo = algo if algo is not None else self.config.algo
        best: Optional[FuzzyMatch] = None
        for target in targets:
            m = self.match(query, target, algo)
            if best is None or m.score > best.score:
                best = m
        return best

    def find_top_k(
        self,
        query: str,
        targets: List[str],
        k: int = 5,
        algo: Optional[FuzzyAlgo] = None,
    ) -> List[FuzzyMatch]:
        """Return top-K matches sorted by score descending."""
        if k <= 0 or not targets:
            return []
        algo = algo if algo is not None else self.config.algo
        all_matches = [self.match(query, t, algo) for t in targets]
        all_matches.sort(key=lambda m: m.score, reverse=True)
        return all_matches[:k]
