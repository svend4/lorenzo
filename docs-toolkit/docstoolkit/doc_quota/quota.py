"""DocQuota implementation — per-owner document storage quotas."""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


class QuotaError(Exception):
    """Raised on quota-related errors."""


@dataclass
class QuotaLimit:
    """Quota limits for an owner. None means unlimited."""

    owner_id: str
    max_docs: Optional[int] = None
    max_total_size: Optional[int] = None
    max_per_doc_size: Optional[int] = None
    max_tags: Optional[int] = None


@dataclass
class OwnerUsage:
    """Current usage for an owner."""

    owner_id: str
    doc_count: int = 0
    total_size: int = 0
    tag_count: int = 0
    updated_at: float = 0.0


@dataclass
class QuotaCheckResult:
    """Result of a check_add_doc call."""

    allowed: bool
    reason: Optional[str] = None
    remaining_docs: Optional[int] = None
    remaining_size: Optional[int] = None


# Sentinel default owner_id for the global default limit
_DEFAULT_LIMIT_KEY = "__default__"


class DocQuota:
    """Manages document quotas and usage per owner."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._limits: dict[str, QuotaLimit] = {}
        self._usages: dict[str, OwnerUsage] = {}
        self._default_limit: Optional[QuotaLimit] = None

    # ----- limit management -----

    def set_limit(
        self,
        owner_id: str,
        max_docs: Optional[int] = None,
        max_total_size: Optional[int] = None,
        max_per_doc_size: Optional[int] = None,
        max_tags: Optional[int] = None,
    ) -> QuotaLimit:
        with self._lock:
            limit = QuotaLimit(
                owner_id=owner_id,
                max_docs=max_docs,
                max_total_size=max_total_size,
                max_per_doc_size=max_per_doc_size,
                max_tags=max_tags,
            )
            self._limits[owner_id] = limit
            return limit

    def get_limit(self, owner_id: str) -> Optional[QuotaLimit]:
        with self._lock:
            return self._limits.get(owner_id)

    def set_default_limit(
        self,
        max_docs: Optional[int] = None,
        max_total_size: Optional[int] = None,
        max_per_doc_size: Optional[int] = None,
        max_tags: Optional[int] = None,
    ) -> QuotaLimit:
        with self._lock:
            limit = QuotaLimit(
                owner_id=_DEFAULT_LIMIT_KEY,
                max_docs=max_docs,
                max_total_size=max_total_size,
                max_per_doc_size=max_per_doc_size,
                max_tags=max_tags,
            )
            self._default_limit = limit
            return limit

    def _effective_limit(self, owner_id: str) -> Optional[QuotaLimit]:
        """Return the limit applicable to owner_id (specific or default)."""
        if owner_id in self._limits:
            return self._limits[owner_id]
        return self._default_limit

    # ----- usage queries -----

    def usage(self, owner_id: str) -> Optional[OwnerUsage]:
        with self._lock:
            return self._usages.get(owner_id)

    def _get_or_create_usage(self, owner_id: str) -> OwnerUsage:
        usage = self._usages.get(owner_id)
        if usage is None:
            usage = OwnerUsage(owner_id=owner_id)
            self._usages[owner_id] = usage
        return usage

    # ----- check -----

    def check_add_doc(
        self, owner_id: str, size: int, num_tags: int = 0
    ) -> QuotaCheckResult:
        with self._lock:
            limit = self._effective_limit(owner_id)
            usage = self._usages.get(owner_id)
            cur_docs = usage.doc_count if usage else 0
            cur_size = usage.total_size if usage else 0
            cur_tags = usage.tag_count if usage else 0

            if limit is None:
                return QuotaCheckResult(
                    allowed=True,
                    reason=None,
                    remaining_docs=None,
                    remaining_size=None,
                )

            # per-doc size check
            if (
                limit.max_per_doc_size is not None
                and size > limit.max_per_doc_size
            ):
                remaining_docs = (
                    (limit.max_docs - cur_docs)
                    if limit.max_docs is not None
                    else None
                )
                remaining_size = (
                    (limit.max_total_size - cur_size)
                    if limit.max_total_size is not None
                    else None
                )
                return QuotaCheckResult(
                    allowed=False,
                    reason=(
                        f"per-doc size {size} exceeds max_per_doc_size "
                        f"{limit.max_per_doc_size}"
                    ),
                    remaining_docs=remaining_docs,
                    remaining_size=remaining_size,
                )

            # max docs check
            if (
                limit.max_docs is not None
                and cur_docs + 1 > limit.max_docs
            ):
                remaining_size = (
                    (limit.max_total_size - cur_size)
                    if limit.max_total_size is not None
                    else None
                )
                return QuotaCheckResult(
                    allowed=False,
                    reason=(
                        f"doc count would exceed max_docs {limit.max_docs}"
                    ),
                    remaining_docs=0,
                    remaining_size=remaining_size,
                )

            # total size check
            if (
                limit.max_total_size is not None
                and cur_size + size > limit.max_total_size
            ):
                remaining_docs = (
                    (limit.max_docs - cur_docs)
                    if limit.max_docs is not None
                    else None
                )
                return QuotaCheckResult(
                    allowed=False,
                    reason=(
                        f"total size would exceed max_total_size "
                        f"{limit.max_total_size}"
                    ),
                    remaining_docs=remaining_docs,
                    remaining_size=max(0, limit.max_total_size - cur_size),
                )

            # tag count check
            if (
                limit.max_tags is not None
                and cur_tags + num_tags > limit.max_tags
            ):
                remaining_docs = (
                    (limit.max_docs - cur_docs)
                    if limit.max_docs is not None
                    else None
                )
                remaining_size = (
                    (limit.max_total_size - cur_size)
                    if limit.max_total_size is not None
                    else None
                )
                return QuotaCheckResult(
                    allowed=False,
                    reason=(
                        f"tag count would exceed max_tags {limit.max_tags}"
                    ),
                    remaining_docs=remaining_docs,
                    remaining_size=remaining_size,
                )

            remaining_docs = (
                (limit.max_docs - cur_docs - 1)
                if limit.max_docs is not None
                else None
            )
            remaining_size = (
                (limit.max_total_size - cur_size - size)
                if limit.max_total_size is not None
                else None
            )
            return QuotaCheckResult(
                allowed=True,
                reason=None,
                remaining_docs=remaining_docs,
                remaining_size=remaining_size,
            )

    # ----- record updates -----

    def record_add(
        self,
        owner_id: str,
        size: int,
        num_tags: int = 0,
        now: float = 0.0,
    ) -> OwnerUsage:
        with self._lock:
            usage = self._get_or_create_usage(owner_id)
            usage.doc_count += 1
            usage.total_size += size
            usage.tag_count += num_tags
            usage.updated_at = now
            return usage

    def record_remove(
        self,
        owner_id: str,
        size: int,
        num_tags: int = 0,
        now: float = 0.0,
    ) -> Optional[OwnerUsage]:
        with self._lock:
            usage = self._usages.get(owner_id)
            if usage is None:
                return None
            usage.doc_count = max(0, usage.doc_count - 1)
            usage.total_size = max(0, usage.total_size - size)
            usage.tag_count = max(0, usage.tag_count - num_tags)
            usage.updated_at = now
            return usage

    def record_resize(
        self,
        owner_id: str,
        delta_size: int,
        now: float = 0.0,
    ) -> Optional[OwnerUsage]:
        with self._lock:
            usage = self._usages.get(owner_id)
            if usage is None:
                return None
            usage.total_size = max(0, usage.total_size + delta_size)
            usage.updated_at = now
            return usage

    # ----- status queries -----

    def is_over_quota(self, owner_id: str) -> bool:
        with self._lock:
            limit = self._effective_limit(owner_id)
            usage = self._usages.get(owner_id)
            if limit is None or usage is None:
                return False
            if (
                limit.max_docs is not None
                and usage.doc_count > limit.max_docs
            ):
                return True
            if (
                limit.max_total_size is not None
                and usage.total_size > limit.max_total_size
            ):
                return True
            if (
                limit.max_tags is not None
                and usage.tag_count > limit.max_tags
            ):
                return True
            return False

    @property
    def total_owners(self) -> int:
        with self._lock:
            return len(
                set(self._limits.keys()) | set(self._usages.keys())
            )

    def cleanup(self, owner_id: str) -> bool:
        with self._lock:
            removed = False
            if owner_id in self._limits:
                del self._limits[owner_id]
                removed = True
            if owner_id in self._usages:
                del self._usages[owner_id]
                removed = True
            return removed

    def reset_usage(self, owner_id: str) -> bool:
        with self._lock:
            if owner_id not in self._usages:
                return False
            self._usages[owner_id] = OwnerUsage(owner_id=owner_id)
            return True

    def all_usages(self) -> list[OwnerUsage]:
        with self._lock:
            return list(self._usages.values())

    def owners_over_quota(self) -> list[str]:
        with self._lock:
            result: list[str] = []
            for owner_id, usage in self._usages.items():
                limit = self._effective_limit(owner_id)
                if limit is None:
                    continue
                over = False
                if (
                    limit.max_docs is not None
                    and usage.doc_count > limit.max_docs
                ):
                    over = True
                elif (
                    limit.max_total_size is not None
                    and usage.total_size > limit.max_total_size
                ):
                    over = True
                elif (
                    limit.max_tags is not None
                    and usage.tag_count > limit.max_tags
                ):
                    over = True
                if over:
                    result.append(owner_id)
            return result
