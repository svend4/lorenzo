"""Tests for E323 doc_workflow_state."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_workflow_state import (
    DocWorkflowState,
    StateRecord,
    StateTransition,
    WorkflowStats,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestStateTransitionDataclass:
    def test_create(self):
        t = StateTransition(from_state="draft", to_state="review", action="submit")
        assert t.from_state == "draft"
        assert t.to_state == "review"
        assert t.action == "submit"

    def test_equality(self):
        a = StateTransition("draft", "review", "submit")
        b = StateTransition("draft", "review", "submit")
        assert a == b

    def test_inequality(self):
        a = StateTransition("draft", "review", "submit")
        b = StateTransition("draft", "approved", "submit")
        assert a != b

    def test_fields(self):
        t = StateTransition(from_state="a", to_state="b", action="go")
        assert hasattr(t, "from_state")
        assert hasattr(t, "to_state")
        assert hasattr(t, "action")


class TestStateRecordDataclass:
    def test_minimal(self):
        r = StateRecord(doc_id="d1", state="draft")
        assert r.doc_id == "d1"
        assert r.state == "draft"
        assert r.entered_at == 0.0
        assert r.entered_by == ""
        assert r.previous_state is None

    def test_full(self):
        r = StateRecord(
            doc_id="d1",
            state="review",
            entered_at=123.0,
            entered_by="alice",
            previous_state="draft",
        )
        assert r.entered_at == 123.0
        assert r.entered_by == "alice"
        assert r.previous_state == "draft"

    def test_equality(self):
        a = StateRecord(doc_id="d1", state="draft", entered_at=1.0)
        b = StateRecord(doc_id="d1", state="draft", entered_at=1.0)
        assert a == b

    def test_defaults_are_correct(self):
        r = StateRecord("x", "y")
        assert r.entered_at == 0.0
        assert r.previous_state is None


class TestWorkflowStatsDataclass:
    def test_default(self):
        s = WorkflowStats(total_docs=0, total_transitions=0)
        assert s.total_docs == 0
        assert s.total_transitions == 0
        assert s.state_counts == {}

    def test_with_counts(self):
        s = WorkflowStats(total_docs=2, total_transitions=3, state_counts={"draft": 2})
        assert s.state_counts == {"draft": 2}

    def test_state_counts_default_factory(self):
        a = WorkflowStats(total_docs=0, total_transitions=0)
        b = WorkflowStats(total_docs=0, total_transitions=0)
        a.state_counts["draft"] = 1
        assert b.state_counts == {}


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_create(self):
        w = DocWorkflowState()
        assert w is not None

    def test_empty_stats(self):
        w = DocWorkflowState()
        s = w.stats()
        assert s.total_docs == 0
        assert s.total_transitions == 0
        assert s.state_counts == {}

    def test_empty_transitions(self):
        w = DocWorkflowState()
        assert w.list_transitions() == []

    def test_empty_all_states(self):
        w = DocWorkflowState()
        assert w.all_states() == []


# ---------------------------------------------------------------------------
# define_transition
# ---------------------------------------------------------------------------


class TestDefineTransition:
    def test_new(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        ts = w.list_transitions()
        assert len(ts) == 1
        assert ts[0].from_state == "draft"
        assert ts[0].action == "submit"
        assert ts[0].to_state == "review"

    def test_replace(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.define_transition("draft", "submit", "approved")
        ts = w.list_transitions()
        assert len(ts) == 1
        assert ts[0].to_state == "approved"

    def test_multiple(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.define_transition("review", "approve", "approved")
        w.define_transition("review", "reject", "draft")
        assert len(w.list_transitions()) == 3

    def test_different_from_states_same_action(self):
        w = DocWorkflowState()
        w.define_transition("draft", "edit", "draft")
        w.define_transition("review", "edit", "draft")
        assert len(w.list_transitions()) == 2


# ---------------------------------------------------------------------------
# remove_transition
# ---------------------------------------------------------------------------


class TestRemoveTransition:
    def test_existing_returns_true(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        assert w.remove_transition("draft", "submit") is True

    def test_actually_removed(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.remove_transition("draft", "submit")
        assert w.list_transitions() == []

    def test_missing_returns_false(self):
        w = DocWorkflowState()
        assert w.remove_transition("draft", "submit") is False

    def test_remove_one_keeps_others(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.define_transition("review", "approve", "approved")
        w.remove_transition("draft", "submit")
        ts = w.list_transitions()
        assert len(ts) == 1
        assert ts[0].action == "approve"


# ---------------------------------------------------------------------------
# list_transitions
# ---------------------------------------------------------------------------


class TestListTransitions:
    def test_sorted_by_from_state(self):
        w = DocWorkflowState()
        w.define_transition("review", "approve", "approved")
        w.define_transition("draft", "submit", "review")
        w.define_transition("approved", "publish", "published")
        ts = w.list_transitions()
        froms = [t.from_state for t in ts]
        assert froms == ["approved", "draft", "review"]

    def test_sorted_by_action_within_from(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.define_transition("draft", "delete", "trash")
        w.define_transition("draft", "archive", "archived")
        ts = [t for t in w.list_transitions() if t.from_state == "draft"]
        actions = [t.action for t in ts]
        assert actions == sorted(actions)

    def test_empty(self):
        w = DocWorkflowState()
        assert w.list_transitions() == []


# ---------------------------------------------------------------------------
# set_initial_state
# ---------------------------------------------------------------------------


class TestSetInitialState:
    def test_creates_record(self):
        w = DocWorkflowState()
        r = w.set_initial_state("d1", "draft", now=100.0)
        assert r.doc_id == "d1"
        assert r.state == "draft"
        assert r.entered_at == 100.0

    def test_previous_state_is_none(self):
        w = DocWorkflowState()
        r = w.set_initial_state("d1", "draft")
        assert r.previous_state is None

    def test_entered_by(self):
        w = DocWorkflowState()
        r = w.set_initial_state("d1", "draft", entered_by="alice")
        assert r.entered_by == "alice"

    def test_now_default_uses_time(self):
        w = DocWorkflowState()
        r = w.set_initial_state("d1", "draft")
        assert r.entered_at > 0.0

    def test_current_state_updated(self):
        w = DocWorkflowState()
        w.set_initial_state("d1", "draft")
        assert w.state_of("d1") == "draft"

    def test_overwrites(self):
        w = DocWorkflowState()
        w.set_initial_state("d1", "draft")
        w.set_initial_state("d1", "review")
        assert w.state_of("d1") == "review"


# ---------------------------------------------------------------------------
# transition
# ---------------------------------------------------------------------------


class TestTransition:
    def test_valid_transition(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft")
        r = w.transition("d1", "submit", now=200.0)
        assert r is not None
        assert r.state == "review"
        assert r.previous_state == "draft"
        assert r.entered_at == 200.0

    def test_invalid_action_returns_none(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft")
        r = w.transition("d1", "unknown_action")
        assert r is None

    def test_missing_doc_returns_none(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        r = w.transition("nope", "submit")
        assert r is None

    def test_history_grows(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.define_transition("review", "approve", "approved")
        w.set_initial_state("d1", "draft")
        assert w.history_for("d1") == []
        w.transition("d1", "submit")
        assert len(w.history_for("d1")) == 1
        w.transition("d1", "approve")
        assert len(w.history_for("d1")) == 2

    def test_history_records_previous_state(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft", entered_by="alice")
        w.transition("d1", "submit", entered_by="bob")
        h = w.history_for("d1")
        assert h[0].state == "draft"
        assert h[0].entered_by == "alice"

    def test_current_updated_after_transition(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft")
        w.transition("d1", "submit")
        assert w.state_of("d1") == "review"

    def test_no_transition_for_wrong_state(self):
        w = DocWorkflowState()
        w.define_transition("review", "approve", "approved")
        w.set_initial_state("d1", "draft")
        r = w.transition("d1", "approve")
        assert r is None
        assert w.state_of("d1") == "draft"

    def test_failed_transition_does_not_grow_history(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft")
        w.transition("d1", "unknown")
        assert w.history_for("d1") == []

    def test_entered_by_recorded(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft")
        r = w.transition("d1", "submit", entered_by="carol")
        assert r.entered_by == "carol"


# ---------------------------------------------------------------------------
# current_state
# ---------------------------------------------------------------------------


class TestCurrentState:
    def test_found(self):
        w = DocWorkflowState()
        w.set_initial_state("d1", "draft", now=10.0)
        r = w.current_state("d1")
        assert r is not None
        assert r.state == "draft"
        assert r.entered_at == 10.0

    def test_not_found(self):
        w = DocWorkflowState()
        assert w.current_state("nope") is None

    def test_after_transition(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft")
        w.transition("d1", "submit")
        r = w.current_state("d1")
        assert r.state == "review"
        assert r.previous_state == "draft"


# ---------------------------------------------------------------------------
# state_of
# ---------------------------------------------------------------------------


class TestStateOf:
    def test_returns_string(self):
        w = DocWorkflowState()
        w.set_initial_state("d1", "draft")
        assert w.state_of("d1") == "draft"

    def test_none_when_missing(self):
        w = DocWorkflowState()
        assert w.state_of("nope") is None

    def test_after_transition(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft")
        w.transition("d1", "submit")
        assert w.state_of("d1") == "review"


# ---------------------------------------------------------------------------
# history_for
# ---------------------------------------------------------------------------


class TestHistoryFor:
    def test_empty_initially(self):
        w = DocWorkflowState()
        w.set_initial_state("d1", "draft")
        assert w.history_for("d1") == []

    def test_empty_for_unknown_doc(self):
        w = DocWorkflowState()
        assert w.history_for("nope") == []

    def test_order_preserved(self):
        w = DocWorkflowState()
        w.define_transition("a", "go", "b")
        w.define_transition("b", "go", "c")
        w.define_transition("c", "go", "d")
        w.set_initial_state("d1", "a")
        w.transition("d1", "go")
        w.transition("d1", "go")
        w.transition("d1", "go")
        states = [r.state for r in w.history_for("d1")]
        assert states == ["a", "b", "c"]

    def test_excludes_current(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft")
        w.transition("d1", "submit")
        h = w.history_for("d1")
        # current is "review", history contains "draft"
        for rec in h:
            assert rec.state != "review"


# ---------------------------------------------------------------------------
# docs_in_state
# ---------------------------------------------------------------------------


class TestDocsInState:
    def test_filters_correctly(self):
        w = DocWorkflowState()
        w.set_initial_state("d1", "draft")
        w.set_initial_state("d2", "review")
        w.set_initial_state("d3", "draft")
        assert w.docs_in_state("draft") == ["d1", "d3"]

    def test_sorted(self):
        w = DocWorkflowState()
        w.set_initial_state("zzz", "draft")
        w.set_initial_state("aaa", "draft")
        w.set_initial_state("mmm", "draft")
        assert w.docs_in_state("draft") == ["aaa", "mmm", "zzz"]

    def test_empty(self):
        w = DocWorkflowState()
        assert w.docs_in_state("draft") == []

    def test_no_matches(self):
        w = DocWorkflowState()
        w.set_initial_state("d1", "draft")
        assert w.docs_in_state("review") == []

    def test_after_transition(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft")
        w.transition("d1", "submit")
        assert w.docs_in_state("draft") == []
        assert w.docs_in_state("review") == ["d1"]


# ---------------------------------------------------------------------------
# available_actions
# ---------------------------------------------------------------------------


class TestAvailableActions:
    def test_based_on_current_state(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.define_transition("draft", "delete", "trash")
        w.define_transition("review", "approve", "approved")
        w.set_initial_state("d1", "draft")
        actions = w.available_actions("d1")
        assert set(actions) == {"submit", "delete"}

    def test_sorted(self):
        w = DocWorkflowState()
        w.define_transition("draft", "zzz", "x")
        w.define_transition("draft", "aaa", "x")
        w.define_transition("draft", "mmm", "x")
        w.set_initial_state("d1", "draft")
        assert w.available_actions("d1") == ["aaa", "mmm", "zzz"]

    def test_empty_when_doc_missing(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        assert w.available_actions("nope") == []

    def test_empty_when_no_transitions_for_state(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "approved")
        assert w.available_actions("d1") == []


# ---------------------------------------------------------------------------
# all_states
# ---------------------------------------------------------------------------


class TestAllStates:
    def test_collected_from_transitions(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.define_transition("review", "approve", "approved")
        assert w.all_states() == ["approved", "draft", "review"]

    def test_collected_from_current_states(self):
        w = DocWorkflowState()
        w.set_initial_state("d1", "custom_state")
        assert "custom_state" in w.all_states()

    def test_union(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "extra")
        states = w.all_states()
        assert set(states) >= {"draft", "review", "extra"}

    def test_sorted_unique(self):
        w = DocWorkflowState()
        w.define_transition("z", "go", "a")
        w.define_transition("a", "go", "z")
        states = w.all_states()
        assert states == ["a", "z"]

    def test_empty(self):
        w = DocWorkflowState()
        assert w.all_states() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        w = DocWorkflowState()
        s = w.stats()
        assert s.total_docs == 0
        assert s.total_transitions == 0
        assert s.state_counts == {}

    def test_total_docs(self):
        w = DocWorkflowState()
        w.set_initial_state("d1", "draft")
        w.set_initial_state("d2", "review")
        assert w.stats().total_docs == 2

    def test_total_transitions(self):
        w = DocWorkflowState()
        w.define_transition("a", "go", "b")
        w.define_transition("b", "go", "c")
        assert w.stats().total_transitions == 2

    def test_state_counts(self):
        w = DocWorkflowState()
        w.set_initial_state("d1", "draft")
        w.set_initial_state("d2", "draft")
        w.set_initial_state("d3", "review")
        s = w.stats()
        assert s.state_counts == {"draft": 2, "review": 1}

    def test_state_counts_after_transition(self):
        w = DocWorkflowState()
        w.define_transition("draft", "submit", "review")
        w.set_initial_state("d1", "draft")
        w.set_initial_state("d2", "draft")
        w.transition("d1", "submit")
        s = w.stats()
        assert s.state_counts == {"draft": 1, "review": 1}


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_transitions(self):
        w = DocWorkflowState()
        # A loop: state cycles a -> b -> a
        w.define_transition("a", "go", "b")
        w.define_transition("b", "go", "a")
        for i in range(50):
            w.set_initial_state(f"d{i}", "a")

        errors: list = []

        def worker(doc_ids):
            try:
                for d in doc_ids:
                    for _ in range(20):
                        w.transition(d, "go")
            except Exception as e:  # pragma: no cover
                errors.append(e)

        threads = []
        chunks = [
            [f"d{i}" for i in range(0, 25)],
            [f"d{i}" for i in range(25, 50)],
        ]
        for c in chunks:
            t = threading.Thread(target=worker, args=(c,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        # all docs should be either "a" or "b"
        for i in range(50):
            assert w.state_of(f"d{i}") in {"a", "b"}

    def test_concurrent_define(self):
        w = DocWorkflowState()
        errors: list = []

        def worker(start):
            try:
                for i in range(50):
                    w.define_transition(f"s{start}_{i}", "go", f"t{start}_{i}")
            except Exception as e:  # pragma: no cover
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(k,)) for k in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []
        assert len(w.list_transitions()) == 200

    def test_concurrent_set_initial(self):
        w = DocWorkflowState()
        errors: list = []

        def worker(start):
            try:
                for i in range(50):
                    w.set_initial_state(f"d{start}_{i}", "draft")
            except Exception as e:  # pragma: no cover
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(k,)) for k in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []
        assert w.stats().total_docs == 200
