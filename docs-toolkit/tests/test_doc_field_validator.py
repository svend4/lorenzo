"""Tests for E237 doc_field_validator."""
from __future__ import annotations

import pytest

from docstoolkit.doc_field_validator import (
    DocFieldValidator,
    FieldSchema,
    FieldType,
    Severity,
    ValidationError,
    ValidationResult,
    ValidationRule,
)


# ---------------------------------------------------------------------------
# Enum tests
# ---------------------------------------------------------------------------
class TestFieldType:
    def test_string_member(self):
        assert FieldType.STRING.value == "string"

    def test_int_member(self):
        assert FieldType.INT.value == "int"

    def test_float_member(self):
        assert FieldType.FLOAT.value == "float"

    def test_bool_member(self):
        assert FieldType.BOOL.value == "bool"

    def test_list_member(self):
        assert FieldType.LIST.value == "list"

    def test_dict_member(self):
        assert FieldType.DICT.value == "dict"

    def test_email_member(self):
        assert FieldType.EMAIL.value == "email"

    def test_url_member(self):
        assert FieldType.URL.value == "url"

    def test_date_member(self):
        assert FieldType.DATE.value == "date"


class TestSeverity:
    def test_error(self):
        assert Severity.ERROR.value == "error"

    def test_warning(self):
        assert Severity.WARNING.value == "warning"

    def test_distinct(self):
        assert Severity.ERROR is not Severity.WARNING


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------
class TestValidationRule:
    def test_minimal(self):
        rule = ValidationRule(rule_type="required")
        assert rule.rule_type == "required"
        assert rule.value is None
        assert rule.message is None
        assert rule.severity is Severity.ERROR

    def test_full(self):
        rule = ValidationRule(
            rule_type="min", value=10, message="too small", severity=Severity.WARNING
        )
        assert rule.rule_type == "min"
        assert rule.value == 10
        assert rule.message == "too small"
        assert rule.severity is Severity.WARNING


class TestFieldSchema:
    def test_defaults(self):
        schema = FieldSchema(name="title")
        assert schema.name == "title"
        assert schema.field_type is None
        assert schema.rules == []
        assert schema.required is False
        assert schema.default is None

    def test_with_rules(self):
        rule = ValidationRule(rule_type="required")
        schema = FieldSchema(name="title", field_type=FieldType.STRING, rules=[rule])
        assert len(schema.rules) == 1
        assert schema.field_type is FieldType.STRING

    def test_required_flag(self):
        schema = FieldSchema(name="x", required=True)
        assert schema.required is True

    def test_default_value(self):
        schema = FieldSchema(name="x", default=42)
        assert schema.default == 42


class TestValidationError:
    def test_default_severity(self):
        err = ValidationError(field="x", rule="required", message="missing")
        assert err.severity is Severity.ERROR

    def test_warning_severity(self):
        err = ValidationError(
            field="x", rule="min", message="small", severity=Severity.WARNING
        )
        assert err.severity is Severity.WARNING


class TestValidationResult:
    def test_empty_valid(self):
        result = ValidationResult(valid=True, errors=[], warnings=[])
        assert result.valid is True
        assert result.total_issues == 0

    def test_total_issues(self):
        err = ValidationError(field="a", rule="required", message="x")
        warn = ValidationError(
            field="b", rule="min", message="y", severity=Severity.WARNING
        )
        result = ValidationResult(valid=False, errors=[err], warnings=[warn])
        assert result.total_issues == 2


# ---------------------------------------------------------------------------
# Schema management
# ---------------------------------------------------------------------------
class TestAddSchema:
    def test_add_new(self):
        v = DocFieldValidator()
        assert v.add_schema(FieldSchema(name="a")) is True

    def test_add_duplicate(self):
        v = DocFieldValidator()
        v.add_schema(FieldSchema(name="a"))
        assert v.add_schema(FieldSchema(name="a")) is False

    def test_add_empty_name(self):
        v = DocFieldValidator()
        assert v.add_schema(FieldSchema(name="")) is False

    def test_add_non_schema(self):
        v = DocFieldValidator()
        assert v.add_schema("not a schema") is False  # type: ignore[arg-type]


class TestAddField:
    def test_basic(self):
        v = DocFieldValidator()
        schema = v.add_field("title", FieldType.STRING)
        assert schema.name == "title"
        assert schema.field_type is FieldType.STRING

    def test_required(self):
        v = DocFieldValidator()
        schema = v.add_field("x", required=True)
        assert schema.required is True

    def test_default(self):
        v = DocFieldValidator()
        schema = v.add_field("x", default=10)
        assert schema.default == 10

    def test_added_to_validator(self):
        v = DocFieldValidator()
        v.add_field("x")
        assert v.field_count == 1


class TestAddRule:
    def test_add_to_existing(self):
        v = DocFieldValidator()
        v.add_field("x")
        assert v.add_rule("x", "min", 5) is True
        assert len(v.get_schema("x").rules) == 1

    def test_add_to_missing(self):
        v = DocFieldValidator()
        assert v.add_rule("missing", "min", 5) is False

    def test_required_rule_sets_flag(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "required")
        assert v.get_schema("x").required is True

    def test_custom_message(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "min", 1, message="custom")
        assert v.get_schema("x").rules[0].message == "custom"


class TestRemoveField:
    def test_existing(self):
        v = DocFieldValidator()
        v.add_field("x")
        assert v.remove_field("x") is True
        assert v.field_count == 0

    def test_missing(self):
        v = DocFieldValidator()
        assert v.remove_field("missing") is False


# ---------------------------------------------------------------------------
# Validation rules
# ---------------------------------------------------------------------------
class TestValidateRequired:
    def test_missing_field(self):
        v = DocFieldValidator()
        v.add_field("title", required=True)
        result = v.validate({})
        assert result.valid is False
        assert any(e.rule == "required" for e in result.errors)

    def test_empty_string(self):
        v = DocFieldValidator()
        v.add_field("title", required=True)
        result = v.validate({"title": ""})
        assert result.valid is False

    def test_none_value(self):
        v = DocFieldValidator()
        v.add_field("title", required=True)
        result = v.validate({"title": None})
        assert result.valid is False

    def test_present_valid(self):
        v = DocFieldValidator()
        v.add_field("title", required=True)
        result = v.validate({"title": "hello"})
        assert result.valid is True


class TestValidateType:
    def test_string_ok(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.STRING)
        assert v.validate({"x": "hi"}).valid

    def test_string_fail(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.STRING)
        assert not v.validate({"x": 5}).valid

    def test_int_ok(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.INT)
        assert v.validate({"x": 5}).valid

    def test_int_not_bool(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.INT)
        assert not v.validate({"x": True}).valid

    def test_float_accepts_int(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.FLOAT)
        assert v.validate({"x": 5}).valid

    def test_float_not_bool(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.FLOAT)
        assert not v.validate({"x": False}).valid

    def test_bool_ok(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.BOOL)
        assert v.validate({"x": True}).valid

    def test_list_ok(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.LIST)
        assert v.validate({"x": [1, 2]}).valid

    def test_dict_ok(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.DICT)
        assert v.validate({"x": {"k": "v"}}).valid

    def test_dict_fail(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.DICT)
        assert not v.validate({"x": [1, 2]}).valid


class TestValidateMinMaxLength:
    def test_min_length_string_ok(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "min_length", 3)
        assert v.validate({"x": "abcd"}).valid

    def test_min_length_string_fail(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "min_length", 3)
        assert not v.validate({"x": "ab"}).valid

    def test_max_length_string_fail(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "max_length", 3)
        assert not v.validate({"x": "abcd"}).valid

    def test_min_length_list(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "min_length", 2)
        assert not v.validate({"x": [1]}).valid

    def test_max_length_list(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "max_length", 2)
        assert v.validate({"x": [1, 2]}).valid


class TestValidateMinMax:
    def test_min_ok(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "min", 0)
        assert v.validate({"x": 5}).valid

    def test_min_fail(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "min", 0)
        assert not v.validate({"x": -1}).valid

    def test_max_fail(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "max", 100)
        assert not v.validate({"x": 101}).valid

    def test_min_max_combined(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "min", 0)
        v.add_rule("x", "max", 100)
        assert v.validate({"x": 50}).valid


class TestValidatePattern:
    def test_match(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "pattern", r"^[a-z]+$")
        assert v.validate({"x": "abc"}).valid

    def test_no_match(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "pattern", r"^[a-z]+$")
        assert not v.validate({"x": "ABC"}).valid

    def test_non_string_fails(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "pattern", r"^\d+$")
        assert not v.validate({"x": 123}).valid


class TestValidateIn:
    def test_in_list(self):
        v = DocFieldValidator()
        v.add_field("status")
        v.add_rule("status", "in", ["draft", "published"])
        assert v.validate({"status": "draft"}).valid

    def test_not_in_list(self):
        v = DocFieldValidator()
        v.add_field("status")
        v.add_rule("status", "in", ["draft", "published"])
        assert not v.validate({"status": "unknown"}).valid


class TestValidateNotIn:
    def test_excluded(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "not_in", ["a", "b"])
        assert not v.validate({"x": "a"}).valid

    def test_allowed(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "not_in", ["a", "b"])
        assert v.validate({"x": "c"}).valid


class TestValidateDependsOn:
    def test_dependency_satisfied(self):
        v = DocFieldValidator()
        v.add_field("status")
        v.add_field("published_at")
        v.add_rule(
            "published_at",
            "depends_on",
            {"field": "status", "values": ["published"]},
        )
        assert v.validate({"status": "published", "published_at": "2025-01-01"}).valid

    def test_dependency_not_satisfied(self):
        v = DocFieldValidator()
        v.add_field("status")
        v.add_field("published_at")
        v.add_rule(
            "published_at",
            "depends_on",
            {"field": "status", "values": ["published"]},
        )
        result = v.validate({"status": "draft", "published_at": "2025-01-01"})
        assert not result.valid

    def test_malformed_rule(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "depends_on", "not a dict")
        assert not v.validate({"x": 1}).valid


# ---------------------------------------------------------------------------
# Field-level helpers
# ---------------------------------------------------------------------------
class TestValidateField:
    def test_known_field_ok(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.INT)
        assert v.validate_field("x", 5) == []

    def test_known_field_bad_type(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.INT)
        errors = v.validate_field("x", "hi")
        assert len(errors) == 1
        assert errors[0].rule == "type"

    def test_unknown_field(self):
        v = DocFieldValidator()
        assert v.validate_field("missing", 5) == []

    def test_required_empty(self):
        v = DocFieldValidator()
        v.add_field("x", required=True)
        errors = v.validate_field("x", None)
        assert any(e.rule == "required" for e in errors)


# ---------------------------------------------------------------------------
# Defaults & coercion
# ---------------------------------------------------------------------------
class TestApplyDefaults:
    def test_fills_missing(self):
        v = DocFieldValidator()
        v.add_field("x", default=10)
        out = v.apply_defaults({})
        assert out["x"] == 10

    def test_keeps_existing(self):
        v = DocFieldValidator()
        v.add_field("x", default=10)
        out = v.apply_defaults({"x": 5})
        assert out["x"] == 5

    def test_no_default(self):
        v = DocFieldValidator()
        v.add_field("x")
        out = v.apply_defaults({})
        assert "x" not in out

    def test_non_dict_input(self):
        v = DocFieldValidator()
        v.add_field("x", default=1)
        out = v.apply_defaults("not a dict")  # type: ignore[arg-type]
        assert out == {"x": 1}


class TestCoerce:
    def test_string_to_int(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.INT)
        out = v.coerce({"x": "42"})
        assert out["x"] == 42

    def test_string_to_float(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.FLOAT)
        out = v.coerce({"x": "3.14"})
        assert out["x"] == 3.14

    def test_string_to_bool_true(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.BOOL)
        out = v.coerce({"x": "true"})
        assert out["x"] is True

    def test_string_to_bool_false(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.BOOL)
        out = v.coerce({"x": "no"})
        assert out["x"] is False

    def test_int_to_string(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.STRING)
        out = v.coerce({"x": 5})
        assert out["x"] == "5"

    def test_already_correct(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.INT)
        out = v.coerce({"x": 5})
        assert out["x"] == 5

    def test_tuple_to_list(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.LIST)
        out = v.coerce({"x": (1, 2, 3)})
        assert out["x"] == [1, 2, 3]

    def test_uncoercible_kept(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.INT)
        out = v.coerce({"x": "not a number"})
        # Value left as-is when coercion fails
        assert out["x"] == "not a number"


# ---------------------------------------------------------------------------
# Strict mode
# ---------------------------------------------------------------------------
class TestStrict:
    def test_extra_field_errors_in_strict(self):
        v = DocFieldValidator()
        v.add_field("x")
        result = v.validate({"x": 1, "extra": 2}, strict=True)
        assert not result.valid
        assert any(e.rule == "extra" for e in result.errors)

    def test_extra_field_ok_in_lax(self):
        v = DocFieldValidator()
        v.add_field("x")
        result = v.validate({"x": 1, "extra": 2}, strict=False)
        assert result.valid

    def test_non_dict_input(self):
        v = DocFieldValidator()
        v.add_field("x")
        result = v.validate("nope")  # type: ignore[arg-type]
        assert not result.valid


# ---------------------------------------------------------------------------
# Format-type rules
# ---------------------------------------------------------------------------
class TestValidateEmail:
    def test_valid_email(self):
        v = DocFieldValidator()
        v.add_field("email", FieldType.EMAIL)
        assert v.validate({"email": "user@example.com"}).valid

    def test_invalid_email(self):
        v = DocFieldValidator()
        v.add_field("email", FieldType.EMAIL)
        assert not v.validate({"email": "not-an-email"}).valid

    def test_non_string(self):
        v = DocFieldValidator()
        v.add_field("email", FieldType.EMAIL)
        assert not v.validate({"email": 123}).valid


class TestValidateUrl:
    def test_valid_url(self):
        v = DocFieldValidator()
        v.add_field("url", FieldType.URL)
        assert v.validate({"url": "https://example.com"}).valid

    def test_invalid_url(self):
        v = DocFieldValidator()
        v.add_field("url", FieldType.URL)
        assert not v.validate({"url": "example.com"}).valid

    def test_http_url(self):
        v = DocFieldValidator()
        v.add_field("url", FieldType.URL)
        assert v.validate({"url": "http://example.com/path"}).valid


class TestValidateDate:
    def test_valid_date(self):
        v = DocFieldValidator()
        v.add_field("d", FieldType.DATE)
        assert v.validate({"d": "2025-01-15"}).valid

    def test_invalid_date(self):
        v = DocFieldValidator()
        v.add_field("d", FieldType.DATE)
        assert not v.validate({"d": "01/15/2025"}).valid


# ---------------------------------------------------------------------------
# Introspection
# ---------------------------------------------------------------------------
class TestSchemas:
    def test_empty(self):
        v = DocFieldValidator()
        assert v.schemas() == []

    def test_multiple(self):
        v = DocFieldValidator()
        v.add_field("a")
        v.add_field("b")
        assert len(v.schemas()) == 2

    def test_returns_list_copy(self):
        v = DocFieldValidator()
        v.add_field("a")
        lst = v.schemas()
        lst.append("foo")  # type: ignore[arg-type]
        assert v.field_count == 1


class TestGetSchema:
    def test_existing(self):
        v = DocFieldValidator()
        v.add_field("a")
        assert v.get_schema("a") is not None

    def test_missing(self):
        v = DocFieldValidator()
        assert v.get_schema("missing") is None


class TestFieldCount:
    def test_zero(self):
        v = DocFieldValidator()
        assert v.field_count == 0

    def test_after_adds(self):
        v = DocFieldValidator()
        v.add_field("a")
        v.add_field("b")
        v.add_field("c")
        assert v.field_count == 3

    def test_after_remove(self):
        v = DocFieldValidator()
        v.add_field("a")
        v.remove_field("a")
        assert v.field_count == 0


class TestClear:
    def test_clear_removes_all(self):
        v = DocFieldValidator()
        v.add_field("a")
        v.add_field("b")
        v.clear()
        assert v.field_count == 0

    def test_clear_empty(self):
        v = DocFieldValidator()
        v.clear()
        assert v.field_count == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_warning_does_not_invalidate(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "min", 10, severity=Severity.WARNING)
        result = v.validate({"x": 5})
        assert result.valid is True
        assert len(result.warnings) == 1

    def test_custom_message_used(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "min", 10, message="custom failure")
        result = v.validate({"x": 5})
        assert result.errors[0].message == "custom failure"

    def test_unknown_rule_is_warning(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "magic_rule", 5)
        result = v.validate({"x": 1})
        assert result.valid is True
        assert len(result.warnings) == 1

    def test_optional_missing_no_error(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.INT)
        assert v.validate({}).valid

    def test_required_missing_skips_other_rules(self):
        v = DocFieldValidator()
        v.add_field("x", required=True)
        v.add_rule("x", "min_length", 5)
        result = v.validate({})
        # Only one error for required, no min_length error from non-existent value
        required_errors = [e for e in result.errors if e.rule == "required"]
        assert len(required_errors) == 1

    def test_multiple_rules_multiple_errors(self):
        v = DocFieldValidator()
        v.add_field("x", FieldType.INT)
        v.add_rule("x", "min", 0)
        v.add_rule("x", "max", 100)
        result = v.validate({"x": "bad"})
        # type error + min and max may all fail (since comparisons fail on str)
        assert len(result.errors) >= 1
        assert not result.valid

    def test_pattern_rule_with_no_value(self):
        v = DocFieldValidator()
        v.add_field("x")
        v.add_rule("x", "pattern", None)
        result = v.validate({"x": "abc"})
        assert not result.valid

    def test_apply_defaults_then_validate(self):
        v = DocFieldValidator()
        v.add_field("status", FieldType.STRING, default="draft")
        filled = v.apply_defaults({})
        result = v.validate(filled)
        assert result.valid

    def test_coerce_then_validate(self):
        v = DocFieldValidator()
        v.add_field("count", FieldType.INT)
        v.add_rule("count", "min", 0)
        coerced = v.coerce({"count": "5"})
        assert v.validate(coerced).valid

    def test_full_workflow(self):
        v = DocFieldValidator()
        v.add_field("title", FieldType.STRING, required=True)
        v.add_rule("title", "min_length", 3)
        v.add_field("age", FieldType.INT)
        v.add_rule("age", "min", 0)
        v.add_rule("age", "max", 150)
        v.add_field("email", FieldType.EMAIL)

        good = {"title": "Hello", "age": 30, "email": "a@b.com"}
        assert v.validate(good).valid

        bad = {"title": "Hi", "age": 200, "email": "nope"}
        result = v.validate(bad)
        assert not result.valid
        assert len(result.errors) >= 3
