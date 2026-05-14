"""E353 DocSegmentCache — keyed segment cache for partial document data.

Public API
----------
:class:`Segment`        — a single cached document segment
:class:`SegmentStats`   — aggregate statistics
:class:`DocSegmentCache` — main interface for segment cache management
"""

from .cache import Segment, SegmentStats, DocSegmentCache

__all__ = ["Segment", "SegmentStats", "DocSegmentCache"]
