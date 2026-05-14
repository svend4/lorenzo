"""Tests for docstoolkit.plugin_system (E69).

Covers:
- PluginMetadata and Plugin ABC
- PluginRegistry: register/unregister/get/list_all/list_by_status/list_by_tag
- PluginManager: full lifecycle, bulk ops, error handling, active_plugins
- resolve_dependencies: no deps, chain, diamond DAG, circular detection
- Lifecycle ordering constraints
- Side-effect tracking for on_load/on_unload/on_activate/on_deactivate
"""

import pytest

from docstoolkit.plugin_system import (
    Plugin,
    PluginManager,
    PluginMetadata,
    PluginRecord,
    PluginRegistry,
    PluginStatus,
)


# ---------------------------------------------------------------------------
# Helpers / concrete fixtures
# ---------------------------------------------------------------------------

class SimplePlugin(Plugin):
    """Minimal plugin with configurable metadata and side-effect tracking."""

    def __init__(
        self,
        name: str = "simple",
        version: str = "0.1.0",
        description: str = "",
        author: str = "",
        dependencies: list[str] | None = None,
        tags: list[str] | None = None,
    ) -> None:
        self._metadata = PluginMetadata(
            name=name,
            version=version,
            description=description,
            author=author,
            dependencies=dependencies or [],
            tags=tags or [],
        )
        self.calls: list[str] = []

    @property
    def metadata(self) -> PluginMetadata:
        return self._metadata

    def on_load(self) -> None:
        self.calls.append("load")

    def on_unload(self) -> None:
        self.calls.append("unload")

    def on_activate(self) -> None:
        self.calls.append("activate")

    def on_deactivate(self) -> None:
        self.calls.append("deactivate")


class ErrorOnLoadPlugin(SimplePlugin):
    """Plugin whose on_load always raises."""

    def on_load(self) -> None:
        raise RuntimeError("load failed intentionally")


class ErrorOnActivatePlugin(SimplePlugin):
    """Plugin whose on_activate always raises."""

    def on_activate(self) -> None:
        raise RuntimeError("activate failed intentionally")


# ---------------------------------------------------------------------------
# 1. PluginMetadata tests
# ---------------------------------------------------------------------------

class TestPluginMetadata:
    def test_required_name(self):
        m = PluginMetadata(name="foo")
        assert m.name == "foo"

    def test_default_version(self):
        m = PluginMetadata(name="foo")
        assert m.version == "0.1.0"

    def test_custom_version(self):
        m = PluginMetadata(name="foo", version="2.3.4")
        assert m.version == "2.3.4"

    def test_default_description_empty(self):
        m = PluginMetadata(name="foo")
        assert m.description == ""

    def test_default_author_empty(self):
        m = PluginMetadata(name="foo")
        assert m.author == ""

    def test_default_dependencies_empty_list(self):
        m = PluginMetadata(name="foo")
        assert m.dependencies == []

    def test_dependencies_not_shared(self):
        m1 = PluginMetadata(name="a")
        m2 = PluginMetadata(name="b")
        m1.dependencies.append("x")
        assert m2.dependencies == []

    def test_default_tags_empty_list(self):
        m = PluginMetadata(name="foo")
        assert m.tags == []

    def test_tags_not_shared(self):
        m1 = PluginMetadata(name="a")
        m2 = PluginMetadata(name="b")
        m1.tags.append("util")
        assert m2.tags == []

    def test_full_metadata(self):
        m = PluginMetadata(
            name="my-plugin",
            version="1.0.0",
            description="A test plugin",
            author="Alice",
            dependencies=["base-plugin"],
            tags=["util", "search"],
        )
        assert m.name == "my-plugin"
        assert m.version == "1.0.0"
        assert m.description == "A test plugin"
        assert m.author == "Alice"
        assert m.dependencies == ["base-plugin"]
        assert m.tags == ["util", "search"]


# ---------------------------------------------------------------------------
# 2. Plugin ABC tests
# ---------------------------------------------------------------------------

class TestPluginABC:
    def test_cannot_instantiate_abstract_plugin(self):
        with pytest.raises(TypeError):
            Plugin()  # type: ignore[abstract]

    def test_concrete_plugin_returns_metadata(self):
        p = SimplePlugin(name="abc")
        assert isinstance(p.metadata, PluginMetadata)
        assert p.metadata.name == "abc"

    def test_on_load_default_noop(self):
        """Plugin subclass that does NOT override on_load still works."""
        class NoOpPlugin(Plugin):
            @property
            def metadata(self):
                return PluginMetadata(name="noop")
        p = NoOpPlugin()
        # Should not raise
        p.on_load()
        p.on_unload()

    def test_on_activate_default_noop(self):
        class NoOpPlugin(Plugin):
            @property
            def metadata(self):
                return PluginMetadata(name="noop2")
        p = NoOpPlugin()
        p.on_activate()
        p.on_deactivate()

    def test_side_effects_tracked(self):
        p = SimplePlugin(name="track")
        p.on_load()
        p.on_activate()
        p.on_deactivate()
        p.on_unload()
        assert p.calls == ["load", "activate", "deactivate", "unload"]


# ---------------------------------------------------------------------------
# 3. PluginStatus enum
# ---------------------------------------------------------------------------

class TestPluginStatus:
    def test_all_statuses_exist(self):
        statuses = {s.name for s in PluginStatus}
        assert statuses == {"UNLOADED", "LOADED", "ACTIVE", "ERROR", "DISABLED"}

    def test_status_values(self):
        assert PluginStatus.UNLOADED.value == "unloaded"
        assert PluginStatus.LOADED.value == "loaded"
        assert PluginStatus.ACTIVE.value == "active"
        assert PluginStatus.ERROR.value == "error"
        assert PluginStatus.DISABLED.value == "disabled"


# ---------------------------------------------------------------------------
# 4. PluginRecord tests
# ---------------------------------------------------------------------------

class TestPluginRecord:
    def test_default_status_unloaded(self):
        p = SimplePlugin(name="r")
        rec = PluginRecord(plugin=p)
        assert rec.status == PluginStatus.UNLOADED

    def test_default_error_empty(self):
        p = SimplePlugin(name="r2")
        rec = PluginRecord(plugin=p)
        assert rec.error == ""

    def test_custom_status(self):
        p = SimplePlugin(name="r3")
        rec = PluginRecord(plugin=p, status=PluginStatus.ACTIVE)
        assert rec.status == PluginStatus.ACTIVE


# ---------------------------------------------------------------------------
# 5. PluginRegistry tests
# ---------------------------------------------------------------------------

class TestPluginRegistry:
    def setup_method(self):
        self.registry = PluginRegistry()
        self.plugin_a = SimplePlugin(name="alpha")
        self.plugin_b = SimplePlugin(name="beta", tags=["util"])
        self.plugin_c = SimplePlugin(name="gamma", tags=["util", "search"])

    def test_register_and_get(self):
        self.registry.register(self.plugin_a)
        rec = self.registry.get("alpha")
        assert rec is not None
        assert rec.plugin is self.plugin_a

    def test_initial_status_unloaded(self):
        self.registry.register(self.plugin_a)
        rec = self.registry.get("alpha")
        assert rec.status == PluginStatus.UNLOADED

    def test_register_duplicate_raises_value_error(self):
        self.registry.register(self.plugin_a)
        with pytest.raises(ValueError, match="alpha"):
            self.registry.register(SimplePlugin(name="alpha"))

    def test_get_unregistered_returns_none(self):
        assert self.registry.get("nonexistent") is None

    def test_unregister_returns_true(self):
        self.registry.register(self.plugin_a)
        assert self.registry.unregister("alpha") is True

    def test_unregister_removes_from_registry(self):
        self.registry.register(self.plugin_a)
        self.registry.unregister("alpha")
        assert self.registry.get("alpha") is None

    def test_unregister_missing_returns_false(self):
        assert self.registry.unregister("ghost") is False

    def test_list_all_empty(self):
        assert self.registry.list_all() == []

    def test_list_all_returns_all(self):
        self.registry.register(self.plugin_a)
        self.registry.register(self.plugin_b)
        records = self.registry.list_all()
        assert len(records) == 2

    def test_list_by_status_unloaded(self):
        self.registry.register(self.plugin_a)
        self.registry.register(self.plugin_b)
        result = self.registry.list_by_status(PluginStatus.UNLOADED)
        assert len(result) == 2

    def test_list_by_status_after_manual_change(self):
        self.registry.register(self.plugin_a)
        rec = self.registry.get("alpha")
        rec.status = PluginStatus.LOADED
        loaded = self.registry.list_by_status(PluginStatus.LOADED)
        assert len(loaded) == 1
        assert loaded[0].plugin is self.plugin_a

    def test_list_by_status_empty_for_unused_status(self):
        self.registry.register(self.plugin_a)
        assert self.registry.list_by_status(PluginStatus.ACTIVE) == []

    def test_list_by_tag_single_match(self):
        self.registry.register(self.plugin_a)
        self.registry.register(self.plugin_b)
        result = self.registry.list_by_tag("util")
        assert len(result) == 1
        assert result[0].plugin is self.plugin_b

    def test_list_by_tag_multiple_matches(self):
        self.registry.register(self.plugin_b)
        self.registry.register(self.plugin_c)
        result = self.registry.list_by_tag("util")
        assert len(result) == 2

    def test_list_by_tag_no_match(self):
        self.registry.register(self.plugin_a)
        assert self.registry.list_by_tag("nonexistent") == []

    def test_reregister_after_unregister(self):
        self.registry.register(self.plugin_a)
        self.registry.unregister("alpha")
        # Should not raise
        self.registry.register(SimplePlugin(name="alpha"))
        assert self.registry.get("alpha") is not None


# ---------------------------------------------------------------------------
# 6. PluginManager lifecycle tests
# ---------------------------------------------------------------------------

class TestPluginManagerLifecycle:
    def setup_method(self):
        self.mgr = PluginManager()
        self.plugin = SimplePlugin(name="p1")
        self.mgr.register(self.plugin)

    def test_load_sets_status_loaded(self):
        result = self.mgr.load("p1")
        assert result is True
        assert self.mgr.registry.get("p1").status == PluginStatus.LOADED

    def test_load_calls_on_load(self):
        self.mgr.load("p1")
        assert "load" in self.plugin.calls

    def test_load_nonexistent_returns_false(self):
        assert self.mgr.load("ghost") is False

    def test_unload_sets_status_unloaded(self):
        self.mgr.load("p1")
        self.mgr.unload("p1")
        assert self.mgr.registry.get("p1").status == PluginStatus.UNLOADED

    def test_unload_calls_on_unload(self):
        self.mgr.load("p1")
        self.mgr.unload("p1")
        assert "unload" in self.plugin.calls

    def test_unload_nonexistent_returns_false(self):
        assert self.mgr.unload("ghost") is False

    def test_activate_from_loaded_succeeds(self):
        self.mgr.load("p1")
        result = self.mgr.activate("p1")
        assert result is True
        assert self.mgr.registry.get("p1").status == PluginStatus.ACTIVE

    def test_activate_calls_on_activate(self):
        self.mgr.load("p1")
        self.mgr.activate("p1")
        assert "activate" in self.plugin.calls

    def test_activate_from_unloaded_fails(self):
        result = self.mgr.activate("p1")
        assert result is False
        assert self.mgr.registry.get("p1").status == PluginStatus.UNLOADED

    def test_activate_nonexistent_returns_false(self):
        assert self.mgr.activate("ghost") is False

    def test_deactivate_from_active_succeeds(self):
        self.mgr.load("p1")
        self.mgr.activate("p1")
        result = self.mgr.deactivate("p1")
        assert result is True
        assert self.mgr.registry.get("p1").status == PluginStatus.LOADED

    def test_deactivate_calls_on_deactivate(self):
        self.mgr.load("p1")
        self.mgr.activate("p1")
        self.mgr.deactivate("p1")
        assert "deactivate" in self.plugin.calls

    def test_deactivate_from_loaded_fails(self):
        self.mgr.load("p1")
        result = self.mgr.deactivate("p1")
        assert result is False

    def test_deactivate_from_unloaded_fails(self):
        result = self.mgr.deactivate("p1")
        assert result is False

    def test_deactivate_nonexistent_returns_false(self):
        assert self.mgr.deactivate("ghost") is False

    def test_disable_sets_status(self):
        result = self.mgr.disable("p1")
        assert result is True
        assert self.mgr.registry.get("p1").status == PluginStatus.DISABLED

    def test_disable_does_not_call_lifecycle_hooks(self):
        self.mgr.disable("p1")
        assert self.plugin.calls == []

    def test_disable_nonexistent_returns_false(self):
        assert self.mgr.disable("ghost") is False

    def test_full_lifecycle_order(self):
        self.mgr.load("p1")
        self.mgr.activate("p1")
        self.mgr.deactivate("p1")
        self.mgr.unload("p1")
        assert self.plugin.calls == ["load", "activate", "deactivate", "unload"]


# ---------------------------------------------------------------------------
# 7. Error handling during lifecycle
# ---------------------------------------------------------------------------

class TestPluginManagerErrors:
    def test_load_error_sets_error_status(self):
        mgr = PluginManager()
        p = ErrorOnLoadPlugin(name="err")
        mgr.register(p)
        result = mgr.load("err")
        assert result is False
        rec = mgr.registry.get("err")
        assert rec.status == PluginStatus.ERROR

    def test_load_error_records_message(self):
        mgr = PluginManager()
        p = ErrorOnLoadPlugin(name="err2")
        mgr.register(p)
        mgr.load("err2")
        rec = mgr.registry.get("err2")
        assert "load failed intentionally" in rec.error

    def test_error_record_clears_on_successful_reload(self):
        """After fixing the error, re-loading should clear error message."""
        mgr = PluginManager()
        p = ErrorOnLoadPlugin(name="err3")
        mgr.register(p)
        mgr.load("err3")  # fails -> ERROR

        # Patch to a working on_load by replacing the method on the instance
        p.on_load = lambda: None  # type: ignore[method-assign]
        result = mgr.load("err3")
        assert result is True
        rec = mgr.registry.get("err3")
        assert rec.status == PluginStatus.LOADED
        assert rec.error == ""


# ---------------------------------------------------------------------------
# 8. Bulk operations
# ---------------------------------------------------------------------------

class TestPluginManagerBulk:
    def test_load_all_loads_every_unloaded(self):
        mgr = PluginManager()
        mgr.register(SimplePlugin(name="a"))
        mgr.register(SimplePlugin(name="b"))
        mgr.register(SimplePlugin(name="c"))
        results = mgr.load_all()
        assert results == {"a": True, "b": True, "c": True}
        for name in ("a", "b", "c"):
            assert mgr.registry.get(name).status == PluginStatus.LOADED

    def test_load_all_skips_already_loaded(self):
        mgr = PluginManager()
        mgr.register(SimplePlugin(name="x"))
        mgr.load("x")  # already loaded
        results = mgr.load_all()
        assert results == {}  # nothing was UNLOADED

    def test_load_all_returns_false_for_errors(self):
        mgr = PluginManager()
        mgr.register(ErrorOnLoadPlugin(name="bad"))
        mgr.register(SimplePlugin(name="good"))
        results = mgr.load_all()
        assert results["bad"] is False
        assert results["good"] is True

    def test_activate_all_activates_every_loaded(self):
        mgr = PluginManager()
        mgr.register(SimplePlugin(name="a"))
        mgr.register(SimplePlugin(name="b"))
        mgr.load_all()
        results = mgr.activate_all()
        assert results == {"a": True, "b": True}
        for name in ("a", "b"):
            assert mgr.registry.get(name).status == PluginStatus.ACTIVE

    def test_activate_all_skips_unloaded(self):
        mgr = PluginManager()
        mgr.register(SimplePlugin(name="u"))
        results = mgr.activate_all()
        assert results == {}


# ---------------------------------------------------------------------------
# 9. active_plugins
# ---------------------------------------------------------------------------

class TestActivePlugins:
    def test_active_plugins_empty_initially(self):
        mgr = PluginManager()
        assert mgr.active_plugins() == []

    def test_active_plugins_after_activate(self):
        mgr = PluginManager()
        p = SimplePlugin(name="live")
        mgr.register(p)
        mgr.load("live")
        mgr.activate("live")
        assert mgr.active_plugins() == [p]

    def test_active_plugins_excludes_loaded(self):
        mgr = PluginManager()
        p = SimplePlugin(name="loaded-only")
        mgr.register(p)
        mgr.load("loaded-only")
        assert mgr.active_plugins() == []

    def test_active_plugins_excludes_deactivated(self):
        mgr = PluginManager()
        p = SimplePlugin(name="was-active")
        mgr.register(p)
        mgr.load("was-active")
        mgr.activate("was-active")
        mgr.deactivate("was-active")
        assert mgr.active_plugins() == []

    def test_active_plugins_multiple(self):
        mgr = PluginManager()
        plugins = [SimplePlugin(name=f"p{i}") for i in range(3)]
        for p in plugins:
            mgr.register(p)
            mgr.load(p.metadata.name)
            mgr.activate(p.metadata.name)
        active = mgr.active_plugins()
        assert len(active) == 3
        assert set(p.metadata.name for p in active) == {"p0", "p1", "p2"}


# ---------------------------------------------------------------------------
# 10. resolve_dependencies
# ---------------------------------------------------------------------------

class TestResolveDependencies:
    def _make_mgr(self) -> PluginManager:
        return PluginManager()

    def test_no_dependencies_returns_empty(self):
        mgr = self._make_mgr()
        mgr.register(SimplePlugin(name="standalone"))
        deps = mgr.resolve_dependencies("standalone")
        assert deps == []

    def test_single_direct_dependency(self):
        mgr = self._make_mgr()
        mgr.register(SimplePlugin(name="base"))
        mgr.register(SimplePlugin(name="app", dependencies=["base"]))
        deps = mgr.resolve_dependencies("app")
        assert deps == ["base"]

    def test_linear_chain(self):
        mgr = self._make_mgr()
        mgr.register(SimplePlugin(name="a"))
        mgr.register(SimplePlugin(name="b", dependencies=["a"]))
        mgr.register(SimplePlugin(name="c", dependencies=["b"]))
        deps = mgr.resolve_dependencies("c")
        # a must come before b
        assert deps.index("a") < deps.index("b")
        assert "c" not in deps

    def test_diamond_dag(self):
        """
        top -> left, right
        left -> base
        right -> base
        """
        mgr = self._make_mgr()
        mgr.register(SimplePlugin(name="base"))
        mgr.register(SimplePlugin(name="left", dependencies=["base"]))
        mgr.register(SimplePlugin(name="right", dependencies=["base"]))
        mgr.register(SimplePlugin(name="top", dependencies=["left", "right"]))
        deps = mgr.resolve_dependencies("top")
        # base must appear exactly once
        assert deps.count("base") == 1
        # base before left and right
        assert deps.index("base") < deps.index("left")
        assert deps.index("base") < deps.index("right")
        assert "top" not in deps

    def test_circular_dependency_raises(self):
        mgr = self._make_mgr()
        mgr.register(SimplePlugin(name="x", dependencies=["y"]))
        mgr.register(SimplePlugin(name="y", dependencies=["x"]))
        with pytest.raises(ValueError, match="[Cc]ircular"):
            mgr.resolve_dependencies("x")

    def test_self_circular_dependency_raises(self):
        mgr = self._make_mgr()
        mgr.register(SimplePlugin(name="self-ref", dependencies=["self-ref"]))
        with pytest.raises(ValueError):
            mgr.resolve_dependencies("self-ref")

    def test_unregistered_target_raises(self):
        mgr = self._make_mgr()
        with pytest.raises(ValueError, match="ghost"):
            mgr.resolve_dependencies("ghost")

    def test_unregistered_dependency_raises(self):
        mgr = self._make_mgr()
        mgr.register(SimplePlugin(name="needs-missing", dependencies=["missing-dep"]))
        with pytest.raises(ValueError, match="missing-dep"):
            mgr.resolve_dependencies("needs-missing")

    def test_result_excludes_target(self):
        mgr = self._make_mgr()
        mgr.register(SimplePlugin(name="dep"))
        mgr.register(SimplePlugin(name="target", dependencies=["dep"]))
        deps = mgr.resolve_dependencies("target")
        assert "target" not in deps


# ---------------------------------------------------------------------------
# 11. PluginManager with custom registry
# ---------------------------------------------------------------------------

class TestPluginManagerCustomRegistry:
    def test_accepts_existing_registry(self):
        reg = PluginRegistry()
        p = SimplePlugin(name="ext")
        reg.register(p)
        mgr = PluginManager(registry=reg)
        assert mgr.registry is reg
        assert mgr.registry.get("ext") is not None

    def test_creates_registry_when_none(self):
        mgr = PluginManager()
        assert isinstance(mgr.registry, PluginRegistry)


# ---------------------------------------------------------------------------
# 12. __init__.py public API
# ---------------------------------------------------------------------------

class TestPublicAPI:
    def test_all_names_importable(self):
        from docstoolkit import plugin_system  # noqa: F401
        import docstoolkit.plugin_system as ps
        for name in ps.__all__:
            assert hasattr(ps, name), f"Missing export: {name}"

    def test_plugin_in_all(self):
        from docstoolkit.plugin_system import Plugin  # noqa: F401

    def test_plugin_metadata_in_all(self):
        from docstoolkit.plugin_system import PluginMetadata  # noqa: F401

    def test_plugin_status_in_all(self):
        from docstoolkit.plugin_system import PluginStatus  # noqa: F401

    def test_plugin_record_in_all(self):
        from docstoolkit.plugin_system import PluginRecord  # noqa: F401

    def test_plugin_registry_in_all(self):
        from docstoolkit.plugin_system import PluginRegistry  # noqa: F401

    def test_plugin_manager_in_all(self):
        from docstoolkit.plugin_system import PluginManager  # noqa: F401
