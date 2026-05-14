"""E385 DocReviewAssignment — assign reviewers to documents.

Public API
----------
:class:`ReviewAssignment`    — a single review assignment
:class:`AssignmentStats`     — aggregate statistics
:class:`DocReviewAssignment` — main interface for review assignment
"""

from .assignment import ReviewAssignment, AssignmentStats, DocReviewAssignment

__all__ = ["ReviewAssignment", "AssignmentStats", "DocReviewAssignment"]
