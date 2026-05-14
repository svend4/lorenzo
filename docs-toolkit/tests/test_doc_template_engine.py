"""Tests for E290 DocTemplateEngine.

Run with:
    python -m pytest tests/test_doc_template_engine.py -q
"""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_template_engine import (
    DocTemplateEngine,
    RenderResult,
    Template,
)


# ===========================================================================
# Fixtures
# ===========================================================================


@pytest.fixture
def engine() -> DocTemplateEngine:
    return DocTemplateEngine()


# ===========================================================================
# register
# ===========================================================================


class TestRegister:
    def test_register_returns_template_instance(self, engine):
        tmpl = engine.register("hello", "Hello, {{name}}!")
        assert isinstance(tmpl, Template)

    def test_register_assigns_template_id(self, engine):
        tmpl = engine.register("t", "content")
        assert tmpl.template_id.startswith("tmpl_")
        assert len(tmpl.template_id) == len("tmpl_") + 10

    def test_register_stores_name(self, engine):
        tmpl = engine.register("mytemplate", "x")
        assert tmpl.name == "mytemplate"

    def test_register_stores_content(self, engine):
        tmpl = engine.register("t", "Hello {{world}}")
        assert tmpl.content == "Hello {{world}}"

    def test_register_extracts_variables(self, engine):
        tmpl = engine.register("t", "{{a}} {{b}} {{c}}")
        assert tmpl.variables == ["a", "b", "c"]

    def test_register_variables_sorted(self, engine):
        tmpl = engine.register("t", "{{z}} {{a}} {{m}}")
        assert tmpl.variables == ["a", "m", "z"]

    def test_register_variables_deduped(self, engine):
        tmpl = engine.register("t", "{{x}} {{x}} {{x}}")
        assert tmpl.variables == ["x"]

    def test_register_no_variables(self, engine):
        tmpl = engine.register("t", "No placeholders here.")
        assert tmpl.variables == []

    def test_register_uses_provided_now(self, engine):
        ts = 1_700_000_000.0
        tmpl = engine.register("t", "x", now=ts)
        assert tmpl.created_at == ts

    def test_register_uses_current_time_if_no_now(self, engine):
        before = time.time()
        tmpl = engine.register("t", "x")
        after = time.time()
        assert before <= tmpl.created_at <= after

    def test_register_unique_ids_for_different_templates(self, engine):
        t1 = engine.register("t1", "{{a}}")
        t2 = engine.register("t2", "{{b}}")
        assert t1.template_id != t2.template_id

    def test_register_same_name_overwrites_old(self, engine):
        engine.register("same", "old content")
        t2 = engine.register("same", "new content")
        found = engine.get_by_name("same")
        assert found is not None
        assert found.content == "new content"
        assert found.template_id == t2.template_id

    def test_register_increases_total_templates(self, engine):
        engine.register("a", "x")
        engine.register("b", "y")
        assert engine.total_templates == 2


# ===========================================================================
# get
# ===========================================================================


class TestGet:
    def test_get_existing_returns_template(self, engine):
        tmpl = engine.register("t", "{{x}}")
        found = engine.get(tmpl.template_id)
        assert found is not None
        assert found.template_id == tmpl.template_id

    def test_get_nonexistent_returns_none(self, engine):
        assert engine.get("tmpl_doesnotexist") is None

    def test_get_after_delete_returns_none(self, engine):
        tmpl = engine.register("t", "x")
        engine.delete(tmpl.template_id)
        assert engine.get(tmpl.template_id) is None


# ===========================================================================
# get_by_name
# ===========================================================================


class TestGetByName:
    def test_get_by_name_existing(self, engine):
        engine.register("greeting", "Hello {{name}}")
        found = engine.get_by_name("greeting")
        assert found is not None
        assert found.name == "greeting"

    def test_get_by_name_nonexistent_returns_none(self, engine):
        assert engine.get_by_name("ghost") is None

    def test_get_by_name_after_delete_returns_none(self, engine):
        tmpl = engine.register("bye", "Goodbye")
        engine.delete(tmpl.template_id)
        assert engine.get_by_name("bye") is None

    def test_get_by_name_returns_latest_after_re_register(self, engine):
        engine.register("dup", "first")
        engine.register("dup", "second")
        found = engine.get_by_name("dup")
        assert found is not None
        assert found.content == "second"


# ===========================================================================
# update
# ===========================================================================


class TestUpdate:
    def test_update_returns_updated_template(self, engine):
        tmpl = engine.register("t", "{{a}}")
        updated = engine.update(tmpl.template_id, "{{b}} {{c}}")
        assert updated is not None
        assert updated.content == "{{b}} {{c}}"

    def test_update_re_extracts_variables(self, engine):
        tmpl = engine.register("t", "{{a}}")
        updated = engine.update(tmpl.template_id, "{{x}} {{y}}")
        assert updated is not None
        assert updated.variables == ["x", "y"]

    def test_update_preserves_template_id(self, engine):
        tmpl = engine.register("t", "{{a}}")
        updated = engine.update(tmpl.template_id, "new")
        assert updated is not None
        assert updated.template_id == tmpl.template_id

    def test_update_preserves_name(self, engine):
        tmpl = engine.register("myname", "{{a}}")
        updated = engine.update(tmpl.template_id, "updated")
        assert updated is not None
        assert updated.name == "myname"

    def test_update_preserves_created_at(self, engine):
        ts = 1_234_567_890.0
        tmpl = engine.register("t", "x", now=ts)
        updated = engine.update(tmpl.template_id, "y")
        assert updated is not None
        assert updated.created_at == ts

    def test_update_nonexistent_returns_none(self, engine):
        assert engine.update("tmpl_nothere", "content") is None

    def test_update_reflected_in_get(self, engine):
        tmpl = engine.register("t", "old")
        engine.update(tmpl.template_id, "new")
        found = engine.get(tmpl.template_id)
        assert found is not None
        assert found.content == "new"


# ===========================================================================
# delete
# ===========================================================================


class TestDelete:
    def test_delete_existing_returns_true(self, engine):
        tmpl = engine.register("t", "x")
        assert engine.delete(tmpl.template_id) is True

    def test_delete_nonexistent_returns_false(self, engine):
        assert engine.delete("tmpl_missing") is False

    def test_delete_reduces_total_templates(self, engine):
        tmpl = engine.register("t", "x")
        engine.delete(tmpl.template_id)
        assert engine.total_templates == 0

    def test_delete_removes_from_name_index(self, engine):
        tmpl = engine.register("byname", "x")
        engine.delete(tmpl.template_id)
        assert engine.get_by_name("byname") is None

    def test_double_delete_returns_false_second_time(self, engine):
        tmpl = engine.register("t", "x")
        engine.delete(tmpl.template_id)
        assert engine.delete(tmpl.template_id) is False


# ===========================================================================
# render
# ===========================================================================


class TestRender:
    def test_render_basic_substitution(self, engine):
        tmpl = engine.register("t", "Hello, {{name}}!")
        result = engine.render(tmpl.template_id, {"name": "World"})
        assert result is not None
        assert result.rendered == "Hello, World!"

    def test_render_returns_render_result_instance(self, engine):
        tmpl = engine.register("t", "{{x}}")
        result = engine.render(tmpl.template_id, {"x": "1"})
        assert isinstance(result, RenderResult)

    def test_render_template_id_in_result(self, engine):
        tmpl = engine.register("t", "{{x}}")
        result = engine.render(tmpl.template_id, {"x": "v"})
        assert result is not None
        assert result.template_id == tmpl.template_id

    def test_render_variables_used(self, engine):
        tmpl = engine.register("t", "{{a}} {{b}}")
        result = engine.render(tmpl.template_id, {"a": "1", "b": "2"})
        assert result is not None
        assert sorted(result.variables_used) == ["a", "b"]

    def test_render_missing_vars_non_strict(self, engine):
        tmpl = engine.register("t", "{{a}} {{b}}")
        result = engine.render(tmpl.template_id, {"a": "1"})
        assert result is not None
        assert result.missing_vars == ["b"]
        assert "{{b}}" in result.rendered

    def test_render_missing_var_left_in_output(self, engine):
        tmpl = engine.register("t", "{{missing}} text")
        result = engine.render(tmpl.template_id, {})
        assert result is not None
        assert result.rendered == "{{missing}} text"

    def test_render_strict_raises_on_missing(self, engine):
        tmpl = engine.register("t", "{{x}} {{y}}")
        with pytest.raises(ValueError) as exc_info:
            engine.render(tmpl.template_id, {"x": "1"}, strict=True)
        assert "y" in str(exc_info.value)

    def test_render_strict_succeeds_when_all_provided(self, engine):
        tmpl = engine.register("t", "{{x}}")
        result = engine.render(tmpl.template_id, {"x": "ok"}, strict=True)
        assert result is not None
        assert result.rendered == "ok"

    def test_render_nonexistent_template_returns_none(self, engine):
        assert engine.render("tmpl_ghost", {}) is None

    def test_render_numeric_value_converted_to_str(self, engine):
        tmpl = engine.register("t", "Count: {{n}}")
        result = engine.render(tmpl.template_id, {"n": 42})
        assert result is not None
        assert result.rendered == "Count: 42"

    def test_render_extra_variables_ignored(self, engine):
        tmpl = engine.register("t", "{{a}}")
        result = engine.render(tmpl.template_id, {"a": "x", "unused": "y"})
        assert result is not None
        assert result.rendered == "x"
        assert "unused" not in result.variables_used

    def test_render_repeated_placeholder(self, engine):
        tmpl = engine.register("t", "{{x}} and {{x}}")
        result = engine.render(tmpl.template_id, {"x": "hello"})
        assert result is not None
        assert result.rendered == "hello and hello"
        assert result.variables_used == ["x"]

    def test_render_empty_template(self, engine):
        tmpl = engine.register("t", "")
        result = engine.render(tmpl.template_id, {"a": "b"})
        assert result is not None
        assert result.rendered == ""

    def test_render_no_placeholders_unchanged(self, engine):
        tmpl = engine.register("t", "Static text only.")
        result = engine.render(tmpl.template_id, {"x": "ignored"})
        assert result is not None
        assert result.rendered == "Static text only."

    def test_render_multiline_template(self, engine):
        content = "Line1: {{a}}\nLine2: {{b}}\nLine3"
        tmpl = engine.register("t", content)
        result = engine.render(tmpl.template_id, {"a": "A", "b": "B"})
        assert result is not None
        assert result.rendered == "Line1: A\nLine2: B\nLine3"


# ===========================================================================
# render_string
# ===========================================================================


class TestRenderString:
    def test_render_string_basic(self, engine):
        result = engine.render_string("Hi {{name}}!", {"name": "Alice"})
        assert result.rendered == "Hi Alice!"

    def test_render_string_returns_render_result(self, engine):
        result = engine.render_string("{{x}}", {"x": "1"})
        assert isinstance(result, RenderResult)

    def test_render_string_template_id_empty(self, engine):
        result = engine.render_string("{{x}}", {"x": "v"})
        assert result.template_id == ""

    def test_render_string_missing_var_non_strict(self, engine):
        result = engine.render_string("{{a}} {{b}}", {"a": "1"})
        assert result.missing_vars == ["b"]
        assert "{{b}}" in result.rendered

    def test_render_string_strict_raises(self, engine):
        with pytest.raises(ValueError):
            engine.render_string("{{x}}", {}, strict=True)

    def test_render_string_strict_no_missing(self, engine):
        result = engine.render_string("{{x}}", {"x": "ok"}, strict=True)
        assert result.rendered == "ok"

    def test_render_string_does_not_register_template(self, engine):
        engine.render_string("{{x}}", {"x": "v"})
        assert engine.total_templates == 0

    def test_render_string_variables_used_populated(self, engine):
        result = engine.render_string("{{a}} {{b}}", {"a": "1", "b": "2"})
        assert sorted(result.variables_used) == ["a", "b"]

    def test_render_string_no_placeholders(self, engine):
        result = engine.render_string("plain text", {})
        assert result.rendered == "plain text"
        assert result.variables_used == []
        assert result.missing_vars == []


# ===========================================================================
# templates()
# ===========================================================================


class TestTemplates:
    def test_templates_empty(self, engine):
        assert engine.templates() == []

    def test_templates_returns_all(self, engine):
        engine.register("alpha", "{{a}}")
        engine.register("beta", "{{b}}")
        result = engine.templates()
        assert len(result) == 2

    def test_templates_sorted_by_name(self, engine):
        engine.register("zzz", "x")
        engine.register("aaa", "y")
        engine.register("mmm", "z")
        names = [t.name for t in engine.templates()]
        assert names == ["aaa", "mmm", "zzz"]

    def test_templates_excludes_deleted(self, engine):
        t1 = engine.register("keep", "x")
        t2 = engine.register("drop", "y")
        engine.delete(t2.template_id)
        result = engine.templates()
        assert len(result) == 1
        assert result[0].name == "keep"


# ===========================================================================
# find_templates_using
# ===========================================================================


class TestFindTemplatesUsing:
    def test_find_templates_using_returns_matching(self, engine):
        engine.register("t1", "{{author}} wrote {{title}}")
        engine.register("t2", "Hello {{author}}")
        engine.register("t3", "No match here")
        result = engine.find_templates_using("author")
        names = {t.name for t in result}
        assert names == {"t1", "t2"}

    def test_find_templates_using_no_match(self, engine):
        engine.register("t1", "{{x}}")
        assert engine.find_templates_using("zzz") == []

    def test_find_templates_using_empty_engine(self, engine):
        assert engine.find_templates_using("anything") == []

    def test_find_templates_using_excludes_deleted(self, engine):
        t1 = engine.register("t1", "{{var}}")
        engine.register("t2", "{{var}}")
        engine.delete(t1.template_id)
        result = engine.find_templates_using("var")
        assert len(result) == 1
        assert result[0].name == "t2"


# ===========================================================================
# total_templates
# ===========================================================================


class TestTotalTemplates:
    def test_total_templates_starts_at_zero(self, engine):
        assert engine.total_templates == 0

    def test_total_templates_increments_on_register(self, engine):
        engine.register("a", "x")
        assert engine.total_templates == 1
        engine.register("b", "y")
        assert engine.total_templates == 2

    def test_total_templates_decrements_on_delete(self, engine):
        tmpl = engine.register("a", "x")
        engine.delete(tmpl.template_id)
        assert engine.total_templates == 0

    def test_total_templates_unchanged_on_update(self, engine):
        tmpl = engine.register("a", "x")
        engine.update(tmpl.template_id, "y")
        assert engine.total_templates == 1


# ===========================================================================
# Thread safety
# ===========================================================================


class TestThreadSafety:
    def test_concurrent_register(self, engine):
        errors: list[Exception] = []

        def worker(i: int) -> None:
            try:
                engine.register(f"tmpl_{i}", f"{{{{var_{i}}}}}")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(30)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert engine.total_templates == 30

    def test_concurrent_render(self, engine):
        tmpl = engine.register("t", "Hello {{name}}!")
        errors: list[Exception] = []
        results: list[str] = []
        lock = threading.Lock()

        def worker(name: str) -> None:
            try:
                r = engine.render(tmpl.template_id, {"name": name})
                assert r is not None
                with lock:
                    results.append(r.rendered)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(f"User{i}",)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert len(results) == 20
        for rendered in results:
            assert rendered.startswith("Hello ") and rendered.endswith("!")

    def test_concurrent_delete_and_get(self, engine):
        templates = [engine.register(f"t{i}", f"{{{{x{i}}}}}") for i in range(10)]
        errors: list[Exception] = []

        def deleter(tid: str) -> None:
            try:
                engine.delete(tid)
            except Exception as exc:
                errors.append(exc)

        def getter(tid: str) -> None:
            try:
                engine.get(tid)  # may return None if already deleted
            except Exception as exc:
                errors.append(exc)

        threads = []
        for tmpl in templates:
            threads.append(threading.Thread(target=deleter, args=(tmpl.template_id,)))
            threads.append(threading.Thread(target=getter, args=(tmpl.template_id,)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
