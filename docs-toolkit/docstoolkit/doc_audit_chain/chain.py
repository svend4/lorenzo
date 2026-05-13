"""E230 Doc Audit Chain — tamper-evident append-only audit log.

Cryptographic hash chain for document audit events with merkle-style
verification proofs. Pure stdlib: hashlib, threading, json.
"""
from __future__ import annotations

import hashlib
import json
import threading
from dataclasses import dataclass, field, asdict
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class AuditEntry:
    """A single tamper-evident audit log entry."""

    entry_id: int
    doc_id: str
    action: str
    actor: str
    payload: dict
    timestamp: float
    prev_hash: str
    entry_hash: str

    def to_dict(self) -> dict:
        """Return a JSON-serializable dict."""
        return asdict(self)


@dataclass
class VerificationResult:
    """Result of verifying a chain or a range of it."""

    valid: bool
    total_entries: int
    verified_count: int
    first_invalid_id: Optional[int]
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Proof:
    """Inclusion proof for a single audit entry."""

    entry_id: int
    entry_hash: str
    prev_hash: str
    position: int  # 1-based index in chain
    total_entries: int

    def to_dict(self) -> dict:
        return asdict(self)


# ---------------------------------------------------------------------------
# DocAuditChain
# ---------------------------------------------------------------------------


class DocAuditChain:
    """Append-only audit chain with SHA-256 hash linking and proofs."""

    def __init__(self, genesis_seed: str = "") -> None:
        self._genesis_seed = genesis_seed
        self._genesis_hash = hashlib.sha256(
            genesis_seed.encode("utf-8")
        ).hexdigest()
        self._entries: list[AuditEntry] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Hashing
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_hash(
        entry_id: int,
        doc_id: str,
        action: str,
        actor: str,
        payload: dict,
        timestamp: float,
        prev_hash: str,
    ) -> str:
        body = json.dumps(
            {
                "entry_id": entry_id,
                "doc_id": doc_id,
                "action": action,
                "actor": actor,
                "payload": payload,
                "timestamp": timestamp,
                "prev_hash": prev_hash,
            },
            sort_keys=True,
        )
        return hashlib.sha256(body.encode("utf-8")).hexdigest()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def genesis_hash(self) -> str:
        """SHA-256 of the genesis seed."""
        return self._genesis_hash

    @property
    def head_hash(self) -> Optional[str]:
        """Hash of the last entry, or None for empty chain."""
        with self._lock:
            if not self._entries:
                return None
            return self._entries[-1].entry_hash

    @property
    def total_entries(self) -> int:
        """Total number of entries in the chain."""
        with self._lock:
            return len(self._entries)

    # ------------------------------------------------------------------
    # Append
    # ------------------------------------------------------------------

    def append(
        self,
        doc_id: str,
        action: str,
        actor: str,
        payload: Optional[dict] = None,
        now: float = 0.0,
    ) -> AuditEntry:
        """Append a new entry to the chain."""
        if payload is None:
            payload = {}
        else:
            payload = dict(payload)

        with self._lock:
            entry_id = len(self._entries) + 1
            if not self._entries:
                prev_hash = self._genesis_hash
            else:
                prev_hash = self._entries[-1].entry_hash

            entry_hash = self._compute_hash(
                entry_id, doc_id, action, actor, payload, now, prev_hash
            )
            entry = AuditEntry(
                entry_id=entry_id,
                doc_id=doc_id,
                action=action,
                actor=actor,
                payload=payload,
                timestamp=now,
                prev_hash=prev_hash,
                entry_hash=entry_hash,
            )
            self._entries.append(entry)
            return entry

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get(self, entry_id: int) -> Optional[AuditEntry]:
        """Return the entry with *entry_id* (1-based)."""
        with self._lock:
            if entry_id < 1 or entry_id > len(self._entries):
                return None
            return self._entries[entry_id - 1]

    def entries_for_doc(
        self, doc_id: str, limit: Optional[int] = None
    ) -> list[AuditEntry]:
        """Return entries for a given doc_id (in append order)."""
        with self._lock:
            result = [e for e in self._entries if e.doc_id == doc_id]
        if limit is not None:
            result = result[:limit]
        return result

    def entries_by_actor(
        self, actor: str, limit: Optional[int] = None
    ) -> list[AuditEntry]:
        """Return entries by the given actor."""
        with self._lock:
            result = [e for e in self._entries if e.actor == actor]
        if limit is not None:
            result = result[:limit]
        return result

    def entries_by_action(
        self, action: str, limit: Optional[int] = None
    ) -> list[AuditEntry]:
        """Return entries with the given action."""
        with self._lock:
            result = [e for e in self._entries if e.action == action]
        if limit is not None:
            result = result[:limit]
        return result

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def verify(self) -> VerificationResult:
        """Verify the entire chain."""
        with self._lock:
            entries = list(self._entries)
        return self._verify_entries(entries, expected_first_prev=self._genesis_hash)

    def verify_range(self, start_id: int, end_id: int) -> VerificationResult:
        """Verify a range [start_id, end_id] (inclusive, 1-based)."""
        with self._lock:
            total = len(self._entries)
            if start_id < 1 or end_id < start_id or start_id > total:
                return VerificationResult(
                    valid=False,
                    total_entries=total,
                    verified_count=0,
                    first_invalid_id=None,
                    error="invalid range",
                )
            end = min(end_id, total)
            entries = list(self._entries[start_id - 1 : end])
            # Determine expected prev_hash for the first entry in range.
            if start_id == 1:
                expected_first_prev = self._genesis_hash
            else:
                expected_first_prev = self._entries[start_id - 2].entry_hash
        return self._verify_entries(entries, expected_first_prev=expected_first_prev)

    def _verify_entries(
        self,
        entries: list[AuditEntry],
        expected_first_prev: str,
    ) -> VerificationResult:
        total = len(entries)
        verified = 0
        prev_hash_expected = expected_first_prev
        for entry in entries:
            # Check prev_hash linkage
            if entry.prev_hash != prev_hash_expected:
                return VerificationResult(
                    valid=False,
                    total_entries=total,
                    verified_count=verified,
                    first_invalid_id=entry.entry_id,
                    error="prev_hash mismatch",
                )
            # Recompute hash
            recomputed = self._compute_hash(
                entry.entry_id,
                entry.doc_id,
                entry.action,
                entry.actor,
                entry.payload,
                entry.timestamp,
                entry.prev_hash,
            )
            if recomputed != entry.entry_hash:
                return VerificationResult(
                    valid=False,
                    total_entries=total,
                    verified_count=verified,
                    first_invalid_id=entry.entry_id,
                    error="entry_hash mismatch",
                )
            verified += 1
            prev_hash_expected = entry.entry_hash
        return VerificationResult(
            valid=True,
            total_entries=total,
            verified_count=verified,
            first_invalid_id=None,
            error=None,
        )

    # ------------------------------------------------------------------
    # Proofs
    # ------------------------------------------------------------------

    def proof(self, entry_id: int) -> Optional[Proof]:
        """Build an inclusion proof for *entry_id*."""
        with self._lock:
            total = len(self._entries)
            if entry_id < 1 or entry_id > total:
                return None
            entry = self._entries[entry_id - 1]
            return Proof(
                entry_id=entry.entry_id,
                entry_hash=entry.entry_hash,
                prev_hash=entry.prev_hash,
                position=entry_id,
                total_entries=total,
            )

    def verify_proof(self, proof: Proof) -> bool:
        """Verify a single-entry proof against the stored chain."""
        if proof is None:
            return False
        with self._lock:
            if proof.entry_id < 1 or proof.entry_id > len(self._entries):
                return False
            entry = self._entries[proof.entry_id - 1]
        if entry.entry_hash != proof.entry_hash:
            return False
        if entry.prev_hash != proof.prev_hash:
            return False
        if proof.position != proof.entry_id:
            return False
        # Recompute the entry hash to be sure.
        recomputed = self._compute_hash(
            entry.entry_id,
            entry.doc_id,
            entry.action,
            entry.actor,
            entry.payload,
            entry.timestamp,
            entry.prev_hash,
        )
        return recomputed == proof.entry_hash

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_json(self) -> str:
        """Serialize the entire chain as a JSON string."""
        with self._lock:
            payload = {
                "genesis_seed": self._genesis_seed,
                "genesis_hash": self._genesis_hash,
                "entries": [e.to_dict() for e in self._entries],
            }
        return json.dumps(payload, sort_keys=True)

    def from_json(self, json_str: str) -> bool:
        """Load chain from JSON. Verifies before installing; returns False on error."""
        try:
            data = json.loads(json_str)
        except (ValueError, TypeError):
            return False
        if not isinstance(data, dict):
            return False
        seed = data.get("genesis_seed", "")
        entries_raw = data.get("entries", [])
        if not isinstance(seed, str) or not isinstance(entries_raw, list):
            return False

        new_entries: list[AuditEntry] = []
        for raw in entries_raw:
            if not isinstance(raw, dict):
                return False
            try:
                entry = AuditEntry(
                    entry_id=int(raw["entry_id"]),
                    doc_id=str(raw["doc_id"]),
                    action=str(raw["action"]),
                    actor=str(raw["actor"]),
                    payload=dict(raw.get("payload") or {}),
                    timestamp=float(raw["timestamp"]),
                    prev_hash=str(raw["prev_hash"]),
                    entry_hash=str(raw["entry_hash"]),
                )
            except (KeyError, TypeError, ValueError):
                return False
            new_entries.append(entry)

        new_genesis_hash = hashlib.sha256(seed.encode("utf-8")).hexdigest()

        # Verify chain before installing
        result = self._verify_entries(
            new_entries, expected_first_prev=new_genesis_hash
        )
        if not result.valid:
            return False

        # Also ensure entry_ids are 1..N
        for idx, e in enumerate(new_entries, start=1):
            if e.entry_id != idx:
                return False

        with self._lock:
            self._genesis_seed = seed
            self._genesis_hash = new_genesis_hash
            self._entries = new_entries
        return True

    # ------------------------------------------------------------------
    # Misc
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove all entries (genesis seed is preserved)."""
        with self._lock:
            self._entries.clear()
