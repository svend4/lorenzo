"""Tests for docstoolkit.cli_args."""

import pytest

from docstoolkit.cli_args import (
    ArgType,
    Argument,
    CliParser,
    ParseError,
    ParseResult,
)


# ---------------------------------------------------------------- ArgType


class TestArgType:
    def test_string_member(self):
        assert ArgType.STRING.value == "string"

    def test_int_member(self):
        assert ArgType.INT.value == "int"

    def test_float_member(self):
        assert ArgType.FLOAT.value == "float"

    def test_bool_member(self):
        assert ArgType.BOOL.value == "bool"

    def test_list_string_member(self):
        assert ArgType.LIST_STRING.value == "list_string"

    def test_list_int_member(self):
        assert ArgType.LIST_INT.value == "list_int"

    def test_all_distinct(self):
        assert len({t.value for t in ArgType}) == 6


# ---------------------------------------------------------------- Argument


class TestArgument:
    def test_defaults(self):
        a = Argument(name="verbose")
        assert a.name == "verbose"
        assert a.arg_type == ArgType.STRING
        assert a.required is False
        assert a.default is None
        assert a.short is None
        assert a.help == ""
        assert a.choices is None

    def test_custom_fields(self):
        a = Argument(
            name="port",
            arg_type=ArgType.INT,
            required=True,
            default=8080,
            short="p",
            help="port number",
            choices=[80, 8080],
        )
        assert a.required is True
        assert a.default == 8080
        assert a.short == "p"
        assert a.choices == [80, 8080]

    def test_is_list_true(self):
        assert Argument("x", ArgType.LIST_STRING).is_list is True
        assert Argument("x", ArgType.LIST_INT).is_list is True

    def test_is_list_false(self):
        assert Argument("x", ArgType.STRING).is_list is False

    def test_is_bool(self):
        assert Argument("x", ArgType.BOOL).is_bool is True
        assert Argument("x", ArgType.STRING).is_bool is False


# ---------------------------------------------------------------- ParseResult


class TestParseResult:
    def test_empty_valid(self):
        r = ParseResult()
        assert r.is_valid is True
        assert r.values == {}
        assert r.positional == []
        assert r.errors == []

    def test_with_errors_invalid(self):
        r = ParseResult(errors=["bad"])
        assert r.is_valid is False

    def test_get_existing(self):
        r = ParseResult(values={"x": 1})
        assert r.get("x") == 1

    def test_get_missing_returns_default(self):
        r = ParseResult()
        assert r.get("x", 42) == 42

    def test_get_missing_no_default(self):
        r = ParseResult()
        assert r.get("x") is None


# ---------------------------------------------------------------- AddArgument


class TestAddArgument:
    def test_basic_add(self):
        p = CliParser()
        a = p.add_argument("name")
        assert isinstance(a, Argument)
        assert a.name == "name"

    def test_argument_count_increments(self):
        p = CliParser()
        assert p.argument_count == 0
        p.add_argument("a")
        p.add_argument("b")
        assert p.argument_count == 2

    def test_duplicate_name_raises(self):
        p = CliParser()
        p.add_argument("x")
        with pytest.raises(ValueError):
            p.add_argument("x")

    def test_duplicate_short_raises(self):
        p = CliParser()
        p.add_argument("x", short="x")
        with pytest.raises(ValueError):
            p.add_argument("y", short="x")

    def test_empty_name_raises(self):
        p = CliParser()
        with pytest.raises(ValueError):
            p.add_argument("")

    def test_with_kwargs(self):
        p = CliParser()
        a = p.add_argument("port", ArgType.INT, required=True, default=80)
        assert a.required is True
        assert a.default == 80


# ---------------------------------------------------------------- AddFlag


class TestAddFlag:
    def test_add_flag_creates_bool(self):
        p = CliParser()
        a = p.add_flag("verbose")
        assert a.arg_type == ArgType.BOOL
        assert a.default is False

    def test_add_flag_short(self):
        p = CliParser()
        a = p.add_flag("verbose", short="v")
        assert a.short == "v"

    def test_add_flag_default_false_in_parse(self):
        p = CliParser()
        p.add_flag("verbose")
        r = p.parse([])
        assert r.values["verbose"] is False


# ---------------------------------------------------------------- AddPositional


class TestAddPositional:
    def test_add_positional(self):
        p = CliParser()
        p.add_positional("file")
        assert p.argument_count == 1

    def test_duplicate_positional_raises(self):
        p = CliParser()
        p.add_positional("file")
        with pytest.raises(ValueError):
            p.add_positional("file")

    def test_empty_positional_raises(self):
        p = CliParser()
        with pytest.raises(ValueError):
            p.add_positional("")

    def test_positional_name_conflicts_with_named(self):
        p = CliParser()
        p.add_argument("file")
        with pytest.raises(ValueError):
            p.add_positional("file")


# ---------------------------------------------------------------- ParseString


class TestParseString:
    def test_string_value(self):
        p = CliParser()
        p.add_argument("name")
        r = p.parse(["--name", "alice"])
        assert r.values["name"] == "alice"
        assert r.is_valid

    def test_string_default(self):
        p = CliParser()
        p.add_argument("name", default="bob")
        r = p.parse([])
        assert r.values["name"] == "bob"


# ---------------------------------------------------------------- ParseInt


class TestParseInt:
    def test_int_value(self):
        p = CliParser()
        p.add_argument("port", ArgType.INT)
        r = p.parse(["--port", "8080"])
        assert r.values["port"] == 8080
        assert r.is_valid

    def test_int_invalid_value_error(self):
        p = CliParser()
        p.add_argument("port", ArgType.INT)
        r = p.parse(["--port", "abc"])
        assert not r.is_valid

    def test_int_equals_form(self):
        p = CliParser()
        p.add_argument("port", ArgType.INT)
        r = p.parse(["--port=80"])
        assert r.values["port"] == 80


# ---------------------------------------------------------------- ParseFloat


class TestParseFloat:
    def test_float_value(self):
        p = CliParser()
        p.add_argument("ratio", ArgType.FLOAT)
        r = p.parse(["--ratio", "0.5"])
        assert r.values["ratio"] == 0.5

    def test_float_invalid(self):
        p = CliParser()
        p.add_argument("ratio", ArgType.FLOAT)
        r = p.parse(["--ratio", "xyz"])
        assert not r.is_valid


# ---------------------------------------------------------------- ParseBool


class TestParseBool:
    def test_bool_flag_present(self):
        p = CliParser()
        p.add_flag("verbose")
        r = p.parse(["--verbose"])
        assert r.values["verbose"] is True

    def test_bool_flag_absent(self):
        p = CliParser()
        p.add_flag("verbose")
        r = p.parse([])
        assert r.values["verbose"] is False

    def test_bool_negation(self):
        p = CliParser()
        p.add_argument("verbose", ArgType.BOOL, default=True)
        r = p.parse(["--no-verbose"])
        assert r.values["verbose"] is False

    def test_bool_explicit_value_true(self):
        p = CliParser()
        p.add_argument("verbose", ArgType.BOOL)
        r = p.parse(["--verbose=true"])
        assert r.values["verbose"] is True

    def test_bool_explicit_value_false(self):
        p = CliParser()
        p.add_argument("verbose", ArgType.BOOL)
        r = p.parse(["--verbose=false"])
        assert r.values["verbose"] is False

    def test_bool_invalid_value(self):
        p = CliParser()
        p.add_argument("v", ArgType.BOOL)
        r = p.parse(["--v=maybe"])
        assert not r.is_valid


# ---------------------------------------------------------------- ParseList


class TestParseList:
    def test_list_string_csv(self):
        p = CliParser()
        p.add_argument("items", ArgType.LIST_STRING)
        r = p.parse(["--items=a,b,c"])
        assert r.values["items"] == ["a", "b", "c"]

    def test_list_string_repeated(self):
        p = CliParser()
        p.add_argument("items", ArgType.LIST_STRING)
        r = p.parse(["--items", "a", "--items", "b"])
        assert r.values["items"] == ["a", "b"]

    def test_list_int(self):
        p = CliParser()
        p.add_argument("nums", ArgType.LIST_INT)
        r = p.parse(["--nums=1,2,3"])
        assert r.values["nums"] == [1, 2, 3]

    def test_list_int_invalid(self):
        p = CliParser()
        p.add_argument("nums", ArgType.LIST_INT)
        r = p.parse(["--nums=1,foo"])
        assert not r.is_valid

    def test_list_default_empty(self):
        p = CliParser()
        p.add_argument("items", ArgType.LIST_STRING)
        r = p.parse([])
        assert r.values["items"] == []


# ---------------------------------------------------------------- Short options


class TestParseShortOptions:
    def test_short_with_value_separated(self):
        p = CliParser()
        p.add_argument("port", ArgType.INT, short="p")
        r = p.parse(["-p", "80"])
        assert r.values["port"] == 80

    def test_short_with_value_glued(self):
        p = CliParser()
        p.add_argument("port", ArgType.INT, short="p")
        r = p.parse(["-p80"])
        assert r.values["port"] == 80

    def test_short_flag(self):
        p = CliParser()
        p.add_flag("verbose", short="v")
        r = p.parse(["-v"])
        assert r.values["verbose"] is True

    def test_short_combined_flags(self):
        p = CliParser()
        p.add_flag("verbose", short="v")
        p.add_flag("quiet", short="q")
        r = p.parse(["-vq"])
        assert r.values["verbose"] is True
        assert r.values["quiet"] is True

    def test_short_unknown(self):
        p = CliParser()
        r = p.parse(["-x"])
        assert not r.is_valid

    def test_short_missing_value(self):
        p = CliParser()
        p.add_argument("port", ArgType.INT, short="p")
        r = p.parse(["-p"])
        assert not r.is_valid

    def test_combined_includes_non_bool_errors(self):
        p = CliParser()
        p.add_flag("verbose", short="v")
        p.add_argument("port", ArgType.INT, short="p")
        r = p.parse(["-vp"])
        # -v is bool, -p is non-bool; treat as -v then inline-value for v => error
        assert not r.is_valid


# ---------------------------------------------------------------- Long=value


class TestParseLongEquals:
    def test_long_equals_string(self):
        p = CliParser()
        p.add_argument("name")
        r = p.parse(["--name=alice"])
        assert r.values["name"] == "alice"

    def test_long_equals_empty_value(self):
        p = CliParser()
        p.add_argument("name")
        r = p.parse(["--name="])
        assert r.values["name"] == ""


# ---------------------------------------------------------------- Long space


class TestParseLongSpace:
    def test_long_space_string(self):
        p = CliParser()
        p.add_argument("name")
        r = p.parse(["--name", "alice"])
        assert r.values["name"] == "alice"

    def test_long_missing_value(self):
        p = CliParser()
        p.add_argument("name")
        r = p.parse(["--name"])
        assert not r.is_valid

    def test_unknown_long(self):
        p = CliParser()
        r = p.parse(["--unknown=x"])
        assert not r.is_valid


# ---------------------------------------------------------------- Positional


class TestPositional:
    def test_one_positional(self):
        p = CliParser()
        p.add_positional("file")
        r = p.parse(["a.txt"])
        assert r.values["file"] == "a.txt"

    def test_multiple_positionals(self):
        p = CliParser()
        p.add_positional("src")
        p.add_positional("dst")
        r = p.parse(["a", "b"])
        assert r.values["src"] == "a"
        assert r.values["dst"] == "b"

    def test_positional_missing(self):
        p = CliParser()
        p.add_positional("file")
        r = p.parse([])
        assert not r.is_valid

    def test_extra_positional_collected(self):
        p = CliParser()
        p.add_positional("src")
        r = p.parse(["a", "b", "c"])
        assert r.values["src"] == "a"
        assert r.positional == ["b", "c"]

    def test_positional_int_type(self):
        p = CliParser()
        p.add_positional("n", ArgType.INT)
        r = p.parse(["42"])
        assert r.values["n"] == 42

    def test_positional_with_named_intermixed(self):
        p = CliParser()
        p.add_argument("name")
        p.add_positional("file")
        r = p.parse(["--name", "alice", "a.txt"])
        assert r.values["name"] == "alice"
        assert r.values["file"] == "a.txt"


# ---------------------------------------------------------------- Required


class TestRequired:
    def test_required_missing(self):
        p = CliParser()
        p.add_argument("name", required=True)
        r = p.parse([])
        assert not r.is_valid

    def test_required_present(self):
        p = CliParser()
        p.add_argument("name", required=True)
        r = p.parse(["--name", "alice"])
        assert r.is_valid


# ---------------------------------------------------------------- Default


class TestDefault:
    def test_default_used(self):
        p = CliParser()
        p.add_argument("port", ArgType.INT, default=80)
        r = p.parse([])
        assert r.values["port"] == 80

    def test_default_overridden(self):
        p = CliParser()
        p.add_argument("port", ArgType.INT, default=80)
        r = p.parse(["--port", "9090"])
        assert r.values["port"] == 9090


# ---------------------------------------------------------------- Choices


class TestChoices:
    def test_choices_valid(self):
        p = CliParser()
        p.add_argument("color", choices=["red", "green", "blue"])
        r = p.parse(["--color", "red"])
        assert r.is_valid
        assert r.values["color"] == "red"

    def test_choices_invalid(self):
        p = CliParser()
        p.add_argument("color", choices=["red", "green"])
        r = p.parse(["--color", "purple"])
        assert not r.is_valid

    def test_choices_int(self):
        p = CliParser()
        p.add_argument("level", ArgType.INT, choices=[1, 2, 3])
        r = p.parse(["--level", "2"])
        assert r.is_valid

    def test_choices_int_invalid(self):
        p = CliParser()
        p.add_argument("level", ArgType.INT, choices=[1, 2, 3])
        r = p.parse(["--level", "5"])
        assert not r.is_valid

    def test_choices_list(self):
        p = CliParser()
        p.add_argument("tags", ArgType.LIST_STRING, choices=["a", "b", "c"])
        r = p.parse(["--tags=a,b"])
        assert r.is_valid


# ---------------------------------------------------------------- EndOfOptions


class TestEndOfOptions:
    def test_double_dash_stops_options(self):
        p = CliParser()
        p.add_argument("name")
        r = p.parse(["--", "--name", "alice"])
        assert r.values["name"] is None
        assert r.positional == ["--name", "alice"]

    def test_double_dash_with_positionals(self):
        p = CliParser()
        p.add_positional("file")
        r = p.parse(["--", "-weird-name"])
        assert r.values["file"] == "-weird-name"


# ---------------------------------------------------------------- Strict


class TestParseStrict:
    def test_strict_returns_values(self):
        p = CliParser()
        p.add_argument("name")
        d = p.parse_strict(["--name", "alice"])
        assert d["name"] == "alice"

    def test_strict_raises_on_error(self):
        p = CliParser()
        p.add_argument("name", required=True)
        with pytest.raises(ParseError):
            p.parse_strict([])

    def test_strict_raises_on_unknown(self):
        p = CliParser()
        with pytest.raises(ParseError):
            p.parse_strict(["--unknown"])


# ---------------------------------------------------------------- FormatHelp


class TestFormatHelp:
    def test_format_usage_contains_program(self):
        p = CliParser(program_name="myprog")
        assert "myprog" in p.format_usage()

    def test_format_usage_lists_args(self):
        p = CliParser()
        p.add_argument("name")
        usage = p.format_usage()
        assert "--name" in usage

    def test_format_help_contains_description(self):
        p = CliParser(description="A neat tool")
        assert "A neat tool" in p.format_help()

    def test_format_help_lists_argument(self):
        p = CliParser()
        p.add_argument("name", help="user name")
        h = p.format_help()
        assert "--name" in h
        assert "user name" in h

    def test_format_help_marks_required(self):
        p = CliParser()
        p.add_argument("name", required=True)
        h = p.format_help()
        assert "required" in h

    def test_format_help_shows_default(self):
        p = CliParser()
        p.add_argument("port", ArgType.INT, default=80)
        h = p.format_help()
        assert "80" in h

    def test_format_help_shows_positional(self):
        p = CliParser()
        p.add_positional("file", help="input file")
        h = p.format_help()
        assert "file" in h
        assert "input file" in h

    def test_format_help_shows_choices(self):
        p = CliParser()
        p.add_argument("color", choices=["red", "green"])
        h = p.format_help()
        assert "red" in h


# ---------------------------------------------------------------- EdgeCases


class TestEdgeCases:
    def test_empty_argv(self):
        p = CliParser()
        r = p.parse([])
        assert r.is_valid
        assert r.values == {}

    def test_only_flags(self):
        p = CliParser()
        p.add_flag("a")
        p.add_flag("b")
        r = p.parse(["--a", "--b"])
        assert r.values["a"] is True
        assert r.values["b"] is True

    def test_positional_before_option(self):
        p = CliParser()
        p.add_argument("name")
        p.add_positional("file")
        r = p.parse(["a.txt", "--name", "alice"])
        assert r.values["file"] == "a.txt"
        assert r.values["name"] == "alice"

    def test_short_dash_alone_is_positional(self):
        p = CliParser()
        p.add_positional("file")
        r = p.parse(["-"])
        assert r.values["file"] == "-"

    def test_argument_count_with_positional(self):
        p = CliParser()
        p.add_argument("name")
        p.add_positional("file")
        assert p.argument_count == 2

    def test_multiple_errors_collected(self):
        p = CliParser()
        p.add_argument("name", required=True)
        p.add_argument("port", ArgType.INT, required=True)
        r = p.parse([])
        assert len(r.errors) >= 2

    def test_list_repeated_with_csv(self):
        p = CliParser()
        p.add_argument("items", ArgType.LIST_STRING)
        r = p.parse(["--items=a,b", "--items", "c"])
        assert r.values["items"] == ["a", "b", "c"]

    def test_parse_result_get_method_after_parse(self):
        p = CliParser()
        p.add_argument("name", default="x")
        r = p.parse([])
        assert r.get("name") == "x"
        assert r.get("missing", "fallback") == "fallback"
