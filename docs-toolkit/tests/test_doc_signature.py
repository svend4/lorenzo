"""Tests for doc_signature module (E165)."""
from __future__ import annotations

import json

import pytest

from docstoolkit.doc_signature import (
    DocSigner,
    MultiKeyDocSigner,
    Signature,
    SignatureAlgo,
    SignedDocument,
    VerifyResult,
)


class TestSignatureAlgo:
    def test_has_sha256(self):
        assert SignatureAlgo.HMAC_SHA256.value == "HMAC_SHA256"

    def test_has_sha512(self):
        assert SignatureAlgo.HMAC_SHA512.value == "HMAC_SHA512"

    def test_has_blake2b(self):
        assert SignatureAlgo.HMAC_BLAKE2B.value == "HMAC_BLAKE2B"

    def test_is_enum(self):
        assert isinstance(SignatureAlgo.HMAC_SHA256, SignatureAlgo)


class TestSignature:
    def test_create(self):
        sig = Signature(value="abc", algo=SignatureAlgo.HMAC_SHA256)
        assert sig.value == "abc"
        assert sig.algo == SignatureAlgo.HMAC_SHA256
        assert sig.key_id is None
        assert sig.created_at == 0.0

    def test_with_key_id(self):
        sig = Signature(value="x", algo=SignatureAlgo.HMAC_SHA512, key_id="k1")
        assert sig.key_id == "k1"

    def test_with_created_at(self):
        sig = Signature(value="x", algo=SignatureAlgo.HMAC_SHA256, created_at=123.45)
        assert sig.created_at == 123.45

    def test_to_dict(self):
        sig = Signature(value="abc", algo=SignatureAlgo.HMAC_SHA256, key_id="k", created_at=1.0)
        d = sig.to_dict()
        assert d["value"] == "abc"
        assert d["algo"] == "HMAC_SHA256"
        assert d["key_id"] == "k"
        assert d["created_at"] == 1.0


class TestSignedDocument:
    def test_create(self):
        sig = Signature(value="v", algo=SignatureAlgo.HMAC_SHA256)
        doc = SignedDocument(content="hello", signature=sig)
        assert doc.content == "hello"
        assert doc.signature is sig

    def test_to_dict(self):
        sig = Signature(value="v", algo=SignatureAlgo.HMAC_SHA256, key_id="k")
        doc = SignedDocument(content="hello", signature=sig)
        d = doc.to_dict()
        assert d["content"] == "hello"
        assert d["signature"]["value"] == "v"
        assert d["signature"]["algo"] == "HMAC_SHA256"
        assert d["signature"]["key_id"] == "k"

    def test_to_json(self):
        sig = Signature(value="v", algo=SignatureAlgo.HMAC_SHA256)
        doc = SignedDocument(content="hello", signature=sig)
        s = doc.to_json()
        parsed = json.loads(s)
        assert parsed["content"] == "hello"
        assert parsed["signature"]["algo"] == "HMAC_SHA256"

    def test_to_json_unicode(self):
        sig = Signature(value="v", algo=SignatureAlgo.HMAC_SHA256)
        doc = SignedDocument(content="привет", signature=sig)
        s = doc.to_json()
        parsed = json.loads(s)
        assert parsed["content"] == "привет"


class TestVerifyResult:
    def test_valid(self):
        r = VerifyResult(valid=True, reason=None, algo=SignatureAlgo.HMAC_SHA256)
        assert r.valid is True
        assert r.reason is None

    def test_invalid(self):
        r = VerifyResult(valid=False, reason="bad", algo=SignatureAlgo.HMAC_SHA256)
        assert r.valid is False
        assert r.reason == "bad"


class TestSignAll:
    def test_sign_sha256(self):
        signer = DocSigner("secret")
        sig = signer.sign("hello", algo=SignatureAlgo.HMAC_SHA256)
        assert sig.algo == SignatureAlgo.HMAC_SHA256
        assert sig.value
        assert len(sig.value) > 0

    def test_sign_sha512(self):
        signer = DocSigner("secret")
        sig = signer.sign("hello", algo=SignatureAlgo.HMAC_SHA512)
        assert sig.algo == SignatureAlgo.HMAC_SHA512
        assert sig.value

    def test_sign_blake2b(self):
        signer = DocSigner("secret")
        sig = signer.sign("hello", algo=SignatureAlgo.HMAC_BLAKE2B)
        assert sig.algo == SignatureAlgo.HMAC_BLAKE2B
        assert sig.value

    def test_different_algos_differ(self):
        signer = DocSigner("secret")
        s256 = signer.sign("hello", algo=SignatureAlgo.HMAC_SHA256)
        s512 = signer.sign("hello", algo=SignatureAlgo.HMAC_SHA512)
        sblake = signer.sign("hello", algo=SignatureAlgo.HMAC_BLAKE2B)
        assert s256.value != s512.value
        assert s256.value != sblake.value
        assert s512.value != sblake.value


class TestSignDeterministic:
    def test_same_content_same_sig(self):
        signer = DocSigner("secret")
        a = signer.sign("hello")
        b = signer.sign("hello")
        assert a.value == b.value

    def test_diff_content_diff_sig(self):
        signer = DocSigner("secret")
        a = signer.sign("hello")
        b = signer.sign("world")
        assert a.value != b.value

    def test_diff_secret_diff_sig(self):
        s1 = DocSigner("secret1")
        s2 = DocSigner("secret2")
        a = s1.sign("hello")
        b = s2.sign("hello")
        assert a.value != b.value


class TestSignDocument:
    def test_basic(self):
        signer = DocSigner("secret")
        doc = signer.sign_document("hello")
        assert doc.content == "hello"
        assert doc.signature.algo == SignatureAlgo.HMAC_SHA256

    def test_with_key_id(self):
        signer = DocSigner("secret")
        doc = signer.sign_document("hello", key_id="k1")
        assert doc.signature.key_id == "k1"

    def test_with_now(self):
        signer = DocSigner("secret")
        doc = signer.sign_document("hello", now=100.5)
        assert doc.signature.created_at == 100.5

    def test_algo_param(self):
        signer = DocSigner("secret")
        doc = signer.sign_document("hello", algo=SignatureAlgo.HMAC_BLAKE2B)
        assert doc.signature.algo == SignatureAlgo.HMAC_BLAKE2B


class TestVerifyValid:
    def test_verify_sha256(self):
        signer = DocSigner("secret")
        sig = signer.sign("hello", algo=SignatureAlgo.HMAC_SHA256)
        result = signer.verify("hello", sig)
        assert result.valid is True
        assert result.reason is None

    def test_verify_sha512(self):
        signer = DocSigner("secret")
        sig = signer.sign("hello", algo=SignatureAlgo.HMAC_SHA512)
        result = signer.verify("hello", sig)
        assert result.valid is True

    def test_verify_blake2b(self):
        signer = DocSigner("secret")
        sig = signer.sign("hello", algo=SignatureAlgo.HMAC_BLAKE2B)
        result = signer.verify("hello", sig)
        assert result.valid is True

    def test_result_algo_matches(self):
        signer = DocSigner("secret")
        sig = signer.sign("hello", algo=SignatureAlgo.HMAC_SHA512)
        result = signer.verify("hello", sig)
        assert result.algo == SignatureAlgo.HMAC_SHA512


class TestVerifyInvalid:
    def test_tampered_content(self):
        signer = DocSigner("secret")
        sig = signer.sign("hello")
        result = signer.verify("world", sig)
        assert result.valid is False
        assert result.reason is not None

    def test_wrong_secret(self):
        s1 = DocSigner("secret1")
        s2 = DocSigner("secret2")
        sig = s1.sign("hello")
        result = s2.verify("hello", sig)
        assert result.valid is False

    def test_tampered_signature(self):
        signer = DocSigner("secret")
        sig = signer.sign("hello")
        # Modify base64 value (keep valid base64 form)
        tampered_value = "AAAA" + sig.value[4:] if len(sig.value) > 4 else "AAAA"
        bad = Signature(value=tampered_value, algo=sig.algo)
        result = signer.verify("hello", bad)
        assert result.valid is False

    def test_invalid_base64(self):
        signer = DocSigner("secret")
        bad = Signature(value="!!!not_base64!!!", algo=SignatureAlgo.HMAC_SHA256)
        result = signer.verify("hello", bad)
        assert result.valid is False


class TestVerifyDocument:
    def test_valid_doc(self):
        signer = DocSigner("secret")
        doc = signer.sign_document("hello")
        result = signer.verify_document(doc)
        assert result.valid is True

    def test_tampered_doc(self):
        signer = DocSigner("secret")
        doc = signer.sign_document("hello")
        tampered = SignedDocument(content="world", signature=doc.signature)
        result = signer.verify_document(tampered)
        assert result.valid is False


class TestRoundTripJson:
    def test_roundtrip_basic(self):
        signer = DocSigner("secret")
        doc = signer.sign_document("hello")
        s = doc.to_json()
        restored = DocSigner.from_json(s)
        assert restored.content == "hello"
        assert restored.signature.value == doc.signature.value
        assert restored.signature.algo == doc.signature.algo

    def test_roundtrip_verify(self):
        signer = DocSigner("secret")
        doc = signer.sign_document("hello", key_id="k", now=42.0)
        s = doc.to_json()
        restored = DocSigner.from_json(s)
        result = signer.verify_document(restored)
        assert result.valid is True
        assert restored.signature.key_id == "k"
        assert restored.signature.created_at == 42.0

    def test_roundtrip_unicode(self):
        signer = DocSigner("секрет")
        doc = signer.sign_document("привет, мир!")
        s = doc.to_json()
        restored = DocSigner.from_json(s)
        assert restored.content == "привет, мир!"
        assert signer.verify_document(restored).valid is True


class TestKeyRotation:
    def test_rotate_key(self):
        signer = DocSigner("old_secret")
        sig_old = signer.sign("hello")
        signer.rotate_key("new_secret")
        # Old signature no longer verifies
        assert signer.verify("hello", sig_old).valid is False

    def test_rotate_then_new_signs(self):
        signer = DocSigner("old_secret")
        signer.rotate_key("new_secret")
        sig = signer.sign("hello")
        assert signer.verify("hello", sig).valid is True

    def test_rotate_type_check(self):
        signer = DocSigner("old")
        with pytest.raises(TypeError):
            signer.rotate_key(123)  # type: ignore[arg-type]


class TestBatch:
    def test_sign_batch(self):
        signer = DocSigner("secret")
        sigs = signer.sign_batch(["a", "b", "c"])
        assert len(sigs) == 3
        for sig in sigs:
            assert sig.algo == SignatureAlgo.HMAC_SHA256

    def test_sign_batch_with_algo(self):
        signer = DocSigner("secret")
        sigs = signer.sign_batch(["a", "b"], algo=SignatureAlgo.HMAC_SHA512)
        for sig in sigs:
            assert sig.algo == SignatureAlgo.HMAC_SHA512

    def test_verify_batch_all_valid(self):
        signer = DocSigner("secret")
        docs = [signer.sign_document(c) for c in ["a", "b", "c"]]
        results = signer.verify_batch(docs)
        assert all(r.valid for r in results)
        assert len(results) == 3

    def test_verify_batch_mixed(self):
        signer = DocSigner("secret")
        docs = [signer.sign_document(c) for c in ["a", "b", "c"]]
        # Tamper with middle one
        docs[1] = SignedDocument(content="tampered", signature=docs[1].signature)
        results = signer.verify_batch(docs)
        assert results[0].valid is True
        assert results[1].valid is False
        assert results[2].valid is True

    def test_sign_batch_empty(self):
        signer = DocSigner("secret")
        sigs = signer.sign_batch([])
        assert sigs == []


class TestMultiKeyAdd:
    def test_add(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "secret1")
        assert m.has_key("k1")

    def test_add_multiple(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "s1")
        m.add_key("k2", "s2")
        assert "k1" in m.key_ids
        assert "k2" in m.key_ids
        assert len(m.key_ids) == 2

    def test_add_empty_key_id_fails(self):
        m = MultiKeyDocSigner()
        with pytest.raises(ValueError):
            m.add_key("", "secret")

    def test_overwrite_key(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "old")
        m.add_key("k1", "new")
        assert len(m.key_ids) == 1


class TestMultiKeyRemove:
    def test_remove_existing(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "s1")
        assert m.remove_key("k1") is True
        assert not m.has_key("k1")

    def test_remove_missing(self):
        m = MultiKeyDocSigner()
        assert m.remove_key("nonexistent") is False

    def test_has_key_false(self):
        m = MultiKeyDocSigner()
        assert m.has_key("anything") is False


class TestMultiKeyVerify:
    def test_sign_and_verify(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "secret1")
        sig = m.sign("hello", key_id="k1")
        result = m.verify("hello", sig)
        assert result.valid is True

    def test_different_keys_different_sigs(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "s1")
        m.add_key("k2", "s2")
        s1 = m.sign("hello", key_id="k1")
        s2 = m.sign("hello", key_id="k2")
        assert s1.value != s2.value

    def test_verify_uses_correct_key(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "s1")
        m.add_key("k2", "s2")
        sig = m.sign("hello", key_id="k1")
        assert m.verify("hello", sig).valid is True

    def test_sign_with_algo(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "s1")
        sig = m.sign("hello", key_id="k1", algo=SignatureAlgo.HMAC_BLAKE2B)
        assert sig.algo == SignatureAlgo.HMAC_BLAKE2B
        assert m.verify("hello", sig).valid is True

    def test_sign_tampered_content_invalid(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "s1")
        sig = m.sign("hello", key_id="k1")
        assert m.verify("tampered", sig).valid is False


class TestMultiKeyUnknown:
    def test_verify_unknown_key(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "s1")
        # Construct a signature claiming an unknown key
        bad_sig = Signature(value="aaaa", algo=SignatureAlgo.HMAC_SHA256, key_id="unknown")
        result = m.verify("hello", bad_sig)
        assert result.valid is False
        assert result.reason == "unknown key"

    def test_verify_no_key_id(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "s1")
        bad_sig = Signature(value="aaaa", algo=SignatureAlgo.HMAC_SHA256, key_id=None)
        result = m.verify("hello", bad_sig)
        assert result.valid is False
        assert result.reason == "unknown key"

    def test_sign_unknown_key_raises(self):
        m = MultiKeyDocSigner()
        with pytest.raises(KeyError):
            m.sign("hello", key_id="nope")

    def test_removed_key_verify_fails(self):
        m = MultiKeyDocSigner()
        m.add_key("k1", "s1")
        sig = m.sign("hello", key_id="k1")
        m.remove_key("k1")
        result = m.verify("hello", sig)
        assert result.valid is False
        assert result.reason == "unknown key"


class TestEdgeCases:
    def test_empty_content(self):
        signer = DocSigner("secret")
        sig = signer.sign("")
        assert signer.verify("", sig).valid is True
        assert signer.verify("nonempty", sig).valid is False

    def test_unicode_content(self):
        signer = DocSigner("secret")
        content = "Привет, 世界! 🌍"
        sig = signer.sign(content)
        assert signer.verify(content, sig).valid is True

    def test_unicode_secret(self):
        signer = DocSigner("секретный_ключ_🔑")
        sig = signer.sign("hello")
        assert signer.verify("hello", sig).valid is True

    def test_very_long_content(self):
        signer = DocSigner("secret")
        content = "x" * 100000
        sig = signer.sign(content)
        assert signer.verify(content, sig).valid is True

    def test_newlines_in_content(self):
        signer = DocSigner("secret")
        content = "line1\nline2\r\nline3"
        sig = signer.sign(content)
        assert signer.verify(content, sig).valid is True

    def test_whitespace_sensitive(self):
        signer = DocSigner("secret")
        sig = signer.sign("hello")
        # Trailing space changes the content
        assert signer.verify("hello ", sig).valid is False

    def test_signer_secret_type_check(self):
        with pytest.raises(TypeError):
            DocSigner(123)  # type: ignore[arg-type]
