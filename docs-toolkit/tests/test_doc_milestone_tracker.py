"""Tests for E367 DocMilestoneTracker."""

from __future__ import annotations

import threading
import time
import uuid

import pytest

from docstoolkit.doc_milestone_tracker import (
    DocMilestoneTracker,
    Milestone,
    MilestoneStats,
)


# --------------------------------------------------------------------------- #
# Milestone dataclass                                                          #
# --------------------------------------------------------------------------- #
class TestMilestoneDataclass:
    def test_required_fields(self):
        m = Milestone(
            milestone_id="m1",
            doc_id="d1",
            name="Draft",
            target_date=100.0,
        )
        assert m.milestone_id == "m1"
        assert m.doc_id == "d1"
        assert m.name == "Draft"
        assert m.target_date == 100.0

    def test_default_status_pending(self):
        m = Milestone(milestone_id="x", doc_id="d", name="n", target_date=1.0)
        assert m.status == "pending"

    def test_default_description_empty(self):
        m = Milestone(milestone_id="x", doc_id="d", name="n", target_date=1.0)
        assert m.description == ""

    def test_default_completed_at_none(self):
        m = Milestone(milestone_id="x", doc_id="d", name="n", target_date=1.0)
        assert m.completed_at is None

    def test_default_progress_zero(self):
        m = Milestone(milestone_id="x", doc_id="d", name="n", target_date=1.0)
        assert m.progress == 0.0

    def test_custom_fields(self):
        m = Milestone(
            milestone_id="x",
            doc_id="d",
            name="n",
            target_date=1.0,
            status="in_progress",
            description="desc",
            completed_at=12.0,
            progress=0.5,
        )
        assert m.status == "in_progress"
        assert m.description == "desc"
        assert m.completed_at == 12.0
        assert m.progress == 0.5


# --------------------------------------------------------------------------- #
# MilestoneStats dataclass                                                     #
# --------------------------------------------------------------------------- #
class TestMilestoneStatsDataclass:
    def test_construct(self):
        s = MilestoneStats(
            total=5,
            pending=1,
            in_progress=1,
            completed=1,
            missed=1,
            cancelled=1,
            avg_progress=0.5,
        )
        assert s.total == 5
        assert s.pending == 1
        assert s.in_progress == 1
        assert s.completed == 1
        assert s.missed == 1
        assert s.cancelled == 1
        assert s.avg_progress == 0.5

    def test_zero_stats(self):
        s = MilestoneStats(0, 0, 0, 0, 0, 0, 0.0)
        assert s.total == 0
        assert s.avg_progress == 0.0


# --------------------------------------------------------------------------- #
# Construction                                                                 #
# --------------------------------------------------------------------------- #
class TestConstruction:
    def test_empty_init(self):
        t = DocMilestoneTracker()
        assert t.stats().total == 0

    def test_independent_instances(self):
        t1 = DocMilestoneTracker()
        t2 = DocMilestoneTracker()
        t1.create_milestone("d", "n", 1.0)
        assert t2.stats().total == 0


# --------------------------------------------------------------------------- #
# create_milestone                                                             #
# --------------------------------------------------------------------------- #
class TestCreateMilestone:
    def test_returns_milestone(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d1", "Draft", 100.0)
        assert isinstance(m, Milestone)

    def test_uuid_format(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d1", "Draft", 100.0)
        # raises ValueError if invalid
        uuid.UUID(m.milestone_id)

    def test_unique_ids(self):
        t = DocMilestoneTracker()
        ids = {t.create_milestone("d", "n", 1.0).milestone_id for _ in range(50)}
        assert len(ids) == 50

    def test_default_status_pending(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        assert m.status == "pending"

    def test_default_progress_zero(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        assert m.progress == 0.0

    def test_default_completed_at_none(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        assert m.completed_at is None

    def test_description_stored(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0, description="hello")
        assert m.description == "hello"

    def test_indexed_by_doc(self):
        t = DocMilestoneTracker()
        t.create_milestone("d1", "a", 1.0)
        t.create_milestone("d1", "b", 2.0)
        t.create_milestone("d2", "c", 3.0)
        assert len(t.milestones_for_doc("d1")) == 2
        assert len(t.milestones_for_doc("d2")) == 1


# --------------------------------------------------------------------------- #
# start                                                                        #
# --------------------------------------------------------------------------- #
class TestStart:
    def test_pending_to_in_progress(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        assert t.start(m.milestone_id) is True
        assert t.get(m.milestone_id).status == "in_progress"

    def test_start_unknown_returns_false(self):
        t = DocMilestoneTracker()
        assert t.start("does-not-exist") is False

    def test_start_in_progress_returns_false(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.start(m.milestone_id)
        assert t.start(m.milestone_id) is False

    def test_start_completed_returns_false(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.complete(m.milestone_id)
        assert t.start(m.milestone_id) is False

    def test_start_cancelled_returns_false(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.cancel(m.milestone_id)
        assert t.start(m.milestone_id) is False


# --------------------------------------------------------------------------- #
# complete                                                                     #
# --------------------------------------------------------------------------- #
class TestComplete:
    def test_complete_from_pending(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        assert t.complete(m.milestone_id, now=50.0) is True
        got = t.get(m.milestone_id)
        assert got.status == "completed"
        assert got.progress == 1.0
        assert got.completed_at == 50.0

    def test_complete_from_in_progress(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.start(m.milestone_id)
        assert t.complete(m.milestone_id, now=99.0) is True
        assert t.get(m.milestone_id).status == "completed"

    def test_complete_unknown(self):
        t = DocMilestoneTracker()
        assert t.complete("missing") is False

    def test_complete_already_completed(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.complete(m.milestone_id)
        assert t.complete(m.milestone_id) is False

    def test_complete_cancelled(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.cancel(m.milestone_id)
        assert t.complete(m.milestone_id) is False

    def test_complete_default_now_is_set(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        before = time.time()
        t.complete(m.milestone_id)
        after = time.time()
        ts = t.get(m.milestone_id).completed_at
        assert before <= ts <= after


# --------------------------------------------------------------------------- #
# cancel                                                                       #
# --------------------------------------------------------------------------- #
class TestCancel:
    def test_cancel_from_pending(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        assert t.cancel(m.milestone_id) is True
        assert t.get(m.milestone_id).status == "cancelled"

    def test_cancel_from_in_progress(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.start(m.milestone_id)
        assert t.cancel(m.milestone_id) is True
        assert t.get(m.milestone_id).status == "cancelled"

    def test_cancel_unknown(self):
        t = DocMilestoneTracker()
        assert t.cancel("nope") is False

    def test_cancel_completed(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.complete(m.milestone_id)
        assert t.cancel(m.milestone_id) is False

    def test_cancel_already_cancelled(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.cancel(m.milestone_id)
        assert t.cancel(m.milestone_id) is False


# --------------------------------------------------------------------------- #
# update_progress                                                              #
# --------------------------------------------------------------------------- #
class TestUpdateProgress:
    def test_basic_update(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        assert t.update_progress(m.milestone_id, 0.4) is True
        assert t.get(m.milestone_id).progress == 0.4

    def test_clamp_below_zero(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.update_progress(m.milestone_id, -0.5)
        assert t.get(m.milestone_id).progress == 0.0

    def test_clamp_above_one(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.update_progress(m.milestone_id, 2.5)
        assert t.get(m.milestone_id).progress == 1.0

    def test_boundary_zero(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        assert t.update_progress(m.milestone_id, 0.0) is True
        assert t.get(m.milestone_id).progress == 0.0

    def test_boundary_one(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        assert t.update_progress(m.milestone_id, 1.0) is True
        assert t.get(m.milestone_id).progress == 1.0

    def test_unknown_returns_false(self):
        t = DocMilestoneTracker()
        assert t.update_progress("missing", 0.5) is False

    def test_terminal_completed_rejected(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.complete(m.milestone_id)
        assert t.update_progress(m.milestone_id, 0.5) is False
        # progress stayed at 1.0
        assert t.get(m.milestone_id).progress == 1.0

    def test_terminal_cancelled_rejected(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.cancel(m.milestone_id)
        assert t.update_progress(m.milestone_id, 0.5) is False

    def test_terminal_missed_rejected(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.mark_missed(now=10.0)
        assert t.get(m.milestone_id).status == "missed"
        assert t.update_progress(m.milestone_id, 0.5) is False

    def test_works_on_in_progress(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.start(m.milestone_id)
        assert t.update_progress(m.milestone_id, 0.7) is True
        assert t.get(m.milestone_id).progress == 0.7


# --------------------------------------------------------------------------- #
# mark_missed                                                                  #
# --------------------------------------------------------------------------- #
class TestMarkMissed:
    def test_mark_all_overdue(self):
        t = DocMilestoneTracker()
        t.create_milestone("d", "a", 1.0)
        t.create_milestone("d", "b", 2.0)
        t.create_milestone("d", "c", 100.0)
        n = t.mark_missed(now=10.0)
        assert n == 2

    def test_does_not_affect_future(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "future", 100.0)
        t.mark_missed(now=10.0)
        assert t.get(m.milestone_id).status == "pending"

    def test_skips_completed(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.complete(m.milestone_id)
        n = t.mark_missed(now=10.0)
        assert n == 0
        assert t.get(m.milestone_id).status == "completed"

    def test_skips_cancelled(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.cancel(m.milestone_id)
        n = t.mark_missed(now=10.0)
        assert n == 0
        assert t.get(m.milestone_id).status == "cancelled"

    def test_in_progress_also_marked(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.start(m.milestone_id)
        n = t.mark_missed(now=10.0)
        assert n == 1
        assert t.get(m.milestone_id).status == "missed"

    def test_explicit_ids(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 1.0)
        b = t.create_milestone("d", "b", 2.0)
        n = t.mark_missed(milestone_ids=[a.milestone_id], now=10.0)
        assert n == 1
        assert t.get(a.milestone_id).status == "missed"
        assert t.get(b.milestone_id).status == "pending"

    def test_explicit_ids_unknown_ignored(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 1.0)
        n = t.mark_missed(milestone_ids=[a.milestone_id, "bogus"], now=10.0)
        assert n == 1

    def test_explicit_ids_future_not_marked(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 100.0)
        n = t.mark_missed(milestone_ids=[m.milestone_id], now=10.0)
        assert n == 0
        assert t.get(m.milestone_id).status == "pending"

    def test_default_now_uses_time(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", time.time() - 10.0)
        n = t.mark_missed()
        assert n == 1
        assert t.get(m.milestone_id).status == "missed"


# --------------------------------------------------------------------------- #
# get                                                                          #
# --------------------------------------------------------------------------- #
class TestGet:
    def test_found(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        got = t.get(m.milestone_id)
        assert got is not None
        assert got.milestone_id == m.milestone_id

    def test_not_found(self):
        t = DocMilestoneTracker()
        assert t.get("nope") is None


# --------------------------------------------------------------------------- #
# milestones_for_doc                                                           #
# --------------------------------------------------------------------------- #
class TestMilestonesForDoc:
    def test_empty(self):
        t = DocMilestoneTracker()
        assert t.milestones_for_doc("missing") == []

    def test_sorted_by_target_date(self):
        t = DocMilestoneTracker()
        t.create_milestone("d", "c", 3.0)
        t.create_milestone("d", "a", 1.0)
        t.create_milestone("d", "b", 2.0)
        names = [m.name for m in t.milestones_for_doc("d")]
        assert names == ["a", "b", "c"]

    def test_status_filter(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 1.0)
        t.create_milestone("d", "b", 2.0)
        t.start(a.milestone_id)
        ms = t.milestones_for_doc("d", status="in_progress")
        assert len(ms) == 1
        assert ms[0].name == "a"

    def test_only_target_doc(self):
        t = DocMilestoneTracker()
        t.create_milestone("d1", "a", 1.0)
        t.create_milestone("d2", "b", 2.0)
        ms = t.milestones_for_doc("d1")
        assert len(ms) == 1
        assert ms[0].name == "a"


# --------------------------------------------------------------------------- #
# upcoming                                                                     #
# --------------------------------------------------------------------------- #
class TestUpcoming:
    def test_within_window(self):
        t = DocMilestoneTracker()
        t.create_milestone("d", "a", 50.0)
        t.create_milestone("d", "b", 200.0)
        ms = t.upcoming(within_seconds=100.0, now=10.0)
        assert [m.name for m in ms] == ["a"]

    def test_sorted_asc(self):
        t = DocMilestoneTracker()
        t.create_milestone("d", "c", 80.0)
        t.create_milestone("d", "a", 20.0)
        t.create_milestone("d", "b", 50.0)
        ms = t.upcoming(within_seconds=100.0, now=10.0)
        assert [m.name for m in ms] == ["a", "b", "c"]

    def test_excludes_past(self):
        t = DocMilestoneTracker()
        t.create_milestone("d", "past", 1.0)
        t.create_milestone("d", "soon", 50.0)
        ms = t.upcoming(within_seconds=100.0, now=10.0)
        assert [m.name for m in ms] == ["soon"]

    def test_excludes_completed(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 50.0)
        t.complete(a.milestone_id)
        assert t.upcoming(within_seconds=100.0, now=10.0) == []

    def test_excludes_cancelled(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 50.0)
        t.cancel(a.milestone_id)
        assert t.upcoming(within_seconds=100.0, now=10.0) == []

    def test_inclusive_boundary(self):
        t = DocMilestoneTracker()
        t.create_milestone("d", "right_now", 10.0)
        t.create_milestone("d", "boundary", 110.0)
        ms = t.upcoming(within_seconds=100.0, now=10.0)
        assert len(ms) == 2


# --------------------------------------------------------------------------- #
# overdue                                                                      #
# --------------------------------------------------------------------------- #
class TestOverdue:
    def test_simple(self):
        t = DocMilestoneTracker()
        t.create_milestone("d", "a", 1.0)
        t.create_milestone("d", "b", 100.0)
        ms = t.overdue(now=10.0)
        assert [m.name for m in ms] == ["a"]

    def test_sorted_asc(self):
        t = DocMilestoneTracker()
        t.create_milestone("d", "b", 5.0)
        t.create_milestone("d", "a", 1.0)
        ms = t.overdue(now=10.0)
        assert [m.name for m in ms] == ["a", "b"]

    def test_excludes_completed(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 1.0)
        t.complete(a.milestone_id)
        assert t.overdue(now=10.0) == []

    def test_excludes_cancelled(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 1.0)
        t.cancel(a.milestone_id)
        assert t.overdue(now=10.0) == []

    def test_excludes_missed(self):
        t = DocMilestoneTracker()
        t.create_milestone("d", "a", 1.0)
        t.mark_missed(now=10.0)
        assert t.overdue(now=10.0) == []

    def test_default_now(self):
        t = DocMilestoneTracker()
        t.create_milestone("d", "a", time.time() - 10.0)
        assert len(t.overdue()) == 1


# --------------------------------------------------------------------------- #
# delete                                                                       #
# --------------------------------------------------------------------------- #
class TestDelete:
    def test_delete_existing(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        assert t.delete(m.milestone_id) is True
        assert t.get(m.milestone_id) is None

    def test_delete_missing(self):
        t = DocMilestoneTracker()
        assert t.delete("nope") is False

    def test_delete_removes_from_doc_index(self):
        t = DocMilestoneTracker()
        m = t.create_milestone("d", "n", 1.0)
        t.delete(m.milestone_id)
        assert t.milestones_for_doc("d") == []

    def test_delete_does_not_affect_others(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 1.0)
        b = t.create_milestone("d", "b", 2.0)
        t.delete(a.milestone_id)
        ms = t.milestones_for_doc("d")
        assert len(ms) == 1
        assert ms[0].milestone_id == b.milestone_id


# --------------------------------------------------------------------------- #
# stats                                                                        #
# --------------------------------------------------------------------------- #
class TestStats:
    def test_empty(self):
        s = DocMilestoneTracker().stats()
        assert s.total == 0
        assert s.avg_progress == 0.0

    def test_counts(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 1.0)
        b = t.create_milestone("d", "b", 100.0)
        c = t.create_milestone("d", "c", 100.0)
        d = t.create_milestone("d", "d", 1.0)
        t.start(b.milestone_id)
        t.complete(c.milestone_id)
        t.cancel(d.milestone_id)
        t.mark_missed(milestone_ids=[a.milestone_id], now=10.0)
        s = t.stats()
        assert s.total == 4
        assert s.pending == 0
        assert s.in_progress == 1
        assert s.completed == 1
        assert s.missed == 1
        assert s.cancelled == 1

    def test_avg_progress(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 1.0)
        b = t.create_milestone("d", "b", 1.0)
        t.update_progress(a.milestone_id, 0.2)
        t.update_progress(b.milestone_id, 0.8)
        s = t.stats()
        assert s.avg_progress == pytest.approx(0.5)

    def test_avg_progress_with_completed(self):
        t = DocMilestoneTracker()
        a = t.create_milestone("d", "a", 1.0)
        b = t.create_milestone("d", "b", 1.0)
        t.complete(a.milestone_id)  # progress=1.0
        t.update_progress(b.milestone_id, 0.0)
        s = t.stats()
        assert s.avg_progress == pytest.approx(0.5)


# --------------------------------------------------------------------------- #
# Thread safety                                                                #
# --------------------------------------------------------------------------- #
class TestThreadSafety:
    def test_concurrent_create(self):
        t = DocMilestoneTracker()
        errors: list[BaseException] = []

        def worker(n: int) -> None:
            try:
                for i in range(n):
                    t.create_milestone("d", f"m{i}", float(i))
            except BaseException as exc:  # pragma: no cover
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(40,)) for _ in range(8)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        assert errors == []
        assert t.stats().total == 8 * 40

    def test_concurrent_mixed_ops(self):
        t = DocMilestoneTracker()
        ms = [t.create_milestone("d", f"m{i}", float(i)) for i in range(50)]

        def updater():
            for m in ms:
                t.update_progress(m.milestone_id, 0.5)

        def starter():
            for m in ms:
                t.start(m.milestone_id)

        threads = [threading.Thread(target=updater) for _ in range(3)] + [
            threading.Thread(target=starter) for _ in range(3)
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        # All should still be retrievable
        for m in ms:
            assert t.get(m.milestone_id) is not None
