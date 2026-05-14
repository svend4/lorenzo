"""Tests for docstoolkit.crosslingual — E24 cross-lingual support module.

Coverage:
  - LanguageDetector: detect() and detect_batch()
  - LangDetectionResult: is_confident()
  - TextNormalizer: normalize(), tokenize(), stem_ru(), stem_en()
  - CrossLingualSearcher: prepare_query(), score(), search()
"""
import pytest

from docstoolkit.crosslingual import (
    Language,
    LangDetectionResult,
    LanguageDetector,
    NormalizationConfig,
    TextNormalizer,
    CrossLingualQuery,
    CrossLingualSearcher,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def detector():
    return LanguageDetector()


@pytest.fixture()
def normalizer():
    return TextNormalizer()


@pytest.fixture()
def searcher():
    return CrossLingualSearcher()


# ---------------------------------------------------------------------------
# LanguageDetector — pure Russian
# ---------------------------------------------------------------------------

class TestLanguageDetectorRussian:
    def test_pure_ru_short_sentence(self, detector):
        result = detector.detect("Привет мир это тест")
        assert result.language == Language.RUSSIAN

    def test_pure_ru_long_sentence(self, detector):
        text = "Это длинный русский текст который содержит много кириллических символов"
        result = detector.detect(text)
        assert result.language == Language.RUSSIAN

    def test_ru_ru_ratio_high(self, detector):
        result = detector.detect("Это русское предложение без латиницы")
        assert result.ru_ratio > 0.7

    def test_ru_confidence_high(self, detector):
        result = detector.detect("Это русское предложение без латиницы")
        assert result.confidence > 0.7

    def test_ru_is_confident_true(self, detector):
        result = detector.detect("Это русское предложение без латиницы")
        assert result.is_confident() is True

    def test_ru_en_ratio_low(self, detector):
        result = detector.detect("Привет это чисто русский текст с буквами")
        assert result.en_ratio < 0.3

    def test_ru_single_word_long(self, detector):
        result = detector.detect("кириллический")
        # 13 chars — all Cyrillic, total >= 10
        assert result.language == Language.RUSSIAN

    def test_ru_with_spaces_and_digits(self, detector):
        result = detector.detect("Версия 2 это система для хранения знаний в памяти")
        assert result.language == Language.RUSSIAN


# ---------------------------------------------------------------------------
# LanguageDetector — pure English
# ---------------------------------------------------------------------------

class TestLanguageDetectorEnglish:
    def test_pure_en_short(self, detector):
        result = detector.detect("Hello world this is test")
        assert result.language == Language.ENGLISH

    def test_pure_en_long(self, detector):
        text = "This is a long English text that contains many Latin characters and words"
        result = detector.detect(text)
        assert result.language == Language.ENGLISH

    def test_en_en_ratio_high(self, detector):
        result = detector.detect("This is pure English text without Cyrillic")
        assert result.en_ratio > 0.7

    def test_en_confidence_high(self, detector):
        result = detector.detect("This is pure English text without Cyrillic")
        assert result.confidence > 0.7

    def test_en_is_confident_true(self, detector):
        result = detector.detect("This is pure English text")
        assert result.is_confident() is True

    def test_en_ru_ratio_low(self, detector):
        result = detector.detect("Pure English text without any Cyrillic characters here")
        assert result.ru_ratio < 0.3

    def test_en_single_word_long(self, detector):
        result = detector.detect("international")
        # 13 chars — all Latin
        assert result.language == Language.ENGLISH

    def test_en_with_digits(self, detector):
        result = detector.detect("Version 2 is the best system for knowledge storage")
        assert result.language == Language.ENGLISH


# ---------------------------------------------------------------------------
# LanguageDetector — MIXED
# ---------------------------------------------------------------------------

class TestLanguageDetectorMixed:
    def test_mixed_detection(self, detector):
        text = "This is mixed текст with English and русским языком"
        result = detector.detect(text)
        assert result.language == Language.MIXED

    def test_mixed_both_ratios_above_threshold(self, detector):
        text = "Hello мир this is смешанный text"
        result = detector.detect(text)
        assert result.ru_ratio > 0.2
        assert result.en_ratio > 0.2

    def test_mixed_code_comments(self, detector):
        # Typical code comment pattern: Russian description, English keywords
        text = "function calculate память agent retrieval функция поиска"
        result = detector.detect(text)
        assert result.language == Language.MIXED

    def test_mixed_ratios_sum_to_one(self, detector):
        text = "hello мир world память english русский"
        result = detector.detect(text)
        assert abs(result.ru_ratio + result.en_ratio - 1.0) < 1e-9


# ---------------------------------------------------------------------------
# LanguageDetector — UNKNOWN
# ---------------------------------------------------------------------------

class TestLanguageDetectorUnknown:
    def test_empty_string(self, detector):
        result = detector.detect("")
        assert result.language == Language.UNKNOWN

    def test_too_short_text(self, detector):
        # total < 10 chars
        result = detector.detect("ab")
        assert result.language == Language.UNKNOWN

    def test_digits_only(self, detector):
        result = detector.detect("12345678")
        assert result.language == Language.UNKNOWN

    def test_symbols_only(self, detector):
        result = detector.detect("!@#$%^&*()")
        assert result.language == Language.UNKNOWN

    def test_whitespace_only(self, detector):
        result = detector.detect("         ")
        assert result.language == Language.UNKNOWN


# ---------------------------------------------------------------------------
# LangDetectionResult — is_confident
# ---------------------------------------------------------------------------

class TestLangDetectionResultIsConfident:
    def test_confident_above_default_threshold(self):
        r = LangDetectionResult(
            language=Language.RUSSIAN,
            confidence=0.85,
            ru_ratio=0.85,
            en_ratio=0.15,
        )
        assert r.is_confident() is True

    def test_not_confident_below_default_threshold(self):
        r = LangDetectionResult(
            language=Language.MIXED,
            confidence=0.55,
            ru_ratio=0.55,
            en_ratio=0.45,
        )
        assert r.is_confident() is False

    def test_is_confident_custom_threshold_low(self):
        r = LangDetectionResult(
            language=Language.ENGLISH,
            confidence=0.65,
            ru_ratio=0.35,
            en_ratio=0.65,
        )
        assert r.is_confident(threshold=0.6) is True

    def test_is_confident_custom_threshold_high(self):
        r = LangDetectionResult(
            language=Language.RUSSIAN,
            confidence=0.75,
            ru_ratio=0.75,
            en_ratio=0.25,
        )
        assert r.is_confident(threshold=0.9) is False

    def test_is_confident_exactly_at_threshold(self):
        r = LangDetectionResult(
            language=Language.ENGLISH,
            confidence=0.7,
            ru_ratio=0.3,
            en_ratio=0.7,
        )
        assert r.is_confident(threshold=0.7) is True


# ---------------------------------------------------------------------------
# LanguageDetector — detect_batch
# ---------------------------------------------------------------------------

class TestDetectBatch:
    def test_batch_returns_correct_length(self, detector):
        texts = ["Привет мир это тест", "Hello world test text", "mixed смешанный"]
        results = detector.detect_batch(texts)
        assert len(results) == 3

    def test_batch_correct_languages(self, detector):
        texts = [
            "Это русский текст с кириллицей",
            "This is English text with Latin",
        ]
        results = detector.detect_batch(texts)
        assert results[0].language == Language.RUSSIAN
        assert results[1].language == Language.ENGLISH

    def test_batch_empty_list(self, detector):
        assert detector.detect_batch([]) == []

    def test_batch_single_item(self, detector):
        results = detector.detect_batch(["Hello world this is text"])
        assert len(results) == 1
        assert results[0].language == Language.ENGLISH


# ---------------------------------------------------------------------------
# TextNormalizer — normalize
# ---------------------------------------------------------------------------

class TestTextNormalizerNormalize:
    def test_lowercase_default(self, normalizer):
        result = normalizer.normalize("Hello World")
        assert result == "hello world"

    def test_lowercase_russian(self, normalizer):
        result = normalizer.normalize("Привет МИР")
        assert result == "привет мир"

    def test_no_lowercase_when_disabled(self, normalizer):
        config = NormalizationConfig(lowercase=False)
        result = normalizer.normalize("Hello World", config)
        assert result == "Hello World"

    def test_strip_punctuation(self, normalizer):
        config = NormalizationConfig(strip_punctuation=True)
        result = normalizer.normalize("Hello, world!", config)
        assert "," not in result
        assert "!" not in result

    def test_strip_punctuation_keeps_words(self, normalizer):
        config = NormalizationConfig(strip_punctuation=True)
        result = normalizer.normalize("Hello, world!", config)
        assert "hello" in result
        assert "world" in result

    def test_strip_numbers(self, normalizer):
        config = NormalizationConfig(strip_numbers=True)
        result = normalizer.normalize("Version 2 is ready", config)
        assert "2" not in result

    def test_no_strip_numbers_by_default(self, normalizer):
        result = normalizer.normalize("Version 2 is ready")
        assert "2" in result

    def test_collapse_whitespace(self, normalizer):
        result = normalizer.normalize("hello   world")
        assert result == "hello world"

    def test_collapse_whitespace_tabs_and_newlines(self, normalizer):
        result = normalizer.normalize("hello\t\tworld\nnew")
        assert result == "hello world new"

    def test_no_collapse_whitespace_when_disabled(self, normalizer):
        config = NormalizationConfig(collapse_whitespace=False)
        result = normalizer.normalize("hello   world", config)
        assert "   " in result

    def test_strip_leading_trailing_whitespace(self, normalizer):
        result = normalizer.normalize("  hello world  ")
        assert result == "hello world"

    def test_all_options_combined(self, normalizer):
        config = NormalizationConfig(
            lowercase=True,
            strip_punctuation=True,
            strip_numbers=True,
            collapse_whitespace=True,
        )
        result = normalizer.normalize("  Hello, World! 42  ", config)
        # strip_numbers removes "42", collapse_whitespace strips and squeezes
        assert "hello" in result
        assert "world" in result
        assert "42" not in result
        assert "," not in result
        assert "!" not in result


# ---------------------------------------------------------------------------
# TextNormalizer — tokenize
# ---------------------------------------------------------------------------

class TestTextNormalizerTokenize:
    def test_tokenize_basic(self, normalizer):
        tokens = normalizer.tokenize("Hello World")
        assert tokens == ["hello", "world"]

    def test_tokenize_russian(self, normalizer):
        tokens = normalizer.tokenize("Привет Мир")
        assert tokens == ["привет", "мир"]

    def test_tokenize_empty_string(self, normalizer):
        assert normalizer.tokenize("") == []

    def test_tokenize_extra_spaces_filtered(self, normalizer):
        tokens = normalizer.tokenize("hello   world")
        assert tokens == ["hello", "world"]

    def test_tokenize_returns_list(self, normalizer):
        result = normalizer.tokenize("one two three")
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# TextNormalizer — stem_ru
# ---------------------------------------------------------------------------

class TestStemRu:
    def test_stem_ого_suffix(self, normalizer):
        assert normalizer.stem_ru("красивого") == "красив"

    def test_stem_ому_suffix(self, normalizer):
        assert normalizer.stem_ru("красивому") == "красив"

    def test_stem_ый_suffix(self, normalizer):
        assert normalizer.stem_ru("красивый") == "красив"

    def test_stem_ая_suffix(self, normalizer):
        assert normalizer.stem_ru("красивая") == "красив"

    def test_stem_ами_suffix(self, normalizer):
        assert normalizer.stem_ru("столами") == "стол"

    def test_stem_ов_suffix(self, normalizer):
        result = normalizer.stem_ru("столов")
        assert result == "стол"

    def test_stem_short_token_unchanged(self, normalizer):
        # len <= 4 — no stemming
        assert normalizer.stem_ru("кот") == "кот"

    def test_stem_exactly_4_chars_unchanged(self, normalizer):
        assert normalizer.stem_ru("коты") == "коты"

    def test_stem_no_matching_suffix(self, normalizer):
        # No recognized suffix — return lowercased
        result = normalizer.stem_ru("программа")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_stem_ru_returns_lowercase(self, normalizer):
        result = normalizer.stem_ru("КРАСИВЫЙ")
        assert result == result.lower()

    def test_stem_ей_suffix(self, normalizer):
        result = normalizer.stem_ru("ветвей")
        assert result == "ветв"


# ---------------------------------------------------------------------------
# TextNormalizer — stem_en
# ---------------------------------------------------------------------------

class TestStemEn:
    def test_stem_ing_suffix(self, normalizer):
        assert normalizer.stem_en("running") == "runn"

    def test_stem_ed_suffix(self, normalizer):
        assert normalizer.stem_en("walked") == "walk"

    def test_stem_er_suffix(self, normalizer):
        assert normalizer.stem_en("faster") == "fast"

    def test_stem_est_suffix(self, normalizer):
        assert normalizer.stem_en("fastest") == "fast"

    def test_stem_ly_suffix(self, normalizer):
        assert normalizer.stem_en("quickly") == "quick"

    def test_stem_tion_suffix(self, normalizer):
        # "detection" (9 chars) - "tion" (4 chars) = "detec" (5 chars)
        # stripping -tion suffix yields the stem "detec"
        result = normalizer.stem_en("detection")
        assert result == "detec"
        # "creation" (8 chars) - "tion" = "crea"
        assert normalizer.stem_en("creation") == "crea"

    def test_stem_ness_suffix(self, normalizer):
        assert normalizer.stem_en("darkness") == "dark"

    def test_stem_ment_suffix(self, normalizer):
        assert normalizer.stem_en("movement") == "move"

    def test_stem_short_token_unchanged(self, normalizer):
        # len <= 4 — no stemming
        assert normalizer.stem_en("run") == "run"

    def test_stem_exactly_4_chars_unchanged(self, normalizer):
        assert normalizer.stem_en("runs") == "runs"

    def test_stem_no_matching_suffix(self, normalizer):
        result = normalizer.stem_en("computer")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_stem_en_returns_lowercase(self, normalizer):
        result = normalizer.stem_en("RUNNING")
        assert result == result.lower()


# ---------------------------------------------------------------------------
# CrossLingualSearcher — prepare_query
# ---------------------------------------------------------------------------

class TestPrepareQuery:
    def test_prepare_ru_query(self, searcher):
        q = searcher.prepare_query("память агента")
        assert q.language == Language.RUSSIAN
        assert q.original == "память агента"
        assert isinstance(q.normalized, str)
        assert isinstance(q.tokens, list)

    def test_prepare_en_query(self, searcher):
        q = searcher.prepare_query("agent memory retrieval")
        assert q.language == Language.ENGLISH

    def test_prepare_query_tokens_not_empty(self, searcher):
        q = searcher.prepare_query("agent memory retrieval system")
        assert len(q.tokens) > 0

    def test_prepare_query_normalized_lowercase(self, searcher):
        q = searcher.prepare_query("Hello World")
        assert q.normalized == "hello world"

    def test_prepare_query_returns_crosslingual_query(self, searcher):
        q = searcher.prepare_query("some query text")
        assert isinstance(q, CrossLingualQuery)

    def test_prepare_query_original_preserved(self, searcher):
        original = "Hello World"
        q = searcher.prepare_query(original)
        assert q.original == original


# ---------------------------------------------------------------------------
# CrossLingualSearcher — score
# ---------------------------------------------------------------------------

class TestScore:
    def test_exact_match_higher_score(self, searcher):
        q = searcher.prepare_query("agent memory system")
        doc_match = "agent memory system for retrieval"
        doc_no_match = "database storage with indexing"
        score_match = searcher.score(q, doc_match)
        score_no = searcher.score(q, doc_no_match)
        assert score_match > score_no

    def test_zero_overlap_gives_low_score(self, searcher):
        q = searcher.prepare_query("agent memory system")
        doc = "абсолютно другой контент без совпадений"
        score = searcher.score(q, doc)
        assert score == 0.0

    def test_partial_overlap(self, searcher):
        q = searcher.prepare_query("agent memory system")
        doc = "memory retrieval"
        score = searcher.score(q, doc)
        assert 0.0 < score <= 1.0

    def test_score_denominator_avoids_div_zero(self, searcher):
        # Empty query tokens
        q = CrossLingualQuery(
            original="",
            language=Language.UNKNOWN,
            normalized="",
            tokens=[],
        )
        score = searcher.score(q, "some document text")
        assert score == 0.0

    def test_score_returns_float(self, searcher):
        q = searcher.prepare_query("hello world")
        score = searcher.score(q, "hello world this is a test")
        assert isinstance(score, float)

    def test_mixed_query_stemmed_overlap(self, searcher):
        # MIXED language query: stemming should help match morphological variants
        q = searcher.prepare_query("running быстрого")
        # score should be non-negative
        score = searcher.score(q, "run быстрый")
        assert score >= 0.0


# ---------------------------------------------------------------------------
# CrossLingualSearcher — search (ordering)
# ---------------------------------------------------------------------------

class TestSearch:
    def test_search_returns_list(self, searcher):
        docs = {"d1": "agent memory", "d2": "database storage"}
        result = searcher.search("agent memory", docs)
        assert isinstance(result, list)

    def test_search_returns_all_docs(self, searcher):
        docs = {"d1": "agent memory", "d2": "database storage", "d3": "neural network"}
        result = searcher.search("agent memory", docs)
        assert len(result) == 3

    def test_search_sorted_descending(self, searcher):
        docs = {"d1": "agent memory", "d2": "database storage"}
        result = searcher.search("agent memory", docs)
        scores = [s for _, s in result]
        assert scores == sorted(scores, reverse=True)

    def test_search_best_match_first(self, searcher):
        docs = {
            "exact": "agent memory retrieval system",
            "partial": "memory storage",
            "unrelated": "pizza cooking recipe",
        }
        result = searcher.search("agent memory retrieval", docs)
        assert result[0][0] == "exact"

    def test_search_empty_documents(self, searcher):
        result = searcher.search("hello world", {})
        assert result == []

    def test_search_result_tuples(self, searcher):
        docs = {"d1": "hello world"}
        result = searcher.search("hello world", docs)
        assert len(result) == 1
        key, score = result[0]
        assert key == "d1"
        assert isinstance(score, float)

    def test_search_russian_query(self, searcher):
        docs = {
            "ru_doc": "память агента для хранения знаний",
            "en_doc": "agent memory for knowledge storage",
        }
        result = searcher.search("память агента", docs)
        # Russian query should match Russian doc better
        assert result[0][0] == "ru_doc"

    def test_search_scores_non_negative(self, searcher):
        docs = {"d1": "hello world", "d2": "foo bar baz"}
        result = searcher.search("hello world", docs)
        for _, score in result:
            assert score >= 0.0

    def test_search_custom_detector_and_normalizer(self):
        # Verify constructor injection works
        custom_detector = LanguageDetector()
        custom_normalizer = TextNormalizer()
        searcher = CrossLingualSearcher(
            detector=custom_detector,
            normalizer=custom_normalizer,
        )
        docs = {"d1": "hello world test"}
        result = searcher.search("hello world", docs)
        assert len(result) == 1
