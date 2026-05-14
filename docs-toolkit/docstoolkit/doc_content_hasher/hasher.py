"""Content-addressable hashing for documents (E286).

Provides configurable hashing (sha256/sha1/md5), deduplication detection,
and change tracking.  Pure stdlib, thread-safe.
"""

import hashlib
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


_SUPPORTED_ALGORITHMS = frozenset({"sha256", "sha1", "md5"})


@dataclass
class ContentHash:
    """Stored hash record for a single document."""

    doc_id: str
    algorithm: str       # "sha256", "sha1", "md5"
    digest: str          # hex digest
    content_len: int     # bytes (len of UTF-8 encoded content, or raw bytes)
    computed_at: float   # Unix timestamp


@dataclass
class ChangeRecord:
    """Record of a digest change for a document."""

    doc_id: str
    old_digest: str
    new_digest: str
    changed_at: float
    algorithm: str


@dataclass
class HasherStats:
    """Aggregate statistics for a DocContentHasher instance."""

    total_hashed: int                    # total hash_content / hash_bytes calls
    total_docs: int                      # unique doc_ids currently stored
    total_changes: int                   # total ChangeRecords accumulated
    algorithm_counts: dict               # algorithm -> number of hashes stored


def _compute_digest(data: bytes, algorithm: str) -> str:
    """Return hex digest of *data* using *algorithm*."""
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()


class DocContentHasher:
    """Content-addressable hasher with change tracking and deduplication.

    All public methods are thread-safe via an internal :class:`threading.Lock`.

    Parameters
    ----------
    default_algorithm:
        Algorithm used when no *algorithm* argument is supplied to a method.
        Must be one of "sha256", "sha1", "md5".
    """

    def __init__(self, default_algorithm: str = "sha256") -> None:
        if default_algorithm not in _SUPPORTED_ALGORITHMS:
            raise ValueError(
                f"Unsupported algorithm {default_algorithm!r}. "
                f"Choose from {sorted(_SUPPORTED_ALGORITHMS)}."
            )
        self._default_algorithm = default_algorithm
        # (doc_id, algorithm) -> ContentHash
        self._hashes: dict[tuple[str, str], ContentHash] = {}
        # doc_id -> list[ChangeRecord]
        self._changes: dict[str, list[ChangeRecord]] = {}
        self._total_hashed: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _resolve_algo(self, algorithm: Optional[str]) -> str:
        algo = algorithm if algorithm is not None else self._default_algorithm
        if algo not in _SUPPORTED_ALGORITHMS:
            raise ValueError(
                f"Unsupported algorithm {algo!r}. "
                f"Choose from {sorted(_SUPPORTED_ALGORITHMS)}."
            )
        return algo

    def _store(
        self,
        doc_id: str,
        data: bytes,
        algorithm: str,
        now: Optional[float],
    ) -> "ContentHash":
        """Core logic (must be called with lock held)."""
        ts = now if now is not None else time.time()
        algo = self._resolve_algo(algorithm)
        digest = _compute_digest(data, algo)
        content_len = len(data)

        key = (doc_id, algo)
        existing = self._hashes.get(key)
        if existing is not None and existing.digest != digest:
            record = ChangeRecord(
                doc_id=doc_id,
                old_digest=existing.digest,
                new_digest=digest,
                changed_at=ts,
                algorithm=algo,
            )
            self._changes.setdefault(doc_id, []).append(record)

        ch = ContentHash(
            doc_id=doc_id,
            algorithm=algo,
            digest=digest,
            content_len=content_len,
            computed_at=ts,
        )
        self._hashes[key] = ch
        self._total_hashed += 1
        return ch

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def hash_content(
        self,
        doc_id: str,
        content: str,
        algorithm: Optional[str] = None,
        now: Optional[float] = None,
    ) -> ContentHash:
        """Hash a text string and store the result.

        Parameters
        ----------
        doc_id:
            Unique identifier for the document.
        content:
            Text content to hash.
        algorithm:
            One of "sha256", "sha1", "md5".  Defaults to *default_algorithm*.
        now:
            Override the ``computed_at`` timestamp (useful for testing).

        Returns
        -------
        ContentHash
            The newly computed and stored hash record.
        """
        data = content.encode("utf-8")
        with self._lock:
            return self._store(doc_id, data, self._resolve_algo(algorithm), now)

    def hash_bytes(
        self,
        doc_id: str,
        data: bytes,
        algorithm: Optional[str] = None,
        now: Optional[float] = None,
    ) -> ContentHash:
        """Hash raw bytes and store the result.

        Parameters
        ----------
        doc_id:
            Unique identifier for the document.
        data:
            Raw bytes to hash.
        algorithm:
            One of "sha256", "sha1", "md5".  Defaults to *default_algorithm*.
        now:
            Override the ``computed_at`` timestamp.

        Returns
        -------
        ContentHash
            The newly computed and stored hash record.
        """
        with self._lock:
            return self._store(doc_id, data, self._resolve_algo(algorithm), now)

    def get_hash(
        self,
        doc_id: str,
        algorithm: Optional[str] = None,
    ) -> Optional[ContentHash]:
        """Return the stored hash for *doc_id*, or ``None`` if absent.

        Parameters
        ----------
        algorithm:
            Which hash slot to look up.  Defaults to *default_algorithm*.
        """
        with self._lock:
            algo = self._resolve_algo(algorithm)
            return self._hashes.get((doc_id, algo))

    def verify(
        self,
        doc_id: str,
        content: str,
        algorithm: Optional[str] = None,
    ) -> bool:
        """Return ``True`` if *content* hashes to the stored digest.

        Returns ``False`` when no hash is stored for *doc_id*.
        """
        with self._lock:
            algo = self._resolve_algo(algorithm)
            existing = self._hashes.get((doc_id, algo))
            if existing is None:
                return False
            return _compute_digest(content.encode("utf-8"), algo) == existing.digest

    def has_changed(
        self,
        doc_id: str,
        content: str,
        algorithm: Optional[str] = None,
    ) -> bool:
        """Return ``True`` if *content* differs from the stored digest.

        Returns ``False`` when no prior hash is stored (not considered changed).
        """
        with self._lock:
            algo = self._resolve_algo(algorithm)
            existing = self._hashes.get((doc_id, algo))
            if existing is None:
                return False
            return _compute_digest(content.encode("utf-8"), algo) != existing.digest

    def changes_for(self, doc_id: str) -> list:
        """Return all :class:`ChangeRecord` objects for *doc_id*, oldest first."""
        with self._lock:
            return list(self._changes.get(doc_id, []))

    def find_duplicates(self) -> dict:
        """Return a mapping of digest -> [doc_id, ...] for shared digests.

        Only digests held by more than one *doc_id* are included.  When a
        doc_id has hashes under multiple algorithms, each (digest, algorithm)
        pair is treated independently.
        """
        with self._lock:
            # Group by (algorithm, digest) -> set of doc_ids
            groups: dict[tuple[str, str], list[str]] = {}
            for (doc_id, algo), ch in self._hashes.items():
                key = (algo, ch.digest)
                groups.setdefault(key, []).append(doc_id)
            result: dict[str, list[str]] = {}
            for (algo, digest), doc_ids in groups.items():
                if len(doc_ids) > 1:
                    result[digest] = sorted(doc_ids)
            return result

    def delete(self, doc_id: str) -> bool:
        """Remove the stored hash(es) for *doc_id*.

        Removes hashes under all algorithms for the given *doc_id*.

        Returns
        -------
        bool
            ``True`` if at least one hash was removed, ``False`` otherwise.
        """
        with self._lock:
            keys = [k for k in self._hashes if k[0] == doc_id]
            if not keys:
                return False
            for k in keys:
                del self._hashes[k]
            # Keep change history — intentionally preserved after deletion
            return True

    def stats(self) -> HasherStats:
        """Return aggregate statistics for this hasher instance."""
        with self._lock:
            algo_counts: dict[str, int] = {}
            for (doc_id, algo) in self._hashes:
                algo_counts[algo] = algo_counts.get(algo, 0) + 1

            unique_docs = len({doc_id for (doc_id, _) in self._hashes})
            total_changes = sum(len(v) for v in self._changes.values())

            return HasherStats(
                total_hashed=self._total_hashed,
                total_docs=unique_docs,
                total_changes=total_changes,
                algorithm_counts=dict(algo_counts),
            )

    @property
    def total_docs(self) -> int:
        """Number of unique doc_ids currently stored."""
        with self._lock:
            return len({doc_id for (doc_id, _) in self._hashes})
