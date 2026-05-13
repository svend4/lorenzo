"""Инкрементальный индекс: перестраивает только изменившиеся документы.

Хранит манифест всех проиндексированных файлов в SQLite.
При повторном запуске возвращает только те файлы, которые изменились или добавились.

Локация: <root>/.docstoolkit/index_manifest.sqlite

Использование:
    from docstoolkit.embeddings.incremental import IncrementalIndex

    idx = IncrementalIndex(root)
    stale = idx.get_stale_docs(docs_dir)          # список файлов для переиндексации
    for path in stale:
        content = path.read_text()
        # ... re-index ...
        idx.mark_indexed(path, path.stat().st_mtime, path.stat().st_size,
                         hashlib.sha256(content.encode()).hexdigest()[:16])
    deleted = idx.purge_deleted(docs_dir)          # очистить удалённые
"""
import hashlib
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS manifest (
    path         TEXT PRIMARY KEY,
    mtime        REAL NOT NULL,
    size         INTEGER NOT NULL,
    content_hash TEXT NOT NULL,
    indexed_ts   REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_manifest_mtime ON manifest(mtime);
"""


def _hash_file(path: Path) -> str:
    """SHA-256 первых 64 КБ файла (для быстрого content-hash)."""
    h = hashlib.sha256()
    try:
        with path.open("rb") as f:
            chunk = f.read(65536)
            h.update(chunk)
    except OSError:
        return ""
    return h.hexdigest()[:16]


class IncrementalIndex:
    """Манифест проиндексированных файлов с инкрементальными обновлениями."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.db_path = self.root / ".docstoolkit" / "index_manifest.sqlite"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    # ----- Core operations -----

    def needs_update(self, path: Path, mtime: float, size: int) -> bool:
        """Проверить, нужно ли переиндексировать файл.

        Возвращает True если:
        - файл отсутствует в манифесте, или
        - mtime или size отличается от сохранённых.
        """
        row = self.conn.execute(
            "SELECT mtime, size FROM manifest WHERE path = ?",
            (str(path),)
        ).fetchone()
        if row is None:
            return True
        return row["mtime"] != mtime or row["size"] != size

    def mark_indexed(self, path: Path, mtime: float, size: int,
                     content_hash: str) -> None:
        """Обновить запись в манифесте после успешной индексации."""
        self.conn.execute(
            "INSERT OR REPLACE INTO manifest "
            "(path, mtime, size, content_hash, indexed_ts) "
            "VALUES (?, ?, ?, ?, ?)",
            (str(path), mtime, size, content_hash, time.time())
        )
        self.conn.commit()

    def get_stale_docs(self, docs_dir: Path) -> list[Path]:
        """Обойти docs_dir и вернуть файлы, которые изменились или не проиндексированы."""
        docs_dir = Path(docs_dir)
        stale: list[Path] = []
        for path in sorted(docs_dir.rglob("*.md")):
            if not path.is_file():
                continue
            try:
                stat = path.stat()
            except OSError:
                continue
            if self.needs_update(path, stat.st_mtime, stat.st_size):
                stale.append(path)
        return stale

    def purge_deleted(self, docs_dir: Path) -> int:
        """Удалить из манифеста записи для файлов, которые больше не существуют.

        Возвращает количество удалённых записей.
        """
        docs_dir = Path(docs_dir)
        rows = self.conn.execute("SELECT path FROM manifest").fetchall()
        deleted = 0
        for row in rows:
            p = Path(row["path"])
            # Удаляем если файл исчез или находится вне docs_dir
            try:
                p.relative_to(docs_dir)
            except ValueError:
                # Путь не в этой docs_dir — не трогаем
                continue
            if not p.exists():
                self.conn.execute("DELETE FROM manifest WHERE path = ?", (row["path"],))
                deleted += 1
        if deleted:
            self.conn.commit()
        return deleted

    # ----- Stats -----

    def stats(self) -> dict:
        """Статистика манифеста."""
        total = self.conn.execute(
            "SELECT COUNT(*) AS n FROM manifest"
        ).fetchone()["n"]

        last_ts_row = self.conn.execute(
            "SELECT MAX(indexed_ts) AS ts FROM manifest"
        ).fetchone()
        last_update = last_ts_row["ts"] if last_ts_row and last_ts_row["ts"] else None

        return {
            "total_tracked": total,
            "last_update": last_update,
            "db_path": str(self.db_path),
        }
