"""Tests for ``docstoolkit.doc_index_full``."""

from __future__ import annotations

import pytest

from docstoolkit.doc_index_full import (
    DocIndexFull,
    IndexEntry,
    IndexStats,
    Match,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestIndexEntry:
    def test_construction(self):
        e = IndexEntry(doc_id="d1", position=2, char_offset=10)
        assert e.doc_id == "d1"
        assert e.position == 2
        assert e.char_offset == 10

    def test_equality(self):
        assert IndexEntry("d", 0, 0) == IndexEntry("d", 0, 0)

    def test_inequality(self):
        assert IndexEntry("d", 0, 0) != IndexEntry("d", 1, 0)


class TestMatch:
    def test_defaults(self):
        m = Match(doc_id="d", term="t")
        assert m.positions == []
        assert m.score == 1.0

    def test_full(self):
        m = Match(doc_id="d", term="t", positions=[1, 2], score=3.5)
        assert m.positions == [1, 2]
        assert m.score == 3.5

    def test_independent_positions(self):
        m1 = Match(doc_id="d", term="t")
        m2 = Match(doc_id="d", term="t")
        m1.positions.append(1)
        assert m2.positions == []


class TestIndexStats:
    def test_construction(self):
        s = IndexStats(
            total_docs=2, total_tokens=10, unique_terms=5, avg_doc_length=5.0
        )
        assert s.total_docs == 2
        assert s.total_tokens == 10
        assert s.unique_terms == 5
        assert s.avg_doc_length == 5.0


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def idx():
    return DocIndexFull()


@pytest.fixture
def idx_no_stem():
    return DocIndexFull(stem=False)


@pytest.fixture
def idx_case():
    return DocIndexFull(case_sensitive=True, stem=False)


@pytest.fixture
def populated():
    i = DocIndexFull(stem=False)
    i.index_doc("a", "the quick brown fox jumps over the lazy dog")
    i.index_doc("b", "the quick brown rabbit eats carrots")
    i.index_doc("c", "lazy slow turtles dream slowly")
    return i


# ---------------------------------------------------------------------------
# index_doc
# ---------------------------------------------------------------------------


class TestIndexDoc:
    def test_returns_word_count(self, idx):
        n = idx.index_doc("d1", "one two three")
        assert n == 3

    def test_empty_text(self, idx):
        assert idx.index_doc("d1", "") == 0
        assert "d1" in idx.doc_ids()

    def test_punctuation_stripped(self, idx_no_stem):
        n = idx_no_stem.index_doc("d", "hello, world!")
        assert n == 2
        assert idx_no_stem.term_frequency("hello") == 1
        assert idx_no_stem.term_frequency("world") == 1

    def test_case_folded_by_default(self, idx_no_stem):
        idx_no_stem.index_doc("d", "Hello HELLO hello")
        assert idx_no_stem.term_frequency("hello") == 3

    def test_reindex_replaces(self, idx_no_stem):
        idx_no_stem.index_doc("d", "alpha beta")
        idx_no_stem.index_doc("d", "gamma")
        assert idx_no_stem.term_frequency("alpha") == 0
        assert idx_no_stem.term_frequency("gamma") == 1

    def test_doc_count_grows(self, idx_no_stem):
        idx_no_stem.index_doc("a", "x")
        idx_no_stem.index_doc("b", "y")
        assert idx_no_stem.doc_count == 2


# ---------------------------------------------------------------------------
# update_doc
# ---------------------------------------------------------------------------


class TestUpdateDoc:
    def test_update_is_reindex(self, idx_no_stem):
        idx_no_stem.index_doc("d", "old text")
        idx_no_stem.update_doc("d", "new text")
        assert idx_no_stem.term_frequency("old") == 0
        assert idx_no_stem.term_frequency("new") == 1

    def test_update_returns_count(self, idx_no_stem):
        idx_no_stem.index_doc("d", "one")
        assert idx_no_stem.update_doc("d", "one two three") == 3

    def test_update_unknown_doc_acts_as_insert(self, idx_no_stem):
        idx_no_stem.update_doc("new", "hello there")
        assert "new" in idx_no_stem.doc_ids()


# ---------------------------------------------------------------------------
# remove_doc
# ---------------------------------------------------------------------------


class TestRemoveDoc:
    def test_remove_existing(self, idx_no_stem):
        idx_no_stem.index_doc("d", "x y z")
        assert idx_no_stem.remove_doc("d") is True
        assert idx_no_stem.doc_count == 0

    def test_remove_unknown(self, idx_no_stem):
        assert idx_no_stem.remove_doc("missing") is False

    def test_remove_purges_postings(self, idx_no_stem):
        idx_no_stem.index_doc("d", "x")
        idx_no_stem.remove_doc("d")
        assert idx_no_stem.lookup("x") == []
        assert "x" not in idx_no_stem.vocabulary()


# ---------------------------------------------------------------------------
# lookup
# ---------------------------------------------------------------------------


class TestLookup:
    def test_basic(self, idx_no_stem):
        idx_no_stem.index_doc("d", "alpha beta alpha")
        entries = idx_no_stem.lookup("alpha")
        assert len(entries) == 2
        assert all(isinstance(e, IndexEntry) for e in entries)
        positions = sorted(e.position for e in entries)
        assert positions == [0, 2]

    def test_missing(self, idx_no_stem):
        assert idx_no_stem.lookup("nope") == []

    def test_char_offsets(self, idx_no_stem):
        idx_no_stem.index_doc("d", "foo bar")
        entries = idx_no_stem.lookup("bar")
        assert entries[0].char_offset == 4


# ---------------------------------------------------------------------------
# find
# ---------------------------------------------------------------------------


class TestFind:
    def test_basic(self, populated):
        hits = populated.find("quick")
        assert {h.doc_id for h in hits} == {"a", "b"}
        assert all(isinstance(h, Match) for h in hits)

    def test_score_is_tf(self, idx_no_stem):
        idx_no_stem.index_doc("d", "x x x y")
        hits = idx_no_stem.find("x")
        assert hits[0].score == 3.0

    def test_missing(self, populated):
        assert populated.find("aardvark") == []

    def test_sorted_by_score(self, idx_no_stem):
        idx_no_stem.index_doc("a", "x")
        idx_no_stem.index_doc("b", "x x x")
        hits = idx_no_stem.find("x")
        assert [h.doc_id for h in hits] == ["b", "a"]


# ---------------------------------------------------------------------------
# find_phrase
# ---------------------------------------------------------------------------


class TestFindPhrase:
    def test_consecutive(self, populated):
        hits = populated.find_phrase("quick brown")
        assert {h.doc_id for h in hits} == {"a", "b"}

    def test_non_consecutive(self, populated):
        # "quick" then "fox" — not consecutive
        assert populated.find_phrase("quick fox") == []

    def test_single_token(self, populated):
        hits = populated.find_phrase("lazy")
        assert {h.doc_id for h in hits} == {"a", "c"}

    def test_empty(self, populated):
        assert populated.find_phrase("") == []

    def test_missing_token(self, populated):
        assert populated.find_phrase("quick martian") == []


# ---------------------------------------------------------------------------
# find_proximity (unordered)
# ---------------------------------------------------------------------------


class TestFindProximity:
    def test_within_distance(self, idx_no_stem):
        idx_no_stem.index_doc("d", "alpha beta gamma delta")
        hits = idx_no_stem.find_proximity(["alpha", "delta"], max_distance=3)
        assert len(hits) == 1
        assert hits[0].doc_id == "d"

    def test_out_of_distance(self, idx_no_stem):
        idx_no_stem.index_doc("d", "alpha beta gamma delta")
        assert idx_no_stem.find_proximity(["alpha", "delta"], max_distance=2) == []

    def test_three_terms(self, idx_no_stem):
        idx_no_stem.index_doc("d", "x y z w")
        # positions 0, 2, 3 -> max adjacent gap = 2
        hits = idx_no_stem.find_proximity(["x", "z", "w"], max_distance=2)
        assert len(hits) == 1

    def test_missing_term(self, idx_no_stem):
        idx_no_stem.index_doc("d", "alpha beta")
        assert idx_no_stem.find_proximity(["alpha", "missing"], max_distance=5) == []

    def test_empty_list(self, idx_no_stem):
        assert idx_no_stem.find_proximity([], max_distance=5) == []

    def test_negative_distance(self, idx_no_stem):
        idx_no_stem.index_doc("d", "alpha beta")
        assert idx_no_stem.find_proximity(["alpha", "beta"], max_distance=-1) == []


# ---------------------------------------------------------------------------
# find_proximity (ordered)
# ---------------------------------------------------------------------------


class TestFindProximityOrdered:
    def test_in_order(self, idx_no_stem):
        idx_no_stem.index_doc("d", "alpha gap beta")
        hits = idx_no_stem.find_proximity(
            ["alpha", "beta"], max_distance=2, ordered=True
        )
        assert len(hits) == 1

    def test_out_of_order(self, idx_no_stem):
        idx_no_stem.index_doc("d", "beta gap alpha")
        assert (
            idx_no_stem.find_proximity(["alpha", "beta"], max_distance=2, ordered=True)
            == []
        )

    def test_unordered_matches_when_out_of_order(self, idx_no_stem):
        idx_no_stem.index_doc("d", "beta gap alpha")
        hits = idx_no_stem.find_proximity(
            ["alpha", "beta"], max_distance=2, ordered=False
        )
        assert len(hits) == 1


# ---------------------------------------------------------------------------
# find_or
# ---------------------------------------------------------------------------


class TestFindOr:
    def test_union(self, populated):
        hits = populated.find_or(["fox", "rabbit"])
        assert {h.doc_id for h in hits} == {"a", "b"}

    def test_some_missing(self, populated):
        hits = populated.find_or(["fox", "nonexistent"])
        assert {h.doc_id for h in hits} == {"a"}

    def test_empty(self, populated):
        assert populated.find_or([]) == []

    def test_all_missing(self, populated):
        assert populated.find_or(["nope", "zilch"]) == []


# ---------------------------------------------------------------------------
# find_and
# ---------------------------------------------------------------------------


class TestFindAnd:
    def test_intersection(self, populated):
        hits = populated.find_and(["quick", "brown"])
        assert {h.doc_id for h in hits} == {"a", "b"}

    def test_some_missing(self, populated):
        assert populated.find_and(["quick", "missing"]) == []

    def test_empty(self, populated):
        assert populated.find_and([]) == []

    def test_intersects_only(self, populated):
        hits = populated.find_and(["quick", "fox"])
        assert {h.doc_id for h in hits} == {"a"}


# ---------------------------------------------------------------------------
# find_not
# ---------------------------------------------------------------------------


class TestFindNot:
    def test_excludes(self, populated):
        docs = populated.find_not("rabbit")
        assert docs == ["a", "c"]

    def test_missing_term_returns_all(self, populated):
        assert populated.find_not("missing") == ["a", "b", "c"]

    def test_sorted(self, idx_no_stem):
        idx_no_stem.index_doc("z", "x")
        idx_no_stem.index_doc("a", "y")
        docs = idx_no_stem.find_not("x")
        assert docs == ["a"]


# ---------------------------------------------------------------------------
# term_frequency
# ---------------------------------------------------------------------------


class TestTermFrequency:
    def test_corpus(self, idx_no_stem):
        idx_no_stem.index_doc("a", "x x")
        idx_no_stem.index_doc("b", "x y")
        assert idx_no_stem.term_frequency("x") == 3

    def test_per_doc(self, idx_no_stem):
        idx_no_stem.index_doc("a", "x x")
        idx_no_stem.index_doc("b", "x y")
        assert idx_no_stem.term_frequency("x", "a") == 2
        assert idx_no_stem.term_frequency("x", "b") == 1

    def test_missing(self, idx_no_stem):
        assert idx_no_stem.term_frequency("nope") == 0
        assert idx_no_stem.term_frequency("nope", "any") == 0


# ---------------------------------------------------------------------------
# doc_frequency
# ---------------------------------------------------------------------------


class TestDocFrequency:
    def test_basic(self, populated):
        assert populated.doc_frequency("quick") == 2
        assert populated.doc_frequency("rabbit") == 1
        assert populated.doc_frequency("nope") == 0


# ---------------------------------------------------------------------------
# vocabulary
# ---------------------------------------------------------------------------


class TestVocabulary:
    def test_basic(self, idx_no_stem):
        idx_no_stem.index_doc("d", "alpha beta")
        assert idx_no_stem.vocabulary() == {"alpha", "beta"}

    def test_empty(self, idx_no_stem):
        assert idx_no_stem.vocabulary() == set()

    def test_with_stems(self):
        i = DocIndexFull(stem=True)
        i.index_doc("d", "running")
        assert "run" in i.vocabulary()
        assert "running" in i.vocabulary()


# ---------------------------------------------------------------------------
# doc_ids
# ---------------------------------------------------------------------------


class TestDocIds:
    def test_sorted(self, idx_no_stem):
        idx_no_stem.index_doc("b", "x")
        idx_no_stem.index_doc("a", "y")
        assert idx_no_stem.doc_ids() == ["a", "b"]

    def test_empty(self, idx_no_stem):
        assert idx_no_stem.doc_ids() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self, idx_no_stem):
        s = idx_no_stem.stats()
        assert s.total_docs == 0
        assert s.total_tokens == 0
        assert s.unique_terms == 0
        assert s.avg_doc_length == 0.0

    def test_populated(self, idx_no_stem):
        idx_no_stem.index_doc("a", "x y z")
        idx_no_stem.index_doc("b", "x y")
        s = idx_no_stem.stats()
        assert s.total_docs == 2
        assert s.total_tokens == 5
        assert s.unique_terms == 3
        assert s.avg_doc_length == 2.5


# ---------------------------------------------------------------------------
# snippet
# ---------------------------------------------------------------------------


class TestSnippet:
    def test_basic(self, idx_no_stem):
        idx_no_stem.index_doc("d", "abcdefg hello ijklmno")
        snip = idx_no_stem.snippet("d", "hello", max_chars=10)
        assert snip is not None
        assert "hello" in snip

    def test_unknown_doc(self, idx_no_stem):
        assert idx_no_stem.snippet("missing", "x") is None

    def test_unknown_term(self, idx_no_stem):
        idx_no_stem.index_doc("d", "x")
        assert idx_no_stem.snippet("d", "absent") is None

    def test_zero_chars(self, idx_no_stem):
        idx_no_stem.index_doc("d", "hello")
        assert idx_no_stem.snippet("d", "hello", max_chars=0) == ""

    def test_short_doc_no_ellipsis(self, idx_no_stem):
        idx_no_stem.index_doc("d", "tiny")
        snip = idx_no_stem.snippet("d", "tiny", max_chars=100)
        assert snip == "tiny"


# ---------------------------------------------------------------------------
# Stemming
# ---------------------------------------------------------------------------


class TestStemming:
    def test_running_matches_run(self):
        i = DocIndexFull(stem=True)
        i.index_doc("d", "running")
        assert i.find("run")
        assert i.find("running")

    def test_ed_suffix(self):
        i = DocIndexFull(stem=True)
        i.index_doc("d", "jumped")
        assert i.doc_frequency("jump") == 1
        assert i.doc_frequency("jumped") == 1

    def test_ly_suffix(self):
        i = DocIndexFull(stem=True)
        i.index_doc("d", "quickly")
        assert i.find("quick")

    def test_tion_suffix(self):
        i = DocIndexFull(stem=True)
        i.index_doc("d", "navigation")
        assert i.find("naviga")

    def test_ment_suffix(self):
        i = DocIndexFull(stem=True)
        i.index_doc("d", "development")
        assert i.find("develop")

    def test_ness_suffix(self):
        i = DocIndexFull(stem=True)
        i.index_doc("d", "happiness")
        assert i.find("happi")

    def test_s_suffix(self):
        i = DocIndexFull(stem=True)
        i.index_doc("d", "cats")
        assert i.find("cat")

    def test_no_stem_for_short_words(self):
        i = DocIndexFull(stem=True)
        i.index_doc("d", "is")  # too short to strip "s"
        # No stem variant since stem would be too short
        assert "is" in i.vocabulary()

    def test_disable_stem(self):
        i = DocIndexFull(stem=False)
        i.index_doc("d", "running")
        assert not i.find("run")
        assert i.find("running")


# ---------------------------------------------------------------------------
# case sensitivity
# ---------------------------------------------------------------------------


class TestCaseSensitive:
    def test_case_sensitive_distinct(self, idx_case):
        idx_case.index_doc("d", "Apple apple APPLE")
        assert idx_case.term_frequency("apple") == 1
        assert idx_case.term_frequency("Apple") == 1
        assert idx_case.term_frequency("APPLE") == 1

    def test_case_insensitive_default(self, idx_no_stem):
        idx_no_stem.index_doc("d", "Apple apple APPLE")
        assert idx_no_stem.term_frequency("apple") == 3


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_removes_everything(self, populated):
        populated.clear()
        assert populated.doc_count == 0
        assert populated.vocabulary() == set()
        assert populated.doc_ids() == []

    def test_clear_empty(self, idx_no_stem):
        idx_no_stem.clear()
        assert idx_no_stem.doc_count == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_unicode_tokens(self, idx_no_stem):
        idx_no_stem.index_doc("d", "привет мир")
        assert idx_no_stem.find("привет")

    def test_doc_count_property(self, idx_no_stem):
        assert idx_no_stem.doc_count == 0
        idx_no_stem.index_doc("a", "x")
        assert idx_no_stem.doc_count == 1

    def test_phrase_repeated_in_doc(self, idx_no_stem):
        idx_no_stem.index_doc("d", "go now go now")
        hits = idx_no_stem.find_phrase("go now")
        assert hits[0].score == 2.0

    def test_proximity_with_repeated_terms(self, idx_no_stem):
        idx_no_stem.index_doc("d", "x y x y x")
        hits = idx_no_stem.find_proximity(["x", "y"], max_distance=1)
        assert len(hits) == 1

    def test_find_and_single_term(self, idx_no_stem):
        idx_no_stem.index_doc("a", "x")
        idx_no_stem.index_doc("b", "y")
        hits = idx_no_stem.find_and(["x"])
        assert [h.doc_id for h in hits] == ["a"]

    def test_find_or_single_term(self, idx_no_stem):
        idx_no_stem.index_doc("a", "x")
        hits = idx_no_stem.find_or(["x"])
        assert [h.doc_id for h in hits] == ["a"]

    def test_overwrite_then_remove(self, idx_no_stem):
        idx_no_stem.index_doc("d", "a b")
        idx_no_stem.index_doc("d", "c d")
        assert idx_no_stem.remove_doc("d") is True
        assert idx_no_stem.vocabulary() == set()
