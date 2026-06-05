"""E206 DocAudit — audit trail manager with compliance categorization."""
from __future__ import annotations

import json
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class EventCategory(Enum):
    """High-level audit event category."""

    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    ADMINISTRATIVE = "administrative"
    SECURITY = "security"
    COMPLIANCE = "compliance"


class ComplianceTag(Enum):
    """Compliance regimes an event is relevant to."""

    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOX = "sox"
    PCI_DSS = "pci_dss"
    CCPA = "ccpa"
    GENERAL = "general"


class Severity(Enum):
    """Severity of an audit event."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class AuditEvent:
    """A single audit event."""

    event_id: int
    timestamp: float
    actor: str
    action: str
    resource: str
    category: EventCategory
    severity: Severity = Severity.LOW
    compliance_tags: set = field(default_factory=set)
    outcome: str = "success"
    details: dict = field(default_factory=dict)


@dataclass
class ComplianceReport:
    """A compliance-scoped report over a time window."""

    tag: ComplianceTag
    period_start: float
    period_end: float
    total_events: int
    by_category: dict
    by_severity: dict
    by_outcome: dict
    unique_actors: int


# ---------------------------------------------------------------------------
# DocAudit
# ---------------------------------------------------------------------------


class DocAudit:
    """SQLite-backed audit trail manager with categorization and compliance."""

    _CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS events (
        event_id           INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp          REAL NOT NULL,
        actor              TEXT NOT NULL,
        action             TEXT NOT NULL,
        resource           TEXT NOT NULL,
        category           TEXT NOT NULL,
        severity           TEXT NOT NULL,
        compliance_tags_json TEXT NOT NULL,
        outcome            TEXT NOT NULL,
        details_json       TEXT NOT NULL
    )
    """

    _CREATE_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_events_actor ON events(actor)",
        "CREATE INDEX IF NOT EXISTS idx_events_resource ON events(resource)",
        "CREATE INDEX IF NOT EXISTS idx_events_category ON events(category)",
        "CREATE INDEX IF NOT EXISTS idx_events_severity ON events(severity)",
        "CREATE INDEX IF NOT EXISTS idx_events_outcome ON events(outcome)",
        "CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)",
    ]

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = str(db_path)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute(self._CREATE_TABLE)
        for stmt in self._CREATE_INDEXES:
            self._conn.execute(stmt)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _row_to_event(row: sqlite3.Row) -> AuditEvent:
        tags_raw = json.loads(row["compliance_tags_json"] or "[]")
        tags = {ComplianceTag(t) for t in tags_raw}
        return AuditEvent(
            event_id=row["event_id"],
            timestamp=row["timestamp"],
            actor=row["actor"],
            action=row["action"],
            resource=row["resource"],
            category=EventCategory(row["category"]),
            severity=Severity(row["severity"]),
            compliance_tags=tags,
            outcome=row["outcome"],
            details=json.loads(row["details_json"] or "{}"),
        )

    @staticmethod
    def _now(now: float) -> float:
        return now if now else time.time()

    # ------------------------------------------------------------------
    # Writes
    # ------------------------------------------------------------------

    def log(
        self,
        actor: str,
        action: str,
        resource: str,
        category: EventCategory,
        severity: Severity = Severity.LOW,
        compliance_tags: set = None,
        outcome: str = "success",
        details: dict = None,
        now: float = 0.0,
    ) -> AuditEvent:
        """Append a new audit event and return the persisted instance."""
        ts = self._now(now)
        tags = set(compliance_tags) if compliance_tags else set()
        det = dict(details) if details else {}
        tags_json = json.dumps(sorted(t.value for t in tags))
        det_json = json.dumps(det, sort_keys=True, default=str)
        with self._lock:
            cur = self._conn.execute(
                """
                INSERT INTO events
                    (timestamp, actor, action, resource, category, severity,
                     compliance_tags_json, outcome, details_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    ts,
                    actor,
                    action,
                    resource,
                    category.value,
                    severity.value,
                    tags_json,
                    outcome,
                    det_json,
                ),
            )
            event_id = cur.lastrowid
            self._conn.commit()
        return AuditEvent(
            event_id=event_id,
            timestamp=ts,
            actor=actor,
            action=action,
            resource=resource,
            category=category,
            severity=severity,
            compliance_tags=tags,
            outcome=outcome,
            details=det,
        )

    # ------------------------------------------------------------------
    # Reads
    # ------------------------------------------------------------------

    def get(self, event_id: int) -> Optional[AuditEvent]:
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM events WHERE event_id = ?", (event_id,)
            ).fetchone()
        return self._row_to_event(row) if row else None

    def _query(self, where: str, params: tuple, limit: Optional[int]) -> list:
        sql = f"SELECT * FROM events WHERE {where} ORDER BY event_id ASC"
        if limit is not None:
            sql += " LIMIT ?"
            params = params + (limit,)
        with self._lock:
            rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_event(r) for r in rows]

    def events_by_actor(self, actor: str, limit: int = None) -> list:
        return self._query("actor = ?", (actor,), limit)

    def events_by_resource(self, resource: str, limit: int = None) -> list:
        return self._query("resource = ?", (resource,), limit)

    def events_by_category(
        self, category: EventCategory, limit: int = None
    ) -> list:
        return self._query("category = ?", (category.value,), limit)

    def events_by_severity(self, severity: Severity, limit: int = None) -> list:
        return self._query("severity = ?", (severity.value,), limit)

    def events_by_compliance_tag(
        self, tag: ComplianceTag, limit: int = None
    ) -> list:
        # Filter via JSON containment by scanning matching rows.
        # Tags are stored as JSON array of strings, e.g. ["gdpr", "hipaa"].
        sql = "SELECT * FROM events ORDER BY event_id ASC"
        with self._lock:
            rows = self._conn.execute(sql).fetchall()
        results = []
        for r in rows:
            arr = json.loads(r["compliance_tags_json"] or "[]")
            if tag.value in arr:
                results.append(self._row_to_event(r))
                if limit is not None and len(results) >= limit:
                    break
        return results

    def events_in_range(self, start: float, end: float) -> list:
        return self._query(
            "timestamp >= ? AND timestamp <= ?", (start, end), None
        )

    def failures(self, limit: int = None) -> list:
        return self._query("outcome != ?", ("success",), limit)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def compliance_report(
        self, tag: ComplianceTag, start: float, end: float
    ) -> ComplianceReport:
        sql = (
            "SELECT * FROM events WHERE timestamp >= ? AND timestamp <= ? "
            "ORDER BY event_id ASC"
        )
        with self._lock:
            rows = self._conn.execute(sql, (start, end)).fetchall()
        by_category: dict = {}
        by_severity: dict = {}
        by_outcome: dict = {}
        actors: set = set()
        total = 0
        for r in rows:
            arr = json.loads(r["compliance_tags_json"] or "[]")
            if tag.value not in arr:
                continue
            total += 1
            by_category[r["category"]] = by_category.get(r["category"], 0) + 1
            by_severity[r["severity"]] = by_severity.get(r["severity"], 0) + 1
            by_outcome[r["outcome"]] = by_outcome.get(r["outcome"], 0) + 1
            actors.add(r["actor"])
        return ComplianceReport(
            tag=tag,
            period_start=start,
            period_end=end,
            total_events=total,
            by_category=by_category,
            by_severity=by_severity,
            by_outcome=by_outcome,
            unique_actors=len(actors),
        )

    def count(
        self,
        actor: str = None,
        category: EventCategory = None,
        severity: Severity = None,
        outcome: str = None,
    ) -> int:
        clauses = []
        params: list = []
        if actor is not None:
            clauses.append("actor = ?")
            params.append(actor)
        if category is not None:
            clauses.append("category = ?")
            params.append(category.value)
        if severity is not None:
            clauses.append("severity = ?")
            params.append(severity.value)
        if outcome is not None:
            clauses.append("outcome = ?")
            params.append(outcome)
        sql = "SELECT COUNT(*) AS c FROM events"
        if clauses:
            sql += " WHERE " + " AND ".join(clauses)
        with self._lock:
            row = self._conn.execute(sql, tuple(params)).fetchone()
        return int(row["c"])

    def recent(self, limit: int = 10) -> list:
        sql = "SELECT * FROM events ORDER BY event_id DESC LIMIT ?"
        with self._lock:
            rows = self._conn.execute(sql, (limit,)).fetchall()
        return [self._row_to_event(r) for r in rows]

    @property
    def total_events(self) -> int:
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*) AS c FROM events"
            ).fetchone()
        return int(row["c"])

    def actors_count(self) -> int:
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(DISTINCT actor) AS c FROM events"
            ).fetchone()
        return int(row["c"])

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def purge_older_than(self, older_than: float, now: float = 0.0) -> int:
        """Delete events with timestamp < (now - older_than). Returns rows removed."""
        cutoff = self._now(now) - older_than
        with self._lock:
            cur = self._conn.execute(
                "DELETE FROM events WHERE timestamp < ?", (cutoff,)
            )
            removed = cur.rowcount
            self._conn.commit()
        return int(removed)

    def clear(self) -> None:
        with self._lock:
            self._conn.execute("DELETE FROM events")
            # Reset autoincrement counter so event_id restarts at 1.
            self._conn.execute(
                "DELETE FROM sqlite_sequence WHERE name = 'events'"
            )
            self._conn.commit()

    def close(self) -> None:
        with self._lock:
            try:
                self._conn.close()
            except Exception:
                pass
