"""Tests for E278 DocSettingsStore."""
import threading
from docstoolkit.doc_settings_store import (
    DocSettingsStore,
    SettingValue,
    SettingSchema,
    SettingsStoreStats,
)

T0 = 1_700_000_000.0


def _store() -> DocSettingsStore:
    return DocSettingsStore(db_path=":memory:")


# ---------------------------------------------------------------------------
# Basic set / get
# ---------------------------------------------------------------------------


def test_set_returns_setting_value():
    s = _store()
    sv = s.set("doc:1", "color", "red", now=T0)
    assert isinstance(sv, SettingValue)


def test_set_get_roundtrip_str():
    s = _store()
    s.set("doc:1", "title", "Hello World", now=T0)
    assert s.get("doc:1", "title") == "Hello World"


def test_set_get_roundtrip_int():
    s = _store()
    s.set("doc:1", "version", 42, now=T0)
    assert s.get("doc:1", "version") == 42


def test_set_get_roundtrip_float():
    s = _store()
    s.set("doc:1", "score", 3.14, now=T0)
    assert abs(s.get("doc:1", "score") - 3.14) < 1e-9


def test_set_get_roundtrip_bool_true():
    s = _store()
    s.set("doc:1", "published", True, now=T0)
    assert s.get("doc:1", "published") is True


def test_set_get_roundtrip_bool_false():
    s = _store()
    s.set("doc:1", "published", False, now=T0)
    assert s.get("doc:1", "published") is False


def test_set_get_roundtrip_json():
    s = _store()
    s.register_schema("meta", "json")
    s.set("doc:1", "meta", {"key": [1, 2]}, now=T0)
    assert s.get("doc:1", "meta") == {"key": [1, 2]}


def test_get_missing_returns_default():
    s = _store()
    assert s.get("doc:1", "nope", default="fallback") == "fallback"


def test_get_missing_returns_none_by_default():
    s = _store()
    assert s.get("doc:1", "nope") is None


def test_set_overwrites_existing():
    s = _store()
    s.set("doc:1", "title", "First", now=T0)
    s.set("doc:1", "title", "Second", now=T0 + 1)
    assert s.get("doc:1", "title") == "Second"


def test_set_stores_timestamp():
    s = _store()
    sv = s.set("doc:1", "key", "val", now=T0)
    assert sv.set_at == T0


# ---------------------------------------------------------------------------
# get_value
# ---------------------------------------------------------------------------


def test_get_value_returns_setting_value():
    s = _store()
    s.set("doc:1", "x", 7, now=T0)
    sv = s.get_value("doc:1", "x")
    assert isinstance(sv, SettingValue)
    assert sv.value == 7
    assert sv.doc_id == "doc:1"
    assert sv.key == "x"


def test_get_value_missing_returns_none():
    s = _store()
    assert s.get_value("doc:1", "missing") is None


# ---------------------------------------------------------------------------
# has
# ---------------------------------------------------------------------------


def test_has_existing_returns_true():
    s = _store()
    s.set("doc:1", "k", "v", now=T0)
    assert s.has("doc:1", "k") is True


def test_has_missing_returns_false():
    s = _store()
    assert s.has("doc:1", "k") is False


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


def test_delete_existing_returns_true():
    s = _store()
    s.set("doc:1", "k", "v", now=T0)
    assert s.delete("doc:1", "k") is True


def test_delete_removes_setting():
    s = _store()
    s.set("doc:1", "k", "v", now=T0)
    s.delete("doc:1", "k")
    assert s.has("doc:1", "k") is False


def test_delete_missing_returns_false():
    s = _store()
    assert s.delete("doc:1", "k") is False


# ---------------------------------------------------------------------------
# delete_doc
# ---------------------------------------------------------------------------


def test_delete_doc_removes_all_settings():
    s = _store()
    s.set("doc:1", "a", 1, now=T0)
    s.set("doc:1", "b", 2, now=T0)
    count = s.delete_doc("doc:1")
    assert count == 2
    assert s.keys_for_doc("doc:1") == []


def test_delete_doc_missing_returns_zero():
    s = _store()
    assert s.delete_doc("no-such") == 0


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


def test_register_schema_returns_schema():
    s = _store()
    schema = s.register_schema("priority", "int", default=0)
    assert isinstance(schema, SettingSchema)
    assert schema.key == "priority"
    assert schema.value_type == "int"


def test_schema_default_returned_when_not_set():
    s = _store()
    s.register_schema("priority", "int", default=5)
    assert s.get("doc:1", "priority") == 5


def test_schema_default_overridden_by_set_value():
    s = _store()
    s.register_schema("priority", "int", default=5)
    s.set("doc:1", "priority", 99, now=T0)
    assert s.get("doc:1", "priority") == 99


def test_register_schema_replaces_existing():
    s = _store()
    s.register_schema("flag", "bool", default=False)
    s.register_schema("flag", "bool", default=True)
    schema = s.get_schema("flag")
    assert schema.default is True


def test_register_schema_invalid_type_raises():
    s = _store()
    try:
        s.register_schema("k", "uuid")
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_get_schema_returns_schema():
    s = _store()
    s.register_schema("level", "str", default="low")
    schema = s.get_schema("level")
    assert schema is not None
    assert schema.value_type == "str"


def test_get_schema_missing_returns_none():
    s = _store()
    assert s.get_schema("no-such") is None


def test_schemas_returns_sorted_list():
    s = _store()
    s.register_schema("z_key", "str")
    s.register_schema("a_key", "int")
    keys = [sch.key for sch in s.schemas()]
    assert keys == sorted(keys)


def test_schema_required_flag():
    s = _store()
    s.register_schema("must_have", "str", required=True)
    errors = s.validate("doc:1")
    assert any("must_have" in err for err in errors)


def test_validate_no_errors_when_required_present():
    s = _store()
    s.register_schema("must_have", "str", required=True)
    s.set("doc:1", "must_have", "ok", now=T0)
    errors = s.validate("doc:1")
    assert errors == []


# ---------------------------------------------------------------------------
# keys_for_doc / docs_with_setting
# ---------------------------------------------------------------------------


def test_keys_for_doc_returns_sorted_keys():
    s = _store()
    s.set("doc:1", "beta", 1, now=T0)
    s.set("doc:1", "alpha", 2, now=T0)
    assert s.keys_for_doc("doc:1") == ["alpha", "beta"]


def test_keys_for_doc_empty_returns_empty():
    s = _store()
    assert s.keys_for_doc("no-such") == []


def test_docs_with_setting_returns_sorted():
    s = _store()
    s.set("doc:2", "color", "red", now=T0)
    s.set("doc:1", "color", "blue", now=T0)
    result = s.docs_with_setting("color")
    assert result == sorted(result)
    assert "doc:1" in result
    assert "doc:2" in result


def test_docs_with_value_exact_match():
    s = _store()
    s.set("doc:1", "status", "active", now=T0)
    s.set("doc:2", "status", "inactive", now=T0)
    s.set("doc:3", "status", "active", now=T0)
    result = s.docs_with_value("status", "active")
    assert "doc:1" in result
    assert "doc:3" in result
    assert "doc:2" not in result


# ---------------------------------------------------------------------------
# bulk_set
# ---------------------------------------------------------------------------


def test_bulk_set_returns_count():
    s = _store()
    count = s.bulk_set("doc:1", {"a": 1, "b": 2, "c": 3}, now=T0)
    assert count == 3


def test_bulk_set_values_retrievable():
    s = _store()
    s.bulk_set("doc:1", {"x": 10, "y": 20}, now=T0)
    assert s.get("doc:1", "x") == 10
    assert s.get("doc:1", "y") == 20


def test_bulk_set_empty_returns_zero():
    s = _store()
    assert s.bulk_set("doc:1", {}) == 0


# ---------------------------------------------------------------------------
# inherit
# ---------------------------------------------------------------------------


def test_inherit_copies_settings():
    s = _store()
    s.set("parent", "theme", "dark", now=T0)
    s.set("parent", "lang", "en", now=T0)
    copied = s.inherit("child", "parent", now=T0)
    assert copied == 2
    assert s.get("child", "theme") == "dark"
    assert s.get("child", "lang") == "en"


def test_inherit_no_override_by_default():
    s = _store()
    s.set("parent", "theme", "dark", now=T0)
    s.set("child", "theme", "light", now=T0)
    s.inherit("child", "parent", override=False, now=T0)
    assert s.get("child", "theme") == "light"


def test_inherit_with_override_replaces():
    s = _store()
    s.set("parent", "theme", "dark", now=T0)
    s.set("child", "theme", "light", now=T0)
    s.inherit("child", "parent", override=True, now=T0)
    assert s.get("child", "theme") == "dark"


def test_inherit_missing_parent_returns_zero():
    s = _store()
    assert s.inherit("child", "no-parent", now=T0) == 0


# ---------------------------------------------------------------------------
# stats / total_docs / total_settings
# ---------------------------------------------------------------------------


def test_stats_returns_settings_store_stats():
    s = _store()
    assert isinstance(s.stats(), SettingsStoreStats)


def test_total_docs_property():
    s = _store()
    s.set("doc:1", "k", "v", now=T0)
    s.set("doc:2", "k", "v", now=T0)
    assert s.total_docs == 2


def test_total_settings_property():
    s = _store()
    s.set("doc:1", "a", 1, now=T0)
    s.set("doc:1", "b", 2, now=T0)
    assert s.total_settings == 2


def test_stats_avg_settings_per_doc():
    s = _store()
    s.set("doc:1", "a", 1, now=T0)
    s.set("doc:1", "b", 2, now=T0)
    s.set("doc:2", "a", 3, now=T0)
    st = s.stats()
    assert abs(st.avg_settings_per_doc - 1.5) < 1e-9


def test_stats_zero_docs():
    s = _store()
    st = s.stats()
    assert st.total_docs == 0
    assert st.avg_settings_per_doc == 0.0


# ---------------------------------------------------------------------------
# close
# ---------------------------------------------------------------------------


def test_close_does_not_raise():
    s = _store()
    s.set("doc:1", "k", "v", now=T0)
    s.close()


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_concurrent_set():
    s = _store()
    errors = []

    def worker(doc_id: str):
        try:
            for i in range(20):
                s.set(doc_id, f"k{i}", i, now=T0)
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(f"doc:{t}",)) for t in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert s.total_docs == 5
