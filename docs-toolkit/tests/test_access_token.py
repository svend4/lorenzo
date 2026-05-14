"""Tests for ``docstoolkit.access_token``."""

from __future__ import annotations

import base64
import time

import pytest

from docstoolkit.access_token import (
    Token,
    TokenManager,
    TokenStatus,
    ValidationResult,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
T0 = 1_000_000.0  # deterministic "now" used across most tests


def make_manager(secret: str = "topsecret") -> TokenManager:
    return TokenManager(secret)


# ---------------------------------------------------------------------------
# TestTokenStatus
# ---------------------------------------------------------------------------
class TestTokenStatus:
    def test_has_four_members(self):
        assert {s.name for s in TokenStatus} == {
            "VALID",
            "EXPIRED",
            "REVOKED",
            "INVALID",
        }

    def test_values_are_strings(self):
        for s in TokenStatus:
            assert isinstance(s.value, str)

    def test_members_are_unique(self):
        values = [s.value for s in TokenStatus]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# TestToken
# ---------------------------------------------------------------------------
class TestToken:
    def test_basic_construction(self):
        tok = Token(
            token_id="abc",
            subject="alice",
            scopes=["read"],
            created_at=1.0,
            expires_at=2.0,
        )
        assert tok.token_id == "abc"
        assert tok.subject == "alice"
        assert tok.scopes == ["read"]
        assert tok.metadata == {}
        assert tok.revoked is False

    def test_metadata_default_factory_independent(self):
        a = Token("a", "s", [], 0.0, 1.0)
        b = Token("b", "s", [], 0.0, 1.0)
        a.metadata["k"] = "v"
        assert b.metadata == {}

    def test_custom_metadata(self):
        tok = Token("a", "s", [], 0.0, 1.0, metadata={"ip": "1.1.1.1"})
        assert tok.metadata == {"ip": "1.1.1.1"}


# ---------------------------------------------------------------------------
# TestValidationResult
# ---------------------------------------------------------------------------
class TestValidationResult:
    def test_is_valid_true_for_valid_status(self):
        r = ValidationResult(TokenStatus.VALID, None, None)
        assert r.is_valid is True

    def test_is_valid_false_for_other_statuses(self):
        for s in (TokenStatus.EXPIRED, TokenStatus.REVOKED, TokenStatus.INVALID):
            assert ValidationResult(s, None, None).is_valid is False

    def test_optional_fields_default(self):
        r = ValidationResult(TokenStatus.VALID)
        assert r.token is None
        assert r.reason is None


# ---------------------------------------------------------------------------
# TestIssue
# ---------------------------------------------------------------------------
class TestIssue:
    def test_returns_string_and_token(self):
        m = make_manager()
        s, t = m.issue("alice", now=T0)
        assert isinstance(s, str) and len(s) > 0
        assert isinstance(t, Token)

    def test_token_id_is_32_hex(self):
        m = make_manager()
        _, t = m.issue("alice", now=T0)
        assert len(t.token_id) == 32
        int(t.token_id, 16)  # parses as hex

    def test_subject_and_scopes_recorded(self):
        m = make_manager()
        _, t = m.issue("alice", scopes=["read", "write"], now=T0)
        assert t.subject == "alice"
        assert t.scopes == ["read", "write"]

    def test_default_scopes_empty(self):
        m = make_manager()
        _, t = m.issue("alice", now=T0)
        assert t.scopes == []

    def test_metadata_recorded(self):
        m = make_manager()
        _, t = m.issue("alice", metadata={"ip": "127.0.0.1"}, now=T0)
        assert t.metadata == {"ip": "127.0.0.1"}

    def test_expires_at_uses_ttl(self):
        m = make_manager()
        _, t = m.issue("alice", ttl=120, now=T0)
        assert t.expires_at == T0 + 120
        assert t.created_at == T0

    def test_two_issuances_have_different_ids(self):
        m = make_manager()
        _, a = m.issue("alice", now=T0)
        _, b = m.issue("alice", now=T0)
        assert a.token_id != b.token_id

    def test_token_stored(self):
        m = make_manager()
        _, t = m.issue("alice", now=T0)
        assert m.get(t.token_id) is t

    def test_empty_subject_rejected(self):
        m = make_manager()
        with pytest.raises(ValueError):
            m.issue("", now=T0)

    def test_issued_string_is_base64url(self):
        m = make_manager()
        s, _ = m.issue("alice", now=T0)
        # base64url-decodable (no padding) — should not raise
        pad = (-len(s)) % 4
        base64.urlsafe_b64decode(s + ("=" * pad))


# ---------------------------------------------------------------------------
# TestValidateValid
# ---------------------------------------------------------------------------
class TestValidateValid:
    def test_fresh_token_validates(self):
        m = make_manager()
        s, t = m.issue("alice", now=T0)
        r = m.validate(s, now=T0 + 1)
        assert r.is_valid
        assert r.status is TokenStatus.VALID
        assert r.token is t
        assert r.reason is None

    def test_validates_just_before_expiry(self):
        m = make_manager()
        s, _ = m.issue("alice", ttl=10, now=T0)
        r = m.validate(s, now=T0 + 9.999)
        assert r.is_valid

    def test_validate_uses_wallclock_when_now_is_zero(self):
        m = make_manager()
        s, _ = m.issue("alice", ttl=3600)
        r = m.validate(s)
        assert r.is_valid

    def test_validate_returns_validation_result(self):
        m = make_manager()
        s, _ = m.issue("alice", now=T0)
        assert isinstance(m.validate(s, now=T0 + 1), ValidationResult)


# ---------------------------------------------------------------------------
# TestValidateExpired
# ---------------------------------------------------------------------------
class TestValidateExpired:
    def test_expired_token_status(self):
        m = make_manager()
        s, _ = m.issue("alice", ttl=10, now=T0)
        r = m.validate(s, now=T0 + 10)
        assert r.status is TokenStatus.EXPIRED
        assert not r.is_valid

    def test_expired_includes_token(self):
        m = make_manager()
        s, t = m.issue("alice", ttl=10, now=T0)
        r = m.validate(s, now=T0 + 100)
        assert r.token is t

    def test_expired_has_reason(self):
        m = make_manager()
        s, _ = m.issue("alice", ttl=1, now=T0)
        r = m.validate(s, now=T0 + 1000)
        assert r.reason is not None

    def test_ttl_zero_is_immediately_expired(self):
        m = make_manager()
        s, _ = m.issue("alice", ttl=0, now=T0)
        r = m.validate(s, now=T0)
        assert r.status is TokenStatus.EXPIRED


# ---------------------------------------------------------------------------
# TestValidateRevoked
# ---------------------------------------------------------------------------
class TestValidateRevoked:
    def test_revoked_status(self):
        m = make_manager()
        s, t = m.issue("alice", now=T0)
        m.revoke(t.token_id)
        r = m.validate(s, now=T0 + 1)
        assert r.status is TokenStatus.REVOKED
        assert not r.is_valid

    def test_revoked_token_returned(self):
        m = make_manager()
        s, t = m.issue("alice", now=T0)
        m.revoke(t.token_id)
        r = m.validate(s, now=T0 + 1)
        assert r.token is t

    def test_expired_overrides_revoked(self):
        # Expired check happens before revoked check in our pipeline.
        m = make_manager()
        s, t = m.issue("alice", ttl=10, now=T0)
        m.revoke(t.token_id)
        r = m.validate(s, now=T0 + 1000)
        assert r.status is TokenStatus.EXPIRED


# ---------------------------------------------------------------------------
# TestValidateBadSignature
# ---------------------------------------------------------------------------
class TestValidateBadSignature:
    def test_random_garbage_invalid(self):
        m = make_manager()
        r = m.validate("not-a-token", now=T0)
        assert r.status is TokenStatus.INVALID

    def test_empty_string_invalid(self):
        m = make_manager()
        r = m.validate("", now=T0)
        assert r.status is TokenStatus.INVALID

    def test_tampered_signature_invalid(self):
        m = make_manager()
        s, _ = m.issue("alice", now=T0)
        # Decode, flip one character of the signature, re-encode.
        raw = base64.urlsafe_b64decode(
            s + ("=" * ((-len(s)) % 4))
        ).decode("ascii")
        tid, sig = raw.split(".", 1)
        flipped = "0" if sig[0] != "0" else "1"
        bad_raw = f"{tid}.{flipped}{sig[1:]}"
        bad = base64.urlsafe_b64encode(bad_raw.encode("ascii")).rstrip(b"=").decode()
        r = m.validate(bad, now=T0 + 1)
        assert r.status is TokenStatus.INVALID

    def test_other_managers_secret_invalid(self):
        a = make_manager("secret-a")
        b = make_manager("secret-b")
        s, _ = a.issue("alice", now=T0)
        r = b.validate(s, now=T0 + 1)
        assert r.status is TokenStatus.INVALID

    def test_signature_match_but_unknown_id_invalid(self):
        # Construct a perfectly signed token but never store it.
        m = make_manager()
        tid = "a" * 32
        sig = m._sign(tid)
        raw = f"{tid}.{sig}".encode("ascii")
        token_string = base64.urlsafe_b64encode(raw).rstrip(b"=").decode()
        r = m.validate(token_string, now=T0)
        assert r.status is TokenStatus.INVALID


# ---------------------------------------------------------------------------
# TestValidateScopes
# ---------------------------------------------------------------------------
class TestValidateScopes:
    def test_required_scope_met(self):
        m = make_manager()
        s, _ = m.issue("alice", scopes=["read", "write"], now=T0)
        r = m.validate(s, now=T0 + 1, required_scopes=["read"])
        assert r.is_valid

    def test_required_scope_missing(self):
        m = make_manager()
        s, _ = m.issue("alice", scopes=["read"], now=T0)
        r = m.validate(s, now=T0 + 1, required_scopes=["write"])
        assert r.status is TokenStatus.INVALID
        assert r.reason and "write" in r.reason

    def test_multiple_required_scopes_all_met(self):
        m = make_manager()
        s, _ = m.issue("alice", scopes=["a", "b", "c"], now=T0)
        r = m.validate(s, now=T0 + 1, required_scopes=["a", "b"])
        assert r.is_valid

    def test_multiple_required_scopes_partial(self):
        m = make_manager()
        s, _ = m.issue("alice", scopes=["a"], now=T0)
        r = m.validate(s, now=T0 + 1, required_scopes=["a", "b"])
        assert r.status is TokenStatus.INVALID

    def test_empty_required_scopes_allows(self):
        m = make_manager()
        s, _ = m.issue("alice", scopes=[], now=T0)
        r = m.validate(s, now=T0 + 1, required_scopes=[])
        assert r.is_valid

    def test_none_required_scopes_allows(self):
        m = make_manager()
        s, _ = m.issue("alice", scopes=[], now=T0)
        r = m.validate(s, now=T0 + 1, required_scopes=None)
        assert r.is_valid


# ---------------------------------------------------------------------------
# TestRevoke
# ---------------------------------------------------------------------------
class TestRevoke:
    def test_revoke_existing(self):
        m = make_manager()
        _, t = m.issue("alice", now=T0)
        assert m.revoke(t.token_id) is True
        assert t.revoked is True

    def test_revoke_unknown_returns_false(self):
        m = make_manager()
        assert m.revoke("nope") is False

    def test_revoke_twice_returns_false_second_time(self):
        m = make_manager()
        _, t = m.issue("alice", now=T0)
        assert m.revoke(t.token_id) is True
        assert m.revoke(t.token_id) is False


# ---------------------------------------------------------------------------
# TestRevokeSubject
# ---------------------------------------------------------------------------
class TestRevokeSubject:
    def test_revokes_all_active(self):
        m = make_manager()
        _, t1 = m.issue("alice", now=T0)
        _, t2 = m.issue("alice", now=T0)
        _, t3 = m.issue("bob", now=T0)
        n = m.revoke_subject("alice")
        assert n == 2
        assert t1.revoked and t2.revoked
        assert not t3.revoked

    def test_unknown_subject_returns_zero(self):
        m = make_manager()
        m.issue("alice", now=T0)
        assert m.revoke_subject("ghost") == 0

    def test_does_not_double_count_already_revoked(self):
        m = make_manager()
        _, t = m.issue("alice", now=T0)
        m.revoke(t.token_id)
        assert m.revoke_subject("alice") == 0


# ---------------------------------------------------------------------------
# TestGet
# ---------------------------------------------------------------------------
class TestGet:
    def test_returns_stored_token(self):
        m = make_manager()
        _, t = m.issue("alice", now=T0)
        assert m.get(t.token_id) is t

    def test_returns_none_for_unknown(self):
        m = make_manager()
        assert m.get("missing") is None


# ---------------------------------------------------------------------------
# TestCleanupExpired
# ---------------------------------------------------------------------------
class TestCleanupExpired:
    def test_removes_only_expired(self):
        m = make_manager()
        _, expired = m.issue("alice", ttl=10, now=T0)
        _, fresh = m.issue("alice", ttl=10_000, now=T0)
        removed = m.cleanup_expired(now=T0 + 100)
        assert removed == 1
        assert m.get(expired.token_id) is None
        assert m.get(fresh.token_id) is fresh

    def test_no_expired_returns_zero(self):
        m = make_manager()
        m.issue("alice", ttl=10_000, now=T0)
        assert m.cleanup_expired(now=T0 + 1) == 0

    def test_all_expired(self):
        m = make_manager()
        m.issue("a", ttl=1, now=T0)
        m.issue("b", ttl=1, now=T0)
        m.issue("c", ttl=1, now=T0)
        assert m.cleanup_expired(now=T0 + 100) == 3
        assert m.count == 0


# ---------------------------------------------------------------------------
# TestCount
# ---------------------------------------------------------------------------
class TestCount:
    def test_empty_manager_count(self):
        assert make_manager().count == 0

    def test_count_increments_on_issue(self):
        m = make_manager()
        m.issue("a", now=T0)
        m.issue("b", now=T0)
        assert m.count == 2

    def test_count_includes_revoked(self):
        m = make_manager()
        _, t = m.issue("a", now=T0)
        m.revoke(t.token_id)
        assert m.count == 1


# ---------------------------------------------------------------------------
# TestActiveCount
# ---------------------------------------------------------------------------
class TestActiveCount:
    def test_only_active_counted(self):
        m = make_manager()
        m.issue("a", ttl=10_000, now=T0)  # active
        _, expired = m.issue("b", ttl=10, now=T0)
        _, revoked = m.issue("c", ttl=10_000, now=T0)
        m.revoke(revoked.token_id)
        assert m.active_count(now=T0 + 1000) == 1

    def test_empty_active_count_zero(self):
        assert make_manager().active_count(now=T0) == 0

    def test_all_active(self):
        m = make_manager()
        m.issue("a", ttl=10_000, now=T0)
        m.issue("b", ttl=10_000, now=T0)
        assert m.active_count(now=T0 + 1) == 2


# ---------------------------------------------------------------------------
# TestTokensForSubject
# ---------------------------------------------------------------------------
class TestTokensForSubject:
    def test_returns_only_matching(self):
        m = make_manager()
        _, a1 = m.issue("alice", now=T0)
        _, a2 = m.issue("alice", now=T0)
        m.issue("bob", now=T0)
        result = m.tokens_for_subject("alice")
        assert {t.token_id for t in result} == {a1.token_id, a2.token_id}

    def test_unknown_subject_empty(self):
        m = make_manager()
        m.issue("alice", now=T0)
        assert m.tokens_for_subject("ghost") == []

    def test_includes_revoked_tokens(self):
        m = make_manager()
        _, t = m.issue("alice", now=T0)
        m.revoke(t.token_id)
        result = m.tokens_for_subject("alice")
        assert len(result) == 1
        assert result[0].revoked


# ---------------------------------------------------------------------------
# TestClear
# ---------------------------------------------------------------------------
class TestClear:
    def test_clear_removes_all(self):
        m = make_manager()
        m.issue("a", now=T0)
        m.issue("b", now=T0)
        m.clear()
        assert m.count == 0

    def test_clear_on_empty(self):
        m = make_manager()
        m.clear()
        assert m.count == 0

    def test_validate_after_clear_invalid(self):
        m = make_manager()
        s, _ = m.issue("alice", now=T0)
        m.clear()
        r = m.validate(s, now=T0 + 1)
        assert r.status is TokenStatus.INVALID


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_empty_secret_rejected(self):
        with pytest.raises(ValueError):
            TokenManager("")

    def test_non_string_secret_rejected(self):
        with pytest.raises(ValueError):
            TokenManager(None)  # type: ignore[arg-type]

    def test_malformed_token_no_dot(self):
        m = make_manager()
        raw = b"hello world"
        token_string = base64.urlsafe_b64encode(raw).rstrip(b"=").decode()
        r = m.validate(token_string, now=T0)
        assert r.status is TokenStatus.INVALID

    def test_malformed_token_multiple_dots(self):
        m = make_manager()
        raw = b"a.b.c"
        token_string = base64.urlsafe_b64encode(raw).rstrip(b"=").decode()
        r = m.validate(token_string, now=T0)
        assert r.status is TokenStatus.INVALID

    def test_token_string_with_invalid_base64(self):
        m = make_manager()
        r = m.validate("!!!not base64!!!", now=T0)
        assert r.status is TokenStatus.INVALID

    def test_expired_immediately_with_negative_ttl(self):
        m = make_manager()
        s, _ = m.issue("alice", ttl=-1, now=T0)
        r = m.validate(s, now=T0)
        assert r.status is TokenStatus.EXPIRED

    def test_long_lived_token_round_trip(self):
        m = make_manager()
        s, t = m.issue("alice", scopes=["admin"], ttl=10**6, now=T0)
        r = m.validate(s, now=T0 + 1, required_scopes=["admin"])
        assert r.is_valid and r.token is t

    def test_revoke_then_validate_then_cleanup(self):
        m = make_manager()
        s, t = m.issue("alice", ttl=100, now=T0)
        m.revoke(t.token_id)
        assert m.validate(s, now=T0 + 1).status is TokenStatus.REVOKED
        # After expiry, cleanup_expired removes it.
        assert m.cleanup_expired(now=T0 + 1000) == 1
        assert m.validate(s, now=T0 + 1001).status is TokenStatus.INVALID

    def test_metadata_isolated_between_tokens(self):
        m = make_manager()
        _, a = m.issue("alice", metadata={"ip": "1"}, now=T0)
        _, b = m.issue("bob", metadata={"ip": "2"}, now=T0)
        a.metadata["ip"] = "999"
        assert b.metadata["ip"] == "2"

    def test_scopes_isolated_between_tokens(self):
        m = make_manager()
        scopes = ["read"]
        _, a = m.issue("alice", scopes=scopes, now=T0)
        scopes.append("write")
        assert a.scopes == ["read"]
