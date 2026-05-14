"""Tests for docstoolkit.text_similarity module."""
import math
import pytest

from docstoolkit.text_similarity import TextSimilarity, SimilarityMethod, SimilarityResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def approx(value: float, rel: float = 1e-6):
    return pytest.approx(value, rel=rel)


ts = TextSimilarity()


# ---------------------------------------------------------------------------
# TestSimilarityMethod
# ---------------------------------------------------------------------------

class TestSimilarityMethod:
    def test_jaccard_value(self):
        assert SimilarityMethod.JACCARD.value == "jaccard"

    def test_cosine_value(self):
        assert SimilarityMethod.COSINE.value == "cosine"

    def test_overlap_value(self):
        assert SimilarityMethod.OVERLAP.value == "overlap"

    def test_levenshtein_value(self):
        assert SimilarityMethod.LEVENSHTEIN.value == "levenshtein"

    def test_dice_value(self):
        assert SimilarityMethod.DICE.value == "dice"

    def test_all_members_present(self):
        members = {m.name for m in SimilarityMethod}
        assert members == {"JACCARD", "COSINE", "OVERLAP", "LEVENSHTEIN", "DICE"}


# ---------------------------------------------------------------------------
# TestSimilarityResult
# ---------------------------------------------------------------------------

class TestSimilarityResult:
    def test_fields_stored(self):
        r = SimilarityResult(
            method=SimilarityMethod.JACCARD,
            score=0.5,
            text_a="hello",
            text_b="world",
        )
        assert r.method is SimilarityMethod.JACCARD
        assert r.score == 0.5
        assert r.text_a == "hello"
        assert r.text_b == "world"

    def test_score_zero_valid(self):
        r = SimilarityResult(SimilarityMethod.COSINE, 0.0, "a", "b")
        assert r.score == 0.0

    def test_score_one_valid(self):
        r = SimilarityResult(SimilarityMethod.COSINE, 1.0, "a", "a")
        assert r.score == 1.0

    def test_score_out_of_range_raises(self):
        with pytest.raises((ValueError, AssertionError)):
            SimilarityResult(SimilarityMethod.JACCARD, 1.5, "a", "b")

    def test_score_negative_raises(self):
        with pytest.raises((ValueError, AssertionError)):
            SimilarityResult(SimilarityMethod.JACCARD, -0.1, "a", "b")

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(SimilarityResult)


# ---------------------------------------------------------------------------
# TestJaccard
# ---------------------------------------------------------------------------

class TestJaccard:
    def test_identical_texts(self):
        assert ts.jaccard("hello world", "hello world") == approx(1.0)

    def test_completely_disjoint(self):
        assert ts.jaccard("apple banana", "cat dog") == approx(0.0)

    def test_partial_overlap(self):
        # {"hello", "world"} vs {"hello", "python"} → intersection=1, union=3
        assert ts.jaccard("hello world", "hello python") == approx(1 / 3)

    def test_both_empty(self):
        assert ts.jaccard("", "") == 0.0

    def test_one_empty(self):
        assert ts.jaccard("hello", "") == 0.0

    def test_subset(self):
        # {"a"} ⊆ {"a", "b"} → 1/2
        assert ts.jaccard("a", "a b") == approx(0.5)

    def test_case_insensitive(self):
        assert ts.jaccard("Hello World", "hello world") == approx(1.0)

    def test_symmetric(self):
        a, b = "the quick brown fox", "the lazy dog fox"
        assert ts.jaccard(a, b) == approx(ts.jaccard(b, a))


# ---------------------------------------------------------------------------
# TestCosine
# ---------------------------------------------------------------------------

class TestCosine:
    def test_identical_texts(self):
        assert ts.cosine("hello world hello", "hello world hello") == approx(1.0)

    def test_disjoint_texts(self):
        assert ts.cosine("apple banana", "cat dog") == approx(0.0)

    def test_partial_overlap(self):
        score = ts.cosine("hello world", "hello python")
        assert 0.0 < score < 1.0

    def test_both_empty(self):
        assert ts.cosine("", "") == 0.0

    def test_one_empty(self):
        assert ts.cosine("hello", "") == 0.0

    def test_symmetric(self):
        a, b = "machine learning", "deep learning neural"
        assert ts.cosine(a, b) == approx(ts.cosine(b, a))

    def test_repeated_words_affect_score(self):
        # "cat cat" vs "cat" should still yield 1.0 (cosine normalises)
        assert ts.cosine("cat cat", "cat") == approx(1.0)

    def test_case_insensitive(self):
        assert ts.cosine("Hello World", "hello world") == approx(1.0)


# ---------------------------------------------------------------------------
# TestOverlap
# ---------------------------------------------------------------------------

class TestOverlap:
    def test_identical_texts(self):
        assert ts.overlap("hello world", "hello world") == approx(1.0)

    def test_disjoint_texts(self):
        assert ts.overlap("apple banana", "cat dog") == approx(0.0)

    def test_subset_returns_one(self):
        # {"a"} ⊆ {"a","b","c"} → 1/min(1,3) = 1.0
        assert ts.overlap("a", "a b c") == approx(1.0)

    def test_partial(self):
        # {"a","b"} vs {"b","c"} → intersection=1, min=2 → 0.5
        assert ts.overlap("a b", "b c") == approx(0.5)

    def test_both_empty(self):
        assert ts.overlap("", "") == 0.0

    def test_one_empty(self):
        assert ts.overlap("hello", "") == 0.0

    def test_symmetric(self):
        a, b = "cat dog", "dog elephant"
        assert ts.overlap(a, b) == approx(ts.overlap(b, a))


# ---------------------------------------------------------------------------
# TestLevenshtein
# ---------------------------------------------------------------------------

class TestLevenshtein:
    def test_identical_strings(self):
        assert ts.levenshtein("hello", "hello") == approx(1.0)

    def test_both_empty_returns_one(self):
        assert ts.levenshtein("", "") == approx(1.0)

    def test_one_empty_returns_zero(self):
        assert ts.levenshtein("hello", "") == approx(0.0)
        assert ts.levenshtein("", "hello") == approx(0.0)

    def test_single_substitution(self):
        # "cat" → "bat": 1 edit, max=3 → 1 - 1/3
        assert ts.levenshtein("cat", "bat") == approx(1.0 - 1 / 3)

    def test_completely_different(self):
        # "abc" vs "xyz": 3 edits, max=3 → 0.0
        assert ts.levenshtein("abc", "xyz") == approx(0.0)

    def test_score_range(self):
        score = ts.levenshtein("kitten", "sitting")
        assert 0.0 <= score <= 1.0

    def test_char_level_not_word_level(self):
        # character-level: "ab" vs "a b" has edit distance 1 (space insertion)
        score = ts.levenshtein("ab", "a b")
        assert score == approx(1.0 - 1 / 3)

    def test_symmetric(self):
        assert ts.levenshtein("kitten", "sitting") == approx(
            ts.levenshtein("sitting", "kitten")
        )

    def test_insertion(self):
        # "" → "a": 1 edit, max=1 → 0.0
        assert ts.levenshtein("", "a") == approx(0.0)

    def test_long_strings(self):
        a = "the quick brown fox jumps over the lazy dog"
        b = "the quick brown cat jumps over the lazy dog"
        score = ts.levenshtein(a, b)
        assert 0.0 < score < 1.0


# ---------------------------------------------------------------------------
# TestDice
# ---------------------------------------------------------------------------

class TestDice:
    def test_identical_texts(self):
        assert ts.dice("hello world", "hello world") == approx(1.0)

    def test_disjoint_texts(self):
        assert ts.dice("apple banana", "cat dog") == approx(0.0)

    def test_partial_overlap(self):
        # {"hello","world"} vs {"hello","python"}: 2*1/(2+2) = 0.5
        assert ts.dice("hello world", "hello python") == approx(0.5)

    def test_both_empty(self):
        assert ts.dice("", "") == 0.0

    def test_one_empty(self):
        assert ts.dice("hello", "") == 0.0

    def test_symmetric(self):
        a, b = "knowledge graph", "graph neural network"
        assert ts.dice(a, b) == approx(ts.dice(b, a))

    def test_subset(self):
        # {"a"} vs {"a","b"}: 2*1/(1+2) = 2/3
        assert ts.dice("a", "a b") == approx(2 / 3)

    def test_case_insensitive(self):
        assert ts.dice("Hello World", "hello world") == approx(1.0)


# ---------------------------------------------------------------------------
# TestSimilarityDispatch
# ---------------------------------------------------------------------------

class TestSimilarityDispatch:
    def test_returns_similarity_result(self):
        result = ts.similarity("hello world", "hello python")
        assert isinstance(result, SimilarityResult)

    def test_default_method_is_jaccard(self):
        result = ts.similarity("hello world", "hello python")
        assert result.method is SimilarityMethod.JACCARD

    def test_score_matches_direct_call(self):
        a, b = "cat sat on mat", "cat mat"
        result = ts.similarity(a, b, SimilarityMethod.JACCARD)
        assert result.score == approx(ts.jaccard(a, b))

    def test_cosine_dispatch(self):
        a, b = "machine learning model", "deep learning neural model"
        result = ts.similarity(a, b, SimilarityMethod.COSINE)
        assert result.method is SimilarityMethod.COSINE
        assert result.score == approx(ts.cosine(a, b))

    def test_levenshtein_dispatch(self):
        result = ts.similarity("kitten", "sitting", SimilarityMethod.LEVENSHTEIN)
        assert result.method is SimilarityMethod.LEVENSHTEIN
        assert result.score == approx(ts.levenshtein("kitten", "sitting"))

    def test_texts_stored_in_result(self):
        result = ts.similarity("alpha", "beta", SimilarityMethod.DICE)
        assert result.text_a == "alpha"
        assert result.text_b == "beta"

    def test_overlap_dispatch(self):
        result = ts.similarity("a b c", "a b", SimilarityMethod.OVERLAP)
        assert result.method is SimilarityMethod.OVERLAP

    def test_score_in_range(self):
        for method in SimilarityMethod:
            result = ts.similarity("quick fox", "lazy dog", method)
            assert 0.0 <= result.score <= 1.0, f"Out of range for {method}"


# ---------------------------------------------------------------------------
# TestMostSimilar
# ---------------------------------------------------------------------------

class TestMostSimilar:
    CANDIDATES = [
        "the cat sat on the mat",      # 0
        "the dog lay on the rug",       # 1
        "a cat and a dog",              # 2
        "completely unrelated words",   # 3
        "cat cat cat",                  # 4
    ]

    def test_returns_list_of_tuples(self):
        results = ts.most_similar("cat mat", self.CANDIDATES)
        assert isinstance(results, list)
        assert all(isinstance(r, tuple) and len(r) == 2 for r in results)

    def test_sorted_descending(self):
        results = ts.most_similar("cat mat", self.CANDIDATES)
        scores = [r[1] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_top_k_limits_results(self):
        results = ts.most_similar("cat mat", self.CANDIDATES, top_k=2)
        assert len(results) == 2

    def test_top_k_larger_than_candidates(self):
        results = ts.most_similar("cat mat", self.CANDIDATES, top_k=100)
        assert len(results) == len(self.CANDIDATES)

    def test_empty_candidates(self):
        results = ts.most_similar("cat mat", [])
        assert results == []

    def test_indices_are_valid(self):
        results = ts.most_similar("cat mat", self.CANDIDATES)
        for idx, score in results:
            assert 0 <= idx < len(self.CANDIDATES)

    def test_default_method_cosine(self):
        # Just verify it runs without error with default method
        results = ts.most_similar("cat", self.CANDIDATES)
        assert len(results) > 0

    def test_jaccard_method(self):
        results = ts.most_similar("cat mat", self.CANDIDATES, method=SimilarityMethod.JACCARD)
        scores = [r[1] for r in results]
        assert scores == sorted(scores, reverse=True)


# ---------------------------------------------------------------------------
# TestAllSimilarities
# ---------------------------------------------------------------------------

class TestAllSimilarities:
    def test_returns_dict(self):
        result = ts.all_similarities("hello world", "hello python")
        assert isinstance(result, dict)

    def test_all_five_methods_present(self):
        result = ts.all_similarities("hello world", "hello python")
        assert set(result.keys()) == set(SimilarityMethod)

    def test_all_scores_in_range(self):
        result = ts.all_similarities("the quick brown fox", "the slow red fox")
        for method, score in result.items():
            assert 0.0 <= score <= 1.0, f"Score out of range for {method}"

    def test_identical_texts_high_scores(self):
        result = ts.all_similarities("knowledge graph", "knowledge graph")
        for method, score in result.items():
            assert score == approx(1.0), f"Expected 1.0 for {method}, got {score}"

    def test_values_match_direct_methods(self):
        a, b = "agent memory system", "memory retrieval agent"
        result = ts.all_similarities(a, b)
        assert result[SimilarityMethod.JACCARD] == approx(ts.jaccard(a, b))
        assert result[SimilarityMethod.COSINE] == approx(ts.cosine(a, b))
        assert result[SimilarityMethod.OVERLAP] == approx(ts.overlap(a, b))
        assert result[SimilarityMethod.LEVENSHTEIN] == approx(ts.levenshtein(a, b))
        assert result[SimilarityMethod.DICE] == approx(ts.dice(a, b))


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_single_word_identical(self):
        for method in SimilarityMethod:
            result = ts.similarity("hello", "hello", method)
            if method is not SimilarityMethod.LEVENSHTEIN:
                # word-set methods give 1.0
                assert result.score == approx(1.0), f"Expected 1.0 for {method}"

    def test_single_word_different(self):
        for method in (
            SimilarityMethod.JACCARD,
            SimilarityMethod.COSINE,
            SimilarityMethod.OVERLAP,
            SimilarityMethod.DICE,
        ):
            score = ts.similarity("cat", "dog", method).score
            assert score == approx(0.0), f"Expected 0.0 for {method}"

    def test_both_empty_all_methods(self):
        result = ts.all_similarities("", "")
        # levenshtein: 1.0; others: 0.0
        assert result[SimilarityMethod.LEVENSHTEIN] == approx(1.0)
        assert result[SimilarityMethod.JACCARD] == approx(0.0)
        assert result[SimilarityMethod.COSINE] == approx(0.0)
        assert result[SimilarityMethod.OVERLAP] == approx(0.0)
        assert result[SimilarityMethod.DICE] == approx(0.0)

    def test_one_empty_all_word_methods(self):
        for method in (
            SimilarityMethod.JACCARD,
            SimilarityMethod.COSINE,
            SimilarityMethod.OVERLAP,
            SimilarityMethod.DICE,
        ):
            assert ts.similarity("hello world", "", method).score == approx(0.0)
            assert ts.similarity("", "hello world", method).score == approx(0.0)

    def test_one_empty_levenshtein(self):
        # one non-empty → 0.0
        assert ts.levenshtein("", "abc") == approx(0.0)
        assert ts.levenshtein("abc", "") == approx(0.0)

    def test_identical_long_text(self):
        text = "the quick brown fox jumps over the lazy dog " * 10
        assert ts.jaccard(text, text) == approx(1.0)
        assert ts.cosine(text, text) == approx(1.0)
        assert ts.dice(text, text) == approx(1.0)
        assert ts.overlap(text, text) == approx(1.0)

    def test_punctuation_ignored(self):
        # punctuation not matched by \b\w+\b
        assert ts.jaccard("hello, world!", "hello world") == approx(1.0)

    def test_numbers_as_tokens(self):
        # digits are word chars
        score = ts.jaccard("2024 report", "2024 analysis")
        assert 0.0 < score < 1.0
