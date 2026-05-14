"""Tests for docstoolkit.settings_layer."""
import threading

import pytest

from docstoolkit.settings_layer import LayerName, Setting, SettingsLayer


class TestLayerName:
    def test_has_all_layers(self):
        assert LayerName.DEFAULTS
        assert LayerName.FILE
        assert LayerName.ENV
        assert LayerName.USER
        assert LayerName.RUNTIME

    def test_layer_values_are_strings(self):
        assert LayerName.DEFAULTS.value == "defaults"
        assert LayerName.RUNTIME.value == "runtime"

    def test_layer_count(self):
        assert len(list(LayerName)) == 5

    def test_layers_are_unique(self):
        values = [l.value for l in LayerName]
        assert len(values) == len(set(values))


class TestSetting:
    def test_create(self):
        s = Setting(key="x", value=1, layer=LayerName.USER)
        assert s.key == "x"
        assert s.value == 1
        assert s.layer == LayerName.USER
        assert s.source is None

    def test_with_source(self):
        s = Setting(key="x", value=1, layer=LayerName.FILE, source="/etc/cfg")
        assert s.source == "/etc/cfg"

    def test_equality(self):
        s1 = Setting(key="x", value=1, layer=LayerName.USER)
        s2 = Setting(key="x", value=1, layer=LayerName.USER)
        assert s1 == s2

    def test_inequality(self):
        s1 = Setting(key="x", value=1, layer=LayerName.USER)
        s2 = Setting(key="x", value=2, layer=LayerName.USER)
        assert s1 != s2


class TestSetDefaults:
    def test_set_default_single(self):
        s = SettingsLayer()
        s.set_default("k", "v")
        assert s.get("k") == "v"

    def test_set_defaults_multi(self):
        s = SettingsLayer()
        s.set_defaults({"a": 1, "b": 2})
        assert s.get("a") == 1
        assert s.get("b") == 2

    def test_default_layer_resolves(self):
        s = SettingsLayer()
        s.set_default("k", "v")
        assert s.get_layer("k") == LayerName.DEFAULTS

    def test_overwrite_default(self):
        s = SettingsLayer()
        s.set_default("k", 1)
        s.set_default("k", 2)
        assert s.get("k") == 2

    def test_default_value_none(self):
        s = SettingsLayer()
        s.set_default("k", None)
        assert s.get("k") is None
        assert s.has("k") is True


class TestLoadFileLayer:
    def test_basic_load(self):
        s = SettingsLayer()
        s.load_file_layer({"a": 1, "b": 2})
        assert s.get("a") == 1
        assert s.get("b") == 2

    def test_file_overrides_defaults(self):
        s = SettingsLayer()
        s.set_default("a", 0)
        s.load_file_layer({"a": 99})
        assert s.get("a") == 99
        assert s.get_layer("a") == LayerName.FILE

    def test_file_with_source(self):
        s = SettingsLayer()
        s.load_file_layer({"a": 1}, source="/etc/cfg.json")
        setting = s.get_setting("a")
        assert setting.source == "/etc/cfg.json"

    def test_file_coerces_to_default_type(self):
        s = SettingsLayer()
        s.set_default("port", 8080)
        s.load_file_layer({"port": "9000"})
        assert s.get("port") == 9000
        assert isinstance(s.get("port"), int)

    def test_file_empty(self):
        s = SettingsLayer()
        s.load_file_layer({})
        assert s.all_keys() == set()


class TestLoadEnvLayer:
    def test_basic_env(self):
        s = SettingsLayer()
        s.load_env_layer({"FOO": "bar"})
        assert s.get("foo") == "bar"

    def test_env_with_prefix(self):
        s = SettingsLayer()
        s.load_env_layer({"APP_HOST": "localhost", "OTHER": "x"}, prefix="APP_")
        assert s.get("host") == "localhost"
        assert s.has("other") is False

    def test_env_lowercases(self):
        s = SettingsLayer()
        s.load_env_layer({"MY_KEY": "v"})
        assert s.get("my_key") == "v"

    def test_env_coerces_int(self):
        s = SettingsLayer()
        s.set_default("port", 80)
        s.load_env_layer({"PORT": "443"})
        assert s.get("port") == 443
        assert isinstance(s.get("port"), int)

    def test_env_coerces_bool(self):
        s = SettingsLayer()
        s.set_default("debug", False)
        s.load_env_layer({"DEBUG": "true"})
        assert s.get("debug") is True

    def test_env_coerces_bool_false(self):
        s = SettingsLayer()
        s.set_default("debug", True)
        s.load_env_layer({"DEBUG": "0"})
        assert s.get("debug") is False

    def test_env_coerces_float(self):
        s = SettingsLayer()
        s.set_default("ratio", 0.5)
        s.load_env_layer({"RATIO": "0.75"})
        assert s.get("ratio") == 0.75

    def test_env_source_is_raw_key(self):
        s = SettingsLayer()
        s.load_env_layer({"APP_HOST": "x"}, prefix="APP_")
        setting = s.get_setting("host")
        assert setting.source == "APP_HOST"

    def test_env_overrides_file_and_defaults(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        s.load_file_layer({"a": 2})
        s.load_env_layer({"A": "3"})
        assert s.get("a") == 3
        assert s.get_layer("a") == LayerName.ENV

    def test_env_skips_prefix_mismatch(self):
        s = SettingsLayer()
        s.load_env_layer({"X": "1", "APP_Y": "2"}, prefix="APP_")
        assert s.has("x") is False
        assert s.get("y") == "2"

    def test_env_empty_key_after_prefix_skipped(self):
        s = SettingsLayer()
        s.load_env_layer({"APP_": "x"}, prefix="APP_")
        assert s.all_keys() == set()


class TestSetUser:
    def test_set_user(self):
        s = SettingsLayer()
        s.set_user("k", "v")
        assert s.get("k") == "v"
        assert s.get_layer("k") == LayerName.USER

    def test_user_overrides_env(self):
        s = SettingsLayer()
        s.load_env_layer({"K": "env"})
        s.set_user("k", "user")
        assert s.get("k") == "user"

    def test_user_overrides_file(self):
        s = SettingsLayer()
        s.load_file_layer({"k": "file"})
        s.set_user("k", "user")
        assert s.get("k") == "user"


class TestSetRuntime:
    def test_set_runtime(self):
        s = SettingsLayer()
        s.set_runtime("k", "v")
        assert s.get("k") == "v"

    def test_runtime_overrides_user(self):
        s = SettingsLayer()
        s.set_user("k", "user")
        s.set_runtime("k", "rt")
        assert s.get("k") == "rt"
        assert s.get_layer("k") == LayerName.RUNTIME

    def test_runtime_is_highest(self):
        s = SettingsLayer()
        s.set_default("k", "d")
        s.load_file_layer({"k": "f"})
        s.load_env_layer({"K": "e"})
        s.set_user("k", "u")
        s.set_runtime("k", "r")
        assert s.get("k") == "r"


class TestGetCascade:
    def test_only_defaults(self):
        s = SettingsLayer()
        s.set_default("k", 1)
        assert s.get_layer("k") == LayerName.DEFAULTS

    def test_file_over_defaults(self):
        s = SettingsLayer()
        s.set_default("k", 1)
        s.load_file_layer({"k": 2})
        assert s.get_layer("k") == LayerName.FILE

    def test_env_over_file(self):
        s = SettingsLayer()
        s.load_file_layer({"k": 1})
        s.load_env_layer({"K": "2"})
        assert s.get_layer("k") == LayerName.ENV

    def test_user_over_env(self):
        s = SettingsLayer()
        s.load_env_layer({"K": "1"})
        s.set_user("k", 2)
        assert s.get_layer("k") == LayerName.USER

    def test_runtime_over_user(self):
        s = SettingsLayer()
        s.set_user("k", 1)
        s.set_runtime("k", 2)
        assert s.get_layer("k") == LayerName.RUNTIME

    def test_full_cascade(self):
        s = SettingsLayer()
        s.set_default("k", "d")
        assert s.get("k") == "d"
        s.load_file_layer({"k": "f"})
        assert s.get("k") == "f"
        s.load_env_layer({"K": "e"})
        assert s.get("k") == "e"
        s.set_user("k", "u")
        assert s.get("k") == "u"
        s.set_runtime("k", "r")
        assert s.get("k") == "r"

    def test_missing_returns_default(self):
        s = SettingsLayer()
        assert s.get("missing", "fallback") == "fallback"

    def test_missing_returns_none(self):
        s = SettingsLayer()
        assert s.get("missing") is None


class TestGetLayer:
    def test_missing_key(self):
        s = SettingsLayer()
        assert s.get_layer("nope") is None

    def test_returns_correct_layer(self):
        s = SettingsLayer()
        s.load_file_layer({"a": 1})
        assert s.get_layer("a") == LayerName.FILE


class TestGetSetting:
    def test_missing(self):
        s = SettingsLayer()
        assert s.get_setting("nope") is None

    def test_returns_setting(self):
        s = SettingsLayer()
        s.set_user("a", 5)
        st = s.get_setting("a")
        assert st.key == "a"
        assert st.value == 5
        assert st.layer == LayerName.USER

    def test_setting_source(self):
        s = SettingsLayer()
        s.load_file_layer({"a": 1}, source="cfg.json")
        st = s.get_setting("a")
        assert st.source == "cfg.json"

    def test_setting_no_source_for_user_layer(self):
        s = SettingsLayer()
        s.set_user("a", 1)
        st = s.get_setting("a")
        assert st.source is None


class TestHas:
    def test_has_true(self):
        s = SettingsLayer()
        s.set_default("k", 1)
        assert s.has("k") is True

    def test_has_false(self):
        s = SettingsLayer()
        assert s.has("k") is False

    def test_has_at_runtime(self):
        s = SettingsLayer()
        s.set_runtime("k", 1)
        assert s.has("k") is True


class TestAllKeys:
    def test_empty(self):
        s = SettingsLayer()
        assert s.all_keys() == set()

    def test_union_across_layers(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        s.load_file_layer({"b": 2})
        s.set_user("c", 3)
        s.set_runtime("d", 4)
        assert s.all_keys() == {"a", "b", "c", "d"}

    def test_no_duplicates(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        s.set_user("a", 2)
        s.set_runtime("a", 3)
        assert s.all_keys() == {"a"}


class TestEffectiveSettings:
    def test_empty(self):
        s = SettingsLayer()
        assert s.effective_settings() == {}

    def test_resolves_all_keys(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        s.set_user("b", 2)
        result = s.effective_settings()
        assert result == {"a": 1, "b": 2}

    def test_uses_highest_priority(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        s.set_runtime("a", 99)
        assert s.effective_settings()["a"] == 99


class TestLayerValues:
    def test_empty_layer(self):
        s = SettingsLayer()
        assert s.layer_values(LayerName.USER) == {}

    def test_returns_layer_only(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        s.set_user("b", 2)
        assert s.layer_values(LayerName.DEFAULTS) == {"a": 1}
        assert s.layer_values(LayerName.USER) == {"b": 2}

    def test_returns_copy(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        d = s.layer_values(LayerName.DEFAULTS)
        d["a"] = 999
        assert s.get("a") == 1


class TestClearLayer:
    def test_clear_empty_returns_zero(self):
        s = SettingsLayer()
        assert s.clear_layer(LayerName.USER) == 0

    def test_clear_count(self):
        s = SettingsLayer()
        s.set_user("a", 1)
        s.set_user("b", 2)
        assert s.clear_layer(LayerName.USER) == 2

    def test_clear_makes_unresolved(self):
        s = SettingsLayer()
        s.set_user("a", 1)
        s.clear_layer(LayerName.USER)
        assert s.has("a") is False

    def test_clear_reveals_lower_layer(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        s.set_user("a", 99)
        s.clear_layer(LayerName.USER)
        assert s.get("a") == 1
        assert s.get_layer("a") == LayerName.DEFAULTS


class TestClearAll:
    def test_clear_all(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        s.set_user("b", 2)
        s.set_runtime("c", 3)
        s.clear_all()
        assert s.all_keys() == set()

    def test_clear_all_empty(self):
        s = SettingsLayer()
        s.clear_all()  # should not raise
        assert s.all_keys() == set()


class TestSubscribe:
    def test_basic_subscription(self):
        s = SettingsLayer()
        events = []
        s.subscribe("k", lambda key, old, new: events.append((key, old, new)))
        s.set_user("k", 1)
        assert events == [("k", None, 1)]

    def test_subscription_fires_on_change(self):
        s = SettingsLayer()
        events = []
        s.subscribe("k", lambda key, old, new: events.append((key, old, new)))
        s.set_user("k", 1)
        s.set_user("k", 2)
        assert len(events) == 2
        assert events[1] == ("k", 1, 2)

    def test_no_fire_when_same_value(self):
        s = SettingsLayer()
        events = []
        s.subscribe("k", lambda key, old, new: events.append((key, old, new)))
        s.set_user("k", 1)
        s.set_user("k", 1)
        assert len(events) == 1

    def test_subscription_only_for_subscribed_key(self):
        s = SettingsLayer()
        events = []
        s.subscribe("a", lambda key, old, new: events.append(key))
        s.set_user("b", 1)
        assert events == []

    def test_wildcard_subscription(self):
        s = SettingsLayer()
        events = []
        s.subscribe("*", lambda key, old, new: events.append(key))
        s.set_user("a", 1)
        s.set_user("b", 2)
        assert events == ["a", "b"]

    def test_subscription_fires_on_runtime(self):
        s = SettingsLayer()
        events = []
        s.subscribe("k", lambda key, old, new: events.append((key, old, new)))
        s.set_runtime("k", 5)
        assert events == [("k", None, 5)]

    def test_subscription_on_file_load(self):
        s = SettingsLayer()
        events = []
        s.subscribe("k", lambda key, old, new: events.append((old, new)))
        s.load_file_layer({"k": 1})
        assert events == [(None, 1)]

    def test_subscription_on_env_load(self):
        s = SettingsLayer()
        events = []
        s.subscribe("k", lambda key, old, new: events.append((old, new)))
        s.load_env_layer({"K": "1"})
        assert events == [(None, "1")]

    def test_subscription_no_fire_when_effective_unchanged(self):
        s = SettingsLayer()
        events = []
        s.set_runtime("k", "rt")
        s.subscribe("k", lambda key, old, new: events.append(1))
        # Setting file/env/user/default below runtime should not fire
        s.set_default("k", "d")
        s.load_file_layer({"k": "f"})
        s.load_env_layer({"K": "e"})
        s.set_user("k", "u")
        assert events == []

    def test_subscription_id_unique(self):
        s = SettingsLayer()
        cb = lambda k, o, n: None
        id1 = s.subscribe("a", cb)
        id2 = s.subscribe("b", cb)
        assert id1 != id2

    def test_callback_exception_doesnt_break(self):
        s = SettingsLayer()
        def bad(k, o, n):
            raise RuntimeError("boom")
        events = []
        s.subscribe("k", bad)
        s.subscribe("k", lambda k, o, n: events.append(n))
        s.set_user("k", 1)
        assert events == [1]


class TestUnsubscribe:
    def test_unsubscribe_returns_true(self):
        s = SettingsLayer()
        sid = s.subscribe("k", lambda k, o, n: None)
        assert s.unsubscribe(sid) is True

    def test_unsubscribe_invalid(self):
        s = SettingsLayer()
        assert s.unsubscribe(99999) is False

    def test_unsubscribe_stops_notifications(self):
        s = SettingsLayer()
        events = []
        sid = s.subscribe("k", lambda k, o, n: events.append(n))
        s.set_user("k", 1)
        s.unsubscribe(sid)
        s.set_user("k", 2)
        assert events == [1]

    def test_double_unsubscribe(self):
        s = SettingsLayer()
        sid = s.subscribe("k", lambda k, o, n: None)
        assert s.unsubscribe(sid) is True
        assert s.unsubscribe(sid) is False


class TestExportImport:
    def test_export_empty(self):
        s = SettingsLayer()
        data = s.export()
        assert set(data.keys()) == {l.value for l in LayerName}
        for v in data.values():
            assert v == {}

    def test_export_with_data(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        s.set_user("b", 2)
        data = s.export()
        assert data["defaults"] == {"a": 1}
        assert data["user"] == {"b": 2}

    def test_round_trip(self):
        s1 = SettingsLayer()
        s1.set_default("a", 1)
        s1.load_file_layer({"b": "x"})
        s1.set_user("c", True)
        s1.set_runtime("d", 3.14)
        data = s1.export()

        s2 = SettingsLayer()
        s2.import_(data)
        assert s2.get("a") == 1
        assert s2.get("b") == "x"
        assert s2.get("c") is True
        assert s2.get("d") == 3.14
        assert s2.get_layer("a") == LayerName.DEFAULTS
        assert s2.get_layer("b") == LayerName.FILE

    def test_import_clears_first(self):
        s = SettingsLayer()
        s.set_user("old", 1)
        s.import_({"defaults": {"new": 2}})
        assert s.has("old") is False
        assert s.get("new") == 2

    def test_import_ignores_unknown_layer(self):
        s = SettingsLayer()
        s.import_({"unknown_layer": {"a": 1}, "defaults": {"b": 2}})
        assert s.get("b") == 2
        assert s.has("a") is False


class TestEdgeCases:
    def test_empty_settings(self):
        s = SettingsLayer()
        assert s.all_keys() == set()
        assert s.effective_settings() == {}
        assert s.get("any") is None

    def test_none_as_value(self):
        s = SettingsLayer()
        s.set_user("k", None)
        assert s.get("k") is None
        assert s.has("k") is True
        assert s.get_layer("k") == LayerName.USER

    def test_complex_value(self):
        s = SettingsLayer()
        s.set_user("k", {"nested": [1, 2, 3]})
        assert s.get("k") == {"nested": [1, 2, 3]}

    def test_type_coerce_failure_keeps_raw(self):
        s = SettingsLayer()
        s.set_default("port", 8080)
        s.load_env_layer({"PORT": "not-an-int"})
        # Coercion failed, original string preserved
        assert s.get("port") == "not-an-int"

    def test_coerce_no_default_uses_raw(self):
        s = SettingsLayer()
        s.load_env_layer({"X": "123"})
        assert s.get("x") == "123"

    def test_thread_safety_concurrent_writes(self):
        s = SettingsLayer()
        def worker(i):
            for j in range(20):
                s.set_runtime(f"k_{i}_{j}", j)
        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(s.all_keys()) == 5 * 20

    def test_layer_values_independent_dicts(self):
        s = SettingsLayer()
        s.set_default("a", 1)
        s.set_user("a", 2)
        assert s.layer_values(LayerName.DEFAULTS) == {"a": 1}
        assert s.layer_values(LayerName.USER) == {"a": 2}

    def test_get_setting_after_clear(self):
        s = SettingsLayer()
        s.set_user("a", 1)
        s.clear_layer(LayerName.USER)
        assert s.get_setting("a") is None

    def test_env_no_prefix(self):
        s = SettingsLayer()
        s.load_env_layer({"FOO": "1", "BAR": "2"})
        assert s.get("foo") == "1"
        assert s.get("bar") == "2"

    def test_bool_coerce_various(self):
        s = SettingsLayer()
        s.set_default("a", False)
        s.load_env_layer({"A": "yes"})
        assert s.get("a") is True

    def test_clear_layer_fires_subscription_when_change(self):
        s = SettingsLayer()
        s.set_user("k", "user_val")
        events = []
        s.subscribe("k", lambda key, old, new: events.append((old, new)))
        s.clear_layer(LayerName.USER)
        assert events == [("user_val", None)]

    def test_clear_layer_reveals_lower_fires_change(self):
        s = SettingsLayer()
        s.set_default("k", "default_val")
        s.set_user("k", "user_val")
        events = []
        s.subscribe("k", lambda key, old, new: events.append((old, new)))
        s.clear_layer(LayerName.USER)
        assert events == [("user_val", "default_val")]
