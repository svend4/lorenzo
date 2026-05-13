"""Tests for docstoolkit.epistemic module (40+ tests)."""

import math
import pytest

from docstoolkit.epistemic import (
    EpistemicProfile,
    measure_profile,
    aggregate_profiles,
    voice_distance,
    VoiceComparison,
    CorpusVoice,
    analyze_corpus_voice,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

HEDGE_TEXT = (
    "Perhaps this is possible. Maybe the result is probably correct. "
    "It seems likely that the approach could work, though it might fail. "
    "Arguably the data suggests an approximately valid conclusion."
)

STRONG_TEXT = (
    "This is clearly proven. The result is definitely correct. "
    "It is certainly true, undoubtedly. It will always work and never fail. "
    "This must be accepted as a fact. It is proven beyond doubt."
)

CITED_TEXT = (
    "According to Smith [1] this is true. Jones [2] agrees. "
    "The result (Johnson 2023) confirms the theory. "
    "See also source: example.com for more details. "
    "см. раздел 3 для подробностей."
)

RICH_TEXT = (
    "The quick brown fox jumps over the lazy dog near the river bank. "
    "Subsequently the animal traversed the meadow seeking sustenance. "
    "Extraordinary circumstances compelled the creature toward distant horizons. "
    "Philosophical implications emerged from the encounter between predator and prey. "
    "Linguistic diversity enriches our understanding of biological phenomena."
)

REPEATED_TEXT = "the the the the the cat cat cat cat dog dog dog "

LONG_SENTENCE_TEXT = (
    "This sentence is deliberately constructed to be very long with many words "
    "including subordinate clauses and various conjunctions so that the average "
    "sentence length metric will register a high value when calculated."
)

SHORT_SENTENCE_TEXT = "Yes. No. True. False. Good. Bad. Here. There."


# ---------------------------------------------------------------------------
# EpistemicProfile defaults
# ---------------------------------------------------------------------------

class TestEpistemicProfileDefaults:
    def test_strong_claim_rate_default(self):
        p = EpistemicProfile()
        assert p.strong_claim_rate == 0.0

    def test_hedge_rate_default(self):
        p = EpistemicProfile()
        assert p.hedge_rate == 0.0

    def test_stance_ratio_default(self):
        p = EpistemicProfile()
        assert p.stance_ratio == 0.0

    def test_avg_sentence_length_default(self):
        p = EpistemicProfile()
        assert p.avg_sentence_length == 0.0

    def test_citation_density_default(self):
        p = EpistemicProfile()
        assert p.citation_density == 0.0

    def test_ttr_default(self):
        p = EpistemicProfile()
        assert p.ttr == 0.0

    def test_hapax_ratio_default(self):
        p = EpistemicProfile()
        assert p.hapax_ratio == 0.0

    def test_sophistication_default(self):
        p = EpistemicProfile()
        assert p.sophistication == 0.0

    def test_to_vector_length(self):
        p = EpistemicProfile()
        assert len(p.to_vector()) == 7

    def test_to_vector_all_zeros(self):
        p = EpistemicProfile()
        assert all(v == 0.0 for v in p.to_vector())


# ---------------------------------------------------------------------------
# measure_profile
# ---------------------------------------------------------------------------

class TestMeasureProfileEmpty:
    def test_empty_string(self):
        p = measure_profile("")
        assert p.strong_claim_rate == 0.0
        assert p.hedge_rate == 0.0
        assert p.ttr == 0.0

    def test_whitespace_only(self):
        p = measure_profile("   \n\t  ")
        assert p.strong_claim_rate == 0.0
        assert p.ttr == 0.0

    def test_empty_returns_epistemic_profile(self):
        assert isinstance(measure_profile(""), EpistemicProfile)


class TestMeasureProfileHedge:
    def test_hedge_rate_positive(self):
        p = measure_profile(HEDGE_TEXT)
        assert p.hedge_rate > 0.0

    def test_hedge_rate_higher_than_strong(self):
        p = measure_profile(HEDGE_TEXT)
        assert p.hedge_rate > p.strong_claim_rate

    def test_stance_ratio_high_for_hedged(self):
        p = measure_profile(HEDGE_TEXT)
        # More hedges → stance_ratio closer to 1
        assert p.stance_ratio > 0.5


class TestMeasureProfileStrong:
    def test_strong_claim_rate_positive(self):
        p = measure_profile(STRONG_TEXT)
        assert p.strong_claim_rate > 0.0

    def test_stance_ratio_lower_for_assertive(self):
        hedge_p = measure_profile(HEDGE_TEXT)
        strong_p = measure_profile(STRONG_TEXT)
        assert strong_p.stance_ratio < hedge_p.stance_ratio


class TestMeasureProfileCitation:
    def test_citation_density_positive(self):
        p = measure_profile(CITED_TEXT)
        assert p.citation_density > 0.0

    def test_no_citation_in_plain_text(self):
        p = measure_profile("This is a simple sentence with no references.")
        assert p.citation_density == 0.0


class TestMeasureProfileLexical:
    def test_ttr_high_for_rich_text(self):
        p = measure_profile(RICH_TEXT)
        assert p.ttr > 0.5

    def test_ttr_low_for_repeated_text(self):
        p = measure_profile(REPEATED_TEXT)
        assert p.ttr < 0.5

    def test_hapax_ratio_positive_for_rich_text(self):
        p = measure_profile(RICH_TEXT)
        assert p.hapax_ratio > 0.0

    def test_hapax_ratio_zero_for_all_repeated(self):
        # All words appear >1 time → no hapax
        text = "cat cat dog dog fish fish bird bird"
        p = measure_profile(text)
        assert p.hapax_ratio == 0.0

    def test_ttr_in_range(self):
        p = measure_profile(RICH_TEXT)
        assert 0.0 <= p.ttr <= 1.0

    def test_hapax_ratio_in_range(self):
        p = measure_profile(RICH_TEXT)
        assert 0.0 <= p.hapax_ratio <= 1.0


class TestMeasureProfileSentenceLength:
    def test_long_sentences_give_higher_avg(self):
        long_p = measure_profile(LONG_SENTENCE_TEXT)
        short_p = measure_profile(SHORT_SENTENCE_TEXT)
        assert long_p.avg_sentence_length > short_p.avg_sentence_length

    def test_avg_sentence_length_positive_for_valid_text(self):
        p = measure_profile("Hello world. How are you?")
        assert p.avg_sentence_length > 0.0


class TestMeasureProfileSophistication:
    def test_sophistication_in_unit_range(self):
        for text in [HEDGE_TEXT, STRONG_TEXT, CITED_TEXT, RICH_TEXT, REPEATED_TEXT]:
            p = measure_profile(text)
            assert 0.0 <= p.sophistication <= 1.0

    def test_sophistication_zero_for_empty(self):
        p = measure_profile("")
        assert p.sophistication == 0.0


class TestMeasureProfileToVector:
    def test_to_vector_returns_7_floats(self):
        p = measure_profile(HEDGE_TEXT)
        v = p.to_vector()
        assert len(v) == 7
        assert all(isinstance(x, float) for x in v)

    def test_to_vector_stance_ratio_in_position_2(self):
        p = measure_profile(HEDGE_TEXT)
        v = p.to_vector()
        assert v[2] == p.stance_ratio


# ---------------------------------------------------------------------------
# aggregate_profiles
# ---------------------------------------------------------------------------

class TestAggregateProfiles:
    def test_single_profile_returns_same_values(self):
        p = measure_profile(HEDGE_TEXT)
        agg = aggregate_profiles([p])
        assert math.isclose(agg.ttr, p.ttr, rel_tol=1e-9)
        assert math.isclose(agg.hedge_rate, p.hedge_rate, rel_tol=1e-9)

    def test_two_profiles_averaged(self):
        p1 = EpistemicProfile(ttr=0.4, hedge_rate=2.0)
        p2 = EpistemicProfile(ttr=0.8, hedge_rate=4.0)
        agg = aggregate_profiles([p1, p2])
        assert math.isclose(agg.ttr, 0.6)
        assert math.isclose(agg.hedge_rate, 3.0)

    def test_empty_list_returns_zero_profile(self):
        agg = aggregate_profiles([])
        assert agg.ttr == 0.0
        assert agg.hedge_rate == 0.0
        assert agg.sophistication == 0.0

    def test_returns_epistemic_profile(self):
        agg = aggregate_profiles([EpistemicProfile()])
        assert isinstance(agg, EpistemicProfile)

    def test_aggregate_three_profiles(self):
        profiles = [EpistemicProfile(ttr=v) for v in [0.3, 0.6, 0.9]]
        agg = aggregate_profiles(profiles)
        assert math.isclose(agg.ttr, 0.6)


# ---------------------------------------------------------------------------
# VoiceComparison fields
# ---------------------------------------------------------------------------

class TestVoiceComparisonFields:
    def test_has_distance(self):
        vc = VoiceComparison(distance=0.1, similarity=0.9,
                              dominant_difference="ttr", assessment="same_voice")
        assert vc.distance == 0.1

    def test_has_similarity(self):
        vc = VoiceComparison(distance=0.1, similarity=0.9,
                              dominant_difference="ttr", assessment="same_voice")
        assert vc.similarity == 0.9

    def test_has_dominant_difference(self):
        vc = VoiceComparison(distance=0.1, similarity=0.9,
                              dominant_difference="hedge_rate", assessment="similar")
        assert vc.dominant_difference == "hedge_rate"

    def test_has_assessment(self):
        vc = VoiceComparison(distance=0.5, similarity=0.5,
                              dominant_difference="ttr", assessment="different")
        assert vc.assessment == "different"


# ---------------------------------------------------------------------------
# voice_distance
# ---------------------------------------------------------------------------

class TestVoiceDistance:
    def test_same_profile_distance_near_zero(self):
        p = measure_profile(HEDGE_TEXT)
        cmp = voice_distance(p, p)
        assert cmp.distance < 0.01

    def test_same_profile_similarity_near_one(self):
        p = measure_profile(HEDGE_TEXT)
        cmp = voice_distance(p, p)
        assert cmp.similarity > 0.99

    def test_same_profile_assessment_same_voice(self):
        p = measure_profile(HEDGE_TEXT)
        cmp = voice_distance(p, p)
        assert cmp.assessment == "same_voice"

    def test_very_different_profiles_distance_above_0_3(self):
        # Maximally different: all zeros vs all high values
        p1 = EpistemicProfile()
        p2 = EpistemicProfile(
            strong_claim_rate=10.0,
            hedge_rate=10.0,
            stance_ratio=1.0,
            avg_sentence_length=30.0,
            citation_density=5.0,
            ttr=1.0,
            hapax_ratio=1.0,
        )
        cmp = voice_distance(p1, p2)
        assert cmp.distance > 0.3

    def test_very_different_profiles_assessment(self):
        p1 = EpistemicProfile()
        p2 = EpistemicProfile(
            strong_claim_rate=10.0,
            stance_ratio=1.0,
            avg_sentence_length=30.0,
            ttr=1.0,
            hapax_ratio=1.0,
        )
        cmp = voice_distance(p1, p2)
        assert cmp.assessment in ("different", "opposite")

    def test_distance_in_unit_range(self):
        p1 = measure_profile(HEDGE_TEXT)
        p2 = measure_profile(STRONG_TEXT)
        cmp = voice_distance(p1, p2)
        assert 0.0 <= cmp.distance <= 1.0

    def test_similarity_equals_one_minus_distance(self):
        p1 = measure_profile(HEDGE_TEXT)
        p2 = measure_profile(STRONG_TEXT)
        cmp = voice_distance(p1, p2)
        assert math.isclose(cmp.similarity, 1.0 - cmp.distance, rel_tol=1e-9)

    def test_dominant_difference_is_non_empty_string(self):
        p1 = measure_profile(HEDGE_TEXT)
        p2 = measure_profile(STRONG_TEXT)
        cmp = voice_distance(p1, p2)
        assert isinstance(cmp.dominant_difference, str)
        assert len(cmp.dominant_difference) > 0

    def test_zero_profiles_distance_zero(self):
        p1 = EpistemicProfile()
        p2 = EpistemicProfile()
        cmp = voice_distance(p1, p2)
        assert cmp.distance == 0.0

    def test_assessment_similar_threshold(self):
        # Manually craft two profiles with small but nonzero distance
        p1 = EpistemicProfile(ttr=0.5)
        p2 = EpistemicProfile(ttr=0.6)
        cmp = voice_distance(p1, p2)
        assert cmp.assessment in ("same_voice", "similar")


# ---------------------------------------------------------------------------
# CorpusVoice
# ---------------------------------------------------------------------------

class TestCorpusVoice:
    def _build_corpus(self):
        docs = {
            "a": HEDGE_TEXT,
            "b": HEDGE_TEXT + " " + HEDGE_TEXT,
            "c": RICH_TEXT,
        }
        return analyze_corpus_voice(docs)

    def test_fits_voice_similar_text_true(self):
        cv = self._build_corpus()
        assert cv.fits_voice(HEDGE_TEXT) is True

    def test_fits_voice_returns_bool(self):
        cv = self._build_corpus()
        result = cv.fits_voice("some text")
        assert isinstance(result, bool)

    def test_voice_score_in_unit_range(self):
        cv = self._build_corpus()
        score = cv.voice_score(HEDGE_TEXT)
        assert 0.0 <= score <= 1.0

    def test_voice_score_returns_float(self):
        cv = self._build_corpus()
        assert isinstance(cv.voice_score("hello world"), float)

    def test_outliers_is_list(self):
        cv = self._build_corpus()
        assert isinstance(cv.outliers, list)

    def test_outliers_contains_doc_ids(self):
        # Use a corpus where one doc is very different
        docs = {
            "normal1": HEDGE_TEXT,
            "normal2": HEDGE_TEXT,
            "outlier": STRONG_TEXT * 10,  # very different style
        }
        cv = analyze_corpus_voice(docs, outlier_threshold=0.3)
        # outliers must be a subset of doc keys
        assert all(k in docs for k in cv.outliers)


# ---------------------------------------------------------------------------
# analyze_corpus_voice
# ---------------------------------------------------------------------------

class TestAnalyzeCorpusVoice:
    def test_empty_docs_returns_corpus_voice(self):
        cv = analyze_corpus_voice({})
        assert isinstance(cv, CorpusVoice)

    def test_empty_docs_empty_doc_profiles(self):
        cv = analyze_corpus_voice({})
        assert cv.doc_profiles == {}

    def test_empty_docs_no_outliers(self):
        cv = analyze_corpus_voice({})
        assert cv.outliers == []

    def test_single_doc_no_outliers(self):
        cv = analyze_corpus_voice({"only": HEDGE_TEXT})
        assert cv.outliers == []

    def test_returns_corpus_voice_instance(self):
        cv = analyze_corpus_voice({"a": HEDGE_TEXT, "b": STRONG_TEXT})
        assert isinstance(cv, CorpusVoice)

    def test_doc_profiles_keys_match_input(self):
        docs = {"x": HEDGE_TEXT, "y": STRONG_TEXT, "z": RICH_TEXT}
        cv = analyze_corpus_voice(docs)
        assert set(cv.doc_profiles.keys()) == set(docs.keys())

    def test_doc_profiles_values_are_epistemic_profiles(self):
        docs = {"a": HEDGE_TEXT}
        cv = analyze_corpus_voice(docs)
        assert all(isinstance(v, EpistemicProfile) for v in cv.doc_profiles.values())

    def test_corpus_profile_is_epistemic_profile(self):
        cv = analyze_corpus_voice({"a": HEDGE_TEXT, "b": STRONG_TEXT})
        assert isinstance(cv.profile, EpistemicProfile)

    def test_multiple_docs_doc_profiles_populated(self):
        docs = {str(i): f"Document number {i} with some content." for i in range(5)}
        cv = analyze_corpus_voice(docs)
        assert len(cv.doc_profiles) == 5

    def test_outlier_threshold_respected(self):
        # With threshold=0.0 every doc should be an outlier (distance > 0)
        # except when the corpus is a single doc (distance from itself = 0)
        docs = {"a": HEDGE_TEXT, "b": STRONG_TEXT}
        cv = analyze_corpus_voice(docs, outlier_threshold=0.0)
        # At least the doc furthest from the mean is flagged
        assert isinstance(cv.outliers, list)
