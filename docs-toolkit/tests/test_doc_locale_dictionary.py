"""Tests for ``docstoolkit.doc_locale_dictionary``."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_locale_dictionary import (
    DictionaryStats,
    DocLocaleDictionary,
    Translation,
)


# ---------------------------------------------------------------------------
# TestTranslationDataclass
# ---------------------------------------------------------------------------
class TestTranslationDataclass:
    def test_construct_with_defaults(self):
        t = Translation(key="greeting", locale="en", value="Hello")
        assert t.key == "greeting"
        assert t.locale == "en"
        assert t.value == "Hello"
        assert t.updated_at == 0.0

    def test_construct_with_timestamp(self):
        t = Translation(key="greeting", locale="en", value="Hi", updated_at=123.5)
        assert t.updated_at == 123.5

    def test_equality(self):
        a = Translation(key="k", locale="en", value="v", updated_at=1.0)
        b = Translation(key="k", locale="en", value="v", updated_at=1.0)
        assert a == b

    def test_inequality_on_value(self):
        a = Translation(key="k", locale="en", value="v1")
        b = Translation(key="k", locale="en", value="v2")
        assert a != b

    def test_inequality_on_locale(self):
        a = Translation(key="k", locale="en", value="v")
        b = Translation(key="k", locale="fr", value="v")
        assert a != b

    def test_fields_mutable(self):
        t = Translation(key="k", locale="en", value="v")
        t.value = "new"
        assert t.value == "new"


# ---------------------------------------------------------------------------
# TestDictionaryStatsDataclass
# ---------------------------------------------------------------------------
class TestDictionaryStatsDataclass:
    def test_construct_with_defaults(self):
        s = DictionaryStats(total_translations=0, unique_keys=0, unique_locales=0)
        assert s.coverage_by_locale == {}

    def test_construct_with_coverage(self):
        s = DictionaryStats(
            total_translations=3,
            unique_keys=2,
            unique_locales=2,
            coverage_by_locale={"en": 2, "fr": 1},
        )
        assert s.coverage_by_locale == {"en": 2, "fr": 1}

    def test_coverage_default_is_independent(self):
        s1 = DictionaryStats(total_translations=0, unique_keys=0, unique_locales=0)
        s2 = DictionaryStats(total_translations=0, unique_keys=0, unique_locales=0)
        s1.coverage_by_locale["x"] = 1
        assert s2.coverage_by_locale == {}


# ---------------------------------------------------------------------------
# TestSetTranslation
# ---------------------------------------------------------------------------
class TestSetTranslation:
    def test_set_returns_translation(self):
        d = DocLocaleDictionary()
        t = d.set_translation("en", "hi", "Hello")
        assert isinstance(t, Translation)
        assert t.locale == "en"
        assert t.key == "hi"
        assert t.value == "Hello"

    def test_set_assigns_updated_at(self):
        d = DocLocaleDictionary()
        t = d.set_translation("en", "hi", "Hello", now=42.0)
        assert t.updated_at == 42.0

    def test_set_default_timestamp_is_set(self):
        d = DocLocaleDictionary()
        t = d.set_translation("en", "hi", "Hello")
        assert t.updated_at > 0.0

    def test_set_persists(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "hi", "Hello")
        assert d.get_translation("en", "hi") == "Hello"

    def test_set_overwrites_existing(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "hi", "Hello")
        d.set_translation("en", "hi", "Howdy")
        assert d.get_translation("en", "hi") == "Howdy"

    def test_set_multiple_locales_for_same_key(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "hi", "Hello")
        d.set_translation("fr", "hi", "Bonjour")
        assert d.get_translation("en", "hi") == "Hello"
        assert d.get_translation("fr", "hi") == "Bonjour"


# ---------------------------------------------------------------------------
# TestGetTranslation
# ---------------------------------------------------------------------------
class TestGetTranslation:
    def test_get_missing_returns_none(self):
        d = DocLocaleDictionary()
        assert d.get_translation("en", "nope") is None

    def test_get_existing(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k", "v")
        assert d.get_translation("en", "k") == "v"

    def test_get_wrong_locale(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k", "v")
        assert d.get_translation("fr", "k") is None

    def test_get_wrong_key(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k", "v")
        assert d.get_translation("en", "other") is None

    def test_get_does_not_use_fallback(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k", "v")
        d.set_fallback_chain(["en"])
        assert d.get_translation("fr", "k") is None


# ---------------------------------------------------------------------------
# TestLookup
# ---------------------------------------------------------------------------
class TestLookup:
    def test_lookup_exact_match(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "hi", "Hello")
        assert d.lookup("en", "hi") == "Hello"

    def test_lookup_no_match_no_fallback(self):
        d = DocLocaleDictionary()
        assert d.lookup("en", "hi") is None

    def test_lookup_uses_fallback_chain(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "hi", "Hello")
        d.set_fallback_chain(["en"])
        assert d.lookup("fr", "hi") == "Hello"

    def test_lookup_walks_chain_in_order(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "hi", "Hello")
        d.set_translation("de", "hi", "Hallo")
        d.set_fallback_chain(["de", "en"])
        assert d.lookup("fr", "hi") == "Hallo"

    def test_lookup_skips_self_in_chain(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "hi", "Hello")
        d.set_fallback_chain(["fr", "en"])
        # asking for fr — fr is in chain but skipped, en provides value
        assert d.lookup("fr", "hi") == "Hello"

    def test_lookup_exact_takes_priority_over_fallback(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "hi", "Hello")
        d.set_translation("fr", "hi", "Bonjour")
        d.set_fallback_chain(["en"])
        assert d.lookup("fr", "hi") == "Bonjour"

    def test_lookup_chain_with_missing_key_returns_none(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "other", "X")
        d.set_fallback_chain(["en"])
        assert d.lookup("fr", "hi") is None

    def test_lookup_with_empty_chain(self):
        d = DocLocaleDictionary()
        d.set_fallback_chain([])
        assert d.lookup("en", "hi") is None


# ---------------------------------------------------------------------------
# TestDelete
# ---------------------------------------------------------------------------
class TestDelete:
    def test_delete_existing_returns_true(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k", "v")
        assert d.delete("en", "k") is True

    def test_delete_missing_returns_false(self):
        d = DocLocaleDictionary()
        assert d.delete("en", "k") is False

    def test_delete_removes_value(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k", "v")
        d.delete("en", "k")
        assert d.get_translation("en", "k") is None

    def test_delete_cleans_secondary_indices(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k", "v")
        d.delete("en", "k")
        assert d.keys_for_locale("en") == []
        assert d.locales_for_key("k") == []

    def test_delete_one_keeps_others(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k", "v1")
        d.set_translation("fr", "k", "v2")
        d.delete("en", "k")
        assert d.get_translation("fr", "k") == "v2"
        assert d.locales_for_key("k") == ["fr"]


# ---------------------------------------------------------------------------
# TestFallbackChain
# ---------------------------------------------------------------------------
class TestFallbackChain:
    def test_default_chain_empty(self):
        d = DocLocaleDictionary()
        assert d.get_fallback_chain() == []

    def test_set_then_get(self):
        d = DocLocaleDictionary()
        d.set_fallback_chain(["en", "de"])
        assert d.get_fallback_chain() == ["en", "de"]

    def test_set_copies_input(self):
        d = DocLocaleDictionary()
        original = ["en", "de"]
        d.set_fallback_chain(original)
        original.append("fr")
        assert d.get_fallback_chain() == ["en", "de"]

    def test_get_returns_copy(self):
        d = DocLocaleDictionary()
        d.set_fallback_chain(["en"])
        out = d.get_fallback_chain()
        out.append("xx")
        assert d.get_fallback_chain() == ["en"]

    def test_replace_chain(self):
        d = DocLocaleDictionary()
        d.set_fallback_chain(["en", "de"])
        d.set_fallback_chain(["ja"])
        assert d.get_fallback_chain() == ["ja"]


# ---------------------------------------------------------------------------
# TestKeysForLocale
# ---------------------------------------------------------------------------
class TestKeysForLocale:
    def test_empty(self):
        d = DocLocaleDictionary()
        assert d.keys_for_locale("en") == []

    def test_sorted(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "b", "1")
        d.set_translation("en", "a", "2")
        d.set_translation("en", "c", "3")
        assert d.keys_for_locale("en") == ["a", "b", "c"]

    def test_only_for_locale(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.set_translation("fr", "b", "2")
        assert d.keys_for_locale("en") == ["a"]


# ---------------------------------------------------------------------------
# TestLocalesForKey
# ---------------------------------------------------------------------------
class TestLocalesForKey:
    def test_empty(self):
        d = DocLocaleDictionary()
        assert d.locales_for_key("k") == []

    def test_sorted(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k", "x")
        d.set_translation("de", "k", "x")
        d.set_translation("fr", "k", "x")
        assert d.locales_for_key("k") == ["de", "en", "fr"]

    def test_only_for_key(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k1", "x")
        d.set_translation("fr", "k2", "x")
        assert d.locales_for_key("k1") == ["en"]


# ---------------------------------------------------------------------------
# TestMissingTranslations
# ---------------------------------------------------------------------------
class TestMissingTranslations:
    def test_no_data(self):
        d = DocLocaleDictionary()
        assert d.missing_translations("fr", "en") == []

    def test_basic_missing(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "x")
        d.set_translation("en", "b", "y")
        d.set_translation("fr", "a", "x")
        assert d.missing_translations("fr", "en") == ["b"]

    def test_none_missing(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "x")
        d.set_translation("fr", "a", "x")
        assert d.missing_translations("fr", "en") == []

    def test_all_missing(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "x")
        d.set_translation("en", "b", "y")
        assert d.missing_translations("fr", "en") == ["a", "b"]

    def test_sorted_output(self):
        d = DocLocaleDictionary()
        for k in ["zz", "aa", "mm"]:
            d.set_translation("en", k, "x")
        assert d.missing_translations("fr", "en") == ["aa", "mm", "zz"]


# ---------------------------------------------------------------------------
# TestClearLocale
# ---------------------------------------------------------------------------
class TestClearLocale:
    def test_clear_empty(self):
        d = DocLocaleDictionary()
        assert d.clear_locale("en") == 0

    def test_clear_count(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.set_translation("en", "b", "2")
        d.set_translation("en", "c", "3")
        assert d.clear_locale("en") == 3

    def test_clear_removes_entries(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.clear_locale("en")
        assert d.get_translation("en", "a") is None
        assert d.keys_for_locale("en") == []

    def test_clear_keeps_other_locales(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.set_translation("fr", "a", "2")
        d.clear_locale("en")
        assert d.get_translation("fr", "a") == "2"
        assert d.locales_for_key("a") == ["fr"]

    def test_clear_removes_key_when_orphaned(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.clear_locale("en")
        assert d.locales_for_key("a") == []
        assert d.all_keys() == []


# ---------------------------------------------------------------------------
# TestClearKey
# ---------------------------------------------------------------------------
class TestClearKey:
    def test_clear_empty(self):
        d = DocLocaleDictionary()
        assert d.clear_key("a") == 0

    def test_clear_count(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.set_translation("fr", "a", "2")
        d.set_translation("de", "a", "3")
        assert d.clear_key("a") == 3

    def test_clear_removes_entries(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.set_translation("fr", "a", "2")
        d.clear_key("a")
        assert d.get_translation("en", "a") is None
        assert d.get_translation("fr", "a") is None

    def test_clear_keeps_other_keys(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.set_translation("en", "b", "2")
        d.clear_key("a")
        assert d.get_translation("en", "b") == "2"
        assert d.keys_for_locale("en") == ["b"]

    def test_clear_removes_locale_when_orphaned(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.clear_key("a")
        assert d.all_locales() == []


# ---------------------------------------------------------------------------
# TestAllKeysAndLocales
# ---------------------------------------------------------------------------
class TestAllKeysAndLocales:
    def test_all_keys_empty(self):
        d = DocLocaleDictionary()
        assert d.all_keys() == []

    def test_all_keys_unique_sorted(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "b", "x")
        d.set_translation("fr", "b", "x")
        d.set_translation("en", "a", "x")
        assert d.all_keys() == ["a", "b"]

    def test_all_locales_empty(self):
        d = DocLocaleDictionary()
        assert d.all_locales() == []

    def test_all_locales_unique_sorted(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "x")
        d.set_translation("fr", "a", "x")
        d.set_translation("en", "b", "x")
        assert d.all_locales() == ["en", "fr"]


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty(self):
        d = DocLocaleDictionary()
        s = d.stats()
        assert s.total_translations == 0
        assert s.unique_keys == 0
        assert s.unique_locales == 0
        assert s.coverage_by_locale == {}

    def test_total_translations(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.set_translation("fr", "a", "2")
        d.set_translation("en", "b", "3")
        s = d.stats()
        assert s.total_translations == 3

    def test_unique_keys_and_locales(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.set_translation("fr", "a", "2")
        d.set_translation("en", "b", "3")
        s = d.stats()
        assert s.unique_keys == 2
        assert s.unique_locales == 2

    def test_coverage_by_locale(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "a", "1")
        d.set_translation("en", "b", "2")
        d.set_translation("fr", "a", "3")
        s = d.stats()
        assert s.coverage_by_locale == {"en": 2, "fr": 1}

    def test_stats_returns_instance(self):
        d = DocLocaleDictionary()
        assert isinstance(d.stats(), DictionaryStats)


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_writes(self):
        d = DocLocaleDictionary()

        def writer(locale: str, start: int):
            for i in range(start, start + 50):
                d.set_translation(locale, f"k{i}", f"v{i}")

        threads = [
            threading.Thread(target=writer, args=("en", 0)),
            threading.Thread(target=writer, args=("fr", 100)),
            threading.Thread(target=writer, args=("de", 200)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = d.stats()
        assert s.total_translations == 150
        assert s.unique_locales == 3

    def test_concurrent_reads_and_writes(self):
        d = DocLocaleDictionary()
        d.set_translation("en", "k", "v")

        errors: list = []

        def reader():
            try:
                for _ in range(200):
                    d.get_translation("en", "k")
                    d.lookup("en", "k")
                    d.all_keys()
            except Exception as exc:  # pragma: no cover - defensive
                errors.append(exc)

        def writer():
            try:
                for i in range(200):
                    d.set_translation("en", "k", f"v{i}")
            except Exception as exc:  # pragma: no cover - defensive
                errors.append(exc)

        threads = [threading.Thread(target=reader) for _ in range(3)] + [
            threading.Thread(target=writer) for _ in range(2)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == []
        assert d.get_translation("en", "k") is not None

    def test_concurrent_fallback_chain_updates(self):
        d = DocLocaleDictionary()

        def setter(chain):
            for _ in range(100):
                d.set_fallback_chain(chain)

        t1 = threading.Thread(target=setter, args=(["en", "de"],))
        t2 = threading.Thread(target=setter, args=(["fr", "ja"],))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # Either chain should be present, never partial
        assert d.get_fallback_chain() in (["en", "de"], ["fr", "ja"])
