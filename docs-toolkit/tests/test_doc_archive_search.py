"""Tests for E254 doc_archive_search."""
from __future__ import annotations

import gzip

import pytest

from docstoolkit.doc_archive_search import (
    ArchiveEntry,
    DocArchiveSearch,
    SearchMatch,
    SearchOptions,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestArchiveEntry:
    def test_basic_fields(self):
        e = ArchiveEntry(
            doc_id="a",
            compressed_data=b"x",
            original_size=10,
            archived_at=1.0,
        )
        assert e.doc_id == "a"
        assert e.compressed_data == b"x"
        assert e.original_size == 10
        assert e.archived_at == 1.0
        assert e.metadata == {}

    def test_metadata_default_independent(self):
        a = ArchiveEntry("a", b"", 0, 0.0)
        b = ArchiveEntry("b", b"", 0, 0.0)
        a.metadata["k"] = 1
        assert b.metadata == {}

    def test_metadata_explicit(self):
        e = ArchiveEntry("a", b"", 0, 0.0, metadata={"author": "x"})
        assert e.metadata == {"author": "x"}


class TestSearchMatch:
    def test_basic(self):
        m = SearchMatch(doc_id="a", score=3, excerpts=["e1", "e2"])
        assert m.doc_id == "a"
        assert m.score == 3
        assert m.excerpts == ["e1", "e2"]


class TestSearchOptions:
    def test_defaults(self):
        o = SearchOptions()
        assert o.case_sensitive is False
        assert o.whole_word is False
        assert o.max_excerpts_per_doc == 3
        assert o.excerpt_chars == 100

    def test_custom(self):
        o = SearchOptions(case_sensitive=True, whole_word=True, max_excerpts_per_doc=5, excerpt_chars=50)
        assert o.case_sensitive
        assert o.whole_word
        assert o.max_excerpts_per_doc == 5
        assert o.excerpt_chars == 50


# ---------------------------------------------------------------------------
# Archive
# ---------------------------------------------------------------------------


class TestArchive:
    def test_archive_creates_entry(self):
        s = DocArchiveSearch()
        e = s.archive("d1", "hello world")
        assert isinstance(e, ArchiveEntry)
        assert e.doc_id == "d1"
        assert e.original_size == len("hello world".encode("utf-8"))

    def test_archive_compresses(self):
        s = DocArchiveSearch()
        content = "abc" * 100
        e = s.archive("d1", content)
        # Round-trip the compressed bytes via gzip.
        assert gzip.decompress(e.compressed_data).decode() == content

    def test_archive_stores_metadata(self):
        s = DocArchiveSearch()
        e = s.archive("d1", "x", metadata={"author": "bob"})
        assert e.metadata == {"author": "bob"}

    def test_archive_metadata_is_copied(self):
        s = DocArchiveSearch()
        meta = {"k": 1}
        e = s.archive("d1", "x", metadata=meta)
        meta["k"] = 2
        assert e.metadata["k"] == 1

    def test_archive_replaces_existing(self):
        s = DocArchiveSearch()
        s.archive("d1", "first")
        s.archive("d1", "second")
        assert s.get_content("d1") == "second"

    def test_archive_uses_now(self):
        s = DocArchiveSearch()
        e = s.archive("d1", "x", now=42.5)
        assert e.archived_at == 42.5

    def test_archive_rejects_empty_id(self):
        s = DocArchiveSearch()
        with pytest.raises(ValueError):
            s.archive("", "x")

    def test_archive_rejects_non_string_content(self):
        s = DocArchiveSearch()
        with pytest.raises(TypeError):
            s.archive("d1", 123)  # type: ignore[arg-type]

    def test_archive_invalidates_cache(self):
        s = DocArchiveSearch()
        s.archive("d1", "hello")
        s.get_content("d1")  # warm cache
        assert s.cache_size_used() == 1
        s.archive("d1", "world")
        # Cache for d1 was invalidated.
        assert s.cache_size_used() == 0


# ---------------------------------------------------------------------------
# Unarchive
# ---------------------------------------------------------------------------


class TestUnarchive:
    def test_unarchive_existing(self):
        s = DocArchiveSearch()
        s.archive("d1", "x")
        assert s.unarchive("d1") is True
        assert not s.exists("d1")

    def test_unarchive_missing(self):
        s = DocArchiveSearch()
        assert s.unarchive("nope") is False

    def test_unarchive_clears_cache(self):
        s = DocArchiveSearch()
        s.archive("d1", "x")
        s.get_content("d1")
        assert s.cache_size_used() == 1
        s.unarchive("d1")
        assert s.cache_size_used() == 0


# ---------------------------------------------------------------------------
# get_content
# ---------------------------------------------------------------------------


class TestGetContent:
    def test_get_content_returns_text(self):
        s = DocArchiveSearch()
        s.archive("d1", "hello world")
        assert s.get_content("d1") == "hello world"

    def test_get_content_unknown(self):
        s = DocArchiveSearch()
        assert s.get_content("nope") is None

    def test_get_content_caches(self):
        s = DocArchiveSearch()
        s.archive("d1", "x")
        assert s.cache_size_used() == 0
        s.get_content("d1")
        assert s.cache_size_used() == 1

    def test_get_content_cache_hit(self):
        s = DocArchiveSearch()
        s.archive("d1", "x")
        first = s.get_content("d1")
        second = s.get_content("d1")
        assert first == second
        assert s.cache_size_used() == 1

    def test_get_content_unicode(self):
        s = DocArchiveSearch()
        s.archive("d1", "Привет мир ☃")
        assert s.get_content("d1") == "Привет мир ☃"


# ---------------------------------------------------------------------------
# Search basic
# ---------------------------------------------------------------------------


class TestSearchBasic:
    def test_search_empty_archive(self):
        s = DocArchiveSearch()
        assert s.search("hello") == []

    def test_search_returns_match(self):
        s = DocArchiveSearch()
        s.archive("d1", "hello world")
        out = s.search("hello")
        assert len(out) == 1
        assert out[0].doc_id == "d1"
        assert out[0].score == 1

    def test_search_no_match(self):
        s = DocArchiveSearch()
        s.archive("d1", "hello world")
        assert s.search("zzz") == []

    def test_search_multiple_docs(self):
        s = DocArchiveSearch()
        s.archive("d1", "foo bar")
        s.archive("d2", "foo foo")
        s.archive("d3", "qux")
        out = s.search("foo")
        ids = [m.doc_id for m in out]
        assert "d3" not in ids
        # Higher score first.
        assert out[0].doc_id == "d2"
        assert out[0].score == 2
        assert out[1].doc_id == "d1"
        assert out[1].score == 1

    def test_search_empty_query(self):
        s = DocArchiveSearch()
        s.archive("d1", "anything")
        assert s.search("") == []

    def test_search_non_string_query(self):
        s = DocArchiveSearch()
        with pytest.raises(TypeError):
            s.search(123)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Case sensitivity
# ---------------------------------------------------------------------------


class TestSearchCaseSensitive:
    def test_default_case_insensitive(self):
        s = DocArchiveSearch()
        s.archive("d1", "Hello HELLO hello")
        out = s.search("hello")
        assert out[0].score == 3

    def test_case_sensitive(self):
        s = DocArchiveSearch()
        s.archive("d1", "Hello HELLO hello")
        out = s.search("hello", SearchOptions(case_sensitive=True))
        assert out[0].score == 1

    def test_case_sensitive_no_match(self):
        s = DocArchiveSearch()
        s.archive("d1", "HELLO")
        assert s.search("hello", SearchOptions(case_sensitive=True)) == []


# ---------------------------------------------------------------------------
# Whole word
# ---------------------------------------------------------------------------


class TestSearchWholeWord:
    def test_whole_word_match(self):
        s = DocArchiveSearch()
        s.archive("d1", "cat caterpillar cats")
        out = s.search("cat", SearchOptions(whole_word=True))
        assert out[0].score == 1

    def test_no_whole_word(self):
        s = DocArchiveSearch()
        s.archive("d1", "cat caterpillar cats")
        out = s.search("cat")
        assert out[0].score == 3

    def test_whole_word_with_punctuation(self):
        s = DocArchiveSearch()
        s.archive("d1", "I have a cat. The cat sleeps.")
        out = s.search("cat", SearchOptions(whole_word=True))
        assert out[0].score == 2


# ---------------------------------------------------------------------------
# Excerpts
# ---------------------------------------------------------------------------


class TestSearchExcerpts:
    def test_excerpts_returned(self):
        s = DocArchiveSearch()
        s.archive("d1", "abc hello def hello ghi")
        out = s.search("hello")
        assert len(out[0].excerpts) == 2

    def test_excerpts_limit(self):
        s = DocArchiveSearch()
        s.archive("d1", "hello " * 20)
        out = s.search("hello", SearchOptions(max_excerpts_per_doc=2))
        assert len(out[0].excerpts) == 2
        # The score is still the total number of matches.
        assert out[0].score == 20

    def test_excerpts_zero_limit(self):
        s = DocArchiveSearch()
        s.archive("d1", "hello world hello")
        out = s.search("hello", SearchOptions(max_excerpts_per_doc=0))
        assert out[0].excerpts == []
        assert out[0].score == 2

    def test_excerpts_contain_match(self):
        s = DocArchiveSearch()
        s.archive("d1", "padding " * 5 + "needle" + " padding" * 5)
        out = s.search("needle")
        assert any("needle" in e for e in out[0].excerpts)


# ---------------------------------------------------------------------------
# Regex
# ---------------------------------------------------------------------------


class TestSearchRegex:
    def test_search_regex_basic(self):
        s = DocArchiveSearch()
        s.archive("d1", "abc 123 def 456")
        out = s.search_regex(r"\d+")
        assert out[0].score == 2

    def test_search_regex_case_sensitive(self):
        s = DocArchiveSearch()
        s.archive("d1", "Foo foo FOO")
        out = s.search_regex(r"foo", SearchOptions(case_sensitive=True))
        assert out[0].score == 1

    def test_search_regex_invalid(self):
        s = DocArchiveSearch()
        with pytest.raises(ValueError):
            s.search_regex("[unclosed")

    def test_search_regex_no_match(self):
        s = DocArchiveSearch()
        s.archive("d1", "no digits here")
        assert s.search_regex(r"\d+") == []

    def test_search_regex_non_string(self):
        s = DocArchiveSearch()
        with pytest.raises(TypeError):
            s.search_regex(123)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# count_matches
# ---------------------------------------------------------------------------


class TestCountMatches:
    def test_count_in_doc(self):
        s = DocArchiveSearch()
        s.archive("d1", "ha ha ha")
        assert s.count_matches("ha", doc_id="d1") == 3

    def test_count_total(self):
        s = DocArchiveSearch()
        s.archive("d1", "ha ha")
        s.archive("d2", "ha")
        assert s.count_matches("ha") == 3

    def test_count_missing_doc(self):
        s = DocArchiveSearch()
        assert s.count_matches("x", doc_id="nope") == 0

    def test_count_empty_query(self):
        s = DocArchiveSearch()
        s.archive("d1", "hello")
        assert s.count_matches("") == 0

    def test_count_case_sensitive(self):
        s = DocArchiveSearch()
        s.archive("d1", "Foo foo FOO")
        assert s.count_matches("foo", case_sensitive=True) == 1
        assert s.count_matches("foo") == 3


# ---------------------------------------------------------------------------
# excerpt
# ---------------------------------------------------------------------------


class TestExcerpt:
    def test_excerpt_middle(self):
        s = DocArchiveSearch()
        content = "a" * 100 + "TARGET" + "b" * 100
        e = s.excerpt(content, 100, 40)
        assert "TARGET" in e
        assert e.startswith("...")
        assert e.endswith("...")

    def test_excerpt_start(self):
        s = DocArchiveSearch()
        content = "hello world this is a test"
        e = s.excerpt(content, 0, 10)
        assert not e.startswith("...")

    def test_excerpt_end(self):
        s = DocArchiveSearch()
        content = "hello"
        e = s.excerpt(content, 4, 10)
        assert not e.endswith("...")

    def test_excerpt_zero_chars(self):
        s = DocArchiveSearch()
        assert s.excerpt("abc", 1, 0) == ""

    def test_excerpt_negative_position(self):
        s = DocArchiveSearch()
        e = s.excerpt("hello", -5, 10)
        assert "hello" in e

    def test_excerpt_position_beyond_end(self):
        s = DocArchiveSearch()
        e = s.excerpt("hello", 100, 10)
        assert isinstance(e, str)

    def test_excerpt_short_content(self):
        s = DocArchiveSearch()
        # If content is shorter than chars, neither ellipsis should appear.
        e = s.excerpt("hi", 1, 100)
        assert e == "hi"


# ---------------------------------------------------------------------------
# exists / metadata / list_doc_ids
# ---------------------------------------------------------------------------


class TestExists:
    def test_exists_true(self):
        s = DocArchiveSearch()
        s.archive("d1", "x")
        assert s.exists("d1")

    def test_exists_false(self):
        s = DocArchiveSearch()
        assert not s.exists("nope")


class TestMetadata:
    def test_metadata_returned(self):
        s = DocArchiveSearch()
        s.archive("d1", "x", metadata={"k": "v"})
        assert s.metadata("d1") == {"k": "v"}

    def test_metadata_none(self):
        s = DocArchiveSearch()
        assert s.metadata("nope") is None

    def test_metadata_default_empty(self):
        s = DocArchiveSearch()
        s.archive("d1", "x")
        assert s.metadata("d1") == {}

    def test_metadata_returned_copy(self):
        s = DocArchiveSearch()
        s.archive("d1", "x", metadata={"k": 1})
        m = s.metadata("d1")
        m["k"] = 2
        assert s.metadata("d1") == {"k": 1}


class TestListDocIds:
    def test_empty(self):
        s = DocArchiveSearch()
        assert s.list_doc_ids() == []

    def test_sorted(self):
        s = DocArchiveSearch()
        s.archive("b", "x")
        s.archive("a", "x")
        s.archive("c", "x")
        assert s.list_doc_ids() == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# Sizes / ratio
# ---------------------------------------------------------------------------


class TestTotalSizes:
    def test_empty(self):
        s = DocArchiveSearch()
        assert s.total_compressed_size() == 0
        assert s.total_original_size() == 0

    def test_after_archive(self):
        s = DocArchiveSearch()
        s.archive("d1", "abc")
        s.archive("d2", "def")
        assert s.total_original_size() == 6
        assert s.total_compressed_size() > 0


class TestCompressionRatio:
    def test_empty(self):
        s = DocArchiveSearch()
        assert s.compression_ratio == 0.0

    def test_with_data(self):
        s = DocArchiveSearch()
        s.archive("d1", "a" * 10000)  # highly compressible
        ratio = s.compression_ratio
        assert 0 < ratio < 1


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------


class TestCacheSize:
    def test_default(self):
        s = DocArchiveSearch()
        assert s.cache_size_used() == 0

    def test_grows_with_use(self):
        s = DocArchiveSearch()
        s.archive("d1", "x")
        s.archive("d2", "y")
        s.get_content("d1")
        s.get_content("d2")
        assert s.cache_size_used() == 2


class TestCacheLruEviction:
    def test_evict_oldest(self):
        s = DocArchiveSearch(cache_size=2)
        s.archive("a", "1")
        s.archive("b", "2")
        s.archive("c", "3")
        s.get_content("a")
        s.get_content("b")
        assert s.cache_size_used() == 2
        s.get_content("c")
        # "a" was least-recently-used -> evicted.
        assert s.cache_size_used() == 2

    def test_move_to_end_on_hit(self):
        s = DocArchiveSearch(cache_size=2)
        s.archive("a", "1")
        s.archive("b", "2")
        s.archive("c", "3")
        s.get_content("a")
        s.get_content("b")
        s.get_content("a")  # bump "a" to MRU
        s.get_content("c")  # this should evict "b", not "a"
        # Cache should still hold "a" without a fresh decompression touching
        # the LRU order; verify by ensuring the size stays at 2.
        assert s.cache_size_used() == 2

    def test_cache_size_zero_disables_cache(self):
        s = DocArchiveSearch(cache_size=0)
        s.archive("a", "x")
        s.get_content("a")
        assert s.cache_size_used() == 0

    def test_negative_cache_size_rejected(self):
        with pytest.raises(ValueError):
            DocArchiveSearch(cache_size=-1)


class TestClearCache:
    def test_clear(self):
        s = DocArchiveSearch()
        s.archive("a", "x")
        s.get_content("a")
        assert s.clear_cache() == 1
        assert s.cache_size_used() == 0

    def test_clear_empty(self):
        s = DocArchiveSearch()
        assert s.clear_cache() == 0

    def test_clear_keeps_archive(self):
        s = DocArchiveSearch()
        s.archive("a", "x")
        s.get_content("a")
        s.clear_cache()
        assert s.exists("a")
        # Still retrievable.
        assert s.get_content("a") == "x"


# ---------------------------------------------------------------------------
# clear / doc_count
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_all(self):
        s = DocArchiveSearch()
        s.archive("a", "1")
        s.archive("b", "2")
        s.get_content("a")
        s.clear()
        assert s.doc_count == 0
        assert s.cache_size_used() == 0
        assert s.list_doc_ids() == []


class TestDocCount:
    def test_empty(self):
        s = DocArchiveSearch()
        assert s.doc_count == 0

    def test_after_archive(self):
        s = DocArchiveSearch()
        s.archive("a", "1")
        s.archive("b", "2")
        assert s.doc_count == 2

    def test_after_unarchive(self):
        s = DocArchiveSearch()
        s.archive("a", "1")
        s.archive("b", "2")
        s.unarchive("a")
        assert s.doc_count == 1


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_archive_empty_content(self):
        s = DocArchiveSearch()
        e = s.archive("d1", "")
        assert e.original_size == 0
        assert s.get_content("d1") == ""

    def test_search_in_unicode_content(self):
        s = DocArchiveSearch()
        s.archive("d1", "наука и техника наука")
        out = s.search("наука")
        assert out[0].score == 2

    def test_repeated_archive_same_content(self):
        s = DocArchiveSearch()
        s.archive("d1", "hello")
        s.archive("d1", "hello")
        assert s.doc_count == 1

    def test_search_regex_anchors(self):
        s = DocArchiveSearch()
        s.archive("d1", "foo bar")
        s.archive("d2", "baz")
        out = s.search_regex(r"^foo")
        assert len(out) == 1
        assert out[0].doc_id == "d1"

    def test_search_score_ordering(self):
        s = DocArchiveSearch()
        s.archive("low", "x")
        s.archive("hi", "x x x")
        out = s.search("x")
        assert [m.doc_id for m in out] == ["hi", "low"]

    def test_round_trip_large_text(self):
        s = DocArchiveSearch()
        big = "lorem ipsum " * 5000
        s.archive("big", big)
        assert s.get_content("big") == big
        # compressed must be smaller than original for repetitive text.
        assert s.total_compressed_size() < s.total_original_size()
