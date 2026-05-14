"""Tests for E409 doc_workflow_state_v2."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_workflow_state_v2 import (
    DocWorkflowStateV2,
    StateGuard,
    StateRecord,
    Transition,
    WorkflowStatsV2,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestStateGuardDataclass:
    def test_create_with_condition(self):
        g = StateGuard(name="is_admin", condition=lambda d, c: True)
        assert g.name == "is_admin"
        assert callable(g.condition)

    def test_create_default_condition_none(self):
        g = StateGuard(name="always")
        assert g.name == "always"
        assert g.condition is None

    def test_equality_by_name_only_when_cond_equal(self):
        a = StateGuard(name="g", condition=None)
        b = StateGuard(name="g", condition=None)
        assert a == b

    def test_inequality_different_names(self):
        a = StateGuard(name="a")
        b = StateGuard(name="b")
        assert a != b


class TestTransitionDataclass:
    def test_create_no_guards(self):
        t = Transition(from_state="draft", to_state="review", action="submit")
        assert t.from_state == "draft"
        assert t.to_state == "review"
        assert t.action == "submit"
        assert t.guards == []

    def test_create_with_guards(self):
        g = StateGuard(name="g")
        t = Transition("a", "b", "go", guards=[g])
        assert t.guards == [g]

    def test_independent_default_lists(self):
        a = Transition("s", "t", "act")
        b = Transition("s", "t", "act")
        a.guards.append(StateGuard(name="x"))
        assert b.guards == []


class TestStateRecordDataclass:
    def test_create_minimal(self):
        r = StateRecord(doc_id="d", state="draft")
        assert r.doc_id == "d"
        assert r.state == "draft"
        assert r.entered_at == 0.0
        assert r.entered_by == ""
        assert r.previous_state is None
        assert r.transition_count == 0

    def test_create_full(self):
        r = StateRecord(
            doc_id="d",
            state="review",
            entered_at=42.0,
            entered_by="alice",
            previous_state="draft",
            transition_count=3,
        )
        assert r.previous_state == "draft"
        assert r.transition_count == 3
        assert r.entered_by == "alice"


class TestWorkflowStatsV2Dataclass:
    def test_create_default(self):
        s = WorkflowStatsV2(total_docs=0, total_transitions=0, guard_failures=0)
        assert s.state_counts == {}

    def test_create_full(self):
        s = WorkflowStatsV2(
            total_docs=2,
            total_transitions=4,
            state_counts={"draft": 1},
            guard_failures=1,
        )
        assert s.total_docs == 2
        assert s.total_transitions == 4
        assert s.state_counts == {"draft": 1}
        assert s.guard_failures == 1

    def test_independent_default_dicts(self):
        a = WorkflowStatsV2(total_docs=0, total_transitions=0, guard_failures=0)
        b = WorkflowStatsV2(total_docs=0, total_transitions=0, guard_failures=0)
        a.state_counts["draft"] = 1
        assert b.state_counts == {}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def sm():
    return DocWorkflowStateV2()


@pytest.fixture
def basic_sm():
    s = DocWorkflowStateV2()
    s.define_transition(Transition("draft", "review", "submit"))
    s.define_transition(Transition("review", "published", "approve"))
    s.define_transition(Transition("review", "draft", "reject"))
    return s


# ---------------------------------------------------------------------------
# define_transition / remove_transition / list_transitions
# ---------------------------------------------------------------------------


class TestDefineTransition:
    def test_define_single(self, sm):
        t = Transition("a", "b", "go")
        sm.define_transition(t)
        assert sm.list_transitions() == [t]

    def test_define_replaces_existing(self, sm):
        sm.define_transition(Transition("a", "b", "go"))
        sm.define_transition(Transition("a", "c", "go"))
        ts = sm.list_transitions()
        assert len(ts) == 1
        assert ts[0].to_state == "c"

    def test_define_multiple(self, sm):
        sm.define_transition(Transition("a", "b", "x"))
        sm.define_transition(Transition("a", "c", "y"))
        assert len(sm.list_transitions()) == 2

    def test_define_with_guards_preserved(self, sm):
        g = StateGuard(name="guard1")
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        assert sm.list_transitions()[0].guards == [g]


class TestRemoveTransition:
    def test_remove_existing(self, sm):
        sm.define_transition(Transition("a", "b", "go"))
        assert sm.remove_transition("a", "go") is True
        assert sm.list_transitions() == []

    def test_remove_missing(self, sm):
        assert sm.remove_transition("a", "go") is False

    def test_remove_only_targeted(self, sm):
        sm.define_transition(Transition("a", "b", "x"))
        sm.define_transition(Transition("a", "c", "y"))
        assert sm.remove_transition("a", "x") is True
        remaining = sm.list_transitions()
        assert len(remaining) == 1
        assert remaining[0].action == "y"


class TestListTransitions:
    def test_empty(self, sm):
        assert sm.list_transitions() == []

    def test_sorted_by_from_then_action(self, sm):
        sm.define_transition(Transition("b", "x", "go"))
        sm.define_transition(Transition("a", "x", "z"))
        sm.define_transition(Transition("a", "x", "a"))
        ts = sm.list_transitions()
        assert [(t.from_state, t.action) for t in ts] == [
            ("a", "a"),
            ("a", "z"),
            ("b", "go"),
        ]


# ---------------------------------------------------------------------------
# set_initial_state
# ---------------------------------------------------------------------------


class TestSetInitialState:
    def test_basic(self, sm):
        rec = sm.set_initial_state("d1", "draft", now=100.0)
        assert rec.doc_id == "d1"
        assert rec.state == "draft"
        assert rec.entered_at == 100.0
        assert rec.previous_state is None
        assert rec.transition_count == 0

    def test_entered_by(self, sm):
        rec = sm.set_initial_state("d1", "draft", entered_by="alice", now=1.0)
        assert rec.entered_by == "alice"

    def test_overwrites(self, sm):
        sm.set_initial_state("d1", "draft", now=1.0)
        rec = sm.set_initial_state("d1", "review", now=2.0)
        assert rec.state == "review"
        assert sm.state_of("d1") == "review"

    def test_default_now_is_time(self, sm):
        rec = sm.set_initial_state("d1", "draft")
        assert rec.entered_at > 0.0


# ---------------------------------------------------------------------------
# transition
# ---------------------------------------------------------------------------


class TestTransition:
    def test_basic(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        rec = basic_sm.transition("d", "submit", now=2.0)
        assert rec is not None
        assert rec.state == "review"
        assert rec.previous_state == "draft"
        assert rec.entered_at == 2.0
        assert rec.transition_count == 1

    def test_returns_none_unknown_doc(self, basic_sm):
        assert basic_sm.transition("missing", "submit") is None

    def test_returns_none_no_transition_defined(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        assert basic_sm.transition("d", "approve") is None

    def test_transition_count_increments(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        basic_sm.transition("d", "submit", now=2.0)
        basic_sm.transition("d", "reject", now=3.0)
        basic_sm.transition("d", "submit", now=4.0)
        rec = basic_sm.current_state("d")
        assert rec.transition_count == 3

    def test_entered_by_recorded(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        rec = basic_sm.transition("d", "submit", entered_by="bob", now=2.0)
        assert rec.entered_by == "bob"

    def test_default_now_used(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        rec = basic_sm.transition("d", "submit")
        assert rec.entered_at > 0.0

    def test_context_passed_to_guard(self):
        sm = DocWorkflowStateV2()
        seen = {}

        def cond(doc_id, ctx):
            seen["doc"] = doc_id
            seen["ctx"] = ctx
            return True

        sm.define_transition(
            Transition("a", "b", "go", guards=[StateGuard(name="g", condition=cond)])
        )
        sm.set_initial_state("d1", "a")
        sm.transition("d1", "go", context={"user": "alice"})
        assert seen["doc"] == "d1"
        assert seen["ctx"] == {"user": "alice"}

    def test_default_context_is_empty_dict(self):
        sm = DocWorkflowStateV2()
        seen = {}

        def cond(doc_id, ctx):
            seen["ctx"] = ctx
            return True

        sm.define_transition(
            Transition("a", "b", "go", guards=[StateGuard(name="g", condition=cond)])
        )
        sm.set_initial_state("d1", "a")
        sm.transition("d1", "go")
        assert seen["ctx"] == {}


# ---------------------------------------------------------------------------
# Guards
# ---------------------------------------------------------------------------


class TestGuards:
    def test_single_passing_guard(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="ok", condition=lambda d, c: True)
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        rec = sm.transition("d", "go")
        assert rec is not None
        assert rec.state == "b"

    def test_single_failing_guard(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="no", condition=lambda d, c: False)
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        assert sm.transition("d", "go") is None
        assert sm.state_of("d") == "a"

    def test_guard_failure_increments_counter(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="no", condition=lambda d, c: False)
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        sm.transition("d", "go")
        sm.transition("d", "go")
        assert sm.stats().guard_failures == 2

    def test_guard_pass_does_not_increment(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="ok", condition=lambda d, c: True)
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        sm.transition("d", "go")
        assert sm.stats().guard_failures == 0

    def test_multiple_guards_all_must_pass(self):
        sm = DocWorkflowStateV2()
        g1 = StateGuard(name="g1", condition=lambda d, c: True)
        g2 = StateGuard(name="g2", condition=lambda d, c: True)
        sm.define_transition(Transition("a", "b", "go", guards=[g1, g2]))
        sm.set_initial_state("d", "a")
        assert sm.transition("d", "go") is not None

    def test_multiple_guards_any_fail_blocks(self):
        sm = DocWorkflowStateV2()
        g1 = StateGuard(name="g1", condition=lambda d, c: True)
        g2 = StateGuard(name="g2", condition=lambda d, c: False)
        sm.define_transition(Transition("a", "b", "go", guards=[g1, g2]))
        sm.set_initial_state("d", "a")
        assert sm.transition("d", "go") is None
        assert sm.stats().guard_failures == 1

    def test_none_condition_is_pass(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="g", condition=None)
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        assert sm.transition("d", "go") is not None

    def test_guard_uses_context(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="admin", condition=lambda d, c: c.get("role") == "admin")
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        assert sm.transition("d", "go", context={"role": "user"}) is None
        assert sm.transition("d", "go", context={"role": "admin"}) is not None

    def test_guard_exception_treated_as_failure(self):
        sm = DocWorkflowStateV2()

        def bad(doc_id, ctx):
            raise RuntimeError("boom")

        g = StateGuard(name="g", condition=bad)
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        assert sm.transition("d", "go") is None
        assert sm.stats().guard_failures == 1

    def test_guard_truthy_non_bool_passes(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="g", condition=lambda d, c: [1])
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        assert sm.transition("d", "go") is not None

    def test_guard_falsy_non_bool_blocks(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="g", condition=lambda d, c: [])
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        assert sm.transition("d", "go") is None


# ---------------------------------------------------------------------------
# current_state / state_of
# ---------------------------------------------------------------------------


class TestCurrentState:
    def test_unknown_doc(self, sm):
        assert sm.current_state("missing") is None
        assert sm.state_of("missing") is None

    def test_after_initial(self, sm):
        sm.set_initial_state("d", "draft", now=1.0)
        rec = sm.current_state("d")
        assert rec is not None
        assert rec.state == "draft"
        assert sm.state_of("d") == "draft"

    def test_after_transition(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        basic_sm.transition("d", "submit", now=2.0)
        assert basic_sm.state_of("d") == "review"


# ---------------------------------------------------------------------------
# history_for
# ---------------------------------------------------------------------------


class TestHistoryFor:
    def test_unknown_doc(self, sm):
        assert sm.history_for("missing") == []

    def test_initial_only(self, sm):
        sm.set_initial_state("d", "draft")
        assert sm.history_for("d") == []

    def test_excludes_current(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        basic_sm.transition("d", "submit", now=2.0)
        history = basic_sm.history_for("d")
        assert len(history) == 1
        assert history[0].state == "draft"

    def test_multiple_transitions(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        basic_sm.transition("d", "submit", now=2.0)
        basic_sm.transition("d", "reject", now=3.0)
        basic_sm.transition("d", "submit", now=4.0)
        history = basic_sm.history_for("d")
        assert [r.state for r in history] == ["draft", "review", "draft"]

    def test_history_is_copy(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        basic_sm.transition("d", "submit", now=2.0)
        h = basic_sm.history_for("d")
        h.clear()
        assert len(basic_sm.history_for("d")) == 1

    def test_failed_transition_no_history(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="no", condition=lambda d, c: False)
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        sm.transition("d", "go")
        assert sm.history_for("d") == []


# ---------------------------------------------------------------------------
# available_actions
# ---------------------------------------------------------------------------


class TestAvailableActions:
    def test_unknown_doc(self, sm):
        assert sm.available_actions("missing") == []

    def test_no_actions_defined(self, sm):
        sm.set_initial_state("d", "draft")
        assert sm.available_actions("d") == []

    def test_sorted(self, basic_sm):
        basic_sm.set_initial_state("d", "review", now=1.0)
        assert basic_sm.available_actions("d") == ["approve", "reject"]

    def test_only_for_current_state(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        assert basic_sm.available_actions("d") == ["submit"]

    def test_ignores_guards(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="no", condition=lambda d, c: False)
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        # Action is structurally defined even though guard blocks it.
        assert sm.available_actions("d") == ["go"]


# ---------------------------------------------------------------------------
# docs_in_state
# ---------------------------------------------------------------------------


class TestDocsInState:
    def test_empty(self, sm):
        assert sm.docs_in_state("draft") == []

    def test_sorted(self, sm):
        sm.set_initial_state("zeta", "draft")
        sm.set_initial_state("alpha", "draft")
        sm.set_initial_state("mid", "draft")
        assert sm.docs_in_state("draft") == ["alpha", "mid", "zeta"]

    def test_filtered_by_state(self, sm):
        sm.set_initial_state("d1", "draft")
        sm.set_initial_state("d2", "review")
        assert sm.docs_in_state("draft") == ["d1"]
        assert sm.docs_in_state("review") == ["d2"]

    def test_after_transition(self, basic_sm):
        basic_sm.set_initial_state("d", "draft", now=1.0)
        basic_sm.transition("d", "submit", now=2.0)
        assert basic_sm.docs_in_state("draft") == []
        assert basic_sm.docs_in_state("review") == ["d"]


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self, sm):
        s = sm.stats()
        assert s.total_docs == 0
        assert s.total_transitions == 0
        assert s.state_counts == {}
        assert s.guard_failures == 0

    def test_counts_transitions(self, basic_sm):
        s = basic_sm.stats()
        assert s.total_transitions == 3

    def test_counts_docs(self, basic_sm):
        basic_sm.set_initial_state("d1", "draft")
        basic_sm.set_initial_state("d2", "draft")
        basic_sm.set_initial_state("d3", "review")
        s = basic_sm.stats()
        assert s.total_docs == 3
        assert s.state_counts == {"draft": 2, "review": 1}

    def test_guard_failures_tracked(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="no", condition=lambda d, c: False)
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        sm.set_initial_state("d", "a")
        sm.transition("d", "go")
        sm.transition("d", "go")
        sm.transition("d", "go")
        assert sm.stats().guard_failures == 3


# ---------------------------------------------------------------------------
# Thread-safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_set_initial(self, sm):
        def worker(i):
            sm.set_initial_state(f"d{i}", "draft", now=float(i))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert sm.stats().total_docs == 50

    def test_concurrent_transitions(self, basic_sm):
        for i in range(20):
            basic_sm.set_initial_state(f"d{i}", "draft", now=1.0)

        def worker(i):
            basic_sm.transition(f"d{i}", "submit", now=2.0)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert basic_sm.docs_in_state("review") == sorted(f"d{i}" for i in range(20))

    def test_concurrent_define(self, sm):
        def worker(i):
            sm.define_transition(Transition(f"s{i}", f"t{i}", f"a{i}"))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(30)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(sm.list_transitions()) == 30

    def test_concurrent_guard_failures(self):
        sm = DocWorkflowStateV2()
        g = StateGuard(name="no", condition=lambda d, c: False)
        sm.define_transition(Transition("a", "b", "go", guards=[g]))
        for i in range(20):
            sm.set_initial_state(f"d{i}", "a")

        def worker(i):
            sm.transition(f"d{i}", "go")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert sm.stats().guard_failures == 20


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


class TestIntegration:
    def test_full_workflow(self):
        sm = DocWorkflowStateV2()
        sm.define_transition(Transition("draft", "review", "submit"))
        sm.define_transition(
            Transition(
                "review",
                "published",
                "approve",
                guards=[StateGuard(name="admin", condition=lambda d, c: c.get("admin"))],
            )
        )
        sm.define_transition(Transition("review", "draft", "reject"))
        sm.set_initial_state("doc1", "draft", entered_by="author", now=1.0)
        sm.transition("doc1", "submit", entered_by="author", now=2.0)
        assert sm.state_of("doc1") == "review"
        # Without admin context, approve is blocked.
        assert sm.transition("doc1", "approve", context={"admin": False}, now=3.0) is None
        assert sm.state_of("doc1") == "review"
        # With admin context, approve succeeds.
        rec = sm.transition("doc1", "approve", context={"admin": True}, now=4.0)
        assert rec is not None
        assert rec.state == "published"
        assert rec.transition_count == 2
        # History captures both prior states.
        history = sm.history_for("doc1")
        assert [r.state for r in history] == ["draft", "review"]
        s = sm.stats()
        assert s.total_docs == 1
        assert s.total_transitions == 3
        assert s.guard_failures == 1
        assert s.state_counts == {"published": 1}
