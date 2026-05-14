"""Tests for E314 DocFormatRegistry."""

import threading
import pytest

from docstoolkit.doc_format_registry import (
    FormatSpec,
    ValidationResult,
    FormatStats,
    DocFormatRegistry,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _md_spec(**kwargs) -> FormatSpec:
    defaults = dict(
        format_id="markdown",
        mime_type="text/markdown",
        extensions=[".md", ".markdown"],
        description="Markdown document",
    )
    defaults.update(kwargs)
    return FormatSpec(**defaults)


def _pdf_spec(**kwargs) -> FormatSpec:
    defaults = dict(
        format_id="pdf",
        mime_type="application/pdf",
        extensions=[".pdf"],
        max_size_bytes=10_000_000,
        description="PDF document",
    )
    defaults.update(kwargs)
    return FormatSpec(**defaults)


def _docx_spec(**kwargs) -> FormatSpec:
    defaults = dict(
        format_id="docx",
        mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        extensions=[".docx"],
        description="Word document",
    )
    defaults.update(kwargs)
    return FormatSpec(**defaults)


# ---------------------------------------------------------------------------
# TestFormatSpecDataclass
# ---------------------------------------------------------------------------

class TestFormatSpecDataclass:
    def test_required_fields(self):
        spec = FormatSpec(format_id="txt", mime_type="text/plain")
        assert spec.format_id == "txt"
        assert spec.mime_type == "text/plain"

    def test_default_extensions(self):
        spec = FormatSpec(format_id="txt", mime_type="text/plain")
        assert spec.extensions == []

    def test_default_max_size_bytes_none(self):
        spec = FormatSpec(format_id="txt", mime_type="text/plain")
        assert spec.max_size_bytes is None

    def test_default_description_empty(self):
        spec = FormatSpec(format_id="txt", mime_type="text/plain")
        assert spec.description == ""

    def test_default_schema_empty_dict(self):
        spec = FormatSpec(format_id="txt", mime_type="text/plain")
        assert spec.schema == {}

    def test_extensions_independent(self):
        # Mutable default is independent per instance
        s1 = FormatSpec(format_id="a", mime_type="x/a")
        s2 = FormatSpec(format_id="b", mime_type="x/b")
        s1.extensions.append(".a")
        assert s2.extensions == []

    def test_schema_independent(self):
        s1 = FormatSpec(format_id="a", mime_type="x/a")
        s2 = FormatSpec(format_id="b", mime_type="x/b")
        s1.schema["key"] = "val"
        assert "key" not in s2.schema

    def test_explicit_values(self):
        spec = FormatSpec(
            format_id="pdf",
            mime_type="application/pdf",
            extensions=[".pdf"],
            max_size_bytes=1024,
            description="PDF",
            schema={"required_fields": ["title"]},
        )
        assert spec.max_size_bytes == 1024
        assert spec.description == "PDF"
        assert spec.schema == {"required_fields": ["title"]}


# ---------------------------------------------------------------------------
# TestValidationResultDataclass
# ---------------------------------------------------------------------------

class TestValidationResultDataclass:
    def test_valid_true(self):
        vr = ValidationResult(valid=True, format_id="md")
        assert vr.valid is True
        assert vr.format_id == "md"

    def test_default_errors_empty(self):
        vr = ValidationResult(valid=True, format_id="md")
        assert vr.errors == []

    def test_default_warnings_empty(self):
        vr = ValidationResult(valid=True, format_id="md")
        assert vr.warnings == []

    def test_errors_independent(self):
        v1 = ValidationResult(valid=False, format_id="a")
        v2 = ValidationResult(valid=False, format_id="b")
        v1.errors.append("err")
        assert v2.errors == []

    def test_warnings_independent(self):
        v1 = ValidationResult(valid=True, format_id="a")
        v2 = ValidationResult(valid=True, format_id="b")
        v1.warnings.append("warn")
        assert v2.warnings == []


# ---------------------------------------------------------------------------
# TestFormatStatsDataclass
# ---------------------------------------------------------------------------

class TestFormatStatsDataclass:
    def test_fields(self):
        fs = FormatStats(total_formats=3, total_mime_types=2, total_extensions=5)
        assert fs.total_formats == 3
        assert fs.total_mime_types == 2
        assert fs.total_extensions == 5

    def test_zero_values(self):
        fs = FormatStats(total_formats=0, total_mime_types=0, total_extensions=0)
        assert fs.total_formats == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_registry(self):
        reg = DocFormatRegistry()
        assert reg.list_formats() == []

    def test_stats_empty(self):
        reg = DocFormatRegistry()
        s = reg.stats()
        assert s.total_formats == 0
        assert s.total_mime_types == 0
        assert s.total_extensions == 0


# ---------------------------------------------------------------------------
# TestRegister
# ---------------------------------------------------------------------------

class TestRegister:
    def test_register_new(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        assert reg.get_format("markdown") is not None

    def test_register_sets_ext_index(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        assert reg.by_extension(".md") is not None
        assert reg.by_extension(".markdown") is not None

    def test_register_sets_mime_index(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        assert reg.by_mime_type("text/markdown") is not None

    def test_register_replaces_existing(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(description="v1"))
        reg.register(_md_spec(description="v2"))
        assert reg.get_format("markdown").description == "v2"

    def test_register_replace_updates_ext_index(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(extensions=[".md"]))
        # Replace with different extensions
        reg.register(_md_spec(extensions=[".mdown"]))
        # Old extension should no longer point to markdown
        assert reg.by_extension(".md") is None
        assert reg.by_extension(".mdown") is not None

    def test_register_replace_updates_mime_index(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(mime_type="text/markdown"))
        reg.register(_md_spec(mime_type="text/x-markdown"))
        # Old MIME should be removed
        assert reg.by_mime_type("text/markdown") is None
        assert reg.by_mime_type("text/x-markdown") is not None

    def test_register_multiple(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        reg.register(_pdf_spec())
        assert len(reg.list_formats()) == 2

    def test_last_registered_wins_for_ext(self):
        """If two formats share an extension, last registered wins."""
        reg = DocFormatRegistry()
        reg.register(FormatSpec(format_id="a", mime_type="x/a", extensions=[".txt"]))
        reg.register(FormatSpec(format_id="b", mime_type="x/b", extensions=[".txt"]))
        result = reg.by_extension(".txt")
        assert result is not None
        assert result.format_id == "b"

    def test_last_registered_wins_for_mime(self):
        reg = DocFormatRegistry()
        reg.register(FormatSpec(format_id="a", mime_type="text/plain", extensions=[]))
        reg.register(FormatSpec(format_id="b", mime_type="text/plain", extensions=[]))
        result = reg.by_mime_type("text/plain")
        assert result is not None
        assert result.format_id == "b"


# ---------------------------------------------------------------------------
# TestUnregister
# ---------------------------------------------------------------------------

class TestUnregister:
    def test_unregister_existing_returns_true(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        assert reg.unregister("markdown") is True

    def test_unregister_missing_returns_false(self):
        reg = DocFormatRegistry()
        assert reg.unregister("nonexistent") is False

    def test_unregister_removes_from_formats(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        reg.unregister("markdown")
        assert reg.get_format("markdown") is None

    def test_unregister_removes_from_ext_index(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        reg.unregister("markdown")
        assert reg.by_extension(".md") is None
        assert reg.by_extension(".markdown") is None

    def test_unregister_removes_from_mime_index(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        reg.unregister("markdown")
        assert reg.by_mime_type("text/markdown") is None

    def test_unregister_only_removes_own_ext_entries(self):
        """Unregister should not remove ext index entries owned by another format."""
        reg = DocFormatRegistry()
        reg.register(FormatSpec(format_id="a", mime_type="x/a", extensions=[".txt"]))
        reg.register(FormatSpec(format_id="b", mime_type="x/b", extensions=[".txt"]))
        # "b" now owns .txt; unregistering "a" should not remove .txt
        reg.unregister("a")
        assert reg.by_extension(".txt") is not None
        assert reg.by_extension(".txt").format_id == "b"


# ---------------------------------------------------------------------------
# TestGetFormat
# ---------------------------------------------------------------------------

class TestGetFormat:
    def test_found(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        spec = reg.get_format("markdown")
        assert spec is not None
        assert spec.format_id == "markdown"

    def test_not_found(self):
        reg = DocFormatRegistry()
        assert reg.get_format("unknown") is None


# ---------------------------------------------------------------------------
# TestByExtension
# ---------------------------------------------------------------------------

class TestByExtension:
    def test_found(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        spec = reg.by_extension(".md")
        assert spec is not None
        assert spec.format_id == "markdown"

    def test_found_second_ext(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        spec = reg.by_extension(".markdown")
        assert spec is not None

    def test_not_found(self):
        reg = DocFormatRegistry()
        assert reg.by_extension(".xyz") is None

    def test_not_found_empty_registry(self):
        reg = DocFormatRegistry()
        assert reg.by_extension(".md") is None


# ---------------------------------------------------------------------------
# TestByMimeType
# ---------------------------------------------------------------------------

class TestByMimeType:
    def test_found(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        spec = reg.by_mime_type("text/markdown")
        assert spec is not None
        assert spec.format_id == "markdown"

    def test_not_found(self):
        reg = DocFormatRegistry()
        assert reg.by_mime_type("application/unknown") is None

    def test_not_found_empty_registry(self):
        reg = DocFormatRegistry()
        assert reg.by_mime_type("text/plain") is None


# ---------------------------------------------------------------------------
# TestListFormats
# ---------------------------------------------------------------------------

class TestListFormats:
    def test_empty(self):
        reg = DocFormatRegistry()
        assert reg.list_formats() == []

    def test_sorted_by_format_id(self):
        reg = DocFormatRegistry()
        reg.register(_pdf_spec())
        reg.register(_md_spec())
        reg.register(_docx_spec())
        ids = [s.format_id for s in reg.list_formats()]
        assert ids == sorted(ids)

    def test_returns_all_registered(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        reg.register(_pdf_spec())
        assert len(reg.list_formats()) == 2

    def test_contains_correct_specs(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        specs = reg.list_formats()
        assert specs[0].format_id == "markdown"


# ---------------------------------------------------------------------------
# TestValidateUnknown
# ---------------------------------------------------------------------------

class TestValidateUnknown:
    def test_unknown_format_invalid(self):
        reg = DocFormatRegistry()
        result = reg.validate("ghost", "some content")
        assert result.valid is False

    def test_unknown_format_error_message(self):
        reg = DocFormatRegistry()
        result = reg.validate("ghost", "some content")
        assert "Unknown format" in result.errors

    def test_unknown_format_id_preserved(self):
        reg = DocFormatRegistry()
        result = reg.validate("ghost", "")
        assert result.format_id == "ghost"


# ---------------------------------------------------------------------------
# TestValidateSize
# ---------------------------------------------------------------------------

class TestValidateSize:
    def test_under_limit_ok(self):
        reg = DocFormatRegistry()
        reg.register(_pdf_spec(max_size_bytes=1000))
        result = reg.validate("pdf", "content", size_bytes=500)
        assert "Exceeds max size" not in result.errors

    def test_exactly_at_limit_ok(self):
        reg = DocFormatRegistry()
        reg.register(_pdf_spec(max_size_bytes=1000))
        result = reg.validate("pdf", "content", size_bytes=1000)
        assert "Exceeds max size" not in result.errors

    def test_over_limit_error(self):
        reg = DocFormatRegistry()
        reg.register(_pdf_spec(max_size_bytes=1000))
        result = reg.validate("pdf", "content", size_bytes=1001)
        assert "Exceeds max size" in result.errors

    def test_over_limit_invalid(self):
        reg = DocFormatRegistry()
        reg.register(_pdf_spec(max_size_bytes=100))
        result = reg.validate("pdf", "content", size_bytes=200)
        assert result.valid is False

    def test_no_max_size_no_error(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(max_size_bytes=None))
        result = reg.validate("markdown", "content", size_bytes=999_999_999)
        assert "Exceeds max size" not in result.errors

    def test_no_size_bytes_arg_no_check(self):
        reg = DocFormatRegistry()
        reg.register(_pdf_spec(max_size_bytes=10))
        # size_bytes not passed — no size check should happen
        result = reg.validate("pdf", "content")
        assert "Exceeds max size" not in result.errors


# ---------------------------------------------------------------------------
# TestValidateRequiredFields
# ---------------------------------------------------------------------------

class TestValidateRequiredFields:
    def test_required_field_present(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"required_fields": ["title:"]}))
        result = reg.validate("markdown", "title: My Doc\nbody text")
        assert not any("title:" in e for e in result.errors)

    def test_required_field_missing(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"required_fields": ["title:"]}))
        result = reg.validate("markdown", "just some body text")
        assert any("title:" in e for e in result.errors)

    def test_missing_required_makes_invalid(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"required_fields": ["author:"]}))
        result = reg.validate("markdown", "no author here")
        assert result.valid is False

    def test_multiple_required_all_present(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"required_fields": ["title:", "date:"]}))
        result = reg.validate("markdown", "title: Doc\ndate: 2026-01-01")
        assert result.errors == []

    def test_multiple_required_one_missing(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"required_fields": ["title:", "date:"]}))
        result = reg.validate("markdown", "title: Doc\nno date here")
        assert len(result.errors) == 1
        assert "date:" in result.errors[0]

    def test_no_required_fields_no_error(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={}))
        result = reg.validate("markdown", "")
        assert result.errors == []


# ---------------------------------------------------------------------------
# TestValidateForbiddenPatterns
# ---------------------------------------------------------------------------

class TestValidateForbiddenPatterns:
    def test_forbidden_absent_no_warning(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"forbidden_patterns": ["<script>"]}))
        result = reg.validate("markdown", "safe content here")
        assert result.warnings == []

    def test_forbidden_present_warning(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"forbidden_patterns": ["<script>"]}))
        result = reg.validate("markdown", "text <script>alert(1)</script> text")
        assert any("<script>" in w for w in result.warnings)

    def test_forbidden_present_still_valid(self):
        """Forbidden patterns add warnings, not errors — still valid."""
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"forbidden_patterns": ["TODO"]}))
        result = reg.validate("markdown", "this is a TODO item")
        assert result.valid is True

    def test_multiple_forbidden_all_present(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"forbidden_patterns": ["<script>", "DROP TABLE"]}))
        result = reg.validate("markdown", "hey <script> and DROP TABLE danger")
        assert len(result.warnings) == 2

    def test_multiple_forbidden_one_present(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"forbidden_patterns": ["<script>", "DROP TABLE"]}))
        result = reg.validate("markdown", "hey <script> only")
        assert len(result.warnings) == 1


# ---------------------------------------------------------------------------
# TestValidateValid
# ---------------------------------------------------------------------------

class TestValidateValid:
    def test_no_errors_is_valid(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        result = reg.validate("markdown", "hello world")
        assert result.valid is True

    def test_errors_present_is_invalid(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"required_fields": ["MUST_HAVE"]}))
        result = reg.validate("markdown", "no required field here")
        assert result.valid is False

    def test_warnings_do_not_affect_valid(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(schema={"forbidden_patterns": ["BAD"]}))
        result = reg.validate("markdown", "this is BAD content")
        assert result.valid is True
        assert len(result.warnings) == 1

    def test_format_id_preserved_in_result(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        result = reg.validate("markdown", "content")
        assert result.format_id == "markdown"


# ---------------------------------------------------------------------------
# TestDetectFormat
# ---------------------------------------------------------------------------

class TestDetectFormat:
    def test_detect_md(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        spec = reg.detect_format("README.md")
        assert spec is not None
        assert spec.format_id == "markdown"

    def test_detect_markdown_ext(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        spec = reg.detect_format("notes.markdown")
        assert spec is not None
        assert spec.format_id == "markdown"

    def test_detect_pdf(self):
        reg = DocFormatRegistry()
        reg.register(_pdf_spec())
        spec = reg.detect_format("report.pdf")
        assert spec is not None
        assert spec.format_id == "pdf"

    def test_unknown_extension_returns_none(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        assert reg.detect_format("file.xyz") is None

    def test_no_extension_returns_none(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        assert reg.detect_format("Makefile") is None

    def test_path_with_dots_uses_last_ext(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        spec = reg.detect_format("my.archive.md")
        assert spec is not None
        assert spec.format_id == "markdown"


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_total_formats(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        reg.register(_pdf_spec())
        assert reg.stats().total_formats == 2

    def test_unique_mime_types(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(mime_type="text/plain"))
        reg.register(_pdf_spec(mime_type="text/plain"))  # same MIME
        assert reg.stats().total_mime_types == 1

    def test_unique_extensions(self):
        reg = DocFormatRegistry()
        reg.register(_md_spec(extensions=[".md", ".markdown"]))
        reg.register(_pdf_spec(extensions=[".pdf"]))
        assert reg.stats().total_extensions == 3

    def test_shared_extensions_counted_once(self):
        reg = DocFormatRegistry()
        reg.register(FormatSpec(format_id="a", mime_type="x/a", extensions=[".txt"]))
        reg.register(FormatSpec(format_id="b", mime_type="x/b", extensions=[".txt"]))
        # ".txt" appears in two specs but should be counted once as unique
        assert reg.stats().total_extensions == 1

    def test_empty_registry_stats(self):
        reg = DocFormatRegistry()
        s = reg.stats()
        assert s.total_formats == 0
        assert s.total_mime_types == 0
        assert s.total_extensions == 0


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_register(self):
        """Concurrent registrations must not raise or lose data."""
        reg = DocFormatRegistry()
        errors = []

        def register_format(i: int) -> None:
            try:
                spec = FormatSpec(
                    format_id=f"fmt_{i}",
                    mime_type=f"application/x-fmt-{i}",
                    extensions=[f".f{i}"],
                )
                reg.register(spec)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=register_format, args=(i,)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Exceptions during concurrent register: {errors}"
        assert reg.stats().total_formats == 50

    def test_concurrent_register_and_lookup(self):
        """Concurrent reads and writes must not raise."""
        reg = DocFormatRegistry()
        reg.register(_md_spec())
        errors = []

        def writer(i: int) -> None:
            try:
                reg.register(
                    FormatSpec(format_id=f"w{i}", mime_type=f"x/w{i}", extensions=[])
                )
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def reader() -> None:
            try:
                reg.list_formats()
                reg.by_extension(".md")
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [threading.Thread(target=writer, args=(i,)) for i in range(20)]
        threads += [threading.Thread(target=reader) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Exceptions during concurrent access: {errors}"
