"""Tests for docstoolkit.config_profiles — layered configuration profiles."""
import json
import tempfile
from pathlib import Path

import pytest

from docstoolkit.config_profiles import (
    ConfigProfile,
    ProfileLayer,
    ProfileLoader,
    ProfileMergeResult,
    load_profile,
    merge_profiles,
)


# ---------------------------------------------------------------------------
# ProfileLayer enum
# ---------------------------------------------------------------------------

class TestProfileLayerEnum:
    def test_base_value(self):
        assert ProfileLayer.BASE.value == "base"

    def test_environment_value(self):
        assert ProfileLayer.ENVIRONMENT.value == "environment"

    def test_user_value(self):
        assert ProfileLayer.USER.value == "user"

    def test_runtime_value(self):
        assert ProfileLayer.RUNTIME.value == "runtime"

    def test_is_str_subclass(self):
        assert isinstance(ProfileLayer.BASE, str)

    def test_all_four_members(self):
        assert len(ProfileLayer) == 4


# ---------------------------------------------------------------------------
# ConfigProfile — construction and field defaults
# ---------------------------------------------------------------------------

class TestConfigProfileFields:
    def test_name_and_layer_required(self):
        p = ConfigProfile(name="test", layer=ProfileLayer.BASE)
        assert p.name == "test"
        assert p.layer == ProfileLayer.BASE

    def test_values_default_empty(self):
        p = ConfigProfile(name="x", layer=ProfileLayer.BASE)
        assert p.values == {}

    def test_extends_default_empty_string(self):
        p = ConfigProfile(name="x", layer=ProfileLayer.BASE)
        assert p.extends == ""

    def test_description_default_empty_string(self):
        p = ConfigProfile(name="x", layer=ProfileLayer.BASE)
        assert p.description == ""

    def test_values_set_on_construction(self):
        p = ConfigProfile(name="x", layer=ProfileLayer.USER, values={"a": 1})
        assert p.values == {"a": 1}

    def test_extends_set_on_construction(self):
        p = ConfigProfile(name="child", layer=ProfileLayer.USER, extends="parent")
        assert p.extends == "parent"

    def test_description_set_on_construction(self):
        p = ConfigProfile(name="x", layer=ProfileLayer.BASE, description="desc")
        assert p.description == "desc"


# ---------------------------------------------------------------------------
# ConfigProfile — methods
# ---------------------------------------------------------------------------

class TestConfigProfileGet:
    def test_get_existing_key(self):
        p = ConfigProfile(name="p", layer=ProfileLayer.BASE, values={"k": 42})
        assert p.get("k") == 42

    def test_get_missing_key_returns_none(self):
        p = ConfigProfile(name="p", layer=ProfileLayer.BASE)
        assert p.get("missing") is None

    def test_get_missing_key_with_default(self):
        p = ConfigProfile(name="p", layer=ProfileLayer.BASE)
        assert p.get("missing", "fallback") == "fallback"

    def test_get_falsy_value_not_masked_by_default(self):
        p = ConfigProfile(name="p", layer=ProfileLayer.BASE, values={"z": 0})
        assert p.get("z", 99) == 0


class TestConfigProfileSet:
    def test_set_new_key(self):
        p = ConfigProfile(name="p", layer=ProfileLayer.BASE)
        p.set("foo", "bar")
        assert p.values["foo"] == "bar"

    def test_set_overwrites_existing_key(self):
        p = ConfigProfile(name="p", layer=ProfileLayer.BASE, values={"x": 1})
        p.set("x", 2)
        assert p.values["x"] == 2

    def test_set_various_types(self):
        p = ConfigProfile(name="p", layer=ProfileLayer.BASE)
        p.set("num", 3.14)
        p.set("lst", [1, 2, 3])
        p.set("nested", {"a": 1})
        assert p.get("num") == 3.14
        assert p.get("lst") == [1, 2, 3]
        assert p.get("nested") == {"a": 1}


class TestConfigProfileKeys:
    def test_keys_empty(self):
        p = ConfigProfile(name="p", layer=ProfileLayer.BASE)
        assert p.keys() == []

    def test_keys_returns_list(self):
        p = ConfigProfile(name="p", layer=ProfileLayer.BASE, values={"a": 1, "b": 2})
        assert sorted(p.keys()) == ["a", "b"]

    def test_keys_reflects_set(self):
        p = ConfigProfile(name="p", layer=ProfileLayer.BASE)
        p.set("new_key", True)
        assert "new_key" in p.keys()


# ---------------------------------------------------------------------------
# ConfigProfile — serialisation round-trips
# ---------------------------------------------------------------------------

class TestConfigProfileToDict:
    def test_to_dict_contains_all_fields(self):
        p = ConfigProfile(
            name="env",
            layer=ProfileLayer.ENVIRONMENT,
            values={"debug": True},
            extends="base",
            description="Environment profile",
        )
        d = p.to_dict()
        assert d["name"] == "env"
        assert d["layer"] == "environment"
        assert d["values"] == {"debug": True}
        assert d["extends"] == "base"
        assert d["description"] == "Environment profile"

    def test_from_dict_round_trip(self):
        p = ConfigProfile(
            name="rt",
            layer=ProfileLayer.RUNTIME,
            values={"x": 10},
            extends="user",
            description="runtime override",
        )
        restored = ConfigProfile.from_dict(p.to_dict())
        assert restored.name == p.name
        assert restored.layer == p.layer
        assert restored.values == p.values
        assert restored.extends == p.extends
        assert restored.description == p.description

    def test_from_dict_defaults_layer_to_base(self):
        d = {"name": "minimal"}
        p = ConfigProfile.from_dict(d)
        assert p.layer == ProfileLayer.BASE

    def test_from_dict_defaults_values_empty(self):
        d = {"name": "minimal"}
        p = ConfigProfile.from_dict(d)
        assert p.values == {}

    def test_from_dict_defaults_extends_empty(self):
        d = {"name": "minimal"}
        p = ConfigProfile.from_dict(d)
        assert p.extends == ""


class TestConfigProfileJson:
    def test_to_json_is_valid_json(self):
        p = ConfigProfile(name="j", layer=ProfileLayer.USER, values={"k": "v"})
        s = p.to_json()
        parsed = json.loads(s)
        assert parsed["name"] == "j"

    def test_from_json_round_trip(self):
        p = ConfigProfile(
            name="jrt",
            layer=ProfileLayer.USER,
            values={"a": 1, "b": "two"},
            extends="base",
            description="json test",
        )
        restored = ConfigProfile.from_json(p.to_json())
        assert restored.name == p.name
        assert restored.layer == p.layer
        assert restored.values == p.values
        assert restored.extends == p.extends
        assert restored.description == p.description

    def test_to_json_indented(self):
        p = ConfigProfile(name="j", layer=ProfileLayer.BASE)
        s = p.to_json()
        # indent=2 means newlines are present
        assert "\n" in s


# ---------------------------------------------------------------------------
# ProfileLoader
# ---------------------------------------------------------------------------

class TestProfileLoaderRegisterGet:
    def test_register_and_get(self):
        loader = ProfileLoader()
        p = ConfigProfile(name="alpha", layer=ProfileLayer.BASE)
        loader.register(p)
        assert loader.get("alpha") is p

    def test_get_missing_returns_none(self):
        loader = ProfileLoader()
        assert loader.get("nonexistent") is None

    def test_register_overwrites_same_name(self):
        loader = ProfileLoader()
        p1 = ConfigProfile(name="x", layer=ProfileLayer.BASE, values={"v": 1})
        p2 = ConfigProfile(name="x", layer=ProfileLayer.BASE, values={"v": 2})
        loader.register(p1)
        loader.register(p2)
        assert loader.get("x").values["v"] == 2


class TestProfileLoaderListNames:
    def test_list_names_empty(self):
        loader = ProfileLoader()
        assert loader.list_names() == []

    def test_list_names_sorted(self):
        loader = ProfileLoader()
        for name in ["beta", "alpha", "gamma"]:
            loader.register(ConfigProfile(name=name, layer=ProfileLayer.BASE))
        assert loader.list_names() == ["alpha", "beta", "gamma"]


class TestProfileLoaderLoadFromDict:
    def test_load_from_dict_returns_profile(self):
        loader = ProfileLoader()
        d = {"name": "d-profile", "layer": "user", "values": {"x": 5}}
        p = loader.load_from_dict(d)
        assert isinstance(p, ConfigProfile)
        assert p.name == "d-profile"

    def test_load_from_dict_registers_profile(self):
        loader = ProfileLoader()
        d = {"name": "reg-test", "layer": "base"}
        loader.load_from_dict(d)
        assert loader.get("reg-test") is not None


class TestProfileLoaderLoadFromJson:
    def test_load_from_json_registers_and_returns(self):
        loader = ProfileLoader()
        j = json.dumps({"name": "json-p", "layer": "environment", "values": {"env": "prod"}})
        p = loader.load_from_json(j)
        assert p.name == "json-p"
        assert loader.get("json-p") is p


class TestProfileLoaderLoadFromFile:
    def test_load_from_file(self, tmp_path):
        data = {"name": "file-p", "layer": "user", "values": {"file": True}}
        f = tmp_path / "profile.json"
        f.write_text(json.dumps(data), encoding="utf-8")
        loader = ProfileLoader()
        p = loader.load_from_file(f)
        assert p.name == "file-p"
        assert p.values["file"] is True
        assert loader.get("file-p") is p


# ---------------------------------------------------------------------------
# ProfileLoader.resolve_chain
# ---------------------------------------------------------------------------

class TestResolveChain:
    def test_single_profile_no_parent(self):
        loader = ProfileLoader()
        p = ConfigProfile(name="solo", layer=ProfileLayer.BASE)
        loader.register(p)
        chain = loader.resolve_chain("solo")
        assert chain == [p]

    def test_two_levels_parent_child(self):
        loader = ProfileLoader()
        parent = ConfigProfile(name="parent", layer=ProfileLayer.BASE, values={"a": 1})
        child = ConfigProfile(name="child", layer=ProfileLayer.ENVIRONMENT, extends="parent", values={"b": 2})
        loader.register(parent)
        loader.register(child)
        chain = loader.resolve_chain("child")
        assert chain == [parent, child]

    def test_three_levels(self):
        loader = ProfileLoader()
        base = ConfigProfile(name="base", layer=ProfileLayer.BASE)
        env = ConfigProfile(name="env", layer=ProfileLayer.ENVIRONMENT, extends="base")
        user = ConfigProfile(name="user", layer=ProfileLayer.USER, extends="env")
        loader.register(base)
        loader.register(env)
        loader.register(user)
        chain = loader.resolve_chain("user")
        assert chain == [base, env, user]

    def test_missing_profile_returns_empty(self):
        loader = ProfileLoader()
        chain = loader.resolve_chain("ghost")
        assert chain == []

    def test_circular_extends_stops(self):
        loader = ProfileLoader()
        a = ConfigProfile(name="a", layer=ProfileLayer.BASE, extends="b")
        b = ConfigProfile(name="b", layer=ProfileLayer.BASE, extends="a")
        loader.register(a)
        loader.register(b)
        # Should not hang; length <= 2 (max_depth=10 but cycle broken by visited set)
        chain = loader.resolve_chain("a")
        assert len(chain) <= 10
        names = [p.name for p in chain]
        # Both should appear once
        assert names.count("a") <= 1
        assert names.count("b") <= 1

    def test_parent_not_in_registry_stops_chain(self):
        loader = ProfileLoader()
        child = ConfigProfile(name="child", layer=ProfileLayer.USER, extends="missing-parent")
        loader.register(child)
        chain = loader.resolve_chain("child")
        assert chain == [child]


# ---------------------------------------------------------------------------
# load_profile convenience function
# ---------------------------------------------------------------------------

class TestLoadProfile:
    def test_returns_config_profile(self):
        p = load_profile("quick")
        assert isinstance(p, ConfigProfile)

    def test_name_set(self):
        p = load_profile("my-profile")
        assert p.name == "my-profile"

    def test_default_layer_is_runtime(self):
        p = load_profile("rt")
        assert p.layer == ProfileLayer.RUNTIME

    def test_custom_layer(self):
        p = load_profile("base-p", layer=ProfileLayer.BASE)
        assert p.layer == ProfileLayer.BASE

    def test_values_passed_through(self):
        p = load_profile("with-vals", values={"key": "val"})
        assert p.get("key") == "val"

    def test_none_values_defaults_to_empty(self):
        p = load_profile("empty-vals", values=None)
        assert p.values == {}


# ---------------------------------------------------------------------------
# ProfileMergeResult
# ---------------------------------------------------------------------------

class TestProfileMergeResult:
    def _make_result(self):
        return ProfileMergeResult(
            merged={"a": 1, "b": 2},
            sources={"a": "base", "b": "env"},
            layers_applied=["base", "env"],
            _all_setters={"a": ["base"], "b": ["base", "env"]},
        )

    def test_get_existing_key(self):
        r = self._make_result()
        assert r.get("a") == 1

    def test_get_missing_key_default_none(self):
        r = self._make_result()
        assert r.get("missing") is None

    def test_get_missing_key_custom_default(self):
        r = self._make_result()
        assert r.get("missing", 99) == 99

    def test_who_set_returns_profile_name(self):
        r = self._make_result()
        assert r.who_set("b") == "env"

    def test_who_set_unknown_key_returns_empty(self):
        r = self._make_result()
        assert r.who_set("unknown") == ""

    def test_conflicts_returns_keys_set_by_multiple(self):
        r = self._make_result()
        # "b" was set by both "base" and "env"
        assert "b" in r.conflicts()

    def test_conflicts_excludes_keys_set_by_one(self):
        r = self._make_result()
        assert "a" not in r.conflicts()

    def test_conflicts_empty_when_no_overlap(self):
        r = ProfileMergeResult(
            merged={"x": 1},
            sources={"x": "only"},
            layers_applied=["only"],
            _all_setters={"x": ["only"]},
        )
        assert r.conflicts() == []


# ---------------------------------------------------------------------------
# merge_profiles
# ---------------------------------------------------------------------------

class TestMergeProfiles:
    def test_single_profile_merged_equals_values(self):
        p = ConfigProfile(name="solo", layer=ProfileLayer.BASE, values={"a": 1, "b": 2})
        result = merge_profiles([p])
        assert result.merged == {"a": 1, "b": 2}

    def test_later_profile_overrides_earlier(self):
        base = ConfigProfile(name="base", layer=ProfileLayer.BASE, values={"x": 1, "y": 10})
        env = ConfigProfile(name="env", layer=ProfileLayer.ENVIRONMENT, values={"x": 2})
        result = merge_profiles([base, env])
        assert result.merged["x"] == 2   # overridden
        assert result.merged["y"] == 10  # from base

    def test_sources_reflect_last_setter(self):
        base = ConfigProfile(name="base", layer=ProfileLayer.BASE, values={"k": "old"})
        user = ConfigProfile(name="user", layer=ProfileLayer.USER, values={"k": "new"})
        result = merge_profiles([base, user])
        assert result.who_set("k") == "user"

    def test_layers_applied_in_order(self):
        profiles = [
            ConfigProfile(name="base", layer=ProfileLayer.BASE),
            ConfigProfile(name="env", layer=ProfileLayer.ENVIRONMENT),
            ConfigProfile(name="runtime", layer=ProfileLayer.RUNTIME),
        ]
        result = merge_profiles(profiles)
        assert result.layers_applied == ["base", "env", "runtime"]

    def test_empty_profiles_list(self):
        result = merge_profiles([])
        assert result.merged == {}
        assert result.layers_applied == []

    def test_conflict_detected_when_key_in_two_profiles(self):
        p1 = ConfigProfile(name="p1", layer=ProfileLayer.BASE, values={"shared": 1})
        p2 = ConfigProfile(name="p2", layer=ProfileLayer.ENVIRONMENT, values={"shared": 2})
        result = merge_profiles([p1, p2])
        assert "shared" in result.conflicts()

    def test_no_conflict_for_unique_keys(self):
        p1 = ConfigProfile(name="p1", layer=ProfileLayer.BASE, values={"a": 1})
        p2 = ConfigProfile(name="p2", layer=ProfileLayer.ENVIRONMENT, values={"b": 2})
        result = merge_profiles([p1, p2])
        assert result.conflicts() == []

    def test_three_layer_merge_order(self):
        base = ConfigProfile(name="base", layer=ProfileLayer.BASE, values={"a": "base", "b": "base"})
        env = ConfigProfile(name="env", layer=ProfileLayer.ENVIRONMENT, values={"b": "env", "c": "env"})
        runtime = ConfigProfile(name="runtime", layer=ProfileLayer.RUNTIME, values={"c": "runtime", "d": "runtime"})
        result = merge_profiles([base, env, runtime])
        assert result.merged["a"] == "base"
        assert result.merged["b"] == "env"
        assert result.merged["c"] == "runtime"
        assert result.merged["d"] == "runtime"

    def test_three_layer_sources(self):
        base = ConfigProfile(name="base", layer=ProfileLayer.BASE, values={"a": 1})
        env = ConfigProfile(name="env", layer=ProfileLayer.ENVIRONMENT, values={"a": 2})
        runtime = ConfigProfile(name="runtime", layer=ProfileLayer.RUNTIME, values={"a": 3})
        result = merge_profiles([base, env, runtime])
        assert result.who_set("a") == "runtime"

    def test_empty_values_profiles_contribute_no_keys(self):
        p1 = ConfigProfile(name="p1", layer=ProfileLayer.BASE)
        p2 = ConfigProfile(name="p2", layer=ProfileLayer.ENVIRONMENT, values={"only_env": True})
        result = merge_profiles([p1, p2])
        assert list(result.merged.keys()) == ["only_env"]

    def test_layers_applied_includes_empty_profiles(self):
        p1 = ConfigProfile(name="empty1", layer=ProfileLayer.BASE)
        p2 = ConfigProfile(name="empty2", layer=ProfileLayer.ENVIRONMENT)
        result = merge_profiles([p1, p2])
        assert result.layers_applied == ["empty1", "empty2"]
