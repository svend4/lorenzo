"""Tests for docstoolkit.doc_observer."""
from __future__ import annotations

import pytest

from docstoolkit.doc_observer import (
    ChangeType,
    DocChange,
    DocObserver,
    Observer,
    ObserverConfig,
)


# ---------------------------------------------------------------------------
# ChangeType
# ---------------------------------------------------------------------------
class TestChangeType:
    def test_added_value(self):
        assert ChangeType.ADDED.value == "added"

    def test_modified_value(self):
        assert ChangeType.MODIFIED.value == "modified"

    def test_removed_value(self):
        assert ChangeType.REMOVED.value == "removed"

    def test_members(self):
        assert {c.name for c in ChangeType} == {"ADDED", "MODIFIED", "REMOVED"}


# ---------------------------------------------------------------------------
# DocChange
# ---------------------------------------------------------------------------
class TestDocChange:
    def test_basic_fields(self):
        c = DocChange(doc_id="d1", change_type=ChangeType.ADDED)
        assert c.doc_id == "d1"
        assert c.change_type is ChangeType.ADDED
        assert c.timestamp == 0.0
        assert c.old_content is None
        assert c.new_content is None
        assert c.metadata == {}

    def test_with_content(self):
        c = DocChange(
            doc_id="d2",
            change_type=ChangeType.MODIFIED,
            timestamp=1.5,
            old_content="a",
            new_content="b",
        )
        assert c.old_content == "a"
        assert c.new_content == "b"
        assert c.timestamp == 1.5

    def test_metadata_independent(self):
        a = DocChange(doc_id="x", change_type=ChangeType.ADDED)
        b = DocChange(doc_id="y", change_type=ChangeType.ADDED)
        a.metadata["k"] = 1
        assert b.metadata == {}


# ---------------------------------------------------------------------------
# ObserverConfig
# ---------------------------------------------------------------------------
class TestObserverConfig:
    def test_defaults(self):
        cfg = ObserverConfig()
        assert cfg.notify_on_unchanged is False
        assert cfg.track_history is True
        assert cfg.max_history == 100

    def test_overrides(self):
        cfg = ObserverConfig(
            notify_on_unchanged=True, track_history=False, max_history=5
        )
        assert cfg.notify_on_unchanged is True
        assert cfg.track_history is False
        assert cfg.max_history == 5


# ---------------------------------------------------------------------------
# Observer
# ---------------------------------------------------------------------------
class TestObserver:
    def test_defaults(self):
        obs = Observer(
            observer_id="x", pattern="*", callback=lambda c: None
        )
        assert obs.enabled is True
        assert ChangeType.ADDED in obs.change_types
        assert ChangeType.MODIFIED in obs.change_types
        assert ChangeType.REMOVED in obs.change_types

    def test_custom_change_types(self):
        obs = Observer(
            observer_id="x",
            pattern="*",
            callback=lambda c: None,
            change_types={ChangeType.ADDED},
        )
        assert obs.change_types == {ChangeType.ADDED}


# ---------------------------------------------------------------------------
# add_doc
# ---------------------------------------------------------------------------
class TestAddDoc:
    def test_add_new(self):
        do = DocObserver()
        assert do.add_doc("d1", "hello") is True
        assert do.get_doc("d1") == "hello"

    def test_add_duplicate(self):
        do = DocObserver()
        do.add_doc("d1", "hello")
        assert do.add_doc("d1", "world") is False
        assert do.get_doc("d1") == "hello"

    def test_add_records_history(self):
        do = DocObserver()
        do.add_doc("d1", "x", now=1.0)
        hist = do.history()
        assert len(hist) == 1
        assert hist[0].change_type is ChangeType.ADDED
        assert hist[0].timestamp == 1.0
        assert hist[0].new_content == "x"
        assert hist[0].old_content is None


# ---------------------------------------------------------------------------
# update_doc
# ---------------------------------------------------------------------------
class TestUpdateDoc:
    def test_update_existing(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        assert do.update_doc("d1", "b") is True
        assert do.get_doc("d1") == "b"

    def test_update_missing(self):
        do = DocObserver()
        assert do.update_doc("d1", "x") is False

    def test_update_records_history(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.update_doc("d1", "b", now=2.5)
        hist = do.history()
        assert len(hist) == 2
        mod = hist[-1]
        assert mod.change_type is ChangeType.MODIFIED
        assert mod.old_content == "a"
        assert mod.new_content == "b"
        assert mod.timestamp == 2.5

    def test_update_unchanged_no_event(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        events: list[DocChange] = []
        do.register_observer("d1", events.append)
        assert do.update_doc("d1", "a") is True
        assert events == []


# ---------------------------------------------------------------------------
# remove_doc
# ---------------------------------------------------------------------------
class TestRemoveDoc:
    def test_remove_existing(self):
        do = DocObserver()
        do.add_doc("d1", "x")
        assert do.remove_doc("d1") is True
        assert do.get_doc("d1") is None

    def test_remove_missing(self):
        do = DocObserver()
        assert do.remove_doc("d1") is False

    def test_remove_records_history(self):
        do = DocObserver()
        do.add_doc("d1", "x")
        do.remove_doc("d1", now=3.0)
        hist = do.history()
        rem = hist[-1]
        assert rem.change_type is ChangeType.REMOVED
        assert rem.old_content == "x"
        assert rem.new_content is None
        assert rem.timestamp == 3.0


# ---------------------------------------------------------------------------
# register_observer
# ---------------------------------------------------------------------------
class TestRegisterObserver:
    def test_register_returns_id(self):
        do = DocObserver()
        oid = do.register_observer("*", lambda c: None)
        assert isinstance(oid, str)
        assert len(oid) > 0

    def test_register_default_change_types(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("*", events.append)
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        do.remove_doc("d1")
        assert [e.change_type for e in events] == [
            ChangeType.ADDED,
            ChangeType.MODIFIED,
            ChangeType.REMOVED,
        ]

    def test_register_custom_change_types(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("*", events.append, change_types={ChangeType.ADDED})
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        assert len(events) == 1
        assert events[0].change_type is ChangeType.ADDED

    def test_register_multiple(self):
        do = DocObserver()
        a = do.register_observer("*", lambda c: None)
        b = do.register_observer("*", lambda c: None)
        assert a != b
        assert do.observer_count() == 2


# ---------------------------------------------------------------------------
# unregister_observer
# ---------------------------------------------------------------------------
class TestUnregisterObserver:
    def test_unregister_existing(self):
        do = DocObserver()
        oid = do.register_observer("*", lambda c: None)
        assert do.unregister_observer(oid) is True
        assert do.observer_count() == 0

    def test_unregister_missing(self):
        do = DocObserver()
        assert do.unregister_observer("nope") is False

    def test_unregistered_does_not_fire(self):
        do = DocObserver()
        events: list[DocChange] = []
        oid = do.register_observer("*", events.append)
        do.unregister_observer(oid)
        do.add_doc("d1", "x")
        assert events == []


# ---------------------------------------------------------------------------
# enable / disable
# ---------------------------------------------------------------------------
class TestEnableDisableObserver:
    def test_disable(self):
        do = DocObserver()
        events: list[DocChange] = []
        oid = do.register_observer("*", events.append)
        assert do.disable_observer(oid) is True
        do.add_doc("d1", "x")
        assert events == []

    def test_enable(self):
        do = DocObserver()
        events: list[DocChange] = []
        oid = do.register_observer("*", events.append)
        do.disable_observer(oid)
        assert do.enable_observer(oid) is True
        do.add_doc("d1", "x")
        assert len(events) == 1

    def test_enable_missing(self):
        do = DocObserver()
        assert do.enable_observer("nope") is False

    def test_disable_missing(self):
        do = DocObserver()
        assert do.disable_observer("nope") is False


# ---------------------------------------------------------------------------
# matches_pattern
# ---------------------------------------------------------------------------
class TestMatchesPattern:
    def test_exact(self):
        assert DocObserver.matches_pattern("doc_1", "doc_1") is True

    def test_star(self):
        assert DocObserver.matches_pattern("doc_001", "doc_*") is True

    def test_no_match(self):
        assert DocObserver.matches_pattern("note_1", "doc_*") is False

    def test_question_mark(self):
        assert DocObserver.matches_pattern("d1", "d?") is True
        assert DocObserver.matches_pattern("d12", "d?") is False

    def test_match_all(self):
        assert DocObserver.matches_pattern("anything", "*") is True


# ---------------------------------------------------------------------------
# get_doc
# ---------------------------------------------------------------------------
class TestGetDoc:
    def test_missing_returns_none(self):
        do = DocObserver()
        assert do.get_doc("d1") is None

    def test_existing(self):
        do = DocObserver()
        do.add_doc("d1", "hello")
        assert do.get_doc("d1") == "hello"

    def test_after_update(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        assert do.get_doc("d1") == "b"

    def test_after_remove(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.remove_doc("d1")
        assert do.get_doc("d1") is None


# ---------------------------------------------------------------------------
# all_docs
# ---------------------------------------------------------------------------
class TestAllDocs:
    def test_empty(self):
        do = DocObserver()
        assert do.all_docs() == {}

    def test_returns_snapshot(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.add_doc("d2", "b")
        snap = do.all_docs()
        assert snap == {"d1": "a", "d2": "b"}
        # mutating snapshot does not affect store
        snap["d3"] = "c"
        assert do.get_doc("d3") is None


# ---------------------------------------------------------------------------
# history
# ---------------------------------------------------------------------------
class TestHistory:
    def test_all(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        do.remove_doc("d1")
        assert len(do.history()) == 3

    def test_filter_by_doc(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.add_doc("d2", "b")
        do.update_doc("d1", "c")
        h = do.history(doc_id="d1")
        assert len(h) == 2
        assert all(c.doc_id == "d1" for c in h)

    def test_limit(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        do.update_doc("d1", "c")
        h = do.history(limit=2)
        assert len(h) == 2
        # most recent two
        assert h[-1].new_content == "c"

    def test_no_tracking(self):
        do = DocObserver(ObserverConfig(track_history=False))
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        assert do.history() == []


# ---------------------------------------------------------------------------
# observer_count
# ---------------------------------------------------------------------------
class TestObserverCount:
    def test_empty(self):
        do = DocObserver()
        assert do.observer_count() == 0

    def test_count_all(self):
        do = DocObserver()
        do.register_observer("*", lambda c: None)
        oid = do.register_observer("*", lambda c: None)
        do.disable_observer(oid)
        assert do.observer_count(enabled_only=False) == 2

    def test_count_enabled_only(self):
        do = DocObserver()
        do.register_observer("*", lambda c: None)
        oid = do.register_observer("*", lambda c: None)
        do.disable_observer(oid)
        assert do.observer_count(enabled_only=True) == 1


# ---------------------------------------------------------------------------
# doc_count
# ---------------------------------------------------------------------------
class TestDocCount:
    def test_zero(self):
        do = DocObserver()
        assert do.doc_count == 0

    def test_increments(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.add_doc("d2", "b")
        assert do.doc_count == 2

    def test_decrements_on_remove(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.remove_doc("d1")
        assert do.doc_count == 0


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------
class TestClear:
    def test_clear_all(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.register_observer("*", lambda c: None)
        do.clear()
        assert do.doc_count == 0
        assert do.observer_count(enabled_only=False) == 0
        assert do.history() == []


# ---------------------------------------------------------------------------
# Observer fires on add
# ---------------------------------------------------------------------------
class TestObserverFiresOnAdd:
    def test_fires(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("*", events.append)
        do.add_doc("d1", "x")
        assert len(events) == 1
        assert events[0].change_type is ChangeType.ADDED
        assert events[0].new_content == "x"

    def test_fires_with_timestamp(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("*", events.append)
        do.add_doc("d1", "x", now=42.0)
        assert events[0].timestamp == 42.0


# ---------------------------------------------------------------------------
# Observer fires on update
# ---------------------------------------------------------------------------
class TestObserverFiresOnUpdate:
    def test_fires_modified(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.add_doc("d1", "a")
        do.register_observer("*", events.append)
        do.update_doc("d1", "b")
        assert len(events) == 1
        assert events[0].change_type is ChangeType.MODIFIED
        assert events[0].old_content == "a"
        assert events[0].new_content == "b"

    def test_no_event_for_missing(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("*", events.append)
        do.update_doc("d1", "b")
        assert events == []


# ---------------------------------------------------------------------------
# Observer fires on remove
# ---------------------------------------------------------------------------
class TestObserverFiresOnRemove:
    def test_fires_removed(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.add_doc("d1", "x")
        do.register_observer("*", events.append)
        do.remove_doc("d1")
        assert len(events) == 1
        assert events[0].change_type is ChangeType.REMOVED
        assert events[0].old_content == "x"

    def test_no_event_for_missing(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("*", events.append)
        do.remove_doc("d1")
        assert events == []


# ---------------------------------------------------------------------------
# Pattern filtering
# ---------------------------------------------------------------------------
class TestObserverFilterByPattern:
    def test_glob_match(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("doc_*", events.append)
        do.add_doc("doc_1", "a")
        do.add_doc("note_1", "b")
        assert len(events) == 1
        assert events[0].doc_id == "doc_1"

    def test_exact_pattern(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("d1", events.append)
        do.add_doc("d1", "a")
        do.add_doc("d2", "b")
        assert len(events) == 1

    def test_star_matches_all(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("*", events.append)
        do.add_doc("anything", "a")
        do.add_doc("else", "b")
        assert len(events) == 2


# ---------------------------------------------------------------------------
# Change-type filtering
# ---------------------------------------------------------------------------
class TestObserverFilterByChangeType:
    def test_only_added(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("*", events.append, change_types={ChangeType.ADDED})
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        do.remove_doc("d1")
        assert [e.change_type for e in events] == [ChangeType.ADDED]

    def test_only_removed(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer("*", events.append, change_types={ChangeType.REMOVED})
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        do.remove_doc("d1")
        assert [e.change_type for e in events] == [ChangeType.REMOVED]

    def test_added_and_removed(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.register_observer(
            "*",
            events.append,
            change_types={ChangeType.ADDED, ChangeType.REMOVED},
        )
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        do.remove_doc("d1")
        assert [e.change_type for e in events] == [
            ChangeType.ADDED,
            ChangeType.REMOVED,
        ]


# ---------------------------------------------------------------------------
# notify_on_unchanged
# ---------------------------------------------------------------------------
class TestNotifyOnUnchanged:
    def test_default_no_event(self):
        do = DocObserver()
        events: list[DocChange] = []
        do.add_doc("d1", "a")
        do.register_observer("*", events.append)
        do.update_doc("d1", "a")
        assert events == []

    def test_enabled_fires_event(self):
        do = DocObserver(ObserverConfig(notify_on_unchanged=True))
        events: list[DocChange] = []
        do.add_doc("d1", "a")
        do.register_observer("*", events.append)
        do.update_doc("d1", "a")
        assert len(events) == 1
        assert events[0].change_type is ChangeType.MODIFIED
        assert events[0].old_content == "a"
        assert events[0].new_content == "a"


# ---------------------------------------------------------------------------
# max_history truncation
# ---------------------------------------------------------------------------
class TestMaxHistory:
    def test_truncates(self):
        do = DocObserver(ObserverConfig(max_history=3))
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        do.update_doc("d1", "c")
        do.update_doc("d1", "d")
        do.update_doc("d1", "e")
        hist = do.history()
        assert len(hist) == 3
        # oldest entries dropped, so last three are c/d/e
        assert hist[-1].new_content == "e"
        assert hist[0].new_content == "c"

    def test_no_truncation_under_cap(self):
        do = DocObserver(ObserverConfig(max_history=10))
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        assert len(do.history()) == 2


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_callback_exception_does_not_break_chain(self):
        do = DocObserver()
        good_events: list[DocChange] = []

        def bad(_change):
            raise RuntimeError("boom")

        do.register_observer("*", bad)
        do.register_observer("*", good_events.append)
        do.add_doc("d1", "x")
        assert len(good_events) == 1

    def test_multiple_observers_same_pattern(self):
        do = DocObserver()
        a: list[DocChange] = []
        b: list[DocChange] = []
        do.register_observer("doc_*", a.append)
        do.register_observer("doc_*", b.append)
        do.add_doc("doc_1", "x")
        assert len(a) == 1
        assert len(b) == 1

    def test_observer_can_register_during_iteration(self):
        # An observer that adds another observer should not crash.
        do = DocObserver()
        events: list[DocChange] = []

        def add_another(_change):
            do.register_observer("*", events.append)

        do.register_observer("*", add_another)
        do.add_doc("d1", "x")
        # First add: only add_another fires (events still empty).
        do.add_doc("d2", "y")
        # Second add: now both fire (and add_another runs again).
        assert len(events) >= 1

    def test_empty_content(self):
        do = DocObserver()
        do.add_doc("d1", "")
        assert do.get_doc("d1") == ""

    def test_history_limit_zero(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.update_doc("d1", "b")
        assert do.history(limit=0) == []

    def test_history_filter_no_results(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        assert do.history(doc_id="missing") == []

    def test_clear_then_use(self):
        do = DocObserver()
        do.add_doc("d1", "a")
        do.register_observer("*", lambda c: None)
        do.clear()
        # store is fresh; new add should still work and history starts empty
        assert do.add_doc("d1", "x") is True
        assert len(do.history()) == 1

    def test_observer_disabled_does_not_count_as_enabled(self):
        do = DocObserver()
        oid = do.register_observer("*", lambda c: None)
        do.disable_observer(oid)
        assert do.observer_count(enabled_only=True) == 0
        assert do.observer_count(enabled_only=False) == 1
