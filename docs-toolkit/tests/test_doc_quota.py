"""Tests for docstoolkit.doc_quota (E197)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_quota import (
    DocQuota,
    OwnerUsage,
    QuotaCheckResult,
    QuotaError,
    QuotaLimit,
)


class TestQuotaLimit:
    def test_create_with_owner_only(self):
        lim = QuotaLimit(owner_id="alice")
        assert lim.owner_id == "alice"
        assert lim.max_docs is None
        assert lim.max_total_size is None
        assert lim.max_per_doc_size is None
        assert lim.max_tags is None

    def test_create_with_all_fields(self):
        lim = QuotaLimit(
            owner_id="bob",
            max_docs=10,
            max_total_size=1000,
            max_per_doc_size=100,
            max_tags=20,
        )
        assert lim.max_docs == 10
        assert lim.max_total_size == 1000
        assert lim.max_per_doc_size == 100
        assert lim.max_tags == 20

    def test_equality(self):
        a = QuotaLimit(owner_id="x", max_docs=5)
        b = QuotaLimit(owner_id="x", max_docs=5)
        assert a == b


class TestOwnerUsage:
    def test_defaults_zero(self):
        u = OwnerUsage(owner_id="alice")
        assert u.doc_count == 0
        assert u.total_size == 0
        assert u.tag_count == 0
        assert u.updated_at == 0.0

    def test_custom_fields(self):
        u = OwnerUsage(owner_id="bob", doc_count=3, total_size=500, tag_count=2, updated_at=42.0)
        assert u.doc_count == 3
        assert u.total_size == 500
        assert u.tag_count == 2
        assert u.updated_at == 42.0


class TestQuotaCheckResult:
    def test_allowed_basic(self):
        r = QuotaCheckResult(allowed=True)
        assert r.allowed is True
        assert r.reason is None
        assert r.remaining_docs is None
        assert r.remaining_size is None

    def test_with_reason(self):
        r = QuotaCheckResult(allowed=False, reason="too big", remaining_docs=0, remaining_size=10)
        assert r.allowed is False
        assert r.reason == "too big"
        assert r.remaining_docs == 0
        assert r.remaining_size == 10


class TestSetLimit:
    def test_set_limit_returns_limit(self):
        dq = DocQuota()
        lim = dq.set_limit("alice", max_docs=10)
        assert lim.owner_id == "alice"
        assert lim.max_docs == 10

    def test_set_limit_persists(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=5, max_total_size=1000)
        got = dq.get_limit("alice")
        assert got is not None
        assert got.max_docs == 5
        assert got.max_total_size == 1000

    def test_set_limit_overwrites(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=5)
        dq.set_limit("alice", max_docs=10)
        assert dq.get_limit("alice").max_docs == 10

    def test_set_limit_multiple_owners(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=5)
        dq.set_limit("bob", max_docs=10)
        assert dq.get_limit("alice").max_docs == 5
        assert dq.get_limit("bob").max_docs == 10


class TestGetLimit:
    def test_get_nonexistent(self):
        dq = DocQuota()
        assert dq.get_limit("ghost") is None

    def test_get_existing(self):
        dq = DocQuota()
        dq.set_limit("alice", max_tags=3)
        lim = dq.get_limit("alice")
        assert lim.max_tags == 3


class TestCheckAddDocOK:
    def test_no_limit_returns_allowed(self):
        dq = DocQuota()
        r = dq.check_add_doc("ghost", size=1000)
        assert r.allowed is True
        assert r.remaining_docs is None
        assert r.remaining_size is None

    def test_under_limits(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=10, max_total_size=10000)
        r = dq.check_add_doc("alice", size=500)
        assert r.allowed is True
        assert r.remaining_docs == 9
        assert r.remaining_size == 9500

    def test_at_boundary_allowed(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=1, max_total_size=100)
        r = dq.check_add_doc("alice", size=100)
        assert r.allowed is True
        assert r.remaining_docs == 0
        assert r.remaining_size == 0

    def test_remaining_unlimited_fields(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=5)  # no size limit
        r = dq.check_add_doc("alice", size=999999)
        assert r.allowed is True
        assert r.remaining_docs == 4
        assert r.remaining_size is None


class TestCheckAddDocFailMaxDocs:
    def test_exceed_max_docs(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=2)
        dq.record_add("alice", size=1)
        dq.record_add("alice", size=1)
        r = dq.check_add_doc("alice", size=1)
        assert r.allowed is False
        assert "max_docs" in r.reason
        assert r.remaining_docs == 0

    def test_one_doc_limit(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=1)
        dq.record_add("alice", size=10)
        r = dq.check_add_doc("alice", size=10)
        assert r.allowed is False


class TestCheckAddDocFailTotalSize:
    def test_exceed_total_size(self):
        dq = DocQuota()
        dq.set_limit("alice", max_total_size=1000)
        dq.record_add("alice", size=800)
        r = dq.check_add_doc("alice", size=300)
        assert r.allowed is False
        assert "max_total_size" in r.reason

    def test_exact_remaining(self):
        dq = DocQuota()
        dq.set_limit("alice", max_total_size=1000)
        dq.record_add("alice", size=900)
        r = dq.check_add_doc("alice", size=200)
        assert r.allowed is False
        assert r.remaining_size == 100


class TestCheckAddDocFailPerDocSize:
    def test_exceed_per_doc_size(self):
        dq = DocQuota()
        dq.set_limit("alice", max_per_doc_size=100)
        r = dq.check_add_doc("alice", size=101)
        assert r.allowed is False
        assert "per-doc" in r.reason or "max_per_doc_size" in r.reason

    def test_per_doc_at_boundary_ok(self):
        dq = DocQuota()
        dq.set_limit("alice", max_per_doc_size=100)
        r = dq.check_add_doc("alice", size=100)
        assert r.allowed is True


class TestCheckAddDocFailMaxTags:
    def test_exceed_max_tags(self):
        dq = DocQuota()
        dq.set_limit("alice", max_tags=5)
        dq.record_add("alice", size=1, num_tags=4)
        r = dq.check_add_doc("alice", size=1, num_tags=2)
        assert r.allowed is False
        assert "max_tags" in r.reason

    def test_tags_under_limit(self):
        dq = DocQuota()
        dq.set_limit("alice", max_tags=10)
        r = dq.check_add_doc("alice", size=1, num_tags=3)
        assert r.allowed is True


class TestRecordAdd:
    def test_record_add_creates_usage(self):
        dq = DocQuota()
        u = dq.record_add("alice", size=100)
        assert u.doc_count == 1
        assert u.total_size == 100
        assert u.tag_count == 0

    def test_record_add_increments(self):
        dq = DocQuota()
        dq.record_add("alice", size=100)
        u = dq.record_add("alice", size=200, num_tags=3)
        assert u.doc_count == 2
        assert u.total_size == 300
        assert u.tag_count == 3

    def test_record_add_updates_timestamp(self):
        dq = DocQuota()
        u = dq.record_add("alice", size=10, now=123.45)
        assert u.updated_at == 123.45


class TestRecordRemove:
    def test_record_remove_decrements(self):
        dq = DocQuota()
        dq.record_add("alice", size=100, num_tags=2)
        dq.record_add("alice", size=50, num_tags=1)
        u = dq.record_remove("alice", size=50, num_tags=1)
        assert u.doc_count == 1
        assert u.total_size == 100
        assert u.tag_count == 2

    def test_record_remove_nonexistent_owner(self):
        dq = DocQuota()
        assert dq.record_remove("ghost", size=10) is None

    def test_record_remove_clamps_to_zero(self):
        dq = DocQuota()
        dq.record_add("alice", size=10)
        u = dq.record_remove("alice", size=999, num_tags=999)
        assert u.doc_count == 0
        assert u.total_size == 0
        assert u.tag_count == 0

    def test_record_remove_updates_timestamp(self):
        dq = DocQuota()
        dq.record_add("alice", size=10)
        u = dq.record_remove("alice", size=10, now=99.0)
        assert u.updated_at == 99.0


class TestRecordResize:
    def test_record_resize_positive(self):
        dq = DocQuota()
        dq.record_add("alice", size=100)
        u = dq.record_resize("alice", delta_size=50)
        assert u.total_size == 150

    def test_record_resize_negative(self):
        dq = DocQuota()
        dq.record_add("alice", size=100)
        u = dq.record_resize("alice", delta_size=-30)
        assert u.total_size == 70

    def test_record_resize_clamps_negative(self):
        dq = DocQuota()
        dq.record_add("alice", size=10)
        u = dq.record_resize("alice", delta_size=-999)
        assert u.total_size == 0

    def test_record_resize_nonexistent(self):
        dq = DocQuota()
        assert dq.record_resize("ghost", delta_size=10) is None

    def test_record_resize_updates_timestamp(self):
        dq = DocQuota()
        dq.record_add("alice", size=10)
        u = dq.record_resize("alice", delta_size=5, now=77.0)
        assert u.updated_at == 77.0


class TestUsage:
    def test_usage_nonexistent(self):
        dq = DocQuota()
        assert dq.usage("ghost") is None

    def test_usage_after_add(self):
        dq = DocQuota()
        dq.record_add("alice", size=10)
        u = dq.usage("alice")
        assert u is not None
        assert u.doc_count == 1


class TestIsOverQuota:
    def test_no_limit_not_over(self):
        dq = DocQuota()
        dq.record_add("alice", size=100000)
        assert dq.is_over_quota("alice") is False

    def test_no_usage_not_over(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=1)
        assert dq.is_over_quota("alice") is False

    def test_over_docs(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=1)
        dq.record_add("alice", size=1)
        dq.record_add("alice", size=1)  # bypass check
        assert dq.is_over_quota("alice") is True

    def test_over_size(self):
        dq = DocQuota()
        dq.set_limit("alice", max_total_size=100)
        dq.record_add("alice", size=200)
        assert dq.is_over_quota("alice") is True

    def test_over_tags(self):
        dq = DocQuota()
        dq.set_limit("alice", max_tags=5)
        dq.record_add("alice", size=1, num_tags=10)
        assert dq.is_over_quota("alice") is True

    def test_under_quota(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=10)
        dq.record_add("alice", size=1)
        assert dq.is_over_quota("alice") is False


class TestCleanup:
    def test_cleanup_existing(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=5)
        dq.record_add("alice", size=10)
        assert dq.cleanup("alice") is True
        assert dq.get_limit("alice") is None
        assert dq.usage("alice") is None

    def test_cleanup_nonexistent(self):
        dq = DocQuota()
        assert dq.cleanup("ghost") is False

    def test_cleanup_only_limit(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=5)
        assert dq.cleanup("alice") is True

    def test_cleanup_only_usage(self):
        dq = DocQuota()
        dq.record_add("alice", size=10)
        assert dq.cleanup("alice") is True


class TestResetUsage:
    def test_reset_existing(self):
        dq = DocQuota()
        dq.record_add("alice", size=100, num_tags=5)
        assert dq.reset_usage("alice") is True
        u = dq.usage("alice")
        assert u.doc_count == 0
        assert u.total_size == 0
        assert u.tag_count == 0

    def test_reset_nonexistent(self):
        dq = DocQuota()
        assert dq.reset_usage("ghost") is False

    def test_reset_preserves_limit(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=10)
        dq.record_add("alice", size=10)
        dq.reset_usage("alice")
        assert dq.get_limit("alice").max_docs == 10


class TestAllUsages:
    def test_empty(self):
        dq = DocQuota()
        assert dq.all_usages() == []

    def test_multiple(self):
        dq = DocQuota()
        dq.record_add("alice", size=10)
        dq.record_add("bob", size=20)
        usages = dq.all_usages()
        assert len(usages) == 2
        ids = {u.owner_id for u in usages}
        assert ids == {"alice", "bob"}


class TestOwnersOverQuota:
    def test_empty(self):
        dq = DocQuota()
        assert dq.owners_over_quota() == []

    def test_none_over(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=10)
        dq.record_add("alice", size=10)
        assert dq.owners_over_quota() == []

    def test_one_over(self):
        dq = DocQuota()
        dq.set_limit("alice", max_total_size=100)
        dq.set_limit("bob", max_total_size=100)
        dq.record_add("alice", size=200)
        dq.record_add("bob", size=50)
        result = dq.owners_over_quota()
        assert result == ["alice"]

    def test_multiple_over(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=1)
        dq.set_limit("bob", max_total_size=10)
        dq.record_add("alice", size=1)
        dq.record_add("alice", size=1)
        dq.record_add("bob", size=100)
        assert set(dq.owners_over_quota()) == {"alice", "bob"}


class TestDefaultLimit:
    def test_default_applies_to_unconfigured(self):
        dq = DocQuota()
        dq.set_default_limit(max_docs=2)
        dq.record_add("alice", size=1)
        dq.record_add("alice", size=1)
        r = dq.check_add_doc("alice", size=1)
        assert r.allowed is False

    def test_specific_overrides_default(self):
        dq = DocQuota()
        dq.set_default_limit(max_docs=1)
        dq.set_limit("alice", max_docs=10)
        for _ in range(5):
            dq.record_add("alice", size=1)
        r = dq.check_add_doc("alice", size=1)
        assert r.allowed is True

    def test_default_returns_limit(self):
        dq = DocQuota()
        lim = dq.set_default_limit(max_docs=5, max_total_size=500)
        assert lim.max_docs == 5
        assert lim.max_total_size == 500

    def test_default_used_in_is_over_quota(self):
        dq = DocQuota()
        dq.set_default_limit(max_docs=1)
        dq.record_add("alice", size=1)
        dq.record_add("alice", size=1)
        assert dq.is_over_quota("alice") is True

    def test_no_default_no_limit_allows_all(self):
        dq = DocQuota()
        r = dq.check_add_doc("anyone", size=999999, num_tags=100)
        assert r.allowed is True


class TestTotalOwners:
    def test_empty(self):
        dq = DocQuota()
        assert dq.total_owners == 0

    def test_owners_with_limit_only(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=1)
        assert dq.total_owners == 1

    def test_owners_with_usage_only(self):
        dq = DocQuota()
        dq.record_add("bob", size=1)
        assert dq.total_owners == 1

    def test_owners_distinct(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=1)
        dq.record_add("alice", size=1)
        dq.record_add("bob", size=1)
        assert dq.total_owners == 2


class TestEdgeCases:
    def test_zero_size_doc(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=10, max_total_size=100)
        r = dq.check_add_doc("alice", size=0)
        assert r.allowed is True

    def test_zero_max_docs(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=0)
        r = dq.check_add_doc("alice", size=1)
        assert r.allowed is False

    def test_zero_max_total_size(self):
        dq = DocQuota()
        dq.set_limit("alice", max_total_size=0)
        r = dq.check_add_doc("alice", size=1)
        assert r.allowed is False

    def test_quota_error_is_exception(self):
        assert issubclass(QuotaError, Exception)

    def test_unconfigured_owner_no_default_check(self):
        dq = DocQuota()
        r = dq.check_add_doc("ghost", size=10**9)
        assert r.allowed is True
        assert r.remaining_docs is None
        assert r.remaining_size is None

    def test_check_does_not_modify_usage(self):
        dq = DocQuota()
        dq.set_limit("alice", max_docs=10)
        dq.check_add_doc("alice", size=10)
        assert dq.usage("alice") is None

    def test_large_values(self):
        dq = DocQuota()
        dq.set_limit("alice", max_total_size=10**12)
        dq.record_add("alice", size=10**11)
        r = dq.check_add_doc("alice", size=10**11)
        assert r.allowed is True

    def test_per_doc_check_before_total(self):
        # If both per-doc and total would fail, per-doc reason is returned
        dq = DocQuota()
        dq.set_limit("alice", max_per_doc_size=10, max_total_size=5)
        r = dq.check_add_doc("alice", size=100)
        assert r.allowed is False
        assert "per-doc" in r.reason or "max_per_doc_size" in r.reason
