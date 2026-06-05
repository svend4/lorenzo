"""Tests for E175 doc_tagger module."""
from __future__ import annotations

import pytest

from docstoolkit.doc_tagger import DocTagger, TaggerConfig, TagRule, TaggingResult


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestTagRule:
    def test_defaults(self):
        rule = TagRule(tag="python")
        assert rule.tag == "python"
        assert rule.keywords == []
        assert rule.patterns == []
        assert rule.min_matches == 1
        assert rule.excluded_keywords == []

    def test_with_values(self):
        rule = TagRule(
            tag="ml",
            keywords=["neural", "model"],
            patterns=[r"\bRAG\b"],
            min_matches=2,
            excluded_keywords=["spam"],
        )
        assert rule.keywords == ["neural", "model"]
        assert rule.patterns == [r"\bRAG\b"]
        assert rule.min_matches == 2
        assert rule.excluded_keywords == ["spam"]

    def test_independent_default_lists(self):
        r1 = TagRule(tag="a")
        r2 = TagRule(tag="b")
        r1.keywords.append("x")
        assert r2.keywords == []


class TestTaggingResult:
    def test_construction(self):
        result = TaggingResult(
            doc_id="d1",
            tags=["a", "b"],
            matched_rules=["a", "b"],
            score_by_tag={"a": 1, "b": 2},
        )
        assert result.doc_id == "d1"
        assert result.tags == ["a", "b"]
        assert result.matched_rules == ["a", "b"]
        assert result.score_by_tag == {"a": 1, "b": 2}


class TestTaggerConfig:
    def test_defaults(self):
        cfg = TaggerConfig()
        assert cfg.case_sensitive is False
        assert cfg.whole_word is True
        assert cfg.max_tags == 0

    def test_custom(self):
        cfg = TaggerConfig(case_sensitive=True, whole_word=False, max_tags=3)
        assert cfg.case_sensitive is True
        assert cfg.whole_word is False
        assert cfg.max_tags == 3


# ---------------------------------------------------------------------------
# Rule management
# ---------------------------------------------------------------------------


class TestAddRule:
    def test_add_single(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="python", keywords=["python"]))
        assert t.rule_count == 1
        assert "python" in t.tags_supported

    def test_replace_existing(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="python", keywords=["python"]))
        t.add_rule(TagRule(tag="python", keywords=["py"]))
        assert t.rule_count == 1

    def test_add_rule_type_error(self):
        t = DocTagger()
        with pytest.raises(TypeError):
            t.add_rule("not-a-rule")  # type: ignore[arg-type]

    def test_add_rule_empty_tag(self):
        t = DocTagger()
        with pytest.raises(ValueError):
            t.add_rule(TagRule(tag="", keywords=["x"]))


class TestAddRules:
    def test_add_many(self):
        t = DocTagger()
        t.add_rules(
            [
                TagRule(tag="a", keywords=["a"]),
                TagRule(tag="b", keywords=["b"]),
                TagRule(tag="c", keywords=["c"]),
            ]
        )
        assert t.rule_count == 3

    def test_add_empty_list(self):
        t = DocTagger()
        t.add_rules([])
        assert t.rule_count == 0


class TestRemoveRule:
    def test_remove_existing(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="python", keywords=["python"]))
        assert t.remove_rule("python") is True
        assert t.rule_count == 0

    def test_remove_missing(self):
        t = DocTagger()
        assert t.remove_rule("nope") is False


# ---------------------------------------------------------------------------
# Tagging behaviour
# ---------------------------------------------------------------------------


class TestTagBasic:
    def test_keyword_match(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="python", keywords=["python"]))
        result = t.tag("I love python", doc_id="d1")
        assert result.tags == ["python"]
        assert result.matched_rules == ["python"]
        assert result.score_by_tag == {"python": 1}
        assert result.doc_id == "d1"

    def test_no_match(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="python", keywords=["python"]))
        result = t.tag("nothing here")
        assert result.tags == []
        assert result.score_by_tag == {}

    def test_multiple_tags(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="python", keywords=["python"]))
        t.add_rule(TagRule(tag="ml", keywords=["model"]))
        result = t.tag("python model")
        assert result.tags == ["ml", "python"]

    def test_unique_keywords_counted_once(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="python", keywords=["python"]))
        # 3 occurrences but only one unique keyword -> score 1
        result = t.tag("python python python")
        assert result.score_by_tag["python"] == 1

    def test_tags_sorted(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="zzz", keywords=["foo"]))
        t.add_rule(TagRule(tag="aaa", keywords=["bar"]))
        result = t.tag("foo bar")
        assert result.tags == ["aaa", "zzz"]

    def test_default_doc_id(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="x", keywords=["x"]))
        assert t.tag("x").doc_id == "doc"


class TestTagPatterns:
    def test_regex_match(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="version", patterns=[r"v\d+\.\d+"]))
        result = t.tag("release v1.2 and v3.4")
        assert result.tags == ["version"]
        assert result.score_by_tag["version"] == 2

    def test_keyword_plus_pattern(self):
        t = DocTagger()
        t.add_rule(
            TagRule(tag="api", keywords=["api"], patterns=[r"/v\d+/"])
        )
        result = t.tag("the api at /v1/ and /v2/")
        # 1 unique keyword + 2 pattern hits
        assert result.score_by_tag["api"] == 3

    def test_pattern_no_match(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="x", patterns=[r"\d{5}"]))
        result = t.tag("only words")
        assert result.tags == []

    def test_invalid_pattern_skipped(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="x", patterns=["[unclosed", r"valid"], keywords=[]))
        # Should not raise. "valid" still matches.
        result = t.tag("this is valid text")
        assert "x" in result.tags


class TestTagMinMatches:
    def test_below_threshold(self):
        t = DocTagger()
        t.add_rule(
            TagRule(tag="ml", keywords=["model", "neural", "loss"], min_matches=2)
        )
        result = t.tag("only model here")
        assert result.tags == []

    def test_at_threshold(self):
        t = DocTagger()
        t.add_rule(
            TagRule(tag="ml", keywords=["model", "neural", "loss"], min_matches=2)
        )
        result = t.tag("model and neural network")
        assert result.tags == ["ml"]
        assert result.score_by_tag["ml"] == 2

    def test_above_threshold(self):
        t = DocTagger()
        t.add_rule(
            TagRule(tag="ml", keywords=["model", "neural", "loss"], min_matches=2)
        )
        result = t.tag("model neural loss everywhere")
        assert result.score_by_tag["ml"] == 3


class TestTagExcluded:
    def test_excluded_blocks_rule(self):
        t = DocTagger()
        t.add_rule(
            TagRule(
                tag="python",
                keywords=["python"],
                excluded_keywords=["snake"],
            )
        )
        result = t.tag("python the snake")
        assert result.tags == []

    def test_excluded_not_present(self):
        t = DocTagger()
        t.add_rule(
            TagRule(
                tag="python",
                keywords=["python"],
                excluded_keywords=["snake"],
            )
        )
        result = t.tag("python rocks")
        assert result.tags == ["python"]

    def test_excluded_only_for_one_rule(self):
        t = DocTagger()
        t.add_rule(
            TagRule(tag="python", keywords=["python"], excluded_keywords=["snake"])
        )
        t.add_rule(TagRule(tag="reptile", keywords=["snake"]))
        result = t.tag("python the snake")
        assert "python" not in result.tags
        assert "reptile" in result.tags


class TestTagWholeWord:
    def test_whole_word_default(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="cat", keywords=["cat"]))
        # "category" should not match the keyword "cat"
        result = t.tag("category and concatenation")
        assert result.tags == []

    def test_whole_word_match(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="cat", keywords=["cat"]))
        result = t.tag("the cat sat")
        assert result.tags == ["cat"]

    def test_substring_mode(self):
        t = DocTagger(TaggerConfig(whole_word=False))
        t.add_rule(TagRule(tag="cat", keywords=["cat"]))
        result = t.tag("category")
        assert result.tags == ["cat"]


class TestTagCaseSensitive:
    def test_default_case_insensitive(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="python", keywords=["Python"]))
        result = t.tag("PYTHON rules")
        assert result.tags == ["python"]

    def test_case_sensitive_no_match(self):
        t = DocTagger(TaggerConfig(case_sensitive=True))
        t.add_rule(TagRule(tag="python", keywords=["Python"]))
        result = t.tag("python rules")
        assert result.tags == []

    def test_case_sensitive_match(self):
        t = DocTagger(TaggerConfig(case_sensitive=True))
        t.add_rule(TagRule(tag="python", keywords=["Python"]))
        result = t.tag("Python rules")
        assert result.tags == ["python"]

    def test_case_sensitive_regex(self):
        t = DocTagger(TaggerConfig(case_sensitive=True))
        t.add_rule(TagRule(tag="ver", patterns=[r"V\d"]))
        result = t.tag("v1 and V2")
        assert result.score_by_tag["ver"] == 1


class TestTagBatch:
    def test_batch(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="python", keywords=["python"]))
        t.add_rule(TagRule(tag="ml", keywords=["model"]))
        results = t.tag_batch(
            {
                "d1": "python rocks",
                "d2": "model training",
                "d3": "python model",
                "d4": "nothing",
            }
        )
        assert len(results) == 4
        by_id = {r.doc_id: r for r in results}
        assert by_id["d1"].tags == ["python"]
        assert by_id["d2"].tags == ["ml"]
        assert by_id["d3"].tags == ["ml", "python"]
        assert by_id["d4"].tags == []

    def test_batch_empty(self):
        t = DocTagger()
        assert t.tag_batch({}) == []

    def test_batch_preserves_doc_ids(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="t", keywords=["x"]))
        results = t.tag_batch({"alpha": "x", "beta": "x"})
        ids = {r.doc_id for r in results}
        assert ids == {"alpha", "beta"}


# ---------------------------------------------------------------------------
# Existing-tag helpers
# ---------------------------------------------------------------------------


class TestExtractExistingTags:
    def test_basic(self):
        t = DocTagger()
        assert t.extract_existing_tags("hello #python #ml world") == ["ml", "python"]

    def test_no_tags(self):
        t = DocTagger()
        assert t.extract_existing_tags("nothing here") == []

    def test_empty(self):
        t = DocTagger()
        assert t.extract_existing_tags("") == []

    def test_duplicates_unique(self):
        t = DocTagger()
        assert t.extract_existing_tags("#a #a #b") == ["a", "b"]

    def test_ignores_in_word(self):
        t = DocTagger()
        # "abc#def" should not yield "def"
        assert t.extract_existing_tags("abc#def") == []

    def test_hyphen_and_underscore(self):
        t = DocTagger()
        assert t.extract_existing_tags("#multi-word #snake_case") == [
            "multi-word",
            "snake_case",
        ]


class TestMergeTags:
    def test_union(self):
        t = DocTagger()
        assert t.merge_tags(["a", "b"], ["b", "c"]) == ["a", "b", "c"]

    def test_empty(self):
        t = DocTagger()
        assert t.merge_tags([], []) == []

    def test_one_empty(self):
        t = DocTagger()
        assert t.merge_tags(["x"], []) == ["x"]
        assert t.merge_tags([], ["y"]) == ["y"]

    def test_sorted(self):
        t = DocTagger()
        assert t.merge_tags(["zz", "aa"], ["mm"]) == ["aa", "mm", "zz"]


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidateRule:
    def test_valid(self):
        t = DocTagger()
        ok, errs = t.validate_rule(TagRule(tag="python", keywords=["py"]))
        assert ok is True
        assert errs == []

    def test_empty_tag(self):
        t = DocTagger()
        ok, errs = t.validate_rule(TagRule(tag="", keywords=["x"]))
        assert ok is False
        assert any("tag" in e for e in errs)

    def test_no_keywords_no_patterns(self):
        t = DocTagger()
        ok, errs = t.validate_rule(TagRule(tag="x"))
        assert ok is False
        assert any("keyword" in e or "pattern" in e for e in errs)

    def test_min_matches_zero(self):
        t = DocTagger()
        ok, errs = t.validate_rule(
            TagRule(tag="x", keywords=["x"], min_matches=0)
        )
        assert ok is False
        assert any("min_matches" in e for e in errs)

    def test_bad_regex(self):
        t = DocTagger()
        ok, errs = t.validate_rule(TagRule(tag="x", patterns=["[bad"]))
        assert ok is False
        assert any("regex" in e for e in errs)

    def test_not_a_tagrule(self):
        t = DocTagger()
        ok, errs = t.validate_rule("hi")  # type: ignore[arg-type]
        assert ok is False
        assert errs


# ---------------------------------------------------------------------------
# Max tags
# ---------------------------------------------------------------------------


class TestMaxTags:
    def test_unlimited(self):
        t = DocTagger(TaggerConfig(max_tags=0))
        t.add_rule(TagRule(tag="a", keywords=["a"]))
        t.add_rule(TagRule(tag="b", keywords=["b"]))
        t.add_rule(TagRule(tag="c", keywords=["c"]))
        result = t.tag("a b c")
        assert len(result.tags) == 3

    def test_limits_results(self):
        t = DocTagger(TaggerConfig(max_tags=2))
        t.add_rule(TagRule(tag="a", keywords=["a"]))
        t.add_rule(TagRule(tag="b", keywords=["b"]))
        t.add_rule(TagRule(tag="c", keywords=["c"]))
        result = t.tag("a b c")
        assert len(result.tags) == 2

    def test_keeps_top_scoring(self):
        t = DocTagger(TaggerConfig(max_tags=1))
        t.add_rule(TagRule(tag="rare", keywords=["rare"]))
        t.add_rule(TagRule(tag="common", patterns=[r"x"]))
        # "x x x" => 3 pattern hits; "rare" => 1 keyword hit -> common kept.
        result = t.tag("rare x x x")
        assert result.tags == ["common"]
        assert result.score_by_tag == {"common": 3}

    def test_max_tags_under_match_count(self):
        t = DocTagger(TaggerConfig(max_tags=10))
        t.add_rule(TagRule(tag="a", keywords=["a"]))
        result = t.tag("a")
        assert result.tags == ["a"]


# ---------------------------------------------------------------------------
# Misc properties
# ---------------------------------------------------------------------------


class TestRuleCount:
    def test_starts_zero(self):
        assert DocTagger().rule_count == 0

    def test_increments(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="x", keywords=["x"]))
        assert t.rule_count == 1
        t.add_rule(TagRule(tag="y", keywords=["y"]))
        assert t.rule_count == 2

    def test_decrements(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="x", keywords=["x"]))
        t.remove_rule("x")
        assert t.rule_count == 0


class TestTagsSupported:
    def test_empty(self):
        assert DocTagger().tags_supported == []

    def test_sorted(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="zz", keywords=["a"]))
        t.add_rule(TagRule(tag="aa", keywords=["b"]))
        assert t.tags_supported == ["aa", "zz"]


class TestClear:
    def test_clear_resets(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="x", keywords=["x"]))
        t.add_rule(TagRule(tag="y", keywords=["y"]))
        t.clear()
        assert t.rule_count == 0
        assert t.tags_supported == []

    def test_clear_idempotent(self):
        t = DocTagger()
        t.clear()
        t.clear()
        assert t.rule_count == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_no_rules(self):
        t = DocTagger()
        result = t.tag("anything goes")
        assert result.tags == []
        assert result.matched_rules == []
        assert result.score_by_tag == {}

    def test_empty_text(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="x", keywords=["x"]))
        result = t.tag("")
        assert result.tags == []

    def test_all_excluded(self):
        t = DocTagger()
        t.add_rule(
            TagRule(
                tag="python",
                keywords=["python"],
                excluded_keywords=["snake"],
            )
        )
        t.add_rule(
            TagRule(tag="ml", keywords=["model"], excluded_keywords=["spam"])
        )
        result = t.tag("python snake model spam")
        assert result.tags == []

    def test_empty_keyword_string_ignored(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="x", keywords=["", "foo"]))
        result = t.tag("foo bar")
        assert result.tags == ["x"]
        assert result.score_by_tag["x"] == 1

    def test_returns_tagging_result_instance(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="x", keywords=["x"]))
        assert isinstance(t.tag("x"), TaggingResult)

    def test_score_by_tag_only_for_matched(self):
        t = DocTagger()
        t.add_rule(TagRule(tag="a", keywords=["a"]))
        t.add_rule(TagRule(tag="b", keywords=["b"]))
        result = t.tag("only a here")
        assert "a" in result.score_by_tag
        assert "b" not in result.score_by_tag
