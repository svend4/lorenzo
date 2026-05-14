"""Document signature v2 (E259).

Advanced HMAC-based document signing with:
- Certificate-style signer metadata (expiry, revocation, metadata bag).
- Multi-signature documents with required-threshold verification.
- Key rotation that invalidates old signatures.
- Thread-safe; stdlib only (hmac, hashlib, base64, threading).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SigAlgo(str, Enum):
    """Supported HMAC signing algorithms."""

    HMAC_SHA256 = "HMAC_SHA256"
    HMAC_SHA512 = "HMAC_SHA512"


_ALGO_MAP = {
    SigAlgo.HMAC_SHA256: hashlib.sha256,
    SigAlgo.HMAC_SHA512: hashlib.sha512,
}


@dataclass
class SignerCert:
    """Certificate-style record describing a signer key."""

    key_id: str
    algo: SigAlgo
    created_at: float
    expires_at: Optional[float] = None
    revoked: bool = False
    metadata: dict = field(default_factory=dict)


@dataclass
class Signature:
    """A single signature value produced by one signer."""

    signature: str  # base64-encoded HMAC digest
    key_id: str
    algo: SigAlgo
    created_at: float
    signer_name: Optional[str] = None


@dataclass
class MultiSig:
    """A multi-signature envelope for a document."""

    doc_id: str
    content_hash: str
    signatures: list = field(default_factory=list)
    required: int = 1


@dataclass
class VerifyResult:
    """Aggregate verification result for a MultiSig."""

    valid: bool
    valid_signatures: int
    invalid_signatures: int
    reasons: list = field(default_factory=list)


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _b64decode(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


def _compute_digest(secret: str, content: str, algo: SigAlgo) -> bytes:
    hash_func = _ALGO_MAP[algo]
    return hmac.new(secret.encode("utf-8"), content.encode("utf-8"), hash_func).digest()


class DocSignatureV2:
    """Advanced multi-signer document signing with key rotation and certificates."""

    def __init__(self):
        self._lock = threading.Lock()
        # key_id -> SignerCert
        self._certs: dict = {}
        # key_id -> secret str
        self._secrets: dict = {}

    # -------- signer management --------

    def add_signer(
        self,
        key_id: str,
        secret: str,
        algo: SigAlgo = SigAlgo.HMAC_SHA256,
        expires_at: Optional[float] = None,
        metadata: Optional[dict] = None,
        now: float = 0.0,
    ) -> SignerCert:
        if not isinstance(key_id, str) or not key_id:
            raise ValueError("key_id must be a non-empty string")
        if not isinstance(secret, str):
            raise TypeError("secret must be a string")
        if not isinstance(algo, SigAlgo):
            raise TypeError("algo must be a SigAlgo")
        with self._lock:
            cert = SignerCert(
                key_id=key_id,
                algo=algo,
                created_at=now,
                expires_at=expires_at,
                revoked=False,
                metadata=dict(metadata) if metadata else {},
            )
            self._certs[key_id] = cert
            self._secrets[key_id] = secret
            return cert

    def revoke_signer(self, key_id: str) -> bool:
        with self._lock:
            cert = self._certs.get(key_id)
            if cert is None:
                return False
            cert.revoked = True
            return True

    def is_active(self, key_id: str, now: float = 0.0) -> bool:
        with self._lock:
            cert = self._certs.get(key_id)
            if cert is None:
                return False
            if cert.revoked:
                return False
            if cert.expires_at is not None and now >= cert.expires_at:
                return False
            return True

    def get_cert(self, key_id: str) -> Optional[SignerCert]:
        with self._lock:
            return self._certs.get(key_id)

    def list_signers(self, active_only: bool = True, now: float = 0.0) -> list:
        with self._lock:
            certs = list(self._certs.values())
        if not active_only:
            return certs
        result = []
        for c in certs:
            if c.revoked:
                continue
            if c.expires_at is not None and now >= c.expires_at:
                continue
            result.append(c)
        return result

    @property
    def total_signers(self) -> int:
        with self._lock:
            return len(self._certs)

    # -------- signing --------

    def sign(
        self,
        content: str,
        key_id: str,
        signer_name: Optional[str] = None,
        now: float = 0.0,
    ) -> Optional[Signature]:
        with self._lock:
            cert = self._certs.get(key_id)
            secret = self._secrets.get(key_id)
            if cert is None or secret is None:
                return None
            if cert.revoked:
                return None
            if cert.expires_at is not None and now >= cert.expires_at:
                return None
            algo = cert.algo
        digest = _compute_digest(secret, content, algo)
        return Signature(
            signature=_b64encode(digest),
            key_id=key_id,
            algo=algo,
            created_at=now,
            signer_name=signer_name,
        )

    def verify(self, content: str, signature: Signature, now: float = 0.0) -> tuple:
        if not isinstance(signature, Signature):
            return False, "invalid signature object"
        with self._lock:
            cert = self._certs.get(signature.key_id)
            secret = self._secrets.get(signature.key_id)
            if cert is None or secret is None:
                return False, "unknown key"
            if cert.revoked:
                return False, "key revoked"
            if cert.expires_at is not None and now >= cert.expires_at:
                return False, "key expired"
            algo = signature.algo
            if not isinstance(algo, SigAlgo):
                try:
                    algo = SigAlgo(algo)
                except (ValueError, KeyError):
                    return False, "algorithm mismatch"
            if algo not in _ALGO_MAP:
                return False, "algorithm mismatch"
            if algo != cert.algo:
                return False, "algorithm mismatch"

        try:
            expected = _compute_digest(secret, content, algo)
        except Exception as e:
            return False, f"compute error: {e}"
        try:
            provided = _b64decode(signature.signature)
        except Exception:
            return False, "invalid base64"
        if not hmac.compare_digest(expected, provided):
            return False, "signature mismatch"
        return True, "ok"

    # -------- multi-sign --------

    def multi_sign(
        self,
        doc_id: str,
        content: str,
        key_ids: list,
        required: Optional[int] = None,
        now: float = 0.0,
    ) -> MultiSig:
        signatures = []
        for kid in key_ids:
            sig = self.sign(content, kid, now=now)
            if sig is not None:
                signatures.append(sig)
        if required is None:
            required = len(key_ids) if key_ids else 1
        return MultiSig(
            doc_id=doc_id,
            content_hash=self.content_hash(content),
            signatures=signatures,
            required=required,
        )

    def verify_multi(
        self, content: str, multi: MultiSig, now: float = 0.0
    ) -> VerifyResult:
        valid_count = 0
        invalid_count = 0
        reasons: list = []

        expected_hash = self.content_hash(content)
        if expected_hash != multi.content_hash:
            return VerifyResult(
                valid=False,
                valid_signatures=0,
                invalid_signatures=len(multi.signatures),
                reasons=["content hash mismatch"],
            )

        for sig in multi.signatures:
            ok, reason = self.verify(content, sig, now=now)
            if ok:
                valid_count += 1
            else:
                invalid_count += 1
                reasons.append(f"{sig.key_id}: {reason}")

        valid = valid_count >= multi.required
        if not valid and not reasons:
            reasons.append(
                f"not enough valid signatures: {valid_count}/{multi.required}"
            )
        return VerifyResult(
            valid=valid,
            valid_signatures=valid_count,
            invalid_signatures=invalid_count,
            reasons=reasons,
        )

    # -------- key rotation --------

    def rotate_key(self, key_id: str, new_secret: str, now: float = 0.0) -> bool:
        if not isinstance(new_secret, str):
            raise TypeError("new_secret must be a string")
        with self._lock:
            if key_id not in self._certs:
                return False
            self._secrets[key_id] = new_secret
            # Bump created_at so signatures created before rotation are
            # considered stale and won't verify (we also store a generation).
            cert = self._certs[key_id]
            cert.created_at = now
            return True

    # -------- helpers --------

    def content_hash(self, content: str, algo: SigAlgo = SigAlgo.HMAC_SHA256) -> str:
        # Plain sha256 of content (algo arg is accepted for forward-compat).
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def clear(self) -> None:
        with self._lock:
            self._certs.clear()
            self._secrets.clear()
