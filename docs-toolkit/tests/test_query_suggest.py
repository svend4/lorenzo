"""Tests for the query_suggest module (E29).

Covers:
- QueryTrie: insert, search, starts_with, node_count, query_count
- QueryHistory: record, top_queries, recent_queries, popular_for_prefix, total_queries
- QuerySuggester: suggest ordering, min_prefix_len guard, dedup, complete()
- Edge cases: empty prefix, unknown prefix, single query, case normalisation
"""
from __future__ import annotations

import pytest

from docstoolkit.query_suggest.trie import TrieNode, QueryTrie
from docstoolkit.query_suggest.history import QueryHistory
from docstoolkit.query_suggest.suggester import (
    SuggestionConfig,
    Suggestion,
    QuerySuggester,
)
from docstoolkit.query_suggest import (
    TrieNode as _TrieNode,
    QueryTrie as _QueryTrie,
    QueryHistory as _QueryHistory,
    SuggestionConfig as _SuggestionConfig,
    Suggestion as _Suggestion,
    QuerySuggester as _QuerySuggester,
)


# ===========================================================================
# TrieNode
# ===========================================================================


class TestTrieNode:
    def test_default_children_empty(self):
        node = TrieNode()
        assert node.children == {}

    def test_default_is_end_false(self):
        node = TrieNode()
        assert node.is_end is False

    def test_default_count_zero(self):
        node = TrieNode()
        assert node.count == 0

    def test_default_query_empty_string(self):
        node = TrieNode()
        assert node.query == ""

    def test_can_set_fields(self):
        child = TrieNode(is_end=True, count=3, query="hello")
        assert child.is_end is True
        assert child.count == 3
        assert child.query == "hello"

    def test_children_are_independent_across_instances(self):
        n1 = TrieNode()
        n2 = TrieNode()
        n1.children["a"] = TrieNode()
        assert "a" not in n2.children


# ===========================================================================
# QueryTrie — basic insertion
# ===========================================================================


class TestQueryTrieInsert:
    def test_empty_trie_query_count_zero(self):
        t = QueryTrie()
        assert t.query_count() == 0

    def test_insert_single_query(self):
        t = QueryTrie()
        t.insert("hello")
        assert t.query_count() == 1

    def test_insert_two_distinct_queries(self):
        t = QueryTrie()
        t.insert("hello")
        t.insert("world")
        assert t.query_count() == 2

    def test_insert_same_query_twice_counts_once(self):
        t = QueryTrie()
        t.insert("hello")
        t.insert("hello")
        assert t.query_count() == 1

    def test_insert_accumulates_count(self):
        t = QueryTrie()
        t.insert("hello", count=3)
        t.insert("hello", count=2)
        results = t.search("hel")
        assert results[0] == ("hello", 5)

    def test_insert_normalises_case(self):
        t = QueryTrie()
        t.insert("Hello")
        t.insert("HELLO")
        assert t.query_count() == 1

    def test_insert_normalises_leading_trailing_spaces(self):
        t = QueryTrie()
        t.insert("  hello  ")
        assert t.search("hello") == [("hello", 1)]

    def test_insert_empty_string_is_ignored(self):
        t = QueryTrie()
        t.insert("")
        assert t.query_count() == 0

    def test_insert_whitespace_only_is_ignored(self):
        t = QueryTrie()
        t.insert("   ")
        assert t.query_count() == 0

    def test_node_count_grows(self):
        t = QueryTrie()
        before = t.node_count()
        t.insert("abc")
        assert t.node_count() > before

    def test_shared_prefix_reuses_nodes(self):
        t = QueryTrie()
        t.insert("abc")
        after_first = t.node_count()
        t.insert("abd")
        # Only one new node added for 'd' (a, b already exist)
        assert t.node_count() == after_first + 1


# ===========================================================================
# QueryTrie — search
# ===========================================================================


class TestQueryTrieSearch:
    def setup_method(self):
        self.t = QueryTrie()
        self.t.insert("python tutorial", count=10)
        self.t.insert("python basics", count=5)
        self.t.insert("python advanced", count=3)
        self.t.insert("java tutorial", count=7)

    def test_search_full_match(self):
        results = self.t.search("python tutorial")
        assert results == [("python tutorial", 10)]

    def test_search_prefix_returns_matching(self):
        queries = [q for q, _ in self.t.search("python")]
        assert set(queries) == {"python tutorial", "python basics", "python advanced"}

    def test_search_sorted_by_count_desc(self):
        results = self.t.search("python")
        counts = [c for _, c in results]
        assert counts == sorted(counts, reverse=True)

    def test_search_unknown_prefix_returns_empty(self):
        assert self.t.search("ruby") == []

    def test_search_empty_prefix_returns_all(self):
        results = self.t.search("")
        assert len(results) == 4

    def test_search_case_insensitive(self):
        results = self.t.search("PYTHON")
        assert len(results) == 3

    def test_search_single_char_prefix(self):
        results = self.t.search("j")
        assert results == [("java tutorial", 7)]


# ===========================================================================
# QueryTrie — starts_with
# ===========================================================================


class TestQueryTrieStartsWith:
    def setup_method(self):
        self.t = QueryTrie()
        self.t.insert("machine learning")
        self.t.insert("machine translation")

    def test_starts_with_known_prefix(self):
        assert self.t.starts_with("machine") is True

    def test_starts_with_full_query(self):
        assert self.t.starts_with("machine learning") is True

    def test_starts_with_unknown_prefix(self):
        assert self.t.starts_with("deep learning") is False

    def test_starts_with_empty_string(self):
        # Empty string is a prefix of everything
        assert self.t.starts_with("") is True

    def test_starts_with_case_insensitive(self):
        assert self.t.starts_with("MACHINE") is True


# ===========================================================================
# QueryTrie — counts
# ===========================================================================


class TestQueryTrieCounts:
    def test_node_count_includes_root(self):
        t = QueryTrie()
        assert t.node_count() == 1  # root only

    def test_node_count_single_char_query(self):
        t = QueryTrie()
        t.insert("a")
        assert t.node_count() == 2  # root + 'a'

    def test_query_count_after_multiple_inserts(self):
        t = QueryTrie()
        for w in ["alpha", "beta", "gamma", "delta"]:
            t.insert(w)
        assert t.query_count() == 4


# ===========================================================================
# QueryHistory
# ===========================================================================


class TestQueryHistoryRecord:
    def test_total_queries_starts_zero(self):
        h = QueryHistory()
        assert h.total_queries() == 0

    def test_record_increments_total(self):
        h = QueryHistory()
        h.record("search term")
        assert h.total_queries() == 1

    def test_record_multiple_times_same_query(self):
        h = QueryHistory()
        for _ in range(5):
            h.record("repeat")
        assert h.total_queries() == 5

    def test_record_normalises_case(self):
        h = QueryHistory()
        h.record("HELLO")
        assert h.top_queries(1)[0][0] == "hello"

    def test_record_empty_string_ignored(self):
        h = QueryHistory()
        h.record("")
        assert h.total_queries() == 0

    def test_record_whitespace_only_ignored(self):
        h = QueryHistory()
        h.record("   ")
        assert h.total_queries() == 0


class TestQueryHistoryTopQueries:
    def setup_method(self):
        self.h = QueryHistory()
        for _ in range(10):
            self.h.record("popular query")
        for _ in range(4):
            self.h.record("medium query")
        for _ in range(1):
            self.h.record("rare query")

    def test_top_queries_order(self):
        top = self.h.top_queries(3)
        queries = [q for q, _ in top]
        assert queries[0] == "popular query"
        assert queries[1] == "medium query"

    def test_top_queries_counts(self):
        top = dict(self.h.top_queries(3))
        assert top["popular query"] == 10
        assert top["medium query"] == 4
        assert top["rare query"] == 1

    def test_top_queries_limit(self):
        top = self.h.top_queries(2)
        assert len(top) == 2

    def test_top_queries_empty_history(self):
        h = QueryHistory()
        assert h.top_queries() == []


class TestQueryHistoryRecentQueries:
    def test_recent_queries_order(self):
        h = QueryHistory()
        h.record("first")
        h.record("second")
        h.record("third")
        recent = h.recent_queries(3)
        assert recent[0] == "third"
        assert recent[1] == "second"
        assert recent[2] == "first"

    def test_recent_queries_deduplicates(self):
        h = QueryHistory()
        h.record("a")
        h.record("b")
        h.record("a")  # repeated — should appear once, near top
        recent = h.recent_queries(10)
        assert recent.count("a") == 1

    def test_recent_queries_limit(self):
        h = QueryHistory()
        for i in range(20):
            h.record(f"query{i}")
        assert len(h.recent_queries(5)) == 5

    def test_recent_queries_empty_history(self):
        h = QueryHistory()
        assert h.recent_queries() == []


class TestQueryHistoryPopularForPrefix:
    def setup_method(self):
        self.h = QueryHistory()
        for _ in range(8):
            self.h.record("python tutorial")
        for _ in range(3):
            self.h.record("python basics")
        for _ in range(1):
            self.h.record("java tutorial")

    def test_popular_for_prefix_returns_only_matching(self):
        results = self.h.popular_for_prefix("python")
        queries = [q for q, _ in results]
        assert "java tutorial" not in queries

    def test_popular_for_prefix_sorted_by_count(self):
        results = self.h.popular_for_prefix("python")
        counts = [c for _, c in results]
        assert counts == sorted(counts, reverse=True)

    def test_popular_for_prefix_unknown_returns_empty(self):
        assert self.h.popular_for_prefix("ruby") == []

    def test_popular_for_prefix_limit(self):
        results = self.h.popular_for_prefix("p", n=1)
        assert len(results) == 1

    def test_popular_for_prefix_case_insensitive(self):
        results = self.h.popular_for_prefix("PYTHON")
        assert len(results) == 2


# ===========================================================================
# QuerySuggester
# ===========================================================================


class TestQuerySuggesterBasic:
    def test_empty_trie_returns_empty(self):
        s = QuerySuggester()
        assert s.suggest("py") == []

    def test_below_min_prefix_len_returns_empty(self):
        s = QuerySuggester(SuggestionConfig(min_prefix_len=3))
        s.add_query("python tutorial")
        assert s.suggest("py") == []

    def test_at_min_prefix_len_returns_results(self):
        s = QuerySuggester(SuggestionConfig(min_prefix_len=2))
        s.add_query("python tutorial")
        assert len(s.suggest("py")) > 0

    def test_suggest_unknown_prefix_returns_empty(self):
        s = QuerySuggester()
        s.add_query("python tutorial")
        assert s.suggest("ruby") == []

    def test_suggest_returns_suggestion_objects(self):
        s = QuerySuggester()
        s.add_query("machine learning")
        results = s.suggest("ma")
        assert all(isinstance(r, Suggestion) for r in results)

    def test_suggest_respects_max_suggestions(self):
        cfg = SuggestionConfig(max_suggestions=2)
        s = QuerySuggester(cfg)
        for q in ["python a", "python b", "python c", "python d"]:
            s.add_query(q)
        assert len(s.suggest("python")) <= 2

    def test_suggest_single_query(self):
        s = QuerySuggester()
        s.add_query("only query")
        results = s.suggest("on")
        assert len(results) == 1
        assert results[0].query == "only query"


class TestQuerySuggesterOrdering:
    def test_higher_count_comes_first(self):
        s = QuerySuggester(SuggestionConfig(boost_recent=False, boost_popular=False))
        s.add_query("python popular", count=10)
        s.add_query("python rare", count=1)
        results = s.suggest("py")
        # Both start with 'py' in the trie; popular should rank first
        queries = [r.query for r in results]
        assert queries.index("python popular") < queries.index("python rare")

    def test_scores_in_descending_order(self):
        s = QuerySuggester()
        s.add_query("alpha", count=5)
        s.add_query("always", count=2)
        results = s.suggest("al")
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_score_in_valid_range(self):
        s = QuerySuggester()
        s.add_query("test query", count=7)
        results = s.suggest("te")
        for r in results:
            assert 0.0 <= r.score <= 1.0


class TestQuerySuggesterDedup:
    def test_no_duplicate_queries_in_results(self):
        s = QuerySuggester()
        s.add_query("python tutorial", count=5)
        s.add_query("python tutorial", count=3)
        results = s.suggest("python")
        queries = [r.query for r in results]
        assert len(queries) == len(set(queries))

    def test_trie_and_history_overlap_deduped(self):
        h = QueryHistory()
        h.record("shared query")
        s = QuerySuggester(history=h)
        s.add_query("shared query")
        results = s.suggest("shared")
        queries = [r.query for r in results]
        assert queries.count("shared query") == 1


class TestQuerySuggesterComplete:
    def test_complete_returns_strings(self):
        s = QuerySuggester()
        s.add_query("deep learning")
        result = s.complete("dee")
        assert all(isinstance(q, str) for q in result)

    def test_complete_below_min_prefix_len_returns_empty(self):
        s = QuerySuggester(SuggestionConfig(min_prefix_len=3))
        s.add_query("deep learning")
        assert s.complete("de") == []

    def test_complete_matches_suggest_queries(self):
        s = QuerySuggester()
        s.add_query("neural network")
        s.add_query("natural language")
        assert s.complete("na") == [r.query for r in s.suggest("na")]


class TestQuerySuggesterQueryCount:
    def test_query_count_zero_initially(self):
        s = QuerySuggester()
        assert s.query_count() == 0

    def test_query_count_after_adds(self):
        s = QuerySuggester()
        s.add_query("first")
        s.add_query("second")
        assert s.query_count() == 2

    def test_query_count_same_query_twice(self):
        s = QuerySuggester()
        s.add_query("same")
        s.add_query("same")
        assert s.query_count() == 1


class TestQuerySuggesterSourceField:
    def test_source_is_valid_string(self):
        s = QuerySuggester()
        s.add_query("some query")
        results = s.suggest("so")
        for r in results:
            assert r.source in ("trie", "history", "completion")


class TestQuerySuggesterEdgeCases:
    def test_empty_prefix_below_min_returns_empty(self):
        s = QuerySuggester(SuggestionConfig(min_prefix_len=1))
        s.add_query("anything")
        # Empty string "" has length 0 which is < 1
        assert s.suggest("") == []

    def test_prefix_exactly_at_min_len(self):
        s = QuerySuggester(SuggestionConfig(min_prefix_len=2))
        s.add_query("ab test")
        # prefix "ab" has length 2, equal to min_prefix_len=2
        results = s.suggest("ab")
        assert len(results) > 0

    def test_case_normalised_prefix(self):
        s = QuerySuggester()
        s.add_query("python")
        assert len(s.suggest("PY")) > 0

    def test_shared_history_instance(self):
        h = QueryHistory()
        h.record("shared insight")
        h.record("shared insight")
        h.record("shared insight")
        s = QuerySuggester(history=h)
        results = s.suggest("sh")
        # History results should surface shared insight
        queries = [r.query for r in results]
        assert "shared insight" in queries

    def test_many_queries_max_suggestions_capped(self):
        cfg = SuggestionConfig(max_suggestions=3)
        s = QuerySuggester(cfg)
        for i in range(20):
            s.add_query(f"result {i}")
        assert len(s.suggest("re")) <= 3


# ===========================================================================
# Public API exports
# ===========================================================================


class TestPublicExports:
    def test_trie_node_exported(self):
        assert _TrieNode is TrieNode

    def test_query_trie_exported(self):
        assert _QueryTrie is QueryTrie

    def test_query_history_exported(self):
        assert _QueryHistory is QueryHistory

    def test_suggestion_config_exported(self):
        assert _SuggestionConfig is SuggestionConfig

    def test_suggestion_exported(self):
        assert _Suggestion is Suggestion

    def test_query_suggester_exported(self):
        assert _QuerySuggester is QuerySuggester
