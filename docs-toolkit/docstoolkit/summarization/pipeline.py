"""Summarization pipeline — routes text through extractive/abstractive/hybrid."""
import re
from dataclasses import dataclass, field
from enum import Enum


class SummaryLevel(Enum):
    """Controls target sentence count for summarization."""
    BRIEF = "brief"        # 1-2 sentences
    STANDARD = "standard"  # 3-5 sentences
    DETAILED = "detailed"  # 5-10 sentences


# Map SummaryLevel → number of sentences to request
_LEVEL_SENTENCES: dict[SummaryLevel, int] = {
    SummaryLevel.BRIEF: 2,
    SummaryLevel.STANDARD: 3,
    SummaryLevel.DETAILED: 7,
}


@dataclass
class SummaryConfig:
    """Configuration for SummarizationPipeline."""
    level: SummaryLevel = SummaryLevel.STANDARD
    method: str = "extractive"   # "extractive" | "abstractive" | "hybrid"
    max_words: int = 200


@dataclass
class SummaryResult:
    """The result of a summarization run."""
    text: str
    method: str
    level: SummaryLevel
    word_count: int
    compression_ratio: float  # summary_words / original_words

    def is_brief(self) -> bool:
        """True when the result came from a BRIEF-level config."""
        return self.level == SummaryLevel.BRIEF


def _count_words(text: str) -> int:
    """Count whitespace-separated tokens."""
    return len(text.split()) if text.strip() else 0


def _truncate_to_words(text: str, max_words: int) -> str:
    """Return text truncated to at most max_words words."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words])


def _deduplicate_sentences(sentences: list[str]) -> list[str]:
    """Remove duplicate sentences while preserving order."""
    seen: set[str] = set()
    result: list[str] = []
    for s in sentences:
        key = s.strip().lower()
        if key not in seen:
            seen.add(key)
            result.append(s)
    return result


class SummarizationPipeline:
    """High-level pipeline: configure once, call summarize() for any text."""

    def __init__(self, config: SummaryConfig = None) -> None:
        self.config = config or SummaryConfig()

    # ------------------------------------------------------------------
    # Private routing helpers
    # ------------------------------------------------------------------

    def _run_extractive(self, text: str, n_sentences: int) -> str:
        from docstoolkit.summarization.extractor import ExtractiveSummarizer
        return ExtractiveSummarizer().summarize(text, n_sentences=n_sentences)

    def _run_abstractive(self, text: str) -> str:
        from docstoolkit.summarization.abstractive import AbstractiveSummarizer
        return AbstractiveSummarizer().summarize(text)

    def _run_hybrid(self, text: str, n_sentences: int) -> str:
        """Combine extractive and abstractive output, deduplicate sentences."""
        from docstoolkit.summarization.extractor import ExtractiveSummarizer
        from docstoolkit.summarization.abstractive import AbstractiveSummarizer

        extractive_text = ExtractiveSummarizer().summarize(text, n_sentences=n_sentences)
        abstractive_text = AbstractiveSummarizer().summarize(text)

        # Split both results into sentences and merge
        def split_sents(t: str) -> list[str]:
            parts = re.split(r"(?<=[.!?])\s+", t.strip())
            return [s.strip() for s in parts if s.strip()]

        combined = split_sents(extractive_text) + split_sents(abstractive_text)
        deduped = _deduplicate_sentences(combined)
        return " ".join(deduped)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def summarize(self, text: str) -> SummaryResult:
        """Summarize text according to the pipeline config."""
        original_words = _count_words(text)
        n_sentences = _LEVEL_SENTENCES[self.config.level]
        method = self.config.method

        if method == "extractive":
            summary = self._run_extractive(text, n_sentences)
        elif method == "abstractive":
            summary = self._run_abstractive(text)
        elif method == "hybrid":
            summary = self._run_hybrid(text, n_sentences)
        else:
            raise ValueError(f"Unknown summarization method: {method!r}")

        # Truncate to max_words
        summary = _truncate_to_words(summary, self.config.max_words)

        word_count = _count_words(summary)
        compression_ratio = word_count / original_words if original_words > 0 else 0.0

        return SummaryResult(
            text=summary,
            method=method,
            level=self.config.level,
            word_count=word_count,
            compression_ratio=compression_ratio,
        )
