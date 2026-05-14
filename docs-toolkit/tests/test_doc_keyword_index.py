"""Tests for docstoolkit.doc_keyword_index."""

from __future__ import annotations

import pytest

from docstoolkit.doc_keyword_index import (
    DocKeywordIndex,
    IndexEntry,
    IndexStats,
    MatchHit,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestIndexEntry:
    def test_fields(self):
        e = IndexEntry(doc_id="d1", position=2, char_offset=10)
        assert e.doc_id == "d1"
        assert e.position == 2
        assert e.char_offset == 10

    def test_equality(self):
        assert IndexEntry("d", 1, 5) == IndexEntry("d", 1, 5)

    def test_inequality(self):
        assert IndexEntry("d", 1, 5) != IndexEntry("d", 2, 5)


class TestMatchHit:
    def test_defaults(self):
        h = MatchHit(doc_id="d1")
        assert h.doc_id == "d1"
        assert h.positions == []
        assert h.char_offsets == []
        assert h.score == 0

    def test_with_values(self):
        h = MatchHit(doc_id="d1", positions=[1, 2], char_offsets=[3, 4], score=2)
        assert h.positions == [1, 2]
        assert h.score == 2

    def test_independent_default_lists(self):
        a = MatchHit(doc_id="a")
        b = MatchHit(doc_id="b")
        a.positions.append(1)
        assert b.positions == []


class TestIndexStats:
    def test_fields(self):
        s = IndexStats(total_docs=3, total_terms=10, total_postings=20, avg_doc_length=6.7)
        assert s.total_docs == 3
        assert s.total_terms == 10
        assert s.total_postings == 20
        assert s.avg_doc_length == pytest.approx(6.7)


# ---------------------------------------------------------------------------
# index_doc
# ---------------------------------------------------------------------------


class TestIndexDoc:
    def test_returns_word_count(self):
        idx = DocKeywordIndex()
        assert idx.index_doc("d1", "hello world foo") == 3

    def test_empty_text(self):
        idx = DocKeywordIndex()
        assert idx.index_doc("d1", "") == 0
        assert idx.doc_count == 1

    def test_increments_doc_count(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "x")
        idx.index_doc("b", "y")
        assert idx.doc_count == 2

    def test_reindex_replaces_previous(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        idx.index_doc("d", "gamma delta")
        assert idx.term_frequency("alpha") == 0
        assert idx.term_frequency("gamma") == 1
        assert idx.doc_count == 1

    def test_punctuation_stripped(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "hello, world!")
        assert sorted(idx.vocabulary()) == ["hello", "world"]

    def test_unicode_word_chars(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "привет мир")
        assert "привет" in idx.vocabulary()


# ---------------------------------------------------------------------------
# remove_doc
# ---------------------------------------------------------------------------


class TestRemoveDoc:
    def test_removes_existing(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "a b")
        assert idx.remove_doc("d") is True
        assert idx.doc_count == 0

    def test_missing_returns_false(self):
        idx = DocKeywordIndex()
        assert idx.remove_doc("nope") is False

    def test_removes_postings(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        idx.remove_doc("d")
        assert idx.lookup("alpha") == []

    def test_other_docs_preserved(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha")
        idx.index_doc("b", "alpha")
        idx.remove_doc("a")
        assert idx.doc_frequency("alpha") == 1


# ---------------------------------------------------------------------------
# lookup
# ---------------------------------------------------------------------------


class TestLookup:
    def test_returns_entries(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta alpha")
        entries = idx.lookup("alpha")
        assert len(entries) == 2
        assert all(isinstance(e, IndexEntry) for e in entries)
        assert {e.position for e in entries} == {0, 2}

    def test_missing_term(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha")
        assert idx.lookup("missing") == []

    def test_char_offsets(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        entries = idx.lookup("beta")
        assert entries[0].char_offset == 6

    def test_case_insensitive_default(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "Alpha alpha ALPHA")
        assert len(idx.lookup("alpha")) == 3


# ---------------------------------------------------------------------------
# find
# ---------------------------------------------------------------------------


class TestFind:
    def test_returns_hits_per_doc(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha alpha beta")
        idx.index_doc("b", "alpha gamma")
        hits = idx.find("alpha")
        assert len(hits) == 2
        scores = {h.doc_id: h.score for h in hits}
        assert scores == {"a": 2, "b": 1}

    def test_sorted_by_score_desc(self):
        idx = DocKeywordIndex()
        idx.index_doc("low", "alpha")
        idx.index_doc("high", "alpha alpha alpha")
        hits = idx.find("alpha")
        assert hits[0].doc_id == "high"
        assert hits[1].doc_id == "low"

    def test_positions_recorded(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "x alpha y alpha")
        [hit] = idx.find("alpha")
        assert hit.positions == [1, 3]

    def test_missing_term(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha")
        assert idx.find("nope") == []


# ---------------------------------------------------------------------------
# find_phrase
# ---------------------------------------------------------------------------


class TestFindPhrase:
    def test_consecutive_match(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "the quick brown fox")
        hits = idx.find_phrase("quick brown")
        assert len(hits) == 1 and hits[0].doc_id == "d"
        assert hits[0].positions == [1]

    def test_non_consecutive_no_match(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "quick the brown")
        assert idx.find_phrase("quick brown") == []

    def test_single_term_phrase(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta alpha")
        hits = idx.find_phrase("alpha")
        assert hits[0].score == 2

    def test_repeated_phrase(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "foo bar foo bar end")
        hits = idx.find_phrase("foo bar")
        assert hits[0].score == 2
        assert hits[0].positions == [0, 2]

    def test_empty_phrase(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha")
        assert idx.find_phrase("") == []
        assert idx.find_phrase("   ") == []

    def test_missing_term_no_match(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        assert idx.find_phrase("alpha gamma") == []

    def test_phrase_across_docs(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "quick brown fox")
        idx.index_doc("b", "the quick brown")
        idx.index_doc("c", "brown quick")
        hits = idx.find_phrase("quick brown")
        assert {h.doc_id for h in hits} == {"a", "b"}


# ---------------------------------------------------------------------------
# find_any
# ---------------------------------------------------------------------------


class TestFindAny:
    def test_or_match(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha")
        idx.index_doc("b", "beta")
        idx.index_doc("c", "gamma")
        hits = idx.find_any(["alpha", "beta"])
        assert {h.doc_id for h in hits} == {"a", "b"}

    def test_empty_terms(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "x")
        assert idx.find_any([]) == []

    def test_aggregates_score(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta alpha")
        [hit] = idx.find_any(["alpha", "beta"])
        assert hit.score == 3

    def test_no_match(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "x")
        assert idx.find_any(["a", "b"]) == []


# ---------------------------------------------------------------------------
# find_all
# ---------------------------------------------------------------------------


class TestFindAll:
    def test_and_match(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha beta")
        idx.index_doc("b", "alpha")
        idx.index_doc("c", "alpha beta gamma")
        hits = idx.find_all(["alpha", "beta"])
        assert {h.doc_id for h in hits} == {"a", "c"}

    def test_all_three(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha beta gamma")
        idx.index_doc("b", "alpha beta")
        hits = idx.find_all(["alpha", "beta", "gamma"])
        assert {h.doc_id for h in hits} == {"a"}

    def test_missing_term(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha")
        assert idx.find_all(["alpha", "missing"]) == []

    def test_empty_terms(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha")
        assert idx.find_all([]) == []


# ---------------------------------------------------------------------------
# find_near
# ---------------------------------------------------------------------------


class TestFindNear:
    def test_within_distance(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha x y beta")  # distance 3
        hits = idx.find_near("alpha", "beta", distance=3)
        assert len(hits) == 1

    def test_outside_distance(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha a b c d beta")  # distance 5
        assert idx.find_near("alpha", "beta", distance=2) == []

    def test_distance_zero(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        # adjacent: distance 1
        assert idx.find_near("alpha", "beta", distance=0) == []
        assert idx.find_near("alpha", "beta", distance=1) != []

    def test_missing_term(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha")
        assert idx.find_near("alpha", "missing", distance=5) == []

    def test_negative_distance(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        assert idx.find_near("alpha", "beta", distance=-1) == []

    def test_multi_doc(self):
        idx = DocKeywordIndex()
        idx.index_doc("close", "alpha beta")
        idx.index_doc("far", "alpha x x x x x x beta")
        hits = idx.find_near("alpha", "beta", distance=2)
        assert [h.doc_id for h in hits] == ["close"]


# ---------------------------------------------------------------------------
# snippet
# ---------------------------------------------------------------------------


class TestSnippet:
    def test_basic_snippet(self):
        idx = DocKeywordIndex()
        text = "The quick brown fox jumps over the lazy dog and then runs away"
        idx.index_doc("d", text)
        snip = idx.snippet("d", "fox", max_chars=20)
        assert snip is not None
        assert "fox" in snip

    def test_unknown_doc(self):
        idx = DocKeywordIndex()
        assert idx.snippet("nope", "x") is None

    def test_query_not_in_doc(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        assert idx.snippet("d", "gamma") is None

    def test_empty_query(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        assert idx.snippet("d", "") is None

    def test_short_doc_no_ellipsis(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha")
        snip = idx.snippet("d", "alpha", max_chars=50)
        assert snip == "alpha"

    def test_long_doc_has_ellipsis(self):
        idx = DocKeywordIndex()
        text = "x" * 200 + " needle " + "y" * 200
        idx.index_doc("d", text)
        snip = idx.snippet("d", "needle", max_chars=30)
        assert snip is not None
        assert snip.startswith("...") and snip.endswith("...")
        assert "needle" in snip

    def test_max_chars_zero(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        assert idx.snippet("d", "alpha", max_chars=0) == ""

    def test_picks_earliest_match(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha middle beta")
        snip = idx.snippet("d", "beta alpha", max_chars=100)
        assert snip is not None
        assert snip.startswith("alpha")


# ---------------------------------------------------------------------------
# term_frequency
# ---------------------------------------------------------------------------


class TestTermFrequency:
    def test_corpus_wide(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha alpha")
        idx.index_doc("b", "alpha")
        assert idx.term_frequency("alpha") == 3

    def test_per_doc(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha alpha")
        idx.index_doc("b", "alpha")
        assert idx.term_frequency("alpha", "a") == 2
        assert idx.term_frequency("alpha", "b") == 1

    def test_missing_term(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha")
        assert idx.term_frequency("missing") == 0
        assert idx.term_frequency("missing", "d") == 0

    def test_missing_doc(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha")
        assert idx.term_frequency("alpha", "nope") == 0


# ---------------------------------------------------------------------------
# doc_frequency
# ---------------------------------------------------------------------------


class TestDocFrequency:
    def test_counts_docs(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha")
        idx.index_doc("b", "alpha alpha")
        idx.index_doc("c", "beta")
        assert idx.doc_frequency("alpha") == 2

    def test_missing_term(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "x")
        assert idx.doc_frequency("nope") == 0


# ---------------------------------------------------------------------------
# vocabulary
# ---------------------------------------------------------------------------


class TestVocabulary:
    def test_returns_terms(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta gamma")
        assert idx.vocabulary() == {"alpha", "beta", "gamma"}

    def test_empty(self):
        assert DocKeywordIndex().vocabulary() == set()


# ---------------------------------------------------------------------------
# doc_ids
# ---------------------------------------------------------------------------


class TestDocIds:
    def test_sorted(self):
        idx = DocKeywordIndex()
        idx.index_doc("c", "x")
        idx.index_doc("a", "y")
        idx.index_doc("b", "z")
        assert idx.doc_ids() == ["a", "b", "c"]

    def test_empty(self):
        assert DocKeywordIndex().doc_ids() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        s = DocKeywordIndex().stats()
        assert s.total_docs == 0
        assert s.total_terms == 0
        assert s.total_postings == 0
        assert s.avg_doc_length == 0.0

    def test_populated(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha beta")  # 2 words
        idx.index_doc("b", "alpha alpha gamma")  # 3 words
        s = idx.stats()
        assert s.total_docs == 2
        assert s.total_terms == 3  # alpha beta gamma
        assert s.total_postings == 5  # 2 + 3
        assert s.avg_doc_length == pytest.approx(2.5)


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clears_all(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha")
        idx.clear()
        assert idx.doc_count == 0
        assert idx.vocabulary() == set()
        assert idx.doc_ids() == []

    def test_index_after_clear(self):
        idx = DocKeywordIndex()
        idx.index_doc("a", "alpha")
        idx.clear()
        idx.index_doc("b", "beta")
        assert idx.doc_ids() == ["b"]


# ---------------------------------------------------------------------------
# case sensitive
# ---------------------------------------------------------------------------


class TestCaseSensitive:
    def test_case_insensitive_default(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "Alpha")
        assert idx.term_frequency("alpha") == 1
        assert idx.term_frequency("ALPHA") == 1

    def test_case_sensitive_distinct(self):
        idx = DocKeywordIndex(case_sensitive=True)
        idx.index_doc("d", "Alpha alpha")
        assert idx.term_frequency("Alpha") == 1
        assert idx.term_frequency("alpha") == 1

    def test_case_sensitive_vocabulary(self):
        idx = DocKeywordIndex(case_sensitive=True)
        idx.index_doc("d", "Foo foo FOO")
        assert idx.vocabulary() == {"Foo", "foo", "FOO"}

    def test_case_sensitive_phrase(self):
        idx = DocKeywordIndex(case_sensitive=True)
        idx.index_doc("d", "Quick Brown fox")
        assert idx.find_phrase("Quick Brown") != []
        assert idx.find_phrase("quick brown") == []


# ---------------------------------------------------------------------------
# edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_whitespace_only_doc(self):
        idx = DocKeywordIndex()
        assert idx.index_doc("d", "   \n\t  ") == 0
        assert idx.vocabulary() == set()

    def test_numbers_indexed(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "version 2 release 10")
        assert "2" in idx.vocabulary()
        assert "10" in idx.vocabulary()

    def test_doc_count_property(self):
        idx = DocKeywordIndex()
        assert idx.doc_count == 0
        idx.index_doc("a", "x")
        idx.index_doc("b", "y")
        assert idx.doc_count == 2

    def test_lookup_after_remove(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        idx.remove_doc("d")
        assert idx.lookup("alpha") == []
        assert idx.vocabulary() == set()

    def test_reindex_changes_word_count(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "one two three")
        idx.index_doc("d", "one")
        s = idx.stats()
        assert s.avg_doc_length == 1.0

    def test_phrase_three_terms(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta gamma delta")
        hits = idx.find_phrase("beta gamma delta")
        assert len(hits) == 1 and hits[0].positions == [1]

    def test_find_any_single_term(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha alpha")
        [hit] = idx.find_any(["alpha"])
        assert hit.score == 2

    def test_find_all_single_term(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha alpha")
        [hit] = idx.find_all(["alpha"])
        assert hit.score == 2

    def test_repeated_index_doc_idempotent_word_count(self):
        idx = DocKeywordIndex()
        idx.index_doc("d", "alpha beta")
        idx.index_doc("d", "alpha beta")
        assert idx.term_frequency("alpha") == 1
        assert idx.term_frequency("beta") == 1
