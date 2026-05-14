"""Tests for docstoolkit.doc_layout."""
from __future__ import annotations

import pytest

from docstoolkit.doc_layout import (
    DocLayout,
    Layout,
    LayoutSlot,
    RenderError,
    RenderOutput,
)


class TestLayoutSlot:
    def test_basic(self):
        slot = LayoutSlot(name="title")
        assert slot.name == "title"
        assert slot.default == ""
        assert slot.required is False
        assert slot.multi is False

    def test_with_default(self):
        slot = LayoutSlot(name="footer", default="(c) 2026")
        assert slot.default == "(c) 2026"

    def test_required_slot(self):
        slot = LayoutSlot(name="body", required=True)
        assert slot.required is True

    def test_multi_slot(self):
        slot = LayoutSlot(name="items", multi=True)
        assert slot.multi is True


class TestLayout:
    def test_basic(self):
        layout = Layout(name="simple", template="Hello {{name}}")
        assert layout.name == "simple"
        assert layout.template == "Hello {{name}}"
        assert layout.slots == []
        assert layout.extends is None

    def test_with_slots(self):
        slot = LayoutSlot(name="name")
        layout = Layout(name="simple", template="Hello {{name}}", slots=[slot])
        assert len(layout.slots) == 1

    def test_extends(self):
        layout = Layout(name="child", template="x", extends="parent")
        assert layout.extends == "parent"


class TestRenderError:
    def test_basic(self):
        err = RenderError(slot_name="body", error="missing")
        assert err.slot_name == "body"
        assert err.error == "missing"


class TestRenderOutput:
    def test_default(self):
        output = RenderOutput(text="hello")
        assert output.text == "hello"
        assert output.errors == []
        assert output.success is True
        assert output.unfilled_slots == []

    def test_with_errors(self):
        output = RenderOutput(
            text="",
            errors=[RenderError(slot_name="x", error="missing")],
            success=False,
            unfilled_slots=["x"],
        )
        assert output.success is False
        assert len(output.errors) == 1


class TestRegisterLayout:
    def test_register(self):
        dl = DocLayout()
        layout = dl.register_layout("page", "Body: {{body}}")
        assert layout.name == "page"
        assert dl.total_layouts == 1

    def test_register_with_slots(self):
        dl = DocLayout()
        layout = dl.register_layout(
            "page", "{{body}}", slots=[LayoutSlot(name="body", required=True)]
        )
        assert len(layout.slots) == 1

    def test_register_overwrites(self):
        dl = DocLayout()
        dl.register_layout("page", "v1")
        dl.register_layout("page", "v2")
        assert dl.get_layout("page").template == "v2"

    def test_register_with_extends(self):
        dl = DocLayout()
        dl.register_layout("base", "base")
        layout = dl.register_layout("child", "child", extends="base")
        assert layout.extends == "base"


class TestUnregisterLayout:
    def test_unregister(self):
        dl = DocLayout()
        dl.register_layout("page", "x")
        assert dl.unregister_layout("page") is True
        assert dl.total_layouts == 0

    def test_unregister_missing(self):
        dl = DocLayout()
        assert dl.unregister_layout("missing") is False


class TestGetLayout:
    def test_get(self):
        dl = DocLayout()
        dl.register_layout("page", "x")
        assert dl.get_layout("page") is not None

    def test_get_missing(self):
        dl = DocLayout()
        assert dl.get_layout("missing") is None


class TestRenderBasic:
    def test_no_slots(self):
        dl = DocLayout()
        dl.register_layout("page", "Hello World")
        out = dl.render("page")
        assert out.text == "Hello World"
        assert out.success is True

    def test_missing_layout(self):
        dl = DocLayout()
        out = dl.render("missing")
        assert out.success is False
        assert len(out.errors) == 1


class TestRenderWithSlots:
    def test_single_slot(self):
        dl = DocLayout()
        dl.register_layout("page", "Hello {{name}}")
        out = dl.render("page", {"name": "World"})
        assert out.text == "Hello World"

    def test_multiple_slots(self):
        dl = DocLayout()
        dl.register_layout("page", "{{a}} - {{b}}")
        out = dl.render("page", {"a": "x", "b": "y"})
        assert out.text == "x - y"

    def test_repeated_slot(self):
        dl = DocLayout()
        dl.register_layout("page", "{{a}}-{{a}}")
        out = dl.render("page", {"a": "X"})
        assert out.text == "X-X"

    def test_integer_value_converted(self):
        dl = DocLayout()
        dl.register_layout("page", "Count: {{n}}")
        out = dl.render("page", {"n": 42})
        assert out.text == "Count: 42"


class TestRenderDefault:
    def test_inline_default(self):
        dl = DocLayout()
        dl.register_layout("page", "Hi {{name | Guest}}")
        out = dl.render("page")
        assert out.text == "Hi Guest"

    def test_inline_default_overridden(self):
        dl = DocLayout()
        dl.register_layout("page", "Hi {{name | Guest}}")
        out = dl.render("page", {"name": "Alice"})
        assert out.text == "Hi Alice"

    def test_slot_definition_default(self):
        dl = DocLayout()
        dl.register_layout(
            "page", "Hi {{name}}", slots=[LayoutSlot(name="name", default="Anon")]
        )
        out = dl.render("page")
        assert out.text == "Hi Anon"

    def test_slot_default_overridden_by_content(self):
        dl = DocLayout()
        dl.register_layout(
            "page", "Hi {{name}}", slots=[LayoutSlot(name="name", default="Anon")]
        )
        out = dl.render("page", {"name": "Bob"})
        assert out.text == "Hi Bob"


class TestRenderRequiredMissing:
    def test_required_strict_fails(self):
        dl = DocLayout()
        dl.register_layout(
            "page", "{{body}}", slots=[LayoutSlot(name="body", required=True)]
        )
        out = dl.render("page", strict=True)
        assert out.success is False
        assert any(err.slot_name == "body" for err in out.errors)

    def test_required_non_strict_ok(self):
        dl = DocLayout()
        dl.register_layout(
            "page", "{{body}}", slots=[LayoutSlot(name="body", required=True)]
        )
        out = dl.render("page")
        # body is missing, but strict=False — still considered unfilled
        assert "body" in out.unfilled_slots

    def test_required_filled(self):
        dl = DocLayout()
        dl.register_layout(
            "page", "{{body}}", slots=[LayoutSlot(name="body", required=True)]
        )
        out = dl.render("page", {"body": "text"}, strict=True)
        assert out.success is True


class TestRenderUnfilled:
    def test_unfilled_listed(self):
        dl = DocLayout()
        dl.register_layout("page", "{{a}} {{b}}")
        out = dl.render("page", {"a": "x"})
        assert "b" in out.unfilled_slots
        assert "a" not in out.unfilled_slots

    def test_no_unfilled(self):
        dl = DocLayout()
        dl.register_layout("page", "{{a}}")
        out = dl.render("page", {"a": "x"})
        assert out.unfilled_slots == []

    def test_strict_unfilled_fails(self):
        dl = DocLayout()
        dl.register_layout("page", "{{a}}")
        out = dl.render("page", strict=True)
        assert out.success is False


class TestRenderMultiSlot:
    def test_multi_with_list(self):
        dl = DocLayout()
        dl.register_layout("page", "{{#items}}- {{.}}\n{{/items}}")
        out = dl.render("page", {"items": ["a", "b", "c"]})
        assert "- a" in out.text
        assert "- b" in out.text
        assert "- c" in out.text

    def test_multi_with_dicts(self):
        dl = DocLayout()
        dl.register_layout("page", "{{#users}}[{{name}}:{{age}}]{{/users}}")
        out = dl.render(
            "page",
            {"users": [{"name": "A", "age": "1"}, {"name": "B", "age": "2"}]},
        )
        assert "[A:1]" in out.text
        assert "[B:2]" in out.text

    def test_multi_empty(self):
        dl = DocLayout()
        dl.register_layout("page", "Items:{{#items}}- {{.}}\n{{/items}}END")
        out = dl.render("page", {"items": []})
        assert "Items:" in out.text
        assert "END" in out.text

    def test_multi_missing_unfilled(self):
        dl = DocLayout()
        dl.register_layout("page", "{{#items}}{{.}}{{/items}}")
        out = dl.render("page")
        assert "items" in out.unfilled_slots

    def test_multi_single_value_promoted(self):
        dl = DocLayout()
        dl.register_layout("page", "{{#items}}- {{.}}\n{{/items}}")
        out = dl.render("page", {"items": "solo"})
        assert "- solo" in out.text


class TestExtractSlots:
    def test_basic(self):
        dl = DocLayout()
        slots = dl.extract_slots("Hello {{name}}, you are {{age}}")
        assert slots == ["name", "age"]

    def test_with_default(self):
        dl = DocLayout()
        slots = dl.extract_slots("Hi {{name | Guest}}")
        assert slots == ["name"]

    def test_dedupe(self):
        dl = DocLayout()
        slots = dl.extract_slots("{{a}} {{a}} {{b}}")
        assert slots == ["a", "b"]

    def test_multi_blocks(self):
        dl = DocLayout()
        slots = dl.extract_slots("{{#items}}{{.}}{{/items}} {{title}}")
        assert "items" in slots
        assert "title" in slots

    def test_no_slots(self):
        dl = DocLayout()
        assert dl.extract_slots("plain text") == []


class TestValidateLayout:
    def test_valid(self):
        layout = Layout(name="x", template="Hello {{name}}", slots=[LayoutSlot(name="name")])
        ok, errs = DocLayout().validate_layout(layout)
        assert ok is True
        assert errs == []

    def test_no_name(self):
        layout = Layout(name="", template="x")
        ok, errs = DocLayout().validate_layout(layout)
        assert ok is False

    def test_duplicate_slot(self):
        layout = Layout(
            name="x",
            template="{{a}}",
            slots=[LayoutSlot(name="a"), LayoutSlot(name="a")],
        )
        ok, errs = DocLayout().validate_layout(layout)
        assert ok is False

    def test_unbalanced_multi(self):
        layout = Layout(name="x", template="{{#a}}body")
        ok, errs = DocLayout().validate_layout(layout)
        assert ok is False


class TestResolveInheritance:
    def test_no_parent(self):
        dl = DocLayout()
        dl.register_layout("page", "x", slots=[LayoutSlot(name="a")])
        resolved = dl.resolve_inheritance("page")
        assert resolved is not None
        assert resolved.template == "x"
        assert len(resolved.slots) == 1

    def test_with_parent(self):
        dl = DocLayout()
        dl.register_layout(
            "base", "BASE: {{body}}", slots=[LayoutSlot(name="body", default="empty")]
        )
        dl.register_layout(
            "child",
            "CHILD: {{body}} {{extra}}",
            slots=[LayoutSlot(name="extra")],
            extends="base",
        )
        resolved = dl.resolve_inheritance("child")
        assert resolved is not None
        # Child template wins
        assert "CHILD" in resolved.template
        # Merged slots include parent + child
        slot_names = {slot.name for slot in resolved.slots}
        assert "body" in slot_names
        assert "extra" in slot_names

    def test_child_overrides_slot(self):
        dl = DocLayout()
        dl.register_layout(
            "base", "x", slots=[LayoutSlot(name="a", default="parent")]
        )
        dl.register_layout(
            "child", "x", slots=[LayoutSlot(name="a", default="child")], extends="base"
        )
        resolved = dl.resolve_inheritance("child")
        slot_a = next(slot for slot in resolved.slots if slot.name == "a")
        assert slot_a.default == "child"

    def test_missing(self):
        dl = DocLayout()
        assert dl.resolve_inheritance("missing") is None

    def test_cycle_detection(self):
        dl = DocLayout()
        dl.register_layout("a", "A", extends="b")
        dl.register_layout("b", "B", extends="a")
        # Should not infinite loop
        resolved = dl.resolve_inheritance("a")
        assert resolved is not None

    def test_three_level_chain(self):
        dl = DocLayout()
        dl.register_layout("g", "G", slots=[LayoutSlot(name="g")])
        dl.register_layout("p", "P", slots=[LayoutSlot(name="p")], extends="g")
        dl.register_layout("c", "C", slots=[LayoutSlot(name="c")], extends="p")
        resolved = dl.resolve_inheritance("c")
        slot_names = {slot.name for slot in resolved.slots}
        assert {"g", "p", "c"}.issubset(slot_names)


class TestListLayouts:
    def test_empty(self):
        dl = DocLayout()
        assert dl.list_layouts() == []

    def test_multiple(self):
        dl = DocLayout()
        dl.register_layout("a", "x")
        dl.register_layout("b", "y")
        assert len(dl.list_layouts()) == 2


class TestLayoutsExtending:
    def test_none(self):
        dl = DocLayout()
        dl.register_layout("a", "x")
        assert dl.layouts_extending("a") == []

    def test_some(self):
        dl = DocLayout()
        dl.register_layout("base", "x")
        dl.register_layout("c1", "y", extends="base")
        dl.register_layout("c2", "z", extends="base")
        dl.register_layout("other", "q")
        found = dl.layouts_extending("base")
        assert len(found) == 2
        assert {layout.name for layout in found} == {"c1", "c2"}


class TestSetDefaultSlot:
    def test_update_existing(self):
        dl = DocLayout()
        dl.register_layout("page", "{{a}}", slots=[LayoutSlot(name="a", default="old")])
        assert dl.set_default_slot("page", "a", "new") is True
        layout = dl.get_layout("page")
        slot = next(s for s in layout.slots if s.name == "a")
        assert slot.default == "new"

    def test_add_new_slot(self):
        dl = DocLayout()
        dl.register_layout("page", "{{a}}")
        assert dl.set_default_slot("page", "a", "default") is True
        layout = dl.get_layout("page")
        assert any(s.name == "a" and s.default == "default" for s in layout.slots)

    def test_missing_layout(self):
        dl = DocLayout()
        assert dl.set_default_slot("missing", "a", "x") is False


class TestTotalLayouts:
    def test_zero(self):
        assert DocLayout().total_layouts == 0

    def test_grows(self):
        dl = DocLayout()
        dl.register_layout("a", "x")
        dl.register_layout("b", "y")
        assert dl.total_layouts == 2


class TestClear:
    def test_clear(self):
        dl = DocLayout()
        dl.register_layout("a", "x")
        dl.register_layout("b", "y")
        dl.clear()
        assert dl.total_layouts == 0

    def test_clear_empty(self):
        dl = DocLayout()
        dl.clear()
        assert dl.total_layouts == 0


class TestEdgeCases:
    def test_empty_template(self):
        dl = DocLayout()
        dl.register_layout("page", "")
        out = dl.render("page")
        assert out.text == ""
        assert out.success is True

    def test_template_no_slots(self):
        dl = DocLayout()
        dl.register_layout("page", "just static text")
        out = dl.render("page", {"a": "ignored"})
        assert out.text == "just static text"

    def test_extra_content_ignored(self):
        dl = DocLayout()
        dl.register_layout("page", "{{a}}")
        out = dl.render("page", {"a": "x", "b": "ignored"})
        assert out.text == "x"

    def test_list_value_for_single_slot(self):
        dl = DocLayout()
        dl.register_layout("page", "{{items}}")
        out = dl.render("page", {"items": ["a", "b"]})
        assert out.text == "ab"

    def test_inheritance_with_render(self):
        dl = DocLayout()
        dl.register_layout(
            "base",
            "BASE {{body}}",
            slots=[LayoutSlot(name="body", default="default-body")],
        )
        dl.register_layout(
            "child", "CHILD {{body}} {{extra}}", slots=[LayoutSlot(name="extra")], extends="base"
        )
        out = dl.render("child", {"body": "B", "extra": "E"})
        assert out.text == "CHILD B E"

    def test_inherited_default_used(self):
        dl = DocLayout()
        dl.register_layout(
            "base", "x", slots=[LayoutSlot(name="body", default="parent-default")]
        )
        dl.register_layout("child", "{{body}}", extends="base")
        out = dl.render("child")
        assert out.text == "parent-default"
