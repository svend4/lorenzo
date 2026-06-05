"""Tests for the streaming_json module (E91).

Run with:
    cd /home/user/lorenzo/docs-toolkit && \
        python -m pytest tests/test_streaming_json.py -q --tb=short -p no:randomly
"""

from __future__ import annotations

import json
import os
import tempfile

import pytest

from docstoolkit.streaming_json import (
    JSONPathFilter,
    JSONStreamError,
    StreamEvent,
    StreamFilter,
    StreamingBuilder,
    StreamingParser,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse(text: str) -> list[StreamEvent]:
    return list(StreamingParser().parse(text))


def types(events: list[StreamEvent]) -> list[str]:
    return [e.event_type for e in events]


def paths(events: list[StreamEvent]) -> list[tuple]:
    return [e.path for e in events]


def values(events: list[StreamEvent]) -> list:
    return [e.value for e in events]


# ===========================================================================
# StreamEvent dataclass
# ===========================================================================

class TestStreamEvent:
    def test_default_path_is_empty_tuple(self):
        e = StreamEvent(event_type="value", value=1)
        assert e.path == ()

    def test_default_value_is_none(self):
        e = StreamEvent(event_type="start_object")
        assert e.value is None

    def test_independent_default_paths(self):
        a = StreamEvent("value", 1)
        b = StreamEvent("value", 2)
        # Each instance should have its own empty tuple instance.
        assert a.path == ()
        assert b.path == ()
        assert a.path is not b.path or a.path == ()

    def test_fields(self):
        e = StreamEvent("key", "name", ("users", 0, "name"))
        assert e.event_type == "key"
        assert e.value == "name"
        assert e.path == ("users", 0, "name")

    def test_equality(self):
        a = StreamEvent("value", 1, ("a",))
        b = StreamEvent("value", 1, ("a",))
        assert a == b

    def test_inequality_event_type(self):
        a = StreamEvent("value", 1, ())
        b = StreamEvent("key", 1, ())
        assert a != b

    def test_inequality_value(self):
        a = StreamEvent("value", 1, ())
        b = StreamEvent("value", 2, ())
        assert a != b

    def test_inequality_path(self):
        a = StreamEvent("value", 1, ())
        b = StreamEvent("value", 1, ("x",))
        assert a != b

    def test_repr_contains_type(self):
        e = StreamEvent("value", 5, ("x",))
        assert "value" in repr(e)


# ===========================================================================
# StreamingParser.parse — scalar roots
# ===========================================================================

class TestParseScalarRoot:
    def test_integer_root(self):
        events = parse("42")
        assert len(events) == 1
        assert events[0].event_type == "value"
        assert events[0].value == 42
        assert events[0].path == ()

    def test_float_root(self):
        events = parse("3.14")
        assert len(events) == 1
        assert events[0].value == 3.14

    def test_string_root(self):
        events = parse('"hello"')
        assert events == [StreamEvent("value", "hello", ())]

    def test_true_root(self):
        events = parse("true")
        assert events[0].value is True

    def test_false_root(self):
        events = parse("false")
        assert events[0].value is False

    def test_null_root(self):
        events = parse("null")
        assert events[0].value is None
        assert events[0].event_type == "value"

    def test_negative_integer(self):
        events = parse("-7")
        assert events[0].value == -7

    def test_negative_float(self):
        events = parse("-0.5")
        assert events[0].value == -0.5

    def test_scientific_notation(self):
        events = parse("1e3")
        assert events[0].value == 1000.0


# ===========================================================================
# StreamingParser.parse — objects
# ===========================================================================

class TestParseObjects:
    def test_empty_object(self):
        events = parse("{}")
        assert types(events) == ["start_object", "end_object"]
        assert all(e.path == () for e in events)

    def test_single_key_value(self):
        events = parse('{"name": "alice"}')
        assert types(events) == ["start_object", "key", "value", "end_object"]

    def test_single_key_value_paths(self):
        events = parse('{"name": "alice"}')
        assert events[1].path == ("name",)
        assert events[2].path == ("name",)

    def test_key_event_value_is_key_string(self):
        events = parse('{"foo": 1}')
        key_event = events[1]
        assert key_event.event_type == "key"
        assert key_event.value == "foo"

    def test_scalar_value_event_after_key(self):
        events = parse('{"foo": 7}')
        value_event = events[2]
        assert value_event.event_type == "value"
        assert value_event.value == 7

    def test_two_keys_order_preserved(self):
        events = parse('{"a": 1, "b": 2}')
        keys = [e.value for e in events if e.event_type == "key"]
        assert keys == ["a", "b"]

    def test_nested_object(self):
        events = parse('{"outer": {"inner": 5}}')
        assert types(events) == [
            "start_object",
            "key",
            "start_object",
            "key",
            "value",
            "end_object",
            "end_object",
        ]

    def test_nested_object_paths(self):
        events = parse('{"outer": {"inner": 5}}')
        inner_value_event = events[4]
        assert inner_value_event.event_type == "value"
        assert inner_value_event.path == ("outer", "inner")

    def test_object_with_null(self):
        events = parse('{"x": null}')
        assert events[2].event_type == "value"
        assert events[2].value is None

    def test_object_with_bool(self):
        events = parse('{"x": true}')
        assert events[2].value is True

    def test_three_levels_deep(self):
        events = parse('{"a": {"b": {"c": 9}}}')
        # Find the only "value" event.
        value_events = [e for e in events if e.event_type == "value"]
        assert len(value_events) == 1
        assert value_events[0].path == ("a", "b", "c")
        assert value_events[0].value == 9

    def test_end_object_path(self):
        events = parse('{"outer": {"inner": 5}}')
        # Inner end_object at path ("outer",), outer end_object at ()
        end_events = [e for e in events if e.event_type == "end_object"]
        assert end_events[0].path == ("outer",)
        assert end_events[1].path == ()


# ===========================================================================
# StreamingParser.parse — arrays
# ===========================================================================

class TestParseArrays:
    def test_empty_array(self):
        events = parse("[]")
        assert types(events) == ["start_array", "end_array"]

    def test_array_single_int(self):
        events = parse("[1]")
        assert types(events) == ["start_array", "value", "end_array"]
        assert events[1].value == 1
        assert events[1].path == (0,)

    def test_array_three_ints(self):
        events = parse("[1, 2, 3]")
        value_events = [e for e in events if e.event_type == "value"]
        assert values(value_events) == [1, 2, 3]
        assert paths(value_events) == [(0,), (1,), (2,)]

    def test_array_of_strings(self):
        events = parse('["a", "b", "c"]')
        value_events = [e for e in events if e.event_type == "value"]
        assert values(value_events) == ["a", "b", "c"]

    def test_array_of_mixed(self):
        events = parse('[1, "two", true, null, 4.5]')
        value_events = [e for e in events if e.event_type == "value"]
        assert values(value_events) == [1, "two", True, None, 4.5]

    def test_array_of_arrays(self):
        events = parse("[[1, 2], [3, 4]]")
        value_events = [e for e in events if e.event_type == "value"]
        assert values(value_events) == [1, 2, 3, 4]
        assert paths(value_events) == [(0, 0), (0, 1), (1, 0), (1, 1)]

    def test_array_of_objects(self):
        events = parse('[{"a": 1}, {"a": 2}]')
        value_events = [e for e in events if e.event_type == "value"]
        assert values(value_events) == [1, 2]
        assert paths(value_events) == [(0, "a"), (1, "a")]

    def test_nested_array_start_paths(self):
        events = parse("[[1]]")
        start_events = [e for e in events if e.event_type == "start_array"]
        assert paths(start_events) == [(), (0,)]


# ===========================================================================
# StreamingParser.parse — mixed nesting
# ===========================================================================

class TestParseMixed:
    def test_object_containing_array(self):
        events = parse('{"items": [1, 2]}')
        value_events = [e for e in events if e.event_type == "value"]
        assert paths(value_events) == [("items", 0), ("items", 1)]
        assert values(value_events) == [1, 2]

    def test_array_containing_object(self):
        events = parse('[{"k": "v"}]')
        key_events = [e for e in events if e.event_type == "key"]
        assert key_events[0].path == (0, "k")

    def test_complex_document(self):
        doc = (
            '{"users": [{"name": "alice", "age": 30},'
            ' {"name": "bob", "age": 25}]}'
        )
        events = parse(doc)
        # Find all name values
        names = [
            e.value
            for e in events
            if e.event_type == "value" and len(e.path) == 3 and e.path[-1] == "name"
        ]
        assert names == ["alice", "bob"]


# ===========================================================================
# StreamingParser.parse_file
# ===========================================================================

class TestParseFile:
    def test_read_from_file(self, tmp_path):
        p = tmp_path / "data.json"
        p.write_text('{"x": 1}', encoding="utf-8")
        events = list(StreamingParser().parse_file(str(p)))
        assert any(e.event_type == "key" and e.value == "x" for e in events)
        assert any(e.event_type == "value" and e.value == 1 for e in events)

    def test_parse_file_yields_same_as_parse(self, tmp_path):
        text = '{"a": [1, 2, 3]}'
        p = tmp_path / "doc.json"
        p.write_text(text, encoding="utf-8")
        from_text = parse(text)
        from_file = list(StreamingParser().parse_file(str(p)))
        assert from_text == from_file

    def test_parse_file_missing_raises(self):
        with pytest.raises(JSONStreamError):
            list(StreamingParser().parse_file("/nonexistent/path/__no_such__.json"))

    def test_parse_file_invalid_json_raises(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("not json", encoding="utf-8")
        with pytest.raises(JSONStreamError):
            list(StreamingParser().parse_file(str(p)))


# ===========================================================================
# StreamingParser — error handling
# ===========================================================================

class TestParseErrors:
    def test_invalid_token(self):
        with pytest.raises(JSONStreamError):
            parse("not json")

    def test_unclosed_object(self):
        with pytest.raises(JSONStreamError):
            parse('{"a": 1')

    def test_unclosed_array(self):
        with pytest.raises(JSONStreamError):
            parse("[1, 2")

    def test_trailing_comma(self):
        with pytest.raises(JSONStreamError):
            parse("[1, 2,]")

    def test_bare_word(self):
        with pytest.raises(JSONStreamError):
            parse("foo")

    def test_empty_string_input(self):
        with pytest.raises(JSONStreamError):
            parse("")

    def test_whitespace_only_input(self):
        with pytest.raises(JSONStreamError):
            parse("   \n\t ")

    def test_non_string_input(self):
        with pytest.raises(JSONStreamError):
            list(StreamingParser().parse(123))  # type: ignore[arg-type]

    def test_error_message_contains_invalid(self):
        try:
            parse("not json")
        except JSONStreamError as exc:
            assert "invalid" in str(exc).lower()
        else:
            pytest.fail("expected JSONStreamError")


# ===========================================================================
# JSONPathFilter.match — literal paths
# ===========================================================================

class TestJSONPathFilterLiteral:
    def test_empty_pattern_matches_root(self):
        f = JSONPathFilter("")
        assert f.match(StreamEvent("value", 1, ()))
        assert not f.match(StreamEvent("value", 1, ("x",)))

    def test_single_key(self):
        f = JSONPathFilter("name")
        assert f.match(StreamEvent("value", "x", ("name",)))
        assert not f.match(StreamEvent("value", "x", ("other",)))

    def test_two_level_key(self):
        f = JSONPathFilter("user.name")
        assert f.match(StreamEvent("value", "x", ("user", "name")))
        assert not f.match(StreamEvent("value", "x", ("user",)))
        assert not f.match(StreamEvent("value", "x", ("user", "age")))

    def test_three_level_key(self):
        f = JSONPathFilter("a.b.c")
        assert f.match(StreamEvent("value", 1, ("a", "b", "c")))

    def test_does_not_match_longer_path(self):
        f = JSONPathFilter("a")
        assert not f.match(StreamEvent("value", 1, ("a", "b")))

    def test_does_not_match_shorter_path(self):
        f = JSONPathFilter("a.b")
        assert not f.match(StreamEvent("value", 1, ("a",)))

    def test_numeric_segment_matches_int_index(self):
        f = JSONPathFilter("items.0")
        assert f.match(StreamEvent("value", "x", ("items", 0)))

    def test_numeric_segment_does_not_match_wrong_int(self):
        f = JSONPathFilter("items.0")
        assert not f.match(StreamEvent("value", "x", ("items", 1)))


# ===========================================================================
# JSONPathFilter.match — '*' wildcard
# ===========================================================================

class TestJSONPathFilterStar:
    def test_star_matches_any_key(self):
        f = JSONPathFilter("*.name")
        assert f.match(StreamEvent("value", "x", ("alice", "name")))
        assert f.match(StreamEvent("value", "x", ("bob", "name")))

    def test_star_matches_index(self):
        f = JSONPathFilter("users.*.name")
        assert f.match(StreamEvent("value", "x", ("users", 0, "name")))
        assert f.match(StreamEvent("value", "x", ("users", 5, "name")))

    def test_star_matches_string_key(self):
        f = JSONPathFilter("users.*.name")
        assert f.match(
            StreamEvent("value", "x", ("users", "alice", "name"))
        )

    def test_star_consumes_exactly_one_segment(self):
        f = JSONPathFilter("users.*.name")
        # Two segments between users and name → no match.
        assert not f.match(
            StreamEvent("value", "x", ("users", "a", "b", "name"))
        )
        # Zero segments between → no match.
        assert not f.match(StreamEvent("value", "x", ("users", "name")))

    def test_star_at_end(self):
        f = JSONPathFilter("data.*")
        assert f.match(StreamEvent("value", "x", ("data", "k")))
        assert f.match(StreamEvent("value", "x", ("data", 3)))
        assert not f.match(StreamEvent("value", "x", ("data",)))

    def test_star_alone(self):
        f = JSONPathFilter("*")
        assert f.match(StreamEvent("value", "x", ("anything",)))
        assert f.match(StreamEvent("value", "x", (42,)))
        assert not f.match(StreamEvent("value", "x", ()))
        assert not f.match(StreamEvent("value", "x", ("a", "b")))


# ===========================================================================
# JSONPathFilter.match — '**' wildcard
# ===========================================================================

class TestJSONPathFilterDoubleStar:
    def test_double_star_alone_matches_any_depth(self):
        f = JSONPathFilter("**")
        assert f.match(StreamEvent("value", 1, ()))
        assert f.match(StreamEvent("value", 1, ("x",)))
        assert f.match(StreamEvent("value", 1, ("x", "y", "z")))

    def test_double_star_zero_segments(self):
        f = JSONPathFilter("a.**.b")
        assert f.match(StreamEvent("value", 1, ("a", "b")))

    def test_double_star_one_segment(self):
        f = JSONPathFilter("a.**.b")
        assert f.match(StreamEvent("value", 1, ("a", "x", "b")))

    def test_double_star_many_segments(self):
        f = JSONPathFilter("a.**.b")
        assert f.match(StreamEvent("value", 1, ("a", "x", "y", "z", "b")))

    def test_double_star_at_start(self):
        f = JSONPathFilter("**.tail")
        assert f.match(StreamEvent("value", 1, ("tail",)))
        assert f.match(StreamEvent("value", 1, ("a", "tail")))
        assert f.match(StreamEvent("value", 1, ("a", "b", "tail")))

    def test_double_star_at_end(self):
        f = JSONPathFilter("head.**")
        assert f.match(StreamEvent("value", 1, ("head",)))
        assert f.match(StreamEvent("value", 1, ("head", "a")))
        assert f.match(StreamEvent("value", 1, ("head", "a", "b")))
        assert not f.match(StreamEvent("value", 1, ("other",)))

    def test_double_star_requires_tail_match(self):
        f = JSONPathFilter("a.**.b")
        assert not f.match(StreamEvent("value", 1, ("a", "x", "c")))
        assert not f.match(StreamEvent("value", 1, ("a",)))

    def test_double_star_combined_with_star(self):
        f = JSONPathFilter("users.**.*.name")
        assert f.match(
            StreamEvent("value", "x", ("users", "a", "b", "name"))
        )
        assert f.match(
            StreamEvent("value", "x", ("users", "x", "y", "z", "name"))
        )


# ===========================================================================
# JSONPathFilter — misc
# ===========================================================================

class TestJSONPathFilterMisc:
    def test_match_path_alias(self):
        f = JSONPathFilter("a.b")
        assert f.match_path(("a", "b"))
        assert not f.match_path(("a",))

    def test_pattern_attribute(self):
        f = JSONPathFilter("users.*.name")
        assert f.pattern == "users.*.name"

    def test_non_string_pattern_raises(self):
        with pytest.raises(TypeError):
            JSONPathFilter(123)  # type: ignore[arg-type]


# ===========================================================================
# StreamFilter.select
# ===========================================================================

class TestStreamFilter:
    def test_select_returns_list(self):
        f = StreamFilter(StreamingParser())
        result = f.select('{"a": 1}', "a")
        assert isinstance(result, list)

    def test_select_single_value(self):
        f = StreamFilter(StreamingParser())
        result = f.select('{"name": "alice"}', "name")
        assert result == ["alice"]

    def test_select_no_match_returns_empty(self):
        f = StreamFilter(StreamingParser())
        result = f.select('{"name": "alice"}', "missing")
        assert result == []

    def test_select_array_indexed(self):
        f = StreamFilter(StreamingParser())
        result = f.select('{"items": [10, 20, 30]}', "items.1")
        assert result == [20]

    def test_select_with_wildcard(self):
        f = StreamFilter(StreamingParser())
        result = f.select(
            '{"users": [{"name": "alice"}, {"name": "bob"}]}',
            "users.*.name",
        )
        assert result == ["alice", "bob"]

    def test_select_with_double_wildcard(self):
        f = StreamFilter(StreamingParser())
        doc = '{"a": {"b": {"x": 1}, "c": {"x": 2}}}'
        result = f.select(doc, "a.**.x")
        assert sorted(result) == [1, 2]

    def test_select_root_value(self):
        f = StreamFilter(StreamingParser())
        result = f.select("42", "")
        assert result == [42]

    def test_select_root_string(self):
        f = StreamFilter(StreamingParser())
        result = f.select('"hello"', "")
        assert result == ["hello"]

    def test_select_skips_container_events(self):
        f = StreamFilter(StreamingParser())
        # `**` matches the path of containers too but select only returns
        # scalar values.
        result = f.select('{"a": [1, 2]}', "**")
        assert sorted(result) == [1, 2]

    def test_select_preserves_order(self):
        f = StreamFilter(StreamingParser())
        doc = '{"items": [{"v": 3}, {"v": 1}, {"v": 2}]}'
        result = f.select(doc, "items.*.v")
        assert result == [3, 1, 2]

    def test_select_multiple_matches_with_star_at_end(self):
        f = StreamFilter(StreamingParser())
        doc = '{"data": {"a": 1, "b": 2, "c": 3}}'
        result = f.select(doc, "data.*")
        assert sorted(result) == [1, 2, 3]

    def test_select_propagates_invalid_json(self):
        f = StreamFilter(StreamingParser())
        with pytest.raises(JSONStreamError):
            f.select("bad", "x")


# ===========================================================================
# StreamingBuilder
# ===========================================================================

class TestStreamingBuilder:
    def test_empty_object(self):
        b = StreamingBuilder()
        b.start_object()
        b.end_object()
        assert b.build() == "{}"

    def test_empty_array(self):
        b = StreamingBuilder()
        b.start_array()
        b.end_array()
        assert b.build() == "[]"

    def test_single_key_value(self):
        b = StreamingBuilder()
        b.start_object()
        b.add("name", "alice")
        b.end_object()
        assert json.loads(b.build()) == {"name": "alice"}

    def test_two_key_values(self):
        b = StreamingBuilder()
        b.start_object()
        b.add("a", 1)
        b.add("b", 2)
        b.end_object()
        assert json.loads(b.build()) == {"a": 1, "b": 2}

    def test_array_with_scalars(self):
        b = StreamingBuilder()
        b.start_array()
        b.add(value=1)
        b.add(value=2)
        b.add(value=3)
        b.end_array()
        assert json.loads(b.build()) == [1, 2, 3]

    def test_nested_object_in_object(self):
        b = StreamingBuilder()
        b.start_object()
        b.start_object("inner")
        b.add("x", 1)
        b.end_object()
        b.end_object()
        assert json.loads(b.build()) == {"inner": {"x": 1}}

    def test_nested_array_in_object(self):
        b = StreamingBuilder()
        b.start_object()
        b.start_array("items")
        b.add(value="a")
        b.add(value="b")
        b.end_array()
        b.end_object()
        assert json.loads(b.build()) == {"items": ["a", "b"]}

    def test_nested_object_in_array(self):
        b = StreamingBuilder()
        b.start_array()
        b.start_object()
        b.add("k", "v")
        b.end_object()
        b.end_array()
        assert json.loads(b.build()) == [{"k": "v"}]

    def test_array_of_objects(self):
        b = StreamingBuilder()
        b.start_array()
        for v in (1, 2, 3):
            b.start_object()
            b.add("n", v)
            b.end_object()
        b.end_array()
        assert json.loads(b.build()) == [{"n": 1}, {"n": 2}, {"n": 3}]

    def test_scalar_root_int(self):
        b = StreamingBuilder()
        b.add(value=7)
        assert b.build() == "7"

    def test_scalar_root_string(self):
        b = StreamingBuilder()
        b.add(value="hi")
        assert b.build() == '"hi"'

    def test_scalar_root_null(self):
        b = StreamingBuilder()
        b.add(value=None)
        assert b.build() == "null"

    def test_scalar_root_bool_true(self):
        b = StreamingBuilder()
        b.add(value=True)
        assert b.build() == "true"

    def test_scalar_root_bool_false(self):
        b = StreamingBuilder()
        b.add(value=False)
        assert b.build() == "false"

    def test_escaping_quotes(self):
        b = StreamingBuilder()
        b.start_object()
        b.add("k", 'a"b')
        b.end_object()
        out = b.build()
        assert json.loads(out) == {"k": 'a"b'}

    def test_escaping_newlines(self):
        b = StreamingBuilder()
        b.start_object()
        b.add("k", "a\nb")
        b.end_object()
        out = b.build()
        assert json.loads(out) == {"k": "a\nb"}

    def test_escaping_backslash(self):
        b = StreamingBuilder()
        b.add(value="a\\b")
        out = b.build()
        assert json.loads(out) == "a\\b"

    def test_unicode_value(self):
        b = StreamingBuilder()
        b.start_object()
        b.add("greeting", "привет")
        b.end_object()
        assert json.loads(b.build()) == {"greeting": "привет"}

    def test_keys_with_special_chars(self):
        b = StreamingBuilder()
        b.start_object()
        b.add('a key with "quotes"', 1)
        b.end_object()
        assert json.loads(b.build()) == {'a key with "quotes"': 1}

    def test_add_accepts_dict_value(self):
        b = StreamingBuilder()
        b.start_object()
        b.add("payload", {"x": 1, "y": [1, 2]})
        b.end_object()
        assert json.loads(b.build()) == {"payload": {"x": 1, "y": [1, 2]}}

    def test_add_accepts_list_value(self):
        b = StreamingBuilder()
        b.start_object()
        b.add("items", [1, 2, 3])
        b.end_object()
        assert json.loads(b.build()) == {"items": [1, 2, 3]}

    def test_build_unclosed_object_raises(self):
        b = StreamingBuilder()
        b.start_object()
        with pytest.raises(ValueError):
            b.build()

    def test_build_unclosed_array_raises(self):
        b = StreamingBuilder()
        b.start_array()
        with pytest.raises(ValueError):
            b.build()

    def test_build_no_value_raises(self):
        b = StreamingBuilder()
        with pytest.raises(ValueError):
            b.build()

    def test_end_without_open_raises(self):
        b = StreamingBuilder()
        with pytest.raises(ValueError):
            b.end_object()

    def test_end_wrong_kind_raises(self):
        b = StreamingBuilder()
        b.start_object()
        with pytest.raises(ValueError):
            b.end_array()

    def test_key_required_inside_object(self):
        b = StreamingBuilder()
        b.start_object()
        with pytest.raises(ValueError):
            b.add(value=1)

    def test_key_forbidden_inside_array(self):
        b = StreamingBuilder()
        b.start_array()
        with pytest.raises(ValueError):
            b.add("k", 1)

    def test_two_root_values_raises(self):
        b = StreamingBuilder()
        b.add(value=1)
        with pytest.raises(ValueError):
            b.add(value=2)

    def test_top_level_value_with_key_raises(self):
        b = StreamingBuilder()
        with pytest.raises(ValueError):
            b.add("k", 1)

    def test_non_string_key_raises(self):
        b = StreamingBuilder()
        b.start_object()
        with pytest.raises(TypeError):
            b.add(123, "v")  # type: ignore[arg-type]

    def test_double_build_finalized(self):
        b = StreamingBuilder()
        b.start_object()
        b.end_object()
        b.build()
        # Second build is allowed and returns same string, but writing more
        # is not.
        with pytest.raises(ValueError):
            b.add(value=1)


# ===========================================================================
# Round-trip parse(build(...))
# ===========================================================================

class TestRoundTrip:
    def test_simple_object(self):
        b = StreamingBuilder()
        b.start_object()
        b.add("name", "alice")
        b.add("age", 30)
        b.end_object()
        text = b.build()
        assert json.loads(text) == {"name": "alice", "age": 30}
        # Re-parse through the streaming parser.
        events = list(StreamingParser().parse(text))
        assert events[0].event_type == "start_object"
        assert events[-1].event_type == "end_object"

    def test_complex_round_trip(self):
        b = StreamingBuilder()
        b.start_object()
        b.start_array("users")
        b.start_object()
        b.add("name", "alice")
        b.add("age", 30)
        b.end_object()
        b.start_object()
        b.add("name", "bob")
        b.add("age", 25)
        b.end_object()
        b.end_array()
        b.add("count", 2)
        b.end_object()
        text = b.build()
        assert json.loads(text) == {
            "users": [
                {"name": "alice", "age": 30},
                {"name": "bob", "age": 25},
            ],
            "count": 2,
        }
        # Stream-parse and pull names with the filter.
        filt = StreamFilter(StreamingParser())
        assert filt.select(text, "users.*.name") == ["alice", "bob"]

    def test_round_trip_array_of_scalars(self):
        b = StreamingBuilder()
        b.start_array()
        for v in [1, "two", True, None, 4.5]:
            b.add(value=v)
        b.end_array()
        text = b.build()
        assert json.loads(text) == [1, "two", True, None, 4.5]

    def test_round_trip_deep_nesting(self):
        b = StreamingBuilder()
        b.start_object()
        b.start_object("a")
        b.start_object("b")
        b.start_object("c")
        b.add("value", 42)
        b.end_object()
        b.end_object()
        b.end_object()
        b.end_object()
        text = b.build()
        assert json.loads(text) == {"a": {"b": {"c": {"value": 42}}}}
        # Path via filter
        filt = StreamFilter(StreamingParser())
        assert filt.select(text, "a.b.c.value") == [42]
        assert filt.select(text, "a.**.value") == [42]


# ===========================================================================
# End-to-end: parser + filter on built JSON
# ===========================================================================

class TestEndToEnd:
    def test_filter_after_build(self):
        b = StreamingBuilder()
        b.start_object()
        b.start_array("xs")
        for v in [10, 20, 30]:
            b.add(value=v)
        b.end_array()
        b.end_object()
        text = b.build()
        f = StreamFilter(StreamingParser())
        assert f.select(text, "xs.*") == [10, 20, 30]
        assert f.select(text, "xs.0") == [10]
        assert f.select(text, "xs.2") == [30]
        assert f.select(text, "xs.5") == []

    def test_parse_then_count_keys(self):
        doc = '{"a": 1, "b": 2, "c": 3}'
        keys = [e.value for e in StreamingParser().parse(doc) if e.event_type == "key"]
        assert keys == ["a", "b", "c"]

    def test_iterator_lazy(self):
        # The parser must return an iterator, not a list.
        it = StreamingParser().parse('{"a": 1}')
        assert hasattr(it, "__next__")
        first = next(it)
        assert first.event_type == "start_object"

    def test_parse_file_iterator(self, tmp_path):
        p = tmp_path / "x.json"
        p.write_text("[1, 2, 3]", encoding="utf-8")
        it = StreamingParser().parse_file(str(p))
        assert hasattr(it, "__next__")
