"""Tests for docstoolkit.event_sourcing (E84).

Covers:
- Event: dataclass fields and defaults (id, timestamp, version, payload)
- EventEnvelope: dataclass fields (event, sequence)
- EventStore: append (sequence return, increments, JSON roundtrip),
              append_many (batch transactional),
              get_events (aggregate filter, from_version, to_version, ordering),
              get_by_type (filter, limit), get_all (from_sequence, limit),
              latest_version, count, close
- Projection: apply (generic), apply_typed (specific event type),
              typed-before-generic dispatch order, state accumulation
- ReplayEngine: replay_aggregate, replay_all
"""
import os
import tempfile
import time

import pytest

from docstoolkit.event_sourcing import (
    Event,
    EventEnvelope,
    EventStore,
    Projection,
    ReplayEngine,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_event(
    aggregate_id: str = "agg-1",
    event_type: str = "test.happened",
    payload: dict | None = None,
    version: int = 1,
) -> Event:
    return Event(
        aggregate_id=aggregate_id,
        event_type=event_type,
        payload=dict(payload) if payload is not None else {"key": "value"},
        version=version,
    )


@pytest.fixture()
def store() -> EventStore:
    s = EventStore()
    yield s
    s.close()


@pytest.fixture()
def populated_store() -> EventStore:
    """Store with a few events across two aggregates."""
    s = EventStore()
    s.append(make_event("a1", "created",  {"n": 1}, version=1))
    s.append(make_event("a1", "updated",  {"n": 2}, version=2))
    s.append(make_event("a2", "created",  {"n": 10}, version=1))
    s.append(make_event("a1", "deleted",  {"n": 3}, version=3))
    s.append(make_event("a2", "updated",  {"n": 20}, version=2))
    yield s
    s.close()


# ===========================================================================
# Event dataclass
# ===========================================================================

class TestEventFields:
    def test_aggregate_id_set(self):
        e = Event(aggregate_id="x", event_type="t")
        assert e.aggregate_id == "x"

    def test_event_type_set(self):
        e = Event(aggregate_id="x", event_type="user.created")
        assert e.event_type == "user.created"

    def test_event_id_auto_generated(self):
        e = Event(aggregate_id="x", event_type="t")
        assert isinstance(e.event_id, str)
        assert len(e.event_id) == 12

    def test_event_id_hex_chars(self):
        e = Event(aggregate_id="x", event_type="t")
        assert all(c in "0123456789abcdef" for c in e.event_id)

    def test_event_ids_unique(self):
        ids = {Event(aggregate_id="x", event_type="t").event_id for _ in range(100)}
        assert len(ids) == 100

    def test_payload_default_empty_dict(self):
        e = Event(aggregate_id="x", event_type="t")
        assert e.payload == {}

    def test_payload_independent_between_instances(self):
        a = Event(aggregate_id="x", event_type="t")
        b = Event(aggregate_id="x", event_type="t")
        a.payload["k"] = "v"
        assert "k" not in b.payload

    def test_payload_custom_value(self):
        e = Event(aggregate_id="x", event_type="t", payload={"a": 1, "b": [2, 3]})
        assert e.payload == {"a": 1, "b": [2, 3]}

    def test_version_default_is_1(self):
        e = Event(aggregate_id="x", event_type="t")
        assert e.version == 1

    def test_version_custom(self):
        e = Event(aggregate_id="x", event_type="t", version=42)
        assert e.version == 42

    def test_timestamp_auto_generated(self):
        before = time.time()
        e = Event(aggregate_id="x", event_type="t")
        after = time.time()
        assert before <= e.timestamp <= after

    def test_timestamp_is_float(self):
        e = Event(aggregate_id="x", event_type="t")
        assert isinstance(e.timestamp, float)

    def test_timestamp_custom(self):
        e = Event(aggregate_id="x", event_type="t", timestamp=1_700_000_000.0)
        assert e.timestamp == 1_700_000_000.0

    def test_event_id_custom_override(self):
        e = Event(aggregate_id="x", event_type="t", event_id="abc123")
        assert e.event_id == "abc123"

    def test_all_fields_set_together(self):
        e = Event(
            aggregate_id="agg",
            event_type="x.y",
            event_id="myid12345678",
            payload={"k": 1},
            version=7,
            timestamp=100.5,
        )
        assert e.aggregate_id == "agg"
        assert e.event_type == "x.y"
        assert e.event_id == "myid12345678"
        assert e.payload == {"k": 1}
        assert e.version == 7
        assert e.timestamp == 100.5


# ===========================================================================
# EventEnvelope dataclass
# ===========================================================================

class TestEventEnvelopeFields:
    def test_event_field(self):
        e = make_event()
        env = EventEnvelope(event=e, sequence=1)
        assert env.event is e

    def test_sequence_field(self):
        env = EventEnvelope(event=make_event(), sequence=42)
        assert env.sequence == 42

    def test_envelope_sequence_is_int(self):
        env = EventEnvelope(event=make_event(), sequence=100)
        assert isinstance(env.sequence, int)

    def test_envelope_accepts_zero_sequence(self):
        env = EventEnvelope(event=make_event(), sequence=0)
        assert env.sequence == 0


# ===========================================================================
# EventStore.append
# ===========================================================================

class TestEventStoreAppend:
    def test_append_returns_sequence(self, store):
        seq = store.append(make_event())
        assert isinstance(seq, int)
        assert seq >= 1

    def test_first_sequence_is_1(self, store):
        seq = store.append(make_event())
        assert seq == 1

    def test_sequence_increments(self, store):
        s1 = store.append(make_event())
        s2 = store.append(make_event())
        s3 = store.append(make_event())
        assert s1 == 1
        assert s2 == 2
        assert s3 == 3

    def test_append_persists_event_id(self, store):
        e = make_event()
        store.append(e)
        envs = store.get_events(e.aggregate_id)
        assert envs[0].event.event_id == e.event_id

    def test_append_persists_aggregate_id(self, store):
        e = make_event(aggregate_id="custom-agg")
        store.append(e)
        envs = store.get_events("custom-agg")
        assert envs[0].event.aggregate_id == "custom-agg"

    def test_append_persists_event_type(self, store):
        e = make_event(event_type="order.placed")
        store.append(e)
        envs = store.get_events(e.aggregate_id)
        assert envs[0].event.event_type == "order.placed"

    def test_append_payload_json_roundtrip(self, store):
        payload = {"a": 1, "b": "hello", "nested": {"x": [1, 2, 3]}}
        e = make_event(payload=payload)
        store.append(e)
        envs = store.get_events(e.aggregate_id)
        assert envs[0].event.payload == payload

    def test_append_payload_unicode_roundtrip(self, store):
        payload = {"name": "Лоренцо", "emoji": "test"}
        e = make_event(payload=payload)
        store.append(e)
        envs = store.get_events(e.aggregate_id)
        assert envs[0].event.payload == payload

    def test_append_persists_version(self, store):
        e = make_event(version=5)
        store.append(e)
        envs = store.get_events(e.aggregate_id)
        assert envs[0].event.version == 5

    def test_append_persists_timestamp(self, store):
        e = make_event()
        e.timestamp = 1234567.89
        store.append(e)
        envs = store.get_events(e.aggregate_id)
        assert envs[0].event.timestamp == 1234567.89

    def test_append_increments_count(self, store):
        assert store.count() == 0
        store.append(make_event())
        assert store.count() == 1
        store.append(make_event())
        assert store.count() == 2

    def test_append_returns_increasing_sequences(self, store):
        sequences = [store.append(make_event()) for _ in range(10)]
        assert sequences == sorted(sequences)
        assert sequences == list(range(1, 11))

    def test_append_empty_payload(self, store):
        e = make_event(payload={})
        store.append(e)
        envs = store.get_events(e.aggregate_id)
        assert envs[0].event.payload == {}

    def test_append_payload_with_list(self, store):
        e = make_event(payload={"items": [1, 2, 3, "x"]})
        store.append(e)
        envs = store.get_events(e.aggregate_id)
        assert envs[0].event.payload == {"items": [1, 2, 3, "x"]}


# ===========================================================================
# EventStore.append_many (batch / transactional)
# ===========================================================================

class TestEventStoreAppendMany:
    def test_append_many_returns_list(self, store):
        events = [make_event(version=i + 1) for i in range(3)]
        seqs = store.append_many(events)
        assert isinstance(seqs, list)
        assert len(seqs) == 3

    def test_append_many_sequences_increment(self, store):
        events = [make_event(version=i + 1) for i in range(5)]
        seqs = store.append_many(events)
        assert seqs == [1, 2, 3, 4, 5]

    def test_append_many_after_singles(self, store):
        store.append(make_event(version=1))
        events = [make_event(version=i + 2) for i in range(3)]
        seqs = store.append_many(events)
        assert seqs == [2, 3, 4]

    def test_append_many_empty_list(self, store):
        seqs = store.append_many([])
        assert seqs == []
        assert store.count() == 0

    def test_append_many_persists_all(self, store):
        events = [make_event("ag", version=i + 1) for i in range(4)]
        store.append_many(events)
        assert store.count() == 4

    def test_append_many_atomic_on_failure(self, store):
        good = [make_event("ag", version=i + 1) for i in range(3)]
        # Duplicate event_id should violate the UNIQUE constraint mid-batch.
        bad = make_event("ag", version=4)
        bad.event_id = good[0].event_id
        events = good + [bad]
        with pytest.raises(Exception):
            store.append_many(events)
        # Nothing should have been committed.
        assert store.count() == 0

    def test_append_many_payloads_roundtrip(self, store):
        events = [
            make_event("a", "t1", {"i": 1}, version=1),
            make_event("a", "t2", {"i": 2}, version=2),
        ]
        store.append_many(events)
        envs = store.get_events("a")
        assert envs[0].event.payload == {"i": 1}
        assert envs[1].event.payload == {"i": 2}

    def test_append_many_preserves_order(self, store):
        events = [make_event("a", "t" + str(i), version=i + 1) for i in range(5)]
        store.append_many(events)
        envs = store.get_events("a")
        types = [env.event.event_type for env in envs]
        assert types == [e.event_type for e in events]


# ===========================================================================
# EventStore.get_events
# ===========================================================================

class TestEventStoreGetEvents:
    def test_returns_envelopes(self, store):
        store.append(make_event())
        envs = store.get_events("agg-1")
        assert all(isinstance(env, EventEnvelope) for env in envs)

    def test_filters_by_aggregate_id(self, populated_store):
        envs = populated_store.get_events("a1")
        for env in envs:
            assert env.event.aggregate_id == "a1"

    def test_unknown_aggregate_returns_empty(self, store):
        store.append(make_event())
        assert store.get_events("nonexistent") == []

    def test_returns_ordered_by_sequence(self, populated_store):
        envs = populated_store.get_events("a1")
        seqs = [env.sequence for env in envs]
        assert seqs == sorted(seqs)

    def test_count_matches(self, populated_store):
        # a1 has 3 events, a2 has 2
        assert len(populated_store.get_events("a1")) == 3
        assert len(populated_store.get_events("a2")) == 2

    def test_from_version_inclusive(self, populated_store):
        envs = populated_store.get_events("a1", from_version=2)
        versions = [env.event.version for env in envs]
        assert versions == [2, 3]

    def test_from_version_above_max_returns_empty(self, populated_store):
        envs = populated_store.get_events("a1", from_version=99)
        assert envs == []

    def test_from_version_zero_returns_all(self, populated_store):
        envs = populated_store.get_events("a1", from_version=0)
        assert len(envs) == 3

    def test_to_version_inclusive(self, populated_store):
        envs = populated_store.get_events("a1", to_version=2)
        versions = [env.event.version for env in envs]
        assert versions == [1, 2]

    def test_from_and_to_version(self, populated_store):
        envs = populated_store.get_events("a1", from_version=2, to_version=2)
        versions = [env.event.version for env in envs]
        assert versions == [2]

    def test_to_version_above_max_returns_all(self, populated_store):
        envs = populated_store.get_events("a1", to_version=99)
        assert len(envs) == 3

    def test_from_higher_than_to_returns_empty(self, populated_store):
        envs = populated_store.get_events("a1", from_version=3, to_version=1)
        assert envs == []

    def test_get_events_payload_intact(self, populated_store):
        envs = populated_store.get_events("a1")
        payloads = [env.event.payload for env in envs]
        assert payloads == [{"n": 1}, {"n": 2}, {"n": 3}]


# ===========================================================================
# EventStore.get_by_type
# ===========================================================================

class TestEventStoreGetByType:
    def test_returns_only_matching_type(self, populated_store):
        envs = populated_store.get_by_type("created")
        for env in envs:
            assert env.event.event_type == "created"

    def test_returns_envelopes(self, populated_store):
        envs = populated_store.get_by_type("created")
        assert all(isinstance(env, EventEnvelope) for env in envs)

    def test_unknown_type_returns_empty(self, populated_store):
        assert populated_store.get_by_type("doesnotexist") == []

    def test_default_limit_is_100(self, store):
        for i in range(150):
            store.append(make_event(version=i + 1))
        envs = store.get_by_type("test.happened")
        assert len(envs) == 100

    def test_custom_limit(self, populated_store):
        envs = populated_store.get_by_type("created", limit=1)
        assert len(envs) == 1

    def test_limit_above_actual_count(self, populated_store):
        envs = populated_store.get_by_type("created", limit=1000)
        assert len(envs) == 2

    def test_ordered_by_sequence(self, populated_store):
        envs = populated_store.get_by_type("created")
        seqs = [env.sequence for env in envs]
        assert seqs == sorted(seqs)

    def test_count_matches(self, populated_store):
        # "created" twice, "updated" twice, "deleted" once
        assert len(populated_store.get_by_type("created")) == 2
        assert len(populated_store.get_by_type("updated")) == 2
        assert len(populated_store.get_by_type("deleted")) == 1


# ===========================================================================
# EventStore.get_all
# ===========================================================================

class TestEventStoreGetAll:
    def test_returns_envelopes(self, populated_store):
        envs = populated_store.get_all()
        assert all(isinstance(env, EventEnvelope) for env in envs)

    def test_returns_all_events(self, populated_store):
        envs = populated_store.get_all(limit=1000)
        assert len(envs) == 5

    def test_default_limit_is_100(self, store):
        for i in range(150):
            store.append(make_event(version=i + 1))
        envs = store.get_all()
        assert len(envs) == 100

    def test_ordered_by_sequence(self, populated_store):
        envs = populated_store.get_all(limit=1000)
        seqs = [env.sequence for env in envs]
        assert seqs == sorted(seqs)

    def test_from_sequence_filter(self, populated_store):
        envs = populated_store.get_all(from_sequence=3, limit=1000)
        seqs = [env.sequence for env in envs]
        assert seqs == [3, 4, 5]

    def test_from_sequence_above_max_returns_empty(self, populated_store):
        envs = populated_store.get_all(from_sequence=999)
        assert envs == []

    def test_custom_limit(self, populated_store):
        envs = populated_store.get_all(limit=2)
        assert len(envs) == 2

    def test_from_sequence_zero_returns_all(self, populated_store):
        envs = populated_store.get_all(from_sequence=0, limit=1000)
        assert len(envs) == 5

    def test_from_sequence_and_limit_combined(self, populated_store):
        envs = populated_store.get_all(from_sequence=2, limit=2)
        seqs = [env.sequence for env in envs]
        assert seqs == [2, 3]


# ===========================================================================
# EventStore.latest_version
# ===========================================================================

class TestEventStoreLatestVersion:
    def test_returns_zero_when_no_events(self, store):
        assert store.latest_version("missing") == 0

    def test_returns_zero_for_unknown_aggregate(self, populated_store):
        assert populated_store.latest_version("missing") == 0

    def test_returns_max_version(self, populated_store):
        assert populated_store.latest_version("a1") == 3

    def test_returns_max_version_other_agg(self, populated_store):
        assert populated_store.latest_version("a2") == 2

    def test_single_event_version(self, store):
        store.append(make_event(version=7))
        assert store.latest_version("agg-1") == 7

    def test_non_sequential_versions(self, store):
        store.append(make_event(aggregate_id="x", version=1))
        store.append(make_event(aggregate_id="x", version=5))
        store.append(make_event(aggregate_id="x", version=3))
        assert store.latest_version("x") == 5

    def test_does_not_count_other_aggregates(self, store):
        store.append(make_event(aggregate_id="x", version=10))
        store.append(make_event(aggregate_id="y", version=2))
        assert store.latest_version("y") == 2


# ===========================================================================
# EventStore.count
# ===========================================================================

class TestEventStoreCount:
    def test_empty_store_count_zero(self, store):
        assert store.count() == 0

    def test_count_after_inserts(self, store):
        for i in range(7):
            store.append(make_event(version=i + 1))
        assert store.count() == 7

    def test_count_after_batch(self, store):
        events = [make_event(version=i + 1) for i in range(4)]
        store.append_many(events)
        assert store.count() == 4

    def test_count_aggregates_all_aggregates(self, populated_store):
        assert populated_store.count() == 5


# ===========================================================================
# EventStore lifecycle and persistence
# ===========================================================================

class TestEventStoreLifecycle:
    def test_close_does_not_raise(self):
        s = EventStore()
        s.close()  # should not raise

    def test_default_db_path_is_memory(self):
        s = EventStore()
        assert s.db_path == ":memory:"
        s.close()

    def test_custom_db_path_persists(self, tmp_path):
        db_file = tmp_path / "events.db"
        s = EventStore(str(db_file))
        s.append(make_event())
        s.close()
        s2 = EventStore(str(db_file))
        try:
            assert s2.count() == 1
        finally:
            s2.close()

    def test_file_store_keeps_sequence_on_reopen(self, tmp_path):
        db_file = tmp_path / "events.db"
        s = EventStore(str(db_file))
        s.append(make_event())
        s.append(make_event())
        s.close()
        s2 = EventStore(str(db_file))
        try:
            seq = s2.append(make_event())
            assert seq == 3
        finally:
            s2.close()


# ===========================================================================
# Projection
# ===========================================================================

class TestProjectionBasics:
    def test_name_stored(self):
        p = Projection("my-proj")
        assert p.name == "my-proj"

    def test_initial_state_is_empty_dict(self):
        p = Projection("p")
        assert p.state == {}

    def test_state_is_a_dict(self):
        p = Projection("p")
        assert isinstance(p.state, dict)

    def test_replay_empty_events_returns_state(self):
        p = Projection("p")
        result = p.replay([])
        assert result == {}
        assert result is p.state


class TestProjectionGenericHandlers:
    def test_apply_generic_handler_runs(self):
        p = Projection("p")
        p.apply(lambda s, e: s.update({"hit": True}))
        p.replay([make_event()])
        assert p.state == {"hit": True}

    def test_apply_handler_called_per_event(self):
        p = Projection("p")
        p.apply(lambda s, e: s.update({"count": s.get("count", 0) + 1}))
        p.replay([make_event(), make_event(), make_event()])
        assert p.state["count"] == 3

    def test_apply_multiple_generic_handlers(self):
        p = Projection("p")
        p.apply(lambda s, e: s.update({"a": 1}))
        p.apply(lambda s, e: s.update({"b": 2}))
        p.replay([make_event()])
        assert p.state == {"a": 1, "b": 2}

    def test_generic_handler_receives_event(self):
        p = Projection("p")
        captured = []
        p.apply(lambda s, e: captured.append(e.event_type))
        p.replay([make_event(event_type="x.y")])
        assert captured == ["x.y"]

    def test_state_persists_between_replays(self):
        p = Projection("p")
        p.apply(lambda s, e: s.update({"n": s.get("n", 0) + 1}))
        p.replay([make_event()])
        p.replay([make_event(), make_event()])
        assert p.state["n"] == 3


class TestProjectionTypedHandlers:
    def test_typed_handler_runs_for_matching_event(self):
        p = Projection("p")
        p.apply_typed("foo", lambda s, e: s.update({"foo": True}))
        p.replay([make_event(event_type="foo")])
        assert p.state == {"foo": True}

    def test_typed_handler_skipped_for_non_matching_event(self):
        p = Projection("p")
        p.apply_typed("foo", lambda s, e: s.update({"foo": True}))
        p.replay([make_event(event_type="bar")])
        assert p.state == {}

    def test_typed_handler_invoked_only_for_its_type(self):
        p = Projection("p")
        p.apply_typed("a", lambda s, e: s.update({"a": s.get("a", 0) + 1}))
        p.apply_typed("b", lambda s, e: s.update({"b": s.get("b", 0) + 1}))
        events = [
            make_event(event_type="a"),
            make_event(event_type="b"),
            make_event(event_type="a"),
            make_event(event_type="c"),
        ]
        p.replay(events)
        assert p.state == {"a": 2, "b": 1}

    def test_multiple_typed_handlers_same_type(self):
        p = Projection("p")
        p.apply_typed("foo", lambda s, e: s.update({"x": 1}))
        p.apply_typed("foo", lambda s, e: s.update({"y": 2}))
        p.replay([make_event(event_type="foo")])
        assert p.state == {"x": 1, "y": 2}

    def test_typed_handler_payload_access(self):
        p = Projection("p")
        p.apply_typed(
            "add",
            lambda s, e: s.update({"sum": s.get("sum", 0) + e.payload.get("n", 0)}),
        )
        events = [
            make_event(event_type="add", payload={"n": 1}),
            make_event(event_type="add", payload={"n": 3}),
        ]
        p.replay(events)
        assert p.state["sum"] == 4


class TestProjectionDispatchOrder:
    def test_typed_runs_before_generic(self):
        p = Projection("p")
        order = []
        p.apply(lambda s, e: order.append("generic"))
        p.apply_typed("foo", lambda s, e: order.append("typed"))
        p.replay([make_event(event_type="foo")])
        assert order == ["typed", "generic"]

    def test_typed_runs_before_generic_with_state_dependency(self):
        # Generic sees what typed has written.
        p = Projection("p")
        p.apply_typed("foo", lambda s, e: s.update({"step": "typed"}))
        seen: list = []
        p.apply(lambda s, e: seen.append(s.get("step")))
        p.replay([make_event(event_type="foo")])
        assert seen == ["typed"]

    def test_generic_still_runs_when_typed_missing(self):
        p = Projection("p")
        p.apply(lambda s, e: s.update({"hit": True}))
        p.apply_typed("not_this", lambda s, e: s.update({"x": "y"}))
        p.replay([make_event(event_type="other")])
        assert p.state == {"hit": True}

    def test_multiple_events_dispatch_order(self):
        p = Projection("p")
        order = []
        p.apply_typed("x", lambda s, e: order.append(("typed", e.event_type)))
        p.apply(lambda s, e: order.append(("generic", e.event_type)))
        events = [
            make_event(event_type="x"),
            make_event(event_type="y"),
            make_event(event_type="x"),
        ]
        p.replay(events)
        assert order == [
            ("typed", "x"),
            ("generic", "x"),
            ("generic", "y"),
            ("typed", "x"),
            ("generic", "x"),
        ]


class TestProjectionStateAccumulation:
    def test_accumulate_payload_field(self):
        p = Projection("counter")
        p.apply_typed(
            "inc",
            lambda s, e: s.update({"total": s.get("total", 0) + e.payload["d"]}),
        )
        events = [
            make_event(event_type="inc", payload={"d": 1}),
            make_event(event_type="inc", payload={"d": 5}),
            make_event(event_type="inc", payload={"d": -2}),
        ]
        result = p.replay(events)
        assert result["total"] == 4

    def test_replay_returns_state_dict(self):
        p = Projection("p")
        p.apply(lambda s, e: s.update({"x": 1}))
        result = p.replay([make_event()])
        assert result is p.state

    def test_state_is_dict_after_replay(self):
        p = Projection("p")
        p.apply(lambda s, e: s.update({"k": "v"}))
        result = p.replay([make_event()])
        assert isinstance(result, dict)


# ===========================================================================
# ReplayEngine
# ===========================================================================

class TestReplayEngine:
    def test_init_stores_reference(self, store):
        engine = ReplayEngine(store)
        assert engine.store is store

    def test_replay_aggregate_empty(self, store):
        engine = ReplayEngine(store)
        p = Projection("p")
        p.apply(lambda s, e: s.update({"seen": True}))
        result = engine.replay_aggregate("missing", p)
        assert result == {}

    def test_replay_aggregate_reconstructs_state(self, store):
        store.append(make_event("a", "inc", {"d": 1}, version=1))
        store.append(make_event("a", "inc", {"d": 4}, version=2))
        store.append(make_event("b", "inc", {"d": 99}, version=1))

        engine = ReplayEngine(store)
        p = Projection("counter")
        p.apply_typed(
            "inc",
            lambda s, e: s.update({"total": s.get("total", 0) + e.payload["d"]}),
        )
        result = engine.replay_aggregate("a", p)
        assert result["total"] == 5

    def test_replay_aggregate_filters_by_aggregate(self, store):
        store.append(make_event("a", "t", {"x": 1}, version=1))
        store.append(make_event("b", "t", {"x": 2}, version=1))
        engine = ReplayEngine(store)
        p = Projection("p")
        p.apply(lambda s, e: s.setdefault("ids", []).append(e.aggregate_id))
        engine.replay_aggregate("a", p)
        assert p.state["ids"] == ["a"]

    def test_replay_aggregate_orders_by_sequence(self, store):
        store.append(make_event("a", "t1", version=1))
        store.append(make_event("a", "t2", version=2))
        store.append(make_event("a", "t3", version=3))

        engine = ReplayEngine(store)
        p = Projection("p")
        p.apply(lambda s, e: s.setdefault("types", []).append(e.event_type))
        engine.replay_aggregate("a", p)
        assert p.state["types"] == ["t1", "t2", "t3"]

    def test_replay_all_iterates_every_event(self, populated_store):
        engine = ReplayEngine(populated_store)
        p = Projection("p")
        p.apply(lambda s, e: s.update({"count": s.get("count", 0) + 1}))
        result = engine.replay_all(p)
        assert result["count"] == 5

    def test_replay_all_orders_by_sequence(self, populated_store):
        engine = ReplayEngine(populated_store)
        p = Projection("p")
        p.apply(lambda s, e: s.setdefault("types", []).append(e.event_type))
        engine.replay_all(p)
        # The fixture insertion order:
        # a1.created, a1.updated, a2.created, a1.deleted, a2.updated
        assert p.state["types"] == [
            "created", "updated", "created", "deleted", "updated",
        ]

    def test_replay_all_empty_store(self, store):
        engine = ReplayEngine(store)
        p = Projection("p")
        p.apply(lambda s, e: s.update({"x": 1}))
        result = engine.replay_all(p)
        assert result == {}

    def test_replay_all_uses_typed_handlers(self, populated_store):
        engine = ReplayEngine(populated_store)
        p = Projection("p")
        p.apply_typed("created", lambda s, e: s.update({"c": s.get("c", 0) + 1}))
        p.apply_typed("updated", lambda s, e: s.update({"u": s.get("u", 0) + 1}))
        p.apply_typed("deleted", lambda s, e: s.update({"d": s.get("d", 0) + 1}))
        result = engine.replay_all(p)
        assert result == {"c": 2, "u": 2, "d": 1}

    def test_replay_aggregate_event_type_dispatch(self, store):
        store.append(make_event("a", "inc", {"d": 2}, version=1))
        store.append(make_event("a", "dec", {"d": 1}, version=2))
        store.append(make_event("a", "inc", {"d": 5}, version=3))
        engine = ReplayEngine(store)
        p = Projection("p")
        p.apply_typed(
            "inc",
            lambda s, e: s.update({"v": s.get("v", 0) + e.payload["d"]}),
        )
        p.apply_typed(
            "dec",
            lambda s, e: s.update({"v": s.get("v", 0) - e.payload["d"]}),
        )
        result = engine.replay_aggregate("a", p)
        assert result["v"] == 6  # 2 - 1 + 5

    def test_replay_aggregate_after_append_many(self, store):
        events = [
            make_event("a", "t", {"n": i + 1}, version=i + 1) for i in range(4)
        ]
        store.append_many(events)
        engine = ReplayEngine(store)
        p = Projection("p")
        p.apply(lambda s, e: s.update({"sum": s.get("sum", 0) + e.payload["n"]}))
        result = engine.replay_aggregate("a", p)
        assert result["sum"] == 1 + 2 + 3 + 4


# ===========================================================================
# Integration / round-trip
# ===========================================================================

class TestIntegration:
    def test_end_to_end_counter(self, store):
        # Build a counter projection from events.
        store.append(make_event("c", "inc", {"d": 1}, version=1))
        store.append(make_event("c", "inc", {"d": 2}, version=2))
        store.append(make_event("c", "dec", {"d": 1}, version=3))

        engine = ReplayEngine(store)
        p = Projection("counter")
        p.apply_typed(
            "inc",
            lambda s, e: s.update({"count": s.get("count", 0) + e.payload["d"]}),
        )
        p.apply_typed(
            "dec",
            lambda s, e: s.update({"count": s.get("count", 0) - e.payload["d"]}),
        )
        result = engine.replay_aggregate("c", p)
        assert result == {"count": 2}

    def test_payload_roundtrip_with_nesting(self, store):
        complex_payload = {
            "user": {"name": "Alice", "age": 30},
            "tags": ["a", "b", "c"],
            "score": 3.14,
            "active": True,
            "extras": None,
        }
        e = make_event(payload=complex_payload)
        store.append(e)
        envs = store.get_events(e.aggregate_id)
        assert envs[0].event.payload == complex_payload

    def test_envelope_contains_event_and_sequence(self, store):
        seq = store.append(make_event("a", "t"))
        envs = store.get_all()
        assert envs[0].sequence == seq
        assert envs[0].event.aggregate_id == "a"
        assert envs[0].event.event_type == "t"

    def test_latest_version_zero_initially(self, store):
        assert store.latest_version("anything") == 0

    def test_store_supports_many_events(self, store):
        for i in range(50):
            store.append(make_event("a", "t", version=i + 1))
        assert store.count() == 50
        assert store.latest_version("a") == 50

    def test_replay_all_after_replay_aggregate(self, store):
        store.append(make_event("a", "t", version=1))
        store.append(make_event("b", "t", version=1))
        engine = ReplayEngine(store)
        p1 = Projection("p1")
        p1.apply(lambda s, e: s.update({"c": s.get("c", 0) + 1}))
        engine.replay_aggregate("a", p1)
        assert p1.state["c"] == 1
        p2 = Projection("p2")
        p2.apply(lambda s, e: s.update({"c": s.get("c", 0) + 1}))
        engine.replay_all(p2)
        assert p2.state["c"] == 2
