"""Tests for docstoolkit.text_normalizer â target: >= 72 tests."""
from __future__ import annotations

import re

import pytest

from docstoolkit.text_normalizer import (
    NormPipeline,
    NormRule,
    NormStep,
    NormalizerConfig,
    TextNormalizer,
    case_rules,
    number_rules,
    punctuation_rules,
    whitespace_rules,
)


# ===========================================================================
# NormRule.apply â basic regex substitution
# ===========================================================================

class TestNormRuleApply:
    def test_simple_substitution(self):
        rule = NormRule(name="r", pattern=r"foo", replacement="bar")
        assert rule.apply("foo baz foo") == "bar baz bar"

    def test_no_match_returns_original(self):
        rule = NormRule(name="r", pattern=r"xyz", replacement="ABC")
        assert rule.apply("hello world") == "hello world"

    def test_empty_string_input(self):
        rule = NormRule(name="r", pattern=r"\s+", replacement=" ")
        assert rule.apply("") == ""

    def test_group_reference_in_replacement(self):
        rule = NormRule(name="r", pattern=r"(\w+)", replacement=r"[\1]")
        assert rule.apply("hi") == "[hi]"

    def test_flag_ignorecase(self):
        rule = NormRule(name="r", pattern=r"hello", replacement="HI", flags=re.IGNORECASE)
        assert rule.apply("HELLO world") == "HI world"

    def test_flag_ignorecase_no_flag_does_not_match(self):
        rule = NormRule(name="r", pattern=r"hello", replacement="HI")
        assert rule.apply("HELLO world") == "HELLO world"

    def test_multiline_flag(self):
        rule = NormRule(name="r", pattern=r"^x", replacement="Y", flags=re.MULTILINE)
        assert rule.apply("x\nx") == "Y\nY"

    def test_callable_replacement(self):
        rule = NormRule(name="r", pattern=r"[A-Z]+", replacement=lambda m: m.group(0).lower())
        assert rule.apply("Hello WORLD") == "hello world"

    def test_replace_digits(self):
        rule = NormRule(name="r", pattern=r"\d+", replacement="N")
        assert rule.apply("a1b22c333") == "aNbNcN"

    def test_description_field_stored(self):
        rule = NormRule(name="r", pattern=r"x", replacement="y", description="desc")
        assert rule.description == "desc"

    def test_flags_default_zero(self):
        rule = NormRule(name="r", pattern=r"x", replacement="y")
        assert rule.flags == 0

    def test_apply_returns_str(self):
        rule = NormRule(name="r", pattern=r".", replacement="a")
        assert isinstance(rule.apply("bc"), str)


# ===========================================================================
# whitespace_rules
# ===========================================================================

class TestWhitespaceRules:
    def _apply_all(self, text: str) -> str:
        for rule in whitespace_rules():
            text = rule.apply(text)
        return text

    def test_collapse_multiple_spaces(self):
        assert self._apply_all("a   b") == "a b"

    def test_collapse_tabs(self):
        assert self._apply_all("a\t\tb") == "a b"

    def test_strip_leading_spaces(self):
        assert self._apply_all("   hello") == "hello"

    def test_strip_trailing_spaces(self):
        assert self._apply_all("hello   ") == "hello"

    def test_normalize_crlf(self):
        assert self._apply_all("a\r\nb") == "a\nb"

    def test_normalize_cr(self):
        assert self._apply_all("a\rb") == "a\nb"

    def test_collapse_blank_lines(self):
        result = self._apply_all("a\n\n\n\nb")
        assert result == "a\n\nb"

    def test_two_newlines_preserved(self):
        result = self._apply_all("a\n\nb")
        assert result == "a\n\nb"

    def test_strip_leading_newlines(self):
        result = self._apply_all("\n\nhello")
        assert result == "hello"

    def test_strip_trailing_newlines(self):
        result = self._apply_all("hello\n\n")
        assert result == "hello"

    def test_multiline_strip_per_line(self):
        result = self._apply_all("  line1  \n  line2  ")
        assert result == "line1\nline2"

    def test_returns_five_rules(self):
        assert len(whitespace_rules()) == 5

    def test_already_normalized_unchanged(self):
        text = "hello world"
        assert self._apply_all(text) == text

    def test_only_whitespace_becomes_empty(self):
        assert self._apply_all("   \n  \n  ") == ""

    def test_mixed_spaces_and_tabs_collapsed(self):
        assert self._apply_all("a \t b") == "a b"


# ===========================================================================
# punctuation_rules
# ===========================================================================

class TestPunctuationRules:
    def _apply_all(self, text: str) -> str:
        for rule in punctuation_rules():
            text = rule.apply(text)
        return text

    def test_em_dash_to_hyphen(self):
        assert self._apply_all("word\u2014word") == "word-word"

    def test_en_dash_to_hyphen(self):
        assert self._apply_all("word\u2013word") == "word-word"

    def test_curly_double_quotes(self):
        # U+201C LEFT DOUBLE QUOTATION MARK, U+201D RIGHT DOUBLE QUOTATION MARK
        curly = "\u201chello\u201d"
        assert self._apply_all(curly) == "\"hello\""

    def test_guillemet_quotes(self):
        assert self._apply_all("\u00abhello\u00bb") == "\"hello\""

    def test_low9_quote(self):
        assert self._apply_all("\u201ehello") == "\"hello"

    def test_curly_single_quote(self):
        # U+2018 LEFT SINGLE QUOTATION MARK, U+2019 RIGHT SINGLE QUOTATION MARK
        curly = "\u2018hi\u2019"
        assert self._apply_all(curly) == "'hi'"

    def test_backtick_to_apostrophe(self):
        assert self._apply_all("`code`") == "'code'"

    def test_ellipsis_char_to_dots(self):
        assert self._apply_all("wait\u2026") == "wait..."

    def test_trailing_dot_after_word_before_space(self):
        assert self._apply_all("word. next") == "word next"

    def test_trailing_dot_after_word_at_end(self):
        assert self._apply_all("word.") == "word"

    def test_returns_five_rules(self):
        assert len(punctuation_rules()) == 5

    def test_ascii_hyphen_unchanged(self):
        assert self._apply_all("a-b") == "a-b"

    def test_multiple_dashes(self):
        result = self._apply_all("a\u2014b\u2013c")
        assert result == "a-b-c"


# ===========================================================================
# case_rules
# ===========================================================================

class TestCaseRules:
    def _apply_all(self, text: str) -> str:
        for rule in case_rules():
            text = rule.apply(text)
        return text

    def test_uppercase_to_lower(self):
        assert self._apply_all("HELLO") == "hello"

    def test_mixed_case_to_lower(self):
        assert self._apply_all("Hello World") == "hello world"

    def test_already_lower_unchanged(self):
        assert self._apply_all("hello world") == "hello world"

    def test_cyrillic_uppercase(self):
        # \u041f\u0420\u0418\u0412\u0415\u0422 = PRIVET in Cyrillic uppercase
        assert self._apply_all("\u041f\u0420\u0418\u0412\u0415\u0422") == "\u043f\u0440\u0438\u0432\u0435\u0442"

    def test_numbers_unchanged(self):
        assert self._apply_all("ABC123") == "abc123"

    def test_punctuation_unchanged(self):
        assert self._apply_all("HELLO!") == "hello!"

    def test_returns_one_rule(self):
        assert len(case_rules()) == 1

    def test_empty_string(self):
        assert self._apply_all("") == ""


# ===========================================================================
# number_rules
# ===========================================================================

class TestNumberRules:
    def _apply_all(self, text: str) -> str:
        for rule in number_rules():
            text = rule.apply(text)
        return text

    def test_integer_replaced(self):
        assert self._apply_all("there are 42 items") == "there are [NUM] items"

    def test_float_replaced(self):
        assert self._apply_all("price is 3.14") == "price is [NUM]"

    def test_float_before_integer(self):
        # 3.14 should become one [NUM], not [NUM].[NUM]
        assert self._apply_all("3.14") == "[NUM]"

    def test_multiple_integers(self):
        assert self._apply_all("1 and 2") == "[NUM] and [NUM]"

    def test_number_inside_word_unchanged(self):
        # "model3": 3 is adjacent to \w char, so no word boundary before it
        assert self._apply_all("model3") == "model3"

    def test_returns_two_rules(self):
        assert len(number_rules()) == 2

    def test_zero_replaced(self):
        assert self._apply_all("value is 0") == "value is [NUM]"

    def test_large_integer(self):
        assert self._apply_all("1000000 users") == "[NUM] users"

    def test_empty_string(self):
        assert self._apply_all("") == ""

    def test_text_without_numbers(self):
        assert self._apply_all("hello world") == "hello world"


# ===========================================================================
# TextNormalizer â config flags independently
# ===========================================================================

class TestTextNormalizerFlags:
    def test_default_config_applies_whitespace(self):
        tn = TextNormalizer()
        assert tn.normalize("a   b") == "a b"

    def test_default_config_no_punctuation(self):
        tn = TextNormalizer()
        # em-dash should NOT be touched with default config
        assert tn.normalize("a\u2014b") == "a\u2014b"

    def test_default_config_no_case(self):
        tn = TextNormalizer()
        assert tn.normalize("HELLO") == "HELLO"

    def test_default_config_no_numbers(self):
        tn = TextNormalizer()
        assert tn.normalize("42 items") == "42 items"

    def test_apply_punctuation_flag(self):
        cfg = NormalizerConfig(apply_whitespace=False, apply_punctuation=True)
        tn = TextNormalizer(cfg)
        assert tn.normalize("a\u2014b") == "a-b"

    def test_apply_case_flag(self):
        cfg = NormalizerConfig(apply_whitespace=False, apply_case=True)
        tn = TextNormalizer(cfg)
        assert tn.normalize("HELLO") == "hello"

    def test_apply_numbers_flag(self):
        cfg = NormalizerConfig(apply_whitespace=False, apply_numbers=True)
        tn = TextNormalizer(cfg)
        assert tn.normalize("42 items") == "[NUM] items"

    def test_all_flags_off(self):
        cfg = NormalizerConfig(
            apply_whitespace=False,
            apply_punctuation=False,
            apply_case=False,
            apply_numbers=False,
        )
        tn = TextNormalizer(cfg)
        text = "  HELLO  42  "
        assert tn.normalize(text) == text

    def test_none_config_uses_default(self):
        tn = TextNormalizer(None)
        assert tn.normalize("a   b") == "a b"


# ===========================================================================
# TextNormalizer â combinations
# ===========================================================================

class TestTextNormalizerCombinations:
    def test_whitespace_and_case(self):
        cfg = NormalizerConfig(apply_whitespace=True, apply_case=True)
        tn = TextNormalizer(cfg)
        result = tn.normalize("  HELLO   WORLD  ")
        assert result == "hello world"

    def test_whitespace_and_numbers(self):
        cfg = NormalizerConfig(apply_whitespace=True, apply_numbers=True)
        tn = TextNormalizer(cfg)
        result = tn.normalize("  42   items  ")
        assert result == "[NUM] items"

    def test_all_flags_on(self):
        cfg = NormalizerConfig(
            apply_whitespace=True,
            apply_punctuation=True,
            apply_case=True,
            apply_numbers=True,
        )
        tn = TextNormalizer(cfg)
        result = tn.normalize("  HELLO\u2014WORLD  42  ")
        assert result == "hello-world [NUM]"

    def test_order_whitespace_before_case(self):
        cfg = NormalizerConfig(apply_whitespace=True, apply_case=True)
        tn = TextNormalizer(cfg)
        assert tn.normalize("  A  B  ") == "a b"


# ===========================================================================
# TextNormalizer â normalize_batch, add_rule, active_rules
# ===========================================================================

class TestTextNormalizerBatchAndRules:
    def test_normalize_batch_basic(self):
        tn = TextNormalizer()
        results = tn.normalize_batch(["a   b", "c   d"])
        assert results == ["a b", "c d"]

    def test_normalize_batch_empty_list(self):
        tn = TextNormalizer()
        assert tn.normalize_batch([]) == []

    def test_normalize_batch_preserves_order(self):
        tn = TextNormalizer()
        inputs = ["  z  ", "  a  ", "  m  "]
        assert tn.normalize_batch(inputs) == ["z", "a", "m"]

    def test_add_rule_affects_normalize(self):
        tn = TextNormalizer(NormalizerConfig(apply_whitespace=False))
        tn.add_rule(NormRule(name="bang", pattern=r"!", replacement="?"))
        assert tn.normalize("hello!") == "hello?"

    def test_add_multiple_rules_applied_in_order(self):
        tn = TextNormalizer(NormalizerConfig(apply_whitespace=False))
        tn.add_rule(NormRule(name="a_to_b", pattern=r"a", replacement="b"))
        tn.add_rule(NormRule(name="b_to_c", pattern=r"b", replacement="c"))
        assert tn.normalize("a") == "c"

    def test_active_rules_default_config(self):
        tn = TextNormalizer()
        rules = tn.active_rules()
        names = [r.name for r in rules]
        assert "collapse_spaces" in names

    def test_active_rules_excludes_disabled(self):
        cfg = NormalizerConfig(apply_whitespace=False, apply_case=True)
        tn = TextNormalizer(cfg)
        names = [r.name for r in tn.active_rules()]
        assert "collapse_spaces" not in names
        assert "lowercase_all" in names

    def test_active_rules_includes_custom(self):
        tn = TextNormalizer(NormalizerConfig(apply_whitespace=False))
        custom = NormRule(name="my_rule", pattern=r"x", replacement="y")
        tn.add_rule(custom)
        assert custom in tn.active_rules()

    def test_active_rules_returns_list(self):
        tn = TextNormalizer()
        assert isinstance(tn.active_rules(), list)


# ===========================================================================
# NormPipeline
# ===========================================================================

class TestNormPipeline:
    def _ws_normalizer(self):
        return TextNormalizer()

    def _case_normalizer(self):
        return TextNormalizer(NormalizerConfig(apply_whitespace=False, apply_case=True))

    def test_single_step(self):
        pipeline = NormPipeline([NormStep("ws", self._ws_normalizer())])
        assert pipeline.run("a   b") == "a b"

    def test_multiple_steps_order_matters(self):
        pipeline = NormPipeline([
            NormStep("ws", self._ws_normalizer()),
            NormStep("case", self._case_normalizer()),
        ])
        assert pipeline.run("  HELLO   WORLD  ") == "hello world"

    def test_order_matters_reverse(self):
        pipeline = NormPipeline([
            NormStep("case", self._case_normalizer()),
            NormStep("ws", self._ws_normalizer()),
        ])
        assert pipeline.run("  HELLO   WORLD  ") == "hello world"

    def test_empty_pipeline_returns_input(self):
        pipeline = NormPipeline()
        assert pipeline.run("hello world") == "hello world"

    def test_empty_pipeline_empty_string(self):
        pipeline = NormPipeline()
        assert pipeline.run("") == ""

    def test_add_step(self):
        pipeline = NormPipeline()
        pipeline.add_step(NormStep("ws", self._ws_normalizer()))
        assert pipeline.run("a   b") == "a b"

    def test_step_names_empty(self):
        pipeline = NormPipeline()
        assert pipeline.step_names() == []

    def test_step_names_single(self):
        pipeline = NormPipeline([NormStep("ws", self._ws_normalizer())])
        assert pipeline.step_names() == ["ws"]

    def test_step_names_multiple(self):
        pipeline = NormPipeline([
            NormStep("ws", self._ws_normalizer()),
            NormStep("case", self._case_normalizer()),
        ])
        assert pipeline.step_names() == ["ws", "case"]

    def test_run_batch(self):
        pipeline = NormPipeline([NormStep("ws", self._ws_normalizer())])
        results = pipeline.run_batch(["a   b", "c   d"])
        assert results == ["a b", "c d"]

    def test_run_batch_empty_list(self):
        pipeline = NormPipeline([NormStep("ws", self._ws_normalizer())])
        assert pipeline.run_batch([]) == []

    def test_run_batch_preserves_order(self):
        pipeline = NormPipeline([NormStep("ws", self._ws_normalizer())])
        inputs = ["  z  ", "  a  "]
        assert pipeline.run_batch(inputs) == ["z", "a"]

    def test_init_with_none_steps(self):
        pipeline = NormPipeline(None)
        assert pipeline.step_names() == []

    def test_add_step_returns_none(self):
        pipeline = NormPipeline()
        result = pipeline.add_step(NormStep("ws", self._ws_normalizer()))
        assert result is None


# ===========================================================================
# Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_normalize_empty_string_default(self):
        tn = TextNormalizer()
        assert tn.normalize("") == ""

    def test_normalize_only_whitespace(self):
        tn = TextNormalizer()
        assert tn.normalize("   \t  \n  ") == ""

    def test_normalize_already_normalized_text(self):
        tn = TextNormalizer()
        text = "hello world"
        assert tn.normalize(text) == text

    def test_normalize_single_word(self):
        tn = TextNormalizer()
        assert tn.normalize("hello") == "hello"

    def test_normalize_newline_only(self):
        tn = TextNormalizer()
        assert tn.normalize("\n") == ""

    def test_norm_rule_apply_empty_string(self):
        rule = NormRule(name="r", pattern=r"x", replacement="y")
        assert rule.apply("") == ""

    def test_pipeline_run_empty_string(self):
        pipeline = NormPipeline([NormStep("ws", TextNormalizer())])
        assert pipeline.run("") == ""

    def test_normalize_batch_with_empty_strings(self):
        tn = TextNormalizer()
        assert tn.normalize_batch(["", "a   b", ""]) == ["", "a b", ""]

    def test_custom_rule_on_empty_string(self):
        tn = TextNormalizer(NormalizerConfig(apply_whitespace=False))
        tn.add_rule(NormRule(name="r", pattern=r"x", replacement="y"))
        assert tn.normalize("") == ""

    def test_number_rules_on_empty_string(self):
        cfg = NormalizerConfig(apply_whitespace=False, apply_numbers=True)
        tn = TextNormalizer(cfg)
        assert tn.normalize("") == ""

    def test_unicode_text_whitespace(self):
        tn = TextNormalizer()
        assert tn.normalize("  \u043f\u0440\u0438\u0432\u0435\u0442   \u043c\u0438\u0440  ") == "\u043f\u0440\u0438\u0432\u0435\u0442 \u043c\u0438\u0440"
