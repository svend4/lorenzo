"""E391 DocOwnerRegistry — document ownership tracking implementation."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Ownership:
    """A single doc ownership record."""

    doc_id: str
    owner: str
    co_owners: list[str] = field(default_factory=list)
    assigned_at: float = 0.0
    transferred_from: Optional[str] = None


@dataclass
class OwnershipStats:
    """Aggregate ownership statistics."""

    total_docs: int
    unique_owners: int
    total_co_owners: int
    transferred_count: int


class DocOwnerRegistry:
    """Thread-safe registry tracking document ownership."""

    def __init__(self) -> None:
        self._ownership: dict[str, Ownership] = {}
        self._by_owner: dict[str, set[str]] = {}
        self._co_owner_index: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------
    def set_owner(
        self,
        doc_id: str,
        owner: str,
        now: Optional[float] = None,
    ) -> Ownership:
        """Set or replace primary owner; preserves co_owners."""
        ts = now if now is not None else time.time()
        with self._lock:
            existing = self._ownership.get(doc_id)
            transferred_from: Optional[str] = None
            co_owners: list[str] = []
            if existing is not None:
                co_owners = list(existing.co_owners)
                if existing.owner != owner:
                    transferred_from = existing.owner
                # Remove from previous owner's set
                prev_set = self._by_owner.get(existing.owner)
                if prev_set is not None:
                    prev_set.discard(doc_id)
                    if not prev_set:
                        del self._by_owner[existing.owner]

            # If new primary owner was a co-owner, drop them from co_owners
            if owner in co_owners:
                co_owners = [c for c in co_owners if c != owner]
                co_set = self._co_owner_index.get(owner)
                if co_set is not None:
                    co_set.discard(doc_id)
                    if not co_set:
                        del self._co_owner_index[owner]

            record = Ownership(
                doc_id=doc_id,
                owner=owner,
                co_owners=co_owners,
                assigned_at=ts,
                transferred_from=transferred_from,
            )
            self._ownership[doc_id] = record
            self._by_owner.setdefault(owner, set()).add(doc_id)
            return record

    def transfer_owner(
        self,
        doc_id: str,
        new_owner: str,
        now: Optional[float] = None,
    ) -> Optional[Ownership]:
        """Transfer ownership to a new owner. Returns None if doc not registered."""
        with self._lock:
            if doc_id not in self._ownership:
                return None
        return self.set_owner(doc_id, new_owner, now=now)

    def add_co_owner(self, doc_id: str, user_id: str) -> bool:
        """Add a co-owner. True if newly added."""
        with self._lock:
            record = self._ownership.get(doc_id)
            if record is None:
                return False
            if record.owner == user_id:
                return False
            if user_id in record.co_owners:
                return False
            record.co_owners.append(user_id)
            self._co_owner_index.setdefault(user_id, set()).add(doc_id)
            return True

    def remove_co_owner(self, doc_id: str, user_id: str) -> bool:
        """Remove a co-owner. True if removed."""
        with self._lock:
            record = self._ownership.get(doc_id)
            if record is None:
                return False
            if user_id not in record.co_owners:
                return False
            record.co_owners = [c for c in record.co_owners if c != user_id]
            co_set = self._co_owner_index.get(user_id)
            if co_set is not None:
                co_set.discard(doc_id)
                if not co_set:
                    del self._co_owner_index[user_id]
            return True

    def remove_owner(self, doc_id: str) -> bool:
        """Remove the entire ownership record. True if existed."""
        with self._lock:
            record = self._ownership.pop(doc_id, None)
            if record is None:
                return False
            owner_set = self._by_owner.get(record.owner)
            if owner_set is not None:
                owner_set.discard(doc_id)
                if not owner_set:
                    del self._by_owner[record.owner]
            for co in record.co_owners:
                co_set = self._co_owner_index.get(co)
                if co_set is not None:
                    co_set.discard(doc_id)
                    if not co_set:
                        del self._co_owner_index[co]
            return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def get_ownership(self, doc_id: str) -> Optional[Ownership]:
        with self._lock:
            return self._ownership.get(doc_id)

    def owner_of(self, doc_id: str) -> Optional[str]:
        with self._lock:
            record = self._ownership.get(doc_id)
            return record.owner if record is not None else None

    def docs_owned_by(self, user_id: str) -> list[str]:
        with self._lock:
            ids = self._by_owner.get(user_id, set())
            return sorted(ids)

    def docs_with_co_owner(self, user_id: str) -> list[str]:
        with self._lock:
            ids = self._co_owner_index.get(user_id, set())
            return sorted(ids)

    def docs_accessible_by(self, user_id: str) -> list[str]:
        with self._lock:
            primary = self._by_owner.get(user_id, set())
            co = self._co_owner_index.get(user_id, set())
            return sorted(primary | co)

    def is_owner(self, user_id: str, doc_id: str) -> bool:
        with self._lock:
            record = self._ownership.get(doc_id)
            return record is not None and record.owner == user_id

    def is_co_owner(self, user_id: str, doc_id: str) -> bool:
        """True if user is co-owner only (not primary)."""
        with self._lock:
            record = self._ownership.get(doc_id)
            if record is None:
                return False
            if record.owner == user_id:
                return False
            return user_id in record.co_owners

    def is_authorized(self, user_id: str, doc_id: str) -> bool:
        """True if user is primary owner or co-owner."""
        with self._lock:
            record = self._ownership.get(doc_id)
            if record is None:
                return False
            return record.owner == user_id or user_id in record.co_owners

    def transfer_history_count(self) -> int:
        with self._lock:
            return sum(
                1 for r in self._ownership.values() if r.transferred_from is not None
            )

    def all_doc_ids(self) -> list[str]:
        with self._lock:
            return sorted(self._ownership.keys())

    def stats(self) -> OwnershipStats:
        with self._lock:
            total_docs = len(self._ownership)
            unique_owners = len(self._by_owner)
            total_co_owners = sum(len(r.co_owners) for r in self._ownership.values())
            transferred = sum(
                1 for r in self._ownership.values() if r.transferred_from is not None
            )
            return OwnershipStats(
                total_docs=total_docs,
                unique_owners=unique_owners,
                total_co_owners=total_co_owners,
                transferred_count=transferred,
            )
