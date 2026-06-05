"""Tests for E240 doc_audit_query."""
from __future__ import annotations

import pytest

from docstoolkit.doc_audit_query import (
    AggregateType,
    AggregationResult,
    AuditEvent,
    Bucket,
    DocAuditQuery,
    Query,
    TimeBucket,
)


# ---------------------------------------------------------------------------
# Enums and dataclasses
# ---------------------------------------------------------------------------


class TestAggregateType:
    def test_members(self):
        names = {m.name for m in AggregateType}
        assert {
            "COUNT",
            "COUNT_DISTINCT",
            "MIN_TIME",
            "MAX_TIME",
            "FIRST",
            "LAST",
        } <= names

    def test_value_count(self):
        assert AggregateType.COUNT.value == "count"


class TestTimeBucket:
    def test_minute_seconds(self):
        assert TimeBucket.MINUTE.value == 60

    def test_hour_seconds(self):
        assert TimeBucket.HOUR.value == 3600

    def test_day_seconds(self):
        assert TimeBucket.DAY.value == 86400

    def test_week_seconds(self):
        assert TimeBucket.WEEK.value == 604800

    def test_month_seconds(self):
        assert TimeBucket.MONTH.value == 2592000


class TestAuditEvent:
    def test_defaults(self):
        ev = AuditEvent(event_id=1, timestamp=10.0, actor="a", action="b", resource="c")
        assert ev.outcome == "success"
        assert ev.metadata == {}

    def test_full(self):
        ev = AuditEvent(
            event_id=2,
            timestamp=11.0,
            actor="a",
            action="b",
            resource="c",
            outcome="failure",
            metadata={"k": "v"},
        )
        assert ev.outcome == "failure"
        assert ev.metadata == {"k": "v"}


class TestQuery:
    def test_default_none(self):
        q = Query()
        assert q.actors is None
        assert q.actions is None
        assert q.resources is None
        assert q.outcomes is None
        assert q.start is None
        assert q.end is None
        assert q.text_contains is None

    def test_with_values(self):
        q = Query(actors=["a"], actions=["x"], start=1.0, end=2.0, text_contains="z")
        assert q.actors == ["a"]
        assert q.text_contains == "z"


class TestBucket:
    def test_default_events(self):
        b = Bucket(start=0.0, end=60.0)
        assert b.events == []

    def test_with_events(self):
        ev = AuditEvent(event_id=1, timestamp=1.0, actor="a", action="b", resource="c")
        b = Bucket(start=0.0, end=60.0, events=[ev])
        assert b.events == [ev]


class TestAggregationResult:
    def test_basic(self):
        r = AggregationResult(AggregateType.COUNT, 5)
        assert r.aggregate_type == AggregateType.COUNT
        assert r.value == 5


# ---------------------------------------------------------------------------
# add_event / add_events
# ---------------------------------------------------------------------------


class TestAddEvent:
    def test_add_event_basic(self):
        store = DocAuditQuery()
        ev = store.add_event("alice", "read", "doc1", now=10.0)
        assert ev.event_id == 1
        assert ev.actor == "alice"
        assert ev.action == "read"
        assert ev.resource == "doc1"
        assert ev.outcome == "success"
        assert store.total_events == 1

    def test_add_event_metadata(self):
        store = DocAuditQuery()
        ev = store.add_event("a", "x", "r", metadata={"ip": "1.2.3.4"}, now=1.0)
        assert ev.metadata == {"ip": "1.2.3.4"}

    def test_add_event_ids_increment(self):
        store = DocAuditQuery()
        e1 = store.add_event("a", "x", "r", now=1.0)
        e2 = store.add_event("b", "y", "r", now=2.0)
        assert e1.event_id == 1
        assert e2.event_id == 2

    def test_add_event_failure_outcome(self):
        store = DocAuditQuery()
        ev = store.add_event("a", "x", "r", outcome="failure", now=1.0)
        assert ev.outcome == "failure"


class TestAddEvents:
    def test_add_events_count(self):
        store = DocAuditQuery()
        evs = [
            AuditEvent(event_id=10, timestamp=1.0, actor="a", action="x", resource="r"),
            AuditEvent(event_id=11, timestamp=2.0, actor="b", action="y", resource="r"),
        ]
        added = store.add_events(evs)
        assert added == 2
        assert store.total_events == 2

    def test_add_events_id_bump(self):
        store = DocAuditQuery()
        evs = [
            AuditEvent(event_id=50, timestamp=1.0, actor="a", action="x", resource="r")
        ]
        store.add_events(evs)
        new_ev = store.add_event("z", "k", "r", now=5.0)
        assert new_ev.event_id == 51


# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------


def _populate(store: DocAuditQuery) -> None:
    store.add_event("alice", "read", "doc1", now=100.0)
    store.add_event("alice", "write", "doc2", now=200.0)
    store.add_event("bob", "read", "doc1", now=300.0)
    store.add_event("bob", "delete", "doc3", outcome="failure", now=400.0)
    store.add_event("carol", "read", "doc2", now=500.0)


class TestQueryBasic:
    def test_query_none_match_all(self):
        store = DocAuditQuery()
        _populate(store)
        assert len(store.query(Query())) == 5

    def test_query_empty_store(self):
        store = DocAuditQuery()
        assert store.query(Query()) == []


class TestQueryActors:
    def test_single_actor(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(actors=["alice"]))
        assert len(result) == 2

    def test_multiple_actors(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(actors=["alice", "bob"]))
        assert len(result) == 4

    def test_unknown_actor(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.query(Query(actors=["nobody"])) == []


class TestQueryActions:
    def test_read_only(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(actions=["read"]))
        assert len(result) == 3

    def test_multiple_actions(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(actions=["write", "delete"]))
        assert len(result) == 2


class TestQueryResources:
    def test_single_resource(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(resources=["doc1"]))
        assert len(result) == 2

    def test_unknown_resource(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.query(Query(resources=["docX"])) == []


class TestQueryOutcomes:
    def test_failure(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(outcomes=["failure"]))
        assert len(result) == 1

    def test_success(self):
        store = DocAuditQuery()
        _populate(store)
        assert len(store.query(Query(outcomes=["success"]))) == 4


class TestQueryTimeRange:
    def test_start_inclusive(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(start=300.0))
        assert len(result) == 3

    def test_end_inclusive(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(end=200.0))
        assert len(result) == 2

    def test_range(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(start=200.0, end=400.0))
        assert len(result) == 3


class TestQueryTextContains:
    def test_text_actor(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(text_contains="ali"))
        assert len(result) == 2

    def test_text_action(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(text_contains="delete"))
        assert len(result) == 1

    def test_text_resource(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(text_contains="doc1"))
        assert len(result) == 2

    def test_text_outcome(self):
        store = DocAuditQuery()
        _populate(store)
        result = store.query(Query(text_contains="failure"))
        assert len(result) == 1

    def test_text_no_match(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.query(Query(text_contains="zzzz")) == []


# ---------------------------------------------------------------------------
# Count, distinct
# ---------------------------------------------------------------------------


class TestCount:
    def test_count_all(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.count() == 5

    def test_count_with_query(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.count(Query(actors=["alice"])) == 2

    def test_count_empty(self):
        store = DocAuditQuery()
        assert store.count() == 0


class TestDistinct:
    def test_distinct_actors(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.distinct(Query(), "actor") == {"alice", "bob", "carol"}

    def test_distinct_actions(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.distinct(Query(), "action") == {"read", "write", "delete"}

    def test_distinct_unknown_field(self):
        store = DocAuditQuery()
        _populate(store)
        with pytest.raises(ValueError):
            store.distinct(Query(), "nope")


# ---------------------------------------------------------------------------
# Aggregate
# ---------------------------------------------------------------------------


class TestAggregateCount:
    def test_count(self):
        store = DocAuditQuery()
        _populate(store)
        r = store.aggregate(Query(), AggregateType.COUNT)
        assert r.value == 5

    def test_count_distinct(self):
        store = DocAuditQuery()
        _populate(store)
        r = store.aggregate(Query(), AggregateType.COUNT_DISTINCT, field="actor")
        assert r.value == 3

    def test_count_distinct_requires_field(self):
        store = DocAuditQuery()
        _populate(store)
        with pytest.raises(ValueError):
            store.aggregate(Query(), AggregateType.COUNT_DISTINCT)


class TestAggregateMinMaxTime:
    def test_min_time(self):
        store = DocAuditQuery()
        _populate(store)
        r = store.aggregate(Query(), AggregateType.MIN_TIME)
        assert r.value == 100.0

    def test_max_time(self):
        store = DocAuditQuery()
        _populate(store)
        r = store.aggregate(Query(), AggregateType.MAX_TIME)
        assert r.value == 500.0

    def test_min_time_empty(self):
        store = DocAuditQuery()
        r = store.aggregate(Query(), AggregateType.MIN_TIME)
        assert r.value is None


class TestAggregateFirstLast:
    def test_first(self):
        store = DocAuditQuery()
        _populate(store)
        r = store.aggregate(Query(), AggregateType.FIRST)
        assert isinstance(r.value, AuditEvent)
        assert r.value.timestamp == 100.0

    def test_last(self):
        store = DocAuditQuery()
        _populate(store)
        r = store.aggregate(Query(), AggregateType.LAST)
        assert r.value.timestamp == 500.0

    def test_first_empty(self):
        store = DocAuditQuery()
        r = store.aggregate(Query(), AggregateType.FIRST)
        assert r.value is None


# ---------------------------------------------------------------------------
# Grouping
# ---------------------------------------------------------------------------


class TestGroupByTime:
    def test_group_by_minute(self):
        store = DocAuditQuery()
        store.add_event("a", "x", "r", now=10.0)
        store.add_event("b", "x", "r", now=20.0)
        store.add_event("c", "x", "r", now=70.0)
        buckets = store.group_by_time(Query(), TimeBucket.MINUTE)
        # bucket 0-60 and 60-120
        assert len(buckets) == 2
        assert len(buckets[0].events) == 2
        assert len(buckets[1].events) == 1

    def test_group_by_hour(self):
        store = DocAuditQuery()
        store.add_event("a", "x", "r", now=100.0)
        store.add_event("b", "x", "r", now=3700.0)
        buckets = store.group_by_time(Query(), TimeBucket.HOUR)
        assert len(buckets) == 2
        assert buckets[0].start == 0.0
        assert buckets[0].end == 3600.0
        assert buckets[1].start == 3600.0

    def test_group_empty(self):
        store = DocAuditQuery()
        buckets = store.group_by_time(Query(), TimeBucket.MINUTE)
        assert buckets == []

    def test_group_includes_empty_buckets(self):
        store = DocAuditQuery()
        store.add_event("a", "x", "r", now=10.0)
        store.add_event("b", "x", "r", now=130.0)
        buckets = store.group_by_time(Query(), TimeBucket.MINUTE)
        # 0-60, 60-120, 120-180 → middle one is empty
        assert len(buckets) == 3
        assert buckets[1].events == []


class TestGroupByField:
    def test_group_by_actor(self):
        store = DocAuditQuery()
        _populate(store)
        grouped = store.group_by_field(Query(), "actor")
        assert set(grouped.keys()) == {"alice", "bob", "carol"}
        assert len(grouped["alice"]) == 2

    def test_group_by_action(self):
        store = DocAuditQuery()
        _populate(store)
        grouped = store.group_by_field(Query(), "action")
        assert len(grouped["read"]) == 3

    def test_group_by_unknown_field(self):
        store = DocAuditQuery()
        _populate(store)
        with pytest.raises(ValueError):
            store.group_by_field(Query(), "what")


# ---------------------------------------------------------------------------
# Top-N
# ---------------------------------------------------------------------------


class TestTopActors:
    def test_top_actors(self):
        store = DocAuditQuery()
        _populate(store)
        top = store.top_actors(n=2)
        assert top[0][0] in {"alice", "bob"}
        assert top[0][1] == 2

    def test_top_actors_filtered(self):
        store = DocAuditQuery()
        _populate(store)
        top = store.top_actors(q=Query(actions=["read"]))
        names = {a for a, _ in top}
        assert "alice" in names and "bob" in names and "carol" in names


class TestTopActions:
    def test_top_actions(self):
        store = DocAuditQuery()
        _populate(store)
        top = store.top_actions(n=1)
        assert top[0] == ("read", 3)

    def test_top_actions_empty(self):
        store = DocAuditQuery()
        assert store.top_actions() == []


class TestTopResources:
    def test_top_resources(self):
        store = DocAuditQuery()
        _populate(store)
        top = store.top_resources()
        as_dict = dict(top)
        assert as_dict["doc1"] == 2
        assert as_dict["doc2"] == 2
        assert as_dict["doc3"] == 1

    def test_top_resources_limit(self):
        store = DocAuditQuery()
        _populate(store)
        assert len(store.top_resources(n=1)) == 1


# ---------------------------------------------------------------------------
# Rates and counts
# ---------------------------------------------------------------------------


class TestFailureRate:
    def test_failure_rate(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.failure_rate() == pytest.approx(0.2)

    def test_failure_rate_empty(self):
        store = DocAuditQuery()
        assert store.failure_rate() == 0.0

    def test_failure_rate_all_success(self):
        store = DocAuditQuery()
        store.add_event("a", "x", "r", now=1.0)
        store.add_event("b", "y", "r", now=2.0)
        assert store.failure_rate() == 0.0


class TestUniqueActorsCount:
    def test_unique(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.unique_actors_count() == 3

    def test_unique_filtered(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.unique_actors_count(Query(actions=["read"])) == 3

    def test_unique_empty(self):
        store = DocAuditQuery()
        assert store.unique_actors_count() == 0


class TestRecent:
    def test_recent_order(self):
        store = DocAuditQuery()
        _populate(store)
        recent = store.recent(n=3)
        assert recent[0].timestamp == 500.0
        assert recent[1].timestamp == 400.0
        assert recent[2].timestamp == 300.0

    def test_recent_default(self):
        store = DocAuditQuery()
        _populate(store)
        assert len(store.recent()) == 5

    def test_recent_empty(self):
        store = DocAuditQuery()
        assert store.recent() == []


class TestClear:
    def test_clear(self):
        store = DocAuditQuery()
        _populate(store)
        store.clear()
        assert store.total_events == 0
        assert store.count() == 0

    def test_clear_resets_ids(self):
        store = DocAuditQuery()
        _populate(store)
        store.clear()
        ev = store.add_event("a", "x", "r", now=1.0)
        assert ev.event_id == 1


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_total_events_property(self):
        store = DocAuditQuery()
        assert store.total_events == 0
        store.add_event("a", "x", "r", now=1.0)
        assert store.total_events == 1

    def test_combined_filters(self):
        store = DocAuditQuery()
        _populate(store)
        q = Query(actors=["bob"], actions=["delete"], outcomes=["failure"])
        result = store.query(q)
        assert len(result) == 1

    def test_query_with_no_match_combined(self):
        store = DocAuditQuery()
        _populate(store)
        q = Query(actors=["alice"], actions=["delete"])
        assert store.query(q) == []

    def test_distinct_resource(self):
        store = DocAuditQuery()
        _populate(store)
        assert store.distinct(Query(), "resource") == {"doc1", "doc2", "doc3"}

    def test_aggregate_count_filtered(self):
        store = DocAuditQuery()
        _populate(store)
        r = store.aggregate(Query(actors=["alice"]), AggregateType.COUNT)
        assert r.value == 2

    def test_group_by_time_day(self):
        store = DocAuditQuery()
        # 86400 = 1 day
        store.add_event("a", "x", "r", now=100.0)
        store.add_event("b", "x", "r", now=90000.0)
        buckets = store.group_by_time(Query(), TimeBucket.DAY)
        assert len(buckets) == 2

    def test_metadata_isolation(self):
        store = DocAuditQuery()
        md = {"k": "v"}
        ev = store.add_event("a", "x", "r", metadata=md, now=1.0)
        md["k"] = "changed"
        assert ev.metadata["k"] == "v"
