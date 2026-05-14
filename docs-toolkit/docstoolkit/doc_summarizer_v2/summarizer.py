"""E285 Extractive summarizer using word-frequency + position weighting.

Algorithm summary
-----------------
1. Split text into sentences (on ``. ``, ``! ``, ``? ``, double newline).
2. Filter sentences shorter than ``min_sentence_len`` characters.
3. Build word-frequency map (lowercase, stopwords excluded).
4. Score each sentence:

   * ``freq_score  = sum(freq[w] for w in words) / max_freq / len(words)``
   * ``pos_score   = 1.0 / (1 + position)``  (first sentence → 1.0)
   * ``total_score = freq_weight * freq_score + position_weight * pos_score``

5. Select the top ``max_sentences`` by ``total_score``, preserving original order.
6. Join selected sentences with ``" "``.

All public methods are thread-safe via an internal ``threading.Lock``.
"""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

_SENTINEL: set[str] = set()  # used only as a default-factory placeholder


@dataclass
class SummaryConfig:
    """Configuration for :class:`DocSummarizerV2`."""

    max_sentences: int = 3
    min_sentence_len: int = 10          # characters
    position_weight: float = 0.3        # weight for position score
    freq_weight: float = 0.7            # weight for frequency score
    stopwords: set = field(default_factory=set)


@dataclass
class SentenceScore:
    """A single scored sentence."""

    sentence: str
    position: int           # 0-indexed original position in document
    freq_score: float       # normalised word-frequency score
    pos_score: float        # position score: 1.0 / (1 + position)
    total_score: float      # weighted combination


@dataclass
class Summary:
    """Result returned by :meth:`DocSummarizerV2.summarize`."""

    original_length: int            # word count of the original text
    summary_text: str
    sentences: list[SentenceScore]
    compression_ratio: float        # summary words / original words


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_SENTENCE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+|\n\n+')
_WORD_RE = re.compile(r'\b[a-zA-Zа-яА-ЯёЁ]+\b')


def _split_sentences(text: str, min_len: int) -> list[str]:
    """Split *text* into sentences and filter by minimum character length."""
    parts = _SENTENCE_SPLIT_RE.split(text.strip())
    return [s.strip() for s in parts if len(s.strip()) >= min_len]


def _tokenize(sentence: str, stopwords: set) -> list[str]:
    """Return lowercase word tokens from *sentence*, excluding *stopwords*."""
    words = _WORD_RE.findall(sentence.lower())
    return [w for w in words if w not in stopwords]


def _word_count(text: str) -> int:
    """Count whitespace-separated words in *text*."""
    return len(text.split()) if text.strip() else 0


# ---------------------------------------------------------------------------
# DocSummarizerV2
# ---------------------------------------------------------------------------


class DocSummarizerV2:
    """Extractive text summarizer using word-frequency + position weighting.

    Parameters
    ----------
    config:
        A :class:`SummaryConfig` instance.  Defaults to ``SummaryConfig()``.
    """

    def __init__(self, config: SummaryConfig | None = None) -> None:
        self._config: SummaryConfig = config if config is not None else SummaryConfig()
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def config(self) -> SummaryConfig:
        """Return a snapshot of the current configuration."""
        with self._lock:
            return SummaryConfig(
                max_sentences=self._config.max_sentences,
                min_sentence_len=self._config.min_sentence_len,
                position_weight=self._config.position_weight,
                freq_weight=self._config.freq_weight,
                stopwords=set(self._config.stopwords),
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def summarize(self, text: str) -> Summary:
        """Return an extractive :class:`Summary` of *text*.

        Raises
        ------
        TypeError
            If *text* is not a string.
        """
        if not isinstance(text, str):
            raise TypeError(f"text must be str, got {type(text).__name__!r}")

        with self._lock:
            cfg = SummaryConfig(
                max_sentences=self._config.max_sentences,
                min_sentence_len=self._config.min_sentence_len,
                position_weight=self._config.position_weight,
                freq_weight=self._config.freq_weight,
                stopwords=set(self._config.stopwords),
            )

        original_wc = _word_count(text)

        if not text.strip():
            return Summary(
                original_length=original_wc,
                summary_text="",
                sentences=[],
                compression_ratio=0.0,
            )

        sentences = _split_sentences(text, cfg.min_sentence_len)

        if not sentences:
            return Summary(
                original_length=original_wc,
                summary_text="",
                sentences=[],
                compression_ratio=0.0,
            )

        # Build per-sentence token lists
        token_lists: list[list[str]] = [
            _tokenize(s, cfg.stopwords) for s in sentences
        ]

        # Build global word-frequency map
        freq: dict[str, int] = {}
        for tokens in token_lists:
            for w in tokens:
                freq[w] = freq.get(w, 0) + 1

        max_freq: int = max(freq.values()) if freq else 1

        # Score each sentence
        scored: list[SentenceScore] = []
        for pos, (sentence, tokens) in enumerate(zip(sentences, token_lists)):
            pos_score = 1.0 / (1 + pos)

            if tokens and max_freq > 0:
                raw = sum(freq.get(w, 0) for w in tokens)
                freq_score = raw / max_freq / len(tokens)
            else:
                freq_score = 0.0

            total = cfg.freq_weight * freq_score + cfg.position_weight * pos_score

            scored.append(
                SentenceScore(
                    sentence=sentence,
                    position=pos,
                    freq_score=freq_score,
                    pos_score=pos_score,
                    total_score=total,
                )
            )

        # Select top-N by total_score, preserving original order
        ranked = sorted(scored, key=lambda ss: (-ss.total_score, ss.position))
        selected = ranked[: cfg.max_sentences]
        selected.sort(key=lambda ss: ss.position)

        summary_text = " ".join(ss.sentence for ss in selected)
        summary_wc = _word_count(summary_text)
        compression = summary_wc / original_wc if original_wc > 0 else 0.0

        return Summary(
            original_length=original_wc,
            summary_text=summary_text,
            sentences=selected,
            compression_ratio=compression,
        )

    def summarize_multi(self, texts: list[str]) -> list[Summary]:
        """Summarize each text in *texts* and return a list of :class:`Summary`."""
        return [self.summarize(t) for t in texts]

    def update_config(self, **kwargs: Any) -> SummaryConfig:
        """Update one or more config fields.  Returns the new config snapshot.

        Accepted keyword arguments mirror :class:`SummaryConfig` fields:
        ``max_sentences``, ``min_sentence_len``, ``position_weight``,
        ``freq_weight``, ``stopwords``.

        Raises
        ------
        ValueError
            If an unknown field name is passed.
        """
        valid = {"max_sentences", "min_sentence_len", "position_weight",
                 "freq_weight", "stopwords"}
        unknown = set(kwargs) - valid
        if unknown:
            raise ValueError(f"Unknown config fields: {unknown!r}")

        with self._lock:
            for k, v in kwargs.items():
                setattr(self._config, k, v)
            return SummaryConfig(
                max_sentences=self._config.max_sentences,
                min_sentence_len=self._config.min_sentence_len,
                position_weight=self._config.position_weight,
                freq_weight=self._config.freq_weight,
                stopwords=set(self._config.stopwords),
            )

    def add_stopwords(self, words: list[str]) -> int:
        """Add *words* to the stopwords set.  Returns the new total count."""
        with self._lock:
            self._config.stopwords.update(w.lower() for w in words)
            return len(self._config.stopwords)

    def clear_stopwords(self) -> None:
        """Remove all stopwords."""
        with self._lock:
            self._config.stopwords.clear()
