"""SQLite feedback store + analytics."""
import json
import sqlite3
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from docstoolkit.config import load_config


SCHEMA = """
CREATE TABLE IF NOT EXISTS feedback (
    id TEXT PRIMARY KEY,
    request_id TEXT NOT NULL,
    request TEXT NOT NULL,
    response_text TEXT,
    thumbs TEXT,                    -- up | down | neutral | (null)
    rating INTEGER,                 -- 1-5
    comment TEXT,
    skill TEXT,
    retriever TEXT,
    answerer TEXT,
    citations_json TEXT,
    duration_ms INTEGER,
    cost REAL,
    ts TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_fb_skill ON feedback(skill);
CREATE INDEX IF NOT EXISTS idx_fb_thumbs ON feedback(thumbs);
CREATE INDEX IF NOT EXISTS idx_fb_ts ON feedback(ts);
"""


@dataclass
class Feedback:
    """Один feedback запись."""
    id: str = ""
    request_id: str = ""           # rag.ask request id (если есть)
    request: str = ""              # вопрос пользователя
    response_text: str = ""        # ответ
    thumbs: str = ""               # up | down | neutral | ""
    rating: int = 0                # 1-5 (опц.)
    comment: str = ""              # текстовый отзыв
    skill: str = ""                # rag | search | agent | manual
    retriever: str = ""            # keyword | semantic | hybrid
    answerer: str = ""             # echo | anthropic | etc.
    citations: list[dict] = field(default_factory=list)
    duration_ms: int = 0
    cost: float = 0.0
    ts: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = uuid.uuid4().hex[:12]
        if not self.ts:
            self.ts = datetime.now().isoformat(timespec='seconds')


class FeedbackStore:
    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "feedback.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    def record(self, fb: Feedback) -> str:
        self.conn.execute(
            "INSERT OR REPLACE INTO feedback "
            "(id, request_id, request, response_text, thumbs, rating, "
            " comment, skill, retriever, answerer, citations_json, "
            " duration_ms, cost, ts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                fb.id, fb.request_id, fb.request[:500], fb.response_text[:5000],
                fb.thumbs, fb.rating, fb.comment[:1000],
                fb.skill, fb.retriever, fb.answerer,
                json.dumps(fb.citations, ensure_ascii=False),
                fb.duration_ms, fb.cost, fb.ts,
            )
        )
        self.conn.commit()
        return fb.id

    def get(self, fb_id: str) -> Feedback | None:
        row = self.conn.execute(
            "SELECT * FROM feedback WHERE id = ?", (fb_id,)
        ).fetchone()
        if not row:
            return None
        return self._row_to_fb(row)

    def list_recent(self, limit: int = 50,
                    skill: str = "", thumbs: str = "") -> list[Feedback]:
        sql = "SELECT * FROM feedback WHERE 1=1"
        params: list = []
        if skill:
            sql += " AND skill = ?"
            params.append(skill)
        if thumbs:
            sql += " AND thumbs = ?"
            params.append(thumbs)
        sql += " ORDER BY ts DESC LIMIT ?"
        params.append(limit)
        return [self._row_to_fb(r) for r in self.conn.execute(sql, params).fetchall()]

    def aggregate_per_skill(self) -> dict[str, dict]:
        """Сводка по skill: total / up / down / quality."""
        result: dict[str, dict] = defaultdict(lambda: {
            "total": 0, "up": 0, "down": 0, "neutral": 0,
            "avg_rating": 0.0, "rating_count": 0,
            "avg_duration_ms": 0.0, "total_cost": 0.0,
        })

        for row in self.conn.execute("SELECT * FROM feedback"):
            skill = row["skill"] or "unknown"
            r = result[skill]
            r["total"] += 1
            if row["thumbs"] == "up":
                r["up"] += 1
            elif row["thumbs"] == "down":
                r["down"] += 1
            elif row["thumbs"]:
                r["neutral"] += 1
            if row["rating"]:
                r["avg_rating"] = (r["avg_rating"] * r["rating_count"] + row["rating"]) / (r["rating_count"] + 1)
                r["rating_count"] += 1
            if row["duration_ms"]:
                r["avg_duration_ms"] = (r["avg_duration_ms"] * (r["total"] - 1) + row["duration_ms"]) / r["total"]
            r["total_cost"] += row["cost"] or 0

        # Вычислим quality_score
        for skill, r in result.items():
            r["quality_score"] = self._calc_quality(r["up"], r["down"], r["total"])
        return dict(result)

    def quality_score(self, skill: str = "") -> float:
        """Wilson lower bound для (up vs total): даёт robust quality 0-100."""
        q = "SELECT thumbs FROM feedback WHERE thumbs IN ('up', 'down')"
        params: list = []
        if skill:
            q += " AND skill = ?"
            params.append(skill)
        rows = self.conn.execute(q, params).fetchall()
        up = sum(1 for r in rows if r["thumbs"] == "up")
        down = sum(1 for r in rows if r["thumbs"] == "down")
        return self._calc_quality(up, down, up + down)

    @staticmethod
    def _calc_quality(up: int, down: int, total: int) -> float:
        """Wilson confidence interval lower bound × 100."""
        if total == 0:
            return 0.0
        n = up + down
        if n == 0:
            return 50.0  # no signal
        p = up / n
        # Wilson lower bound, z=1.96 (95%)
        import math
        z = 1.96
        denom = 1 + z * z / n
        center = (p + z * z / (2 * n)) / denom
        margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
        return max(0.0, (center - margin) * 100)

    def _row_to_fb(self, row) -> Feedback:
        return Feedback(
            id=row["id"], request_id=row["request_id"],
            request=row["request"], response_text=row["response_text"] or "",
            thumbs=row["thumbs"] or "", rating=row["rating"] or 0,
            comment=row["comment"] or "",
            skill=row["skill"] or "", retriever=row["retriever"] or "",
            answerer=row["answerer"] or "",
            citations=json.loads(row["citations_json"] or "[]"),
            duration_ms=row["duration_ms"] or 0,
            cost=row["cost"] or 0.0,
            ts=row["ts"],
        )
