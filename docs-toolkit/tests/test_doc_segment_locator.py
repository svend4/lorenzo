"""Tests for E386 DocSegmentLocator."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_segment_locator import (
    DocSegmentLocator,
    LocatorStats,
    Segment,
)


# ---------------------------------------------------------------------------
# Segment dataclass
# ---------------------------------------------------------------------------
class TestSegmentDataclass:
    def test_segment_basic_fields(self):
        seg = Segment(segment_id="s1", doc_id="d1", start=0, end=10)
        assert seg.segment_id == "s1"
        assert seg.doc_id == "d1"
        assert seg.start == 0
        assert seg.end == 10

    def test_segment_default_label_empty(self):
        seg = Segment(segment_id="s", doc_id="d", start=0, end=1)
        assert seg.label == ""

    def test_segment_default_metadata_empty(self):
        seg = Segment(segment_id="s", doc_id="d", start=0, end=1)
        assert seg.metadata == {}

    def test_segment_with_label_and_metadata(self):
        seg = Segment(
            segment_id="s",
            doc_id="d",
            start=2,
            end=5,
            label="L",
            metadata={"k": "v"},
        )
        assert seg.label == "L"
        assert seg.metadata == {"k": "v"}

    def test_segment_metadata_independent_per_instance(self):
        a = Segment(segment_id="a", doc_id="d", start=0, end=1)
        b = Segment(segment_id="b", doc_id="d", start=2, end=3)
        a.metadata["x"] = 1
        assert b.metadata == {}


# ---------------------------------------------------------------------------
# LocatorStats dataclass
# ---------------------------------------------------------------------------
class TestLocatorStatsDataclass:
    def test_stats_fields(self):
        s = LocatorStats(total_segments=3, unique_docs=2, total_length=20)
        assert s.total_segments == 3
        assert s.unique_docs == 2
        assert s.total_length == 20

    def test_stats_equality(self):
        a = LocatorStats(total_segments=1, unique_docs=1, total_length=5)
        b = LocatorStats(total_segments=1, unique_docs=1, total_length=5)
        assert a == b


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty_locator(self):
        loc = DocSegmentLocator()
        st = loc.stats()
        assert st.total_segments == 0
        assert st.unique_docs == 0
        assert st.total_length == 0

    def test_empty_locator_doc_ids(self):
        loc = DocSegmentLocator()
        assert loc.all_doc_ids() == []

    def test_empty_segments_for_doc(self):
        loc = DocSegmentLocator()
        assert loc.segments_for_doc("missing") == []


# ---------------------------------------------------------------------------
# register_segment
# ---------------------------------------------------------------------------
class TestRegisterSegment:
    def test_register_returns_segment(self):
        loc = DocSegmentLocator()
        seg = loc.register_segment("d1", "s1", 0, 10)
        assert isinstance(seg, Segment)
        assert seg.start == 0 and seg.end == 10

    def test_register_stores_segment(self):
        loc = DocSegmentLocator()
        loc.register_segment("d1", "s1", 0, 10)
        got = loc.get_segment("d1", "s1")
        assert got is not None
        assert got.segment_id == "s1"

    def test_register_with_label_metadata(self):
        loc = DocSegmentLocator()
        seg = loc.register_segment(
            "d1", "s1", 0, 5, label="head", metadata={"src": "x"}
        )
        assert seg.label == "head"
        assert seg.metadata == {"src": "x"}

    def test_register_metadata_copied(self):
        loc = DocSegmentLocator()
        meta = {"a": 1}
        loc.register_segment("d", "s", 0, 1, metadata=meta)
        meta["a"] = 999
        got = loc.get_segment("d", "s")
        assert got.metadata == {"a": 1}

    def test_register_replaces_existing(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 0, 5)
        loc.register_segment("d", "s", 10, 20)
        seg = loc.get_segment("d", "s")
        assert seg.start == 10 and seg.end == 20

    def test_register_replace_does_not_duplicate_in_doc(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 0, 5)
        loc.register_segment("d", "s", 10, 20)
        assert len(loc.segments_for_doc("d")) == 1

    def test_register_invalid_negative_start(self):
        loc = DocSegmentLocator()
        with pytest.raises(ValueError):
            loc.register_segment("d", "s", -1, 5)

    def test_register_invalid_end_eq_start(self):
        loc = DocSegmentLocator()
        with pytest.raises(ValueError):
            loc.register_segment("d", "s", 5, 5)

    def test_register_invalid_end_lt_start(self):
        loc = DocSegmentLocator()
        with pytest.raises(ValueError):
            loc.register_segment("d", "s", 10, 5)

    def test_register_multiple_docs(self):
        loc = DocSegmentLocator()
        loc.register_segment("a", "s1", 0, 5)
        loc.register_segment("b", "s1", 0, 5)
        assert loc.get_segment("a", "s1") is not None
        assert loc.get_segment("b", "s1") is not None


# ---------------------------------------------------------------------------
# remove_segment
# ---------------------------------------------------------------------------
class TestRemoveSegment:
    def test_remove_existing(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 0, 5)
        assert loc.remove_segment("d", "s") is True

    def test_remove_missing(self):
        loc = DocSegmentLocator()
        assert loc.remove_segment("d", "s") is False

    def test_remove_then_get(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 0, 5)
        loc.remove_segment("d", "s")
        assert loc.get_segment("d", "s") is None

    def test_remove_last_segment_clears_doc(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 0, 5)
        loc.remove_segment("d", "s")
        assert "d" not in loc.all_doc_ids()

    def test_remove_one_keeps_others(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s1", 0, 5)
        loc.register_segment("d", "s2", 10, 15)
        loc.remove_segment("d", "s1")
        remaining = loc.segments_for_doc("d")
        assert len(remaining) == 1
        assert remaining[0].segment_id == "s2"


# ---------------------------------------------------------------------------
# get_segment
# ---------------------------------------------------------------------------
class TestGetSegment:
    def test_get_existing(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 1, 4)
        seg = loc.get_segment("d", "s")
        assert seg is not None and seg.start == 1

    def test_get_missing_returns_none(self):
        loc = DocSegmentLocator()
        assert loc.get_segment("d", "s") is None

    def test_get_wrong_doc_returns_none(self):
        loc = DocSegmentLocator()
        loc.register_segment("a", "s", 0, 5)
        assert loc.get_segment("b", "s") is None


# ---------------------------------------------------------------------------
# segments_for_doc
# ---------------------------------------------------------------------------
class TestSegmentsForDoc:
    def test_returns_all_for_doc(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s1", 0, 5)
        loc.register_segment("d", "s2", 10, 15)
        assert len(loc.segments_for_doc("d")) == 2

    def test_sorted_by_start(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "b", 30, 40)
        loc.register_segment("d", "a", 0, 10)
        loc.register_segment("d", "c", 15, 20)
        result = loc.segments_for_doc("d")
        starts = [s.start for s in result]
        assert starts == sorted(starts)

    def test_isolated_per_doc(self):
        loc = DocSegmentLocator()
        loc.register_segment("a", "s", 0, 5)
        loc.register_segment("b", "s", 0, 5)
        assert len(loc.segments_for_doc("a")) == 1
        assert len(loc.segments_for_doc("b")) == 1


# ---------------------------------------------------------------------------
# segments_at
# ---------------------------------------------------------------------------
class TestSegmentsAt:
    def test_position_within(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 5, 15)
        assert len(loc.segments_at("d", 10)) == 1

    def test_position_at_start(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 5, 15)
        assert len(loc.segments_at("d", 5)) == 1

    def test_position_at_end_excluded(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 5, 15)
        assert loc.segments_at("d", 15) == []

    def test_position_before(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 5, 15)
        assert loc.segments_at("d", 4) == []

    def test_overlap_returns_all(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 20)
        loc.register_segment("d", "b", 5, 15)
        assert len(loc.segments_at("d", 10)) == 2

    def test_sorted_by_start(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "b", 5, 100)
        loc.register_segment("d", "a", 0, 50)
        result = loc.segments_at("d", 10)
        assert result[0].start <= result[1].start


# ---------------------------------------------------------------------------
# segments_in_range
# ---------------------------------------------------------------------------
class TestSegmentsInRange:
    def test_fully_inside(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 5, 10)
        assert len(loc.segments_in_range("d", 0, 100)) == 1

    def test_partial_overlap_left(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 0, 10)
        assert len(loc.segments_in_range("d", 5, 20)) == 1

    def test_partial_overlap_right(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 15, 25)
        assert len(loc.segments_in_range("d", 10, 20)) == 1

    def test_no_overlap_before(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 0, 5)
        assert loc.segments_in_range("d", 10, 20) == []

    def test_no_overlap_after(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 30, 40)
        assert loc.segments_in_range("d", 10, 20) == []

    def test_touching_end_excluded(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 10, 20)
        # range [20, 30) does not overlap [10, 20)
        assert loc.segments_in_range("d", 20, 30) == []

    def test_sorted(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "b", 50, 60)
        loc.register_segment("d", "a", 0, 10)
        result = loc.segments_in_range("d", 0, 100)
        assert [s.start for s in result] == [0, 50]


# ---------------------------------------------------------------------------
# segments_by_label
# ---------------------------------------------------------------------------
class TestSegmentsByLabel:
    def test_exact_match(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s1", 0, 5, label="head")
        loc.register_segment("d", "s2", 10, 15, label="body")
        result = loc.segments_by_label("d", "head")
        assert len(result) == 1 and result[0].segment_id == "s1"

    def test_no_match(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 0, 5, label="A")
        assert loc.segments_by_label("d", "B") == []

    def test_case_sensitive(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "s", 0, 5, label="Head")
        assert loc.segments_by_label("d", "head") == []

    def test_sorted_by_start(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "b", 50, 60, label="x")
        loc.register_segment("d", "a", 0, 10, label="x")
        result = loc.segments_by_label("d", "x")
        assert [s.start for s in result] == [0, 50]


# ---------------------------------------------------------------------------
# find_overlapping
# ---------------------------------------------------------------------------
class TestFindOverlapping:
    def test_no_overlap(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 5)
        loc.register_segment("d", "b", 10, 20)
        assert loc.find_overlapping("d") == []

    def test_single_overlap(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 10)
        loc.register_segment("d", "b", 5, 15)
        pairs = loc.find_overlapping("d")
        assert len(pairs) == 1

    def test_touching_not_overlap(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 10)
        loc.register_segment("d", "b", 10, 20)
        assert loc.find_overlapping("d") == []

    def test_multiple_overlaps_deduped(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 30)
        loc.register_segment("d", "b", 5, 15)
        loc.register_segment("d", "c", 20, 25)
        # a-b overlap, a-c overlap, b-c do not
        pairs = loc.find_overlapping("d")
        assert len(pairs) == 2

    def test_each_pair_once(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 10)
        loc.register_segment("d", "b", 5, 15)
        loc.register_segment("d", "c", 7, 9)
        pairs = loc.find_overlapping("d")
        seen = set()
        for x, y in pairs:
            key = tuple(sorted([x.segment_id, y.segment_id]))
            assert key not in seen
            seen.add(key)


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------
class TestClearDoc:
    def test_count_cleared(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 5)
        loc.register_segment("d", "b", 10, 15)
        assert loc.clear_doc("d") == 2

    def test_after_clear_empty(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 5)
        loc.clear_doc("d")
        assert loc.segments_for_doc("d") == []

    def test_clear_unknown_doc_returns_zero(self):
        loc = DocSegmentLocator()
        assert loc.clear_doc("missing") == 0

    def test_clear_isolated_to_doc(self):
        loc = DocSegmentLocator()
        loc.register_segment("a", "s", 0, 5)
        loc.register_segment("b", "s", 0, 5)
        loc.clear_doc("a")
        assert loc.get_segment("b", "s") is not None


# ---------------------------------------------------------------------------
# merge_adjacent
# ---------------------------------------------------------------------------
class TestMergeAdjacent:
    def test_simple_merge(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 5, label="x")
        loc.register_segment("d", "b", 5, 10, label="x")
        count = loc.merge_adjacent("d", "x")
        assert count == 1

    def test_after_merge_one_segment(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 5, label="x")
        loc.register_segment("d", "b", 5, 10, label="x")
        loc.merge_adjacent("d", "x")
        segs = loc.segments_by_label("d", "x")
        assert len(segs) == 1
        assert segs[0].start == 0 and segs[0].end == 10

    def test_chain_merge(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 5, label="x")
        loc.register_segment("d", "b", 5, 10, label="x")
        loc.register_segment("d", "c", 10, 15, label="x")
        count = loc.merge_adjacent("d", "x")
        assert count == 2
        segs = loc.segments_by_label("d", "x")
        assert len(segs) == 1 and segs[0].end == 15

    def test_gap_no_merge(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 5, label="x")
        loc.register_segment("d", "b", 6, 10, label="x")
        assert loc.merge_adjacent("d", "x") == 0

    def test_different_labels_not_merged(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 5, label="x")
        loc.register_segment("d", "b", 5, 10, label="y")
        assert loc.merge_adjacent("d", "x") == 0

    def test_no_segments(self):
        loc = DocSegmentLocator()
        assert loc.merge_adjacent("d", "x") == 0


# ---------------------------------------------------------------------------
# total_coverage
# ---------------------------------------------------------------------------
class TestTotalCoverage:
    def test_single_segment(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 10)
        assert loc.total_coverage("d") == 10

    def test_disjoint(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 5)
        loc.register_segment("d", "b", 10, 15)
        assert loc.total_coverage("d") == 10

    def test_overlap_dedup(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 10)
        loc.register_segment("d", "b", 5, 15)
        assert loc.total_coverage("d") == 15

    def test_nested(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 100)
        loc.register_segment("d", "b", 10, 20)
        assert loc.total_coverage("d") == 100

    def test_touching_segments(self):
        loc = DocSegmentLocator()
        loc.register_segment("d", "a", 0, 5)
        loc.register_segment("d", "b", 5, 10)
        assert loc.total_coverage("d") == 10

    def test_empty(self):
        loc = DocSegmentLocator()
        assert loc.total_coverage("d") == 0


# ---------------------------------------------------------------------------
# all_doc_ids
# ---------------------------------------------------------------------------
class TestAllDocIds:
    def test_sorted(self):
        loc = DocSegmentLocator()
        loc.register_segment("c", "s", 0, 1)
        loc.register_segment("a", "s", 0, 1)
        loc.register_segment("b", "s", 0, 1)
        assert loc.all_doc_ids() == ["a", "b", "c"]

    def test_unique(self):
        loc = DocSegmentLocator()
        loc.register_segment("a", "s1", 0, 5)
        loc.register_segment("a", "s2", 10, 15)
        assert loc.all_doc_ids() == ["a"]

    def test_empty(self):
        loc = DocSegmentLocator()
        assert loc.all_doc_ids() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty(self):
        loc = DocSegmentLocator()
        st = loc.stats()
        assert (st.total_segments, st.unique_docs, st.total_length) == (0, 0, 0)

    def test_totals(self):
        loc = DocSegmentLocator()
        loc.register_segment("a", "s1", 0, 10)
        loc.register_segment("a", "s2", 20, 25)
        loc.register_segment("b", "s1", 0, 7)
        st = loc.stats()
        assert st.total_segments == 3
        assert st.unique_docs == 2
        assert st.total_length == 10 + 5 + 7

    def test_after_remove(self):
        loc = DocSegmentLocator()
        loc.register_segment("a", "s", 0, 10)
        loc.remove_segment("a", "s")
        st = loc.stats()
        assert st.total_segments == 0
        assert st.total_length == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_register(self):
        loc = DocSegmentLocator()
        n_threads = 8
        per_thread = 50

        def worker(tid: int) -> None:
            for i in range(per_thread):
                loc.register_segment(
                    f"d{tid}", f"s{i}", i * 10, i * 10 + 5
                )

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        st = loc.stats()
        assert st.total_segments == n_threads * per_thread
        assert st.unique_docs == n_threads

    def test_concurrent_register_same_doc(self):
        loc = DocSegmentLocator()
        n_threads = 6
        per_thread = 40

        def worker(tid: int) -> None:
            for i in range(per_thread):
                loc.register_segment(
                    "shared", f"t{tid}-s{i}", i * 10, i * 10 + 5
                )

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        segs = loc.segments_for_doc("shared")
        assert len(segs) == n_threads * per_thread
