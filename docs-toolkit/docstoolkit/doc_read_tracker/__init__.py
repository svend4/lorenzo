"""E307 DocReadTracker — track document read events per user.

Public API
----------
:class:`ReadEvent`      — a single read event record
:class:`ReadStats`      — aggregate read statistics for a document
:class:`DocReadTracker` — main interface for tracking reads
"""

from .tracker import ReadEvent, ReadStats, DocReadTracker

__all__ = ["ReadEvent", "ReadStats", "DocReadTracker"]
