"""Document Quota module (E197).

Per-user/per-tenant document quotas (count, size, tags) with enforcement.

Usage:
    from docstoolkit.doc_quota import DocQuota

    dq = DocQuota()
    dq.set_limit("tenant:acme", max_docs=100, max_total_size=10_000_000)

    result = dq.check_add_doc("tenant:acme", size=2048, num_tags=3)
    if result.allowed:
        dq.record_add("tenant:acme", size=2048, num_tags=3)
"""
from docstoolkit.doc_quota.quota import (
    DocQuota,
    OwnerUsage,
    QuotaCheckResult,
    QuotaError,
    QuotaLimit,
)

__all__ = [
    "DocQuota",
    "OwnerUsage",
    "QuotaCheckResult",
    "QuotaError",
    "QuotaLimit",
]
