"""Tests for fuzzy_matcher module."""

import pytest

from docstoolkit.fuzzy_matcher import (
    FuzzyAlgo,
    FuzzyConfig,
    FuzzyMatch,
    FuzzyMatcher,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def matcher():
    return FuzzyMatcher()


@pytest.fixture
def case_sensitive_matcher():
    return FuzzyMatcher(FuzzyConfig(case_sensitive=True))


# ---------------------------------------------------------------------------
# Enum and dataclasses
# ---------------------------------------------------------------------------
class TestFuzzyAlgo:
    def test_has_levenshtein(self):
        assert FuzzyAlgo.LEVENSHTEIN.value == "levenshtein"

    def test_has_jaro(self):
        assert FuzzyAlgo.JARO.value == "jaro"

    def test_has_jaro_winkler(self):
        assert FuzzyAlgo.JARO_WINKLER.value == "jaro_winkler"

    def test_has_ngram(self):
        assert FuzzyAlgo.NGRAM.value == "ngram"

    def test_has_ratio(self):
        assert FuzzyAlgo.RATIO.value == "ratio"

    def test_has_partial_ratio(self):
        assert FuzzyAlgo.PARTIAL_RATIO.value == "partial_ratio"

    def test_has_token_sort(self):
        assert FuzzyAlgo.TOKEN_SORT.value == "token_sort"

    def test_has_token_set(self):
        assert FuzzyAlgo.TOKEN_SET.value == "token_set"

    def test_all_unique(self):
        values = [a.value for a in FuzzyAlgo]
        assert len(values) == len(set(values))


class TestFuzzyMatch:
    def test_creation(self):
        m = FuzzyMatch(query="a", target="b", score=0.5, algo=FuzzyAlgo.RATIO)
        assert m.query == "a"
        assert m.target == "b"
        assert m.score == 0.5
        assert m.algo is FuzzyAlgo.RATIO

    def test_default_threshold_flag(self):
        m = FuzzyMatch(query="a", target="b", score=0.5, algo=FuzzyAlgo.RATIO)
        assert m.meets_threshold is False

    def test_explicit_threshold_flag(self):
        m = FuzzyMatch(
            query="a", target="b", score=0.9, algo=FuzzyAlgo.RATIO,
            meets_threshold=True,
        )
        assert m.meets_threshold is True


class TestFuzzyConfig:
    def test_defaults(self):
        c = FuzzyConfig()
        assert c.algo is FuzzyAlgo.RATIO
        assert c.threshold == 0.7
        assert c.case_sensitive is False
        assert c.ngram_size == 2

    def test_custom(self):
        c = FuzzyConfig(
            algo=FuzzyAlgo.JARO_WINKLER,
            threshold=0.9,
            case_sensitive=True,
            ngram_size=3,
        )
        assert c.algo is FuzzyAlgo.JARO_WINKLER
        assert c.threshold == 0.9
        assert c.case_sensitive is True
        assert c.ngram_size == 3


# ---------------------------------------------------------------------------
# Levenshtein
# ---------------------------------------------------------------------------
class TestLevenshteinDistance:
    def test_identical(self, matcher):
        assert matcher.levenshtein_distance("hello", "hello") == 0

    def test_empty_strings(self, matcher):
        assert matcher.levenshtein_distance("", "") == 0

    def test_empty_vs_string(self, matcher):
        assert matcher.levenshtein_distance("", "abc") == 3
        assert matcher.levenshtein_distance("abc", "") == 3

    def test_substitution(self, matcher):
        assert matcher.levenshtein_distance("cat", "bat") == 1

    def test_classic_kitten_sitting(self, matcher):
        assert matcher.levenshtein_distance("kitten", "sitting") == 3

    def test_insertion(self, matcher):
        assert matcher.levenshtein_distance("cat", "cats") == 1

    def test_deletion(self, matcher):
        assert matcher.levenshtein_distance("cats", "cat") == 1


class TestLevenshteinRatio:
    def test_identical(self, matcher):
        assert matcher.levenshtein_ratio("hello", "hello") == 1.0

    def test_empty_both(self, matcher):
        assert matcher.levenshtein_ratio("", "") == 1.0

    def test_empty_one(self, matcher):
        assert matcher.levenshtein_ratio("", "abc") == 0.0

    def test_completely_different(self, matcher):
        # "abc" vs "xyz": distance 3, max len 3 -> ratio 0
        assert matcher.levenshtein_ratio("abc", "xyz") == 0.0

    def test_partial(self, matcher):
        r = matcher.levenshtein_ratio("cat", "bat")
        assert 0.6 < r < 0.7  # 1 - 1/3


# ---------------------------------------------------------------------------
# Jaro / Jaro-Winkler
# ---------------------------------------------------------------------------
class TestJaro:
    def test_identical(self, matcher):
        assert matcher.jaro_similarity("hello", "hello") == 1.0

    def test_martha_marhta(self, matcher):
        # Well-known Jaro example
        r = matcher.jaro_similarity("MARTHA", "MARHTA")
        assert abs(r - 0.9444) < 0.001

    def test_dixon_dicksonx(self, matcher):
        r = matcher.jaro_similarity("DIXON", "DICKSONX")
        assert abs(r - 0.7666) < 0.01

    def test_empty(self, matcher):
        assert matcher.jaro_similarity("", "abc") == 0.0
        assert matcher.jaro_similarity("abc", "") == 0.0

    def test_both_empty(self, matcher):
        assert matcher.jaro_similarity("", "") == 1.0

    def test_no_match(self, matcher):
        assert matcher.jaro_similarity("abc", "xyz") == 0.0


class TestJaroWinkler:
    def test_identical(self, matcher):
        assert matcher.jaro_winkler("hello", "hello") == 1.0

    def test_martha_marhta(self, matcher):
        # Jaro=0.9444, prefix=3 (MAR), so JW = 0.9444 + 3*0.1*(1-0.9444) ≈ 0.9611
        r = matcher.jaro_winkler("MARTHA", "MARHTA")
        assert abs(r - 0.9611) < 0.001

    def test_higher_than_jaro(self, matcher):
        a, b = "DWAYNE", "DUANE"
        assert matcher.jaro_winkler(a, b) >= matcher.jaro_similarity(a, b)

    def test_empty(self, matcher):
        assert matcher.jaro_winkler("", "abc") == 0.0

    def test_prefix_scale(self, matcher):
        r_low = matcher.jaro_winkler("MARTHA", "MARHTA", prefix_scale=0.0)
        r_high = matcher.jaro_winkler("MARTHA", "MARHTA", prefix_scale=0.25)
        # With 0 scale we get pure Jaro
        assert r_high > r_low


# ---------------------------------------------------------------------------
# N-gram
# ---------------------------------------------------------------------------
class TestNgram:
    def test_identical(self, matcher):
        assert matcher.ngram_similarity("hello", "hello") == 1.0

    def test_empty(self, matcher):
        assert matcher.ngram_similarity("", "abc") == 0.0
        assert matcher.ngram_similarity("abc", "") == 0.0

    def test_both_empty(self, matcher):
        assert matcher.ngram_similarity("", "") == 1.0

    def test_no_overlap(self, matcher):
        assert matcher.ngram_similarity("abc", "xyz", n=2) == 0.0

    def test_partial_overlap(self, matcher):
        # "night" bigrams: ni, ig, gh, ht; "nacht" bigrams: na, ac, ch, ht -> 1 shared
        r = matcher.ngram_similarity("night", "nacht", n=2)
        assert abs(r - 0.25) < 0.001  # 2*1/(4+4)

    def test_short_strings_fallback(self, matcher):
        # Strings shorter than n fall back to char set
        r = matcher.ngram_similarity("a", "a", n=2)
        assert r == 1.0

    def test_invalid_n(self, matcher):
        with pytest.raises(ValueError):
            matcher.ngram_similarity("abc", "abc", n=0)


# ---------------------------------------------------------------------------
# Ratio (difflib)
# ---------------------------------------------------------------------------
class TestRatio:
    def test_identical(self, matcher):
        assert matcher.ratio("hello", "hello") == 1.0

    def test_empty_both(self, matcher):
        assert matcher.ratio("", "") == 1.0

    def test_empty_one(self, matcher):
        assert matcher.ratio("", "abc") == 0.0

    def test_partial(self, matcher):
        r = matcher.ratio("apple", "appla")
        assert 0.7 < r < 0.9

    def test_completely_different(self, matcher):
        r = matcher.ratio("abc", "xyz")
        assert r < 0.1


# ---------------------------------------------------------------------------
# Partial ratio
# ---------------------------------------------------------------------------
class TestPartialRatio:
    def test_identical(self, matcher):
        assert matcher.partial_ratio("hello", "hello") == 1.0

    def test_substring_match(self, matcher):
        # "world" appears exactly inside "hello world"
        assert matcher.partial_ratio("world", "hello world") == 1.0

    def test_substring_prefix(self, matcher):
        assert matcher.partial_ratio("hello", "hello world") == 1.0

    def test_no_match(self, matcher):
        r = matcher.partial_ratio("xyz", "abcdef")
        assert r < 0.5

    def test_empty(self, matcher):
        assert matcher.partial_ratio("", "abc") == 0.0

    def test_better_than_ratio_for_substring(self, matcher):
        r_partial = matcher.partial_ratio("fox", "the quick brown fox jumps")
        r_normal = matcher.ratio("fox", "the quick brown fox jumps")
        assert r_partial > r_normal


# ---------------------------------------------------------------------------
# Token sort
# ---------------------------------------------------------------------------
class TestTokenSort:
    def test_identical(self, matcher):
        assert matcher.token_sort_ratio("hello world", "hello world") == 1.0

    def test_reordered(self, matcher):
        assert matcher.token_sort_ratio("fuzzy bear", "bear fuzzy") == 1.0

    def test_reordered_three_tokens(self, matcher):
        assert matcher.token_sort_ratio("a b c", "c b a") == 1.0

    def test_different_tokens(self, matcher):
        r = matcher.token_sort_ratio("apple pie", "banana split")
        assert r < 0.5

    def test_empty(self, matcher):
        assert matcher.token_sort_ratio("", "hello") == 0.0


# ---------------------------------------------------------------------------
# Token set
# ---------------------------------------------------------------------------
class TestTokenSet:
    def test_identical(self, matcher):
        assert matcher.token_set_ratio("hello world", "hello world") == 1.0

    def test_subset(self, matcher):
        # "hello" is a subset of "hello world" -> intersection matches well
        r = matcher.token_set_ratio("hello", "hello world")
        assert r == 1.0  # intersection == sorted_inter, intersection vs sorted_ab=hello world -> ratio of intersection to itself = 1

    def test_overlap(self, matcher):
        r = matcher.token_set_ratio("apple banana", "apple cherry")
        # max of three ratios > 0
        assert 0.0 < r < 1.0

    def test_no_overlap(self, matcher):
        r = matcher.token_set_ratio("apple pie", "banana split")
        assert r < 0.5

    def test_empty(self, matcher):
        assert matcher.token_set_ratio("", "hello") == 0.0

    def test_duplicates(self, matcher):
        # Set semantics: duplicates don't matter
        assert matcher.token_set_ratio("a a a b", "a b") == 1.0


# ---------------------------------------------------------------------------
# match()
# ---------------------------------------------------------------------------
class TestMatch:
    def test_returns_fuzzy_match(self, matcher):
        m = matcher.match("hello", "hello")
        assert isinstance(m, FuzzyMatch)

    def test_identical_score_one(self, matcher):
        m = matcher.match("hello", "hello")
        assert m.score == 1.0

    def test_meets_threshold(self, matcher):
        m = matcher.match("hello", "hello")
        assert m.meets_threshold is True

    def test_fails_threshold(self, matcher):
        m = matcher.match("abc", "xyz")
        assert m.meets_threshold is False

    def test_query_preserved(self, matcher):
        m = matcher.match("Hello", "HELLO")
        assert m.query == "Hello"
        assert m.target == "HELLO"

    def test_algo_override(self, matcher):
        m = matcher.match("hello", "hello", algo=FuzzyAlgo.JARO)
        assert m.algo is FuzzyAlgo.JARO

    def test_uses_config_algo_by_default(self, matcher):
        m = matcher.match("hello", "hello")
        assert m.algo is FuzzyAlgo.RATIO

    def test_all_algos_identical(self, matcher):
        for algo in FuzzyAlgo:
            m = matcher.match("hello world", "hello world", algo=algo)
            assert m.score == 1.0, f"algo={algo} did not return 1.0 for identical"


# ---------------------------------------------------------------------------
# match_many()
# ---------------------------------------------------------------------------
class TestMatchMany:
    def test_filters_by_threshold(self, matcher):
        results = matcher.match_many(
            "hello",
            ["hello", "world", "hxllo", "totally different stuff"],
        )
        assert all(r.meets_threshold for r in results)

    def test_sorted_descending(self, matcher):
        results = matcher.match_many(
            "hello",
            ["hello", "hxllo", "heeeeello"],
            threshold=0.0,
        )
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_empty_targets(self, matcher):
        assert matcher.match_many("hello", []) == []

    def test_explicit_threshold(self, matcher):
        results = matcher.match_many(
            "hello", ["hello", "world"], threshold=0.99,
        )
        assert len(results) == 1
        assert results[0].target == "hello"

    def test_algo_override(self, matcher):
        results = matcher.match_many(
            "hello", ["hello"], algo=FuzzyAlgo.JARO_WINKLER, threshold=0.0,
        )
        assert results[0].algo is FuzzyAlgo.JARO_WINKLER


# ---------------------------------------------------------------------------
# find_best()
# ---------------------------------------------------------------------------
class TestFindBest:
    def test_returns_best(self, matcher):
        result = matcher.find_best(
            "apple", ["banana", "appl", "applx", "apple"],
        )
        assert result.target == "apple"

    def test_empty_targets(self, matcher):
        assert matcher.find_best("hello", []) is None

    def test_single_target(self, matcher):
        result = matcher.find_best("hello", ["world"])
        assert result.target == "world"

    def test_picks_higher_score(self, matcher):
        result = matcher.find_best("cat", ["car", "cat"])
        assert result.target == "cat"


# ---------------------------------------------------------------------------
# find_top_k()
# ---------------------------------------------------------------------------
class TestFindTopK:
    def test_returns_k_results(self, matcher):
        results = matcher.find_top_k(
            "apple", ["appl", "applx", "apple", "banana", "grape"], k=3,
        )
        assert len(results) == 3

    def test_sorted_descending(self, matcher):
        results = matcher.find_top_k(
            "apple", ["appl", "applx", "apple", "banana"], k=4,
        )
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_empty_targets(self, matcher):
        assert matcher.find_top_k("hello", [], k=5) == []

    def test_k_larger_than_targets(self, matcher):
        results = matcher.find_top_k("hello", ["a", "b"], k=10)
        assert len(results) == 2

    def test_k_zero(self, matcher):
        assert matcher.find_top_k("hello", ["a", "b"], k=0) == []

    def test_default_k(self, matcher):
        results = matcher.find_top_k(
            "hello", [f"item{i}" for i in range(10)],
        )
        assert len(results) == 5


# ---------------------------------------------------------------------------
# Threshold semantics
# ---------------------------------------------------------------------------
class TestThreshold:
    def test_threshold_default(self):
        m = FuzzyMatcher()
        assert m.config.threshold == 0.7

    def test_threshold_meets_when_equal(self):
        m = FuzzyMatcher(FuzzyConfig(threshold=1.0))
        match = m.match("hello", "hello")
        assert match.meets_threshold is True

    def test_threshold_strict(self):
        m = FuzzyMatcher(FuzzyConfig(threshold=0.99))
        match = m.match("hello", "hxllo")
        assert match.meets_threshold is False

    def test_match_many_uses_config_threshold(self):
        m = FuzzyMatcher(FuzzyConfig(threshold=0.99))
        results = m.match_many("hello", ["hello", "hxllo"])
        assert len(results) == 1


# ---------------------------------------------------------------------------
# Case sensitivity
# ---------------------------------------------------------------------------
class TestCaseSensitivity:
    def test_case_insensitive_default(self, matcher):
        m = matcher.match("Hello", "hello")
        assert m.score == 1.0

    def test_case_sensitive(self, case_sensitive_matcher):
        m = case_sensitive_matcher.match("Hello", "hello")
        assert m.score < 1.0

    def test_case_sensitive_identical(self, case_sensitive_matcher):
        m = case_sensitive_matcher.match("Hello", "Hello")
        assert m.score == 1.0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_both_empty_match(self, matcher):
        m = matcher.match("", "")
        assert m.score == 1.0

    def test_query_empty(self, matcher):
        m = matcher.match("", "hello")
        assert m.score == 0.0

    def test_target_empty(self, matcher):
        m = matcher.match("hello", "")
        assert m.score == 0.0

    def test_very_long_string(self, matcher):
        a = "a" * 500
        m = matcher.match(a, a)
        assert m.score == 1.0

    def test_long_strings_levenshtein(self, matcher):
        a = "a" * 200
        b = "a" * 199 + "b"
        # Distance 1, ratio = 1 - 1/200 = 0.995
        r = matcher.levenshtein_ratio(a, b)
        assert abs(r - 0.995) < 0.001

    def test_unicode(self, matcher):
        m = matcher.match("привет", "привет")
        assert m.score == 1.0

    def test_unicode_partial(self, matcher):
        r = matcher.levenshtein_ratio("привет", "привт")
        assert 0.7 < r < 1.0

    def test_score_clamped(self, matcher):
        m = matcher.match("abc", "abc")
        assert 0.0 <= m.score <= 1.0

    def test_default_matcher_no_config(self):
        m = FuzzyMatcher()
        assert m.config.algo is FuzzyAlgo.RATIO

    def test_invalid_algo_in_compute(self, matcher):
        # Direct call with bogus value
        class FakeAlgo:
            pass
        with pytest.raises(ValueError):
            matcher._compute("a", "b", FakeAlgo())

    def test_whitespace_only(self, matcher):
        # Treated as a non-empty string
        m = matcher.match("   ", "   ")
        assert m.score == 1.0
