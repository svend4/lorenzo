"""E152 Document summarizer — extractive summarization with multiple algorithms.

Public API
----------
:class:`SummaryMethod`  — enum of summarization methods
:class:`SentenceScore`  — sentence with index and score
:class:`Summary`        — summary result dataclass
:class:`DocSummarizer`  — main summarizer class
"""
from .summarizer import (
    DocSummarizer,
    SentenceScore,
    Summary,
    SummaryMethod,
)

__all__ = [
    "DocSummarizer",
    "SentenceScore",
    "Summary",
    "SummaryMethod",
]
