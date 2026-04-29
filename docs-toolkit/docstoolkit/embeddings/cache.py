"""Persistent SQLite cache для embeddings.

Хранит:
  - IDF (для TF-IDF) — pickled dict
  - Vectors per file (для sentence-transformers) с file hash как key
  - Метаданные модели (имя, dim, ts)

Локация: <cfg.root>/.docstoolkit/cache/embeddings.sqlite

Структура:
  metadata    — provider name, model, dim, version
  idf         — TF-IDF IDF словарь (pickled)
  vectors     — {file_path: hash, vec_blob, ts, content_hash}
  vocab       — словарь токенов с id (опц., для будущего)

Бенефит:
  - TF-IDF.fit() кэшируется → второй вызов мгновенный
  - Embeddings вычисляются 1 раз на файл, переиспользуются пока content_hash совпадает
"""
import hashlib
import pickle
import sqlite3
import time
from datetime import datetime
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS metadata (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_ts INTEGER
);

CREATE TABLE IF NOT EXISTS idf (
    provider TEXT PRIMARY KEY,
    data BLOB,
    n_docs INTEGER,
    updated_ts INTEGER
);

CREATE TABLE IF NOT EXISTS vectors (
    provider TEXT NOT NULL,
    doc_id TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    vector BLOB NOT NULL,
    dim INTEGER,
    updated_ts INTEGER NOT NULL,
    PRIMARY KEY (provider, doc_id)
);
CREATE INDEX IF NOT EXISTS idx_vec_provider ON vectors(provider);
CREATE INDEX IF NOT EXISTS idx_vec_hash ON vectors(content_hash);
"""


def hash_content(text: str) -> str:
    """SHA-256 первых 8 байт от контента (для cache invalidation)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


class EmbeddingCache:
    def __init__(self, db_path: str | Path):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    # ----- Metadata -----

    def set_meta(self, key: str, value: str):
        self.conn.execute(
            "INSERT OR REPLACE INTO metadata (key, value, updated_ts) VALUES (?, ?, ?)",
            (key, value, int(time.time()))
        )
        self.conn.commit()

    def get_meta(self, key: str) -> str | None:
        row = self.conn.execute(
            "SELECT value FROM metadata WHERE key = ?", (key,)
        ).fetchone()
        return row["value"] if row else None

    # ----- IDF (TF-IDF) -----

    def save_idf(self, provider: str, idf: dict, n_docs: int):
        blob = pickle.dumps(idf)
        self.conn.execute(
            "INSERT OR REPLACE INTO idf (provider, data, n_docs, updated_ts) "
            "VALUES (?, ?, ?, ?)",
            (provider, blob, n_docs, int(time.time()))
        )
        self.conn.commit()

    def load_idf(self, provider: str) -> tuple[dict, int] | None:
        row = self.conn.execute(
            "SELECT data, n_docs FROM idf WHERE provider = ?", (provider,)
        ).fetchone()
        if not row:
            return None
        return pickle.loads(row["data"]), row["n_docs"]

    # ----- Vectors -----

    def save_vector(self, provider: str, doc_id: str, content: str,
                    vector, dim: int = 0):
        """Сохранить вектор для документа.

        vector может быть list[float] или dict[str, float] (sparse).
        """
        blob = pickle.dumps(vector)
        ch = hash_content(content)
        self.conn.execute(
            "INSERT OR REPLACE INTO vectors "
            "(provider, doc_id, content_hash, vector, dim, updated_ts) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (provider, doc_id, ch, blob, dim, int(time.time()))
        )
        self.conn.commit()

    def load_vector(self, provider: str, doc_id: str, content: str = None):
        """Загрузить вектор. Если content передан и hash изменился — вернёт None."""
        row = self.conn.execute(
            "SELECT vector, content_hash FROM vectors "
            "WHERE provider = ? AND doc_id = ?",
            (provider, doc_id)
        ).fetchone()
        if not row:
            return None
        if content is not None and row["content_hash"] != hash_content(content):
            return None  # invalidated
        return pickle.loads(row["vector"])

    def has_vector(self, provider: str, doc_id: str, content: str) -> bool:
        return self.load_vector(provider, doc_id, content) is not None

    def list_cached(self, provider: str) -> list[str]:
        rows = self.conn.execute(
            "SELECT doc_id FROM vectors WHERE provider = ? ORDER BY doc_id",
            (provider,)
        ).fetchall()
        return [r["doc_id"] for r in rows]

    def invalidate(self, provider: str, doc_id: str | None = None):
        """Удалить кэш. Если doc_id None — весь провайдер."""
        if doc_id:
            self.conn.execute(
                "DELETE FROM vectors WHERE provider = ? AND doc_id = ?",
                (provider, doc_id)
            )
        else:
            self.conn.execute("DELETE FROM vectors WHERE provider = ?", (provider,))
            self.conn.execute("DELETE FROM idf WHERE provider = ?", (provider,))
        self.conn.commit()

    def clear_all(self):
        self.conn.execute("DELETE FROM vectors")
        self.conn.execute("DELETE FROM idf")
        self.conn.execute("DELETE FROM metadata")
        self.conn.commit()

    # ----- Stats -----

    def stats(self) -> dict:
        result = {}
        result["providers"] = [
            r["provider"] for r in self.conn.execute(
                "SELECT DISTINCT provider FROM vectors ORDER BY provider"
            ).fetchall()
        ]
        result["total_vectors"] = self.conn.execute(
            "SELECT COUNT(*) AS n FROM vectors"
        ).fetchone()["n"]
        result["per_provider"] = {
            r["provider"]: r["n"] for r in self.conn.execute(
                "SELECT provider, COUNT(*) AS n FROM vectors GROUP BY provider"
            ).fetchall()
        }
        result["idf_providers"] = [
            r["provider"] for r in self.conn.execute(
                "SELECT provider FROM idf"
            ).fetchall()
        ]
        result["db_size_kb"] = self.path.stat().st_size // 1024 if self.path.exists() else 0
        return result
