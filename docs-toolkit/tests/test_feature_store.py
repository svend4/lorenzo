"""Tests for the feature_store module (E76)."""

from __future__ import annotations

import time
import pytest

from docstoolkit.feature_store import (
    FeatureType,
    FeatureDefinition,
    FeatureValue,
    FeatureStore,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_store() -> FeatureStore:
    """Return a fresh in-memory FeatureStore."""
    return FeatureStore()


def sample_def(
    name: str = "age",
    feature_type: FeatureType = FeatureType.NUMERIC,
    description: str = "Age in years",
    default_value=None,
    tags: list[str] | None = None,
) -> FeatureDefinition:
    return FeatureDefinition(
        name=name,
        feature_type=feature_type,
        description=description,
        default_value=default_value,
        tags=tags or [],
    )


def sample_fv(
    entity_id: str = "user:1",
    feature_name: str = "age",
    value=25,
    version: int = 1,
) -> FeatureValue:
    return FeatureValue(
        entity_id=entity_id,
        feature_name=feature_name,
        value=value,
        version=version,
    )


# ===========================================================================
# FeatureType tests
# ===========================================================================

class TestFeatureType:
    def test_numeric_value(self):
        assert FeatureType.NUMERIC.value == "numeric"

    def test_categorical_value(self):
        assert FeatureType.CATEGORICAL.value == "categorical"

    def test_binary_value(self):
        assert FeatureType.BINARY.value == "binary"

    def test_text_value(self):
        assert FeatureType.TEXT.value == "text"

    def test_vector_value(self):
        assert FeatureType.VECTOR.value == "vector"

    def test_all_members(self):
        members = {ft.value for ft in FeatureType}
        assert members == {"numeric", "categorical", "binary", "text", "vector"}

    def test_from_string(self):
        assert FeatureType("numeric") is FeatureType.NUMERIC

    def test_enum_identity(self):
        assert FeatureType.NUMERIC is FeatureType.NUMERIC


# ===========================================================================
# FeatureDefinition tests
# ===========================================================================

class TestFeatureDefinition:
    def test_required_fields(self):
        fd = FeatureDefinition(name="score", feature_type=FeatureType.NUMERIC)
        assert fd.name == "score"
        assert fd.feature_type is FeatureType.NUMERIC

    def test_description_default(self):
        fd = FeatureDefinition(name="x", feature_type=FeatureType.TEXT)
        assert fd.description == ""

    def test_default_value_default(self):
        fd = FeatureDefinition(name="x", feature_type=FeatureType.NUMERIC)
        assert fd.default_value is None

    def test_tags_default_empty_list(self):
        fd = FeatureDefinition(name="x", feature_type=FeatureType.NUMERIC)
        assert fd.tags == []

    def test_tags_default_is_independent(self):
        fd1 = FeatureDefinition(name="a", feature_type=FeatureType.NUMERIC)
        fd2 = FeatureDefinition(name="b", feature_type=FeatureType.NUMERIC)
        fd1.tags.append("tag1")
        assert fd2.tags == []

    def test_custom_description(self):
        fd = FeatureDefinition(name="x", feature_type=FeatureType.TEXT, description="My feature")
        assert fd.description == "My feature"

    def test_custom_default_value(self):
        fd = FeatureDefinition(name="x", feature_type=FeatureType.NUMERIC, default_value=0.0)
        assert fd.default_value == 0.0

    def test_custom_tags(self):
        fd = FeatureDefinition(name="x", feature_type=FeatureType.NUMERIC, tags=["ml", "online"])
        assert "ml" in fd.tags
        assert "online" in fd.tags

    def test_all_feature_types_accepted(self):
        for ft in FeatureType:
            fd = FeatureDefinition(name="f", feature_type=ft)
            assert fd.feature_type is ft


# ===========================================================================
# FeatureValue tests
# ===========================================================================

class TestFeatureValue:
    def test_required_fields(self):
        fv = FeatureValue(entity_id="u1", feature_name="age", value=30)
        assert fv.entity_id == "u1"
        assert fv.feature_name == "age"
        assert fv.value == 30

    def test_ts_auto_set(self):
        before = time.time()
        fv = FeatureValue(entity_id="u1", feature_name="age", value=30)
        after = time.time()
        assert before <= fv.ts <= after

    def test_version_default(self):
        fv = FeatureValue(entity_id="u1", feature_name="age", value=30)
        assert fv.version == 1

    def test_custom_ts(self):
        fv = FeatureValue(entity_id="u1", feature_name="age", value=30, ts=1000.0)
        assert fv.ts == 1000.0

    def test_custom_version(self):
        fv = FeatureValue(entity_id="u1", feature_name="age", value=30, version=5)
        assert fv.version == 5

    def test_none_value(self):
        fv = FeatureValue(entity_id="u1", feature_name="age", value=None)
        assert fv.value is None

    def test_list_value(self):
        fv = FeatureValue(entity_id="u1", feature_name="emb", value=[1.0, 2.0, 3.0])
        assert fv.value == [1.0, 2.0, 3.0]

    def test_bool_value(self):
        fv = FeatureValue(entity_id="u1", feature_name="active", value=True)
        assert fv.value is True


# ===========================================================================
# FeatureStore — construction
# ===========================================================================

class TestFeatureStoreInit:
    def test_default_in_memory(self):
        fs = FeatureStore()
        assert fs.entities() == []
        fs.close()

    def test_explicit_memory(self):
        fs = FeatureStore(":memory:")
        assert fs.entities() == []
        fs.close()

    def test_file_db(self, tmp_path):
        db = tmp_path / "test.db"
        fs = FeatureStore(db)
        fs.write(sample_fv())
        fs.close()
        # Reopen and verify persistence
        fs2 = FeatureStore(db)
        result = fs2.read("user:1", "age")
        assert result is not None
        assert result.value == 25
        fs2.close()

    def test_path_object(self, tmp_path):
        from pathlib import Path
        db = Path(tmp_path) / "test2.db"
        fs = FeatureStore(db)
        fs.close()


# ===========================================================================
# FeatureStore — register / get_definition / list_definitions
# ===========================================================================

class TestRegisterDefinition:
    def test_register_and_get(self):
        fs = make_store()
        fd = sample_def()
        fs.register(fd)
        result = fs.get_definition("age")
        assert result is not None
        assert result.name == "age"
        assert result.feature_type is FeatureType.NUMERIC
        fs.close()

    def test_get_unknown_returns_none(self):
        fs = make_store()
        assert fs.get_definition("nonexistent") is None
        fs.close()

    def test_register_upsert_updates_description(self):
        fs = make_store()
        fs.register(sample_def(description="old"))
        fs.register(sample_def(description="new"))
        result = fs.get_definition("age")
        assert result.description == "new"
        fs.close()

    def test_register_upsert_updates_type(self):
        fs = make_store()
        fs.register(sample_def(feature_type=FeatureType.NUMERIC))
        fd2 = FeatureDefinition(name="age", feature_type=FeatureType.CATEGORICAL)
        fs.register(fd2)
        result = fs.get_definition("age")
        assert result.feature_type is FeatureType.CATEGORICAL
        fs.close()

    def test_register_upsert_updates_tags(self):
        fs = make_store()
        fs.register(sample_def(tags=["a"]))
        fs.register(sample_def(tags=["b", "c"]))
        result = fs.get_definition("age")
        assert result.tags == ["b", "c"]
        fs.close()

    def test_register_with_default_value(self):
        fs = make_store()
        fd = sample_def(default_value=42.0)
        fs.register(fd)
        result = fs.get_definition("age")
        assert result.default_value == 42.0
        fs.close()

    def test_register_with_none_default_value(self):
        fs = make_store()
        fd = sample_def(default_value=None)
        fs.register(fd)
        result = fs.get_definition("age")
        assert result.default_value is None
        fs.close()

    def test_list_definitions_empty(self):
        fs = make_store()
        assert fs.list_definitions() == []
        fs.close()

    def test_list_definitions_multiple(self):
        fs = make_store()
        fs.register(sample_def("age", FeatureType.NUMERIC))
        fs.register(sample_def("name", FeatureType.TEXT))
        defs = fs.list_definitions()
        assert len(defs) == 2
        names = {d.name for d in defs}
        assert names == {"age", "name"}
        fs.close()

    def test_list_definitions_sorted_by_name(self):
        fs = make_store()
        fs.register(sample_def("z_feat", FeatureType.NUMERIC))
        fs.register(sample_def("a_feat", FeatureType.NUMERIC))
        defs = fs.list_definitions()
        assert defs[0].name == "a_feat"
        assert defs[1].name == "z_feat"
        fs.close()

    def test_list_definitions_with_tag_filter(self):
        fs = make_store()
        fs.register(sample_def("age", tags=["ml"]))
        fs.register(sample_def("name", tags=["ui"]))
        fs.register(sample_def("score", tags=["ml", "online"]))
        defs = fs.list_definitions(tag="ml")
        names = {d.name for d in defs}
        assert names == {"age", "score"}
        fs.close()

    def test_list_definitions_tag_filter_no_match(self):
        fs = make_store()
        fs.register(sample_def("age", tags=["ml"]))
        defs = fs.list_definitions(tag="nonexistent")
        assert defs == []
        fs.close()

    def test_list_definitions_no_tag_returns_all(self):
        fs = make_store()
        fs.register(sample_def("age", tags=["ml"]))
        fs.register(sample_def("name", tags=[]))
        defs = fs.list_definitions(tag=None)
        assert len(defs) == 2
        fs.close()

    def test_definition_description_roundtrip(self):
        fs = make_store()
        fs.register(sample_def(description="User age feature"))
        result = fs.get_definition("age")
        assert result.description == "User age feature"
        fs.close()


# ===========================================================================
# FeatureStore — write / read
# ===========================================================================

class TestWriteRead:
    def test_write_and_read(self):
        fs = make_store()
        fv = sample_fv()
        fs.write(fv)
        result = fs.read("user:1", "age")
        assert result is not None
        assert result.entity_id == "user:1"
        assert result.feature_name == "age"
        assert result.value == 25
        fs.close()

    def test_read_nonexistent_returns_none(self):
        fs = make_store()
        assert fs.read("ghost", "age") is None
        fs.close()

    def test_read_wrong_entity_returns_none(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="user:1"))
        assert fs.read("user:2", "age") is None
        fs.close()

    def test_read_wrong_feature_returns_none(self):
        fs = make_store()
        fs.write(sample_fv(feature_name="age"))
        assert fs.read("user:1", "score") is None
        fs.close()

    def test_upsert_updates_value(self):
        fs = make_store()
        fs.write(sample_fv(value=25))
        fs.write(sample_fv(value=26))
        result = fs.read("user:1", "age")
        assert result.value == 26
        fs.close()

    def test_upsert_updates_ts(self):
        fs = make_store()
        fs.write(FeatureValue(entity_id="u1", feature_name="f", value=1, ts=100.0))
        fs.write(FeatureValue(entity_id="u1", feature_name="f", value=2, ts=200.0))
        result = fs.read("u1", "f")
        assert result.ts == 200.0
        fs.close()

    def test_upsert_updates_version(self):
        fs = make_store()
        fs.write(FeatureValue(entity_id="u1", feature_name="f", value=1, version=1))
        fs.write(FeatureValue(entity_id="u1", feature_name="f", value=1, version=2))
        result = fs.read("u1", "f")
        assert result.version == 2
        fs.close()

    def test_ts_roundtrip(self):
        fs = make_store()
        ts = 1700000000.123456
        fv = FeatureValue(entity_id="u1", feature_name="f", value=1, ts=ts)
        fs.write(fv)
        result = fs.read("u1", "f")
        assert abs(result.ts - ts) < 1e-6
        fs.close()

    def test_version_roundtrip(self):
        fs = make_store()
        fv = FeatureValue(entity_id="u1", feature_name="f", value=1, version=7)
        fs.write(fv)
        result = fs.read("u1", "f")
        assert result.version == 7
        fs.close()


# ===========================================================================
# FeatureStore — JSON serialization by FeatureType
# ===========================================================================

class TestJsonSerialization:
    def test_numeric_int(self):
        fs = make_store()
        fs.write(sample_fv(value=42))
        assert fs.read("user:1", "age").value == 42
        fs.close()

    def test_numeric_float(self):
        fs = make_store()
        fs.write(sample_fv(value=3.14))
        assert fs.read("user:1", "age").value == pytest.approx(3.14)
        fs.close()

    def test_numeric_zero(self):
        fs = make_store()
        fs.write(sample_fv(value=0))
        assert fs.read("user:1", "age").value == 0
        fs.close()

    def test_categorical_string(self):
        fs = make_store()
        fs.write(sample_fv(feature_name="category", value="premium"))
        assert fs.read("user:1", "category").value == "premium"
        fs.close()

    def test_categorical_empty_string(self):
        fs = make_store()
        fs.write(sample_fv(feature_name="cat", value=""))
        assert fs.read("user:1", "cat").value == ""
        fs.close()

    def test_binary_true(self):
        fs = make_store()
        fs.write(sample_fv(feature_name="active", value=True))
        assert fs.read("user:1", "active").value is True
        fs.close()

    def test_binary_false(self):
        fs = make_store()
        fs.write(sample_fv(feature_name="active", value=False))
        assert fs.read("user:1", "active").value is False
        fs.close()

    def test_text_value(self):
        fs = make_store()
        fs.write(sample_fv(feature_name="bio", value="Hello world"))
        assert fs.read("user:1", "bio").value == "Hello world"
        fs.close()

    def test_text_unicode(self):
        fs = make_store()
        fs.write(sample_fv(feature_name="bio", value="Привет мир 🌍"))
        assert fs.read("user:1", "bio").value == "Привет мир 🌍"
        fs.close()

    def test_vector_float_list(self):
        fs = make_store()
        vec = [0.1, 0.2, 0.3, 0.4]
        fs.write(sample_fv(feature_name="emb", value=vec))
        result = fs.read("user:1", "emb")
        assert len(result.value) == 4
        assert result.value[0] == pytest.approx(0.1)
        fs.close()

    def test_vector_large(self):
        fs = make_store()
        vec = [float(i) / 100 for i in range(768)]
        fs.write(sample_fv(feature_name="emb", value=vec))
        result = fs.read("user:1", "emb")
        assert len(result.value) == 768
        fs.close()

    def test_none_value_roundtrip(self):
        fs = make_store()
        fs.write(sample_fv(value=None))
        assert fs.read("user:1", "age").value is None
        fs.close()

    def test_dict_value_roundtrip(self):
        fs = make_store()
        d = {"key": "val", "num": 1}
        fs.write(sample_fv(value=d))
        assert fs.read("user:1", "age").value == d
        fs.close()


# ===========================================================================
# FeatureStore — write_batch
# ===========================================================================

class TestWriteBatch:
    def test_write_batch_single(self):
        fs = make_store()
        fs.write_batch([sample_fv()])
        assert fs.read("user:1", "age") is not None
        fs.close()

    def test_write_batch_multiple(self):
        fs = make_store()
        fvs = [
            sample_fv(entity_id="u1", feature_name="age", value=20),
            sample_fv(entity_id="u2", feature_name="age", value=30),
            sample_fv(entity_id="u1", feature_name="score", value=0.9),
        ]
        fs.write_batch(fvs)
        assert fs.read("u1", "age").value == 20
        assert fs.read("u2", "age").value == 30
        assert fs.read("u1", "score").value == pytest.approx(0.9)
        fs.close()

    def test_write_batch_empty(self):
        fs = make_store()
        fs.write_batch([])  # should not raise
        assert fs.entities() == []
        fs.close()

    def test_write_batch_upsert(self):
        fs = make_store()
        fs.write_batch([sample_fv(value=10)])
        fs.write_batch([sample_fv(value=20)])
        assert fs.read("user:1", "age").value == 20
        fs.close()

    def test_write_batch_atomicity_reflected(self):
        fs = make_store()
        fvs = [sample_fv(entity_id=f"u{i}", feature_name="x", value=i) for i in range(100)]
        fs.write_batch(fvs)
        assert len(fs.entities()) == 100
        fs.close()


# ===========================================================================
# FeatureStore — read_entity
# ===========================================================================

class TestReadEntity:
    def test_read_entity_all_features(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=25))
        fs.write(sample_fv(entity_id="u1", feature_name="score", value=0.8))
        result = fs.read_entity("u1")
        assert set(result.keys()) == {"age", "score"}
        fs.close()

    def test_read_entity_unknown_returns_empty(self):
        fs = make_store()
        assert fs.read_entity("ghost") == {}
        fs.close()

    def test_read_entity_returns_correct_values(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=25))
        result = fs.read_entity("u1")
        assert result["age"].value == 25
        fs.close()

    def test_read_entity_only_own_features(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=25))
        fs.write(sample_fv(entity_id="u2", feature_name="age", value=30))
        result = fs.read_entity("u1")
        assert len(result) == 1
        assert result["age"].entity_id == "u1"
        fs.close()

    def test_read_entity_returns_feature_values(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=25))
        result = fs.read_entity("u1")
        assert isinstance(result["age"], FeatureValue)
        fs.close()


# ===========================================================================
# FeatureStore — read_feature
# ===========================================================================

class TestReadFeature:
    def test_read_feature_all_entities(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=20))
        fs.write(sample_fv(entity_id="u2", feature_name="age", value=30))
        results = fs.read_feature("age")
        ids = {fv.entity_id for fv in results}
        assert ids == {"u1", "u2"}
        fs.close()

    def test_read_feature_empty(self):
        fs = make_store()
        assert fs.read_feature("age") == []
        fs.close()

    def test_read_feature_filter_entity_ids(self):
        fs = make_store()
        for i in range(5):
            fs.write(sample_fv(entity_id=f"u{i}", feature_name="age", value=i))
        results = fs.read_feature("age", entity_ids=["u1", "u3"])
        ids = {fv.entity_id for fv in results}
        assert ids == {"u1", "u3"}
        fs.close()

    def test_read_feature_empty_entity_ids_list(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=20))
        results = fs.read_feature("age", entity_ids=[])
        assert results == []
        fs.close()

    def test_read_feature_unknown_feature(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=20))
        results = fs.read_feature("score")
        assert results == []
        fs.close()

    def test_read_feature_values_correct(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=42))
        results = fs.read_feature("age")
        assert results[0].value == 42
        fs.close()

    def test_read_feature_filter_nonexistent_entity(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=20))
        results = fs.read_feature("age", entity_ids=["ghost"])
        assert results == []
        fs.close()


# ===========================================================================
# FeatureStore — delete
# ===========================================================================

class TestDelete:
    def test_delete_existing(self):
        fs = make_store()
        fs.write(sample_fv())
        result = fs.delete("user:1", "age")
        assert result is True
        assert fs.read("user:1", "age") is None
        fs.close()

    def test_delete_nonexistent_returns_false(self):
        fs = make_store()
        assert fs.delete("ghost", "age") is False
        fs.close()

    def test_delete_removes_from_entity(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=25))
        fs.write(sample_fv(entity_id="u1", feature_name="score", value=0.9))
        fs.delete("u1", "age")
        entity = fs.read_entity("u1")
        assert "age" not in entity
        assert "score" in entity
        fs.close()

    def test_delete_does_not_affect_other_entity(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=25))
        fs.write(sample_fv(entity_id="u2", feature_name="age", value=30))
        fs.delete("u1", "age")
        assert fs.read("u2", "age") is not None
        fs.close()

    def test_delete_twice_returns_false_second_time(self):
        fs = make_store()
        fs.write(sample_fv())
        fs.delete("user:1", "age")
        assert fs.delete("user:1", "age") is False
        fs.close()


# ===========================================================================
# FeatureStore — entities
# ===========================================================================

class TestEntities:
    def test_entities_empty_store(self):
        fs = make_store()
        assert fs.entities() == []
        fs.close()

    def test_entities_after_write(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1"))
        assert "u1" in fs.entities()
        fs.close()

    def test_entities_multiple(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1"))
        fs.write(sample_fv(entity_id="u2"))
        fs.write(sample_fv(entity_id="u3"))
        assert set(fs.entities()) == {"u1", "u2", "u3"}
        fs.close()

    def test_entities_distinct(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=25))
        fs.write(sample_fv(entity_id="u1", feature_name="score", value=0.9))
        assert fs.entities().count("u1") == 1
        fs.close()

    def test_entities_sorted(self):
        fs = make_store()
        for eid in ["z", "a", "m"]:
            fs.write(sample_fv(entity_id=eid))
        assert fs.entities() == ["a", "m", "z"]
        fs.close()

    def test_entities_after_delete_removes_if_no_features(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1"))
        fs.delete("u1", "age")
        assert "u1" not in fs.entities()
        fs.close()

    def test_entities_after_delete_keeps_if_other_features_remain(self):
        fs = make_store()
        fs.write(sample_fv(entity_id="u1", feature_name="age", value=25))
        fs.write(sample_fv(entity_id="u1", feature_name="score", value=0.9))
        fs.delete("u1", "age")
        assert "u1" in fs.entities()
        fs.close()


# ===========================================================================
# FeatureStore — close
# ===========================================================================

class TestClose:
    def test_close_does_not_raise(self):
        fs = make_store()
        fs.close()  # should not raise

    def test_close_twice_raises_or_no_op(self):
        fs = FeatureStore()
        fs.close()
        # Closing a closed connection raises ProgrammingError in sqlite3
        # We just verify it either succeeds or raises a known exception
        try:
            fs.close()
        except Exception:
            pass  # acceptable
