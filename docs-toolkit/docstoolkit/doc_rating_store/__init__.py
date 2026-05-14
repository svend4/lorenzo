"""E318 DocRatingStore — user ratings for documents with aggregate scoring.

Public API
----------
:class:`Rating`        — a single user rating for a document
:class:`RatingSummary` — aggregate rating summary for a document
:class:`RatingStats`   — global statistics
:class:`DocRatingStore` — main interface for rating management
"""

from .store import Rating, RatingSummary, RatingStats, DocRatingStore

__all__ = ["Rating", "RatingSummary", "RatingStats", "DocRatingStore"]
