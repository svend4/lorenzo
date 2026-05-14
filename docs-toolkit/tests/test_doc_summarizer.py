"""Tests for E152 docstoolkit.doc_summarizer."""
from __future__ import annotations

import pytest

from docstoolkit.doc_summarizer import (
    DocSummarizer,
    SentenceScore,
    Summary,
    SummaryMethod,
)


# --------------------------------------------------------------------------
# Fixtures
# --------------------------------------------------------------------------


@pytest.fixture
def summarizer() -> DocSummarizer:
    return DocSummarizer()


@pytest.fixture
def sample_text() -> str:
    return (
        "Cats are wonderful pets. "
        "Cats love to sleep all day. "
        "Dogs are loyal companions. "
        "Birds can sing beautifully. "
        "Fish are quiet creatures. "
        "Cats and dogs can live together. "
        "Pets bring joy to families."
    )


@pytest.fixture
def short_text() -> str:
    return "Hello world. This is a test. Bye."


# --------------------------------------------------------------------------
# TestSummaryMethod
# --------------------------------------------------------------------------


class TestSummaryMethod:
    def test_has_first_n(self):
        assert SummaryMethod.FIRST_N.value == "first_n"

    def test_has_last_n(self):
        assert SummaryMethod.LAST_N.value == "last_n"

    def test_has_lead_3(self):
        assert SummaryMethod.LEAD_3.value == "lead_3"

    def test_has_keyword_density(self):
        assert SummaryMethod.KEYWORD_DENSITY.value == "keyword_density"

    def test_has_position_weight(self):
        assert SummaryMethod.POSITION_WEIGHT.value == "position_weight"

    def test_has_textrank(self):
        assert SummaryMethod.TEXTRANK.value == "textrank"

    def test_methods_are_distinct(self):
        values = {m.value for m in SummaryMethod}
        assert len(values) == 6


# --------------------------------------------------------------------------
# TestSentenceScore
# --------------------------------------------------------------------------


class TestSentenceScore:
    def test_construct(self):
        s = SentenceScore(sentence="Hi.", index=0, score=1.5)
        assert s.sentence == "Hi."
        assert s.index == 0
        assert s.score == 1.5

    def test_frozen(self):
        s = SentenceScore(sentence="Hi.", index=0, score=1.5)
        with pytest.raises(Exception):  # FrozenInstanceError
            s.score = 2.0  # type: ignore[misc]

    def test_equality(self):
        a = SentenceScore("x", 1, 2.0)
        b = SentenceScore("x", 1, 2.0)
        assert a == b


# --------------------------------------------------------------------------
# TestSummary
# --------------------------------------------------------------------------


class TestSummary:
    def test_compression_ratio_basic(self):
        s = Summary(
            text="abc", sentences=["abc"], method=SummaryMethod.LEAD_3,
            original_length=10, summary_length=3,
        )
        assert s.compression_ratio == pytest.approx(0.3)

    def test_compression_ratio_empty_original(self):
        s = Summary(text="", sentences=[], method=SummaryMethod.LEAD_3)
        assert s.compression_ratio == 0.0

    def test_compression_ratio_full(self):
        s = Summary(
            text="abc", sentences=["abc"], method=SummaryMethod.LEAD_3,
            original_length=3, summary_length=3,
        )
        assert s.compression_ratio == pytest.approx(1.0)

    def test_default_sentences_empty(self):
        s = Summary(text="", method=SummaryMethod.LEAD_3)
        assert s.sentences == []


# --------------------------------------------------------------------------
# TestSummarizeFirstN
# --------------------------------------------------------------------------


class TestSummarizeFirstN:
    def test_picks_first_n(self, summarizer, sample_text):
        out = summarizer.summarize_first_n(sample_text, n=2)
        assert out.sentences[0].startswith("Cats are wonderful")
        assert out.sentences[1].startswith("Cats love to sleep")
        assert len(out.sentences) == 2

    def test_method_set(self, summarizer, sample_text):
        out = summarizer.summarize_first_n(sample_text, n=1)
        assert out.method == SummaryMethod.FIRST_N

    def test_n_larger_than_text(self, summarizer, short_text):
        out = summarizer.summarize_first_n(short_text, n=100)
        assert len(out.sentences) == 3

    def test_n_zero(self, summarizer, sample_text):
        out = summarizer.summarize_first_n(sample_text, n=0)
        assert out.sentences == []
        assert out.text == ""


# --------------------------------------------------------------------------
# TestSummarizeLastN
# --------------------------------------------------------------------------


class TestSummarizeLastN:
    def test_picks_last_n(self, summarizer, sample_text):
        out = summarizer.summarize_last_n(sample_text, n=2)
        assert out.sentences[-1].startswith("Pets bring joy")
        assert len(out.sentences) == 2

    def test_method_set(self, summarizer, sample_text):
        out = summarizer.summarize_last_n(sample_text, n=1)
        assert out.method == SummaryMethod.LAST_N

    def test_preserves_order(self, summarizer, sample_text):
        out = summarizer.summarize_last_n(sample_text, n=3)
        assert out.sentences[0].startswith("Fish are quiet")
        assert out.sentences[1].startswith("Cats and dogs")
        assert out.sentences[2].startswith("Pets bring joy")

    def test_n_zero(self, summarizer, sample_text):
        out = summarizer.summarize_last_n(sample_text, n=0)
        assert out.sentences == []


# --------------------------------------------------------------------------
# TestSummarizeLead3
# --------------------------------------------------------------------------


class TestSummarizeLead3:
    def test_takes_three(self, summarizer, sample_text):
        out = summarizer.summarize_lead_3(sample_text)
        assert len(out.sentences) == 3

    def test_method_set(self, summarizer, sample_text):
        out = summarizer.summarize_lead_3(sample_text)
        assert out.method == SummaryMethod.LEAD_3

    def test_fewer_than_three(self, summarizer):
        out = summarizer.summarize_lead_3("One. Two.")
        assert len(out.sentences) == 2

    def test_order_preserved(self, summarizer, sample_text):
        out = summarizer.summarize_lead_3(sample_text)
        assert out.sentences[0].startswith("Cats are wonderful")
        assert out.sentences[2].startswith("Dogs are loyal")


# --------------------------------------------------------------------------
# TestSummarizeKeywordDensity
# --------------------------------------------------------------------------


class TestSummarizeKeywordDensity:
    def test_returns_summary(self, summarizer, sample_text):
        out = summarizer.summarize_keyword_density(sample_text, max_sentences=2)
        assert isinstance(out, Summary)
        assert out.method == SummaryMethod.KEYWORD_DENSITY

    def test_picks_at_most_max(self, summarizer, sample_text):
        out = summarizer.summarize_keyword_density(sample_text, max_sentences=3)
        assert len(out.sentences) <= 3

    def test_prefers_keyword_rich(self, summarizer):
        # 'cats' is the dominant keyword.
        text = (
            "Cats love cats. "
            "The weather is nice. "
            "Cats cats cats. "
            "Random unrelated thought."
        )
        out = summarizer.summarize_keyword_density(text, max_sentences=2)
        joined = " ".join(out.sentences).lower()
        assert "cats" in joined

    def test_preserves_original_order(self, summarizer, sample_text):
        out = summarizer.summarize_keyword_density(sample_text, max_sentences=3)
        # Indices must be strictly increasing in original sentence list.
        all_s = sample_text.split(". ")
        # Approximate: find indices of picked sentences.
        idxs = []
        for s in out.sentences:
            for i, a in enumerate(all_s):
                if a.strip().rstrip(".") in s:
                    idxs.append(i)
                    break
        assert idxs == sorted(idxs)


# --------------------------------------------------------------------------
# TestSummarizePositionWeight
# --------------------------------------------------------------------------


class TestSummarizePositionWeight:
    def test_returns_summary(self, summarizer, sample_text):
        out = summarizer.summarize_position_weight(sample_text, max_sentences=3)
        assert isinstance(out, Summary)
        assert out.method == SummaryMethod.POSITION_WEIGHT

    def test_first_and_last_picked(self, summarizer, sample_text):
        out = summarizer.summarize_position_weight(sample_text, max_sentences=2)
        # First and last sentences should rank highest.
        first = "Cats are wonderful pets."
        last = "Pets bring joy to families."
        assert first in out.sentences or any(first[:10] in s for s in out.sentences)
        assert last in out.sentences or any(last[:10] in s for s in out.sentences)

    def test_max_zero(self, summarizer, sample_text):
        out = summarizer.summarize_position_weight(sample_text, max_sentences=0)
        assert out.sentences == []

    def test_scores_formula(self, summarizer):
        text = "A. B. C. D."
        scores = summarizer.score_sentences(text, SummaryMethod.POSITION_WEIGHT)
        # total=4 -> score(0)=1/1+1/4=1.25; score(3)=1/4+1/1=1.25; both top.
        s0 = next(s for s in scores if s.index == 0)
        s3 = next(s for s in scores if s.index == 3)
        assert s0.score == pytest.approx(1.25)
        assert s3.score == pytest.approx(1.25)


# --------------------------------------------------------------------------
# TestSummarizeTextrank
# --------------------------------------------------------------------------


class TestSummarizeTextrank:
    def test_returns_summary(self, summarizer, sample_text):
        out = summarizer.summarize_textrank(sample_text, max_sentences=3)
        assert isinstance(out, Summary)
        assert out.method == SummaryMethod.TEXTRANK

    def test_count(self, summarizer, sample_text):
        out = summarizer.summarize_textrank(sample_text, max_sentences=2)
        assert len(out.sentences) == 2

    def test_single_sentence(self, summarizer):
        out = summarizer.summarize_textrank("Only one sentence here.", max_sentences=3)
        assert len(out.sentences) == 1

    def test_picks_central_sentence(self, summarizer):
        # A sentence sharing words with many others should rank high.
        text = (
            "Apples are red. "
            "Bananas are yellow. "
            "Apples bananas oranges grapes are fruits. "
            "Oranges are orange. "
            "Grapes are purple."
        )
        out = summarizer.summarize_textrank(text, max_sentences=1)
        assert "fruits" in out.sentences[0].lower()


# --------------------------------------------------------------------------
# TestSummarizeDispatch
# --------------------------------------------------------------------------


class TestSummarizeDispatch:
    @pytest.mark.parametrize(
        "method",
        [
            SummaryMethod.FIRST_N,
            SummaryMethod.LAST_N,
            SummaryMethod.LEAD_3,
            SummaryMethod.KEYWORD_DENSITY,
            SummaryMethod.POSITION_WEIGHT,
            SummaryMethod.TEXTRANK,
        ],
    )
    def test_dispatch_all_methods(self, summarizer, sample_text, method):
        out = summarizer.summarize(sample_text, method=method, max_sentences=2)
        assert isinstance(out, Summary)
        assert out.method == method

    def test_default_is_lead_3(self, summarizer, sample_text):
        out = summarizer.summarize(sample_text)
        assert out.method == SummaryMethod.LEAD_3

    def test_invalid_method_raises(self, summarizer, sample_text):
        with pytest.raises(ValueError):
            summarizer.summarize(sample_text, method="bogus")  # type: ignore[arg-type]


# --------------------------------------------------------------------------
# TestScoreSentences
# --------------------------------------------------------------------------


class TestScoreSentences:
    def test_returns_list(self, summarizer, sample_text):
        scores = summarizer.score_sentences(sample_text, SummaryMethod.LEAD_3)
        assert isinstance(scores, list)
        assert all(isinstance(s, SentenceScore) for s in scores)

    def test_indices_match_position(self, summarizer, sample_text):
        scores = summarizer.score_sentences(sample_text, SummaryMethod.TEXTRANK)
        for i, s in enumerate(scores):
            assert s.index == i

    def test_lead_3_scoring(self, summarizer, sample_text):
        scores = summarizer.score_sentences(sample_text, SummaryMethod.LEAD_3)
        # First three score 1.0, rest 0.0.
        assert scores[0].score == 1.0
        assert scores[1].score == 1.0
        assert scores[2].score == 1.0
        assert scores[3].score == 0.0

    def test_keyword_density_returns_scores(self, summarizer, sample_text):
        scores = summarizer.score_sentences(sample_text, SummaryMethod.KEYWORD_DENSITY)
        assert len(scores) > 0
        assert all(0.0 <= s.score <= 1.0 for s in scores)

    def test_empty_text(self, summarizer):
        assert summarizer.score_sentences("", SummaryMethod.TEXTRANK) == []

    def test_invalid_method(self, summarizer):
        with pytest.raises(ValueError):
            summarizer.score_sentences("Hi.", "nope")  # type: ignore[arg-type]


# --------------------------------------------------------------------------
# TestTopSentences
# --------------------------------------------------------------------------


class TestTopSentences:
    def test_preserves_original_order(self, summarizer):
        scores = [
            SentenceScore("third", 2, 0.9),
            SentenceScore("first", 0, 1.0),
            SentenceScore("second", 1, 0.5),
        ]
        # Top 2: first (1.0), third (0.9) — in original order: first, third.
        top = summarizer.top_sentences(scores, 2)
        assert top == ["first", "third"]

    def test_n_larger_than_input(self, summarizer):
        scores = [SentenceScore("a", 0, 1.0), SentenceScore("b", 1, 2.0)]
        top = summarizer.top_sentences(scores, 100)
        assert len(top) == 2

    def test_n_zero(self, summarizer):
        scores = [SentenceScore("a", 0, 1.0)]
        assert summarizer.top_sentences(scores, 0) == []

    def test_empty_input(self, summarizer):
        assert summarizer.top_sentences([], 5) == []

    def test_ties_broken_by_index(self, summarizer):
        scores = [
            SentenceScore("b", 1, 1.0),
            SentenceScore("a", 0, 1.0),
            SentenceScore("c", 2, 1.0),
        ]
        top = summarizer.top_sentences(scores, 2)
        # Equal scores -> earlier index wins, then preserve order.
        assert top == ["a", "b"]


# --------------------------------------------------------------------------
# TestExtractKeywords
# --------------------------------------------------------------------------


class TestExtractKeywords:
    def test_picks_frequent_words(self, summarizer):
        text = "cat cat cat dog dog mouse"
        kws = summarizer.extract_keywords(text, top_k=3)
        assert kws[0] == "cat"
        assert "dog" in kws

    def test_skips_stop_words(self, summarizer):
        text = "the the the and and of cat"
        kws = summarizer.extract_keywords(text, top_k=5)
        assert "the" not in kws
        assert "and" not in kws
        assert "cat" in kws

    def test_top_k_zero(self, summarizer):
        assert summarizer.extract_keywords("hello world", top_k=0) == []

    def test_empty_text(self, summarizer):
        assert summarizer.extract_keywords("", top_k=5) == []

    def test_respects_top_k(self, summarizer):
        text = " ".join(f"word{i}" for i in range(20))
        kws = summarizer.extract_keywords(text, top_k=5)
        assert len(kws) == 5


# --------------------------------------------------------------------------
# TestEdgeCases
# --------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_text_lead_3(self, summarizer):
        out = summarizer.summarize_lead_3("")
        assert out.sentences == []
        assert out.text == ""
        assert out.original_length == 0
        assert out.summary_length == 0

    def test_empty_text_textrank(self, summarizer):
        out = summarizer.summarize_textrank("", max_sentences=3)
        assert out.sentences == []

    def test_single_sentence_all_methods(self, summarizer):
        text = "Just one sentence."
        for method in SummaryMethod:
            out = summarizer.summarize(text, method=method, max_sentences=3)
            assert len(out.sentences) == 1

    def test_whitespace_only(self, summarizer):
        out = summarizer.summarize_lead_3("   \n\t  ")
        assert out.sentences == []

    def test_fewer_sentences_than_n(self, summarizer):
        out = summarizer.summarize_first_n("A. B.", n=10)
        assert len(out.sentences) == 2

    def test_compression_ratio_real(self, summarizer, sample_text):
        out = summarizer.summarize_lead_3(sample_text)
        assert 0.0 < out.compression_ratio <= 1.0

    def test_text_field_joined(self, summarizer, sample_text):
        out = summarizer.summarize_first_n(sample_text, n=2)
        assert out.text == " ".join(out.sentences)

    def test_no_punctuation_one_sentence(self, summarizer):
        # No sentence terminator — treated as a single sentence.
        out = summarizer.summarize_lead_3("hello world without punctuation")
        assert len(out.sentences) == 1
