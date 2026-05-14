"""E395 DocRelevanceScore — query-document relevance scoring.

Public API
----------
:class:`RelevanceScore`   — a single relevance score
:class:`ScoringStats`     — aggregate statistics
:class:`DocRelevanceScore` — main interface for relevance scoring
"""

from .score import RelevanceScore, ScoringStats, DocRelevanceScore

__all__ = ["RelevanceScore", "ScoringStats", "DocRelevanceScore"]
