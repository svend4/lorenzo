"""E414 DocLabelFilter — filter documents by labels with set operations.

Public API
----------
:class:`LabelSet`        — set of labels for a doc
:class:`FilterStats`     — aggregate statistics
:class:`DocLabelFilter`  — main interface for label-based filtering
"""

from .filter import LabelSet, FilterStats, DocLabelFilter

__all__ = ["LabelSet", "FilterStats", "DocLabelFilter"]
