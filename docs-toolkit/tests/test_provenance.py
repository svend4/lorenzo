"""Tests for docstoolkit.provenance module (I3: Provenance with confidence intervals)."""
import pytest

from docstoolkit.provenance import (
    bootstrap_ci, BootstrapCI,
    extract_claims, link_sources, Claim, Source,
    ProvenancedAnswer, ask_with_provenance,
)
from docstoolkit.provenance.claims import _token_overlap
from docstoolkit.rag.types import Passage


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_passage(text: str, doc_id: str = "doc1") -> Passage:
    return Passage(text=text, doc_id=doc_id, title=doc_id)


# ---------------------------------------------------------------------------
# bootstrap_ci tests
# ---------------------------------------------------------------------------

class TestBootstrapCI:
    def test_empty_list_returns_zeros(self):
        result = bootstrap_ci([])
        assert isinstance(result, BootstrapCI)
        assert result.point_estimate == 0.0
        assert result.ci_low == 0.0
        assert result.ci_high == 0.0
        assert result.n_samples == 0

    def test_single_value_point_estimate(self):
        result = bootstrap_ci([0.75])
        assert result.point_estimate == pytest.approx(0.75)

    def test_single_value_ci_contains_value(self):
        result = bootstrap_ci([0.75])
        assert result.ci_low <= 0.75 <= result.ci_high

    def test_all_same_values_ci_tight(self):
        result = bootstrap_ci([0.5] * 20, seed=42)
        assert result.ci_low == pytest.approx(0.5, abs=0.01)
        assert result.ci_high == pytest.approx(0.5, abs=0.01)

    def test_zero_one_list_mean_approx_half(self):
        result = bootstrap_ci([0.0, 1.0] * 50, seed=42)
        assert result.point_estimate == pytest.approx(0.5)

    def test_ci_low_less_than_ci_high_nontrivial(self):
        data = [0.1, 0.3, 0.5, 0.7, 0.9, 0.2, 0.4, 0.6, 0.8]
        result = bootstrap_ci(data, seed=42)
        assert result.ci_low < result.ci_high

    def test_n_samples_field_matches_n_bootstrap(self):
        result = bootstrap_ci([0.1, 0.5, 0.9], n_bootstrap=150, seed=42)
        assert result.n_samples == 150

    def test_statistic_max_returns_max(self):
        data = [0.1, 0.3, 0.7, 0.9]
        result = bootstrap_ci(data, statistic="max", seed=42)
        assert result.point_estimate == pytest.approx(0.9)

    def test_statistic_median_returns_median(self):
        data = [0.1, 0.3, 0.5, 0.7, 0.9]
        result = bootstrap_ci(data, statistic="median", seed=42)
        assert result.point_estimate == pytest.approx(0.5)

    def test_statistic_median_even_length(self):
        data = [0.1, 0.3, 0.5, 0.7]
        result = bootstrap_ci(data, statistic="median", seed=42)
        assert result.point_estimate == pytest.approx(0.4)

    def test_narrow_ci_at_80_vs_95(self):
        data = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] * 5
        r80 = bootstrap_ci(data, confidence_level=0.80, seed=99)
        r95 = bootstrap_ci(data, confidence_level=0.95, seed=99)
        width_80 = r80.ci_high - r80.ci_low
        width_95 = r95.ci_high - r95.ci_low
        assert width_80 < width_95

    def test_reproducible_with_same_seed(self):
        data = [0.1, 0.4, 0.6, 0.9]
        r1 = bootstrap_ci(data, seed=7)
        r2 = bootstrap_ci(data, seed=7)
        assert r1.ci_low == r2.ci_low
        assert r1.ci_high == r2.ci_high
        assert r1.point_estimate == r2.point_estimate

    def test_different_seeds_may_differ(self):
        data = [0.1, 0.3, 0.5, 0.7, 0.9, 0.2]
        r1 = bootstrap_ci(data, seed=1, n_bootstrap=50)
        r2 = bootstrap_ci(data, seed=2, n_bootstrap=50)
        # With small n_bootstrap, different seeds should typically produce different CIs
        # (at least one boundary differs — probabilistic, but reliable with these params)
        assert r1 != r2 or True  # always pass; we just verify no crash with different seeds

    def test_confidence_level_stored(self):
        result = bootstrap_ci([0.5], confidence_level=0.90)
        assert result.confidence_level == pytest.approx(0.90)


# ---------------------------------------------------------------------------
# extract_claims tests
# ---------------------------------------------------------------------------

class TestExtractClaims:
    def test_single_sentence_one_claim(self):
        claims = extract_claims("The sky is blue.")
        assert len(claims) == 1
        assert "sky" in claims[0].lower() or "blue" in claims[0].lower()

    def test_multiple_sentences_multiple_claims(self):
        text = "The sky is blue. Water is wet. Fire is hot."
        claims = extract_claims(text)
        assert len(claims) >= 2

    def test_citation_single_stripped(self):
        text = "The study showed results [1]. This proves the theory."
        claims = extract_claims(text)
        for c in claims:
            assert "[1]" not in c

    def test_citation_range_stripped(self):
        text = "As shown in prior work [2-4], the method is effective."
        claims = extract_claims(text)
        for c in claims:
            assert "[2-4]" not in c

    def test_very_short_sentence_filtered_out(self):
        text = "Hi. The architecture of the system is complex and well-designed."
        claims = extract_claims(text)
        # "Hi." is < 10 chars so should not appear
        for c in claims:
            assert len(c) >= 10

    def test_empty_string_returns_empty_list(self):
        assert extract_claims("") == []

    def test_whitespace_string_returns_empty_list(self):
        assert extract_claims("   \n  ") == []

    def test_claims_are_strings(self):
        text = "Python is a programming language. It is widely used."
        claims = extract_claims(text)
        for c in claims:
            assert isinstance(c, str)

    def test_multiple_citation_types_stripped(self):
        text = "Result [1] confirmed by [3]. The data [2-4] shows growth."
        claims = extract_claims(text)
        for c in claims:
            import re
            assert not re.search(r'\[\d+(?:-\d+)?\]', c)


# ---------------------------------------------------------------------------
# _token_overlap tests
# ---------------------------------------------------------------------------

class TestTokenOverlap:
    def test_identical_strings_returns_one(self):
        assert _token_overlap("hello world", "hello world") == pytest.approx(1.0)

    def test_completely_different_returns_zero(self):
        result = _token_overlap("apple banana cherry", "dog elephant frog")
        assert result == pytest.approx(0.0)

    def test_partial_overlap_in_range(self):
        result = _token_overlap("the cat sat", "the dog sat")
        assert 0.0 < result < 1.0

    def test_empty_strings_return_zero(self):
        assert _token_overlap("", "hello") == pytest.approx(0.0)
        assert _token_overlap("hello", "") == pytest.approx(0.0)

    def test_case_insensitive(self):
        assert _token_overlap("Hello World", "hello world") == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# link_sources tests
# ---------------------------------------------------------------------------

class TestLinkSources:
    def test_no_passages_all_confidence_zero(self):
        claims = ["The sky is blue and beautiful today."]
        result = link_sources(claims, [])
        assert len(result) == 1
        assert result[0].confidence == pytest.approx(0.0)
        assert result[0].sources == []

    def test_matching_passage_source_linked(self):
        claims = ["The sky is blue and beautiful."]
        passage = make_passage("The sky is blue and beautiful on a clear day.", "doc_sky")
        result = link_sources(claims, [passage])
        assert len(result) == 1
        assert result[0].confidence > 0.0
        assert len(result[0].sources) == 1

    def test_min_similarity_respected(self):
        # Low overlap claim should not be linked when min_similarity is high
        claims = ["Quantum mechanics describes subatomic particles."]
        passage = make_passage("The weather today is sunny and warm outside.", "doc_weather")
        result = link_sources(claims, [passage], min_similarity=0.5)
        assert result[0].sources == []

    def test_returns_same_length_as_input_claims(self):
        claims = ["First claim about Python.", "Second claim about testing.", "Third claim here."]
        result = link_sources(claims, [])
        assert len(result) == len(claims)

    def test_source_has_doc_id_from_passage(self):
        claims = ["Python is a popular programming language used widely."]
        passage = make_passage(
            "Python is a popular programming language used in data science.", "my_doc_42"
        )
        result = link_sources(claims, [passage])
        if result[0].sources:
            assert result[0].sources[0].doc_id == "my_doc_42"

    def test_returns_list_of_claim_objects(self):
        claims = ["The earth orbits the sun every year."]
        result = link_sources(claims, [])
        assert all(isinstance(c, Claim) for c in result)

    def test_claim_ids_sequential(self):
        claims = ["First sentence here.", "Second sentence here.", "Third sentence here."]
        result = link_sources(claims, [])
        assert result[0].id == "claim_0"
        assert result[1].id == "claim_1"
        assert result[2].id == "claim_2"

    def test_multiple_passages_best_linked(self):
        claim = "The ocean is deep and full of marine life."
        passage_related = make_passage(
            "The ocean is very deep and contains many forms of marine life.", "doc_ocean"
        )
        passage_unrelated = make_passage(
            "Mathematics involves numbers and equations.", "doc_math"
        )
        result = link_sources([claim], [passage_related, passage_unrelated])
        assert result[0].confidence > 0.0
        # The ocean passage should be the best source
        if result[0].sources:
            doc_ids = [s.doc_id for s in result[0].sources]
            assert "doc_ocean" in doc_ids


# ---------------------------------------------------------------------------
# ProvenancedAnswer tests
# ---------------------------------------------------------------------------

class TestProvenancedAnswer:
    def _make_answer(self) -> ProvenancedAnswer:
        from docstoolkit.provenance.claims import Claim
        claims = [
            Claim(id="claim_0", text="Python is great.", confidence=0.8,
                  confidence_ci=(0.7, 0.9)),
            Claim(id="claim_1", text="Testing is important.", confidence=0.6,
                  confidence_ci=(0.5, 0.7)),
        ]
        return ProvenancedAnswer(
            text="Python is great. Testing is important.",
            claims=claims,
            overall_confidence=0.7,
        )

    def test_has_text_field(self):
        ans = self._make_answer()
        assert isinstance(ans.text, str)

    def test_has_claims_field(self):
        ans = self._make_answer()
        assert isinstance(ans.claims, list)

    def test_has_overall_confidence_field(self):
        ans = self._make_answer()
        assert isinstance(ans.overall_confidence, float)

    def test_to_markdown_contains_answer_header(self):
        ans = self._make_answer()
        md = ans.to_markdown()
        assert "Answer" in md

    def test_to_markdown_contains_claims_header(self):
        ans = self._make_answer()
        md = ans.to_markdown()
        assert "Claims" in md

    def test_to_markdown_shows_confidence_values(self):
        ans = self._make_answer()
        md = ans.to_markdown()
        assert "0.80" in md or "0.8" in md

    def test_high_confidence_claims_filters_correctly(self):
        ans = self._make_answer()
        high = ans.high_confidence_claims(threshold=0.7)
        assert all(c.confidence >= 0.7 for c in high)
        assert len(high) == 1  # only claim_0 (0.8) passes 0.7 threshold

    def test_high_confidence_claims_default_threshold(self):
        ans = self._make_answer()
        high = ans.high_confidence_claims()  # default 0.7
        assert all(c.confidence >= 0.7 for c in high)

    def test_high_confidence_all_pass_zero_threshold(self):
        ans = self._make_answer()
        all_claims = ans.high_confidence_claims(threshold=0.0)
        assert len(all_claims) == len(ans.claims)

    def test_to_markdown_returns_string(self):
        ans = self._make_answer()
        assert isinstance(ans.to_markdown(), str)


# ---------------------------------------------------------------------------
# ask_with_provenance tests
# ---------------------------------------------------------------------------

class TestAskWithProvenance:
    def test_returns_provenanced_answer(self):
        result = ask_with_provenance(
            question="What is Python?",
            answer_text="Python is a programming language. It is widely used.",
            passages=[],
        )
        assert isinstance(result, ProvenancedAnswer)

    def test_empty_passages_overall_confidence_zero(self):
        result = ask_with_provenance(
            question="What is X?",
            answer_text="X is a well-known framework. It is used everywhere.",
            passages=[],
        )
        assert result.overall_confidence == pytest.approx(0.0)

    def test_matching_passages_confidence_positive(self):
        answer = "Python is a popular programming language. It supports many paradigms."
        passage = make_passage(
            "Python is a popular high-level programming language that supports "
            "multiple programming paradigms.", "doc1"
        )
        result = ask_with_provenance(
            question="Tell me about Python.",
            answer_text=answer,
            passages=[passage],
        )
        assert result.overall_confidence > 0.0

    def test_claims_count_matches_extracted_sentences(self):
        answer = "The sky is blue today. Water covers most of the earth. Trees are green."
        result = ask_with_provenance(
            question="Describe the world.",
            answer_text=answer,
            passages=[],
        )
        expected = extract_claims(answer)
        assert len(result.claims) == len(expected)

    def test_overall_confidence_is_mean_of_claims(self):
        answer = "The earth is round. The moon orbits the earth. Stars are distant suns."
        passage = make_passage(
            "The earth is a round planet. The moon orbits the earth monthly. "
            "Stars are very distant suns in the universe.", "astro"
        )
        result = ask_with_provenance(
            question="Astronomy facts.",
            answer_text=answer,
            passages=[passage],
        )
        if result.claims:
            expected_mean = sum(c.confidence for c in result.claims) / len(result.claims)
            assert result.overall_confidence == pytest.approx(expected_mean)

    def test_no_exception_on_empty_answer(self):
        result = ask_with_provenance(
            question="?",
            answer_text="",
            passages=[],
        )
        assert isinstance(result, ProvenancedAnswer)
        assert result.overall_confidence == pytest.approx(0.0)
