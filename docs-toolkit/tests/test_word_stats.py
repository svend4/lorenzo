"""Tests for docstoolkit.word_stats — target: >= 45 tests."""
from __future__ import annotations

import math

import pytest

from docstoolkit.word_stats import WordFrequency, TextStats, WordStatsAnalyzer


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

SAMPLE = (
    "The quick brown fox jumps over the lazy dog. "
    "The dog barked loudly. "
    "A fox ran away."
)

PARA_TEXT = "First paragraph here.\n\nSecond paragraph here.\n\nThird one."

CYRILLIC = "Это тест. Тест проверяет слова. Слова важны."


# ===========================================================================
# TestWordFrequency — dataclass fields
# ===========================================================================

class TestWordFrequency:
    def test_word_field(self):
        wf = WordFrequency(word="hello", count=3, frequency=0.3)
        assert wf.word == "hello"

    def test_count_field(self):
        wf = WordFrequency(word="hello", count=3, frequency=0.3)
        assert wf.count == 3

    def test_frequency_field(self):
        wf = WordFrequency(word="hello", count=3, frequency=0.3)
        assert wf.frequency == pytest.approx(0.3)

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(WordFrequency)

    def test_frequency_range(self):
        wf = WordFrequency(word="x", count=1, frequency=1.0)
        assert 0.0 <= wf.frequency <= 1.0


# ===========================================================================
# TestTextStatsFields — all fields present
# ===========================================================================

class TestTextStatsFields:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()
        self.stats = self.analyzer.analyze(SAMPLE)

    def test_word_count_present(self):
        assert hasattr(self.stats, "word_count")

    def test_unique_word_count_present(self):
        assert hasattr(self.stats, "unique_word_count")

    def test_char_count_present(self):
        assert hasattr(self.stats, "char_count")

    def test_sentence_count_present(self):
        assert hasattr(self.stats, "sentence_count")

    def test_paragraph_count_present(self):
        assert hasattr(self.stats, "paragraph_count")

    def test_avg_word_length_present(self):
        assert hasattr(self.stats, "avg_word_length")

    def test_avg_sentence_length_present(self):
        assert hasattr(self.stats, "avg_sentence_length")

    def test_type_token_ratio_present(self):
        assert hasattr(self.stats, "type_token_ratio")

    def test_lexical_density_present(self):
        assert hasattr(self.stats, "lexical_density")

    def test_most_common_present(self):
        assert hasattr(self.stats, "most_common")

    def test_hapax_count_present(self):
        assert hasattr(self.stats, "hapax_count")

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(TextStats)


# ===========================================================================
# TestAnalyzeWordCount
# ===========================================================================

class TestAnalyzeWordCount:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_basic_word_count(self):
        stats = self.analyzer.analyze("hello world foo")
        assert stats.word_count == 3

    def test_repeated_words_counted(self):
        stats = self.analyzer.analyze("the the the")
        assert stats.word_count == 3

    def test_numbers_not_counted(self):
        # digits alone don't match \b[a-zа-яё]+\b
        stats = self.analyzer.analyze("42 items 7")
        assert stats.word_count == 1  # only "items"

    def test_single_word(self):
        stats = self.analyzer.analyze("hello")
        assert stats.word_count == 1

    def test_cyrillic_counted(self):
        stats = self.analyzer.analyze("привет мир")
        assert stats.word_count == 2

    def test_mixed_latin_cyrillic(self):
        stats = self.analyzer.analyze("hello мир")
        assert stats.word_count == 2


# ===========================================================================
# TestAnalyzeUniqueWords
# ===========================================================================

class TestAnalyzeUniqueWords:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_all_unique(self):
        stats = self.analyzer.analyze("alpha beta gamma")
        assert stats.unique_word_count == 3

    def test_duplicates_reduce_unique(self):
        stats = self.analyzer.analyze("foo foo bar")
        assert stats.unique_word_count == 2

    def test_case_insensitive_uniqueness(self):
        stats = self.analyzer.analyze("Hello hello HELLO")
        assert stats.unique_word_count == 1

    def test_unique_count_le_word_count(self):
        stats = self.analyzer.analyze(SAMPLE)
        assert stats.unique_word_count <= stats.word_count


# ===========================================================================
# TestAnalyzeCharCount
# ===========================================================================

class TestAnalyzeCharCount:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_char_count_exact(self):
        text = "hello world"
        stats = self.analyzer.analyze(text)
        assert stats.char_count == len(text)

    def test_char_count_includes_spaces(self):
        text = "a b c"
        stats = self.analyzer.analyze(text)
        assert stats.char_count == 5

    def test_char_count_empty(self):
        stats = self.analyzer.analyze("")
        assert stats.char_count == 0

    def test_char_count_unicode(self):
        text = "привет мир"
        stats = self.analyzer.analyze(text)
        assert stats.char_count == len(text)


# ===========================================================================
# TestAnalyzeSentenceCount
# ===========================================================================

class TestAnalyzeSentenceCount:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_single_sentence_with_period(self):
        stats = self.analyzer.analyze("Hello world.")
        assert stats.sentence_count == 1

    def test_two_sentences(self):
        stats = self.analyzer.analyze("Hello world. How are you?")
        assert stats.sentence_count == 2

    def test_exclamation_marks(self):
        stats = self.analyzer.analyze("Hello! World!")
        assert stats.sentence_count == 2

    def test_no_terminal_punct(self):
        stats = self.analyzer.analyze("Hello world")
        assert stats.sentence_count == 1

    def test_empty_text_zero_sentences(self):
        stats = self.analyzer.analyze("")
        assert stats.sentence_count == 0

    def test_three_sentences(self):
        stats = self.analyzer.analyze("One. Two. Three.")
        assert stats.sentence_count == 3


# ===========================================================================
# TestAnalyzeParagraphCount
# ===========================================================================

class TestAnalyzeParagraphCount:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_single_paragraph(self):
        stats = self.analyzer.analyze("Hello world.")
        assert stats.paragraph_count == 1

    def test_two_paragraphs(self):
        stats = self.analyzer.analyze("Para one.\n\nPara two.")
        assert stats.paragraph_count == 2

    def test_three_paragraphs(self):
        stats = self.analyzer.analyze(PARA_TEXT)
        assert stats.paragraph_count == 3

    def test_empty_text_zero_paragraphs(self):
        stats = self.analyzer.analyze("")
        assert stats.paragraph_count == 0

    def test_multiple_blank_lines_still_one_break(self):
        stats = self.analyzer.analyze("A.\n\n\n\nB.")
        assert stats.paragraph_count == 2


# ===========================================================================
# TestAnalyzeAvgWordLength
# ===========================================================================

class TestAnalyzeAvgWordLength:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_equal_length_words(self):
        # "cat dog rat" — all 3 chars
        stats = self.analyzer.analyze("cat dog rat")
        assert stats.avg_word_length == pytest.approx(3.0)

    def test_mixed_lengths(self):
        # "a" (1) + "bb" (2) = total 3 chars / 2 words = 1.5
        stats = self.analyzer.analyze("a bb")
        assert stats.avg_word_length == pytest.approx(1.5)

    def test_avg_word_length_positive(self):
        stats = self.analyzer.analyze(SAMPLE)
        assert stats.avg_word_length > 0

    def test_empty_text_zero(self):
        stats = self.analyzer.analyze("")
        assert stats.avg_word_length == pytest.approx(0.0)


# ===========================================================================
# TestAnalyzeTypeTokenRatio
# ===========================================================================

class TestAnalyzeTypeTokenRatio:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_all_unique_ratio_one(self):
        stats = self.analyzer.analyze("alpha beta gamma delta")
        assert stats.type_token_ratio == pytest.approx(1.0)

    def test_all_same_ratio_fraction(self):
        stats = self.analyzer.analyze("the the the the")
        assert stats.type_token_ratio == pytest.approx(0.25)

    def test_ratio_between_zero_and_one(self):
        stats = self.analyzer.analyze(SAMPLE)
        assert 0.0 < stats.type_token_ratio <= 1.0

    def test_empty_text_zero(self):
        stats = self.analyzer.analyze("")
        assert stats.type_token_ratio == pytest.approx(0.0)


# ===========================================================================
# TestAnalyzeLexicalDensity
# ===========================================================================

class TestAnalyzeLexicalDensity:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_only_stop_words_zero_density(self):
        # All tokens are stop words
        stats = self.analyzer.analyze("the the the")
        assert stats.lexical_density == pytest.approx(0.0)

    def test_no_stop_words_full_density(self):
        stats = self.analyzer.analyze("python code analysis")
        assert stats.lexical_density == pytest.approx(1.0)

    def test_mixed_density(self):
        # "the" is stop, "cat" is content → 1/2 = 0.5
        stats = self.analyzer.analyze("the cat")
        assert stats.lexical_density == pytest.approx(0.5)

    def test_density_between_zero_and_one(self):
        stats = self.analyzer.analyze(SAMPLE)
        assert 0.0 <= stats.lexical_density <= 1.0

    def test_empty_text_zero(self):
        stats = self.analyzer.analyze("")
        assert stats.lexical_density == pytest.approx(0.0)

    def test_custom_stop_words(self):
        analyzer = WordStatsAnalyzer(stop_words={"cat"})
        stats = analyzer.analyze("cat dog")
        # "cat" is stop, "dog" is content → 0.5
        assert stats.lexical_density == pytest.approx(0.5)


# ===========================================================================
# TestAnalyzeMostCommon — top_n respected, ordering
# ===========================================================================

class TestAnalyzeMostCommon:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_most_common_length_default(self):
        stats = self.analyzer.analyze(SAMPLE)
        assert len(stats.most_common) <= 10

    def test_most_common_top_n_respected(self):
        stats = self.analyzer.analyze(SAMPLE, top_n=3)
        assert len(stats.most_common) <= 3

    def test_most_common_sorted_desc(self):
        stats = self.analyzer.analyze("foo foo foo bar bar baz")
        counts = [wf.count for wf in stats.most_common]
        assert counts == sorted(counts, reverse=True)

    def test_most_common_is_word_frequency(self):
        stats = self.analyzer.analyze(SAMPLE)
        for wf in stats.most_common:
            assert isinstance(wf, WordFrequency)

    def test_most_common_frequency_sums_correctly(self):
        text = "a a b"
        stats = self.analyzer.analyze(text)
        wf_a = next(w for w in stats.most_common if w.word == "a")
        assert wf_a.frequency == pytest.approx(2 / 3)

    def test_most_common_top_one(self):
        stats = self.analyzer.analyze("foo foo bar baz", top_n=1)
        assert len(stats.most_common) == 1
        assert stats.most_common[0].word == "foo"


# ===========================================================================
# TestAnalyzeHapax
# ===========================================================================

class TestAnalyzeHapax:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_all_hapax(self):
        stats = self.analyzer.analyze("alpha beta gamma")
        assert stats.hapax_count == 3

    def test_no_hapax(self):
        stats = self.analyzer.analyze("foo foo bar bar")
        assert stats.hapax_count == 0

    def test_some_hapax(self):
        stats = self.analyzer.analyze("foo foo bar baz")
        # "bar" and "baz" appear once each
        assert stats.hapax_count == 2

    def test_hapax_non_negative(self):
        stats = self.analyzer.analyze(SAMPLE)
        assert stats.hapax_count >= 0

    def test_hapax_le_unique(self):
        stats = self.analyzer.analyze(SAMPLE)
        assert stats.hapax_count <= stats.unique_word_count


# ===========================================================================
# TestWordFrequencies — sorted, top_n limiting
# ===========================================================================

class TestWordFrequencies:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_sorted_by_count_desc(self):
        freqs = self.analyzer.word_frequencies("foo foo bar baz")
        counts = [wf.count for wf in freqs]
        assert counts == sorted(counts, reverse=True)

    def test_top_n_limits_result(self):
        freqs = self.analyzer.word_frequencies(SAMPLE, top_n=5)
        assert len(freqs) <= 5

    def test_top_n_none_returns_all(self):
        text = "alpha beta gamma"
        freqs = self.analyzer.word_frequencies(text, top_n=None)
        assert len(freqs) == 3

    def test_frequency_sums_to_one(self):
        freqs = self.analyzer.word_frequencies("foo bar baz")
        total = sum(wf.frequency for wf in freqs)
        assert total == pytest.approx(1.0)

    def test_empty_text_returns_empty(self):
        freqs = self.analyzer.word_frequencies("")
        assert freqs == []

    def test_returns_word_frequency_instances(self):
        freqs = self.analyzer.word_frequencies("hello world")
        for wf in freqs:
            assert isinstance(wf, WordFrequency)


# ===========================================================================
# TestCompare — shared_words, unique sets, vocab_overlap
# ===========================================================================

class TestCompare:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_shared_words_identical_texts(self):
        result = self.analyzer.compare("foo bar", "foo bar")
        assert "foo" in result["shared_words"]
        assert "bar" in result["shared_words"]

    def test_unique_to_a(self):
        result = self.analyzer.compare("foo bar", "bar baz")
        assert "foo" in result["unique_to_a"]
        assert "baz" not in result["unique_to_a"]

    def test_unique_to_b(self):
        result = self.analyzer.compare("foo bar", "bar baz")
        assert "baz" in result["unique_to_b"]
        assert "foo" not in result["unique_to_b"]

    def test_vocab_overlap_identical(self):
        result = self.analyzer.compare("foo bar baz", "foo bar baz")
        assert result["vocab_overlap"] == pytest.approx(1.0)

    def test_vocab_overlap_disjoint(self):
        result = self.analyzer.compare("foo bar", "baz qux")
        assert result["vocab_overlap"] == pytest.approx(0.0)

    def test_vocab_overlap_partial(self):
        # A={foo,bar}, B={bar,baz} → shared={bar}, union={foo,bar,baz} → 1/3
        result = self.analyzer.compare("foo bar", "bar baz")
        assert result["vocab_overlap"] == pytest.approx(1 / 3)

    def test_result_keys(self):
        result = self.analyzer.compare("foo", "bar")
        assert set(result.keys()) == {"shared_words", "unique_to_a", "unique_to_b", "vocab_overlap"}

    def test_shared_words_is_set(self):
        result = self.analyzer.compare("foo", "foo")
        assert isinstance(result["shared_words"], set)

    def test_unique_to_a_is_set(self):
        result = self.analyzer.compare("foo bar", "foo")
        assert isinstance(result["unique_to_a"], set)

    def test_both_empty(self):
        result = self.analyzer.compare("", "")
        assert result["vocab_overlap"] == pytest.approx(0.0)
        assert result["shared_words"] == set()


# ===========================================================================
# TestReadingTime
# ===========================================================================

class TestReadingTime:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_reading_time_200_wpm(self):
        # 200 words at 200 wpm = 1.0 minute
        text = " ".join(["word"] * 200)
        rt = self.analyzer.reading_time(text, wpm=200)
        assert rt == pytest.approx(1.0)

    def test_reading_time_100_wpm(self):
        text = " ".join(["word"] * 100)
        rt = self.analyzer.reading_time(text, wpm=100)
        assert rt == pytest.approx(1.0)

    def test_reading_time_default_wpm(self):
        text = " ".join(["word"] * 400)
        rt = self.analyzer.reading_time(text)  # default 200 wpm
        assert rt == pytest.approx(2.0)

    def test_reading_time_empty_text(self):
        rt = self.analyzer.reading_time("")
        assert rt == pytest.approx(0.0)

    def test_reading_time_positive(self):
        rt = self.analyzer.reading_time(SAMPLE)
        assert rt > 0.0

    def test_reading_time_proportional(self):
        text_short = " ".join(["word"] * 50)
        text_long = " ".join(["word"] * 100)
        rt_short = self.analyzer.reading_time(text_short)
        rt_long = self.analyzer.reading_time(text_long)
        assert rt_long == pytest.approx(rt_short * 2)


# ===========================================================================
# TestEdgeCases — empty text, single word, only stop words
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.analyzer = WordStatsAnalyzer()

    def test_empty_text_word_count_zero(self):
        stats = self.analyzer.analyze("")
        assert stats.word_count == 0

    def test_empty_text_unique_zero(self):
        stats = self.analyzer.analyze("")
        assert stats.unique_word_count == 0

    def test_empty_text_most_common_empty(self):
        stats = self.analyzer.analyze("")
        assert stats.most_common == []

    def test_empty_text_hapax_zero(self):
        stats = self.analyzer.analyze("")
        assert stats.hapax_count == 0

    def test_single_word(self):
        stats = self.analyzer.analyze("hello")
        assert stats.word_count == 1
        assert stats.unique_word_count == 1
        assert stats.hapax_count == 1
        assert stats.type_token_ratio == pytest.approx(1.0)

    def test_only_stop_words_lexical_density_zero(self):
        stats = self.analyzer.analyze("the and or")
        assert stats.lexical_density == pytest.approx(0.0)

    def test_only_numbers_word_count_zero(self):
        stats = self.analyzer.analyze("123 456 789")
        assert stats.word_count == 0

    def test_min_word_length_filters_short(self):
        analyzer = WordStatsAnalyzer(min_word_length=4)
        stats = analyzer.analyze("hi hello world")
        # "hi" (2) filtered out, "hello" (5) and "world" (5) kept
        assert stats.word_count == 2

    def test_custom_stop_words_empty_set(self):
        analyzer = WordStatsAnalyzer(stop_words=set())
        stats = analyzer.analyze("the cat")
        # No stop words → full lexical density
        assert stats.lexical_density == pytest.approx(1.0)

    def test_whitespace_only_text(self):
        stats = self.analyzer.analyze("   \n\n   \t  ")
        assert stats.word_count == 0
        assert stats.paragraph_count == 0
        assert stats.sentence_count == 0

    def test_avg_sentence_length_no_sentences(self):
        stats = self.analyzer.analyze("")
        assert stats.avg_sentence_length == pytest.approx(0.0)
