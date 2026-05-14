"""HMAC-based document signing and verification (E165).

Stdlib only: hmac, hashlib, base64, json, enum, dataclasses.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Optional


class SignatureAlgo(str, Enum):
    """Supported HMAC algorithms."""

    HMAC_SHA256 = "HMAC_SHA256"
    HMAC_SHA512 = "HMAC_SHA512"
    HMAC_BLAKE2B = "HMAC_BLAKE2B"


_ALGO_MAP = {
    SignatureAlgo.HMAC_SHA256: hashlib.sha256,
    SignatureAlgo.HMAC_SHA512: hashlib.sha512,
    SignatureAlgo.HMAC_BLAKE2B: hashlib.blake2b,
}


@dataclass
class Signature:
    """An HMAC signature value."""

    value: str  # base64-encoded
    algo: SignatureAlgo
    key_id: Optional[str] = None
    created_at: float = 0.0

    def to_dict(self) -> dict:
        return {
            "value": self.value,
            "algo": self.algo.value if isinstance(self.algo, SignatureAlgo) else self.algo,
            "key_id": self.key_id,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Signature":
        algo = d["algo"]
        if isinstance(algo, str):
            algo = SignatureAlgo(algo)
        return cls(
            value=d["value"],
            algo=algo,
            key_id=d.get("key_id"),
            created_at=float(d.get("created_at", 0.0)),
        )


@dataclass
class SignedDocument:
    """A document bundled with its signature."""

    content: str
    signature: Signature

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "signature": self.signature.to_dict(),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, d: dict) -> "SignedDocument":
        return cls(
            content=d["content"],
            signature=Signature.from_dict(d["signature"]),
        )


@dataclass
class VerifyResult:
    """Result of a verification attempt."""

    valid: bool
    reason: Optional[str]
    algo: SignatureAlgo


def _compute_digest(secret: str, content: str, algo: SignatureAlgo) -> bytes:
    hash_func = _ALGO_MAP[algo]
    return hmac.new(secret.encode("utf-8"), content.encode("utf-8"), hash_func).digest()


def _b64encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _b64decode(s: str) -> bytes:
    return base64.b64decode(s.encode("ascii"))


class DocSigner:
    """HMAC-based document signer/verifier with a single secret key."""

    def __init__(self, secret: str):
        if not isinstance(secret, str):
            raise TypeError("secret must be a string")
        self._secret = secret

    def sign(
        self,
        content: str,
        algo: SignatureAlgo = SignatureAlgo.HMAC_SHA256,
        key_id: Optional[str] = None,
        now: float = 0.0,
    ) -> Signature:
        digest = _compute_digest(self._secret, content, algo)
        return Signature(
            value=_b64encode(digest),
            algo=algo,
            key_id=key_id,
            created_at=now,
        )

    def sign_document(
        self,
        content: str,
        algo: SignatureAlgo = SignatureAlgo.HMAC_SHA256,
        key_id: Optional[str] = None,
        now: float = 0.0,
    ) -> SignedDocument:
        sig = self.sign(content, algo=algo, key_id=key_id, now=now)
        return SignedDocument(content=content, signature=sig)

    def verify(self, content: str, signature: Signature) -> VerifyResult:
        algo = signature.algo
        if not isinstance(algo, SignatureAlgo):
            try:
                algo = SignatureAlgo(algo)
            except (ValueError, KeyError):
                return VerifyResult(valid=False, reason="algorithm mismatch", algo=signature.algo)

        if algo not in _ALGO_MAP:
            return VerifyResult(valid=False, reason="algorithm mismatch", algo=algo)

        try:
            expected = _compute_digest(self._secret, content, algo)
        except Exception as e:
            return VerifyResult(valid=False, reason=f"compute error: {e}", algo=algo)

        try:
            provided = _b64decode(signature.value)
        except Exception:
            return VerifyResult(valid=False, reason="invalid base64", algo=algo)

        if not hmac.compare_digest(expected, provided):
            return VerifyResult(valid=False, reason="signature mismatch", algo=algo)

        return VerifyResult(valid=True, reason=None, algo=algo)

    def verify_document(self, doc: SignedDocument) -> VerifyResult:
        return self.verify(doc.content, doc.signature)

    def sign_batch(
        self,
        contents: list,
        algo: SignatureAlgo = SignatureAlgo.HMAC_SHA256,
    ) -> list:
        return [self.sign(c, algo=algo) for c in contents]

    def verify_batch(self, docs: list) -> list:
        return [self.verify_document(d) for d in docs]

    def rotate_key(self, new_secret: str) -> None:
        if not isinstance(new_secret, str):
            raise TypeError("new_secret must be a string")
        self._secret = new_secret

    @staticmethod
    def from_json(json_str: str) -> SignedDocument:
        d = json.loads(json_str)
        return SignedDocument.from_dict(d)


class MultiKeyDocSigner:
    """Signer that supports multiple keys identified by key_id."""

    def __init__(self):
        self._keys: dict = {}

    def add_key(self, key_id: str, secret: str) -> None:
        if not isinstance(key_id, str) or not key_id:
            raise ValueError("key_id must be a non-empty string")
        if not isinstance(secret, str):
            raise TypeError("secret must be a string")
        self._keys[key_id] = secret

    def remove_key(self, key_id: str) -> bool:
        if key_id in self._keys:
            del self._keys[key_id]
            return True
        return False

    def has_key(self, key_id: str) -> bool:
        return key_id in self._keys

    @property
    def key_ids(self) -> list:
        return list(self._keys.keys())

    def sign(
        self,
        content: str,
        key_id: str,
        algo: SignatureAlgo = SignatureAlgo.HMAC_SHA256,
        now: float = 0.0,
    ) -> Signature:
        if key_id not in self._keys:
            raise KeyError(f"unknown key: {key_id}")
        secret = self._keys[key_id]
        digest = _compute_digest(secret, content, algo)
        return Signature(
            value=_b64encode(digest),
            algo=algo,
            key_id=key_id,
            created_at=now,
        )

    def verify(self, content: str, signature: Signature) -> VerifyResult:
        algo = signature.algo
        if not isinstance(algo, SignatureAlgo):
            try:
                algo = SignatureAlgo(algo)
            except (ValueError, KeyError):
                return VerifyResult(valid=False, reason="algorithm mismatch", algo=signature.algo)

        if algo not in _ALGO_MAP:
            return VerifyResult(valid=False, reason="algorithm mismatch", algo=algo)

        key_id = signature.key_id
        if key_id is None or key_id not in self._keys:
            return VerifyResult(valid=False, reason="unknown key", algo=algo)

        secret = self._keys[key_id]
        try:
            expected = _compute_digest(secret, content, algo)
        except Exception as e:
            return VerifyResult(valid=False, reason=f"compute error: {e}", algo=algo)

        try:
            provided = _b64decode(signature.value)
        except Exception:
            return VerifyResult(valid=False, reason="invalid base64", algo=algo)

        if not hmac.compare_digest(expected, provided):
            return VerifyResult(valid=False, reason="signature mismatch", algo=algo)

        return VerifyResult(valid=True, reason=None, algo=algo)
