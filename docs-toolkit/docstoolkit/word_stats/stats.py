"""word_stats.stats — word-level statistics for text documents."""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional


_DEFAULT_STOP_WORDS: frozenset[str] = frozenset({
    "the", "a", "an", "is", "are", "was", "were",
    "in", "on", "at", "to", "of", "and", "or", "but",
    "for", "with", "be", "it", "this", "that", "by",
})

_TOKEN_RE = re.compile(r"\b[a-zа-яё]+\b")
_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+(?:\s|$)")
_PARAGRAPH_SPLIT_RE = re.compile(r"\n\n+")


@dataclass
class WordFrequency:
    """A single word with its absolute count and relative frequency."""

    word: str
    count: int
    frequency: float  # 0.0–1.0 relative to total token count


@dataclass
class TextStats:
    """Aggregate statistics computed over a body of text."""

    word_count: int
    unique_word_count: int
    char_count: int
    sentence_count: int
    paragraph_count: int
    avg_word_length: float
    avg_sentence_length: float  # words per sentence
    type_token_ratio: float     # unique / total (0–1)
    lexical_density: float      # content words / total words (0–1)
    most_common: list[WordFrequency] = field(default_factory=list)
    hapax_count: int = 0


class WordStatsAnalyzer:
    """Compute word-level statistics for text documents.

    Parameters
    ----------
    stop_words:
        Set of lowercase words considered function/stop words.
        Defaults to a small English stop-word list.
    min_word_length:
        Tokens shorter than this value are excluded from all
        computations.  Defaults to 1 (i.e. include everything).
    """

    def __init__(
        self,
        stop_words: Optional[set[str]] = None,
        min_word_length: int = 1,
    ) -> None:
        self._stop_words: frozenset[str] = (
            frozenset(stop_words) if stop_words is not None else _DEFAULT_STOP_WORDS
        )
        self._min_word_length = min_word_length

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _tokenize(self, text: str) -> list[str]:
        """Return lowercase word tokens from *text*, filtered by min_word_length."""
        tokens = _TOKEN_RE.findall(text.lower())
        if self._min_word_length > 1:
            tokens = [t for t in tokens if len(t) >= self._min_word_length]
        return tokens

    @staticmethod
    def _count_sentences(text: str) -> int:
        """Return the number of sentences in *text*.

        A sentence boundary is a sequence of ``[.!?]+`` followed by
        whitespace or end-of-string.  An empty (or whitespace-only)
        text has 0 sentences; any non-empty text that lacks terminal
        punctuation is treated as one sentence.
        """
        stripped = text.strip()
        if not stripped:
            return 0
        parts = [p for p in _SENTENCE_SPLIT_RE.split(stripped) if p.strip()]
        # Each split removes a sentence-ending boundary, so boundaries = len(parts)
        # unless the text ends without punctuation (last part is non-empty).
        n_boundaries = len(_SENTENCE_SPLIT_RE.findall(stripped))
        # Sentences = boundaries + (1 if trailing non-terminated fragment exists)
        has_trailing = bool(stripped) and not _SENTENCE_SPLIT_RE.search(stripped[-3:])
        # Simpler: count boundary separators, then add 1 if there is text after
        # the last boundary (or no boundaries at all but non-empty text).
        remaining_after_last = _SENTENCE_SPLIT_RE.split(stripped)[-1].strip()
        return n_boundaries + (1 if remaining_after_last else 0)

    @staticmethod
    def _count_paragraphs(text: str) -> int:
        """Return paragraph count (split on ``\\n\\n+``)."""
        stripped = text.strip()
        if not stripped:
            return 0
        parts = [p.strip() for p in _PARAGRAPH_SPLIT_RE.split(stripped)]
        return sum(1 for p in parts if p)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze(self, text: str, top_n: int = 10) -> TextStats:
        """Compute :class:`TextStats` for *text*.

        Parameters
        ----------
        text:
            The document text to analyse.
        top_n:
            How many entries to include in ``most_common``.
        """
        tokens = self._tokenize(text)
        total = len(tokens)

        # Basic counts
        char_count = len(text)
        sentence_count = self._count_sentences(text)
        paragraph_count = self._count_paragraphs(text)

        if total == 0:
            return TextStats(
                word_count=0,
                unique_word_count=0,
                char_count=char_count,
                sentence_count=sentence_count,
                paragraph_count=paragraph_count,
                avg_word_length=0.0,
                avg_sentence_length=0.0,
                type_token_ratio=0.0,
                lexical_density=0.0,
                most_common=[],
                hapax_count=0,
            )

        counter: Counter[str] = Counter(tokens)
        unique_count = len(counter)

        avg_word_length = sum(len(w) for w in tokens) / total
        avg_sentence_length = total / sentence_count if sentence_count else 0.0
        type_token_ratio = unique_count / total

        content_words = [t for t in tokens if t not in self._stop_words]
        lexical_density = len(content_words) / total

        most_common_raw = counter.most_common(top_n)
        most_common = [
            WordFrequency(word=w, count=c, frequency=c / total)
            for w, c in most_common_raw
        ]

        hapax_count = sum(1 for c in counter.values() if c == 1)

        return TextStats(
            word_count=total,
            unique_word_count=unique_count,
            char_count=char_count,
            sentence_count=sentence_count,
            paragraph_count=paragraph_count,
            avg_word_length=avg_word_length,
            avg_sentence_length=avg_sentence_length,
            type_token_ratio=type_token_ratio,
            lexical_density=lexical_density,
            most_common=most_common,
            hapax_count=hapax_count,
        )

    def word_frequencies(
        self, text: str, top_n: Optional[int] = None
    ) -> list[WordFrequency]:
        """Return :class:`WordFrequency` objects sorted by count descending.

        Parameters
        ----------
        text:
            The document text to analyse.
        top_n:
            If given, only the top *top_n* entries are returned.
            ``None`` returns all words.
        """
        tokens = self._tokenize(text)
        total = len(tokens)
        if total == 0:
            return []
        counter: Counter[str] = Counter(tokens)
        ranked = counter.most_common(top_n)
        return [
            WordFrequency(word=w, count=c, frequency=c / total) for w, c in ranked
        ]

    def compare(self, text_a: str, text_b: str) -> dict:
        """Compare the vocabularies of two texts.

        Returns
        -------
        dict with keys:

        * ``shared_words`` — set of words in both texts
        * ``unique_to_a`` — set of words only in text_a
        * ``unique_to_b`` — set of words only in text_b
        * ``vocab_overlap`` — Jaccard similarity on word sets (0–1)
        """
        words_a = set(self._tokenize(text_a))
        words_b = set(self._tokenize(text_b))

        shared = words_a & words_b
        unique_a = words_a - words_b
        unique_b = words_b - words_a
        union = words_a | words_b
        jaccard = len(shared) / len(union) if union else 0.0

        return {
            "shared_words": shared,
            "unique_to_a": unique_a,
            "unique_to_b": unique_b,
            "vocab_overlap": jaccard,
        }

    def reading_time(self, text: str, wpm: int = 200) -> float:
        """Estimate reading time in minutes.

        Parameters
        ----------
        text:
            The document text.
        wpm:
            Reading speed in words per minute.  Defaults to 200.
        """
        tokens = self._tokenize(text)
        return len(tokens) / wpm if wpm > 0 else 0.0
