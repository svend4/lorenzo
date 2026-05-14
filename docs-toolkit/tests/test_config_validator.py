"""Tests for E104 Config Validator (docstoolkit.config_validator).

Covers:
  - Valid data → no errors
  - Missing required field
  - Missing optional field → uses default
  - Wrong type
  - int/float min/max validation
  - str min/max length
  - list min/max length
  - regex pattern match/no match
  - allowed_values pass/fail
  - custom validator pass/fail
  - nested schema validation
  - allow_extra=False catches unknown keys
  - allow_extra=True ignores unknown keys
  - Multiple errors collected at once
  - ValidationResult.valid
  - ValidationResult.__str__
  - coerce() fills defaults
  - coerce() doesn't modify original
  - None as default for optional field
  - Type=None accepts any type
  - Tuple of types (int, float) accepts both
"""
import pytest

from docstoolkit.config_validator import (
    ConfigValidator,
    FieldSchema,
    SchemaDefinition,
    ValidationError,
    ValidationResult,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def make_validator() -> ConfigValidator:
    return ConfigValidator()


def simple_schema(**kwargs) -> SchemaDefinition:
    """Return a single-field schema for field 'x' with given FieldSchema kwargs."""
    return SchemaDefinition(fields=[FieldSchema("x", **kwargs)])


# ===========================================================================
# ValidationError dataclass
# ===========================================================================

class TestValidationError:
    def test_field_and_message_stored(self):
        e = ValidationError(field="name", message="missing")
        assert e.field == "name"
        assert e.message == "missing"

    def test_repr_contains_field(self):
        e = ValidationError(field="age", message="bad")
        assert "age" in repr(e)


# ===========================================================================
# ValidationResult
# ===========================================================================

class TestValidationResult:
    def test_empty_result_is_valid(self):
        r = ValidationResult()
        assert r.valid is True

    def test_result_with_error_is_invalid(self):
        r = ValidationResult(errors=[ValidationError("f", "bad")])
        assert r.valid is False

    def test_str_on_valid_result(self):
        r = ValidationResult()
        s = str(r)
        assert "passed" in s.lower()

    def test_str_on_invalid_result_lists_errors(self):
        r = ValidationResult(errors=[
            ValidationError("host", "missing"),
            ValidationError("port", "out of range"),
        ])
        s = str(r)
        assert "host" in s
        assert "port" in s
        assert "2" in s  # error count

    def test_str_shows_error_messages(self):
        r = ValidationResult(errors=[ValidationError("x", "custom message here")])
        assert "custom message here" in str(r)

    def test_valid_property_matches_empty_list(self):
        r = ValidationResult(errors=[])
        assert r.valid is True
        r.errors.append(ValidationError("f", "oops"))
        assert r.valid is False


# ===========================================================================
# Valid data — no errors
# ===========================================================================

class TestValidData:
    def test_all_required_fields_present_and_correct(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("name", type=str),
            FieldSchema("age", type=int),
        ])
        result = make_validator().validate({"name": "Alice", "age": 30}, schema)
        assert result.valid

    def test_optional_field_present_with_correct_value(self):
        schema = simple_schema(type=int, required=False, default=0)
        result = make_validator().validate({"x": 7}, schema)
        assert result.valid

    def test_empty_schema_empty_data(self):
        schema = SchemaDefinition(fields=[])
        result = make_validator().validate({}, schema)
        assert result.valid

    def test_type_none_accepts_any_value(self):
        schema = simple_schema(type=None)
        for val in [42, "hello", 3.14, [], {}, True, None]:
            result = make_validator().validate({"x": val}, schema)
            assert result.valid, f"expected valid for value {val!r}"

    def test_tuple_of_types_accepts_int(self):
        schema = simple_schema(type=(int, float))
        result = make_validator().validate({"x": 10}, schema)
        assert result.valid

    def test_tuple_of_types_accepts_float(self):
        schema = simple_schema(type=(int, float))
        result = make_validator().validate({"x": 3.14}, schema)
        assert result.valid


# ===========================================================================
# Required fields
# ===========================================================================

class TestRequiredField:
    def test_missing_required_field_is_error(self):
        schema = simple_schema(type=str, required=True)
        result = make_validator().validate({}, schema)
        assert not result.valid

    def test_error_field_name_matches(self):
        schema = simple_schema(type=str, required=True)
        result = make_validator().validate({}, schema)
        assert result.errors[0].field == "x"

    def test_error_message_mentions_field(self):
        schema = simple_schema(type=str, required=True)
        result = make_validator().validate({}, schema)
        assert "x" in result.errors[0].message

    def test_present_required_field_no_error(self):
        schema = simple_schema(type=str, required=True)
        result = make_validator().validate({"x": "hello"}, schema)
        assert result.valid


# ===========================================================================
# Optional fields and defaults
# ===========================================================================

class TestOptionalFields:
    def test_missing_optional_no_error(self):
        schema = simple_schema(required=False, default="fallback")
        result = make_validator().validate({}, schema)
        assert result.valid

    def test_missing_optional_with_none_default(self):
        schema = simple_schema(required=False, default=None)
        result = make_validator().validate({}, schema)
        assert result.valid

    def test_missing_optional_with_zero_default(self):
        schema = simple_schema(type=int, required=False, default=0)
        result = make_validator().validate({}, schema)
        assert result.valid

    def test_present_optional_field_validated_normally(self):
        schema = simple_schema(type=int, required=False, default=0)
        result = make_validator().validate({"x": "wrong"}, schema)
        assert not result.valid


# ===========================================================================
# Type checking
# ===========================================================================

class TestTypeCheck:
    def test_correct_str_type(self):
        schema = simple_schema(type=str)
        assert make_validator().validate({"x": "hello"}, schema).valid

    def test_wrong_type_int_given_str_expected(self):
        schema = simple_schema(type=str)
        result = make_validator().validate({"x": 42}, schema)
        assert not result.valid

    def test_wrong_type_error_message_mentions_expected(self):
        schema = simple_schema(type=str)
        result = make_validator().validate({"x": 42}, schema)
        assert "str" in result.errors[0].message

    def test_wrong_type_error_message_mentions_actual(self):
        schema = simple_schema(type=str)
        result = make_validator().validate({"x": 42}, schema)
        assert "int" in result.errors[0].message

    def test_bool_is_subclass_of_int_accepted(self):
        schema = simple_schema(type=int)
        result = make_validator().validate({"x": True}, schema)
        assert result.valid

    def test_tuple_type_rejects_wrong_type(self):
        schema = simple_schema(type=(int, float))
        result = make_validator().validate({"x": "string"}, schema)
        assert not result.valid

    def test_type_none_accepts_dict(self):
        schema = simple_schema(type=None)
        assert make_validator().validate({"x": {"a": 1}}, schema).valid


# ===========================================================================
# Numeric range — min_value / max_value
# ===========================================================================

class TestNumericRange:
    def test_value_within_range(self):
        schema = simple_schema(type=int, min_value=0, max_value=100)
        assert make_validator().validate({"x": 50}, schema).valid

    def test_value_at_min(self):
        schema = simple_schema(type=int, min_value=0, max_value=100)
        assert make_validator().validate({"x": 0}, schema).valid

    def test_value_at_max(self):
        schema = simple_schema(type=int, min_value=0, max_value=100)
        assert make_validator().validate({"x": 100}, schema).valid

    def test_value_below_min_is_error(self):
        schema = simple_schema(type=int, min_value=10)
        result = make_validator().validate({"x": 5}, schema)
        assert not result.valid

    def test_value_above_max_is_error(self):
        schema = simple_schema(type=int, max_value=10)
        result = make_validator().validate({"x": 11}, schema)
        assert not result.valid

    def test_min_error_message_contains_bound(self):
        schema = simple_schema(type=int, min_value=5)
        result = make_validator().validate({"x": 1}, schema)
        assert "5" in result.errors[0].message

    def test_max_error_message_contains_bound(self):
        schema = simple_schema(type=int, max_value=99)
        result = make_validator().validate({"x": 100}, schema)
        assert "99" in result.errors[0].message

    def test_float_value_within_range(self):
        schema = simple_schema(type=float, min_value=0.0, max_value=1.0)
        assert make_validator().validate({"x": 0.5}, schema).valid

    def test_float_value_out_of_range(self):
        schema = simple_schema(type=float, min_value=0.0, max_value=1.0)
        result = make_validator().validate({"x": 1.5}, schema)
        assert not result.valid

    def test_both_bounds_violated_produces_two_errors(self):
        # A single value can violate both min and max simultaneously only if
        # the schema is contradictory (min > max). Test that both checks fire.
        schema = simple_schema(type=int, min_value=20, max_value=10)
        result = make_validator().validate({"x": 15}, schema)
        # 15 < 20 (min violated) but 15 > 10 (max violated)
        assert len(result.errors) == 2


# ===========================================================================
# String / list length — min_length / max_length
# ===========================================================================

class TestLengthCheck:
    def test_string_within_length(self):
        schema = simple_schema(type=str, min_length=2, max_length=10)
        assert make_validator().validate({"x": "hello"}, schema).valid

    def test_string_too_short(self):
        schema = simple_schema(type=str, min_length=5)
        result = make_validator().validate({"x": "hi"}, schema)
        assert not result.valid

    def test_string_too_long(self):
        schema = simple_schema(type=str, max_length=3)
        result = make_validator().validate({"x": "toolong"}, schema)
        assert not result.valid

    def test_string_at_min_length(self):
        schema = simple_schema(type=str, min_length=3)
        assert make_validator().validate({"x": "abc"}, schema).valid

    def test_string_at_max_length(self):
        schema = simple_schema(type=str, max_length=3)
        assert make_validator().validate({"x": "abc"}, schema).valid

    def test_min_length_error_message_contains_bound(self):
        schema = simple_schema(type=str, min_length=10)
        result = make_validator().validate({"x": "short"}, schema)
        assert "10" in result.errors[0].message

    def test_max_length_error_message_contains_bound(self):
        schema = simple_schema(type=str, max_length=3)
        result = make_validator().validate({"x": "toolong"}, schema)
        assert "3" in result.errors[0].message

    def test_list_within_length(self):
        schema = simple_schema(type=list, min_length=1, max_length=5)
        assert make_validator().validate({"x": [1, 2, 3]}, schema).valid

    def test_list_too_short(self):
        schema = simple_schema(type=list, min_length=3)
        result = make_validator().validate({"x": [1]}, schema)
        assert not result.valid

    def test_list_too_long(self):
        schema = simple_schema(type=list, max_length=2)
        result = make_validator().validate({"x": [1, 2, 3]}, schema)
        assert not result.valid


# ===========================================================================
# Regex pattern
# ===========================================================================

class TestRegexPattern:
    def test_matching_string_passes(self):
        schema = simple_schema(type=str, pattern=r"\d{4}")
        assert make_validator().validate({"x": "1234"}, schema).valid

    def test_non_matching_string_fails(self):
        schema = simple_schema(type=str, pattern=r"\d{4}")
        result = make_validator().validate({"x": "abcd"}, schema)
        assert not result.valid

    def test_pattern_error_message_contains_pattern(self):
        schema = simple_schema(type=str, pattern=r"\d{4}")
        result = make_validator().validate({"x": "bad"}, schema)
        assert r"\d{4}" in result.errors[0].message

    def test_fullmatch_requires_entire_string(self):
        # re.fullmatch("\\d+", "123abc") should fail
        schema = simple_schema(type=str, pattern=r"\d+")
        result = make_validator().validate({"x": "123abc"}, schema)
        assert not result.valid

    def test_email_like_pattern(self):
        schema = simple_schema(type=str, pattern=r"[^@]+@[^@]+\.[^@]+")
        assert make_validator().validate({"x": "user@example.com"}, schema).valid
        result = make_validator().validate({"x": "notanemail"}, schema)
        assert not result.valid

    def test_pattern_ignored_for_non_string(self):
        # Pattern only applies to str values; int should not trigger pattern check
        schema = SchemaDefinition(fields=[
            FieldSchema("x", type=None, pattern=r"\d+")
        ])
        # An integer has no .fullmatch; the validator skips pattern for non-str
        result = make_validator().validate({"x": 123}, schema)
        assert result.valid


# ===========================================================================
# Allowed values
# ===========================================================================

class TestAllowedValues:
    def test_value_in_whitelist_passes(self):
        schema = simple_schema(type=str, allowed_values=["a", "b", "c"])
        assert make_validator().validate({"x": "a"}, schema).valid

    def test_value_not_in_whitelist_fails(self):
        schema = simple_schema(type=str, allowed_values=["a", "b"])
        result = make_validator().validate({"x": "z"}, schema)
        assert not result.valid

    def test_error_message_contains_value(self):
        schema = simple_schema(type=str, allowed_values=["yes", "no"])
        result = make_validator().validate({"x": "maybe"}, schema)
        assert "maybe" in result.errors[0].message

    def test_integer_whitelist_passes(self):
        schema = simple_schema(type=int, allowed_values=[1, 2, 3])
        assert make_validator().validate({"x": 2}, schema).valid

    def test_integer_whitelist_fails(self):
        schema = simple_schema(type=int, allowed_values=[1, 2, 3])
        result = make_validator().validate({"x": 99}, schema)
        assert not result.valid

    def test_empty_whitelist_always_fails(self):
        schema = simple_schema(type=str, allowed_values=[])
        result = make_validator().validate({"x": "anything"}, schema)
        assert not result.valid


# ===========================================================================
# Custom validator
# ===========================================================================

class TestCustomValidator:
    def test_custom_validator_returning_true_passes(self):
        schema = simple_schema(type=int, validator=lambda v: v % 2 == 0)
        assert make_validator().validate({"x": 4}, schema).valid

    def test_custom_validator_returning_false_fails(self):
        schema = simple_schema(type=int, validator=lambda v: v % 2 == 0)
        result = make_validator().validate({"x": 3}, schema)
        assert not result.valid

    def test_custom_validator_message_used(self):
        schema = simple_schema(
            type=int,
            validator=lambda v: v > 0,
            validator_msg="must be positive",
        )
        result = make_validator().validate({"x": -1}, schema)
        assert "must be positive" in result.errors[0].message

    def test_custom_validator_exception_becomes_error(self):
        def bad_validator(v):
            raise RuntimeError("exploded")

        schema = simple_schema(validator=bad_validator)
        result = make_validator().validate({"x": 1}, schema)
        assert not result.valid
        assert "exploded" in result.errors[0].message

    def test_custom_validator_receives_actual_value(self):
        seen = []
        def capture(v):
            seen.append(v)
            return True

        schema = simple_schema(validator=capture)
        make_validator().validate({"x": "hello"}, schema)
        assert seen == ["hello"]


# ===========================================================================
# Nested schema
# ===========================================================================

class TestNestedSchema:
    def _make_nested_schema(self) -> SchemaDefinition:
        address_schema = SchemaDefinition(fields=[
            FieldSchema("street", type=str),
            FieldSchema("city", type=str),
        ])
        return SchemaDefinition(fields=[
            FieldSchema("name", type=str),
            FieldSchema("address", type=dict, nested=address_schema),
        ])

    def test_valid_nested_data_passes(self):
        schema = self._make_nested_schema()
        data = {"name": "Alice", "address": {"street": "Main St", "city": "Oslo"}}
        result = make_validator().validate(data, schema)
        assert result.valid

    def test_missing_nested_required_field_is_error(self):
        schema = self._make_nested_schema()
        data = {"name": "Alice", "address": {"street": "Main St"}}  # city missing
        result = make_validator().validate(data, schema)
        assert not result.valid

    def test_nested_error_field_name_is_dotted(self):
        schema = self._make_nested_schema()
        data = {"name": "Alice", "address": {"street": "Main St"}}
        result = make_validator().validate(data, schema)
        field_names = {e.field for e in result.errors}
        assert any("address" in f and "city" in f for f in field_names)

    def test_nested_wrong_type_in_inner_field(self):
        schema = self._make_nested_schema()
        data = {"name": "Alice", "address": {"street": 123, "city": "Oslo"}}
        result = make_validator().validate(data, schema)
        assert not result.valid

    def test_nested_extra_key_rejected_when_not_allowed(self):
        schema = self._make_nested_schema()
        data = {
            "name": "Alice",
            "address": {"street": "Main St", "city": "Oslo", "country": "NO"},
        }
        result = make_validator().validate(data, schema)
        assert not result.valid

    def test_nested_extra_key_allowed_when_allow_extra_true(self):
        address_schema = SchemaDefinition(
            fields=[
                FieldSchema("street", type=str),
                FieldSchema("city", type=str),
            ],
            allow_extra=True,
        )
        schema = SchemaDefinition(fields=[
            FieldSchema("name", type=str),
            FieldSchema("address", type=dict, nested=address_schema),
        ])
        data = {
            "name": "Alice",
            "address": {"street": "Main St", "city": "Oslo", "country": "NO"},
        }
        result = make_validator().validate(data, schema)
        assert result.valid


# ===========================================================================
# allow_extra
# ===========================================================================

class TestAllowExtra:
    def test_extra_key_rejected_by_default(self):
        schema = SchemaDefinition(fields=[FieldSchema("x", type=int)])
        result = make_validator().validate({"x": 1, "y": 2}, schema)
        assert not result.valid

    def test_extra_key_error_mentions_key_name(self):
        schema = SchemaDefinition(fields=[FieldSchema("x", type=int)])
        result = make_validator().validate({"x": 1, "unknown_key": 99}, schema)
        field_names = {e.field for e in result.errors}
        assert "unknown_key" in field_names

    def test_extra_key_allowed_when_allow_extra_true(self):
        schema = SchemaDefinition(
            fields=[FieldSchema("x", type=int)],
            allow_extra=True,
        )
        result = make_validator().validate({"x": 1, "y": 2, "z": 3}, schema)
        assert result.valid

    def test_multiple_extra_keys_each_produce_error(self):
        schema = SchemaDefinition(fields=[FieldSchema("x", type=int)])
        result = make_validator().validate({"x": 1, "a": 1, "b": 2}, schema)
        extra_errors = [e for e in result.errors if e.field in ("a", "b")]
        assert len(extra_errors) == 2


# ===========================================================================
# Multiple errors collected at once
# ===========================================================================

class TestMultipleErrors:
    def test_all_errors_collected_no_short_circuit(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("a", type=str, required=True),
            FieldSchema("b", type=int, required=True),
            FieldSchema("c", type=float, required=True),
        ])
        result = make_validator().validate({}, schema)
        # All three required fields missing → 3 errors
        assert len(result.errors) == 3

    def test_type_and_range_errors_on_different_fields(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("name", type=str),
            FieldSchema("age", type=int, min_value=0, max_value=150),
        ])
        result = make_validator().validate({"name": 123, "age": 200}, schema)
        # name: wrong type; age: above max
        assert len(result.errors) == 2

    def test_allowed_values_and_pattern_both_fail(self):
        schema = SchemaDefinition(
            fields=[
                FieldSchema("code", type=str, pattern=r"\d{3}", allowed_values=["111", "222"]),
            ],
            allow_extra=False,
        )
        result = make_validator().validate({"code": "abc"}, schema)
        # pattern fails; allowed_values fails
        assert len(result.errors) == 2


# ===========================================================================
# coerce()
# ===========================================================================

class TestCoerce:
    def test_coerce_fills_missing_optional(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("host", type=str),
            FieldSchema("port", type=int, required=False, default=8080),
        ])
        out = make_validator().coerce({"host": "localhost"}, schema)
        assert out["port"] == 8080

    def test_coerce_does_not_override_present_value(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("port", type=int, required=False, default=8080),
        ])
        out = make_validator().coerce({"port": 9090}, schema)
        assert out["port"] == 9090

    def test_coerce_does_not_modify_original(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("debug", type=bool, required=False, default=False),
        ])
        original = {"host": "localhost"}
        _ = make_validator().coerce(original, schema)
        assert "debug" not in original

    def test_coerce_returns_new_dict(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("x", required=False, default=42),
        ])
        original = {}
        out = make_validator().coerce(original, schema)
        assert out is not original

    def test_coerce_none_as_default(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("tag", required=False, default=None),
        ])
        out = make_validator().coerce({}, schema)
        assert out["tag"] is None

    def test_coerce_multiple_defaults(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("a", required=False, default=1),
            FieldSchema("b", required=False, default=2),
            FieldSchema("c", required=False, default=3),
        ])
        out = make_validator().coerce({}, schema)
        assert out == {"a": 1, "b": 2, "c": 3}

    def test_coerce_does_not_add_required_fields(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("required_field", type=str, required=True),
        ])
        out = make_validator().coerce({}, schema)
        assert "required_field" not in out

    def test_coerce_preserves_extra_keys(self):
        schema = SchemaDefinition(fields=[
            FieldSchema("x", required=False, default=0),
        ], allow_extra=True)
        out = make_validator().coerce({"extra": "val"}, schema)
        assert out["extra"] == "val"
        assert out["x"] == 0
