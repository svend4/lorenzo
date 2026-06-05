"""DocSignatureStore — digital signature tracking for documents.

Provides a thread-safe, pure-stdlib store for managing signatures placed on
documents.  Signatures can be revoked, unrevoked, and queried by document or
signer.  No third-party dependencies required.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Signature:
    """A single signature on a document."""

    signature_id: str
    doc_id: str
    signer: str
    signature_value: str
    algorithm: str = "sha256"
    signed_at: float = 0.0
    revoked: bool = False
    metadata: dict = field(default_factory=dict)


@dataclass
class SignatureStats:
    """Aggregate statistics for a :class:`DocSignatureStore`."""

    total_signatures: int  # non-revoked
    revoked_count: int
    unique_docs: int
    unique_signers: int


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


class DocSignatureStore:
    """Thread-safe in-memory store for document signatures.

    All public methods are protected by a single :class:`threading.Lock`.
    The store is responsible for tracking metadata only — computing the actual
    cryptographic signature is the caller's responsibility.
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._signatures: dict[str, Signature] = {}
        self._by_doc: dict[str, list[str]] = {}
        self._by_signer: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return now if now is not None else time.time()

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def sign(
        self,
        doc_id: str,
        signer: str,
        signature_value: str,
        algorithm: str = "sha256",
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> Signature:
        """Record a new signature.  Returns the created :class:`Signature`."""
        sig_id = uuid.uuid4().hex
        ts = self._now(now)
        sig = Signature(
            signature_id=sig_id,
            doc_id=doc_id,
            signer=signer,
            signature_value=signature_value,
            algorithm=algorithm,
            signed_at=ts,
            revoked=False,
            metadata=dict(metadata) if metadata else {},
        )
        with self._lock:
            self._signatures[sig_id] = sig
            self._by_doc.setdefault(doc_id, []).append(sig_id)
            self._by_signer.setdefault(signer, []).append(sig_id)
        return sig

    def revoke(self, signature_id: str) -> bool:
        """Mark a signature as revoked.  Returns ``True`` if found."""
        with self._lock:
            sig = self._signatures.get(signature_id)
            if sig is None:
                return False
            sig.revoked = True
        return True

    def unrevoke(self, signature_id: str) -> bool:
        """Clear the revoked flag on a signature.  Returns ``True`` if found."""
        with self._lock:
            sig = self._signatures.get(signature_id)
            if sig is None:
                return False
            sig.revoked = False
        return True

    def delete(self, signature_id: str) -> bool:
        """Fully remove a signature from the store.  Returns ``True`` if existed."""
        with self._lock:
            sig = self._signatures.pop(signature_id, None)
            if sig is None:
                return False
            doc_ids = self._by_doc.get(sig.doc_id)
            if doc_ids is not None:
                try:
                    doc_ids.remove(signature_id)
                except ValueError:
                    pass
                if not doc_ids:
                    del self._by_doc[sig.doc_id]
            signer_ids = self._by_signer.get(sig.signer)
            if signer_ids is not None:
                try:
                    signer_ids.remove(signature_id)
                except ValueError:
                    pass
                if not signer_ids:
                    del self._by_signer[sig.signer]
        return True

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get(self, signature_id: str) -> Optional[Signature]:
        """Return the :class:`Signature` for *signature_id*, or ``None``."""
        with self._lock:
            return self._signatures.get(signature_id)

    def signatures_for_doc(
        self, doc_id: str, include_revoked: bool = False
    ) -> list[Signature]:
        """Return signatures on *doc_id*, sorted by ``signed_at`` ascending."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, ()))
            sigs = [self._signatures[i] for i in ids if i in self._signatures]
        if not include_revoked:
            sigs = [s for s in sigs if not s.revoked]
        return sorted(sigs, key=lambda s: s.signed_at)

    def signatures_by_signer(
        self, signer: str, include_revoked: bool = False
    ) -> list[Signature]:
        """Return signatures by *signer*, sorted by ``signed_at`` ascending."""
        with self._lock:
            ids = list(self._by_signer.get(signer, ()))
            sigs = [self._signatures[i] for i in ids if i in self._signatures]
        if not include_revoked:
            sigs = [s for s in sigs if not s.revoked]
        return sorted(sigs, key=lambda s: s.signed_at)

    def has_signed(self, signer: str, doc_id: str) -> bool:
        """Return ``True`` if *signer* has at least one non-revoked signature on *doc_id*."""
        with self._lock:
            ids = self._by_signer.get(signer, ())
            for i in ids:
                sig = self._signatures.get(i)
                if sig is not None and sig.doc_id == doc_id and not sig.revoked:
                    return True
        return False

    def signers_for_doc(self, doc_id: str) -> list[str]:
        """Return unique signers with non-revoked signatures on *doc_id*, sorted."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, ()))
            signers = {
                self._signatures[i].signer
                for i in ids
                if i in self._signatures and not self._signatures[i].revoked
            }
        return sorted(signers)

    def verify_count(self, doc_id: str) -> int:
        """Return the count of non-revoked signatures on *doc_id*."""
        with self._lock:
            ids = self._by_doc.get(doc_id, ())
            return sum(
                1
                for i in ids
                if i in self._signatures and not self._signatures[i].revoked
            )

    def all_doc_ids(self) -> list[str]:
        """Return a sorted list of all doc_ids that have at least one signature."""
        with self._lock:
            return sorted(self._by_doc.keys())

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> SignatureStats:
        """Return aggregate statistics about this store."""
        with self._lock:
            total = 0
            revoked = 0
            docs: set[str] = set()
            signers: set[str] = set()
            for sig in self._signatures.values():
                if sig.revoked:
                    revoked += 1
                else:
                    total += 1
                docs.add(sig.doc_id)
                signers.add(sig.signer)
        return SignatureStats(
            total_signatures=total,
            revoked_count=revoked,
            unique_docs=len(docs),
            unique_signers=len(signers),
        )
