"""E428 DocLabelAlias — alias mapping for document labels.

Public API
----------
:class:`LabelAliasEntry`  — a single label alias entry
:class:`AliasStats`       — aggregate statistics
:class:`DocLabelAlias`    — main interface for label alias management
"""

from .alias import LabelAliasEntry, AliasStats, DocLabelAlias

__all__ = ["LabelAliasEntry", "AliasStats", "DocLabelAlias"]
