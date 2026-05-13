import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from docstoolkit.snapshot.capture import CapturedState

_SCHEMA = """
CREATE TABLE IF NOT EXISTS snapshots (
    snapshot_id TEXT PRIMARY KEY,
    ts TEXT NOT NULL,
    doc_count INTEGER NOT NULL,
    total_bytes INTEGER NOT NULL,
    state_json TEXT NOT NULL,
    label TEXT NOT NULL DEFAULT ''
);
"""


@dataclass
class SnapshotMeta:
    """Metadata for a stored snapshot."""
    snapshot_id: str
    ts: str
    doc_count: int
    total_bytes: int
    label: str = ""

    def size_kb(self) -> float:
        return self.total_bytes / 1024


class SnapshotStore:
    """SQLite-backed snapshot store."""

    def __init__(self, db_path: Path | str | None = None):
        if db_path is None:
            db_path = ":memory:"
        self._path = str(db_path)
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def save(self, state: CapturedState, label: str = "") -> None:
        """Store snapshot."""
        self._conn.execute(
            "INSERT OR REPLACE INTO snapshots "
            "(snapshot_id, ts, doc_count, total_bytes, state_json, label) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (state.snapshot_id, state.ts, state.doc_count, state.total_bytes,
             json.dumps(state.to_dict()), label),
        )
        self._conn.commit()

    def load(self, snapshot_id: str) -> CapturedState | None:
        """Load by snapshot_id."""
        row = self._conn.execute(
            "SELECT state_json FROM snapshots WHERE snapshot_id = ?",
            (snapshot_id,)
        ).fetchone()
        if not row:
            return None
        return CapturedState.from_dict(json.loads(row["state_json"]))

    def list_snapshots(self) -> list:
        """Return list[SnapshotMeta] ordered by ts desc."""
        rows = self._conn.execute(
            "SELECT snapshot_id, ts, doc_count, total_bytes, label "
            "FROM snapshots ORDER BY ts DESC"
        ).fetchall()
        return [
            SnapshotMeta(
                snapshot_id=r["snapshot_id"],
                ts=r["ts"],
                doc_count=r["doc_count"],
                total_bytes=r["total_bytes"],
                label=r["label"],
            )
            for r in rows
        ]

    def delete(self, snapshot_id: str) -> bool:
        """Delete snapshot. Returns True if found."""
        cur = self._conn.execute(
            "DELETE FROM snapshots WHERE snapshot_id = ?", (snapshot_id,)
        )
        self._conn.commit()
        return cur.rowcount > 0

    def count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM snapshots").fetchone()[0]

    def latest(self) -> CapturedState | None:
        """Return most recent snapshot."""
        row = self._conn.execute(
            "SELECT snapshot_id FROM snapshots ORDER BY ts DESC LIMIT 1"
        ).fetchone()
        if not row:
            return None
        return self.load(row["snapshot_id"])

    def close(self) -> None:
        self._conn.close()
