"""E367 DocMilestoneTracker — milestone tracking for document deliverables.

Public API
----------
:class:`Milestone`           — a single milestone
:class:`MilestoneStats`      — aggregate statistics
:class:`DocMilestoneTracker` — main interface for milestone tracking
"""

from .tracker import Milestone, MilestoneStats, DocMilestoneTracker

__all__ = ["Milestone", "MilestoneStats", "DocMilestoneTracker"]
