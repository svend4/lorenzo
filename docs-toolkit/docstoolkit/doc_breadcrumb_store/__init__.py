"""E357 DocBreadcrumbStore — navigation breadcrumb trail per user.

Public API
----------
:class:`Breadcrumb`        — a single breadcrumb entry
:class:`BreadcrumbStats`   — aggregate statistics
:class:`DocBreadcrumbStore` — main interface for breadcrumb management
"""

from .store import Breadcrumb, BreadcrumbStats, DocBreadcrumbStore

__all__ = ["Breadcrumb", "BreadcrumbStats", "DocBreadcrumbStore"]
