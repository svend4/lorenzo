"""E412 DocQuotaTracker — track usage against quotas per user/resource.

Public API
----------
:class:`QuotaDefinition`  — a defined quota
:class:`QuotaUsage`       — current usage for a key
:class:`QuotaStats`       — aggregate statistics
:class:`DocQuotaTracker`  — main interface for quota tracking
"""

from .tracker import QuotaDefinition, QuotaUsage, QuotaStats, DocQuotaTracker

__all__ = ["QuotaDefinition", "QuotaUsage", "QuotaStats", "DocQuotaTracker"]
