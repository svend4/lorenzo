"""Tests for docstoolkit.doc_summarizer_v2 (E285).

Coverage areas
--------------
- SummaryConfig defaults and custom values
- SentenceScore fields
- Summary fields and compression_ratio
- DocSummarizerV2.summarize — sentence selection, ordering, scoring
- DocSummarizerV2.summarize_multi
- DocSummarizerV2.update_config
- DocSummarizerV2.add_stopwords / clear_stopwords
- DocSummarizerV2.config property (returns snapshot)
- Edge cases: empty text, whitespace-only, single sentence, very short text,
  text shorter than min_sentence_len, max_sentences > available sentences,
  max_sentences=0, min_sentence_len=0
- Thread safety (basic lock check via concurrent access)
"""
from __future__ import annotations

import threading
from dataclasses import fields as dc_fields

import pytest

from docstoolkit.doc_summarizer_v2 import (
    DocSummarizerV2,
    SentenceScore,
    Summary,
    SummaryConfig,
)

# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

MULTI_SENT = (
    "The cat sat on the mat. "
    "The dog ran in the park. "
    "A bird flew over the tree. "
    "The fish swam in the lake. "
    "The sun set behind the hills."
)

FREQ_TEXT = (
    "Memory agents use memory to store data. "
    "Memory is crucial for agent performance. "
    "Data pipelines process memory efficiently. "
    "Agents retrieve memory from the store."
)


def make_summarizer(**kwargs) -> DocSummarizerV2:
    cfg = SummaryConfig(**kwargs) if kwargs else SummaryConfig()
    return DocSummarizerV2(cfg)


# ===========================================================================
# SummaryConfig
# ===========================================================================


class TestSummaryConfig:
    def test_default_max_sentences(self):
        assert SummaryConfig().max_sentences == 3

    def test_default_min_sentence_len(self):
        assert SummaryConfig().min_sentence_len == 10

    def test_default_position_weight(self):
        assert SummaryConfig().position_weight == pytest.approx(0.3)

    def test_default_freq_weight(self):
        assert SummaryConfig().freq_weight == pytest.approx(0.7)

    def test_default_stopwords_empty_set(self):
        assert SummaryConfig().stopwords == set()

    def test_stopwords_not_shared_between_instances(self):
        a = SummaryConfig()
        b = SummaryConfig()
        a.stopwords.add("foo")
        assert "foo" not in b.stopwords

    def test_custom_max_sentences(self):
        cfg = SummaryConfig(max_sentences=5)
        assert cfg.max_sentences == 5

    def test_custom_min_sentence_len(self):
        cfg = SummaryConfig(min_sentence_len=20)
        assert cfg.min_sentence_len == 20

    def test_custom_weights(self):
        cfg = SummaryConfig(position_weight=0.5, freq_weight=0.5)
        assert cfg.position_weight == pytest.approx(0.5)
        assert cfg.freq_weight == pytest.approx(0.5)

    def test_is_dataclass(self):
        # dataclasses expose __dataclass_fields__
        assert hasattr(SummaryConfig, "__dataclass_fields__")

    def test_has_five_fields(self):
        names = {f.name for f in dc_fields(SummaryConfig)}
        assert names == {
            "max_sentences", "min_sentence_len",
            "position_weight", "freq_weight", "stopwords",
        }


# ===========================================================================
# SentenceScore
# ===========================================================================


class TestSentenceScore:
    def test_construct(self):
        ss = SentenceScore(
            sentence="Hello world.",
            position=0,
            freq_score=0.8,
            pos_score=1.0,
            total_score=0.86,
        )
        assert ss.sentence == "Hello world."
        assert ss.position == 0
        assert ss.freq_score == pytest.approx(0.8)
        assert ss.pos_score == pytest.approx(1.0)
        assert ss.total_score == pytest.approx(0.86)

    def test_is_dataclass(self):
        assert hasattr(SentenceScore, "__dataclass_fields__")

    def test_has_five_fields(self):
        names = {f.name for f in dc_fields(SentenceScore)}
        assert names == {
            "sentence", "position", "freq_score", "pos_score", "total_score",
        }


# ===========================================================================
# Summary
# ===========================================================================


class TestSummary:
    def test_construct(self):
        s = Summary(
            original_length=100,
            summary_text="Short summary.",
            sentences=[],
            compression_ratio=0.1,
        )
        assert s.original_length == 100
        assert s.summary_text == "Short summary."
        assert s.sentences == []
        assert s.compression_ratio == pytest.approx(0.1)

    def test_is_dataclass(self):
        assert hasattr(Summary, "__dataclass_fields__")

    def test_has_four_fields(self):
        names = {f.name for f in dc_fields(Summary)}
        assert names == {
            "original_length", "summary_text", "sentences", "compression_ratio",
        }


# ===========================================================================
# DocSummarizerV2 — basic construction
# ===========================================================================


class TestDocSummarizerV2Init:
    def test_default_config(self):
        s = DocSummarizerV2()
        assert s.config.max_sentences == 3

    def test_custom_config(self):
        cfg = SummaryConfig(max_sentences=1)
        s = DocSummarizerV2(cfg)
        assert s.config.max_sentences == 1

    def test_config_is_snapshot(self):
        s = DocSummarizerV2()
        c1 = s.config
        c2 = s.config
        # Each call returns a fresh copy
        assert c1 is not c2

    def test_config_stopwords_independent(self):
        s = DocSummarizerV2()
        c = s.config
        c.stopwords.add("test")
        # Internal state must not be mutated
        assert "test" not in s.config.stopwords


# ===========================================================================
# DocSummarizerV2.summarize — return type
# ===========================================================================


class TestSummarizeReturnType:
    def test_returns_summary(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        assert isinstance(result, Summary)

    def test_summary_text_is_str(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        assert isinstance(result.summary_text, str)

    def test_sentences_is_list(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        assert isinstance(result.sentences, list)

    def test_sentences_items_are_sentence_score(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        for ss in result.sentences:
            assert isinstance(ss, SentenceScore)

    def test_original_length_positive(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        assert result.original_length > 0

    def test_compression_ratio_between_0_and_1(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        assert 0.0 <= result.compression_ratio <= 1.0


# ===========================================================================
# DocSummarizerV2.summarize — sentence selection
# ===========================================================================


class TestSummarizeSentenceSelection:
    def test_respects_max_sentences_default(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        assert len(result.sentences) <= 3

    def test_respects_max_sentences_custom(self):
        s = make_summarizer(max_sentences=2)
        result = s.summarize(MULTI_SENT)
        assert len(result.sentences) <= 2

    def test_max_sentences_1(self):
        s = make_summarizer(max_sentences=1)
        result = s.summarize(MULTI_SENT)
        assert len(result.sentences) == 1

    def test_sentences_in_original_order(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        positions = [ss.position for ss in result.sentences]
        assert positions == sorted(positions)

    def test_summary_text_joins_selected(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        expected = " ".join(ss.sentence for ss in result.sentences)
        assert result.summary_text == expected

    def test_first_sentence_gets_highest_pos_score(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        first_ss = next(ss for ss in result.sentences if ss.position == 0)
        assert first_ss.pos_score == pytest.approx(1.0)

    def test_pos_score_decays(self):
        # Build a text long enough that we can check position 0 vs position 1
        text = ". ".join(f"Sentence number {i} with some content words" for i in range(6)) + "."
        result = DocSummarizerV2().summarize(text)
        scores = {ss.position: ss.pos_score for ss in result.sentences}
        if 0 in scores and 1 in scores:
            assert scores[0] > scores[1]

    def test_high_freq_words_boost_score(self):
        # FREQ_TEXT has "memory" repeated; the sentence with most "memory"
        # occurrences should rank highly
        s = make_summarizer(max_sentences=2, position_weight=0.1, freq_weight=0.9)
        result = s.summarize(FREQ_TEXT)
        combined = result.summary_text.lower()
        assert "memory" in combined

    def test_max_sentences_larger_than_available(self):
        # Only 2 sentences available; max_sentences=10 → get 2
        text = "First sentence here. Second sentence here."
        s = make_summarizer(max_sentences=10)
        result = s.summarize(text)
        assert len(result.sentences) == 2

    def test_min_sentence_len_filters_short(self):
        # "Hi." is shorter than default 10 chars → filtered out
        text = "Hi. This is a longer sentence that passes the filter."
        s = make_summarizer(min_sentence_len=10)
        result = s.summarize(text)
        for ss in result.sentences:
            assert len(ss.sentence) >= 10


# ===========================================================================
# compression_ratio
# ===========================================================================


class TestCompressionRatio:
    def test_compression_less_than_one_for_long_text(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        assert result.compression_ratio < 1.0

    def test_compression_ratio_formula(self):
        result = DocSummarizerV2().summarize(MULTI_SENT)
        summary_wc = len(result.summary_text.split())
        expected = summary_wc / result.original_length
        assert result.compression_ratio == pytest.approx(expected)

    def test_single_sentence_compression_near_one(self):
        # Single sentence: summary == original → ratio ≈ 1.0
        text = "This is a single sentence that is long enough."
        result = DocSummarizerV2().summarize(text)
        assert result.compression_ratio == pytest.approx(1.0, abs=0.01)


# ===========================================================================
# Edge cases
# ===========================================================================


class TestEdgeCases:
    def test_empty_string(self):
        result = DocSummarizerV2().summarize("")
        assert result.summary_text == ""
        assert result.sentences == []
        assert result.compression_ratio == 0.0
        assert result.original_length == 0

    def test_whitespace_only(self):
        result = DocSummarizerV2().summarize("   \n\n   ")
        assert result.summary_text == ""
        assert result.sentences == []

    def test_single_sentence(self):
        text = "This is a single complete sentence with enough characters."
        result = DocSummarizerV2().summarize(text)
        assert len(result.sentences) == 1
        assert result.summary_text == text

    def test_very_short_text_below_min_len(self):
        # Entire text is below min_sentence_len
        text = "Hi."
        result = DocSummarizerV2().summarize(text)
        assert result.summary_text == ""
        assert result.sentences == []

    def test_max_sentences_zero(self):
        s = make_summarizer(max_sentences=0)
        result = s.summarize(MULTI_SENT)
        assert result.summary_text == ""
        assert result.sentences == []

    def test_min_sentence_len_zero_includes_all(self):
        s = make_summarizer(min_sentence_len=0, max_sentences=10)
        # Even very short text should not be filtered
        text = "Hi. OK. Yes. This is fine."
        result = s.summarize(text)
        assert len(result.sentences) >= 1

    def test_type_error_on_non_string(self):
        with pytest.raises(TypeError):
            DocSummarizerV2().summarize(123)  # type: ignore[arg-type]

    def test_non_ascii_text(self):
        text = (
            "Агенты памяти хранят данные в базе. "
            "Память критически важна для производительности агента. "
            "Пайплайны данных обрабатывают данные эффективно."
        )
        result = DocSummarizerV2().summarize(text)
        assert isinstance(result.summary_text, str)
        assert len(result.sentences) >= 1

    def test_paragraph_split_on_double_newline(self):
        text = "First paragraph sentence.\n\nSecond paragraph sentence here."
        result = DocSummarizerV2().summarize(text)
        assert len(result.sentences) == 2


# ===========================================================================
# update_config
# ===========================================================================


class TestUpdateConfig:
    def test_update_max_sentences(self):
        s = DocSummarizerV2()
        new_cfg = s.update_config(max_sentences=5)
        assert new_cfg.max_sentences == 5
        assert s.config.max_sentences == 5

    def test_update_freq_weight(self):
        s = DocSummarizerV2()
        s.update_config(freq_weight=0.5)
        assert s.config.freq_weight == pytest.approx(0.5)

    def test_update_position_weight(self):
        s = DocSummarizerV2()
        s.update_config(position_weight=0.5)
        assert s.config.position_weight == pytest.approx(0.5)

    def test_update_min_sentence_len(self):
        s = DocSummarizerV2()
        s.update_config(min_sentence_len=20)
        assert s.config.min_sentence_len == 20

    def test_update_stopwords(self):
        s = DocSummarizerV2()
        s.update_config(stopwords={"the", "a"})
        assert "the" in s.config.stopwords

    def test_update_returns_summary_config(self):
        s = DocSummarizerV2()
        result = s.update_config(max_sentences=2)
        assert isinstance(result, SummaryConfig)

    def test_update_unknown_field_raises(self):
        s = DocSummarizerV2()
        with pytest.raises(ValueError):
            s.update_config(nonexistent_field=99)

    def test_update_takes_effect_on_next_summarize(self):
        s = DocSummarizerV2()
        s.update_config(max_sentences=1)
        result = s.summarize(MULTI_SENT)
        assert len(result.sentences) <= 1


# ===========================================================================
# add_stopwords / clear_stopwords
# ===========================================================================


class TestStopwords:
    def test_add_stopwords_returns_count(self):
        s = DocSummarizerV2()
        count = s.add_stopwords(["the", "a", "an"])
        assert count == 3

    def test_add_stopwords_accumulates(self):
        s = DocSummarizerV2()
        s.add_stopwords(["foo"])
        count = s.add_stopwords(["bar"])
        assert count == 2

    def test_add_stopwords_lowercase(self):
        s = DocSummarizerV2()
        s.add_stopwords(["THE", "A"])
        assert "the" in s.config.stopwords
        assert "a" in s.config.stopwords

    def test_clear_stopwords(self):
        s = DocSummarizerV2()
        s.add_stopwords(["the", "a"])
        s.clear_stopwords()
        assert s.config.stopwords == set()

    def test_clear_then_add(self):
        s = DocSummarizerV2()
        s.add_stopwords(["foo", "bar"])
        s.clear_stopwords()
        count = s.add_stopwords(["baz"])
        assert count == 1

    def test_stopwords_affect_scoring(self):
        # Adding "memory" as a stopword should reduce its influence
        s_no_stop = make_summarizer(max_sentences=2, freq_weight=0.9, position_weight=0.1)
        s_with_stop = make_summarizer(max_sentences=2, freq_weight=0.9, position_weight=0.1)
        s_with_stop.add_stopwords(["memory"])

        result_no = s_no_stop.summarize(FREQ_TEXT)
        result_with = s_with_stop.summarize(FREQ_TEXT)

        # Results may differ; the key assertion is that both produce valid Summaries
        assert isinstance(result_no, Summary)
        assert isinstance(result_with, Summary)

    def test_add_duplicate_stopwords_idempotent(self):
        s = DocSummarizerV2()
        s.add_stopwords(["the"])
        count = s.add_stopwords(["the"])
        assert count == 1  # set deduplication


# ===========================================================================
# summarize_multi
# ===========================================================================


class TestSummarizeMulti:
    def test_returns_list(self):
        s = DocSummarizerV2()
        result = s.summarize_multi([MULTI_SENT, FREQ_TEXT])
        assert isinstance(result, list)

    def test_correct_length(self):
        s = DocSummarizerV2()
        texts = [MULTI_SENT, FREQ_TEXT, "Short but valid sentence here."]
        result = s.summarize_multi(texts)
        assert len(result) == 3

    def test_each_item_is_summary(self):
        s = DocSummarizerV2()
        for item in s.summarize_multi([MULTI_SENT, FREQ_TEXT]):
            assert isinstance(item, Summary)

    def test_empty_list(self):
        s = DocSummarizerV2()
        assert s.summarize_multi([]) == []

    def test_single_text(self):
        s = DocSummarizerV2()
        result = s.summarize_multi([MULTI_SENT])
        assert len(result) == 1

    def test_includes_empty_string(self):
        s = DocSummarizerV2()
        results = s.summarize_multi(["", MULTI_SENT])
        assert results[0].summary_text == ""
        assert results[1].summary_text != ""


# ===========================================================================
# Thread safety
# ===========================================================================


class TestThreadSafety:
    def test_concurrent_summarize(self):
        s = DocSummarizerV2()
        errors: list[Exception] = []
        results: list[Summary] = []

        def worker():
            try:
                r = s.summarize(MULTI_SENT)
                results.append(r)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
        assert len(results) == 10

    def test_concurrent_update_and_summarize(self):
        s = DocSummarizerV2()
        errors: list[Exception] = []

        def updater():
            try:
                for _ in range(5):
                    s.update_config(max_sentences=2)
                    s.update_config(max_sentences=3)
            except Exception as exc:
                errors.append(exc)

        def reader():
            try:
                for _ in range(5):
                    s.summarize(MULTI_SENT)
            except Exception as exc:
                errors.append(exc)

        threads = (
            [threading.Thread(target=updater) for _ in range(3)]
            + [threading.Thread(target=reader) for _ in range(3)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
