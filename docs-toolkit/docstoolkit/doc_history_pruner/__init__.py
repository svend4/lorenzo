"""E379 DocHistoryPruner — manage and prune document version histories.

Public API
----------
:class:`HistoryVersion`   — a single retained version
:class:`PruneRule`        — a pruning rule (TTL or count-based)
:class:`PruneResult`      — outcome of a pruning operation
:class:`PrunerStats`      — aggregate statistics
:class:`DocHistoryPruner` — main interface for history pruning
"""

from .pruner import HistoryVersion, PruneRule, PruneResult, PrunerStats, DocHistoryPruner

__all__ = ["HistoryVersion", "PruneRule", "PruneResult", "PrunerStats", "DocHistoryPruner"]
