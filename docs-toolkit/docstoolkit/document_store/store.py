"""SQLite-backed document store for arbitrary JSON documents (E116)."""

import json
import sqlite3
import threading
import time
from dataclasses import dataclass, field
from typing import Any, Callable
from uuid import uuid4


# ── Data model ────────────────────────────────────────────────────────────────

@dataclass
class Document:
    doc_id: str = field(default_factory=lambda: uuid4().hex[:12])
    collection: str = "default"
    data: dict = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    text: str = ""
    created_at: float = 0.0
    updated_at: float = 0.0


# ── Schema ────────────────────────────────────────────────────────────────────

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS documents (
    doc_id      TEXT PRIMARY KEY,
    collection  TEXT DEFAULT 'default',
    data        TEXT DEFAULT '{}',
    tags        TEXT DEFAULT '[]',
    text        TEXT DEFAULT '',
    created_at  REAL,
    updated_at  REAL
)
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _row_to_doc(row: sqlite3.Row) -> Document:
    return Document(
        doc_id=row["doc_id"],
        collection=row["collection"],
        data=json.loads(row["data"]),
        tags=json.loads(row["tags"]),
        text=row["text"] or "",
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


# ── Store ─────────────────────────────────────────────────────────────────────

class DocumentStore:
    """Thread-safe SQLite-backed document store.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file, or ``":memory:"`` for an in-memory
        database.
    now_fn:
        Callable that returns the current time as a float (Unix timestamp).
        Defaults to :func:`time.time`.  Useful for deterministic testing.
    """

    def __init__(
        self,
        db_path: str = ":memory:",
        now_fn: Callable[[], float] | None = None,
    ) -> None:
        self._db_path = db_path
        self._now = now_fn if now_fn is not None else time.time
        self._lock = threading.Lock()
        # For :memory: databases all threads must share one connection because
        # each sqlite3.connect(":memory:") opens a *different* database.
        # For file-backed databases we use per-thread connections to avoid
        # "database is locked" contention while still serialising writes with
        # self._lock.
        self._shared_conn: sqlite3.Connection | None = None
        self._local = threading.local()
        # Initialise schema (and create the shared connection for :memory:)
        self._conn()

    # ── Connection management ─────────────────────────────────────────────
    # :memory:  → one shared connection for all threads
    # file path → one connection per thread (WAL allows concurrent reads)

    def _conn(self) -> sqlite3.Connection:
        if self._db_path == ":memory:":
            if self._shared_conn is None:
                conn = sqlite3.connect(
                    self._db_path, check_same_thread=False
                )
                conn.row_factory = sqlite3.Row
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute(_CREATE_TABLE)
                conn.commit()
                self._shared_conn = conn
            return self._shared_conn

        # File-backed: per-thread connection
        if not hasattr(self._local, "conn") or self._local.conn is None:
            conn = sqlite3.connect(self._db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute(_CREATE_TABLE)
            conn.commit()
            self._local.conn = conn
        return self._local.conn

    # ── Public API ────────────────────────────────────────────────────────

    def insert(
        self,
        collection: str,
        data: dict,
        tags: list[str] | None = None,
        text: str = "",
    ) -> Document:
        """Insert a new document and return it with a generated ``doc_id``."""
        now = self._now()
        doc = Document(
            collection=collection,
            data=data,
            tags=list(tags) if tags else [],
            text=text,
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._conn().execute(
                """
                INSERT INTO documents (doc_id, collection, data, tags, text,
                                       created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    doc.doc_id,
                    doc.collection,
                    json.dumps(doc.data),
                    json.dumps(doc.tags),
                    doc.text,
                    doc.created_at,
                    doc.updated_at,
                ),
            )
            self._conn().commit()
        return doc

    def update(
        self,
        doc_id: str,
        data: dict | None = None,
        tags: list[str] | None = None,
        text: str | None = None,
    ) -> "Document | None":
        """Patch fields of an existing document.

        Only the supplied arguments are changed; omitted arguments are left
        unchanged.  Returns the updated :class:`Document`, or ``None`` if
        *doc_id* is not found.
        """
        with self._lock:
            existing = self._get_locked(doc_id)
            if existing is None:
                return None

            new_data = data if data is not None else existing.data
            new_tags = list(tags) if tags is not None else existing.tags
            new_text = text if text is not None else existing.text
            now = self._now()

            self._conn().execute(
                """
                UPDATE documents
                SET data=?, tags=?, text=?, updated_at=?
                WHERE doc_id=?
                """,
                (
                    json.dumps(new_data),
                    json.dumps(new_tags),
                    new_text,
                    now,
                    doc_id,
                ),
            )
            self._conn().commit()

        return self.get(doc_id)

    def get(self, doc_id: str) -> "Document | None":
        """Return the document with the given *doc_id*, or ``None``."""
        row = self._conn().execute(
            "SELECT * FROM documents WHERE doc_id=?", (doc_id,)
        ).fetchone()
        return _row_to_doc(row) if row else None

    def _get_locked(self, doc_id: str) -> "Document | None":
        """Like :meth:`get` but assumes the caller holds ``_lock``."""
        row = self._conn().execute(
            "SELECT * FROM documents WHERE doc_id=?", (doc_id,)
        ).fetchone()
        return _row_to_doc(row) if row else None

    def delete(self, doc_id: str) -> bool:
        """Delete the document.  Returns ``True`` if a row was removed."""
        with self._lock:
            cur = self._conn().execute(
                "DELETE FROM documents WHERE doc_id=?", (doc_id,)
            )
            self._conn().commit()
        return cur.rowcount > 0

    def find(
        self,
        collection: str | None = None,
        tags: list[str] | None = None,
        text_query: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Document]:
        """Return documents matching all supplied filters.

        * *collection*: exact match on the collection field.
        * *tags*: document must contain **all** specified tags.
        * *text_query*: case-insensitive substring match on the ``text``
          field.
        * Results are ordered by ``created_at`` DESC.
        * *limit* / *offset* apply **after** tag filtering in Python.
        """
        sql = "SELECT * FROM documents WHERE 1=1"
        params: list[Any] = []

        if collection is not None:
            sql += " AND collection=?"
            params.append(collection)

        if text_query is not None:
            sql += " AND LOWER(text) LIKE LOWER(?)"
            params.append(f"%{text_query}%")

        sql += " ORDER BY created_at DESC"

        rows = self._conn().execute(sql, params).fetchall()
        docs = [_row_to_doc(r) for r in rows]

        # Tag filter: all specified tags must be present
        if tags:
            required = set(tags)
            docs = [d for d in docs if required.issubset(set(d.tags))]

        return docs[offset: offset + limit]

    def count(
        self,
        collection: str | None = None,
        tags: list[str] | None = None,
    ) -> int:
        """Return the number of documents matching the filters."""
        # Re-use find (without limit) so tag logic stays in one place
        return len(self.find(collection=collection, tags=tags, limit=10**9))

    def collections(self) -> list[str]:
        """Return distinct collection names, sorted alphabetically."""
        rows = self._conn().execute(
            "SELECT DISTINCT collection FROM documents ORDER BY collection"
        ).fetchall()
        return [r[0] for r in rows]

    def all_tags(self) -> list[str]:
        """Return all distinct tag strings across all documents, sorted."""
        rows = self._conn().execute(
            "SELECT tags FROM documents"
        ).fetchall()
        seen: set[str] = set()
        for row in rows:
            for tag in json.loads(row[0]):
                seen.add(tag)
        return sorted(seen)

    def close(self) -> None:
        """Close the database connection(s)."""
        if self._db_path == ":memory:":
            if self._shared_conn is not None:
                self._shared_conn.close()
                self._shared_conn = None
        else:
            conn = getattr(self._local, "conn", None)
            if conn is not None:
                conn.close()
                self._local.conn = None
