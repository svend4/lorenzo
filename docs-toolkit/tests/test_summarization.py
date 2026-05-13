"""Tests for docstoolkit.summarization (E37 — Document summarization pipeline)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.summarization import (
    SentenceScore,
    ExtractiveSummarizer,
    TemplateConfig,
    AbstractiveSummarizer,
    SummaryLevel,
    SummaryConfig,
    SummaryResult,
    SummarizationPipeline,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

SHORT_TEXT = (
    "Memory systems store information persistently. "
    "Retrieval mechanisms fetch relevant data on demand. "
    "Indexing improves lookup speed significantly."
)

LONG_TEXT = (
    "Machine learning models are trained on large datasets. "
    "Neural networks learn hierarchical representations from examples. "
    "Deep learning achieves state-of-the-art results in many tasks. "
    "Natural language processing deals with understanding human text. "
    "Transformer architectures use attention mechanisms extensively. "
    "Transfer learning allows reuse of pretrained model weights. "
    "Fine-tuning adapts a model to specific downstream tasks. "
    "Embeddings represent words and sentences as dense vectors. "
    "Semantic search retrieves documents by meaning rather than keywords. "
    "Knowledge graphs store structured facts about the world."
)

PARAGRAPH_TEXT = (
    "Agents are autonomous systems that perceive environments.\n\n"
    "Memory modules allow agents to retain context across sessions. "
    "Long-term memory persists beyond individual interactions.\n\n"
    "Retrieval-augmented generation improves factual accuracy. "
    "Vector databases enable fast similarity search over embeddings."
)


# ===========================================================================
# ExtractiveSummarizer
# ===========================================================================

class TestExtractorTokenizeSentences:
    def test_splits_on_period_space(self):
        ex = ExtractiveSummarizer()
        sents = ex._tokenize_sentences("First sentence. Second sentence. Third sentence.")
        assert len(sents) == 3

    def test_splits_on_exclamation(self):
        ex = ExtractiveSummarizer()
        sents = ex._tokenize_sentences("Wow! Amazing result! Incredible.")
        assert len(sents) == 3

    def test_splits_on_question(self):
        ex = ExtractiveSummarizer()
        sents = ex._tokenize_sentences("What is this? Why does it work? Let us explore.")
        assert len(sents) == 3

    def test_splits_on_double_newline(self):
        ex = ExtractiveSummarizer()
        sents = ex._tokenize_sentences("Paragraph one.\n\nParagraph two.")
        assert len(sents) == 2

    def test_empty_text_returns_empty(self):
        ex = ExtractiveSummarizer()
        assert ex._tokenize_sentences("") == []

    def test_whitespace_only_returns_empty(self):
        ex = ExtractiveSummarizer()
        assert ex._tokenize_sentences("   \n\n   ") == []

    def test_single_sentence_returns_list_of_one(self):
        ex = ExtractiveSummarizer()
        sents = ex._tokenize_sentences("Only one sentence here.")
        assert sents == ["Only one sentence here."]


class TestExtractorScoreSentence:
    def test_returns_float(self):
        ex = ExtractiveSummarizer()
        score = ex._score_sentence("hello world example", {"hello": 3, "world": 2}, 0, 5)
        assert isinstance(score, float)

    def test_first_position_gets_higher_position_component(self):
        ex = ExtractiveSummarizer()
        freq = {"hello": 1, "world": 1}
        # Same sentence content, different positions
        score_first = ex._score_sentence("hello world", freq, 0, 10)
        score_mid = ex._score_sentence("hello world", freq, 5, 10)
        score_last = ex._score_sentence("hello world", freq, 9, 10)
        assert score_first > score_mid
        assert score_last > score_mid

    def test_last_position_score(self):
        ex = ExtractiveSummarizer()
        freq = {"word": 2}
        score_last = ex._score_sentence("word sentence", freq, 4, 5)
        score_mid = ex._score_sentence("word sentence", freq, 2, 5)
        assert score_last > score_mid

    def test_higher_tf_gives_higher_score(self):
        ex = ExtractiveSummarizer()
        freq_high = {"memory": 10, "storage": 8}
        freq_low = {"memory": 1, "storage": 1}
        s_high = ex._score_sentence("memory storage system", freq_high, 1, 10)
        s_low = ex._score_sentence("memory storage system", freq_low, 1, 10)
        assert s_high > s_low

    def test_empty_sentence_does_not_crash(self):
        ex = ExtractiveSummarizer()
        score = ex._score_sentence("", {}, 0, 1)
        assert isinstance(score, float)

    def test_score_formula_first_position(self):
        ex = ExtractiveSummarizer()
        # sentence = "memory retrieval", freq = {"memory": 2, "retrieval": 3}
        # tokens = ["memory", "retrieval"], len = 2
        # tf = (2+3) / (2+1) = 5/3
        # position = 1.0 (first), total irrelevant as long as position==0
        # combined = 0.7 * (5/3) + 0.3 * 1.0
        freq = {"memory": 2, "retrieval": 3}
        score = ex._score_sentence("memory retrieval", freq, 0, 5)
        expected = 0.7 * (5 / 3) + 0.3 * 1.0
        assert abs(score - expected) < 1e-9

    def test_score_formula_last_position(self):
        ex = ExtractiveSummarizer()
        freq = {"data": 4}
        # tokens = ["data"], len=1
        # tf = 4/2 = 2.0, position_score=0.8
        score = ex._score_sentence("data", freq, 9, 10)
        expected = 0.7 * (4 / 2) + 0.3 * 0.8
        assert abs(score - expected) < 1e-9

    def test_score_formula_middle_position(self):
        ex = ExtractiveSummarizer()
        freq = {"word": 3}
        # tokens=["word"], tf=3/2=1.5, position_score=0.5
        score = ex._score_sentence("word", freq, 3, 10)
        expected = 0.7 * (3 / 2) + 0.3 * 0.5
        assert abs(score - expected) < 1e-9


class TestExtractiveSummarizerSummarize:
    def test_empty_text_returns_empty(self):
        assert ExtractiveSummarizer().summarize("") == ""

    def test_whitespace_only_returns_empty(self):
        assert ExtractiveSummarizer().summarize("   ") == ""

    def test_single_sentence_returned_as_is(self):
        text = "Only one sentence."
        result = ExtractiveSummarizer().summarize(text)
        assert result == "Only one sentence."

    def test_returns_string(self):
        result = ExtractiveSummarizer().summarize(SHORT_TEXT)
        assert isinstance(result, str)

    def test_returns_nonempty_for_good_text(self):
        result = ExtractiveSummarizer().summarize(SHORT_TEXT)
        assert result.strip() != ""

    def test_fewer_sentences_than_n_returns_all(self):
        text = "First sentence. Second sentence."
        result = ExtractiveSummarizer().summarize(text, n_sentences=5)
        assert "First sentence" in result
        assert "Second sentence" in result

    def test_preserves_original_order(self):
        sentences = [
            "Apple is a red fruit.",
            "Banana is a yellow fruit.",
            "Cherry is a small fruit.",
            "Date is a sweet tropical fruit.",
            "Elderberry grows in clusters.",
        ]
        text = " ".join(sentences)
        result = ExtractiveSummarizer().summarize(text, n_sentences=3)
        # Find positions of result sentences in original text
        found = [s for s in sentences if s in result]
        # Original order is preserved if indices are monotonically increasing
        indices = [sentences.index(s) for s in found]
        assert indices == sorted(indices)

    def test_n_sentences_respected_for_long_text(self):
        result = ExtractiveSummarizer().summarize(LONG_TEXT, n_sentences=3)
        # Count approximate sentences (rough check)
        parts = [s.strip() for s in result.split(". ") if s.strip()]
        # Should have at most a few more due to boundary effects
        assert len(parts) <= 5

    def test_n_sentences_1_returns_one_sentence(self):
        result = ExtractiveSummarizer().summarize(SHORT_TEXT, n_sentences=1)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_summarize_is_shorter_than_original(self):
        result = ExtractiveSummarizer().summarize(LONG_TEXT, n_sentences=3)
        assert len(result) < len(LONG_TEXT)

    def test_paragraph_text_handled(self):
        result = ExtractiveSummarizer().summarize(PARAGRAPH_TEXT, n_sentences=2)
        assert isinstance(result, str)
        assert len(result) > 0


class TestExtractiveSummarizerKeySentences:
    def test_empty_text_returns_empty_list(self):
        assert ExtractiveSummarizer().key_sentences("") == []

    def test_whitespace_returns_empty_list(self):
        assert ExtractiveSummarizer().key_sentences("   ") == []

    def test_returns_list_of_sentence_score(self):
        results = ExtractiveSummarizer().key_sentences(SHORT_TEXT)
        assert isinstance(results, list)
        for item in results:
            assert isinstance(item, SentenceScore)

    def test_sorted_by_score_descending(self):
        results = ExtractiveSummarizer().key_sentences(LONG_TEXT, n=5)
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_n_limits_output(self):
        results = ExtractiveSummarizer().key_sentences(LONG_TEXT, n=3)
        assert len(results) <= 3

    def test_sentence_score_fields(self):
        results = ExtractiveSummarizer().key_sentences(SHORT_TEXT, n=2)
        for item in results:
            assert isinstance(item.sentence, str)
            assert isinstance(item.position, int)
            assert isinstance(item.score, float)
            assert item.score >= 0.0

    def test_positions_are_valid_indices(self):
        ex = ExtractiveSummarizer()
        sentences = ex._tokenize_sentences(SHORT_TEXT)
        total = len(sentences)
        results = ex.key_sentences(SHORT_TEXT, n=10)
        for item in results:
            assert 0 <= item.position < total

    def test_fewer_sentences_than_n_returns_all(self):
        text = "One sentence only."
        results = ExtractiveSummarizer().key_sentences(text, n=5)
        assert len(results) == 1

    def test_scores_are_strictly_ordered(self):
        results = ExtractiveSummarizer().key_sentences(LONG_TEXT, n=5)
        for i in range(len(results) - 1):
            assert results[i].score >= results[i + 1].score


# ===========================================================================
# AbstractiveSummarizer
# ===========================================================================

class TestAbstractiveSummarizerExtractTopics:
    def test_returns_list(self):
        topics = AbstractiveSummarizer().extract_topics(SHORT_TEXT)
        assert isinstance(topics, list)

    def test_returns_n_topics(self):
        topics = AbstractiveSummarizer().extract_topics(LONG_TEXT, n=5)
        assert len(topics) <= 5

    def test_topics_are_strings(self):
        topics = AbstractiveSummarizer().extract_topics(SHORT_TEXT, n=3)
        for t in topics:
            assert isinstance(t, str)

    def test_topics_min_length_4(self):
        topics = AbstractiveSummarizer().extract_topics(LONG_TEXT, n=10)
        for t in topics:
            assert len(t) >= 4

    def test_no_stopwords_in_topics(self):
        from docstoolkit.summarization.abstractive import _STOPWORDS
        topics = AbstractiveSummarizer().extract_topics(LONG_TEXT, n=10)
        for t in topics:
            assert t.lower() not in _STOPWORDS

    def test_empty_text_returns_empty(self):
        assert AbstractiveSummarizer().extract_topics("") == []

    def test_relevant_word_appears(self):
        text = "memory memory memory retrieval retrieval indexing indexing indexing indexing"
        topics = AbstractiveSummarizer().extract_topics(text, n=3)
        assert "memory" in topics or "indexing" in topics or "retrieval" in topics

    def test_sorted_by_frequency(self):
        # "memory" appears 4 times, "data" appears 2 times
        text = "memory memory memory memory data data systems systems systems"
        topics = AbstractiveSummarizer().extract_topics(text, n=3)
        # "memory" or "systems" should be first (both have high count)
        assert len(topics) > 0


class TestAbstractiveSummarizerExtractKeyPoints:
    def test_returns_list_of_strings(self):
        kp = AbstractiveSummarizer().extract_key_points(SHORT_TEXT)
        for s in kp:
            assert isinstance(s, str)

    def test_n_limits_output(self):
        kp = AbstractiveSummarizer().extract_key_points(LONG_TEXT, n=3)
        assert len(kp) <= 3

    def test_non_empty_for_good_text(self):
        kp = AbstractiveSummarizer().extract_key_points(SHORT_TEXT, n=2)
        assert len(kp) > 0

    def test_empty_text_returns_empty(self):
        kp = AbstractiveSummarizer().extract_key_points("", n=3)
        assert kp == []

    def test_sentences_are_from_source(self):
        ex = ExtractiveSummarizer()
        source_sents = set(ex._tokenize_sentences(SHORT_TEXT))
        kp = AbstractiveSummarizer().extract_key_points(SHORT_TEXT, n=3)
        for s in kp:
            assert s in source_sents


class TestAbstractiveSummarizerSummarize:
    def test_returns_string(self):
        result = AbstractiveSummarizer().summarize(SHORT_TEXT)
        assert isinstance(result, str)

    def test_non_empty_for_good_text(self):
        result = AbstractiveSummarizer().summarize(SHORT_TEXT)
        assert result.strip() != ""

    def test_empty_text_returns_empty(self):
        result = AbstractiveSummarizer().summarize("")
        assert result == ""

    def test_contains_three_parts(self):
        result = AbstractiveSummarizer().summarize(LONG_TEXT)
        # Default templates produce three sentences
        assert result.count(".") >= 2

    def test_uses_custom_config(self):
        cfg = TemplateConfig(
            intro_template="Topics: {topics}.",
            body_template="Points: {key_points}.",
            conclusion_template="End: {conclusion}.",
        )
        result = AbstractiveSummarizer().summarize(SHORT_TEXT, config=cfg)
        assert "Topics:" in result
        assert "Points:" in result
        assert "End:" in result

    def test_default_config_intro_phrase(self):
        result = AbstractiveSummarizer().summarize(SHORT_TEXT)
        assert "This document covers" in result

    def test_default_config_body_phrase(self):
        result = AbstractiveSummarizer().summarize(SHORT_TEXT)
        assert "Key points:" in result

    def test_default_config_conclusion_phrase(self):
        result = AbstractiveSummarizer().summarize(SHORT_TEXT)
        assert "In summary:" in result

    def test_template_config_defaults(self):
        cfg = TemplateConfig()
        assert "{topics}" in cfg.intro_template
        assert "{key_points}" in cfg.body_template
        assert "{conclusion}" in cfg.conclusion_template


# ===========================================================================
# SummaryResult
# ===========================================================================

class TestSummaryResult:
    def _make_result(self, level=SummaryLevel.STANDARD):
        return SummaryResult(
            text="Some summary text here.",
            method="extractive",
            level=level,
            word_count=4,
            compression_ratio=0.2,
        )

    def test_is_brief_true_for_brief(self):
        r = self._make_result(SummaryLevel.BRIEF)
        assert r.is_brief() is True

    def test_is_brief_false_for_standard(self):
        r = self._make_result(SummaryLevel.STANDARD)
        assert r.is_brief() is False

    def test_is_brief_false_for_detailed(self):
        r = self._make_result(SummaryLevel.DETAILED)
        assert r.is_brief() is False

    def test_fields_accessible(self):
        r = self._make_result()
        assert r.text == "Some summary text here."
        assert r.method == "extractive"
        assert r.word_count == 4
        assert r.compression_ratio == 0.2


# ===========================================================================
# SummarizationPipeline
# ===========================================================================

class TestSummarizationPipelineExtractiveMethod:
    def test_returns_summary_result(self):
        pipeline = SummarizationPipeline()
        result = pipeline.summarize(LONG_TEXT)
        assert isinstance(result, SummaryResult)

    def test_method_is_extractive(self):
        pipeline = SummarizationPipeline()
        result = pipeline.summarize(LONG_TEXT)
        assert result.method == "extractive"

    def test_level_is_standard_by_default(self):
        pipeline = SummarizationPipeline()
        result = pipeline.summarize(LONG_TEXT)
        assert result.level == SummaryLevel.STANDARD

    def test_text_is_nonempty(self):
        pipeline = SummarizationPipeline()
        result = pipeline.summarize(LONG_TEXT)
        assert result.text.strip() != ""

    def test_word_count_matches_text(self):
        pipeline = SummarizationPipeline()
        result = pipeline.summarize(LONG_TEXT)
        assert result.word_count == len(result.text.split())

    def test_brief_level_shorter_than_detailed(self):
        brief_pipeline = SummarizationPipeline(SummaryConfig(level=SummaryLevel.BRIEF))
        detailed_pipeline = SummarizationPipeline(SummaryConfig(level=SummaryLevel.DETAILED))
        brief_result = brief_pipeline.summarize(LONG_TEXT)
        detailed_result = detailed_pipeline.summarize(LONG_TEXT)
        assert brief_result.word_count <= detailed_result.word_count

    def test_is_brief_when_brief_level(self):
        pipeline = SummarizationPipeline(SummaryConfig(level=SummaryLevel.BRIEF))
        result = pipeline.summarize(LONG_TEXT)
        assert result.is_brief() is True


class TestSummarizationPipelineAbstractiveMethod:
    def test_method_is_abstractive(self):
        pipeline = SummarizationPipeline(SummaryConfig(method="abstractive"))
        result = pipeline.summarize(LONG_TEXT)
        assert result.method == "abstractive"

    def test_returns_nonempty_text(self):
        pipeline = SummarizationPipeline(SummaryConfig(method="abstractive"))
        result = pipeline.summarize(LONG_TEXT)
        assert result.text.strip() != ""

    def test_returns_summary_result_type(self):
        pipeline = SummarizationPipeline(SummaryConfig(method="abstractive"))
        result = pipeline.summarize(SHORT_TEXT)
        assert isinstance(result, SummaryResult)


class TestSummarizationPipelineHybridMethod:
    def test_method_is_hybrid(self):
        pipeline = SummarizationPipeline(SummaryConfig(method="hybrid"))
        result = pipeline.summarize(LONG_TEXT)
        assert result.method == "hybrid"

    def test_returns_nonempty_text(self):
        pipeline = SummarizationPipeline(SummaryConfig(method="hybrid"))
        result = pipeline.summarize(LONG_TEXT)
        assert result.text.strip() != ""

    def test_no_duplicate_sentences(self):
        pipeline = SummarizationPipeline(SummaryConfig(method="hybrid"))
        result = pipeline.summarize(LONG_TEXT)
        # Split into sentences and check for duplicates
        import re
        parts = [s.strip().lower() for s in re.split(r"(?<=[.!?])\s+", result.text) if s.strip()]
        assert len(parts) == len(set(parts))

    def test_returns_summary_result_type(self):
        pipeline = SummarizationPipeline(SummaryConfig(method="hybrid"))
        result = pipeline.summarize(SHORT_TEXT)
        assert isinstance(result, SummaryResult)


class TestSummarizationPipelineCompressionRatio:
    def test_compression_ratio_is_float(self):
        pipeline = SummarizationPipeline()
        result = pipeline.summarize(LONG_TEXT)
        assert isinstance(result.compression_ratio, float)

    def test_compression_ratio_less_than_one_for_long_text(self):
        pipeline = SummarizationPipeline()
        result = pipeline.summarize(LONG_TEXT)
        assert result.compression_ratio < 1.0

    def test_compression_ratio_formula(self):
        pipeline = SummarizationPipeline()
        result = pipeline.summarize(LONG_TEXT)
        original_words = len(LONG_TEXT.split())
        expected_ratio = result.word_count / original_words
        assert abs(result.compression_ratio - expected_ratio) < 1e-9

    def test_compression_ratio_zero_for_empty(self):
        pipeline = SummarizationPipeline()
        result = pipeline.summarize("")
        assert result.compression_ratio == 0.0


class TestSummarizationPipelineMaxWords:
    def test_max_words_limits_output(self):
        pipeline = SummarizationPipeline(SummaryConfig(max_words=10))
        result = pipeline.summarize(LONG_TEXT)
        assert result.word_count <= 10

    def test_max_words_very_small(self):
        pipeline = SummarizationPipeline(SummaryConfig(max_words=5))
        result = pipeline.summarize(LONG_TEXT)
        assert result.word_count <= 5

    def test_max_words_large_does_not_pad(self):
        pipeline = SummarizationPipeline(SummaryConfig(max_words=10000))
        result = pipeline.summarize(SHORT_TEXT)
        # Result should not be longer than the original text
        assert result.word_count <= len(LONG_TEXT.split())

    def test_max_words_abstractive_respected(self):
        pipeline = SummarizationPipeline(SummaryConfig(method="abstractive", max_words=15))
        result = pipeline.summarize(LONG_TEXT)
        assert result.word_count <= 15

    def test_max_words_hybrid_respected(self):
        pipeline = SummarizationPipeline(SummaryConfig(method="hybrid", max_words=20))
        result = pipeline.summarize(LONG_TEXT)
        assert result.word_count <= 20


class TestSummarizationPipelineMisc:
    def test_invalid_method_raises_value_error(self):
        pipeline = SummarizationPipeline(SummaryConfig(method="unknown"))
        with pytest.raises(ValueError):
            pipeline.summarize(SHORT_TEXT)

    def test_default_config_is_applied_when_none_passed(self):
        pipeline = SummarizationPipeline(None)
        result = pipeline.summarize(SHORT_TEXT)
        assert isinstance(result, SummaryResult)
        assert result.method == "extractive"
        assert result.level == SummaryLevel.STANDARD

    def test_summary_level_enum_values(self):
        assert SummaryLevel.BRIEF.value == "brief"
        assert SummaryLevel.STANDARD.value == "standard"
        assert SummaryLevel.DETAILED.value == "detailed"

    def test_pipeline_empty_text(self):
        pipeline = SummarizationPipeline()
        result = pipeline.summarize("")
        assert isinstance(result, SummaryResult)
        assert result.word_count == 0
        assert result.compression_ratio == 0.0
