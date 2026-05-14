"""Tests for E432 DocArchiveIndex."""
from __future__ import annotations

import threading
import uuid

import pytest

from docstoolkit.doc_archive_index import (
    ArchiveEntry,
    ArchiveStats,
    DocArchiveIndex,
)


# ---------------------------------------------------------------------------
# Construction / dataclasses
# ---------------------------------------------------------------------------


def test_archive_entry_defaults():
    e = ArchiveEntry(archive_id="a", doc_id="d")
    assert e.archive_id == "a"
    assert e.doc_id == "d"
    assert e.archived_at == 0.0
    assert e.archived_by == ""
    assert e.tags == []
    assert e.size_bytes == 0
    assert e.summary == ""


def test_archive_entry_independent_tag_lists():
    a = ArchiveEntry(archive_id="1", doc_id="d")
    b = ArchiveEntry(archive_id="2", doc_id="d")
    a.tags.append("x")
    assert b.tags == []


def test_archive_stats_fields():
    s = ArchiveStats(total_archives=1, unique_docs=2, total_size_bytes=3, unique_tags=4)
    assert s.total_archives == 1
    assert s.unique_docs == 2
    assert s.total_size_bytes == 3
    assert s.unique_tags == 4


def test_index_starts_empty():
    idx = DocArchiveIndex()
    assert idx.all_doc_ids() == []
    assert idx.all_tags() == []
    st = idx.stats()
    assert st.total_archives == 0
    assert st.unique_docs == 0
    assert st.total_size_bytes == 0
    assert st.unique_tags == 0


# ---------------------------------------------------------------------------
# add_entry
# ---------------------------------------------------------------------------


def test_add_entry_returns_entry_with_uuid():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1")
    assert isinstance(e, ArchiveEntry)
    # archive_id is a valid UUID
    uuid.UUID(e.archive_id)


def test_add_entry_uses_now_if_provided():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1", now=123.0)
    assert e.archived_at == 123.0


def test_add_entry_uses_time_time_when_now_none():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1")
    assert e.archived_at > 0


def test_add_entry_stores_fields():
    idx = DocArchiveIndex()
    e = idx.add_entry(
        "doc1",
        archived_by="alice",
        tags=["A", "B"],
        size_bytes=100,
        summary="hello",
        now=1.0,
    )
    assert e.doc_id == "doc1"
    assert e.archived_by == "alice"
    assert e.size_bytes == 100
    assert e.summary == "hello"
    assert e.archived_at == 1.0


def test_add_entry_lowercases_tags():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1", tags=["Foo", "BAR"])
    assert e.tags == ["foo", "bar"]


def test_add_entry_dedupes_tags():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1", tags=["a", "A", "b", "a"])
    assert e.tags == ["a", "b"]


def test_add_entry_default_tags_empty():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1")
    assert e.tags == []


def test_add_entry_unique_archive_ids():
    idx = DocArchiveIndex()
    ids = {idx.add_entry("doc1").archive_id for _ in range(10)}
    assert len(ids) == 10


def test_add_entry_indexed_by_doc():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("doc1", now=1.0)
    e2 = idx.add_entry("doc1", now=2.0)
    entries = idx.entries_for_doc("doc1")
    ids = {e.archive_id for e in entries}
    assert ids == {e1.archive_id, e2.archive_id}


def test_add_entry_indexed_by_tag():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1", tags=["x"])
    assert idx.entries_with_tag("x") == [e]


# ---------------------------------------------------------------------------
# get_entry
# ---------------------------------------------------------------------------


def test_get_entry_returns_entry():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1")
    assert idx.get_entry(e.archive_id) is e or idx.get_entry(e.archive_id).archive_id == e.archive_id


def test_get_entry_returns_none_for_missing():
    idx = DocArchiveIndex()
    assert idx.get_entry("nope") is None


# ---------------------------------------------------------------------------
# remove_entry
# ---------------------------------------------------------------------------


def test_remove_entry_existing_returns_true():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1")
    assert idx.remove_entry(e.archive_id) is True


def test_remove_entry_missing_returns_false():
    idx = DocArchiveIndex()
    assert idx.remove_entry("nope") is False


def test_remove_entry_removes_from_get():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1")
    idx.remove_entry(e.archive_id)
    assert idx.get_entry(e.archive_id) is None


def test_remove_entry_removes_from_doc_index():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1")
    idx.remove_entry(e.archive_id)
    assert idx.entries_for_doc("doc1") == []
    assert "doc1" not in idx.all_doc_ids()


def test_remove_entry_removes_from_tag_index():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1", tags=["x"])
    idx.remove_entry(e.archive_id)
    assert idx.entries_with_tag("x") == []
    assert "x" not in idx.all_tags()


def test_remove_entry_keeps_other_doc_entries():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("doc1", now=1.0)
    e2 = idx.add_entry("doc1", now=2.0)
    idx.remove_entry(e1.archive_id)
    remaining = idx.entries_for_doc("doc1")
    assert [e.archive_id for e in remaining] == [e2.archive_id]


def test_remove_entry_keeps_other_tag_entries():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("doc1", tags=["x"], now=1.0)
    e2 = idx.add_entry("doc2", tags=["x"], now=2.0)
    idx.remove_entry(e1.archive_id)
    remaining = idx.entries_with_tag("x")
    assert [e.archive_id for e in remaining] == [e2.archive_id]


# ---------------------------------------------------------------------------
# entries_for_doc
# ---------------------------------------------------------------------------


def test_entries_for_doc_empty():
    idx = DocArchiveIndex()
    assert idx.entries_for_doc("doc1") == []


def test_entries_for_doc_sorted_desc():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("doc1", now=1.0)
    e2 = idx.add_entry("doc1", now=3.0)
    e3 = idx.add_entry("doc1", now=2.0)
    result = idx.entries_for_doc("doc1")
    assert [e.archive_id for e in result] == [e2.archive_id, e3.archive_id, e1.archive_id]


def test_entries_for_doc_isolates_docs():
    idx = DocArchiveIndex()
    idx.add_entry("doc1", now=1.0)
    e = idx.add_entry("doc2", now=2.0)
    res = idx.entries_for_doc("doc2")
    assert len(res) == 1
    assert res[0].archive_id == e.archive_id


# ---------------------------------------------------------------------------
# entries_with_tag
# ---------------------------------------------------------------------------


def test_entries_with_tag_empty():
    idx = DocArchiveIndex()
    assert idx.entries_with_tag("absent") == []


def test_entries_with_tag_sorted_desc():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("doc1", tags=["x"], now=1.0)
    e2 = idx.add_entry("doc2", tags=["x"], now=3.0)
    e3 = idx.add_entry("doc3", tags=["x"], now=2.0)
    res = idx.entries_with_tag("x")
    assert [e.archive_id for e in res] == [e2.archive_id, e3.archive_id, e1.archive_id]


def test_entries_with_tag_case_insensitive_query():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1", tags=["Foo"])
    assert [r.archive_id for r in idx.entries_with_tag("FOO")] == [e.archive_id]


def test_entries_with_tag_filters_by_tag():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("doc1", tags=["x"])
    idx.add_entry("doc2", tags=["y"])
    res = idx.entries_with_tag("x")
    assert [e.archive_id for e in res] == [e1.archive_id]


# ---------------------------------------------------------------------------
# entries_in_range
# ---------------------------------------------------------------------------


def test_entries_in_range_inclusive():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("d", now=1.0)
    e2 = idx.add_entry("d", now=2.0)
    e3 = idx.add_entry("d", now=3.0)
    res = idx.entries_in_range(1.0, 3.0)
    assert [e.archive_id for e in res] == [e1.archive_id, e2.archive_id, e3.archive_id]


def test_entries_in_range_sorted_asc():
    idx = DocArchiveIndex()
    e3 = idx.add_entry("d", now=3.0)
    e1 = idx.add_entry("d", now=1.0)
    e2 = idx.add_entry("d", now=2.0)
    res = idx.entries_in_range(0.0, 10.0)
    assert [e.archive_id for e in res] == [e1.archive_id, e2.archive_id, e3.archive_id]


def test_entries_in_range_exclude_outside():
    idx = DocArchiveIndex()
    idx.add_entry("d", now=0.5)
    e = idx.add_entry("d", now=2.0)
    idx.add_entry("d", now=5.0)
    res = idx.entries_in_range(1.0, 3.0)
    assert [r.archive_id for r in res] == [e.archive_id]


def test_entries_in_range_empty():
    idx = DocArchiveIndex()
    assert idx.entries_in_range(0.0, 100.0) == []


def test_entries_in_range_no_match():
    idx = DocArchiveIndex()
    idx.add_entry("d", now=10.0)
    assert idx.entries_in_range(0.0, 5.0) == []


# ---------------------------------------------------------------------------
# entries_by_user
# ---------------------------------------------------------------------------


def test_entries_by_user_empty():
    idx = DocArchiveIndex()
    assert idx.entries_by_user("alice") == []


def test_entries_by_user_filters_actor():
    idx = DocArchiveIndex()
    a1 = idx.add_entry("d", archived_by="alice", now=1.0)
    idx.add_entry("d", archived_by="bob", now=2.0)
    a2 = idx.add_entry("d", archived_by="alice", now=3.0)
    res = idx.entries_by_user("alice")
    assert [e.archive_id for e in res] == [a2.archive_id, a1.archive_id]


def test_entries_by_user_most_recent_first():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("d", archived_by="x", now=1.0)
    e2 = idx.add_entry("d", archived_by="x", now=5.0)
    e3 = idx.add_entry("d", archived_by="x", now=3.0)
    res = idx.entries_by_user("x")
    assert [e.archive_id for e in res] == [e2.archive_id, e3.archive_id, e1.archive_id]


def test_entries_by_user_respects_limit():
    idx = DocArchiveIndex()
    for i in range(5):
        idx.add_entry("d", archived_by="u", now=float(i))
    res = idx.entries_by_user("u", limit=2)
    assert len(res) == 2
    assert res[0].archived_at == 4.0
    assert res[1].archived_at == 3.0


def test_entries_by_user_limit_larger_than_results():
    idx = DocArchiveIndex()
    idx.add_entry("d", archived_by="u", now=1.0)
    res = idx.entries_by_user("u", limit=10)
    assert len(res) == 1


def test_entries_by_user_exact_match_case_sensitive():
    idx = DocArchiveIndex()
    e = idx.add_entry("d", archived_by="Alice")
    assert idx.entries_by_user("alice") == []
    assert [r.archive_id for r in idx.entries_by_user("Alice")] == [e.archive_id]


# ---------------------------------------------------------------------------
# search_summary
# ---------------------------------------------------------------------------


def test_search_summary_substring():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("d", summary="quick brown fox", now=1.0)
    idx.add_entry("d", summary="lazy dog", now=2.0)
    res = idx.search_summary("fox")
    assert [e.archive_id for e in res] == [e1.archive_id]


def test_search_summary_case_insensitive():
    idx = DocArchiveIndex()
    e = idx.add_entry("d", summary="Hello WORLD")
    assert [r.archive_id for r in idx.search_summary("world")] == [e.archive_id]
    assert [r.archive_id for r in idx.search_summary("HELLO")] == [e.archive_id]


def test_search_summary_sorted_desc():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("d", summary="match me", now=1.0)
    e2 = idx.add_entry("d", summary="match me", now=3.0)
    e3 = idx.add_entry("d", summary="match me", now=2.0)
    res = idx.search_summary("match")
    assert [e.archive_id for e in res] == [e2.archive_id, e3.archive_id, e1.archive_id]


def test_search_summary_empty_query_returns_all():
    idx = DocArchiveIndex()
    idx.add_entry("d", summary="a", now=1.0)
    idx.add_entry("d", summary="b", now=2.0)
    assert len(idx.search_summary("")) == 2


def test_search_summary_no_match():
    idx = DocArchiveIndex()
    idx.add_entry("d", summary="hello")
    assert idx.search_summary("absent") == []


# ---------------------------------------------------------------------------
# total_size_for_doc
# ---------------------------------------------------------------------------


def test_total_size_for_doc_empty():
    idx = DocArchiveIndex()
    assert idx.total_size_for_doc("doc1") == 0


def test_total_size_for_doc_sums():
    idx = DocArchiveIndex()
    idx.add_entry("doc1", size_bytes=10)
    idx.add_entry("doc1", size_bytes=20)
    idx.add_entry("doc1", size_bytes=30)
    assert idx.total_size_for_doc("doc1") == 60


def test_total_size_for_doc_isolated():
    idx = DocArchiveIndex()
    idx.add_entry("doc1", size_bytes=10)
    idx.add_entry("doc2", size_bytes=100)
    assert idx.total_size_for_doc("doc1") == 10
    assert idx.total_size_for_doc("doc2") == 100


# ---------------------------------------------------------------------------
# all_doc_ids / all_tags
# ---------------------------------------------------------------------------


def test_all_doc_ids_sorted():
    idx = DocArchiveIndex()
    idx.add_entry("zeta")
    idx.add_entry("alpha")
    idx.add_entry("mu")
    assert idx.all_doc_ids() == ["alpha", "mu", "zeta"]


def test_all_doc_ids_unique():
    idx = DocArchiveIndex()
    idx.add_entry("d")
    idx.add_entry("d")
    assert idx.all_doc_ids() == ["d"]


def test_all_tags_sorted():
    idx = DocArchiveIndex()
    idx.add_entry("d", tags=["zeta", "alpha", "mu"])
    assert idx.all_tags() == ["alpha", "mu", "zeta"]


def test_all_tags_dedup():
    idx = DocArchiveIndex()
    idx.add_entry("d1", tags=["x"])
    idx.add_entry("d2", tags=["x"])
    assert idx.all_tags() == ["x"]


def test_all_tags_empty():
    idx = DocArchiveIndex()
    idx.add_entry("d")  # no tags
    assert idx.all_tags() == []


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------


def test_clear_doc_returns_count():
    idx = DocArchiveIndex()
    idx.add_entry("doc1")
    idx.add_entry("doc1")
    idx.add_entry("doc1")
    assert idx.clear_doc("doc1") == 3


def test_clear_doc_missing_returns_zero():
    idx = DocArchiveIndex()
    assert idx.clear_doc("nope") == 0


def test_clear_doc_removes_entries():
    idx = DocArchiveIndex()
    e1 = idx.add_entry("doc1", tags=["x"])
    e2 = idx.add_entry("doc1", tags=["y"])
    idx.clear_doc("doc1")
    assert idx.get_entry(e1.archive_id) is None
    assert idx.get_entry(e2.archive_id) is None
    assert idx.entries_for_doc("doc1") == []
    assert idx.all_tags() == []


def test_clear_doc_preserves_other_docs():
    idx = DocArchiveIndex()
    idx.add_entry("doc1", tags=["x"])
    e = idx.add_entry("doc2", tags=["x"])
    idx.clear_doc("doc1")
    assert idx.all_doc_ids() == ["doc2"]
    assert idx.all_tags() == ["x"]
    assert [r.archive_id for r in idx.entries_with_tag("x")] == [e.archive_id]


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_empty():
    idx = DocArchiveIndex()
    s = idx.stats()
    assert s == ArchiveStats(0, 0, 0, 0)


def test_stats_basic():
    idx = DocArchiveIndex()
    idx.add_entry("doc1", tags=["a", "b"], size_bytes=10)
    idx.add_entry("doc2", tags=["b", "c"], size_bytes=20)
    s = idx.stats()
    assert s.total_archives == 2
    assert s.unique_docs == 2
    assert s.total_size_bytes == 30
    assert s.unique_tags == 3


def test_stats_after_remove():
    idx = DocArchiveIndex()
    e = idx.add_entry("doc1", tags=["a"], size_bytes=10)
    idx.add_entry("doc2", tags=["b"], size_bytes=20)
    idx.remove_entry(e.archive_id)
    s = idx.stats()
    assert s.total_archives == 1
    assert s.unique_docs == 1
    assert s.total_size_bytes == 20
    assert s.unique_tags == 1


def test_stats_after_clear_doc():
    idx = DocArchiveIndex()
    idx.add_entry("doc1", tags=["a"], size_bytes=10)
    idx.add_entry("doc1", tags=["b"], size_bytes=20)
    idx.add_entry("doc2", tags=["c"], size_bytes=30)
    idx.clear_doc("doc1")
    s = idx.stats()
    assert s.total_archives == 1
    assert s.unique_docs == 1
    assert s.total_size_bytes == 30
    assert s.unique_tags == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_thread_safety_concurrent_adds():
    idx = DocArchiveIndex()
    N = 50
    T = 8

    def worker(start):
        for i in range(N):
            idx.add_entry(f"doc{start}", tags=[f"tag{i % 5}"], size_bytes=1)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(T)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = idx.stats()
    assert s.total_archives == N * T
    assert s.unique_docs == T
    assert s.total_size_bytes == N * T


def test_thread_safety_concurrent_add_and_remove():
    idx = DocArchiveIndex()
    # Pre-populate
    entries = [idx.add_entry("doc", size_bytes=1) for _ in range(200)]

    def adder():
        for _ in range(100):
            idx.add_entry("doc", size_bytes=1)

    def remover():
        for e in entries:
            idx.remove_entry(e.archive_id)

    t1 = threading.Thread(target=adder)
    t2 = threading.Thread(target=remover)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # 200 originals removed, 100 added → 100 left
    s = idx.stats()
    assert s.total_archives == 100


def test_thread_safety_concurrent_reads():
    idx = DocArchiveIndex()
    for i in range(50):
        idx.add_entry("doc", tags=["t"], size_bytes=1, now=float(i))

    results = []

    def reader():
        for _ in range(20):
            results.append(len(idx.entries_for_doc("doc")))
            results.append(len(idx.entries_with_tag("t")))
            results.append(idx.stats().total_archives)

    threads = [threading.Thread(target=reader) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(r == 50 for r in results)
