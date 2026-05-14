"""E415 DocNamespaceStore implementation.

Pure-stdlib, thread-safe multi-namespace document organization. A document may
belong to at most one namespace; calling :meth:`DocNamespaceStore.add_doc` for a
document already in another namespace moves it.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Namespace:
    """A single namespace definition."""

    namespace_id: str
    name: str
    description: str = ""
    created_at: float = 0.0


@dataclass
class NamespaceStats:
    """Aggregate statistics across all namespaces."""

    total_namespaces: int
    total_docs: int
    avg_docs_per_namespace: float


class DocNamespaceStore:
    """Thread-safe store mapping documents to namespaces.

    A document belongs to at most one namespace. Namespaces are identified by
    their string ``namespace_id``.
    """

    def __init__(self) -> None:
        self._namespaces: dict[str, Namespace] = {}
        self._docs: dict[str, set[str]] = {}
        self._doc_namespace: dict[str, str] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ namespaces

    def create_namespace(
        self,
        namespace_id: str,
        name: str,
        description: str = "",
        now: Optional[float] = None,
    ) -> Namespace:
        """Create a new namespace.

        :raises ValueError: if ``namespace_id`` is empty or already exists.
        """
        if not namespace_id:
            raise ValueError("namespace_id must be non-empty")
        if not name:
            raise ValueError("name must be non-empty")
        ts = now if now is not None else time.time()
        with self._lock:
            if namespace_id in self._namespaces:
                raise ValueError(f"namespace already exists: {namespace_id}")
            ns = Namespace(
                namespace_id=namespace_id,
                name=name,
                description=description,
                created_at=ts,
            )
            self._namespaces[namespace_id] = ns
            self._docs[namespace_id] = set()
            return ns

    def delete_namespace(self, namespace_id: str) -> bool:
        """Delete a namespace and forget all its doc memberships."""
        with self._lock:
            if namespace_id not in self._namespaces:
                return False
            for doc_id in self._docs.get(namespace_id, set()):
                self._doc_namespace.pop(doc_id, None)
            self._docs.pop(namespace_id, None)
            self._namespaces.pop(namespace_id, None)
            return True

    def get_namespace(self, namespace_id: str) -> Optional[Namespace]:
        with self._lock:
            return self._namespaces.get(namespace_id)

    def list_namespaces(self) -> list[Namespace]:
        """Return all namespaces sorted by ``name``."""
        with self._lock:
            return sorted(self._namespaces.values(), key=lambda n: n.name)

    # ------------------------------------------------------------------ docs

    def add_doc(self, namespace_id: str, doc_id: str) -> bool:
        """Add ``doc_id`` to ``namespace_id``.

        Returns True when the document is newly added. If the document was in
        another namespace it is moved (returns False). Returns False if the
        document was already in the target namespace.

        :raises KeyError: if ``namespace_id`` does not exist.
        """
        with self._lock:
            if namespace_id not in self._namespaces:
                raise KeyError(f"unknown namespace: {namespace_id}")
            current = self._doc_namespace.get(doc_id)
            if current == namespace_id:
                return False
            if current is not None:
                self._docs[current].discard(doc_id)
            self._docs[namespace_id].add(doc_id)
            self._doc_namespace[doc_id] = namespace_id
            return current is None

    def remove_doc(self, namespace_id: str, doc_id: str) -> bool:
        """Remove ``doc_id`` from ``namespace_id``. Returns True if removed."""
        with self._lock:
            bucket = self._docs.get(namespace_id)
            if bucket is None or doc_id not in bucket:
                return False
            bucket.discard(doc_id)
            if self._doc_namespace.get(doc_id) == namespace_id:
                self._doc_namespace.pop(doc_id, None)
            return True

    def move_doc(self, doc_id: str, new_namespace_id: str) -> bool:
        """Move an existing document to ``new_namespace_id``.

        Returns True on success. Returns False if the document is not in any
        namespace yet.

        :raises KeyError: if ``new_namespace_id`` does not exist.
        """
        with self._lock:
            if new_namespace_id not in self._namespaces:
                raise KeyError(f"unknown namespace: {new_namespace_id}")
            current = self._doc_namespace.get(doc_id)
            if current is None:
                return False
            if current == new_namespace_id:
                return True
            self._docs[current].discard(doc_id)
            self._docs[new_namespace_id].add(doc_id)
            self._doc_namespace[doc_id] = new_namespace_id
            return True

    def namespace_of(self, doc_id: str) -> Optional[str]:
        with self._lock:
            return self._doc_namespace.get(doc_id)

    def docs_in_namespace(self, namespace_id: str) -> list[str]:
        """Return sorted doc ids in ``namespace_id`` (empty if unknown)."""
        with self._lock:
            return sorted(self._docs.get(namespace_id, set()))

    def doc_count_in(self, namespace_id: str) -> int:
        with self._lock:
            bucket = self._docs.get(namespace_id)
            return len(bucket) if bucket is not None else 0

    def all_doc_ids(self) -> list[str]:
        with self._lock:
            return sorted(self._doc_namespace.keys())

    def clear_namespace(self, namespace_id: str) -> int:
        """Remove all document memberships from ``namespace_id``.

        Returns the number of documents that were cleared. The namespace itself
        is preserved. Returns 0 if the namespace does not exist.
        """
        with self._lock:
            bucket = self._docs.get(namespace_id)
            if bucket is None:
                return 0
            count = len(bucket)
            for doc_id in list(bucket):
                if self._doc_namespace.get(doc_id) == namespace_id:
                    self._doc_namespace.pop(doc_id, None)
            bucket.clear()
            return count

    # ------------------------------------------------------------------ stats

    def stats(self) -> NamespaceStats:
        with self._lock:
            total_namespaces = len(self._namespaces)
            total_docs = len(self._doc_namespace)
            avg = (total_docs / total_namespaces) if total_namespaces else 0.0
            return NamespaceStats(
                total_namespaces=total_namespaces,
                total_docs=total_docs,
                avg_docs_per_namespace=avg,
            )
