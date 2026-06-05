"""E305 DocQuotaManager — per-user and per-group document quota management.

Public API
----------
:class:`QuotaRule`      — a quota definition (limit + scope)
:class:`QuotaUsage`     — current usage snapshot for a subject
:class:`QuotaCheckResult` — result of a quota check
:class:`DocQuotaManager`  — main interface for quota CRUD and enforcement
"""

from .manager import QuotaRule, QuotaUsage, QuotaCheckResult, DocQuotaManager

__all__ = ["QuotaRule", "QuotaUsage", "QuotaCheckResult", "DocQuotaManager"]
