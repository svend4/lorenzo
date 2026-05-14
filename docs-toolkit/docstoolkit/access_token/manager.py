"""Opaque access token issuance and validation.

This module implements short-lived opaque access tokens backed by an
in-memory store. Tokens are HMAC-SHA256 signed so that even without
storage, a corrupted/forged token can be detected at parse time.

Wire format
-----------

    token_string = base64url( token_id || "." || hex(hmac_sha256(secret, token_id)) )

where ``token_id = secrets.token_hex(16)`` — a 32-character hex string.

Only stdlib is used: ``secrets``, ``hashlib``, ``hmac``, ``base64``,
``threading``. There is no JWT, no third-party crypto.
"""

from __future__ import annotations

import base64
import hmac
import hashlib
import secrets
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TokenStatus(Enum):
    """Outcome of a token validation attempt."""

    VALID = "valid"
    EXPIRED = "expired"
    REVOKED = "revoked"
    INVALID = "invalid"


@dataclass
class Token:
    """Server-side record of an issued token."""

    token_id: str
    subject: str
    scopes: list[str]
    created_at: float
    expires_at: float
    metadata: dict = field(default_factory=dict)
    revoked: bool = False


@dataclass
class ValidationResult:
    """Result of validating a token string."""

    status: TokenStatus
    token: Optional[Token] = None
    reason: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        return self.status is TokenStatus.VALID


def _now(now: float) -> float:
    """Return ``now`` if non-zero, otherwise current wall-clock time.

    The 0.0 sentinel makes tests deterministic while letting callers
    omit the argument in production.
    """

    if now and now > 0:
        return now
    return time.time()


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    pad = (-len(s)) % 4
    return base64.urlsafe_b64decode(s + ("=" * pad))


class TokenManager:
    """Issue, validate and revoke opaque access tokens.

    Tokens are stored in-process behind a ``threading.Lock``; the
    manager is safe to share between threads but is not persistent.
    """

    def __init__(self, secret: str):
        if not isinstance(secret, str) or not secret:
            raise ValueError("secret must be a non-empty string")
        self._secret = secret.encode("utf-8")
        self._tokens: dict[str, Token] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Issuance
    # ------------------------------------------------------------------
    def issue(
        self,
        subject: str,
        scopes: Optional[list[str]] = None,
        ttl: float = 3600,
        metadata: Optional[dict] = None,
        now: float = 0.0,
    ) -> tuple[str, Token]:
        """Issue a new token for ``subject``.

        Returns the wire ``(token_string, Token)`` tuple. ``ttl`` is
        measured in seconds and may be zero or negative for testing.
        """

        if not isinstance(subject, str) or not subject:
            raise ValueError("subject must be a non-empty string")

        ts = _now(now)
        token_id = secrets.token_hex(16)
        token = Token(
            token_id=token_id,
            subject=subject,
            scopes=list(scopes) if scopes else [],
            created_at=ts,
            expires_at=ts + float(ttl),
            metadata=dict(metadata) if metadata else {},
            revoked=False,
        )
        with self._lock:
            self._tokens[token_id] = token
        token_string = self._encode(token_id)
        return token_string, token

    def _sign(self, token_id: str) -> str:
        mac = hmac.new(self._secret, token_id.encode("ascii"), hashlib.sha256)
        return mac.hexdigest()

    def _encode(self, token_id: str) -> str:
        sig = self._sign(token_id)
        payload = f"{token_id}.{sig}".encode("ascii")
        return _b64url_encode(payload)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate(
        self,
        token_string: str,
        now: float = 0.0,
        required_scopes: Optional[list[str]] = None,
    ) -> ValidationResult:
        """Validate ``token_string`` against the in-memory store."""

        if not isinstance(token_string, str) or not token_string:
            return ValidationResult(
                TokenStatus.INVALID, None, "empty token string"
            )

        # Decode wire format
        try:
            raw = _b64url_decode(token_string).decode("ascii")
        except Exception:
            return ValidationResult(
                TokenStatus.INVALID, None, "malformed base64"
            )

        if raw.count(".") != 1:
            return ValidationResult(
                TokenStatus.INVALID, None, "malformed payload"
            )
        token_id, signature = raw.split(".", 1)
        if not token_id or not signature:
            return ValidationResult(
                TokenStatus.INVALID, None, "malformed payload"
            )

        expected = self._sign(token_id)
        if not hmac.compare_digest(expected, signature):
            return ValidationResult(
                TokenStatus.INVALID, None, "signature mismatch"
            )

        with self._lock:
            token = self._tokens.get(token_id)
        if token is None:
            return ValidationResult(
                TokenStatus.INVALID, None, "unknown token"
            )

        ts = _now(now)
        if ts >= token.expires_at:
            return ValidationResult(TokenStatus.EXPIRED, token, "expired")

        if token.revoked:
            return ValidationResult(TokenStatus.REVOKED, token, "revoked")

        if required_scopes:
            missing = [s for s in required_scopes if s not in token.scopes]
            if missing:
                return ValidationResult(
                    TokenStatus.INVALID,
                    token,
                    f"missing scopes: {', '.join(missing)}",
                )

        return ValidationResult(TokenStatus.VALID, token, None)

    # ------------------------------------------------------------------
    # Revocation
    # ------------------------------------------------------------------
    def revoke(self, token_id: str) -> bool:
        """Mark a single token as revoked. Returns True if found."""

        with self._lock:
            token = self._tokens.get(token_id)
            if token is None:
                return False
            if token.revoked:
                return False
            token.revoked = True
            return True

    def revoke_subject(self, subject: str) -> int:
        """Revoke every active token belonging to ``subject``.

        Returns the number of tokens flipped to revoked on this call.
        """

        count = 0
        with self._lock:
            for token in self._tokens.values():
                if token.subject == subject and not token.revoked:
                    token.revoked = True
                    count += 1
        return count

    # ------------------------------------------------------------------
    # Inspection / maintenance
    # ------------------------------------------------------------------
    def get(self, token_id: str) -> Optional[Token]:
        with self._lock:
            return self._tokens.get(token_id)

    def cleanup_expired(self, now: float = 0.0) -> int:
        """Drop expired tokens from storage. Returns count removed."""

        ts = _now(now)
        with self._lock:
            expired_ids = [
                tid for tid, tok in self._tokens.items() if ts >= tok.expires_at
            ]
            for tid in expired_ids:
                del self._tokens[tid]
        return len(expired_ids)

    @property
    def count(self) -> int:
        with self._lock:
            return len(self._tokens)

    def active_count(self, now: float = 0.0) -> int:
        """Count tokens that would currently validate as VALID."""

        ts = _now(now)
        with self._lock:
            return sum(
                1
                for tok in self._tokens.values()
                if not tok.revoked and ts < tok.expires_at
            )

    def tokens_for_subject(self, subject: str) -> list[Token]:
        with self._lock:
            return [t for t in self._tokens.values() if t.subject == subject]

    def clear(self) -> None:
        with self._lock:
            self._tokens.clear()
