"""E376 DocPriorityScore — weighted priority score for documents.

Public API
----------
:class:`ScoreFactor`     — a named weighted factor
:class:`PriorityScore`   — computed priority for a doc
:class:`PriorityStats`   — aggregate statistics
:class:`DocPriorityScore` — main interface for priority scoring
"""

from .score import ScoreFactor, PriorityScore, PriorityStats, DocPriorityScore

__all__ = ["ScoreFactor", "PriorityScore", "PriorityStats", "DocPriorityScore"]
