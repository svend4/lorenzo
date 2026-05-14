"""Tests for docstoolkit.trust_scoring — E33."""
import math
import pytest

from docstoolkit.trust_scoring import (
    TrustSignal,
    SignalScore,
    TrustSignalExtractor,
    TrustWeights,
    TrustScore,
    TrustScorer,
    TrustRegistry,
)


# ===========================================================================
# Helpers
# ===========================================================================

def make_score(doc_id="doc1", overall=0.75, grade="B", signals=None):
    """Build a minimal TrustScore for registry tests."""
    if signals is None:
        signals = []
    return TrustScore(doc_id=doc_id, overall=overall, grade=grade, signals=signals)


# ===========================================================================
# TrustSignal enum
# ===========================================================================

class TestTrustSignalEnum:
    def test_all_members_present(self):
        members = {s.name for s in TrustSignal}
        assert members == {
            "SOURCE_QUALITY",
            "RECENCY",
            "CITATION_COUNT",
            "AUTHOR_REPUTATION",
            "CONTENT_CONSISTENCY",
            "CROSS_VALIDATION",
        }

    def test_values_are_strings(self):
        for signal in TrustSignal:
            assert isinstance(signal.value, str)


# ===========================================================================
# SignalScore
# ===========================================================================

class TestSignalScore:
    def test_weighted_score_basic(self):
        ss = SignalScore(TrustSignal.RECENCY, raw_value=0.8, normalized=0.8, weight=0.5)
        assert ss.weighted_score() == pytest.approx(0.4)

    def test_weighted_score_full_weight(self):
        ss = SignalScore(TrustSignal.SOURCE_QUALITY, raw_value=1.0, normalized=1.0, weight=1.0)
        assert ss.weighted_score() == pytest.approx(1.0)

    def test_weighted_score_zero_normalized(self):
        ss = SignalScore(TrustSignal.CITATION_COUNT, raw_value=0.0, normalized=0.0, weight=0.9)
        assert ss.weighted_score() == pytest.approx(0.0)

    def test_default_weight_is_one(self):
        ss = SignalScore(TrustSignal.AUTHOR_REPUTATION, raw_value=0.5, normalized=0.5)
        assert ss.weight == 1.0
        assert ss.weighted_score() == pytest.approx(0.5)

    def test_fields_stored(self):
        ss = SignalScore(TrustSignal.CONTENT_CONSISTENCY, 0.7, 0.7, 0.3)
        assert ss.signal == TrustSignal.CONTENT_CONSISTENCY
        assert ss.raw_value == pytest.approx(0.7)
        assert ss.normalized == pytest.approx(0.7)
        assert ss.weight == pytest.approx(0.3)


# ===========================================================================
# TrustSignalExtractor — source_quality
# ===========================================================================

class TestSourceQuality:
    def setup_method(self):
        self.ex = TrustSignalExtractor()

    # Known trusted sources
    def test_github(self):
        assert self.ex.source_quality("https://github.com/user/repo") == pytest.approx(1.0)

    def test_arxiv(self):
        assert self.ex.source_quality("https://arxiv.org/abs/1234") == pytest.approx(1.0)

    def test_wikipedia(self):
        assert self.ex.source_quality("https://wikipedia.org/wiki/Python") == pytest.approx(1.0)

    def test_docs_python(self):
        assert self.ex.source_quality("https://docs.python.org/3/") == pytest.approx(1.0)

    def test_subdomain_of_trusted(self):
        assert self.ex.source_quality("https://gist.github.com/user/abc") == pytest.approx(1.0)

    def test_www_prefix_trusted(self):
        assert self.ex.source_quality("https://www.github.com/user") == pytest.approx(1.0)

    # .edu / .gov
    def test_edu_domain(self):
        assert self.ex.source_quality("https://mit.edu/paper") == pytest.approx(0.7)

    def test_gov_domain(self):
        assert self.ex.source_quality("https://nist.gov/resource") == pytest.approx(0.7)

    # .com / .org
    def test_com_domain(self):
        assert self.ex.source_quality("https://example.com/page") == pytest.approx(0.5)

    def test_org_domain(self):
        assert self.ex.source_quality("https://openai.org/research") == pytest.approx(0.5)

    # Unknown / empty
    def test_empty_url(self):
        assert self.ex.source_quality("") == pytest.approx(0.3)

    def test_unknown_tld(self):
        assert self.ex.source_quality("https://example.xyz/page") == pytest.approx(0.3)

    def test_no_scheme(self):
        assert self.ex.source_quality("not_a_url") == pytest.approx(0.3)


# ===========================================================================
# TrustSignalExtractor — recency
# ===========================================================================

class TestRecency:
    def setup_method(self):
        self.ex = TrustSignalExtractor()

    def test_zero_days(self):
        assert self.ex.recency(0) == pytest.approx(1.0)

    def test_one_year(self):
        # exp(-1) ≈ 0.3679
        assert self.ex.recency(365) == pytest.approx(math.exp(-1), rel=1e-5)

    def test_two_years(self):
        assert self.ex.recency(730) == pytest.approx(math.exp(-2), rel=1e-5)

    def test_negative_days_treated_as_zero(self):
        assert self.ex.recency(-10) == pytest.approx(1.0)

    def test_half_year(self):
        assert self.ex.recency(182.5) == pytest.approx(math.exp(-0.5), rel=1e-3)

    def test_decreasing_with_age(self):
        scores = [self.ex.recency(d) for d in [0, 30, 90, 365, 730]]
        assert scores == sorted(scores, reverse=True)

    def test_range_0_to_1(self):
        for days in [0, 1, 100, 365, 1000, 3650]:
            s = self.ex.recency(days)
            assert 0.0 < s <= 1.0


# ===========================================================================
# TrustSignalExtractor — citation_count
# ===========================================================================

class TestCitationCount:
    def setup_method(self):
        self.ex = TrustSignalExtractor()

    def test_zero(self):
        assert self.ex.citation_count(0) == pytest.approx(0.0)

    def test_50(self):
        assert self.ex.citation_count(50) == pytest.approx(0.5)

    def test_100(self):
        assert self.ex.citation_count(100) == pytest.approx(1.0)

    def test_above_100_capped(self):
        assert self.ex.citation_count(200) == pytest.approx(1.0)
        assert self.ex.citation_count(99999) == pytest.approx(1.0)

    def test_negative_treated_as_zero(self):
        assert self.ex.citation_count(-5) == pytest.approx(0.0)

    def test_linear_below_100(self):
        assert self.ex.citation_count(25) == pytest.approx(0.25)
        assert self.ex.citation_count(75) == pytest.approx(0.75)


# ===========================================================================
# TrustSignalExtractor — content_consistency
# ===========================================================================

class TestContentConsistency:
    def setup_method(self):
        self.ex = TrustSignalExtractor()

    def test_empty_string(self):
        assert self.ex.content_consistency("") == pytest.approx(1.0)

    def test_whitespace_only(self):
        assert self.ex.content_consistency("   ") == pytest.approx(1.0)

    def test_single_sentence(self):
        assert self.ex.content_consistency("Hello world.") == pytest.approx(1.0)

    def test_uniform_sentences_high_score(self):
        # All sentences of similar length → low CV → score close to 1
        text = "The cat sat. The dog ran. The bird flew. The fish swam."
        score = self.ex.content_consistency(text)
        assert score > 0.5

    def test_very_variable_sentences_lower_score(self):
        # Mix a one-word sentence with a very long one
        short = "Yes."
        long_sent = "This is an extraordinarily long sentence filled with many words to create significant length variation. " * 3
        text = short + " " + long_sent
        score = self.ex.content_consistency(text)
        # Should be noticeably below the uniform case
        assert score < 0.9

    def test_output_range(self):
        texts = [
            "A. B. C.",
            "Short. " * 10,
            "Word. " + "A very long sentence with lots of words and content. " * 5,
        ]
        for t in texts:
            s = self.ex.content_consistency(t)
            assert 0.0 <= s <= 1.0


# ===========================================================================
# TrustWeights
# ===========================================================================

class TestTrustWeights:
    def test_default_values(self):
        w = TrustWeights()
        assert w.source == pytest.approx(0.25)
        assert w.recency == pytest.approx(0.20)
        assert w.citations == pytest.approx(0.20)
        assert w.author == pytest.approx(0.15)
        assert w.consistency == pytest.approx(0.10)
        assert w.cross_val == pytest.approx(0.10)

    def test_default_sum(self):
        w = TrustWeights()
        total = w.source + w.recency + w.citations + w.author + w.consistency + w.cross_val
        assert total == pytest.approx(1.0)

    def test_normalize_already_normalized(self):
        w = TrustWeights()
        n = w.normalize()
        total = n.source + n.recency + n.citations + n.author + n.consistency + n.cross_val
        assert total == pytest.approx(1.0)

    def test_normalize_unnormalized(self):
        w = TrustWeights(source=1.0, recency=1.0, citations=1.0,
                         author=1.0, consistency=1.0, cross_val=1.0)
        n = w.normalize()
        total = n.source + n.recency + n.citations + n.author + n.consistency + n.cross_val
        assert total == pytest.approx(1.0)
        # each should be 1/6
        assert n.source == pytest.approx(1 / 6)

    def test_normalize_returns_new_instance(self):
        w = TrustWeights()
        n = w.normalize()
        assert n is not w

    def test_normalize_zero_raises(self):
        w = TrustWeights(source=0, recency=0, citations=0, author=0, consistency=0, cross_val=0)
        with pytest.raises(ValueError):
            w.normalize()

    def test_normalize_proportions_preserved(self):
        w = TrustWeights(source=2.0, recency=1.0, citations=1.0,
                         author=0.0, consistency=0.0, cross_val=0.0)
        n = w.normalize()
        assert n.source == pytest.approx(0.5)
        assert n.recency == pytest.approx(0.25)
        assert n.citations == pytest.approx(0.25)


# ===========================================================================
# TrustScore
# ===========================================================================

def _build_trust_score(signals=None, overall=0.7, grade="B"):
    if signals is None:
        signals = [
            SignalScore(TrustSignal.SOURCE_QUALITY,      0.9, 0.9, 0.3),
            SignalScore(TrustSignal.RECENCY,             0.5, 0.5, 0.2),
            SignalScore(TrustSignal.CITATION_COUNT,      0.1, 0.1, 0.2),
            SignalScore(TrustSignal.AUTHOR_REPUTATION,   0.7, 0.7, 0.15),
            SignalScore(TrustSignal.CONTENT_CONSISTENCY, 0.8, 0.8, 0.1),
            SignalScore(TrustSignal.CROSS_VALIDATION,    0.0, 0.0, 0.05),
        ]
    return TrustScore(doc_id="test", overall=overall, grade=grade, signals=signals)


class TestTrustScore:
    def test_fields(self):
        ts = TrustScore(doc_id="x", overall=0.5, grade="C")
        assert ts.doc_id == "x"
        assert ts.overall == pytest.approx(0.5)
        assert ts.grade == "C"
        assert ts.signals == []

    def test_dominant_signal(self):
        ts = _build_trust_score()
        # SOURCE_QUALITY: 0.9 * 0.3 = 0.27
        # AUTHOR_REPUTATION: 0.7 * 0.15 = 0.105
        # CONTENT_CONSISTENCY: 0.8 * 0.1 = 0.08
        # RECENCY: 0.5 * 0.2 = 0.10
        # CITATION_COUNT: 0.1 * 0.2 = 0.02
        # SOURCE_QUALITY is dominant
        assert ts.dominant_signal() == TrustSignal.SOURCE_QUALITY

    def test_dominant_signal_no_signals_raises(self):
        ts = TrustScore(doc_id="x", overall=0.5, grade="C", signals=[])
        with pytest.raises(ValueError):
            ts.dominant_signal()

    def test_weak_signals_default_threshold(self):
        ts = _build_trust_score()
        weak = ts.weak_signals()
        # CITATION_COUNT normalized=0.1, CROSS_VALIDATION normalized=0.0 → both < 0.3
        assert TrustSignal.CITATION_COUNT in weak
        assert TrustSignal.CROSS_VALIDATION in weak
        assert TrustSignal.SOURCE_QUALITY not in weak

    def test_weak_signals_custom_threshold(self):
        ts = _build_trust_score()
        weak = ts.weak_signals(threshold=0.6)
        # RECENCY=0.5, CITATION_COUNT=0.1, CROSS_VALIDATION=0.0 → < 0.6
        assert TrustSignal.RECENCY in weak
        assert TrustSignal.CITATION_COUNT in weak

    def test_weak_signals_none_below_threshold(self):
        signals = [
            SignalScore(TrustSignal.SOURCE_QUALITY, 0.9, 0.9, 0.5),
            SignalScore(TrustSignal.RECENCY,        0.8, 0.8, 0.5),
        ]
        ts = TrustScore("x", 0.85, "A", signals)
        assert ts.weak_signals(threshold=0.3) == []

    def test_weak_signals_all_below_threshold(self):
        signals = [
            SignalScore(TrustSignal.SOURCE_QUALITY, 0.1, 0.1, 0.5),
            SignalScore(TrustSignal.RECENCY,        0.2, 0.2, 0.5),
        ]
        ts = TrustScore("x", 0.15, "F", signals)
        weak = ts.weak_signals(threshold=0.3)
        assert TrustSignal.SOURCE_QUALITY in weak
        assert TrustSignal.RECENCY in weak


# ===========================================================================
# TrustScorer
# ===========================================================================

class TestTrustScorer:
    def setup_method(self):
        self.scorer = TrustScorer()

    def test_returns_trust_score(self):
        ts = self.scorer.score("doc1", "Hello world.", source_url="https://github.com/x/y")
        assert isinstance(ts, TrustScore)

    def test_doc_id_preserved(self):
        ts = self.scorer.score("my-unique-doc", "content")
        assert ts.doc_id == "my-unique-doc"

    def test_overall_in_range(self):
        ts = self.scorer.score("d", "Some text here. Another sentence.", days_old=10)
        assert 0.0 <= ts.overall <= 1.0

    def test_grade_a_for_high_quality(self):
        ts = self.scorer.score(
            "doc_a",
            "Uniform. Sentences. Here. Now.",
            source_url="https://github.com/x/y",
            days_old=0,
            citation_count=100,
            author_score=1.0,
        )
        assert ts.grade == "A"

    def test_grade_f_for_low_quality(self):
        ts = self.scorer.score(
            "doc_f",
            "",
            source_url="",
            days_old=10000,
            citation_count=0,
            author_score=0.0,
        )
        assert ts.grade == "F"

    def test_grade_mapping(self):
        assert TrustScorer._grade(0.85) == "A"
        assert TrustScorer._grade(0.80) == "A"
        assert TrustScorer._grade(0.79) == "B"
        assert TrustScorer._grade(0.60) == "B"
        assert TrustScorer._grade(0.59) == "C"
        assert TrustScorer._grade(0.40) == "C"
        assert TrustScorer._grade(0.39) == "D"
        assert TrustScorer._grade(0.20) == "D"
        assert TrustScorer._grade(0.19) == "F"
        assert TrustScorer._grade(0.0)  == "F"

    def test_signals_count(self):
        ts = self.scorer.score("d", "text")
        assert len(ts.signals) == 6

    def test_signal_types_present(self):
        ts = self.scorer.score("d", "text")
        signal_types = {s.signal for s in ts.signals}
        assert signal_types == set(TrustSignal)

    def test_source_url_affects_score(self):
        good = self.scorer.score("d1", "text", source_url="https://github.com/x")
        bad  = self.scorer.score("d2", "text", source_url="")
        assert good.overall > bad.overall

    def test_fresher_document_scores_higher(self):
        fresh = self.scorer.score("d1", "text", days_old=0)
        old   = self.scorer.score("d2", "text", days_old=3650)
        assert fresh.overall > old.overall

    def test_more_citations_better(self):
        cited    = self.scorer.score("d1", "text", citation_count=100)
        uncited  = self.scorer.score("d2", "text", citation_count=0)
        assert cited.overall > uncited.overall

    def test_custom_weights_accepted(self):
        w = TrustWeights(source=1.0, recency=0, citations=0, author=0, consistency=0, cross_val=0)
        scorer = TrustScorer(weights=w)
        ts = scorer.score("d", "text", source_url="https://github.com/x")
        # SOURCE_QUALITY = 1.0, weight=1.0 → overall ≈ 1.0
        assert ts.overall == pytest.approx(1.0, abs=1e-9)

    def test_custom_extractor_accepted(self):
        class ConstantExtractor(TrustSignalExtractor):
            def source_quality(self, url):    return 0.5
            def recency(self, days):          return 0.5
            def citation_count(self, count):  return 0.5
            def content_consistency(self, t): return 0.5

        scorer = TrustScorer(extractor=ConstantExtractor())
        # author_score=0.5, CROSS_VALIDATION defaults to 0.0 (no extractor for it)
        # overall = sum(normalized_i * weight_i)
        # = 0.5*(src+rec+cit+auth+cons) + 0.0*cross_val
        # With default weights normalised: source=0.25,rec=0.20,cit=0.20,auth=0.15,cons=0.10,cv=0.10
        # = 0.5*(0.25+0.20+0.20+0.15+0.10) + 0.0*0.10 = 0.5*0.90 = 0.45
        ts = scorer.score("d", "any text", author_score=0.5)
        assert ts.overall == pytest.approx(0.45, abs=1e-6)

    def test_author_score_clamped(self):
        ts_high = self.scorer.score("d1", "text", author_score=999.0)
        ts_low  = self.scorer.score("d2", "text", author_score=-999.0)
        # Should not raise; overall stays in [0,1]
        assert 0.0 <= ts_high.overall <= 1.0
        assert 0.0 <= ts_low.overall  <= 1.0


# ===========================================================================
# TrustRegistry
# ===========================================================================

class TestTrustRegistry:
    def setup_method(self):
        self.reg = TrustRegistry()  # in-memory

    def teardown_method(self):
        self.reg.close()

    # --- save / get -------------------------------------------------------

    def test_save_and_get(self):
        ts = make_score("doc1", overall=0.75, grade="B")
        self.reg.save(ts)
        result = self.reg.get("doc1")
        assert result is not None
        assert result.doc_id == "doc1"
        assert result.overall == pytest.approx(0.75)
        assert result.grade == "B"

    def test_get_missing_returns_none(self):
        assert self.reg.get("nonexistent") is None

    def test_save_overwrites(self):
        ts1 = make_score("d", overall=0.5, grade="C")
        ts2 = make_score("d", overall=0.9, grade="A")
        self.reg.save(ts1)
        self.reg.save(ts2)
        result = self.reg.get("d")
        assert result.overall == pytest.approx(0.9)
        assert result.grade == "A"

    def test_signals_roundtrip(self):
        signals = [
            SignalScore(TrustSignal.SOURCE_QUALITY, 1.0, 1.0, 0.25),
            SignalScore(TrustSignal.RECENCY,        0.5, 0.5, 0.20),
        ]
        ts = TrustScore("d", 0.8, "A", signals)
        self.reg.save(ts)
        result = self.reg.get("d")
        assert len(result.signals) == 2
        assert result.signals[0].signal == TrustSignal.SOURCE_QUALITY
        assert result.signals[0].normalized == pytest.approx(1.0)
        assert result.signals[1].signal == TrustSignal.RECENCY

    # --- top_trusted ------------------------------------------------------

    def test_top_trusted_order(self):
        for i, overall in enumerate([0.9, 0.5, 0.7, 0.3]):
            self.reg.save(make_score(f"d{i}", overall=overall))
        top = self.reg.top_trusted(n=4)
        assert top[0].overall >= top[1].overall >= top[2].overall >= top[3].overall

    def test_top_trusted_limit(self):
        for i in range(20):
            self.reg.save(make_score(f"d{i}", overall=i / 20))
        top = self.reg.top_trusted(n=5)
        assert len(top) == 5

    def test_top_trusted_empty(self):
        assert self.reg.top_trusted() == []

    def test_top_trusted_fewer_than_n(self):
        self.reg.save(make_score("only", overall=0.8))
        top = self.reg.top_trusted(n=10)
        assert len(top) == 1

    # --- low_trust --------------------------------------------------------

    def test_low_trust_below_threshold(self):
        self.reg.save(make_score("low1", overall=0.1))
        self.reg.save(make_score("low2", overall=0.3))
        self.reg.save(make_score("high", overall=0.8))
        low = self.reg.low_trust(threshold=0.4)
        doc_ids = {s.doc_id for s in low}
        assert "low1" in doc_ids
        assert "low2" in doc_ids
        assert "high" not in doc_ids

    def test_low_trust_sorted_ascending(self):
        for i, v in enumerate([0.35, 0.1, 0.25]):
            self.reg.save(make_score(f"d{i}", overall=v))
        low = self.reg.low_trust(threshold=0.4)
        for a, b in zip(low, low[1:]):
            assert a.overall <= b.overall

    def test_low_trust_limit(self):
        for i in range(15):
            self.reg.save(make_score(f"d{i}", overall=0.1))
        low = self.reg.low_trust(n=5)
        assert len(low) == 5

    def test_low_trust_empty_when_all_above(self):
        self.reg.save(make_score("high", overall=0.9))
        assert self.reg.low_trust(threshold=0.4) == []

    # --- stats ------------------------------------------------------------

    def test_stats_empty(self):
        s = self.reg.stats()
        assert s["total"] == 0
        assert s["avg_score"] == pytest.approx(0.0)
        assert s["grade_distribution"] == {}

    def test_stats_total(self):
        for i in range(5):
            self.reg.save(make_score(f"d{i}", overall=0.5, grade="C"))
        s = self.reg.stats()
        assert s["total"] == 5

    def test_stats_avg_score(self):
        self.reg.save(make_score("d1", overall=0.4, grade="C"))
        self.reg.save(make_score("d2", overall=0.6, grade="B"))
        s = self.reg.stats()
        assert s["avg_score"] == pytest.approx(0.5)

    def test_stats_grade_distribution(self):
        self.reg.save(make_score("a1", overall=0.9, grade="A"))
        self.reg.save(make_score("a2", overall=0.85, grade="A"))
        self.reg.save(make_score("b1", overall=0.65, grade="B"))
        s = self.reg.stats()
        dist = s["grade_distribution"]
        assert dist.get("A", 0) == 2
        assert dist.get("B", 0) == 1

    def test_stats_keys_present(self):
        s = self.reg.stats()
        assert "total" in s
        assert "avg_score" in s
        assert "grade_distribution" in s

    # --- context manager --------------------------------------------------

    def test_context_manager(self):
        with TrustRegistry() as reg:
            reg.save(make_score("x", overall=0.5))
            assert reg.get("x") is not None
        # After exit, connection is closed; further calls should raise
        with pytest.raises(Exception):
            reg.get("x")

    # --- integration: full scorer → registry pipeline --------------------

    def test_scorer_to_registry_pipeline(self):
        scorer = TrustScorer()
        docs = [
            ("doc_a", "Content A. More text.", "https://github.com/x", 10, 50, 0.8),
            ("doc_b", "Content B.", "https://example.com/y", 400, 5, 0.4),
            ("doc_c", "Content C.", "", 1000, 0, 0.1),
        ]
        for doc_id, content, url, days, cites, author in docs:
            ts = scorer.score(doc_id, content, url, days, cites, author)
            self.reg.save(ts)

        top = self.reg.top_trusted(n=1)
        assert top[0].doc_id == "doc_a"

        stats = self.reg.stats()
        assert stats["total"] == 3
        assert 0.0 < stats["avg_score"] < 1.0
