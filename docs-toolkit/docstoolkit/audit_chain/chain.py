"""E95 Audit chain: hash-linked append-only audit log with tamper detection."""
from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass, field, asdict
from typing import Optional
from uuid import uuid4


# ---------------------------------------------------------------------------
# AuditRecord
# ---------------------------------------------------------------------------


@dataclass
class AuditRecord:
    """A single record in the audit chain."""

    record_id: str = field(default_factory=lambda: uuid4().hex[:12])
    index: int = 0
    timestamp: float = field(default_factory=time.time)
    actor: str = ""
    action: str = ""
    resource: str = ""
    data: dict = field(default_factory=dict)
    prev_hash: str = ""
    hash: str = ""

    def to_dict(self) -> dict:
        """Return a JSON-serializable dict of this record."""
        return asdict(self)


# ---------------------------------------------------------------------------
# ChainStore — SQLite-backed persistence
# ---------------------------------------------------------------------------


class ChainStore:
    """Persist :class:`AuditRecord` rows in a SQLite database."""

    _CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS audit_chain (
        record_id TEXT PRIMARY KEY,
        idx       INTEGER UNIQUE,
        timestamp REAL,
        actor     TEXT,
        action    TEXT,
        resource  TEXT,
        data      TEXT,
        prev_hash TEXT,
        hash      TEXT
    )
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = str(db_path)
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(self._CREATE_TABLE)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_record(row: sqlite3.Row) -> AuditRecord:
        return AuditRecord(
            record_id=row["record_id"],
            index=row["idx"],
            timestamp=row["timestamp"],
            actor=row["actor"],
            action=row["action"],
            resource=row["resource"],
            data=json.loads(row["data"] or "{}"),
            prev_hash=row["prev_hash"],
            hash=row["hash"],
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def append(self, record: AuditRecord) -> None:
        """Persist *record* to the store."""
        self._conn.execute(
            """
            INSERT INTO audit_chain
                (record_id, idx, timestamp, actor, action, resource,
                 data, prev_hash, hash)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.record_id,
                record.index,
                record.timestamp,
                record.actor,
                record.action,
                record.resource,
                json.dumps(record.data, sort_keys=True),
                record.prev_hash,
                record.hash,
            ),
        )
        self._conn.commit()

    def get(self, record_id: str) -> Optional[AuditRecord]:
        """Return the record with *record_id*, or None if not found."""
        row = self._conn.execute(
            "SELECT * FROM audit_chain WHERE record_id = ?", (record_id,)
        ).fetchone()
        return self._row_to_record(row) if row else None

    def get_by_index(self, index: int) -> Optional[AuditRecord]:
        """Return the record at *index*, or None if not found."""
        row = self._conn.execute(
            "SELECT * FROM audit_chain WHERE idx = ?", (index,)
        ).fetchone()
        return self._row_to_record(row) if row else None

    def list(
        self,
        actor: Optional[str] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditRecord]:
        """Return records matching ALL supplied filters, ordered by index."""
        clauses: list[str] = []
        params: list = []

        if actor is not None:
            clauses.append("actor = ?")
            params.append(actor)
        if action is not None:
            clauses.append("action = ?")
            params.append(action)
        if resource is not None:
            clauses.append("resource = ?")
            params.append(resource)

        where = ("WHERE " + " AND ".join(clauses)) if clauses else ""
        params.append(limit)

        rows = self._conn.execute(
            f"SELECT * FROM audit_chain {where} ORDER BY idx ASC LIMIT ?",
            params,
        ).fetchall()
        return [self._row_to_record(r) for r in rows]

    def latest(self) -> Optional[AuditRecord]:
        """Return the record with the highest index, or None if store is empty."""
        row = self._conn.execute(
            "SELECT * FROM audit_chain ORDER BY idx DESC LIMIT 1"
        ).fetchone()
        return self._row_to_record(row) if row else None

    def count(self) -> int:
        """Return total number of records."""
        return self._conn.execute(
            "SELECT COUNT(*) FROM audit_chain"
        ).fetchone()[0]

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()


# ---------------------------------------------------------------------------
# AuditChain — hash-linked append + verification
# ---------------------------------------------------------------------------


class AuditChain:
    """Hash-linked append-only audit chain with tamper detection."""

    def __init__(self, store: Optional[ChainStore] = None) -> None:
        self._store = store if store is not None else ChainStore()

    # ------------------------------------------------------------------
    # Hashing
    # ------------------------------------------------------------------

    @staticmethod
    def _compute_hash(record: AuditRecord) -> str:
        """SHA-256 of ``index|timestamp|actor|action|resource|data|prev_hash``."""
        payload = "|".join(
            (
                str(record.index),
                repr(record.timestamp),
                record.actor,
                record.action,
                record.resource,
                json.dumps(record.data, sort_keys=True),
                record.prev_hash,
            )
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    # ------------------------------------------------------------------
    # Append
    # ------------------------------------------------------------------

    def append(
        self,
        actor: str,
        action: str,
        resource: str = "",
        data: Optional[dict] = None,
    ) -> AuditRecord:
        """Append a new record to the chain and return it."""
        latest = self._store.latest()
        if latest is None:
            new_index = 0
            prev_hash = ""
        else:
            new_index = latest.index + 1
            prev_hash = latest.hash

        record = AuditRecord(
            index=new_index,
            actor=actor,
            action=action,
            resource=resource,
            data=dict(data) if data is not None else {},
            prev_hash=prev_hash,
        )
        record.hash = self._compute_hash(record)
        self._store.append(record)
        return record

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    def verify(self) -> tuple[bool, list[int]]:
        """Walk the entire chain and report indices with mismatched hashes."""
        return self._verify_records(self._store.list(limit=10**9))

    def verify_range(self, start: int, end: int) -> tuple[bool, list[int]]:
        """Verify records with indices in ``[start, end]`` inclusive."""
        records: list[AuditRecord] = []
        for idx in range(start, end + 1):
            rec = self._store.get_by_index(idx)
            if rec is not None:
                records.append(rec)
        return self._verify_records(records)

    def _verify_records(
        self, records: list[AuditRecord]
    ) -> tuple[bool, list[int]]:
        bad: list[int] = []
        prev_record: Optional[AuditRecord] = None
        for rec in records:
            expected_hash = self._compute_hash(rec)
            mismatched = False
            if rec.hash != expected_hash:
                mismatched = True
            elif prev_record is not None and rec.prev_hash != prev_record.hash:
                mismatched = True
            if mismatched:
                bad.append(rec.index)
            prev_record = rec
        return (len(bad) == 0, bad)

    # ------------------------------------------------------------------
    # Pass-through helpers
    # ------------------------------------------------------------------

    def list(
        self,
        actor: Optional[str] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditRecord]:
        return self._store.list(
            actor=actor, action=action, resource=resource, limit=limit
        )

    def get(self, record_id: str) -> Optional[AuditRecord]:
        return self._store.get(record_id)

    def latest(self) -> Optional[AuditRecord]:
        return self._store.latest()

    def count(self) -> int:
        return self._store.count()

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------

    def export(self) -> list[dict]:
        """Return the entire chain as a list of serialized dicts."""
        return [r.to_dict() for r in self._store.list(limit=10**9)]
