"""Tests for docstoolkit.access_log_v2."""
import pytest

from docstoolkit.access_log_v2 import (
    AccessEntry,
    AccessLevel,
    AccessLogV2,
    Anomaly,
)


# ---------------------------------------------------------------------------
# AccessLevel
# ---------------------------------------------------------------------------


class TestAccessLevel:
    def test_has_info(self):
        assert AccessLevel.INFO.value == "info"

    def test_has_warn(self):
        assert AccessLevel.WARN.value == "warn"

    def test_has_error(self):
        assert AccessLevel.ERROR.value == "error"

    def test_has_critical(self):
        assert AccessLevel.CRITICAL.value == "critical"

    def test_levels_are_distinct(self):
        assert (
            len(
                {
                    AccessLevel.INFO,
                    AccessLevel.WARN,
                    AccessLevel.ERROR,
                    AccessLevel.CRITICAL,
                }
            )
            == 4
        )


# ---------------------------------------------------------------------------
# AccessEntry
# ---------------------------------------------------------------------------


class TestAccessEntry:
    def test_default_construction(self):
        e = AccessEntry()
        assert e.entry_id == 0
        assert e.subject == ""
        assert e.action == ""
        assert e.resource == ""
        assert e.ip_address is None
        assert e.level is AccessLevel.INFO
        assert e.success is True
        assert e.timestamp == 0.0
        assert e.details == {}

    def test_full_construction(self):
        e = AccessEntry(
            entry_id=5,
            subject="alice",
            action="read",
            resource="/file",
            ip_address="1.2.3.4",
            level=AccessLevel.ERROR,
            success=False,
            timestamp=42.0,
            details={"k": "v"},
        )
        assert e.entry_id == 5
        assert e.subject == "alice"
        assert e.level is AccessLevel.ERROR
        assert e.success is False
        assert e.details == {"k": "v"}

    def test_details_independent_per_instance(self):
        a = AccessEntry()
        b = AccessEntry()
        a.details["x"] = 1
        assert "x" not in b.details


# ---------------------------------------------------------------------------
# Anomaly
# ---------------------------------------------------------------------------


class TestAnomaly:
    def test_construction(self):
        a = Anomaly(
            anomaly_type="high_freq",
            subject="bob",
            count=150,
            time_window=300.0,
            severity=AccessLevel.WARN,
        )
        assert a.anomaly_type == "high_freq"
        assert a.subject == "bob"
        assert a.count == 150
        assert a.time_window == 300.0
        assert a.severity is AccessLevel.WARN


# ---------------------------------------------------------------------------
# log()
# ---------------------------------------------------------------------------


class TestLog:
    def test_returns_entry(self):
        log = AccessLogV2()
        e = log.log("alice", "read", "/r", now=1.0)
        assert isinstance(e, AccessEntry)
        assert e.subject == "alice"
        assert e.action == "read"
        assert e.resource == "/r"

    def test_assigns_incrementing_ids(self):
        log = AccessLogV2()
        a = log.log("u", "a", "r", now=1.0)
        b = log.log("u", "a", "r", now=2.0)
        c = log.log("u", "a", "r", now=3.0)
        assert a.entry_id == 1
        assert b.entry_id == 2
        assert c.entry_id == 3

    def test_stores_ip(self):
        log = AccessLogV2()
        e = log.log("u", "a", "r", ip_address="9.9.9.9", now=0.0)
        assert e.ip_address == "9.9.9.9"

    def test_default_ip_is_none(self):
        log = AccessLogV2()
        e = log.log("u", "a", "r", now=0.0)
        assert e.ip_address is None

    def test_stores_level(self):
        log = AccessLogV2()
        e = log.log("u", "a", "r", level=AccessLevel.CRITICAL, now=0.0)
        assert e.level is AccessLevel.CRITICAL

    def test_default_level_is_info(self):
        log = AccessLogV2()
        e = log.log("u", "a", "r", now=0.0)
        assert e.level is AccessLevel.INFO

    def test_stores_success_false(self):
        log = AccessLogV2()
        e = log.log("u", "a", "r", success=False, now=0.0)
        assert e.success is False

    def test_details_via_kwargs(self):
        log = AccessLogV2()
        e = log.log("u", "a", "r", now=0.0, foo=1, bar="x")
        assert e.details == {"foo": 1, "bar": "x"}

    def test_increments_total(self):
        log = AccessLogV2()
        assert log.total_entries == 0
        log.log("u", "a", "r", now=0.0)
        log.log("u", "a", "r", now=1.0)
        assert log.total_entries == 2


# ---------------------------------------------------------------------------
# query()
# ---------------------------------------------------------------------------


@pytest.fixture
def populated_log():
    log = AccessLogV2()
    log.log("alice", "read", "/file1", ip_address="1.1.1.1", now=1.0)
    log.log("alice", "write", "/file1", ip_address="1.1.1.1", now=2.0,
            level=AccessLevel.WARN)
    log.log("bob", "read", "/file2", ip_address="2.2.2.2", success=False, now=3.0)
    log.log("alice", "read", "/file2", ip_address="1.1.1.1", now=4.0,
            level=AccessLevel.ERROR)
    log.log("bob", "delete", "/file1", ip_address="2.2.2.2", now=5.0,
            success=False, level=AccessLevel.CRITICAL)
    return log


class TestQuery:
    def test_no_filters_returns_all(self, populated_log):
        assert len(populated_log.query()) == 5

    def test_by_subject(self, populated_log):
        rs = populated_log.query(subject="alice")
        assert len(rs) == 3
        assert all(e.subject == "alice" for e in rs)

    def test_by_action(self, populated_log):
        rs = populated_log.query(action="read")
        assert len(rs) == 3

    def test_by_resource(self, populated_log):
        rs = populated_log.query(resource="/file1")
        assert len(rs) == 3

    def test_by_level(self, populated_log):
        rs = populated_log.query(level=AccessLevel.CRITICAL)
        assert len(rs) == 1
        assert rs[0].subject == "bob"

    def test_by_success_true(self, populated_log):
        rs = populated_log.query(success=True)
        assert len(rs) == 3

    def test_by_success_false(self, populated_log):
        rs = populated_log.query(success=False)
        assert len(rs) == 2

    def test_by_ip(self, populated_log):
        rs = populated_log.query(ip="1.1.1.1")
        assert len(rs) == 3

    def test_by_start(self, populated_log):
        rs = populated_log.query(start=3.0)
        assert len(rs) == 3

    def test_by_end(self, populated_log):
        rs = populated_log.query(end=2.0)
        assert len(rs) == 2

    def test_by_range(self, populated_log):
        rs = populated_log.query(start=2.0, end=4.0)
        assert len(rs) == 3

    def test_with_limit(self, populated_log):
        rs = populated_log.query(limit=2)
        assert len(rs) == 2

    def test_combined_filters(self, populated_log):
        rs = populated_log.query(subject="alice", action="read")
        assert len(rs) == 2

    def test_no_match_returns_empty(self, populated_log):
        assert populated_log.query(subject="ghost") == []


# ---------------------------------------------------------------------------
# count()
# ---------------------------------------------------------------------------


class TestCount:
    def test_total(self, populated_log):
        assert populated_log.count() == 5

    def test_by_subject(self, populated_log):
        assert populated_log.count(subject="alice") == 3
        assert populated_log.count(subject="bob") == 2

    def test_by_success(self, populated_log):
        assert populated_log.count(success=True) == 3
        assert populated_log.count(success=False) == 2

    def test_by_time_range(self, populated_log):
        assert populated_log.count(start=2.0, end=4.0) == 3

    def test_no_match(self, populated_log):
        assert populated_log.count(subject="ghost") == 0


# ---------------------------------------------------------------------------
# recent()
# ---------------------------------------------------------------------------


class TestRecent:
    def test_recent_default(self, populated_log):
        rs = populated_log.recent()
        assert len(rs) == 5

    def test_recent_specific(self, populated_log):
        rs = populated_log.recent(2)
        assert len(rs) == 2
        # Last two entries — bob/delete and alice/read at 4.0
        assert rs[-1].subject == "bob"
        assert rs[-1].action == "delete"

    def test_recent_more_than_size(self, populated_log):
        rs = populated_log.recent(100)
        assert len(rs) == 5

    def test_recent_zero(self, populated_log):
        assert populated_log.recent(0) == []

    def test_recent_negative(self, populated_log):
        assert populated_log.recent(-3) == []

    def test_recent_on_empty(self):
        log = AccessLogV2()
        assert log.recent(5) == []


# ---------------------------------------------------------------------------
# latest_for_subject()
# ---------------------------------------------------------------------------


class TestLatestForSubject:
    def test_returns_latest(self, populated_log):
        e = populated_log.latest_for_subject("alice")
        assert e is not None
        assert e.timestamp == 4.0

    def test_returns_none_for_unknown(self, populated_log):
        assert populated_log.latest_for_subject("ghost") is None

    def test_on_empty(self):
        log = AccessLogV2()
        assert log.latest_for_subject("alice") is None

    def test_multiple_subjects(self, populated_log):
        e = populated_log.latest_for_subject("bob")
        assert e.timestamp == 5.0


# ---------------------------------------------------------------------------
# block_ip()
# ---------------------------------------------------------------------------


class TestBlockIp:
    def test_block_adds_to_list(self):
        log = AccessLogV2()
        log.block_ip("1.1.1.1")
        assert log.is_blocked("1.1.1.1")

    def test_block_with_reason(self):
        log = AccessLogV2()
        log.block_ip("1.1.1.1", reason="spam")
        assert log.is_blocked("1.1.1.1")

    def test_block_idempotent(self):
        log = AccessLogV2()
        log.block_ip("1.1.1.1")
        log.block_ip("1.1.1.1")
        assert len(log.blocked_ips()) == 1

    def test_block_multiple(self):
        log = AccessLogV2()
        log.block_ip("1.1.1.1")
        log.block_ip("2.2.2.2")
        assert len(log.blocked_ips()) == 2


# ---------------------------------------------------------------------------
# unblock_ip()
# ---------------------------------------------------------------------------


class TestUnblockIp:
    def test_unblock_returns_true(self):
        log = AccessLogV2()
        log.block_ip("1.1.1.1")
        assert log.unblock_ip("1.1.1.1") is True
        assert not log.is_blocked("1.1.1.1")

    def test_unblock_unknown_returns_false(self):
        log = AccessLogV2()
        assert log.unblock_ip("9.9.9.9") is False

    def test_unblock_twice(self):
        log = AccessLogV2()
        log.block_ip("1.1.1.1")
        assert log.unblock_ip("1.1.1.1") is True
        assert log.unblock_ip("1.1.1.1") is False


# ---------------------------------------------------------------------------
# is_blocked()
# ---------------------------------------------------------------------------


class TestIsBlocked:
    def test_unknown_ip_not_blocked(self):
        log = AccessLogV2()
        assert log.is_blocked("9.9.9.9") is False

    def test_blocked_then_unblocked(self):
        log = AccessLogV2()
        log.block_ip("1.1.1.1")
        assert log.is_blocked("1.1.1.1") is True
        log.unblock_ip("1.1.1.1")
        assert log.is_blocked("1.1.1.1") is False


# ---------------------------------------------------------------------------
# blocked_ips()
# ---------------------------------------------------------------------------


class TestBlockedIps:
    def test_empty(self):
        log = AccessLogV2()
        assert log.blocked_ips() == []

    def test_sorted(self):
        log = AccessLogV2()
        log.block_ip("2.2.2.2")
        log.block_ip("1.1.1.1")
        log.block_ip("3.3.3.3")
        assert log.blocked_ips() == ["1.1.1.1", "2.2.2.2", "3.3.3.3"]


# ---------------------------------------------------------------------------
# detect_anomalies — high freq
# ---------------------------------------------------------------------------


class TestDetectAnomaliesHighFreq:
    def test_no_anomaly_below_threshold(self):
        log = AccessLogV2()
        for i in range(50):
            log.log("alice", "read", "/r", now=float(i))
        anomalies = log.detect_anomalies(
            time_window=1000.0, now=100.0, high_freq_threshold=100,
        )
        assert not any(a.anomaly_type == "high_freq" for a in anomalies)

    def test_anomaly_above_threshold(self):
        log = AccessLogV2()
        for i in range(150):
            log.log("alice", "read", "/r", now=float(i))
        anomalies = log.detect_anomalies(
            time_window=10000.0, now=200.0, high_freq_threshold=100,
        )
        high_freqs = [a for a in anomalies if a.anomaly_type == "high_freq"]
        assert len(high_freqs) == 1
        assert high_freqs[0].subject == "alice"
        assert high_freqs[0].count == 150

    def test_outside_window_ignored(self):
        log = AccessLogV2()
        for i in range(150):
            log.log("alice", "read", "/r", now=float(i))
        # Window is [1000-100, 1000] = [900, 1000] — none of the entries qualify
        anomalies = log.detect_anomalies(
            time_window=100.0, now=1000.0, high_freq_threshold=100,
        )
        assert not any(a.anomaly_type == "high_freq" for a in anomalies)


# ---------------------------------------------------------------------------
# detect_anomalies — failures
# ---------------------------------------------------------------------------


class TestDetectAnomaliesFailures:
    def test_no_anomaly_below_threshold(self):
        log = AccessLogV2()
        for i in range(5):
            log.log("alice", "login", "/auth", success=False, now=float(i))
        anomalies = log.detect_anomalies(
            time_window=1000.0, now=100.0, failure_threshold=10,
        )
        assert not any(a.anomaly_type == "many_failures" for a in anomalies)

    def test_anomaly_above_threshold(self):
        log = AccessLogV2()
        for i in range(20):
            log.log("alice", "login", "/auth", success=False, now=float(i))
        anomalies = log.detect_anomalies(
            time_window=1000.0, now=100.0, failure_threshold=10,
        )
        failures = [a for a in anomalies if a.anomaly_type == "many_failures"]
        assert len(failures) == 1
        assert failures[0].subject == "alice"
        assert failures[0].count == 20
        assert failures[0].severity is AccessLevel.ERROR

    def test_successes_not_counted(self):
        log = AccessLogV2()
        for i in range(20):
            log.log("alice", "login", "/auth", success=True, now=float(i))
        anomalies = log.detect_anomalies(
            time_window=1000.0, now=100.0, failure_threshold=10,
        )
        assert not any(a.anomaly_type == "many_failures" for a in anomalies)


# ---------------------------------------------------------------------------
# detect_anomalies — unusual resource
# ---------------------------------------------------------------------------


class TestDetectAnomaliesUnusualResource:
    def test_known_resource_no_anomaly(self):
        log = AccessLogV2()
        log.log("alice", "read", "/known", now=1.0)
        log.log("alice", "read", "/known", now=100.0)
        anomalies = log.detect_anomalies(
            time_window=50.0, now=110.0,
        )
        assert not any(a.anomaly_type == "unusual_resource" for a in anomalies)

    def test_new_resource_triggers_anomaly(self):
        log = AccessLogV2()
        log.log("alice", "read", "/old", now=1.0)
        log.log("alice", "read", "/new", now=100.0)
        anomalies = log.detect_anomalies(
            time_window=50.0, now=110.0,
        )
        unusual = [a for a in anomalies if a.anomaly_type == "unusual_resource"]
        assert len(unusual) == 1
        assert unusual[0].subject == "alice"
        assert unusual[0].count == 1


# ---------------------------------------------------------------------------
# aggregate_by_subject()
# ---------------------------------------------------------------------------


class TestAggregateBySubject:
    def test_empty(self):
        log = AccessLogV2()
        assert log.aggregate_by_subject() == {}

    def test_counts(self, populated_log):
        agg = populated_log.aggregate_by_subject()
        assert agg["alice"] == 3
        assert agg["bob"] == 2


# ---------------------------------------------------------------------------
# aggregate_by_action()
# ---------------------------------------------------------------------------


class TestAggregateByAction:
    def test_empty(self):
        log = AccessLogV2()
        assert log.aggregate_by_action() == {}

    def test_counts(self, populated_log):
        agg = populated_log.aggregate_by_action()
        assert agg["read"] == 3
        assert agg["write"] == 1
        assert agg["delete"] == 1


# ---------------------------------------------------------------------------
# aggregate_by_resource()
# ---------------------------------------------------------------------------


class TestAggregateByResource:
    def test_empty(self):
        log = AccessLogV2()
        assert log.aggregate_by_resource() == {}

    def test_counts(self, populated_log):
        agg = populated_log.aggregate_by_resource()
        assert agg["/file1"] == 3
        assert agg["/file2"] == 2


# ---------------------------------------------------------------------------
# success_rate()
# ---------------------------------------------------------------------------


class TestSuccessRate:
    def test_empty_returns_zero(self):
        log = AccessLogV2()
        assert log.success_rate() == 0.0

    def test_global(self, populated_log):
        # 3 successes / 5 total
        assert populated_log.success_rate() == pytest.approx(3 / 5)

    def test_for_subject(self, populated_log):
        # alice: 3/3
        assert populated_log.success_rate(subject="alice") == 1.0

    def test_for_bob(self, populated_log):
        # bob: 0/2
        assert populated_log.success_rate(subject="bob") == 0.0

    def test_for_unknown_subject(self, populated_log):
        assert populated_log.success_rate(subject="ghost") == 0.0


# ---------------------------------------------------------------------------
# clear()
# ---------------------------------------------------------------------------


class TestClear:
    def test_clears_entries(self, populated_log):
        populated_log.clear()
        assert populated_log.total_entries == 0
        assert populated_log.query() == []

    def test_clear_preserves_blocks(self):
        log = AccessLogV2()
        log.block_ip("1.1.1.1")
        log.log("u", "a", "r", now=1.0)
        log.clear()
        assert log.is_blocked("1.1.1.1")

    def test_clear_empty(self):
        log = AccessLogV2()
        log.clear()
        assert log.total_entries == 0


# ---------------------------------------------------------------------------
# total_entries property
# ---------------------------------------------------------------------------


class TestTotalEntries:
    def test_starts_zero(self):
        log = AccessLogV2()
        assert log.total_entries == 0

    def test_grows(self):
        log = AccessLogV2()
        log.log("u", "a", "r", now=1.0)
        assert log.total_entries == 1
        log.log("u", "a", "r", now=2.0)
        assert log.total_entries == 2


# ---------------------------------------------------------------------------
# purge_older_than()
# ---------------------------------------------------------------------------


class TestPurgeOlderThan:
    def test_purges_old_entries(self):
        log = AccessLogV2()
        log.log("u", "a", "r", now=1.0)
        log.log("u", "a", "r", now=2.0)
        log.log("u", "a", "r", now=10.0)
        removed = log.purge_older_than(older_than=5.0, now=10.0)
        # cutoff = 10 - 5 = 5  → entries < 5.0 are removed (timestamps 1.0, 2.0)
        assert removed == 2
        assert log.total_entries == 1

    def test_nothing_to_purge(self):
        log = AccessLogV2()
        log.log("u", "a", "r", now=10.0)
        removed = log.purge_older_than(older_than=100.0, now=20.0)
        assert removed == 0
        assert log.total_entries == 1

    def test_purge_all(self):
        log = AccessLogV2()
        log.log("u", "a", "r", now=1.0)
        log.log("u", "a", "r", now=2.0)
        removed = log.purge_older_than(older_than=0.0, now=10.0)
        assert removed == 2
        assert log.total_entries == 0

    def test_purge_on_empty(self):
        log = AccessLogV2()
        assert log.purge_older_than(older_than=1.0, now=10.0) == 0


# ---------------------------------------------------------------------------
# max_entries / FIFO eviction
# ---------------------------------------------------------------------------


class TestMaxEntries:
    def test_evicts_oldest_when_full(self):
        log = AccessLogV2(max_entries=3)
        log.log("u", "a", "r", now=1.0)
        log.log("u", "a", "r", now=2.0)
        log.log("u", "a", "r", now=3.0)
        log.log("u", "a", "r", now=4.0)
        assert log.total_entries == 3
        timestamps = [e.timestamp for e in log.query()]
        assert timestamps == [2.0, 3.0, 4.0]

    def test_default_capacity(self):
        log = AccessLogV2()
        assert log.total_entries == 0
        log.log("u", "a", "r", now=1.0)
        assert log.total_entries == 1


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_query(self):
        log = AccessLogV2()
        assert log.query() == []

    def test_empty_aggregations(self):
        log = AccessLogV2()
        assert log.aggregate_by_subject() == {}
        assert log.aggregate_by_action() == {}
        assert log.aggregate_by_resource() == {}

    def test_log_without_ip(self):
        log = AccessLogV2()
        e = log.log("u", "a", "r", now=1.0)
        assert e.ip_address is None
        # Filtering by ip when None has no semantic effect (None means "no filter")
        assert log.query(ip=None) == [e]

    def test_filter_ip_only_returns_matching(self):
        log = AccessLogV2()
        log.log("u", "a", "r", ip_address="1.1.1.1", now=1.0)
        log.log("u", "a", "r", ip_address=None, now=2.0)
        rs = log.query(ip="1.1.1.1")
        assert len(rs) == 1

    def test_detect_anomalies_on_empty(self):
        log = AccessLogV2()
        assert log.detect_anomalies(time_window=300.0, now=100.0) == []

    def test_recent_after_clear(self):
        log = AccessLogV2()
        log.log("u", "a", "r", now=1.0)
        log.clear()
        assert log.recent() == []
