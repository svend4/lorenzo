"""Extractive summarization — pure stdlib, TF + position scoring."""
import re
from collections import Counter
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Stopwords (minimal English set)
# ---------------------------------------------------------------------------
_STOPWORDS: frozenset[str] = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "this", "that",
    "these", "those", "it", "its", "as", "if", "into", "up", "out",
    "not", "no", "nor", "so", "yet", "both", "either", "neither",
    "each", "every", "all", "any", "more", "most", "other", "such",
    "same", "than", "then", "there", "their", "they", "them", "we",
    "our", "you", "your", "he", "she", "his", "her", "my", "me",
    "who", "which", "what", "when", "where", "how", "just", "also",
    "about", "after", "before", "while", "during", "through", "over",
    "under", "between", "among", "against", "within", "without",
})


@dataclass
class SentenceScore:
    """A sentence paired with its position and computed score."""
    sentence: str
    position: int
    score: float


def _tokenize_words(text: str) -> list[str]:
    """Return lowercase word tokens from text."""
    return re.findall(r"[a-zA-Zа-яёА-ЯЁ]+", text.lower())


class ExtractiveSummarizer:
    """Score and select sentences by TF + position heuristics."""

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _tokenize_sentences(self, text: str) -> list[str]:
        """Split text into sentences on '. ', '! ', '? ', or '\\n\\n'."""
        # Split on double newlines first to preserve paragraph boundaries
        parts: list[str] = []
        for para in re.split(r"\n\n+", text):
            para = para.strip()
            if not para:
                continue
            # Split within paragraph on '. ' / '! ' / '? '
            sents = re.split(r"(?<=[.!?]) +", para)
            for s in sents:
                s = s.strip()
                if s:
                    parts.append(s)
        return parts

    def _build_word_freq(self, sentences: list[str]) -> dict[str, int]:
        """Count word frequencies across all sentences, ignoring stopwords."""
        counter: Counter = Counter()
        for s in sentences:
            for w in _tokenize_words(s):
                if w not in _STOPWORDS and len(w) >= 2:
                    counter[w] += 1
        return dict(counter)

    def _score_sentence(
        self,
        sentence: str,
        word_freq: dict[str, int],
        position: int,
        total: int,
    ) -> float:
        """Compute combined TF + position score for a single sentence.

        TF score  : sum(word_freq.get(w, 0) for w in tokens) / (len(tokens) + 1)
        Position  : 1.0 if first, 0.8 if last, 0.5 otherwise
        Combined  : 0.7 * tf_score + 0.3 * position_score
        """
        tokens = _tokenize_words(sentence)
        tf_score = sum(word_freq.get(w, 0) for w in tokens) / (len(tokens) + 1)

        if position == 0:
            position_score = 1.0
        elif position == total - 1:
            position_score = 0.8
        else:
            position_score = 0.5

        return 0.7 * tf_score + 0.3 * position_score

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def summarize(self, text: str, n_sentences: int = 3) -> str:
        """Return the top-n sentences in their original document order."""
        if not text or not text.strip():
            return ""

        sentences = self._tokenize_sentences(text)
        if not sentences:
            return ""

        if len(sentences) <= n_sentences:
            return " ".join(sentences)

        word_freq = self._build_word_freq(sentences)
        total = len(sentences)

        scored: list[tuple[float, int]] = []
        for i, s in enumerate(sentences):
            sc = self._score_sentence(s, word_freq, i, total)
            scored.append((sc, i))

        # Pick top-n by score
        top_indices = sorted(
            [idx for _, idx in sorted(scored, key=lambda x: -x[0])[:n_sentences]]
        )

        return " ".join(sentences[i] for i in top_indices)

    def key_sentences(self, text: str, n: int = 5) -> list[SentenceScore]:
        """Return top-n SentenceScore objects sorted by score descending."""
        if not text or not text.strip():
            return []

        sentences = self._tokenize_sentences(text)
        if not sentences:
            return []

        word_freq = self._build_word_freq(sentences)
        total = len(sentences)

        results: list[SentenceScore] = []
        for i, s in enumerate(sentences):
            sc = self._score_sentence(s, word_freq, i, total)
            results.append(SentenceScore(sentence=s, position=i, score=sc))

        results.sort(key=lambda x: -x.score)
        return results[:n]
