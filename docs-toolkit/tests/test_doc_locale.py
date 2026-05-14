"""Tests for docstoolkit.doc_locale (E220)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_locale import (
    DocLocale,
    DocTranslation,
    LocaleCode,
    LocaleStats,
)


# ---------------------------------------------------------------------------
# LocaleCode
# ---------------------------------------------------------------------------
class TestLocaleCode:
    def test_en_value(self):
        assert LocaleCode.EN.value == "en"

    def test_ru_value(self):
        assert LocaleCode.RU.value == "ru"

    def test_unknown_value(self):
        assert LocaleCode.UNKNOWN.value == "unknown"

    def test_all_required_locales_present(self):
        names = {m.name for m in LocaleCode}
        for required in ("EN", "RU", "ES", "FR", "DE", "IT", "PT",
                         "ZH", "JA", "AR", "UNKNOWN"):
            assert required in names


# ---------------------------------------------------------------------------
# DocTranslation
# ---------------------------------------------------------------------------
class TestDocTranslation:
    def test_basic_create(self):
        t = DocTranslation(doc_id="d1", locale=LocaleCode.EN, content="Hi")
        assert t.doc_id == "d1"
        assert t.locale is LocaleCode.EN
        assert t.content == "Hi"
        assert t.title is None
        assert t.is_canonical is False

    def test_with_title(self):
        t = DocTranslation(
            doc_id="d1", locale=LocaleCode.RU, content="Привет", title="Заголовок"
        )
        assert t.title == "Заголовок"

    def test_is_canonical(self):
        t = DocTranslation(
            doc_id="d1", locale=LocaleCode.EN, content="x", is_canonical=True
        )
        assert t.is_canonical is True


# ---------------------------------------------------------------------------
# LocaleStats
# ---------------------------------------------------------------------------
class TestLocaleStats:
    def test_empty_coverage_zero(self):
        s = LocaleStats(total_docs=0, total_translations=0)
        assert s.coverage == 0.0

    def test_coverage_computation(self):
        # 2 docs * 2 locales = 4 slots, 3 translations → 0.75
        s = LocaleStats(
            total_docs=2,
            total_translations=3,
            by_locale={"en": 2, "ru": 1},
            missing_translations=[("d1", "ru")],
            _required_locales_count=2,
        )
        assert s.coverage == pytest.approx(0.75)

    def test_coverage_zero_when_no_required(self):
        s = LocaleStats(total_docs=2, total_translations=2,
                       _required_locales_count=0)
        assert s.coverage == 0.0


# ---------------------------------------------------------------------------
# register_doc
# ---------------------------------------------------------------------------
class TestRegisterDoc:
    def test_register_new(self):
        dl = DocLocale()
        assert dl.register_doc("d1") is True

    def test_register_existing_returns_false(self):
        dl = DocLocale()
        dl.register_doc("d1")
        assert dl.register_doc("d1") is False

    def test_register_with_canonical_locale(self):
        dl = DocLocale()
        dl.register_doc("d1", canonical_locale=LocaleCode.EN)
        # No translation yet but canonical is tracked
        assert dl.canonical("d1") is None  # no translation yet
        dl.add_translation("d1", LocaleCode.EN, "Hello")
        # After adding, canonical lookup should resolve
        assert dl.canonical("d1") is not None
        assert dl.canonical("d1").locale is LocaleCode.EN

    def test_register_increments_total_docs(self):
        dl = DocLocale()
        dl.register_doc("d1")
        dl.register_doc("d2")
        assert dl.total_docs == 2


# ---------------------------------------------------------------------------
# add_translation
# ---------------------------------------------------------------------------
class TestAddTranslation:
    def test_add_returns_translation(self):
        dl = DocLocale()
        dl.register_doc("d1")
        tr = dl.add_translation("d1", LocaleCode.EN, "Hello")
        assert isinstance(tr, DocTranslation)
        assert tr.content == "Hello"

    def test_add_auto_registers_doc(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        assert dl.total_docs == 1

    def test_add_with_title(self):
        dl = DocLocale()
        tr = dl.add_translation("d1", LocaleCode.EN, "Hi", title="Greeting")
        assert tr.title == "Greeting"

    def test_add_canonical(self):
        dl = DocLocale()
        tr = dl.add_translation("d1", LocaleCode.EN, "Hi", is_canonical=True)
        assert tr.is_canonical is True
        assert dl.canonical("d1") is tr

    def test_add_replaces_existing(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        tr2 = dl.add_translation("d1", LocaleCode.EN, "Hello again")
        assert tr2.content == "Hello again"
        assert dl.get_translation("d1", LocaleCode.EN).content == "Hello again"

    def test_canonical_flag_unique(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi", is_canonical=True)
        dl.add_translation("d1", LocaleCode.RU, "Привет", is_canonical=True)
        # The previous canonical should be unset
        en_tr = dl.get_translation("d1", LocaleCode.EN, fallback=False)
        ru_tr = dl.get_translation("d1", LocaleCode.RU, fallback=False)
        assert ru_tr.is_canonical is True
        assert en_tr.is_canonical is False


# ---------------------------------------------------------------------------
# remove_translation
# ---------------------------------------------------------------------------
class TestRemoveTranslation:
    def test_remove_existing(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        assert dl.remove_translation("d1", LocaleCode.EN) is True

    def test_remove_missing_doc(self):
        dl = DocLocale()
        assert dl.remove_translation("nope", LocaleCode.EN) is False

    def test_remove_missing_locale(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        assert dl.remove_translation("d1", LocaleCode.RU) is False

    def test_remove_clears_canonical(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi", is_canonical=True)
        dl.remove_translation("d1", LocaleCode.EN)
        assert dl.canonical("d1") is None


# ---------------------------------------------------------------------------
# get_translation
# ---------------------------------------------------------------------------
class TestGetTranslation:
    def test_get_existing(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hello")
        tr = dl.get_translation("d1", LocaleCode.EN)
        assert tr.content == "Hello"

    def test_get_missing_doc(self):
        dl = DocLocale()
        assert dl.get_translation("nope", LocaleCode.EN) is None

    def test_get_no_fallback_returns_none(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        assert dl.get_translation("d1", LocaleCode.RU, fallback=False) is None


class TestGetTranslationFallback:
    def test_fallback_to_default(self):
        dl = DocLocale(default_locale=LocaleCode.EN)
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        tr = dl.get_translation("d1", LocaleCode.RU, fallback=True)
        assert tr is not None
        assert tr.locale is LocaleCode.EN

    def test_fallback_to_canonical(self):
        dl = DocLocale(default_locale=LocaleCode.EN)
        # Canonical is RU, default is EN, neither requested locale exists
        dl.add_translation("d1", LocaleCode.RU, "Привет", is_canonical=True)
        tr = dl.get_translation("d1", LocaleCode.FR, fallback=True)
        assert tr is not None
        assert tr.locale is LocaleCode.RU

    def test_fallback_none_when_no_match(self):
        dl = DocLocale(default_locale=LocaleCode.EN)
        dl.add_translation("d1", LocaleCode.FR, "Bonjour")
        # No canonical, default EN absent, requested DE absent
        tr = dl.get_translation("d1", LocaleCode.DE, fallback=True)
        assert tr is None


# ---------------------------------------------------------------------------
# canonical
# ---------------------------------------------------------------------------
class TestCanonical:
    def test_no_canonical(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        assert dl.canonical("d1") is None

    def test_canonical_via_add(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi", is_canonical=True)
        assert dl.canonical("d1").content == "Hi"

    def test_canonical_for_missing_doc(self):
        dl = DocLocale()
        assert dl.canonical("nope") is None


# ---------------------------------------------------------------------------
# available_locales
# ---------------------------------------------------------------------------
class TestAvailableLocales:
    def test_empty(self):
        dl = DocLocale()
        dl.register_doc("d1")
        assert dl.available_locales("d1") == []

    def test_multiple(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.add_translation("d1", LocaleCode.RU, "Привет")
        result = dl.available_locales("d1")
        assert LocaleCode.EN in result
        assert LocaleCode.RU in result

    def test_unknown_doc(self):
        dl = DocLocale()
        assert dl.available_locales("nope") == []


# ---------------------------------------------------------------------------
# translated_docs
# ---------------------------------------------------------------------------
class TestTranslatedDocs:
    def test_filters_by_locale(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.add_translation("d2", LocaleCode.RU, "Привет")
        dl.add_translation("d3", LocaleCode.EN, "Hello")
        en_docs = dl.translated_docs(LocaleCode.EN)
        assert sorted(en_docs) == ["d1", "d3"]

    def test_empty_when_no_match(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        assert dl.translated_docs(LocaleCode.JA) == []


# ---------------------------------------------------------------------------
# missing
# ---------------------------------------------------------------------------
class TestMissing:
    def test_no_required_defaults_to_default(self):
        dl = DocLocale(default_locale=LocaleCode.EN)
        dl.register_doc("d1")
        # No EN translation
        assert dl.missing("d1") == [LocaleCode.EN]

    def test_required_some_present(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        missing = dl.missing("d1", [LocaleCode.EN, LocaleCode.RU, LocaleCode.FR])
        assert LocaleCode.EN not in missing
        assert LocaleCode.RU in missing
        assert LocaleCode.FR in missing

    def test_all_present(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.add_translation("d1", LocaleCode.RU, "Привет")
        assert dl.missing("d1", [LocaleCode.EN, LocaleCode.RU]) == []


# ---------------------------------------------------------------------------
# detect_locale: EN
# ---------------------------------------------------------------------------
class TestDetectLocaleEn:
    def test_english_text(self):
        text = "The quick brown fox jumps over the lazy dog and the cat."
        assert DocLocale().detect_locale(text) is LocaleCode.EN

    def test_english_short(self):
        text = "This is the best of all the options and tools."
        assert DocLocale().detect_locale(text) is LocaleCode.EN


# ---------------------------------------------------------------------------
# detect_locale: RU
# ---------------------------------------------------------------------------
class TestDetectLocaleRu:
    def test_russian_text(self):
        text = "Привет мир! Это тестовая строка на русском языке."
        assert DocLocale().detect_locale(text) is LocaleCode.RU

    def test_mixed_cyrillic_dominant(self):
        text = "Привет world! Это тест с небольшой английской вставкой."
        assert DocLocale().detect_locale(text) is LocaleCode.RU


# ---------------------------------------------------------------------------
# detect_locale: ES
# ---------------------------------------------------------------------------
class TestDetectLocaleEs:
    def test_spanish_text(self):
        text = "El gato y la perra de la casa que comen y duermen."
        assert DocLocale().detect_locale(text) is LocaleCode.ES

    def test_french_text(self):
        text = "Le chat et la souris et les amis dans le jardin."
        assert DocLocale().detect_locale(text) is LocaleCode.FR


# ---------------------------------------------------------------------------
# detect_locale: ZH / JA
# ---------------------------------------------------------------------------
class TestDetectLocaleZhJa:
    def test_chinese_text(self):
        text = "你好世界这是一个测试"
        assert DocLocale().detect_locale(text) is LocaleCode.ZH

    def test_japanese_text(self):
        text = "これはテストです世界"
        assert DocLocale().detect_locale(text) is LocaleCode.JA

    def test_unknown_when_empty(self):
        assert DocLocale().detect_locale("") is LocaleCode.UNKNOWN

    def test_unknown_for_digits(self):
        assert DocLocale().detect_locale("12345 67890 ...") is LocaleCode.UNKNOWN


# ---------------------------------------------------------------------------
# select_best_locale
# ---------------------------------------------------------------------------
class TestSelectBestLocale:
    def test_first_match_wins(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.add_translation("d1", LocaleCode.RU, "Привет")
        result = dl.select_best_locale(
            "d1", [LocaleCode.FR, LocaleCode.RU, LocaleCode.EN]
        )
        assert result is LocaleCode.RU

    def test_falls_back_to_default(self):
        dl = DocLocale(default_locale=LocaleCode.EN)
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        result = dl.select_best_locale("d1", [LocaleCode.JA, LocaleCode.AR])
        assert result is LocaleCode.EN

    def test_explicit_default(self):
        dl = DocLocale(default_locale=LocaleCode.EN)
        dl.add_translation("d1", LocaleCode.FR, "Bonjour")
        result = dl.select_best_locale(
            "d1",
            [LocaleCode.JA],
            default=LocaleCode.FR,
        )
        assert result is LocaleCode.FR

    def test_none_when_nothing_matches(self):
        dl = DocLocale(default_locale=LocaleCode.EN)
        dl.add_translation("d1", LocaleCode.FR, "Bonjour")
        result = dl.select_best_locale("d1", [LocaleCode.JA])
        # default EN unavailable, no canonical, returns None
        assert result is None

    def test_canonical_fallback(self):
        dl = DocLocale(default_locale=LocaleCode.AR)
        dl.add_translation("d1", LocaleCode.RU, "Привет", is_canonical=True)
        result = dl.select_best_locale("d1", [LocaleCode.JA])
        assert result is LocaleCode.RU


# ---------------------------------------------------------------------------
# set_canonical
# ---------------------------------------------------------------------------
class TestSetCanonical:
    def test_set_existing_locale(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.add_translation("d1", LocaleCode.RU, "Привет")
        assert dl.set_canonical("d1", LocaleCode.RU) is True
        assert dl.canonical("d1").locale is LocaleCode.RU

    def test_set_unknown_locale_fails(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        assert dl.set_canonical("d1", LocaleCode.JA) is False

    def test_set_unknown_doc_fails(self):
        dl = DocLocale()
        assert dl.set_canonical("nope", LocaleCode.EN) is False

    def test_set_canonical_updates_flags(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi", is_canonical=True)
        dl.add_translation("d1", LocaleCode.RU, "Привет")
        dl.set_canonical("d1", LocaleCode.RU)
        en_tr = dl.get_translation("d1", LocaleCode.EN, fallback=False)
        ru_tr = dl.get_translation("d1", LocaleCode.RU, fallback=False)
        assert en_tr.is_canonical is False
        assert ru_tr.is_canonical is True


# ---------------------------------------------------------------------------
# all_locales_used
# ---------------------------------------------------------------------------
class TestAllLocalesUsed:
    def test_empty(self):
        dl = DocLocale()
        assert dl.all_locales_used() == set()

    def test_multiple(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.add_translation("d2", LocaleCode.RU, "Привет")
        dl.add_translation("d2", LocaleCode.FR, "Bonjour")
        used = dl.all_locales_used()
        assert used == {LocaleCode.EN, LocaleCode.RU, LocaleCode.FR}


# ---------------------------------------------------------------------------
# docs_count
# ---------------------------------------------------------------------------
class TestDocsCount:
    def test_total(self):
        dl = DocLocale()
        dl.register_doc("d1")
        dl.register_doc("d2")
        assert dl.docs_count() == 2

    def test_filtered_by_locale(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.add_translation("d2", LocaleCode.EN, "Hello")
        dl.add_translation("d3", LocaleCode.RU, "Привет")
        assert dl.docs_count(LocaleCode.EN) == 2
        assert dl.docs_count(LocaleCode.RU) == 1
        assert dl.docs_count(LocaleCode.FR) == 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty_repo(self):
        dl = DocLocale()
        s = dl.stats()
        assert s.total_docs == 0
        assert s.total_translations == 0
        assert s.coverage == 0.0

    def test_basic_stats(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.add_translation("d1", LocaleCode.RU, "Привет")
        dl.add_translation("d2", LocaleCode.EN, "Hello")
        s = dl.stats(required_locales=[LocaleCode.EN, LocaleCode.RU])
        assert s.total_docs == 2
        assert s.total_translations == 3
        assert s.by_locale.get("en") == 2
        assert s.by_locale.get("ru") == 1
        # d2 missing RU
        assert ("d2", "ru") in s.missing_translations
        # 3 / (2*2) = 0.75
        assert s.coverage == pytest.approx(0.75)

    def test_stats_default_required_uses_all_used(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.add_translation("d2", LocaleCode.RU, "Привет")
        s = dl.stats()
        # both en and ru in by_locale, 2 docs, 2 translations
        assert s.total_docs == 2
        assert s.total_translations == 2


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------
class TestClear:
    def test_clear_removes_everything(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi", is_canonical=True)
        dl.add_translation("d2", LocaleCode.RU, "Привет")
        dl.clear()
        assert dl.total_docs == 0
        assert dl.total_translations == 0
        assert dl.all_locales_used() == set()
        assert dl.canonical("d1") is None


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_total_translations_property(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.add_translation("d1", LocaleCode.RU, "Привет")
        assert dl.total_translations == 2

    def test_total_docs_property(self):
        dl = DocLocale()
        dl.register_doc("d1")
        dl.register_doc("d2")
        assert dl.total_docs == 2

    def test_default_locale_initial(self):
        dl = DocLocale(default_locale=LocaleCode.RU)
        dl.add_translation("d1", LocaleCode.RU, "Привет")
        # ask for FR, fallback resolves to RU (default)
        tr = dl.get_translation("d1", LocaleCode.FR, fallback=True)
        assert tr.locale is LocaleCode.RU

    def test_register_then_add_increments(self):
        dl = DocLocale()
        dl.register_doc("d1")
        before = dl.total_docs
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        assert dl.total_docs == before

    def test_empty_text_detect(self):
        dl = DocLocale()
        assert dl.detect_locale("") is LocaleCode.UNKNOWN

    def test_canonical_locale_persisted_after_translation(self):
        dl = DocLocale()
        dl.register_doc("d1", canonical_locale=LocaleCode.RU)
        dl.add_translation("d1", LocaleCode.RU, "Привет")
        tr = dl.get_translation("d1", LocaleCode.RU, fallback=False)
        assert tr.is_canonical is True

    def test_remove_then_add_again(self):
        dl = DocLocale()
        dl.add_translation("d1", LocaleCode.EN, "Hi")
        dl.remove_translation("d1", LocaleCode.EN)
        dl.add_translation("d1", LocaleCode.EN, "Hello")
        assert dl.get_translation("d1", LocaleCode.EN).content == "Hello"
