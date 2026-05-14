"""Active Learning Queue — SQLite-backed queue for human labelling.

Items are added automatically by triggers (low confidence, down-thumb,
golden mismatch) or manually.  Labelled items can be exported as a
YAML golden dataset compatible with GoldenSet / load_golden_from_yaml.
"""
import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from docstoolkit.config import load_config


SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id                TEXT PRIMARY KEY,
    query             TEXT NOT NULL,
    passages_json     TEXT NOT NULL,
    suggested_answer  TEXT NOT NULL,
    priority          REAL NOT NULL DEFAULT 0.5,
    reason            TEXT NOT NULL,
    status            TEXT NOT NULL DEFAULT 'pending',
    labelled_by       TEXT NOT NULL DEFAULT '',
    label_ts          TEXT NOT NULL DEFAULT '',
    golden_doc_ids_json TEXT NOT NULL DEFAULT '[]',
    created_ts        TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_al_status   ON items(status);
CREATE INDEX IF NOT EXISTS idx_al_priority ON items(priority DESC);
CREATE INDEX IF NOT EXISTS idx_al_reason   ON items(reason);
"""


@dataclass
class LearningItem:
    """One item waiting for (or already labelled by) a human annotator."""

    id: str
    query: str
    passages_json: str          # JSON list of {text, doc_id, score}
    suggested_answer: str
    priority: float             # 0-1
    reason: str                 # low_confidence | down_thumb | golden_mismatch | manual
    status: str = "pending"     # pending | labelled | skipped
    labelled_by: str = ""
    label_ts: str = ""
    golden_doc_ids: list[str] = field(default_factory=list)
    created_ts: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = uuid.uuid4().hex[:16]
        if not self.created_ts:
            self.created_ts = datetime.now().isoformat(timespec="seconds")

    # ---- convenience ----

    @property
    def passages(self) -> list[dict]:
        try:
            return json.loads(self.passages_json)
        except Exception:
            return []


class LearningQueue:
    """SQLite-backed active learning queue.

    Default DB location: <project_root>/.docstoolkit/active_learning.sqlite
    """

    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "active_learning.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    # ---- write ----

    def add(self, item: LearningItem) -> str:
        """Insert item; return its id."""
        self.conn.execute(
            """INSERT OR REPLACE INTO items
               (id, query, passages_json, suggested_answer, priority, reason,
                status, labelled_by, label_ts, golden_doc_ids_json, created_ts)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                item.id,
                item.query,
                item.passages_json,
                item.suggested_answer,
                item.priority,
                item.reason,
                item.status,
                item.labelled_by,
                item.label_ts,
                json.dumps(item.golden_doc_ids, ensure_ascii=False),
                item.created_ts,
            ),
        )
        self.conn.commit()
        return item.id

    def label(
        self,
        item_id: str,
        golden_doc_ids: list[str],
        labelled_by: str = "human",
    ) -> None:
        """Mark item as labelled with the given doc ids."""
        ts = datetime.now().isoformat(timespec="seconds")
        self.conn.execute(
            """UPDATE items
               SET status = 'labelled',
                   golden_doc_ids_json = ?,
                   labelled_by = ?,
                   label_ts = ?
               WHERE id = ?""",
            (json.dumps(golden_doc_ids, ensure_ascii=False), labelled_by, ts, item_id),
        )
        self.conn.commit()

    def skip(self, item_id: str) -> None:
        """Mark item as skipped."""
        self.conn.execute(
            "UPDATE items SET status = 'skipped' WHERE id = ?",
            (item_id,),
        )
        self.conn.commit()

    # ---- read ----

    def get(self, item_id: str) -> "LearningItem | None":
        row = self.conn.execute(
            "SELECT * FROM items WHERE id = ?", (item_id,)
        ).fetchone()
        return self._row_to_item(row) if row else None

    def list_pending(self, limit: int = 20) -> list[LearningItem]:
        rows = self.conn.execute(
            "SELECT * FROM items WHERE status = 'pending' "
            "ORDER BY priority DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [self._row_to_item(r) for r in rows]

    def list_labelled(self, limit: int = 200) -> list[LearningItem]:
        rows = self.conn.execute(
            "SELECT * FROM items WHERE status = 'labelled' "
            "ORDER BY label_ts DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [self._row_to_item(r) for r in rows]

    # ---- export ----

    def export_golden(self, output_path: Path) -> int:
        """Write labelled items to a YAML golden dataset.

        Format compatible with load_golden_from_yaml / GoldenSet:
            name: active-learning-export
            items:
              - query: "..."
                golden_doc_ids: [...]
                suggested_answer: "..."
        Returns number of items written.
        """
        items = self.list_labelled()
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lines = ["name: active-learning-export\n", "items:\n"]
        for item in items:
            q_escaped = item.query.replace('"', '\\"')
            lines.append(f'  - query: "{q_escaped}"\n')
            if item.golden_doc_ids:
                lines.append("    golden_doc_ids:\n")
                for doc_id in item.golden_doc_ids:
                    doc_escaped = doc_id.replace('"', '\\"')
                    lines.append(f'      - "{doc_escaped}"\n')
            else:
                lines.append("    golden_doc_ids: []\n")
            ans_escaped = item.suggested_answer.replace('"', '\\"')[:500]
            lines.append(f'    suggested_answer: "{ans_escaped}"\n')

        output_path.write_text("".join(lines), encoding="utf-8")
        return len(items)

    # ---- analytics ----

    def stats(self) -> dict:
        """Return {status: count, total: int, by_reason: {reason: count}}."""
        rows = self.conn.execute(
            "SELECT status, reason, COUNT(*) AS cnt FROM items "
            "GROUP BY status, reason"
        ).fetchall()

        status_counts: dict[str, int] = {}
        reason_counts: dict[str, int] = {}
        total = 0

        for row in rows:
            s, r, cnt = row["status"], row["reason"], row["cnt"]
            status_counts[s] = status_counts.get(s, 0) + cnt
            reason_counts[r] = reason_counts.get(r, 0) + cnt
            total += cnt

        return {
            **status_counts,
            "total": total,
            "by_reason": reason_counts,
        }

    # ---- internal ----

    @staticmethod
    def _row_to_item(row) -> LearningItem:
        return LearningItem(
            id=row["id"],
            query=row["query"],
            passages_json=row["passages_json"],
            suggested_answer=row["suggested_answer"],
            priority=row["priority"],
            reason=row["reason"],
            status=row["status"],
            labelled_by=row["labelled_by"] or "",
            label_ts=row["label_ts"] or "",
            golden_doc_ids=json.loads(row["golden_doc_ids_json"] or "[]"),
            created_ts=row["created_ts"],
        )
