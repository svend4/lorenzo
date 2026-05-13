"""Tests for E143 doc_search."""
from __future__ import annotations

import pytest

from docstoolkit.doc_search import DocSearch, MatchType, SearchHit, SearchQuery


@pytest.fixture
def empty() -> DocSearch:
    return DocSearch()


@pytest.fixture
def populated() -> DocSearch:
    ds = DocSearch()
    ds.index_batch(
        {
            "d1": "The quick brown fox jumps over the lazy dog.",
            "d2": "A quick brown dog leaps over a fox.",
            "d3": "Lorem ipsum dolor sit amet.",
            "d4": "The fox is quick. The dog is lazy. The fox runs.",
            "d5": "Hello World! Python is great. PYTHON rocks.",
        }
    )
    return ds


# ---------------------------------------------------------------------------
# TestMatchType
# ---------------------------------------------------------------------------

class TestMatchType:
    def test_has_exact(self):
        assert MatchType.EXACT.value == "exact"

    def test_has_phrase(self):
        assert MatchType.PHRASE.value == "phrase"

    def test_has_fuzzy(self):
        assert MatchType.FUZZY.value == "fuzzy"

    def test_has_regex(self):
        assert MatchType.REGEX.value == "regex"

    def test_members_distinct(self):
        assert len({m.value for m in MatchType}) == 4


# ---------------------------------------------------------------------------
# TestSearchHit
# ---------------------------------------------------------------------------

class TestSearchHit:
    def test_default_snippets(self):
        hit = SearchHit(doc_id="d", match_type=MatchType.EXACT, score=1.0)
        assert hit.snippets == []
        assert hit.match_count == 0

    def test_construct_with_snippets(self):
        hit = SearchHit(
            doc_id="d",
            match_type=MatchType.PHRASE,
            score=2.5,
            snippets=["abc"],
            match_count=3,
        )
        assert hit.score == 2.5
        assert hit.match_count == 3
        assert hit.snippets == ["abc"]


# ---------------------------------------------------------------------------
# TestSearchQuery
# ---------------------------------------------------------------------------

class TestSearchQuery:
    def test_defaults(self):
        q = SearchQuery(terms=["a"])
        assert q.operator == "AND"
        assert q.match_type is MatchType.EXACT
        assert q.case_sensitive is False

    def test_custom(self):
        q = SearchQuery(
            terms=["a", "b"],
            operator="OR",
            match_type=MatchType.PHRASE,
            case_sensitive=True,
        )
        assert q.operator == "OR"
        assert q.match_type is MatchType.PHRASE
        assert q.case_sensitive is True


# ---------------------------------------------------------------------------
# TestIndex
# ---------------------------------------------------------------------------

class TestIndex:
    def test_index_single(self, empty: DocSearch):
        empty.index("d1", "hello world")
        assert empty.doc_count == 1

    def test_index_replace(self, empty: DocSearch):
        empty.index("d1", "hello world")
        empty.index("d1", "different content")
        assert empty.doc_count == 1
        # The old token should no longer be searchable.
        assert empty.count_matches("hello") == 0
        assert empty.count_matches("different") == 1

    def test_index_batch(self, empty: DocSearch):
        empty.index_batch({"a": "alpha", "b": "beta", "c": "gamma"})
        assert empty.doc_count == 3

    def test_index_batch_empty(self, empty: DocSearch):
        empty.index_batch({})
        assert empty.doc_count == 0

    def test_index_unicode(self, empty: DocSearch):
        empty.index("u1", "Привет мир")
        assert empty.count_matches("привет") == 1


# ---------------------------------------------------------------------------
# TestRemove
# ---------------------------------------------------------------------------

class TestRemove:
    def test_remove_present(self, populated: DocSearch):
        assert populated.remove("d1") is True
        assert populated.doc_count == 4

    def test_remove_absent(self, populated: DocSearch):
        assert populated.remove("missing") is False

    def test_remove_clears_inverted(self, empty: DocSearch):
        empty.index("d1", "unique-token")
        empty.remove("d1")
        assert empty.count_matches("unique-token") == 0
        hits = empty.search("unique-token")
        assert hits == []

    def test_remove_then_reindex(self, populated: DocSearch):
        populated.remove("d1")
        populated.index("d1", "reborn content")
        assert populated.count_matches("reborn") == 1


# ---------------------------------------------------------------------------
# TestSearchBasic
# ---------------------------------------------------------------------------

class TestSearchBasic:
    def test_single_term_finds_doc(self, populated: DocSearch):
        hits = populated.search("fox")
        ids = {h.doc_id for h in hits}
        assert ids == {"d1", "d2", "d4"}

    def test_no_match_returns_empty(self, populated: DocSearch):
        assert populated.search("zzznothing") == []

    def test_search_empty_query(self, populated: DocSearch):
        assert populated.search("") == []

    def test_search_on_empty_index(self, empty: DocSearch):
        assert empty.search("anything") == []

    def test_search_returns_hit_type(self, populated: DocSearch):
        hits = populated.search("fox")
        assert all(isinstance(h, SearchHit) for h in hits)


# ---------------------------------------------------------------------------
# TestSearchAnd
# ---------------------------------------------------------------------------

class TestSearchAnd:
    def test_and_intersects(self, populated: DocSearch):
        hits = populated.search("fox dog")
        ids = {h.doc_id for h in hits}
        assert ids == {"d1", "d2", "d4"}

    def test_and_excludes_partial(self, populated: DocSearch):
        # "lorem" only in d3 which has no "fox".
        hits = populated.search("lorem fox")
        assert hits == []

    def test_and_advanced(self, populated: DocSearch):
        q = SearchQuery(terms=["quick", "fox"], operator="AND")
        ids = {h.doc_id for h in populated.search_advanced(q)}
        assert ids == {"d1", "d2", "d4"}


# ---------------------------------------------------------------------------
# TestSearchOr
# ---------------------------------------------------------------------------

class TestSearchOr:
    def test_or_unions(self, populated: DocSearch):
        q = SearchQuery(terms=["lorem", "python"], operator="OR")
        ids = {h.doc_id for h in populated.search_advanced(q)}
        assert ids == {"d3", "d5"}

    def test_or_single_term(self, populated: DocSearch):
        q = SearchQuery(terms=["lazy"], operator="OR")
        ids = {h.doc_id for h in populated.search_advanced(q)}
        assert ids == {"d1", "d4"}

    def test_or_no_match(self, populated: DocSearch):
        q = SearchQuery(terms=["xxx", "yyy"], operator="OR")
        assert populated.search_advanced(q) == []


# ---------------------------------------------------------------------------
# TestSearchPhrase
# ---------------------------------------------------------------------------

class TestSearchPhrase:
    def test_phrase_match(self, populated: DocSearch):
        hits = populated.search_phrase("quick brown")
        ids = {h.doc_id for h in hits}
        assert ids == {"d1", "d2"}

    def test_phrase_no_match(self, populated: DocSearch):
        assert populated.search_phrase("dog quick") == []

    def test_phrase_case_insensitive(self, populated: DocSearch):
        hits = populated.search_phrase("QUICK BROWN")
        assert {h.doc_id for h in hits} == {"d1", "d2"}

    def test_phrase_empty(self, populated: DocSearch):
        assert populated.search_phrase("") == []
        assert populated.search_phrase("   ") == []

    def test_phrase_via_advanced(self, populated: DocSearch):
        q = SearchQuery(
            terms=["quick", "brown"], match_type=MatchType.PHRASE
        )
        ids = {h.doc_id for h in populated.search_advanced(q)}
        assert ids == {"d1", "d2"}

    def test_phrase_match_count(self, populated: DocSearch):
        hits = populated.search_phrase("the fox")
        # d1 has "The fox"; d4 has "The fox" twice.
        d4 = next(h for h in hits if h.doc_id == "d4")
        assert d4.match_count == 2


# ---------------------------------------------------------------------------
# TestSearchRegex
# ---------------------------------------------------------------------------

class TestSearchRegex:
    def test_regex_simple(self, populated: DocSearch):
        hits = populated.search_regex(r"qu\w+")
        # qu... should appear in d1, d2, d4.
        ids = {h.doc_id for h in hits}
        assert ids == {"d1", "d2", "d4"}

    def test_regex_no_match(self, populated: DocSearch):
        assert populated.search_regex(r"^XXX") == []

    def test_regex_invalid_pattern(self, populated: DocSearch):
        assert populated.search_regex(r"[unclosed") == []

    def test_regex_anchored(self, populated: DocSearch):
        hits = populated.search_regex(r"^Hello")
        assert {h.doc_id for h in hits} == {"d5"}

    def test_regex_match_count(self, populated: DocSearch):
        hits = populated.search_regex(r"fox")
        d4 = next(h for h in hits if h.doc_id == "d4")
        assert d4.match_count == 2


# ---------------------------------------------------------------------------
# TestSearchBoolean
# ---------------------------------------------------------------------------

class TestSearchBoolean:
    def test_must(self, populated: DocSearch):
        hits = populated.search_boolean(must=["fox", "dog"])
        ids = {h.doc_id for h in hits}
        assert ids == {"d1", "d2", "d4"}

    def test_must_not_excludes(self, populated: DocSearch):
        hits = populated.search_boolean(must=["fox"], must_not=["lazy"])
        ids = {h.doc_id for h in hits}
        assert ids == {"d2"}

    def test_should_boosts(self, populated: DocSearch):
        # d1 and d4 both have fox; d4 has "lazy" matching SHOULD.
        hits = populated.search_boolean(must=["fox"], should=["lazy"])
        ranked = [h.doc_id for h in hits]
        # d4 should rank above d2 because it has "lazy" boost and more foxes.
        assert ranked[0] in {"d4", "d1"}

    def test_must_not_only(self, populated: DocSearch):
        hits = populated.search_boolean(must=[], must_not=["fox"])
        ids = {h.doc_id for h in hits}
        # All docs not containing fox.
        assert ids == {"d3", "d5"}

    def test_empty_must(self, populated: DocSearch):
        # Without any constraints we should still get results (effectively all).
        hits = populated.search_boolean(must=[])
        assert len(hits) == populated.doc_count


# ---------------------------------------------------------------------------
# TestCaseSensitivity
# ---------------------------------------------------------------------------

class TestCaseSensitivity:
    def test_case_insensitive_default(self, populated: DocSearch):
        hits = populated.search("PYTHON")
        ids = {h.doc_id for h in hits}
        assert "d5" in ids

    def test_count_case_insensitive(self, populated: DocSearch):
        # d5 has "Python" + "PYTHON".
        assert populated.count_matches("python") == 2

    def test_case_sensitive_query(self, populated: DocSearch):
        q = SearchQuery(
            terms=["PYTHON"], operator="AND", case_sensitive=True
        )
        hits = populated.search_advanced(q)
        ids = {h.doc_id for h in hits}
        # Only d5 contains "PYTHON" in upper case.
        assert ids == {"d5"}

    def test_case_sensitive_no_match(self, populated: DocSearch):
        q = SearchQuery(
            terms=["pyThOn"], operator="AND", case_sensitive=True
        )
        assert populated.search_advanced(q) == []


# ---------------------------------------------------------------------------
# TestCountMatches
# ---------------------------------------------------------------------------

class TestCountMatches:
    def test_count_existing(self, populated: DocSearch):
        # "fox" appears: d1×1, d2×1, d4×2 = 4.
        assert populated.count_matches("fox") == 4

    def test_count_missing(self, populated: DocSearch):
        assert populated.count_matches("zzznothing") == 0

    def test_count_empty_index(self, empty: DocSearch):
        assert empty.count_matches("anything") == 0

    def test_count_case_insensitive(self, populated: DocSearch):
        assert populated.count_matches("Fox") == populated.count_matches("fox")


# ---------------------------------------------------------------------------
# TestSnippet
# ---------------------------------------------------------------------------

class TestSnippet:
    def test_snippet_contains_term(self, populated: DocSearch):
        snip = populated.make_snippet("d1", "fox", context=10)
        assert "fox" in snip.lower()

    def test_snippet_missing_doc(self, populated: DocSearch):
        assert populated.make_snippet("nope", "fox") == ""

    def test_snippet_missing_term(self, populated: DocSearch):
        assert populated.make_snippet("d1", "zzz") == ""

    def test_snippet_context_size(self, empty: DocSearch):
        empty.index("d", "a" * 100 + " TARGET " + "b" * 100)
        snip = empty.make_snippet("d", "TARGET", context=5)
        # The snippet should be much shorter than the doc.
        assert len(snip) < 50

    def test_snippet_ellipsis_for_middle(self, empty: DocSearch):
        empty.index(
            "d", "leading words here " * 20 + "MARKER" + " trailing words" * 20
        )
        snip = empty.make_snippet("d", "MARKER", context=10)
        assert snip.startswith("...")
        assert snip.endswith("...")


# ---------------------------------------------------------------------------
# TestTopK
# ---------------------------------------------------------------------------

class TestTopK:
    def test_top_k_limits(self, populated: DocSearch):
        hits = populated.search("the", top_k=2)
        assert len(hits) <= 2

    def test_top_k_larger_than_results(self, populated: DocSearch):
        hits = populated.search("lorem", top_k=100)
        assert len(hits) == 1

    def test_top_k_zero(self, populated: DocSearch):
        assert populated.search("fox", top_k=0) == []

    def test_top_k_phrase(self, populated: DocSearch):
        hits = populated.search_phrase("quick brown", top_k=1)
        assert len(hits) == 1

    def test_top_k_regex(self, populated: DocSearch):
        hits = populated.search_regex(r"\w+", top_k=3)
        assert len(hits) == 3


# ---------------------------------------------------------------------------
# TestScoring
# ---------------------------------------------------------------------------

class TestScoring:
    def test_more_matches_higher_score(self, populated: DocSearch):
        hits = populated.search("fox")
        # d4 has 2 occurrences of "fox", d1 and d2 have 1.
        scores = {h.doc_id: h.score for h in hits}
        assert scores["d4"] > scores["d1"]
        assert scores["d4"] > scores["d2"]

    def test_sorted_descending(self, populated: DocSearch):
        hits = populated.search("fox")
        for a, b in zip(hits, hits[1:]):
            assert a.score >= b.score

    def test_score_equals_match_count_in_basic(self, populated: DocSearch):
        # Single-term AND query: score == count of that term in the doc.
        hits = populated.search("fox")
        for h in hits:
            assert h.match_count == int(h.score)

    def test_phrase_score(self, populated: DocSearch):
        hits = populated.search_phrase("the fox")
        d4 = next(h for h in hits if h.doc_id == "d4")
        assert d4.score == 2.0


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_index_searches(self, empty: DocSearch):
        assert empty.search("x") == []
        assert empty.search_phrase("x y") == []
        assert empty.search_regex("x") == []
        assert empty.search_boolean(must=["x"]) == []

    def test_doc_count_property(self, populated: DocSearch):
        assert populated.doc_count == 5

    def test_special_chars(self, empty: DocSearch):
        empty.index("d", "Hello, World! foo@bar.com (test).")
        # Punctuation should be stripped by tokenization.
        assert empty.count_matches("hello") == 1
        assert empty.count_matches("foo") == 1

    def test_advanced_no_terms(self, populated: DocSearch):
        q = SearchQuery(terms=[])
        assert populated.search_advanced(q) == []

    def test_not_operator(self, populated: DocSearch):
        q = SearchQuery(terms=["fox"], operator="NOT")
        ids = {h.doc_id for h in populated.search_advanced(q)}
        # Docs that don't contain fox.
        assert ids == {"d3", "d5"}

    def test_index_empty_string(self, empty: DocSearch):
        empty.index("d", "")
        assert empty.doc_count == 1
        assert empty.search("anything") == []

    def test_search_hit_has_match_type(self, populated: DocSearch):
        hits = populated.search("fox")
        for h in hits:
            assert h.match_type is MatchType.EXACT

    def test_phrase_hits_have_phrase_type(self, populated: DocSearch):
        hits = populated.search_phrase("quick brown")
        for h in hits:
            assert h.match_type is MatchType.PHRASE

    def test_regex_hits_have_regex_type(self, populated: DocSearch):
        hits = populated.search_regex(r"fox")
        for h in hits:
            assert h.match_type is MatchType.REGEX

    def test_regex_via_advanced(self, populated: DocSearch):
        q = SearchQuery(terms=[r"qu\w+"], match_type=MatchType.REGEX)
        ids = {h.doc_id for h in populated.search_advanced(q)}
        assert ids == {"d1", "d2", "d4"}
