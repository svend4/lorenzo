"""Tests for docstoolkit.text_normalizer_v2."""
from __future__ import annotations

import unicodedata

import pytest

from docstoolkit.text_normalizer_v2 import (
    NormalizationConfig,
    NormalizationResult,
    NormalizationRule,
    TextNormalizer,
)


# ---------------------------------------------------------------------------
# NormalizationRule
# ---------------------------------------------------------------------------
class TestNormalizationRule:
    def test_has_unicode_forms(self):
        assert NormalizationRule.NFC.value == "NFC"
        assert NormalizationRule.NFKC.value == "NFKC"
        assert NormalizationRule.NFD.value == "NFD"
        assert NormalizationRule.NFKD.value == "NFKD"

    def test_has_case_rules(self):
        assert NormalizationRule.LOWERCASE.value == "LOWERCASE"
        assert NormalizationRule.UPPERCASE.value == "UPPERCASE"

    def test_has_text_rules(self):
        assert NormalizationRule.STRIP_ACCENTS.value == "STRIP_ACCENTS"
        assert NormalizationRule.COLLAPSE_WHITESPACE.value == "COLLAPSE_WHITESPACE"
        assert NormalizationRule.NORMALIZE_QUOTES.value == "NORMALIZE_QUOTES"
        assert NormalizationRule.NORMALIZE_DASHES.value == "NORMALIZE_DASHES"
        assert NormalizationRule.REMOVE_ZWSP.value == "REMOVE_ZWSP"

    def test_enum_unique(self):
        values = [r.value for r in NormalizationRule]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# NormalizationConfig
# ---------------------------------------------------------------------------
class TestNormalizationConfig:
    def test_defaults(self):
        cfg = NormalizationConfig()
        assert cfg.unicode_form == "NFC"
        assert cfg.lowercase is False
        assert cfg.strip_accents is False
        assert cfg.collapse_whitespace is True
        assert cfg.normalize_quotes is True
        assert cfg.normalize_dashes is True
        assert cfg.remove_zero_width is True
        assert cfg.preserve_newlines is True

    def test_custom(self):
        cfg = NormalizationConfig(
            unicode_form="NFKC",
            lowercase=True,
            strip_accents=True,
            collapse_whitespace=False,
            normalize_quotes=False,
            normalize_dashes=False,
            remove_zero_width=False,
            preserve_newlines=False,
        )
        assert cfg.unicode_form == "NFKC"
        assert cfg.lowercase is True
        assert cfg.strip_accents is True
        assert cfg.collapse_whitespace is False
        assert cfg.normalize_quotes is False
        assert cfg.normalize_dashes is False
        assert cfg.remove_zero_width is False
        assert cfg.preserve_newlines is False

    def test_unicode_form_can_be_empty(self):
        cfg = NormalizationConfig(unicode_form="")
        assert cfg.unicode_form == ""


# ---------------------------------------------------------------------------
# NormalizationResult
# ---------------------------------------------------------------------------
class TestNormalizationResult:
    def test_changed_true(self):
        res = NormalizationResult(original="a b", normalized="ab", rules_applied=["X"])
        assert res.changed is True

    def test_changed_false(self):
        res = NormalizationResult(original="abc", normalized="abc", rules_applied=[])
        assert res.changed is False

    def test_char_diff_positive(self):
        res = NormalizationResult(original="hello  world", normalized="hello world", rules_applied=[])
        assert res.char_diff == 1

    def test_char_diff_zero(self):
        res = NormalizationResult(original="abc", normalized="abc", rules_applied=[])
        assert res.char_diff == 0

    def test_char_diff_when_normalized_longer(self):
        res = NormalizationResult(original="a", normalized="ab", rules_applied=[])
        assert res.char_diff == 1

    def test_rules_applied_default_empty(self):
        res = NormalizationResult(original="x", normalized="x")
        assert res.rules_applied == []


# ---------------------------------------------------------------------------
# unicode_normalize
# ---------------------------------------------------------------------------
class TestUnicodeNormalize:
    def setup_method(self):
        self.n = TextNormalizer()

    def test_nfc(self):
        # "é" as two code points (e + COMBINING ACUTE ACCENT) -> single code point
        decomposed = "é"
        result = self.n.unicode_normalize(decomposed, "NFC")
        assert result == "é"
        assert len(result) == 1

    def test_nfd(self):
        composed = "é"
        result = self.n.unicode_normalize(composed, "NFD")
        assert result == "é"
        assert len(result) == 2

    def test_nfkc_compatibility(self):
        # FULLWIDTH LATIN CAPITAL LETTER A -> "A"
        result = self.n.unicode_normalize("Ａ", "NFKC")
        assert result == "A"

    def test_nfkd_compatibility(self):
        result = self.n.unicode_normalize("Ａ", "NFKD")
        assert result == "A"

    def test_empty_form_returns_text(self):
        assert self.n.unicode_normalize("café", "") == "café"

    def test_invalid_form_raises(self):
        with pytest.raises(ValueError):
            self.n.unicode_normalize("text", "BOGUS")

    def test_idempotent_nfc(self):
        text = "Привет, мир"
        once = self.n.unicode_normalize(text, "NFC")
        twice = self.n.unicode_normalize(once, "NFC")
        assert once == twice


# ---------------------------------------------------------------------------
# strip_accents
# ---------------------------------------------------------------------------
class TestStripAccents:
    def setup_method(self):
        self.n = TextNormalizer()

    def test_cafe(self):
        assert self.n.strip_accents("café") == "cafe"

    def test_naive(self):
        assert self.n.strip_accents("naïve") == "naive"

    def test_resume(self):
        assert self.n.strip_accents("résumé") == "resume"

    def test_no_accents(self):
        assert self.n.strip_accents("hello") == "hello"

    def test_empty(self):
        assert self.n.strip_accents("") == ""

    def test_multiple_accents(self):
        assert self.n.strip_accents("àéîõü") == "aeiou"

    def test_preserves_non_latin(self):
        # Cyrillic letters have no combining marks (they're base letters),
        # so they should pass through unchanged.
        assert self.n.strip_accents("Привет") == "Привет"


# ---------------------------------------------------------------------------
# collapse_whitespace
# ---------------------------------------------------------------------------
class TestCollapseWhitespace:
    def setup_method(self):
        self.n = TextNormalizer()

    def test_multiple_spaces(self):
        assert self.n.collapse_whitespace("a    b") == "a b"

    def test_tabs(self):
        assert self.n.collapse_whitespace("a\t\tb") == "a b"

    def test_mixed_tabs_and_spaces(self):
        assert self.n.collapse_whitespace("a \t  b") == "a b"

    def test_preserve_newlines_true(self):
        result = self.n.collapse_whitespace("a   b\n\nc   d", preserve_newlines=True)
        assert "\n" in result
        assert "a b" in result
        assert "c d" in result

    def test_preserve_newlines_false(self):
        result = self.n.collapse_whitespace("a   b\n\nc   d", preserve_newlines=False)
        assert "\n" not in result
        assert result == "a b c d"

    def test_collapse_multiple_newlines_when_preserved(self):
        result = self.n.collapse_whitespace("a\n\n\n\nb", preserve_newlines=True)
        assert result == "a\nb"

    def test_no_whitespace(self):
        assert self.n.collapse_whitespace("abc") == "abc"

    def test_empty_string(self):
        assert self.n.collapse_whitespace("") == ""

    def test_trims_spaces_around_newline(self):
        result = self.n.collapse_whitespace("a   \n   b", preserve_newlines=True)
        assert result == "a\nb"


# ---------------------------------------------------------------------------
# normalize_quotes
# ---------------------------------------------------------------------------
class TestNormalizeQuotes:
    def setup_method(self):
        self.n = TextNormalizer()

    def test_double_curly_quotes(self):
        assert self.n.normalize_quotes("“hello”") == '"hello"'

    def test_single_curly_quotes(self):
        assert self.n.normalize_quotes("‘world’") == "'world'"

    def test_french_quotes(self):
        assert self.n.normalize_quotes("«bonjour»") == '"bonjour"'

    def test_low9_quote(self):
        assert self.n.normalize_quotes("„hallo“") == '"hallo"'

    def test_apostrophe_in_word(self):
        assert self.n.normalize_quotes("it’s") == "it's"

    def test_no_smart_quotes(self):
        assert self.n.normalize_quotes('"plain" \'quotes\'') == "\"plain\" 'quotes'"

    def test_empty(self):
        assert self.n.normalize_quotes("") == ""


# ---------------------------------------------------------------------------
# normalize_dashes
# ---------------------------------------------------------------------------
class TestNormalizeDashes:
    def setup_method(self):
        self.n = TextNormalizer()

    def test_em_dash(self):
        assert self.n.normalize_dashes("a—b") == "a-b"

    def test_en_dash(self):
        assert self.n.normalize_dashes("a–b") == "a-b"

    def test_figure_dash(self):
        assert self.n.normalize_dashes("a‒b") == "a-b"

    def test_horizontal_bar(self):
        assert self.n.normalize_dashes("a―b") == "a-b"

    def test_regular_hyphen_untouched(self):
        assert self.n.normalize_dashes("a-b") == "a-b"

    def test_mixed(self):
        assert self.n.normalize_dashes("x—y–z") == "x-y-z"

    def test_empty(self):
        assert self.n.normalize_dashes("") == ""


# ---------------------------------------------------------------------------
# remove_zero_width
# ---------------------------------------------------------------------------
class TestRemoveZeroWidth:
    def setup_method(self):
        self.n = TextNormalizer()

    def test_zwsp(self):
        assert self.n.remove_zero_width("a​b") == "ab"

    def test_zwnj(self):
        assert self.n.remove_zero_width("a‌b") == "ab"

    def test_zwj(self):
        assert self.n.remove_zero_width("a‍b") == "ab"

    def test_bom(self):
        assert self.n.remove_zero_width("﻿hello") == "hello"

    def test_multiple_zero_width(self):
        text = "a​b‌c‍d﻿e"
        assert self.n.remove_zero_width(text) == "abcde"

    def test_no_zero_width(self):
        assert self.n.remove_zero_width("hello") == "hello"


# ---------------------------------------------------------------------------
# lowercase
# ---------------------------------------------------------------------------
class TestLowercase:
    def setup_method(self):
        self.n = TextNormalizer()

    def test_ascii(self):
        assert self.n.lowercase("Hello") == "hello"

    def test_cyrillic(self):
        assert self.n.lowercase("Привет") == "привет"

    def test_mixed_case(self):
        assert self.n.lowercase("HeLLo WoRLD") == "hello world"

    def test_already_lower(self):
        assert self.n.lowercase("hello") == "hello"


# ---------------------------------------------------------------------------
# normalize() integration
# ---------------------------------------------------------------------------
class TestNormalizeIntegration:
    def test_returns_result(self):
        n = TextNormalizer()
        res = n.normalize("hello")
        assert isinstance(res, NormalizationResult)

    def test_applies_default_rules(self):
        n = TextNormalizer()
        text = "“hello” — world​   here"
        res = n.normalize(text)
        # Smart quotes/dashes normalized, ZWSP removed, whitespace collapsed.
        assert '"' in res.normalized
        assert "-" in res.normalized
        assert "​" not in res.normalized
        assert "   " not in res.normalized
        assert res.changed is True
        assert len(res.rules_applied) >= 1

    def test_unchanged_text(self):
        n = TextNormalizer()
        res = n.normalize("plain text")
        assert res.changed is False
        assert res.normalized == "plain text"
        assert res.rules_applied == []

    def test_original_preserved(self):
        n = TextNormalizer()
        original = "“hi”"
        res = n.normalize(original)
        assert res.original == original
        assert res.normalized != original

    def test_full_pipeline_with_all_rules(self):
        cfg = NormalizationConfig(
            unicode_form="NFC",
            lowercase=True,
            strip_accents=True,
            collapse_whitespace=True,
            normalize_quotes=True,
            normalize_dashes=True,
            remove_zero_width=True,
            preserve_newlines=False,
        )
        n = TextNormalizer(cfg)
        text = "  Café — “Résumé”​  Naïve  "
        res = n.normalize(text)
        # lowercase, accents stripped, dashes/quotes normalized, ws collapsed
        assert "café" not in res.normalized
        assert "cafe" in res.normalized
        assert "resume" in res.normalized
        assert "naive" in res.normalized
        assert "—" not in res.normalized
        assert "“" not in res.normalized
        assert "​" not in res.normalized

    def test_rules_applied_order(self):
        cfg = NormalizationConfig(
            unicode_form="NFC",
            normalize_quotes=True,
            collapse_whitespace=True,
        )
        n = TextNormalizer(cfg)
        res = n.normalize("“hi”   there")
        # quotes should come before collapse_whitespace in the applied list
        assert NormalizationRule.NORMALIZE_QUOTES.value in res.rules_applied
        assert NormalizationRule.COLLAPSE_WHITESPACE.value in res.rules_applied
        idx_q = res.rules_applied.index(NormalizationRule.NORMALIZE_QUOTES.value)
        idx_w = res.rules_applied.index(NormalizationRule.COLLAPSE_WHITESPACE.value)
        assert idx_q < idx_w

    def test_default_config_used_when_none(self):
        n = TextNormalizer(None)
        assert isinstance(n.config, NormalizationConfig)


# ---------------------------------------------------------------------------
# normalize_batch
# ---------------------------------------------------------------------------
class TestNormalizeBatch:
    def test_batch_basic(self):
        n = TextNormalizer()
        results = n.normalize_batch(["hi", "  hello  ", "world"])
        assert len(results) == 3
        assert all(isinstance(r, NormalizationResult) for r in results)

    def test_batch_empty(self):
        n = TextNormalizer()
        assert n.normalize_batch([]) == []

    def test_batch_preserves_order(self):
        n = TextNormalizer()
        results = n.normalize_batch(["one", "two", "three"])
        assert results[0].original == "one"
        assert results[1].original == "two"
        assert results[2].original == "three"


# ---------------------------------------------------------------------------
# Selective rules — config flags control behavior
# ---------------------------------------------------------------------------
class TestSelectiveRules:
    def test_only_quotes(self):
        cfg = NormalizationConfig(
            unicode_form="",
            collapse_whitespace=False,
            normalize_quotes=True,
            normalize_dashes=False,
            remove_zero_width=False,
        )
        n = TextNormalizer(cfg)
        res = n.normalize("“hi” — there")
        assert '"hi"' in res.normalized
        # em dash should remain
        assert "—" in res.normalized

    def test_only_dashes(self):
        cfg = NormalizationConfig(
            unicode_form="",
            collapse_whitespace=False,
            normalize_quotes=False,
            normalize_dashes=True,
            remove_zero_width=False,
        )
        n = TextNormalizer(cfg)
        res = n.normalize("a — “hi”")
        assert "-" in res.normalized
        assert "“" in res.normalized

    def test_lowercase_disabled_by_default(self):
        n = TextNormalizer()
        res = n.normalize("HELLO")
        assert res.normalized == "HELLO"

    def test_strip_accents_disabled_by_default(self):
        n = TextNormalizer()
        res = n.normalize("café")
        assert "é" in res.normalized

    def test_no_collapse_whitespace(self):
        cfg = NormalizationConfig(collapse_whitespace=False)
        n = TextNormalizer(cfg)
        res = n.normalize("a    b")
        assert "    " in res.normalized

    def test_preserve_newlines_false_in_config(self):
        cfg = NormalizationConfig(preserve_newlines=False)
        n = TextNormalizer(cfg)
        res = n.normalize("a   b\n\nc")
        assert "\n" not in res.normalized

    def test_unicode_form_disabled(self):
        cfg = NormalizationConfig(
            unicode_form="",
            collapse_whitespace=False,
            normalize_quotes=False,
            normalize_dashes=False,
            remove_zero_width=False,
        )
        n = TextNormalizer(cfg)
        decomposed = "é"
        res = n.normalize(decomposed)
        # No unicode normalization applied -> output stays decomposed.
        assert res.normalized == decomposed

    def test_nfkc_config(self):
        cfg = NormalizationConfig(
            unicode_form="NFKC",
            collapse_whitespace=False,
            normalize_quotes=False,
            normalize_dashes=False,
            remove_zero_width=False,
        )
        n = TextNormalizer(cfg)
        res = n.normalize("Ａ")  # FULLWIDTH A
        assert res.normalized == "A"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_empty_text(self):
        n = TextNormalizer()
        res = n.normalize("")
        assert res.original == ""
        assert res.normalized == ""
        assert res.changed is False
        assert res.char_diff == 0

    def test_only_whitespace(self):
        n = TextNormalizer()
        res = n.normalize("     ")
        # Inline whitespace collapsed to single space.
        assert res.normalized == " "

    def test_only_whitespace_no_newlines(self):
        cfg = NormalizationConfig(preserve_newlines=False)
        n = TextNormalizer(cfg)
        res = n.normalize("  \t\n  ")
        assert res.normalized == " "

    def test_ascii_only(self):
        n = TextNormalizer()
        res = n.normalize("plain ascii text")
        assert res.normalized == "plain ascii text"
        assert res.changed is False

    def test_long_text(self):
        n = TextNormalizer()
        text = "a" * 10000
        res = n.normalize(text)
        assert res.normalized == text
        assert res.changed is False

    def test_unicode_only(self):
        n = TextNormalizer()
        res = n.normalize("Привет, мир!")
        assert res.normalized == "Привет, мир!"

    def test_combining_marks_normalized_to_nfc(self):
        n = TextNormalizer()
        decomposed = "café"  # cafe + combining acute
        res = n.normalize(decomposed)
        # Default NFC composes "é"
        assert res.normalized == "café"
        # category check: no combining marks left after NFC
        assert all(unicodedata.category(c) != "Mn" for c in res.normalized)

    def test_char_diff_after_collapse(self):
        n = TextNormalizer()
        res = n.normalize("a     b")
        assert res.char_diff == 4  # 4 spaces removed
