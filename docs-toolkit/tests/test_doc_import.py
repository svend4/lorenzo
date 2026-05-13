"""Tests for E196 — docstoolkit.doc_import."""
from __future__ import annotations

import json

import pytest

from docstoolkit.doc_import import (
    DocImporter,
    ImportConfig,
    ImportError,
    ImportFormat,
    ImportResult,
    ImportStats,
)


# --------------------------------------------------------------------------- #
# ImportFormat
# --------------------------------------------------------------------------- #
class TestImportFormat:
    def test_has_json(self):
        assert ImportFormat.JSON.value == "json"

    def test_has_jsonl(self):
        assert ImportFormat.JSONL.value == "jsonl"

    def test_has_csv(self):
        assert ImportFormat.CSV.value == "csv"

    def test_has_tsv(self):
        assert ImportFormat.TSV.value == "tsv"

    def test_has_xml(self):
        assert ImportFormat.XML.value == "xml"

    def test_has_plain_text(self):
        assert ImportFormat.PLAIN_TEXT.value == "plain_text"

    def test_has_markdown(self):
        assert ImportFormat.MARKDOWN.value == "markdown"

    def test_has_auto(self):
        assert ImportFormat.AUTO.value == "auto"


# --------------------------------------------------------------------------- #
# ImportConfig
# --------------------------------------------------------------------------- #
class TestImportConfig:
    def test_defaults(self):
        cfg = ImportConfig()
        assert cfg.format == ImportFormat.AUTO
        assert cfg.delimiter == ","
        assert cfg.has_header is True
        assert cfg.encoding == "utf-8"
        assert cfg.strict is False

    def test_override(self):
        cfg = ImportConfig(
            format=ImportFormat.CSV,
            delimiter=";",
            has_header=False,
            encoding="latin-1",
            strict=True,
        )
        assert cfg.format == ImportFormat.CSV
        assert cfg.delimiter == ";"
        assert cfg.has_header is False
        assert cfg.encoding == "latin-1"
        assert cfg.strict is True


# --------------------------------------------------------------------------- #
# ImportStats
# --------------------------------------------------------------------------- #
class TestImportStats:
    def test_empty_success_rate(self):
        stats = ImportStats()
        assert stats.success_rate == 0.0
        assert stats.docs_imported == 0
        assert stats.docs_skipped == 0
        assert stats.errors == []

    def test_full_success(self):
        stats = ImportStats(docs_imported=10, docs_skipped=0)
        assert stats.success_rate == 1.0

    def test_partial_success(self):
        stats = ImportStats(docs_imported=8, docs_skipped=2)
        assert stats.success_rate == 0.8

    def test_all_skipped(self):
        stats = ImportStats(docs_imported=0, docs_skipped=5)
        assert stats.success_rate == 0.0

    def test_errors_list(self):
        stats = ImportStats(errors=["bad row", "parse error"])
        assert len(stats.errors) == 2


# --------------------------------------------------------------------------- #
# ImportResult
# --------------------------------------------------------------------------- #
class TestImportResult:
    def test_construction(self):
        stats = ImportStats(docs_imported=2)
        res = ImportResult(
            docs=[{"a": 1}, {"b": 2}],
            stats=stats,
            format=ImportFormat.JSON,
        )
        assert len(res.docs) == 2
        assert res.stats.docs_imported == 2
        assert res.format == ImportFormat.JSON


# --------------------------------------------------------------------------- #
# from_json
# --------------------------------------------------------------------------- #
class TestFromJson:
    def test_array(self):
        imp = DocImporter()
        docs = imp.from_json('[{"a": 1}, {"b": 2}]')
        assert docs == [{"a": 1}, {"b": 2}]

    def test_single_object(self):
        imp = DocImporter()
        docs = imp.from_json('{"a": 1, "b": 2}')
        assert docs == [{"a": 1, "b": 2}]

    def test_empty_array(self):
        imp = DocImporter()
        assert imp.from_json("[]") == []

    def test_empty_object(self):
        imp = DocImporter()
        assert imp.from_json("{}") == [{}]

    def test_filters_non_dicts_in_array(self):
        imp = DocImporter()
        docs = imp.from_json('[{"a": 1}, 42, "x", null]')
        assert docs == [{"a": 1}]

    def test_invalid_json_non_strict(self):
        imp = DocImporter()
        assert imp.from_json("not json") == []

    def test_invalid_json_strict(self):
        imp = DocImporter(ImportConfig(strict=True))
        with pytest.raises(ImportError):
            imp.from_json("not json")

    def test_unicode(self):
        imp = DocImporter()
        docs = imp.from_json('[{"title": "Привет"}]')
        assert docs[0]["title"] == "Привет"


# --------------------------------------------------------------------------- #
# from_jsonl
# --------------------------------------------------------------------------- #
class TestFromJsonl:
    def test_basic(self):
        imp = DocImporter()
        text = '{"a": 1}\n{"b": 2}\n{"c": 3}'
        docs = imp.from_jsonl(text)
        assert docs == [{"a": 1}, {"b": 2}, {"c": 3}]

    def test_empty_lines_skipped(self):
        imp = DocImporter()
        text = '{"a": 1}\n\n\n{"b": 2}\n'
        docs = imp.from_jsonl(text)
        assert docs == [{"a": 1}, {"b": 2}]

    def test_bad_line_skipped_non_strict(self):
        imp = DocImporter()
        text = '{"a": 1}\nnot json\n{"b": 2}'
        docs = imp.from_jsonl(text)
        assert docs == [{"a": 1}, {"b": 2}]

    def test_bad_line_strict(self):
        imp = DocImporter(ImportConfig(strict=True))
        with pytest.raises(ImportError):
            imp.from_jsonl('{"a": 1}\nbroken\n')

    def test_non_object_skipped(self):
        imp = DocImporter()
        docs = imp.from_jsonl('{"a": 1}\n[1,2,3]\n42')
        assert docs == [{"a": 1}]

    def test_empty(self):
        imp = DocImporter()
        assert imp.from_jsonl("") == []


# --------------------------------------------------------------------------- #
# from_csv
# --------------------------------------------------------------------------- #
class TestFromCsv:
    def test_with_header(self):
        imp = DocImporter()
        text = "name,age\nAlice,30\nBob,25"
        docs = imp.from_csv(text)
        assert docs == [
            {"name": "Alice", "age": "30"},
            {"name": "Bob", "age": "25"},
        ]

    def test_without_header(self):
        imp = DocImporter()
        text = "Alice,30\nBob,25"
        docs = imp.from_csv(text, has_header=False)
        assert docs == [
            {"col_0": "Alice", "col_1": "30"},
            {"col_0": "Bob", "col_1": "25"},
        ]

    def test_custom_delimiter(self):
        imp = DocImporter()
        text = "name;age\nAlice;30"
        docs = imp.from_csv(text, delimiter=";")
        assert docs == [{"name": "Alice", "age": "30"}]

    def test_empty(self):
        imp = DocImporter()
        assert imp.from_csv("") == []
        assert imp.from_csv("   ") == []

    def test_only_header(self):
        imp = DocImporter()
        docs = imp.from_csv("name,age\n")
        assert docs == []

    def test_quoted_fields(self):
        imp = DocImporter()
        text = 'title,content\n"Hello","world, and more"'
        docs = imp.from_csv(text)
        assert docs == [{"title": "Hello", "content": "world, and more"}]


# --------------------------------------------------------------------------- #
# from_tsv
# --------------------------------------------------------------------------- #
class TestFromTsv:
    def test_basic(self):
        imp = DocImporter()
        text = "name\tage\nAlice\t30\nBob\t25"
        docs = imp.from_tsv(text)
        assert docs == [
            {"name": "Alice", "age": "30"},
            {"name": "Bob", "age": "25"},
        ]

    def test_no_header(self):
        imp = DocImporter()
        text = "Alice\t30"
        docs = imp.from_tsv(text, has_header=False)
        assert docs == [{"col_0": "Alice", "col_1": "30"}]


# --------------------------------------------------------------------------- #
# from_xml
# --------------------------------------------------------------------------- #
class TestFromXml:
    def test_basic(self):
        imp = DocImporter()
        text = (
            "<?xml version='1.0'?>"
            "<documents>"
            "<document><title>A</title><body>aa</body></document>"
            "<document><title>B</title><body>bb</body></document>"
            "</documents>"
        )
        docs = imp.from_xml(text)
        assert docs == [
            {"title": "A", "body": "aa"},
            {"title": "B", "body": "bb"},
        ]

    def test_single_document_root(self):
        imp = DocImporter()
        text = "<document><title>X</title></document>"
        docs = imp.from_xml(text)
        assert docs == [{"title": "X"}]

    def test_other_root_children_fallback(self):
        imp = DocImporter()
        text = "<root><item><x>1</x></item><item><x>2</x></item></root>"
        docs = imp.from_xml(text)
        # 'item' children are not 'document' — fall back to all root children
        assert docs == [{"x": "1"}, {"x": "2"}]

    def test_bad_xml_non_strict(self):
        imp = DocImporter()
        assert imp.from_xml("<unclosed>") == []

    def test_bad_xml_strict(self):
        imp = DocImporter(ImportConfig(strict=True))
        with pytest.raises(ImportError):
            imp.from_xml("<unclosed>")

    def test_empty_element_value(self):
        imp = DocImporter()
        text = "<documents><document><empty/></document></documents>"
        docs = imp.from_xml(text)
        assert docs == [{"empty": ""}]


# --------------------------------------------------------------------------- #
# from_plain_text
# --------------------------------------------------------------------------- #
class TestFromPlainText:
    def test_paragraphs(self):
        imp = DocImporter()
        text = "First paragraph.\n\nSecond paragraph.\n\nThird."
        docs = imp.from_plain_text(text)
        assert docs == [
            {"content": "First paragraph."},
            {"content": "Second paragraph."},
            {"content": "Third."},
        ]

    def test_lines_when_no_blank_separator(self):
        imp = DocImporter()
        text = "line1\nline2\nline3"
        docs = imp.from_plain_text(text)
        assert docs == [
            {"content": "line1"},
            {"content": "line2"},
            {"content": "line3"},
        ]

    def test_empty(self):
        imp = DocImporter()
        assert imp.from_plain_text("") == []
        assert imp.from_plain_text("   \n\n  ") == []

    def test_single_line(self):
        imp = DocImporter()
        docs = imp.from_plain_text("hello")
        assert docs == [{"content": "hello"}]


# --------------------------------------------------------------------------- #
# from_markdown
# --------------------------------------------------------------------------- #
class TestFromMarkdown:
    def test_horizontal_rule_split(self):
        imp = DocImporter()
        text = "# Title A\n\nBody A.\n\n---\n\n# Title B\n\nBody B.\n"
        docs = imp.from_markdown(text)
        assert len(docs) == 2
        assert docs[0]["title"] == "Title A"
        assert docs[0]["content"] == "Body A."
        assert docs[1]["title"] == "Title B"
        assert docs[1]["content"] == "Body B."

    def test_heading_split(self):
        imp = DocImporter()
        text = "# One\n\ncontent one\n\n# Two\n\ncontent two"
        docs = imp.from_markdown(text)
        assert len(docs) == 2
        assert docs[0]["title"] == "One"
        assert docs[0]["content"] == "content one"
        assert docs[1]["title"] == "Two"

    def test_no_heading(self):
        imp = DocImporter()
        text = "just some text without heading"
        docs = imp.from_markdown(text)
        assert len(docs) == 1
        assert docs[0]["title"] == ""
        assert "just some text" in docs[0]["content"]

    def test_empty(self):
        imp = DocImporter()
        assert imp.from_markdown("") == []

    def test_multiple_headings_first_used_as_title(self):
        imp = DocImporter()
        text = "# A\n\n## sub\n\ncontent"
        docs = imp.from_markdown(text)
        assert docs[0]["title"] == "A"
        assert "## sub" in docs[0]["content"]


# --------------------------------------------------------------------------- #
# detect_format
# --------------------------------------------------------------------------- #
class TestDetectFormat:
    def test_json_array(self):
        imp = DocImporter()
        assert imp.detect_format("[{}]") == ImportFormat.JSON

    def test_json_object(self):
        imp = DocImporter()
        assert imp.detect_format('{"a": 1}') == ImportFormat.JSON

    def test_jsonl(self):
        imp = DocImporter()
        text = '{"a": 1}\n{"b": 2}\n{"c": 3}'
        assert imp.detect_format(text) == ImportFormat.JSONL

    def test_xml_with_prolog(self):
        imp = DocImporter()
        assert imp.detect_format("<?xml version='1.0'?><x/>") == ImportFormat.XML

    def test_xml_without_prolog(self):
        imp = DocImporter()
        assert imp.detect_format("<documents><doc/></documents>") == ImportFormat.XML

    def test_csv(self):
        imp = DocImporter()
        text = "a,b\n1,2\n3,4"
        assert imp.detect_format(text) == ImportFormat.CSV

    def test_markdown(self):
        imp = DocImporter()
        text = "# Heading\n\nsome body"
        assert imp.detect_format(text) == ImportFormat.MARKDOWN

    def test_plain_text(self):
        imp = DocImporter()
        assert imp.detect_format("just text without commas") == ImportFormat.PLAIN_TEXT

    def test_empty(self):
        imp = DocImporter()
        assert imp.detect_format("") == ImportFormat.PLAIN_TEXT
        assert imp.detect_format("   ") == ImportFormat.PLAIN_TEXT


# --------------------------------------------------------------------------- #
# import_string
# --------------------------------------------------------------------------- #
class TestImportString:
    def test_explicit_json(self):
        imp = DocImporter()
        res = imp.import_string('[{"a": 1}]', format=ImportFormat.JSON)
        assert res.format == ImportFormat.JSON
        assert res.docs == [{"a": 1}]
        assert res.stats.docs_imported == 1

    def test_auto_detect_json(self):
        imp = DocImporter()
        res = imp.import_string('[{"a": 1}]')
        assert res.format == ImportFormat.JSON
        assert res.docs == [{"a": 1}]

    def test_auto_detect_jsonl(self):
        imp = DocImporter()
        res = imp.import_string('{"a": 1}\n{"b": 2}')
        assert res.format == ImportFormat.JSONL
        assert len(res.docs) == 2

    def test_auto_detect_csv(self):
        imp = DocImporter()
        res = imp.import_string("a,b\n1,2")
        assert res.format == ImportFormat.CSV
        assert res.docs == [{"a": "1", "b": "2"}]

    def test_auto_detect_xml(self):
        imp = DocImporter()
        res = imp.import_string(
            "<documents><document><a>1</a></document></documents>"
        )
        assert res.format == ImportFormat.XML
        assert res.docs == [{"a": "1"}]

    def test_auto_detect_markdown(self):
        imp = DocImporter()
        res = imp.import_string("# Hello\n\nworld")
        assert res.format == ImportFormat.MARKDOWN
        assert res.docs[0]["title"] == "Hello"

    def test_auto_detect_plain(self):
        imp = DocImporter()
        res = imp.import_string("just text")
        assert res.format == ImportFormat.PLAIN_TEXT
        assert res.docs == [{"content": "just text"}]

    def test_none_text_non_strict(self):
        imp = DocImporter()
        res = imp.import_string(None)
        assert res.docs == []
        assert res.stats.errors

    def test_none_text_strict(self):
        imp = DocImporter(ImportConfig(strict=True))
        with pytest.raises(ImportError):
            imp.import_string(None)

    def test_stats_imported_count(self):
        imp = DocImporter()
        res = imp.import_string('[{"a":1},{"b":2},{"c":3}]')
        assert res.stats.docs_imported == 3

    def test_jsonl_with_bad_line_counted_in_stats(self):
        imp = DocImporter()
        res = imp.import_string(
            '{"a": 1}\nbroken\n{"b": 2}', format=ImportFormat.JSONL
        )
        assert res.stats.docs_imported == 2
        assert res.stats.docs_skipped == 1


# --------------------------------------------------------------------------- #
# validate
# --------------------------------------------------------------------------- #
class TestValidate:
    def test_no_required(self):
        imp = DocImporter()
        ok, errors = imp.validate({"a": 1})
        assert ok is True
        assert errors == []

    def test_all_present(self):
        imp = DocImporter()
        ok, errors = imp.validate(
            {"title": "x", "content": "y"},
            required_fields=["title", "content"],
        )
        assert ok is True
        assert errors == []

    def test_missing_field(self):
        imp = DocImporter()
        ok, errors = imp.validate(
            {"title": "x"}, required_fields=["title", "content"]
        )
        assert ok is False
        assert any("content" in e for e in errors)

    def test_empty_field(self):
        imp = DocImporter()
        ok, errors = imp.validate(
            {"title": ""}, required_fields=["title"]
        )
        assert ok is False
        assert any("empty" in e for e in errors)

    def test_non_dict(self):
        imp = DocImporter()
        ok, errors = imp.validate("not a dict")  # type: ignore[arg-type]
        assert ok is False
        assert errors


# --------------------------------------------------------------------------- #
# import_batch
# --------------------------------------------------------------------------- #
class TestImportBatch:
    def test_basic(self):
        imp = DocImporter()
        results = imp.import_batch(
            ['[{"a": 1}]', '[{"b": 2}, {"c": 3}]'],
            format=ImportFormat.JSON,
        )
        assert len(results) == 2
        assert results[0].docs == [{"a": 1}]
        assert results[1].docs == [{"b": 2}, {"c": 3}]

    def test_mixed_auto(self):
        imp = DocImporter()
        results = imp.import_batch(['{"a": 1}', "name,age\nAlice,30"])
        assert results[0].format == ImportFormat.JSON
        assert results[1].format == ImportFormat.CSV

    def test_empty_list(self):
        imp = DocImporter()
        assert imp.import_batch([]) == []

    def test_invalid_arg(self):
        imp = DocImporter()
        with pytest.raises(ImportError):
            imp.import_batch("not a list")  # type: ignore[arg-type]


# --------------------------------------------------------------------------- #
# Round trip with DocExporter
# --------------------------------------------------------------------------- #
class TestRoundTrip:
    def test_json_roundtrip(self):
        from docstoolkit.doc_export import DocExporter, ExportFormat

        docs = [{"title": "A", "content": "x"}, {"title": "B", "content": "y"}]
        exp = DocExporter()
        text = exp.export_to_string(docs, format=ExportFormat.JSON)
        imp = DocImporter()
        res = imp.import_string(text, format=ImportFormat.JSON)
        assert res.docs == docs

    def test_jsonl_roundtrip(self):
        from docstoolkit.doc_export import DocExporter, ExportFormat

        docs = [{"a": 1}, {"b": 2}, {"c": 3}]
        exp = DocExporter()
        text = exp.export_to_string(docs, format=ExportFormat.JSONL)
        imp = DocImporter()
        res = imp.import_string(text, format=ImportFormat.JSONL)
        assert res.docs == docs

    def test_csv_roundtrip(self):
        from docstoolkit.doc_export import DocExporter, ExportFormat

        docs = [
            {"name": "Alice", "age": "30"},
            {"name": "Bob", "age": "25"},
        ]
        exp = DocExporter()
        text = exp.export_to_string(docs, format=ExportFormat.CSV)
        imp = DocImporter()
        res = imp.import_string(text, format=ImportFormat.CSV)
        assert res.docs == docs

    def test_xml_roundtrip_simple(self):
        from docstoolkit.doc_export import DocExporter, ExportFormat

        docs = [{"title": "A", "body": "aa"}, {"title": "B", "body": "bb"}]
        exp = DocExporter()
        text = exp.export_to_string(docs, format=ExportFormat.XML)
        imp = DocImporter()
        res = imp.import_string(text, format=ImportFormat.XML)
        assert res.docs == docs


# --------------------------------------------------------------------------- #
# Strict mode
# --------------------------------------------------------------------------- #
class TestStrictMode:
    def test_strict_bad_json(self):
        imp = DocImporter(ImportConfig(strict=True, format=ImportFormat.JSON))
        with pytest.raises(ImportError):
            imp.import_string("not json")

    def test_strict_bad_jsonl(self):
        imp = DocImporter(ImportConfig(strict=True))
        with pytest.raises(ImportError):
            imp.import_string("broken\nalso broken", format=ImportFormat.JSONL)

    def test_strict_bad_xml(self):
        imp = DocImporter(ImportConfig(strict=True, format=ImportFormat.XML))
        with pytest.raises(ImportError):
            imp.import_string("<unclosed>")


# --------------------------------------------------------------------------- #
# Non-strict mode
# --------------------------------------------------------------------------- #
class TestNonStrict:
    def test_non_strict_bad_json(self):
        imp = DocImporter()
        res = imp.import_string("not json", format=ImportFormat.JSON)
        assert res.docs == []

    def test_non_strict_skips_bad_jsonl(self):
        imp = DocImporter()
        res = imp.import_string(
            '{"a": 1}\nbad\n{"b": 2}', format=ImportFormat.JSONL
        )
        assert len(res.docs) == 2
        assert res.stats.docs_skipped == 1

    def test_non_strict_bad_xml(self):
        imp = DocImporter()
        res = imp.import_string("<oops>", format=ImportFormat.XML)
        assert res.docs == []


# --------------------------------------------------------------------------- #
# Edge cases
# --------------------------------------------------------------------------- #
class TestEdgeCases:
    def test_empty_string_auto(self):
        imp = DocImporter()
        res = imp.import_string("")
        assert res.docs == []

    def test_whitespace_only(self):
        imp = DocImporter()
        res = imp.import_string("   \n  ")
        assert res.docs == []

    def test_json_with_unicode(self):
        imp = DocImporter()
        res = imp.import_string('[{"t": "ü"}]', format=ImportFormat.JSON)
        assert res.docs == [{"t": "ü"}]

    def test_csv_one_row(self):
        imp = DocImporter()
        res = imp.import_string("a,b\n1,2", format=ImportFormat.CSV)
        assert res.docs == [{"a": "1", "b": "2"}]

    def test_markdown_just_separator(self):
        imp = DocImporter()
        res = imp.import_string("---", format=ImportFormat.MARKDOWN)
        assert res.docs == []

    def test_unsupported_format_dispatch(self):
        # Should never happen via enum, but covers dispatch fallback.
        imp = DocImporter(ImportConfig(strict=True))
        with pytest.raises(ImportError):
            imp.import_string("x", format="not-a-format")  # type: ignore[arg-type]

    def test_jsonl_only_blank(self):
        imp = DocImporter()
        res = imp.import_string("\n\n\n", format=ImportFormat.JSONL)
        assert res.docs == []
