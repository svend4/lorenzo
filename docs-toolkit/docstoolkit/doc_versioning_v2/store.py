"""VersionStore — SQLite-backed document version history with branches and tags."""
from __future__ import annotations

import difflib
import sqlite3
import threading
from dataclasses import dataclass
from typing import List, Optional

DEFAULT_BRANCH = "main"


@dataclass
class DocVersion:
    """A single committed version of a document."""

    version_id: int
    doc_id: str
    content: str
    created_at: float
    author: Optional[str] = None
    message: Optional[str] = None
    parent_id: Optional[int] = None


@dataclass
class Branch:
    """A named pointer to a head version."""

    name: str
    head_version: int
    created_at: float


@dataclass
class Tag:
    """A named pointer to a specific version."""

    name: str
    version_id: int
    created_at: float


class VersionStore:
    """SQLite-backed store of document versions, branches and tags.

    The store is thread-safe and supports both in-memory (``":memory:"``)
    and file-backed databases.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._db_path = db_path
        self._lock = threading.Lock()
        # check_same_thread=False so the same connection can be used from
        # multiple threads under our explicit lock.
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._closed = False
        self._init_schema()

    # ------------------------------------------------------------------ schema
    def _init_schema(self) -> None:
        with self._lock:
            cur = self._conn.cursor()
            cur.executescript(
                """
                CREATE TABLE IF NOT EXISTS versions (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    doc_id      TEXT NOT NULL,
                    content     TEXT NOT NULL,
                    created_at  REAL NOT NULL,
                    author      TEXT,
                    message     TEXT,
                    parent_id   INTEGER,
                    branch      TEXT NOT NULL DEFAULT 'main'
                );
                CREATE INDEX IF NOT EXISTS idx_versions_doc
                    ON versions(doc_id, branch);

                CREATE TABLE IF NOT EXISTS branches (
                    name          TEXT PRIMARY KEY,
                    head_version  INTEGER NOT NULL,
                    created_at    REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS tags (
                    name        TEXT PRIMARY KEY,
                    version_id  INTEGER NOT NULL,
                    created_at  REAL NOT NULL
                );
                """
            )
            self._conn.commit()

    # ------------------------------------------------------------------ helpers
    def _ensure_open(self) -> None:
        if self._closed:
            raise RuntimeError("VersionStore is closed")

    @staticmethod
    def _row_to_version(row: sqlite3.Row) -> DocVersion:
        return DocVersion(
            version_id=row["id"],
            doc_id=row["doc_id"],
            content=row["content"],
            created_at=row["created_at"],
            author=row["author"],
            message=row["message"],
            parent_id=row["parent_id"],
        )

    @staticmethod
    def _row_to_branch(row: sqlite3.Row) -> Branch:
        return Branch(
            name=row["name"],
            head_version=row["head_version"],
            created_at=row["created_at"],
        )

    @staticmethod
    def _row_to_tag(row: sqlite3.Row) -> Tag:
        return Tag(
            name=row["name"],
            version_id=row["version_id"],
            created_at=row["created_at"],
        )

    def _branch_exists(self, name: str) -> bool:
        cur = self._conn.execute(
            "SELECT 1 FROM branches WHERE name = ?", (name,)
        )
        return cur.fetchone() is not None

    def _ensure_main_branch(self, head_version: int, now: float) -> None:
        if not self._branch_exists(DEFAULT_BRANCH):
            self._conn.execute(
                "INSERT INTO branches(name, head_version, created_at) "
                "VALUES(?, ?, ?)",
                (DEFAULT_BRANCH, head_version, now),
            )

    # ------------------------------------------------------------------ commit
    def commit(
        self,
        doc_id: str,
        content: str,
        message: Optional[str] = None,
        author: Optional[str] = None,
        parent_id: Optional[int] = None,
        now: float = 0.0,
        branch: str = DEFAULT_BRANCH,
    ) -> DocVersion:
        """Store a new version on ``branch`` and advance its head."""
        self._ensure_open()
        with self._lock:
            # Resolve parent: if not given, use current head of branch for doc.
            if parent_id is None:
                cur = self._conn.execute(
                    "SELECT id FROM versions "
                    "WHERE doc_id = ? AND branch = ? "
                    "ORDER BY id DESC LIMIT 1",
                    (doc_id, branch),
                )
                row = cur.fetchone()
                if row is not None:
                    parent_id = row["id"]

            cur = self._conn.execute(
                "INSERT INTO versions(doc_id, content, created_at, author, "
                "message, parent_id, branch) VALUES(?, ?, ?, ?, ?, ?, ?)",
                (doc_id, content, now, author, message, parent_id, branch),
            )
            version_id = cur.lastrowid

            # Update branch head (auto-create branch if missing).
            if branch == DEFAULT_BRANCH and not self._branch_exists(branch):
                self._ensure_main_branch(version_id, now)
            else:
                if self._branch_exists(branch):
                    self._conn.execute(
                        "UPDATE branches SET head_version = ? WHERE name = ?",
                        (version_id, branch),
                    )
                elif branch == DEFAULT_BRANCH:
                    self._ensure_main_branch(version_id, now)
                # If branch was passed but doesn't exist and isn't "main",
                # we silently create it for robustness.
                else:
                    self._conn.execute(
                        "INSERT INTO branches(name, head_version, created_at) "
                        "VALUES(?, ?, ?)",
                        (branch, version_id, now),
                    )

            self._conn.commit()
            return DocVersion(
                version_id=version_id,
                doc_id=doc_id,
                content=content,
                created_at=now,
                author=author,
                message=message,
                parent_id=parent_id,
            )

    # ------------------------------------------------------------------ get
    def get(self, version_id: int) -> Optional[DocVersion]:
        self._ensure_open()
        with self._lock:
            cur = self._conn.execute(
                "SELECT * FROM versions WHERE id = ?", (version_id,)
            )
            row = cur.fetchone()
            return self._row_to_version(row) if row else None

    def get_current(
        self, doc_id: str, branch: str = DEFAULT_BRANCH
    ) -> Optional[DocVersion]:
        """Return the latest version of ``doc_id`` on ``branch``."""
        self._ensure_open()
        with self._lock:
            cur = self._conn.execute(
                "SELECT * FROM versions "
                "WHERE doc_id = ? AND branch = ? "
                "ORDER BY id DESC LIMIT 1",
                (doc_id, branch),
            )
            row = cur.fetchone()
            return self._row_to_version(row) if row else None

    # ------------------------------------------------------------------ history
    def history(
        self, doc_id: str, branch: str = DEFAULT_BRANCH
    ) -> List[DocVersion]:
        """Return all versions of ``doc_id`` on ``branch``, newest first."""
        self._ensure_open()
        with self._lock:
            cur = self._conn.execute(
                "SELECT * FROM versions "
                "WHERE doc_id = ? AND branch = ? "
                "ORDER BY id DESC",
                (doc_id, branch),
            )
            return [self._row_to_version(r) for r in cur.fetchall()]

    # ------------------------------------------------------------------ rollback
    def rollback(
        self,
        doc_id: str,
        version_id: int,
        branch: str = DEFAULT_BRANCH,
        now: float = 0.0,
    ) -> DocVersion:
        """Create a new commit that restores the content of ``version_id``."""
        self._ensure_open()
        target = self.get(version_id)
        if target is None:
            raise KeyError(f"Unknown version_id: {version_id}")
        if target.doc_id != doc_id:
            raise ValueError(
                f"Version {version_id} belongs to doc {target.doc_id!r}, "
                f"not {doc_id!r}"
            )
        return self.commit(
            doc_id=doc_id,
            content=target.content,
            message=f"Rollback to version {version_id}",
            author=target.author,
            now=now,
            branch=branch,
        )

    # ------------------------------------------------------------------ diff
    def diff(self, version_a: int, version_b: int) -> str:
        """Return a unified diff between two versions."""
        self._ensure_open()
        a = self.get(version_a)
        b = self.get(version_b)
        if a is None:
            raise KeyError(f"Unknown version_id: {version_a}")
        if b is None:
            raise KeyError(f"Unknown version_id: {version_b}")
        a_lines = a.content.splitlines(keepends=True)
        b_lines = b.content.splitlines(keepends=True)
        diff_iter = difflib.unified_diff(
            a_lines,
            b_lines,
            fromfile=f"version_{version_a}",
            tofile=f"version_{version_b}",
            lineterm="",
        )
        return "\n".join(line.rstrip("\n") for line in diff_iter)

    # ------------------------------------------------------------------ branches
    def create_branch(
        self, name: str, from_version: int, now: float = 0.0
    ) -> Branch:
        self._ensure_open()
        if not name:
            raise ValueError("Branch name must be non-empty")
        with self._lock:
            if self._branch_exists(name):
                raise ValueError(f"Branch already exists: {name}")
            cur = self._conn.execute(
                "SELECT 1 FROM versions WHERE id = ?", (from_version,)
            )
            if cur.fetchone() is None:
                raise KeyError(f"Unknown version_id: {from_version}")
            self._conn.execute(
                "INSERT INTO branches(name, head_version, created_at) "
                "VALUES(?, ?, ?)",
                (name, from_version, now),
            )
            self._conn.commit()
            return Branch(name=name, head_version=from_version, created_at=now)

    def list_branches(self) -> List[Branch]:
        self._ensure_open()
        with self._lock:
            cur = self._conn.execute(
                "SELECT * FROM branches ORDER BY created_at, name"
            )
            return [self._row_to_branch(r) for r in cur.fetchall()]

    def delete_branch(self, name: str) -> bool:
        self._ensure_open()
        if name == DEFAULT_BRANCH:
            raise ValueError("Cannot delete the 'main' branch")
        with self._lock:
            cur = self._conn.execute(
                "DELETE FROM branches WHERE name = ?", (name,)
            )
            self._conn.commit()
            return cur.rowcount > 0

    # ------------------------------------------------------------------ tags
    def tag(self, name: str, version_id: int, now: float = 0.0) -> Tag:
        self._ensure_open()
        if not name:
            raise ValueError("Tag name must be non-empty")
        with self._lock:
            cur = self._conn.execute(
                "SELECT 1 FROM versions WHERE id = ?", (version_id,)
            )
            if cur.fetchone() is None:
                raise KeyError(f"Unknown version_id: {version_id}")
            cur = self._conn.execute(
                "SELECT 1 FROM tags WHERE name = ?", (name,)
            )
            if cur.fetchone() is not None:
                raise ValueError(f"Tag already exists: {name}")
            self._conn.execute(
                "INSERT INTO tags(name, version_id, created_at) "
                "VALUES(?, ?, ?)",
                (name, version_id, now),
            )
            self._conn.commit()
            return Tag(name=name, version_id=version_id, created_at=now)

    def list_tags(self) -> List[Tag]:
        self._ensure_open()
        with self._lock:
            cur = self._conn.execute(
                "SELECT * FROM tags ORDER BY created_at, name"
            )
            return [self._row_to_tag(r) for r in cur.fetchall()]

    def get_by_tag(self, name: str) -> Optional[DocVersion]:
        self._ensure_open()
        with self._lock:
            cur = self._conn.execute(
                "SELECT version_id FROM tags WHERE name = ?", (name,)
            )
            row = cur.fetchone()
            if row is None:
                return None
            version_id = row["version_id"]
        return self.get(version_id)

    # ------------------------------------------------------------------ counts
    def version_count(self, doc_id: str) -> int:
        self._ensure_open()
        with self._lock:
            cur = self._conn.execute(
                "SELECT COUNT(*) AS c FROM versions WHERE doc_id = ?",
                (doc_id,),
            )
            return int(cur.fetchone()["c"])

    # ------------------------------------------------------------------ close
    def close(self) -> None:
        with self._lock:
            if not self._closed:
                self._conn.close()
                self._closed = True

    def __enter__(self) -> "VersionStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
