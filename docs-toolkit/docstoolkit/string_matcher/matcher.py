"""String matching algorithms: exact, fuzzy, glob, regex, soundex, prefix, suffix.

Stdlib-only implementation using ``re``, ``difflib`` and ``fnmatch``.
"""

from __future__ import annotations

import difflib
import fnmatch
import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class MatchMode(Enum):
    """Enumeration of supported matching modes."""

    EXACT = "exact"
    EXACT_CI = "exact_ci"
    SUBSTRING = "substring"
    FUZZY = "fuzzy"
    GLOB = "glob"
    REGEX = "regex"
    SOUNDEX = "soundex"
    PREFIX = "prefix"
    SUFFIX = "suffix"


@dataclass
class MatchScore:
    """Result of matching a query against a single target."""

    query: str
    target: str
    score: float
    mode: MatchMode
    matched: bool


@dataclass
class MatcherConfig:
    """Configuration knobs for :class:`StringMatcher`."""

    case_sensitive: bool = True
    fuzzy_threshold: float = 0.6


# Soundex mapping for English consonants.
_SOUNDEX_MAP = {
    "B": "1", "F": "1", "P": "1", "V": "1",
    "C": "2", "G": "2", "J": "2", "K": "2",
    "Q": "2", "S": "2", "X": "2", "Z": "2",
    "D": "3", "T": "3",
    "L": "4",
    "M": "5", "N": "5",
    "R": "6",
}


class StringMatcher:
    """Multi-mode string matcher with simple scoring semantics."""

    def __init__(self, config: Optional[MatcherConfig] = None) -> None:
        self.config = config if config is not None else MatcherConfig()

    # ------------------------------------------------------------------ #
    # Individual matchers
    # ------------------------------------------------------------------ #
    def exact(self, query: str, target: str, case_sensitive: bool = True) -> bool:
        """Return ``True`` if ``query`` equals ``target``."""
        if case_sensitive:
            return query == target
        return query.lower() == target.lower()

    def substring(self, query: str, target: str, case_sensitive: bool = True) -> bool:
        """Return ``True`` if ``query`` is a substring of ``target``."""
        if case_sensitive:
            return query in target
        return query.lower() in target.lower()

    def fuzzy(self, query: str, target: str) -> float:
        """Return ``difflib.SequenceMatcher`` ratio in ``[0.0, 1.0]``."""
        if not query and not target:
            return 1.0
        return difflib.SequenceMatcher(None, query, target).ratio()

    def glob(self, pattern: str, target: str) -> bool:
        """Glob match using :func:`fnmatch.fnmatchcase` (case-sensitive)."""
        return fnmatch.fnmatchcase(target, pattern)

    def regex(self, pattern: str, target: str) -> bool:
        """Return ``True`` if ``pattern`` matches anywhere inside ``target``."""
        try:
            return re.search(pattern, target) is not None
        except re.error:
            return False

    def soundex(self, word: str) -> str:
        """Compute the 4-character Soundex code for an English word."""
        if not word:
            return ""

        word = word.upper()
        # Strip non-letters – Soundex is defined on alphabetic input.
        letters = [ch for ch in word if "A" <= ch <= "Z"]
        if not letters:
            return ""

        first = letters[0]
        # Map remaining letters; vowels and H/W/Y become "0" (drop later).
        coded = [first]
        for ch in letters[1:]:
            coded.append(_SOUNDEX_MAP.get(ch, "0"))

        # Code for the first letter is needed to suppress adjacent duplicates.
        first_code = _SOUNDEX_MAP.get(first, "0")

        # Collapse adjacent duplicates (including a duplicate following the
        # first letter's code), then drop zeros.
        collapsed: List[str] = [first]
        prev = first_code
        for code in coded[1:]:
            if code != prev:
                collapsed.append(code)
            prev = code

        digits = [c for c in collapsed[1:] if c != "0"]
        result = first + "".join(digits)
        result = (result + "000")[:4]
        return result

    def prefix(self, query: str, target: str, case_sensitive: bool = True) -> bool:
        """Return ``True`` if ``target`` starts with ``query``."""
        if case_sensitive:
            return target.startswith(query)
        return target.lower().startswith(query.lower())

    def suffix(self, query: str, target: str, case_sensitive: bool = True) -> bool:
        """Return ``True`` if ``target`` ends with ``query``."""
        if case_sensitive:
            return target.endswith(query)
        return target.lower().endswith(query.lower())

    # ------------------------------------------------------------------ #
    # Dispatching API
    # ------------------------------------------------------------------ #
    def match(
        self,
        query: str,
        target: str,
        mode: MatchMode = MatchMode.EXACT,
    ) -> MatchScore:
        """Match ``query`` against ``target`` using ``mode``."""
        cs = self.config.case_sensitive

        if mode == MatchMode.EXACT:
            ok = self.exact(query, target, case_sensitive=True)
            score = 1.0 if ok else 0.0
        elif mode == MatchMode.EXACT_CI:
            ok = self.exact(query, target, case_sensitive=False)
            score = 1.0 if ok else 0.0
        elif mode == MatchMode.SUBSTRING:
            ok = self.substring(query, target, case_sensitive=cs)
            score = 1.0 if ok else 0.0
        elif mode == MatchMode.FUZZY:
            score = self.fuzzy(query, target)
            ok = score > self.config.fuzzy_threshold
        elif mode == MatchMode.GLOB:
            ok = self.glob(query, target)
            score = 1.0 if ok else 0.0
        elif mode == MatchMode.REGEX:
            ok = self.regex(query, target)
            score = 1.0 if ok else 0.0
        elif mode == MatchMode.SOUNDEX:
            ok = bool(query) and bool(target) and self.soundex(query) == self.soundex(target)
            score = 1.0 if ok else 0.0
        elif mode == MatchMode.PREFIX:
            ok = self.prefix(query, target, case_sensitive=cs)
            score = 1.0 if ok else 0.0
        elif mode == MatchMode.SUFFIX:
            ok = self.suffix(query, target, case_sensitive=cs)
            score = 1.0 if ok else 0.0
        else:  # pragma: no cover - defensive
            raise ValueError(f"Unsupported match mode: {mode!r}")

        if mode == MatchMode.FUZZY:
            matched = score > self.config.fuzzy_threshold
        else:
            matched = score > 0

        return MatchScore(
            query=query,
            target=target,
            score=score,
            mode=mode,
            matched=matched,
        )

    def match_all(
        self,
        query: str,
        targets: List[str],
        mode: MatchMode = MatchMode.EXACT,
    ) -> List[MatchScore]:
        """Match ``query`` against each entry of ``targets``."""
        return [self.match(query, t, mode) for t in targets]

    def find_best(
        self,
        query: str,
        targets: List[str],
        mode: MatchMode = MatchMode.FUZZY,
    ) -> Optional[MatchScore]:
        """Return the highest-scoring :class:`MatchScore` (or ``None``)."""
        if not targets:
            return None
        scored = self.match_all(query, targets, mode)
        best = max(scored, key=lambda s: s.score)
        if not best.matched:
            return None
        return best

    def find_top_k(
        self,
        query: str,
        targets: List[str],
        k: int = 5,
        mode: MatchMode = MatchMode.FUZZY,
    ) -> List[MatchScore]:
        """Return up to ``k`` best matches, sorted by descending score."""
        if k <= 0 or not targets:
            return []
        scored = self.match_all(query, targets, mode)
        scored = [s for s in scored if s.matched]
        scored.sort(key=lambda s: s.score, reverse=True)
        return scored[:k]
