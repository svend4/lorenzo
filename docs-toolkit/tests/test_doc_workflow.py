"""Tests for docstoolkit.doc_workflow (E192)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_workflow import (
    DocState,
    DocWorkflow,
    Transition,
    TransitionResult,
    WorkflowDefinition,
    WorkflowStatus,
)


def _basic_definition() -> WorkflowDefinition:
    """Standard draft -> review -> approved -> published flow."""
    d = WorkflowDefinition("article")
    d.add_transition(WorkflowStatus.DRAFT, WorkflowStatus.REVIEW)
    d.add_transition(
        WorkflowStatus.REVIEW,
        WorkflowStatus.APPROVED,
        required_role="editor",
    )
    d.add_transition(
        WorkflowStatus.APPROVED,
        WorkflowStatus.PUBLISHED,
        required_role="publisher",
    )
    d.add_transition(WorkflowStatus.REVIEW, WorkflowStatus.REJECTED)
    d.add_transition(WorkflowStatus.DRAFT, WorkflowStatus.ARCHIVED)
    return d


class TestWorkflowStatus:
    def test_all_statuses_exist(self):
        assert WorkflowStatus.DRAFT
        assert WorkflowStatus.REVIEW
        assert WorkflowStatus.APPROVED
        assert WorkflowStatus.PUBLISHED
        assert WorkflowStatus.REJECTED
        assert WorkflowStatus.ARCHIVED

    def test_status_count(self):
        assert len(list(WorkflowStatus)) == 6

    def test_status_value(self):
        assert WorkflowStatus.DRAFT.value == "draft"

    def test_statuses_are_unique(self):
        values = {s.value for s in WorkflowStatus}
        assert len(values) == 6


class TestTransition:
    def test_create_minimal(self):
        t = Transition(
            from_status=WorkflowStatus.DRAFT,
            to_status=WorkflowStatus.REVIEW,
        )
        assert t.from_status == WorkflowStatus.DRAFT
        assert t.to_status == WorkflowStatus.REVIEW
        assert t.required_role is None
        assert t.condition is None

    def test_create_with_role(self):
        t = Transition(
            from_status=WorkflowStatus.REVIEW,
            to_status=WorkflowStatus.APPROVED,
            required_role="editor",
        )
        assert t.required_role == "editor"

    def test_create_with_condition(self):
        fn = lambda s: True  # noqa: E731
        t = Transition(
            from_status=WorkflowStatus.DRAFT,
            to_status=WorkflowStatus.REVIEW,
            condition=fn,
        )
        assert t.condition is fn


class TestDocState:
    def test_create_minimal(self):
        s = DocState(doc_id="d1", status=WorkflowStatus.DRAFT)
        assert s.doc_id == "d1"
        assert s.status == WorkflowStatus.DRAFT
        assert s.assigned_to is None
        assert s.history == []
        assert s.metadata == {}
        assert s.created_at == 0.0
        assert s.updated_at == 0.0

    def test_create_full(self):
        s = DocState(
            doc_id="d1",
            status=WorkflowStatus.REVIEW,
            assigned_to="alice",
            history=[{"from": WorkflowStatus.DRAFT}],
            metadata={"k": "v"},
            created_at=1.0,
            updated_at=2.0,
        )
        assert s.assigned_to == "alice"
        assert len(s.history) == 1
        assert s.metadata == {"k": "v"}
        assert s.created_at == 1.0
        assert s.updated_at == 2.0


class TestTransitionResult:
    def test_success_result(self):
        r = TransitionResult(
            success=True, new_status=WorkflowStatus.REVIEW, reason="ok"
        )
        assert r.success
        assert r.new_status == WorkflowStatus.REVIEW
        assert r.reason == "ok"

    def test_failure_result(self):
        r = TransitionResult(
            success=False, new_status=None, reason="invalid"
        )
        assert not r.success
        assert r.new_status is None


class TestWorkflowDefinition:
    def test_create(self):
        d = WorkflowDefinition("my-wf")
        assert d.name == "my-wf"

    def test_empty_definition_has_no_transitions(self):
        d = WorkflowDefinition("empty")
        assert d.allowed_transitions(WorkflowStatus.DRAFT) == []


class TestAddTransition:
    def test_add_returns_transition(self):
        d = WorkflowDefinition("x")
        t = d.add_transition(WorkflowStatus.DRAFT, WorkflowStatus.REVIEW)
        assert isinstance(t, Transition)
        assert t.from_status == WorkflowStatus.DRAFT
        assert t.to_status == WorkflowStatus.REVIEW

    def test_add_with_role(self):
        d = WorkflowDefinition("x")
        t = d.add_transition(
            WorkflowStatus.REVIEW,
            WorkflowStatus.APPROVED,
            required_role="editor",
        )
        assert t.required_role == "editor"

    def test_add_with_condition(self):
        d = WorkflowDefinition("x")
        cond = lambda s: True  # noqa: E731
        t = d.add_transition(
            WorkflowStatus.DRAFT,
            WorkflowStatus.REVIEW,
            condition=cond,
        )
        assert t.condition is cond

    def test_add_multiple(self):
        d = WorkflowDefinition("x")
        d.add_transition(WorkflowStatus.DRAFT, WorkflowStatus.REVIEW)
        d.add_transition(WorkflowStatus.REVIEW, WorkflowStatus.APPROVED)
        assert len(d.allowed_transitions(WorkflowStatus.DRAFT)) == 1
        assert len(d.allowed_transitions(WorkflowStatus.REVIEW)) == 1


class TestAllowedTransitions:
    def test_empty_when_none(self):
        d = WorkflowDefinition("x")
        assert d.allowed_transitions(WorkflowStatus.DRAFT) == []

    def test_returns_outgoing(self):
        d = _basic_definition()
        outgoing = d.allowed_transitions(WorkflowStatus.DRAFT)
        targets = {t.to_status for t in outgoing}
        assert targets == {WorkflowStatus.REVIEW, WorkflowStatus.ARCHIVED}

    def test_excludes_incoming(self):
        d = _basic_definition()
        outgoing = d.allowed_transitions(WorkflowStatus.APPROVED)
        for t in outgoing:
            assert t.from_status == WorkflowStatus.APPROVED


class TestIsValidTransition:
    def test_valid(self):
        d = _basic_definition()
        assert d.is_valid_transition(
            WorkflowStatus.DRAFT, WorkflowStatus.REVIEW
        )

    def test_invalid(self):
        d = _basic_definition()
        assert not d.is_valid_transition(
            WorkflowStatus.DRAFT, WorkflowStatus.PUBLISHED
        )

    def test_reverse_not_valid(self):
        d = _basic_definition()
        assert not d.is_valid_transition(
            WorkflowStatus.REVIEW, WorkflowStatus.DRAFT
        )


class TestTerminalStatuses:
    def test_set_contents(self):
        d = WorkflowDefinition("x")
        assert d.terminal_statuses() == {
            WorkflowStatus.PUBLISHED,
            WorkflowStatus.REJECTED,
            WorkflowStatus.ARCHIVED,
        }

    def test_returns_copy(self):
        d = WorkflowDefinition("x")
        s = d.terminal_statuses()
        s.add(WorkflowStatus.DRAFT)
        assert WorkflowStatus.DRAFT not in d.terminal_statuses()


class TestRegister:
    def test_register_default(self):
        wf = DocWorkflow(_basic_definition())
        s = wf.register("d1")
        assert s.doc_id == "d1"
        assert s.status == WorkflowStatus.DRAFT
        assert s.assigned_to is None

    def test_register_custom_status(self):
        wf = DocWorkflow(_basic_definition())
        s = wf.register("d1", initial_status=WorkflowStatus.REVIEW)
        assert s.status == WorkflowStatus.REVIEW

    def test_register_assigned(self):
        wf = DocWorkflow(_basic_definition())
        s = wf.register("d1", assigned_to="alice", now=1.0)
        assert s.assigned_to == "alice"
        assert s.created_at == 1.0
        assert s.updated_at == 1.0

    def test_register_idempotent(self):
        wf = DocWorkflow(_basic_definition())
        s1 = wf.register("d1")
        s2 = wf.register("d1")
        assert s1 is s2
        assert wf.total_docs == 1


class TestGet:
    def test_get_existing(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        assert wf.get("d1") is not None

    def test_get_unknown(self):
        wf = DocWorkflow(_basic_definition())
        assert wf.get("nope") is None


class TestTransitionSuccess:
    def test_simple_transition(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        r = wf.transition("d1", WorkflowStatus.REVIEW, actor="alice")
        assert r.success
        assert r.new_status == WorkflowStatus.REVIEW
        assert r.reason == "ok"

    def test_status_updated(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="alice")
        assert wf.get("d1").status == WorkflowStatus.REVIEW

    def test_history_recorded(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="alice", now=5.0)
        h = wf.history("d1")
        assert len(h) == 1
        assert h[0]["from"] == WorkflowStatus.DRAFT
        assert h[0]["to"] == WorkflowStatus.REVIEW
        assert h[0]["actor"] == "alice"
        assert h[0]["timestamp"] == 5.0

    def test_chain_transitions(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        wf.transition(
            "d1",
            WorkflowStatus.APPROVED,
            actor="b",
            user_role="editor",
        )
        wf.transition(
            "d1",
            WorkflowStatus.PUBLISHED,
            actor="c",
            user_role="publisher",
        )
        assert wf.get("d1").status == WorkflowStatus.PUBLISHED


class TestTransitionInvalidFrom:
    def test_unknown_doc(self):
        wf = DocWorkflow(_basic_definition())
        r = wf.transition("missing", WorkflowStatus.REVIEW, actor="a")
        assert not r.success
        assert r.reason == "unknown_doc"
        assert r.new_status is None

    def test_invalid_transition(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        r = wf.transition("d1", WorkflowStatus.PUBLISHED, actor="a")
        assert not r.success
        assert r.reason == "invalid_transition"
        assert r.new_status == WorkflowStatus.DRAFT

    def test_no_status_change_on_invalid(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.PUBLISHED, actor="a")
        assert wf.get("d1").status == WorkflowStatus.DRAFT
        assert wf.history("d1") == []


class TestTransitionRoleRequired:
    def test_role_required_missing(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        r = wf.transition("d1", WorkflowStatus.APPROVED, actor="b")
        assert not r.success
        assert r.reason == "role_mismatch"

    def test_role_required_wrong(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        r = wf.transition(
            "d1", WorkflowStatus.APPROVED, actor="b", user_role="viewer"
        )
        assert not r.success
        assert r.reason == "role_mismatch"

    def test_role_required_correct(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        r = wf.transition(
            "d1", WorkflowStatus.APPROVED, actor="b", user_role="editor"
        )
        assert r.success

    def test_role_recorded_in_history(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        wf.transition(
            "d1", WorkflowStatus.APPROVED, actor="b", user_role="editor"
        )
        h = wf.history("d1")
        assert h[1]["role"] == "editor"


class TestTransitionConditionFails:
    def test_condition_false_blocks(self):
        d = WorkflowDefinition("x")
        d.add_transition(
            WorkflowStatus.DRAFT,
            WorkflowStatus.REVIEW,
            condition=lambda s: False,
        )
        wf = DocWorkflow(d)
        wf.register("d1")
        r = wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        assert not r.success
        assert r.reason == "condition_failed"

    def test_condition_true_allows(self):
        d = WorkflowDefinition("x")
        d.add_transition(
            WorkflowStatus.DRAFT,
            WorkflowStatus.REVIEW,
            condition=lambda s: True,
        )
        wf = DocWorkflow(d)
        wf.register("d1")
        r = wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        assert r.success

    def test_condition_sees_state(self):
        d = WorkflowDefinition("x")
        d.add_transition(
            WorkflowStatus.DRAFT,
            WorkflowStatus.REVIEW,
            condition=lambda s: s.metadata.get("ready") is True,
        )
        wf = DocWorkflow(d)
        wf.register("d1")
        r = wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        assert not r.success
        wf.metadata_update("d1", {"ready": True})
        r2 = wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        assert r2.success

    def test_condition_exception_blocks(self):
        def bad(_):
            raise RuntimeError("boom")

        d = WorkflowDefinition("x")
        d.add_transition(
            WorkflowStatus.DRAFT, WorkflowStatus.REVIEW, condition=bad
        )
        wf = DocWorkflow(d)
        wf.register("d1")
        r = wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        assert not r.success
        assert r.reason == "condition_failed"


class TestAssign:
    def test_assign_existing(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        assert wf.assign("d1", "alice") is True
        assert wf.get("d1").assigned_to == "alice"

    def test_assign_unknown(self):
        wf = DocWorkflow(_basic_definition())
        assert wf.assign("nope", "alice") is False

    def test_assign_overwrite(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1", assigned_to="alice")
        wf.assign("d1", "bob")
        assert wf.get("d1").assigned_to == "bob"


class TestMetadataUpdate:
    def test_update_existing(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        assert wf.metadata_update("d1", {"k": "v"}) is True
        assert wf.get("d1").metadata == {"k": "v"}

    def test_update_unknown(self):
        wf = DocWorkflow(_basic_definition())
        assert wf.metadata_update("nope", {"k": "v"}) is False

    def test_update_merges(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.metadata_update("d1", {"a": 1})
        wf.metadata_update("d1", {"b": 2})
        assert wf.get("d1").metadata == {"a": 1, "b": 2}

    def test_update_overwrites_keys(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.metadata_update("d1", {"a": 1})
        wf.metadata_update("d1", {"a": 2})
        assert wf.get("d1").metadata["a"] == 2


class TestHistory:
    def test_empty_initially(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        assert wf.history("d1") == []

    def test_returns_copy(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        h = wf.history("d1")
        h.append({"fake": True})
        assert len(wf.history("d1")) == 1

    def test_unknown_returns_empty(self):
        wf = DocWorkflow(_basic_definition())
        assert wf.history("nope") == []

    def test_accumulates(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        wf.transition(
            "d1", WorkflowStatus.APPROVED, actor="b", user_role="editor"
        )
        assert len(wf.history("d1")) == 2


class TestDocsInStatus:
    def test_empty(self):
        wf = DocWorkflow(_basic_definition())
        assert wf.docs_in_status(WorkflowStatus.DRAFT) == []

    def test_filtered(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.register("d2")
        wf.register("d3")
        wf.transition("d2", WorkflowStatus.REVIEW, actor="a")
        drafts = wf.docs_in_status(WorkflowStatus.DRAFT)
        assert len(drafts) == 2
        ids = {s.doc_id for s in drafts}
        assert ids == {"d1", "d3"}

    def test_review_status(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        rs = wf.docs_in_status(WorkflowStatus.REVIEW)
        assert len(rs) == 1
        assert rs[0].doc_id == "d1"


class TestDocsAssignedTo:
    def test_empty(self):
        wf = DocWorkflow(_basic_definition())
        assert wf.docs_assigned_to("alice") == []

    def test_filtered(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1", assigned_to="alice")
        wf.register("d2", assigned_to="bob")
        wf.register("d3", assigned_to="alice")
        rs = wf.docs_assigned_to("alice")
        ids = {s.doc_id for s in rs}
        assert ids == {"d1", "d3"}

    def test_after_assign(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        assert wf.docs_assigned_to("alice") == []
        wf.assign("d1", "alice")
        assert len(wf.docs_assigned_to("alice")) == 1


class TestIsTerminal:
    def test_initial_not_terminal(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        assert wf.is_terminal("d1") is False

    def test_published_is_terminal(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        wf.transition(
            "d1", WorkflowStatus.APPROVED, actor="b", user_role="editor"
        )
        wf.transition(
            "d1",
            WorkflowStatus.PUBLISHED,
            actor="c",
            user_role="publisher",
        )
        assert wf.is_terminal("d1") is True

    def test_rejected_terminal(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.REVIEW, actor="a")
        wf.transition("d1", WorkflowStatus.REJECTED, actor="b")
        assert wf.is_terminal("d1") is True

    def test_archived_terminal(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.ARCHIVED, actor="a")
        assert wf.is_terminal("d1") is True

    def test_unknown_not_terminal(self):
        wf = DocWorkflow(_basic_definition())
        assert wf.is_terminal("nope") is False


class TestCountByStatus:
    def test_empty(self):
        wf = DocWorkflow(_basic_definition())
        counts = wf.count_by_status()
        for s in WorkflowStatus:
            assert counts[s] == 0

    def test_all_statuses_present(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        counts = wf.count_by_status()
        assert set(counts.keys()) == set(WorkflowStatus)

    def test_counts(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.register("d2")
        wf.register("d3")
        wf.transition("d2", WorkflowStatus.REVIEW, actor="a")
        wf.transition("d3", WorkflowStatus.ARCHIVED, actor="a")
        counts = wf.count_by_status()
        assert counts[WorkflowStatus.DRAFT] == 1
        assert counts[WorkflowStatus.REVIEW] == 1
        assert counts[WorkflowStatus.ARCHIVED] == 1
        assert counts[WorkflowStatus.PUBLISHED] == 0


class TestRemove:
    def test_remove_existing(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        assert wf.remove("d1") is True
        assert wf.get("d1") is None

    def test_remove_unknown(self):
        wf = DocWorkflow(_basic_definition())
        assert wf.remove("nope") is False

    def test_remove_decrements_total(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.register("d2")
        assert wf.total_docs == 2
        wf.remove("d1")
        assert wf.total_docs == 1


class TestTotalDocs:
    def test_empty(self):
        wf = DocWorkflow(_basic_definition())
        assert wf.total_docs == 0

    def test_after_register(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.register("d2")
        assert wf.total_docs == 2

    def test_after_clear(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.clear()
        assert wf.total_docs == 0


class TestClear:
    def test_clear_empty(self):
        wf = DocWorkflow(_basic_definition())
        wf.clear()
        assert wf.total_docs == 0

    def test_clear_populated(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.register("d2")
        wf.clear()
        assert wf.total_docs == 0
        assert wf.get("d1") is None


class TestEdgeCases:
    def test_transition_unknown_doc(self):
        wf = DocWorkflow(_basic_definition())
        r = wf.transition("missing", WorkflowStatus.REVIEW, actor="a")
        assert r.reason == "unknown_doc"

    def test_terminal_blocks_outgoing(self):
        wf = DocWorkflow(_basic_definition())
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.ARCHIVED, actor="a")
        # try moving out of ARCHIVED — no such transition; should be terminal
        r = wf.transition("d1", WorkflowStatus.DRAFT, actor="a")
        assert not r.success
        assert r.reason == "terminal_status"

    def test_terminal_blocks_even_if_listed(self):
        d = WorkflowDefinition("x")
        # Even if user defines a transition out of a terminal status,
        # DocWorkflow refuses to leave terminal.
        d.add_transition(WorkflowStatus.DRAFT, WorkflowStatus.PUBLISHED)
        d.add_transition(WorkflowStatus.PUBLISHED, WorkflowStatus.DRAFT)
        wf = DocWorkflow(d)
        wf.register("d1")
        wf.transition("d1", WorkflowStatus.PUBLISHED, actor="a")
        r = wf.transition("d1", WorkflowStatus.DRAFT, actor="a")
        assert not r.success
        assert r.reason == "terminal_status"

    def test_history_unknown_doc(self):
        wf = DocWorkflow(_basic_definition())
        assert wf.history("nope") == []

    def test_count_includes_zero_buckets(self):
        wf = DocWorkflow(_basic_definition())
        counts = wf.count_by_status()
        assert len(counts) == 6

    def test_thread_safety_smoke(self):
        import threading as _t

        wf = DocWorkflow(_basic_definition())
        for i in range(20):
            wf.register(f"d{i}")

        def worker(i):
            wf.transition(f"d{i}", WorkflowStatus.REVIEW, actor="a")

        threads = [_t.Thread(target=worker, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert wf.total_docs == 20
        review_docs = wf.docs_in_status(WorkflowStatus.REVIEW)
        assert len(review_docs) == 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
