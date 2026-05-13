import json
import sqlite3
from pathlib import Path
from docstoolkit.feature_flags.flag import FeatureFlag, FlagStatus, RolloutStrategy

_SCHEMA = """
CREATE TABLE IF NOT EXISTS feature_flags (
    name TEXT PRIMARY KEY,
    status TEXT NOT NULL DEFAULT 'disabled',
    rollout_pct REAL NOT NULL DEFAULT 0.0,
    strategy TEXT NOT NULL DEFAULT 'none',
    allowlist_json TEXT NOT NULL DEFAULT '[]',
    description TEXT NOT NULL DEFAULT '',
    tags_json TEXT NOT NULL DEFAULT '[]'
);
"""

class FlagStore:
    """SQLite-backed feature flag store."""

    def __init__(self, db_path=None):
        self._path = str(db_path) if db_path else ":memory:"
        self._conn = sqlite3.connect(self._path)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(_SCHEMA)
        self._conn.commit()

    def save(self, flag: FeatureFlag) -> None:
        self._conn.execute(
            "INSERT OR REPLACE INTO feature_flags "
            "(name, status, rollout_pct, strategy, allowlist_json, description, tags_json) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (flag.name, flag.status.value, flag.rollout_pct, flag.strategy.value,
             json.dumps(flag.allowlist), flag.description, json.dumps(flag.tags)),
        )
        self._conn.commit()

    def get(self, name: str) -> FeatureFlag | None:
        row = self._conn.execute(
            "SELECT * FROM feature_flags WHERE name=?", (name,)
        ).fetchone()
        return self._row_to_flag(row) if row else None

    def list_flags(self, status: FlagStatus | None = None) -> list:
        if status:
            rows = self._conn.execute(
                "SELECT * FROM feature_flags WHERE status=? ORDER BY name",
                (status.value,)
            ).fetchall()
        else:
            rows = self._conn.execute(
                "SELECT * FROM feature_flags ORDER BY name"
            ).fetchall()
        return [self._row_to_flag(r) for r in rows]

    def delete(self, name: str) -> bool:
        cur = self._conn.execute(
            "DELETE FROM feature_flags WHERE name=?", (name,)
        )
        self._conn.commit()
        return cur.rowcount > 0

    def count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM feature_flags").fetchone()[0]

    def close(self):
        self._conn.close()

    def _row_to_flag(self, row) -> FeatureFlag:
        return FeatureFlag(
            name=row["name"],
            status=FlagStatus(row["status"]),
            rollout_pct=row["rollout_pct"],
            strategy=RolloutStrategy(row["strategy"]),
            allowlist=json.loads(row["allowlist_json"] or "[]"),
            description=row["description"],
            tags=json.loads(row["tags_json"] or "[]"),
        )
