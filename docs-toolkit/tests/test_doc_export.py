"""Tests for the E195 doc_export module."""
from __future__ import annotations

import csv
import io
import json

import pytest

from docstoolkit.doc_export import (
    DocExporter,
    ExportConfig,
    ExportError,
    ExportFormat,
    ExportResult,
)


# --------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------- #
@pytest.fixture
def sample_docs():
    return [
        {"id": 1, "title": "First", "content": "Hello world"},
        {"id": 2, "title": "Second", "content": "Another doc"},
    ]


@pytest.fixture
def exporter():
    return DocExporter()


# --------------------------------------------------------------------- #
class TestExportFormat:
    def test_has_json(self):
        assert ExportFormat.JSON.value == "json"

    def test_has_jsonl(self):
        assert ExportFormat.JSONL.value == "jsonl"

    def test_has_csv(self):
        assert ExportFormat.CSV.value == "csv"

    def test_has_tsv(self):
        assert ExportFormat.TSV.value == "tsv"

    def test_has_xml(self):
        assert ExportFormat.XML.value == "xml"

    def test_has_plain_text(self):
        assert ExportFormat.PLAIN_TEXT.value == "plain_text"

    def test_has_markdown(self):
        assert ExportFormat.MARKDOWN.value == "markdown"

    def test_member_count(self):
        assert len(list(ExportFormat)) == 7


class TestExportConfig:
    def test_default_format_is_json(self):
        cfg = ExportConfig()
        assert cfg.format == ExportFormat.JSON

    def test_default_include_metadata(self):
        assert ExportConfig().include_metadata is True

    def test_default_pretty_false(self):
        assert ExportConfig().pretty is False

    def test_default_delimiter_comma(self):
        assert ExportConfig().delimiter == ","

    def test_default_encoding_utf8(self):
        assert ExportConfig().encoding == "utf-8"

    def test_override(self):
        cfg = ExportConfig(format=ExportFormat.CSV, pretty=True, delimiter=";")
        assert cfg.format == ExportFormat.CSV
        assert cfg.pretty is True
        assert cfg.delimiter == ";"


class TestExportResult:
    def test_fields(self):
        r = ExportResult(
            format=ExportFormat.JSON,
            content="[]",
            doc_count=0,
            byte_size=2,
        )
        assert r.format == ExportFormat.JSON
        assert r.content == "[]"
        assert r.doc_count == 0
        assert r.byte_size == 2

    def test_result_from_export(self, exporter, sample_docs):
        res = exporter.export(sample_docs, ExportConfig(format=ExportFormat.JSON))
        assert isinstance(res, ExportResult)
        assert res.doc_count == 2


# --------------------------------------------------------------------- #
class TestExportJson:
    def test_returns_string(self, exporter, sample_docs):
        out = exporter.export_to_json(sample_docs)
        assert isinstance(out, str)

    def test_roundtrip(self, exporter, sample_docs):
        out = exporter.export_to_json(sample_docs)
        assert json.loads(out) == sample_docs

    def test_empty(self, exporter):
        out = exporter.export_to_json([])
        assert json.loads(out) == []

    def test_unicode(self, exporter):
        out = exporter.export_to_json([{"text": "Привет"}])
        assert "Привет" in out

    def test_unserializable_raises(self, exporter):
        class X:
            pass

        with pytest.raises(ExportError):
            exporter.export_to_json([{"x": X()}])


class TestExportJsonPretty:
    def test_pretty_indented(self, exporter, sample_docs):
        out = exporter.export_to_json(sample_docs, pretty=True)
        assert "\n" in out
        assert "  " in out

    def test_pretty_via_config(self, sample_docs):
        cfg = ExportConfig(format=ExportFormat.JSON, pretty=True)
        res = DocExporter(cfg).export(sample_docs)
        assert "\n" in res.content

    def test_not_pretty_default(self, exporter, sample_docs):
        out = exporter.export_to_json(sample_docs, pretty=False)
        # compact JSON has no newlines
        assert "\n" not in out


class TestExportJsonl:
    def test_one_per_line(self, exporter, sample_docs):
        out = exporter.export_to_jsonl(sample_docs)
        lines = out.split("\n")
        assert len(lines) == 2

    def test_each_line_valid_json(self, exporter, sample_docs):
        out = exporter.export_to_jsonl(sample_docs)
        for line in out.split("\n"):
            assert isinstance(json.loads(line), dict)

    def test_empty(self, exporter):
        assert exporter.export_to_jsonl([]) == ""

    def test_unicode_jsonl(self, exporter):
        out = exporter.export_to_jsonl([{"t": "тест"}])
        assert "тест" in out


class TestExportCsv:
    def test_header_present(self, exporter, sample_docs):
        out = exporter.export_to_csv(sample_docs)
        first_line = out.splitlines()[0]
        assert "id" in first_line
        assert "title" in first_line

    def test_row_count(self, exporter, sample_docs):
        out = exporter.export_to_csv(sample_docs)
        assert len(out.splitlines()) == 3  # header + 2 rows

    def test_parseable(self, exporter, sample_docs):
        out = exporter.export_to_csv(sample_docs)
        reader = csv.DictReader(io.StringIO(out))
        rows = list(reader)
        assert len(rows) == 2
        assert rows[0]["title"] == "First"

    def test_empty(self, exporter):
        assert exporter.export_to_csv([]) == ""

    def test_union_of_keys(self, exporter):
        docs = [{"a": 1}, {"b": 2}]
        out = exporter.export_to_csv(docs)
        header = out.splitlines()[0]
        assert "a" in header and "b" in header

    def test_missing_key_blank(self, exporter):
        docs = [{"a": 1, "b": 2}, {"a": 3}]
        out = exporter.export_to_csv(docs)
        reader = csv.DictReader(io.StringIO(out))
        rows = list(reader)
        assert rows[1]["b"] == ""

    def test_custom_delimiter(self, exporter, sample_docs):
        out = exporter.export_to_csv(sample_docs, delimiter=";")
        assert ";" in out.splitlines()[0]

    def test_nested_value_serialized(self, exporter):
        out = exporter.export_to_csv([{"x": [1, 2, 3]}])
        assert "[1, 2, 3]" in out


class TestExportTsv:
    def test_tab_delimited(self, exporter, sample_docs):
        out = exporter.export_to_tsv(sample_docs)
        assert "\t" in out.splitlines()[0]

    def test_parseable(self, exporter, sample_docs):
        out = exporter.export_to_tsv(sample_docs)
        reader = csv.DictReader(io.StringIO(out), delimiter="\t")
        rows = list(reader)
        assert rows[0]["title"] == "First"

    def test_empty(self, exporter):
        assert exporter.export_to_tsv([]) == ""


class TestExportXml:
    def test_has_root(self, exporter, sample_docs):
        out = exporter.export_to_xml(sample_docs)
        assert "<documents>" in out
        assert "</documents>" in out

    def test_each_doc_wrapped(self, exporter, sample_docs):
        out = exporter.export_to_xml(sample_docs)
        assert out.count("<document>") == 2
        assert out.count("</document>") == 2

    def test_xml_declaration(self, exporter, sample_docs):
        out = exporter.export_to_xml(sample_docs)
        assert out.startswith("<?xml")

    def test_contains_values(self, exporter, sample_docs):
        out = exporter.export_to_xml(sample_docs)
        assert "Hello world" in out

    def test_empty(self, exporter):
        out = exporter.export_to_xml([])
        assert "<documents>" in out and "</documents>" in out

    def test_nested_dict(self, exporter):
        out = exporter.export_to_xml([{"meta": {"k": "v"}}])
        assert "<meta>" in out and "<k>v</k>" in out

    def test_nested_list(self, exporter):
        out = exporter.export_to_xml([{"tags": ["a", "b"]}])
        assert "<tags>" in out
        assert out.count("<item>") == 2


class TestExportXmlEscape:
    def test_amp_escaped(self, exporter):
        out = exporter.export_to_xml([{"t": "A & B"}])
        assert "&amp;" in out
        assert "A & B" not in out  # raw form must not appear

    def test_lt_escaped(self, exporter):
        out = exporter.export_to_xml([{"t": "1 < 2"}])
        assert "&lt;" in out

    def test_gt_escaped(self, exporter):
        out = exporter.export_to_xml([{"t": "2 > 1"}])
        assert "&gt;" in out

    def test_escape_in_nested(self, exporter):
        out = exporter.export_to_xml([{"meta": {"k": "a&b"}}])
        assert "&amp;" in out


class TestExportPlainText:
    def test_uses_content_field(self, exporter, sample_docs):
        out = exporter.export_to_plain_text(sample_docs)
        assert "Hello world" in out
        assert "Another doc" in out

    def test_blank_line_separator(self, exporter, sample_docs):
        out = exporter.export_to_plain_text(sample_docs)
        assert "\n\n" in out

    def test_empty(self, exporter):
        assert exporter.export_to_plain_text([]) == ""

    def test_no_content_falls_back_to_kv(self, exporter):
        out = exporter.export_to_plain_text([{"a": 1, "b": 2}])
        assert "a: 1" in out
        assert "b: 2" in out


class TestExportMarkdown:
    def test_h1_title(self, exporter, sample_docs):
        out = exporter.export_to_markdown(sample_docs)
        assert "# First" in out
        assert "# Second" in out

    def test_body_present(self, exporter, sample_docs):
        out = exporter.export_to_markdown(sample_docs)
        assert "Hello world" in out

    def test_separator(self, exporter, sample_docs):
        out = exporter.export_to_markdown(sample_docs)
        assert "---" in out

    def test_empty(self, exporter):
        assert exporter.export_to_markdown([]) == ""

    def test_missing_title_uses_default(self, exporter):
        out = exporter.export_to_markdown([{"content": "x"}])
        assert "# Untitled" in out


class TestExportToString:
    def test_default_uses_config_format(self, sample_docs):
        cfg = ExportConfig(format=ExportFormat.JSONL)
        exp = DocExporter(cfg)
        out = exp.export_to_string(sample_docs)
        # jsonl => 2 lines
        assert len(out.split("\n")) == 2

    def test_format_override(self, exporter, sample_docs):
        out = exporter.export_to_string(sample_docs, format=ExportFormat.MARKDOWN)
        assert "# First" in out

    def test_unsupported_dispatch(self, exporter, sample_docs):
        # Build a fake-looking format value via direct dispatch
        cfg = ExportConfig(format=ExportFormat.JSON)
        # Manipulating .format to a bogus value
        cfg.format = "not-an-enum"  # type: ignore[assignment]
        with pytest.raises(ExportError):
            exporter.export(sample_docs, cfg)


class TestExportBatch:
    def test_returns_one_per_batch(self, exporter):
        batches = [
            [{"a": 1}],
            [{"a": 2}, {"a": 3}],
            [],
        ]
        results = exporter.export_batch(batches, ExportFormat.JSON)
        assert len(results) == 3
        assert results[0].doc_count == 1
        assert results[1].doc_count == 2
        assert results[2].doc_count == 0

    def test_all_results_use_format(self, exporter):
        batches = [[{"a": 1}], [{"b": 2}]]
        results = exporter.export_batch(batches, ExportFormat.CSV)
        for r in results:
            assert r.format == ExportFormat.CSV

    def test_bad_input_raises(self, exporter):
        with pytest.raises(ExportError):
            exporter.export_batch("not a list", ExportFormat.JSON)  # type: ignore[arg-type]

    def test_bad_batch_member_raises(self, exporter):
        with pytest.raises(ExportError):
            exporter.export_batch([{"not": "a list"}], ExportFormat.JSON)  # type: ignore[list-item]


class TestAvailableFormats:
    def test_returns_list(self, exporter):
        fmts = exporter.available_formats()
        assert isinstance(fmts, list)

    def test_includes_all(self, exporter):
        fmts = exporter.available_formats()
        assert set(fmts) == set(ExportFormat)


class TestExportConfigOverride:
    def test_per_call_overrides_default(self, sample_docs):
        default_cfg = ExportConfig(format=ExportFormat.JSON)
        exp = DocExporter(default_cfg)
        res = exp.export(sample_docs, ExportConfig(format=ExportFormat.CSV))
        assert res.format == ExportFormat.CSV
        assert "id" in res.content.splitlines()[0]

    def test_default_used_when_no_override(self, sample_docs):
        exp = DocExporter(ExportConfig(format=ExportFormat.MARKDOWN))
        res = exp.export(sample_docs)
        assert res.format == ExportFormat.MARKDOWN

    def test_delimiter_override(self, sample_docs):
        exp = DocExporter(ExportConfig(format=ExportFormat.CSV, delimiter="|"))
        res = exp.export(sample_docs)
        assert "|" in res.content.splitlines()[0]


class TestDocCount:
    def test_doc_count_matches(self, exporter, sample_docs):
        res = exporter.export(sample_docs, ExportConfig(format=ExportFormat.JSON))
        assert res.doc_count == 2

    def test_doc_count_zero(self, exporter):
        res = exporter.export([], ExportConfig(format=ExportFormat.JSON))
        assert res.doc_count == 0

    def test_doc_count_large(self, exporter):
        docs = [{"i": i} for i in range(100)]
        res = exporter.export(docs, ExportConfig(format=ExportFormat.JSONL))
        assert res.doc_count == 100


class TestByteSize:
    def test_byte_size_positive(self, exporter, sample_docs):
        res = exporter.export(sample_docs, ExportConfig(format=ExportFormat.JSON))
        assert res.byte_size > 0

    def test_byte_size_matches_encoded(self, exporter, sample_docs):
        res = exporter.export(sample_docs, ExportConfig(format=ExportFormat.JSON))
        assert res.byte_size == len(res.content.encode("utf-8"))

    def test_byte_size_unicode_multibyte(self, exporter):
        docs = [{"t": "Привет"}]
        res = exporter.export(docs, ExportConfig(format=ExportFormat.JSON))
        # Russian chars are multibyte in UTF-8
        assert res.byte_size > len(res.content)


class TestEdgeCases:
    def test_empty_docs_json(self, exporter):
        res = exporter.export([], ExportConfig(format=ExportFormat.JSON))
        assert res.content == "[]"
        assert res.doc_count == 0

    def test_empty_docs_csv(self, exporter):
        res = exporter.export([], ExportConfig(format=ExportFormat.CSV))
        assert res.content == ""

    def test_none_docs_raises(self, exporter):
        with pytest.raises(ExportError):
            exporter.export(None)  # type: ignore[arg-type]

    def test_non_list_raises(self, exporter):
        with pytest.raises(ExportError):
            exporter.export({"a": 1})  # type: ignore[arg-type]

    def test_non_dict_item_raises(self, exporter):
        with pytest.raises(ExportError):
            exporter.export(["not a dict"])  # type: ignore[list-item]

    def test_unicode_roundtrip_json(self, exporter):
        docs = [{"t": "Привет, мир 🌍"}]
        res = exporter.export(docs, ExportConfig(format=ExportFormat.JSON))
        assert "Привет" in res.content
        assert "🌍" in res.content

    def test_csv_special_chars_quoted(self, exporter):
        docs = [{"t": 'has "quote" and, comma'}]
        out = exporter.export_to_csv(docs)
        # csv stdlib will quote and escape
        reader = csv.DictReader(io.StringIO(out))
        row = next(reader)
        assert row["t"] == 'has "quote" and, comma'

    def test_newline_in_value_csv(self, exporter):
        docs = [{"t": "line1\nline2"}]
        out = exporter.export_to_csv(docs)
        reader = csv.DictReader(io.StringIO(out))
        row = next(reader)
        assert row["t"] == "line1\nline2"

    def test_xml_empty_value(self, exporter):
        out = exporter.export_to_xml([{"k": None}])
        assert "<k></k>" in out

    def test_markdown_unicode(self, exporter):
        out = exporter.export_to_markdown([{"title": "Заголовок", "content": "тело"}])
        assert "# Заголовок" in out
        assert "тело" in out
