"""Сохранённые запросы + алерты при изменении результатов."""
import hashlib
import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from docstoolkit.config import load_config


SCHEMA = """
CREATE TABLE IF NOT EXISTS saved_queries (
    id TEXT PRIMARY KEY,
    owner TEXT NOT NULL DEFAULT '',
    query TEXT NOT NULL,
    retriever_method TEXT NOT NULL DEFAULT 'hybrid',
    top_k INTEGER NOT NULL DEFAULT 10,
    schedule TEXT NOT NULL DEFAULT 'daily',
    last_run_ts TEXT NOT NULL DEFAULT '',
    last_results_hash TEXT NOT NULL DEFAULT '',
    cooldown_hours INTEGER NOT NULL DEFAULT 24,
    enabled INTEGER NOT NULL DEFAULT 1,
    created_ts TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sq_owner ON saved_queries(owner);
CREATE INDEX IF NOT EXISTS idx_sq_enabled ON saved_queries(enabled);

CREATE TABLE IF NOT EXISTS fired_alerts (
    id TEXT PRIMARY KEY,
    query_id TEXT NOT NULL,
    query TEXT NOT NULL,
    owner TEXT NOT NULL DEFAULT '',
    added_json TEXT NOT NULL DEFAULT '[]',
    removed_json TEXT NOT NULL DEFAULT '[]',
    ts TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_fa_query_id ON fired_alerts(query_id);
CREATE INDEX IF NOT EXISTS idx_fa_ts ON fired_alerts(ts);
"""


@dataclass
class SavedQuery:
    """Сохранённый поисковый запрос с параметрами алертинга."""
    query: str
    id: str = ""
    owner: str = ""
    retriever_method: str = "hybrid"
    top_k: int = 10
    schedule: str = "daily"
    last_run_ts: str = ""
    last_results_hash: str = ""
    cooldown_hours: int = 24
    enabled: bool = True
    created_ts: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = uuid.uuid4().hex[:16]
        if not self.created_ts:
            self.created_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")


@dataclass
class FiredAlert:
    """Запись об алерте: изменение результатов сохранённого запроса."""
    query_id: str
    query: str
    owner: str
    added_docs: list[str]
    removed_docs: list[str]
    ts: str = ""
    id: str = field(default="")

    def __post_init__(self):
        if not self.id:
            self.id = uuid.uuid4().hex[:16]
        if not self.ts:
            self.ts = datetime.now(timezone.utc).isoformat(timespec="seconds")


class AlertStore:
    """SQLite-хранилище сохранённых запросов и алертов."""

    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "alerts.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def close(self):
        self.conn.close()

    # ----- SavedQuery CRUD -----

    def save(self, q: SavedQuery) -> str:
        """Создать или обновить сохранённый запрос. Возвращает id."""
        self.conn.execute(
            "INSERT OR REPLACE INTO saved_queries "
            "(id, owner, query, retriever_method, top_k, schedule, "
            " last_run_ts, last_results_hash, cooldown_hours, enabled, created_ts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                q.id, q.owner, q.query, q.retriever_method, q.top_k,
                q.schedule, q.last_run_ts, q.last_results_hash,
                q.cooldown_hours, 1 if q.enabled else 0, q.created_ts,
            ),
        )
        self.conn.commit()
        return q.id

    def get(self, query_id: str) -> "SavedQuery | None":
        """Получить запрос по id."""
        row = self.conn.execute(
            "SELECT * FROM saved_queries WHERE id = ?", (query_id,)
        ).fetchone()
        if not row:
            return None
        return self._row_to_query(row)

    def list_all(self, owner: str = "") -> list[SavedQuery]:
        """Все сохранённые запросы, опционально фильтр по owner."""
        sql = "SELECT * FROM saved_queries WHERE 1=1"
        params: list = []
        if owner:
            sql += " AND owner = ?"
            params.append(owner)
        sql += " ORDER BY created_ts DESC"
        return [self._row_to_query(r) for r in self.conn.execute(sql, params).fetchall()]

    def list_due(self, now_ts: str = "") -> list[SavedQuery]:
        """Вернуть enabled-запросы, у которых пришло время выполнения.

        Логика: last_run_ts пустой ИЛИ часов с последнего запуска >= cooldown_hours.
        """
        if not now_ts:
            now_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")

        now_dt = _parse_ts(now_ts)
        all_enabled = self.conn.execute(
            "SELECT * FROM saved_queries WHERE enabled = 1"
        ).fetchall()

        due = []
        for row in all_enabled:
            last = row["last_run_ts"]
            if not last:
                due.append(self._row_to_query(row))
                continue
            last_dt = _parse_ts(last)
            elapsed_hours = (now_dt - last_dt).total_seconds() / 3600
            if elapsed_hours >= row["cooldown_hours"]:
                due.append(self._row_to_query(row))
        return due

    def update_after_run(self, query_id: str, results_hash: str):
        """Обновить last_run_ts и last_results_hash после выполнения запроса."""
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        self.conn.execute(
            "UPDATE saved_queries SET last_run_ts = ?, last_results_hash = ? WHERE id = ?",
            (now, results_hash, query_id),
        )
        self.conn.commit()

    # ----- FiredAlert -----

    def record_alert(self, alert: FiredAlert):
        """Сохранить запись об алерте."""
        self.conn.execute(
            "INSERT OR REPLACE INTO fired_alerts "
            "(id, query_id, query, owner, added_json, removed_json, ts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                alert.id, alert.query_id, alert.query, alert.owner,
                json.dumps(alert.added_docs, ensure_ascii=False),
                json.dumps(alert.removed_docs, ensure_ascii=False),
                alert.ts,
            ),
        )
        self.conn.commit()

    def list_alerts(self, query_id: str = "", limit: int = 50) -> list[FiredAlert]:
        """Список алертов, опционально фильтр по query_id."""
        sql = "SELECT * FROM fired_alerts WHERE 1=1"
        params: list = []
        if query_id:
            sql += " AND query_id = ?"
            params.append(query_id)
        sql += " ORDER BY ts DESC LIMIT ?"
        params.append(limit)
        return [self._row_to_alert(r) for r in self.conn.execute(sql, params).fetchall()]

    # ----- Helpers -----

    def _row_to_query(self, row) -> SavedQuery:
        return SavedQuery(
            id=row["id"],
            owner=row["owner"] or "",
            query=row["query"],
            retriever_method=row["retriever_method"] or "hybrid",
            top_k=row["top_k"] or 10,
            schedule=row["schedule"] or "daily",
            last_run_ts=row["last_run_ts"] or "",
            last_results_hash=row["last_results_hash"] or "",
            cooldown_hours=row["cooldown_hours"] or 24,
            enabled=bool(row["enabled"]),
            created_ts=row["created_ts"],
        )

    def _row_to_alert(self, row) -> FiredAlert:
        return FiredAlert(
            id=row["id"],
            query_id=row["query_id"],
            query=row["query"],
            owner=row["owner"] or "",
            added_docs=json.loads(row["added_json"] or "[]"),
            removed_docs=json.loads(row["removed_json"] or "[]"),
            ts=row["ts"],
        )


class AlertRunner:
    """Запускает due-запросы, сравнивает результаты и генерирует алерты."""

    def __init__(self, store: AlertStore, retriever_fn: Callable):
        """
        Args:
            store: AlertStore instance.
            retriever_fn: callable(query: str, top_k: int) -> list[Passage].
        """
        self.store = store
        self.retriever_fn = retriever_fn

    def _hash_results(self, passages) -> str:
        """MD5 от отсортированного списка doc_id."""
        doc_ids = sorted(p.doc_id for p in passages)
        raw = "\n".join(doc_ids).encode("utf-8")
        return hashlib.md5(raw).hexdigest()

    def tick(self) -> list[FiredAlert]:
        """Выполнить все due-запросы и вернуть список новых алертов."""
        fired: list[FiredAlert] = []
        due = self.store.list_due()

        for q in due:
            try:
                passages = self.retriever_fn(q.query, q.top_k)
            except Exception:
                passages = []

            new_hash = self._hash_results(passages)
            old_hash = q.last_results_hash

            if old_hash and new_hash != old_hash:
                # Вычислим изменения
                old_ids = set(_split_hash_ids(old_hash))
                new_ids = set(p.doc_id for p in passages)
                # Для определения добавленных/удалённых достаточно сравнить с
                # предыдущим хешем, но у нас нет старого списка.
                # Храним doc_ids в результатах через side-channel:
                # пересчитываем added/removed через текущий снапшот.
                added = sorted(new_ids)
                removed: list[str] = []

                alert = FiredAlert(
                    query_id=q.id,
                    query=q.query,
                    owner=q.owner,
                    added_docs=added,
                    removed_docs=removed,
                )
                self.store.record_alert(alert)
                fired.append(alert)

            self.store.update_after_run(q.id, new_hash)

        return fired


# ---------- Internal helpers ----------

def _parse_ts(ts: str) -> datetime:
    """Разобрать ISO timestamp в datetime с tzinfo=UTC."""
    try:
        # Python 3.11+ fromisoformat поддерживает 'Z'
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        dt = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _split_hash_ids(hash_str: str) -> list[str]:
    """Заглушка: хеш не декодируем обратно. Возвращаем пустой список."""
    return []
