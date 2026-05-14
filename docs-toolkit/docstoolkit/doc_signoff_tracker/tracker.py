"""E358 DocSignoffTracker — track sign-off acknowledgements per user/doc."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Signoff:
    """A single sign-off record."""

    doc_id: str
    user_id: str
    version: str = ""
    signed_at: float = 0.0
    revoked: bool = False
    note: str = ""


@dataclass
class SignoffStats:
    """Aggregate statistics over all sign-offs."""

    total_signoffs: int = 0
    revoked_count: int = 0
    unique_docs: int = 0
    unique_users: int = 0


class DocSignoffTracker:
    """Thread-safe tracker for per-user, per-doc sign-off acknowledgements."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._signoffs: Dict[Tuple[str, str], Signoff] = {}
        self._by_doc: Dict[str, Set[str]] = {}
        self._by_user: Dict[str, Set[str]] = {}

    # ----- mutation -----

    def sign_off(
        self,
        doc_id: str,
        user_id: str,
        version: str = "",
        note: str = "",
        now: Optional[float] = None,
    ) -> Signoff:
        """Create or replace a sign-off. Resets ``revoked`` to ``False``."""
        ts = time.time() if now is None else now
        signoff = Signoff(
            doc_id=doc_id,
            user_id=user_id,
            version=version,
            signed_at=ts,
            revoked=False,
            note=note,
        )
        with self._lock:
            self._signoffs[(doc_id, user_id)] = signoff
            self._by_doc.setdefault(doc_id, set()).add(user_id)
            self._by_user.setdefault(user_id, set()).add(doc_id)
        return signoff

    def revoke(self, doc_id: str, user_id: str) -> bool:
        """Mark an existing sign-off as revoked. Returns True if it existed."""
        with self._lock:
            existing = self._signoffs.get((doc_id, user_id))
            if existing is None:
                return False
            existing.revoked = True
            return True

    def unrevoke(self, doc_id: str, user_id: str) -> bool:
        """Clear the revoked flag on an existing sign-off."""
        with self._lock:
            existing = self._signoffs.get((doc_id, user_id))
            if existing is None:
                return False
            existing.revoked = False
            return True

    def delete(self, doc_id: str, user_id: str) -> bool:
        """Fully remove a sign-off record. Returns True if it existed."""
        with self._lock:
            return self._delete_locked(doc_id, user_id)

    def _delete_locked(self, doc_id: str, user_id: str) -> bool:
        if (doc_id, user_id) not in self._signoffs:
            return False
        del self._signoffs[(doc_id, user_id)]
        doc_users = self._by_doc.get(doc_id)
        if doc_users is not None:
            doc_users.discard(user_id)
            if not doc_users:
                del self._by_doc[doc_id]
        user_docs = self._by_user.get(user_id)
        if user_docs is not None:
            user_docs.discard(doc_id)
            if not user_docs:
                del self._by_user[user_id]
        return True

    # ----- queries -----

    def get(self, doc_id: str, user_id: str) -> Optional[Signoff]:
        """Return the sign-off if present, else ``None``."""
        with self._lock:
            return self._signoffs.get((doc_id, user_id))

    def has_signed_off(self, user_id: str, doc_id: str) -> bool:
        """Return True iff the user has a non-revoked sign-off for the doc."""
        with self._lock:
            existing = self._signoffs.get((doc_id, user_id))
            return existing is not None and not existing.revoked

    def signers_for_doc(
        self, doc_id: str, include_revoked: bool = False
    ) -> List[str]:
        """Return sorted user_ids that signed off this doc."""
        with self._lock:
            users = self._by_doc.get(doc_id, set())
            if include_revoked:
                return sorted(users)
            return sorted(
                u
                for u in users
                if not self._signoffs[(doc_id, u)].revoked
            )

    def docs_for_user(
        self, user_id: str, include_revoked: bool = False
    ) -> List[str]:
        """Return sorted doc_ids signed off by this user."""
        with self._lock:
            docs = self._by_user.get(user_id, set())
            if include_revoked:
                return sorted(docs)
            return sorted(
                d
                for d in docs
                if not self._signoffs[(d, user_id)].revoked
            )

    def signoff_count(self, doc_id: str) -> int:
        """Count of non-revoked sign-offs for the doc."""
        with self._lock:
            users = self._by_doc.get(doc_id, set())
            return sum(
                1
                for u in users
                if not self._signoffs[(doc_id, u)].revoked
            )

    def all_doc_ids(self) -> List[str]:
        """Sorted list of all doc_ids with any sign-off record."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def clear_doc(self, doc_id: str) -> int:
        """Remove all sign-offs for ``doc_id``. Returns the number removed."""
        with self._lock:
            users = list(self._by_doc.get(doc_id, set()))
            removed = 0
            for u in users:
                if self._delete_locked(doc_id, u):
                    removed += 1
            return removed

    def clear_user(self, user_id: str) -> int:
        """Remove all sign-offs for ``user_id``. Returns the number removed."""
        with self._lock:
            docs = list(self._by_user.get(user_id, set()))
            removed = 0
            for d in docs:
                if self._delete_locked(d, user_id):
                    removed += 1
            return removed

    def stats(self) -> SignoffStats:
        """Aggregate statistics over all stored sign-offs."""
        with self._lock:
            total = 0
            revoked = 0
            for s in self._signoffs.values():
                if s.revoked:
                    revoked += 1
                else:
                    total += 1
            return SignoffStats(
                total_signoffs=total,
                revoked_count=revoked,
                unique_docs=len(self._by_doc),
                unique_users=len(self._by_user),
            )
