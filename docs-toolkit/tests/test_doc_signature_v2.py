"""Tests for doc_signature_v2 (E259)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_signature_v2 import (
    DocSignatureV2,
    MultiSig,
    SigAlgo,
    Signature,
    SignerCert,
    VerifyResult,
)


# ---------- enum / dataclasses ----------

class TestSigAlgo:
    def test_has_sha256(self):
        assert SigAlgo.HMAC_SHA256.value == "HMAC_SHA256"

    def test_has_sha512(self):
        assert SigAlgo.HMAC_SHA512.value == "HMAC_SHA512"

    def test_is_string_enum(self):
        assert SigAlgo.HMAC_SHA256 == "HMAC_SHA256"


class TestSignerCert:
    def test_basic_fields(self):
        c = SignerCert(key_id="k1", algo=SigAlgo.HMAC_SHA256, created_at=1.0)
        assert c.key_id == "k1"
        assert c.algo == SigAlgo.HMAC_SHA256
        assert c.created_at == 1.0
        assert c.expires_at is None
        assert c.revoked is False
        assert c.metadata == {}

    def test_with_metadata(self):
        c = SignerCert(
            key_id="k1",
            algo=SigAlgo.HMAC_SHA256,
            created_at=1.0,
            metadata={"owner": "alice"},
        )
        assert c.metadata["owner"] == "alice"

    def test_default_metadata_independent(self):
        a = SignerCert(key_id="a", algo=SigAlgo.HMAC_SHA256, created_at=0)
        b = SignerCert(key_id="b", algo=SigAlgo.HMAC_SHA256, created_at=0)
        a.metadata["x"] = 1
        assert "x" not in b.metadata


class TestSignature:
    def test_basic_fields(self):
        s = Signature(
            signature="abc",
            key_id="k1",
            algo=SigAlgo.HMAC_SHA256,
            created_at=1.0,
        )
        assert s.signature == "abc"
        assert s.key_id == "k1"
        assert s.signer_name is None

    def test_with_signer_name(self):
        s = Signature(
            signature="x",
            key_id="k",
            algo=SigAlgo.HMAC_SHA256,
            created_at=0,
            signer_name="Alice",
        )
        assert s.signer_name == "Alice"


class TestMultiSig:
    def test_defaults(self):
        m = MultiSig(doc_id="d1", content_hash="h")
        assert m.signatures == []
        assert m.required == 1

    def test_with_signatures(self):
        sig = Signature(signature="x", key_id="k", algo=SigAlgo.HMAC_SHA256, created_at=0)
        m = MultiSig(doc_id="d", content_hash="h", signatures=[sig], required=1)
        assert len(m.signatures) == 1


class TestVerifyResult:
    def test_default_reasons(self):
        r = VerifyResult(valid=True, valid_signatures=1, invalid_signatures=0)
        assert r.reasons == []

    def test_with_reasons(self):
        r = VerifyResult(
            valid=False, valid_signatures=0, invalid_signatures=1, reasons=["x"]
        )
        assert r.reasons == ["x"]


# ---------- add_signer ----------

class TestAddSigner:
    def test_returns_cert(self):
        ds = DocSignatureV2()
        c = ds.add_signer("k1", "secret")
        assert isinstance(c, SignerCert)
        assert c.key_id == "k1"
        assert c.algo == SigAlgo.HMAC_SHA256

    def test_with_expiry(self):
        ds = DocSignatureV2()
        c = ds.add_signer("k", "s", expires_at=100.0, now=0)
        assert c.expires_at == 100.0

    def test_with_metadata(self):
        ds = DocSignatureV2()
        c = ds.add_signer("k", "s", metadata={"role": "ci"})
        assert c.metadata["role"] == "ci"

    def test_with_algo_sha512(self):
        ds = DocSignatureV2()
        c = ds.add_signer("k", "s", algo=SigAlgo.HMAC_SHA512)
        assert c.algo == SigAlgo.HMAC_SHA512

    def test_empty_key_id_rejected(self):
        ds = DocSignatureV2()
        with pytest.raises(ValueError):
            ds.add_signer("", "s")

    def test_non_string_secret_rejected(self):
        ds = DocSignatureV2()
        with pytest.raises(TypeError):
            ds.add_signer("k", 123)  # type: ignore[arg-type]


# ---------- revoke_signer ----------

class TestRevokeSigner:
    def test_revoke_existing(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        assert ds.revoke_signer("k") is True

    def test_revoke_missing(self):
        ds = DocSignatureV2()
        assert ds.revoke_signer("missing") is False

    def test_revoke_sets_flag(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        ds.revoke_signer("k")
        cert = ds.get_cert("k")
        assert cert.revoked is True


# ---------- is_active ----------

class TestIsActive:
    def test_active_after_add(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s", now=0)
        assert ds.is_active("k", now=0) is True

    def test_not_active_after_revoke(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        ds.revoke_signer("k")
        assert ds.is_active("k") is False

    def test_not_active_after_expiry(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s", expires_at=10.0, now=0)
        assert ds.is_active("k", now=20.0) is False

    def test_active_before_expiry(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s", expires_at=100.0, now=0)
        assert ds.is_active("k", now=50.0) is True

    def test_unknown_key(self):
        ds = DocSignatureV2()
        assert ds.is_active("nope") is False


# ---------- sign ----------

class TestSign:
    def test_sign_returns_signature(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        sig = ds.sign("hello", "k")
        assert isinstance(sig, Signature)
        assert sig.key_id == "k"
        assert sig.algo == SigAlgo.HMAC_SHA256
        assert sig.signature

    def test_sign_unknown_key_none(self):
        ds = DocSignatureV2()
        assert ds.sign("x", "missing") is None

    def test_sign_revoked_returns_none(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        ds.revoke_signer("k")
        assert ds.sign("x", "k") is None

    def test_sign_expired_returns_none(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s", expires_at=10.0, now=0)
        assert ds.sign("x", "k", now=20.0) is None

    def test_sign_with_name(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        sig = ds.sign("x", "k", signer_name="Alice")
        assert sig.signer_name == "Alice"

    def test_sign_uses_signer_algo(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s", algo=SigAlgo.HMAC_SHA512)
        sig = ds.sign("x", "k")
        assert sig.algo == SigAlgo.HMAC_SHA512

    def test_sign_deterministic(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        a = ds.sign("hello", "k")
        b = ds.sign("hello", "k")
        assert a.signature == b.signature


# ---------- verify ----------

class TestVerify:
    def test_verify_good(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        sig = ds.sign("hello", "k")
        ok, reason = ds.verify("hello", sig)
        assert ok is True
        assert reason == "ok"

    def test_verify_tampered(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        sig = ds.sign("hello", "k")
        ok, reason = ds.verify("HELLO", sig)
        assert ok is False
        assert "mismatch" in reason

    def test_verify_unknown_key(self):
        ds = DocSignatureV2()
        sig = Signature(
            signature="x", key_id="ghost", algo=SigAlgo.HMAC_SHA256, created_at=0
        )
        ok, reason = ds.verify("hello", sig)
        assert ok is False
        assert "unknown" in reason

    def test_verify_invalid_base64(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        bad = Signature(
            signature="!!!not-base64!!!",
            key_id="k",
            algo=SigAlgo.HMAC_SHA256,
            created_at=0,
        )
        ok, reason = ds.verify("hello", bad)
        assert ok is False

    def test_verify_non_signature_obj(self):
        ds = DocSignatureV2()
        ok, reason = ds.verify("x", "not a sig")  # type: ignore[arg-type]
        assert ok is False


class TestVerifyExpired:
    def test_verify_expired_fails(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s", expires_at=10.0, now=0)
        sig = ds.sign("hello", "k", now=5.0)
        ok, reason = ds.verify("hello", sig, now=20.0)
        assert ok is False
        assert "expire" in reason

    def test_verify_pre_expiry_works(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s", expires_at=100.0, now=0)
        sig = ds.sign("hello", "k", now=5.0)
        ok, _ = ds.verify("hello", sig, now=50.0)
        assert ok is True


class TestVerifyRevoked:
    def test_verify_after_revoke_fails(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        sig = ds.sign("hello", "k")
        ds.revoke_signer("k")
        ok, reason = ds.verify("hello", sig)
        assert ok is False
        assert "revoke" in reason


# ---------- multi_sign ----------

class TestMultiSign:
    def test_multi_sign_basic(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        ds.add_signer("b", "sb")
        m = ds.multi_sign("doc1", "content", ["a", "b"])
        assert isinstance(m, MultiSig)
        assert m.doc_id == "doc1"
        assert len(m.signatures) == 2

    def test_multi_sign_default_required_is_all(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        ds.add_signer("b", "sb")
        m = ds.multi_sign("doc", "x", ["a", "b"])
        assert m.required == 2

    def test_multi_sign_custom_required(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        ds.add_signer("b", "sb")
        m = ds.multi_sign("doc", "x", ["a", "b"], required=1)
        assert m.required == 1

    def test_multi_sign_skips_unknown(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        m = ds.multi_sign("doc", "x", ["a", "ghost"])
        assert len(m.signatures) == 1

    def test_multi_sign_content_hash_set(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        m = ds.multi_sign("doc", "hello", ["a"])
        assert m.content_hash == ds.content_hash("hello")

    def test_multi_sign_skips_revoked(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        ds.add_signer("b", "sb")
        ds.revoke_signer("b")
        m = ds.multi_sign("doc", "x", ["a", "b"])
        assert len(m.signatures) == 1
        assert m.signatures[0].key_id == "a"


# ---------- verify_multi ----------

class TestVerifyMulti:
    def test_verify_multi_valid(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        ds.add_signer("b", "sb")
        m = ds.multi_sign("doc", "hello", ["a", "b"])
        r = ds.verify_multi("hello", m)
        assert r.valid is True
        assert r.valid_signatures == 2
        assert r.invalid_signatures == 0

    def test_verify_multi_tampered_content(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        m = ds.multi_sign("doc", "hello", ["a"])
        r = ds.verify_multi("HELLO", m)
        assert r.valid is False
        # content hash mismatch short-circuits
        assert "content hash mismatch" in r.reasons

    def test_verify_multi_with_required_threshold(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        ds.add_signer("b", "sb")
        m = ds.multi_sign("doc", "x", ["a", "b"], required=1)
        # revoke 'b' after signing
        ds.revoke_signer("b")
        r = ds.verify_multi("x", m)
        assert r.valid_signatures == 1
        assert r.valid is True

    def test_verify_multi_returns_verify_result(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        m = ds.multi_sign("doc", "x", ["a"])
        r = ds.verify_multi("x", m)
        assert isinstance(r, VerifyResult)


class TestVerifyMultiNotEnough:
    def test_not_enough_valid(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        ds.add_signer("b", "sb")
        m = ds.multi_sign("doc", "x", ["a", "b"], required=2)
        ds.revoke_signer("b")
        r = ds.verify_multi("x", m)
        assert r.valid is False
        assert r.valid_signatures == 1
        assert r.invalid_signatures == 1
        assert any("revoke" in x for x in r.reasons)

    def test_empty_signatures_fails_when_required(self):
        ds = DocSignatureV2()
        m = MultiSig(
            doc_id="d",
            content_hash=ds.content_hash("x"),
            signatures=[],
            required=1,
        )
        r = ds.verify_multi("x", m)
        assert r.valid is False


# ---------- rotate_key ----------

class TestRotateKey:
    def test_rotate_returns_true(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "old")
        assert ds.rotate_key("k", "new") is True

    def test_rotate_missing_returns_false(self):
        ds = DocSignatureV2()
        assert ds.rotate_key("missing", "x") is False

    def test_old_signatures_become_invalid(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "old")
        old_sig = ds.sign("hello", "k")
        ds.rotate_key("k", "new")
        ok, reason = ds.verify("hello", old_sig)
        assert ok is False
        assert "mismatch" in reason

    def test_new_signatures_after_rotation_verify(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "old")
        ds.rotate_key("k", "new")
        new_sig = ds.sign("hello", "k")
        ok, _ = ds.verify("hello", new_sig)
        assert ok is True

    def test_rotate_non_string_secret(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "old")
        with pytest.raises(TypeError):
            ds.rotate_key("k", 123)  # type: ignore[arg-type]


# ---------- list_signers ----------

class TestListSigners:
    def test_empty(self):
        ds = DocSignatureV2()
        assert ds.list_signers() == []

    def test_active_only_default(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        ds.add_signer("b", "sb")
        ds.revoke_signer("b")
        result = ds.list_signers()
        ids = {c.key_id for c in result}
        assert ids == {"a"}

    def test_include_revoked(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        ds.add_signer("b", "sb")
        ds.revoke_signer("b")
        result = ds.list_signers(active_only=False)
        assert len(result) == 2

    def test_filters_expired(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa", expires_at=10.0, now=0)
        result = ds.list_signers(active_only=True, now=20.0)
        assert result == []


# ---------- get_cert ----------

class TestGetCert:
    def test_returns_cert(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        c = ds.get_cert("k")
        assert c is not None
        assert c.key_id == "k"

    def test_missing_is_none(self):
        ds = DocSignatureV2()
        assert ds.get_cert("missing") is None


# ---------- content_hash ----------

class TestContentHash:
    def test_deterministic(self):
        ds = DocSignatureV2()
        assert ds.content_hash("hello") == ds.content_hash("hello")

    def test_different_content_different_hash(self):
        ds = DocSignatureV2()
        assert ds.content_hash("a") != ds.content_hash("b")

    def test_hex_length(self):
        ds = DocSignatureV2()
        h = ds.content_hash("anything")
        # sha256 hex digest is 64 chars
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)


# ---------- total_signers ----------

class TestTotalSigners:
    def test_zero_initially(self):
        assert DocSignatureV2().total_signers == 0

    def test_increments(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "x")
        ds.add_signer("b", "x")
        assert ds.total_signers == 2

    def test_includes_revoked(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "x")
        ds.revoke_signer("a")
        # revoked signers still exist in the cert store
        assert ds.total_signers == 1


# ---------- clear ----------

class TestClear:
    def test_clear_resets(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "x")
        ds.add_signer("b", "y")
        ds.clear()
        assert ds.total_signers == 0
        assert ds.list_signers(active_only=False) == []

    def test_after_clear_sign_fails(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "x")
        ds.clear()
        assert ds.sign("hello", "a") is None


# ---------- edge cases ----------

class TestEdgeCases:
    def test_empty_content(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        sig = ds.sign("", "k")
        ok, _ = ds.verify("", sig)
        assert ok is True

    def test_unicode_content(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        sig = ds.sign("привет мир 🌍", "k")
        ok, _ = ds.verify("привет мир 🌍", sig)
        assert ok is True

    def test_unicode_secret(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "секрет")
        sig = ds.sign("x", "k")
        ok, _ = ds.verify("x", sig)
        assert ok is True

    def test_re_add_overrides(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "old", metadata={"v": 1})
        ds.add_signer("k", "new", metadata={"v": 2})
        c = ds.get_cert("k")
        assert c.metadata["v"] == 2

    def test_multi_sign_doc_id_preserved(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        m = ds.multi_sign("special-id", "x", ["a"])
        assert m.doc_id == "special-id"

    def test_sign_after_expired_then_extend_not_supported_but_safe(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s", expires_at=10.0, now=0)
        # past expiry — sign returns None
        assert ds.sign("x", "k", now=20.0) is None

    def test_sha512_round_trip(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s", algo=SigAlgo.HMAC_SHA512)
        sig = ds.sign("hello", "k")
        assert sig.algo == SigAlgo.HMAC_SHA512
        ok, _ = ds.verify("hello", sig)
        assert ok is True

    def test_verify_algo_mismatch(self):
        ds = DocSignatureV2()
        ds.add_signer("k", "s", algo=SigAlgo.HMAC_SHA256)
        sig = ds.sign("hello", "k")
        # Forge a signature claiming sha512 with sha256 digest
        forged = Signature(
            signature=sig.signature,
            key_id="k",
            algo=SigAlgo.HMAC_SHA512,
            created_at=0,
        )
        ok, reason = ds.verify("hello", forged)
        assert ok is False
        assert "algorithm" in reason

    def test_concurrent_safe_smoke(self):
        import threading
        ds = DocSignatureV2()
        ds.add_signer("k", "s")
        results = []

        def worker():
            sig = ds.sign("x", "k")
            results.append(ds.verify("x", sig)[0])

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert all(results)

    def test_rotate_invalidates_multi_sig_too(self):
        ds = DocSignatureV2()
        ds.add_signer("a", "sa")
        ds.add_signer("b", "sb")
        m = ds.multi_sign("doc", "x", ["a", "b"])
        ds.rotate_key("a", "new_sa")
        r = ds.verify_multi("x", m)
        # 'a' signature should be invalid now, 'b' still valid
        assert r.valid_signatures == 1
        assert r.invalid_signatures == 1
