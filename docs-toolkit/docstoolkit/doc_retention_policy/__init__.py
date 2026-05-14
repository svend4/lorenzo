"""E299 DocRetentionPolicy — per-document retention rule management.

Public API
----------
:class:`RetentionRule`    — a single retention rule for a doc or pattern
:class:`RetentionResult`  — result of applying retention to a doc
:class:`PolicyStats`      — aggregate statistics for the policy store
:class:`DocRetentionPolicy` — main interface for retention rule CRUD and evaluation
"""

from .policy import RetentionRule, RetentionResult, PolicyStats, DocRetentionPolicy

__all__ = ["RetentionRule", "RetentionResult", "PolicyStats", "DocRetentionPolicy"]
