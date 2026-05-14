"""Tests for docstoolkit.ini_parser."""
import pytest

from docstoolkit.ini_parser import (
    IniFile,
    IniParser,
    IniSection,
    ParseError,
)


@pytest.fixture()
def p():
    return IniParser()


# -------------------------------------------------------------- IniSection ---
class TestIniSection:
    def test_default_construction(self):
        sec = IniSection(name="foo")
        assert sec.name == "foo"
        assert sec.entries == {}
        assert sec.comments == []

    def test_entries_isolated(self):
        a = IniSection(name="a")
        b = IniSection(name="b")
        a.entries["x"] = "1"
        assert "x" not in b.entries

    def test_comments_isolated(self):
        a = IniSection(name="a")
        b = IniSection(name="b")
        a.comments.append("; a")
        assert b.comments == []

    def test_with_data(self):
        sec = IniSection(
            name="srv",
            entries={"port": "80"},
            comments=["; main"],
        )
        assert sec.entries["port"] == "80"
        assert sec.comments == ["; main"]


# ----------------------------------------------------------------- IniFile ---
class TestIniFile:
    def test_default_construction(self):
        ini = IniFile()
        assert ini.sections == {}
        assert ini.header_comments == []

    def test_section_names_empty(self):
        assert IniFile().section_names == []

    def test_section_names_preserves_order(self):
        ini = IniFile()
        ini.sections["z"] = IniSection(name="z")
        ini.sections["a"] = IniSection(name="a")
        ini.sections["m"] = IniSection(name="m")
        assert ini.section_names == ["z", "a", "m"]

    def test_get_section_present(self):
        ini = IniFile()
        ini.sections["s"] = IniSection(name="s")
        assert ini.get_section("s").name == "s"

    def test_get_section_missing_returns_none(self):
        assert IniFile().get_section("nope") is None


# -------------------------------------------------------------- parse basic --
class TestParseBasic:
    def test_single_section_single_key(self, p):
        ini = p.parse("[s]\nk = v")
        assert ini.section_names == ["s"]
        assert ini.sections["s"].entries == {"k": "v"}

    def test_multiple_sections(self, p):
        ini = p.parse("[a]\nx = 1\n[b]\ny = 2")
        assert ini.section_names == ["a", "b"]
        assert ini.sections["a"].entries == {"x": "1"}
        assert ini.sections["b"].entries == {"y": "2"}

    def test_returns_ini_file_instance(self, p):
        assert isinstance(p.parse("[a]\nk = v"), IniFile)

    def test_preserves_key_order(self, p):
        ini = p.parse("[s]\nb = 2\nz = 9\na = 1")
        assert list(ini.sections["s"].entries.keys()) == ["b", "z", "a"]

    def test_value_with_spaces(self, p):
        ini = p.parse("[s]\nk = hello world")
        assert ini.sections["s"].entries["k"] == "hello world"

    def test_reopen_section(self, p):
        ini = p.parse("[a]\nx = 1\n[b]\ny = 2\n[a]\nz = 3")
        assert ini.sections["a"].entries == {"x": "1", "z": "3"}


# ----------------------------------------------------------- parse comments --
class TestParseComments:
    def test_semicolon_comment(self, p):
        ini = p.parse("; hi\n[s]\nk = v")
        assert ini.header_comments == ["; hi"]

    def test_hash_comment(self, p):
        ini = p.parse("# hi\n[s]\nk = v")
        assert ini.header_comments == ["# hi"]

    def test_section_comment_captured(self, p):
        ini = p.parse("[a]\nk = v\n; before b\n[b]\nx = 1")
        assert ini.sections["b"].comments == ["; before b"]

    def test_multiple_header_comments(self, p):
        ini = p.parse("; one\n; two\n# three\n[s]\nk = v")
        assert ini.header_comments == ["; one", "; two", "# three"]

    def test_blank_lines_between_comments(self, p):
        ini = p.parse("; one\n\n; two\n[s]\nk = v")
        assert ini.header_comments == ["; one", "; two"]

    def test_only_comments_no_section(self, p):
        ini = p.parse("; just a header\n# nothing else")
        assert ini.header_comments == ["; just a header", "# nothing else"]
        assert ini.sections == {}


# ---------------------------------------------------------- parse sections --
class TestParseSections:
    def test_section_with_spaces_in_name(self, p):
        ini = p.parse("[my section]\nk = v")
        assert "my section" in ini.sections

    def test_section_with_special_chars(self, p):
        ini = p.parse("[a.b/c-d_e]\nk = v")
        assert "a.b/c-d_e" in ini.sections

    def test_default_section(self, p):
        ini = p.parse("[DEFAULT]\nlevel = info")
        assert ini.sections["DEFAULT"].entries["level"] == "info"

    def test_section_with_trailing_whitespace(self, p):
        ini = p.parse("[s]   \nk = v")
        assert "s" in ini.sections


# ------------------------------------------------------------ parse values --
class TestParseValues:
    def test_equals_separator(self, p):
        ini = p.parse("[s]\nk = v")
        assert ini.sections["s"].entries["k"] == "v"

    def test_colon_separator(self, p):
        ini = p.parse("[s]\nk: v")
        assert ini.sections["s"].entries["k"] == "v"

    def test_no_space_around_equals(self, p):
        ini = p.parse("[s]\nk=v")
        assert ini.sections["s"].entries["k"] == "v"

    def test_value_keeps_internal_spaces(self, p):
        ini = p.parse("[s]\nk = a  b  c")
        assert ini.sections["s"].entries["k"] == "a  b  c"

    def test_empty_value(self, p):
        ini = p.parse("[s]\nk =")
        assert ini.sections["s"].entries["k"] == ""

    def test_numeric_value_stored_as_string(self, p):
        ini = p.parse("[s]\nport = 8080")
        assert ini.sections["s"].entries["port"] == "8080"


# ------------------------------------------------------------- parse empty --
class TestParseEmpty:
    def test_empty_string(self, p):
        ini = p.parse("")
        assert ini.sections == {}
        assert ini.header_comments == []

    def test_only_whitespace(self, p):
        ini = p.parse("\n\n\n   \n")
        assert ini.sections == {}

    def test_section_no_keys(self, p):
        ini = p.parse("[empty]")
        assert "empty" in ini.sections
        assert ini.sections["empty"].entries == {}


# ------------------------------------------------------------ parse invalid --
class TestParseInvalid:
    def test_non_string_input(self, p):
        with pytest.raises(ParseError):
            p.parse(42)

    def test_empty_section_name(self, p):
        with pytest.raises(ParseError):
            p.parse("[]\nk = v")

    def test_key_without_separator(self, p):
        with pytest.raises(ParseError):
            p.parse("[s]\nbroken_line")

    def test_value_without_section(self, p):
        with pytest.raises(ParseError):
            p.parse("orphan = 1")

    def test_missing_key(self, p):
        with pytest.raises(ParseError):
            p.parse("[s]\n = value")


# -------------------------------------------------------------------- dump --
class TestDump:
    def test_empty(self, p):
        assert p.dump(IniFile()) == ""

    def test_single_section(self, p):
        ini = IniFile()
        ini.sections["s"] = IniSection(name="s", entries={"k": "v"})
        out = p.dump(ini)
        assert "[s]" in out
        assert "k = v" in out

    def test_multiple_sections_separated_by_blank(self, p):
        ini = IniFile()
        ini.sections["a"] = IniSection(name="a", entries={"x": "1"})
        ini.sections["b"] = IniSection(name="b", entries={"y": "2"})
        out = p.dump(ini)
        assert "[a]" in out and "[b]" in out
        assert "\n\n[b]" in out

    def test_header_comments_dumped(self, p):
        ini = IniFile(header_comments=["; top"])
        ini.sections["s"] = IniSection(name="s", entries={"k": "v"})
        out = p.dump(ini)
        assert out.startswith("; top")

    def test_section_comments_dumped(self, p):
        ini = IniFile()
        ini.sections["s"] = IniSection(
            name="s",
            entries={"k": "v"},
            comments=["; about s"],
        )
        out = p.dump(ini)
        assert "; about s" in out
        assert out.index("; about s") < out.index("[s]")


# --------------------------------------------------------------- roundtrip --
class TestRoundTrip:
    def test_basic_roundtrip(self, p):
        text = "[s]\nk = v\n"
        again = p.dump(p.parse(text))
        ini2 = p.parse(again)
        assert ini2.sections["s"].entries == {"k": "v"}

    def test_multi_section_roundtrip(self, p):
        text = "[a]\nx = 1\n[b]\ny = 2\n"
        ini2 = p.parse(p.dump(p.parse(text)))
        assert ini2.section_names == ["a", "b"]
        assert ini2.sections["a"].entries == {"x": "1"}
        assert ini2.sections["b"].entries == {"y": "2"}

    def test_roundtrip_with_comments(self, p):
        text = "; top\n[s]\nk = v\n"
        ini2 = p.parse(p.dump(p.parse(text)))
        assert ini2.header_comments == ["; top"]


# --------------------------------------------------------------------- get --
class TestGet:
    def test_simple(self, p):
        assert p.get("[s]\nk = v", "s", "k") == "v"

    def test_missing_key_returns_default(self, p):
        assert p.get("[s]\nk = v", "s", "nope", default="d") == "d"

    def test_missing_section_returns_default(self, p):
        assert p.get("[s]\nk = v", "x", "k") is None

    def test_default_section_fallback(self, p):
        text = "[DEFAULT]\nlevel = info\n[srv]\nport = 80"
        assert p.get(text, "srv", "level") == "info"

    def test_specific_overrides_default(self, p):
        text = "[DEFAULT]\nlevel = info\n[srv]\nlevel = debug"
        assert p.get(text, "srv", "level") == "debug"


# ----------------------------------------------------------------- get_int --
class TestGetInt:
    def test_basic(self, p):
        assert p.get_int("[s]\nn = 42", "s", "n") == 42

    def test_negative(self, p):
        assert p.get_int("[s]\nn = -7", "s", "n") == -7

    def test_missing_returns_default(self, p):
        assert p.get_int("[s]\nn = 1", "s", "x", default=99) == 99

    def test_invalid_returns_default(self, p):
        assert p.get_int("[s]\nn = abc", "s", "n", default=5) == 5

    def test_float_string_truncated(self, p):
        assert p.get_int("[s]\nn = 3.7", "s", "n") == 3


# --------------------------------------------------------------- get_float --
class TestGetFloat:
    def test_basic(self, p):
        assert p.get_float("[s]\nn = 3.14", "s", "n") == 3.14

    def test_int_value(self, p):
        assert p.get_float("[s]\nn = 5", "s", "n") == 5.0

    def test_missing_returns_default(self, p):
        assert p.get_float("[s]\nn = 1", "s", "x", default=2.5) == 2.5

    def test_invalid_returns_default(self, p):
        assert p.get_float("[s]\nn = wat", "s", "n", default=0.1) == 0.1


# ---------------------------------------------------------------- get_bool --
class TestGetBool:
    @pytest.mark.parametrize("v", ["true", "True", "1", "yes", "YES", "on"])
    def test_truthy(self, p, v):
        assert p.get_bool(f"[s]\nb = {v}", "s", "b") is True

    @pytest.mark.parametrize("v", ["false", "0", "no", "off", "OFF"])
    def test_falsy(self, p, v):
        assert p.get_bool(f"[s]\nb = {v}", "s", "b") is False

    def test_missing_returns_default(self, p):
        assert p.get_bool("[s]\nb = true", "s", "x", default=True) is True

    def test_invalid_returns_default(self, p):
        assert p.get_bool("[s]\nb = maybe", "s", "b", default=True) is True


# ---------------------------------------------------------------- get_list --
class TestGetList:
    def test_basic(self, p):
        assert p.get_list("[s]\nl = a,b,c", "s", "l") == ["a", "b", "c"]

    def test_strips_items(self, p):
        assert p.get_list("[s]\nl = a , b , c", "s", "l") == ["a", "b", "c"]

    def test_custom_separator(self, p):
        assert p.get_list(
            "[s]\nl = a|b|c", "s", "l", separator="|"
        ) == ["a", "b", "c"]

    def test_missing_returns_empty(self, p):
        assert p.get_list("[s]\nl = a", "s", "x") == []

    def test_empty_value(self, p):
        assert p.get_list("[s]\nl =", "s", "l") == []

    def test_single_item(self, p):
        assert p.get_list("[s]\nl = only", "s", "l") == ["only"]


# --------------------------------------------------------------------- set --
class TestSet:
    def test_update_existing(self, p):
        out = p.set("[s]\nk = v\n", "s", "k", "new")
        assert p.get(out, "s", "k") == "new"

    def test_add_new_key(self, p):
        out = p.set("[s]\nk = v\n", "s", "x", "1")
        assert p.get(out, "s", "x") == "1"
        assert p.get(out, "s", "k") == "v"

    def test_add_new_section(self, p):
        out = p.set("[s]\nk = v\n", "new", "z", "9")
        assert p.get(out, "new", "z") == "9"
        assert p.get(out, "s", "k") == "v"

    def test_empty_text(self, p):
        out = p.set("", "s", "k", "v")
        assert p.get(out, "s", "k") == "v"


# -------------------------------------------------------------- remove_key --
class TestRemoveKey:
    def test_existing(self, p):
        out = p.remove_key("[s]\nk = v\nx = 1\n", "s", "k")
        assert p.get(out, "s", "k") is None
        assert p.get(out, "s", "x") == "1"

    def test_missing_key_no_error(self, p):
        out = p.remove_key("[s]\nk = v\n", "s", "nope")
        assert p.get(out, "s", "k") == "v"

    def test_missing_section_no_error(self, p):
        out = p.remove_key("[s]\nk = v\n", "no", "k")
        assert p.get(out, "s", "k") == "v"


# ----------------------------------------------------------- remove_section -
class TestRemoveSection:
    def test_existing(self, p):
        out = p.remove_section("[a]\nx = 1\n[b]\ny = 2\n", "a")
        ini = p.parse(out)
        assert "a" not in ini.sections
        assert "b" in ini.sections

    def test_missing_section_no_error(self, p):
        out = p.remove_section("[s]\nk = v\n", "nope")
        assert p.get(out, "s", "k") == "v"


# ------------------------------------------------------------------- merge --
class TestMerge:
    def test_b_overrides_a(self, p):
        a = p.parse("[s]\nk = original")
        b = p.parse("[s]\nk = overridden")
        merged = p.merge(a, b)
        assert merged.sections["s"].entries["k"] == "overridden"

    def test_extends_with_new_keys(self, p):
        a = p.parse("[s]\nx = 1")
        b = p.parse("[s]\ny = 2")
        merged = p.merge(a, b)
        assert merged.sections["s"].entries == {"x": "1", "y": "2"}

    def test_keeps_a_only_sections(self, p):
        a = p.parse("[a]\nx = 1\n[b]\ny = 2")
        b = p.parse("[c]\nz = 3")
        merged = p.merge(a, b)
        assert merged.section_names == ["a", "b", "c"]

    def test_adds_b_only_sections(self, p):
        a = p.parse("[a]\nx = 1")
        b = p.parse("[new]\nk = v")
        merged = p.merge(a, b)
        assert "new" in merged.sections
        assert merged.sections["new"].entries == {"k": "v"}

    def test_returns_new_instance(self, p):
        a = p.parse("[s]\nk = v")
        b = p.parse("[s]\nk = w")
        merged = p.merge(a, b)
        assert merged is not a and merged is not b


# ---------------------------------------------------------------- is_valid --
class TestIsValid:
    def test_valid(self, p):
        assert p.is_valid("[s]\nk = v") is True

    def test_valid_empty(self, p):
        assert p.is_valid("") is True

    def test_invalid_orphan_key(self, p):
        assert p.is_valid("orphan = 1") is False

    def test_invalid_empty_section(self, p):
        assert p.is_valid("[]\nk = v") is False

    def test_invalid_no_separator(self, p):
        assert p.is_valid("[s]\njust-a-word") is False


# -------------------------------------------------------------- edge cases --
class TestEdgeCases:
    def test_section_name_with_brackets_not_supported(self, p):
        # closing bracket inside name is not allowed by our grammar
        with pytest.raises(ParseError):
            p.parse("[bad]extra]\nk = v")

    def test_value_with_equals_sign(self, p):
        # first separator wins → everything after it is the value
        ini = p.parse("[s]\nurl = a=b=c")
        assert ini.sections["s"].entries["url"] == "a=b=c"

    def test_value_with_colon(self, p):
        ini = p.parse("[s]\nk = http://example.com")
        # = comes before :, so value is the full URL
        assert ini.sections["s"].entries["k"] == "http://example.com"

    def test_colon_then_equals(self, p):
        ini = p.parse("[s]\nk: a=b")
        assert ini.sections["s"].entries["k"] == "a=b"

    def test_case_sensitive_keys(self, p):
        ini = p.parse("[s]\nKey = 1\nkey = 2")
        assert ini.sections["s"].entries == {"Key": "1", "key": "2"}

    def test_keys_preserve_insertion_order_after_set(self, p):
        text = "[s]\na = 1\nb = 2\n"
        out = p.set(text, "s", "c", "3")
        ini = p.parse(out)
        assert list(ini.sections["s"].entries.keys()) == ["a", "b", "c"]

    def test_unicode_values(self, p):
        ini = p.parse("[s]\nname = Юникод")
        assert ini.sections["s"].entries["name"] == "Юникод"

    def test_dump_then_parse_preserves_section_count(self, p):
        text = "[a]\nx = 1\n[b]\ny = 2\n[c]\nz = 3\n"
        ini = p.parse(p.dump(p.parse(text)))
        assert ini.section_names == ["a", "b", "c"]
