"""Tests for doc_localization (E238)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_localization import (
    DocLocalization,
    LocalizationStats,
    Plural,
    Translation,
)


class TestPlural:
    def test_members(self):
        assert Plural.ZERO.value == "zero"
        assert Plural.ONE.value == "one"
        assert Plural.FEW.value == "few"
        assert Plural.MANY.value == "many"
        assert Plural.OTHER.value == "other"

    def test_distinct(self):
        assert len({Plural.ZERO, Plural.ONE, Plural.FEW, Plural.MANY, Plural.OTHER}) == 5

    def test_dict_key(self):
        d = {Plural.ONE: "one item"}
        assert d[Plural.ONE] == "one item"


class TestTranslation:
    def test_basic(self):
        t = Translation(key="hi", locale="en", text="Hello")
        assert t.key == "hi"
        assert t.locale == "en"
        assert t.text == "Hello"
        assert t.plural_forms == {}

    def test_with_plural_forms(self):
        t = Translation(
            key="items",
            locale="en",
            text="items",
            plural_forms={Plural.ONE: "item", Plural.OTHER: "items"},
        )
        assert t.plural_forms[Plural.ONE] == "item"

    def test_default_plural_forms_distinct(self):
        a = Translation(key="a", locale="en", text="A")
        b = Translation(key="b", locale="en", text="B")
        a.plural_forms[Plural.ONE] = "x"
        assert Plural.ONE not in b.plural_forms


class TestLocalizationStats:
    def test_create(self):
        s = LocalizationStats(
            total_keys=2,
            total_translations=4,
            locales=["en", "ru"],
            coverage_by_locale={"en": 1.0, "ru": 0.5},
        )
        assert s.total_keys == 2
        assert s.total_translations == 4
        assert s.locales == ["en", "ru"]
        assert s.coverage_by_locale["en"] == 1.0


class TestRegisterKey:
    def test_register_new(self):
        dl = DocLocalization()
        assert dl.register_key("greeting") is True

    def test_register_duplicate(self):
        dl = DocLocalization()
        dl.register_key("greeting")
        assert dl.register_key("greeting") is False

    def test_register_with_default(self):
        dl = DocLocalization()
        dl.register_key("hi", default_text="Hello")
        assert dl.translate("hi", "fr") == "Hello"

    def test_register_empty(self):
        dl = DocLocalization()
        assert dl.register_key("") is False

    def test_register_updates_default(self):
        dl = DocLocalization()
        dl.register_key("k")
        dl.register_key("k", default_text="default")
        assert dl.translate("k", "xx") == "default"


class TestAddTranslation:
    def test_add(self):
        dl = DocLocalization()
        dl.register_key("hi")
        t = dl.add_translation("hi", "ru", "Привет")
        assert t is not None
        assert t.text == "Привет"

    def test_add_autoregisters_key(self):
        dl = DocLocalization()
        t = dl.add_translation("new", "en", "New")
        assert t is not None
        assert dl.total_keys == 1

    def test_add_with_plural(self):
        dl = DocLocalization()
        t = dl.add_translation(
            "items", "en", "items",
            plural_forms={Plural.ONE: "item", Plural.OTHER: "items"},
        )
        assert t.plural_forms[Plural.ONE] == "item"

    def test_add_invalid_key(self):
        dl = DocLocalization()
        assert dl.add_translation("", "en", "x") is None

    def test_add_invalid_locale(self):
        dl = DocLocalization()
        assert dl.add_translation("k", "", "x") is None

    def test_replace(self):
        dl = DocLocalization()
        dl.add_translation("k", "en", "old")
        dl.add_translation("k", "en", "new")
        assert dl.get_translation("k", "en").text == "new"


class TestTranslate:
    def test_basic(self):
        dl = DocLocalization()
        dl.add_translation("hi", "en", "Hello")
        assert dl.translate("hi", "en") == "Hello"

    def test_default_locale(self):
        dl = DocLocalization(default_locale="ru")
        dl.add_translation("hi", "ru", "Привет")
        assert dl.translate("hi") == "Привет"

    def test_missing_returns_default_text(self):
        dl = DocLocalization()
        dl.register_key("hi", default_text="Hello")
        assert dl.translate("hi", "fr") == "Hello"

    def test_missing_returns_key(self):
        dl = DocLocalization()
        assert dl.translate("missing", "en") == "missing"

    def test_unregistered_key_no_translation(self):
        dl = DocLocalization()
        assert dl.translate("nope", "en") == "nope"


class TestTranslateFallback:
    def test_fallback_chain(self):
        dl = DocLocalization(default_locale="en")
        dl.set_fallback_chain(["ru", "en"])
        dl.add_translation("hi", "ru", "Привет")
        assert dl.translate("hi", "fr") == "Привет"

    def test_fallback_locale_ctor(self):
        dl = DocLocalization(default_locale="en", fallback_locale="ru")
        dl.add_translation("hi", "ru", "Привет")
        assert dl.translate("hi", "fr") == "Привет"

    def test_default_locale_fallback(self):
        dl = DocLocalization(default_locale="en")
        dl.add_translation("hi", "en", "Hello")
        assert dl.translate("hi", "xx") == "Hello"

    def test_chain_order(self):
        dl = DocLocalization(default_locale="en")
        dl.set_fallback_chain(["es", "ru"])
        dl.add_translation("hi", "ru", "Привет")
        dl.add_translation("hi", "es", "Hola")
        assert dl.translate("hi", "fr") == "Hola"

    def test_exact_locale_wins_over_fallback(self):
        dl = DocLocalization(default_locale="en")
        dl.set_fallback_chain(["en"])
        dl.add_translation("hi", "en", "Hello")
        dl.add_translation("hi", "ru", "Привет")
        assert dl.translate("hi", "ru") == "Привет"


class TestTranslateInterpolation:
    def test_basic(self):
        dl = DocLocalization()
        dl.add_translation("welcome", "en", "Hello, {name}!")
        assert dl.translate("welcome", "en", name="Alice") == "Hello, Alice!"

    def test_multiple(self):
        dl = DocLocalization()
        dl.add_translation("x", "en", "{a} + {b} = {c}")
        assert dl.translate("x", "en", a=1, b=2, c=3) == "1 + 2 = 3"

    def test_missing_placeholder_kept(self):
        dl = DocLocalization()
        dl.add_translation("x", "en", "Hello, {name}!")
        assert dl.translate("x", "en") == "Hello, {name}!"

    def test_extra_kwargs_ignored(self):
        dl = DocLocalization()
        dl.add_translation("x", "en", "Hi")
        assert dl.translate("x", "en", junk=1) == "Hi"

    def test_default_text_interpolated(self):
        dl = DocLocalization()
        dl.register_key("greet", default_text="Hi {name}")
        assert dl.translate("greet", "xx", name="Bob") == "Hi Bob"


class TestTranslatePlural:
    def test_one(self):
        dl = DocLocalization()
        dl.add_translation(
            "items", "en", "items",
            plural_forms={Plural.ONE: "1 item", Plural.OTHER: "{count} items"},
        )
        assert dl.translate_plural("items", 1, "en") == "1 item"

    def test_other(self):
        dl = DocLocalization()
        dl.add_translation(
            "items", "en", "items",
            plural_forms={Plural.ONE: "1 item", Plural.OTHER: "{count} items"},
        )
        assert dl.translate_plural("items", 5, "en") == "5 items"

    def test_zero(self):
        dl = DocLocalization()
        dl.add_translation(
            "items", "en", "items",
            plural_forms={
                Plural.ZERO: "No items",
                Plural.ONE: "1 item",
                Plural.OTHER: "{count} items",
            },
        )
        assert dl.translate_plural("items", 0, "en") == "No items"

    def test_zero_falls_back_to_other(self):
        dl = DocLocalization()
        dl.add_translation(
            "items", "en", "items",
            plural_forms={Plural.ONE: "1 item", Plural.OTHER: "{count} items"},
        )
        assert dl.translate_plural("items", 0, "en") == "0 items"

    def test_no_plural_forms_uses_text(self):
        dl = DocLocalization()
        dl.add_translation("items", "en", "{count} thing(s)")
        assert dl.translate_plural("items", 3, "en") == "3 thing(s)"

    def test_interpolation_override(self):
        dl = DocLocalization()
        dl.add_translation(
            "k", "en", "x",
            plural_forms={Plural.OTHER: "{count} {name}s"},
        )
        assert dl.translate_plural("k", 3, "en", name="apple") == "3 apples"

    def test_default_locale(self):
        dl = DocLocalization(default_locale="en")
        dl.add_translation(
            "k", "en", "x",
            plural_forms={Plural.OTHER: "{count}"},
        )
        assert dl.translate_plural("k", 7) == "7"

    def test_missing_translation_uses_key(self):
        dl = DocLocalization()
        result = dl.translate_plural("missing", 5, "en")
        assert result == "missing"


class TestSetFallbackChain:
    def test_set(self):
        dl = DocLocalization()
        dl.set_fallback_chain(["a", "b", "c"])
        dl.add_translation("k", "a", "AAA")
        assert dl.translate("k", "z") == "AAA"

    def test_overwrite(self):
        dl = DocLocalization()
        dl.set_fallback_chain(["a"])
        dl.set_fallback_chain(["b"])
        dl.add_translation("k", "b", "BBB")
        assert dl.translate("k", "z") == "BBB"

    def test_empty(self):
        dl = DocLocalization()
        dl.set_fallback_chain([])
        # no error
        assert dl.translate("nokey", "en") == "nokey"


class TestSetDefaultLocale:
    def test_set(self):
        dl = DocLocalization(default_locale="en")
        dl.set_default_locale("ru")
        dl.add_translation("k", "ru", "RR")
        assert dl.translate("k") == "RR"

    def test_change_affects_lookup(self):
        dl = DocLocalization(default_locale="en")
        dl.add_translation("k", "en", "E")
        dl.add_translation("k", "fr", "F")
        dl.set_default_locale("fr")
        assert dl.translate("k") == "F"


class TestGetTranslation:
    def test_found(self):
        dl = DocLocalization()
        dl.add_translation("k", "en", "E")
        t = dl.get_translation("k", "en")
        assert t is not None
        assert t.text == "E"

    def test_missing_locale(self):
        dl = DocLocalization()
        dl.add_translation("k", "en", "E")
        assert dl.get_translation("k", "ru") is None

    def test_missing_key(self):
        dl = DocLocalization()
        assert dl.get_translation("missing", "en") is None


class TestAvailableLocales:
    def test_all(self):
        dl = DocLocalization()
        dl.add_translation("k", "en", "E")
        dl.add_translation("k", "ru", "R")
        dl.add_translation("k2", "es", "S")
        assert dl.available_locales() == ["en", "es", "ru"]

    def test_per_key(self):
        dl = DocLocalization()
        dl.add_translation("k", "en", "E")
        dl.add_translation("k", "ru", "R")
        dl.add_translation("k2", "es", "S")
        assert dl.available_locales("k") == ["en", "ru"]

    def test_unknown_key(self):
        dl = DocLocalization()
        assert dl.available_locales("x") == []

    def test_empty(self):
        dl = DocLocalization()
        assert dl.available_locales() == []


class TestMissingKeys:
    def test_basic(self):
        dl = DocLocalization()
        dl.register_key("a")
        dl.register_key("b")
        dl.add_translation("a", "en", "A")
        assert dl.missing_keys("en") == ["b"]

    def test_none_missing(self):
        dl = DocLocalization()
        dl.register_key("a")
        dl.add_translation("a", "en", "A")
        assert dl.missing_keys("en") == []

    def test_all_missing(self):
        dl = DocLocalization()
        dl.register_key("a")
        dl.register_key("b")
        assert sorted(dl.missing_keys("en")) == ["a", "b"]


class TestCoverage:
    def test_full(self):
        dl = DocLocalization()
        dl.register_key("a")
        dl.register_key("b")
        dl.add_translation("a", "en", "A")
        dl.add_translation("b", "en", "B")
        assert dl.coverage("en") == 1.0

    def test_half(self):
        dl = DocLocalization()
        dl.register_key("a")
        dl.register_key("b")
        dl.add_translation("a", "en", "A")
        assert dl.coverage("en") == 0.5

    def test_zero_keys(self):
        dl = DocLocalization()
        assert dl.coverage("en") == 0.0

    def test_unknown_locale(self):
        dl = DocLocalization()
        dl.register_key("a")
        assert dl.coverage("xx") == 0.0


class TestStats:
    def test_basic(self):
        dl = DocLocalization()
        dl.register_key("a")
        dl.register_key("b")
        dl.add_translation("a", "en", "A")
        dl.add_translation("a", "ru", "R")
        s = dl.stats()
        assert s.total_keys == 2
        assert s.total_translations == 2
        assert sorted(s.locales) == ["en", "ru"]

    def test_coverage_in_stats(self):
        dl = DocLocalization()
        dl.register_key("a")
        dl.register_key("b")
        dl.add_translation("a", "en", "A")
        s = dl.stats()
        assert s.coverage_by_locale["en"] == 0.5

    def test_empty(self):
        dl = DocLocalization()
        s = dl.stats()
        assert s.total_keys == 0
        assert s.total_translations == 0
        assert s.locales == []


class TestRemoveKey:
    def test_remove(self):
        dl = DocLocalization()
        dl.register_key("a")
        assert dl.remove_key("a") is True
        assert dl.total_keys == 0

    def test_remove_unknown(self):
        dl = DocLocalization()
        assert dl.remove_key("x") is False

    def test_remove_clears_translations(self):
        dl = DocLocalization()
        dl.add_translation("a", "en", "A")
        dl.remove_key("a")
        assert dl.get_translation("a", "en") is None


class TestRemoveTranslation:
    def test_remove(self):
        dl = DocLocalization()
        dl.add_translation("a", "en", "A")
        assert dl.remove_translation("a", "en") is True
        assert dl.get_translation("a", "en") is None

    def test_remove_unknown_locale(self):
        dl = DocLocalization()
        dl.add_translation("a", "en", "A")
        assert dl.remove_translation("a", "ru") is False

    def test_remove_unknown_key(self):
        dl = DocLocalization()
        assert dl.remove_translation("x", "en") is False

    def test_key_persists_after_translation_removed(self):
        dl = DocLocalization()
        dl.add_translation("a", "en", "A")
        dl.remove_translation("a", "en")
        assert dl.total_keys == 1


class TestBulkLoad:
    def test_basic(self):
        dl = DocLocalization()
        n = dl.bulk_load({"en": {"a": "A", "b": "B"}, "ru": {"a": "А"}})
        assert n == 3
        assert dl.translate("a", "ru") == "А"
        assert dl.translate("b", "en") == "B"

    def test_empty(self):
        dl = DocLocalization()
        assert dl.bulk_load({}) == 0

    def test_skips_invalid(self):
        dl = DocLocalization()
        n = dl.bulk_load({"en": {"": "x", "k": None}, "": {"k": "v"}})  # type: ignore[dict-item]
        assert n == 0

    def test_overwrites(self):
        dl = DocLocalization()
        dl.add_translation("k", "en", "old")
        dl.bulk_load({"en": {"k": "new"}})
        assert dl.translate("k", "en") == "new"


class TestTotalKeys:
    def test_zero(self):
        dl = DocLocalization()
        assert dl.total_keys == 0

    def test_after_register(self):
        dl = DocLocalization()
        dl.register_key("a")
        dl.register_key("b")
        assert dl.total_keys == 2

    def test_after_add_translation(self):
        dl = DocLocalization()
        dl.add_translation("a", "en", "A")
        assert dl.total_keys == 1


class TestTotalTranslations:
    def test_zero(self):
        dl = DocLocalization()
        assert dl.total_translations == 0

    def test_count(self):
        dl = DocLocalization()
        dl.add_translation("a", "en", "A")
        dl.add_translation("a", "ru", "R")
        dl.add_translation("b", "en", "B")
        assert dl.total_translations == 3

    def test_replace_does_not_increase(self):
        dl = DocLocalization()
        dl.add_translation("a", "en", "A")
        dl.add_translation("a", "en", "B")
        assert dl.total_translations == 1


class TestClear:
    def test_clear(self):
        dl = DocLocalization()
        dl.add_translation("a", "en", "A")
        dl.set_fallback_chain(["x"])
        dl.clear()
        assert dl.total_keys == 0
        assert dl.total_translations == 0

    def test_clear_empty(self):
        dl = DocLocalization()
        dl.clear()
        assert dl.total_keys == 0


class TestEdgeCases:
    def test_thread_safety_smoke(self):
        import threading as _t
        dl = DocLocalization()

        def worker(i):
            dl.add_translation(f"k{i}", "en", f"v{i}")

        threads = [_t.Thread(target=worker, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert dl.total_translations == 20

    def test_unicode(self):
        dl = DocLocalization()
        dl.add_translation("hi", "ja", "こんにちは")
        assert dl.translate("hi", "ja") == "こんにちは"

    def test_complex_fallback(self):
        dl = DocLocalization(default_locale="en", fallback_locale="ru")
        dl.set_fallback_chain(["fr"])
        dl.add_translation("k", "fr", "F")
        dl.add_translation("k", "ru", "R")
        dl.add_translation("k", "en", "E")
        # exact match
        assert dl.translate("k", "fr") == "F"
        # use chain first (fr)
        assert dl.translate("k", "es") == "F"

    def test_count_in_plural_interpolation(self):
        dl = DocLocalization()
        dl.add_translation(
            "k", "en", "x",
            plural_forms={Plural.ONE: "1 item", Plural.OTHER: "many ({count})"},
        )
        assert dl.translate_plural("k", 7, "en") == "many (7)"

    def test_plural_negative_count(self):
        dl = DocLocalization()
        dl.add_translation(
            "k", "en", "x",
            plural_forms={Plural.OTHER: "{count} items"},
        )
        # -1 is not 0 and not 1 -> OTHER
        assert dl.translate_plural("k", -1, "en") == "-1 items"

    def test_remove_key_then_readd(self):
        dl = DocLocalization()
        dl.add_translation("a", "en", "A")
        dl.remove_key("a")
        dl.add_translation("a", "en", "B")
        assert dl.translate("a", "en") == "B"

    def test_placeholder_with_underscore_and_digits(self):
        dl = DocLocalization()
        dl.add_translation("k", "en", "{var_1} and {a2b}")
        assert dl.translate("k", "en", var_1="x", a2b="y") == "x and y"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
