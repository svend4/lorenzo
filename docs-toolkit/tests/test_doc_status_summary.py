"""Tests for the E430 ``doc_status_summary`` module."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_status_summary import (
    DocStatusSummary,
    StatusSnapshot,
    SummaryReport,
    SummaryStats,
)


# ----------------------------------------------------------------------
# Construction
# ----------------------------------------------------------------------

def test_construct_default() -> None:
    s = DocStatusSummary()
    assert s.stats().total_docs == 0


def test_construct_no_snapshots() -> None:
    s = DocStatusSummary()
    assert s.all_doc_ids() == []


def test_construct_no_statuses() -> None:
    s = DocStatusSummary()
    assert s.all_statuses() == []


def test_construct_reports_generated_zero() -> None:
    s = DocStatusSummary()
    assert s.stats().reports_generated == 0


# ----------------------------------------------------------------------
# update_status
# ----------------------------------------------------------------------

def test_update_status_returns_snapshot() -> None:
    s = DocStatusSummary()
    snap = s.update_status("d1", "draft", now=100.0)
    assert isinstance(snap, StatusSnapshot)
    assert snap.doc_id == "d1"
    assert snap.status == "draft"
    assert snap.updated_at == 100.0


def test_update_status_stored() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft", now=100.0)
    snap = s.get_snapshot("d1")
    assert snap is not None
    assert snap.status == "draft"


def test_update_status_replaces() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft", now=100.0)
    s.update_status("d1", "review", now=110.0)
    snap = s.get_snapshot("d1")
    assert snap is not None
    assert snap.status == "review"
    assert snap.updated_at == 110.0


def test_update_status_default_now() -> None:
    s = DocStatusSummary()
    before = time.time()
    snap = s.update_status("d1", "draft")
    after = time.time()
    assert before <= snap.updated_at <= after


def test_update_status_multiple_docs() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft", now=1.0)
    s.update_status("d2", "review", now=2.0)
    s.update_status("d3", "published", now=3.0)
    assert s.stats().total_docs == 3


def test_update_status_same_status_twice() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft", now=1.0)
    s.update_status("d1", "draft", now=2.0)
    snap = s.get_snapshot("d1")
    assert snap is not None
    assert snap.updated_at == 2.0


# ----------------------------------------------------------------------
# get_snapshot
# ----------------------------------------------------------------------

def test_get_snapshot_unknown() -> None:
    s = DocStatusSummary()
    assert s.get_snapshot("nope") is None


def test_get_snapshot_known() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft", now=5.0)
    snap = s.get_snapshot("d1")
    assert snap is not None
    assert snap.doc_id == "d1"
    assert snap.status == "draft"
    assert snap.updated_at == 5.0


def test_get_snapshot_after_clear() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft", now=5.0)
    s.clear_doc("d1")
    assert s.get_snapshot("d1") is None


# ----------------------------------------------------------------------
# clear_doc
# ----------------------------------------------------------------------

def test_clear_doc_existing() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    assert s.clear_doc("d1") is True


def test_clear_doc_missing() -> None:
    s = DocStatusSummary()
    assert s.clear_doc("nope") is False


def test_clear_doc_isolation() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d2", "review")
    s.clear_doc("d1")
    assert s.get_snapshot("d1") is None
    assert s.get_snapshot("d2") is not None


def test_clear_doc_twice() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    assert s.clear_doc("d1") is True
    assert s.clear_doc("d1") is False


# ----------------------------------------------------------------------
# clear_all
# ----------------------------------------------------------------------

def test_clear_all_empty() -> None:
    s = DocStatusSummary()
    assert s.clear_all() == 0


def test_clear_all_returns_count() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d2", "review")
    s.update_status("d3", "published")
    assert s.clear_all() == 3


def test_clear_all_empties_store() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d2", "review")
    s.clear_all()
    assert s.all_doc_ids() == []
    assert s.stats().total_docs == 0


def test_clear_all_preserves_reports_counter() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.summarize()
    s.clear_all()
    assert s.stats().reports_generated == 1


# ----------------------------------------------------------------------
# docs_with_status
# ----------------------------------------------------------------------

def test_docs_with_status_empty() -> None:
    s = DocStatusSummary()
    assert s.docs_with_status("draft") == []


def test_docs_with_status_returns_sorted() -> None:
    s = DocStatusSummary()
    s.update_status("zeta", "draft")
    s.update_status("alpha", "draft")
    s.update_status("mike", "draft")
    assert s.docs_with_status("draft") == ["alpha", "mike", "zeta"]


def test_docs_with_status_filters_by_status() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d2", "review")
    s.update_status("d3", "draft")
    assert s.docs_with_status("draft") == ["d1", "d3"]
    assert s.docs_with_status("review") == ["d2"]


def test_docs_with_status_unknown_status() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    assert s.docs_with_status("archived") == []


# ----------------------------------------------------------------------
# summarize
# ----------------------------------------------------------------------

def test_summarize_empty() -> None:
    s = DocStatusSummary()
    rep = s.summarize(now=10.0)
    assert isinstance(rep, SummaryReport)
    assert rep.total == 0
    assert rep.status_counts == {}
    assert rep.generated_at == 10.0


def test_summarize_counts() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d2", "draft")
    s.update_status("d3", "review")
    rep = s.summarize(now=1.0)
    assert rep.total == 3
    assert rep.status_counts == {"draft": 2, "review": 1}


def test_summarize_default_now() -> None:
    s = DocStatusSummary()
    before = time.time()
    rep = s.summarize()
    after = time.time()
    assert before <= rep.generated_at <= after


def test_summarize_increments_counter() -> None:
    s = DocStatusSummary()
    s.summarize()
    s.summarize()
    s.summarize()
    assert s.stats().reports_generated == 3


def test_summarize_counter_starts_at_zero() -> None:
    s = DocStatusSummary()
    assert s.stats().reports_generated == 0
    s.summarize()
    assert s.stats().reports_generated == 1


def test_summarize_after_clear_doc() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d2", "draft")
    s.clear_doc("d1")
    rep = s.summarize()
    assert rep.total == 1
    assert rep.status_counts == {"draft": 1}


# ----------------------------------------------------------------------
# top_statuses
# ----------------------------------------------------------------------

def test_top_statuses_empty() -> None:
    s = DocStatusSummary()
    assert s.top_statuses() == []


def test_top_statuses_sorted_by_count_desc() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d2", "draft")
    s.update_status("d3", "draft")
    s.update_status("d4", "review")
    s.update_status("d5", "published")
    s.update_status("d6", "published")
    top = s.top_statuses()
    assert top == [("draft", 3), ("published", 2), ("review", 1)]


def test_top_statuses_tiebreak_by_status_asc() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "zeta")
    s.update_status("d2", "alpha")
    s.update_status("d3", "mike")
    top = s.top_statuses()
    assert top == [("alpha", 1), ("mike", 1), ("zeta", 1)]


def test_top_statuses_limit() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "a")
    s.update_status("d2", "b")
    s.update_status("d3", "c")
    s.update_status("d4", "d")
    top = s.top_statuses(limit=2)
    assert len(top) == 2


def test_top_statuses_limit_zero() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "a")
    assert s.top_statuses(limit=0) == []


def test_top_statuses_limit_negative() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "a")
    assert s.top_statuses(limit=-1) == []


def test_top_statuses_limit_larger_than_data() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "a")
    assert s.top_statuses(limit=100) == [("a", 1)]


# ----------------------------------------------------------------------
# status_changed_since
# ----------------------------------------------------------------------

def test_status_changed_since_empty() -> None:
    s = DocStatusSummary()
    assert s.status_changed_since(0.0) == []


def test_status_changed_since_includes_newer() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft", now=10.0)
    s.update_status("d2", "review", now=20.0)
    out = s.status_changed_since(15.0)
    assert len(out) == 1
    assert out[0].doc_id == "d2"


def test_status_changed_since_strictly_after() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft", now=10.0)
    out = s.status_changed_since(10.0)
    assert out == []


def test_status_changed_since_sorted_asc() -> None:
    s = DocStatusSummary()
    s.update_status("d3", "draft", now=30.0)
    s.update_status("d1", "draft", now=10.0)
    s.update_status("d2", "draft", now=20.0)
    out = s.status_changed_since(0.0)
    assert [snap.updated_at for snap in out] == [10.0, 20.0, 30.0]


def test_status_changed_since_all() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft", now=5.0)
    s.update_status("d2", "review", now=6.0)
    out = s.status_changed_since(0.0)
    assert len(out) == 2


# ----------------------------------------------------------------------
# all_doc_ids
# ----------------------------------------------------------------------

def test_all_doc_ids_empty() -> None:
    s = DocStatusSummary()
    assert s.all_doc_ids() == []


def test_all_doc_ids_sorted() -> None:
    s = DocStatusSummary()
    s.update_status("zeta", "draft")
    s.update_status("alpha", "draft")
    s.update_status("mike", "draft")
    assert s.all_doc_ids() == ["alpha", "mike", "zeta"]


def test_all_doc_ids_after_clear() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d2", "draft")
    s.clear_doc("d1")
    assert s.all_doc_ids() == ["d2"]


# ----------------------------------------------------------------------
# all_statuses
# ----------------------------------------------------------------------

def test_all_statuses_empty() -> None:
    s = DocStatusSummary()
    assert s.all_statuses() == []


def test_all_statuses_unique_and_sorted() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "zeta")
    s.update_status("d2", "alpha")
    s.update_status("d3", "mike")
    s.update_status("d4", "alpha")
    assert s.all_statuses() == ["alpha", "mike", "zeta"]


def test_all_statuses_after_doc_update() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d1", "review")
    assert s.all_statuses() == ["review"]


# ----------------------------------------------------------------------
# stats
# ----------------------------------------------------------------------

def test_stats_empty() -> None:
    s = DocStatusSummary()
    st = s.stats()
    assert isinstance(st, SummaryStats)
    assert st.total_docs == 0
    assert st.unique_statuses == 0
    assert st.reports_generated == 0


def test_stats_total_docs() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d2", "review")
    assert s.stats().total_docs == 2


def test_stats_unique_statuses() -> None:
    s = DocStatusSummary()
    s.update_status("d1", "draft")
    s.update_status("d2", "draft")
    s.update_status("d3", "review")
    assert s.stats().unique_statuses == 2


def test_stats_reports_generated_after_summarize() -> None:
    s = DocStatusSummary()
    s.summarize()
    s.summarize()
    assert s.stats().reports_generated == 2


def test_stats_returns_fresh_instance() -> None:
    s = DocStatusSummary()
    a = s.stats()
    s.update_status("d1", "draft")
    b = s.stats()
    assert a.total_docs == 0
    assert b.total_docs == 1


# ----------------------------------------------------------------------
# Dataclass shapes
# ----------------------------------------------------------------------

def test_status_snapshot_defaults() -> None:
    snap = StatusSnapshot(doc_id="x", status="draft")
    assert snap.updated_at == 0.0


def test_summary_report_defaults() -> None:
    rep = SummaryReport()
    assert rep.status_counts == {}
    assert rep.total == 0
    assert rep.generated_at == 0.0


def test_summary_report_independent_default_dict() -> None:
    a = SummaryReport()
    b = SummaryReport()
    a.status_counts["draft"] = 1
    assert b.status_counts == {}


# ----------------------------------------------------------------------
# Thread safety
# ----------------------------------------------------------------------

def test_thread_safety_concurrent_updates() -> None:
    s = DocStatusSummary()

    def writer(prefix: str) -> None:
        for i in range(100):
            s.update_status(f"{prefix}-{i}", "draft")

    threads = [threading.Thread(target=writer, args=(f"w{n}",)) for n in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert s.stats().total_docs == 8 * 100


def test_thread_safety_concurrent_summarize() -> None:
    s = DocStatusSummary()
    for i in range(50):
        s.update_status(f"d{i}", "draft")

    def reader() -> None:
        for _ in range(50):
            s.summarize()

    threads = [threading.Thread(target=reader) for _ in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert s.stats().reports_generated == 6 * 50


def test_thread_safety_mixed_ops() -> None:
    s = DocStatusSummary()

    def worker(idx: int) -> None:
        for i in range(50):
            s.update_status(f"doc-{idx}-{i}", "draft")
            s.summarize()
            s.docs_with_status("draft")
            s.top_statuses()

    threads = [threading.Thread(target=worker, args=(n,)) for n in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert s.stats().total_docs == 4 * 50


def test_thread_safety_concurrent_clear() -> None:
    s = DocStatusSummary()
    for i in range(200):
        s.update_status(f"d{i}", "draft")

    def deleter(start: int) -> None:
        for i in range(start, start + 50):
            s.clear_doc(f"d{i}")

    threads = [threading.Thread(target=deleter, args=(n * 50,)) for n in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert s.stats().total_docs == 0
