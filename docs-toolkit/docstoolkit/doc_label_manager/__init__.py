"""E302 DocLabelManager — colored label management for documents.

Public API
----------
:class:`Label`            — a named label with color and description
:class:`DocLabels`        — labels assigned to a document
:class:`LabelStats`       — aggregate statistics
:class:`DocLabelManager`  — main interface for label CRUD and assignment
"""

from .manager import Label, DocLabels, LabelStats, DocLabelManager

__all__ = ["Label", "DocLabels", "LabelStats", "DocLabelManager"]
