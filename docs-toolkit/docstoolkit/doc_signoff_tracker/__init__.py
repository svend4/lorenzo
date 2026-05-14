"""E358 DocSignoffTracker — track sign-off acknowledgements per user/doc.

Public API
----------
:class:`Signoff`           — a single sign-off record
:class:`SignoffStats`      — aggregate statistics
:class:`DocSignoffTracker` — main interface for sign-off tracking
"""

from .tracker import Signoff, SignoffStats, DocSignoffTracker

__all__ = ["Signoff", "SignoffStats", "DocSignoffTracker"]
