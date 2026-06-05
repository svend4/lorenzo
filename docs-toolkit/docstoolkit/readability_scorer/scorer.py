"""Readability scoring — Flesch, Flesch-Kincaid, Gunning Fog, ARI, Coleman-Liau.

Stdlib-only implementation. All formulas operate on counts derived from simple
tokenization (word = run of letters/digits; sentence = run terminated by .!?).
Syllable counting uses a vowel-group heuristic with a silent-e adjustment.

For empty input or zero-division corner cases, metrics return ``0.0`` instead
of raising.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


VOWELS = set("aeiouy")
_WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?")
_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")


class ReadabilityLevel(str, Enum):
    """Qualitative readability bucket derived from Flesch Reading Ease."""

    VERY_EASY = "very_easy"
    EASY = "easy"
    FAIRLY_EASY = "fairly_easy"
    STANDARD = "standard"
    FAIRLY_DIFFICULT = "fairly_difficult"
    DIFFICULT = "difficult"
    VERY_DIFFICULT = "very_difficult"


@dataclass
class ReadabilityScore:
    """Container of readability metrics for a piece of text."""

    flesch_reading_ease: float
    flesch_kincaid_grade: float
    gunning_fog: float
    automated_readability_index: float
    coleman_liau_index: float
    level: ReadabilityLevel
    word_count: int
    sentence_count: int
    syllable_count: int
    complex_word_count: int
    avg_sentence_length: float
    avg_syllables_per_word: float


def _level_for_flesch(score: float) -> ReadabilityLevel:
    if score >= 90:
        return ReadabilityLevel.VERY_EASY
    if score >= 80:
        return ReadabilityLevel.EASY
    if score >= 70:
        return ReadabilityLevel.FAIRLY_EASY
    if score >= 60:
        return ReadabilityLevel.STANDARD
    if score >= 50:
        return ReadabilityLevel.FAIRLY_DIFFICULT
    if score >= 30:
        return ReadabilityLevel.DIFFICULT
    return ReadabilityLevel.VERY_DIFFICULT


class ReadabilityScorer:
    """Compute classical readability metrics for English-style text."""

    # ------------------------------------------------------------------ tokenization

    @staticmethod
    def _words(text: str) -> list[str]:
        if not text:
            return []
        return _WORD_RE.findall(text)

    @staticmethod
    def _sentences(text: str) -> list[str]:
        if not text or not text.strip():
            return []
        parts = [p.strip() for p in _SENTENCE_SPLIT_RE.split(text) if p.strip()]
        return parts

    # ------------------------------------------------------------------ syllables

    def count_syllables(self, word: str) -> int:
        """Count syllables using a vowel-group heuristic.

        - Lowercase the word.
        - Each maximal run of vowels (``aeiouy``) counts as one syllable.
        - If the word ends in a silent ``e`` (and that ``e`` constituted its own
          vowel group), subtract one syllable.
        - The minimum result for any non-empty word is 1.
        """
        if not word:
            return 0
        w = re.sub(r"[^A-Za-z]", "", word).lower()
        if not w:
            return 0

        count = 0
        prev_is_vowel = False
        for ch in w:
            is_vowel = ch in VOWELS
            if is_vowel and not prev_is_vowel:
                count += 1
            prev_is_vowel = is_vowel

        # Silent trailing 'e': only strip if 'e' is its own vowel group
        # (i.e., preceded by a consonant) and removing it still leaves >=1 syllable.
        if w.endswith("e") and len(w) >= 2 and w[-2] not in VOWELS and count > 1:
            count -= 1

        return max(count, 1)

    # ------------------------------------------------------------------ counts

    def count_words(self, text: str) -> int:
        return len(self._words(text))

    def count_sentences(self, text: str) -> int:
        return len(self._sentences(text))

    def count_complex_words(self, text: str) -> int:
        return sum(1 for w in self._words(text) if self.count_syllables(w) >= 3)

    def _total_syllables(self, words: list[str]) -> int:
        return sum(self.count_syllables(w) for w in words)

    def _letter_count(self, words: list[str]) -> int:
        return sum(len(re.sub(r"[^A-Za-z]", "", w)) for w in words)

    def _char_count(self, words: list[str]) -> int:
        # ARI uses characters (letters + digits) — count all alphanumerics.
        return sum(len(re.sub(r"[^A-Za-z0-9]", "", w)) for w in words)

    # ------------------------------------------------------------------ individual metrics

    def flesch_reading_ease(self, text: str) -> float:
        words = self._words(text)
        sentences = self._sentences(text)
        if not words or not sentences:
            return 0.0
        syllables = self._total_syllables(words)
        if syllables == 0:
            return 0.0
        return 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllables / len(words))

    def flesch_kincaid_grade(self, text: str) -> float:
        words = self._words(text)
        sentences = self._sentences(text)
        if not words or not sentences:
            return 0.0
        syllables = self._total_syllables(words)
        if syllables == 0:
            return 0.0
        return 0.39 * (len(words) / len(sentences)) + 11.8 * (syllables / len(words)) - 15.59

    def gunning_fog(self, text: str) -> float:
        words = self._words(text)
        sentences = self._sentences(text)
        if not words or not sentences:
            return 0.0
        complex_words = self.count_complex_words(text)
        return 0.4 * ((len(words) / len(sentences)) + 100 * (complex_words / len(words)))

    def automated_readability_index(self, text: str) -> float:
        words = self._words(text)
        sentences = self._sentences(text)
        if not words or not sentences:
            return 0.0
        chars = self._char_count(words)
        if chars == 0:
            return 0.0
        return 4.71 * (chars / len(words)) + 0.5 * (len(words) / len(sentences)) - 21.43

    def coleman_liau_index(self, text: str) -> float:
        words = self._words(text)
        sentences = self._sentences(text)
        if not words or not sentences:
            return 0.0
        letters = self._letter_count(words)
        if letters == 0:
            return 0.0
        L = letters / len(words) * 100  # letters per 100 words
        S = len(sentences) / len(words) * 100  # sentences per 100 words
        return 0.0588 * L - 0.296 * S - 15.8

    # ------------------------------------------------------------------ aggregate

    def score(self, text: str) -> ReadabilityScore:
        words = self._words(text)
        sentences = self._sentences(text)
        word_count = len(words)
        sentence_count = len(sentences)
        syllable_count = self._total_syllables(words) if words else 0
        complex_word_count = sum(1 for w in words if self.count_syllables(w) >= 3)

        if word_count == 0 or sentence_count == 0:
            return ReadabilityScore(
                flesch_reading_ease=0.0,
                flesch_kincaid_grade=0.0,
                gunning_fog=0.0,
                automated_readability_index=0.0,
                coleman_liau_index=0.0,
                level=_level_for_flesch(0.0),
                word_count=word_count,
                sentence_count=sentence_count,
                syllable_count=syllable_count,
                complex_word_count=complex_word_count,
                avg_sentence_length=0.0,
                avg_syllables_per_word=0.0,
            )

        fre = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllable_count / word_count)
        fkg = 0.39 * (word_count / sentence_count) + 11.8 * (syllable_count / word_count) - 15.59
        fog = 0.4 * ((word_count / sentence_count) + 100 * (complex_word_count / word_count))
        chars = self._char_count(words)
        ari = (4.71 * (chars / word_count) + 0.5 * (word_count / sentence_count) - 21.43) if chars else 0.0
        letters = self._letter_count(words)
        if letters:
            L = letters / word_count * 100
            S = sentence_count / word_count * 100
            cli = 0.0588 * L - 0.296 * S - 15.8
        else:
            cli = 0.0

        return ReadabilityScore(
            flesch_reading_ease=fre,
            flesch_kincaid_grade=fkg,
            gunning_fog=fog,
            automated_readability_index=ari,
            coleman_liau_index=cli,
            level=_level_for_flesch(fre),
            word_count=word_count,
            sentence_count=sentence_count,
            syllable_count=syllable_count,
            complex_word_count=complex_word_count,
            avg_sentence_length=word_count / sentence_count,
            avg_syllables_per_word=syllable_count / word_count,
        )

    def score_batch(self, texts: list[str]) -> list[ReadabilityScore]:
        return [self.score(t) for t in texts]

    # ------------------------------------------------------------------ compare

    def compare(self, text_a: str, text_b: str) -> dict:
        """Return a dict of metric deltas (``b - a``) plus the raw scores."""
        a = self.score(text_a)
        b = self.score(text_b)
        return {
            "a": a,
            "b": b,
            "flesch_reading_ease_diff": b.flesch_reading_ease - a.flesch_reading_ease,
            "flesch_kincaid_grade_diff": b.flesch_kincaid_grade - a.flesch_kincaid_grade,
            "gunning_fog_diff": b.gunning_fog - a.gunning_fog,
            "automated_readability_index_diff": b.automated_readability_index - a.automated_readability_index,
            "coleman_liau_index_diff": b.coleman_liau_index - a.coleman_liau_index,
            "word_count_diff": b.word_count - a.word_count,
            "sentence_count_diff": b.sentence_count - a.sentence_count,
            "syllable_count_diff": b.syllable_count - a.syllable_count,
            "complex_word_count_diff": b.complex_word_count - a.complex_word_count,
            "avg_sentence_length_diff": b.avg_sentence_length - a.avg_sentence_length,
            "avg_syllables_per_word_diff": b.avg_syllables_per_word - a.avg_syllables_per_word,
        }
