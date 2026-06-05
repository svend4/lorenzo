"""High-level SQLite document repository (E157)."""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RepoDocument:
    """A document stored in the repository."""

    doc_id: str
    title: str
    content: str
    tags: list[str] = field(default_factory=list)
    created_at: float = 0.0
    updated_at: float = 0.0
    metadata: dict = field(default_factory=dict)


@dataclass
class RepoStats:
    """Statistics about the repository state."""

    total_docs: int
    total_tags: int
    avg_doc_length: float
    most_used_tags: list[tuple[str, int]]
    oldest_doc_id: Optional[str]
    newest_doc_id: Optional[str]


@dataclass
class RepoConfig:
    """Configuration for DocRepository."""

    db_path: str = ":memory:"
    auto_timestamps: bool = True


class DocRepository:
    """SQLite-backed document repository with CRUD, tagging, query, and stats."""

    def __init__(self, config: Optional[RepoConfig] = None):
        self.config = config or RepoConfig()
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(
            self.config.db_path,
            check_same_thread=False,
        )
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS docs (
                    doc_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    metadata_json TEXT NOT NULL
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS doc_tags (
                    doc_id TEXT NOT NULL,
                    tag TEXT NOT NULL,
                    PRIMARY KEY (doc_id, tag),
                    FOREIGN KEY (doc_id) REFERENCES docs(doc_id) ON DELETE CASCADE
                )
                """
            )
            cur.execute("CREATE INDEX IF NOT EXISTS idx_doc_tags_tag ON doc_tags(tag)")
            self._conn.commit()

    # ----- internal helpers -----

    def _now(self, now: float) -> float:
        if now and now > 0.0:
            return now
        if self.config.auto_timestamps:
            return time.time()
        return 0.0

    def _row_to_doc(self, row: sqlite3.Row, tags: list[str]) -> RepoDocument:
        return RepoDocument(
            doc_id=row["doc_id"],
            title=row["title"],
            content=row["content"],
            tags=tags,
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            metadata=json.loads(row["metadata_json"]) if row["metadata_json"] else {},
        )

    def _get_tags(self, doc_id: str) -> list[str]:
        cur = self._conn.cursor()
        cur.execute(
            "SELECT tag FROM doc_tags WHERE doc_id = ? ORDER BY tag", (doc_id,)
        )
        return [r["tag"] for r in cur.fetchall()]

    def _doc_from_id(self, doc_id: str) -> Optional[RepoDocument]:
        cur = self._conn.cursor()
        cur.execute("SELECT * FROM docs WHERE doc_id = ?", (doc_id,))
        row = cur.fetchone()
        if not row:
            return None
        return self._row_to_doc(row, self._get_tags(doc_id))

    # ----- CRUD -----

    def create(
        self,
        doc_id: str,
        title: str,
        content: str,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict] = None,
        now: float = 0.0,
    ) -> RepoDocument:
        ts = self._now(now)
        tags = list(dict.fromkeys(tags or []))  # dedup preserve order
        metadata = metadata or {}
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                "INSERT INTO docs (doc_id, title, content, created_at, updated_at, metadata_json) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (doc_id, title, content, ts, ts, json.dumps(metadata)),
            )
            for tag in tags:
                cur.execute(
                    "INSERT OR IGNORE INTO doc_tags (doc_id, tag) VALUES (?, ?)",
                    (doc_id, tag),
                )
            self._conn.commit()
        return RepoDocument(
            doc_id=doc_id,
            title=title,
            content=content,
            tags=tags,
            created_at=ts,
            updated_at=ts,
            metadata=metadata,
        )

    def get(self, doc_id: str) -> Optional[RepoDocument]:
        with self._lock:
            return self._doc_from_id(doc_id)

    def update(
        self,
        doc_id: str,
        title: Optional[str] = None,
        content: Optional[str] = None,
        tags: Optional[list[str]] = None,
        metadata: Optional[dict] = None,
        now: float = 0.0,
    ) -> Optional[RepoDocument]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("SELECT * FROM docs WHERE doc_id = ?", (doc_id,))
            row = cur.fetchone()
            if not row:
                return None
            new_title = title if title is not None else row["title"]
            new_content = content if content is not None else row["content"]
            new_metadata = (
                metadata if metadata is not None else json.loads(row["metadata_json"])
            )
            ts = self._now(now)
            cur.execute(
                "UPDATE docs SET title = ?, content = ?, updated_at = ?, metadata_json = ? "
                "WHERE doc_id = ?",
                (new_title, new_content, ts, json.dumps(new_metadata), doc_id),
            )
            if tags is not None:
                cur.execute("DELETE FROM doc_tags WHERE doc_id = ?", (doc_id,))
                for tag in dict.fromkeys(tags):
                    cur.execute(
                        "INSERT OR IGNORE INTO doc_tags (doc_id, tag) VALUES (?, ?)",
                        (doc_id, tag),
                    )
            self._conn.commit()
            return self._doc_from_id(doc_id)

    def delete(self, doc_id: str) -> bool:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("DELETE FROM doc_tags WHERE doc_id = ?", (doc_id,))
            cur.execute("DELETE FROM docs WHERE doc_id = ?", (doc_id,))
            deleted = cur.rowcount > 0
            self._conn.commit()
            return deleted

    def exists(self, doc_id: str) -> bool:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("SELECT 1 FROM docs WHERE doc_id = ?", (doc_id,))
            return cur.fetchone() is not None

    # ----- listing & queries -----

    def list_all(
        self, limit: Optional[int] = None, offset: int = 0
    ) -> list[RepoDocument]:
        with self._lock:
            cur = self._conn.cursor()
            if limit is not None:
                cur.execute(
                    "SELECT * FROM docs ORDER BY created_at, doc_id LIMIT ? OFFSET ?",
                    (limit, offset),
                )
            else:
                cur.execute(
                    "SELECT * FROM docs ORDER BY created_at, doc_id LIMIT -1 OFFSET ?",
                    (offset,),
                )
            rows = cur.fetchall()
            return [self._row_to_doc(r, self._get_tags(r["doc_id"])) for r in rows]

    def find_by_tag(self, tag: str) -> list[RepoDocument]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                "SELECT d.* FROM docs d JOIN doc_tags t ON d.doc_id = t.doc_id "
                "WHERE t.tag = ? ORDER BY d.created_at, d.doc_id",
                (tag,),
            )
            rows = cur.fetchall()
            return [self._row_to_doc(r, self._get_tags(r["doc_id"])) for r in rows]

    def find_by_tags(
        self, tags: list[str], match_all: bool = False
    ) -> list[RepoDocument]:
        if not tags:
            return []
        with self._lock:
            cur = self._conn.cursor()
            placeholders = ",".join("?" for _ in tags)
            if match_all:
                cur.execute(
                    f"SELECT d.* FROM docs d JOIN doc_tags t ON d.doc_id = t.doc_id "
                    f"WHERE t.tag IN ({placeholders}) "
                    f"GROUP BY d.doc_id HAVING COUNT(DISTINCT t.tag) = ? "
                    f"ORDER BY d.created_at, d.doc_id",
                    (*tags, len(set(tags))),
                )
            else:
                cur.execute(
                    f"SELECT DISTINCT d.* FROM docs d JOIN doc_tags t ON d.doc_id = t.doc_id "
                    f"WHERE t.tag IN ({placeholders}) ORDER BY d.created_at, d.doc_id",
                    tuple(tags),
                )
            rows = cur.fetchall()
            return [self._row_to_doc(r, self._get_tags(r["doc_id"])) for r in rows]

    def find_by_title(self, query: str) -> list[RepoDocument]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                "SELECT * FROM docs WHERE LOWER(title) LIKE ? ORDER BY created_at, doc_id",
                (f"%{query.lower()}%",),
            )
            rows = cur.fetchall()
            return [self._row_to_doc(r, self._get_tags(r["doc_id"])) for r in rows]

    def find_by_content(self, query: str) -> list[RepoDocument]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                "SELECT * FROM docs WHERE LOWER(content) LIKE ? ORDER BY created_at, doc_id",
                (f"%{query.lower()}%",),
            )
            rows = cur.fetchall()
            return [self._row_to_doc(r, self._get_tags(r["doc_id"])) for r in rows]

    # ----- tagging -----

    def add_tag(self, doc_id: str, tag: str) -> bool:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("SELECT 1 FROM docs WHERE doc_id = ?", (doc_id,))
            if not cur.fetchone():
                return False
            cur.execute(
                "INSERT OR IGNORE INTO doc_tags (doc_id, tag) VALUES (?, ?)",
                (doc_id, tag),
            )
            inserted = cur.rowcount > 0
            self._conn.commit()
            return inserted

    def remove_tag(self, doc_id: str, tag: str) -> bool:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                "DELETE FROM doc_tags WHERE doc_id = ? AND tag = ?", (doc_id, tag)
            )
            removed = cur.rowcount > 0
            self._conn.commit()
            return removed

    def all_tags(self) -> list[str]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("SELECT DISTINCT tag FROM doc_tags ORDER BY tag")
            return [r["tag"] for r in cur.fetchall()]

    # ----- stats -----

    @property
    def count(self) -> int:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("SELECT COUNT(*) AS c FROM docs")
            return cur.fetchone()["c"]

    def stats(self) -> RepoStats:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("SELECT COUNT(*) AS c FROM docs")
            total_docs = cur.fetchone()["c"]
            cur.execute("SELECT COUNT(DISTINCT tag) AS c FROM doc_tags")
            total_tags = cur.fetchone()["c"]
            cur.execute(
                "SELECT AVG(LENGTH(content)) AS avg_len FROM docs"
            )
            row = cur.fetchone()
            avg_doc_length = float(row["avg_len"]) if row["avg_len"] is not None else 0.0
            cur.execute(
                "SELECT tag, COUNT(*) AS c FROM doc_tags "
                "GROUP BY tag ORDER BY c DESC, tag ASC LIMIT 10"
            )
            most_used_tags = [(r["tag"], r["c"]) for r in cur.fetchall()]
            cur.execute(
                "SELECT doc_id FROM docs ORDER BY created_at ASC, doc_id ASC LIMIT 1"
            )
            r = cur.fetchone()
            oldest_doc_id = r["doc_id"] if r else None
            cur.execute(
                "SELECT doc_id FROM docs ORDER BY created_at DESC, doc_id DESC LIMIT 1"
            )
            r = cur.fetchone()
            newest_doc_id = r["doc_id"] if r else None
            return RepoStats(
                total_docs=total_docs,
                total_tags=total_tags,
                avg_doc_length=avg_doc_length,
                most_used_tags=most_used_tags,
                oldest_doc_id=oldest_doc_id,
                newest_doc_id=newest_doc_id,
            )

    def close(self) -> None:
        with self._lock:
            self._conn.close()
