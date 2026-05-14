"""Tests for doc_metadata_v2 module."""
from __future__ import annotations

import pytest

from docstoolkit.doc_metadata_v2 import (
    DocMetadataV2,
    ExtractorDef,
    MetadataField,
    MetadataRecord,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestMetadataField:
    def test_basic_construction(self):
        mf = MetadataField(name="title", value="Hello", source="manual")
        assert mf.name == "title"
        assert mf.value == "Hello"
        assert mf.source == "manual"
        assert mf.confidence == 1.0

    def test_with_confidence(self):
        mf = MetadataField(
            name="author", value="Alice", source="extractor:fm", confidence=0.7
        )
        assert mf.confidence == 0.7

    def test_value_can_be_list(self):
        mf = MetadataField(name="tags", value=["a", "b"], source="inline_tag")
        assert mf.value == ["a", "b"]

    def test_value_can_be_int(self):
        mf = MetadataField(name="year", value=2026, source="frontmatter")
        assert mf.value == 2026


class TestExtractorDef:
    def test_basic(self):
        def fn(text):
            return {}

        ed = ExtractorDef(name="x", extract=fn)
        assert ed.name == "x"
        assert ed.extract is fn
        assert ed.enabled is True
        assert ed.priority == 0

    def test_with_priority(self):
        ed = ExtractorDef(name="x", extract=lambda t: {}, priority=10)
        assert ed.priority == 10

    def test_disabled(self):
        ed = ExtractorDef(name="x", extract=lambda t: {}, enabled=False)
        assert ed.enabled is False


class TestMetadataRecord:
    def test_default(self):
        r = MetadataRecord(doc_id="d1")
        assert r.doc_id == "d1"
        assert r.fields == {}
        assert r.updated_at == 0.0

    def test_with_fields(self):
        mf = MetadataField(name="t", value="x", source="manual")
        r = MetadataRecord(doc_id="d1", fields={"t": mf}, updated_at=1.5)
        assert "t" in r.fields
        assert r.updated_at == 1.5


# ---------------------------------------------------------------------------
# Extract
# ---------------------------------------------------------------------------


class TestExtractBasic:
    def test_extract_returns_record(self):
        m = DocMetadataV2()
        r = m.extract("d1", "hello world", now=1.0)
        assert isinstance(r, MetadataRecord)
        assert r.doc_id == "d1"
        assert r.updated_at == 1.0

    def test_extract_frontmatter_fields(self):
        m = DocMetadataV2()
        content = "---\ntitle: Test\nauthor: Alice\n---\nbody"
        r = m.extract("d1", content)
        assert "title" in r.fields
        assert r.fields["title"].value == "Test"
        assert r.fields["author"].value == "Alice"

    def test_extract_inline_tags(self):
        m = DocMetadataV2()
        r = m.extract("d1", "Has #python and #ml tags")
        assert "tags" in r.fields
        assert "python" in r.fields["tags"].value
        assert "ml" in r.fields["tags"].value

    def test_extract_no_content(self):
        m = DocMetadataV2()
        r = m.extract("d1", "")
        assert r.doc_id == "d1"
        # No frontmatter/tags so likely empty
        assert isinstance(r.fields, dict)

    def test_extract_updates_existing_record(self):
        m = DocMetadataV2()
        m.extract("d1", "---\ntitle: A\n---\n", now=1.0)
        m.extract("d1", "---\nauthor: Bob\n---\n", now=2.0)
        r = m.record_for("d1")
        # First-wins: title from first call still present? No — second call
        # has different keys, so both should now exist.
        assert "title" in r.fields
        assert "author" in r.fields
        assert r.updated_at == 2.0

    def test_extract_first_wins(self):
        # Higher-priority extractor's field should win over lower-priority.
        m = DocMetadataV2()
        # frontmatter (priority 100) sets title
        m.register_extractor("low", lambda t: {"title": "FROM_LOW"}, priority=1)
        r = m.extract("d1", "---\ntitle: FROM_FM\n---\nbody")
        assert r.fields["title"].value == "FROM_FM"

    def test_extract_source_label(self):
        m = DocMetadataV2()
        r = m.extract("d1", "---\nkey: v\n---\n")
        assert r.fields["key"].source == "extractor:frontmatter"


# ---------------------------------------------------------------------------
# set_field
# ---------------------------------------------------------------------------


class TestSetField:
    def test_set_field_new_doc(self):
        m = DocMetadataV2()
        mf = m.set_field("d1", "status", "draft")
        assert mf.value == "draft"
        assert mf.source == "manual"
        assert m.total_docs == 1

    def test_set_field_overrides(self):
        m = DocMetadataV2()
        m.set_field("d1", "status", "draft")
        m.set_field("d1", "status", "published")
        assert m.get_value("d1", "status") == "published"

    def test_set_field_custom_source(self):
        m = DocMetadataV2()
        mf = m.set_field("d1", "year", 2026, source="extractor:custom")
        assert mf.source == "extractor:custom"

    def test_set_field_confidence(self):
        m = DocMetadataV2()
        mf = m.set_field("d1", "topic", "ai", confidence=0.65)
        assert mf.confidence == 0.65

    def test_set_field_updates_timestamp(self):
        m = DocMetadataV2()
        m.set_field("d1", "f", "v", now=5.0)
        assert m.record_for("d1").updated_at == 5.0


# ---------------------------------------------------------------------------
# get_field
# ---------------------------------------------------------------------------


class TestGetField:
    def test_get_existing(self):
        m = DocMetadataV2()
        m.set_field("d1", "title", "Hello")
        mf = m.get_field("d1", "title")
        assert mf is not None
        assert mf.value == "Hello"

    def test_get_missing_doc(self):
        m = DocMetadataV2()
        assert m.get_field("nope", "title") is None

    def test_get_missing_field(self):
        m = DocMetadataV2()
        m.set_field("d1", "title", "x")
        assert m.get_field("d1", "missing") is None


# ---------------------------------------------------------------------------
# get_value
# ---------------------------------------------------------------------------


class TestGetValue:
    def test_value_existing(self):
        m = DocMetadataV2()
        m.set_field("d1", "x", 42)
        assert m.get_value("d1", "x") == 42

    def test_default_missing_doc(self):
        m = DocMetadataV2()
        assert m.get_value("nope", "x", default="dflt") == "dflt"

    def test_default_missing_field(self):
        m = DocMetadataV2()
        m.set_field("d1", "x", 1)
        assert m.get_value("d1", "y", default=99) == 99

    def test_default_none(self):
        m = DocMetadataV2()
        assert m.get_value("nope", "x") is None


# ---------------------------------------------------------------------------
# remove_field
# ---------------------------------------------------------------------------


class TestRemoveField:
    def test_remove_existing(self):
        m = DocMetadataV2()
        m.set_field("d1", "k", "v")
        assert m.remove_field("d1", "k") is True
        assert m.get_field("d1", "k") is None

    def test_remove_missing(self):
        m = DocMetadataV2()
        m.set_field("d1", "k", "v")
        assert m.remove_field("d1", "other") is False

    def test_remove_no_doc(self):
        m = DocMetadataV2()
        assert m.remove_field("nope", "k") is False

    def test_remove_keeps_other_fields(self):
        m = DocMetadataV2()
        m.set_field("d1", "a", 1)
        m.set_field("d1", "b", 2)
        m.remove_field("d1", "a")
        assert m.get_value("d1", "b") == 2


# ---------------------------------------------------------------------------
# record_for
# ---------------------------------------------------------------------------


class TestRecordFor:
    def test_existing(self):
        m = DocMetadataV2()
        m.set_field("d1", "k", "v")
        r = m.record_for("d1")
        assert r is not None
        assert r.doc_id == "d1"

    def test_missing(self):
        m = DocMetadataV2()
        assert m.record_for("nope") is None


# ---------------------------------------------------------------------------
# all_records
# ---------------------------------------------------------------------------


class TestAllRecords:
    def test_empty(self):
        m = DocMetadataV2()
        assert m.all_records() == []

    def test_multiple(self):
        m = DocMetadataV2()
        m.set_field("a", "x", 1)
        m.set_field("b", "x", 2)
        recs = m.all_records()
        ids = {r.doc_id for r in recs}
        assert ids == {"a", "b"}


# ---------------------------------------------------------------------------
# register_extractor
# ---------------------------------------------------------------------------


class TestRegisterExtractor:
    def test_register_basic(self):
        m = DocMetadataV2()
        ed = m.register_extractor("custom", lambda t: {"custom": 1})
        assert ed.name == "custom"
        assert ed.enabled is True

    def test_register_replaces(self):
        m = DocMetadataV2()
        m.register_extractor("c", lambda t: {"a": 1})
        m.register_extractor("c", lambda t: {"b": 2})
        r = m.extract("d1", "x")
        assert r.fields.get("b") is not None
        assert r.fields.get("a") is None

    def test_register_runs_in_extract(self):
        m = DocMetadataV2()
        m.register_extractor("c", lambda t: {"size": len(t)})
        r = m.extract("d1", "hello")
        assert r.fields["size"].value == 5
        assert r.fields["size"].source == "extractor:c"

    def test_register_priority(self):
        m = DocMetadataV2()
        m.register_extractor("low", lambda t: {"x": "L"}, priority=1)
        m.register_extractor("high", lambda t: {"x": "H"}, priority=100)
        r = m.extract("d1", "anything")
        assert r.fields["x"].value == "H"


# ---------------------------------------------------------------------------
# unregister_extractor
# ---------------------------------------------------------------------------


class TestUnregisterExtractor:
    def test_unregister_existing(self):
        m = DocMetadataV2()
        m.register_extractor("c", lambda t: {})
        assert m.unregister_extractor("c") is True

    def test_unregister_missing(self):
        m = DocMetadataV2()
        assert m.unregister_extractor("nope") is False

    def test_unregister_builtin(self):
        m = DocMetadataV2()
        assert m.unregister_extractor("frontmatter") is True
        r = m.extract("d1", "---\ntitle: x\n---\n")
        assert "title" not in r.fields


# ---------------------------------------------------------------------------
# enable / disable
# ---------------------------------------------------------------------------


class TestEnableDisableExtractor:
    def test_disable(self):
        m = DocMetadataV2()
        assert m.disable_extractor("frontmatter") is True
        r = m.extract("d1", "---\ntitle: A\n---\n")
        assert "title" not in r.fields

    def test_enable_back(self):
        m = DocMetadataV2()
        m.disable_extractor("frontmatter")
        m.enable_extractor("frontmatter")
        r = m.extract("d1", "---\ntitle: A\n---\n")
        assert "title" in r.fields

    def test_enable_missing(self):
        m = DocMetadataV2()
        assert m.enable_extractor("nope") is False

    def test_disable_missing(self):
        m = DocMetadataV2()
        assert m.disable_extractor("nope") is False


# ---------------------------------------------------------------------------
# list_extractors
# ---------------------------------------------------------------------------


class TestListExtractors:
    def test_default_includes_builtins(self):
        m = DocMetadataV2()
        names = [e.name for e in m.list_extractors()]
        assert "frontmatter" in names
        assert "inline_tags" in names

    def test_sorted_by_priority_desc(self):
        m = DocMetadataV2()
        m.register_extractor("zzz", lambda t: {}, priority=200)
        first = m.list_extractors()[0]
        assert first.name == "zzz"

    def test_includes_disabled(self):
        m = DocMetadataV2()
        m.disable_extractor("frontmatter")
        names = [e.name for e in m.list_extractors()]
        assert "frontmatter" in names


# ---------------------------------------------------------------------------
# extract_frontmatter
# ---------------------------------------------------------------------------


class TestExtractFrontmatter:
    def test_simple(self):
        m = DocMetadataV2()
        result = m.extract_frontmatter("---\ntitle: A\nauthor: B\n---\nbody")
        assert result == {"title": "A", "author": "B"}

    def test_no_frontmatter(self):
        m = DocMetadataV2()
        assert m.extract_frontmatter("plain content") == {}

    def test_empty_string(self):
        m = DocMetadataV2()
        assert m.extract_frontmatter("") == {}

    def test_numeric_values(self):
        m = DocMetadataV2()
        r = m.extract_frontmatter("---\nyear: 2026\nrating: 4.5\n---\n")
        assert r["year"] == 2026
        assert r["rating"] == 4.5

    def test_boolean_values(self):
        m = DocMetadataV2()
        r = m.extract_frontmatter("---\npublished: true\ndraft: false\n---\n")
        assert r["published"] is True
        assert r["draft"] is False

    def test_list_value(self):
        m = DocMetadataV2()
        r = m.extract_frontmatter("---\ntags: [a, b, c]\n---\n")
        assert r["tags"] == ["a", "b", "c"]

    def test_quoted_string(self):
        m = DocMetadataV2()
        r = m.extract_frontmatter('---\ntitle: "hello world"\n---\n')
        assert r["title"] == "hello world"

    def test_no_closing(self):
        m = DocMetadataV2()
        # No closing fence — should not parse
        assert m.extract_frontmatter("---\ntitle: A\nbody...") == {}


# ---------------------------------------------------------------------------
# extract_inline_tags
# ---------------------------------------------------------------------------


class TestExtractInlineTags:
    def test_simple(self):
        m = DocMetadataV2()
        r = m.extract_inline_tags("hello #foo bye")
        assert r == {"tags": ["foo"]}

    def test_multiple(self):
        m = DocMetadataV2()
        r = m.extract_inline_tags("tags #a #b #c here")
        assert r["tags"] == ["a", "b", "c"]

    def test_dedup(self):
        m = DocMetadataV2()
        r = m.extract_inline_tags("#a and #a again")
        assert r["tags"] == ["a"]

    def test_none(self):
        m = DocMetadataV2()
        assert m.extract_inline_tags("plain") == {}

    def test_empty(self):
        m = DocMetadataV2()
        assert m.extract_inline_tags("") == {}

    def test_hyphenated(self):
        m = DocMetadataV2()
        r = m.extract_inline_tags("#machine-learning rocks")
        assert "machine-learning" in r["tags"]


# ---------------------------------------------------------------------------
# delete_doc
# ---------------------------------------------------------------------------


class TestDeleteDoc:
    def test_existing(self):
        m = DocMetadataV2()
        m.set_field("d1", "k", "v")
        assert m.delete_doc("d1") is True
        assert m.record_for("d1") is None

    def test_missing(self):
        m = DocMetadataV2()
        assert m.delete_doc("nope") is False


# ---------------------------------------------------------------------------
# docs_with_field
# ---------------------------------------------------------------------------


class TestDocsWithField:
    def test_any_value(self):
        m = DocMetadataV2()
        m.set_field("a", "k", 1)
        m.set_field("b", "k", 2)
        m.set_field("c", "other", "x")
        ids = m.docs_with_field("k")
        assert set(ids) == {"a", "b"}

    def test_specific_value(self):
        m = DocMetadataV2()
        m.set_field("a", "status", "draft")
        m.set_field("b", "status", "published")
        m.set_field("c", "status", "draft")
        ids = m.docs_with_field("status", "draft")
        assert set(ids) == {"a", "c"}

    def test_no_match(self):
        m = DocMetadataV2()
        m.set_field("a", "k", 1)
        assert m.docs_with_field("k", 999) == []

    def test_empty_store(self):
        m = DocMetadataV2()
        assert m.docs_with_field("k") == []


# ---------------------------------------------------------------------------
# total_docs
# ---------------------------------------------------------------------------


class TestTotalDocs:
    def test_empty(self):
        assert DocMetadataV2().total_docs == 0

    def test_after_inserts(self):
        m = DocMetadataV2()
        m.set_field("a", "x", 1)
        m.set_field("b", "x", 2)
        assert m.total_docs == 2

    def test_after_delete(self):
        m = DocMetadataV2()
        m.set_field("a", "x", 1)
        m.delete_doc("a")
        assert m.total_docs == 0


# ---------------------------------------------------------------------------
# total_fields
# ---------------------------------------------------------------------------


class TestTotalFields:
    def test_empty(self):
        assert DocMetadataV2().total_fields() == 0

    def test_count(self):
        m = DocMetadataV2()
        m.set_field("a", "x", 1)
        m.set_field("a", "y", 2)
        m.set_field("b", "x", 3)
        assert m.total_fields() == 3

    def test_after_remove(self):
        m = DocMetadataV2()
        m.set_field("a", "x", 1)
        m.set_field("a", "y", 2)
        m.remove_field("a", "x")
        assert m.total_fields() == 1


# ---------------------------------------------------------------------------
# unique_field_names
# ---------------------------------------------------------------------------


class TestUniqueFieldNames:
    def test_empty(self):
        assert DocMetadataV2().unique_field_names() == set()

    def test_basic(self):
        m = DocMetadataV2()
        m.set_field("a", "title", "x")
        m.set_field("b", "title", "y")
        m.set_field("b", "author", "z")
        assert m.unique_field_names() == {"title", "author"}


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clears_records(self):
        m = DocMetadataV2()
        m.set_field("a", "x", 1)
        m.clear()
        assert m.total_docs == 0

    def test_keeps_extractors(self):
        m = DocMetadataV2()
        m.set_field("a", "x", 1)
        m.clear()
        # built-ins still registered
        names = [e.name for e in m.list_extractors()]
        assert "frontmatter" in names


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_extractor_returning_non_dict(self):
        m = DocMetadataV2()
        m.register_extractor("bad", lambda t: "not a dict")
        # Should not crash
        r = m.extract("d1", "x")
        assert isinstance(r.fields, dict)

    def test_extractor_raising(self):
        m = DocMetadataV2()

        def bad(t):
            raise RuntimeError("boom")

        m.register_extractor("bad", bad)
        r = m.extract("d1", "---\ntitle: A\n---\n")
        # Frontmatter extractor still runs
        assert "title" in r.fields

    def test_extractor_non_string_key(self):
        m = DocMetadataV2()
        m.register_extractor("weird", lambda t: {123: "x", "ok": "y"})
        r = m.extract("d1", "x")
        assert "ok" in r.fields
        assert 123 not in r.fields

    def test_set_field_then_extract_preserves_manual(self):
        m = DocMetadataV2()
        m.set_field("d1", "title", "MANUAL", source="manual")
        m.extract("d1", "---\ntitle: FROM_FM\n---\n")
        # Manual was set first; first-wins keeps it
        mf = m.get_field("d1", "title")
        assert mf.value == "MANUAL"
        assert mf.source == "manual"

    def test_inline_tags_via_extract(self):
        m = DocMetadataV2()
        r = m.extract("d1", "see #ai and #ml")
        assert r.fields["tags"].source == "extractor:inline_tags"

    def test_frontmatter_overrides_inline(self):
        # Both extractors might produce "tags" — frontmatter has higher priority
        m = DocMetadataV2()
        content = "---\ntags: [fm-tag]\n---\nbody with #inline-tag"
        r = m.extract("d1", content)
        assert r.fields["tags"].value == ["fm-tag"]
        assert r.fields["tags"].source == "extractor:frontmatter"

    def test_clear_then_use(self):
        m = DocMetadataV2()
        m.set_field("a", "x", 1)
        m.clear()
        m.set_field("b", "y", 2)
        assert m.total_docs == 1
        assert m.get_value("b", "y") == 2
