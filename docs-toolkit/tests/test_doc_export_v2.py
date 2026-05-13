"""Tests for E235 doc_export_v2."""
from __future__ import annotations

import json

import pytest

from docstoolkit.doc_export_v2 import (
    DocExportV2,
    ExportConfig,
    ExportFormat,
    ExportResult,
)


# ----------------------------- Fixtures -----------------------------


@pytest.fixture
def exporter() -> DocExportV2:
    return DocExportV2()


@pytest.fixture
def docs() -> list:
    return [
        {"title": "Doc A", "content": "Hello", "tags": ["a", "b"]},
        {"title": "Doc B", "content": "World", "tags": ["c"]},
    ]


@pytest.fixture
def simple_docs() -> list:
    return [{"id": 1, "name": "alpha"}, {"id": 2, "name": "beta"}]


# ----------------------------- TestExportFormat -----------------------------


class TestExportFormat:
    def test_json_value(self):
        assert ExportFormat.JSON.value == "json"

    def test_jsonl_value(self):
        assert ExportFormat.JSONL.value == "jsonl"

    def test_csv_value(self):
        assert ExportFormat.CSV.value == "csv"

    def test_tsv_value(self):
        assert ExportFormat.TSV.value == "tsv"

    def test_xml_value(self):
        assert ExportFormat.XML.value == "xml"

    def test_markdown_value(self):
        assert ExportFormat.MARKDOWN.value == "markdown"

    def test_yaml_like_value(self):
        assert ExportFormat.YAML_LIKE.value == "yaml_like"

    def test_html_value(self):
        assert ExportFormat.HTML.value == "html"

    def test_text_value(self):
        assert ExportFormat.TEXT.value == "text"

    def test_all_distinct(self):
        values = {f.value for f in ExportFormat}
        assert len(values) == 9


# ----------------------------- TestExportConfig -----------------------------


class TestExportConfig:
    def test_defaults(self):
        cfg = ExportConfig()
        assert cfg.format == ExportFormat.JSON
        assert cfg.pretty is False
        assert cfg.delimiter == ","
        assert cfg.encoding == "utf-8"
        assert cfg.template is None
        assert cfg.fields is None
        assert cfg.include_metadata is True

    def test_custom_format(self):
        cfg = ExportConfig(format=ExportFormat.CSV)
        assert cfg.format == ExportFormat.CSV

    def test_pretty_flag(self):
        cfg = ExportConfig(pretty=True)
        assert cfg.pretty is True

    def test_fields_subset(self):
        cfg = ExportConfig(fields=["title"])
        assert cfg.fields == ["title"]

    def test_template_passed(self):
        cfg = ExportConfig(template="${title}")
        assert cfg.template == "${title}"


# ----------------------------- TestExportResult -----------------------------


class TestExportResult:
    def test_construction(self):
        res = ExportResult(
            content="x", format=ExportFormat.JSON, doc_count=1, byte_size=1, format_name="json"
        )
        assert res.content == "x"
        assert res.format == ExportFormat.JSON
        assert res.doc_count == 1
        assert res.byte_size == 1
        assert res.format_name == "json"

    def test_zero_count(self):
        res = ExportResult(
            content="[]", format=ExportFormat.JSON, doc_count=0, byte_size=2, format_name="json"
        )
        assert res.doc_count == 0


# ----------------------------- TestRegisterPlugin -----------------------------


class TestRegisterPlugin:
    def test_register_success(self, exporter):
        def plugin(docs, config):
            return "x"

        assert exporter.register_plugin("mycustom", plugin) is True
        assert "mycustom" in exporter.available_formats()

    def test_register_duplicate_returns_false(self, exporter):
        def plugin(docs, config):
            return "x"

        exporter.register_plugin("mycustom", plugin)
        assert exporter.register_plugin("mycustom", plugin) is False

    def test_register_builtin_name_rejected(self, exporter):
        def plugin(docs, config):
            return "x"

        assert exporter.register_plugin("json", plugin) is False

    def test_register_empty_name_rejected(self, exporter):
        assert exporter.register_plugin("", lambda d, c: "") is False

    def test_register_noncallable_rejected(self, exporter):
        assert exporter.register_plugin("foo", "notcallable") is False


# ----------------------------- TestUnregisterPlugin -----------------------------


class TestUnregisterPlugin:
    def test_unregister_success(self, exporter):
        exporter.register_plugin("p1", lambda d, c: "")
        assert exporter.unregister_plugin("p1") is True

    def test_unregister_unknown_returns_false(self, exporter):
        assert exporter.unregister_plugin("nope") is False

    def test_unregister_decrements_count(self, exporter):
        exporter.register_plugin("p1", lambda d, c: "")
        assert exporter.plugin_count == 1
        exporter.unregister_plugin("p1")
        assert exporter.plugin_count == 0


# ----------------------------- TestExportJson -----------------------------


class TestExportJson:
    def test_returns_string(self, exporter, simple_docs):
        out = exporter.export_to_json(simple_docs)
        assert isinstance(out, str)

    def test_roundtrip(self, exporter, simple_docs):
        out = exporter.export_to_json(simple_docs)
        assert json.loads(out) == simple_docs

    def test_pretty_has_newlines(self, exporter, simple_docs):
        out = exporter.export_to_json(simple_docs, pretty=True)
        assert "\n" in out

    def test_compact_no_extra_whitespace(self, exporter, simple_docs):
        out = exporter.export_to_json(simple_docs, pretty=False)
        assert "\n" not in out

    def test_empty_list(self, exporter):
        assert exporter.export_to_json([]) == "[]"

    def test_unicode_preserved(self, exporter):
        out = exporter.export_to_json([{"x": "Привет"}])
        assert "Привет" in out


# ----------------------------- TestExportJsonl -----------------------------


class TestExportJsonl:
    def test_one_line_per_doc(self, exporter, simple_docs):
        out = exporter.export_to_jsonl(simple_docs)
        assert len(out.split("\n")) == 2

    def test_each_line_valid_json(self, exporter, simple_docs):
        out = exporter.export_to_jsonl(simple_docs)
        for line in out.split("\n"):
            json.loads(line)

    def test_empty_list(self, exporter):
        assert exporter.export_to_jsonl([]) == ""

    def test_single_doc(self, exporter):
        out = exporter.export_to_jsonl([{"a": 1}])
        assert out == '{"a": 1}'


# ----------------------------- TestExportCsv -----------------------------


class TestExportCsv:
    def test_has_header(self, exporter, simple_docs):
        out = exporter.export_to_csv(simple_docs)
        first_line = out.split("\n")[0]
        assert "id" in first_line and "name" in first_line

    def test_rows_match(self, exporter, simple_docs):
        out = exporter.export_to_csv(simple_docs)
        lines = [ln for ln in out.split("\n") if ln]
        assert len(lines) == 3  # header + 2 rows

    def test_custom_delimiter(self, exporter, simple_docs):
        out = exporter.export_to_csv(simple_docs, delimiter=";")
        assert ";" in out

    def test_empty_returns_empty(self, exporter):
        assert exporter.export_to_csv([]) == ""

    def test_fields_subset(self, exporter, simple_docs):
        out = exporter.export_to_csv(simple_docs, fields=["name"])
        first = out.split("\n")[0]
        assert "name" in first
        assert "id" not in first


# ----------------------------- TestExportTsv -----------------------------


class TestExportTsv:
    def test_uses_tab_delimiter(self, exporter, simple_docs):
        out = exporter.export_to_tsv(simple_docs)
        assert "\t" in out

    def test_no_comma_separator(self, exporter, simple_docs):
        out = exporter.export_to_tsv(simple_docs)
        # commas may appear inside values, but the header should be tab-separated
        header = out.split("\n")[0]
        assert "\t" in header

    def test_empty(self, exporter):
        assert exporter.export_to_tsv([]) == ""


# ----------------------------- TestExportXml -----------------------------


class TestExportXml:
    def test_has_xml_declaration(self, exporter, simple_docs):
        out = exporter.export_to_xml(simple_docs)
        assert out.startswith("<?xml")

    def test_root_element(self, exporter, simple_docs):
        out = exporter.export_to_xml(simple_docs)
        assert "<documents>" in out
        assert "</documents>" in out

    def test_doc_elements(self, exporter, simple_docs):
        out = exporter.export_to_xml(simple_docs)
        assert out.count("<document>") == 2

    def test_field_tags(self, exporter, simple_docs):
        out = exporter.export_to_xml(simple_docs)
        assert "<id>" in out
        assert "<name>" in out

    def test_xml_escape(self, exporter):
        out = exporter.export_to_xml([{"x": "<a>&b"}])
        assert "&lt;a&gt;" in out
        assert "&amp;" in out


# ----------------------------- TestExportMarkdown -----------------------------


class TestExportMarkdown:
    def test_default_template_used(self, exporter, docs):
        out = exporter.export_to_markdown(docs)
        assert "# Doc A" in out
        assert "# Doc B" in out

    def test_separator_present(self, exporter, docs):
        out = exporter.export_to_markdown(docs)
        assert "---" in out

    def test_content_included(self, exporter, docs):
        out = exporter.export_to_markdown(docs)
        assert "Hello" in out
        assert "World" in out

    def test_empty(self, exporter):
        assert exporter.export_to_markdown([]) == ""


# ----------------------------- TestExportMarkdownWithTemplate -----------------------------


class TestExportMarkdownWithTemplate:
    def test_custom_template(self, exporter, docs):
        out = exporter.export_to_markdown(docs, template="## ${title}\n")
        assert "## Doc A" in out
        assert "## Doc B" in out

    def test_unknown_field_empty(self, exporter, docs):
        out = exporter.export_to_markdown(docs, template="${nope}|")
        assert out == "|" * 2

    def test_multiple_fields(self, exporter, docs):
        out = exporter.export_to_markdown(docs, template="${title}: ${content}\n")
        assert "Doc A: Hello" in out
        assert "Doc B: World" in out

    def test_template_no_placeholders(self, exporter, docs):
        out = exporter.export_to_markdown(docs, template="STATIC\n")
        assert out == "STATIC\nSTATIC\n"


# ----------------------------- TestExportYamlLike -----------------------------


class TestExportYamlLike:
    def test_key_value_format(self, exporter, simple_docs):
        out = exporter.export_to_yaml_like(simple_docs)
        assert "name: " in out

    def test_strings_quoted(self, exporter):
        out = exporter.export_to_yaml_like([{"x": "hello"}])
        assert '"hello"' in out

    def test_list_items(self, exporter, docs):
        out = exporter.export_to_yaml_like(docs)
        assert "- " in out

    def test_blank_line_between_docs(self, exporter, simple_docs):
        out = exporter.export_to_yaml_like(simple_docs)
        assert "\n\n" in out

    def test_empty(self, exporter):
        assert exporter.export_to_yaml_like([]) == ""

    def test_null_handling(self, exporter):
        out = exporter.export_to_yaml_like([{"x": None}])
        assert "null" in out


# ----------------------------- TestExportHtml -----------------------------


class TestExportHtml:
    def test_wraps_html_body(self, exporter, docs):
        out = exporter.export_to_html(docs)
        assert out.startswith("<html><body>")
        assert out.endswith("</body></html>")

    def test_default_doc_div(self, exporter, docs):
        out = exporter.export_to_html(docs)
        assert '<div class="doc">' in out

    def test_titles_rendered(self, exporter, docs):
        out = exporter.export_to_html(docs)
        assert "<h1>Doc A</h1>" in out
        assert "<h1>Doc B</h1>" in out

    def test_custom_template(self, exporter, docs):
        out = exporter.export_to_html(docs, template="<p>${title}</p>")
        assert "<p>Doc A</p>" in out

    def test_html_escape(self, exporter):
        out = exporter.export_to_html([{"title": "<x>", "content": "&y"}])
        assert "&lt;x&gt;" in out


# ----------------------------- TestExportText -----------------------------


class TestExportText:
    def test_key_value_lines(self, exporter, simple_docs):
        out = exporter.export_to_text(simple_docs)
        assert "id: 1" in out
        assert "name: alpha" in out

    def test_blank_between_docs(self, exporter, simple_docs):
        out = exporter.export_to_text(simple_docs)
        assert "\n\n" in out

    def test_empty(self, exporter):
        assert exporter.export_to_text([]) == ""


# ----------------------------- TestExportCustom -----------------------------


class TestExportCustom:
    def test_invokes_plugin(self, exporter, simple_docs):
        def plugin(docs, config):
            return f"COUNT={len(docs)}"

        exporter.register_plugin("count", plugin)
        out = exporter.export_to_custom(simple_docs, "count")
        assert out == "COUNT=2"

    def test_unknown_raises(self, exporter, simple_docs):
        with pytest.raises(ValueError):
            exporter.export_to_custom(simple_docs, "nope")

    def test_uses_default_config(self, exporter):
        captured = {}

        def plugin(docs, config):
            captured["config"] = config
            return ""

        exporter.register_plugin("p", plugin)
        exporter.export_to_custom([], "p")
        assert isinstance(captured["config"], ExportConfig)

    def test_passes_config(self, exporter):
        captured = {}

        def plugin(docs, config):
            captured["cfg"] = config
            return ""

        exporter.register_plugin("p", plugin)
        custom_cfg = ExportConfig(pretty=True)
        exporter.export_to_custom([], "p", custom_cfg)
        assert captured["cfg"].pretty is True


# ----------------------------- TestExportStream -----------------------------


class TestExportStream:
    def test_json_stream_brackets(self, exporter, simple_docs):
        cfg = ExportConfig(format=ExportFormat.JSON)
        chunks = list(exporter.export_stream(simple_docs, cfg))
        assert chunks[0] == "["
        assert chunks[-1] == "]"

    def test_json_stream_joined_valid(self, exporter, simple_docs):
        cfg = ExportConfig(format=ExportFormat.JSON)
        joined = "".join(exporter.export_stream(simple_docs, cfg))
        assert json.loads(joined) == simple_docs

    def test_jsonl_stream_one_line_each(self, exporter, simple_docs):
        cfg = ExportConfig(format=ExportFormat.JSONL)
        joined = "".join(exporter.export_stream(simple_docs, cfg))
        assert len(joined.split("\n")) == 2

    def test_other_format_single_chunk(self, exporter, simple_docs):
        cfg = ExportConfig(format=ExportFormat.CSV)
        chunks = list(exporter.export_stream(simple_docs, cfg))
        assert len(chunks) == 1

    def test_empty_json_stream(self, exporter):
        cfg = ExportConfig(format=ExportFormat.JSON)
        joined = "".join(exporter.export_stream([], cfg))
        assert joined == "[]"


# ----------------------------- TestAvailableFormats -----------------------------


class TestAvailableFormats:
    def test_contains_builtins(self, exporter):
        formats = exporter.available_formats()
        for name in ["json", "jsonl", "csv", "tsv", "xml", "markdown", "html", "text", "yaml_like"]:
            assert name in formats

    def test_contains_plugin(self, exporter):
        exporter.register_plugin("custom1", lambda d, c: "")
        assert "custom1" in exporter.available_formats()

    def test_count_after_register(self, exporter):
        base = len(exporter.available_formats())
        exporter.register_plugin("c1", lambda d, c: "")
        exporter.register_plugin("c2", lambda d, c: "")
        assert len(exporter.available_formats()) == base + 2


# ----------------------------- TestPluginCount -----------------------------


class TestPluginCount:
    def test_zero_initially(self, exporter):
        assert exporter.plugin_count == 0

    def test_increments(self, exporter):
        exporter.register_plugin("a", lambda d, c: "")
        assert exporter.plugin_count == 1
        exporter.register_plugin("b", lambda d, c: "")
        assert exporter.plugin_count == 2

    def test_property_readonly_via_assignment_raises(self, exporter):
        with pytest.raises(AttributeError):
            exporter.plugin_count = 5  # type: ignore[misc]


# ----------------------------- TestExportDispatch -----------------------------


class TestExportDispatch:
    def test_dispatch_json(self, exporter, simple_docs):
        res = exporter.export(simple_docs, ExportConfig(format=ExportFormat.JSON))
        assert res.format == ExportFormat.JSON
        assert json.loads(res.content) == simple_docs

    def test_dispatch_csv(self, exporter, simple_docs):
        res = exporter.export(simple_docs, ExportConfig(format=ExportFormat.CSV))
        assert res.format_name == "csv"

    def test_dispatch_markdown(self, exporter, docs):
        res = exporter.export(docs, ExportConfig(format=ExportFormat.MARKDOWN))
        assert "# Doc A" in res.content

    def test_doc_count_set(self, exporter, simple_docs):
        res = exporter.export(simple_docs, ExportConfig(format=ExportFormat.JSON))
        assert res.doc_count == 2

    def test_byte_size_positive(self, exporter, simple_docs):
        res = exporter.export(simple_docs, ExportConfig(format=ExportFormat.JSON))
        assert res.byte_size > 0

    def test_format_name_matches(self, exporter, simple_docs):
        for fmt, name in [
            (ExportFormat.JSON, "json"),
            (ExportFormat.JSONL, "jsonl"),
            (ExportFormat.CSV, "csv"),
            (ExportFormat.TSV, "tsv"),
            (ExportFormat.XML, "xml"),
            (ExportFormat.MARKDOWN, "markdown"),
            (ExportFormat.YAML_LIKE, "yaml_like"),
            (ExportFormat.HTML, "html"),
            (ExportFormat.TEXT, "text"),
        ]:
            res = exporter.export(simple_docs, ExportConfig(format=fmt))
            assert res.format_name == name


# ----------------------------- TestFieldsSubset -----------------------------


class TestFieldsSubset:
    def test_json_subset(self, exporter, docs):
        cfg = ExportConfig(format=ExportFormat.JSON, fields=["title"])
        res = exporter.export(docs, cfg)
        parsed = json.loads(res.content)
        for d in parsed:
            assert set(d.keys()) == {"title"}

    def test_csv_subset(self, exporter, docs):
        cfg = ExportConfig(format=ExportFormat.CSV, fields=["title"])
        res = exporter.export(docs, cfg)
        header = res.content.split("\n")[0]
        assert "title" in header
        assert "content" not in header

    def test_jsonl_subset(self, exporter, docs):
        cfg = ExportConfig(format=ExportFormat.JSONL, fields=["title"])
        res = exporter.export(docs, cfg)
        for line in res.content.split("\n"):
            parsed = json.loads(line)
            assert set(parsed.keys()) == {"title"}


# ----------------------------- TestEdgeCases -----------------------------


class TestEdgeCases:
    def test_empty_docs_json(self, exporter):
        res = exporter.export([], ExportConfig(format=ExportFormat.JSON))
        assert res.doc_count == 0
        assert res.content == "[]"

    def test_empty_docs_jsonl(self, exporter):
        res = exporter.export([], ExportConfig(format=ExportFormat.JSONL))
        assert res.doc_count == 0

    def test_unsupported_format_raises(self, exporter):
        class FakeFmt:
            pass

        cfg = ExportConfig()
        cfg.format = FakeFmt()  # type: ignore[assignment]
        with pytest.raises(ValueError):
            exporter.export([], cfg)

    def test_doc_with_none_value(self, exporter):
        out = exporter.export_to_csv([{"x": None}])
        assert "x" in out

    def test_doc_with_nested_dict(self, exporter):
        out = exporter.export_to_csv([{"x": {"nested": True}}])
        # stringified, no exceptions
        assert "x" in out

    def test_unicode_xml(self, exporter):
        out = exporter.export_to_xml([{"k": "Привет"}])
        assert "Привет" in out

    def test_stream_returns_iterator(self, exporter, simple_docs):
        import types
        cfg = ExportConfig(format=ExportFormat.JSON)
        gen = exporter.export_stream(simple_docs, cfg)
        assert isinstance(gen, types.GeneratorType)

    def test_register_then_unregister_then_register(self, exporter):
        exporter.register_plugin("p", lambda d, c: "")
        exporter.unregister_plugin("p")
        assert exporter.register_plugin("p", lambda d, c: "") is True

    def test_csv_collects_all_fields_across_docs(self, exporter):
        docs = [{"a": 1}, {"b": 2}]
        out = exporter.export_to_csv(docs)
        header = out.split("\n")[0]
        assert "a" in header and "b" in header

    def test_text_handles_list_values(self, exporter):
        out = exporter.export_to_text([{"tags": ["x", "y"]}])
        assert "x" in out and "y" in out
