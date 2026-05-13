"""Extractive document summarization.

Provides multiple heuristic algorithms (no LLM, stdlib only):
  * FIRST_N / LAST_N    — naive head/tail selection
  * LEAD_3              — classic newswire lead
  * KEYWORD_DENSITY     — score by keyword occurrences
  * POSITION_WEIGHT     — score by sentence position (first + last preferred)
  * TEXTRANK            — graph-based ranking (PageRank on Jaccard similarity)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

# --------------------------------------------------------------------------
# Stop words (small Eng+Rus list; stdlib only)
# --------------------------------------------------------------------------

_STOP_WORDS: frozenset[str] = frozenset(
    {
        # English
        "a", "an", "the", "and", "or", "but", "if", "then", "else", "of",
        "in", "on", "at", "to", "for", "with", "by", "from", "as", "is",
        "are", "was", "were", "be", "been", "being", "it", "its", "this",
        "that", "these", "those", "i", "you", "he", "she", "we", "they",
        "them", "his", "her", "our", "their", "my", "your", "me", "us",
        "do", "does", "did", "have", "has", "had", "not", "no", "so",
        "than", "too", "very", "can", "will", "just", "would", "could",
        "should", "may", "might", "must", "shall", "about", "into", "out",
        "up", "down", "over", "under", "again", "more", "most", "some",
        "any", "all", "each", "every", "such", "what", "which", "who",
        "whom", "whose", "where", "when", "why", "how", "there", "here",
        "also", "only", "own", "same", "other", "another",
        # Russian
        "и", "в", "во", "не", "что", "он", "она", "оно", "они", "на",
        "я", "с", "со", "как", "а", "то", "все", "она", "так", "его",
        "но", "да", "ты", "к", "у", "же", "вы", "за", "бы", "по", "от",
        "из", "о", "об", "это", "этот", "эта", "эти", "для", "при",
        "или", "ли", "до", "над", "под", "без", "был", "была", "было",
        "были", "быть", "есть", "был", "ещё", "уже", "только", "очень",
    }
)


# --------------------------------------------------------------------------
# Enums / Data classes
# --------------------------------------------------------------------------


class SummaryMethod(str, Enum):
    """Available summarization methods."""

    FIRST_N = "first_n"
    LAST_N = "last_n"
    LEAD_3 = "lead_3"
    KEYWORD_DENSITY = "keyword_density"
    POSITION_WEIGHT = "position_weight"
    TEXTRANK = "textrank"


@dataclass(frozen=True)
class SentenceScore:
    """Sentence with its original position and computed score."""

    sentence: str
    index: int
    score: float


@dataclass
class Summary:
    """Result of a summarization operation."""

    text: str
    sentences: list[str] = field(default_factory=list)
    method: SummaryMethod = SummaryMethod.LEAD_3
    original_length: int = 0
    summary_length: int = 0

    @property
    def compression_ratio(self) -> float:
        """Ratio of summary length to original length (0.0 if original empty)."""
        if self.original_length <= 0:
            return 0.0
        return self.summary_length / self.original_length


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------


_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
_WORD_RE = re.compile(r"[\w']+", re.UNICODE)


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences on punctuation boundary."""
    if not text or not text.strip():
        return []
    parts = _SENTENCE_SPLIT_RE.split(text.strip())
    return [p.strip() for p in parts if p.strip()]


def _tokenize(text: str) -> list[str]:
    """Lowercase word tokens."""
    return [w.lower() for w in _WORD_RE.findall(text)]


def _content_words(text: str) -> list[str]:
    """Tokens without stop words and pure-digit tokens."""
    return [w for w in _tokenize(text) if w not in _STOP_WORDS and not w.isdigit()]


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = a & b
    union = a | b
    if not union:
        return 0.0
    return len(inter) / len(union)


# --------------------------------------------------------------------------
# DocSummarizer
# --------------------------------------------------------------------------


class DocSummarizer:
    """Extractive summarizer supporting several heuristic methods."""

    # ----- main dispatch ---------------------------------------------------

    def summarize(
        self,
        text: str,
        method: SummaryMethod = SummaryMethod.LEAD_3,
        max_sentences: int = 3,
    ) -> Summary:
        """Dispatch to the appropriate method-specific function."""
        if method == SummaryMethod.FIRST_N:
            return self.summarize_first_n(text, n=max_sentences)
        if method == SummaryMethod.LAST_N:
            return self.summarize_last_n(text, n=max_sentences)
        if method == SummaryMethod.LEAD_3:
            return self.summarize_lead_3(text)
        if method == SummaryMethod.KEYWORD_DENSITY:
            return self.summarize_keyword_density(text, max_sentences=max_sentences)
        if method == SummaryMethod.POSITION_WEIGHT:
            return self.summarize_position_weight(text, max_sentences=max_sentences)
        if method == SummaryMethod.TEXTRANK:
            return self.summarize_textrank(text, max_sentences=max_sentences)
        raise ValueError(f"Unknown summary method: {method!r}")

    # ----- naive head / tail ----------------------------------------------

    def summarize_first_n(self, text: str, n: int = 3) -> Summary:
        sentences = _split_sentences(text)
        picked = sentences[: max(0, n)]
        return self._build_summary(text, sentences, picked, SummaryMethod.FIRST_N)

    def summarize_last_n(self, text: str, n: int = 3) -> Summary:
        sentences = _split_sentences(text)
        n = max(0, n)
        picked = sentences[-n:] if n > 0 else []
        return self._build_summary(text, sentences, picked, SummaryMethod.LAST_N)

    def summarize_lead_3(self, text: str) -> Summary:
        sentences = _split_sentences(text)
        picked = sentences[:3]
        return self._build_summary(text, sentences, picked, SummaryMethod.LEAD_3)

    # ----- keyword density -------------------------------------------------

    def summarize_keyword_density(self, text: str, max_sentences: int = 3) -> Summary:
        sentences = _split_sentences(text)
        if not sentences:
            return self._build_summary(text, sentences, [], SummaryMethod.KEYWORD_DENSITY)
        scores = self._score_keyword_density(sentences)
        picked = self.top_sentences(scores, max_sentences)
        return self._build_summary(text, sentences, picked, SummaryMethod.KEYWORD_DENSITY)

    # ----- position weight -------------------------------------------------

    def summarize_position_weight(self, text: str, max_sentences: int = 3) -> Summary:
        sentences = _split_sentences(text)
        if not sentences:
            return self._build_summary(text, sentences, [], SummaryMethod.POSITION_WEIGHT)
        scores = self._score_position_weight(sentences)
        picked = self.top_sentences(scores, max_sentences)
        return self._build_summary(text, sentences, picked, SummaryMethod.POSITION_WEIGHT)

    # ----- textrank --------------------------------------------------------

    def summarize_textrank(self, text: str, max_sentences: int = 3) -> Summary:
        sentences = _split_sentences(text)
        if not sentences:
            return self._build_summary(text, sentences, [], SummaryMethod.TEXTRANK)
        scores = self._score_textrank(sentences)
        picked = self.top_sentences(scores, max_sentences)
        return self._build_summary(text, sentences, picked, SummaryMethod.TEXTRANK)

    # ----- score_sentences -------------------------------------------------

    def score_sentences(self, text: str, method: SummaryMethod) -> list[SentenceScore]:
        """Return per-sentence scores for the given method."""
        sentences = _split_sentences(text)
        if not sentences:
            return []
        if method == SummaryMethod.FIRST_N:
            # Higher score = earlier position.
            n = len(sentences)
            return [
                SentenceScore(sentence=s, index=i, score=float(n - i))
                for i, s in enumerate(sentences)
            ]
        if method == SummaryMethod.LAST_N:
            return [
                SentenceScore(sentence=s, index=i, score=float(i + 1))
                for i, s in enumerate(sentences)
            ]
        if method == SummaryMethod.LEAD_3:
            return [
                SentenceScore(
                    sentence=s,
                    index=i,
                    score=1.0 if i < 3 else 0.0,
                )
                for i, s in enumerate(sentences)
            ]
        if method == SummaryMethod.KEYWORD_DENSITY:
            return self._score_keyword_density(sentences)
        if method == SummaryMethod.POSITION_WEIGHT:
            return self._score_position_weight(sentences)
        if method == SummaryMethod.TEXTRANK:
            return self._score_textrank(sentences)
        raise ValueError(f"Unknown summary method: {method!r}")

    # ----- top_sentences ---------------------------------------------------

    def top_sentences(self, scores: Iterable[SentenceScore], n: int) -> list[str]:
        """Pick top-n sentences by score, return them in original order."""
        scores_list = list(scores)
        if n <= 0 or not scores_list:
            return []
        # Sort by score desc, tie-break on index asc for stability.
        ranked = sorted(scores_list, key=lambda s: (-s.score, s.index))
        chosen = ranked[: min(n, len(ranked))]
        chosen.sort(key=lambda s: s.index)
        return [s.sentence for s in chosen]

    # ----- keywords --------------------------------------------------------

    def extract_keywords(self, text: str, top_k: int = 10) -> list[str]:
        """Return top-k content-word keywords by frequency."""
        if top_k <= 0:
            return []
        words = _content_words(text)
        if not words:
            return []
        freq: dict[str, int] = {}
        for w in words:
            freq[w] = freq.get(w, 0) + 1
        ranked = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
        return [w for w, _ in ranked[:top_k]]

    # ======================================================================
    # Internal scoring routines
    # ======================================================================

    def _score_keyword_density(self, sentences: list[str]) -> list[SentenceScore]:
        # Build keyword set from whole corpus (top by frequency).
        joined = " ".join(sentences)
        keywords = set(self.extract_keywords(joined, top_k=10))
        results: list[SentenceScore] = []
        for i, s in enumerate(sentences):
            tokens = _content_words(s)
            if not tokens:
                score = 0.0
            else:
                hits = sum(1 for t in tokens if t in keywords)
                score = hits / len(tokens)
            results.append(SentenceScore(sentence=s, index=i, score=score))
        return results

    def _score_position_weight(self, sentences: list[str]) -> list[SentenceScore]:
        total = len(sentences)
        results: list[SentenceScore] = []
        for i, s in enumerate(sentences):
            score = 1.0 / (i + 1) + 1.0 / (total - i)
            results.append(SentenceScore(sentence=s, index=i, score=score))
        return results

    def _score_textrank(
        self,
        sentences: list[str],
        *,
        iterations: int = 10,
        damping: float = 0.85,
    ) -> list[SentenceScore]:
        n = len(sentences)
        if n == 0:
            return []
        if n == 1:
            return [SentenceScore(sentence=sentences[0], index=0, score=1.0)]

        # Pre-compute sentence word sets (content words only).
        word_sets: list[set[str]] = [set(_content_words(s)) for s in sentences]

        # Similarity matrix (symmetric, zero diagonal).
        sim = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                w = _jaccard(word_sets[i], word_sets[j])
                sim[i][j] = w
                sim[j][i] = w

        # Out-weights for normalization.
        out_sum = [sum(row) for row in sim]

        scores = [1.0] * n
        for _ in range(iterations):
            new_scores = [0.0] * n
            for i in range(n):
                acc = 0.0
                for j in range(n):
                    if j == i or sim[j][i] == 0.0 or out_sum[j] == 0.0:
                        continue
                    acc += (sim[j][i] / out_sum[j]) * scores[j]
                new_scores[i] = (1.0 - damping) + damping * acc
            scores = new_scores

        return [
            SentenceScore(sentence=sentences[i], index=i, score=scores[i])
            for i in range(n)
        ]

    # ----- builder ---------------------------------------------------------

    def _build_summary(
        self,
        original: str,
        all_sentences: list[str],
        picked: list[str],
        method: SummaryMethod,
    ) -> Summary:
        text = " ".join(picked)
        return Summary(
            text=text,
            sentences=list(picked),
            method=method,
            original_length=len(original),
            summary_length=len(text),
        )
