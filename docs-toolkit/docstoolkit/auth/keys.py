"""API key store с SQLite backend."""
import hashlib
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from docstoolkit.config import load_config


SCHEMA = """
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key_hash TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    scopes_json TEXT NOT NULL,
    created_ts TEXT NOT NULL,
    last_used_ts TEXT,
    revoked INTEGER DEFAULT 0,
    notes TEXT
);
CREATE INDEX IF NOT EXISTS idx_keys_hash ON api_keys(key_hash);
CREATE INDEX IF NOT EXISTS idx_keys_revoked ON api_keys(revoked);
"""

KEY_PREFIX = "dt_"
KEY_LENGTH = 32


@dataclass
class ApiKey:
    id: int
    key_hash: str
    name: str
    scopes: list[str]
    created_ts: str
    last_used_ts: str | None
    revoked: bool = False
    notes: str = ""


def generate_key() -> str:
    """Генерирует новый ключ: dt_<32-byte-hex>."""
    return KEY_PREFIX + secrets.token_hex(KEY_LENGTH)


def hash_key(key: str) -> str:
    """SHA-256 хэш ключа (для хранения)."""
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


class KeyStore:
    def __init__(self, db_path: Path | None = None):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "api_keys.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def close(self):
        self.conn.close()

    def create(self, name: str, scopes: list[str],
               notes: str = "") -> tuple[str, ApiKey]:
        """Создаёт новый key. Возвращает (plain_key, ApiKey).
        plain_key показывается ОДИН РАЗ — потом только hash."""
        import json as _json
        plain_key = generate_key()
        key_h = hash_key(plain_key)
        now = datetime.now().isoformat(timespec='seconds')
        cur = self.conn.execute(
            "INSERT INTO api_keys (key_hash, name, scopes_json, created_ts, notes) "
            "VALUES (?, ?, ?, ?, ?)",
            (key_h, name, _json.dumps(scopes), now, notes)
        )
        self.conn.commit()
        api_key = ApiKey(
            id=cur.lastrowid, key_hash=key_h, name=name,
            scopes=scopes, created_ts=now, last_used_ts=None, notes=notes,
        )
        return plain_key, api_key

    def verify(self, plain_key: str) -> ApiKey | None:
        """Проверяет key. Возвращает ApiKey или None."""
        if not plain_key.startswith(KEY_PREFIX):
            return None
        key_h = hash_key(plain_key)
        row = self.conn.execute(
            "SELECT * FROM api_keys WHERE key_hash = ? AND revoked = 0",
            (key_h,)
        ).fetchone()
        if not row:
            return None
        # Update last_used
        self.conn.execute(
            "UPDATE api_keys SET last_used_ts = ? WHERE id = ?",
            (datetime.now().isoformat(timespec='seconds'), row["id"])
        )
        self.conn.commit()
        return self._row_to_key(row)

    def list(self, include_revoked: bool = False) -> list[ApiKey]:
        sql = "SELECT * FROM api_keys"
        if not include_revoked:
            sql += " WHERE revoked = 0"
        sql += " ORDER BY id"
        return [self._row_to_key(r) for r in self.conn.execute(sql).fetchall()]

    def revoke(self, key_id: int) -> bool:
        cur = self.conn.execute(
            "UPDATE api_keys SET revoked = 1 WHERE id = ?", (key_id,)
        )
        self.conn.commit()
        return cur.rowcount > 0

    def revoke_by_name(self, name: str) -> int:
        cur = self.conn.execute(
            "UPDATE api_keys SET revoked = 1 WHERE name = ?", (name,)
        )
        self.conn.commit()
        return cur.rowcount

    def _row_to_key(self, row) -> ApiKey:
        import json as _json
        return ApiKey(
            id=row["id"],
            key_hash=row["key_hash"],
            name=row["name"],
            scopes=_json.loads(row["scopes_json"]),
            created_ts=row["created_ts"],
            last_used_ts=row["last_used_ts"],
            revoked=bool(row["revoked"]),
            notes=row["notes"] or "",
        )
