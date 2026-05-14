"""Tests for docstoolkit.consent_manager (E109).

Coverage:
  - ConsentStatus enum values and str-enum behaviour
  - ConsentRecord dataclass fields and defaults
  - ConsentManager.grant — creates record, overwrites existing
  - ConsentManager.withdraw — sets WITHDRAWN, raises KeyError on missing
  - ConsentManager.has_consent — True/False for GRANTED/WITHDRAWN/missing + min_version
  - ConsentManager.get — returns record or None
  - ConsentManager.list_user — returns all records for user
  - ConsentManager.list_purpose — filters by purpose
  - ConsentManager.revoke_all — withdraws all GRANTED, returns count
  - ConsentManager.granted_users — correct list + min_version filter
  - ConsentManager.delete — removes record, returns False for missing
  - metadata stored and retrieved correctly
  - Persistence across ConsentManager instances (file DB)
  - Thread safety (concurrent grants)
  - Virtual time via now_fn
"""
from __future__ import annotations

import threading
import time
from pathlib import Path

import pytest

from docstoolkit.consent_manager import ConsentManager, ConsentRecord, ConsentStatus


# ===========================================================================
# Helpers
# ===========================================================================

def make_manager(db_path: str = ":memory:", now_fn=None) -> ConsentManager:
    return ConsentManager(db_path=db_path, now_fn=now_fn)


def fixed_clock(ts: float):
    """Return a now_fn that always returns *ts*."""
    return lambda: ts


def counter_clock(start: float = 1_000.0, step: float = 1.0):
    """Return a now_fn that increments by *step* on each call."""
    state = [start]

    def _now() -> float:
        t = state[0]
        state[0] += step
        return t

    return _now


# ===========================================================================
# ConsentStatus enum
# ===========================================================================

class TestConsentStatus:
    def test_granted_value(self):
        assert ConsentStatus.GRANTED.value == "granted"

    def test_withdrawn_value(self):
        assert ConsentStatus.WITHDRAWN.value == "withdrawn"

    def test_pending_value(self):
        assert ConsentStatus.PENDING.value == "pending"

    def test_is_str_enum(self):
        assert isinstance(ConsentStatus.GRANTED, str)

    def test_total_members(self):
        assert len(ConsentStatus) == 3

    def test_equality_with_string(self):
        assert ConsentStatus.GRANTED == "granted"


# ===========================================================================
# ConsentRecord dataclass
# ===========================================================================

class TestConsentRecord:
    def test_required_fields(self):
        r = ConsentRecord(user_id="u1", purpose="analytics", status=ConsentStatus.GRANTED)
        assert r.user_id == "u1"
        assert r.purpose == "analytics"
        assert r.status == ConsentStatus.GRANTED

    def test_version_default(self):
        r = ConsentRecord(user_id="u1", purpose="p", status=ConsentStatus.PENDING)
        assert r.version == 1

    def test_granted_at_default_none(self):
        r = ConsentRecord(user_id="u1", purpose="p", status=ConsentStatus.PENDING)
        assert r.granted_at is None

    def test_withdrawn_at_default_none(self):
        r = ConsentRecord(user_id="u1", purpose="p", status=ConsentStatus.PENDING)
        assert r.withdrawn_at is None

    def test_metadata_default_empty_dict(self):
        r = ConsentRecord(user_id="u1", purpose="p", status=ConsentStatus.PENDING)
        assert r.metadata == {}

    def test_metadata_not_shared_between_instances(self):
        r1 = ConsentRecord(user_id="u1", purpose="p", status=ConsentStatus.PENDING)
        r2 = ConsentRecord(user_id="u2", purpose="p", status=ConsentStatus.PENDING)
        r1.metadata["key"] = "value"
        assert r2.metadata == {}

    def test_explicit_fields(self):
        r = ConsentRecord(
            user_id="u1",
            purpose="marketing",
            status=ConsentStatus.WITHDRAWN,
            version=3,
            granted_at=100.0,
            withdrawn_at=200.0,
            metadata={"ip": "1.2.3.4"},
        )
        assert r.version == 3
        assert r.granted_at == 100.0
        assert r.withdrawn_at == 200.0
        assert r.metadata == {"ip": "1.2.3.4"}


# ===========================================================================
# ConsentManager.grant
# ===========================================================================

class TestGrant:
    def test_grant_returns_consent_record(self):
        mgr = make_manager()
        r = mgr.grant("u1", "analytics")
        assert isinstance(r, ConsentRecord)

    def test_grant_status_is_granted(self):
        mgr = make_manager()
        r = mgr.grant("u1", "analytics")
        assert r.status == ConsentStatus.GRANTED

    def test_grant_sets_user_id(self):
        mgr = make_manager()
        r = mgr.grant("alice", "marketing")
        assert r.user_id == "alice"

    def test_grant_sets_purpose(self):
        mgr = make_manager()
        r = mgr.grant("u1", "marketing")
        assert r.purpose == "marketing"

    def test_grant_sets_granted_at(self):
        ts = 9999.0
        mgr = make_manager(now_fn=fixed_clock(ts))
        r = mgr.grant("u1", "p")
        assert r.granted_at == ts

    def test_grant_withdrawn_at_is_none(self):
        mgr = make_manager()
        r = mgr.grant("u1", "p")
        assert r.withdrawn_at is None

    def test_grant_default_version(self):
        mgr = make_manager()
        r = mgr.grant("u1", "p")
        assert r.version == 1

    def test_grant_custom_version(self):
        mgr = make_manager()
        r = mgr.grant("u1", "p", version=5)
        assert r.version == 5

    def test_grant_overwrites_existing(self):
        clock = counter_clock(1000.0)
        mgr = make_manager(now_fn=clock)
        mgr.grant("u1", "p", version=1)
        r2 = mgr.grant("u1", "p", version=2)
        assert r2.version == 2
        assert r2.status == ConsentStatus.GRANTED

    def test_grant_overwrites_withdrawn(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "p")
        mgr.withdraw("u1", "p")
        r = mgr.grant("u1", "p")
        assert r.status == ConsentStatus.GRANTED
        assert r.withdrawn_at is None

    def test_grant_multiple_purposes(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        mgr.grant("u1", "marketing")
        records = mgr.list_user("u1")
        assert len(records) == 2

    def test_grant_multiple_users_same_purpose(self):
        mgr = make_manager()
        mgr.grant("alice", "analytics")
        mgr.grant("bob", "analytics")
        users = mgr.granted_users("analytics")
        assert set(users) == {"alice", "bob"}


# ===========================================================================
# ConsentManager.withdraw
# ===========================================================================

class TestWithdraw:
    def test_withdraw_returns_record(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "p")
        r = mgr.withdraw("u1", "p")
        assert isinstance(r, ConsentRecord)

    def test_withdraw_sets_status_withdrawn(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "p")
        r = mgr.withdraw("u1", "p")
        assert r.status == ConsentStatus.WITHDRAWN

    def test_withdraw_sets_withdrawn_at(self):
        clock = counter_clock(1000.0)
        mgr = make_manager(now_fn=clock)
        mgr.grant("u1", "p")          # consumes t=1000
        r = mgr.withdraw("u1", "p")   # consumes t=1001
        assert r.withdrawn_at == 1001.0

    def test_withdraw_preserves_granted_at(self):
        clock = counter_clock(500.0)
        mgr = make_manager(now_fn=clock)
        r1 = mgr.grant("u1", "p")     # granted_at=500
        r2 = mgr.withdraw("u1", "p")
        assert r2.granted_at == r1.granted_at

    def test_withdraw_raises_key_error_missing(self):
        mgr = make_manager()
        with pytest.raises(KeyError):
            mgr.withdraw("nobody", "analytics")

    def test_withdraw_raises_key_error_wrong_purpose(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "analytics")
        with pytest.raises(KeyError):
            mgr.withdraw("u1", "marketing")

    def test_withdraw_after_withdraw_raises(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "p")
        mgr.withdraw("u1", "p")
        # Record still exists but withdraw again should succeed (not re-raise):
        # actually the spec only raises if *no record* exists — a WITHDRAWN record
        # exists, so it should succeed and keep status WITHDRAWN.
        r = mgr.withdraw("u1", "p")
        assert r.status == ConsentStatus.WITHDRAWN


# ===========================================================================
# ConsentManager.has_consent
# ===========================================================================

class TestHasConsent:
    def test_returns_true_for_granted(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        assert mgr.has_consent("u1", "analytics") is True

    def test_returns_false_for_withdrawn(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "analytics")
        mgr.withdraw("u1", "analytics")
        assert mgr.has_consent("u1", "analytics") is False

    def test_returns_false_for_missing(self):
        mgr = make_manager()
        assert mgr.has_consent("nobody", "analytics") is False

    def test_returns_false_wrong_purpose(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        assert mgr.has_consent("u1", "marketing") is False

    def test_min_version_exact_match(self):
        mgr = make_manager()
        mgr.grant("u1", "p", version=3)
        assert mgr.has_consent("u1", "p", min_version=3) is True

    def test_min_version_higher_ok(self):
        mgr = make_manager()
        mgr.grant("u1", "p", version=5)
        assert mgr.has_consent("u1", "p", min_version=3) is True

    def test_min_version_too_low(self):
        mgr = make_manager()
        mgr.grant("u1", "p", version=2)
        assert mgr.has_consent("u1", "p", min_version=3) is False

    def test_min_version_default_one(self):
        mgr = make_manager()
        mgr.grant("u1", "p", version=1)
        assert mgr.has_consent("u1", "p") is True

    def test_pending_status_returns_false(self):
        # PENDING records can only be inserted directly via SQL in tests;
        # has_consent should return False for non-GRANTED statuses.
        mgr = make_manager()
        # Insert a PENDING record bypassing public API
        mgr._conn.execute(
            "INSERT INTO consent (user_id, purpose, status, version) VALUES (?, ?, ?, ?)",
            ("u1", "p", "pending", 1),
        )
        mgr._conn.commit()
        assert mgr.has_consent("u1", "p") is False


# ===========================================================================
# ConsentManager.get
# ===========================================================================

class TestGet:
    def test_get_returns_record(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        r = mgr.get("u1", "analytics")
        assert r is not None
        assert r.user_id == "u1"
        assert r.purpose == "analytics"

    def test_get_returns_none_missing(self):
        mgr = make_manager()
        assert mgr.get("nobody", "analytics") is None

    def test_get_after_withdraw(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "p")
        mgr.withdraw("u1", "p")
        r = mgr.get("u1", "p")
        assert r is not None
        assert r.status == ConsentStatus.WITHDRAWN

    def test_get_returns_correct_version(self):
        mgr = make_manager()
        mgr.grant("u1", "p", version=7)
        r = mgr.get("u1", "p")
        assert r.version == 7


# ===========================================================================
# ConsentManager.list_user
# ===========================================================================

class TestListUser:
    def test_list_user_empty(self):
        mgr = make_manager()
        assert mgr.list_user("nobody") == []

    def test_list_user_single(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        records = mgr.list_user("u1")
        assert len(records) == 1
        assert records[0].purpose == "analytics"

    def test_list_user_multiple(self):
        mgr = make_manager()
        for purpose in ("analytics", "marketing", "research"):
            mgr.grant("u1", purpose)
        records = mgr.list_user("u1")
        assert len(records) == 3
        purposes = {r.purpose for r in records}
        assert purposes == {"analytics", "marketing", "research"}

    def test_list_user_isolates_users(self):
        mgr = make_manager()
        mgr.grant("alice", "analytics")
        mgr.grant("bob", "analytics")
        records = mgr.list_user("alice")
        assert all(r.user_id == "alice" for r in records)
        assert len(records) == 1

    def test_list_user_includes_withdrawn(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "analytics")
        mgr.withdraw("u1", "analytics")
        mgr.grant("u1", "marketing")
        records = mgr.list_user("u1")
        assert len(records) == 2


# ===========================================================================
# ConsentManager.list_purpose
# ===========================================================================

class TestListPurpose:
    def test_list_purpose_empty(self):
        mgr = make_manager()
        assert mgr.list_purpose("nonexistent") == []

    def test_list_purpose_single(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        records = mgr.list_purpose("analytics")
        assert len(records) == 1

    def test_list_purpose_multiple_users(self):
        mgr = make_manager()
        for user in ("alice", "bob", "carol"):
            mgr.grant(user, "analytics")
        records = mgr.list_purpose("analytics")
        assert len(records) == 3
        assert {r.user_id for r in records} == {"alice", "bob", "carol"}

    def test_list_purpose_isolates_purposes(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        mgr.grant("u1", "marketing")
        records = mgr.list_purpose("analytics")
        assert all(r.purpose == "analytics" for r in records)

    def test_list_purpose_includes_withdrawn(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "analytics")
        mgr.withdraw("u1", "analytics")
        records = mgr.list_purpose("analytics")
        assert len(records) == 1
        assert records[0].status == ConsentStatus.WITHDRAWN


# ===========================================================================
# ConsentManager.revoke_all
# ===========================================================================

class TestRevokeAll:
    def test_revoke_all_returns_count(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        mgr.grant("u1", "marketing")
        count = mgr.revoke_all("u1")
        assert count == 2

    def test_revoke_all_sets_withdrawn(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        mgr.grant("u1", "marketing")
        mgr.revoke_all("u1")
        for r in mgr.list_user("u1"):
            assert r.status == ConsentStatus.WITHDRAWN

    def test_revoke_all_no_grants_returns_zero(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "analytics")
        mgr.withdraw("u1", "analytics")
        count = mgr.revoke_all("u1")
        assert count == 0

    def test_revoke_all_missing_user_returns_zero(self):
        mgr = make_manager()
        count = mgr.revoke_all("nobody")
        assert count == 0

    def test_revoke_all_only_affects_target_user(self):
        mgr = make_manager()
        mgr.grant("alice", "analytics")
        mgr.grant("bob", "analytics")
        mgr.revoke_all("alice")
        assert mgr.has_consent("bob", "analytics") is True

    def test_revoke_all_sets_withdrawn_at(self):
        ts = 7777.0
        mgr = make_manager(now_fn=fixed_clock(ts))
        mgr.grant("u1", "analytics")
        mgr.revoke_all("u1")
        r = mgr.get("u1", "analytics")
        assert r.withdrawn_at == ts

    def test_revoke_all_skips_already_withdrawn(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "analytics")
        mgr.grant("u1", "marketing")
        mgr.withdraw("u1", "analytics")
        count = mgr.revoke_all("u1")
        assert count == 1   # only marketing was GRANTED


# ===========================================================================
# ConsentManager.granted_users
# ===========================================================================

class TestGrantedUsers:
    def test_granted_users_empty(self):
        mgr = make_manager()
        assert mgr.granted_users("analytics") == []

    def test_granted_users_returns_ids(self):
        mgr = make_manager()
        mgr.grant("alice", "analytics")
        mgr.grant("bob", "analytics")
        users = mgr.granted_users("analytics")
        assert set(users) == {"alice", "bob"}

    def test_granted_users_excludes_withdrawn(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("alice", "analytics")
        mgr.grant("bob", "analytics")
        mgr.withdraw("bob", "analytics")
        users = mgr.granted_users("analytics")
        assert users == ["alice"]

    def test_granted_users_respects_min_version(self):
        mgr = make_manager()
        mgr.grant("alice", "analytics", version=1)
        mgr.grant("bob", "analytics", version=2)
        mgr.grant("carol", "analytics", version=3)
        users = mgr.granted_users("analytics", min_version=2)
        assert set(users) == {"bob", "carol"}

    def test_granted_users_min_version_excludes_all(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics", version=1)
        users = mgr.granted_users("analytics", min_version=99)
        assert users == []

    def test_granted_users_isolates_purpose(self):
        mgr = make_manager()
        mgr.grant("alice", "analytics")
        mgr.grant("bob", "marketing")
        users = mgr.granted_users("analytics")
        assert users == ["alice"]


# ===========================================================================
# ConsentManager.delete
# ===========================================================================

class TestDelete:
    def test_delete_returns_true(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        assert mgr.delete("u1", "analytics") is True

    def test_delete_removes_record(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        mgr.delete("u1", "analytics")
        assert mgr.get("u1", "analytics") is None

    def test_delete_returns_false_missing(self):
        mgr = make_manager()
        assert mgr.delete("nobody", "analytics") is False

    def test_delete_idempotent(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        mgr.delete("u1", "analytics")
        assert mgr.delete("u1", "analytics") is False

    def test_delete_does_not_affect_other_purposes(self):
        mgr = make_manager()
        mgr.grant("u1", "analytics")
        mgr.grant("u1", "marketing")
        mgr.delete("u1", "analytics")
        assert mgr.get("u1", "marketing") is not None

    def test_delete_does_not_affect_other_users(self):
        mgr = make_manager()
        mgr.grant("alice", "analytics")
        mgr.grant("bob", "analytics")
        mgr.delete("alice", "analytics")
        assert mgr.get("bob", "analytics") is not None


# ===========================================================================
# Metadata
# ===========================================================================

class TestMetadata:
    def test_metadata_stored_and_retrieved(self):
        mgr = make_manager()
        meta = {"ip": "10.0.0.1", "channel": "web", "version": 2}
        r = mgr.grant("u1", "analytics", metadata=meta)
        assert r.metadata == meta

    def test_metadata_retrieved_via_get(self):
        mgr = make_manager()
        mgr.grant("u1", "p", metadata={"source": "mobile"})
        r = mgr.get("u1", "p")
        assert r.metadata == {"source": "mobile"}

    def test_metadata_none_defaults_to_empty_dict(self):
        mgr = make_manager()
        r = mgr.grant("u1", "p", metadata=None)
        assert r.metadata == {}

    def test_metadata_preserved_after_withdraw(self):
        mgr = make_manager(now_fn=counter_clock())
        mgr.grant("u1", "p", metadata={"ref": "abc"})
        r = mgr.withdraw("u1", "p")
        assert r.metadata == {"ref": "abc"}

    def test_metadata_nested_structure(self):
        mgr = make_manager()
        meta = {"user": {"country": "DE"}, "flags": [1, 2, 3]}
        mgr.grant("u1", "p", metadata=meta)
        r = mgr.get("u1", "p")
        assert r.metadata == meta


# ===========================================================================
# Persistence (file DB)
# ===========================================================================

class TestPersistence:
    def test_record_survives_new_instance(self, tmp_path):
        db = str(tmp_path / "consent.db")
        mgr1 = ConsentManager(db_path=db)
        mgr1.grant("u1", "analytics", version=2, metadata={"ok": True})
        mgr1.close()

        mgr2 = ConsentManager(db_path=db)
        r = mgr2.get("u1", "analytics")
        mgr2.close()

        assert r is not None
        assert r.status == ConsentStatus.GRANTED
        assert r.version == 2
        assert r.metadata == {"ok": True}

    def test_withdrawal_survives_new_instance(self, tmp_path):
        db = str(tmp_path / "consent.db")
        mgr1 = ConsentManager(db_path=db, now_fn=counter_clock())
        mgr1.grant("u1", "p")
        mgr1.withdraw("u1", "p")
        mgr1.close()

        mgr2 = ConsentManager(db_path=db)
        r = mgr2.get("u1", "p")
        mgr2.close()

        assert r.status == ConsentStatus.WITHDRAWN

    def test_deleted_record_absent_in_new_instance(self, tmp_path):
        db = str(tmp_path / "consent.db")
        mgr1 = ConsentManager(db_path=db)
        mgr1.grant("u1", "p")
        mgr1.delete("u1", "p")
        mgr1.close()

        mgr2 = ConsentManager(db_path=db)
        assert mgr2.get("u1", "p") is None
        mgr2.close()

    def test_multiple_records_survive_restart(self, tmp_path):
        db = str(tmp_path / "consent.db")
        mgr1 = ConsentManager(db_path=db)
        for purpose in ("analytics", "marketing", "research"):
            mgr1.grant("u1", purpose)
        mgr1.close()

        mgr2 = ConsentManager(db_path=db)
        records = mgr2.list_user("u1")
        mgr2.close()

        assert len(records) == 3


# ===========================================================================
# Thread safety
# ===========================================================================

class TestThreadSafety:
    def test_concurrent_grants_no_data_loss(self):
        mgr = make_manager()
        purposes = [f"purpose_{i}" for i in range(50)]
        errors: list[Exception] = []

        def _grant(purpose: str) -> None:
            try:
                mgr.grant("shared_user", purpose)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=_grant, args=(p,)) for p in purposes]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Unexpected errors: {errors}"
        records = mgr.list_user("shared_user")
        assert len(records) == 50

    def test_concurrent_grants_different_users(self):
        mgr = make_manager()
        users = [f"user_{i}" for i in range(30)]
        errors: list[Exception] = []

        def _grant(user_id: str) -> None:
            try:
                mgr.grant(user_id, "analytics")
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=_grant, args=(u,)) for u in users]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        granted = mgr.granted_users("analytics")
        assert set(granted) == set(users)

    def test_concurrent_revoke_and_grant(self):
        """Grant then revoke in parallel — no exceptions expected."""
        mgr = make_manager(now_fn=time.time)
        for i in range(20):
            mgr.grant(f"u{i}", "p")

        errors: list[Exception] = []

        def _revoke(user_id: str) -> None:
            try:
                mgr.revoke_all(user_id)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=_revoke, args=(f"u{i}",)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []


# ===========================================================================
# Virtual time via now_fn
# ===========================================================================

class TestVirtualTime:
    def test_now_fn_called_on_grant(self):
        calls: list[float] = []

        def recording_clock() -> float:
            t = float(len(calls) + 1) * 100
            calls.append(t)
            return t

        mgr = make_manager(now_fn=recording_clock)
        r = mgr.grant("u1", "p")
        assert len(calls) == 1
        assert r.granted_at == 100.0

    def test_now_fn_called_on_withdraw(self):
        clock = counter_clock(start=0.0, step=50.0)
        mgr = make_manager(now_fn=clock)
        mgr.grant("u1", "p")      # t=0.0
        r = mgr.withdraw("u1", "p")  # t=50.0
        assert r.granted_at == 0.0
        assert r.withdrawn_at == 50.0

    def test_now_fn_called_on_revoke_all(self):
        clock = counter_clock(start=200.0, step=10.0)
        mgr = make_manager(now_fn=clock)
        mgr.grant("u1", "analytics")  # t=200
        mgr.grant("u1", "marketing")  # t=210
        mgr.revoke_all("u1")          # t=220

        for r in mgr.list_user("u1"):
            assert r.withdrawn_at == 220.0

    def test_fixed_clock_no_real_sleep(self):
        """No time.sleep needed — virtual clock is injected."""
        mgr = make_manager(now_fn=fixed_clock(42.0))
        r1 = mgr.grant("u1", "p")
        # Overwrite — second grant should also get t=42 from the fixed clock
        r2 = mgr.grant("u1", "p", version=2)
        assert r1.granted_at == 42.0
        assert r2.granted_at == 42.0

    def test_counter_clock_monotonically_increases(self):
        clock = counter_clock(start=0.0, step=1.0)
        mgr = make_manager(now_fn=clock)
        r1 = mgr.grant("u1", "analytics")
        r2 = mgr.grant("u1", "marketing")
        assert r2.granted_at > r1.granted_at
