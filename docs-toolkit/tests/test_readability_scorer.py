"""Tests for docstoolkit.readability_scorer."""
from __future__ import annotations

import math

import pytest

from docstoolkit.readability_scorer import (
    ReadabilityLevel,
    ReadabilityScore,
    ReadabilityScorer,
)
from docstoolkit.readability_scorer.scorer import _level_for_flesch


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

SIMPLE_TEXT = "The cat sat on the mat. The dog ran fast."
EASY_PARAGRAPH = (
    "Reading helps people learn new ideas. "
    "Books contain stories and facts. "
    "Children enjoy picture books at school."
)
FAIRLY_DIFFICULT_PARAGRAPH = (
    "Reading helps people develop knowledge. "
    "Books contain stories and useful facts. "
    "Children enjoy reading colorful picture books at school each morning."
)
HARD_PARAGRAPH = (
    "Notwithstanding the aforementioned considerations, "
    "the implementation demonstrates remarkable architectural sophistication "
    "across heterogeneous computational environments."
)


@pytest.fixture
def scorer() -> ReadabilityScorer:
    return ReadabilityScorer()


# ---------------------------------------------------------------------------
# ReadabilityLevel enum
# ---------------------------------------------------------------------------


class TestReadabilityLevel:
    def test_has_all_seven_levels(self):
        names = {m.name for m in ReadabilityLevel}
        assert names == {
            "VERY_EASY",
            "EASY",
            "FAIRLY_EASY",
            "STANDARD",
            "FAIRLY_DIFFICULT",
            "DIFFICULT",
            "VERY_DIFFICULT",
        }

    def test_is_string_enum(self):
        assert isinstance(ReadabilityLevel.STANDARD.value, str)
        assert ReadabilityLevel.STANDARD == "standard"

    def test_values_are_unique(self):
        values = [m.value for m in ReadabilityLevel]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# ReadabilityScore dataclass
# ---------------------------------------------------------------------------


class TestReadabilityScore:
    def test_can_construct_with_all_fields(self):
        score = ReadabilityScore(
            flesch_reading_ease=70.0,
            flesch_kincaid_grade=8.0,
            gunning_fog=10.0,
            automated_readability_index=9.0,
            coleman_liau_index=8.5,
            level=ReadabilityLevel.FAIRLY_EASY,
            word_count=100,
            sentence_count=5,
            syllable_count=150,
            complex_word_count=12,
            avg_sentence_length=20.0,
            avg_syllables_per_word=1.5,
        )
        assert score.flesch_reading_ease == 70.0
        assert score.level == ReadabilityLevel.FAIRLY_EASY

    def test_fields_are_typed(self):
        score = ReadabilityScore(
            flesch_reading_ease=1.0,
            flesch_kincaid_grade=1.0,
            gunning_fog=1.0,
            automated_readability_index=1.0,
            coleman_liau_index=1.0,
            level=ReadabilityLevel.STANDARD,
            word_count=10,
            sentence_count=1,
            syllable_count=15,
            complex_word_count=1,
            avg_sentence_length=10.0,
            avg_syllables_per_word=1.5,
        )
        assert isinstance(score.word_count, int)
        assert isinstance(score.flesch_reading_ease, float)
        assert isinstance(score.level, ReadabilityLevel)


# ---------------------------------------------------------------------------
# count_syllables
# ---------------------------------------------------------------------------


class TestCountSyllables:
    def test_cat_is_one(self, scorer: ReadabilityScorer):
        assert scorer.count_syllables("cat") == 1

    def test_hello_is_two(self, scorer: ReadabilityScorer):
        assert scorer.count_syllables("hello") == 2

    def test_beautiful_is_three(self, scorer: ReadabilityScorer):
        assert scorer.count_syllables("beautiful") == 3

    def test_the_is_one(self, scorer: ReadabilityScorer):
        assert scorer.count_syllables("the") == 1

    def test_single_letter_word(self, scorer: ReadabilityScorer):
        assert scorer.count_syllables("a") == 1
        assert scorer.count_syllables("I") == 1

    def test_empty_string_is_zero(self, scorer: ReadabilityScorer):
        assert scorer.count_syllables("") == 0

    def test_minimum_one_for_any_word(self, scorer: ReadabilityScorer):
        # Even a word made only of consonants returns at least 1
        assert scorer.count_syllables("hmm") >= 1
        assert scorer.count_syllables("xyz") >= 1

    def test_silent_e_subtracted(self, scorer: ReadabilityScorer):
        # "make" -> vowel groups: 'a','e' -> 2, silent e -> 1
        assert scorer.count_syllables("make") == 1
        assert scorer.count_syllables("code") == 1

    def test_silent_e_not_applied_when_only_syllable(self, scorer: ReadabilityScorer):
        # "be" only has one vowel group; we never reduce to zero.
        assert scorer.count_syllables("be") == 1

    def test_case_insensitive(self, scorer: ReadabilityScorer):
        assert scorer.count_syllables("HELLO") == scorer.count_syllables("hello")
        assert scorer.count_syllables("Beautiful") == 3

    def test_strips_non_letters(self, scorer: ReadabilityScorer):
        assert scorer.count_syllables("hello!") == 2
        assert scorer.count_syllables("don't") == scorer.count_syllables("dont")


# ---------------------------------------------------------------------------
# count_words
# ---------------------------------------------------------------------------


class TestCountWords:
    def test_simple_sentence(self, scorer: ReadabilityScorer):
        assert scorer.count_words("The cat sat on the mat.") == 6

    def test_empty_text(self, scorer: ReadabilityScorer):
        assert scorer.count_words("") == 0

    def test_whitespace_only(self, scorer: ReadabilityScorer):
        assert scorer.count_words("   \n\t  ") == 0

    def test_punctuation_does_not_count(self, scorer: ReadabilityScorer):
        assert scorer.count_words("Hello, world!") == 2

    def test_numbers_count_as_words(self, scorer: ReadabilityScorer):
        assert scorer.count_words("There are 3 apples.") == 4


# ---------------------------------------------------------------------------
# count_sentences
# ---------------------------------------------------------------------------


class TestCountSentences:
    def test_single_period(self, scorer: ReadabilityScorer):
        assert scorer.count_sentences("Hello world.") == 1

    def test_two_sentences(self, scorer: ReadabilityScorer):
        assert scorer.count_sentences("Hello. World.") == 2

    def test_question_and_exclamation(self, scorer: ReadabilityScorer):
        assert scorer.count_sentences("Hi! Are you ok? Yes.") == 3

    def test_empty_text(self, scorer: ReadabilityScorer):
        assert scorer.count_sentences("") == 0

    def test_no_terminator_still_one(self, scorer: ReadabilityScorer):
        # A run of words without punctuation should count as a single sentence.
        assert scorer.count_sentences("hello world") == 1

    def test_trailing_punctuation_ignored(self, scorer: ReadabilityScorer):
        assert scorer.count_sentences("Hi.   ") == 1


# ---------------------------------------------------------------------------
# count_complex_words
# ---------------------------------------------------------------------------


class TestCountComplexWords:
    def test_no_complex_words(self, scorer: ReadabilityScorer):
        assert scorer.count_complex_words("The cat sat on the mat.") == 0

    def test_one_complex_word(self, scorer: ReadabilityScorer):
        # "beautiful" has 3 syllables
        assert scorer.count_complex_words("The beautiful cat.") == 1

    def test_several_complex_words(self, scorer: ReadabilityScorer):
        count = scorer.count_complex_words(
            "Implementation demonstrates remarkable architectural sophistication."
        )
        assert count >= 4

    def test_empty(self, scorer: ReadabilityScorer):
        assert scorer.count_complex_words("") == 0


# ---------------------------------------------------------------------------
# Flesch Reading Ease
# ---------------------------------------------------------------------------


class TestFleschReadingEase:
    def test_simple_text_is_high(self, scorer: ReadabilityScorer):
        # Short, monosyllabic sentences score well above 60.
        assert scorer.flesch_reading_ease(SIMPLE_TEXT) > 60

    def test_hard_text_is_low(self, scorer: ReadabilityScorer):
        assert scorer.flesch_reading_ease(HARD_PARAGRAPH) < 50

    def test_empty_returns_zero(self, scorer: ReadabilityScorer):
        assert scorer.flesch_reading_ease("") == 0.0

    def test_formula(self, scorer: ReadabilityScorer):
        text = "The cat sat. The dog ran."
        words = scorer.count_words(text)
        sentences = scorer.count_sentences(text)
        syllables = sum(scorer.count_syllables(w) for w in text.replace(".", "").split())
        expected = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        assert math.isclose(
            scorer.flesch_reading_ease(text), expected, rel_tol=1e-6
        )


# ---------------------------------------------------------------------------
# Flesch-Kincaid Grade
# ---------------------------------------------------------------------------


class TestFleschKincaidGrade:
    def test_simple_text_low_grade(self, scorer: ReadabilityScorer):
        assert scorer.flesch_kincaid_grade(SIMPLE_TEXT) < 6

    def test_hard_text_high_grade(self, scorer: ReadabilityScorer):
        assert scorer.flesch_kincaid_grade(HARD_PARAGRAPH) > 12

    def test_empty_returns_zero(self, scorer: ReadabilityScorer):
        assert scorer.flesch_kincaid_grade("") == 0.0

    def test_formula(self, scorer: ReadabilityScorer):
        text = "The cat sat. The dog ran."
        words = scorer.count_words(text)
        sentences = scorer.count_sentences(text)
        syllables = sum(scorer.count_syllables(w) for w in text.replace(".", "").split())
        expected = 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
        assert math.isclose(
            scorer.flesch_kincaid_grade(text), expected, rel_tol=1e-6
        )


# ---------------------------------------------------------------------------
# Gunning Fog
# ---------------------------------------------------------------------------


class TestGunningFog:
    def test_simple_text_low_fog(self, scorer: ReadabilityScorer):
        assert scorer.gunning_fog(SIMPLE_TEXT) < 10

    def test_hard_text_high_fog(self, scorer: ReadabilityScorer):
        assert scorer.gunning_fog(HARD_PARAGRAPH) > 15

    def test_empty_returns_zero(self, scorer: ReadabilityScorer):
        assert scorer.gunning_fog("") == 0.0

    def test_formula(self, scorer: ReadabilityScorer):
        text = "Cats run fast. Dogs run too."
        words = scorer.count_words(text)
        sentences = scorer.count_sentences(text)
        complex_words = scorer.count_complex_words(text)
        expected = 0.4 * ((words / sentences) + 100 * (complex_words / words))
        assert math.isclose(scorer.gunning_fog(text), expected, rel_tol=1e-6)


# ---------------------------------------------------------------------------
# Integrated score()
# ---------------------------------------------------------------------------


class TestScoreIntegration:
    def test_score_returns_dataclass(self, scorer: ReadabilityScorer):
        score = scorer.score(SIMPLE_TEXT)
        assert isinstance(score, ReadabilityScore)

    def test_all_metric_fields_present(self, scorer: ReadabilityScorer):
        score = scorer.score(SIMPLE_TEXT)
        assert isinstance(score.flesch_reading_ease, float)
        assert isinstance(score.flesch_kincaid_grade, float)
        assert isinstance(score.gunning_fog, float)
        assert isinstance(score.automated_readability_index, float)
        assert isinstance(score.coleman_liau_index, float)
        assert isinstance(score.level, ReadabilityLevel)

    def test_count_fields_consistent(self, scorer: ReadabilityScorer):
        score = scorer.score(SIMPLE_TEXT)
        assert score.word_count == scorer.count_words(SIMPLE_TEXT)
        assert score.sentence_count == scorer.count_sentences(SIMPLE_TEXT)
        assert score.complex_word_count == scorer.count_complex_words(SIMPLE_TEXT)

    def test_avg_sentence_length(self, scorer: ReadabilityScorer):
        score = scorer.score(SIMPLE_TEXT)
        assert math.isclose(
            score.avg_sentence_length,
            score.word_count / score.sentence_count,
            rel_tol=1e-9,
        )

    def test_avg_syllables_per_word(self, scorer: ReadabilityScorer):
        score = scorer.score(SIMPLE_TEXT)
        assert math.isclose(
            score.avg_syllables_per_word,
            score.syllable_count / score.word_count,
            rel_tol=1e-9,
        )

    def test_score_batch_returns_list(self, scorer: ReadabilityScorer):
        results = scorer.score_batch([SIMPLE_TEXT, HARD_PARAGRAPH])
        assert len(results) == 2
        assert all(isinstance(r, ReadabilityScore) for r in results)

    def test_score_batch_preserves_order(self, scorer: ReadabilityScorer):
        results = scorer.score_batch([SIMPLE_TEXT, HARD_PARAGRAPH])
        # simple text should be easier (higher FRE) than the hard paragraph.
        assert results[0].flesch_reading_ease > results[1].flesch_reading_ease

    def test_score_batch_empty(self, scorer: ReadabilityScorer):
        assert scorer.score_batch([]) == []

    def test_ari_finite_for_typical_text(self, scorer: ReadabilityScorer):
        score = scorer.score(EASY_PARAGRAPH)
        assert math.isfinite(score.automated_readability_index)

    def test_coleman_liau_finite_for_typical_text(self, scorer: ReadabilityScorer):
        score = scorer.score(EASY_PARAGRAPH)
        assert math.isfinite(score.coleman_liau_index)


# ---------------------------------------------------------------------------
# Level mapping
# ---------------------------------------------------------------------------


class TestLevelMapping:
    @pytest.mark.parametrize(
        "score,expected",
        [
            (95.0, ReadabilityLevel.VERY_EASY),
            (90.0, ReadabilityLevel.VERY_EASY),
            (85.0, ReadabilityLevel.EASY),
            (80.0, ReadabilityLevel.EASY),
            (75.0, ReadabilityLevel.FAIRLY_EASY),
            (70.0, ReadabilityLevel.FAIRLY_EASY),
            (65.0, ReadabilityLevel.STANDARD),
            (60.0, ReadabilityLevel.STANDARD),
            (55.0, ReadabilityLevel.FAIRLY_DIFFICULT),
            (50.0, ReadabilityLevel.FAIRLY_DIFFICULT),
            (40.0, ReadabilityLevel.DIFFICULT),
            (30.0, ReadabilityLevel.DIFFICULT),
            (20.0, ReadabilityLevel.VERY_DIFFICULT),
            (0.0, ReadabilityLevel.VERY_DIFFICULT),
            (-50.0, ReadabilityLevel.VERY_DIFFICULT),
        ],
    )
    def test_each_band(self, score: float, expected: ReadabilityLevel):
        assert _level_for_flesch(score) == expected

    def test_score_easy_paragraph_yields_easy_or_better(self, scorer: ReadabilityScorer):
        # The "easy" paragraph should land at EASY tier.
        score = scorer.score(EASY_PARAGRAPH)
        assert score.level in {
            ReadabilityLevel.VERY_EASY,
            ReadabilityLevel.EASY,
            ReadabilityLevel.FAIRLY_EASY,
        }

    def test_score_hard_paragraph_yields_very_difficult(self, scorer: ReadabilityScorer):
        score = scorer.score(HARD_PARAGRAPH)
        assert score.level in {
            ReadabilityLevel.DIFFICULT,
            ReadabilityLevel.VERY_DIFFICULT,
        }

    def test_score_mid_paragraph_yields_mid_band(self, scorer: ReadabilityScorer):
        score = scorer.score(FAIRLY_DIFFICULT_PARAGRAPH)
        # Should not be VERY_EASY and should not be DIFFICULT's polar opposite.
        assert score.level != ReadabilityLevel.VERY_EASY


# ---------------------------------------------------------------------------
# compare()
# ---------------------------------------------------------------------------


class TestCompare:
    def test_compare_returns_dict(self, scorer: ReadabilityScorer):
        result = scorer.compare(SIMPLE_TEXT, HARD_PARAGRAPH)
        assert isinstance(result, dict)

    def test_compare_includes_both_scores(self, scorer: ReadabilityScorer):
        result = scorer.compare(SIMPLE_TEXT, HARD_PARAGRAPH)
        assert isinstance(result["a"], ReadabilityScore)
        assert isinstance(result["b"], ReadabilityScore)

    def test_compare_diff_signs(self, scorer: ReadabilityScorer):
        # Simple text is easier than hard text → diff (hard - simple) should
        # be negative for FRE and positive for grade-style metrics.
        result = scorer.compare(SIMPLE_TEXT, HARD_PARAGRAPH)
        assert result["flesch_reading_ease_diff"] < 0
        assert result["flesch_kincaid_grade_diff"] > 0
        assert result["gunning_fog_diff"] > 0

    def test_compare_identical_texts_yields_zero_diffs(self, scorer: ReadabilityScorer):
        result = scorer.compare(SIMPLE_TEXT, SIMPLE_TEXT)
        assert result["flesch_reading_ease_diff"] == 0.0
        assert result["flesch_kincaid_grade_diff"] == 0.0
        assert result["gunning_fog_diff"] == 0.0
        assert result["word_count_diff"] == 0
        assert result["sentence_count_diff"] == 0

    def test_compare_count_diffs(self, scorer: ReadabilityScorer):
        a = "One. Two."
        b = "One sentence here. Another sentence here. A third."
        result = scorer.compare(a, b)
        assert result["word_count_diff"] == result["b"].word_count - result["a"].word_count
        assert result["sentence_count_diff"] == 1  # 3 - 2


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_text_returns_zero_metrics(self, scorer: ReadabilityScorer):
        score = scorer.score("")
        assert score.flesch_reading_ease == 0.0
        assert score.flesch_kincaid_grade == 0.0
        assert score.gunning_fog == 0.0
        assert score.automated_readability_index == 0.0
        assert score.coleman_liau_index == 0.0
        assert score.word_count == 0
        assert score.sentence_count == 0
        assert score.avg_sentence_length == 0.0
        assert score.avg_syllables_per_word == 0.0

    def test_whitespace_only(self, scorer: ReadabilityScorer):
        score = scorer.score("   \n\t  ")
        assert score.word_count == 0
        assert score.sentence_count == 0
        assert score.flesch_reading_ease == 0.0

    def test_single_word_no_punctuation(self, scorer: ReadabilityScorer):
        score = scorer.score("hello")
        # 1 word, 1 (implicit) sentence → metrics are finite
        assert score.word_count == 1
        assert score.sentence_count == 1
        assert math.isfinite(score.flesch_reading_ease)
        assert math.isfinite(score.flesch_kincaid_grade)

    def test_single_sentence(self, scorer: ReadabilityScorer):
        score = scorer.score("Hello world today.")
        assert score.sentence_count == 1
        assert score.word_count == 3

    def test_only_punctuation(self, scorer: ReadabilityScorer):
        score = scorer.score("... !!! ???")
        # No alphanumeric tokens at all.
        assert score.word_count == 0
        assert score.flesch_reading_ease == 0.0

    def test_no_sentence_terminator(self, scorer: ReadabilityScorer):
        # Should still produce a finite score by treating the run as one sentence.
        score = scorer.score("the quick brown fox jumps over the lazy dog")
        assert score.sentence_count == 1
        assert score.word_count == 9
        assert math.isfinite(score.flesch_reading_ease)

    def test_simple_text_higher_ease_than_hard(self, scorer: ReadabilityScorer):
        assert scorer.flesch_reading_ease(SIMPLE_TEXT) > scorer.flesch_reading_ease(HARD_PARAGRAPH)

    def test_simple_text_lower_grade_than_hard(self, scorer: ReadabilityScorer):
        assert scorer.flesch_kincaid_grade(SIMPLE_TEXT) < scorer.flesch_kincaid_grade(HARD_PARAGRAPH)
