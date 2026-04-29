"""Webhook dispatcher: SQLite-backed subscription registry + HTTP delivery."""
import hashlib
import hmac
import json
import sqlite3
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from docstoolkit.config import load_config


SCHEMA = """
CREATE TABLE IF NOT EXISTS subscriptions (
    id TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    events_csv TEXT NOT NULL,        -- "*" | "job.*" | "job.done,feedback.received"
    secret TEXT,
    headers_json TEXT,
    active INTEGER DEFAULT 1,
    created_ts TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sub_active ON subscriptions(active);

CREATE TABLE IF NOT EXISTS deliveries (
    id TEXT PRIMARY KEY,
    sub_id TEXT NOT NULL,
    event TEXT NOT NULL,
    payload_json TEXT,
    status TEXT NOT NULL,            -- pending | sent | failed | dead
    attempts INTEGER DEFAULT 0,
    last_error TEXT,
    response_code INTEGER,
    sent_ts TEXT,
    created_ts TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_del_status ON deliveries(status);
CREATE INDEX IF NOT EXISTS idx_del_sub ON deliveries(sub_id);
"""


class DeliveryStatus:
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    DEAD = "dead"                    # max retries exhausted


@dataclass
class Subscription:
    """Подписка одного endpoint'а на список событий."""
    id: str = ""
    url: str = ""
    events: list[str] = field(default_factory=lambda: ["*"])
    secret: str = ""                 # для HMAC-SHA256 signing
    headers: dict = field(default_factory=dict)
    active: bool = True
    created_ts: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = uuid.uuid4().hex[:12]
        if not self.created_ts:
            self.created_ts = datetime.now().isoformat(timespec='seconds')

    def matches(self, event: str) -> bool:
        for pattern in self.events:
            if pattern == "*" or pattern == event:
                return True
            if pattern.endswith(".*") and event.startswith(pattern[:-1]):
                return True
        return False


@dataclass
class Delivery:
    """Одна попытка доставки."""
    id: str = ""
    sub_id: str = ""
    event: str = ""
    payload: dict = field(default_factory=dict)
    status: str = DeliveryStatus.PENDING
    attempts: int = 0
    last_error: str = ""
    response_code: int = 0
    sent_ts: str = ""
    created_ts: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = uuid.uuid4().hex[:12]
        if not self.created_ts:
            self.created_ts = datetime.now().isoformat(timespec='seconds')


def sign_payload(payload: dict, secret: str) -> str:
    """HMAC-SHA256(json(payload)) → hex digest. Empty secret → ''."""
    if not secret:
        return ""
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode()
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


class WebhookDispatcher:
    def __init__(self, db_path: Path | None = None,
                 *, http_send=None, max_retries: int = 3,
                 retry_backoff_s: float = 1.0):
        if db_path is None:
            cfg = load_config()
            db_path = cfg.root / ".docstoolkit" / "webhooks.sqlite"
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.path))
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)
        self.http_send = http_send or _default_http_send
        self.max_retries = max_retries
        self.retry_backoff_s = retry_backoff_s

    def close(self):
        self.conn.close()

    # ---- subscriptions ----
    def subscribe(self, sub: Subscription) -> str:
        self.conn.execute(
            "INSERT OR REPLACE INTO subscriptions "
            "(id, url, events_csv, secret, headers_json, active, created_ts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (sub.id, sub.url, ",".join(sub.events), sub.secret,
             json.dumps(sub.headers, ensure_ascii=False),
             int(sub.active), sub.created_ts),
        )
        self.conn.commit()
        return sub.id

    def unsubscribe(self, sub_id: str) -> None:
        self.conn.execute("DELETE FROM subscriptions WHERE id = ?", (sub_id,))
        self.conn.commit()

    def list_subscriptions(self, active_only: bool = True) -> list[Subscription]:
        if active_only:
            rows = self.conn.execute(
                "SELECT * FROM subscriptions WHERE active = 1"
            ).fetchall()
        else:
            rows = self.conn.execute("SELECT * FROM subscriptions").fetchall()
        return [self._row_to_sub(r) for r in rows]

    def matching_subscriptions(self, event: str) -> list[Subscription]:
        return [s for s in self.list_subscriptions() if s.matches(event)]

    # ---- dispatch ----
    def dispatch(self, *, event: str, payload: dict) -> list[Delivery]:
        """Отправляет event всем подписанным subs. Возвращает list[Delivery]."""
        subs = self.matching_subscriptions(event)
        deliveries = []
        for sub in subs:
            d = Delivery(sub_id=sub.id, event=event, payload=payload)
            self._save_delivery(d)
            self._attempt_delivery(d, sub)
            deliveries.append(d)
        return deliveries

    def retry_failed(self, *, max_to_retry: int = 50) -> int:
        """Повторяет deliveries в статусе failed (если attempts<max). Returns count."""
        rows = self.conn.execute(
            "SELECT * FROM deliveries WHERE status = ? "
            "AND attempts < ? ORDER BY created_ts ASC LIMIT ?",
            (DeliveryStatus.FAILED, self.max_retries, max_to_retry),
        ).fetchall()
        retried = 0
        for r in rows:
            d = self._row_to_delivery(r)
            sub = self._get_sub(d.sub_id)
            if not sub:
                continue
            self._attempt_delivery(d, sub)
            retried += 1
        return retried

    def list_deliveries(self, *, status: str = "",
                         sub_id: str = "", limit: int = 100) -> list[Delivery]:
        sql = "SELECT * FROM deliveries WHERE 1=1"
        params: list = []
        if status:
            sql += " AND status = ?"
            params.append(status)
        if sub_id:
            sql += " AND sub_id = ?"
            params.append(sub_id)
        sql += " ORDER BY created_ts DESC LIMIT ?"
        params.append(limit)
        return [self._row_to_delivery(r)
                for r in self.conn.execute(sql, params).fetchall()]

    def stats(self) -> dict:
        out = {"subscriptions": 0, "active_subscriptions": 0}
        out["subscriptions"] = self.conn.execute(
            "SELECT COUNT(*) AS n FROM subscriptions"
        ).fetchone()["n"]
        out["active_subscriptions"] = self.conn.execute(
            "SELECT COUNT(*) AS n FROM subscriptions WHERE active=1"
        ).fetchone()["n"]
        for status in (DeliveryStatus.PENDING, DeliveryStatus.SENT,
                       DeliveryStatus.FAILED, DeliveryStatus.DEAD):
            out[f"deliveries_{status}"] = self.conn.execute(
                "SELECT COUNT(*) AS n FROM deliveries WHERE status = ?",
                (status,),
            ).fetchone()["n"]
        return out

    # ---- internals ----
    def _attempt_delivery(self, d: Delivery, sub: Subscription) -> None:
        d.attempts += 1
        signature = sign_payload(d.payload, sub.secret)
        headers = dict(sub.headers)
        headers["Content-Type"] = "application/json"
        headers["X-Lorenzo-Event"] = d.event
        headers["X-Lorenzo-Delivery-Id"] = d.id
        if signature:
            headers["X-Lorenzo-Signature"] = signature

        try:
            code, body = self.http_send(sub.url, d.payload, headers,
                                         timeout=10)
            d.response_code = code
            if 200 <= code < 300:
                d.status = DeliveryStatus.SENT
                d.sent_ts = datetime.now().isoformat(timespec='seconds')
                d.last_error = ""
            else:
                d.last_error = f"HTTP {code}: {body[:200]}"
                d.status = (DeliveryStatus.DEAD if d.attempts >= self.max_retries
                            else DeliveryStatus.FAILED)
        except Exception as e:
            d.last_error = f"{type(e).__name__}: {str(e)[:200]}"
            d.status = (DeliveryStatus.DEAD if d.attempts >= self.max_retries
                        else DeliveryStatus.FAILED)

        self._save_delivery(d)

    def _save_delivery(self, d: Delivery) -> None:
        self.conn.execute(
            "INSERT OR REPLACE INTO deliveries "
            "(id, sub_id, event, payload_json, status, attempts, "
            " last_error, response_code, sent_ts, created_ts) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (d.id, d.sub_id, d.event,
             json.dumps(d.payload, ensure_ascii=False),
             d.status, d.attempts, d.last_error,
             d.response_code, d.sent_ts, d.created_ts),
        )
        self.conn.commit()

    def _get_sub(self, sub_id: str) -> Subscription | None:
        row = self.conn.execute(
            "SELECT * FROM subscriptions WHERE id = ?", (sub_id,)
        ).fetchone()
        return self._row_to_sub(row) if row else None

    def _row_to_sub(self, row) -> Subscription:
        return Subscription(
            id=row["id"], url=row["url"],
            events=row["events_csv"].split(","),
            secret=row["secret"] or "",
            headers=json.loads(row["headers_json"] or "{}"),
            active=bool(row["active"]),
            created_ts=row["created_ts"],
        )

    def _row_to_delivery(self, row) -> Delivery:
        return Delivery(
            id=row["id"], sub_id=row["sub_id"], event=row["event"],
            payload=json.loads(row["payload_json"] or "{}"),
            status=row["status"], attempts=row["attempts"] or 0,
            last_error=row["last_error"] or "",
            response_code=row["response_code"] or 0,
            sent_ts=row["sent_ts"] or "",
            created_ts=row["created_ts"],
        )


def _default_http_send(url: str, payload: dict, headers: dict,
                        *, timeout: float = 10.0) -> tuple[int, str]:
    """Простая stdlib-only POST. Возвращает (code, body[:500])."""
    body = json.dumps(payload, ensure_ascii=False).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.getcode(), resp.read(500).decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read(500).decode(errors="replace") if e.fp else ""
    # Other URLError raises naturally to caller
