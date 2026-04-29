"""Тесты auth + RBAC."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.auth import (
    KeyStore, ApiKey, hash_key, generate_key,
    scope_matches, require_scope, AuthError, AuthContext,
    extract_token, authenticate,
)


def test_generate_key_format():
    key = generate_key()
    assert key.startswith("dt_")
    assert len(key) == len("dt_") + 64  # 32 bytes hex


def test_hash_key_deterministic():
    assert hash_key("dt_xyz") == hash_key("dt_xyz")
    assert hash_key("dt_a") != hash_key("dt_b")


def test_keystore_create_verify(tmp_path):
    store = KeyStore(db_path=tmp_path / "k.sqlite")
    plain, ak = store.create("alice", ["read:*"])
    assert plain.startswith("dt_")
    verified = store.verify(plain)
    assert verified is not None
    assert verified.name == "alice"
    assert "read:*" in verified.scopes
    store.close()


def test_keystore_invalid_key(tmp_path):
    store = KeyStore(db_path=tmp_path / "k.sqlite")
    assert store.verify("dt_invalid") is None
    assert store.verify("not_a_key") is None
    store.close()


def test_keystore_revoke(tmp_path):
    store = KeyStore(db_path=tmp_path / "k.sqlite")
    plain, ak = store.create("bob", ["read:*"])
    assert store.revoke(ak.id) is True
    assert store.verify(plain) is None
    store.close()


def test_keystore_list(tmp_path):
    store = KeyStore(db_path=tmp_path / "k.sqlite")
    store.create("a", ["read:*"])
    store.create("b", ["write:*"])
    keys = store.list()
    assert len(keys) == 2
    store.close()


def test_scope_matches_exact():
    assert scope_matches("read:docs", ["read:docs"])
    assert not scope_matches("read:docs", ["read:search"])


def test_scope_matches_wildcard_prefix():
    assert scope_matches("read:docs", ["read:*"])
    assert scope_matches("write:docs", ["write:*"])
    assert not scope_matches("write:docs", ["read:*"])


def test_scope_matches_root():
    assert scope_matches("admin:keys", ["*"])
    assert scope_matches("anything:thing", ["*"])


def test_require_scope_decorator_pass():
    @require_scope("read:docs")
    def fn(ctx):
        return "ok"
    ctx = AuthContext(name="x", scopes=["read:*"])
    assert fn(ctx) == "ok"


def test_require_scope_decorator_denied():
    @require_scope("write:docs")
    def fn(ctx):
        return "ok"
    ctx = AuthContext(name="x", scopes=["read:*"])
    with pytest.raises(AuthError):
        fn(ctx)


def test_require_scope_no_ctx_passes():
    """Если нет AuthContext — auth disabled, пропускаем."""
    @require_scope("write:docs")
    def fn():
        return "ok"
    assert fn() == "ok"


def test_extract_token_bearer():
    assert extract_token({"Authorization": "Bearer dt_xyz"}) == "dt_xyz"


def test_extract_token_x_api_key():
    assert extract_token({"X-API-Key": "dt_abc"}) == "dt_abc"


def test_extract_token_none():
    assert extract_token({}) is None


def test_extract_token_lowercase():
    assert extract_token({"authorization": "Bearer dt_x"}) == "dt_x"


def test_authenticate_with_store(tmp_path):
    store = KeyStore(db_path=tmp_path / "k.sqlite")
    plain, ak = store.create("admin", ["*"])

    ctx = authenticate(plain, store=store)
    assert ctx is not None
    assert ctx.name == "admin"
    assert ctx.is_admin is True

    assert authenticate("dt_invalid", store=store) is None
    assert authenticate(None, store=store) is None
    store.close()
