"""Tests for docstoolkit.dlq.replay — DLQ replay API with idempotency."""
from __future__ import annotations

import pytest

from docstoolkit.dlq import (
    DeadLetterItem, DeadLetterQueue, FailureReason,
    ReplayFilter, ReplayResult, ReplayEngine, replay_dlq,
)
from docstoolkit.dlq.replay import IdempotencyStore, _infer_job_type


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _item(job_id, payload='{}', reason=FailureReason.ERROR, tags=None):
    return DeadLetterItem(
        job_id=job_id,
        payload=payload,
        reason=reason,
        tags=tags or [],
    )


def _filled_dlq(*job_ids, reason=FailureReason.ERROR, tags=None):
    dlq = DeadLetterQueue()
    for jid in job_ids:
        dlq.push(_item(jid, reason=reason, tags=tags or []))
    return dlq


# ---------------------------------------------------------------------------
# ReplayFilter
# ---------------------------------------------------------------------------

class TestReplayFilter:
    def test_empty_filter_matches_any(self):
        flt = ReplayFilter()
        item = _item("job-1")
        assert flt.matches(item) is True

    def test_job_ids_allowlist(self):
        flt = ReplayFilter(job_ids=["job-1", "job-2"])
        assert flt.matches(_item("job-1")) is True
        assert flt.matches(_item("job-3")) is False

    def test_tags_all_required(self):
        flt = ReplayFilter(tags=["urgent", "retryable"])
        assert flt.matches(_item("x", tags=["urgent", "retryable", "other"])) is True
        assert flt.matches(_item("x", tags=["urgent"])) is False
        assert flt.matches(_item("x", tags=[])) is False

    def test_reason_filter(self):
        flt = ReplayFilter(reason=FailureReason.TIMEOUT)
        assert flt.matches(_item("x", reason=FailureReason.TIMEOUT)) is True
        assert flt.matches(_item("x", reason=FailureReason.ERROR)) is False

    def test_job_type_prefix(self):
        flt = ReplayFilter(job_type="email")
        assert flt.matches(_item("email:abc")) is True
        assert flt.matches(_item("sms:xyz")) is False
        assert flt.matches(_item("nocolon")) is False

    def test_after_ts_inclusive(self):
        item = _item("x")
        item.first_failure_ts = "2024-01-15T10:00:00"
        flt = ReplayFilter(after_ts="2024-01-15T10:00:00")
        assert flt.matches(item) is True

    def test_after_ts_excludes_older(self):
        item = _item("x")
        item.first_failure_ts = "2024-01-10T00:00:00"
        flt = ReplayFilter(after_ts="2024-01-15T00:00:00")
        assert flt.matches(item) is False

    def test_before_ts_inclusive(self):
        item = _item("x")
        item.first_failure_ts = "2024-01-15T10:00:00"
        flt = ReplayFilter(before_ts="2024-01-15T10:00:00")
        assert flt.matches(item) is True

    def test_before_ts_excludes_newer(self):
        item = _item("x")
        item.first_failure_ts = "2024-01-20T00:00:00"
        flt = ReplayFilter(before_ts="2024-01-15T00:00:00")
        assert flt.matches(item) is False

    def test_conditions_are_anded(self):
        flt = ReplayFilter(job_ids=["email:x"], job_type="email")
        assert flt.matches(_item("email:x")) is True
        assert flt.matches(_item("email:y")) is False  # not in job_ids


# ---------------------------------------------------------------------------
# ReplayResult
# ---------------------------------------------------------------------------

class TestReplayResult:
    def test_total_sums_all_lists(self):
        r = ReplayResult(replayed=["a", "b"], skipped=["c"], errors=["d"])
        assert r.total == 4

    def test_empty_result(self):
        r = ReplayResult()
        assert r.total == 0


# ---------------------------------------------------------------------------
# IdempotencyStore
# ---------------------------------------------------------------------------

class TestIdempotencyStore:
    def test_not_replayed_initially(self):
        store = IdempotencyStore()
        assert store.has_been_replayed("job-1") is False

    def test_mark_and_check(self):
        store = IdempotencyStore()
        store.mark_replayed("job-1")
        assert store.has_been_replayed("job-1") is True

    def test_replay_count_zero_initially(self):
        store = IdempotencyStore()
        assert store.replay_count("job-1") == 0

    def test_replay_count_increments(self):
        store = IdempotencyStore()
        store.mark_replayed("job-1")
        store.mark_replayed("job-1")
        assert store.replay_count("job-1") == 2

    def test_budget_none_by_default(self):
        store = IdempotencyStore()
        assert store.budget_for("email") is None

    def test_set_and_get_budget(self):
        store = IdempotencyStore()
        store.set_budget("email", 3)
        assert store.budget_for("email") == 3

    def test_budget_overwrite(self):
        store = IdempotencyStore()
        store.set_budget("email", 3)
        store.set_budget("email", 7)
        assert store.budget_for("email") == 7


# ---------------------------------------------------------------------------
# ReplayEngine — dry-run mode
# ---------------------------------------------------------------------------

class TestReplayEngineDryRun:
    def test_dry_run_does_not_call_handler(self):
        dlq = _filled_dlq("job-1", "job-2")
        called = []
        engine = ReplayEngine(dlq)
        engine.replay(lambda jid, p: called.append(jid), mode="dry-run")
        assert called == []

    def test_dry_run_all_appear_in_skipped(self):
        dlq = _filled_dlq("job-1", "job-2", "job-3")
        engine = ReplayEngine(dlq)
        result = engine.replay(lambda jid, p: None, mode="dry-run")
        assert set(result.skipped) == {"job-1", "job-2", "job-3"}
        assert result.replayed == []

    def test_dry_run_does_not_resolve_items(self):
        dlq = _filled_dlq("job-1")
        engine = ReplayEngine(dlq)
        engine.replay(lambda jid, p: None, mode="dry-run")
        assert dlq.stats()["pending"] == 1

    def test_invalid_mode_raises(self):
        dlq = _filled_dlq("job-1")
        engine = ReplayEngine(dlq)
        with pytest.raises(ValueError, match="mode"):
            engine.replay(lambda jid, p: None, mode="execute")


# ---------------------------------------------------------------------------
# ReplayEngine — apply mode
# ---------------------------------------------------------------------------

class TestReplayEngineApply:
    def test_apply_calls_handler(self):
        dlq = _filled_dlq("job-1", "job-2")
        called = []
        engine = ReplayEngine(dlq)
        engine.replay(lambda jid, p: called.append(jid), mode="apply")
        assert set(called) == {"job-1", "job-2"}

    def test_apply_resolves_items(self):
        dlq = _filled_dlq("job-1", "job-2")
        engine = ReplayEngine(dlq)
        engine.replay(lambda jid, p: None, mode="apply")
        assert dlq.stats()["pending"] == 0
        assert dlq.stats()["resolved"] == 2

    def test_apply_marks_replayed_in_result(self):
        dlq = _filled_dlq("job-1", "job-2")
        engine = ReplayEngine(dlq)
        result = engine.replay(lambda jid, p: None, mode="apply")
        assert set(result.replayed) == {"job-1", "job-2"}
        assert result.errors == []

    def test_apply_handler_error_goes_to_errors(self):
        dlq = _filled_dlq("job-bad")

        def bad_handler(jid, p):
            raise RuntimeError("simulated failure")

        engine = ReplayEngine(dlq)
        result = engine.replay(bad_handler, mode="apply")
        assert "job-bad" in result.errors
        assert "job-bad" not in result.replayed

    def test_apply_handler_error_increments_attempt(self):
        dlq = _filled_dlq("job-bad")
        dlq_item = dlq.get("job-bad")
        initial = dlq_item.attempt_count

        def bad_handler(jid, p):
            raise RuntimeError("fail")

        engine = ReplayEngine(dlq)
        engine.replay(bad_handler, mode="apply")
        updated = dlq.get("job-bad")
        assert updated.attempt_count == initial + 1


# ---------------------------------------------------------------------------
# Idempotency guard — double-execution prevention
# ---------------------------------------------------------------------------

class TestIdempotencyGuard:
    def test_second_replay_call_skips_already_replayed(self):
        dlq = _filled_dlq("job-1")
        calls = []
        engine = ReplayEngine(dlq)

        # First apply call
        engine.replay(lambda jid, p: calls.append(jid), mode="apply")
        # Second apply call — job already resolved AND in idempotency store
        engine.replay(lambda jid, p: calls.append(jid), mode="apply")

        # handler should have been called exactly once
        assert calls.count("job-1") == 1

    def test_resolved_items_not_in_pending(self):
        dlq = _filled_dlq("job-1")
        engine = ReplayEngine(dlq)
        engine.replay(lambda jid, p: None, mode="apply")
        # list_pending returns empty now
        assert dlq.list_pending() == []


# ---------------------------------------------------------------------------
# Per-job-type retry budget
# ---------------------------------------------------------------------------

class TestRetryBudget:
    def test_budget_exceeded_skips_item(self):
        dlq = _filled_dlq("email:001", "email:002")
        calls = []
        engine = ReplayEngine(dlq, default_max_replays=1)

        # First call uses up budget
        engine.replay(lambda jid, p: calls.append(jid), mode="apply")
        calls_after_first = list(calls)

        # Manually re-add the jobs as unresolved to simulate new failures
        dlq2 = DeadLetterQueue()
        for jid in ("email:003", "email:004"):
            dlq2.push(_item(jid))

        engine2 = ReplayEngine(dlq2, default_max_replays=0)
        result = engine2.replay(lambda jid, p: None, mode="apply")
        assert set(result.skipped) == {"email:003", "email:004"}

    def test_job_type_budget_overrides_default(self):
        dlq = _filled_dlq("sms:x")
        engine = ReplayEngine(dlq, default_max_replays=5)
        engine.set_budget("sms", 0)  # block sms type completely

        result = engine.replay(lambda jid, p: None, mode="apply")
        assert "sms:x" in result.skipped
        assert "sms:x" not in result.replayed


# ---------------------------------------------------------------------------
# Filtering + apply combination
# ---------------------------------------------------------------------------

class TestReplayWithFilter:
    def test_filter_by_reason_only_replays_matching(self):
        dlq = DeadLetterQueue()
        dlq.push(_item("timeout:1", reason=FailureReason.TIMEOUT))
        dlq.push(_item("error:2", reason=FailureReason.ERROR))

        called = []
        engine = ReplayEngine(dlq)
        engine.replay(
            lambda jid, p: called.append(jid),
            filter=ReplayFilter(reason=FailureReason.TIMEOUT),
            mode="apply",
        )
        assert called == ["timeout:1"]

    def test_filter_by_tags(self):
        dlq = DeadLetterQueue()
        dlq.push(_item("job-A", tags=["urgent"]))
        dlq.push(_item("job-B", tags=["low-priority"]))

        called = []
        engine = ReplayEngine(dlq)
        engine.replay(
            lambda jid, p: called.append(jid),
            filter=ReplayFilter(tags=["urgent"]),
            mode="apply",
        )
        assert called == ["job-A"]

    def test_limit_respected(self):
        dlq = _filled_dlq("j1", "j2", "j3", "j4", "j5")
        called = []
        engine = ReplayEngine(dlq)
        engine.replay(lambda jid, p: called.append(jid), mode="apply", limit=3)
        assert len(called) <= 3


# ---------------------------------------------------------------------------
# replay_dlq convenience function
# ---------------------------------------------------------------------------

class TestReplayDlqFunction:
    def test_dry_run(self):
        dlq = _filled_dlq("x", "y")
        result = replay_dlq(dlq, lambda jid, p: None, mode="dry-run")
        assert set(result.skipped) == {"x", "y"}
        assert result.replayed == []

    def test_apply(self):
        dlq = _filled_dlq("x", "y")
        called = []
        result = replay_dlq(dlq, lambda jid, p: called.append(jid), mode="apply")
        assert set(called) == {"x", "y"}
        assert set(result.replayed) == {"x", "y"}

    def test_with_filter(self):
        dlq = _filled_dlq("a:1", "b:2")
        called = []
        result = replay_dlq(
            dlq,
            lambda jid, p: called.append(jid),
            filter=ReplayFilter(job_type="a"),
            mode="apply",
        )
        assert called == ["a:1"]


# ---------------------------------------------------------------------------
# Helper: _infer_job_type
# ---------------------------------------------------------------------------

class TestInferJobType:
    def test_colon_prefix(self):
        assert _infer_job_type("email:abc123") == "email"

    def test_no_colon_returns_none(self):
        assert _infer_job_type("plainjobid") is None

    def test_empty_string(self):
        assert _infer_job_type("") is None

    def test_multiple_colons_uses_first(self):
        assert _infer_job_type("email:retry:123") == "email"
