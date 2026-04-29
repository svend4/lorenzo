"""SQLite conversation store + context-window management."""
import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from docstoolkit.config import load_config


SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    user TEXT,
    title TEXT,
    skill TEXT,
    metadata_json TEXT,
    created_ts TEXT NOT NULL,
    updated_ts TEXT NOT NULL,
    summary TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_sess_user ON sessions(user);
CREATE INDEX IF NOT EXISTS idx_sess_updated ON sessions(updated_ts);

CREATE TABLE IF NOT EXISTS messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,                 -- system | user | assistant | tool
    content TEXT NOT NULL,
    tokens INTEGER DEFAULT 0,
    metadata_json TEXT,
    ts TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
CREATE INDEX IF NOT EXISTS idx_msg_session ON messages(session_id);
CREATE INDEX IF NOT EXISTS idx_msg_ts ON messages(ts);
"""


@dataclass
class Session:
    id: str = ""
    user: str = ""
    title: str = ""
    skill: str = ""
    metadata: dict = field(default_factory=dict)
    created_ts: str = ""
    updated_ts: str = ""
    summary: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = uuid.uuid4().hex[:16]
        if not self.created_ts:
            self.created_ts = datetime.now().isoformat(timespec='seconds')
        if not self.updated_ts:
            self.updated_ts = self.created_ts


@dataclass
class Message:
    id: str = ""
    session_id: str = ""
    role: str = "user"
    content: str = ""
    tokens: int = 0
    metadata: dict = field(default_factory=dict)
    ts: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = uuid.uuid4().hex[:12]
        if not self.ts:
            self.ts = datetime.now().isoformat(timespec='seconds')
        if not self.tokens:
            # rough estimate: 1 token ≈ 3 chars (conservative)
            self.tokens = max(1, len(self.content) // 3)


class ConversationStore:
    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "conversations.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    # ---- sessions ----
    def create_session(self, *, user: str = "", title: str = "",
                       skill: str = "", metadata: dict | None = None) -> str:
        s = Session(user=user, title=title, skill=skill,
                    metadata=metadata or {})
        self.conn.execute(
            "INSERT INTO sessions "
            "(id, user, title, skill, metadata_json, created_ts, updated_ts, summary) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (s.id, s.user, s.title, s.skill,
             json.dumps(s.metadata, ensure_ascii=False),
             s.created_ts, s.updated_ts, s.summary),
        )
        self.conn.commit()
        return s.id

    def get_session(self, sid: str) -> Session | None:
        row = self.conn.execute(
            "SELECT * FROM sessions WHERE id = ?", (sid,)
        ).fetchone()
        if not row:
            return None
        return self._row_to_session(row)

    def list_sessions(self, user: str = "", limit: int = 50) -> list[Session]:
        if user:
            rows = self.conn.execute(
                "SELECT * FROM sessions WHERE user = ? "
                "ORDER BY updated_ts DESC LIMIT ?",
                (user, limit),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT * FROM sessions ORDER BY updated_ts DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [self._row_to_session(r) for r in rows]

    def delete_session(self, sid: str) -> None:
        self.conn.execute("DELETE FROM messages WHERE session_id = ?", (sid,))
        self.conn.execute("DELETE FROM sessions WHERE id = ?", (sid,))
        self.conn.commit()

    def update_summary(self, sid: str, summary: str) -> None:
        self.conn.execute(
            "UPDATE sessions SET summary = ?, updated_ts = ? WHERE id = ?",
            (summary, datetime.now().isoformat(timespec='seconds'), sid),
        )
        self.conn.commit()

    # ---- messages ----
    def append(self, sid: str, *, role: str, content: str,
               metadata: dict | None = None) -> str:
        m = Message(session_id=sid, role=role, content=content,
                    metadata=metadata or {})
        self.conn.execute(
            "INSERT INTO messages "
            "(id, session_id, role, content, tokens, metadata_json, ts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (m.id, m.session_id, m.role, m.content, m.tokens,
             json.dumps(m.metadata, ensure_ascii=False), m.ts),
        )
        self.conn.execute(
            "UPDATE sessions SET updated_ts = ? WHERE id = ?",
            (m.ts, sid),
        )
        self.conn.commit()
        return m.id

    def messages(self, sid: str, *, limit: int = 1000) -> list[Message]:
        rows = self.conn.execute(
            "SELECT * FROM messages WHERE session_id = ? "
            "ORDER BY ts ASC LIMIT ?",
            (sid, limit),
        ).fetchall()
        return [self._row_to_message(r) for r in rows]

    # ---- context-window management ----
    def history_for_llm(self, sid: str, *, max_tokens: int = 4000,
                         summarize_old: bool = True,
                         system_prompt: str = "") -> list[dict]:
        """Возвращает список {role, content} для отправки в LLM.

        Логика:
          1. Берём system_prompt (если есть) + summary сессии (если есть)
          2. Добавляем сообщения с конца (newest first), пока токены не превысят бюджет
          3. Возвращаем в хронологическом порядке.
        """
        msgs = self.messages(sid)
        sess = self.get_session(sid)

        result: list[dict] = []
        if system_prompt:
            result.append({"role": "system", "content": system_prompt})

        if sess and sess.summary and summarize_old:
            result.append({"role": "system",
                           "content": f"[История сессии]: {sess.summary}"})

        # Tail-fit
        used_tokens = sum(len(r["content"]) // 3 for r in result)
        keep: list[Message] = []
        for m in reversed(msgs):
            cost = m.tokens
            if used_tokens + cost > max_tokens and keep:
                # Не помещается, и уже что-то есть — стоп
                break
            keep.append(m)
            used_tokens += cost

        keep.reverse()
        for m in keep:
            result.append({"role": m.role, "content": m.content})
        return result

    def squash_old(self, sid: str, *, keep_last: int = 6,
                    summarizer=None) -> str:
        """Обновляет session.summary из старых сообщений.

        summarizer(messages: list[Message]) -> str
        Если None — простая heuristic: первые слова user/assistant сообщений.
        Удаляет старые messages из БД (оставляет последние keep_last).
        """
        msgs = self.messages(sid)
        if len(msgs) <= keep_last:
            return ""

        old = msgs[:-keep_last] if keep_last > 0 else msgs
        new_summary = (summarizer(old) if summarizer
                        else _heuristic_summary(old))
        sess = self.get_session(sid)
        prev = sess.summary if sess else ""
        full = (prev + "\n" + new_summary).strip() if prev else new_summary
        self.update_summary(sid, full)

        # удалить squashed
        ids_to_drop = [m.id for m in old]
        if ids_to_drop:
            qmarks = ",".join("?" * len(ids_to_drop))
            self.conn.execute(
                f"DELETE FROM messages WHERE id IN ({qmarks})",
                ids_to_drop,
            )
            self.conn.commit()
        return new_summary

    # ---- internals ----
    def _row_to_session(self, row) -> Session:
        return Session(
            id=row["id"], user=row["user"] or "",
            title=row["title"] or "", skill=row["skill"] or "",
            metadata=json.loads(row["metadata_json"] or "{}"),
            created_ts=row["created_ts"], updated_ts=row["updated_ts"],
            summary=row["summary"] or "",
        )

    def _row_to_message(self, row) -> Message:
        return Message(
            id=row["id"], session_id=row["session_id"],
            role=row["role"], content=row["content"],
            tokens=row["tokens"] or 0,
            metadata=json.loads(row["metadata_json"] or "{}"),
            ts=row["ts"],
        )


def _heuristic_summary(msgs: list[Message]) -> str:
    """Простой fallback summary: ключевые user/assistant moves."""
    parts = []
    for m in msgs:
        snippet = m.content.replace("\n", " ").strip()[:100]
        if not snippet:
            continue
        if m.role == "user":
            parts.append(f"U: {snippet}")
        elif m.role == "assistant":
            parts.append(f"A: {snippet}")
    return "; ".join(parts[:8])  # cap
