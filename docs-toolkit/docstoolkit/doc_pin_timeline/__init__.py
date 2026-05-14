"""E435 DocPinTimeline — time-bounded pinning of documents.

Public API
----------
:class:`TimedPin`         — a pinning entry with optional expiry
:class:`TimelineStats`    — aggregate statistics
:class:`DocPinTimeline`   — main interface for time-bounded pins
"""

from .timeline import TimedPin, TimelineStats, DocPinTimeline

__all__ = ["TimedPin", "TimelineStats", "DocPinTimeline"]
