"""E82 API rate quota module.

Public API:
    QuotaPeriod, QuotaDefinition, QuotaUsage, QuotaExceeded — core types
    QuotaStore  — SQLite-backed counter storage
    QuotaManager — high-level registration + enforcement
"""
from docstoolkit.rate_quota.quota import (
    QuotaPeriod,
    QuotaDefinition,
    QuotaUsage,
    QuotaExceeded,
)
from docstoolkit.rate_quota.store import QuotaStore
from docstoolkit.rate_quota.manager import QuotaManager

__all__ = [
    "QuotaPeriod",
    "QuotaDefinition",
    "QuotaUsage",
    "QuotaExceeded",
    "QuotaStore",
    "QuotaManager",
]
