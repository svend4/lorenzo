"""Tests for the structured_output module (E36).

Run with:
    cd /home/user/lorenzo/docs-toolkit && python -m pytest tests/test_structured_output.py -q
"""

from __future__ import annotations

import pytest

from docstoolkit.structured_output import (
    ExtractionResult,
    FieldSchema,
    FieldType,
    OutputSchema,
    OutputValidator,
    ParseConfig,
    ParseResult,
    StructuredExtractor,
    StructuredOutputParser,
    ValidationError,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_schema(schema_name: str = "test", **kwargs) -> OutputSchema:
    """Build a simple OutputSchema from keyword arguments.

    Each kwarg: field_name=(FieldType, required, default)
    or field_name=FieldType  (required=True, default=None)
    """
    fields = []
    for fname, spec in kwargs.items():
        if isinstance(spec, FieldType):
            fields.append(FieldSchema(fname, spec))
        else:
            ft, req, default = spec
            fields.append(FieldSchema(fname, ft, required=req, default=default))
    return OutputSchema(name=schema_name, fields=fields)


# ===========================================================================
# OutputSchema tests
# ===========================================================================

class TestOutputSchema:
    def test_field_names_empty(self):
        schema = OutputSchema(name="empty")
        assert schema.field_names() == []

    def test_field_names(self):
        schema = make_schema("s", x=FieldType.STRING, y=FieldType.INTEGER)
        assert schema.field_names() == ["x", "y"]

    def test_required_fields(self):
        schema = OutputSchema(
            name="s",
            fields=[
                FieldSchema("a", FieldType.STRING, required=True),
                FieldSchema("b", FieldType.INTEGER, required=False),
                FieldSchema("c", FieldType.FLOAT, required=True),
            ],
        )
        assert [f.name for f in schema.required_fields()] == ["a", "c"]

    def test_optional_fields(self):
        schema = OutputSchema(
            name="s",
            fields=[
                FieldSchema("a", FieldType.STRING, required=True),
                FieldSchema("b", FieldType.INTEGER, required=False, default=0),
            ],
        )
        assert [f.name for f in schema.optional_fields()] == ["b"]

    def test_all_required(self):
        schema = make_schema("s", x=FieldType.STRING, y=FieldType.FLOAT)
        assert len(schema.optional_fields()) == 0
        assert len(schema.required_fields()) == 2

    def test_all_optional(self):
        schema = OutputSchema(
            name="s",
            fields=[
                FieldSchema("a", FieldType.STRING, required=False),
                FieldSchema("b", FieldType.INTEGER, required=False),
            ],
        )
        assert len(schema.required_fields()) == 0
        assert len(schema.optional_fields()) == 2

    def test_field_schema_defaults(self):
        fs = FieldSchema("x", FieldType.STRING)
        assert fs.required is True
        assert fs.default is None
        assert fs.description == ""

    def test_field_schema_custom(self):
        fs = FieldSchema("x", FieldType.INTEGER, required=False, default=42, description="count")
        assert fs.required is False
        assert fs.default == 42
        assert fs.description == "count"

    def test_output_schema_name(self):
        schema = OutputSchema(name="my_schema")
        assert schema.name == "my_schema"


# ===========================================================================
# ExtractionResult tests
# ===========================================================================

class TestExtractionResult:
    def test_is_complete_true(self):
        r = ExtractionResult(data={"a": 1}, missing_fields=[], parse_errors=[], raw_text="")
        assert r.is_complete() is True

    def test_is_complete_false(self):
        r = ExtractionResult(data={}, missing_fields=["x"], parse_errors=[], raw_text="")
        assert r.is_complete() is False

    def test_is_valid_true(self):
        r = ExtractionResult(data={}, missing_fields=[], parse_errors=[], raw_text="")
        assert r.is_valid() is True

    def test_is_valid_false(self):
        r = ExtractionResult(data={}, missing_fields=[], parse_errors=["err"], raw_text="")
        assert r.is_valid() is False

    def test_is_complete_and_valid(self):
        r = ExtractionResult(data={"a": 1}, missing_fields=[], parse_errors=[], raw_text="t")
        assert r.is_complete() and r.is_valid()


# ===========================================================================
# StructuredExtractor — extract_json
# ===========================================================================

class TestExtractJson:
    def setup_method(self):
        self.ex = StructuredExtractor()

    def test_plain_json(self):
        result = self.ex.extract_json('{"key": "value"}')
        assert result == {"key": "value"}

    def test_json_in_prose(self):
        text = "Here is the result: {\"name\": \"Alice\", \"age\": 30} that was it."
        result = self.ex.extract_json(text)
        assert result == {"name": "Alice", "age": 30}

    def test_json_in_code_fence(self):
        text = "```json\n{\"x\": 1}\n```"
        result = self.ex.extract_json(text)
        assert result == {"x": 1}

    def test_nested_json(self):
        text = '{"outer": {"inner": 42}}'
        result = self.ex.extract_json(text)
        assert result == {"outer": {"inner": 42}}

    def test_json_with_list_value(self):
        text = '{"items": [1, 2, 3]}'
        result = self.ex.extract_json(text)
        assert result == {"items": [1, 2, 3]}

    def test_no_json(self):
        result = self.ex.extract_json("no json here at all")
        assert result is None

    def test_malformed_json(self):
        result = self.ex.extract_json("{broken json}")
        assert result is None

    def test_malformed_then_valid(self):
        text = "{broken} then {\"ok\": true}"
        result = self.ex.extract_json(text)
        assert result == {"ok": True}

    def test_empty_object(self):
        result = self.ex.extract_json("{}")
        assert result == {}

    def test_json_with_string_containing_braces(self):
        text = '{"msg": "say {hello}"}'
        result = self.ex.extract_json(text)
        assert result == {"msg": "say {hello}"}

    def test_returns_first_json_object(self):
        text = '{"first": 1} {"second": 2}'
        result = self.ex.extract_json(text)
        assert result == {"first": 1}

    def test_array_not_returned_as_dict(self):
        result = self.ex.extract_json("[1, 2, 3]")
        assert result is None

    def test_unicode_values(self):
        text = '{"greeting": "Привет"}'
        result = self.ex.extract_json(text)
        assert result == {"greeting": "Привет"}


# ===========================================================================
# StructuredExtractor — extract_markdown_table
# ===========================================================================

class TestExtractMarkdownTable:
    def setup_method(self):
        self.ex = StructuredExtractor()

    def test_basic_table(self):
        text = "| Name | Age |\n|------|-----|\n| Alice | 30 |\n| Bob | 25 |"
        rows = self.ex.extract_markdown_table(text)
        assert len(rows) == 2
        assert rows[0] == {"Name": "Alice", "Age": "30"}
        assert rows[1] == {"Name": "Bob", "Age": "25"}

    def test_single_row(self):
        text = "| City | Country |\n|------|---------|\n| Paris | France |"
        rows = self.ex.extract_markdown_table(text)
        assert rows == [{"City": "Paris", "Country": "France"}]

    def test_no_table(self):
        text = "No table here, just text."
        rows = self.ex.extract_markdown_table(text)
        assert rows == []

    def test_empty_string(self):
        rows = self.ex.extract_markdown_table("")
        assert rows == []

    def test_three_columns(self):
        text = "| A | B | C |\n|---|---|---|\n| 1 | 2 | 3 |"
        rows = self.ex.extract_markdown_table(text)
        assert rows == [{"A": "1", "B": "2", "C": "3"}]

    def test_header_only_no_data(self):
        text = "| Name | Value |\n|------|-------|\n"
        rows = self.ex.extract_markdown_table(text)
        assert rows == []

    def test_table_no_separator(self):
        text = "| Name | Age |\n| Alice | 30 |"
        rows = self.ex.extract_markdown_table(text)
        assert rows == []

    def test_aligned_separator(self):
        text = "| Name | Score |\n|:-----|------:|\n| Alice | 95 |"
        rows = self.ex.extract_markdown_table(text)
        assert rows == [{"Name": "Alice", "Score": "95"}]

    def test_whitespace_trimmed(self):
        text = "|  Name  |  Age  |\n|--------|-------|\n|  Bob   |  42   |"
        rows = self.ex.extract_markdown_table(text)
        assert rows[0]["Name"] == "Bob"
        assert rows[0]["Age"] == "42"


# ===========================================================================
# StructuredExtractor — extract_key_value
# ===========================================================================

class TestExtractKeyValue:
    def setup_method(self):
        self.ex = StructuredExtractor()

    def test_basic(self):
        text = "name: Alice\nage: 30"
        result = self.ex.extract_key_value(text)
        assert result == {"name": "Alice", "age": "30"}

    def test_custom_separator(self):
        text = "name=Alice\nage=30"
        result = self.ex.extract_key_value(text, sep="=")
        assert result == {"name": "Alice", "age": "30"}

    def test_skip_empty_lines(self):
        text = "\nname: Alice\n\nage: 30\n"
        result = self.ex.extract_key_value(text)
        assert result == {"name": "Alice", "age": "30"}

    def test_skip_lines_without_sep(self):
        text = "name: Alice\nsome line without separator\nage: 30"
        result = self.ex.extract_key_value(text)
        assert result == {"name": "Alice", "age": "30"}

    def test_empty_value(self):
        text = "name: \nage: 30"
        result = self.ex.extract_key_value(text)
        assert result["name"] == ""
        assert result["age"] == "30"

    def test_value_with_colon(self):
        text = "url: http://example.com:8080/path"
        result = self.ex.extract_key_value(text)
        assert result["url"] == "http://example.com:8080/path"

    def test_empty_text(self):
        result = self.ex.extract_key_value("")
        assert result == {}

    def test_whitespace_stripped_from_key(self):
        text = "  name  : Alice"
        result = self.ex.extract_key_value(text)
        assert "name" in result


# ===========================================================================
# StructuredExtractor — extract_code_block
# ===========================================================================

class TestExtractCodeBlock:
    def setup_method(self):
        self.ex = StructuredExtractor()

    def test_any_lang(self):
        text = "```\nhello world\n```"
        result = self.ex.extract_code_block(text)
        assert result == "hello world"

    def test_specific_lang(self):
        text = "```python\nprint('hi')\n```"
        result = self.ex.extract_code_block(text, lang="python")
        assert result == "print('hi')"

    def test_wrong_lang_returns_none(self):
        text = "```python\nprint('hi')\n```"
        result = self.ex.extract_code_block(text, lang="json")
        assert result is None

    def test_no_fence_returns_none(self):
        result = self.ex.extract_code_block("no code here")
        assert result is None

    def test_multiline_content(self):
        text = "```\nline1\nline2\nline3\n```"
        result = self.ex.extract_code_block(text)
        assert "line1" in result
        assert "line2" in result
        assert "line3" in result

    def test_json_block(self):
        text = 'Some text\n```json\n{"key": "value"}\n```\nMore text'
        result = self.ex.extract_code_block(text, lang="json")
        assert result == '{"key": "value"}'

    def test_empty_block(self):
        text = "```\n```"
        result = self.ex.extract_code_block(text)
        assert result == ""

    def test_unclosed_fence_returns_none(self):
        text = "```python\nprint('hi')"
        result = self.ex.extract_code_block(text, lang="python")
        assert result is None


# ===========================================================================
# OutputValidator — coerce
# ===========================================================================

class TestCoerce:
    def setup_method(self):
        self.v = OutputValidator()

    def test_string_coerce(self):
        assert self.v.coerce(42, FieldType.STRING) == "42"

    def test_integer_from_int(self):
        assert self.v.coerce(5, FieldType.INTEGER) == 5

    def test_integer_from_string(self):
        assert self.v.coerce("42", FieldType.INTEGER) == 42

    def test_integer_from_float_whole(self):
        assert self.v.coerce(3.0, FieldType.INTEGER) == 3

    def test_integer_from_float_fractional_raises(self):
        with pytest.raises(ValueError):
            self.v.coerce(3.5, FieldType.INTEGER)

    def test_integer_from_bad_string_raises(self):
        with pytest.raises(ValueError):
            self.v.coerce("hello", FieldType.INTEGER)

    def test_float_from_int(self):
        assert self.v.coerce(3, FieldType.FLOAT) == 3.0

    def test_float_from_string(self):
        assert self.v.coerce("3.14", FieldType.FLOAT) == 3.14

    def test_float_from_bad_string_raises(self):
        with pytest.raises(ValueError):
            self.v.coerce("abc", FieldType.FLOAT)

    def test_boolean_true_values(self):
        for val in ["true", "True", "TRUE", "yes", "YES", "1", "on", "ON"]:
            assert self.v.coerce(val, FieldType.BOOLEAN) is True

    def test_boolean_false_values(self):
        for val in ["false", "False", "FALSE", "no", "NO", "0", "off", "OFF"]:
            assert self.v.coerce(val, FieldType.BOOLEAN) is False

    def test_boolean_from_bool(self):
        assert self.v.coerce(True, FieldType.BOOLEAN) is True
        assert self.v.coerce(False, FieldType.BOOLEAN) is False

    def test_boolean_from_int_0_1(self):
        assert self.v.coerce(1, FieldType.BOOLEAN) is True
        assert self.v.coerce(0, FieldType.BOOLEAN) is False

    def test_boolean_from_int_other_raises(self):
        with pytest.raises(ValueError):
            self.v.coerce(2, FieldType.BOOLEAN)

    def test_boolean_bad_string_raises(self):
        with pytest.raises(ValueError):
            self.v.coerce("maybe", FieldType.BOOLEAN)

    def test_list_from_list(self):
        assert self.v.coerce([1, 2], FieldType.LIST) == [1, 2]

    def test_list_from_json_string(self):
        assert self.v.coerce("[1, 2, 3]", FieldType.LIST) == [1, 2, 3]

    def test_list_from_bad_string_raises(self):
        with pytest.raises(ValueError):
            self.v.coerce("not a list", FieldType.LIST)

    def test_dict_from_dict(self):
        assert self.v.coerce({"a": 1}, FieldType.DICT) == {"a": 1}

    def test_dict_from_json_string(self):
        assert self.v.coerce('{"a": 1}', FieldType.DICT) == {"a": 1}

    def test_dict_from_bad_string_raises(self):
        with pytest.raises(ValueError):
            self.v.coerce("not a dict", FieldType.DICT)

    def test_date_valid(self):
        assert self.v.coerce("2024-01-15", FieldType.DATE) == "2024-01-15"

    def test_date_invalid_format(self):
        with pytest.raises(ValueError):
            self.v.coerce("15/01/2024", FieldType.DATE)

    def test_date_invalid_month(self):
        with pytest.raises(ValueError):
            self.v.coerce("2024-13-01", FieldType.DATE)

    def test_date_invalid_day(self):
        with pytest.raises(ValueError):
            self.v.coerce("2024-01-32", FieldType.DATE)


# ===========================================================================
# OutputValidator — validate
# ===========================================================================

class TestOutputValidator:
    def setup_method(self):
        self.v = OutputValidator()

    def test_valid_data(self):
        schema = OutputSchema(
            name="s",
            fields=[
                FieldSchema("name", FieldType.STRING),
                FieldSchema("age", FieldType.INTEGER),
            ],
        )
        errors = self.v.validate({"name": "Alice", "age": 30}, schema)
        assert errors == []

    def test_missing_required_field(self):
        schema = OutputSchema(
            name="s",
            fields=[FieldSchema("name", FieldType.STRING)],
        )
        errors = self.v.validate({}, schema)
        assert len(errors) == 1
        assert errors[0].field == "name"

    def test_missing_optional_field_no_error(self):
        schema = OutputSchema(
            name="s",
            fields=[FieldSchema("x", FieldType.STRING, required=False)],
        )
        errors = self.v.validate({}, schema)
        assert errors == []

    def test_type_error_reported(self):
        schema = OutputSchema(
            name="s",
            fields=[FieldSchema("age", FieldType.INTEGER)],
        )
        errors = self.v.validate({"age": "not_a_number"}, schema)
        assert len(errors) == 1
        assert errors[0].field == "age"

    def test_coercible_string_to_int(self):
        schema = OutputSchema(
            name="s",
            fields=[FieldSchema("age", FieldType.INTEGER)],
        )
        errors = self.v.validate({"age": "42"}, schema)
        assert errors == []

    def test_unknown_fields_ignored(self):
        schema = OutputSchema(name="s", fields=[FieldSchema("x", FieldType.STRING)])
        errors = self.v.validate({"x": "hello", "unknown": "value"}, schema)
        assert errors == []

    def test_multiple_missing_fields(self):
        schema = OutputSchema(
            name="s",
            fields=[
                FieldSchema("a", FieldType.STRING),
                FieldSchema("b", FieldType.INTEGER),
                FieldSchema("c", FieldType.FLOAT),
            ],
        )
        errors = self.v.validate({}, schema)
        missing = {e.field for e in errors}
        assert missing == {"a", "b", "c"}

    def test_none_value_for_required_is_error(self):
        schema = OutputSchema(
            name="s",
            fields=[FieldSchema("x", FieldType.STRING)],
        )
        errors = self.v.validate({"x": None}, schema)
        assert len(errors) == 1

    def test_boolean_coercion_in_validate(self):
        schema = OutputSchema(
            name="s",
            fields=[FieldSchema("flag", FieldType.BOOLEAN)],
        )
        errors = self.v.validate({"flag": "yes"}, schema)
        assert errors == []


# ===========================================================================
# StructuredOutputParser
# ===========================================================================

class TestStructuredOutputParser:
    def _make_parser(self, **kwargs):
        schema = make_schema("test", **kwargs)
        return StructuredOutputParser(schema)

    def test_parse_json_success(self):
        parser = self._make_parser(name=FieldType.STRING, age=FieldType.INTEGER)
        result = parser.parse('{"name": "Alice", "age": 30}')
        assert result.is_success()
        assert result.extracted.data["name"] == "Alice"

    def test_parse_json_with_string_age(self):
        parser = self._make_parser(name=FieldType.STRING, age=FieldType.INTEGER)
        result = parser.parse('{"name": "Bob", "age": "25"}')
        assert result.is_success()

    def test_parse_falls_back_to_kv(self):
        parser = self._make_parser(name=FieldType.STRING, age=FieldType.STRING)
        result = parser.parse("name: Alice\nage: 30")
        assert result.is_success()
        assert result.extracted.data["name"] == "Alice"

    def test_parse_falls_back_to_table(self):
        parser = self._make_parser(name=FieldType.STRING, age=FieldType.STRING)
        text = "| name | age |\n|------|-----|\n| Carol | 28 |"
        result = parser.parse(text)
        assert result.is_success()
        assert result.extracted.data["name"] == "Carol"

    def test_missing_required_field(self):
        parser = self._make_parser(name=FieldType.STRING, age=FieldType.INTEGER)
        result = parser.parse('{"name": "Alice"}')
        assert not result.is_success()
        assert "age" in result.extracted.missing_fields

    def test_schema_name_in_result(self):
        schema = OutputSchema(name="my_schema", fields=[FieldSchema("x", FieldType.STRING)])
        parser = StructuredOutputParser(schema)
        result = parser.parse('{"x": "hello"}')
        assert result.schema_name == "my_schema"

    def test_no_extraction_possible(self):
        parser = self._make_parser(name=FieldType.STRING)
        result = parser.parse("nothing useful here...")
        assert not result.is_success()
        assert "name" in result.extracted.missing_fields

    def test_default_applied_for_optional(self):
        schema = OutputSchema(
            name="s",
            fields=[
                FieldSchema("name", FieldType.STRING),
                FieldSchema("score", FieldType.INTEGER, required=False, default=0),
            ],
        )
        parser = StructuredOutputParser(schema)
        result = parser.parse('{"name": "Alice"}')
        assert result.is_success()
        assert result.extracted.data["score"] == 0

    def test_config_disable_json(self):
        config = ParseConfig(try_json=False, try_markdown_table=False, try_key_value=True)
        schema = make_schema("s", name=FieldType.STRING)
        parser = StructuredOutputParser(schema, config=config)
        result = parser.parse('{"name": "Alice"}\nname: Bob')
        # JSON disabled, key-value used
        assert result.extracted.data["name"] == "Bob"

    def test_parse_result_is_success_false_on_validation_error(self):
        schema = OutputSchema(
            name="s",
            fields=[FieldSchema("count", FieldType.INTEGER)],
        )
        parser = StructuredOutputParser(schema)
        result = parser.parse('{"count": "not_a_number"}')
        assert not result.is_success()
        assert len(result.validated) > 0

    def test_default_config_applied(self):
        schema = make_schema("s", x=FieldType.STRING)
        parser = StructuredOutputParser(schema)
        assert parser.config is not None
        assert parser.config.try_json is True


# ===========================================================================
# Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_json_deeply_nested(self):
        ex = StructuredExtractor()
        text = '{"a": {"b": {"c": 42}}}'
        result = ex.extract_json(text)
        assert result == {"a": {"b": {"c": 42}}}

    def test_markdown_table_empty_cells(self):
        ex = StructuredExtractor()
        text = "| A | B |\n|---|---|\n| 1 |  |"
        rows = ex.extract_markdown_table(text)
        assert rows[0]["B"] == ""

    def test_key_value_multiline_value_first_sep_wins(self):
        ex = StructuredExtractor()
        text = "desc: hello: world"
        result = ex.extract_key_value(text)
        assert result["desc"] == "hello: world"

    def test_validation_error_has_value(self):
        v = OutputValidator()
        schema = OutputSchema(
            name="s",
            fields=[FieldSchema("n", FieldType.INTEGER)],
        )
        errors = v.validate({"n": "bad"}, schema)
        assert errors[0].value == "bad"

    def test_validation_error_dataclass_fields(self):
        err = ValidationError(field="x", message="bad", value=99)
        assert err.field == "x"
        assert err.message == "bad"
        assert err.value == 99

    def test_parse_config_defaults(self):
        c = ParseConfig()
        assert c.try_json is True
        assert c.try_markdown_table is True
        assert c.try_key_value is True
        assert c.strict is False

    def test_code_block_lang_case_sensitive(self):
        ex = StructuredExtractor()
        text = "```Python\ncode\n```"
        result = ex.extract_code_block(text, lang="python")
        assert result is None  # case-sensitive match

    def test_extraction_result_defaults(self):
        r = ExtractionResult(data={}, raw_text="x")
        assert r.missing_fields == []
        assert r.parse_errors == []

    def test_json_array_of_objects_not_matched(self):
        ex = StructuredExtractor()
        result = ex.extract_json('[{"a": 1}]')
        assert result is None

    def test_parser_json_in_prose(self):
        schema = make_schema("s", title=FieldType.STRING, year=FieldType.INTEGER)
        parser = StructuredOutputParser(schema)
        text = 'The result is: {"title": "Dune", "year": 1965} — end.'
        result = parser.parse(text)
        assert result.is_success()
        assert result.extracted.data["title"] == "Dune"
