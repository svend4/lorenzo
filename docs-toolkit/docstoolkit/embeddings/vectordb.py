"""Vector DB backends для production scale.

3 опции:
  - SQLiteBackend (default) — встроенный, миллионы векторов на одной машине
  - QdrantBackend (pip install qdrant-client) — production vector DB
  - PgVectorBackend (pip install psycopg) — Postgres extension

Интерфейс одинаковый: upsert/search/delete.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class VectorMatch:
    doc_id: str
    score: float
    metadata: dict | None = None


class VectorBackend(ABC):
    """Универсальный интерфейс vector DB."""

    name: str = "base"
    dim: int = 0

    @abstractmethod
    def upsert(self, doc_id: str, vector: list[float],
               metadata: dict | None = None):
        ...

    @abstractmethod
    def upsert_batch(self, items: list[tuple[str, list[float], dict]]):
        ...

    @abstractmethod
    def search(self, query_vector: list[float],
               top_k: int = 10) -> list[VectorMatch]:
        ...

    @abstractmethod
    def delete(self, doc_id: str):
        ...

    @abstractmethod
    def count(self) -> int:
        ...

    @abstractmethod
    def close(self):
        ...


class SQLiteBackend(VectorBackend):
    """Default — JSON-stored vectors в SQLite. Не для миллионов."""

    name = "sqlite"

    def __init__(self, db_path: str, dim: int = 384):
        import sqlite3
        import json as _json
        from pathlib import Path
        self._json = _json
        self.dim = dim
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vectors (
                doc_id TEXT PRIMARY KEY,
                vector_json TEXT NOT NULL,
                metadata_json TEXT,
                dim INTEGER
            )
        """)
        self.conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_vec_doc ON vectors(doc_id)"
        )

    def upsert(self, doc_id: str, vector, metadata=None):
        self.conn.execute(
            "INSERT OR REPLACE INTO vectors (doc_id, vector_json, metadata_json, dim) "
            "VALUES (?, ?, ?, ?)",
            (doc_id, self._json.dumps(vector),
             self._json.dumps(metadata or {}), len(vector) if vector else 0)
        )
        self.conn.commit()

    def upsert_batch(self, items):
        self.conn.executemany(
            "INSERT OR REPLACE INTO vectors (doc_id, vector_json, metadata_json, dim) "
            "VALUES (?, ?, ?, ?)",
            [(d, self._json.dumps(v), self._json.dumps(m or {}),
              len(v) if v else 0) for d, v, m in items]
        )
        self.conn.commit()

    def search(self, query_vector, top_k=10):
        import math
        rows = self.conn.execute(
            "SELECT doc_id, vector_json, metadata_json FROM vectors"
        ).fetchall()
        scored = []
        q_norm = math.sqrt(sum(x * x for x in query_vector))
        if q_norm == 0:
            return []
        for doc_id, vec_json, meta_json in rows:
            vec = self._json.loads(vec_json)
            if len(vec) != len(query_vector):
                continue
            dot = sum(a * b for a, b in zip(query_vector, vec))
            v_norm = math.sqrt(sum(x * x for x in vec))
            if v_norm == 0:
                continue
            score = dot / (q_norm * v_norm)
            scored.append(VectorMatch(
                doc_id=doc_id, score=score,
                metadata=self._json.loads(meta_json or "{}")
            ))
        scored.sort(key=lambda x: -x.score)
        return scored[:top_k]

    def delete(self, doc_id):
        self.conn.execute("DELETE FROM vectors WHERE doc_id = ?", (doc_id,))
        self.conn.commit()

    def count(self):
        row = self.conn.execute("SELECT COUNT(*) FROM vectors").fetchone()
        return row[0]

    def close(self):
        self.conn.close()


class QdrantBackend(VectorBackend):
    """Qdrant — production vector DB. Требует pip install qdrant-client."""

    name = "qdrant"

    def __init__(self, url: str = "http://localhost:6333",
                 collection: str = "docs", dim: int = 384):
        try:
            from qdrant_client import QdrantClient
            from qdrant_client.http import models as qmodels
        except ImportError:
            raise ImportError("Для Qdrant: pip install qdrant-client")
        self._qmodels = qmodels
        self.client = QdrantClient(url=url)
        self.collection = collection
        self.dim = dim
        # Создать collection если нет
        try:
            self.client.get_collection(collection)
        except Exception:
            self.client.create_collection(
                collection_name=collection,
                vectors_config=qmodels.VectorParams(
                    size=dim, distance=qmodels.Distance.COSINE
                ),
            )

    def upsert(self, doc_id, vector, metadata=None):
        self.client.upsert(
            collection_name=self.collection,
            points=[self._qmodels.PointStruct(
                id=hash(doc_id) % (2**63),
                vector=vector,
                payload={"doc_id": doc_id, **(metadata or {})},
            )],
        )

    def upsert_batch(self, items):
        points = [
            self._qmodels.PointStruct(
                id=hash(d) % (2**63), vector=v,
                payload={"doc_id": d, **(m or {})},
            )
            for d, v, m in items
        ]
        self.client.upsert(collection_name=self.collection, points=points)

    def search(self, query_vector, top_k=10):
        results = self.client.search(
            collection_name=self.collection,
            query_vector=query_vector, limit=top_k,
        )
        return [
            VectorMatch(
                doc_id=r.payload.get("doc_id", str(r.id)),
                score=r.score,
                metadata=r.payload,
            )
            for r in results
        ]

    def delete(self, doc_id):
        self.client.delete(
            collection_name=self.collection,
            points_selector=self._qmodels.PointIdsList(
                points=[hash(doc_id) % (2**63)]
            ),
        )

    def count(self):
        info = self.client.get_collection(self.collection)
        return info.points_count

    def close(self):
        self.client.close()


class PgVectorBackend(VectorBackend):
    """pgvector — Postgres extension. Требует psycopg + расширение pgvector."""

    name = "pgvector"

    def __init__(self, dsn: str, table: str = "doc_vectors", dim: int = 384):
        try:
            import psycopg
        except ImportError:
            raise ImportError("Для pgvector: pip install psycopg")
        self.dim = dim
        self.table = table
        self.conn = psycopg.connect(dsn)
        with self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {table} ("
                f"doc_id TEXT PRIMARY KEY, "
                f"embedding vector({dim}), "
                f"metadata JSONB)"
            )
            cur.execute(
                f"CREATE INDEX IF NOT EXISTS idx_{table}_emb "
                f"ON {table} USING ivfflat (embedding vector_cosine_ops)"
            )
        self.conn.commit()

    def upsert(self, doc_id, vector, metadata=None):
        import json as _json
        with self.conn.cursor() as cur:
            cur.execute(
                f"INSERT INTO {self.table} (doc_id, embedding, metadata) "
                f"VALUES (%s, %s::vector, %s::jsonb) "
                f"ON CONFLICT (doc_id) DO UPDATE SET "
                f"embedding = EXCLUDED.embedding, metadata = EXCLUDED.metadata",
                (doc_id, vector, _json.dumps(metadata or {}))
            )
        self.conn.commit()

    def upsert_batch(self, items):
        import json as _json
        with self.conn.cursor() as cur:
            cur.executemany(
                f"INSERT INTO {self.table} (doc_id, embedding, metadata) "
                f"VALUES (%s, %s::vector, %s::jsonb) "
                f"ON CONFLICT (doc_id) DO UPDATE SET "
                f"embedding = EXCLUDED.embedding, metadata = EXCLUDED.metadata",
                [(d, v, _json.dumps(m or {})) for d, v, m in items]
            )
        self.conn.commit()

    def search(self, query_vector, top_k=10):
        with self.conn.cursor() as cur:
            cur.execute(
                f"SELECT doc_id, 1 - (embedding <=> %s::vector) AS score, metadata "
                f"FROM {self.table} ORDER BY embedding <=> %s::vector LIMIT %s",
                (query_vector, query_vector, top_k)
            )
            return [
                VectorMatch(doc_id=r[0], score=float(r[1]), metadata=r[2])
                for r in cur.fetchall()
            ]

    def delete(self, doc_id):
        with self.conn.cursor() as cur:
            cur.execute(f"DELETE FROM {self.table} WHERE doc_id = %s", (doc_id,))
        self.conn.commit()

    def count(self):
        with self.conn.cursor() as cur:
            cur.execute(f"SELECT COUNT(*) FROM {self.table}")
            return cur.fetchone()[0]

    def close(self):
        self.conn.close()


_REGISTRY = {
    "sqlite": SQLiteBackend,
}


def get_backend(name: str = "sqlite", **kwargs) -> VectorBackend:
    """Factory: имя → backend instance."""
    if name == "qdrant":
        return QdrantBackend(**kwargs)
    if name == "pgvector":
        return PgVectorBackend(**kwargs)
    if name not in _REGISTRY:
        name = "sqlite"
    return _REGISTRY[name](**kwargs)


def list_backends() -> list[dict]:
    """Доступные backends с runtime status."""
    result = [{"name": "sqlite", "available": True, "kind": "embedded"}]
    for name in ["qdrant", "pgvector"]:
        try:
            if name == "qdrant":
                import qdrant_client
            else:
                import psycopg
            result.append({"name": name, "available": True, "kind": "external"})
        except ImportError:
            result.append({"name": name, "available": False,
                           "kind": "external",
                           "error": f"pip install {name}-client" if name == "qdrant" else "pip install psycopg"})
    return result
