"""Tests for docstoolkit.template_engine — target: >= 85 tests."""
from __future__ import annotations

import copy

import pytest

from docstoolkit.template_engine import Template, TemplateEngine, TemplateError


# ===========================================================================
# Helpers
# ===========================================================================

def make_engine(strict: bool = True) -> TemplateEngine:
    return TemplateEngine(strict=strict)


def render(source: str, ctx: dict, strict: bool = True) -> str:
    return make_engine(strict).render_string(source, ctx)


# ===========================================================================
# Variable substitution — simple
# ===========================================================================

class TestVariableSubstitution:
    def test_single_variable(self):
        assert render("Hello {{ name }}!", {"name": "World"}) == "Hello World!"

    def test_variable_at_start(self):
        assert render("{{ greeting }} there", {"greeting": "Hi"}) == "Hi there"

    def test_variable_at_end(self):
        assert render("Hello {{ name }}", {"name": "Bob"}) == "Hello Bob"

    def test_multiple_variables_same_line(self):
        result = render("{{ a }} + {{ b }}", {"a": "1", "b": "2"})
        assert result == "1 + 2"

    def test_variable_surrounded_by_text(self):
        assert render("x{{ y }}z", {"y": "!"}) == "x!z"

    def test_integer_value(self):
        assert render("Count: {{ n }}", {"n": 42}) == "Count: 42"

    def test_float_value(self):
        assert render("Pi: {{ pi }}", {"pi": 3.14}) == "Pi: 3.14"

    def test_bool_true_value(self):
        assert render("{{ flag }}", {"flag": True}) == "True"

    def test_bool_false_value(self):
        assert render("{{ flag }}", {"flag": False}) == "False"

    def test_zero_integer(self):
        assert render("{{ n }}", {"n": 0}) == "0"

    def test_empty_string_value(self):
        assert render("{{ v }}", {"v": ""}) == ""

    def test_whitespace_around_var_name(self):
        assert render("{{  name  }}", {"name": "x"}) == "x"

    def test_no_variables_returns_source(self):
        assert render("no vars here", {}) == "no vars here"


# ===========================================================================
# Variable substitution — missing variable
# ===========================================================================

class TestMissingVariable:
    def test_missing_strict_raises(self):
        with pytest.raises(TemplateError, match="Undefined variable"):
            render("{{ missing }}", {}, strict=True)

    def test_missing_non_strict_empty(self):
        assert render("{{ missing }}", {}, strict=False) == ""

    def test_missing_non_strict_partial(self):
        result = render("{{ a }} {{ b }}", {"a": "hi"}, strict=False)
        assert result == "hi "

    def test_missing_strict_error_contains_name(self):
        with pytest.raises(TemplateError, match="nope"):
            render("{{ nope }}", {}, strict=True)


# ===========================================================================
# Dot notation
# ===========================================================================

class TestDotNotation:
    def test_simple_dot(self):
        assert render("{{ user.name }}", {"user": {"name": "Alice"}}) == "Alice"

    def test_two_levels(self):
        ctx = {"a": {"b": {"c": "deep"}}}
        assert render("{{ a.b.c }}", ctx) == "deep"

    def test_dot_on_missing_key_strict(self):
        with pytest.raises(TemplateError):
            render("{{ user.age }}", {"user": {"name": "Alice"}}, strict=True)

    def test_dot_on_missing_key_non_strict(self):
        result = render("{{ user.age }}", {"user": {"name": "Alice"}}, strict=False)
        assert result == ""

    def test_dot_on_non_dict_strict(self):
        with pytest.raises(TemplateError):
            render("{{ x.y }}", {"x": 42}, strict=True)

    def test_dot_on_non_dict_non_strict(self):
        assert render("{{ x.y }}", {"x": 42}, strict=False) == ""


# ===========================================================================
# Comments
# ===========================================================================

class TestComments:
    def test_comment_removed(self):
        assert render("{# this is a comment #}", {}) == ""

    def test_comment_inline(self):
        result = render("Hello {# hi #} World", {})
        assert result == "Hello  World"

    def test_multiple_comments(self):
        result = render("{# a #}x{# b #}", {})
        assert result == "x"

    def test_comment_does_not_affect_vars(self):
        result = render("{# ignore #}{{ v }}", {"v": "ok"})
        assert result == "ok"


# ===========================================================================
# Conditionals — if / endif
# ===========================================================================

class TestConditionalIfEndif:
    def test_true_condition_shows_block(self):
        tmpl = "{% if show %}\nvisible\n{% endif %}"
        assert "visible" in render(tmpl, {"show": True})

    def test_false_condition_hides_block(self):
        tmpl = "{% if show %}\nvisible\n{% endif %}"
        assert "visible" not in render(tmpl, {"show": False})

    def test_empty_string_is_falsy(self):
        tmpl = "{% if val %}\nyes\n{% endif %}"
        assert "yes" not in render(tmpl, {"val": ""})

    def test_zero_is_falsy(self):
        tmpl = "{% if n %}\nyes\n{% endif %}"
        assert "yes" not in render(tmpl, {"n": 0})

    def test_nonempty_string_is_truthy(self):
        tmpl = "{% if val %}\nyes\n{% endif %}"
        assert "yes" in render(tmpl, {"val": "something"})

    def test_nonzero_int_is_truthy(self):
        tmpl = "{% if n %}\nyes\n{% endif %}"
        assert "yes" in render(tmpl, {"n": 1})

    def test_list_truthy(self):
        tmpl = "{% if items %}\nhas items\n{% endif %}"
        assert "has items" in render(tmpl, {"items": ["a"]})

    def test_empty_list_falsy(self):
        tmpl = "{% if items %}\nhas items\n{% endif %}"
        assert "has items" not in render(tmpl, {"items": []})

    def test_content_before_if(self):
        tmpl = "before\n{% if show %}\ninside\n{% endif %}"
        result = render(tmpl, {"show": True})
        assert result.startswith("before")
        assert "inside" in result

    def test_content_after_endif(self):
        tmpl = "{% if show %}\ninside\n{% endif %}\nafter"
        result = render(tmpl, {"show": True})
        assert result.endswith("after")


# ===========================================================================
# Conditionals — if / else / endif
# ===========================================================================

class TestConditionalIfElse:
    def test_true_shows_if_branch(self):
        tmpl = "{% if flag %}\nyes\n{% else %}\nno\n{% endif %}"
        result = render(tmpl, {"flag": True})
        assert "yes" in result
        assert "no" not in result

    def test_false_shows_else_branch(self):
        tmpl = "{% if flag %}\nyes\n{% else %}\nno\n{% endif %}"
        result = render(tmpl, {"flag": False})
        assert "no" in result
        assert "yes" not in result

    def test_else_with_variable(self):
        tmpl = "{% if flag %}\n{{ a }}\n{% else %}\n{{ b }}\n{% endif %}"
        result = render(tmpl, {"flag": False, "a": "A", "b": "B"})
        assert "B" in result
        assert "A" not in result


# ===========================================================================
# Nested conditionals
# ===========================================================================

class TestNestedConditionals:
    def test_nested_both_true(self):
        tmpl = (
            "{% if outer %}\n"
            "{% if inner %}\n"
            "deep\n"
            "{% endif %}\n"
            "{% endif %}"
        )
        assert "deep" in render(tmpl, {"outer": True, "inner": True})

    def test_nested_outer_false(self):
        tmpl = (
            "{% if outer %}\n"
            "{% if inner %}\n"
            "deep\n"
            "{% endif %}\n"
            "{% endif %}"
        )
        assert "deep" not in render(tmpl, {"outer": False, "inner": True})

    def test_nested_inner_false(self):
        tmpl = (
            "{% if outer %}\n"
            "outer content\n"
            "{% if inner %}\n"
            "deep\n"
            "{% endif %}\n"
            "{% endif %}"
        )
        result = render(tmpl, {"outer": True, "inner": False})
        assert "outer content" in result
        assert "deep" not in result

    def test_nested_with_else(self):
        tmpl = (
            "{% if a %}\n"
            "{% if b %}\nAB\n{% else %}\nA\n{% endif %}\n"
            "{% else %}\n"
            "none\n"
            "{% endif %}"
        )
        assert "AB" in render(tmpl, {"a": True, "b": True})
        assert "A" in render(tmpl, {"a": True, "b": False})
        assert "none" in render(tmpl, {"a": False, "b": False})


# ===========================================================================
# For loops
# ===========================================================================

class TestForLoop:
    def test_basic_loop(self):
        tmpl = "{% for item in items %}\n{{ item }}\n{% endfor %}"
        result = render(tmpl, {"items": ["a", "b", "c"]})
        assert "a" in result
        assert "b" in result
        assert "c" in result

    def test_empty_list_no_output(self):
        tmpl = "{% for item in items %}\n{{ item }}\n{% endfor %}"
        result = render(tmpl, {"items": []})
        assert result == ""

    def test_single_item(self):
        tmpl = "{% for x in xs %}\n{{ x }}\n{% endfor %}"
        result = render(tmpl, {"xs": ["only"]})
        assert "only" in result

    def test_loop_order_preserved(self):
        tmpl = "{% for n in nums %}\n{{ n }}\n{% endfor %}"
        result = render(tmpl, {"nums": [1, 2, 3]})
        idx1 = result.index("1")
        idx2 = result.index("2")
        idx3 = result.index("3")
        assert idx1 < idx2 < idx3

    def test_loop_dict_items(self):
        tmpl = "{% for p in people %}\n{{ p.name }}\n{% endfor %}"
        people = [{"name": "Alice"}, {"name": "Bob"}]
        result = render(tmpl, {"people": people})
        assert "Alice" in result
        assert "Bob" in result

    def test_loop_dict_multiple_fields(self):
        tmpl = "{% for p in people %}\n{{ p.name }}: {{ p.age }}\n{% endfor %}"
        people = [{"name": "Alice", "age": 30}]
        result = render(tmpl, {"people": people})
        assert "Alice: 30" in result

    def test_loop_with_surrounding_text(self):
        tmpl = "start\n{% for x in xs %}\n{{ x }}\n{% endfor %}\nend"
        result = render(tmpl, {"xs": ["m"]})
        assert result.startswith("start")
        assert result.strip().endswith("end")

    def test_loop_integers(self):
        tmpl = "{% for n in nums %}\n{{ n }}\n{% endfor %}"
        result = render(tmpl, {"nums": [10, 20]})
        assert "10" in result
        assert "20" in result


# ===========================================================================
# Nested loops and conditionals
# ===========================================================================

class TestNestedLoopAndConditional:
    def test_conditional_inside_loop(self):
        tmpl = (
            "{% for item in items %}\n"
            "{% if item.active %}\n"
            "{{ item.name }}\n"
            "{% endif %}\n"
            "{% endfor %}"
        )
        items = [
            {"name": "Alpha", "active": True},
            {"name": "Beta", "active": False},
            {"name": "Gamma", "active": True},
        ]
        result = render(tmpl, {"items": items})
        assert "Alpha" in result
        assert "Beta" not in result
        assert "Gamma" in result

    def test_loop_inside_conditional(self):
        tmpl = (
            "{% if show %}\n"
            "{% for x in xs %}\n"
            "{{ x }}\n"
            "{% endfor %}\n"
            "{% endif %}"
        )
        result = render(tmpl, {"show": True, "xs": ["p", "q"]})
        assert "p" in result
        assert "q" in result

    def test_loop_inside_conditional_false(self):
        tmpl = (
            "{% if show %}\n"
            "{% for x in xs %}\n"
            "{{ x }}\n"
            "{% endfor %}\n"
            "{% endif %}"
        )
        result = render(tmpl, {"show": False, "xs": ["p", "q"]})
        assert "p" not in result
        assert "q" not in result


# ===========================================================================
# register / render by name
# ===========================================================================

class TestRegisterAndRender:
    def test_register_and_render(self):
        engine = make_engine()
        engine.register(Template("greet", "Hello {{ name }}!"))
        assert engine.render("greet", {"name": "Alice"}) == "Hello Alice!"

    def test_render_unknown_raises(self):
        engine = make_engine()
        with pytest.raises(TemplateError, match="not registered"):
            engine.render("ghost", {})

    def test_register_multiple(self):
        engine = make_engine()
        engine.register(Template("t1", "{{ a }}"))
        engine.register(Template("t2", "{{ b }}"))
        assert engine.render("t1", {"a": "A"}) == "A"
        assert engine.render("t2", {"b": "B"}) == "B"

    def test_register_overwrites(self):
        engine = make_engine()
        engine.register(Template("t", "old"))
        engine.register(Template("t", "new"))
        assert engine.render("t", {}) == "new"


# ===========================================================================
# registered() list
# ===========================================================================

class TestRegisteredList:
    def test_empty_initially(self):
        assert make_engine().registered() == []

    def test_single_registered(self):
        engine = make_engine()
        engine.register(Template("foo", ""))
        assert engine.registered() == ["foo"]

    def test_multiple_registered(self):
        engine = make_engine()
        engine.register(Template("a", ""))
        engine.register(Template("b", ""))
        assert set(engine.registered()) == {"a", "b"}

    def test_overwrite_does_not_duplicate(self):
        engine = make_engine()
        engine.register(Template("t", "v1"))
        engine.register(Template("t", "v2"))
        assert engine.registered().count("t") == 1


# ===========================================================================
# render_string
# ===========================================================================

class TestRenderString:
    def test_render_string_basic(self):
        engine = make_engine()
        assert engine.render_string("{{ x }}", {"x": "ok"}) == "ok"

    def test_render_string_strict_missing(self):
        engine = make_engine(strict=True)
        with pytest.raises(TemplateError):
            engine.render_string("{{ gone }}", {})

    def test_render_string_non_strict_missing(self):
        engine = make_engine(strict=False)
        assert engine.render_string("{{ gone }}", {}) == ""


# ===========================================================================
# Context immutability
# ===========================================================================

class TestContextNotModified:
    def test_loop_does_not_pollute_outer_context(self):
        engine = make_engine()
        ctx = {"items": [1, 2, 3]}
        original = copy.deepcopy(ctx)
        engine.render_string(
            "{% for item in items %}\n{{ item }}\n{% endfor %}", ctx
        )
        assert ctx == original

    def test_conditional_does_not_pollute_context(self):
        ctx = {"flag": True, "val": "hi"}
        original = copy.deepcopy(ctx)
        render("{% if flag %}\n{{ val }}\n{% endif %}", ctx)
        assert ctx == original


# ===========================================================================
# Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_empty_template(self):
        assert render("", {}) == ""

    def test_template_with_only_whitespace(self):
        result = render("   ", {})
        assert result == "   "

    def test_multiple_variables_different_lines(self):
        tmpl = "{{ a }}\n{{ b }}"
        result = render(tmpl, {"a": "line1", "b": "line2"})
        assert "line1" in result
        assert "line2" in result

    def test_whitespace_preserved_around_if_block(self):
        tmpl = "before\n{% if flag %}\ncontent\n{% endif %}\nafter"
        result = render(tmpl, {"flag": True})
        assert "before" in result
        assert "content" in result
        assert "after" in result

    def test_whitespace_preserved_around_for_block(self):
        tmpl = "before\n{% for x in xs %}\n{{ x }}\n{% endfor %}\nafter"
        result = render(tmpl, {"xs": ["m"]})
        assert "before" in result
        assert "m" in result
        assert "after" in result

    def test_template_dataclass_fields(self):
        t = Template(name="t", source="src")
        assert t.name == "t"
        assert t.source == "src"

    def test_template_error_is_exception(self):
        assert issubclass(TemplateError, Exception)

    def test_strict_default_is_true(self):
        engine = TemplateEngine()
        with pytest.raises(TemplateError):
            engine.render_string("{{ missing }}", {})

    def test_non_strict_engine_does_not_raise(self):
        engine = TemplateEngine(strict=False)
        result = engine.render_string("{{ missing }}", {})
        assert result == ""

    def test_variable_in_loop_body_with_outer_context(self):
        """Loop body can still access outer context variables."""
        tmpl = "{% for x in xs %}\n{{ prefix }}{{ x }}\n{% endfor %}"
        result = render(tmpl, {"xs": ["a", "b"], "prefix": "- "})
        assert "- a" in result
        assert "- b" in result

    def test_comment_multiline_not_present(self):
        # Comments are inline only (no multiline by design in this engine)
        result = render("a{# c #}b", {})
        assert result == "ab"

    def test_loop_with_missing_iterable_strict(self):
        with pytest.raises(TemplateError):
            render("{% for x in missing %}\n{{ x }}\n{% endfor %}", {}, strict=True)

    def test_loop_with_missing_iterable_non_strict(self):
        result = render(
            "{% for x in missing %}\n{{ x }}\n{% endfor %}", {}, strict=False
        )
        assert result == ""

    def test_none_value_renders_none_string(self):
        assert render("{{ v }}", {"v": None}) == "None"

    def test_list_value_renders_str(self):
        result = render("{{ v }}", {"v": [1, 2, 3]})
        assert result == "[1, 2, 3]"

    def test_multiple_if_blocks_independent(self):
        tmpl = (
            "{% if a %}\nA\n{% endif %}\n"
            "{% if b %}\nB\n{% endif %}"
        )
        result = render(tmpl, {"a": True, "b": False})
        assert "A" in result
        assert "B" not in result

    def test_if_missing_condition_strict(self):
        tmpl = "{% if no_such_var %}\ncontent\n{% endif %}"
        with pytest.raises(TemplateError):
            render(tmpl, {}, strict=True)

    def test_if_missing_condition_non_strict(self):
        tmpl = "{% if no_such_var %}\ncontent\n{% endif %}"
        result = render(tmpl, {}, strict=False)
        assert "content" not in result
