"""Tests for docstoolkit.string_matcher."""

from __future__ import annotations

import pytest

from docstoolkit.string_matcher import (
    MatchMode,
    MatchScore,
    MatcherConfig,
    StringMatcher,
)


# --------------------------------------------------------------------------- #
# Basic dataclasses / enums
# --------------------------------------------------------------------------- #
class TestMatchMode:
    def test_has_all_modes(self):
        names = {m.name for m in MatchMode}
        assert {
            "EXACT", "EXACT_CI", "SUBSTRING", "FUZZY", "GLOB",
            "REGEX", "SOUNDEX", "PREFIX", "SUFFIX",
        } <= names

    def test_values_are_strings(self):
        for m in MatchMode:
            assert isinstance(m.value, str)

    def test_enum_uniqueness(self):
        values = [m.value for m in MatchMode]
        assert len(values) == len(set(values))


class TestMatchScore:
    def test_construction(self):
        s = MatchScore(query="a", target="a", score=1.0, mode=MatchMode.EXACT, matched=True)
        assert s.query == "a"
        assert s.target == "a"
        assert s.score == 1.0
        assert s.mode is MatchMode.EXACT
        assert s.matched is True

    def test_score_can_be_zero(self):
        s = MatchScore(query="x", target="y", score=0.0, mode=MatchMode.EXACT, matched=False)
        assert s.score == 0.0
        assert s.matched is False


class TestMatcherConfig:
    def test_defaults(self):
        c = MatcherConfig()
        assert c.case_sensitive is True
        assert c.fuzzy_threshold == 0.6

    def test_override(self):
        c = MatcherConfig(case_sensitive=False, fuzzy_threshold=0.8)
        assert c.case_sensitive is False
        assert c.fuzzy_threshold == 0.8


# --------------------------------------------------------------------------- #
# Individual matchers
# --------------------------------------------------------------------------- #
class TestExact:
    def setup_method(self):
        self.m = StringMatcher()

    def test_exact_match(self):
        assert self.m.exact("hello", "hello") is True

    def test_exact_mismatch(self):
        assert self.m.exact("hello", "world") is False

    def test_case_sensitive_diff_case(self):
        assert self.m.exact("Hello", "hello") is False

    def test_case_insensitive(self):
        assert self.m.exact("Hello", "hello", case_sensitive=False) is True


class TestExactCi:
    def setup_method(self):
        self.m = StringMatcher()

    def test_ci_match(self):
        r = self.m.match("Hello", "HELLO", mode=MatchMode.EXACT_CI)
        assert r.matched is True
        assert r.score == 1.0

    def test_ci_mismatch(self):
        r = self.m.match("foo", "bar", mode=MatchMode.EXACT_CI)
        assert r.matched is False
        assert r.score == 0.0

    def test_ci_does_not_affect_exact_mode(self):
        r = self.m.match("Hello", "HELLO", mode=MatchMode.EXACT)
        assert r.matched is False


class TestSubstring:
    def setup_method(self):
        self.m = StringMatcher()

    def test_substring_present(self):
        assert self.m.substring("ell", "hello") is True

    def test_substring_absent(self):
        assert self.m.substring("xyz", "hello") is False

    def test_substring_case_sensitive(self):
        assert self.m.substring("ELL", "hello") is False

    def test_substring_case_insensitive(self):
        assert self.m.substring("ELL", "hello", case_sensitive=False) is True


class TestFuzzy:
    def setup_method(self):
        self.m = StringMatcher()

    def test_fuzzy_identical(self):
        assert self.m.fuzzy("hello", "hello") == 1.0

    def test_fuzzy_completely_different(self):
        score = self.m.fuzzy("abc", "xyz")
        assert 0.0 <= score <= 1.0
        assert score < 0.5

    def test_fuzzy_partial(self):
        score = self.m.fuzzy("kitten", "sitting")
        assert 0.0 < score < 1.0

    def test_fuzzy_in_range(self):
        for q, t in [("a", "b"), ("abc", "abd"), ("hello world", "hallo word")]:
            s = self.m.fuzzy(q, t)
            assert 0.0 <= s <= 1.0

    def test_fuzzy_both_empty(self):
        assert self.m.fuzzy("", "") == 1.0


class TestGlob:
    def setup_method(self):
        self.m = StringMatcher()

    def test_star_pattern(self):
        assert self.m.glob("*.txt", "file.txt") is True
        assert self.m.glob("*.txt", "file.md") is False

    def test_question_mark(self):
        assert self.m.glob("file?.txt", "file1.txt") is True
        assert self.m.glob("file?.txt", "file12.txt") is False

    def test_char_class(self):
        assert self.m.glob("file[abc].txt", "filea.txt") is True
        assert self.m.glob("file[abc].txt", "filed.txt") is False

    def test_glob_via_match(self):
        r = self.m.match("*.py", "matcher.py", mode=MatchMode.GLOB)
        assert r.matched is True
        assert r.score == 1.0


class TestRegex:
    def setup_method(self):
        self.m = StringMatcher()

    def test_regex_match(self):
        assert self.m.regex(r"\d+", "abc123") is True

    def test_regex_no_match(self):
        assert self.m.regex(r"\d+", "abcdef") is False

    def test_regex_invalid_pattern(self):
        # invalid regex must not blow up
        assert self.m.regex("[unclosed", "abc") is False

    def test_regex_via_match(self):
        r = self.m.match(r"^hello", "hello world", mode=MatchMode.REGEX)
        assert r.matched is True


class TestSoundex:
    def setup_method(self):
        self.m = StringMatcher()

    def test_robert(self):
        assert self.m.soundex("Robert") == "R163"

    def test_rupert(self):
        assert self.m.soundex("Rupert") == "R163"

    def test_smith(self):
        assert self.m.soundex("Smith") == "S530"

    def test_smyth_matches_smith(self):
        assert self.m.soundex("Smyth") == self.m.soundex("Smith")

    def test_empty_string(self):
        assert self.m.soundex("") == ""

    def test_padding_short_word(self):
        # Single-letter word: code is letter + "000".
        assert self.m.soundex("A") == "A000"

    def test_soundex_mode_via_match(self):
        r = self.m.match("Robert", "Rupert", mode=MatchMode.SOUNDEX)
        assert r.matched is True
        assert r.score == 1.0

    def test_soundex_mode_mismatch(self):
        r = self.m.match("Robert", "Smith", mode=MatchMode.SOUNDEX)
        assert r.matched is False
        assert r.score == 0.0


class TestPrefix:
    def setup_method(self):
        self.m = StringMatcher()

    def test_prefix_true(self):
        assert self.m.prefix("hel", "hello") is True

    def test_prefix_false(self):
        assert self.m.prefix("ell", "hello") is False

    def test_prefix_case_sensitive(self):
        assert self.m.prefix("Hel", "hello") is False

    def test_prefix_case_insensitive(self):
        assert self.m.prefix("HEL", "hello", case_sensitive=False) is True


class TestSuffix:
    def setup_method(self):
        self.m = StringMatcher()

    def test_suffix_true(self):
        assert self.m.suffix("llo", "hello") is True

    def test_suffix_false(self):
        assert self.m.suffix("hel", "hello") is False

    def test_suffix_case_sensitive(self):
        assert self.m.suffix("LLO", "hello") is False

    def test_suffix_case_insensitive(self):
        assert self.m.suffix("LLO", "hello", case_sensitive=False) is True


# --------------------------------------------------------------------------- #
# Dispatch and collection APIs
# --------------------------------------------------------------------------- #
class TestMatchDispatch:
    def setup_method(self):
        self.m = StringMatcher()

    def test_exact_dispatch(self):
        r = self.m.match("a", "a", mode=MatchMode.EXACT)
        assert r.mode is MatchMode.EXACT
        assert r.score == 1.0
        assert r.matched is True

    def test_substring_dispatch(self):
        r = self.m.match("ell", "hello", mode=MatchMode.SUBSTRING)
        assert r.matched is True

    def test_fuzzy_threshold_below(self):
        cfg = MatcherConfig(fuzzy_threshold=0.95)
        m = StringMatcher(cfg)
        r = m.match("hello", "hallo", mode=MatchMode.FUZZY)
        assert r.matched is False

    def test_fuzzy_threshold_above(self):
        cfg = MatcherConfig(fuzzy_threshold=0.1)
        m = StringMatcher(cfg)
        r = m.match("hello", "hallo", mode=MatchMode.FUZZY)
        assert r.matched is True

    def test_prefix_dispatch(self):
        r = self.m.match("he", "hello", mode=MatchMode.PREFIX)
        assert r.matched is True

    def test_suffix_dispatch(self):
        r = self.m.match("lo", "hello", mode=MatchMode.SUFFIX)
        assert r.matched is True

    def test_glob_dispatch(self):
        r = self.m.match("*.md", "doc.md", mode=MatchMode.GLOB)
        assert r.matched is True

    def test_regex_dispatch(self):
        r = self.m.match(r"[0-9]+", "abc42", mode=MatchMode.REGEX)
        assert r.matched is True

    def test_score_in_range(self):
        for mode in MatchMode:
            q, t = ("hello", "hello") if mode is not MatchMode.GLOB else ("hello", "hello")
            r = self.m.match(q, t, mode=mode)
            assert 0.0 <= r.score <= 1.0


class TestMatchAll:
    def setup_method(self):
        self.m = StringMatcher()

    def test_match_all_returns_one_per_target(self):
        targets = ["a", "b", "c"]
        out = self.m.match_all("a", targets, mode=MatchMode.EXACT)
        assert len(out) == 3
        assert all(isinstance(x, MatchScore) for x in out)

    def test_match_all_results(self):
        out = self.m.match_all("a", ["a", "b", "a"], mode=MatchMode.EXACT)
        assert [s.matched for s in out] == [True, False, True]

    def test_match_all_empty(self):
        out = self.m.match_all("a", [], mode=MatchMode.EXACT)
        assert out == []


class TestFindBest:
    def setup_method(self):
        self.m = StringMatcher()

    def test_find_best_returns_top(self):
        targets = ["hello", "help", "world"]
        best = self.m.find_best("hello", targets, mode=MatchMode.FUZZY)
        assert best is not None
        assert best.target == "hello"
        assert best.score == 1.0

    def test_find_best_with_empty(self):
        assert self.m.find_best("x", [], mode=MatchMode.FUZZY) is None

    def test_find_best_no_match(self):
        cfg = MatcherConfig(fuzzy_threshold=0.99)
        m = StringMatcher(cfg)
        result = m.find_best("hello", ["xxxxx", "yyyyy"], mode=MatchMode.FUZZY)
        assert result is None

    def test_find_best_exact_mode(self):
        best = self.m.find_best("foo", ["bar", "foo", "baz"], mode=MatchMode.EXACT)
        assert best is not None
        assert best.target == "foo"


class TestFindTopK:
    def setup_method(self):
        self.m = StringMatcher()

    def test_top_k_basic(self):
        targets = ["hello", "help", "world", "helmet", "halt"]
        top = self.m.find_top_k("hello", targets, k=3, mode=MatchMode.FUZZY)
        assert len(top) <= 3
        scores = [r.score for r in top]
        assert scores == sorted(scores, reverse=True)

    def test_top_k_zero(self):
        assert self.m.find_top_k("a", ["a", "b"], k=0, mode=MatchMode.EXACT) == []

    def test_top_k_empty_targets(self):
        assert self.m.find_top_k("a", [], k=5, mode=MatchMode.EXACT) == []

    def test_top_k_only_matched(self):
        cfg = MatcherConfig(fuzzy_threshold=0.99)
        m = StringMatcher(cfg)
        out = m.find_top_k("hello", ["xxx", "yyy"], k=5, mode=MatchMode.FUZZY)
        assert out == []

    def test_top_k_returns_at_most_k(self):
        targets = [f"hello{i}" for i in range(10)]
        top = self.m.find_top_k("hello", targets, k=4, mode=MatchMode.FUZZY)
        assert len(top) <= 4


# --------------------------------------------------------------------------- #
# Edge cases
# --------------------------------------------------------------------------- #
class TestEdgeCases:
    def setup_method(self):
        self.m = StringMatcher()

    def test_empty_query_exact(self):
        r = self.m.match("", "", mode=MatchMode.EXACT)
        assert r.score == 1.0
        assert r.matched is True

    def test_empty_query_substring(self):
        # Empty substring is always present.
        assert self.m.substring("", "hello") is True

    def test_empty_target_substring(self):
        assert self.m.substring("x", "") is False

    def test_special_chars_substring(self):
        assert self.m.substring("$@#", "a$@#b") is True

    def test_unicode_exact(self):
        assert self.m.exact("héllo", "héllo") is True

    def test_unicode_fuzzy(self):
        score = self.m.fuzzy("café", "cafe")
        assert 0.0 < score < 1.0

    def test_soundex_with_non_letters(self):
        # Non-alphabetic input should be sanitised; pure punctuation = "".
        assert self.m.soundex("123") == ""

    def test_regex_special_meta(self):
        assert self.m.regex(r"\.", "file.txt") is True

    def test_long_strings_fuzzy(self):
        a = "a" * 500
        b = "a" * 499 + "b"
        score = self.m.fuzzy(a, b)
        assert score > 0.9

    def test_default_config_is_isolated(self):
        a = StringMatcher()
        b = StringMatcher()
        a.config.fuzzy_threshold = 0.99
        assert b.config.fuzzy_threshold == 0.6


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
