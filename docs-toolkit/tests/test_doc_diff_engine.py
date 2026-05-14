"""Tests for E322 DocDiffEngine."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_diff_engine import (
    DiffLine,
    DiffResult,
    DiffStats,
    DocDiffEngine,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------
class TestDiffLineDataclass:
    def test_minimal(self):
        ln = DiffLine(op="equal", line="hello")
        assert ln.op == "equal"
        assert ln.line == "hello"
        assert ln.line_number_a is None
        assert ln.line_number_b is None

    def test_with_line_numbers(self):
        ln = DiffLine(op="equal", line="x", line_number_a=1, line_number_b=2)
        assert ln.line_number_a == 1
        assert ln.line_number_b == 2

    def test_insert(self):
        ln = DiffLine(op="insert", line="new", line_number_b=3)
        assert ln.op == "insert"
        assert ln.line_number_a is None
        assert ln.line_number_b == 3

    def test_delete(self):
        ln = DiffLine(op="delete", line="old", line_number_a=5)
        assert ln.op == "delete"
        assert ln.line_number_a == 5
        assert ln.line_number_b is None

    def test_equality(self):
        a = DiffLine(op="equal", line="x", line_number_a=1, line_number_b=1)
        b = DiffLine(op="equal", line="x", line_number_a=1, line_number_b=1)
        assert a == b


class TestDiffResultDataclass:
    def test_minimal(self):
        r = DiffResult(doc_id="d", version_a="v1", version_b="v2")
        assert r.doc_id == "d"
        assert r.version_a == "v1"
        assert r.version_b == "v2"
        assert r.lines == []
        assert r.additions == 0
        assert r.deletions == 0
        assert r.computed_at == 0.0

    def test_with_lines(self):
        ln = DiffLine(op="equal", line="x")
        r = DiffResult(
            doc_id="d",
            version_a="a",
            version_b="b",
            lines=[ln],
            additions=2,
            deletions=3,
            computed_at=100.5,
        )
        assert r.lines == [ln]
        assert r.additions == 2
        assert r.deletions == 3
        assert r.computed_at == 100.5

    def test_default_lines_independent(self):
        r1 = DiffResult(doc_id="a", version_a="1", version_b="2")
        r2 = DiffResult(doc_id="b", version_a="1", version_b="2")
        r1.lines.append(DiffLine(op="equal", line="x"))
        assert r2.lines == []


class TestDiffStatsDataclass:
    def test_defaults(self):
        s = DiffStats()
        assert s.total_diffs == 0
        assert s.unique_docs == 0

    def test_explicit(self):
        s = DiffStats(total_diffs=5, unique_docs=3)
        assert s.total_diffs == 5
        assert s.unique_docs == 3


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_construct(self):
        eng = DocDiffEngine()
        assert isinstance(eng, DocDiffEngine)

    def test_starts_empty(self):
        eng = DocDiffEngine()
        s = eng.stats()
        assert s.total_diffs == 0
        assert s.unique_docs == 0

    def test_separate_instances_isolated(self):
        a = DocDiffEngine()
        b = DocDiffEngine()
        a.compute("d", "v1", "x", "v2", "y")
        assert b.stats().total_diffs == 0


# ---------------------------------------------------------------------------
# Compute
# ---------------------------------------------------------------------------
class TestCompute:
    def test_identical_all_equal(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb\nc", "v2", "a\nb\nc")
        assert all(ln.op == "equal" for ln in r.lines)
        assert r.additions == 0
        assert r.deletions == 0

    def test_identical_line_count(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb\nc", "v2", "a\nb\nc")
        assert len(r.lines) == 3

    def test_addition_detected(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb", "v2", "a\nb\nc")
        assert r.additions == 1
        assert r.deletions == 0
        ops = [ln.op for ln in r.lines]
        assert "insert" in ops

    def test_deletion_detected(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb\nc", "v2", "a\nb")
        assert r.deletions == 1
        assert r.additions == 0
        ops = [ln.op for ln in r.lines]
        assert "delete" in ops

    def test_both_addition_and_deletion(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb\nc", "v2", "a\nx\nc")
        assert r.additions >= 1
        assert r.deletions >= 1

    def test_line_number_a_for_equal(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb", "v2", "a\nb")
        for i, ln in enumerate(r.lines, start=1):
            assert ln.line_number_a == i
            assert ln.line_number_b == i

    def test_line_number_for_insert_only_b(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a", "v2", "a\nb")
        inserts = [ln for ln in r.lines if ln.op == "insert"]
        assert len(inserts) == 1
        assert inserts[0].line_number_a is None
        assert inserts[0].line_number_b == 2

    def test_line_number_for_delete_only_a(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb", "v2", "a")
        dels = [ln for ln in r.lines if ln.op == "delete"]
        assert len(dels) == 1
        assert dels[0].line_number_a == 2
        assert dels[0].line_number_b is None

    def test_empty_strings(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "", "v2", "")
        assert r.additions == 0
        assert r.deletions == 0

    def test_empty_to_content(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "", "v2", "a\nb")
        assert r.additions >= 1

    def test_content_to_empty(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb", "v2", "")
        assert r.deletions >= 1

    def test_computed_at_set(self):
        eng = DocDiffEngine()
        before = time.time()
        r = eng.compute("d", "v1", "x", "v2", "y")
        after = time.time()
        assert before <= r.computed_at <= after

    def test_computed_at_explicit(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "x", "v2", "y", now=42.5)
        assert r.computed_at == 42.5

    def test_doc_id_stored(self):
        eng = DocDiffEngine()
        r = eng.compute("mydoc", "v1", "x", "v2", "y")
        assert r.doc_id == "mydoc"

    def test_version_labels_stored(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "draft", "x", "final", "y")
        assert r.version_a == "draft"
        assert r.version_b == "final"


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
class TestCache:
    def test_cache_true_stores(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y", cache=True)
        assert eng.stats().total_diffs == 1

    def test_cache_false_skips(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y", cache=False)
        assert eng.stats().total_diffs == 0

    def test_repeat_compute_overwrites(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y")
        eng.compute("d", "v1", "x", "v2", "y")
        assert eng.stats().total_diffs == 1

    def test_different_versions_distinct_entries(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y")
        eng.compute("d", "v2", "y", "v3", "z")
        assert eng.stats().total_diffs == 2

    def test_cached_is_same_object(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "x", "v2", "y")
        cached = eng.get_cached("d", "v1", "v2")
        assert cached is r


# ---------------------------------------------------------------------------
# get_cached
# ---------------------------------------------------------------------------
class TestGetCached:
    def test_found(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y")
        assert eng.get_cached("d", "v1", "v2") is not None

    def test_not_found(self):
        eng = DocDiffEngine()
        assert eng.get_cached("d", "v1", "v2") is None

    def test_not_found_after_cache_false(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y", cache=False)
        assert eng.get_cached("d", "v1", "v2") is None

    def test_wrong_doc_id(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y")
        assert eng.get_cached("other", "v1", "v2") is None

    def test_wrong_version(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y")
        assert eng.get_cached("d", "v1", "v3") is None


# ---------------------------------------------------------------------------
# Invalidate
# ---------------------------------------------------------------------------
class TestInvalidate:
    def test_returns_count(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y")
        eng.compute("d", "v2", "y", "v3", "z")
        assert eng.invalidate("d") == 2

    def test_doc_specific_only(self):
        eng = DocDiffEngine()
        eng.compute("d1", "v1", "x", "v2", "y")
        eng.compute("d2", "v1", "x", "v2", "y")
        removed = eng.invalidate("d1")
        assert removed == 1
        assert eng.get_cached("d2", "v1", "v2") is not None

    def test_missing_doc_returns_zero(self):
        eng = DocDiffEngine()
        assert eng.invalidate("nope") == 0

    def test_after_invalidate_get_cached_is_none(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y")
        eng.invalidate("d")
        assert eng.get_cached("d", "v1", "v2") is None


# ---------------------------------------------------------------------------
# Invalidate all
# ---------------------------------------------------------------------------
class TestInvalidateAll:
    def test_clears(self):
        eng = DocDiffEngine()
        eng.compute("d1", "v1", "x", "v2", "y")
        eng.compute("d2", "v1", "x", "v2", "y")
        eng.invalidate_all()
        assert eng.stats().total_diffs == 0

    def test_returns_count(self):
        eng = DocDiffEngine()
        eng.compute("d1", "v1", "x", "v2", "y")
        eng.compute("d2", "v1", "x", "v2", "y")
        assert eng.invalidate_all() == 2

    def test_empty_returns_zero(self):
        eng = DocDiffEngine()
        assert eng.invalidate_all() == 0

    def test_safe_to_call_twice(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y")
        eng.invalidate_all()
        assert eng.invalidate_all() == 0


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
class TestSummary:
    def test_keys(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a", "v2", "a")
        s = eng.summary(r)
        assert set(s.keys()) == {"additions", "deletions", "unchanged"}

    def test_all_equal(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb\nc", "v2", "a\nb\nc")
        s = eng.summary(r)
        assert s["unchanged"] == 3
        assert s["additions"] == 0
        assert s["deletions"] == 0

    def test_additions(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a", "v2", "a\nb\nc")
        s = eng.summary(r)
        assert s["additions"] == 2

    def test_deletions(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb\nc", "v2", "a")
        s = eng.summary(r)
        assert s["deletions"] == 2

    def test_unchanged_count_matches_equal_lines(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb\nc", "v2", "a\nx\nc")
        s = eng.summary(r)
        equal_count = sum(1 for ln in r.lines if ln.op == "equal")
        assert s["unchanged"] == equal_count


# ---------------------------------------------------------------------------
# as_text
# ---------------------------------------------------------------------------
class TestAsText:
    def test_equal_prefix(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "hello", "v2", "hello")
        text = eng.as_text(r)
        assert text.startswith("  hello")

    def test_insert_prefix(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "", "v2", "new")
        text = eng.as_text(r)
        assert "+ new" in text or text.startswith("+ ")

    def test_delete_prefix(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "old", "v2", "")
        text = eng.as_text(r)
        assert "- old" in text or text.startswith("- ")

    def test_joined_by_newline(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb", "v2", "a\nb")
        text = eng.as_text(r)
        assert "\n" in text

    def test_line_count_matches(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "a\nb\nc", "v2", "a\nb\nc")
        text = eng.as_text(r)
        assert len(text.split("\n")) == len(r.lines)

    def test_empty_diff(self):
        eng = DocDiffEngine()
        r = eng.compute("d", "v1", "", "v2", "")
        text = eng.as_text(r)
        # Either empty or two-space-prefixed empty lines, no exception
        assert isinstance(text, str)


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_returns_diffstats(self):
        eng = DocDiffEngine()
        assert isinstance(eng.stats(), DiffStats)

    def test_total_diffs(self):
        eng = DocDiffEngine()
        eng.compute("d1", "v1", "x", "v2", "y")
        eng.compute("d1", "v2", "y", "v3", "z")
        eng.compute("d2", "v1", "x", "v2", "y")
        assert eng.stats().total_diffs == 3

    def test_unique_docs(self):
        eng = DocDiffEngine()
        eng.compute("d1", "v1", "x", "v2", "y")
        eng.compute("d1", "v2", "y", "v3", "z")
        eng.compute("d2", "v1", "x", "v2", "y")
        assert eng.stats().unique_docs == 2

    def test_empty_engine(self):
        eng = DocDiffEngine()
        s = eng.stats()
        assert s.total_diffs == 0
        assert s.unique_docs == 0

    def test_after_invalidate(self):
        eng = DocDiffEngine()
        eng.compute("d", "v1", "x", "v2", "y")
        eng.invalidate("d")
        assert eng.stats().total_diffs == 0
        assert eng.stats().unique_docs == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_compute(self):
        eng = DocDiffEngine()

        def worker(i: int) -> None:
            for j in range(10):
                eng.compute(f"d{i}", f"v{j}", f"a{j}", f"v{j+1}", f"a{j+1}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Each worker writes 10 distinct (d{i}, v{j}, v{j+1}) keys
        assert eng.stats().total_diffs == 50
        assert eng.stats().unique_docs == 5

    def test_concurrent_invalidate(self):
        eng = DocDiffEngine()
        for i in range(20):
            eng.compute(f"d{i}", "v1", "x", "v2", "y")

        results: list[int] = []
        lock = threading.Lock()

        def worker(doc_id: str) -> None:
            removed = eng.invalidate(doc_id)
            with lock:
                results.append(removed)

        threads = [threading.Thread(target=worker, args=(f"d{i}",)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert sum(results) == 20
        assert eng.stats().total_diffs == 0

    def test_concurrent_mixed(self):
        eng = DocDiffEngine()

        def writer() -> None:
            for j in range(50):
                eng.compute("d", f"v{j}", "x", f"v{j+1}", "y")

        def reader() -> None:
            for _ in range(50):
                eng.stats()
                eng.get_cached("d", "v0", "v1")

        threads = [
            threading.Thread(target=writer),
            threading.Thread(target=reader),
            threading.Thread(target=writer),
            threading.Thread(target=reader),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # No exception — pass
        assert eng.stats().total_diffs >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
