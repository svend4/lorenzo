"""Tests for E442 DocThreadIndex."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_thread_index import DocThreadIndex, ThreadRef, ThreadStats


# ---------------------------------------------------------------- creation


def test_create_returns_thread_ref():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert isinstance(ref, ThreadRef)


def test_create_assigns_uuid_thread_id():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    # UUID4 string length is 36 with hyphens
    assert isinstance(ref.thread_id, str) and len(ref.thread_id) == 36


def test_create_unique_thread_ids():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1")
    b = idx.create_thread("doc1")
    assert a.thread_id != b.thread_id


def test_create_sets_doc_id():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert ref.doc_id == "doc1"


def test_create_default_title_empty():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert ref.title == ""


def test_create_with_title():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", title="Bug fix")
    assert ref.title == "Bug fix"


def test_create_with_creator_added_as_participant():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", created_by="alice")
    assert ref.participants == ["alice"]


def test_create_without_creator_no_participants():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert ref.participants == []


def test_create_sets_timestamps_equal_initially():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", now=100.0)
    assert ref.created_at == 100.0
    assert ref.last_activity_at == 100.0


def test_create_default_message_count_zero():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert ref.message_count == 0


def test_create_default_unresolved():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert ref.resolved is False


def test_create_uses_current_time_when_now_none():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert ref.created_at > 0


# ----------------------------------------------------------------- lookup


def test_get_thread_returns_ref():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    got = idx.get_thread(ref.thread_id)
    assert got is ref


def test_get_thread_unknown_returns_none():
    idx = DocThreadIndex()
    assert idx.get_thread("nope") is None


def test_delete_thread_existing_returns_true():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert idx.delete_thread(ref.thread_id) is True


def test_delete_thread_unknown_returns_false():
    idx = DocThreadIndex()
    assert idx.delete_thread("nope") is False


def test_delete_thread_removes_from_get():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    idx.delete_thread(ref.thread_id)
    assert idx.get_thread(ref.thread_id) is None


def test_delete_thread_removes_from_doc_index():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    idx.delete_thread(ref.thread_id)
    assert idx.threads_for_doc("doc1") == []


def test_delete_thread_removes_from_participant_index():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", created_by="alice")
    idx.delete_thread(ref.thread_id)
    assert idx.threads_for_participant("alice") == []


# ---------------------------------------------------------------- messages


def test_add_message_increments_count():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", created_by="alice", now=100.0)
    idx.add_message(ref.thread_id, "bob", now=200.0)
    assert ref.message_count == 1


def test_add_message_updates_last_activity():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", created_by="alice", now=100.0)
    idx.add_message(ref.thread_id, "bob", now=200.0)
    assert ref.last_activity_at == 200.0


def test_add_message_keeps_created_at_unchanged():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", created_by="alice", now=100.0)
    idx.add_message(ref.thread_id, "bob", now=200.0)
    assert ref.created_at == 100.0


def test_add_message_adds_new_participant():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", created_by="alice")
    idx.add_message(ref.thread_id, "bob")
    assert "bob" in ref.participants


def test_add_message_skips_existing_participant():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", created_by="alice")
    idx.add_message(ref.thread_id, "alice")
    assert ref.participants.count("alice") == 1


def test_add_message_unknown_thread_returns_false():
    idx = DocThreadIndex()
    assert idx.add_message("nope", "alice") is False


def test_add_message_found_returns_true():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert idx.add_message(ref.thread_id, "alice") is True


def test_add_message_indexes_participant():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    idx.add_message(ref.thread_id, "alice")
    found = idx.threads_for_participant("alice")
    assert len(found) == 1 and found[0] is ref


# -------------------------------------------------------- participants


def test_add_participant_new():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert idx.add_participant(ref.thread_id, "alice") is True
    assert "alice" in ref.participants


def test_add_participant_duplicate_returns_false():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", created_by="alice")
    assert idx.add_participant(ref.thread_id, "alice") is False


def test_add_participant_unknown_thread_returns_false():
    idx = DocThreadIndex()
    assert idx.add_participant("nope", "alice") is False


def test_add_participant_empty_string_returns_false():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert idx.add_participant(ref.thread_id, "") is False


def test_remove_participant_existing():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", created_by="alice")
    assert idx.remove_participant(ref.thread_id, "alice") is True
    assert "alice" not in ref.participants


def test_remove_participant_missing_returns_false():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert idx.remove_participant(ref.thread_id, "alice") is False


def test_remove_participant_unknown_thread_returns_false():
    idx = DocThreadIndex()
    assert idx.remove_participant("nope", "alice") is False


def test_remove_participant_updates_index():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1", created_by="alice")
    idx.remove_participant(ref.thread_id, "alice")
    assert idx.threads_for_participant("alice") == []


# ---------------------------------------------------------------- resolve


def test_resolve_sets_flag():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    assert idx.resolve(ref.thread_id) is True
    assert ref.resolved is True


def test_resolve_unknown_returns_false():
    idx = DocThreadIndex()
    assert idx.resolve("nope") is False


def test_reopen_clears_flag():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    idx.resolve(ref.thread_id)
    assert idx.reopen(ref.thread_id) is True
    assert ref.resolved is False


def test_reopen_unknown_returns_false():
    idx = DocThreadIndex()
    assert idx.reopen("nope") is False


# ------------------------------------------------------- threads_for_doc


def test_threads_for_doc_empty():
    idx = DocThreadIndex()
    assert idx.threads_for_doc("nope") == []


def test_threads_for_doc_returns_only_matching():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1")
    idx.create_thread("doc2")
    refs = idx.threads_for_doc("doc1")
    assert [r.thread_id for r in refs] == [a.thread_id]


def test_threads_for_doc_sorted_by_activity_desc():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1", now=100.0)
    b = idx.create_thread("doc1", now=200.0)
    c = idx.create_thread("doc1", now=150.0)
    refs = idx.threads_for_doc("doc1")
    assert [r.thread_id for r in refs] == [b.thread_id, c.thread_id, a.thread_id]


def test_threads_for_doc_filter_resolved_true():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1")
    idx.create_thread("doc1")
    idx.resolve(a.thread_id)
    refs = idx.threads_for_doc("doc1", resolved=True)
    assert [r.thread_id for r in refs] == [a.thread_id]


def test_threads_for_doc_filter_resolved_false():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1")
    b = idx.create_thread("doc1")
    idx.resolve(a.thread_id)
    refs = idx.threads_for_doc("doc1", resolved=False)
    assert [r.thread_id for r in refs] == [b.thread_id]


# --------------------------------------------------- threads_for_participant


def test_threads_for_participant_empty():
    idx = DocThreadIndex()
    assert idx.threads_for_participant("alice") == []


def test_threads_for_participant_multiple_threads():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1", created_by="alice", now=100.0)
    b = idx.create_thread("doc2", created_by="alice", now=200.0)
    refs = idx.threads_for_participant("alice")
    assert [r.thread_id for r in refs] == [b.thread_id, a.thread_id]


def test_threads_for_participant_excludes_others():
    idx = DocThreadIndex()
    idx.create_thread("doc1", created_by="bob")
    a = idx.create_thread("doc2", created_by="alice")
    refs = idx.threads_for_participant("alice")
    assert [r.thread_id for r in refs] == [a.thread_id]


# -------------------------------------------------------- active_threads


def test_active_threads_within_window():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1", now=100.0)
    idx.add_message(a.thread_id, "alice", now=10000.0)
    refs = idx.active_threads(within_seconds=100, now=10050.0)
    assert [r.thread_id for r in refs] == [a.thread_id]


def test_active_threads_outside_window():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1", now=100.0)
    idx.add_message(a.thread_id, "alice", now=200.0)
    refs = idx.active_threads(within_seconds=10, now=10000.0)
    assert refs == []


def test_active_threads_sorted_desc():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1", now=100.0)
    b = idx.create_thread("doc2", now=200.0)
    c = idx.create_thread("doc3", now=150.0)
    refs = idx.active_threads(within_seconds=10000, now=300.0)
    assert [r.thread_id for r in refs] == [b.thread_id, c.thread_id, a.thread_id]


# ---------------------------------------------------- unresolved_threads


def test_unresolved_threads_empty():
    idx = DocThreadIndex()
    assert idx.unresolved_threads() == []


def test_unresolved_threads_returns_only_unresolved():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1", now=100.0)
    b = idx.create_thread("doc1", now=200.0)
    idx.resolve(a.thread_id)
    refs = idx.unresolved_threads()
    assert [r.thread_id for r in refs] == [b.thread_id]


def test_unresolved_threads_sorted_oldest_first():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1", now=300.0)
    b = idx.create_thread("doc1", now=100.0)
    c = idx.create_thread("doc1", now=200.0)
    refs = idx.unresolved_threads()
    assert [r.thread_id for r in refs] == [b.thread_id, c.thread_id, a.thread_id]


# ------------------------------------------------------------- clear_doc


def test_clear_doc_removes_all_threads():
    idx = DocThreadIndex()
    idx.create_thread("doc1")
    idx.create_thread("doc1")
    removed = idx.clear_doc("doc1")
    assert removed == 2
    assert idx.threads_for_doc("doc1") == []


def test_clear_doc_returns_zero_when_missing():
    idx = DocThreadIndex()
    assert idx.clear_doc("nope") == 0


def test_clear_doc_keeps_other_docs():
    idx = DocThreadIndex()
    idx.create_thread("doc1")
    keep = idx.create_thread("doc2")
    idx.clear_doc("doc1")
    refs = idx.threads_for_doc("doc2")
    assert [r.thread_id for r in refs] == [keep.thread_id]


def test_clear_doc_clears_participant_index():
    idx = DocThreadIndex()
    idx.create_thread("doc1", created_by="alice")
    idx.clear_doc("doc1")
    assert idx.threads_for_participant("alice") == []


# ----------------------------------------------------------- all_doc_ids


def test_all_doc_ids_empty():
    idx = DocThreadIndex()
    assert idx.all_doc_ids() == []


def test_all_doc_ids_sorted_unique():
    idx = DocThreadIndex()
    idx.create_thread("z-doc")
    idx.create_thread("a-doc")
    idx.create_thread("a-doc")
    assert idx.all_doc_ids() == ["a-doc", "z-doc"]


# ----------------------------------------------------------------- stats


def test_stats_empty():
    idx = DocThreadIndex()
    s = idx.stats()
    assert isinstance(s, ThreadStats)
    assert s.total_threads == 0
    assert s.unresolved_count == 0
    assert s.unique_docs == 0
    assert s.total_messages == 0


def test_stats_counts_threads():
    idx = DocThreadIndex()
    idx.create_thread("doc1")
    idx.create_thread("doc2")
    s = idx.stats()
    assert s.total_threads == 2
    assert s.unique_docs == 2


def test_stats_counts_unresolved():
    idx = DocThreadIndex()
    a = idx.create_thread("doc1")
    idx.create_thread("doc1")
    idx.resolve(a.thread_id)
    s = idx.stats()
    assert s.unresolved_count == 1


def test_stats_counts_messages():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    idx.add_message(ref.thread_id, "alice")
    idx.add_message(ref.thread_id, "bob")
    idx.add_message(ref.thread_id, "alice")
    s = idx.stats()
    assert s.total_messages == 3


# --------------------------------------------------------- thread safety


def test_thread_safe_concurrent_create():
    idx = DocThreadIndex()
    n_threads = 10
    per_thread = 50

    def worker():
        for _ in range(per_thread):
            idx.create_thread("doc1", created_by="alice")

    threads = [threading.Thread(target=worker) for _ in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = idx.stats()
    assert s.total_threads == n_threads * per_thread
    assert s.unique_docs == 1


def test_thread_safe_concurrent_add_message():
    idx = DocThreadIndex()
    ref = idx.create_thread("doc1")
    n_threads = 8
    per_thread = 25

    def worker(name: str):
        for _ in range(per_thread):
            idx.add_message(ref.thread_id, name)

    threads = [
        threading.Thread(target=worker, args=(f"u{i}",)) for i in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert ref.message_count == n_threads * per_thread
    # All 8 unique participants should be registered
    assert len(ref.participants) == n_threads


def test_thread_safe_concurrent_mixed_ops():
    idx = DocThreadIndex()
    refs = [idx.create_thread(f"doc{i}") for i in range(20)]

    def adder():
        for r in refs:
            idx.add_message(r.thread_id, "alice")

    def resolver():
        for r in refs:
            idx.resolve(r.thread_id)
            idx.reopen(r.thread_id)

    def reader():
        for _ in range(10):
            idx.stats()
            idx.all_doc_ids()

    threads = [
        threading.Thread(target=adder),
        threading.Thread(target=resolver),
        threading.Thread(target=reader),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = idx.stats()
    assert s.total_threads == 20
    assert s.total_messages == 20


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
