"""Tests for E348 DocTokenIndex."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_token_index import DocTokenIndex, IndexStats, TokenInfo


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestTokenInfoDataclass:
    def test_construction(self):
        ti = TokenInfo(token="foo", doc_count=2, total_count=5)
        assert ti.token == "foo"
        assert ti.doc_count == 2
        assert ti.total_count == 5

    def test_equality(self):
        a = TokenInfo("x", 1, 2)
        b = TokenInfo("x", 1, 2)
        assert a == b

    def test_inequality(self):
        a = TokenInfo("x", 1, 2)
        b = TokenInfo("y", 1, 2)
        assert a != b

    def test_fields_mutable(self):
        ti = TokenInfo("a", 1, 1)
        ti.doc_count = 5
        assert ti.doc_count == 5


class TestIndexStatsDataclass:
    def test_construction(self):
        s = IndexStats(total_docs=3, unique_tokens=10, total_tokens=20)
        assert s.total_docs == 3
        assert s.unique_tokens == 10
        assert s.total_tokens == 20

    def test_equality(self):
        a = IndexStats(1, 2, 3)
        b = IndexStats(1, 2, 3)
        assert a == b

    def test_zero_defaults_via_construction(self):
        s = IndexStats(0, 0, 0)
        assert s.total_docs == 0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_index(self):
        idx = DocTokenIndex()
        assert idx.stats().total_docs == 0
        assert idx.stats().unique_tokens == 0
        assert idx.stats().total_tokens == 0

    def test_independent_instances(self):
        a = DocTokenIndex()
        b = DocTokenIndex()
        a.index_doc("d1", "hello world")
        assert b.stats().total_docs == 0


# ---------------------------------------------------------------------------
# index_doc
# ---------------------------------------------------------------------------


class TestIndexDoc:
    def test_returns_token_count(self):
        idx = DocTokenIndex()
        assert idx.index_doc("d1", "hello world hello") == 3

    def test_counts_tokens(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo bar foo")
        assert idx.token_count_in_doc("d1", "foo") == 2
        assert idx.token_count_in_doc("d1", "bar") == 1

    def test_lowercases_tokens(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "Hello HELLO hello")
        assert idx.token_count_in_doc("d1", "hello") == 3

    def test_ignores_punctuation(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "hello, world! hello.")
        assert idx.token_count_in_doc("d1", "hello") == 2
        assert idx.token_count_in_doc("d1", "world") == 1

    def test_alphanumeric_tokens(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "abc123 test42")
        assert idx.token_count_in_doc("d1", "abc123") == 1
        assert idx.token_count_in_doc("d1", "test42") == 1

    def test_reindex_replaces(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo bar")
        idx.index_doc("d1", "baz qux")
        assert idx.token_count_in_doc("d1", "foo") == 0
        assert idx.token_count_in_doc("d1", "baz") == 1
        info = idx.token_info("foo")
        assert info is None

    def test_reindex_updates_totals(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo foo")
        idx.index_doc("d2", "foo")
        idx.index_doc("d1", "bar")
        info = idx.token_info("foo")
        assert info is not None
        assert info.total_count == 1
        assert info.doc_count == 1

    def test_empty_text(self):
        idx = DocTokenIndex()
        assert idx.index_doc("d1", "") == 0
        assert idx.tokens_for_doc("d1") == {}

    def test_multiple_docs(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "a b c")
        idx.index_doc("d2", "b c d")
        assert idx.stats().total_docs == 2
        assert idx.stats().unique_tokens == 4


# ---------------------------------------------------------------------------
# remove_doc
# ---------------------------------------------------------------------------


class TestRemoveDoc:
    def test_returns_true_when_present(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "hello")
        assert idx.remove_doc("d1") is True

    def test_returns_false_when_absent(self):
        idx = DocTokenIndex()
        assert idx.remove_doc("d1") is False

    def test_totals_updated(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo foo")
        idx.index_doc("d2", "foo bar")
        idx.remove_doc("d1")
        info = idx.token_info("foo")
        assert info is not None
        assert info.total_count == 1
        assert info.doc_count == 1

    def test_token_disappears_when_no_docs(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "unique")
        idx.remove_doc("d1")
        assert idx.token_info("unique") is None

    def test_doc_tokens_gone(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "x y")
        idx.remove_doc("d1")
        assert idx.tokens_for_doc("d1") == {}

    def test_remove_twice(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "x")
        assert idx.remove_doc("d1") is True
        assert idx.remove_doc("d1") is False


# ---------------------------------------------------------------------------
# tokens_for_doc
# ---------------------------------------------------------------------------


class TestTokensForDoc:
    def test_returns_dict(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo bar foo")
        assert idx.tokens_for_doc("d1") == {"foo": 2, "bar": 1}

    def test_returns_copy(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo")
        d = idx.tokens_for_doc("d1")
        d["mutated"] = 99
        assert idx.token_count_in_doc("d1", "mutated") == 0

    def test_missing_doc(self):
        idx = DocTokenIndex()
        assert idx.tokens_for_doc("missing") == {}


# ---------------------------------------------------------------------------
# docs_for_token
# ---------------------------------------------------------------------------


class TestDocsForToken:
    def test_sorted_doc_ids(self):
        idx = DocTokenIndex()
        idx.index_doc("d2", "foo")
        idx.index_doc("d1", "foo")
        idx.index_doc("d3", "foo")
        assert idx.docs_for_token("foo") == ["d1", "d2", "d3"]

    def test_empty_for_unknown(self):
        idx = DocTokenIndex()
        assert idx.docs_for_token("nope") == []

    def test_case_insensitive(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "FOO")
        assert idx.docs_for_token("Foo") == ["d1"]

    def test_only_docs_that_contain(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo bar")
        idx.index_doc("d2", "baz")
        assert idx.docs_for_token("foo") == ["d1"]


# ---------------------------------------------------------------------------
# token_count_in_doc
# ---------------------------------------------------------------------------


class TestTokenCountInDoc:
    def test_present(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "x x x y")
        assert idx.token_count_in_doc("d1", "x") == 3

    def test_absent(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "x")
        assert idx.token_count_in_doc("d1", "y") == 0

    def test_unknown_doc(self):
        idx = DocTokenIndex()
        assert idx.token_count_in_doc("nope", "x") == 0

    def test_case_insensitive(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "Foo foo FOO")
        assert idx.token_count_in_doc("d1", "FOO") == 3


# ---------------------------------------------------------------------------
# token_info
# ---------------------------------------------------------------------------


class TestTokenInfo:
    def test_fields_populated(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo foo")
        idx.index_doc("d2", "foo bar")
        info = idx.token_info("foo")
        assert info is not None
        assert info.token == "foo"
        assert info.doc_count == 2
        assert info.total_count == 3

    def test_none_for_unknown(self):
        idx = DocTokenIndex()
        assert idx.token_info("nope") is None

    def test_case_insensitive(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "Foo")
        info = idx.token_info("FOO")
        assert info is not None
        assert info.token == "foo"


# ---------------------------------------------------------------------------
# top_tokens
# ---------------------------------------------------------------------------


class TestTopTokens:
    def test_sorted_by_total_desc(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "a a a b b c")
        top = idx.top_tokens(limit=3)
        assert top == [("a", 3), ("b", 2), ("c", 1)]

    def test_tie_broken_by_token_asc(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "b a c")
        top = idx.top_tokens(limit=3)
        assert top == [("a", 1), ("b", 1), ("c", 1)]

    def test_limit_respected(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "a b c d e")
        assert len(idx.top_tokens(limit=2)) == 2

    def test_empty(self):
        idx = DocTokenIndex()
        assert idx.top_tokens() == []


# ---------------------------------------------------------------------------
# co_occurring_tokens
# ---------------------------------------------------------------------------


class TestCoOccurringTokens:
    def test_only_docs_sharing_the_token(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo bar baz")
        idx.index_doc("d2", "foo qux")
        idx.index_doc("d3", "unrelated stuff")
        co = idx.co_occurring_tokens("foo")
        assert "unrelated" not in co
        assert "bar" in co
        assert "qux" in co

    def test_excludes_self(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo bar")
        assert "foo" not in idx.co_occurring_tokens("foo")

    def test_sorted_by_joint_desc_then_asc(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo a b")
        idx.index_doc("d2", "foo a c")
        co = idx.co_occurring_tokens("foo")
        assert co[0] == "a"  # appears in both d1 and d2

    def test_unknown_token(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "x")
        assert idx.co_occurring_tokens("nope") == []

    def test_limit_respected(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "foo a b c d e")
        assert len(idx.co_occurring_tokens("foo", limit=2)) == 2


# ---------------------------------------------------------------------------
# search (alias)
# ---------------------------------------------------------------------------


class TestSearch:
    def test_alias_behavior(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "hello")
        idx.index_doc("d2", "hello")
        assert idx.search("hello") == idx.docs_for_token("hello")

    def test_empty(self):
        idx = DocTokenIndex()
        assert idx.search("nope") == []


# ---------------------------------------------------------------------------
# tokens_starting_with
# ---------------------------------------------------------------------------


class TestTokensStartingWith:
    def test_sorted_prefix_match(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "apple application apex banana")
        result = idx.tokens_starting_with("ap")
        assert result == ["apex", "apple", "application"]

    def test_case_insensitive(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "Apple Apex")
        assert idx.tokens_starting_with("AP") == ["apex", "apple"]

    def test_no_matches(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "hello")
        assert idx.tokens_starting_with("xyz") == []

    def test_empty_prefix_returns_all(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "b a c")
        assert idx.tokens_starting_with("") == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_returns_count(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "x")
        idx.index_doc("d2", "y")
        assert idx.clear() == 2

    def test_empty_clear(self):
        idx = DocTokenIndex()
        assert idx.clear() == 0

    def test_state_after_clear(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "x")
        idx.clear()
        s = idx.stats()
        assert s.total_docs == 0
        assert s.unique_tokens == 0
        assert s.total_tokens == 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_totals(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "a a b")
        idx.index_doc("d2", "b c")
        s = idx.stats()
        assert s.total_docs == 2
        assert s.unique_tokens == 3
        assert s.total_tokens == 5

    def test_empty(self):
        idx = DocTokenIndex()
        s = idx.stats()
        assert s == IndexStats(0, 0, 0)

    def test_after_removal(self):
        idx = DocTokenIndex()
        idx.index_doc("d1", "a b")
        idx.index_doc("d2", "c d")
        idx.remove_doc("d1")
        s = idx.stats()
        assert s.total_docs == 1
        assert s.unique_tokens == 2
        assert s.total_tokens == 2


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_index_doc(self):
        idx = DocTokenIndex()
        n_threads = 16
        n_docs_each = 25

        def worker(tid: int) -> None:
            for i in range(n_docs_each):
                idx.index_doc(f"t{tid}-d{i}", f"token{tid} shared word{i % 5}")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = idx.stats()
        assert s.total_docs == n_threads * n_docs_each
        # "shared" should appear in every doc
        info = idx.token_info("shared")
        assert info is not None
        assert info.doc_count == n_threads * n_docs_each
        assert info.total_count == n_threads * n_docs_each

    def test_concurrent_mixed(self):
        idx = DocTokenIndex()
        for i in range(50):
            idx.index_doc(f"d{i}", f"word{i} common")

        errors: list[Exception] = []

        def remover() -> None:
            try:
                for i in range(50):
                    idx.remove_doc(f"d{i}")
            except Exception as e:  # pragma: no cover - safety net
                errors.append(e)

        def reader() -> None:
            try:
                for _ in range(100):
                    idx.docs_for_token("common")
                    idx.stats()
            except Exception as e:  # pragma: no cover - safety net
                errors.append(e)

        threads = [
            threading.Thread(target=remover),
            threading.Thread(target=reader),
            threading.Thread(target=reader),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
