"""Tests for E353 DocSegmentCache."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_segment_cache import DocSegmentCache, Segment, SegmentStats


# ---------- Dataclasses ----------


class TestSegmentDataclass:
    def test_required_fields(self):
        s = Segment(doc_id="d1", segment_id="s1", content="hello")
        assert s.doc_id == "d1"
        assert s.segment_id == "s1"
        assert s.content == "hello"

    def test_defaults(self):
        s = Segment(doc_id="d", segment_id="s", content="x")
        assert s.stored_at == 0.0
        assert s.byte_size == 0
        assert s.hit_count == 0

    def test_custom_values(self):
        s = Segment(
            doc_id="d",
            segment_id="s",
            content="x",
            stored_at=1.5,
            byte_size=10,
            hit_count=3,
        )
        assert s.stored_at == 1.5
        assert s.byte_size == 10
        assert s.hit_count == 3

    def test_equality(self):
        a = Segment("d", "s", "x", 1.0, 1, 0)
        b = Segment("d", "s", "x", 1.0, 1, 0)
        assert a == b

    def test_inequality(self):
        a = Segment("d", "s", "x")
        b = Segment("d", "s", "y")
        assert a != b


class TestSegmentStatsDataclass:
    def test_required_fields(self):
        st = SegmentStats(total_segments=1, unique_docs=2, total_size_bytes=3, total_hits=4)
        assert st.total_segments == 1
        assert st.unique_docs == 2
        assert st.total_size_bytes == 3
        assert st.total_hits == 4

    def test_equality(self):
        a = SegmentStats(0, 0, 0, 0)
        b = SegmentStats(0, 0, 0, 0)
        assert a == b

    def test_zero_state(self):
        st = SegmentStats(0, 0, 0, 0)
        assert st.total_segments == 0


# ---------- Construction ----------


class TestConstruction:
    def test_construct_empty(self):
        c = DocSegmentCache()
        assert c.stats().total_segments == 0

    def test_independent_instances(self):
        a = DocSegmentCache()
        b = DocSegmentCache()
        a.store("d", "s", "x")
        assert b.stats().total_segments == 0

    def test_empty_doc_ids(self):
        c = DocSegmentCache()
        assert c.all_doc_ids() == []


# ---------- Store ----------


class TestStore:
    def test_store_new_returns_segment(self):
        c = DocSegmentCache()
        seg = c.store("d1", "s1", "hello")
        assert isinstance(seg, Segment)
        assert seg.doc_id == "d1"
        assert seg.segment_id == "s1"
        assert seg.content == "hello"

    def test_store_byte_size_ascii(self):
        c = DocSegmentCache()
        seg = c.store("d", "s", "hello")
        assert seg.byte_size == 5

    def test_store_byte_size_unicode(self):
        c = DocSegmentCache()
        seg = c.store("d", "s", "привет")
        assert seg.byte_size == len("привет".encode("utf-8"))

    def test_store_byte_size_empty(self):
        c = DocSegmentCache()
        seg = c.store("d", "s", "")
        assert seg.byte_size == 0

    def test_store_replace(self):
        c = DocSegmentCache()
        c.store("d", "s", "a")
        c.store("d", "s", "bb")
        assert c.peek("d", "s").content == "bb"
        assert c.stats().total_segments == 1

    def test_store_replace_resets_hits(self):
        c = DocSegmentCache()
        c.store("d", "s", "a")
        c.get("d", "s")
        c.get("d", "s")
        c.store("d", "s", "b")
        assert c.peek("d", "s").hit_count == 0

    def test_store_sets_stored_at_default(self):
        c = DocSegmentCache()
        seg = c.store("d", "s", "x")
        assert seg.stored_at > 0.0

    def test_store_sets_stored_at_explicit(self):
        c = DocSegmentCache()
        seg = c.store("d", "s", "x", now=42.5)
        assert seg.stored_at == 42.5

    def test_store_multiple_segments(self):
        c = DocSegmentCache()
        c.store("d", "s1", "a")
        c.store("d", "s2", "b")
        assert c.stats().total_segments == 2

    def test_store_multiple_docs(self):
        c = DocSegmentCache()
        c.store("d1", "s", "a")
        c.store("d2", "s", "b")
        assert c.stats().unique_docs == 2


# ---------- Get ----------


class TestGet:
    def test_get_returns_content(self):
        c = DocSegmentCache()
        c.store("d", "s", "hello")
        assert c.get("d", "s") == "hello"

    def test_get_missing_returns_none(self):
        c = DocSegmentCache()
        assert c.get("d", "s") is None

    def test_get_missing_doc(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        assert c.get("other", "s") is None

    def test_get_increments_hit_count(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        c.get("d", "s")
        assert c.peek("d", "s").hit_count == 1

    def test_get_multiple_increments(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        for _ in range(5):
            c.get("d", "s")
        assert c.peek("d", "s").hit_count == 5

    def test_get_missing_no_increment(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        c.get("d", "missing")
        assert c.peek("d", "s").hit_count == 0


# ---------- Peek ----------


class TestPeek:
    def test_peek_returns_segment(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        seg = c.peek("d", "s")
        assert isinstance(seg, Segment)
        assert seg.content == "x"

    def test_peek_missing_returns_none(self):
        c = DocSegmentCache()
        assert c.peek("d", "s") is None

    def test_peek_does_not_increment(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        c.peek("d", "s")
        c.peek("d", "s")
        assert c.peek("d", "s").hit_count == 0


# ---------- Delete ----------


class TestDelete:
    def test_delete_existing_returns_true(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        assert c.delete("d", "s") is True

    def test_delete_missing_returns_false(self):
        c = DocSegmentCache()
        assert c.delete("d", "s") is False

    def test_delete_removes(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        c.delete("d", "s")
        assert not c.exists("d", "s")

    def test_delete_cleans_by_doc(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        c.delete("d", "s")
        assert c.all_doc_ids() == []

    def test_delete_partial_keeps_others(self):
        c = DocSegmentCache()
        c.store("d", "s1", "a")
        c.store("d", "s2", "b")
        c.delete("d", "s1")
        assert c.exists("d", "s2")
        assert "d" in c.all_doc_ids()


# ---------- Delete doc ----------


class TestDeleteDoc:
    def test_delete_doc_returns_count(self):
        c = DocSegmentCache()
        c.store("d", "s1", "a")
        c.store("d", "s2", "b")
        assert c.delete_doc("d") == 2

    def test_delete_doc_missing_returns_zero(self):
        c = DocSegmentCache()
        assert c.delete_doc("nope") == 0

    def test_delete_doc_removes_all(self):
        c = DocSegmentCache()
        c.store("d", "s1", "a")
        c.store("d", "s2", "b")
        c.delete_doc("d")
        assert c.stats().total_segments == 0

    def test_delete_doc_keeps_other_docs(self):
        c = DocSegmentCache()
        c.store("d1", "s", "a")
        c.store("d2", "s", "b")
        c.delete_doc("d1")
        assert c.exists("d2", "s")


# ---------- Exists ----------


class TestExists:
    def test_exists_true(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        assert c.exists("d", "s") is True

    def test_exists_false(self):
        c = DocSegmentCache()
        assert c.exists("d", "s") is False

    def test_exists_after_delete(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        c.delete("d", "s")
        assert c.exists("d", "s") is False


# ---------- segments_for_doc ----------


class TestSegmentsForDoc:
    def test_empty_doc(self):
        c = DocSegmentCache()
        assert c.segments_for_doc("d") == []

    def test_sorted_by_segment_id(self):
        c = DocSegmentCache()
        c.store("d", "s3", "c")
        c.store("d", "s1", "a")
        c.store("d", "s2", "b")
        ids = [s.segment_id for s in c.segments_for_doc("d")]
        assert ids == ["s1", "s2", "s3"]

    def test_only_current_doc(self):
        c = DocSegmentCache()
        c.store("d1", "s", "a")
        c.store("d2", "s", "b")
        segs = c.segments_for_doc("d1")
        assert len(segs) == 1
        assert segs[0].content == "a"


# ---------- total_size_for_doc ----------


class TestTotalSizeForDoc:
    def test_no_segments(self):
        c = DocSegmentCache()
        assert c.total_size_for_doc("d") == 0

    def test_sum(self):
        c = DocSegmentCache()
        c.store("d", "s1", "abc")  # 3
        c.store("d", "s2", "defg")  # 4
        assert c.total_size_for_doc("d") == 7

    def test_excludes_other_docs(self):
        c = DocSegmentCache()
        c.store("d1", "s", "abc")
        c.store("d2", "s", "defgh")
        assert c.total_size_for_doc("d1") == 3


# ---------- most_accessed ----------


class TestMostAccessed:
    def test_empty(self):
        c = DocSegmentCache()
        assert c.most_accessed() == []

    def test_sorted_desc(self):
        c = DocSegmentCache()
        c.store("d", "s1", "a")
        c.store("d", "s2", "b")
        c.store("d", "s3", "c")
        for _ in range(3):
            c.get("d", "s2")
        c.get("d", "s1")
        order = [s.segment_id for s in c.most_accessed()]
        assert order[0] == "s2"
        assert order[1] == "s1"
        assert order[2] == "s3"

    def test_limit(self):
        c = DocSegmentCache()
        for i in range(5):
            c.store("d", f"s{i}", "x")
        assert len(c.most_accessed(limit=3)) == 3

    def test_tiebreak(self):
        c = DocSegmentCache()
        c.store("d2", "s2", "x")
        c.store("d1", "s1", "x")
        c.store("d1", "s2", "x")
        result = c.most_accessed()
        keys = [(s.doc_id, s.segment_id) for s in result]
        assert keys == [("d1", "s1"), ("d1", "s2"), ("d2", "s2")]


# ---------- all_doc_ids ----------


class TestAllDocIds:
    def test_empty(self):
        c = DocSegmentCache()
        assert c.all_doc_ids() == []

    def test_sorted_unique(self):
        c = DocSegmentCache()
        c.store("z", "s", "x")
        c.store("a", "s", "x")
        c.store("m", "s", "x")
        c.store("a", "s2", "x")  # dup doc
        assert c.all_doc_ids() == ["a", "m", "z"]

    def test_after_delete(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        c.delete("d", "s")
        assert c.all_doc_ids() == []


# ---------- Clear ----------


class TestClear:
    def test_clear_empty(self):
        c = DocSegmentCache()
        assert c.clear() == 0

    def test_clear_returns_count(self):
        c = DocSegmentCache()
        c.store("d", "s1", "x")
        c.store("d", "s2", "y")
        c.store("d2", "s", "z")
        assert c.clear() == 3

    def test_clear_resets(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")
        c.clear()
        assert c.stats().total_segments == 0
        assert c.all_doc_ids() == []


# ---------- Stats ----------


class TestStats:
    def test_empty_stats(self):
        c = DocSegmentCache()
        st = c.stats()
        assert st == SegmentStats(0, 0, 0, 0)

    def test_totals(self):
        c = DocSegmentCache()
        c.store("d1", "s1", "ab")  # 2 bytes
        c.store("d1", "s2", "cde")  # 3 bytes
        c.store("d2", "s1", "f")  # 1 byte
        c.get("d1", "s1")
        c.get("d1", "s1")
        c.get("d2", "s1")
        st = c.stats()
        assert st.total_segments == 3
        assert st.unique_docs == 2
        assert st.total_size_bytes == 6
        assert st.total_hits == 3

    def test_stats_after_delete(self):
        c = DocSegmentCache()
        c.store("d", "s", "ab")
        c.delete("d", "s")
        assert c.stats() == SegmentStats(0, 0, 0, 0)


# ---------- Thread safety ----------


class TestThreadSafety:
    def test_concurrent_store(self):
        c = DocSegmentCache()
        N = 50
        T = 8

        def worker(tid):
            for i in range(N):
                c.store(f"d{tid}", f"s{i}", f"content-{tid}-{i}")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(T)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        st = c.stats()
        assert st.total_segments == N * T
        assert st.unique_docs == T

    def test_concurrent_get_and_store(self):
        c = DocSegmentCache()
        c.store("d", "s", "x")

        def reader():
            for _ in range(200):
                c.get("d", "s")

        def writer():
            for i in range(100):
                c.store("d", f"s{i}", "y")

        threads = [
            threading.Thread(target=reader),
            threading.Thread(target=reader),
            threading.Thread(target=writer),
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        # No crash and stats are consistent.
        st = c.stats()
        assert st.total_segments >= 1
