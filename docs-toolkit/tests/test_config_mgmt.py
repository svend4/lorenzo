"""Tests for docstoolkit.config_mgmt — sources, manager, validator."""
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from docstoolkit.config_mgmt import (
    ConfigManager,
    ConfigRule,
    ConfigSource,
    ConfigValidator,
    DictSource,
    EnvSource,
    IniFileSource,
    JsonFileSource,
)


# =============================================================================
# Helpers
# =============================================================================

def _write_tmp_json(data: dict) -> Path:
    """Write *data* to a temp JSON file and return its Path."""
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8"
    )
    json.dump(data, f)
    f.close()
    return Path(f.name)


def _write_tmp_ini(content: str) -> Path:
    """Write *content* to a temp INI file and return its Path."""
    f = tempfile.NamedTemporaryFile(
        mode="w", suffix=".ini", delete=False, encoding="utf-8"
    )
    f.write(content)
    f.close()
    return Path(f.name)


# =============================================================================
# DictSource
# =============================================================================

class TestDictSource:
    def test_load_returns_dict(self):
        ds = DictSource({"a": 1, "b": 2})
        result = ds.load()
        assert isinstance(result, dict)

    def test_load_returns_correct_values(self):
        ds = DictSource({"x": "hello", "y": 42})
        result = ds.load()
        assert result["x"] == "hello"
        assert result["y"] == 42

    def test_load_returns_copy_not_original(self):
        original = {"key": "value"}
        ds = DictSource(original)
        result = ds.load()
        result["key"] = "mutated"
        # The source's stored copy must not be affected
        assert ds.load()["key"] == "value"

    def test_mutations_dont_affect_original_dict(self):
        original = {"key": "value"}
        ds = DictSource(original)
        result = ds.load()
        result["new_key"] = "added"
        assert "new_key" not in ds.load()

    def test_empty_dict_load(self):
        ds = DictSource({})
        assert ds.load() == {}

    def test_nested_dict_preserved(self):
        ds = DictSource({"db": {"host": "localhost", "port": 5432}})
        result = ds.load()
        assert result["db"]["host"] == "localhost"
        assert result["db"]["port"] == 5432

    def test_load_multiple_times_same_result(self):
        ds = DictSource({"a": 1})
        assert ds.load() == ds.load()

    def test_is_config_source_subclass(self):
        ds = DictSource({})
        assert isinstance(ds, ConfigSource)


# =============================================================================
# EnvSource
# =============================================================================

class TestEnvSource:
    def test_reads_env_var_with_prefix(self):
        with patch.dict(os.environ, {"APP_HOST": "myhost"}, clear=False):
            es = EnvSource(prefix="APP_")
            result = es.load()
        assert "host" in result
        assert result["host"] == "myhost"

    def test_strips_prefix(self):
        with patch.dict(os.environ, {"CFG_NAME": "test"}, clear=False):
            es = EnvSource(prefix="CFG_")
            result = es.load()
        assert "name" in result
        assert "cfg_name" not in result

    def test_lowercases_keys(self):
        with patch.dict(os.environ, {"APP_MY_VAR": "val"}, clear=False):
            es = EnvSource(prefix="APP_")
            result = es.load()
        # The remaining key "MY_VAR" does not use __ as separator, so
        # it should appear as "my_var" (lowercased but one segment since
        # default separator is __)
        assert "my_var" in result

    def test_nested_key_via_double_underscore(self):
        with patch.dict(os.environ, {"APP__DB__HOST": "dbhost"}, clear=False):
            es = EnvSource(prefix="APP")
            result = es.load()
        assert result["db"]["host"] == "dbhost"

    def test_nested_key_three_levels(self):
        with patch.dict(os.environ, {"APP__A__B__C": "deep"}, clear=False):
            es = EnvSource(prefix="APP")
            result = es.load()
        assert result["a"]["b"]["c"] == "deep"

    def test_no_prefix_reads_all_vars(self):
        with patch.dict(os.environ, {"MYUNIQVAR_999": "found"}, clear=True):
            es = EnvSource(prefix="")
            result = es.load()
        assert "myuniqvar_999" in result

    def test_prefix_filters_out_non_matching(self):
        env = {"APP__X": "1", "OTHER__Y": "2"}
        with patch.dict(os.environ, env, clear=True):
            es = EnvSource(prefix="APP")
            result = es.load()
        assert "x" in result
        assert "other__y" not in result
        assert "y" not in result

    def test_custom_separator(self):
        with patch.dict(os.environ, {"APP.DB.HOST": "h"}, clear=False):
            es = EnvSource(prefix="APP", separator=".")
            result = es.load()
        assert result["db"]["host"] == "h"

    def test_empty_prefix_uses_full_key(self):
        with patch.dict(os.environ, {"JUSTKEY": "v"}, clear=True):
            es = EnvSource(prefix="")
            result = es.load()
        assert result["justkey"] == "v"

    def test_separator_stripped_after_prefix(self):
        # "APP__DB" with prefix="APP" should strip "APP" then the "__" leaving "db"
        with patch.dict(os.environ, {"APP__DB": "value"}, clear=True):
            es = EnvSource(prefix="APP", separator="__")
            result = es.load()
        assert result.get("db") == "value"

    def test_multiple_env_vars_all_loaded(self):
        env = {"PFX__A": "1", "PFX__B": "2", "PFX__C": "3"}
        with patch.dict(os.environ, env, clear=True):
            es = EnvSource(prefix="PFX")
            result = es.load()
        assert result["a"] == "1"
        assert result["b"] == "2"
        assert result["c"] == "3"

    def test_is_config_source_subclass(self):
        assert isinstance(EnvSource(), ConfigSource)

    def test_returns_dict_type(self):
        with patch.dict(os.environ, {}, clear=True):
            es = EnvSource(prefix="NOTHINGHERE_XYZ")
            result = es.load()
        assert isinstance(result, dict)


# =============================================================================
# JsonFileSource
# =============================================================================

class TestJsonFileSource:
    def test_reads_json_file(self):
        path = _write_tmp_json({"key": "value"})
        try:
            js = JsonFileSource(path)
            result = js.load()
            assert result["key"] == "value"
        finally:
            path.unlink(missing_ok=True)

    def test_returns_dict(self):
        path = _write_tmp_json({"a": 1})
        try:
            js = JsonFileSource(path)
            assert isinstance(js.load(), dict)
        finally:
            path.unlink(missing_ok=True)

    def test_raises_file_not_found_on_missing(self):
        js = JsonFileSource("/tmp/does_not_exist_abc123xyz.json")
        with pytest.raises(FileNotFoundError):
            js.load()

    def test_rereads_on_each_call(self):
        path = _write_tmp_json({"version": 1})
        try:
            js = JsonFileSource(path)
            assert js.load()["version"] == 1
            # Overwrite the file
            path.write_text(json.dumps({"version": 2}), encoding="utf-8")
            assert js.load()["version"] == 2
        finally:
            path.unlink(missing_ok=True)

    def test_nested_json(self):
        path = _write_tmp_json({"db": {"host": "localhost", "port": 5432}})
        try:
            js = JsonFileSource(path)
            result = js.load()
            assert result["db"]["host"] == "localhost"
        finally:
            path.unlink(missing_ok=True)

    def test_accepts_string_path(self):
        path = _write_tmp_json({"ok": True})
        try:
            js = JsonFileSource(str(path))
            result = js.load()
            assert result["ok"] is True
        finally:
            path.unlink(missing_ok=True)

    def test_raises_value_error_for_json_list(self):
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        )
        json.dump([1, 2, 3], f)
        f.close()
        path = Path(f.name)
        try:
            js = JsonFileSource(path)
            with pytest.raises(ValueError):
                js.load()
        finally:
            path.unlink(missing_ok=True)

    def test_is_config_source_subclass(self):
        js = JsonFileSource("/tmp/dummy.json")
        assert isinstance(js, ConfigSource)

    def test_empty_json_object(self):
        path = _write_tmp_json({})
        try:
            js = JsonFileSource(path)
            assert js.load() == {}
        finally:
            path.unlink(missing_ok=True)


# =============================================================================
# IniFileSource
# =============================================================================

class TestIniFileSource:
    def test_reads_ini_file(self):
        ini = "[section]\nkey = value\n"
        path = _write_tmp_ini(ini)
        try:
            src = IniFileSource(path)
            result = src.load()
            assert "section" in result
            assert result["section"]["key"] == "value"
        finally:
            path.unlink(missing_ok=True)

    def test_sections_become_top_level_keys(self):
        ini = "[alpha]\na = 1\n[beta]\nb = 2\n"
        path = _write_tmp_ini(ini)
        try:
            src = IniFileSource(path)
            result = src.load()
            assert "alpha" in result
            assert "beta" in result
        finally:
            path.unlink(missing_ok=True)

    def test_values_are_strings(self):
        ini = "[sec]\nport = 5432\nflag = true\n"
        path = _write_tmp_ini(ini)
        try:
            src = IniFileSource(path)
            result = src.load()
            assert isinstance(result["sec"]["port"], str)
            assert isinstance(result["sec"]["flag"], str)
        finally:
            path.unlink(missing_ok=True)

    def test_raises_file_not_found_on_missing(self):
        src = IniFileSource("/tmp/totally_missing_abc.ini")
        with pytest.raises(FileNotFoundError):
            src.load()

    def test_multiple_keys_in_section(self):
        ini = "[db]\nhost = localhost\nport = 5432\nname = mydb\n"
        path = _write_tmp_ini(ini)
        try:
            src = IniFileSource(path)
            result = src.load()
            assert result["db"]["host"] == "localhost"
            assert result["db"]["port"] == "5432"
            assert result["db"]["name"] == "mydb"
        finally:
            path.unlink(missing_ok=True)

    def test_rereads_on_each_call(self):
        ini1 = "[sec]\nval = first\n"
        ini2 = "[sec]\nval = second\n"
        path = _write_tmp_ini(ini1)
        try:
            src = IniFileSource(path)
            assert src.load()["sec"]["val"] == "first"
            path.write_text(ini2, encoding="utf-8")
            assert src.load()["sec"]["val"] == "second"
        finally:
            path.unlink(missing_ok=True)

    def test_returns_dict(self):
        ini = "[s]\nk = v\n"
        path = _write_tmp_ini(ini)
        try:
            src = IniFileSource(path)
            assert isinstance(src.load(), dict)
        finally:
            path.unlink(missing_ok=True)

    def test_is_config_source_subclass(self):
        src = IniFileSource("/tmp/dummy.ini")
        assert isinstance(src, ConfigSource)

    def test_accepts_string_path(self):
        ini = "[x]\ny = z\n"
        path = _write_tmp_ini(ini)
        try:
            src = IniFileSource(str(path))
            result = src.load()
            assert result["x"]["y"] == "z"
        finally:
            path.unlink(missing_ok=True)


# =============================================================================
# ConfigManager — basic
# =============================================================================

class TestConfigManagerBasic:
    def test_empty_manager_get_returns_default(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.get("missing") is None
        assert mgr.get("missing", "fallback") == "fallback"

    def test_single_source_loaded(self):
        mgr = ConfigManager([DictSource({"host": "localhost"})])
        mgr.load()
        assert mgr.get("host") == "localhost"

    def test_add_source_after_construction(self):
        mgr = ConfigManager()
        mgr.add_source(DictSource({"a": 1}))
        mgr.load()
        assert mgr.get("a") == 1

    def test_no_sources_all_returns_empty(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.all() == {}

    def test_set_stores_value(self):
        mgr = ConfigManager()
        mgr.load()
        mgr.set("foo", "bar")
        assert mgr.get("foo") == "bar"

    def test_all_returns_full_dict(self):
        mgr = ConfigManager([DictSource({"x": 1, "y": 2})])
        mgr.load()
        result = mgr.all()
        assert result == {"x": 1, "y": 2}

    def test_all_returns_deep_copy(self):
        mgr = ConfigManager([DictSource({"nested": {"k": "v"}})])
        mgr.load()
        copy1 = mgr.all()
        copy1["nested"]["k"] = "mutated"
        copy2 = mgr.all()
        assert copy2["nested"]["k"] == "v"

    def test_load_rebuilds_config(self):
        ds = DictSource({"a": 1})
        mgr = ConfigManager([ds])
        mgr.load()
        assert mgr.get("a") == 1
        # Manually swap source
        mgr._sources = [DictSource({"b": 2})]
        mgr.load()
        assert mgr.get("a") is None
        assert mgr.get("b") == 2


# =============================================================================
# ConfigManager — priority merge
# =============================================================================

class TestConfigManagerPriority:
    def test_later_source_wins_scalar(self):
        s1 = DictSource({"key": "first"})
        s2 = DictSource({"key": "second"})
        mgr = ConfigManager([s1, s2])
        mgr.load()
        assert mgr.get("key") == "second"

    def test_earlier_source_value_kept_when_not_overridden(self):
        s1 = DictSource({"a": 1, "b": 2})
        s2 = DictSource({"b": 99})
        mgr = ConfigManager([s1, s2])
        mgr.load()
        assert mgr.get("a") == 1
        assert mgr.get("b") == 99

    def test_deep_merge_nested_dicts(self):
        s1 = DictSource({"db": {"host": "localhost", "port": 5432}})
        s2 = DictSource({"db": {"port": 9999}})
        mgr = ConfigManager([s1, s2])
        mgr.load()
        assert mgr.get("db.host") == "localhost"
        assert mgr.get("db.port") == 9999

    def test_three_sources_last_wins(self):
        s1 = DictSource({"x": 1})
        s2 = DictSource({"x": 2})
        s3 = DictSource({"x": 3})
        mgr = ConfigManager([s1, s2, s3])
        mgr.load()
        assert mgr.get("x") == 3

    def test_add_source_after_load_takes_effect_on_next_load(self):
        mgr = ConfigManager([DictSource({"a": "original"})])
        mgr.load()
        assert mgr.get("a") == "original"
        mgr.add_source(DictSource({"a": "override"}))
        mgr.load()
        assert mgr.get("a") == "override"

    def test_nested_override_does_not_wipe_sibling_keys(self):
        s1 = DictSource({"cfg": {"timeout": 30, "retries": 3}})
        s2 = DictSource({"cfg": {"timeout": 60}})
        mgr = ConfigManager([s1, s2])
        mgr.load()
        assert mgr.get("cfg.timeout") == 60
        assert mgr.get("cfg.retries") == 3


# =============================================================================
# ConfigManager — dot-notation
# =============================================================================

class TestConfigManagerDotNotation:
    def test_get_nested_key(self):
        mgr = ConfigManager([DictSource({"db": {"host": "h"}})])
        mgr.load()
        assert mgr.get("db.host") == "h"

    def test_get_deeply_nested_key(self):
        mgr = ConfigManager([DictSource({"a": {"b": {"c": "deep"}}})])
        mgr.load()
        assert mgr.get("a.b.c") == "deep"

    def test_get_missing_nested_returns_default(self):
        mgr = ConfigManager([DictSource({"a": {"b": 1}})])
        mgr.load()
        assert mgr.get("a.c", 42) == 42

    def test_set_nested_key_dot_notation(self):
        mgr = ConfigManager()
        mgr.load()
        mgr.set("db.host", "newhost")
        assert mgr.get("db.host") == "newhost"

    def test_set_creates_intermediate_dicts(self):
        mgr = ConfigManager()
        mgr.load()
        mgr.set("a.b.c", "value")
        assert mgr.get("a.b.c") == "value"

    def test_set_overwrites_existing_nested(self):
        mgr = ConfigManager([DictSource({"db": {"host": "old"}})])
        mgr.load()
        mgr.set("db.host", "new")
        assert mgr.get("db.host") == "new"


# =============================================================================
# ConfigManager — typed accessors
# =============================================================================

class TestGetInt:
    def test_get_int_from_int_value(self):
        mgr = ConfigManager([DictSource({"port": 8080})])
        mgr.load()
        assert mgr.get_int("port") == 8080

    def test_get_int_from_string(self):
        mgr = ConfigManager([DictSource({"port": "8080"})])
        mgr.load()
        assert mgr.get_int("port") == 8080

    def test_get_int_missing_returns_default(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.get_int("port", 3306) == 3306

    def test_get_int_default_zero_when_not_specified(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.get_int("missing") == 0

    def test_get_int_invalid_string_raises(self):
        mgr = ConfigManager([DictSource({"port": "notanumber"})])
        mgr.load()
        with pytest.raises((ValueError, TypeError)):
            mgr.get_int("port")


class TestGetFloat:
    def test_get_float_from_float(self):
        mgr = ConfigManager([DictSource({"rate": 0.5})])
        mgr.load()
        assert mgr.get_float("rate") == pytest.approx(0.5)

    def test_get_float_from_string(self):
        mgr = ConfigManager([DictSource({"rate": "3.14"})])
        mgr.load()
        assert mgr.get_float("rate") == pytest.approx(3.14)

    def test_get_float_missing_returns_default(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.get_float("missing", 1.5) == pytest.approx(1.5)

    def test_get_float_default_zero(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.get_float("missing") == pytest.approx(0.0)


class TestGetBool:
    @pytest.mark.parametrize("truthy", ["1", "true", "yes", "on",
                                         "True", "YES", "ON", "TRUE"])
    def test_truthy_strings(self, truthy):
        mgr = ConfigManager([DictSource({"flag": truthy})])
        mgr.load()
        assert mgr.get_bool("flag") is True

    @pytest.mark.parametrize("falsy", ["0", "false", "no", "off", "nope", ""])
    def test_falsy_strings(self, falsy):
        mgr = ConfigManager([DictSource({"flag": falsy})])
        mgr.load()
        assert mgr.get_bool("flag") is False

    def test_bool_true_passthrough(self):
        mgr = ConfigManager([DictSource({"flag": True})])
        mgr.load()
        assert mgr.get_bool("flag") is True

    def test_bool_false_passthrough(self):
        mgr = ConfigManager([DictSource({"flag": False})])
        mgr.load()
        assert mgr.get_bool("flag") is False

    def test_missing_returns_default_false(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.get_bool("missing") is False

    def test_missing_returns_specified_default(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.get_bool("missing", True) is True

    def test_integer_one_is_truthy(self):
        mgr = ConfigManager([DictSource({"flag": 1})])
        mgr.load()
        assert mgr.get_bool("flag") is True

    def test_integer_zero_is_falsy(self):
        mgr = ConfigManager([DictSource({"flag": 0})])
        mgr.load()
        assert mgr.get_bool("flag") is False


class TestGetList:
    def test_list_passthrough(self):
        mgr = ConfigManager([DictSource({"items": ["a", "b", "c"]})])
        mgr.load()
        assert mgr.get_list("items") == ["a", "b", "c"]

    def test_string_split_by_comma(self):
        mgr = ConfigManager([DictSource({"items": "a,b,c"})])
        mgr.load()
        assert mgr.get_list("items") == ["a", "b", "c"]

    def test_string_split_strips_whitespace(self):
        mgr = ConfigManager([DictSource({"items": "a , b , c"})])
        mgr.load()
        assert mgr.get_list("items") == ["a", "b", "c"]

    def test_custom_separator(self):
        mgr = ConfigManager([DictSource({"items": "a|b|c"})])
        mgr.load()
        assert mgr.get_list("items", separator="|") == ["a", "b", "c"]

    def test_missing_key_returns_empty_list(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.get_list("missing") == []

    def test_missing_key_returns_specified_default(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.get_list("missing", default=["x"]) == ["x"]

    def test_single_item_no_separator(self):
        mgr = ConfigManager([DictSource({"items": "solo"})])
        mgr.load()
        assert mgr.get_list("items") == ["solo"]


# =============================================================================
# ConfigValidator + ConfigRule
# =============================================================================

class TestConfigValidator:
    def _mgr(self, data: dict) -> ConfigManager:
        mgr = ConfigManager([DictSource(data)])
        mgr.load()
        return mgr

    def test_valid_config_no_errors(self):
        mgr = self._mgr({"host": "localhost", "port": 5432})
        v = ConfigValidator([
            ConfigRule("host", required=True, type_=str),
            ConfigRule("port", required=True, type_=int),
        ])
        assert v.validate(mgr) == []

    def test_required_key_missing_produces_error(self):
        mgr = self._mgr({})
        v = ConfigValidator([ConfigRule("host", required=True)])
        errors = v.validate(mgr)
        assert len(errors) == 1
        assert "host" in errors[0]

    def test_type_mismatch_produces_error(self):
        mgr = self._mgr({"port": "not_an_int"})
        v = ConfigValidator([ConfigRule("port", required=True, type_=int)])
        errors = v.validate(mgr)
        assert any("port" in e for e in errors)

    def test_custom_validator_called_and_passes(self):
        mgr = self._mgr({"port": 8080})
        v = ConfigValidator([
            ConfigRule("port", validator=lambda p: 1 <= p <= 65535)
        ])
        assert v.validate(mgr) == []

    def test_custom_validator_failure_produces_error(self):
        mgr = self._mgr({"port": 99999})
        v = ConfigValidator([
            ConfigRule("port", validator=lambda p: 1 <= p <= 65535)
        ])
        errors = v.validate(mgr)
        assert len(errors) == 1
        assert "port" in errors[0]

    def test_validator_exception_produces_error(self):
        mgr = self._mgr({"port": "bad"})
        def bad_validator(v):
            raise RuntimeError("exploded")
        v = ConfigValidator([ConfigRule("port", validator=bad_validator)])
        errors = v.validate(mgr)
        assert len(errors) == 1
        assert "exception" in errors[0].lower() or "exploded" in errors[0]

    def test_multiple_rules_multiple_errors(self):
        mgr = self._mgr({})
        v = ConfigValidator([
            ConfigRule("host", required=True),
            ConfigRule("port", required=True),
        ])
        errors = v.validate(mgr)
        assert len(errors) == 2

    def test_optional_key_absent_no_error(self):
        mgr = self._mgr({})
        v = ConfigValidator([ConfigRule("opt", required=False, type_=str)])
        assert v.validate(mgr) == []

    def test_add_rule_method(self):
        mgr = self._mgr({})
        v = ConfigValidator()
        v.add_rule(ConfigRule("x", required=True))
        errors = v.validate(mgr)
        assert len(errors) == 1

    def test_description_in_error_message(self):
        mgr = self._mgr({})
        v = ConfigValidator([
            ConfigRule("host", required=True, description="database hostname")
        ])
        errors = v.validate(mgr)
        assert "database hostname" in errors[0]

    def test_nested_key_validation(self):
        mgr = self._mgr({"db": {"host": "localhost"}})
        v = ConfigValidator([ConfigRule("db.host", required=True, type_=str)])
        assert v.validate(mgr) == []

    def test_nested_key_missing_required(self):
        mgr = self._mgr({"db": {}})
        v = ConfigValidator([ConfigRule("db.host", required=True)])
        errors = v.validate(mgr)
        assert len(errors) == 1

    def test_empty_rules_no_errors(self):
        mgr = self._mgr({"any": "value"})
        v = ConfigValidator()
        assert v.validate(mgr) == []

    def test_type_check_skipped_for_absent_optional(self):
        mgr = self._mgr({})
        v = ConfigValidator([ConfigRule("opt", required=False, type_=int)])
        assert v.validate(mgr) == []

    def test_validator_skipped_for_absent_optional(self):
        called = []
        def spy(v):
            called.append(v)
            return True
        mgr = self._mgr({})
        v = ConfigValidator([ConfigRule("opt", required=False, validator=spy)])
        v.validate(mgr)
        assert called == []


# =============================================================================
# Edge cases
# =============================================================================

class TestEdgeCases:
    def test_empty_sources_list(self):
        mgr = ConfigManager([])
        mgr.load()
        assert mgr.all() == {}

    def test_set_does_not_persist_across_load(self):
        mgr = ConfigManager([DictSource({"a": 1})])
        mgr.load()
        mgr.set("a", 999)
        assert mgr.get("a") == 999
        mgr.load()
        # After reload, the in-memory override is gone
        assert mgr.get("a") == 1

    def test_deep_copy_independence_in_all(self):
        mgr = ConfigManager([DictSource({"lst": [1, 2, 3]})])
        mgr.load()
        snapshot = mgr.all()
        snapshot["lst"].append(4)
        assert len(mgr.all()["lst"]) == 3

    def test_overriding_dict_with_scalar(self):
        s1 = DictSource({"a": {"b": 1}})
        s2 = DictSource({"a": "scalar"})
        mgr = ConfigManager([s1, s2])
        mgr.load()
        assert mgr.get("a") == "scalar"

    def test_overriding_scalar_with_dict(self):
        s1 = DictSource({"a": "scalar"})
        s2 = DictSource({"a": {"b": 1}})
        mgr = ConfigManager([s1, s2])
        mgr.load()
        assert mgr.get("a") == {"b": 1}

    def test_env_source_returns_dict(self):
        with patch.dict(os.environ, {}, clear=True):
            es = EnvSource(prefix="TOTALLY_ABSENT_PREFIX_XYZ")
            assert es.load() == {}

    def test_json_source_path_object_works(self):
        path = _write_tmp_json({"pathobj": True})
        try:
            js = JsonFileSource(Path(path))
            assert js.load()["pathobj"] is True
        finally:
            path.unlink(missing_ok=True)

    def test_config_manager_no_sources_constructor(self):
        mgr = ConfigManager()
        mgr.load()
        assert mgr.get("x", "default") == "default"
