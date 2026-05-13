"""URL shortener implementation backed by SQLite."""
from __future__ import annotations

import hashlib
import sqlite3
import threading
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


DEFAULT_ALPHABET = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
)


@dataclass
class ShortUrl:
    """A shortened URL record."""

    short_code: str
    original_url: str
    created_at: float
    click_count: int = 0
    expires_at: Optional[float] = None


@dataclass
class ShortenerStats:
    """Aggregate statistics about stored short URLs."""

    total_urls: int
    total_clicks: int
    most_clicked: List[Tuple[str, int]] = field(default_factory=list)
    oldest_at: Optional[float] = None


@dataclass
class ShortenerConfig:
    """Configuration for UrlShortener."""

    code_length: int = 7
    db_path: str = ":memory:"
    alphabet: str = DEFAULT_ALPHABET


class UrlShortener:
    """Generates short codes for URLs and persists them to SQLite."""

    _CREATE_TABLE = """
    CREATE TABLE IF NOT EXISTS short_urls (
        short_code   TEXT PRIMARY KEY,
        original_url TEXT NOT NULL,
        created_at   REAL NOT NULL,
        click_count  INTEGER NOT NULL DEFAULT 0,
        expires_at   REAL
    )
    """

    _CREATE_INDEXES = [
        "CREATE INDEX IF NOT EXISTS idx_short_urls_created_at ON short_urls(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_short_urls_clicks     ON short_urls(click_count)",
    ]

    def __init__(self, config: Optional[ShortenerConfig] = None) -> None:
        self._config = config or ShortenerConfig()
        if self._config.code_length <= 0:
            raise ValueError("code_length must be positive")
        if not self._config.alphabet:
            raise ValueError("alphabet must be non-empty")
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(
            self._config.db_path, check_same_thread=False
        )
        self._conn.row_factory = sqlite3.Row
        self._setup()

    # ------------------------------------------------------------------
    # Setup
    # ------------------------------------------------------------------

    def _setup(self) -> None:
        cur = self._conn.cursor()
        cur.execute(self._CREATE_TABLE)
        for stmt in self._CREATE_INDEXES:
            cur.execute(stmt)
        self._conn.commit()

    # ------------------------------------------------------------------
    # Code generation
    # ------------------------------------------------------------------

    def _encode(self, digest: bytes) -> str:
        """Convert raw bytes into a string using the configured alphabet."""
        alphabet = self._config.alphabet
        base = len(alphabet)
        # Treat the digest as a big-endian integer and convert into base-N.
        n = int.from_bytes(digest, "big")
        if n == 0:
            return alphabet[0] * self._config.code_length
        chars = []
        length = self._config.code_length
        while n > 0 and len(chars) < length * 2:
            chars.append(alphabet[n % base])
            n //= base
        # Take the first `code_length` characters.
        encoded = "".join(reversed(chars))
        if len(encoded) >= length:
            return encoded[:length]
        # Pad with the first alphabet char if too short (very unlikely).
        return encoded.rjust(length, alphabet[0])

    def _generate_code(self, url: str, now: float) -> str:
        """Generate a unique short code for *url*.

        Hashes URL + timestamp + counter; on collisions, increments counter.
        """
        counter = 0
        while True:
            payload = f"{url}|{now}|{counter}".encode("utf-8")
            digest = hashlib.sha256(payload).digest()
            code = self._encode(digest)
            if not self._exists_locked(code):
                return code
            counter += 1
            if counter > 1_000_000:  # pragma: no cover - safety net
                raise RuntimeError("Unable to generate unique short code")

    def _validate_custom_code(self, code: str) -> None:
        if not code:
            raise ValueError("custom_code must be non-empty")
        alphabet_set = set(self._config.alphabet)
        for ch in code:
            if ch not in alphabet_set:
                raise ValueError(
                    f"custom_code contains character {ch!r} not in alphabet"
                )

    # ------------------------------------------------------------------
    # Internal queries
    # ------------------------------------------------------------------

    def _exists_locked(self, short_code: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM short_urls WHERE short_code = ?", (short_code,)
        ).fetchone()
        return row is not None

    @staticmethod
    def _row_to_short_url(row: sqlite3.Row) -> ShortUrl:
        return ShortUrl(
            short_code=row["short_code"],
            original_url=row["original_url"],
            created_at=row["created_at"],
            click_count=row["click_count"],
            expires_at=row["expires_at"],
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def shorten(
        self,
        url: str,
        custom_code: Optional[str] = None,
        expires_at: Optional[float] = None,
        now: float = 0.0,
    ) -> ShortUrl:
        """Shorten *url*. Returns the stored ShortUrl record."""
        if url is None:
            raise ValueError("url must not be None")
        with self._lock:
            if custom_code is not None:
                self._validate_custom_code(custom_code)
                if self._exists_locked(custom_code):
                    raise ValueError(
                        f"short_code {custom_code!r} already exists"
                    )
                code = custom_code
            else:
                code = self._generate_code(url, now)

            self._conn.execute(
                """
                INSERT INTO short_urls
                    (short_code, original_url, created_at, click_count, expires_at)
                VALUES (?, ?, ?, 0, ?)
                """,
                (code, url, now, expires_at),
            )
            self._conn.commit()

            return ShortUrl(
                short_code=code,
                original_url=url,
                created_at=now,
                click_count=0,
                expires_at=expires_at,
            )

    def expand(
        self, short_code: str, now: float = 0.0
    ) -> Optional[ShortUrl]:
        """Return the ShortUrl for *short_code*, or None if missing/expired."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM short_urls WHERE short_code = ?",
                (short_code,),
            ).fetchone()
            if row is None:
                return None
            short_url = self._row_to_short_url(row)
            if (
                short_url.expires_at is not None
                and now >= short_url.expires_at
            ):
                return None
            return short_url

    def visit(self, short_code: str, now: float = 0.0) -> Optional[str]:
        """Increment click_count and return the original URL, or None."""
        with self._lock:
            row = self._conn.execute(
                "SELECT * FROM short_urls WHERE short_code = ?",
                (short_code,),
            ).fetchone()
            if row is None:
                return None
            expires_at = row["expires_at"]
            if expires_at is not None and now >= expires_at:
                return None
            self._conn.execute(
                "UPDATE short_urls SET click_count = click_count + 1 "
                "WHERE short_code = ?",
                (short_code,),
            )
            self._conn.commit()
            return row["original_url"]

    def delete(self, short_code: str) -> bool:
        """Delete *short_code*. Returns True if a row was removed."""
        with self._lock:
            cur = self._conn.execute(
                "DELETE FROM short_urls WHERE short_code = ?", (short_code,)
            )
            self._conn.commit()
            return cur.rowcount > 0

    def exists(self, short_code: str) -> bool:
        """Return True if *short_code* is currently stored."""
        with self._lock:
            return self._exists_locked(short_code)

    def list_all(self, limit: Optional[int] = None) -> List[ShortUrl]:
        """List all stored ShortUrl records, newest first."""
        with self._lock:
            if limit is not None:
                rows = self._conn.execute(
                    "SELECT * FROM short_urls ORDER BY created_at DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            else:
                rows = self._conn.execute(
                    "SELECT * FROM short_urls ORDER BY created_at DESC"
                ).fetchall()
            return [self._row_to_short_url(r) for r in rows]

    def stats(self) -> ShortenerStats:
        """Return aggregate stats over all stored URLs."""
        with self._lock:
            total_urls_row = self._conn.execute(
                "SELECT COUNT(*) AS c, COALESCE(SUM(click_count), 0) AS s, "
                "MIN(created_at) AS oldest FROM short_urls"
            ).fetchone()
            total_urls = total_urls_row["c"] or 0
            total_clicks = total_urls_row["s"] or 0
            oldest_at = total_urls_row["oldest"]

            most_clicked_rows = self._conn.execute(
                "SELECT short_code, click_count FROM short_urls "
                "WHERE click_count > 0 "
                "ORDER BY click_count DESC, short_code ASC LIMIT 10"
            ).fetchall()
            most_clicked = [
                (r["short_code"], r["click_count"]) for r in most_clicked_rows
            ]
            return ShortenerStats(
                total_urls=total_urls,
                total_clicks=total_clicks,
                most_clicked=most_clicked,
                oldest_at=oldest_at,
            )

    def cleanup_expired(self, now: float = 0.0) -> int:
        """Delete every URL whose expires_at is <= now. Returns count."""
        with self._lock:
            cur = self._conn.execute(
                "DELETE FROM short_urls WHERE expires_at IS NOT NULL "
                "AND expires_at <= ?",
                (now,),
            )
            self._conn.commit()
            return cur.rowcount

    @property
    def count(self) -> int:
        """Total stored short URLs."""
        with self._lock:
            row = self._conn.execute(
                "SELECT COUNT(*) AS c FROM short_urls"
            ).fetchone()
            return row["c"] or 0

    def close(self) -> None:
        """Close the underlying database connection."""
        self._conn.close()
