"""Tests for E317 DocTranslationStore."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_translation_store import (
    DocTranslationStore,
    Translation,
    TranslationStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_store() -> DocTranslationStore:
    return DocTranslationStore()


# ---------------------------------------------------------------------------
# TestTranslationDataclass
# ---------------------------------------------------------------------------

class TestTranslationDataclass:
    def test_required_fields(self):
        t = Translation(doc_id="d1", locale="en", field="title", value="Hello")
        assert t.doc_id == "d1"
        assert t.locale == "en"
        assert t.field == "title"
        assert t.value == "Hello"

    def test_default_translated_at(self):
        t = Translation(doc_id="d1", locale="en", field="title", value="Hello")
        assert t.translated_at == 0.0

    def test_default_translator(self):
        t = Translation(doc_id="d1", locale="en", field="title", value="Hello")
        assert t.translator == ""

    def test_explicit_translated_at(self):
        t = Translation(doc_id="d1", locale="en", field="title", value="Hi", translated_at=9.99)
        assert t.translated_at == 9.99

    def test_explicit_translator(self):
        t = Translation(doc_id="d1", locale="en", field="title", value="Hi", translator="gpt-4")
        assert t.translator == "gpt-4"

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(Translation)


# ---------------------------------------------------------------------------
# TestTranslationStatsDataclass
# ---------------------------------------------------------------------------

class TestTranslationStatsDataclass:
    def test_fields(self):
        s = TranslationStats(
            total_translations=10,
            unique_docs=3,
            unique_locales=2,
            unique_fields=4,
        )
        assert s.total_translations == 10
        assert s.unique_docs == 3
        assert s.unique_locales == 2
        assert s.unique_fields == 4

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(TranslationStats)

    def test_zero_values(self):
        s = TranslationStats(
            total_translations=0,
            unique_docs=0,
            unique_locales=0,
            unique_fields=0,
        )
        assert s.total_translations == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_store(self):
        store = make_store()
        assert store.stats().total_translations == 0

    def test_all_locales_empty(self):
        store = make_store()
        assert store.all_locales() == []

    def test_all_doc_ids_empty(self):
        store = make_store()
        assert store.all_doc_ids() == []


# ---------------------------------------------------------------------------
# TestSet
# ---------------------------------------------------------------------------

class TestSet:
    def test_set_returns_translation(self):
        store = make_store()
        t = store.set("d1", "en", "title", "Hello")
        assert isinstance(t, Translation)

    def test_set_stores_value(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        t = store.get("d1", "en", "title")
        assert t is not None
        assert t.value == "Hello"

    def test_set_stores_doc_id(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        t = store.get("d1", "en", "title")
        assert t.doc_id == "d1"

    def test_set_stores_locale(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        t = store.get("d1", "en", "title")
        assert t.locale == "en"

    def test_set_stores_field(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        t = store.get("d1", "en", "title")
        assert t.field == "title"

    def test_set_replaces_existing(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        store.set("d1", "en", "title", "World")
        t = store.get("d1", "en", "title")
        assert t.value == "World"

    def test_set_auto_timestamp(self):
        store = make_store()
        before = time.time()
        t = store.set("d1", "en", "title", "Hello")
        after = time.time()
        assert before <= t.translated_at <= after

    def test_set_custom_timestamp(self):
        store = make_store()
        t = store.set("d1", "en", "title", "Hello", now=1234567890.0)
        assert t.translated_at == 1234567890.0

    def test_set_translator(self):
        store = make_store()
        t = store.set("d1", "en", "title", "Hello", translator="human")
        assert t.translator == "human"

    def test_set_multiple_fields(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        store.set("d1", "en", "body", "World")
        assert store.stats().total_translations == 2

    def test_set_multiple_locales(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        store.set("d1", "ru", "title", "Привет")
        assert store.stats().total_translations == 2


# ---------------------------------------------------------------------------
# TestGet
# ---------------------------------------------------------------------------

class TestGet:
    def test_get_found(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        t = store.get("d1", "en", "title")
        assert t is not None
        assert t.value == "Hello"

    def test_get_not_found_wrong_locale(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.get("d1", "ru", "title") is None

    def test_get_not_found_wrong_field(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.get("d1", "en", "body") is None

    def test_get_not_found_wrong_doc(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.get("d2", "en", "title") is None

    def test_get_empty_store(self):
        store = make_store()
        assert store.get("d1", "en", "title") is None


# ---------------------------------------------------------------------------
# TestDelete
# ---------------------------------------------------------------------------

class TestDelete:
    def test_delete_existing_returns_true(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.delete("d1", "en", "title") is True

    def test_delete_removes_entry(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        store.delete("d1", "en", "title")
        assert store.get("d1", "en", "title") is None

    def test_delete_missing_returns_false(self):
        store = make_store()
        assert store.delete("d1", "en", "title") is False

    def test_delete_leaves_other_entries(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        store.set("d1", "en", "body", "World")
        store.delete("d1", "en", "title")
        assert store.get("d1", "en", "body") is not None

    def test_delete_twice_returns_false(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        store.delete("d1", "en", "title")
        assert store.delete("d1", "en", "title") is False


# ---------------------------------------------------------------------------
# TestGetField
# ---------------------------------------------------------------------------

class TestGetField:
    def test_get_field_found(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.get_field("d1", "title", "en") == "Hello"

    def test_get_field_not_found_no_fallback(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.get_field("d1", "title", "ru") is None

    def test_get_field_fallback_used(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        result = store.get_field("d1", "title", "ru", fallback_locale="en")
        assert result == "Hello"

    def test_get_field_primary_preferred_over_fallback(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello EN")
        store.set("d1", "ru", "title", "Привет RU")
        result = store.get_field("d1", "title", "ru", fallback_locale="en")
        assert result == "Привет RU"

    def test_get_field_fallback_missing_too(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        result = store.get_field("d1", "title", "ru", fallback_locale="de")
        assert result is None

    def test_get_field_no_fallback_arg_returns_none(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.get_field("d1", "title", "de") is None


# ---------------------------------------------------------------------------
# TestTranslationsForDoc
# ---------------------------------------------------------------------------

class TestTranslationsForDoc:
    def test_single_entry(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        result = store.translations_for_doc("d1")
        assert len(result) == 1
        assert result[0].value == "Hello"

    def test_sorted_by_locale_then_field(self):
        store = make_store()
        store.set("d1", "ru", "title", "Заголовок")
        store.set("d1", "en", "body", "Body EN")
        store.set("d1", "en", "title", "Title EN")
        result = store.translations_for_doc("d1")
        keys = [(t.locale, t.field) for t in result]
        assert keys == sorted(keys)

    def test_empty_for_unknown_doc(self):
        store = make_store()
        assert store.translations_for_doc("unknown") == []

    def test_does_not_include_other_docs(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello d1")
        store.set("d2", "en", "title", "Hello d2")
        result = store.translations_for_doc("d1")
        assert all(t.doc_id == "d1" for t in result)


# ---------------------------------------------------------------------------
# TestTranslationsForLocale
# ---------------------------------------------------------------------------

class TestTranslationsForLocale:
    def test_single_entry(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        result = store.translations_for_locale("en")
        assert len(result) == 1

    def test_sorted_by_doc_id_then_field(self):
        store = make_store()
        store.set("d2", "en", "title", "Title d2")
        store.set("d1", "en", "body", "Body d1")
        store.set("d1", "en", "title", "Title d1")
        result = store.translations_for_locale("en")
        keys = [(t.doc_id, t.field) for t in result]
        assert keys == sorted(keys)

    def test_cross_doc(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        store.set("d2", "en", "title", "World")
        store.set("d3", "ru", "title", "Нет")
        result = store.translations_for_locale("en")
        assert len(result) == 2
        assert all(t.locale == "en" for t in result)

    def test_empty_for_unknown_locale(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.translations_for_locale("ja") == []


# ---------------------------------------------------------------------------
# TestLocalesForDoc
# ---------------------------------------------------------------------------

class TestLocalesForDoc:
    def test_single_locale(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.locales_for_doc("d1") == ["en"]

    def test_multiple_locales_sorted(self):
        store = make_store()
        store.set("d1", "ru", "title", "Заголовок")
        store.set("d1", "de", "title", "Titel")
        store.set("d1", "en", "title", "Title")
        result = store.locales_for_doc("d1")
        assert result == sorted(result)
        assert set(result) == {"en", "ru", "de"}

    def test_unique_locales(self):
        store = make_store()
        store.set("d1", "en", "title", "T")
        store.set("d1", "en", "body", "B")
        assert store.locales_for_doc("d1") == ["en"]

    def test_empty_for_unknown_doc(self):
        store = make_store()
        assert store.locales_for_doc("unknown") == []


# ---------------------------------------------------------------------------
# TestFieldsForDoc
# ---------------------------------------------------------------------------

class TestFieldsForDoc:
    def test_single_field(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.fields_for_doc("d1", "en") == ["title"]

    def test_multiple_fields_sorted(self):
        store = make_store()
        store.set("d1", "en", "summary", "Sum")
        store.set("d1", "en", "body", "Body")
        store.set("d1", "en", "title", "Title")
        result = store.fields_for_doc("d1", "en")
        assert result == sorted(result)
        assert set(result) == {"title", "body", "summary"}

    def test_does_not_include_other_locale_fields(self):
        store = make_store()
        store.set("d1", "en", "title", "Title EN")
        store.set("d1", "ru", "body", "Тело RU")
        assert store.fields_for_doc("d1", "en") == ["title"]
        assert store.fields_for_doc("d1", "ru") == ["body"]

    def test_empty_for_unknown_locale(self):
        store = make_store()
        store.set("d1", "en", "title", "Hello")
        assert store.fields_for_doc("d1", "de") == []


# ---------------------------------------------------------------------------
# TestDeleteDoc
# ---------------------------------------------------------------------------

class TestDeleteDoc:
    def test_returns_count(self):
        store = make_store()
        store.set("d1", "en", "title", "T")
        store.set("d1", "ru", "title", "З")
        store.set("d1", "en", "body", "B")
        assert store.delete_doc("d1") == 3

    def test_all_entries_removed(self):
        store = make_store()
        store.set("d1", "en", "title", "T")
        store.set("d1", "ru", "body", "B")
        store.delete_doc("d1")
        assert store.translations_for_doc("d1") == []

    def test_does_not_remove_other_docs(self):
        store = make_store()
        store.set("d1", "en", "title", "T1")
        store.set("d2", "en", "title", "T2")
        store.delete_doc("d1")
        assert store.get("d2", "en", "title") is not None

    def test_unknown_doc_returns_zero(self):
        store = make_store()
        assert store.delete_doc("ghost") == 0


# ---------------------------------------------------------------------------
# TestDeleteLocale
# ---------------------------------------------------------------------------

class TestDeleteLocale:
    def test_returns_count(self):
        store = make_store()
        store.set("d1", "en", "title", "T1")
        store.set("d2", "en", "body", "B2")
        store.set("d1", "ru", "title", "З1")
        assert store.delete_locale("en") == 2

    def test_removes_across_docs(self):
        store = make_store()
        store.set("d1", "en", "title", "T1")
        store.set("d2", "en", "title", "T2")
        store.delete_locale("en")
        assert store.get("d1", "en", "title") is None
        assert store.get("d2", "en", "title") is None

    def test_leaves_other_locales(self):
        store = make_store()
        store.set("d1", "en", "title", "EN")
        store.set("d1", "ru", "title", "RU")
        store.delete_locale("en")
        assert store.get("d1", "ru", "title") is not None

    def test_unknown_locale_returns_zero(self):
        store = make_store()
        assert store.delete_locale("klingon") == 0


# ---------------------------------------------------------------------------
# TestAllLocales
# ---------------------------------------------------------------------------

class TestAllLocales:
    def test_sorted(self):
        store = make_store()
        store.set("d1", "ru", "title", "Z")
        store.set("d1", "en", "title", "A")
        store.set("d2", "de", "title", "B")
        result = store.all_locales()
        assert result == sorted(result)
        assert set(result) == {"en", "ru", "de"}

    def test_unique(self):
        store = make_store()
        store.set("d1", "en", "title", "T")
        store.set("d2", "en", "title", "T")
        assert store.all_locales() == ["en"]

    def test_empty(self):
        store = make_store()
        assert store.all_locales() == []


# ---------------------------------------------------------------------------
# TestAllDocIds
# ---------------------------------------------------------------------------

class TestAllDocIds:
    def test_sorted(self):
        store = make_store()
        store.set("doc_c", "en", "title", "C")
        store.set("doc_a", "en", "title", "A")
        store.set("doc_b", "en", "title", "B")
        result = store.all_doc_ids()
        assert result == sorted(result)
        assert set(result) == {"doc_a", "doc_b", "doc_c"}

    def test_unique(self):
        store = make_store()
        store.set("d1", "en", "title", "T")
        store.set("d1", "ru", "title", "T")
        assert store.all_doc_ids() == ["d1"]

    def test_empty(self):
        store = make_store()
        assert store.all_doc_ids() == []


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_total_translations(self):
        store = make_store()
        store.set("d1", "en", "title", "T")
        store.set("d1", "ru", "title", "З")
        store.set("d2", "en", "body", "B")
        s = store.stats()
        assert s.total_translations == 3

    def test_unique_docs(self):
        store = make_store()
        store.set("d1", "en", "title", "T")
        store.set("d1", "ru", "title", "З")
        store.set("d2", "en", "title", "T2")
        s = store.stats()
        assert s.unique_docs == 2

    def test_unique_locales(self):
        store = make_store()
        store.set("d1", "en", "title", "T")
        store.set("d1", "ru", "title", "З")
        store.set("d2", "en", "body", "B")
        s = store.stats()
        assert s.unique_locales == 2

    def test_unique_fields(self):
        store = make_store()
        store.set("d1", "en", "title", "T")
        store.set("d1", "en", "body", "B")
        store.set("d2", "ru", "title", "З")
        s = store.stats()
        assert s.unique_fields == 2

    def test_empty_store_stats(self):
        store = make_store()
        s = store.stats()
        assert s.total_translations == 0
        assert s.unique_docs == 0
        assert s.unique_locales == 0
        assert s.unique_fields == 0

    def test_stats_returns_translation_stats_type(self):
        store = make_store()
        assert isinstance(store.stats(), TranslationStats)


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_set(self):
        store = make_store()
        errors: list[Exception] = []

        def worker(doc_id: str, locale: str, n: int) -> None:
            try:
                for i in range(n):
                    store.set(doc_id, locale, f"field_{i}", f"value_{i}")
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        threads = [
            threading.Thread(target=worker, args=(f"doc_{t}", f"loc_{t}", 50))
            for t in range(10)
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert errors == [], f"Thread errors: {errors}"
        # Each thread writes 50 distinct (doc, locale, field) keys
        assert store.stats().total_translations == 500

    def test_concurrent_set_same_key(self):
        """Last writer wins; no crash."""
        store = make_store()
        errors: list[Exception] = []
        results: list[str] = []

        def writer(val: str) -> None:
            try:
                t = store.set("d1", "en", "title", val)
                results.append(t.value)
            except Exception as exc:  # pragma: no cover
                errors.append(exc)

        threads = [threading.Thread(target=writer, args=(f"v{i}",)) for i in range(20)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert errors == []
        # Exactly one value should be present (last writer wins)
        assert store.stats().total_translations == 1
        stored = store.get("d1", "en", "title")
        assert stored is not None
        assert stored.value in {f"v{i}" for i in range(20)}
