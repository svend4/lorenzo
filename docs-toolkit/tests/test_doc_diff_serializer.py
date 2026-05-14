"""Tests for E413 doc_diff_serializer."""

from __future__ import annotations

import json
import threading

import pytest

from docstoolkit.doc_diff_serializer import (
    DiffOp,
    SerializedDiff,
    SerializerStats,
    DocDiffSerializer,
)


# ---------------------------------------------------------------------------
# Dataclass smoke tests
# ---------------------------------------------------------------------------
def test_diffop_defaults():
    op = DiffOp(op="insert", position=0)
    assert op.length == 0
    assert op.text == ""


def test_diffop_explicit():
    op = DiffOp(op="replace", position=5, length=3, text="hello")
    assert op.op == "replace"
    assert op.position == 5
    assert op.length == 3
    assert op.text == "hello"


def test_serializeddiff_defaults():
    d = SerializedDiff(doc_id="d", from_version="v1", to_version="v2")
    assert d.ops == []
    assert d.metadata == {}


def test_serializeddiff_with_ops():
    d = SerializedDiff(
        doc_id="d", from_version="v1", to_version="v2",
        ops=[DiffOp("insert", 0, text="x")],
        metadata={"author": "alice"},
    )
    assert len(d.ops) == 1
    assert d.metadata["author"] == "alice"


def test_stats_dataclass():
    s = SerializerStats(total_diffs=1, total_ops_serialized=2, total_ops_parsed=3)
    assert s.total_diffs == 1
    assert s.total_ops_serialized == 2
    assert s.total_ops_parsed == 3


# ---------------------------------------------------------------------------
# Serialize
# ---------------------------------------------------------------------------
def test_serialize_empty():
    ser = DocDiffSerializer()
    d = SerializedDiff(doc_id="d", from_version="v1", to_version="v2")
    out = ser.serialize(d)
    parsed = json.loads(out)
    assert parsed["doc_id"] == "d"
    assert parsed["from_version"] == "v1"
    assert parsed["to_version"] == "v2"
    assert parsed["ops"] == []
    assert parsed["metadata"] == {}


def test_serialize_with_ops():
    ser = DocDiffSerializer()
    d = SerializedDiff(
        doc_id="d", from_version="v1", to_version="v2",
        ops=[DiffOp("insert", 0, text="hi"), DiffOp("delete", 5, length=2)],
    )
    out = ser.serialize(d)
    parsed = json.loads(out)
    assert len(parsed["ops"]) == 2
    assert parsed["ops"][0]["text"] == "hi"


def test_serialize_updates_stats():
    ser = DocDiffSerializer()
    d = SerializedDiff(
        doc_id="d", from_version="v1", to_version="v2",
        ops=[DiffOp("insert", 0, text="x"), DiffOp("insert", 1, text="y")],
    )
    ser.serialize(d)
    assert ser.stats().total_ops_serialized == 2


def test_serialize_non_diff_raises():
    ser = DocDiffSerializer()
    with pytest.raises(TypeError):
        ser.serialize({"not": "a diff"})


def test_serialize_unicode():
    ser = DocDiffSerializer()
    d = SerializedDiff(doc_id="д", from_version="v1", to_version="v2",
                      ops=[DiffOp("insert", 0, text="привет")])
    out = ser.serialize(d)
    assert "привет" in out


def test_serialize_metadata():
    ser = DocDiffSerializer()
    d = SerializedDiff(doc_id="d", from_version="v1", to_version="v2",
                      metadata={"author": "bob", "timestamp": "2026-01-01"})
    out = ser.serialize(d)
    parsed = json.loads(out)
    assert parsed["metadata"]["author"] == "bob"


# ---------------------------------------------------------------------------
# Parse
# ---------------------------------------------------------------------------
def test_parse_empty_ops():
    ser = DocDiffSerializer()
    raw = json.dumps({"doc_id": "d", "from_version": "v1", "to_version": "v2", "ops": []})
    d = ser.parse(raw)
    assert d.doc_id == "d"
    assert d.ops == []


def test_parse_with_ops():
    ser = DocDiffSerializer()
    raw = json.dumps({
        "doc_id": "d", "from_version": "v1", "to_version": "v2",
        "ops": [{"op": "insert", "position": 0, "text": "hi"}],
    })
    d = ser.parse(raw)
    assert isinstance(d.ops[0], DiffOp)
    assert d.ops[0].text == "hi"


def test_parse_updates_stats():
    ser = DocDiffSerializer()
    raw = json.dumps({
        "doc_id": "d", "from_version": "v1", "to_version": "v2",
        "ops": [
            {"op": "insert", "position": 0, "text": "a"},
            {"op": "delete", "position": 1, "length": 1},
            {"op": "replace", "position": 2, "length": 1, "text": "x"},
        ],
    })
    ser.parse(raw)
    assert ser.stats().total_ops_parsed == 3


def test_parse_invalid_json():
    ser = DocDiffSerializer()
    with pytest.raises(ValueError):
        ser.parse("{not json")


def test_parse_non_object_top_level():
    ser = DocDiffSerializer()
    with pytest.raises(ValueError):
        ser.parse("[]")


def test_parse_missing_doc_id():
    ser = DocDiffSerializer()
    raw = json.dumps({"from_version": "v1", "to_version": "v2"})
    with pytest.raises(ValueError):
        ser.parse(raw)


def test_parse_missing_from_version():
    ser = DocDiffSerializer()
    raw = json.dumps({"doc_id": "d", "to_version": "v2"})
    with pytest.raises(ValueError):
        ser.parse(raw)


def test_parse_missing_to_version():
    ser = DocDiffSerializer()
    raw = json.dumps({"doc_id": "d", "from_version": "v1"})
    with pytest.raises(ValueError):
        ser.parse(raw)


def test_parse_non_string_doc_id():
    ser = DocDiffSerializer()
    raw = json.dumps({"doc_id": 123, "from_version": "v1", "to_version": "v2"})
    with pytest.raises(ValueError):
        ser.parse(raw)


def test_parse_ops_not_list():
    ser = DocDiffSerializer()
    raw = json.dumps({"doc_id": "d", "from_version": "v1", "to_version": "v2", "ops": "x"})
    with pytest.raises(ValueError):
        ser.parse(raw)


def test_parse_op_unknown_kind():
    ser = DocDiffSerializer()
    raw = json.dumps({
        "doc_id": "d", "from_version": "v1", "to_version": "v2",
        "ops": [{"op": "weird", "position": 0}],
    })
    with pytest.raises(ValueError):
        ser.parse(raw)


def test_parse_op_missing_position():
    ser = DocDiffSerializer()
    raw = json.dumps({
        "doc_id": "d", "from_version": "v1", "to_version": "v2",
        "ops": [{"op": "insert"}],
    })
    with pytest.raises(ValueError):
        ser.parse(raw)


def test_parse_op_non_int_position():
    ser = DocDiffSerializer()
    raw = json.dumps({
        "doc_id": "d", "from_version": "v1", "to_version": "v2",
        "ops": [{"op": "insert", "position": "0"}],
    })
    with pytest.raises(ValueError):
        ser.parse(raw)


def test_parse_op_not_dict():
    ser = DocDiffSerializer()
    raw = json.dumps({
        "doc_id": "d", "from_version": "v1", "to_version": "v2",
        "ops": ["x"],
    })
    with pytest.raises(ValueError):
        ser.parse(raw)


def test_parse_metadata_not_object():
    ser = DocDiffSerializer()
    raw = json.dumps({
        "doc_id": "d", "from_version": "v1", "to_version": "v2",
        "ops": [], "metadata": "x",
    })
    with pytest.raises(ValueError):
        ser.parse(raw)


def test_parse_non_string_input():
    ser = DocDiffSerializer()
    with pytest.raises(ValueError):
        ser.parse(123)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Round-trip
# ---------------------------------------------------------------------------
def test_round_trip():
    ser = DocDiffSerializer()
    original = SerializedDiff(
        doc_id="doc", from_version="v1", to_version="v2",
        ops=[
            DiffOp("insert", 0, text="hi"),
            DiffOp("delete", 5, length=3),
            DiffOp("replace", 10, length=2, text="zz"),
        ],
        metadata={"author": "alice"},
    )
    serialized = ser.serialize(original)
    parsed = ser.parse(serialized)
    assert parsed.doc_id == original.doc_id
    assert parsed.from_version == original.from_version
    assert parsed.to_version == original.to_version
    assert len(parsed.ops) == len(original.ops)
    for a, b in zip(parsed.ops, original.ops):
        assert a.op == b.op
        assert a.position == b.position
        assert a.length == b.length
        assert a.text == b.text
    assert parsed.metadata == original.metadata


# ---------------------------------------------------------------------------
# Store / retrieve / delete
# ---------------------------------------------------------------------------
def test_store_and_retrieve():
    ser = DocDiffSerializer()
    d = SerializedDiff(doc_id="d", from_version="v1", to_version="v2")
    ser.store(d)
    got = ser.retrieve("d", "v1", "v2")
    assert got is d


def test_retrieve_missing():
    ser = DocDiffSerializer()
    assert ser.retrieve("x", "v1", "v2") is None


def test_store_replaces_existing():
    ser = DocDiffSerializer()
    d1 = SerializedDiff(doc_id="d", from_version="v1", to_version="v2", metadata={"r": 1})
    d2 = SerializedDiff(doc_id="d", from_version="v1", to_version="v2", metadata={"r": 2})
    ser.store(d1)
    ser.store(d2)
    got = ser.retrieve("d", "v1", "v2")
    assert got is d2


def test_delete_existing():
    ser = DocDiffSerializer()
    d = SerializedDiff(doc_id="d", from_version="v1", to_version="v2")
    ser.store(d)
    assert ser.delete("d", "v1", "v2") is True
    assert ser.retrieve("d", "v1", "v2") is None


def test_delete_missing():
    ser = DocDiffSerializer()
    assert ser.delete("x", "v1", "v2") is False


def test_store_non_diff_raises():
    ser = DocDiffSerializer()
    with pytest.raises(TypeError):
        ser.store({"not": "a diff"})


def test_diffs_for_doc_sorted():
    ser = DocDiffSerializer()
    ser.store(SerializedDiff("d", "v2", "v3"))
    ser.store(SerializedDiff("d", "v1", "v2"))
    ser.store(SerializedDiff("d", "v3", "v4"))
    diffs = ser.diffs_for_doc("d")
    assert [(d.from_version, d.to_version) for d in diffs] == [
        ("v1", "v2"), ("v2", "v3"), ("v3", "v4"),
    ]


def test_diffs_for_doc_filters_by_doc():
    ser = DocDiffSerializer()
    ser.store(SerializedDiff("d1", "v1", "v2"))
    ser.store(SerializedDiff("d2", "v1", "v2"))
    diffs = ser.diffs_for_doc("d1")
    assert len(diffs) == 1
    assert diffs[0].doc_id == "d1"


def test_diffs_for_doc_empty():
    ser = DocDiffSerializer()
    assert ser.diffs_for_doc("nobody") == []


# ---------------------------------------------------------------------------
# apply_diff
# ---------------------------------------------------------------------------
def test_apply_insert():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("insert", 5, text="X")])
    assert ser.apply_diff("hello world", d) == "helloX world"


def test_apply_insert_at_start():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("insert", 0, text="X")])
    assert ser.apply_diff("hi", d) == "Xhi"


def test_apply_insert_at_end():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("insert", 2, text="X")])
    assert ser.apply_diff("hi", d) == "hiX"


def test_apply_delete():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("delete", 5, length=6)])
    assert ser.apply_diff("hello world", d) == "hello"


def test_apply_replace():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("replace", 6, length=5, text="there")])
    assert ser.apply_diff("hello world", d) == "hello there"


def test_apply_multi_ops_sequential():
    # Note: ops apply sequentially against the evolving result.
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[
        DiffOp("insert", 0, text="X"),  # "Xhello"
        DiffOp("delete", 1, length=2),  # "Xllo"
    ])
    assert ser.apply_diff("hello", d) == "Xllo"


def test_apply_empty_ops_unchanged():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2")
    assert ser.apply_diff("hello", d) == "hello"


def test_apply_negative_position():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("insert", -1, text="X")])
    with pytest.raises(ValueError):
        ser.apply_diff("hi", d)


def test_apply_position_out_of_bounds():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("insert", 100, text="X")])
    with pytest.raises(ValueError):
        ser.apply_diff("hi", d)


def test_apply_delete_past_end():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("delete", 2, length=100)])
    with pytest.raises(ValueError):
        ser.apply_diff("hello", d)


def test_apply_replace_past_end():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("replace", 2, length=100, text="x")])
    with pytest.raises(ValueError):
        ser.apply_diff("hello", d)


def test_apply_non_string_content():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2")
    with pytest.raises(TypeError):
        ser.apply_diff(123, d)  # type: ignore[arg-type]


def test_apply_non_diff():
    ser = DocDiffSerializer()
    with pytest.raises(TypeError):
        ser.apply_diff("hi", {"not": "a diff"})  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# validate_diff
# ---------------------------------------------------------------------------
def test_validate_ok():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[
        DiffOp("insert", 0, text="x"),
        DiffOp("delete", 1, length=2),
        DiffOp("replace", 3, length=1, text="y"),
    ])
    assert ser.validate_diff(d) == []


def test_validate_empty_doc_id():
    ser = DocDiffSerializer()
    d = SerializedDiff("", "v1", "v2")
    errs = ser.validate_diff(d)
    assert any("doc_id" in e for e in errs)


def test_validate_empty_from_version():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "", "v2")
    errs = ser.validate_diff(d)
    assert any("from_version" in e for e in errs)


def test_validate_empty_to_version():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "")
    errs = ser.validate_diff(d)
    assert any("to_version" in e for e in errs)


def test_validate_negative_position():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("insert", -1, text="x")])
    errs = ser.validate_diff(d)
    assert any("position" in e for e in errs)


def test_validate_negative_length():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("delete", 0, length=-1)])
    errs = ser.validate_diff(d)
    assert any("length" in e for e in errs)


def test_validate_unknown_op_kind():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("weird", 0)])
    errs = ser.validate_diff(d)
    assert any("unknown op kind" in e for e in errs)


def test_validate_insert_with_length():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("insert", 0, length=2, text="x")])
    errs = ser.validate_diff(d)
    assert any("length == 0" in e for e in errs)


def test_validate_delete_zero_length():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("delete", 0, length=0)])
    errs = ser.validate_diff(d)
    assert any("length > 0" in e for e in errs)


def test_validate_delete_with_text():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("delete", 0, length=1, text="x")])
    errs = ser.validate_diff(d)
    assert any("empty text" in e for e in errs)


def test_validate_replace_zero_length():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("replace", 0, length=0, text="x")])
    errs = ser.validate_diff(d)
    assert any("length > 0" in e for e in errs)


def test_validate_non_diff():
    ser = DocDiffSerializer()
    errs = ser.validate_diff({"not": "a diff"})  # type: ignore[arg-type]
    assert errs and "SerializedDiff" in errs[0]


def test_validate_op_not_diffop():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=["not an op"])
    errs = ser.validate_diff(d)
    assert any("not a DiffOp" in e for e in errs)


# ---------------------------------------------------------------------------
# clear / stats
# ---------------------------------------------------------------------------
def test_clear_returns_count():
    ser = DocDiffSerializer()
    ser.store(SerializedDiff("d", "v1", "v2"))
    ser.store(SerializedDiff("d", "v2", "v3"))
    assert ser.clear() == 2
    assert ser.retrieve("d", "v1", "v2") is None


def test_clear_empty():
    ser = DocDiffSerializer()
    assert ser.clear() == 0


def test_stats_initial():
    ser = DocDiffSerializer()
    s = ser.stats()
    assert s.total_diffs == 0
    assert s.total_ops_serialized == 0
    assert s.total_ops_parsed == 0


def test_stats_after_activity():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("insert", 0, text="x")])
    ser.serialize(d)
    raw = json.dumps({
        "doc_id": "d", "from_version": "v1", "to_version": "v2",
        "ops": [{"op": "insert", "position": 0, "text": "y"}, {"op": "delete", "position": 1, "length": 1}],
    })
    ser.parse(raw)
    ser.store(d)
    s = ser.stats()
    assert s.total_diffs == 1
    assert s.total_ops_serialized == 1
    assert s.total_ops_parsed == 2


def test_stats_returns_dataclass():
    ser = DocDiffSerializer()
    assert isinstance(ser.stats(), SerializerStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
def test_concurrent_store():
    ser = DocDiffSerializer()

    def worker(i: int):
        for j in range(20):
            ser.store(SerializedDiff(f"d{i}", f"v{j}", f"v{j+1}"))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert ser.stats().total_diffs == 8 * 20


def test_concurrent_serialize():
    ser = DocDiffSerializer()
    d = SerializedDiff("d", "v1", "v2", ops=[DiffOp("insert", 0, text="x")])

    def worker():
        for _ in range(50):
            ser.serialize(d)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert ser.stats().total_ops_serialized == 8 * 50


def test_concurrent_parse():
    ser = DocDiffSerializer()
    raw = json.dumps({
        "doc_id": "d", "from_version": "v1", "to_version": "v2",
        "ops": [{"op": "insert", "position": 0, "text": "x"}],
    })

    def worker():
        for _ in range(50):
            ser.parse(raw)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert ser.stats().total_ops_parsed == 8 * 50


def test_concurrent_mixed():
    ser = DocDiffSerializer()

    def store_worker(i: int):
        for j in range(10):
            ser.store(SerializedDiff(f"d{i}", f"v{j}", f"v{j+1}"))

    def retrieve_worker(i: int):
        for j in range(10):
            ser.retrieve(f"d{i}", f"v{j}", f"v{j+1}")

    threads = []
    for i in range(4):
        threads.append(threading.Thread(target=store_worker, args=(i,)))
        threads.append(threading.Thread(target=retrieve_worker, args=(i,)))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert ser.stats().total_diffs == 4 * 10
