"""Tests for docstoolkit.doc_normalizer."""
from __future__ import annotations

import pytest

from docstoolkit.doc_normalizer import (
    DocNormalizer,
    NormalizeConfig,
    NormalizeResult,
    NormalizerStep,
    Preset,
)


# ---------------------------------------------------------------------------
# NormalizerStep
# ---------------------------------------------------------------------------
class TestNormalizerStep:
    def test_has_all_steps(self):
        names = {s.name for s in NormalizerStep}
        assert {
            "LOWERCASE",
            "STRIP",
            "COLLAPSE_WS",
            "EXPAND_CONTRACTIONS",
            "REMOVE_PUNCTUATION",
            "REMOVE_DIGITS",
            "FIX_UNICODE",
            "NORMALIZE_QUOTES",
            "REMOVE_DIACRITICS",
            "EXPAND_ABBREVIATIONS",
        }.issubset(names)

    def test_values_unique(self):
        values = [s.value for s in NormalizerStep]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# Preset
# ---------------------------------------------------------------------------
class TestPreset:
    def test_has_all_presets(self):
        assert Preset.MINIMAL.value == "MINIMAL"
        assert Preset.STANDARD.value == "STANDARD"
        assert Preset.AGGRESSIVE.value == "AGGRESSIVE"
        assert Preset.SEARCH.value == "SEARCH"

    def test_presets_unique(self):
        values = [p.value for p in Preset]
        assert len(values) == len(set(values))


# ---------------------------------------------------------------------------
# NormalizeConfig
# ---------------------------------------------------------------------------
class TestNormalizeConfig:
    def test_defaults(self):
        cfg = NormalizeConfig()
        assert cfg.steps == []
        assert cfg.preserve_newlines is True
        assert cfg.custom_replacements == []
        assert cfg.custom_contractions == {}
        assert cfg.custom_abbreviations == {}

    def test_custom_values(self):
        cfg = NormalizeConfig(
            steps=[NormalizerStep.LOWERCASE],
            preserve_newlines=False,
            custom_replacements=[("a", "b")],
            custom_contractions={"foo": "bar"},
            custom_abbreviations={"X.": "ten"},
        )
        assert cfg.steps == [NormalizerStep.LOWERCASE]
        assert cfg.preserve_newlines is False
        assert cfg.custom_replacements == [("a", "b")]
        assert cfg.custom_contractions == {"foo": "bar"}
        assert cfg.custom_abbreviations == {"X.": "ten"}


# ---------------------------------------------------------------------------
# NormalizeResult
# ---------------------------------------------------------------------------
class TestNormalizeResult:
    def test_changed_property_true(self):
        r = NormalizeResult(original="a", normalized="b", applied_steps=[])
        assert r.changed is True

    def test_changed_property_false(self):
        r = NormalizeResult(original="a", normalized="a", applied_steps=[])
        assert r.changed is False

    def test_length_delta_positive(self):
        r = NormalizeResult(original="hi", normalized="hello", applied_steps=[])
        assert r.length_delta == 3

    def test_length_delta_negative(self):
        r = NormalizeResult(original="hello", normalized="hi", applied_steps=[])
        assert r.length_delta == -3

    def test_length_delta_zero(self):
        r = NormalizeResult(original="abc", normalized="xyz", applied_steps=[])
        assert r.length_delta == 0


# ---------------------------------------------------------------------------
# Lowercase
# ---------------------------------------------------------------------------
class TestLowercase:
    def test_basic(self):
        assert DocNormalizer().lowercase("HELLO") == "hello"

    def test_mixed(self):
        assert DocNormalizer().lowercase("Hello World") == "hello world"

    def test_already_lower(self):
        assert DocNormalizer().lowercase("hello") == "hello"


# ---------------------------------------------------------------------------
# Strip
# ---------------------------------------------------------------------------
class TestStrip:
    def test_basic_trim(self):
        assert DocNormalizer().strip("  hello  ") == "hello"

    def test_tightens_around_newlines(self):
        assert DocNormalizer().strip("a   \n   b") == "a\nb"

    def test_no_change(self):
        assert DocNormalizer().strip("hello") == "hello"


# ---------------------------------------------------------------------------
# CollapseWhitespace
# ---------------------------------------------------------------------------
class TestCollapseWhitespace:
    def test_collapse_spaces(self):
        assert DocNormalizer().collapse_whitespace("a    b") == "a b"

    def test_collapse_tabs(self):
        assert DocNormalizer().collapse_whitespace("a\t\tb") == "a b"

    def test_preserve_single_newline(self):
        assert DocNormalizer().collapse_whitespace("a\nb") == "a\nb"

    def test_collapse_multiple_newlines(self):
        assert DocNormalizer().collapse_whitespace("a\n\n\nb") == "a\nb"

    def test_no_preserve_newlines(self):
        assert (
            DocNormalizer().collapse_whitespace("a\n\nb", preserve_newlines=False)
            == "a b"
        )


# ---------------------------------------------------------------------------
# ExpandContractions
# ---------------------------------------------------------------------------
class TestExpandContractions:
    def test_dont(self):
        out = DocNormalizer().expand_contractions("don't")
        assert out == "do not"

    def test_wont(self):
        assert DocNormalizer().expand_contractions("won't") == "will not"

    def test_im(self):
        assert DocNormalizer().expand_contractions("i'm") == "i am"

    def test_case_insensitive(self):
        assert DocNormalizer().expand_contractions("I'm") == "i am"

    def test_in_sentence(self):
        out = DocNormalizer().expand_contractions("I can't go")
        assert "can not" in out.lower()

    def test_custom_extra(self):
        out = DocNormalizer().expand_contractions(
            "y'all", extra={"y'all": "you all"}
        )
        assert out == "you all"


# ---------------------------------------------------------------------------
# RemovePunctuation
# ---------------------------------------------------------------------------
class TestRemovePunctuation:
    def test_basic(self):
        assert DocNormalizer().remove_punctuation("hello, world!") == "hello world"

    def test_keeps_letters_and_spaces(self):
        out = DocNormalizer().remove_punctuation("a.b,c;d")
        assert out == "abcd"

    def test_no_punctuation(self):
        assert DocNormalizer().remove_punctuation("hello world") == "hello world"


# ---------------------------------------------------------------------------
# RemoveDigits
# ---------------------------------------------------------------------------
class TestRemoveDigits:
    def test_basic(self):
        assert DocNormalizer().remove_digits("abc123def") == "abcdef"

    def test_only_digits(self):
        assert DocNormalizer().remove_digits("12345") == ""

    def test_no_digits(self):
        assert DocNormalizer().remove_digits("hello") == "hello"


# ---------------------------------------------------------------------------
# FixUnicode
# ---------------------------------------------------------------------------
class TestFixUnicode:
    def test_nfkc_compatibility(self):
        # Fullwidth digits should become ASCII via NFKC.
        out = DocNormalizer().fix_unicode("１２３")
        assert out == "123"

    def test_idempotent_for_ascii(self):
        assert DocNormalizer().fix_unicode("hello") == "hello"

    def test_combining_marks_recomposed(self):
        # "e" + combining acute (NFD) becomes "é" (NFKC composed).
        decomposed = "é"
        assert DocNormalizer().fix_unicode(decomposed) == "é"


# ---------------------------------------------------------------------------
# NormalizeQuotes
# ---------------------------------------------------------------------------
class TestNormalizeQuotes:
    def test_double_quotes(self):
        assert DocNormalizer().normalize_quotes("“hi”") == '"hi"'

    def test_single_quotes(self):
        assert DocNormalizer().normalize_quotes("‘hi’") == "'hi'"

    def test_angle_quotes(self):
        assert DocNormalizer().normalize_quotes("«hi»") == '"hi"'

    def test_no_quotes(self):
        assert DocNormalizer().normalize_quotes("hello") == "hello"


# ---------------------------------------------------------------------------
# RemoveDiacritics
# ---------------------------------------------------------------------------
class TestRemoveDiacritics:
    def test_cafe(self):
        assert DocNormalizer().remove_diacritics("café") == "cafe"

    def test_naive(self):
        assert DocNormalizer().remove_diacritics("naïve") == "naive"

    def test_no_diacritics(self):
        assert DocNormalizer().remove_diacritics("hello") == "hello"

    def test_multiple(self):
        assert DocNormalizer().remove_diacritics("élève") == "eleve"


# ---------------------------------------------------------------------------
# ExpandAbbreviations
# ---------------------------------------------------------------------------
class TestExpandAbbreviations:
    def test_mr(self):
        assert DocNormalizer().expand_abbreviations("Mr.") == "Mister"

    def test_dr(self):
        assert DocNormalizer().expand_abbreviations("Dr.") == "Doctor"

    def test_st(self):
        assert DocNormalizer().expand_abbreviations("St.") == "Saint"

    def test_eg(self):
        assert DocNormalizer().expand_abbreviations("e.g.") == "for example"

    def test_ie(self):
        assert DocNormalizer().expand_abbreviations("i.e.") == "that is"

    def test_etc(self):
        assert DocNormalizer().expand_abbreviations("etc.") == "et cetera"

    def test_extra(self):
        out = DocNormalizer().expand_abbreviations(
            "Esq.", extra={"Esq.": "Esquire"}
        )
        assert out == "Esquire"


# ---------------------------------------------------------------------------
# ApplyReplacements
# ---------------------------------------------------------------------------
class TestApplyReplacements:
    def test_single_replacement(self):
        out = DocNormalizer().apply_replacements("hello", [("hello", "hi")])
        assert out == "hi"

    def test_multiple_replacements(self):
        out = DocNormalizer().apply_replacements(
            "foo bar baz", [("foo", "FOO"), ("baz", "BAZ")]
        )
        assert out == "FOO bar BAZ"

    def test_empty_replacements(self):
        assert DocNormalizer().apply_replacements("hello", []) == "hello"


# ---------------------------------------------------------------------------
# Normalize with config (integration of pipeline)
# ---------------------------------------------------------------------------
class TestNormalizeIntegration:
    def test_uses_steps_in_order(self):
        cfg = NormalizeConfig(
            steps=[NormalizerStep.LOWERCASE, NormalizerStep.REMOVE_PUNCTUATION]
        )
        r = DocNormalizer().normalize("HELLO!", cfg)
        assert r.normalized == "hello"
        assert NormalizerStep.LOWERCASE in r.applied_steps
        assert NormalizerStep.REMOVE_PUNCTUATION in r.applied_steps

    def test_no_steps_returns_unchanged(self):
        r = DocNormalizer().normalize("hello", NormalizeConfig(steps=[]))
        assert r.normalized == "hello"
        assert r.applied_steps == []
        assert r.changed is False

    def test_returns_result_object(self):
        r = DocNormalizer().normalize("hello", NormalizeConfig())
        assert isinstance(r, NormalizeResult)
        assert r.original == "hello"

    def test_applied_steps_only_when_changed(self):
        # LOWERCASE applied to already-lowercase doesn't register as applied.
        cfg = NormalizeConfig(steps=[NormalizerStep.LOWERCASE])
        r = DocNormalizer().normalize("hello", cfg)
        assert r.applied_steps == []

    def test_config_passed_at_init(self):
        cfg = NormalizeConfig(steps=[NormalizerStep.LOWERCASE])
        norm = DocNormalizer(cfg)
        r = norm.normalize("HELLO")
        assert r.normalized == "hello"


# ---------------------------------------------------------------------------
# apply_preset
# ---------------------------------------------------------------------------
class TestApplyPreset:
    def test_minimal(self):
        cfg = DocNormalizer().apply_preset(Preset.MINIMAL)
        assert cfg.steps == [NormalizerStep.STRIP, NormalizerStep.COLLAPSE_WS]

    def test_standard(self):
        cfg = DocNormalizer().apply_preset(Preset.STANDARD)
        assert NormalizerStep.FIX_UNICODE in cfg.steps
        assert NormalizerStep.NORMALIZE_QUOTES in cfg.steps

    def test_aggressive_includes_many(self):
        cfg = DocNormalizer().apply_preset(Preset.AGGRESSIVE)
        assert NormalizerStep.LOWERCASE in cfg.steps
        assert NormalizerStep.REMOVE_DIGITS not in cfg.steps

    def test_search(self):
        cfg = DocNormalizer().apply_preset(Preset.SEARCH)
        assert NormalizerStep.LOWERCASE in cfg.steps
        assert NormalizerStep.REMOVE_PUNCTUATION in cfg.steps
        assert NormalizerStep.REMOVE_DIACRITICS in cfg.steps


# ---------------------------------------------------------------------------
# apply_step
# ---------------------------------------------------------------------------
class TestApplyStep:
    def test_lowercase_step(self):
        assert DocNormalizer().apply_step("HELLO", NormalizerStep.LOWERCASE) == "hello"

    def test_strip_step(self):
        assert DocNormalizer().apply_step("  hi  ", NormalizerStep.STRIP) == "hi"

    def test_collapse_ws_step(self):
        assert DocNormalizer().apply_step("a    b", NormalizerStep.COLLAPSE_WS) == "a b"

    def test_remove_punctuation_step(self):
        assert (
            DocNormalizer().apply_step("a, b!", NormalizerStep.REMOVE_PUNCTUATION)
            == "a b"
        )

    def test_remove_digits_step(self):
        assert (
            DocNormalizer().apply_step("a1b2c3", NormalizerStep.REMOVE_DIGITS) == "abc"
        )

    def test_fix_unicode_step(self):
        out = DocNormalizer().apply_step("１２３", NormalizerStep.FIX_UNICODE)
        assert out == "123"

    def test_normalize_quotes_step(self):
        out = DocNormalizer().apply_step("“hi”", NormalizerStep.NORMALIZE_QUOTES)
        assert out == '"hi"'

    def test_remove_diacritics_step(self):
        out = DocNormalizer().apply_step("café", NormalizerStep.REMOVE_DIACRITICS)
        assert out == "cafe"

    def test_expand_contractions_step(self):
        out = DocNormalizer().apply_step(
            "don't", NormalizerStep.EXPAND_CONTRACTIONS
        )
        assert out == "do not"

    def test_expand_abbreviations_step(self):
        out = DocNormalizer().apply_step("Mr.", NormalizerStep.EXPAND_ABBREVIATIONS)
        assert out == "Mister"


# ---------------------------------------------------------------------------
# normalize_batch
# ---------------------------------------------------------------------------
class TestNormalizeBatch:
    def test_batch_returns_list(self):
        cfg = NormalizeConfig(steps=[NormalizerStep.LOWERCASE])
        out = DocNormalizer().normalize_batch(["HI", "BYE"], cfg)
        assert len(out) == 2
        assert all(isinstance(r, NormalizeResult) for r in out)

    def test_batch_results(self):
        cfg = NormalizeConfig(steps=[NormalizerStep.LOWERCASE])
        out = DocNormalizer().normalize_batch(["HI", "BYE"], cfg)
        assert [r.normalized for r in out] == ["hi", "bye"]

    def test_batch_empty(self):
        out = DocNormalizer().normalize_batch([], NormalizeConfig())
        assert out == []


# ---------------------------------------------------------------------------
# Preset: MINIMAL
# ---------------------------------------------------------------------------
class TestPresetMinimal:
    def test_minimal_trims_and_collapses(self):
        norm = DocNormalizer()
        cfg = norm.apply_preset(Preset.MINIMAL)
        r = norm.normalize("  hello    world  ", cfg)
        assert r.normalized == "hello world"


# ---------------------------------------------------------------------------
# Preset: STANDARD
# ---------------------------------------------------------------------------
class TestPresetStandard:
    def test_standard_fixes_quotes(self):
        norm = DocNormalizer()
        cfg = norm.apply_preset(Preset.STANDARD)
        r = norm.normalize("  “hi” ", cfg)
        assert '"hi"' in r.normalized

    def test_standard_does_not_lowercase(self):
        norm = DocNormalizer()
        cfg = norm.apply_preset(Preset.STANDARD)
        r = norm.normalize("Hello", cfg)
        assert r.normalized == "Hello"


# ---------------------------------------------------------------------------
# Preset: AGGRESSIVE
# ---------------------------------------------------------------------------
class TestPresetAggressive:
    def test_aggressive_lowercases(self):
        norm = DocNormalizer()
        cfg = norm.apply_preset(Preset.AGGRESSIVE)
        r = norm.normalize("Hello, World!", cfg)
        assert r.normalized.islower() or r.normalized == r.normalized.lower()

    def test_aggressive_removes_punctuation(self):
        norm = DocNormalizer()
        cfg = norm.apply_preset(Preset.AGGRESSIVE)
        r = norm.normalize("Hello, World!", cfg)
        assert "," not in r.normalized
        assert "!" not in r.normalized

    def test_aggressive_keeps_digits(self):
        norm = DocNormalizer()
        cfg = norm.apply_preset(Preset.AGGRESSIVE)
        r = norm.normalize("year 2025", cfg)
        assert "2025" in r.normalized


# ---------------------------------------------------------------------------
# Preset: SEARCH
# ---------------------------------------------------------------------------
class TestPresetSearch:
    def test_search_lowercases(self):
        norm = DocNormalizer()
        cfg = norm.apply_preset(Preset.SEARCH)
        r = norm.normalize("Hello", cfg)
        assert r.normalized == "hello"

    def test_search_strips_diacritics_and_punctuation(self):
        norm = DocNormalizer()
        cfg = norm.apply_preset(Preset.SEARCH)
        r = norm.normalize("Café, élève!", cfg)
        assert "," not in r.normalized
        assert "é" not in r.normalized
        assert "cafe" in r.normalized


# ---------------------------------------------------------------------------
# Custom replacements
# ---------------------------------------------------------------------------
class TestCustomReplacements:
    def test_replacements_applied_at_end(self):
        cfg = NormalizeConfig(
            steps=[NormalizerStep.LOWERCASE],
            custom_replacements=[("hello", "greetings")],
        )
        r = DocNormalizer().normalize("HELLO", cfg)
        assert r.normalized == "greetings"

    def test_multiple_custom_replacements(self):
        cfg = NormalizeConfig(
            steps=[],
            custom_replacements=[("a", "1"), ("b", "2")],
        )
        r = DocNormalizer().normalize("aabb", cfg)
        assert r.normalized == "1122"

    def test_custom_contractions(self):
        cfg = NormalizeConfig(
            steps=[NormalizerStep.EXPAND_CONTRACTIONS],
            custom_contractions={"gonna": "going to"},
        )
        r = DocNormalizer().normalize("gonna", cfg)
        assert r.normalized == "going to"

    def test_custom_abbreviations(self):
        cfg = NormalizeConfig(
            steps=[NormalizerStep.EXPAND_ABBREVIATIONS],
            custom_abbreviations={"Capt.": "Captain"},
        )
        r = DocNormalizer().normalize("Capt.", cfg)
        assert r.normalized == "Captain"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_empty_string(self):
        cfg = NormalizeConfig(steps=[NormalizerStep.LOWERCASE])
        r = DocNormalizer().normalize("", cfg)
        assert r.normalized == ""
        assert r.changed is False

    def test_only_whitespace(self):
        cfg = NormalizeConfig(steps=[NormalizerStep.STRIP])
        r = DocNormalizer().normalize("   ", cfg)
        assert r.normalized == ""

    def test_unknown_step_raises(self):
        with pytest.raises(ValueError):
            # Fabricate a fake "step" via duck-typing: not in dispatcher.
            DocNormalizer().apply_step("hi", "NOT_A_STEP")  # type: ignore[arg-type]

    def test_unicode_only(self):
        cfg = NormalizeConfig(
            steps=[NormalizerStep.REMOVE_DIACRITICS, NormalizerStep.LOWERCASE]
        )
        r = DocNormalizer().normalize("Élève", cfg)
        assert r.normalized == "eleve"

    def test_preserve_newlines_in_config(self):
        cfg = NormalizeConfig(
            steps=[NormalizerStep.COLLAPSE_WS], preserve_newlines=True
        )
        r = DocNormalizer().normalize("a\n\nb", cfg)
        assert r.normalized == "a\nb"

    def test_preserve_newlines_false_in_config(self):
        cfg = NormalizeConfig(
            steps=[NormalizerStep.COLLAPSE_WS], preserve_newlines=False
        )
        r = DocNormalizer().normalize("a\n\nb", cfg)
        assert r.normalized == "a b"
