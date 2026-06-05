"""E386 DocSegmentLocator — locate segments by position within documents.

Public API
----------
:class:`Segment`         — a single segment with range
:class:`LocatorStats`    — aggregate statistics
:class:`DocSegmentLocator` — main interface for segment location
"""

from .locator import Segment, LocatorStats, DocSegmentLocator

__all__ = ["Segment", "LocatorStats", "DocSegmentLocator"]
