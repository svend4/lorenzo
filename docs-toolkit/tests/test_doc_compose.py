"""Tests for the doc_compose module (E266)."""

from __future__ import annotations

import pytest

from docstoolkit.doc_compose import (
    Composition,
    DocCompose,
    Fragment,
    FragmentType,
    RenderResult,
)


# ---------------------------------------------------------------------------
# FragmentType
# ---------------------------------------------------------------------------
class TestFragmentType:
    def test_header_exists(self):
        assert FragmentType.HEADER

    def test_body_exists(self):
        assert FragmentType.BODY

    def test_footer_exists(self):
        assert FragmentType.FOOTER

    def test_sidebar_exists(self):
        assert FragmentType.SIDEBAR

    def test_nav_exists(self):
        assert FragmentType.NAV

    def test_aside_exists(self):
        assert FragmentType.ASIDE

    def test_other_exists(self):
        assert FragmentType.OTHER

    def test_values_unique(self):
        vals = {t.value for t in FragmentType}
        assert len(vals) == 7


# ---------------------------------------------------------------------------
# Fragment dataclass
# ---------------------------------------------------------------------------
class TestFragment:
    def test_minimal(self):
        f = Fragment(fragment_id="a", fragment_type=FragmentType.BODY, content="x")
        assert f.fragment_id == "a"
        assert f.fragment_type == FragmentType.BODY
        assert f.content == "x"
        assert f.name is None
        assert f.variables == {}
        assert f.created_at == 0.0

    def test_full(self):
        f = Fragment(
            fragment_id="h",
            fragment_type=FragmentType.HEADER,
            content="# ${title}",
            name="main_header",
            variables={"title": "Hello"},
            created_at=12.5,
        )
        assert f.name == "main_header"
        assert f.variables["title"] == "Hello"
        assert f.created_at == 12.5


# ---------------------------------------------------------------------------
# Composition dataclass
# ---------------------------------------------------------------------------
class TestComposition:
    def test_minimal(self):
        c = Composition(composition_id="c1", fragments=["a", "b"])
        assert c.composition_id == "c1"
        assert c.fragments == ["a", "b"]
        assert c.variables == {}
        assert c.parent is None

    def test_with_parent(self):
        c = Composition(composition_id="child", fragments=[], parent="base")
        assert c.parent == "base"

    def test_with_variables(self):
        c = Composition(composition_id="c", fragments=[], variables={"k": "v"})
        assert c.variables == {"k": "v"}


# ---------------------------------------------------------------------------
# RenderResult dataclass
# ---------------------------------------------------------------------------
class TestRenderResult:
    def test_defaults(self):
        r = RenderResult(content="hi")
        assert r.content == "hi"
        assert r.applied_fragments == []
        assert r.missing_vars == []
        assert r.errors == []
        assert r.success is True

    def test_failure(self):
        r = RenderResult(content="", errors=["x"], success=False)
        assert r.success is False
        assert r.errors == ["x"]


# ---------------------------------------------------------------------------
# register_fragment
# ---------------------------------------------------------------------------
class TestRegisterFragment:
    def test_returns_fragment(self):
        d = DocCompose()
        f = d.register_fragment("a", FragmentType.BODY, "content")
        assert isinstance(f, Fragment)
        assert f.fragment_id == "a"

    def test_stored(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "content")
        assert d.get_fragment("a") is not None

    def test_with_name(self):
        d = DocCompose()
        f = d.register_fragment("a", FragmentType.HEADER, "h", name="main")
        assert f.name == "main"

    def test_with_variables(self):
        d = DocCompose()
        f = d.register_fragment("a", FragmentType.BODY, "x", variables={"k": 1})
        assert f.variables["k"] == 1

    def test_with_timestamp(self):
        d = DocCompose()
        f = d.register_fragment("a", FragmentType.BODY, "x", now=100.0)
        assert f.created_at == 100.0


# ---------------------------------------------------------------------------
# unregister_fragment
# ---------------------------------------------------------------------------
class TestUnregisterFragment:
    def test_returns_true_when_exists(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "x")
        assert d.unregister_fragment("a") is True

    def test_returns_false_when_missing(self):
        d = DocCompose()
        assert d.unregister_fragment("nope") is False

    def test_actually_removes(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "x")
        d.unregister_fragment("a")
        assert d.get_fragment("a") is None


# ---------------------------------------------------------------------------
# get_fragment
# ---------------------------------------------------------------------------
class TestGetFragment:
    def test_returns_none_when_missing(self):
        d = DocCompose()
        assert d.get_fragment("x") is None

    def test_returns_fragment(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "x")
        f = d.get_fragment("a")
        assert f is not None and f.fragment_id == "a"


# ---------------------------------------------------------------------------
# fragments_by_type
# ---------------------------------------------------------------------------
class TestFragmentsByType:
    def test_empty(self):
        d = DocCompose()
        assert d.fragments_by_type(FragmentType.BODY) == []

    def test_filter(self):
        d = DocCompose()
        d.register_fragment("h", FragmentType.HEADER, "h")
        d.register_fragment("b", FragmentType.BODY, "b")
        d.register_fragment("f", FragmentType.FOOTER, "f")
        bodies = d.fragments_by_type(FragmentType.BODY)
        assert len(bodies) == 1
        assert bodies[0].fragment_id == "b"

    def test_multiple_same_type(self):
        d = DocCompose()
        d.register_fragment("b1", FragmentType.BODY, "x")
        d.register_fragment("b2", FragmentType.BODY, "y")
        assert len(d.fragments_by_type(FragmentType.BODY)) == 2


# ---------------------------------------------------------------------------
# find_fragment_by_name
# ---------------------------------------------------------------------------
class TestFindFragmentByName:
    def test_finds(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.HEADER, "x", name="hdr")
        f = d.find_fragment_by_name("hdr")
        assert f is not None and f.fragment_id == "a"

    def test_returns_none(self):
        d = DocCompose()
        assert d.find_fragment_by_name("nope") is None


# ---------------------------------------------------------------------------
# register_composition
# ---------------------------------------------------------------------------
class TestRegisterComposition:
    def test_basic(self):
        d = DocCompose()
        c = d.register_composition("c1", ["a", "b"])
        assert c.composition_id == "c1"
        assert c.fragments == ["a", "b"]

    def test_with_variables(self):
        d = DocCompose()
        c = d.register_composition("c1", [], variables={"t": "v"})
        assert c.variables == {"t": "v"}

    def test_with_parent(self):
        d = DocCompose()
        c = d.register_composition("child", [], parent="base")
        assert c.parent == "base"

    def test_stored(self):
        d = DocCompose()
        d.register_composition("c1", [])
        assert d.get_composition("c1") is not None


# ---------------------------------------------------------------------------
# unregister_composition
# ---------------------------------------------------------------------------
class TestUnregisterComposition:
    def test_returns_true(self):
        d = DocCompose()
        d.register_composition("c", [])
        assert d.unregister_composition("c") is True

    def test_returns_false(self):
        d = DocCompose()
        assert d.unregister_composition("c") is False

    def test_actually_removes(self):
        d = DocCompose()
        d.register_composition("c", [])
        d.unregister_composition("c")
        assert d.get_composition("c") is None


# ---------------------------------------------------------------------------
# get_composition
# ---------------------------------------------------------------------------
class TestGetComposition:
    def test_returns_none(self):
        assert DocCompose().get_composition("x") is None

    def test_returns_comp(self):
        d = DocCompose()
        d.register_composition("c", ["a"])
        c = d.get_composition("c")
        assert c is not None and c.fragments == ["a"]


# ---------------------------------------------------------------------------
# render
# ---------------------------------------------------------------------------
class TestRender:
    def test_simple(self):
        d = DocCompose()
        d.register_fragment("h", FragmentType.HEADER, "HEADER")
        d.register_fragment("b", FragmentType.BODY, "BODY")
        d.register_composition("c", ["h", "b"])
        r = d.render("c")
        assert "HEADER" in r.content
        assert "BODY" in r.content
        assert r.success is True

    def test_with_variables(self):
        d = DocCompose()
        d.register_fragment("h", FragmentType.HEADER, "Hello ${name}")
        d.register_composition("c", ["h"])
        r = d.render("c", variables={"name": "World"})
        assert r.content == "Hello World"

    def test_missing_variables_tracked(self):
        d = DocCompose()
        d.register_fragment("h", FragmentType.HEADER, "Hi ${x}")
        d.register_composition("c", ["h"])
        r = d.render("c")
        assert "x" in r.missing_vars

    def test_missing_composition(self):
        d = DocCompose()
        r = d.render("nope")
        assert r.success is False
        assert r.errors

    def test_missing_fragment(self):
        d = DocCompose()
        d.register_composition("c", ["nope"])
        r = d.render("c")
        assert r.success is False
        assert r.errors

    def test_applied_fragments(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "A")
        d.register_fragment("b", FragmentType.BODY, "B")
        d.register_composition("c", ["a", "b"])
        r = d.render("c")
        assert r.applied_fragments == ["a", "b"]

    def test_composition_vars_used(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "${k}")
        d.register_composition("c", ["a"], variables={"k": "value"})
        r = d.render("c")
        assert r.content == "value"

    def test_call_vars_override_composition_vars(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "${k}")
        d.register_composition("c", ["a"], variables={"k": "comp"})
        r = d.render("c", variables={"k": "call"})
        assert r.content == "call"


# ---------------------------------------------------------------------------
# render_fragment
# ---------------------------------------------------------------------------
class TestRenderFragment:
    def test_simple(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "Hello")
        assert d.render_fragment("a") == "Hello"

    def test_with_vars(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "Hi ${who}")
        assert d.render_fragment("a", {"who": "Bob"}) == "Hi Bob"

    def test_uses_fragment_defaults(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "Hi ${who}", variables={"who": "default"})
        assert d.render_fragment("a") == "Hi default"

    def test_missing_fragment(self):
        d = DocCompose()
        assert d.render_fragment("none") == ""


# ---------------------------------------------------------------------------
# expand_variables
# ---------------------------------------------------------------------------
class TestExpandVariables:
    def test_substitutes(self):
        d = DocCompose()
        out, missing = d.expand_variables("Hi ${x}", {"x": "Y"})
        assert out == "Hi Y"
        assert missing == []

    def test_missing_listed(self):
        d = DocCompose()
        out, missing = d.expand_variables("Hi ${x}", {})
        assert "${x}" in out
        assert "x" in missing

    def test_multiple(self):
        d = DocCompose()
        out, missing = d.expand_variables("${a}-${b}", {"a": "1", "b": "2"})
        assert out == "1-2"

    def test_no_vars(self):
        d = DocCompose()
        out, missing = d.expand_variables("plain text", {})
        assert out == "plain text"
        assert missing == []

    def test_partial(self):
        d = DocCompose()
        out, missing = d.expand_variables("${a}-${b}", {"a": "1"})
        assert "1" in out
        assert "${b}" in out
        assert missing == ["b"]


# ---------------------------------------------------------------------------
# expand_variables with default
# ---------------------------------------------------------------------------
class TestExpandVariablesDefault:
    def test_default_used(self):
        d = DocCompose()
        out, missing = d.expand_variables("${x | hello}", {})
        assert out == "hello"
        assert missing == []

    def test_default_overridden(self):
        d = DocCompose()
        out, missing = d.expand_variables("${x | hello}", {"x": "actual"})
        assert out == "actual"

    def test_default_with_spaces(self):
        d = DocCompose()
        out, _ = d.expand_variables("${x | default value}", {})
        assert out == "default value"


# ---------------------------------------------------------------------------
# extract_variables
# ---------------------------------------------------------------------------
class TestExtractVariables:
    def test_extracts(self):
        d = DocCompose()
        assert set(d.extract_variables("${a} ${b}")) == {"a", "b"}

    def test_unique(self):
        d = DocCompose()
        assert d.extract_variables("${a} ${a}") == ["a"]

    def test_with_defaults(self):
        d = DocCompose()
        names = d.extract_variables("${x | default}")
        assert names == ["x"]

    def test_none(self):
        d = DocCompose()
        assert d.extract_variables("plain") == []

    def test_ignores_includes(self):
        d = DocCompose()
        assert d.extract_variables("${include:a}") == []


# ---------------------------------------------------------------------------
# process_includes
# ---------------------------------------------------------------------------
class TestProcessIncludes:
    def test_basic(self):
        d = DocCompose()
        d.register_fragment("inner", FragmentType.BODY, "INNER")
        assert d.process_includes("before ${include:inner} after") == "before INNER after"

    def test_by_name(self):
        d = DocCompose()
        d.register_fragment("x", FragmentType.BODY, "Z", name="mybit")
        assert d.process_includes("${include:mybit}") == "Z"

    def test_missing_left_intact(self):
        d = DocCompose()
        out = d.process_includes("${include:nope}")
        assert "${include:nope}" in out

    def test_no_includes(self):
        d = DocCompose()
        assert d.process_includes("plain") == "plain"

    def test_recursive(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "A->${include:b}")
        d.register_fragment("b", FragmentType.BODY, "B")
        assert d.process_includes("${include:a}") == "A->B"

    def test_max_depth(self):
        d = DocCompose()
        # Self-include: with max_depth, should bottom out (no infinite recursion)
        d.register_fragment("a", FragmentType.BODY, "X${include:a}")
        out = d.process_includes("${include:a}", max_depth=3)
        # finite output
        assert out.count("X") <= 5
        assert isinstance(out, str)


# ---------------------------------------------------------------------------
# resolve_inheritance
# ---------------------------------------------------------------------------
class TestResolveInheritance:
    def test_no_parent(self):
        d = DocCompose()
        d.register_composition("c", ["a"])
        r = d.resolve_inheritance("c")
        assert r is not None
        assert r.fragments == ["a"]

    def test_with_parent_fragments_first(self):
        d = DocCompose()
        d.register_composition("base", ["x"])
        d.register_composition("child", ["y"], parent="base")
        r = d.resolve_inheritance("child")
        assert r.fragments == ["x", "y"]

    def test_child_vars_override(self):
        d = DocCompose()
        d.register_composition("base", [], variables={"k": "base"})
        d.register_composition("child", [], variables={"k": "child"}, parent="base")
        r = d.resolve_inheritance("child")
        assert r.variables["k"] == "child"

    def test_missing(self):
        d = DocCompose()
        assert d.resolve_inheritance("nope") is None

    def test_cycle_detected(self):
        d = DocCompose()
        d.register_composition("a", ["fa"], parent="b")
        d.register_composition("b", ["fb"], parent="a")
        # should not loop forever
        r = d.resolve_inheritance("a")
        assert r is not None

    def test_deep_chain(self):
        d = DocCompose()
        d.register_composition("root", ["r"])
        d.register_composition("mid", ["m"], parent="root")
        d.register_composition("leaf", ["l"], parent="mid")
        r = d.resolve_inheritance("leaf")
        assert r.fragments == ["r", "m", "l"]


# ---------------------------------------------------------------------------
# total_fragments
# ---------------------------------------------------------------------------
class TestTotalFragments:
    def test_empty(self):
        assert DocCompose().total_fragments == 0

    def test_after_register(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "x")
        d.register_fragment("b", FragmentType.BODY, "x")
        assert d.total_fragments == 2

    def test_after_unregister(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "x")
        d.unregister_fragment("a")
        assert d.total_fragments == 0


# ---------------------------------------------------------------------------
# total_compositions
# ---------------------------------------------------------------------------
class TestTotalCompositions:
    def test_empty(self):
        assert DocCompose().total_compositions == 0

    def test_after_register(self):
        d = DocCompose()
        d.register_composition("c", [])
        assert d.total_compositions == 1

    def test_after_unregister(self):
        d = DocCompose()
        d.register_composition("c", [])
        d.unregister_composition("c")
        assert d.total_compositions == 0


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------
class TestClear:
    def test_clears_fragments(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "x")
        d.clear()
        assert d.total_fragments == 0

    def test_clears_compositions(self):
        d = DocCompose()
        d.register_composition("c", [])
        d.clear()
        assert d.total_compositions == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_empty_composition_renders_empty(self):
        d = DocCompose()
        d.register_composition("c", [])
        r = d.render("c")
        assert r.content == ""
        assert r.success is True

    def test_render_with_includes_and_vars(self):
        d = DocCompose()
        d.register_fragment("inner", FragmentType.BODY, "INNER:${who}")
        d.register_fragment("outer", FragmentType.BODY, "[${include:inner}]")
        d.register_composition("c", ["outer"], variables={"who": "Alice"})
        r = d.render("c")
        assert r.content == "[INNER:Alice]"

    def test_overwrite_fragment(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "v1")
        d.register_fragment("a", FragmentType.BODY, "v2")
        assert d.get_fragment("a").content == "v2"
        assert d.total_fragments == 1

    def test_inheritance_then_render(self):
        d = DocCompose()
        d.register_fragment("h", FragmentType.HEADER, "H:${title}")
        d.register_fragment("b", FragmentType.BODY, "B")
        d.register_composition("base", ["h"], variables={"title": "Base"})
        d.register_composition("child", ["b"], parent="base")
        r = d.render("child")
        assert "H:Base" in r.content
        assert "B" in r.content

    def test_child_overrides_parent_var(self):
        d = DocCompose()
        d.register_fragment("h", FragmentType.HEADER, "${t}")
        d.register_composition("base", ["h"], variables={"t": "P"})
        d.register_composition("child", [], variables={"t": "C"}, parent="base")
        r = d.render("child")
        assert r.content == "C"

    def test_fragment_default_used_when_no_composition_var(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "${k}", variables={"k": "fdef"})
        d.register_composition("c", ["a"])
        r = d.render("c")
        assert r.content == "fdef"

    def test_composition_var_overrides_fragment_default(self):
        d = DocCompose()
        d.register_fragment("a", FragmentType.BODY, "${k}", variables={"k": "fdef"})
        d.register_composition("c", ["a"], variables={"k": "cdef"})
        r = d.render("c")
        assert r.content == "cdef"

    def test_render_result_is_dataclass(self):
        d = DocCompose()
        d.register_composition("c", [])
        r = d.render("c")
        assert isinstance(r, RenderResult)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
