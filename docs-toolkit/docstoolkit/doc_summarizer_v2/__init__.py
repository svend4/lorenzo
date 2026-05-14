"""E285 DocSummarizerV2 — extractive text summarizer using sentence scoring.

Combines word-frequency and position weighting. Pure stdlib, no ML libs.

Public API
----------
:class:`SummaryConfig`   — configuration dataclass
:class:`SentenceScore`   — per-sentence scoring result
:class:`Summary`         — full summary result
:class:`DocSummarizerV2` — main summarizer class
"""
from .summarizer import (
    DocSummarizerV2,
    SentenceScore,
    Summary,
    SummaryConfig,
)

__all__ = [
    "DocSummarizerV2",
    "SentenceScore",
    "Summary",
    "SummaryConfig",
]
