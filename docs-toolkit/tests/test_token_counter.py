"""Comprehensive tests for the token_counter module — 40+ tests."""
from __future__ import annotations

import dataclasses

import pytest

from docstoolkit.token_counter import TokenBudget, TokenCount, TokenCounter, TokenStrategy


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def counter() -> TokenCounter:
    return TokenCounter()


# ===========================================================================
# 1. TokenStrategy
# ===========================================================================


class TestTokenStrategy:
    def test_word_member_exists(self):
        assert TokenStrategy.WORD

    def test_char_member_exists(self):
        assert TokenStrategy.CHAR

    def test_whitespace_member_exists(self):
        assert TokenStrategy.WHITESPACE

    def test_sentence_member_exists(self):
        assert TokenStrategy.SENTENCE

    def test_subword_member_exists(self):
        assert TokenStrategy.SUBWORD

    def test_all_five_members(self):
        names = {m.name for m in TokenStrategy}
        assert names == {"WORD", "CHAR", "WHITESPACE", "SENTENCE", "SUBWORD"}

    def test_values_are_strings(self):
        for member in TokenStrategy:
            assert isinstance(member.value, str)

    def test_lookup_by_value(self):
        assert TokenStrategy("word") is TokenStrategy.WORD
        assert TokenStrategy("char") is TokenStrategy.CHAR


# ===========================================================================
# 2. TokenCount dataclass
# ===========================================================================


class TestTokenCountDataclass:
    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(TokenCount)

    def test_fields_present(self):
        tc = TokenCount(
            text="hello world",
            strategy=TokenStrategy.WORD,
            count=2,
            tokens=["hello", "world"],
        )
        assert tc.text == "hello world"
        assert tc.strategy is TokenStrategy.WORD
        assert tc.count == 2
        assert tc.tokens == ["hello", "world"]

    def test_equality(self):
        a = TokenCount(text="hi", strategy=TokenStrategy.WORD, count=1, tokens=["hi"])
        b = TokenCount(text="hi", strategy=TokenStrategy.WORD, count=1, tokens=["hi"])
        assert a == b

    def test_inequality(self):
        a = TokenCount(text="hi", strategy=TokenStrategy.WORD, count=1, tokens=["hi"])
        b = TokenCount(text="bye", strategy=TokenStrategy.WORD, count=1, tokens=["bye"])
        assert a != b

    def test_tokens_list_type(self):
        tc = TokenCount(text="a", strategy=TokenStrategy.CHAR, count=1, tokens=["a"])
        assert isinstance(tc.tokens, list)


# ===========================================================================
# 3. TokenCounter — WORD strategy
# ===========================================================================


class TestTokenCounterWord:
    def test_basic(self, counter):
        tc = counter.count("hello world")
        assert tc.count == 2
        assert tc.tokens == ["hello", "world"]

    def test_default_strategy_is_word(self, counter):
        tc = counter.count("one two three")
        assert tc.strategy is TokenStrategy.WORD

    def test_empty_string(self, counter):
        tc = counter.count("")
        assert tc.count == 0
        assert tc.tokens == []

    def test_punctuation_stripped(self, counter):
        tc = counter.count("Hello, world!")
        assert tc.count == 2
        assert "Hello" in tc.tokens
        assert "world" in tc.tokens

    def test_numbers_counted(self, counter):
        tc = counter.count("price is 42 dollars")
        assert tc.count == 4
        assert "42" in tc.tokens

    def test_hyphenated_word(self, counter):
        # re.findall(r'\b\w+\b') splits on '-'
        tc = counter.count("well-known")
        assert tc.count == 2
        assert "well" in tc.tokens
        assert "known" in tc.tokens

    def test_multiple_spaces(self, counter):
        tc = counter.count("a   b   c")
        assert tc.count == 3

    def test_text_stored(self, counter):
        text = "store me"
        tc = counter.count(text, TokenStrategy.WORD)
        assert tc.text == text

    def test_strategy_stored(self, counter):
        tc = counter.count("x", TokenStrategy.WORD)
        assert tc.strategy is TokenStrategy.WORD


# ===========================================================================
# 4. TokenCounter — CHAR strategy
# ===========================================================================


class TestTokenCounterChar:
    def test_basic(self, counter):
        tc = counter.count("abc", TokenStrategy.CHAR)
        assert tc.count == 3
        assert tc.tokens == ["a", "b", "c"]

    def test_whitespace_excluded(self, counter):
        tc = counter.count("a b c", TokenStrategy.CHAR)
        assert tc.count == 3

    def test_empty(self, counter):
        tc = counter.count("", TokenStrategy.CHAR)
        assert tc.count == 0

    def test_only_spaces(self, counter):
        tc = counter.count("   ", TokenStrategy.CHAR)
        assert tc.count == 0

    def test_mixed_unicode(self, counter):
        tc = counter.count("hi мир", TokenStrategy.CHAR)
        # h, i, м, и, р — 5 non-space chars
        assert tc.count == 5


# ===========================================================================
# 5. TokenCounter — WHITESPACE strategy
# ===========================================================================


class TestTokenCounterWhitespace:
    def test_basic(self, counter):
        tc = counter.count("one two three", TokenStrategy.WHITESPACE)
        assert tc.count == 3
        assert tc.tokens == ["one", "two", "three"]

    def test_empty(self, counter):
        tc = counter.count("", TokenStrategy.WHITESPACE)
        assert tc.count == 0

    def test_leading_trailing_spaces(self, counter):
        tc = counter.count("  hello world  ", TokenStrategy.WHITESPACE)
        assert tc.count == 2

    def test_tabs_and_newlines(self, counter):
        tc = counter.count("a\tb\nc", TokenStrategy.WHITESPACE)
        assert tc.count == 3

    def test_keeps_punctuation_attached(self, counter):
        tc = counter.count("Hello, world!", TokenStrategy.WHITESPACE)
        assert "Hello," in tc.tokens
        assert "world!" in tc.tokens


# ===========================================================================
# 6. TokenCounter — SENTENCE strategy
# ===========================================================================


class TestTokenCounterSentence:
    def test_basic(self, counter):
        tc = counter.count("Hello. World.", TokenStrategy.SENTENCE)
        assert tc.count == 2
        assert "Hello" in tc.tokens
        assert "World" in tc.tokens

    def test_question_mark(self, counter):
        tc = counter.count("How are you? Fine.", TokenStrategy.SENTENCE)
        assert tc.count == 2

    def test_exclamation(self, counter):
        tc = counter.count("Stop! Look! Listen!", TokenStrategy.SENTENCE)
        assert tc.count == 3

    def test_newline_separator(self, counter):
        tc = counter.count("Line one\nLine two\nLine three", TokenStrategy.SENTENCE)
        assert tc.count == 3

    def test_empty(self, counter):
        tc = counter.count("", TokenStrategy.SENTENCE)
        assert tc.count == 0

    def test_no_separator_single_sentence(self, counter):
        tc = counter.count("just one sentence here", TokenStrategy.SENTENCE)
        assert tc.count == 1

    def test_strips_whitespace_from_parts(self, counter):
        tc = counter.count("  Hello.  World.  ", TokenStrategy.SENTENCE)
        for t in tc.tokens:
            assert t == t.strip()


# ===========================================================================
# 7. TokenCounter — SUBWORD strategy
# ===========================================================================


class TestTokenCounterSubword:
    def test_short_word_single_chunk(self, counter):
        tc = counter.count("abc", TokenStrategy.SUBWORD)
        assert tc.tokens == ["abc"]

    def test_four_char_word_single_chunk(self, counter):
        tc = counter.count("abcd", TokenStrategy.SUBWORD)
        assert tc.tokens == ["abcd"]

    def test_five_char_word_two_chunks(self, counter):
        tc = counter.count("abcde", TokenStrategy.SUBWORD)
        assert tc.tokens == ["abcd", "e"]

    def test_eight_char_word_two_chunks(self, counter):
        tc = counter.count("abcdefgh", TokenStrategy.SUBWORD)
        assert tc.tokens == ["abcd", "efgh"]

    def test_nine_char_word_three_chunks(self, counter):
        tc = counter.count("abcdefghi", TokenStrategy.SUBWORD)
        assert tc.tokens == ["abcd", "efgh", "i"]

    def test_multiple_words(self, counter):
        tc = counter.count("hello world", TokenStrategy.SUBWORD)
        # hello -> hell, o  (5 chars); world -> worl, d (5 chars) => 4 chunks
        assert tc.tokens == ["hell", "o", "worl", "d"]

    def test_empty(self, counter):
        tc = counter.count("", TokenStrategy.SUBWORD)
        assert tc.count == 0

    def test_count_matches_tokens_length(self, counter):
        tc = counter.count("tokenization is fun", TokenStrategy.SUBWORD)
        assert tc.count == len(tc.tokens)


# ===========================================================================
# 8. count_batch
# ===========================================================================


class TestCountBatch:
    def test_returns_list(self, counter):
        results = counter.count_batch(["a", "b", "c"], TokenStrategy.WORD)
        assert isinstance(results, list)

    def test_length_matches_input(self, counter):
        texts = ["one", "two three", "four five six"]
        results = counter.count_batch(texts, TokenStrategy.WORD)
        assert len(results) == 3

    def test_each_element_is_token_count(self, counter):
        results = counter.count_batch(["hello"], TokenStrategy.WORD)
        assert isinstance(results[0], TokenCount)

    def test_empty_batch(self, counter):
        results = counter.count_batch([], TokenStrategy.WORD)
        assert results == []

    def test_strategy_applied_uniformly(self, counter):
        texts = ["a b c", "1 2 3"]
        results = counter.count_batch(texts, TokenStrategy.WHITESPACE)
        for r in results:
            assert r.strategy is TokenStrategy.WHITESPACE

    def test_counts_correct(self, counter):
        results = counter.count_batch(["one", "one two", "one two three"], TokenStrategy.WORD)
        assert [r.count for r in results] == [1, 2, 3]

    def test_texts_preserved(self, counter):
        texts = ["alpha", "beta"]
        results = counter.count_batch(texts, TokenStrategy.WORD)
        assert [r.text for r in results] == texts


# ===========================================================================
# 9. estimate_cost
# ===========================================================================


class TestEstimateCost:
    def test_default_rate(self, counter):
        # 1000 words → rate 0.002 → cost 0.002
        text = " ".join(["word"] * 1000)
        cost = counter.estimate_cost(text)
        assert abs(cost - 0.002) < 1e-9

    def test_custom_rate(self, counter):
        text = " ".join(["word"] * 500)
        cost = counter.estimate_cost(text, rate_per_1k=0.004)
        assert abs(cost - 0.002) < 1e-9

    def test_empty_text_zero_cost(self, counter):
        assert counter.estimate_cost("") == 0.0

    def test_returns_float(self, counter):
        result = counter.estimate_cost("hello world")
        assert isinstance(result, float)

    def test_proportional_to_word_count(self, counter):
        c1 = counter.estimate_cost("hello world")
        c2 = counter.estimate_cost("hello world foo bar")
        assert c2 == pytest.approx(c1 * 2)

    def test_uses_word_strategy(self, counter):
        # punctuation adjacent to words: "hello,world" → 2 WORD tokens
        text = "hello,world"
        cost = counter.estimate_cost(text)
        expected = (2 / 1000.0) * 0.002
        assert abs(cost - expected) < 1e-12


# ===========================================================================
# 10. truncate
# ===========================================================================


class TestTruncate:
    def test_word_truncate_basic(self, counter):
        result = counter.truncate("one two three four five", max_tokens=3)
        assert result == "one two three"

    def test_word_truncate_to_zero(self, counter):
        result = counter.truncate("hello world", max_tokens=0)
        assert result == ""

    def test_word_truncate_already_short(self, counter):
        result = counter.truncate("hi", max_tokens=10)
        assert result == "hi"

    def test_word_truncate_exact_length(self, counter):
        result = counter.truncate("a b c", max_tokens=3)
        assert result == "a b c"

    def test_char_truncate(self, counter):
        result = counter.truncate("abcdef", max_tokens=3, strategy=TokenStrategy.CHAR)
        assert result == "abc"

    def test_whitespace_truncate(self, counter):
        result = counter.truncate("hello world foo", max_tokens=2, strategy=TokenStrategy.WHITESPACE)
        assert result == "hello world"

    def test_sentence_truncate(self, counter):
        result = counter.truncate(
            "First sentence. Second sentence. Third sentence.",
            max_tokens=2,
            strategy=TokenStrategy.SENTENCE,
        )
        # result contains the first two sentence tokens joined by space
        assert "First sentence" in result
        assert "Second sentence" in result
        assert "Third" not in result

    def test_subword_truncate(self, counter):
        result = counter.truncate("hello", max_tokens=1, strategy=TokenStrategy.SUBWORD)
        assert result == "hell"

    def test_negative_max_tokens_returns_empty(self, counter):
        result = counter.truncate("hello world", max_tokens=-5)
        assert result == ""


# ===========================================================================
# 11. fits_in
# ===========================================================================


class TestFitsIn:
    def test_fits(self, counter):
        assert counter.fits_in("one two", max_tokens=5) is True

    def test_does_not_fit(self, counter):
        assert counter.fits_in("one two three four five", max_tokens=3) is False

    def test_exact_boundary_fits(self, counter):
        assert counter.fits_in("one two three", max_tokens=3) is True

    def test_empty_string_fits_any(self, counter):
        assert counter.fits_in("", max_tokens=0) is True

    def test_returns_bool(self, counter):
        result = counter.fits_in("hello", max_tokens=1)
        assert type(result) is bool

    def test_strategy_respected(self, counter):
        # "ab cd ef" → 6 CHAR tokens (non-space)
        assert counter.fits_in("ab cd ef", max_tokens=5, strategy=TokenStrategy.CHAR) is False
        assert counter.fits_in("ab cd ef", max_tokens=6, strategy=TokenStrategy.CHAR) is True


# ===========================================================================
# 12. TokenBudget
# ===========================================================================


class TestTokenBudget:
    def test_initial_used_zero(self):
        budget = TokenBudget(limit=100)
        assert budget.used == 0

    def test_initial_remaining_equals_limit(self):
        budget = TokenBudget(limit=50)
        assert budget.remaining == 50

    def test_not_exhausted_initially(self):
        budget = TokenBudget(limit=10)
        assert budget.is_exhausted is False

    def test_add_returns_true_within_budget(self):
        budget = TokenBudget(limit=100)
        assert budget.add("hello world") is True

    def test_add_updates_used(self):
        budget = TokenBudget(limit=100)
        budget.add("hello world")  # 2 WORD tokens
        assert budget.used == 2

    def test_remaining_decreases_after_add(self):
        budget = TokenBudget(limit=10)
        budget.add("one two")  # 2 tokens
        assert budget.remaining == 8

    def test_add_returns_false_when_exceeds(self):
        budget = TokenBudget(limit=3)
        budget.add("one two three")  # uses all 3
        result = budget.add("one more")  # 2 more would exceed
        assert result is False

    def test_budget_not_modified_on_false(self):
        budget = TokenBudget(limit=3)
        budget.add("one two three")
        used_before = budget.used
        budget.add("extra token here")
        assert budget.used == used_before

    def test_is_exhausted_when_full(self):
        budget = TokenBudget(limit=2)
        budget.add("one two")
        assert budget.is_exhausted is True

    def test_reset_zeroes_used(self):
        budget = TokenBudget(limit=10)
        budget.add("one two three")
        budget.reset()
        assert budget.used == 0

    def test_reset_restores_remaining(self):
        budget = TokenBudget(limit=10)
        budget.add("one two three")
        budget.reset()
        assert budget.remaining == 10

    def test_reset_clears_exhausted(self):
        budget = TokenBudget(limit=2)
        budget.add("one two")
        assert budget.is_exhausted
        budget.reset()
        assert not budget.is_exhausted

    def test_add_after_reset(self):
        budget = TokenBudget(limit=5)
        budget.add("one two three four five")
        budget.reset()
        assert budget.add("hello world") is True

    def test_remaining_never_negative(self):
        # Manually inflate _used beyond limit (edge case guard)
        budget = TokenBudget(limit=2)
        budget._used = 5
        assert budget.remaining == 0

    def test_custom_strategy_char(self):
        budget = TokenBudget(limit=5, strategy=TokenStrategy.CHAR)
        # "abc" → 3 CHAR tokens
        assert budget.add("abc") is True
        assert budget.used == 3
        # "de" → 2 CHAR tokens; 3+2=5 <= 5
        assert budget.add("de") is True
        # "f" → 1 CHAR token; 5+1=6 > 5
        assert budget.add("f") is False

    def test_add_empty_string_always_succeeds(self):
        budget = TokenBudget(limit=0)
        # empty string has 0 tokens → 0 + 0 == 0 <= 0
        assert budget.add("") is True

    def test_multiple_sequential_adds(self):
        budget = TokenBudget(limit=10)
        budget.add("one")       # 1
        budget.add("two three")  # 2
        budget.add("four")      # 1
        assert budget.used == 4
        assert budget.remaining == 6

    def test_is_exhausted_property_type(self):
        budget = TokenBudget(limit=5)
        assert type(budget.is_exhausted) is bool
