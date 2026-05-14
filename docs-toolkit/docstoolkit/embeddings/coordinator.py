"""IndexCoordinator — атомарное обновление всех зарегистрированных индексов.

Когда документ меняется, coordinator:
1. Читает файл, вычисляет MD5-хэш содержимого.
2. Сравнивает с манифестом (SQLite).
3. Если изменился — вызывает add/update на каждом зарегистрированном Index.
4. Обновляет запись в манифесте.

Использование:
    from docstoolkit.embeddings.coordinator import IndexCoordinator, Index, IndexHit

    coordinator = IndexCoordinator()
    coordinator.register("bm25", my_bm25_index)
    coordinator.register("tfidf", my_tfidf_index)

    updated = coordinator.on_doc_change(Path("docs/readme.md"))
    results = coordinator.query_all("search query")
"""
from __future__ import annotations

import hashlib
import sqlite3
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol, runtime_checkable


MANIFEST_SCHEMA = """
CREATE TABLE IF NOT EXISTS doc_manifest (
    doc_id       TEXT PRIMARY KEY,
    path         TEXT NOT NULL,
    mtime        REAL NOT NULL,
    content_hash TEXT NOT NULL,
    updated_ts   TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_manifest_path ON doc_manifest(path);
"""


@runtime_checkable
class Index(Protocol):
    """Protocol for a searchable index that supports CRUD operations."""

    def add(self, doc_id: str, content: str) -> None: ...
    def remove(self, doc_id: str) -> None: ...
    def update(self, doc_id: str, content: str) -> None: ...
    def query(self, q: str, top_k: int = 10) -> list[dict]: ...


@dataclass
class IndexHit:
    """A single hit returned by an index query."""
    doc_id: str
    score: float
    index_name: str = ""


def _md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8", errors="replace")).hexdigest()


def _normalize_doc_id(path: str | Path) -> str:
    """Normalize a path to a consistent doc_id string."""
    return str(Path(path))


class IndexCoordinator:
    """Atomically updates all registered Index instances when a doc changes.

    Maintains a SQLite manifest that tracks: doc_id, path, mtime, content_hash,
    and updated_ts for every document that has been indexed.

    Thread-safe: all public methods acquire an internal Lock.
    """

    def __init__(self, db_path: str = ":memory:") -> None:
        self._lock = threading.Lock()
        self._indexes: dict[str, Index] = {}
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.executescript(MANIFEST_SCHEMA)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, name: str, index: Index) -> None:
        """Register an index under a given name."""
        with self._lock:
            self._indexes[name] = index

    # ------------------------------------------------------------------
    # Document lifecycle
    # ------------------------------------------------------------------

    def on_doc_change(self, path: str | Path) -> list[str]:
        """Read file at *path*, update all indexes if content changed.

        Returns the list of index names that were updated.
        Raises FileNotFoundError if the file does not exist.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        content = path.read_text(encoding="utf-8", errors="replace")
        content_hash = _md5(content)
        mtime = path.stat().st_mtime
        doc_id = _normalize_doc_id(path)

        with self._lock:
            row = self._conn.execute(
                "SELECT content_hash FROM doc_manifest WHERE doc_id = ?",
                (doc_id,),
            ).fetchone()

            if row is not None and row["content_hash"] == content_hash:
                # Content unchanged — nothing to do.
                return []

            is_new = row is None
            updated_names: list[str] = []

            for name, idx in self._indexes.items():
                if is_new:
                    idx.add(doc_id, content)
                else:
                    idx.update(doc_id, content)
                updated_names.append(name)

            now_ts = datetime.now(timezone.utc).isoformat()
            self._conn.execute(
                "INSERT OR REPLACE INTO doc_manifest "
                "(doc_id, path, mtime, content_hash, updated_ts) "
                "VALUES (?, ?, ?, ?, ?)",
                (doc_id, str(path), mtime, content_hash, now_ts),
            )
            self._conn.commit()

            return updated_names

    def on_doc_remove(self, path: str | Path) -> None:
        """Remove doc from all indexes and from the manifest."""
        doc_id = _normalize_doc_id(path)
        with self._lock:
            for idx in self._indexes.values():
                idx.remove(doc_id)
            self._conn.execute(
                "DELETE FROM doc_manifest WHERE doc_id = ?",
                (doc_id,),
            )
            self._conn.commit()

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------

    def query_all(self, q: str, top_k: int = 10) -> dict[str, list[IndexHit]]:
        """Query all registered indexes.

        Returns {index_name: [IndexHit, ...]} for every registered index.
        Indexes that raise an exception are skipped (empty list returned).
        """
        with self._lock:
            snapshot = dict(self._indexes)

        results: dict[str, list[IndexHit]] = {}
        for name, idx in snapshot.items():
            try:
                raw = idx.query(q, top_k=top_k)
                hits = [
                    IndexHit(
                        doc_id=hit.get("doc_id", ""),
                        score=float(hit.get("score", 0.0)),
                        index_name=name,
                    )
                    for hit in raw
                ]
            except Exception:
                hits = []
            results[name] = hits

        return results

    # ------------------------------------------------------------------
    # Verification / diagnostics
    # ------------------------------------------------------------------

    def verify(self) -> dict[str, list[str]]:
        """Check which doc_ids are in the manifest but missing from each index.

        Only works for indexes that implement an optional ``list_all() -> list[str]``
        method. Indexes without ``list_all`` are skipped (empty list returned).

        Returns {index_name: [missing_doc_ids]}.
        """
        with self._lock:
            rows = self._conn.execute(
                "SELECT doc_id FROM doc_manifest"
            ).fetchall()
            manifest_ids = {row["doc_id"] for row in rows}
            snapshot = dict(self._indexes)

        missing: dict[str, list[str]] = {}
        for name, idx in snapshot.items():
            list_all = getattr(idx, "list_all", None)
            if not callable(list_all):
                missing[name] = []
                continue
            try:
                indexed_ids = set(list_all())
            except Exception:
                missing[name] = []
                continue
            missing[name] = sorted(manifest_ids - indexed_ids)

        return missing

    def stats(self) -> dict:
        """Return basic statistics about the coordinator state."""
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*) AS n FROM doc_manifest"
            ).fetchone()
            docs_tracked = row["n"] if row else 0
            index_names = list(self._indexes.keys())

        return {
            "docs_tracked": docs_tracked,
            "indexes": index_names,
            "db_path": self._db_path,
        }

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the SQLite connection."""
        with self._lock:
            self._conn.close()
