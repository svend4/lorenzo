"""DocAclStore — thread-safe access control list store for documents."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AclEntry:
    """A single ACL entry binding a principal to a document with permissions."""

    doc_id: str
    principal: str
    permissions: list[str] = field(default_factory=list)
    granted_at: float = 0.0
    granted_by: str = ""


@dataclass
class AclStats:
    """Aggregate statistics for the ACL store."""

    total_entries: int
    unique_docs: int
    unique_principals: int


class DocAclStore:
    """Thread-safe in-memory ACL store keyed by (doc_id, principal)."""

    WILDCARD = "*"

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._entries: dict[tuple[str, str], AclEntry] = {}
        self._by_doc: dict[str, set[str]] = {}
        self._by_principal: dict[str, set[str]] = {}

    # ------------------------------------------------------------------ grant
    def grant(
        self,
        doc_id: str,
        principal: str,
        permissions: list[str],
        granted_by: str = "",
        now: Optional[float] = None,
    ) -> AclEntry:
        """Create or replace an ACL entry for (doc_id, principal)."""
        ts = now if now is not None else time.time()
        # Deduplicate while preserving order
        seen: set[str] = set()
        normalized_perms: list[str] = []
        for p in permissions:
            if p not in seen:
                seen.add(p)
                normalized_perms.append(p)
        entry = AclEntry(
            doc_id=doc_id,
            principal=principal,
            permissions=normalized_perms,
            granted_at=ts,
            granted_by=granted_by,
        )
        with self._lock:
            self._entries[(doc_id, principal)] = entry
            self._by_doc.setdefault(doc_id, set()).add(principal)
            self._by_principal.setdefault(principal, set()).add(doc_id)
        return entry

    # ----------------------------------------------------------------- revoke
    def revoke(self, doc_id: str, principal: str) -> bool:
        """Remove a single (doc_id, principal) entry. Return True if it existed."""
        with self._lock:
            return self._revoke_locked(doc_id, principal)

    def _revoke_locked(self, doc_id: str, principal: str) -> bool:
        key = (doc_id, principal)
        if key not in self._entries:
            return False
        del self._entries[key]
        doc_set = self._by_doc.get(doc_id)
        if doc_set is not None:
            doc_set.discard(principal)
            if not doc_set:
                del self._by_doc[doc_id]
        prin_set = self._by_principal.get(principal)
        if prin_set is not None:
            prin_set.discard(doc_id)
            if not prin_set:
                del self._by_principal[principal]
        return True

    def revoke_principal(self, principal: str) -> int:
        """Remove every entry for a principal. Return number removed."""
        with self._lock:
            docs = list(self._by_principal.get(principal, ()))
            count = 0
            for doc_id in docs:
                if self._revoke_locked(doc_id, principal):
                    count += 1
            return count

    def revoke_doc(self, doc_id: str) -> int:
        """Remove every entry for a document. Return number removed."""
        with self._lock:
            principals = list(self._by_doc.get(doc_id, ()))
            count = 0
            for principal in principals:
                if self._revoke_locked(doc_id, principal):
                    count += 1
            return count

    # ------------------------------------------------------------ permissions
    def add_permission(self, doc_id: str, principal: str, permission: str) -> bool:
        """Add a permission to an existing entry.

        Returns True only if the entry exists and the permission is newly added.
        Returns False if the entry does not exist or the permission was already present.
        """
        with self._lock:
            entry = self._entries.get((doc_id, principal))
            if entry is None:
                return False
            if permission in entry.permissions:
                return False
            entry.permissions.append(permission)
            return True

    def remove_permission(self, doc_id: str, principal: str, permission: str) -> bool:
        """Remove a permission from an existing entry.

        Returns True if the permission was present and removed, else False.
        """
        with self._lock:
            entry = self._entries.get((doc_id, principal))
            if entry is None:
                return False
            if permission not in entry.permissions:
                return False
            entry.permissions.remove(permission)
            return True

    # ----------------------------------------------------------------- lookup
    def get_entry(self, doc_id: str, principal: str) -> Optional[AclEntry]:
        """Return the ACL entry for (doc_id, principal) or None."""
        with self._lock:
            return self._entries.get((doc_id, principal))

    def has_permission(self, doc_id: str, principal: str, permission: str) -> bool:
        """Check if a principal has a permission, considering wildcard ``*``."""
        with self._lock:
            direct = self._entries.get((doc_id, principal))
            if direct is not None and permission in direct.permissions:
                return True
            if principal == self.WILDCARD:
                return False
            wildcard = self._entries.get((doc_id, self.WILDCARD))
            if wildcard is not None and permission in wildcard.permissions:
                return True
            return False

    def permissions_for(self, doc_id: str, principal: str) -> list[str]:
        """Sorted union of principal's perms and wildcard perms."""
        with self._lock:
            perms: set[str] = set()
            direct = self._entries.get((doc_id, principal))
            if direct is not None:
                perms.update(direct.permissions)
            if principal != self.WILDCARD:
                wildcard = self._entries.get((doc_id, self.WILDCARD))
                if wildcard is not None:
                    perms.update(wildcard.permissions)
            return sorted(perms)

    def principals_for(self, doc_id: str) -> list[AclEntry]:
        """All entries for a document, sorted by principal."""
        with self._lock:
            principals = sorted(self._by_doc.get(doc_id, ()))
            return [self._entries[(doc_id, p)] for p in principals]

    def docs_for_principal(self, principal: str) -> list[str]:
        """Sorted list of doc_ids the principal has entries for."""
        with self._lock:
            return sorted(self._by_principal.get(principal, ()))

    def principals_with_permission(self, doc_id: str, permission: str) -> list[str]:
        """Sorted principals (including ``*`` if granted) that have the permission."""
        with self._lock:
            result: list[str] = []
            for principal in self._by_doc.get(doc_id, ()):
                entry = self._entries.get((doc_id, principal))
                if entry is not None and permission in entry.permissions:
                    result.append(principal)
            return sorted(result)

    # ------------------------------------------------------------------ stats
    def stats(self) -> AclStats:
        """Return aggregate statistics."""
        with self._lock:
            return AclStats(
                total_entries=len(self._entries),
                unique_docs=len(self._by_doc),
                unique_principals=len(self._by_principal),
            )
