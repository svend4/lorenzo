"""E430 DocStatusSummary — aggregate status summary across docs.

Public API
----------
:class:`StatusSnapshot`     — per-doc status at a point in time
:class:`SummaryReport`      — aggregate summary report
:class:`SummaryStats`       — aggregate statistics
:class:`DocStatusSummary`   — main interface for status summary
"""

from .summary import StatusSnapshot, SummaryReport, SummaryStats, DocStatusSummary

__all__ = ["StatusSnapshot", "SummaryReport", "SummaryStats", "DocStatusSummary"]
