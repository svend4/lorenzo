"""E370 DocFreshnessScanner — document staleness/freshness analysis.

Public API
----------
:class:`FreshnessRecord`     — recorded last-touched timestamp for a doc
:class:`StaleDoc`            — doc identified as stale
:class:`FreshnessStats`      — aggregate statistics
:class:`DocFreshnessScanner` — main interface for freshness analysis
"""

from .scanner import FreshnessRecord, StaleDoc, FreshnessStats, DocFreshnessScanner

__all__ = ["FreshnessRecord", "StaleDoc", "FreshnessStats", "DocFreshnessScanner"]
