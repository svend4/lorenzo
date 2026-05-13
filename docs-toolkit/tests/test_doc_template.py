"""Tests for docstoolkit.doc_template."""
from __future__ import annotations

import pytest

from docstoolkit.doc_template import (
    DocTemplate,
    RenderResult,
    TemplateDefinition,
    TemplateRegistry,
    TemplateSection,
)


# ---------------------------------------------------------------------------
# TemplateSection
# ---------------------------------------------------------------------------


class TestTemplateSection:
    def test_create_basic(self):
        sec = TemplateSection(name="intro", content="Hello")
        assert sec.name == "intro"
        assert sec.content == "Hello"
        assert sec.is_required is False

    def test_create_required(self):
        sec = TemplateSection(name="body", content="...", is_required=True)
        assert sec.is_required is True

    def test_equality(self):
        a = TemplateSection(name="x", content="y")
        b = TemplateSection(name="x", content="y")
        assert a == b


# ---------------------------------------------------------------------------
# TemplateDefinition
# ---------------------------------------------------------------------------


class TestTemplateDefinition:
    def test_create_basic(self):
        td = TemplateDefinition(name="t1")
        assert td.name == "t1"
        assert td.sections == []
        assert td.variables == []
        assert td.description == ""

    def test_with_sections(self):
        secs = [TemplateSection("a", "A"), TemplateSection("b", "B")]
        td = TemplateDefinition(name="t", sections=secs)
        assert len(td.sections) == 2
        assert td.sections[0].name == "a"

    def test_with_variables(self):
        td = TemplateDefinition(name="t", variables=["x", "y"])
        assert td.variables == ["x", "y"]

    def test_with_description(self):
        td = TemplateDefinition(name="t", description="docs")
        assert td.description == "docs"


# ---------------------------------------------------------------------------
# RenderResult
# ---------------------------------------------------------------------------


class TestRenderResult:
    def test_success_when_empty_missing(self):
        r = RenderResult(output="ok")
        assert r.success is True

    def test_not_success_when_missing_vars(self):
        r = RenderResult(output="x", missing_variables=["a"])
        assert r.success is False

    def test_not_success_when_missing_sections(self):
        r = RenderResult(output="x", missing_sections=["intro"])
        assert r.success is False

    def test_default_lists(self):
        r = RenderResult(output="x")
        assert r.missing_variables == []
        assert r.missing_sections == []


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class TestRegistry:
    def test_empty(self):
        reg = TemplateRegistry()
        assert reg.count == 0
        assert reg.list_names() == []

    def test_register(self):
        reg = TemplateRegistry()
        td = TemplateDefinition(name="foo")
        reg.register(td)
        assert reg.count == 1
        assert "foo" in reg.list_names()

    def test_get(self):
        reg = TemplateRegistry()
        td = TemplateDefinition(name="foo")
        reg.register(td)
        assert reg.get("foo") is td

    def test_get_missing(self):
        reg = TemplateRegistry()
        assert reg.get("nope") is None

    def test_list_sorted(self):
        reg = TemplateRegistry()
        reg.register(TemplateDefinition(name="b"))
        reg.register(TemplateDefinition(name="a"))
        assert reg.list_names() == ["a", "b"]

    def test_register_overwrites(self):
        reg = TemplateRegistry()
        reg.register(TemplateDefinition(name="x", description="v1"))
        reg.register(TemplateDefinition(name="x", description="v2"))
        assert reg.count == 1
        assert reg.get("x").description == "v2"

    def test_register_invalid_type(self):
        reg = TemplateRegistry()
        with pytest.raises(TypeError):
            reg.register("not a template")  # type: ignore[arg-type]

    def test_register_empty_name(self):
        reg = TemplateRegistry()
        with pytest.raises(ValueError):
            reg.register(TemplateDefinition(name=""))


# ---------------------------------------------------------------------------
# Registry: remove
# ---------------------------------------------------------------------------


class TestRegistryRemove:
    def test_remove_existing(self):
        reg = TemplateRegistry()
        reg.register(TemplateDefinition(name="x"))
        assert reg.remove("x") is True
        assert reg.count == 0

    def test_remove_missing(self):
        reg = TemplateRegistry()
        assert reg.remove("nope") is False

    def test_remove_then_get(self):
        reg = TemplateRegistry()
        reg.register(TemplateDefinition(name="x"))
        reg.remove("x")
        assert reg.get("x") is None


# ---------------------------------------------------------------------------
# Render string: variables
# ---------------------------------------------------------------------------


class TestRenderString:
    def test_simple_var(self):
        dt = DocTemplate()
        out = dt.render_string("Hello ${name}", {"name": "World"})
        assert out == "Hello World"

    def test_multiple_vars(self):
        dt = DocTemplate()
        out = dt.render_string("${a}+${b}=${c}", {"a": 1, "b": 2, "c": 3})
        assert out == "1+2=3"

    def test_var_repeated(self):
        dt = DocTemplate()
        out = dt.render_string("${x}-${x}", {"x": "v"})
        assert out == "v-v"

    def test_no_vars(self):
        dt = DocTemplate()
        assert dt.render_string("plain text", {}) == "plain text"

    def test_missing_var_left_intact(self):
        dt = DocTemplate()
        out = dt.render_string("Hello ${name}", {})
        assert "${name}" in out

    def test_numeric_value(self):
        dt = DocTemplate()
        out = dt.render_string("${n}", {"n": 42})
        assert out == "42"

    def test_none_template(self):
        dt = DocTemplate()
        assert dt.render_string(None, {}) == ""  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Render string: defaults
# ---------------------------------------------------------------------------


class TestRenderStringDefault:
    def test_default_used(self):
        dt = DocTemplate()
        out = dt.render_string("Hello ${name:Anon}", {})
        assert out == "Hello Anon"

    def test_default_overridden(self):
        dt = DocTemplate()
        out = dt.render_string("Hello ${name:Anon}", {"name": "Bob"})
        assert out == "Hello Bob"

    def test_empty_default(self):
        dt = DocTemplate()
        out = dt.render_string("[${name:}]", {})
        assert out == "[]"

    def test_default_with_spaces(self):
        dt = DocTemplate()
        out = dt.render_string("[${greet:Hi there}]", {})
        assert out == "[Hi there]"


# ---------------------------------------------------------------------------
# Comments
# ---------------------------------------------------------------------------


class TestRenderComments:
    def test_comment_removed(self):
        dt = DocTemplate()
        out = dt.render_string("Hello {{# this is a note }}World", {})
        assert "this is a note" not in out
        assert "Hello " in out
        assert "World" in out

    def test_multiline_comment(self):
        dt = DocTemplate()
        text = "A{{# multi\nline }}B"
        out = dt.render_string(text, {})
        assert "multi" not in out
        assert out.startswith("A")
        assert out.endswith("B")

    def test_multiple_comments(self):
        dt = DocTemplate()
        out = dt.render_string("{{# c1 }}X{{# c2 }}Y", {})
        assert out == "XY"

    def test_comment_with_vars_outside(self):
        dt = DocTemplate()
        out = dt.render_string("${a}{{# note }}${b}", {"a": "1", "b": "2"})
        assert out == "12"


# ---------------------------------------------------------------------------
# Render section
# ---------------------------------------------------------------------------


class TestRenderSection:
    def test_simple(self):
        dt = DocTemplate()
        out = dt.render_section("# ${title}", {"title": "Doc"})
        assert out == "# Doc"

    def test_no_vars(self):
        dt = DocTemplate()
        assert dt.render_section("just text", {}) == "just text"


# ---------------------------------------------------------------------------
# Render full template (from registry)
# ---------------------------------------------------------------------------


class TestRenderTemplate:
    def _registry_with(self, td: TemplateDefinition) -> TemplateRegistry:
        reg = TemplateRegistry()
        reg.register(td)
        return reg

    def test_simple_render(self):
        td = TemplateDefinition(
            name="t",
            sections=[TemplateSection("body", "Hello ${name}")],
            variables=["name"],
        )
        dt = DocTemplate(self._registry_with(td))
        result = dt.render("t", {"name": "World"})
        assert result.success is True
        assert "Hello World" in result.output

    def test_multiple_sections(self):
        td = TemplateDefinition(
            name="t",
            sections=[
                TemplateSection("a", "AAA"),
                TemplateSection("b", "BBB"),
            ],
        )
        dt = DocTemplate(self._registry_with(td))
        result = dt.render("t", {})
        assert "AAA" in result.output
        assert "BBB" in result.output

    def test_section_override(self):
        td = TemplateDefinition(
            name="t",
            sections=[TemplateSection("intro", "default intro")],
        )
        dt = DocTemplate(self._registry_with(td))
        result = dt.render("t", {}, sections={"intro": "custom intro"})
        assert "custom intro" in result.output
        assert "default intro" not in result.output

    def test_missing_template(self):
        dt = DocTemplate()
        result = dt.render("nope", {})
        assert result.success is False
        assert any("nope" in s for s in result.missing_sections)

    def test_section_marker_inline(self):
        td = TemplateDefinition(
            name="t",
            sections=[TemplateSection("body", "Start\n{{section: foot}}\nEnd")],
        )
        dt = DocTemplate(self._registry_with(td))
        result = dt.render("t", {}, sections={"foot": "FOOTER"})
        assert "FOOTER" in result.output


# ---------------------------------------------------------------------------
# Extract variables
# ---------------------------------------------------------------------------


class TestExtractVariables:
    def test_single(self):
        dt = DocTemplate()
        assert dt.extract_variables("Hello ${name}") == ["name"]

    def test_multiple_unique(self):
        dt = DocTemplate()
        assert dt.extract_variables("${a} ${b} ${c}") == ["a", "b", "c"]

    def test_duplicates_dedup(self):
        dt = DocTemplate()
        assert dt.extract_variables("${a} ${a} ${b}") == ["a", "b"]

    def test_with_defaults(self):
        dt = DocTemplate()
        assert dt.extract_variables("${a:x} ${b:y}") == ["a", "b"]

    def test_empty(self):
        dt = DocTemplate()
        assert dt.extract_variables("") == []

    def test_no_vars(self):
        dt = DocTemplate()
        assert dt.extract_variables("plain text") == []


# ---------------------------------------------------------------------------
# Extract sections
# ---------------------------------------------------------------------------


class TestExtractSections:
    def test_single(self):
        dt = DocTemplate()
        assert dt.extract_sections("{{section: intro}}") == ["intro"]

    def test_multiple(self):
        dt = DocTemplate()
        assert dt.extract_sections(
            "{{section: a}} text {{section: b}}"
        ) == ["a", "b"]

    def test_dedup(self):
        dt = DocTemplate()
        assert dt.extract_sections("{{section: a}}{{section: a}}") == ["a"]

    def test_empty(self):
        dt = DocTemplate()
        assert dt.extract_sections("") == []

    def test_no_sections(self):
        dt = DocTemplate()
        assert dt.extract_sections("just ${vars} no sections") == []


# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------


class TestParse:
    def test_no_frontmatter(self):
        dt = DocTemplate()
        td = dt.parse("Hello ${name}")
        assert td.name == "untitled"
        # auto-extracts vars
        assert "name" in td.variables
        assert len(td.sections) == 1
        assert td.sections[0].name == "body"

    def test_with_frontmatter(self):
        text = (
            "---\n"
            "name: My Template\n"
            "description: A test\n"
            "variables: [title, date]\n"
            "---\n"
            "# ${title}\n"
            "Date: ${date}\n"
        )
        dt = DocTemplate()
        td = dt.parse(text)
        assert td.name == "My Template"
        assert td.description == "A test"
        assert "title" in td.variables
        assert "date" in td.variables

    def test_frontmatter_body_only(self):
        text = (
            "---\n"
            "name: T\n"
            "---\n"
            "Body content here\n"
        )
        dt = DocTemplate()
        td = dt.parse(text)
        assert td.name == "T"
        assert td.sections[0].name == "body"
        assert "Body content" in td.sections[0].content

    def test_parse_with_section_markers(self):
        text = (
            "---\n"
            "name: X\n"
            "---\n"
            "{{section: intro}}\n"
            "Intro body\n"
            "{{section: outro}}\n"
            "Outro body\n"
        )
        dt = DocTemplate()
        td = dt.parse(text)
        names = [s.name for s in td.sections]
        assert "intro" in names
        assert "outro" in names

    def test_parse_empty(self):
        dt = DocTemplate()
        td = dt.parse("")
        assert td.name == "untitled"
        assert len(td.sections) == 1

    def test_parse_none(self):
        dt = DocTemplate()
        td = dt.parse(None)  # type: ignore[arg-type]
        assert td.name == "untitled"

    def test_parse_variables_quoted(self):
        text = (
            "---\n"
            "name: T\n"
            "variables: ['a', \"b\"]\n"
            "---\n"
            "body\n"
        )
        dt = DocTemplate()
        td = dt.parse(text)
        assert "a" in td.variables
        assert "b" in td.variables


# ---------------------------------------------------------------------------
# Validate
# ---------------------------------------------------------------------------


class TestValidate:
    def test_all_ok(self):
        dt = DocTemplate()
        td = TemplateDefinition(name="t", variables=["a", "b"])
        ok, missing = dt.validate(td, {"a": 1, "b": 2})
        assert ok is True
        assert missing == []

    def test_missing_var(self):
        dt = DocTemplate()
        td = TemplateDefinition(name="t", variables=["a", "b"])
        ok, missing = dt.validate(td, {"a": 1})
        assert ok is False
        assert "var:b" in missing

    def test_required_section_missing(self):
        dt = DocTemplate()
        td = TemplateDefinition(
            name="t",
            sections=[TemplateSection("intro", "", is_required=True)],
        )
        ok, missing = dt.validate(td, {})
        assert ok is False
        assert "section:intro" in missing

    def test_required_section_provided(self):
        dt = DocTemplate()
        td = TemplateDefinition(
            name="t",
            sections=[TemplateSection("intro", "", is_required=True)],
        )
        ok, missing = dt.validate(td, {}, sections={"intro": "X"})
        assert ok is True

    def test_required_section_has_default(self):
        dt = DocTemplate()
        td = TemplateDefinition(
            name="t",
            sections=[TemplateSection("intro", "default", is_required=True)],
        )
        ok, missing = dt.validate(td, {})
        assert ok is True


# ---------------------------------------------------------------------------
# Missing variables (via render)
# ---------------------------------------------------------------------------


class TestMissingVariables:
    def test_render_reports_missing(self):
        td = TemplateDefinition(
            name="t",
            sections=[TemplateSection("body", "${a} ${b}")],
            variables=["a", "b"],
        )
        reg = TemplateRegistry()
        reg.register(td)
        dt = DocTemplate(reg)
        result = dt.render("t", {"a": "X"})
        assert result.success is False
        assert "b" in result.missing_variables

    def test_render_reports_missing_section(self):
        td = TemplateDefinition(
            name="t",
            sections=[TemplateSection("body", "", is_required=True)],
        )
        reg = TemplateRegistry()
        reg.register(td)
        dt = DocTemplate(reg)
        result = dt.render("t", {})
        assert result.success is False
        assert "body" in result.missing_sections

    def test_render_success_when_all_provided(self):
        td = TemplateDefinition(
            name="t",
            sections=[TemplateSection("body", "${name}")],
            variables=["name"],
        )
        reg = TemplateRegistry()
        reg.register(td)
        dt = DocTemplate(reg)
        result = dt.render("t", {"name": "Bob"})
        assert result.success is True
        assert "Bob" in result.output


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_template_string(self):
        dt = DocTemplate()
        assert dt.render_string("", {}) == ""

    def test_no_variables_passed(self):
        dt = DocTemplate()
        out = dt.render_string("plain text", {})
        assert out == "plain text"

    def test_empty_template_definition(self):
        td = TemplateDefinition(name="empty")
        reg = TemplateRegistry()
        reg.register(td)
        dt = DocTemplate(reg)
        result = dt.render("empty", {})
        assert result.success is True
        assert result.output == ""

    def test_registry_isolated_from_dt(self):
        dt1 = DocTemplate()
        dt2 = DocTemplate()
        dt1.registry.register(TemplateDefinition(name="x"))
        assert dt2.registry.get("x") is None

    def test_registry_shared(self):
        reg = TemplateRegistry()
        dt1 = DocTemplate(reg)
        dt2 = DocTemplate(reg)
        dt1.registry.register(TemplateDefinition(name="x"))
        assert dt2.registry.get("x") is not None

    def test_underscore_var_name(self):
        dt = DocTemplate()
        out = dt.render_string("${my_var}", {"my_var": "ok"})
        assert out == "ok"

    def test_no_default_value_keeps_placeholder(self):
        dt = DocTemplate()
        out = dt.render_string("X${missing}Y", {})
        assert out == "X${missing}Y"
