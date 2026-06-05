"""E424 DocCapacityTracker — track capacity limits per resource bucket.

Public API
----------
:class:`CapacityBucket`     — a capacity bucket
:class:`CapacityCheck`      — outcome of a capacity check
:class:`CapacityStats`      — aggregate statistics
:class:`DocCapacityTracker` — main interface for capacity tracking
"""

from .tracker import CapacityBucket, CapacityCheck, CapacityStats, DocCapacityTracker

__all__ = ["CapacityBucket", "CapacityCheck", "CapacityStats", "DocCapacityTracker"]
