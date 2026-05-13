"""Tests for docstoolkit.event_sourcing (E47).

Covers:
- DomainEvent: construction, auto-fields, to_dict / from_dict round-trip
- EventStore:  append, get_events ordering, version conflict, latest_version,
               get_all_events (with/without filter), aggregate_ids, snapshot_count
- EventSourcedAggregate: append_event version increment, rebuild_state,
                         current_state, event_count, partial replay,
                         metadata propagation
"""
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.event_sourcing import (
    DomainEvent,
    EventStore,
    VersionConflictError,
    AggregateState,
    EventApplier,
    EventSourcedAggregate,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_event(**kwargs) -> DomainEvent:
    defaults = dict(
        event_type="test.happened",
        aggregate_id="agg-1",
        aggregate_type="TestAggregate",
        payload={"key": "value"},
    )
    defaults.update(kwargs)
    return DomainEvent(**defaults)


class SimpleApplier(EventApplier):
    """Accumulates 'delta' from each event payload into state['total']."""

    def apply(self, state: AggregateState, event: DomainEvent) -> AggregateState:
        state.state["total"] = state.state.get("total", 0) + event.payload.get("delta", 0)
        state.state["last_type"] = event.event_type
        return state


class ListApplier(EventApplier):
    """Appends event_type names to state['events'] list."""

    def apply(self, state: AggregateState, event: DomainEvent) -> AggregateState:
        state.state.setdefault("events", []).append(event.event_type)
        return state


@pytest.fixture()
def store() -> EventStore:
    return EventStore()


@pytest.fixture()
def agg(store: EventStore) -> EventSourcedAggregate:
    return EventSourcedAggregate("agg-1", "Order", SimpleApplier(), store)


# ===========================================================================
# DomainEvent
# ===========================================================================

class TestDomainEventAutoFields:
    def test_event_id_auto_generated(self):
        e = make_event()
        assert e.event_id
        assert len(e.event_id) == 8

    def test_event_ids_are_unique(self):
        ids = {make_event().event_id for _ in range(50)}
        assert len(ids) == 50

    def test_ts_auto_generated(self):
        before = time.time()
        e = make_event()
        after = time.time()
        assert before <= e.ts <= after

    def test_version_default_is_1(self):
        e = make_event()
        assert e.version == 1

    def test_metadata_default_is_empty_dict(self):
        e = make_event()
        assert e.metadata == {}

    def test_metadata_not_shared_between_instances(self):
        e1 = make_event()
        e2 = make_event()
        e1.metadata["x"] = 1
        assert "x" not in e2.metadata


class TestDomainEventFields:
    def test_event_type_stored(self):
        e = make_event(event_type="user.created")
        assert e.event_type == "user.created"

    def test_aggregate_id_stored(self):
        e = make_event(aggregate_id="user-42")
        assert e.aggregate_id == "user-42"

    def test_aggregate_type_stored(self):
        e = make_event(aggregate_type="User")
        assert e.aggregate_type == "User"

    def test_payload_stored(self):
        e = make_event(payload={"name": "Alice", "age": 30})
        assert e.payload == {"name": "Alice", "age": 30}

    def test_explicit_event_id(self):
        e = make_event(event_id="abc12345")
        assert e.event_id == "abc12345"

    def test_explicit_version(self):
        e = make_event(version=7)
        assert e.version == 7

    def test_explicit_metadata(self):
        e = make_event(metadata={"correlation_id": "xyz"})
        assert e.metadata["correlation_id"] == "xyz"


class TestDomainEventToDict:
    def test_to_dict_keys(self):
        e = make_event()
        d = e.to_dict()
        expected_keys = {
            "event_id", "event_type", "aggregate_id", "aggregate_type",
            "payload", "ts", "version", "metadata",
        }
        assert set(d.keys()) == expected_keys

    def test_to_dict_values(self):
        e = make_event(event_type="order.placed", aggregate_id="o-1",
                       aggregate_type="Order", payload={"amount": 99})
        d = e.to_dict()
        assert d["event_type"] == "order.placed"
        assert d["aggregate_id"] == "o-1"
        assert d["aggregate_type"] == "Order"
        assert d["payload"] == {"amount": 99}
        assert d["version"] == 1

    def test_to_dict_ts_is_float(self):
        e = make_event()
        assert isinstance(e.to_dict()["ts"], float)

    def test_to_dict_metadata_included(self):
        e = make_event(metadata={"user": "bob"})
        assert e.to_dict()["metadata"] == {"user": "bob"}


class TestDomainEventFromDict:
    def test_round_trip(self):
        original = make_event(
            event_type="item.added",
            aggregate_id="cart-9",
            aggregate_type="Cart",
            payload={"sku": "ABC", "qty": 3},
            version=4,
            metadata={"source": "web"},
        )
        reconstructed = DomainEvent.from_dict(original.to_dict())
        assert reconstructed.event_id == original.event_id
        assert reconstructed.event_type == original.event_type
        assert reconstructed.aggregate_id == original.aggregate_id
        assert reconstructed.aggregate_type == original.aggregate_type
        assert reconstructed.payload == original.payload
        assert reconstructed.ts == original.ts
        assert reconstructed.version == original.version
        assert reconstructed.metadata == original.metadata

    def test_from_dict_missing_metadata_defaults_to_empty(self):
        d = make_event().to_dict()
        del d["metadata"]
        e = DomainEvent.from_dict(d)
        assert e.metadata == {}

    def test_from_dict_preserves_type(self):
        d = make_event().to_dict()
        e = DomainEvent.from_dict(d)
        assert isinstance(e, DomainEvent)


# ===========================================================================
# EventStore
# ===========================================================================

class TestEventStoreAppend:
    def test_append_single_event(self, store):
        e = make_event(version=1)
        store.append(e)
        assert store.snapshot_count() == 1

    def test_append_multiple_events(self, store):
        for i in range(1, 6):
            store.append(make_event(version=i, event_id=f"id-{i:04d}"))
        assert store.snapshot_count() == 5

    def test_append_version_conflict_raises(self, store):
        e1 = make_event(version=1, event_id="aa000001")
        e2 = make_event(version=1, event_id="bb000002")  # same aggregate + version
        store.append(e1)
        with pytest.raises(VersionConflictError):
            store.append(e2)

    def test_append_same_version_different_aggregates_ok(self, store):
        e1 = make_event(aggregate_id="agg-A", version=1, event_id="aaaa0001")
        e2 = make_event(aggregate_id="agg-B", version=1, event_id="bbbb0001")
        store.append(e1)
        store.append(e2)  # no conflict
        assert store.snapshot_count() == 2

    def test_version_conflict_error_message(self, store):
        store.append(make_event(version=1, event_id="cc000001"))
        with pytest.raises(VersionConflictError, match="agg-1"):
            store.append(make_event(version=1, event_id="dd000002"))


class TestEventStoreGetEvents:
    def _seed(self, store, n=5, agg_id="agg-1"):
        for i in range(1, n + 1):
            store.append(make_event(aggregate_id=agg_id, version=i,
                                    event_id=f"{agg_id}-{i:04d}"))

    def test_get_events_returns_correct_count(self, store):
        self._seed(store, 3)
        assert len(store.get_events("agg-1")) == 3

    def test_get_events_ordered_by_version(self, store):
        self._seed(store, 4)
        events = store.get_events("agg-1")
        versions = [e.version for e in events]
        assert versions == sorted(versions)

    def test_get_events_from_version(self, store):
        self._seed(store, 5)
        events = store.get_events("agg-1", from_version=3)
        assert all(e.version >= 3 for e in events)
        assert len(events) == 3

    def test_get_events_unknown_aggregate_returns_empty(self, store):
        assert store.get_events("nonexistent") == []

    def test_get_events_isolates_aggregate(self, store):
        self._seed(store, 3, "agg-A")
        self._seed(store, 2, "agg-B")
        assert len(store.get_events("agg-A")) == 3
        assert len(store.get_events("agg-B")) == 2

    def test_get_events_returns_domain_event_instances(self, store):
        self._seed(store, 1)
        events = store.get_events("agg-1")
        assert isinstance(events[0], DomainEvent)

    def test_get_events_payload_preserved(self, store):
        e = make_event(version=1, payload={"amount": 42})
        store.append(e)
        loaded = store.get_events("agg-1")[0]
        assert loaded.payload == {"amount": 42}

    def test_get_events_metadata_preserved(self, store):
        e = make_event(version=1, metadata={"correlation_id": "corr-99"})
        store.append(e)
        loaded = store.get_events("agg-1")[0]
        assert loaded.metadata["correlation_id"] == "corr-99"


class TestEventStoreGetAllEvents:
    def test_get_all_events_returns_all(self, store):
        store.append(make_event(aggregate_id="a1", version=1, event_id="e0001"))
        store.append(make_event(aggregate_id="a2", version=1, event_id="e0002"))
        assert len(store.get_all_events()) == 2

    def test_get_all_events_ordered_by_ts(self, store):
        for i in range(1, 4):
            e = make_event(aggregate_id="a1", version=i,
                           event_id=f"ts-{i:04d}", ts=float(i))
            store.append(e)
        events = store.get_all_events()
        ts_list = [e.ts for e in events]
        assert ts_list == sorted(ts_list)

    def test_get_all_events_type_filter(self, store):
        store.append(make_event(event_type="alpha", version=1, event_id="al0001"))
        store.append(make_event(event_type="beta",  version=2, event_id="be0001"))
        store.append(make_event(event_type="alpha", version=3, event_id="al0002"))
        result = store.get_all_events(event_type="alpha")
        assert len(result) == 2
        assert all(e.event_type == "alpha" for e in result)

    def test_get_all_events_type_filter_no_match(self, store):
        store.append(make_event(event_type="alpha", version=1, event_id="al0001"))
        assert store.get_all_events(event_type="gamma") == []

    def test_get_all_events_empty_store(self, store):
        assert store.get_all_events() == []


class TestEventStoreLatestVersion:
    def test_latest_version_zero_for_unknown(self, store):
        assert store.latest_version("nonexistent") == 0

    def test_latest_version_single_event(self, store):
        store.append(make_event(version=1))
        assert store.latest_version("agg-1") == 1

    def test_latest_version_multiple_events(self, store):
        for i in range(1, 6):
            store.append(make_event(version=i, event_id=f"lv-{i:04d}"))
        assert store.latest_version("agg-1") == 5

    def test_latest_version_independent_per_aggregate(self, store):
        store.append(make_event(aggregate_id="a", version=1, event_id="a0001"))
        store.append(make_event(aggregate_id="a", version=2, event_id="a0002"))
        store.append(make_event(aggregate_id="b", version=1, event_id="b0001"))
        assert store.latest_version("a") == 2
        assert store.latest_version("b") == 1


class TestEventStoreAggregateIds:
    def test_aggregate_ids_empty_store(self, store):
        assert store.aggregate_ids() == []

    def test_aggregate_ids_single(self, store):
        store.append(make_event(version=1))
        ids = store.aggregate_ids()
        assert "agg-1" in ids

    def test_aggregate_ids_multiple(self, store):
        for agg_id in ["alpha", "beta", "gamma"]:
            store.append(make_event(aggregate_id=agg_id, version=1,
                                    event_id=f"{agg_id[:2]}-0001"))
        ids = store.aggregate_ids()
        assert set(ids) == {"alpha", "beta", "gamma"}

    def test_aggregate_ids_no_duplicates(self, store):
        for i in range(1, 4):
            store.append(make_event(aggregate_id="agg-1", version=i,
                                    event_id=f"nd-{i:04d}"))
        assert store.aggregate_ids().count("agg-1") == 1


class TestEventStoreSnapshotCount:
    def test_snapshot_count_zero(self, store):
        assert store.snapshot_count() == 0

    def test_snapshot_count_increments(self, store):
        for i in range(1, 4):
            store.append(make_event(version=i, event_id=f"sc-{i:04d}"))
        assert store.snapshot_count() == 3


# ===========================================================================
# AggregateState
# ===========================================================================

class TestAggregateState:
    def test_default_version_is_zero(self):
        s = AggregateState("id", "Type")
        assert s.version == 0

    def test_default_state_is_empty_dict(self):
        s = AggregateState("id", "Type")
        assert s.state == {}

    def test_state_not_shared_between_instances(self):
        s1 = AggregateState("id1", "T")
        s2 = AggregateState("id2", "T")
        s1.state["x"] = 1
        assert "x" not in s2.state


# ===========================================================================
# EventSourcedAggregate
# ===========================================================================

class TestEventSourcedAggregateAppend:
    def test_append_returns_domain_event(self, agg):
        e = agg.append_event("order.placed", {"amount": 10})
        assert isinstance(e, DomainEvent)

    def test_first_event_has_version_1(self, agg):
        e = agg.append_event("order.placed", {"amount": 10})
        assert e.version == 1

    def test_version_increments(self, agg):
        e1 = agg.append_event("order.placed",  {"amount": 10})
        e2 = agg.append_event("order.updated", {"amount": 20})
        e3 = agg.append_event("order.shipped", {})
        assert e1.version == 1
        assert e2.version == 2
        assert e3.version == 3

    def test_event_stored_in_store(self, agg, store):
        agg.append_event("order.placed", {"amount": 5})
        assert store.latest_version("agg-1") == 1

    def test_aggregate_id_set_on_event(self, agg):
        e = agg.append_event("x", {})
        assert e.aggregate_id == "agg-1"

    def test_aggregate_type_set_on_event(self, agg):
        e = agg.append_event("x", {})
        assert e.aggregate_type == "Order"

    def test_metadata_stored(self, agg):
        e = agg.append_event("x", {}, metadata={"user": "alice"})
        assert e.metadata["user"] == "alice"

    def test_metadata_defaults_to_empty(self, agg):
        e = agg.append_event("x", {})
        assert e.metadata == {}


class TestEventSourcedAggregateRebuildState:
    def test_rebuild_empty_aggregate(self, store):
        agg = EventSourcedAggregate("empty", "T", SimpleApplier(), store)
        state = agg.rebuild_state()
        assert state.version == 0
        assert state.state == {}

    def test_rebuild_single_event(self, agg):
        agg.append_event("order.placed", {"delta": 10})
        state = agg.rebuild_state()
        assert state.state["total"] == 10
        assert state.version == 1

    def test_rebuild_multiple_events(self, agg):
        agg.append_event("order.placed",  {"delta": 10})
        agg.append_event("item.added",    {"delta": 5})
        agg.append_event("discount.applied", {"delta": -3})
        state = agg.rebuild_state()
        assert state.state["total"] == 12
        assert state.version == 3

    def test_rebuild_from_version_partial(self, agg):
        agg.append_event("order.placed",  {"delta": 100})  # version 1, ignored
        agg.append_event("item.added",    {"delta": 20})   # version 2
        agg.append_event("item.added",    {"delta": 5})    # version 3
        state = agg.rebuild_state(from_version=2)
        # Only events at version >= 2 are replayed
        assert state.state["total"] == 25
        assert state.version == 3

    def test_rebuild_state_has_correct_aggregate_id(self, agg):
        agg.append_event("x", {})
        state = agg.rebuild_state()
        assert state.aggregate_id == "agg-1"

    def test_rebuild_state_has_correct_aggregate_type(self, agg):
        agg.append_event("x", {})
        state = agg.rebuild_state()
        assert state.aggregate_type == "Order"

    def test_rebuild_last_type_tracked(self, agg):
        agg.append_event("order.placed",  {"delta": 1})
        agg.append_event("order.shipped", {"delta": 0})
        state = agg.rebuild_state()
        assert state.state["last_type"] == "order.shipped"


class TestEventSourcedAggregateCurrentState:
    def test_current_state_empty(self, store):
        agg = EventSourcedAggregate("fresh", "T", SimpleApplier(), store)
        assert agg.current_state().version == 0

    def test_current_state_equals_full_rebuild(self, agg):
        agg.append_event("a", {"delta": 1})
        agg.append_event("b", {"delta": 2})
        s1 = agg.current_state()
        s2 = agg.rebuild_state(from_version=1)
        assert s1.version == s2.version
        assert s1.state == s2.state

    def test_current_state_version_matches_latest(self, agg, store):
        agg.append_event("a", {"delta": 0})
        agg.append_event("b", {"delta": 0})
        agg.append_event("c", {"delta": 0})
        assert agg.current_state().version == store.latest_version("agg-1")


class TestEventSourcedAggregateEventCount:
    def test_event_count_zero_for_new_aggregate(self, store):
        agg = EventSourcedAggregate("brand-new", "T", SimpleApplier(), store)
        assert agg.event_count() == 0

    def test_event_count_increments(self, agg):
        assert agg.event_count() == 0
        agg.append_event("a", {})
        assert agg.event_count() == 1
        agg.append_event("b", {})
        assert agg.event_count() == 2

    def test_event_count_independent_per_aggregate(self, store):
        a1 = EventSourcedAggregate("id-A", "T", SimpleApplier(), store)
        a2 = EventSourcedAggregate("id-B", "T", SimpleApplier(), store)
        a1.append_event("x", {})
        a1.append_event("y", {})
        a2.append_event("z", {})
        assert a1.event_count() == 2
        assert a2.event_count() == 1


class TestEventSourcedAggregateDefaultStore:
    def test_default_store_is_created(self):
        agg = EventSourcedAggregate("x", "T", SimpleApplier())
        agg.append_event("a", {"delta": 7})
        assert agg.current_state().state["total"] == 7

    def test_two_aggregates_share_store(self, store):
        a1 = EventSourcedAggregate("s1", "T", ListApplier(), store)
        a2 = EventSourcedAggregate("s2", "T", ListApplier(), store)
        a1.append_event("ping", {})
        a2.append_event("pong", {})
        assert store.snapshot_count() == 2

    def test_list_applier_accumulates(self, store):
        agg = EventSourcedAggregate("list-agg", "Demo", ListApplier(), store)
        agg.append_event("created", {})
        agg.append_event("updated", {})
        agg.append_event("deleted", {})
        state = agg.current_state()
        assert state.state["events"] == ["created", "updated", "deleted"]
