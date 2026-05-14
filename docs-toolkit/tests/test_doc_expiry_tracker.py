"""Tests for docstoolkit.doc_expiry_tracker (E303)."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_expiry_tracker import DocExpiryTracker, ExpiryRecord, ExpiryStats


# --------------------------------------------------------------------------- #
# TestExpiryRecordDataclass
# --------------------------------------------------------------------------- #
class TestExpiryRecordDataclass:
    def test_required_fields(self):
        r = ExpiryRecord(doc_id="doc1", expires_at=1000.0)
        assert r.doc_id == "doc1"
        assert r.expires_at == 1000.0

    def test_created_at_default(self):
        r = ExpiryRecord(doc_id="doc1", expires_at=500.0)
        assert r.created_at == 0.0

    def test_renewed_at_default_is_none(self):
        r = ExpiryRecord(doc_id="doc1", expires_at=500.0)
        assert r.renewed_at is None

    def test_grace_seconds_default(self):
        r = ExpiryRecord(doc_id="doc1", expires_at=500.0)
        assert r.grace_seconds == 0.0

    def test_label_default(self):
        r = ExpiryRecord(doc_id="doc1", expires_at=500.0)
        assert r.label == ""

    def test_all_fields_explicit(self):
        r = ExpiryRecord(
            doc_id="d",
            expires_at=200.0,
            created_at=100.0,
            renewed_at=150.0,
            grace_seconds=30.0,
            label="my-doc",
        )
        assert r.doc_id == "d"
        assert r.expires_at == 200.0
        assert r.created_at == 100.0
        assert r.renewed_at == 150.0
        assert r.grace_seconds == 30.0
        assert r.label == "my-doc"

    def test_renewed_at_accepts_float(self):
        r = ExpiryRecord(doc_id="d", expires_at=100.0, renewed_at=99.5)
        assert isinstance(r.renewed_at, float)

    def test_renewed_at_accepts_none(self):
        r = ExpiryRecord(doc_id="d", expires_at=100.0, renewed_at=None)
        assert r.renewed_at is None

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(ExpiryRecord)


# --------------------------------------------------------------------------- #
# TestExpiryStatsDataclass
# --------------------------------------------------------------------------- #
class TestExpiryStatsDataclass:
    def test_required_fields(self):
        s = ExpiryStats(total_tracked=5, expired_count=2, expiring_soon_count=1)
        assert s.total_tracked == 5
        assert s.expired_count == 2
        assert s.expiring_soon_count == 1

    def test_soon_seconds_default(self):
        s = ExpiryStats(total_tracked=0, expired_count=0, expiring_soon_count=0)
        assert s.soon_seconds == 3600.0

    def test_soon_seconds_explicit(self):
        s = ExpiryStats(
            total_tracked=1, expired_count=0, expiring_soon_count=0, soon_seconds=300.0
        )
        assert s.soon_seconds == 300.0

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(ExpiryStats)


# --------------------------------------------------------------------------- #
# TestConstruction
# --------------------------------------------------------------------------- #
class TestConstruction:
    def test_empty_state(self):
        tracker = DocExpiryTracker()
        assert tracker.all_records() == []

    def test_expired_docs_empty(self):
        tracker = DocExpiryTracker()
        assert tracker.expired_docs(now=0.0) == []

    def test_expiring_soon_empty(self):
        tracker = DocExpiryTracker()
        assert tracker.expiring_soon(within_seconds=3600.0, now=0.0) == []

    def test_stats_empty(self):
        tracker = DocExpiryTracker()
        s = tracker.stats(now=0.0)
        assert s.total_tracked == 0
        assert s.expired_count == 0
        assert s.expiring_soon_count == 0


# --------------------------------------------------------------------------- #
# TestTrack
# --------------------------------------------------------------------------- #
class TestTrack:
    def test_new_record_stored(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        assert tracker.get("doc1") is not None

    def test_returns_expiry_record(self):
        tracker = DocExpiryTracker()
        record = tracker.track("doc1", expires_at=100.0, now=0.0)
        assert isinstance(record, ExpiryRecord)

    def test_expires_at_stored(self):
        tracker = DocExpiryTracker()
        record = tracker.track("doc1", expires_at=500.0, now=0.0)
        assert record.expires_at == 500.0

    def test_created_at_set_to_now(self):
        tracker = DocExpiryTracker()
        record = tracker.track("doc1", expires_at=100.0, now=42.0)
        assert record.created_at == 42.0

    def test_label_stored(self):
        tracker = DocExpiryTracker()
        record = tracker.track("doc1", expires_at=100.0, label="important", now=0.0)
        assert record.label == "important"

    def test_grace_seconds_stored(self):
        tracker = DocExpiryTracker()
        record = tracker.track("doc1", expires_at=100.0, grace_seconds=60.0, now=0.0)
        assert record.grace_seconds == 60.0

    def test_replace_existing(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        record = tracker.track("doc1", expires_at=200.0, now=5.0)
        assert record.expires_at == 200.0
        assert record.created_at == 5.0
        assert len(tracker.all_records()) == 1

    def test_renewed_at_is_none_on_track(self):
        tracker = DocExpiryTracker()
        record = tracker.track("doc1", expires_at=100.0, now=0.0)
        assert record.renewed_at is None


# --------------------------------------------------------------------------- #
# TestRenew
# --------------------------------------------------------------------------- #
class TestRenew:
    def test_updates_expires_at(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        record = tracker.renew("doc1", new_expires_at=300.0, now=10.0)
        assert record.expires_at == 300.0

    def test_sets_renewed_at(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        record = tracker.renew("doc1", new_expires_at=300.0, now=10.0)
        assert record.renewed_at == 10.0

    def test_not_found_returns_none(self):
        tracker = DocExpiryTracker()
        result = tracker.renew("missing", new_expires_at=300.0, now=10.0)
        assert result is None

    def test_renewed_record_is_same_object_in_store(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        tracker.renew("doc1", new_expires_at=200.0, now=5.0)
        stored = tracker.get("doc1")
        assert stored.expires_at == 200.0
        assert stored.renewed_at == 5.0


# --------------------------------------------------------------------------- #
# TestExtend
# --------------------------------------------------------------------------- #
class TestExtend:
    def test_adds_seconds_to_expires_at(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        record = tracker.extend("doc1", extra_seconds=50.0, now=5.0)
        assert record.expires_at == 150.0

    def test_not_found_returns_none(self):
        tracker = DocExpiryTracker()
        result = tracker.extend("missing", extra_seconds=50.0, now=0.0)
        assert result is None

    def test_sets_renewed_at(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        record = tracker.extend("doc1", extra_seconds=20.0, now=7.0)
        assert record.renewed_at == 7.0

    def test_extend_persists_in_store(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        tracker.extend("doc1", extra_seconds=100.0, now=0.0)
        stored = tracker.get("doc1")
        assert stored.expires_at == 200.0

    def test_extend_by_zero(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        record = tracker.extend("doc1", extra_seconds=0.0, now=1.0)
        assert record.expires_at == 100.0


# --------------------------------------------------------------------------- #
# TestUntrack
# --------------------------------------------------------------------------- #
class TestUntrack:
    def test_returns_true_if_existed(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        assert tracker.untrack("doc1") is True

    def test_returns_false_if_missing(self):
        tracker = DocExpiryTracker()
        assert tracker.untrack("missing") is False

    def test_record_gone_after_untrack(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        tracker.untrack("doc1")
        assert tracker.get("doc1") is None

    def test_untrack_only_removes_target(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        tracker.track("doc2", expires_at=200.0, now=0.0)
        tracker.untrack("doc1")
        assert tracker.get("doc2") is not None


# --------------------------------------------------------------------------- #
# TestGet
# --------------------------------------------------------------------------- #
class TestGet:
    def test_returns_record_when_found(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        record = tracker.get("doc1")
        assert record is not None
        assert record.doc_id == "doc1"

    def test_returns_none_when_not_found(self):
        tracker = DocExpiryTracker()
        assert tracker.get("missing") is None

    def test_returns_expired_record_too(self):
        # get() does not filter by expiry — it's a raw lookup
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=1.0, now=0.0)
        record = tracker.get("doc1")
        assert record is not None


# --------------------------------------------------------------------------- #
# TestIsExpired
# --------------------------------------------------------------------------- #
class TestIsExpired:
    def test_not_expired_before_expiry(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        assert tracker.is_expired("doc1", now=50.0) is False

    def test_not_expired_at_expiry_boundary(self):
        # strict >, so exactly AT expires_at is NOT expired yet
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        assert tracker.is_expired("doc1", now=100.0) is False

    def test_expired_just_past_boundary(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        assert tracker.is_expired("doc1", now=100.001) is True

    def test_expired_well_past_expiry(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        assert tracker.is_expired("doc1", now=999.0) is True

    def test_grace_seconds_extends_expiry(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, grace_seconds=30.0, now=0.0)
        # past expires_at but within grace
        assert tracker.is_expired("doc1", now=110.0) is False

    def test_grace_seconds_expired_past_grace(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, grace_seconds=30.0, now=0.0)
        assert tracker.is_expired("doc1", now=131.0) is True

    def test_not_tracked_returns_false(self):
        tracker = DocExpiryTracker()
        assert tracker.is_expired("missing", now=0.0) is False


# --------------------------------------------------------------------------- #
# TestTimeUntilExpiry
# --------------------------------------------------------------------------- #
class TestTimeUntilExpiry:
    def test_positive_when_not_expired(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        assert tracker.time_until_expiry("doc1", now=40.0) == pytest.approx(60.0)

    def test_negative_when_expired(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        assert tracker.time_until_expiry("doc1", now=120.0) == pytest.approx(-20.0)

    def test_zero_at_effective_boundary(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        assert tracker.time_until_expiry("doc1", now=100.0) == pytest.approx(0.0)

    def test_includes_grace_in_computation(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, grace_seconds=20.0, now=0.0)
        # effective expiry = 120, now = 110 → 10 remaining
        assert tracker.time_until_expiry("doc1", now=110.0) == pytest.approx(10.0)

    def test_none_when_not_tracked(self):
        tracker = DocExpiryTracker()
        assert tracker.time_until_expiry("missing", now=0.0) is None


# --------------------------------------------------------------------------- #
# TestExpiredDocs
# --------------------------------------------------------------------------- #
class TestExpiredDocs:
    def test_empty_tracker(self):
        tracker = DocExpiryTracker()
        assert tracker.expired_docs(now=0.0) == []

    def test_single_expired(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=10.0, now=0.0)
        assert tracker.expired_docs(now=20.0) == ["doc1"]

    def test_single_not_expired(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        assert tracker.expired_docs(now=50.0) == []

    def test_multiple_mixed(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=10.0, now=0.0)
        tracker.track("doc2", expires_at=100.0, now=0.0)
        tracker.track("doc3", expires_at=5.0, now=0.0)
        result = tracker.expired_docs(now=20.0)
        assert sorted(result) == ["doc1", "doc3"]

    def test_result_is_sorted(self):
        tracker = DocExpiryTracker()
        tracker.track("z_doc", expires_at=5.0, now=0.0)
        tracker.track("a_doc", expires_at=5.0, now=0.0)
        tracker.track("m_doc", expires_at=5.0, now=0.0)
        result = tracker.expired_docs(now=10.0)
        assert result == sorted(result)

    def test_grace_respected(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=10.0, grace_seconds=20.0, now=0.0)
        # now=15 is past expires_at but within grace
        assert tracker.expired_docs(now=15.0) == []
        # now=35 is past grace
        assert tracker.expired_docs(now=35.0) == ["doc1"]


# --------------------------------------------------------------------------- #
# TestExpiringSoon
# --------------------------------------------------------------------------- #
class TestExpiringSoon:
    def test_empty_tracker(self):
        tracker = DocExpiryTracker()
        assert tracker.expiring_soon(within_seconds=3600.0, now=0.0) == []

    def test_within_window(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=500.0, now=0.0)
        result = tracker.expiring_soon(within_seconds=3600.0, now=0.0)
        assert "doc1" in result

    def test_excludes_already_expired(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=10.0, now=0.0)
        result = tracker.expiring_soon(within_seconds=3600.0, now=100.0)
        assert "doc1" not in result

    def test_excludes_far_future(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=10000.0, now=0.0)
        result = tracker.expiring_soon(within_seconds=3600.0, now=0.0)
        assert "doc1" not in result

    def test_result_is_sorted(self):
        tracker = DocExpiryTracker()
        tracker.track("z_doc", expires_at=500.0, now=0.0)
        tracker.track("a_doc", expires_at=500.0, now=0.0)
        tracker.track("m_doc", expires_at=500.0, now=0.0)
        result = tracker.expiring_soon(within_seconds=3600.0, now=0.0)
        assert result == sorted(result)

    def test_mixed_soon_and_not_soon(self):
        tracker = DocExpiryTracker()
        tracker.track("soon", expires_at=200.0, now=0.0)
        tracker.track("far", expires_at=5000.0, now=0.0)
        tracker.track("expired", expires_at=1.0, now=0.0)
        result = tracker.expiring_soon(within_seconds=300.0, now=10.0)
        assert result == ["soon"]

    def test_grace_affects_expiring_soon(self):
        tracker = DocExpiryTracker()
        # expires_at=50, grace=100 → effective expiry=150
        # now=0, window=200 → 150 is within 200 → should appear
        tracker.track("doc1", expires_at=50.0, grace_seconds=100.0, now=0.0)
        result = tracker.expiring_soon(within_seconds=200.0, now=0.0)
        assert "doc1" in result


# --------------------------------------------------------------------------- #
# TestAllRecords
# --------------------------------------------------------------------------- #
class TestAllRecords:
    def test_empty(self):
        tracker = DocExpiryTracker()
        assert tracker.all_records() == []

    def test_sorted_by_expires_at(self):
        tracker = DocExpiryTracker()
        tracker.track("doc_c", expires_at=300.0, now=0.0)
        tracker.track("doc_a", expires_at=100.0, now=0.0)
        tracker.track("doc_b", expires_at=200.0, now=0.0)
        records = tracker.all_records()
        assert [r.expires_at for r in records] == [100.0, 200.0, 300.0]

    def test_includes_expired_records(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=1.0, now=0.0)
        tracker.track("doc2", expires_at=1000.0, now=0.0)
        records = tracker.all_records()
        assert len(records) == 2

    def test_returns_list_of_expiry_records(self):
        tracker = DocExpiryTracker()
        tracker.track("doc1", expires_at=100.0, now=0.0)
        records = tracker.all_records()
        assert all(isinstance(r, ExpiryRecord) for r in records)


# --------------------------------------------------------------------------- #
# TestStats
# --------------------------------------------------------------------------- #
class TestStats:
    def test_empty(self):
        tracker = DocExpiryTracker()
        s = tracker.stats(now=0.0)
        assert s.total_tracked == 0
        assert s.expired_count == 0
        assert s.expiring_soon_count == 0

    def test_total_tracked(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=100.0, now=0.0)
        tracker.track("d2", expires_at=200.0, now=0.0)
        s = tracker.stats(now=0.0)
        assert s.total_tracked == 2

    def test_expired_count(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=10.0, now=0.0)
        tracker.track("d2", expires_at=100.0, now=0.0)
        s = tracker.stats(now=50.0)
        assert s.expired_count == 1

    def test_expiring_soon_count(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=500.0, now=0.0)
        tracker.track("d2", expires_at=5000.0, now=0.0)
        s = tracker.stats(now=0.0, soon_seconds=1000.0)
        assert s.expiring_soon_count == 1

    def test_soon_seconds_stored(self):
        tracker = DocExpiryTracker()
        s = tracker.stats(now=0.0, soon_seconds=300.0)
        assert s.soon_seconds == 300.0

    def test_expired_not_counted_as_expiring_soon(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=1.0, now=0.0)
        s = tracker.stats(now=100.0, soon_seconds=50000.0)
        assert s.expired_count == 1
        assert s.expiring_soon_count == 0

    def test_all_expired(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=5.0, now=0.0)
        tracker.track("d2", expires_at=10.0, now=0.0)
        s = tracker.stats(now=100.0)
        assert s.expired_count == 2
        assert s.total_tracked == 2


# --------------------------------------------------------------------------- #
# TestInjectableNow
# --------------------------------------------------------------------------- #
class TestInjectableNow:
    def test_track_uses_now(self):
        tracker = DocExpiryTracker()
        r = tracker.track("d1", expires_at=200.0, now=123.0)
        assert r.created_at == 123.0

    def test_renew_uses_now(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=100.0, now=0.0)
        r = tracker.renew("d1", new_expires_at=200.0, now=55.0)
        assert r.renewed_at == 55.0

    def test_extend_uses_now(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=100.0, now=0.0)
        r = tracker.extend("d1", extra_seconds=50.0, now=77.0)
        assert r.renewed_at == 77.0

    def test_is_expired_uses_now(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=100.0, now=0.0)
        assert tracker.is_expired("d1", now=50.0) is False
        assert tracker.is_expired("d1", now=200.0) is True

    def test_time_until_expiry_uses_now(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=100.0, now=0.0)
        assert tracker.time_until_expiry("d1", now=60.0) == pytest.approx(40.0)

    def test_expired_docs_uses_now(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=50.0, now=0.0)
        assert tracker.expired_docs(now=10.0) == []
        assert tracker.expired_docs(now=100.0) == ["d1"]

    def test_expiring_soon_uses_now(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=100.0, now=0.0)
        # At now=0, d1 expires in 100s — within window of 200
        assert "d1" in tracker.expiring_soon(within_seconds=200.0, now=0.0)
        # At now=200, d1 is already expired
        assert "d1" not in tracker.expiring_soon(within_seconds=200.0, now=200.0)

    def test_stats_uses_now(self):
        tracker = DocExpiryTracker()
        tracker.track("d1", expires_at=50.0, now=0.0)
        s_before = tracker.stats(now=10.0)
        s_after = tracker.stats(now=100.0)
        assert s_before.expired_count == 0
        assert s_after.expired_count == 1


# --------------------------------------------------------------------------- #
# TestThreadSafety
# --------------------------------------------------------------------------- #
class TestThreadSafety:
    def test_concurrent_track_calls(self):
        tracker = DocExpiryTracker()
        errors: list[Exception] = []

        def track_docs(start: int, count: int) -> None:
            try:
                for i in range(start, start + count):
                    tracker.track(f"doc_{i}", expires_at=float(i + 100), now=0.0)
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=track_docs, args=(i * 50, 50))
            for i in range(10)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(tracker.all_records()) == 500

    def test_concurrent_mixed_operations(self):
        tracker = DocExpiryTracker()
        # Pre-populate
        for i in range(20):
            tracker.track(f"doc_{i}", expires_at=float(i + 1000), now=0.0)

        errors: list[Exception] = []

        def mixed_ops() -> None:
            try:
                for i in range(20):
                    tracker.is_expired(f"doc_{i}", now=500.0)
                    tracker.time_until_expiry(f"doc_{i}", now=500.0)
                    tracker.get(f"doc_{i}")
                    tracker.expired_docs(now=500.0)
                    tracker.expiring_soon(within_seconds=1000.0, now=0.0)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=mixed_ops) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
