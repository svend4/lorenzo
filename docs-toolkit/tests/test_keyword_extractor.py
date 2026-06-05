"""Tests for docstoolkit.keyword_extractor — target: >= 40 tests."""
from __future__ import annotations

import math

import pytest

from docstoolkit.keyword_extractor import ExtractionConfig, Keyword, KeywordExtractor


# ===========================================================================
# TestExtractionConfig
# ===========================================================================


class TestExtractionConfig:
    def test_default_max_keywords(self):
        cfg = ExtractionConfig()
        assert cfg.max_keywords == 10

    def test_default_min_freq(self):
        cfg = ExtractionConfig()
        assert cfg.min_freq == 1

    def test_default_min_length(self):
        cfg = ExtractionConfig()
        assert cfg.min_length == 3

    def test_default_max_length(self):
        cfg = ExtractionConfig()
        assert cfg.max_length == 50

    def test_default_use_bigrams(self):
        cfg = ExtractionConfig()
        assert cfg.use_bigrams is False

    def test_default_stop_words_empty_set(self):
        cfg = ExtractionConfig()
        assert isinstance(cfg.stop_words, set)
        assert len(cfg.stop_words) == 0

    def test_stop_words_instances_are_independent(self):
        cfg1 = ExtractionConfig()
        cfg2 = ExtractionConfig()
        cfg1.stop_words.add("the")
        assert "the" not in cfg2.stop_words

    def test_custom_values(self):
        cfg = ExtractionConfig(
            max_keywords=5,
            min_freq=2,
            min_length=4,
            max_length=20,
            use_bigrams=True,
            stop_words={"the", "and"},
        )
        assert cfg.max_keywords == 5
        assert cfg.min_freq == 2
        assert cfg.min_length == 4
        assert cfg.max_length == 20
        assert cfg.use_bigrams is True
        assert cfg.stop_words == {"the", "and"}


# ===========================================================================
# TestKeywordDataclass
# ===========================================================================


class TestKeywordDataclass:
    def test_fields_accessible(self):
        kw = Keyword(term="python", score=0.5, frequency=3, doc_frequency=2)
        assert kw.term == "python"
        assert kw.score == 0.5
        assert kw.frequency == 3
        assert kw.doc_frequency == 2

    def test_zero_values(self):
        kw = Keyword(term="foo", score=0.0, frequency=0, doc_frequency=0)
        assert kw.score == 0.0
        assert kw.frequency == 0
        assert kw.doc_frequency == 0

    def test_equality(self):
        kw1 = Keyword(term="test", score=1.0, frequency=1, doc_frequency=1)
        kw2 = Keyword(term="test", score=1.0, frequency=1, doc_frequency=1)
        assert kw1 == kw2


# ===========================================================================
# TestExtractorUnfitted
# ===========================================================================


class TestExtractorUnfitted:
    def test_is_fitted_false_initially(self):
        extractor = KeywordExtractor()
        assert extractor.is_fitted is False

    def test_vocabulary_size_zero_initially(self):
        extractor = KeywordExtractor()
        assert extractor.vocabulary_size == 0

    def test_extract_without_fit_returns_keywords(self):
        extractor = KeywordExtractor()
        results = extractor.extract("machine learning algorithms are powerful tools")
        assert isinstance(results, list)
        assert len(results) > 0

    def test_extract_without_fit_tf_only_doc_frequency_zero(self):
        extractor = KeywordExtractor()
        results = extractor.extract("hello world hello")
        for kw in results:
            assert kw.doc_frequency == 0

    def test_extract_without_fit_score_equals_tf(self):
        # When unfitted, IDF=1.0, so score = TF * 1.0 = TF
        extractor = KeywordExtractor()
        text = "cat cat cat dog dog"
        results = extractor.extract(text)
        total_tokens = 5  # all >= min_length=3
        cat_kw = next(k for k in results if k.term == "cat")
        assert abs(cat_kw.score - (3 / total_tokens)) < 1e-9

    def test_top_keywords_empty_when_not_fitted(self):
        extractor = KeywordExtractor()
        assert extractor.top_keywords == []


# ===========================================================================
# TestExtractorFit
# ===========================================================================


class TestExtractorFit:
    def test_is_fitted_true_after_fit(self):
        extractor = KeywordExtractor()
        extractor.fit(["hello world"])
        assert extractor.is_fitted is True

    def test_vocabulary_size_after_fit(self):
        extractor = KeywordExtractor()
        extractor.fit(["cat dog", "dog bird"])
        # "cat", "dog", "bird" — 3 terms
        assert extractor.vocabulary_size == 3

    def test_fit_replaces_previous_corpus(self):
        extractor = KeywordExtractor()
        extractor.fit(["one two three four five"])
        size1 = extractor.vocabulary_size
        extractor.fit(["aaa"])
        size2 = extractor.vocabulary_size
        assert size1 > size2

    def test_fit_empty_corpus(self):
        extractor = KeywordExtractor()
        extractor.fit([])
        assert extractor.is_fitted is False
        assert extractor.vocabulary_size == 0

    def test_fit_single_document(self):
        extractor = KeywordExtractor()
        extractor.fit(["only one document here"])
        assert extractor.is_fitted is True
        assert extractor.vocabulary_size >= 1

    def test_fit_counts_document_frequency_correctly(self):
        extractor = KeywordExtractor()
        # "shared" appears in two docs, "unique" only in one
        extractor.fit(["shared unique", "shared other"])
        # Access internal state for verification
        assert extractor._df.get("shared") == 2
        assert extractor._df.get("unique") == 1


# ===========================================================================
# TestExtractorExtract
# ===========================================================================


class TestExtractorExtract:
    def test_returns_list(self):
        extractor = KeywordExtractor()
        result = extractor.extract("simple test sentence")
        assert isinstance(result, list)

    def test_keywords_are_keyword_instances(self):
        extractor = KeywordExtractor()
        results = extractor.extract("test document about keywords")
        for kw in results:
            assert isinstance(kw, Keyword)

    def test_results_sorted_by_score_descending(self):
        extractor = KeywordExtractor()
        results = extractor.extract(
            "alpha alpha alpha beta beta gamma"
        )
        scores = [kw.score for kw in results]
        assert scores == sorted(scores, reverse=True)

    def test_respects_max_keywords_default(self):
        cfg = ExtractionConfig(max_keywords=3)
        extractor = KeywordExtractor(cfg)
        text = " ".join(["word" + str(i) for i in range(20)])
        results = extractor.extract(text)
        assert len(results) <= 3

    def test_frequency_correct(self):
        extractor = KeywordExtractor()
        results = extractor.extract("apple apple banana")
        apple_kw = next(k for k in results if k.term == "apple")
        assert apple_kw.frequency == 2

    def test_empty_text_returns_empty_list(self):
        extractor = KeywordExtractor()
        assert extractor.extract("") == []

    def test_text_with_only_short_words_returns_empty(self):
        # default min_length=3, so "a", "bb" are filtered
        extractor = KeywordExtractor()
        assert extractor.extract("a bb") == []

    def test_tfidf_score_with_fitted_extractor(self):
        extractor = KeywordExtractor()
        # "rare" appears in 1 of 3 docs; "common" in all 3
        extractor.fit(["rare unique term", "common words here", "common words there"])
        results = extractor.extract("rare common")
        rare_kw = next((k for k in results if k.term == "rare"), None)
        common_kw = next((k for k in results if k.term == "common"), None)
        assert rare_kw is not None
        assert common_kw is not None
        # "rare" has higher IDF so should score higher (equal TF)
        assert rare_kw.score > common_kw.score


# ===========================================================================
# TestExtractorMinFreq
# ===========================================================================


class TestExtractorMinFreq:
    def test_min_freq_filters_low_frequency_terms(self):
        cfg = ExtractionConfig(min_freq=2)
        extractor = KeywordExtractor(cfg)
        # "once" appears once, "twice" appears twice
        results = extractor.extract("once twice twice")
        terms = {kw.term for kw in results}
        assert "once" not in terms
        assert "twice" in terms

    def test_min_freq_one_keeps_all(self):
        cfg = ExtractionConfig(min_freq=1)
        extractor = KeywordExtractor(cfg)
        results = extractor.extract("alpha beta gamma")
        assert len(results) == 3

    def test_min_freq_equal_to_occurrence_keeps_term(self):
        cfg = ExtractionConfig(min_freq=3)
        extractor = KeywordExtractor(cfg)
        results = extractor.extract("apple apple apple banana banana")
        terms = {kw.term for kw in results}
        assert "apple" in terms
        assert "banana" not in terms


# ===========================================================================
# TestExtractorMinLength
# ===========================================================================


class TestExtractorMinLength:
    def test_min_length_filters_short_terms(self):
        cfg = ExtractionConfig(min_length=5)
        extractor = KeywordExtractor(cfg)
        # "four" has 4 chars, "fiver" has 5
        results = extractor.extract("four fiver fiver")
        terms = {kw.term for kw in results}
        assert "four" not in terms
        assert "fiver" in terms

    def test_max_length_filters_long_terms(self):
        cfg = ExtractionConfig(max_length=5)
        extractor = KeywordExtractor(cfg)
        # "toolong" has 7 chars
        results = extractor.extract("short toolong short")
        terms = {kw.term for kw in results}
        assert "short" in terms
        assert "toolong" not in terms

    def test_min_length_three_default(self):
        extractor = KeywordExtractor()
        results = extractor.extract("go run python")
        terms = {kw.term for kw in results}
        assert "go" not in terms
        assert "run" in terms
        assert "python" in terms


# ===========================================================================
# TestExtractorStopWords
# ===========================================================================


class TestExtractorStopWords:
    def test_stop_words_excluded_from_results(self):
        cfg = ExtractionConfig(stop_words={"the", "and", "for"})
        extractor = KeywordExtractor(cfg)
        results = extractor.extract("the cat and the dog are for playing")
        terms = {kw.term for kw in results}
        assert "the" not in terms
        assert "and" not in terms
        assert "for" not in terms

    def test_non_stop_words_still_present(self):
        cfg = ExtractionConfig(stop_words={"the"})
        extractor = KeywordExtractor(cfg)
        results = extractor.extract("the quick brown fox")
        terms = {kw.term for kw in results}
        assert "quick" in terms
        assert "brown" in terms
        assert "fox" in terms

    def test_all_stop_words_returns_empty(self):
        cfg = ExtractionConfig(stop_words={"cat", "dog"})
        extractor = KeywordExtractor(cfg)
        results = extractor.extract("cat dog")
        assert results == []

    def test_stop_words_case_insensitive_after_lower(self):
        cfg = ExtractionConfig(stop_words={"python"})
        extractor = KeywordExtractor(cfg)
        # text is lowercased during tokenization, so "Python" -> "python"
        results = extractor.extract("Python is great")
        terms = {kw.term for kw in results}
        assert "python" not in terms


# ===========================================================================
# TestExtractorBigrams
# ===========================================================================


class TestExtractorBigrams:
    def test_bigrams_enabled_produces_underscore_terms(self):
        cfg = ExtractionConfig(use_bigrams=True, max_keywords=20)
        extractor = KeywordExtractor(cfg)
        results = extractor.extract("machine learning algorithms")
        terms = {kw.term for kw in results}
        bigrams = {t for t in terms if "_" in t}
        assert len(bigrams) > 0

    def test_bigrams_disabled_no_underscore_terms(self):
        cfg = ExtractionConfig(use_bigrams=False)
        extractor = KeywordExtractor(cfg)
        results = extractor.extract("machine learning algorithms")
        terms = {kw.term for kw in results}
        bigrams = {t for t in terms if "_" in t}
        assert len(bigrams) == 0

    def test_bigram_correct_form(self):
        cfg = ExtractionConfig(use_bigrams=True, max_keywords=20)
        extractor = KeywordExtractor(cfg)
        results = extractor.extract("neural network model")
        terms = {kw.term for kw in results}
        assert "neural_network" in terms or "network_model" in terms

    def test_bigrams_single_token_no_bigrams(self):
        cfg = ExtractionConfig(use_bigrams=True)
        extractor = KeywordExtractor(cfg)
        results = extractor.extract("python")
        terms = {kw.term for kw in results}
        bigrams = {t for t in terms if "_" in t}
        assert len(bigrams) == 0


# ===========================================================================
# TestExtractorTopK
# ===========================================================================


class TestExtractorTopK:
    def test_top_k_limits_results(self):
        extractor = KeywordExtractor()
        text = " ".join(["word" + str(i) for i in range(20)])
        results = extractor.extract(text, top_k=5)
        assert len(results) <= 5

    def test_top_k_overrides_config_max_keywords(self):
        cfg = ExtractionConfig(max_keywords=10)
        extractor = KeywordExtractor(cfg)
        text = " ".join(["word" + str(i) for i in range(20)])
        results = extractor.extract(text, top_k=2)
        assert len(results) <= 2

    def test_top_k_none_uses_config_max_keywords(self):
        cfg = ExtractionConfig(max_keywords=3)
        extractor = KeywordExtractor(cfg)
        text = " ".join(["word" + str(i) for i in range(20)])
        results = extractor.extract(text, top_k=None)
        assert len(results) <= 3

    def test_top_k_larger_than_available_returns_all(self):
        extractor = KeywordExtractor()
        results = extractor.extract("alpha beta", top_k=100)
        assert len(results) == 2


# ===========================================================================
# TestExtractorBatch
# ===========================================================================


class TestExtractorBatch:
    def test_batch_returns_list_of_lists(self):
        extractor = KeywordExtractor()
        results = extractor.extract_batch(["hello world", "foo bar baz"])
        assert isinstance(results, list)
        assert len(results) == 2
        for r in results:
            assert isinstance(r, list)

    def test_batch_length_matches_input(self):
        extractor = KeywordExtractor()
        texts = ["text one", "text two", "text three", "text four"]
        results = extractor.extract_batch(texts)
        assert len(results) == len(texts)

    def test_batch_empty_list(self):
        extractor = KeywordExtractor()
        results = extractor.extract_batch([])
        assert results == []

    def test_batch_top_k_applied_to_each(self):
        extractor = KeywordExtractor()
        texts = [
            " ".join(["word" + str(i) for i in range(20)]),
            " ".join(["term" + str(i) for i in range(20)]),
        ]
        results = extractor.extract_batch(texts, top_k=3)
        for r in results:
            assert len(r) <= 3

    def test_batch_results_are_sorted(self):
        extractor = KeywordExtractor()
        results = extractor.extract_batch(["alpha alpha beta gamma"])
        for r in results:
            scores = [kw.score for kw in r]
            assert scores == sorted(scores, reverse=True)


# ===========================================================================
# TestExtractorTopKeywords
# ===========================================================================


class TestExtractorTopKeywords:
    def test_top_keywords_returns_list_of_strings(self):
        extractor = KeywordExtractor()
        extractor.fit(["machine learning", "deep learning", "neural network"])
        result = extractor.top_keywords
        assert isinstance(result, list)
        for t in result:
            assert isinstance(t, str)

    def test_top_keywords_length_respects_max_keywords(self):
        cfg = ExtractionConfig(max_keywords=5)
        extractor = KeywordExtractor(cfg)
        # Fit with enough unique terms
        extractor.fit([f"unique{i} common" for i in range(20)])
        result = extractor.top_keywords
        assert len(result) <= 5

    def test_top_keywords_empty_when_not_fitted(self):
        extractor = KeywordExtractor()
        assert extractor.top_keywords == []

    def test_top_keywords_rare_terms_rank_higher(self):
        extractor = KeywordExtractor()
        # "rare" appears in 1 of 4 docs; "common" in all 4
        extractor.fit([
            "rare term here",
            "common word here",
            "common word there",
            "common word everywhere",
        ])
        top = extractor.top_keywords
        # "rare" should appear before "common" among top terms
        assert "rare" in top
        if "common" in top:
            assert top.index("rare") < top.index("common")


# ===========================================================================
# TestExtractorIDF
# ===========================================================================


class TestExtractorIDF:
    def test_idf_formula_known_values(self):
        extractor = KeywordExtractor()
        # N=3 docs, term appears in df=1 doc
        extractor.fit(["alpha unique", "beta gamma", "delta epsilon"])
        # Expected IDF = log((1+3)/(1+1)) + 1 = log(2) + 1
        expected = math.log(4 / 2) + 1
        actual = extractor._idf("unique")
        assert abs(actual - expected) < 1e-9

    def test_idf_common_term_lower_than_rare(self):
        extractor = KeywordExtractor()
        extractor.fit([
            "common rare",
            "common foo",
            "common bar",
        ])
        idf_common = extractor._idf("common")
        idf_rare = extractor._idf("rare")
        assert idf_rare > idf_common

    def test_idf_unknown_term_uses_zero_df(self):
        extractor = KeywordExtractor()
        extractor.fit(["some document here"])
        # "unknown" not in corpus: df=0, N=1
        expected = math.log((1 + 1) / (1 + 0)) + 1
        actual = extractor._idf("unknown")
        assert abs(actual - expected) < 1e-9

    def test_idf_unfitted_returns_one(self):
        extractor = KeywordExtractor()
        assert extractor._idf("anything") == 1.0


# ===========================================================================
# TestEdgeCases
# ===========================================================================


class TestEdgeCases:
    def test_extract_empty_string(self):
        extractor = KeywordExtractor()
        assert extractor.extract("") == []

    def test_extract_whitespace_only(self):
        extractor = KeywordExtractor()
        assert extractor.extract("   \t\n  ") == []

    def test_extract_single_word_above_min_length(self):
        extractor = KeywordExtractor()
        results = extractor.extract("python")
        assert len(results) == 1
        assert results[0].term == "python"
        assert results[0].frequency == 1

    def test_extract_all_tokens_are_stop_words(self):
        cfg = ExtractionConfig(stop_words={"the", "and", "foo"})
        extractor = KeywordExtractor(cfg)
        assert extractor.extract("the and foo") == []

    def test_extract_cyrillic_text(self):
        extractor = KeywordExtractor()
        results = extractor.extract("машинное обучение алгоритм")
        terms = {kw.term for kw in results}
        assert "машинное" in terms
        assert "обучение" in terms
        assert "алгоритм" in terms

    def test_extract_mixed_latin_cyrillic(self):
        extractor = KeywordExtractor()
        results = extractor.extract("python питон code код")
        terms = {kw.term for kw in results}
        assert "python" in terms
        assert "питон" in terms
        assert "code" in terms
        assert "код" in terms

    def test_extract_numeric_only_text(self):
        extractor = KeywordExtractor()
        # digits don't match [a-zа-яё]
        assert extractor.extract("123 456 789") == []

    def test_fit_then_extract_doc_frequency_populated(self):
        extractor = KeywordExtractor()
        extractor.fit(["alpha beta", "alpha gamma"])
        results = extractor.extract("alpha")
        assert len(results) == 1
        assert results[0].doc_frequency == 2

    def test_extract_repeated_word_frequency(self):
        extractor = KeywordExtractor()
        results = extractor.extract("hello hello hello world")
        hello_kw = next(k for k in results if k.term == "hello")
        assert hello_kw.frequency == 3
