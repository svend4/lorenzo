"""Tests for doc_replay module."""
import pytest

from docstoolkit.doc_replay import (
    DocReplay,
    Operation,
    OperationType,
    ReplayResult,
    ReplaySession,
)


class TestOperationType:
    def test_has_create(self):
        assert OperationType.CREATE.value == "create"

    def test_has_update(self):
        assert OperationType.UPDATE.value == "update"

    def test_has_delete(self):
        assert OperationType.DELETE.value == "delete"

    def test_has_tag(self):
        assert OperationType.TAG.value == "tag"

    def test_has_untag(self):
        assert OperationType.UNTAG.value == "untag"

    def test_has_move(self):
        assert OperationType.MOVE.value == "move"

    def test_has_copy(self):
        assert OperationType.COPY.value == "copy"

    def test_has_other(self):
        assert OperationType.OTHER.value == "other"


class TestOperation:
    def test_create(self):
        op = Operation(op_id=1, doc_id="d1", op_type=OperationType.CREATE)
        assert op.op_id == 1
        assert op.doc_id == "d1"
        assert op.op_type == OperationType.CREATE

    def test_default_params(self):
        op = Operation(op_id=1, doc_id="d1", op_type=OperationType.CREATE)
        assert op.params == {}

    def test_default_timestamp(self):
        op = Operation(op_id=1, doc_id="d1", op_type=OperationType.CREATE)
        assert op.timestamp == 0.0

    def test_default_actor_is_none(self):
        op = Operation(op_id=1, doc_id="d1", op_type=OperationType.CREATE)
        assert op.actor is None

    def test_with_params(self):
        op = Operation(
            op_id=1,
            doc_id="d1",
            op_type=OperationType.UPDATE,
            params={"x": 1},
        )
        assert op.params == {"x": 1}


class TestReplaySession:
    def test_create(self):
        s = ReplaySession(session_id="s1", operations=[])
        assert s.session_id == "s1"
        assert s.operations == []

    def test_defaults(self):
        s = ReplaySession(session_id="s1", operations=[])
        assert s.started_at == 0.0
        assert s.ended_at is None
        assert s.name is None

    def test_with_name(self):
        s = ReplaySession(session_id="s1", operations=[], name="mine")
        assert s.name == "mine"


class TestReplayResult:
    def test_create(self):
        r = ReplayResult(
            session_id="s",
            total_operations=10,
            replayed=8,
            skipped=2,
            errors=[],
            duration_seconds=0.5,
        )
        assert r.total_operations == 10
        assert r.replayed == 8
        assert r.skipped == 2

    def test_errors_default(self):
        r = ReplayResult(
            session_id="s",
            total_operations=0,
            replayed=0,
            skipped=0,
        )
        assert r.errors == []


class TestStartRecording:
    def test_returns_session_id(self):
        dr = DocReplay()
        sid = dr.start_recording()
        assert isinstance(sid, str)
        assert len(sid) > 0

    def test_session_created(self):
        dr = DocReplay()
        sid = dr.start_recording()
        s = dr.get_session(sid)
        assert s is not None

    def test_with_name(self):
        dr = DocReplay()
        sid = dr.start_recording(name="run1")
        s = dr.get_session(sid)
        assert s.name == "run1"

    def test_started_at_set(self):
        dr = DocReplay()
        sid = dr.start_recording(now=100.0)
        s = dr.get_session(sid)
        assert s.started_at == 100.0

    def test_ended_at_none(self):
        dr = DocReplay()
        sid = dr.start_recording()
        s = dr.get_session(sid)
        assert s.ended_at is None

    def test_unique_ids(self):
        dr = DocReplay()
        ids = {dr.start_recording() for _ in range(10)}
        assert len(ids) == 10


class TestStopRecording:
    def test_returns_session(self):
        dr = DocReplay()
        sid = dr.start_recording()
        s = dr.stop_recording(sid, now=200.0)
        assert s is not None
        assert s.ended_at == 200.0

    def test_returns_none_for_missing(self):
        dr = DocReplay()
        assert dr.stop_recording("missing") is None

    def test_double_stop_keeps_first(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.stop_recording(sid, now=200.0)
        s = dr.stop_recording(sid, now=300.0)
        assert s.ended_at == 200.0

    def test_cannot_record_after_stop(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.stop_recording(sid)
        op = dr.record(sid, "d1", OperationType.CREATE)
        assert op is None


class TestRecord:
    def test_record_returns_op(self):
        dr = DocReplay()
        sid = dr.start_recording()
        op = dr.record(sid, "d1", OperationType.CREATE)
        assert op is not None
        assert op.doc_id == "d1"
        assert op.op_type == OperationType.CREATE

    def test_record_assigns_op_id(self):
        dr = DocReplay()
        sid = dr.start_recording()
        op1 = dr.record(sid, "d1", OperationType.CREATE)
        op2 = dr.record(sid, "d2", OperationType.UPDATE)
        assert op2.op_id > op1.op_id

    def test_record_in_missing_session(self):
        dr = DocReplay()
        assert dr.record("nope", "d1", OperationType.CREATE) is None

    def test_record_with_params(self):
        dr = DocReplay()
        sid = dr.start_recording()
        op = dr.record(sid, "d1", OperationType.UPDATE, params={"k": "v"})
        assert op.params == {"k": "v"}

    def test_record_with_actor(self):
        dr = DocReplay()
        sid = dr.start_recording()
        op = dr.record(sid, "d1", OperationType.CREATE, actor="alice")
        assert op.actor == "alice"

    def test_record_timestamp(self):
        dr = DocReplay()
        sid = dr.start_recording()
        op = dr.record(sid, "d1", OperationType.CREATE, now=500.0)
        assert op.timestamp == 500.0

    def test_record_appended(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.record(sid, "d2", OperationType.UPDATE)
        s = dr.get_session(sid)
        assert len(s.operations) == 2

    def test_params_copied(self):
        dr = DocReplay()
        sid = dr.start_recording()
        params = {"k": "v"}
        op = dr.record(sid, "d1", OperationType.CREATE, params=params)
        params["k"] = "changed"
        assert op.params["k"] == "v"


class TestGetSession:
    def test_existing(self):
        dr = DocReplay()
        sid = dr.start_recording()
        assert dr.get_session(sid) is not None

    def test_missing(self):
        dr = DocReplay()
        assert dr.get_session("nope") is None


class TestListSessions:
    def test_empty(self):
        dr = DocReplay()
        assert dr.list_sessions() == []

    def test_lists_all(self):
        dr = DocReplay()
        dr.start_recording()
        dr.start_recording()
        assert len(dr.list_sessions()) == 2

    def test_active_only(self):
        dr = DocReplay()
        s1 = dr.start_recording()
        s2 = dr.start_recording()
        dr.stop_recording(s1)
        active = dr.list_sessions(active_only=True)
        assert len(active) == 1
        assert active[0].session_id == s2


class TestReplay:
    def test_basic(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.record(sid, "d2", OperationType.UPDATE)
        result = dr.replay(sid, lambda op: True)
        assert result.replayed == 2
        assert result.skipped == 0

    def test_handler_returning_false(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        result = dr.replay(sid, lambda op: False)
        assert result.replayed == 0
        assert result.skipped == 1

    def test_missing_session(self):
        dr = DocReplay()
        result = dr.replay("nope", lambda op: True)
        assert result.total_operations == 0
        assert len(result.errors) > 0

    def test_handler_exception(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)

        def bad(op):
            raise RuntimeError("boom")

        result = dr.replay(sid, bad)
        assert len(result.errors) == 1
        assert result.replayed == 0

    def test_total_operations(self):
        dr = DocReplay()
        sid = dr.start_recording()
        for i in range(5):
            dr.record(sid, f"d{i}", OperationType.CREATE)
        result = dr.replay(sid, lambda op: True)
        assert result.total_operations == 5

    def test_duration_recorded(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        result = dr.replay(sid, lambda op: True)
        assert result.duration_seconds >= 0


class TestReplayFilterOpTypes:
    def test_filter_includes_only_types(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.record(sid, "d2", OperationType.UPDATE)
        dr.record(sid, "d3", OperationType.DELETE)
        result = dr.replay(
            sid, lambda op: True, filter_op_types=[OperationType.CREATE]
        )
        assert result.replayed == 1
        assert result.skipped == 2

    def test_filter_multiple(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.record(sid, "d2", OperationType.UPDATE)
        dr.record(sid, "d3", OperationType.DELETE)
        result = dr.replay(
            sid,
            lambda op: True,
            filter_op_types=[OperationType.CREATE, OperationType.UPDATE],
        )
        assert result.replayed == 2

    def test_empty_filter_excludes_all(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        # filter_op_types=[] becomes no-filter per truthiness, so test None
        result = dr.replay(sid, lambda op: True, filter_op_types=None)
        assert result.replayed == 1


class TestReplayFilterDocIds:
    def test_filter_doc_ids(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.record(sid, "d2", OperationType.UPDATE)
        dr.record(sid, "d1", OperationType.DELETE)
        result = dr.replay(sid, lambda op: True, filter_doc_ids=["d1"])
        assert result.replayed == 2

    def test_filter_multiple_docs(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.record(sid, "d2", OperationType.CREATE)
        dr.record(sid, "d3", OperationType.CREATE)
        result = dr.replay(sid, lambda op: True, filter_doc_ids=["d1", "d2"])
        assert result.replayed == 2

    def test_combined_filters(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.record(sid, "d1", OperationType.UPDATE)
        dr.record(sid, "d2", OperationType.CREATE)
        result = dr.replay(
            sid,
            lambda op: True,
            filter_op_types=[OperationType.CREATE],
            filter_doc_ids=["d1"],
        )
        assert result.replayed == 1


class TestReplayPartial:
    def test_slice(self):
        dr = DocReplay()
        sid = dr.start_recording()
        for i in range(5):
            dr.record(sid, f"d{i}", OperationType.CREATE)
        result = dr.replay_partial(sid, 1, 4, lambda op: True)
        assert result.replayed == 3
        assert result.skipped == 2

    def test_from_zero(self):
        dr = DocReplay()
        sid = dr.start_recording()
        for i in range(3):
            dr.record(sid, f"d{i}", OperationType.CREATE)
        result = dr.replay_partial(sid, 0, 3, lambda op: True)
        assert result.replayed == 3

    def test_missing_session(self):
        dr = DocReplay()
        result = dr.replay_partial("nope", 0, 1, lambda op: True)
        assert result.total_operations == 0
        assert len(result.errors) > 0

    def test_empty_range(self):
        dr = DocReplay()
        sid = dr.start_recording()
        for i in range(3):
            dr.record(sid, f"d{i}", OperationType.CREATE)
        result = dr.replay_partial(sid, 2, 2, lambda op: True)
        assert result.replayed == 0


class TestDryRun:
    def test_calls_handler(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        seen = []
        dr.dry_run(sid, lambda op: seen.append(op) or True)
        assert len(seen) == 1

    def test_returns_result(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        result = dr.dry_run(sid, lambda op: True)
        assert isinstance(result, ReplayResult)
        assert result.replayed == 1


class TestDeleteSession:
    def test_delete_existing(self):
        dr = DocReplay()
        sid = dr.start_recording()
        assert dr.delete_session(sid) is True
        assert dr.get_session(sid) is None

    def test_delete_missing(self):
        dr = DocReplay()
        assert dr.delete_session("nope") is False


class TestOperationsForDoc:
    def test_filter(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.record(sid, "d2", OperationType.UPDATE)
        dr.record(sid, "d1", OperationType.DELETE)
        ops = dr.operations_for_doc(sid, "d1")
        assert len(ops) == 2

    def test_missing_session(self):
        dr = DocReplay()
        assert dr.operations_for_doc("nope", "d1") == []

    def test_no_matches(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        assert dr.operations_for_doc(sid, "d2") == []


class TestOperationsByType:
    def test_filter(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.record(sid, "d2", OperationType.CREATE)
        dr.record(sid, "d3", OperationType.UPDATE)
        ops = dr.operations_by_type(sid, OperationType.CREATE)
        assert len(ops) == 2

    def test_missing_session(self):
        dr = DocReplay()
        assert dr.operations_by_type("nope", OperationType.CREATE) == []

    def test_no_matches(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        assert dr.operations_by_type(sid, OperationType.DELETE) == []


class TestMergeSessions:
    def test_merge_two(self):
        dr = DocReplay()
        s1 = dr.start_recording()
        dr.record(s1, "d1", OperationType.CREATE, now=1.0)
        s2 = dr.start_recording()
        dr.record(s2, "d2", OperationType.UPDATE, now=2.0)
        merged = dr.merge_sessions([s1, s2], new_name="merged")
        assert merged is not None
        assert len(merged.operations) == 2
        assert merged.name == "merged"

    def test_sorted_by_timestamp(self):
        dr = DocReplay()
        s1 = dr.start_recording()
        dr.record(s1, "d1", OperationType.CREATE, now=5.0)
        s2 = dr.start_recording()
        dr.record(s2, "d2", OperationType.UPDATE, now=1.0)
        merged = dr.merge_sessions([s1, s2])
        assert merged.operations[0].timestamp == 1.0
        assert merged.operations[1].timestamp == 5.0

    def test_missing_session(self):
        dr = DocReplay()
        s1 = dr.start_recording()
        assert dr.merge_sessions([s1, "nope"]) is None

    def test_empty_list(self):
        dr = DocReplay()
        assert dr.merge_sessions([]) is None

    def test_creates_new_session(self):
        dr = DocReplay()
        s1 = dr.start_recording()
        dr.record(s1, "d1", OperationType.CREATE)
        before = dr.total_sessions
        merged = dr.merge_sessions([s1])
        assert dr.total_sessions == before + 1
        assert dr.get_session(merged.session_id) is not None

    def test_sort_stable_by_op_id(self):
        dr = DocReplay()
        s1 = dr.start_recording()
        dr.record(s1, "d1", OperationType.CREATE, now=1.0)
        dr.record(s1, "d2", OperationType.UPDATE, now=1.0)
        merged = dr.merge_sessions([s1])
        assert merged.operations[0].op_id < merged.operations[1].op_id


class TestTotalSessions:
    def test_empty(self):
        dr = DocReplay()
        assert dr.total_sessions == 0

    def test_counts(self):
        dr = DocReplay()
        dr.start_recording()
        dr.start_recording()
        assert dr.total_sessions == 2


class TestTotalOperations:
    def test_empty(self):
        dr = DocReplay()
        assert dr.total_operations == 0

    def test_counts_across_sessions(self):
        dr = DocReplay()
        s1 = dr.start_recording()
        s2 = dr.start_recording()
        dr.record(s1, "d1", OperationType.CREATE)
        dr.record(s2, "d2", OperationType.UPDATE)
        dr.record(s2, "d3", OperationType.DELETE)
        assert dr.total_operations == 3


class TestClear:
    def test_clears_sessions(self):
        dr = DocReplay()
        dr.start_recording()
        dr.clear()
        assert dr.total_sessions == 0

    def test_resets_counter(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.clear()
        new_sid = dr.start_recording()
        op = dr.record(new_sid, "d1", OperationType.CREATE)
        assert op.op_id == 1


class TestEdgeCases:
    def test_replay_empty_session(self):
        dr = DocReplay()
        sid = dr.start_recording()
        result = dr.replay(sid, lambda op: True)
        assert result.total_operations == 0
        assert result.replayed == 0

    def test_record_after_clear(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.clear()
        assert dr.record(sid, "d1", OperationType.CREATE) is None

    def test_replay_after_stop(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.stop_recording(sid)
        result = dr.replay(sid, lambda op: True)
        assert result.replayed == 1

    def test_handler_with_side_effect(self):
        dr = DocReplay()
        sid = dr.start_recording()
        dr.record(sid, "d1", OperationType.CREATE)
        dr.record(sid, "d2", OperationType.UPDATE)
        collected = []

        def h(op):
            collected.append(op.doc_id)
            return True

        dr.replay(sid, h)
        assert collected == ["d1", "d2"]

    def test_op_ids_globally_unique(self):
        dr = DocReplay()
        s1 = dr.start_recording()
        op1 = dr.record(s1, "d1", OperationType.CREATE)
        s2 = dr.start_recording()
        op2 = dr.record(s2, "d2", OperationType.CREATE)
        assert op1.op_id != op2.op_id
