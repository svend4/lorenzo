"""SQLite-backed triple store for the Knowledge Graph (Phase V.1).

The in-memory `KnowledgeGraph` is fine for small corpora and tests, but
once you build a graph over thousands of documents you want:
  - persistence (don't re-extract on every run)
  - indexed lookup by subject / object / predicate
  - join with document provenance (which doc, which span)

`TripleStore` is the thin SQLite layer for that. Schema:

    CREATE TABLE entities (
        entity_id   TEXT PRIMARY KEY,
        name        TEXT NOT NULL,
        entity_type TEXT NOT NULL,
        aliases     TEXT,            -- JSON array
        metadata    TEXT             -- JSON object
    );
    CREATE TABLE triples (
        triple_id   TEXT PRIMARY KEY,
        subject     TEXT NOT NULL,    -- FK entities.entity_id
        predicate   TEXT NOT NULL,
        object      TEXT NOT NULL,    -- FK entities.entity_id
        doc_id      TEXT,
        span_start  INTEGER,
        span_end    INTEGER,
        score       REAL DEFAULT 1.0,
        ts          TEXT,
        UNIQUE(subject, predicate, object, doc_id)
    );
    CREATE INDEX idx_subj  ON triples(subject);
    CREATE INDEX idx_obj   ON triples(object);
    CREATE INDEX idx_pred  ON triples(predicate);
    CREATE INDEX idx_doc   ON triples(doc_id);

The store is local-first (single SQLite file, WAL) and stdlib-only.
"""
from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from docstoolkit.knowledge_graph.entity import Entity, EntityType
from docstoolkit.knowledge_graph.relation import Relation, RelationType


@dataclass(frozen=True)
class Triple:
    """One subject-predicate-object fact, optionally tied to a doc span.

    Mirrors a row in the `triples` table; differs from `Relation` by
    carrying the source-document provenance (`doc_id`, `span_start`,
    `span_end`).
    """
    subject: str       # entity_id
    predicate: str     # RelationType.value
    object: str        # entity_id
    doc_id: str = ""
    span_start: int = 0
    span_end: int = 0
    score: float = 1.0
    triple_id: str = ""


_SCHEMA = """
CREATE TABLE IF NOT EXISTS entities (
    entity_id   TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    aliases     TEXT,
    metadata    TEXT
);
CREATE TABLE IF NOT EXISTS triples (
    triple_id   TEXT PRIMARY KEY,
    subject     TEXT NOT NULL,
    predicate   TEXT NOT NULL,
    object      TEXT NOT NULL,
    doc_id      TEXT DEFAULT '',
    span_start  INTEGER DEFAULT 0,
    span_end    INTEGER DEFAULT 0,
    score       REAL DEFAULT 1.0,
    ts          TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_triple_unique
    ON triples(subject, predicate, object, doc_id);
CREATE INDEX IF NOT EXISTS idx_subj ON triples(subject);
CREATE INDEX IF NOT EXISTS idx_obj  ON triples(object);
CREATE INDEX IF NOT EXISTS idx_pred ON triples(predicate);
CREATE INDEX IF NOT EXISTS idx_doc  ON triples(doc_id);
"""


def _new_id() -> str:
    return uuid.uuid4().hex[:12]


class TripleStore:
    """Persistent KG storage backed by SQLite.

    Phase V.1 — stdlib-only, in-memory mode for tests (`:memory:`).

    Example::

        store = TripleStore("/tmp/kg.sqlite")
        store.add_entity(Entity("py", "Python", EntityType.TECHNOLOGY))
        store.add_entity(Entity("rag", "RAG", EntityType.CONCEPT))
        store.add_triple(Triple(
            subject="py", predicate=RelationType.USES.value, object="rag",
            doc_id="docs/01-svyazi/rag.md", score=0.92,
        ))
        for t in store.find_triples(subject="py"):
            print(t)
        store.close()
    """

    def __init__(self, path: str | Path = ":memory:"):
        self.path = str(path)
        self._conn = sqlite3.connect(self.path)
        # Phase V.1 — enable WAL for concurrent readers; safe for :memory:
        if self.path != ":memory:":
            try:
                self._conn.execute("PRAGMA journal_mode = WAL")
            except sqlite3.DatabaseError:
                pass
        self._conn.execute("PRAGMA foreign_keys = ON")
        with closing(self._conn.cursor()) as cur:
            cur.executescript(_SCHEMA)
        self._conn.commit()

    # ---------------- Entities ----------------

    def add_entity(self, entity: Entity) -> None:
        with closing(self._conn.cursor()) as cur:
            cur.execute(
                """INSERT OR REPLACE INTO entities
                   (entity_id, name, entity_type, aliases, metadata)
                   VALUES (?, ?, ?, ?, ?)""",
                (
                    entity.entity_id,
                    entity.name,
                    entity.entity_type.value,
                    json.dumps(list(entity.aliases), ensure_ascii=False),
                    json.dumps(dict(entity.metadata), ensure_ascii=False),
                ),
            )
        self._conn.commit()

    def get_entity(self, entity_id: str) -> Entity | None:
        with closing(self._conn.cursor()) as cur:
            row = cur.execute(
                """SELECT entity_id, name, entity_type, aliases, metadata
                   FROM entities WHERE entity_id = ?""",
                (entity_id,),
            ).fetchone()
        if not row:
            return None
        return Entity(
            entity_id=row[0],
            name=row[1],
            entity_type=EntityType(row[2]),
            aliases=tuple(json.loads(row[3] or "[]")),
            metadata=json.loads(row[4] or "{}"),
        )

    def find_entity(self, name: str) -> Entity | None:
        """Find by exact name (case-insensitive) or by alias."""
        lower = name.lower()
        with closing(self._conn.cursor()) as cur:
            rows = cur.execute(
                """SELECT entity_id, name, entity_type, aliases, metadata
                   FROM entities"""
            ).fetchall()
        for row in rows:
            if row[1].lower() == lower:
                return Entity(
                    entity_id=row[0], name=row[1],
                    entity_type=EntityType(row[2]),
                    aliases=tuple(json.loads(row[3] or "[]")),
                    metadata=json.loads(row[4] or "{}"),
                )
            for alias in json.loads(row[3] or "[]"):
                if alias.lower() == lower:
                    return Entity(
                        entity_id=row[0], name=row[1],
                        entity_type=EntityType(row[2]),
                        aliases=tuple(json.loads(row[3] or "[]")),
                        metadata=json.loads(row[4] or "{}"),
                    )
        return None

    def entity_count(self) -> int:
        with closing(self._conn.cursor()) as cur:
            row = cur.execute("SELECT COUNT(*) FROM entities").fetchone()
        return int(row[0])

    # ---------------- Triples ----------------

    def add_triple(self, triple: Triple) -> str:
        tid = triple.triple_id or _new_id()
        with closing(self._conn.cursor()) as cur:
            # ON CONFLICT bumps score (max), preserves earliest ts.
            cur.execute(
                """INSERT INTO triples
                   (triple_id, subject, predicate, object,
                    doc_id, span_start, span_end, score, ts)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(subject, predicate, object, doc_id) DO UPDATE
                     SET score = MAX(score, excluded.score)""",
                (tid, triple.subject, triple.predicate, triple.object,
                 triple.doc_id, triple.span_start, triple.span_end,
                 triple.score, datetime.utcnow().isoformat(timespec="seconds")),
            )
        self._conn.commit()
        return tid

    def add_relation(self, relation: Relation, doc_id: str = "",
                     score: float = 1.0) -> str:
        """Convenience: add a Relation as a Triple with given doc provenance."""
        return self.add_triple(Triple(
            subject=relation.source_id,
            predicate=relation.relation_type.value,
            object=relation.target_id,
            doc_id=doc_id,
            score=score,
        ))

    def find_triples(self, *,
                     subject: str | None = None,
                     predicate: str | None = None,
                     object: str | None = None,
                     doc_id: str | None = None,
                     limit: int = 1000) -> list[Triple]:
        """Filter triples by any combination of fields."""
        clauses, args = [], []
        if subject is not None:
            clauses.append("subject = ?")
            args.append(subject)
        if predicate is not None:
            clauses.append("predicate = ?")
            args.append(predicate)
        if object is not None:
            clauses.append("object = ?")
            args.append(object)
        if doc_id is not None:
            clauses.append("doc_id = ?")
            args.append(doc_id)
        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        args.append(int(limit))
        sql = (
            "SELECT triple_id, subject, predicate, object, doc_id, "
            "span_start, span_end, score FROM triples" + where +
            " ORDER BY score DESC LIMIT ?"
        )
        with closing(self._conn.cursor()) as cur:
            rows = cur.execute(sql, tuple(args)).fetchall()
        return [
            Triple(triple_id=r[0], subject=r[1], predicate=r[2], object=r[3],
                   doc_id=r[4], span_start=r[5], span_end=r[6], score=r[7])
            for r in rows
        ]

    def triple_count(self) -> int:
        with closing(self._conn.cursor()) as cur:
            row = cur.execute("SELECT COUNT(*) FROM triples").fetchone()
        return int(row[0])

    def neighbors(self, entity_id: str, *,
                  predicate: str | None = None) -> list[str]:
        """Return entity_ids connected to `entity_id` (either direction)."""
        clauses = ["(subject = ? OR object = ?)"]
        args: list = [entity_id, entity_id]
        if predicate is not None:
            clauses.append("predicate = ?")
            args.append(predicate)
        sql = ("SELECT subject, object FROM triples WHERE " +
               " AND ".join(clauses))
        with closing(self._conn.cursor()) as cur:
            rows = cur.execute(sql, tuple(args)).fetchall()
        seen: set[str] = set()
        out: list[str] = []
        for s, o in rows:
            other = o if s == entity_id else s
            if other != entity_id and other not in seen:
                seen.add(other)
                out.append(other)
        return out

    # ---------------- Lifecycle ----------------

    def close(self) -> None:
        try:
            self._conn.close()
        except sqlite3.ProgrammingError:
            pass


__all__ = ["Triple", "TripleStore"]
