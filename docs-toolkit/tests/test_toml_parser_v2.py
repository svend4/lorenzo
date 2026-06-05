"""Tests for docstoolkit.toml_parser_v2."""
import pytest

from docstoolkit.toml_parser_v2 import ParseError, TomlParser


@pytest.fixture()
def p():
    return TomlParser()


# --------------------------------------------------------------------- KV ---
class TestParseSimpleKV:
    def test_single_pair(self, p):
        assert p.parse('name = "lorenzo"') == {"name": "lorenzo"}

    def test_multiple_pairs(self, p):
        text = 'a = 1\nb = 2\nc = 3'
        assert p.parse(text) == {"a": 1, "b": 2, "c": 3}

    def test_whitespace_around_equals(self, p):
        assert p.parse("x   =    42") == {"x": 42}

    def test_mixed_types(self, p):
        text = 'name = "x"\ncount = 5\npi = 3.14\nok = true'
        assert p.parse(text) == {
            "name": "x",
            "count": 5,
            "pi": 3.14,
            "ok": True,
        }


# ------------------------------------------------------------------ STRINGS -
class TestParseStrings:
    def test_basic_string(self, p):
        assert p.parse('k = "hello"') == {"k": "hello"}

    def test_empty_string(self, p):
        assert p.parse('k = ""') == {"k": ""}

    def test_escape_newline(self, p):
        assert p.parse(r'k = "a\nb"') == {"k": "a\nb"}

    def test_escape_tab(self, p):
        assert p.parse(r'k = "a\tb"') == {"k": "a\tb"}

    def test_escape_backslash(self, p):
        assert p.parse(r'k = "a\\b"') == {"k": "a\\b"}

    def test_escape_quote(self, p):
        assert p.parse(r'k = "a\"b"') == {"k": 'a"b'}

    def test_string_with_spaces(self, p):
        assert p.parse('k = "hello world"') == {"k": "hello world"}

    def test_unicode_passthrough(self, p):
        assert p.parse('k = "тест"') == {"k": "тест"}


# ----------------------------------------------------------------- INTEGERS -
class TestParseIntegers:
    def test_positive(self, p):
        assert p.parse("x = 123") == {"x": 123}

    def test_negative(self, p):
        assert p.parse("x = -5") == {"x": -5}

    def test_zero(self, p):
        assert p.parse("x = 0") == {"x": 0}

    def test_underscore_separator(self, p):
        assert p.parse("x = 1_000") == {"x": 1000}

    def test_large_number(self, p):
        assert p.parse("x = 1_000_000") == {"x": 1_000_000}

    def test_negative_with_underscore(self, p):
        assert p.parse("x = -1_234") == {"x": -1234}


# ------------------------------------------------------------------- FLOATS -
class TestParseFloats:
    def test_basic_float(self, p):
        assert p.parse("x = 3.14") == {"x": 3.14}

    def test_negative_float(self, p):
        assert p.parse("x = -0.5") == {"x": -0.5}

    def test_exponent(self, p):
        assert p.parse("x = 1e10") == {"x": 1e10}

    def test_exponent_capital(self, p):
        assert p.parse("x = 1E2") == {"x": 100.0}

    def test_negative_exponent(self, p):
        assert p.parse("x = 1.5e-2") == {"x": 0.015}


# ---------------------------------------------------------------- BOOLEANS -
class TestParseBooleans:
    def test_true(self, p):
        assert p.parse("x = true") == {"x": True}

    def test_false(self, p):
        assert p.parse("x = false") == {"x": False}

    def test_bool_not_string(self, p):
        out = p.parse("x = true")
        assert out["x"] is True
        assert not isinstance(out["x"], str)


# ------------------------------------------------------------------ ARRAYS -
class TestParseArrays:
    def test_int_array(self, p):
        assert p.parse("x = [1, 2, 3]") == {"x": [1, 2, 3]}

    def test_string_array(self, p):
        assert p.parse('x = ["a", "b"]') == {"x": ["a", "b"]}

    def test_empty_array(self, p):
        assert p.parse("x = []") == {"x": []}

    def test_single_element(self, p):
        assert p.parse("x = [42]") == {"x": [42]}

    def test_nested_array(self, p):
        assert p.parse("x = [[1, 2], [3, 4]]") == {"x": [[1, 2], [3, 4]]}

    def test_multiline_array(self, p):
        text = "x = [\n  1,\n  2,\n  3,\n]"
        assert p.parse(text) == {"x": [1, 2, 3]}

    def test_mixed_array(self, p):
        # TOML 1.0 actually allows heterogeneous arrays
        assert p.parse('x = [1, "a", true]') == {"x": [1, "a", True]}


# ----------------------------------------------------------- INLINE TABLES -
class TestParseInlineTable:
    def test_simple_inline(self, p):
        assert p.parse("x = { a = 1, b = 2 }") == {"x": {"a": 1, "b": 2}}

    def test_empty_inline(self, p):
        assert p.parse("x = {}") == {"x": {}}

    def test_inline_with_strings(self, p):
        assert p.parse('x = { name = "z" }') == {"x": {"name": "z"}}

    def test_inline_single_pair(self, p):
        assert p.parse("x = { a = 1 }") == {"x": {"a": 1}}


# ------------------------------------------------------------------ TABLES -
class TestParseTables:
    def test_single_table(self, p):
        text = "[server]\nport = 80"
        assert p.parse(text) == {"server": {"port": 80}}

    def test_table_with_multiple_keys(self, p):
        text = '[server]\nport = 80\nhost = "x"'
        assert p.parse(text) == {"server": {"port": 80, "host": "x"}}

    def test_two_tables(self, p):
        text = "[a]\nx = 1\n[b]\ny = 2"
        assert p.parse(text) == {"a": {"x": 1}, "b": {"y": 2}}

    def test_top_level_then_table(self, p):
        text = "name = 'top'\n[t]\nk = 1"
        # only basic strings, so use double quotes
        text = 'name = "top"\n[t]\nk = 1'
        assert p.parse(text) == {"name": "top", "t": {"k": 1}}


# ----------------------------------------------------------- NESTED TABLES -
class TestParseNestedTables:
    def test_two_levels(self, p):
        text = "[a.b]\nx = 1"
        assert p.parse(text) == {"a": {"b": {"x": 1}}}

    def test_three_levels(self, p):
        text = "[a.b.c]\nx = 1"
        assert p.parse(text) == {"a": {"b": {"c": {"x": 1}}}}

    def test_sibling_nested(self, p):
        text = "[a.b]\nx = 1\n[a.c]\ny = 2"
        assert p.parse(text) == {"a": {"b": {"x": 1}, "c": {"y": 2}}}

    def test_dotted_key_value(self, p):
        text = "a.b = 1"
        assert p.parse(text) == {"a": {"b": 1}}


# ---------------------------------------------------------------- COMMENTS -
class TestParseComments:
    def test_line_comment(self, p):
        assert p.parse("# just a comment") == {}

    def test_trailing_comment(self, p):
        assert p.parse("x = 1 # comment") == {"x": 1}

    def test_comment_then_value(self, p):
        text = "# header\nx = 1"
        assert p.parse(text) == {"x": 1}

    def test_hash_inside_string(self, p):
        assert p.parse('x = "a#b"') == {"x": "a#b"}


# ------------------------------------------------------------------- EMPTY -
class TestParseEmpty:
    def test_empty_string(self, p):
        assert p.parse("") == {}

    def test_only_whitespace(self, p):
        assert p.parse("   \n\n  \n") == {}

    def test_only_comments(self, p):
        assert p.parse("# a\n# b") == {}


# ----------------------------------------------------------------- INVALID -
class TestParseInvalid:
    def test_no_equals(self, p):
        with pytest.raises(ParseError):
            p.parse("just_a_key")

    def test_missing_key(self, p):
        with pytest.raises(ParseError):
            p.parse("= 1")

    def test_unterminated_string(self, p):
        with pytest.raises(ParseError):
            p.parse('x = "abc')

    def test_unterminated_array(self, p):
        with pytest.raises(ParseError):
            p.parse("x = [1, 2")

    def test_empty_table_header(self, p):
        with pytest.raises(ParseError):
            p.parse("[]\nx = 1")

    def test_non_string_input(self, p):
        with pytest.raises(ParseError):
            p.parse(123)  # type: ignore[arg-type]

    def test_bad_escape(self, p):
        with pytest.raises(ParseError):
            p.parse(r'x = "a\zb"')


# -------------------------------------------------------------- DUMP SIMPLE -
class TestDumpSimple:
    def test_dump_string(self, p):
        assert p.dump({"k": "v"}) == 'k = "v"\n'

    def test_dump_int(self, p):
        assert p.dump({"k": 5}) == "k = 5\n"

    def test_dump_bool(self, p):
        assert p.dump({"k": True}) == "k = true\n"

    def test_dump_float(self, p):
        out = p.dump({"k": 3.14})
        assert out == "k = 3.14\n"

    def test_dump_empty_dict(self, p):
        assert p.dump({}) == ""

    def test_dump_multiple_scalars(self, p):
        out = p.dump({"a": 1, "b": 2})
        assert "a = 1" in out
        assert "b = 2" in out


# -------------------------------------------------------------- DUMP ARRAYS -
class TestDumpArrays:
    def test_dump_int_array(self, p):
        assert p.dump({"k": [1, 2, 3]}) == "k = [1, 2, 3]\n"

    def test_dump_string_array(self, p):
        assert p.dump({"k": ["a", "b"]}) == 'k = ["a", "b"]\n'

    def test_dump_empty_array(self, p):
        assert p.dump({"k": []}) == "k = []\n"


# -------------------------------------------------------------- DUMP TABLES -
class TestDumpTables:
    def test_dump_simple_table(self, p):
        out = p.dump({"server": {"port": 80}})
        assert "[server]" in out
        assert "port = 80" in out

    def test_dump_nested_table(self, p):
        out = p.dump({"a": {"b": {"x": 1}}})
        assert "[a.b]" in out
        assert "x = 1" in out

    def test_dump_with_top_scalar_and_table(self, p):
        out = p.dump({"name": "top", "t": {"k": 1}})
        assert 'name = "top"' in out
        assert "[t]" in out


# ------------------------------------------------------------- ROUND TRIP --
class TestRoundTrip:
    def test_round_trip_scalars(self, p):
        data = {"a": 1, "b": "x", "c": True, "d": 3.14}
        assert p.parse(p.dump(data)) == data

    def test_round_trip_table(self, p):
        data = {"server": {"port": 80, "host": "x"}}
        assert p.parse(p.dump(data)) == data

    def test_round_trip_array(self, p):
        data = {"items": [1, 2, 3]}
        assert p.parse(p.dump(data)) == data

    def test_round_trip_nested(self, p):
        data = {"a": {"b": {"c": [1, 2]}}, "x": "y"}
        assert p.parse(p.dump(data)) == data

    def test_round_trip_strings_with_escapes(self, p):
        data = {"k": 'line1\nline2\twith "quote"'}
        assert p.parse(p.dump(data)) == data


# ---------------------------------------------------------- PARSE_VALUE ---
class TestParseValue:
    def test_int(self, p):
        assert p.parse_value("42") == 42

    def test_string(self, p):
        assert p.parse_value('"hi"') == "hi"

    def test_bool(self, p):
        assert p.parse_value("true") is True

    def test_array(self, p):
        assert p.parse_value("[1, 2]") == [1, 2]

    def test_trailing_text_invalid(self, p):
        with pytest.raises(ParseError):
            p.parse_value("1 garbage")


# --------------------------------------------------------- FORMAT_VALUE ---
class TestFormatValue:
    def test_int(self, p):
        assert p.format_value(5) == "5"

    def test_str(self, p):
        assert p.format_value("hi") == '"hi"'

    def test_bool(self, p):
        assert p.format_value(False) == "false"

    def test_float_has_dot(self, p):
        # Python's repr(1.0) is '1.0', repr(int)==no dot — we ensure dot
        out = p.format_value(1.0)
        assert "." in out or "e" in out

    def test_list(self, p):
        assert p.format_value([1, 2]) == "[1, 2]"

    def test_inline_dict(self, p):
        assert p.format_value({"a": 1}) == "{a = 1}"

    def test_unsupported(self, p):
        with pytest.raises(ParseError):
            p.format_value(None)


# --------------------------------------------------------------- GET / SET -
class TestGetSet:
    def test_get_simple(self, p):
        data = {"a": 1}
        assert p.get(data, "a") == 1

    def test_get_nested(self, p):
        data = {"a": {"b": {"c": 5}}}
        assert p.get(data, "a.b.c") == 5

    def test_get_missing_default(self, p):
        assert p.get({}, "x.y", default="fallback") == "fallback"

    def test_get_missing_none(self, p):
        assert p.get({}, "x.y") is None

    def test_get_empty_key(self, p):
        assert p.get({"a": 1}, "", default="d") == "d"

    def test_set_simple(self, p):
        data: dict = {}
        p.set(data, "a", 1)
        assert data == {"a": 1}

    def test_set_nested(self, p):
        data: dict = {}
        p.set(data, "a.b.c", 7)
        assert data == {"a": {"b": {"c": 7}}}

    def test_set_overwrite(self, p):
        data = {"a": 1}
        p.set(data, "a", 2)
        assert data == {"a": 2}

    def test_set_invalid_key(self, p):
        with pytest.raises(ParseError):
            p.set({}, "", 1)


# --------------------------------------------------------------- IS_VALID -
class TestIsValid:
    def test_valid_empty(self, p):
        assert p.is_valid("") is True

    def test_valid_kv(self, p):
        assert p.is_valid("x = 1") is True

    def test_valid_table(self, p):
        assert p.is_valid("[t]\nx = 1") is True

    def test_invalid_unterminated(self, p):
        assert p.is_valid('x = "abc') is False

    def test_invalid_no_equals(self, p):
        assert p.is_valid("garbage") is False


# ------------------------------------------------------------- EDGE CASES -
class TestEdgeCases:
    def test_string_with_equals(self, p):
        assert p.parse('x = "a=b"') == {"x": "a=b"}

    def test_string_with_brackets(self, p):
        assert p.parse('x = "[1]"') == {"x": "[1]"}

    def test_trailing_newline(self, p):
        assert p.parse("x = 1\n") == {"x": 1}

    def test_blank_lines_between(self, p):
        text = "x = 1\n\n\ny = 2"
        assert p.parse(text) == {"x": 1, "y": 2}

    def test_negative_zero_int(self, p):
        assert p.parse("x = -0") == {"x": 0}

    def test_array_in_table(self, p):
        text = "[t]\nitems = [1, 2, 3]"
        assert p.parse(text) == {"t": {"items": [1, 2, 3]}}

    def test_dump_then_isvalid(self, p):
        data = {"a": {"b": 1}, "c": [1, 2]}
        assert p.is_valid(p.dump(data)) is True

    def test_string_with_hash_then_real_comment(self, p):
        assert p.parse('x = "a#b" # tail') == {"x": "a#b"}
