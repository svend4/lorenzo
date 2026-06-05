"""Tests for docstoolkit.doc_word_index (E293).

Coverage: IndexEntry, SearchResult, IndexStats dataclasses; DocWordIndex
methods index_doc, remove_doc, search, search_multi, get_entry, words_in_doc,
docs_count, word_count, top_words, stats; and thread-safety.
"""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_word_index import (
    DocWordIndex,
    IndexEntry,
    IndexStats,
    SearchResult,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestIndexEntry:
    def test_fields(self):
        e = IndexEntry(doc_id="d1", word="hello", positions=[0, 6], frequency=2)
        assert e.doc_id == "d1"
        assert e.word == "hello"
        assert e.positions == [0, 6]
        assert e.frequency == 2

    def test_equality(self):
        e1 = IndexEntry("d", "w", [0], 1)
        e2 = IndexEntry("d", "w", [0], 1)
        assert e1 == e2

    def test_inequality(self):
        assert IndexEntry("d", "w", [0], 1) != IndexEntry("d", "w", [1], 1)


class TestSearchResult:
    def test_fields(self):
        r = SearchResult(doc_id="d1", word="foo", frequency=3, positions=[0, 4, 8], score=3.0)
        assert r.doc_id == "d1"
        assert r.word == "foo"
        assert r.frequency == 3
        assert r.positions == [0, 4, 8]
        assert r.score == pytest.approx(3.0)

    def test_equality(self):
        r1 = SearchResult("d", "w", 1, [0], 1.0)
        r2 = SearchResult("d", "w", 1, [0], 1.0)
        assert r1 == r2


class TestIndexStats:
    def test_fields(self):
        s = IndexStats(total_docs=2, total_words=5, total_entries=8, avg_words_per_doc=4.0)
        assert s.total_docs == 2
        assert s.total_words == 5
        assert s.total_entries == 8
        assert s.avg_words_per_doc == pytest.approx(4.0)


# ---------------------------------------------------------------------------
# index_doc
# ---------------------------------------------------------------------------


class TestIndexDoc:
    def test_returns_unique_word_count(self):
        idx = DocWordIndex()
        assert idx.index_doc("d1", "hello world hello") == 2

    def test_empty_content_returns_zero(self):
        idx = DocWordIndex()
        assert idx.index_doc("d1", "") == 0

    def test_empty_content_still_registers_doc(self):
        idx = DocWordIndex()
        idx.index_doc("d1", "")
        assert idx.docs_count() == 1

    def test_increments_docs_count(self):
        idx = DocWordIndex()
        idx.index_doc("a", "foo")
        idx.index_doc("b", "bar")
        assert idx.docs_count() == 2

    def test_lowercase_normalization(self):
        idx = DocWordIndex()
        idx.index_doc("d", "Hello WORLD")
        r = idx.search("hello")
        assert len(r) == 1
        assert r[0].word == "hello"

    def test_position_tracking(self):
        idx = DocWordIndex()
        idx.index_doc("d", "foo bar foo")
        entry = idx.get_entry("d", "foo")
        assert entry is not None
        # "foo" starts at char 0 and char 8
        assert 0 in entry.positions
        assert 8 in entry.positions

    def test_reindex_replaces_old_entries(self):
        idx = DocWordIndex()
        idx.index_doc("d", "alpha beta")
        idx.index_doc("d", "gamma delta")
        assert idx.search("alpha") == []
        assert len(idx.search("gamma")) == 1

    def test_reindex_does_not_increase_docs_count(self):
        idx = DocWordIndex()
        idx.index_doc("d", "alpha")
        idx.index_doc("d", "beta")
        assert idx.docs_count() == 1

    def test_min_word_len_filters_short_words(self):
        idx = DocWordIndex(min_word_len=3)
        idx.index_doc("d", "a bb ccc dddd")
        words = idx.words_in_doc("d")
        assert "a" not in words
        assert "bb" not in words
        assert "ccc" in words
        assert "dddd" in words

    def test_min_word_len_default_filters_single_chars(self):
        idx = DocWordIndex()  # default min_word_len=2
        idx.index_doc("d", "a bb ccc")
        assert "a" not in idx.words_in_doc("d")
        assert "bb" in idx.words_in_doc("d")

    def test_unicode_content(self):
        idx = DocWordIndex()
        idx.index_doc("d", "привет мир")
        assert "привет" in idx.words_in_doc("d")
        assert "мир" in idx.words_in_doc("d")

    def test_numbers_indexed(self):
        idx = DocWordIndex()
        idx.index_doc("d", "version 42 release")
        assert "42" in idx.words_in_doc("d")


# ---------------------------------------------------------------------------
# remove_doc
# ---------------------------------------------------------------------------


class TestRemoveDoc:
    def test_returns_count_of_removed_words(self):
        idx = DocWordIndex()
        idx.index_doc("d", "alpha beta gamma")
        assert idx.remove_doc("d") == 3

    def test_removes_doc(self):
        idx = DocWordIndex()
        idx.index_doc("d", "alpha")
        idx.remove_doc("d")
        assert idx.docs_count() == 0

    def test_missing_doc_returns_zero(self):
        idx = DocWordIndex()
        assert idx.remove_doc("nope") == 0

    def test_removes_word_entries(self):
        idx = DocWordIndex()
        idx.index_doc("d", "alpha beta")
        idx.remove_doc("d")
        assert idx.search("alpha") == []
        assert idx.word_count() == 0

    def test_other_docs_unaffected(self):
        idx = DocWordIndex()
        idx.index_doc("a", "alpha")
        idx.index_doc("b", "alpha")
        idx.remove_doc("a")
        results = idx.search("alpha")
        assert len(results) == 1
        assert results[0].doc_id == "b"

    def test_word_count_decreases_when_word_only_in_removed_doc(self):
        idx = DocWordIndex()
        idx.index_doc("a", "unique")
        idx.index_doc("b", "shared")
        idx.remove_doc("a")
        assert idx.word_count() == 1


# ---------------------------------------------------------------------------
# search
# ---------------------------------------------------------------------------


class TestSearch:
    def test_basic_search(self):
        idx = DocWordIndex()
        idx.index_doc("d", "hello world")
        results = idx.search("hello")
        assert len(results) == 1
        assert results[0].doc_id == "d"

    def test_missing_word_returns_empty(self):
        idx = DocWordIndex()
        idx.index_doc("d", "hello")
        assert idx.search("missing") == []

    def test_sorted_by_frequency_desc(self):
        idx = DocWordIndex()
        idx.index_doc("low", "hello")
        idx.index_doc("high", "hello hello hello")
        results = idx.search("hello")
        assert results[0].doc_id == "high"
        assert results[1].doc_id == "low"

    def test_frequency_and_positions_set(self):
        idx = DocWordIndex()
        idx.index_doc("d", "go go go")
        r = idx.search("go")[0]
        assert r.frequency == 3
        assert len(r.positions) == 3

    def test_score_equals_frequency(self):
        idx = DocWordIndex()
        idx.index_doc("d", "yes yes")
        r = idx.search("yes")[0]
        assert r.score == pytest.approx(r.frequency)

    def test_limit_caps_results(self):
        idx = DocWordIndex()
        for i in range(5):
            idx.index_doc(f"d{i}", "word")
        results = idx.search("word", limit=3)
        assert len(results) == 3

    def test_case_insensitive_search(self):
        idx = DocWordIndex()
        idx.index_doc("d", "Hello HELLO hello")
        r = idx.search("HELLO")
        assert r[0].frequency == 3

    def test_word_field_lowercased(self):
        idx = DocWordIndex()
        idx.index_doc("d", "Python")
        r = idx.search("Python")
        assert r[0].word == "python"


# ---------------------------------------------------------------------------
# search_multi
# ---------------------------------------------------------------------------


class TestSearchMulti:
    def test_any_mode_union(self):
        idx = DocWordIndex()
        idx.index_doc("a", "alpha")
        idx.index_doc("b", "beta")
        idx.index_doc("c", "gamma")
        result = idx.search_multi(["alpha", "beta"], mode="any")
        assert sorted(result) == ["a", "b"]

    def test_all_mode_intersection(self):
        idx = DocWordIndex()
        idx.index_doc("a", "alpha beta")
        idx.index_doc("b", "alpha")
        idx.index_doc("c", "alpha beta gamma")
        result = idx.search_multi(["alpha", "beta"], mode="all")
        assert sorted(result) == ["a", "c"]

    def test_any_empty_words_returns_empty(self):
        idx = DocWordIndex()
        idx.index_doc("d", "x")
        assert idx.search_multi([], mode="any") == []

    def test_all_empty_words_returns_empty(self):
        idx = DocWordIndex()
        idx.index_doc("d", "x")
        assert idx.search_multi([], mode="all") == []

    def test_all_missing_word_returns_empty(self):
        idx = DocWordIndex()
        idx.index_doc("d", "alpha")
        assert idx.search_multi(["alpha", "missing"], mode="all") == []

    def test_result_sorted_by_doc_id(self):
        idx = DocWordIndex()
        for ch in ["c", "a", "b"]:
            idx.index_doc(ch, "word")
        result = idx.search_multi(["word"], mode="any")
        assert result == ["a", "b", "c"]

    def test_any_deduplicates_doc_ids(self):
        idx = DocWordIndex()
        idx.index_doc("d", "alpha beta")
        result = idx.search_multi(["alpha", "beta"], mode="any")
        assert result == ["d"]

    def test_any_single_word(self):
        idx = DocWordIndex()
        idx.index_doc("d", "hello hello")
        assert idx.search_multi(["hello"]) == ["d"]

    def test_all_three_words(self):
        idx = DocWordIndex()
        idx.index_doc("a", "foo bar baz")
        idx.index_doc("b", "foo bar")
        result = idx.search_multi(["foo", "bar", "baz"], mode="all")
        assert result == ["a"]


# ---------------------------------------------------------------------------
# get_entry
# ---------------------------------------------------------------------------


class TestGetEntry:
    def test_returns_entry(self):
        idx = DocWordIndex()
        idx.index_doc("d", "hello world hello")
        entry = idx.get_entry("d", "hello")
        assert isinstance(entry, IndexEntry)
        assert entry.doc_id == "d"
        assert entry.word == "hello"
        assert entry.frequency == 2

    def test_positions_correct(self):
        idx = DocWordIndex()
        idx.index_doc("d", "hi hi")
        entry = idx.get_entry("d", "hi")
        assert 0 in entry.positions
        assert 3 in entry.positions

    def test_missing_word_returns_none(self):
        idx = DocWordIndex()
        idx.index_doc("d", "alpha")
        assert idx.get_entry("d", "beta") is None

    def test_missing_doc_returns_none(self):
        idx = DocWordIndex()
        idx.index_doc("d", "alpha")
        assert idx.get_entry("nope", "alpha") is None

    def test_case_insensitive_lookup(self):
        idx = DocWordIndex()
        idx.index_doc("d", "WORD")
        assert idx.get_entry("d", "word") is not None
        assert idx.get_entry("d", "WORD") is not None


# ---------------------------------------------------------------------------
# words_in_doc
# ---------------------------------------------------------------------------


class TestWordsInDoc:
    def test_returns_sorted_list(self):
        idx = DocWordIndex()
        idx.index_doc("d", "banana apple cherry")
        assert idx.words_in_doc("d") == ["apple", "banana", "cherry"]

    def test_missing_doc_returns_empty(self):
        idx = DocWordIndex()
        assert idx.words_in_doc("nope") == []

    def test_empty_doc_returns_empty(self):
        idx = DocWordIndex()
        idx.index_doc("d", "")
        assert idx.words_in_doc("d") == []


# ---------------------------------------------------------------------------
# docs_count / word_count
# ---------------------------------------------------------------------------


class TestCountMethods:
    def test_docs_count_empty(self):
        assert DocWordIndex().docs_count() == 0

    def test_word_count_empty(self):
        assert DocWordIndex().word_count() == 0

    def test_docs_count_after_adds(self):
        idx = DocWordIndex()
        idx.index_doc("a", "x")
        idx.index_doc("b", "y")
        assert idx.docs_count() == 2

    def test_word_count_unique(self):
        idx = DocWordIndex()
        idx.index_doc("a", "apple banana")
        idx.index_doc("b", "apple cherry")
        # apple, banana, cherry = 3 unique
        assert idx.word_count() == 3

    def test_docs_count_after_remove(self):
        idx = DocWordIndex()
        idx.index_doc("a", "x")
        idx.remove_doc("a")
        assert idx.docs_count() == 0


# ---------------------------------------------------------------------------
# top_words
# ---------------------------------------------------------------------------


class TestTopWords:
    def test_returns_sorted_by_freq_desc(self):
        idx = DocWordIndex()
        idx.index_doc("d", "go go go run run stop")
        top = idx.top_words(limit=3)
        assert top[0] == ("go", 3)
        assert top[1] == ("run", 2)
        assert top[2] == ("stop", 1)

    def test_limit_respected(self):
        idx = DocWordIndex()
        idx.index_doc("d", "aa bb cc dd ee ff")
        top = idx.top_words(limit=3)
        assert len(top) == 3

    def test_corpus_wide_sums_across_docs(self):
        idx = DocWordIndex()
        idx.index_doc("a", "word word")
        idx.index_doc("b", "word")
        top = idx.top_words()
        assert ("word", 3) in top

    def test_per_doc_restricts_to_doc(self):
        idx = DocWordIndex()
        idx.index_doc("a", "alpha alpha")
        idx.index_doc("b", "alpha alpha alpha beta")
        top_a = idx.top_words(doc_id="a")
        # For doc "a": alpha appears 2 times
        assert ("alpha", 2) in top_a
        # beta should not appear (it is only in "b")
        assert all(w != "beta" for w, _ in top_a)

    def test_per_doc_missing_doc_returns_empty(self):
        idx = DocWordIndex()
        idx.index_doc("d", "word")
        assert idx.top_words(doc_id="nope") == []

    def test_empty_index_returns_empty(self):
        assert DocWordIndex().top_words() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty_index(self):
        s = DocWordIndex().stats()
        assert s.total_docs == 0
        assert s.total_words == 0
        assert s.total_entries == 0
        assert s.avg_words_per_doc == pytest.approx(0.0)

    def test_single_doc(self):
        idx = DocWordIndex()
        idx.index_doc("d", "hello world")
        s = idx.stats()
        assert s.total_docs == 1
        assert s.total_words == 2   # hello, world
        assert s.total_entries == 2
        assert s.avg_words_per_doc == pytest.approx(2.0)

    def test_multiple_docs(self):
        idx = DocWordIndex()
        idx.index_doc("a", "alpha beta")       # 2 unique words
        idx.index_doc("b", "alpha gamma")      # 2 unique words (alpha shared)
        s = idx.stats()
        assert s.total_docs == 2
        assert s.total_words == 3              # alpha, beta, gamma
        assert s.total_entries == 4            # alpha->a, beta->a, alpha->b, gamma->b
        # avg = 4 entries / 2 docs = 2.0
        assert s.avg_words_per_doc == pytest.approx(2.0)

    def test_stats_after_remove(self):
        idx = DocWordIndex()
        idx.index_doc("a", "alpha")
        idx.index_doc("b", "beta")
        idx.remove_doc("b")
        s = idx.stats()
        assert s.total_docs == 1
        assert s.total_words == 1

    def test_stats_type(self):
        assert isinstance(DocWordIndex().stats(), IndexStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_index_doc(self):
        """Many threads index different docs simultaneously without data corruption."""
        idx = DocWordIndex()
        errors: list[Exception] = []

        def worker(doc_id: str, content: str) -> None:
            try:
                idx.index_doc(doc_id, content)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=worker, args=(f"doc{i}", f"word{i} shared token"))
            for i in range(50)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], errors
        assert idx.docs_count() == 50

    def test_concurrent_search(self):
        """Concurrent reads do not raise errors or return corrupt data."""
        idx = DocWordIndex()
        idx.index_doc("d", "hello world hello world")
        results: list[list[SearchResult]] = []
        errors: list[Exception] = []

        def reader() -> None:
            try:
                results.append(idx.search("hello"))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=reader) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        for r in results:
            assert r[0].frequency == 2

    def test_concurrent_index_and_remove(self):
        """Interleaved index/remove operations stay consistent."""
        idx = DocWordIndex()
        errors: list[Exception] = []

        def add(n: int) -> None:
            try:
                idx.index_doc(f"add{n}", "data point")
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def remove(n: int) -> None:
            try:
                idx.index_doc(f"rm{n}", "temporary")
                idx.remove_doc(f"rm{n}")
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = (
            [threading.Thread(target=add, args=(i,)) for i in range(30)]
            + [threading.Thread(target=remove, args=(i,)) for i in range(30)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        # All "add" docs should still be present; none of the "rm" docs
        doc_ids = set(idx.search_multi(["data"], mode="any"))
        assert all(f"add{i}" in doc_ids for i in range(30))
