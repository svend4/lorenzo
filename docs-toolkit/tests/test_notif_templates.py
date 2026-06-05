"""Tests for the notif_templates module (E70).

Coverage targets:
- TemplateFormat enum
- TemplateVariable dataclass
- NotifTemplate dataclass (required_variables / optional_variables)
- TemplateRenderer (render, render_batch, validate)
- TemplateRegistry (register, get, get_by_name, list_all, list_by_tag,
                    unregister, render delegation)
- Edge cases
"""
from __future__ import annotations

import pytest

from docstoolkit.notif_templates import (
    NotifTemplate,
    RenderResult,
    TemplateFormat,
    TemplateRegistry,
    TemplateRenderer,
    TemplateVariable,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_var(name: str, required: bool = True, default: str = "", desc: str = "") -> TemplateVariable:
    return TemplateVariable(name=name, required=required, default_value=default, description=desc)


def _make_tmpl(
    name: str = "test",
    body: str = "Hello",
    subject: str = "",
    fmt: TemplateFormat = TemplateFormat.TEXT,
    variables: list[TemplateVariable] | None = None,
    tags: list[str] | None = None,
    template_id: str | None = None,
) -> NotifTemplate:
    kwargs: dict = dict(
        name=name,
        body=body,
        subject=subject,
        format=fmt,
        variables=variables or [],
        tags=tags or [],
    )
    if template_id is not None:
        kwargs["template_id"] = template_id
    return NotifTemplate(**kwargs)


# ---------------------------------------------------------------------------
# TemplateFormat
# ---------------------------------------------------------------------------

class TestTemplateFormat:
    def test_text_value(self):
        assert TemplateFormat.TEXT.value == "text"

    def test_html_value(self):
        assert TemplateFormat.HTML.value == "html"

    def test_markdown_value(self):
        assert TemplateFormat.MARKDOWN.value == "markdown"

    def test_json_value(self):
        assert TemplateFormat.JSON.value == "json"

    def test_enum_members_count(self):
        assert len(TemplateFormat) == 4

    def test_enum_membership(self):
        assert TemplateFormat("text") is TemplateFormat.TEXT

    def test_enum_iteration(self):
        values = {f.value for f in TemplateFormat}
        assert values == {"text", "html", "markdown", "json"}


# ---------------------------------------------------------------------------
# TemplateVariable
# ---------------------------------------------------------------------------

class TestTemplateVariable:
    def test_required_defaults_to_true(self):
        v = TemplateVariable(name="foo")
        assert v.required is True

    def test_default_value_defaults_to_empty(self):
        v = TemplateVariable(name="foo")
        assert v.default_value == ""

    def test_description_defaults_to_empty(self):
        v = TemplateVariable(name="foo")
        assert v.description == ""

    def test_explicit_values(self):
        v = TemplateVariable(name="bar", required=False, default_value="N/A", description="A field")
        assert v.name == "bar"
        assert v.required is False
        assert v.default_value == "N/A"
        assert v.description == "A field"

    def test_optional_variable(self):
        v = TemplateVariable(name="opt", required=False)
        assert not v.required

    def test_required_variable(self):
        v = TemplateVariable(name="req", required=True)
        assert v.required


# ---------------------------------------------------------------------------
# NotifTemplate
# ---------------------------------------------------------------------------

class TestNotifTemplate:
    def test_auto_generated_template_id(self):
        t = _make_tmpl()
        assert t.template_id
        assert len(t.template_id) == 8

    def test_unique_template_ids(self):
        ids = {_make_tmpl().template_id for _ in range(20)}
        assert len(ids) == 20

    def test_explicit_template_id(self):
        t = _make_tmpl(template_id="abc12345")
        assert t.template_id == "abc12345"

    def test_name_stored(self):
        t = _make_tmpl(name="welcome")
        assert t.name == "welcome"

    def test_body_stored(self):
        t = _make_tmpl(body="Dear {user}")
        assert t.body == "Dear {user}"

    def test_subject_defaults_to_empty(self):
        t = _make_tmpl()
        assert t.subject == ""

    def test_format_defaults_to_text(self):
        t = _make_tmpl()
        assert t.format is TemplateFormat.TEXT

    def test_tags_default_empty(self):
        t = _make_tmpl()
        assert t.tags == []

    def test_variables_default_empty(self):
        t = _make_tmpl()
        assert t.variables == []

    def test_required_variables_all_required(self):
        t = _make_tmpl(variables=[_make_var("a"), _make_var("b")])
        assert t.required_variables() == ["a", "b"]

    def test_optional_variables_none_when_all_required(self):
        t = _make_tmpl(variables=[_make_var("a"), _make_var("b")])
        assert t.optional_variables() == []

    def test_required_variables_none_when_all_optional(self):
        t = _make_tmpl(variables=[_make_var("x", required=False), _make_var("y", required=False)])
        assert t.required_variables() == []

    def test_optional_variables_all_optional(self):
        t = _make_tmpl(variables=[_make_var("x", required=False), _make_var("y", required=False)])
        assert t.optional_variables() == ["x", "y"]

    def test_mixed_variables(self):
        t = _make_tmpl(variables=[
            _make_var("req1"),
            _make_var("opt1", required=False),
            _make_var("req2"),
            _make_var("opt2", required=False),
        ])
        assert t.required_variables() == ["req1", "req2"]
        assert t.optional_variables() == ["opt1", "opt2"]

    def test_empty_variables_list(self):
        t = _make_tmpl()
        assert t.required_variables() == []
        assert t.optional_variables() == []


# ---------------------------------------------------------------------------
# RenderResult
# ---------------------------------------------------------------------------

class TestRenderResult:
    def test_is_complete_no_missing(self):
        r = RenderResult(subject="hi", body="body", format=TemplateFormat.TEXT, missing_vars=[])
        assert r.is_complete() is True

    def test_is_complete_with_missing(self):
        r = RenderResult(subject="hi", body="body", format=TemplateFormat.TEXT, missing_vars=["x"])
        assert r.is_complete() is False

    def test_fields_accessible(self):
        r = RenderResult(subject="s", body="b", format=TemplateFormat.HTML, missing_vars=["y"])
        assert r.subject == "s"
        assert r.body == "b"
        assert r.format is TemplateFormat.HTML
        assert r.missing_vars == ["y"]


# ---------------------------------------------------------------------------
# TemplateRenderer
# ---------------------------------------------------------------------------

class TestTemplateRenderer:
    def setup_method(self):
        self.renderer = TemplateRenderer()

    # -- basic render --------------------------------------------------------

    def test_render_no_placeholders(self):
        t = _make_tmpl(body="Hello world")
        r = self.renderer.render(t, {})
        assert r.body == "Hello world"
        assert r.is_complete()

    def test_render_fills_body_placeholder(self):
        t = _make_tmpl(
            body="Hello {name}",
            variables=[_make_var("name")],
        )
        r = self.renderer.render(t, {"name": "Alice"})
        assert r.body == "Hello Alice"

    def test_render_fills_subject_placeholder(self):
        t = _make_tmpl(
            subject="Welcome {name}",
            body="Body",
            variables=[_make_var("name")],
        )
        r = self.renderer.render(t, {"name": "Bob"})
        assert r.subject == "Welcome Bob"

    def test_render_fills_multiple_placeholders(self):
        t = _make_tmpl(
            body="{greeting}, {name}! Your code is {code}.",
            variables=[_make_var("greeting"), _make_var("name"), _make_var("code")],
        )
        r = self.renderer.render(t, {"greeting": "Hi", "name": "Carol", "code": "42"})
        assert r.body == "Hi, Carol! Your code is 42."

    def test_render_format_propagated(self):
        t = _make_tmpl(body="body", fmt=TemplateFormat.HTML)
        r = self.renderer.render(t, {})
        assert r.format is TemplateFormat.HTML

    # -- missing required variable ------------------------------------------

    def test_missing_required_var_recorded(self):
        t = _make_tmpl(
            body="Hello {name}",
            variables=[_make_var("name")],
        )
        r = self.renderer.render(t, {})
        assert "name" in r.missing_vars

    def test_missing_required_var_not_complete(self):
        t = _make_tmpl(
            body="{x}",
            variables=[_make_var("x")],
        )
        r = self.renderer.render(t, {})
        assert not r.is_complete()

    def test_multiple_missing_required_vars(self):
        t = _make_tmpl(
            body="{a} {b} {c}",
            variables=[_make_var("a"), _make_var("b"), _make_var("c")],
        )
        r = self.renderer.render(t, {})
        assert set(r.missing_vars) == {"a", "b", "c"}

    def test_missing_required_does_not_raise(self):
        t = _make_tmpl(body="{x}", variables=[_make_var("x")])
        # Must not raise
        r = self.renderer.render(t, {})
        assert r is not None

    # -- optional variable uses default -------------------------------------

    def test_optional_var_uses_default(self):
        t = _make_tmpl(
            body="Hi {title}",
            variables=[_make_var("title", required=False, default="friend")],
        )
        r = self.renderer.render(t, {})
        assert r.body == "Hi friend"
        assert r.is_complete()

    def test_optional_var_context_overrides_default(self):
        t = _make_tmpl(
            body="Hi {title}",
            variables=[_make_var("title", required=False, default="friend")],
        )
        r = self.renderer.render(t, {"title": "Alice"})
        assert r.body == "Hi Alice"

    def test_optional_var_empty_string_default(self):
        t = _make_tmpl(
            body="pre{suffix}post",
            variables=[_make_var("suffix", required=False, default="")],
        )
        r = self.renderer.render(t, {})
        assert r.body == "prepost"
        assert r.is_complete()

    def test_only_optional_vars_complete(self):
        t = _make_tmpl(
            body="{a} {b}",
            variables=[
                _make_var("a", required=False, default="X"),
                _make_var("b", required=False, default="Y"),
            ],
        )
        r = self.renderer.render(t, {})
        assert r.is_complete()
        assert r.body == "X Y"

    # -- render_batch --------------------------------------------------------

    def test_render_batch_returns_list(self):
        t = _make_tmpl(body="Hi {name}", variables=[_make_var("name")])
        results = self.renderer.render_batch(t, [{"name": "A"}, {"name": "B"}])
        assert isinstance(results, list)
        assert len(results) == 2

    def test_render_batch_each_result(self):
        t = _make_tmpl(body="{n}", variables=[_make_var("n")])
        results = self.renderer.render_batch(t, [{"n": "1"}, {"n": "2"}, {"n": "3"}])
        assert [r.body for r in results] == ["1", "2", "3"]

    def test_render_batch_empty_list(self):
        t = _make_tmpl(body="x")
        results = self.renderer.render_batch(t, [])
        assert results == []

    def test_render_batch_independent_missing(self):
        t = _make_tmpl(body="{x}", variables=[_make_var("x")])
        results = self.renderer.render_batch(t, [{"x": "ok"}, {}])
        assert results[0].is_complete()
        assert not results[1].is_complete()

    # -- validate ------------------------------------------------------------

    def test_validate_all_present(self):
        t = _make_tmpl(variables=[_make_var("a"), _make_var("b")])
        assert self.renderer.validate(t, {"a": "1", "b": "2"}) == []

    def test_validate_missing_one(self):
        t = _make_tmpl(variables=[_make_var("a"), _make_var("b")])
        missing = self.renderer.validate(t, {"a": "1"})
        assert missing == ["b"]

    def test_validate_missing_all(self):
        t = _make_tmpl(variables=[_make_var("x"), _make_var("y")])
        missing = self.renderer.validate(t, {})
        assert set(missing) == {"x", "y"}

    def test_validate_ignores_optional(self):
        t = _make_tmpl(variables=[
            _make_var("req"),
            _make_var("opt", required=False),
        ])
        missing = self.renderer.validate(t, {"req": "v"})
        assert missing == []

    def test_validate_empty_template_empty_context(self):
        t = _make_tmpl()
        assert self.renderer.validate(t, {}) == []

    def test_validate_returns_sorted(self):
        t = _make_tmpl(variables=[_make_var("z"), _make_var("a"), _make_var("m")])
        missing = self.renderer.validate(t, {})
        assert missing == sorted(missing)

    # -- all vars provided ---------------------------------------------------

    def test_all_vars_provided_complete(self):
        t = _make_tmpl(
            body="{a} {b}",
            variables=[_make_var("a"), _make_var("b")],
        )
        r = self.renderer.render(t, {"a": "1", "b": "2"})
        assert r.is_complete()
        assert r.missing_vars == []

    # -- empty context -------------------------------------------------------

    def test_empty_context_no_vars_complete(self):
        t = _make_tmpl(body="static")
        r = self.renderer.render(t, {})
        assert r.is_complete()
        assert r.body == "static"


# ---------------------------------------------------------------------------
# TemplateRegistry
# ---------------------------------------------------------------------------

class TestTemplateRegistry:
    def setup_method(self):
        self.registry = TemplateRegistry()

    def _register(self, tid: str = "t001", name: str = "tmpl", **kw) -> NotifTemplate:
        t = _make_tmpl(template_id=tid, name=name, **kw)
        self.registry.register(t)
        return t

    # -- register ------------------------------------------------------------

    def test_register_success(self):
        t = self._register("id1")
        assert self.registry.get("id1") is t

    def test_register_duplicate_raises(self):
        self._register("id1")
        t2 = _make_tmpl(template_id="id1", name="other")
        with pytest.raises(ValueError):
            self.registry.register(t2)

    def test_register_multiple_distinct(self):
        self._register("a")
        self._register("b")
        assert len(self.registry.list_all()) == 2

    # -- get -----------------------------------------------------------------

    def test_get_existing(self):
        t = self._register("x1")
        assert self.registry.get("x1") is t

    def test_get_nonexistent_returns_none(self):
        assert self.registry.get("nope") is None

    # -- get_by_name ---------------------------------------------------------

    def test_get_by_name_existing(self):
        t = self._register("id1", name="welcome")
        assert self.registry.get_by_name("welcome") is t

    def test_get_by_name_nonexistent_returns_none(self):
        assert self.registry.get_by_name("ghost") is None

    def test_get_by_name_returns_first_match(self):
        t1 = self._register("id1", name="dup")
        self._register("id2", name="dup")
        # first registered is returned
        assert self.registry.get_by_name("dup") is t1

    # -- list_all ------------------------------------------------------------

    def test_list_all_empty(self):
        assert self.registry.list_all() == []

    def test_list_all_returns_all(self):
        t1 = self._register("a1")
        t2 = self._register("a2")
        all_ids = {t.template_id for t in self.registry.list_all()}
        assert all_ids == {t1.template_id, t2.template_id}

    def test_list_all_preserves_insertion_order(self):
        ids = [f"id{i}" for i in range(5)]
        templates = [self._register(tid) for tid in ids]
        assert self.registry.list_all() == templates

    # -- list_by_tag ---------------------------------------------------------

    def test_list_by_tag_no_match(self):
        self._register("t1", tags=["a"])
        assert self.registry.list_by_tag("z") == []

    def test_list_by_tag_single_match(self):
        t = self._register("t1", tags=["promo"])
        self._register("t2", tags=["system"])
        assert self.registry.list_by_tag("promo") == [t]

    def test_list_by_tag_multiple_matches(self):
        t1 = self._register("t1", tags=["urgent", "email"])
        t2 = self._register("t2", tags=["urgent", "sms"])
        result = self.registry.list_by_tag("urgent")
        assert {t.template_id for t in result} == {t1.template_id, t2.template_id}

    def test_list_by_tag_empty_registry(self):
        assert self.registry.list_by_tag("any") == []

    # -- unregister ----------------------------------------------------------

    def test_unregister_existing_returns_true(self):
        self._register("del1")
        assert self.registry.unregister("del1") is True

    def test_unregister_existing_removes_it(self):
        self._register("del2")
        self.registry.unregister("del2")
        assert self.registry.get("del2") is None

    def test_unregister_nonexistent_returns_false(self):
        assert self.registry.unregister("ghost") is False

    def test_unregister_does_not_affect_others(self):
        self._register("keep")
        self._register("drop")
        self.registry.unregister("drop")
        assert self.registry.get("keep") is not None
        assert len(self.registry.list_all()) == 1

    def test_reregister_after_unregister(self):
        self._register("reuse")
        self.registry.unregister("reuse")
        t2 = _make_tmpl(template_id="reuse", name="new")
        self.registry.register(t2)
        assert self.registry.get("reuse") is t2

    # -- render delegates ---------------------------------------------------

    def test_render_delegate_fills_body(self):
        self._register(
            "r1",
            body="Hi {name}",
            variables=[_make_var("name")],
        )
        result = self.registry.render("r1", {"name": "Alice"})
        assert result.body == "Hi Alice"

    def test_render_delegate_raises_key_error_for_missing_id(self):
        with pytest.raises(KeyError):
            self.registry.render("nonexistent", {})

    def test_render_delegate_records_missing_vars(self):
        self._register(
            "r2",
            body="{x}",
            variables=[_make_var("x")],
        )
        result = self.registry.render("r2", {})
        assert "x" in result.missing_vars

    def test_render_delegate_returns_render_result(self):
        self._register("r3", body="static")
        result = self.registry.render("r3", {})
        assert isinstance(result, RenderResult)

    # -- edge cases ----------------------------------------------------------

    def test_empty_context_with_optional_vars(self):
        t = _make_tmpl(
            template_id="ec1",
            body="{a}!",
            variables=[_make_var("a", required=False, default="world")],
        )
        self.registry.register(t)
        result = self.registry.render("ec1", {})
        assert result.body == "world!"
        assert result.is_complete()

    def test_template_with_no_vars_renders_static(self):
        t = _make_tmpl(template_id="ec2", body="No placeholders here.")
        self.registry.register(t)
        result = self.registry.render("ec2", {"extra": "ignored"})
        assert result.body == "No placeholders here."
        assert result.is_complete()

    def test_all_vars_provided_is_complete(self):
        t = _make_tmpl(
            template_id="ec3",
            body="{p} {q}",
            variables=[_make_var("p"), _make_var("q")],
        )
        self.registry.register(t)
        result = self.registry.render("ec3", {"p": "hello", "q": "world"})
        assert result.is_complete()
        assert result.body == "hello world"
