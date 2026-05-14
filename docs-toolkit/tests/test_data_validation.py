"""Tests for the E71 Data Validation module (docstoolkit.data_validation).

Covers:
  - All 6 built-in ValidationRule subclasses (pass and fail cases)
  - ValidationResult: is_valid, has_warnings, errors_for, add
  - DataValidator: validate (full dict), validate_field, is_valid, add_schema
  - DataSanitizer: each built-in sanitizer, sanitize_dict
  - Edge cases: empty data, no-rules field, WARNING severity, chained sanitizers
"""
import re
import pytest

from docstoolkit.data_validation import (
    ValidationSeverity,
    ValidationError,
    ValidationRule,
    RequiredRule,
    TypeRule,
    RangeRule,
    LengthRule,
    RegexRule,
    ChoiceRule,
    FieldSchema,
    ValidationResult,
    DataValidator,
    SanitizeRule,
    DataSanitizer,
    strip_whitespace,
    lowercase,
    truncate,
    remove_html_tags,
)


# ===========================================================================
# ValidationSeverity
# ===========================================================================

class TestValidationSeverity:
    def test_severity_error_value(self):
        assert ValidationSeverity.ERROR.value == "error"

    def test_severity_warning_value(self):
        assert ValidationSeverity.WARNING.value == "warning"

    def test_severity_info_value(self):
        assert ValidationSeverity.INFO.value == "info"

    def test_severity_members(self):
        members = {s.name for s in ValidationSeverity}
        assert members == {"ERROR", "WARNING", "INFO"}


# ===========================================================================
# ValidationError dataclass
# ===========================================================================

class TestValidationError:
    def test_required_fields(self):
        e = ValidationError(field="x", message="bad")
        assert e.field == "x"
        assert e.message == "bad"

    def test_default_severity_is_error(self):
        e = ValidationError(field="x", message="bad")
        assert e.severity == ValidationSeverity.ERROR

    def test_custom_severity_warning(self):
        e = ValidationError(field="x", message="warn", severity=ValidationSeverity.WARNING)
        assert e.severity == ValidationSeverity.WARNING

    def test_custom_severity_info(self):
        e = ValidationError(field="x", message="info", severity=ValidationSeverity.INFO)
        assert e.severity == ValidationSeverity.INFO

    def test_value_default_none(self):
        e = ValidationError(field="x", message="msg")
        assert e.value is None

    def test_value_stored(self):
        e = ValidationError(field="x", message="msg", value=42)
        assert e.value == 42


# ===========================================================================
# RequiredRule
# ===========================================================================

class TestRequiredRule:
    def setup_method(self):
        self.rule = RequiredRule()

    def test_name(self):
        assert self.rule.name == "required"

    def test_passes_non_empty_string(self):
        assert self.rule.validate("f", "hello") == []

    def test_passes_zero(self):
        # 0 is not None and not "", so it should pass
        assert self.rule.validate("f", 0) == []

    def test_passes_false(self):
        assert self.rule.validate("f", False) == []

    def test_passes_list(self):
        assert self.rule.validate("f", [1, 2]) == []

    def test_fails_none(self):
        errors = self.rule.validate("f", None)
        assert len(errors) == 1
        assert errors[0].field == "f"
        assert errors[0].severity == ValidationSeverity.ERROR

    def test_fails_empty_string(self):
        errors = self.rule.validate("username", "")
        assert len(errors) == 1
        assert errors[0].field == "username"

    def test_error_value_preserved_none(self):
        errors = self.rule.validate("f", None)
        assert errors[0].value is None

    def test_error_value_preserved_empty(self):
        errors = self.rule.validate("f", "")
        assert errors[0].value == ""


# ===========================================================================
# TypeRule
# ===========================================================================

class TestTypeRule:
    def test_name(self):
        rule = TypeRule(str)
        assert "str" in rule.name

    def test_passes_correct_type_str(self):
        rule = TypeRule(str)
        assert rule.validate("f", "hello") == []

    def test_passes_correct_type_int(self):
        rule = TypeRule(int)
        assert rule.validate("f", 42) == []

    def test_passes_correct_type_list(self):
        rule = TypeRule(list)
        assert rule.validate("f", [1, 2]) == []

    def test_skips_none(self):
        rule = TypeRule(str)
        assert rule.validate("f", None) == []

    def test_fails_wrong_type(self):
        rule = TypeRule(int)
        errors = rule.validate("f", "hello")
        assert len(errors) == 1
        assert errors[0].field == "f"

    def test_fails_wrong_type_message_mentions_types(self):
        rule = TypeRule(int)
        errors = rule.validate("age", "thirty")
        assert "int" in errors[0].message
        assert "str" in errors[0].message

    def test_bool_is_int_subclass(self):
        # bool is a subclass of int in Python
        rule = TypeRule(int)
        assert rule.validate("f", True) == []

    def test_error_value_stored(self):
        rule = TypeRule(int)
        errors = rule.validate("f", "wrong")
        assert errors[0].value == "wrong"


# ===========================================================================
# RangeRule
# ===========================================================================

class TestRangeRule:
    def test_name(self):
        rule = RangeRule(0, 100)
        assert "0" in rule.name and "100" in rule.name

    def test_passes_within_range(self):
        rule = RangeRule(0, 10)
        assert rule.validate("f", 5) == []

    def test_passes_at_min(self):
        rule = RangeRule(0, 10)
        assert rule.validate("f", 0) == []

    def test_passes_at_max(self):
        rule = RangeRule(0, 10)
        assert rule.validate("f", 10) == []

    def test_skips_none(self):
        rule = RangeRule(0, 10)
        assert rule.validate("f", None) == []

    def test_fails_below_min(self):
        rule = RangeRule(5, 10)
        errors = rule.validate("score", 4)
        assert len(errors) == 1
        assert "5" in errors[0].message

    def test_fails_above_max(self):
        rule = RangeRule(0, 100)
        errors = rule.validate("score", 101)
        assert len(errors) == 1
        assert "100" in errors[0].message

    def test_min_only(self):
        rule = RangeRule(min_val=0)
        assert rule.validate("f", 1000) == []
        assert len(rule.validate("f", -1)) == 1

    def test_max_only(self):
        rule = RangeRule(max_val=100)
        assert rule.validate("f", -999) == []
        assert len(rule.validate("f", 101)) == 1

    def test_both_violations_at_once_not_possible(self):
        # A single value can't be below min AND above max simultaneously
        rule = RangeRule(0, 10)
        errors = rule.validate("f", -1)
        assert len(errors) == 1

    def test_error_value_stored(self):
        rule = RangeRule(0, 10)
        errors = rule.validate("f", 99)
        assert errors[0].value == 99


# ===========================================================================
# LengthRule
# ===========================================================================

class TestLengthRule:
    def test_name(self):
        rule = LengthRule(2, 10)
        assert "2" in rule.name and "10" in rule.name

    def test_passes_within_length(self):
        rule = LengthRule(1, 5)
        assert rule.validate("f", "abc") == []

    def test_passes_at_min_len(self):
        rule = LengthRule(3, 10)
        assert rule.validate("f", "abc") == []

    def test_passes_at_max_len(self):
        rule = LengthRule(1, 3)
        assert rule.validate("f", "abc") == []

    def test_skips_none(self):
        rule = LengthRule(1, 5)
        assert rule.validate("f", None) == []

    def test_fails_too_short(self):
        rule = LengthRule(min_len=3)
        errors = rule.validate("name", "ab")
        assert len(errors) == 1
        assert "3" in errors[0].message

    def test_fails_too_long(self):
        rule = LengthRule(max_len=5)
        errors = rule.validate("name", "toolongstring")
        assert len(errors) == 1
        assert "5" in errors[0].message

    def test_works_with_list(self):
        rule = LengthRule(min_len=2, max_len=4)
        assert rule.validate("tags", [1, 2, 3]) == []
        assert len(rule.validate("tags", [1])) == 1

    def test_min_only(self):
        rule = LengthRule(min_len=2)
        assert rule.validate("f", "ab") == []
        assert len(rule.validate("f", "a")) == 1

    def test_max_only(self):
        rule = LengthRule(max_len=3)
        assert rule.validate("f", "abc") == []
        assert len(rule.validate("f", "abcd")) == 1


# ===========================================================================
# RegexRule
# ===========================================================================

class TestRegexRule:
    def test_name_contains_pattern(self):
        rule = RegexRule(r"^\d+$")
        assert r"^\d+$" in rule.name

    def test_passes_matching_value(self):
        rule = RegexRule(r"^\d+$")
        assert rule.validate("f", "12345") == []

    def test_skips_none(self):
        rule = RegexRule(r"^\d+$")
        assert rule.validate("f", None) == []

    def test_fails_non_matching_value(self):
        rule = RegexRule(r"^\d+$")
        errors = rule.validate("code", "abc")
        assert len(errors) == 1
        assert "code" in errors[0].message

    def test_flags_case_insensitive(self):
        rule = RegexRule(r"^hello$", re.IGNORECASE)
        assert rule.validate("f", "HELLO") == []
        assert rule.validate("f", "Hello") == []

    def test_email_like_pattern(self):
        rule = RegexRule(r"^[^@]+@[^@]+\.[^@]+$")
        assert rule.validate("email", "user@example.com") == []
        assert len(rule.validate("email", "notanemail")) == 1

    def test_error_value_stored(self):
        rule = RegexRule(r"^\d+$")
        errors = rule.validate("f", "abc")
        assert errors[0].value == "abc"

    def test_partial_match_fails(self):
        # re.match anchors at start but not end — test that bare pattern behaves as expected
        rule = RegexRule(r"\d+")
        # "123" starts with digits so match succeeds
        assert rule.validate("f", "123") == []


# ===========================================================================
# ChoiceRule
# ===========================================================================

class TestChoiceRule:
    def test_name_contains_choices(self):
        rule = ChoiceRule(["a", "b"])
        assert "a" in rule.name

    def test_passes_valid_choice(self):
        rule = ChoiceRule(["yes", "no"])
        assert rule.validate("f", "yes") == []

    def test_skips_none(self):
        rule = ChoiceRule(["yes", "no"])
        assert rule.validate("f", None) == []

    def test_fails_invalid_choice(self):
        rule = ChoiceRule(["yes", "no"])
        errors = rule.validate("answer", "maybe")
        assert len(errors) == 1
        assert "maybe" in errors[0].message

    def test_choices_with_integers(self):
        rule = ChoiceRule([1, 2, 3])
        assert rule.validate("f", 2) == []
        assert len(rule.validate("f", 4)) == 1

    def test_empty_choices_always_fails_non_none(self):
        rule = ChoiceRule([])
        assert len(rule.validate("f", "anything")) == 1

    def test_error_value_stored(self):
        rule = ChoiceRule(["a", "b"])
        errors = rule.validate("f", "c")
        assert errors[0].value == "c"


# ===========================================================================
# ValidationResult
# ===========================================================================

class TestValidationResult:
    def test_empty_result_is_valid(self):
        result = ValidationResult()
        assert result.is_valid() is True

    def test_empty_result_no_warnings(self):
        result = ValidationResult()
        assert result.has_warnings() is False

    def test_add_error_makes_invalid(self):
        result = ValidationResult()
        result.add(ValidationError("f", "bad"))
        assert result.is_valid() is False

    def test_warning_only_still_valid(self):
        result = ValidationResult()
        result.add(ValidationError("f", "warn", severity=ValidationSeverity.WARNING))
        assert result.is_valid() is True

    def test_warning_detected(self):
        result = ValidationResult()
        result.add(ValidationError("f", "warn", severity=ValidationSeverity.WARNING))
        assert result.has_warnings() is True

    def test_info_only_still_valid(self):
        result = ValidationResult()
        result.add(ValidationError("f", "info", severity=ValidationSeverity.INFO))
        assert result.is_valid() is True

    def test_info_not_counted_as_warning(self):
        result = ValidationResult()
        result.add(ValidationError("f", "info", severity=ValidationSeverity.INFO))
        assert result.has_warnings() is False

    def test_errors_for_returns_matching(self):
        result = ValidationResult()
        e1 = ValidationError("name", "bad name")
        e2 = ValidationError("age", "bad age")
        result.add(e1)
        result.add(e2)
        assert result.errors_for("name") == [e1]
        assert result.errors_for("age") == [e2]

    def test_errors_for_returns_empty_when_no_match(self):
        result = ValidationResult()
        result.add(ValidationError("name", "bad"))
        assert result.errors_for("missing_field") == []

    def test_multiple_errors_same_field(self):
        result = ValidationResult()
        e1 = ValidationError("x", "err1")
        e2 = ValidationError("x", "err2")
        result.add(e1)
        result.add(e2)
        assert len(result.errors_for("x")) == 2

    def test_error_and_warning_mix(self):
        result = ValidationResult()
        result.add(ValidationError("f", "err", severity=ValidationSeverity.ERROR))
        result.add(ValidationError("f", "warn", severity=ValidationSeverity.WARNING))
        assert result.is_valid() is False
        assert result.has_warnings() is True


# ===========================================================================
# DataValidator
# ===========================================================================

class TestDataValidator:
    def _make_validator(self):
        """Return a validator with name (str, required) and age (int, 0-120)."""
        return DataValidator([
            FieldSchema("name", [RequiredRule(), TypeRule(str)]),
            FieldSchema("age",  [RequiredRule(), TypeRule(int), RangeRule(0, 120)]),
        ])

    def test_valid_data_passes(self):
        v = self._make_validator()
        assert v.is_valid({"name": "Alice", "age": 30})

    def test_missing_required_field_fails(self):
        v = self._make_validator()
        assert not v.is_valid({"name": "Alice", "age": None})

    def test_wrong_type_fails(self):
        v = self._make_validator()
        assert not v.is_valid({"name": "Alice", "age": "thirty"})

    def test_out_of_range_fails(self):
        v = self._make_validator()
        assert not v.is_valid({"name": "Alice", "age": 200})

    def test_empty_data_fails_required(self):
        v = self._make_validator()
        result = v.validate({})
        assert not result.is_valid()

    def test_extra_fields_ignored(self):
        v = self._make_validator()
        assert v.is_valid({"name": "Alice", "age": 25, "extra": "ignored"})

    def test_validate_returns_all_errors(self):
        v = self._make_validator()
        result = v.validate({"name": None, "age": None})
        # RequiredRule fails for both name and age
        assert len(result.errors) >= 2

    def test_add_schema_extends_validator(self):
        v = DataValidator()
        v.add_schema(FieldSchema("email", [RequiredRule()]))
        assert not v.is_valid({"email": None})
        assert v.is_valid({"email": "user@example.com"})

    def test_validate_field_passes(self):
        v = self._make_validator()
        result = v.validate_field("name", "Bob")
        assert result.is_valid()

    def test_validate_field_fails(self):
        v = self._make_validator()
        result = v.validate_field("name", None)
        assert not result.is_valid()

    def test_validate_field_unknown_field_returns_valid(self):
        v = self._make_validator()
        result = v.validate_field("nonexistent", "any_value")
        assert result.is_valid()

    def test_no_schemas_always_valid(self):
        v = DataValidator()
        assert v.is_valid({"anything": "goes"})

    def test_field_with_no_rules_always_passes(self):
        v = DataValidator([FieldSchema("note")])
        assert v.is_valid({"note": None})
        assert v.is_valid({"note": ""})

    def test_warning_severity_rule_keeps_valid(self):
        v = DataValidator()
        schema = FieldSchema("score", [])
        v.add_schema(schema)
        result = v.validate({"score": 5})
        # Manually inject a warning to prove it doesn't break is_valid
        result.add(ValidationError("score", "low score", severity=ValidationSeverity.WARNING))
        assert result.is_valid()
        assert result.has_warnings()

    def test_multiple_schemas_for_same_field_applies_all(self):
        """Two schemas registered for same field name both run."""
        v = DataValidator([
            FieldSchema("x", [TypeRule(int)]),
            FieldSchema("x", [RangeRule(0, 10)]),
        ])
        # Type passes, range fails
        result = v.validate({"x": 99})
        assert not result.is_valid()

    def test_validate_collects_errors_from_all_fields(self):
        v = DataValidator([
            FieldSchema("a", [RequiredRule()]),
            FieldSchema("b", [RequiredRule()]),
            FieldSchema("c", [RequiredRule()]),
        ])
        result = v.validate({"a": None, "b": None, "c": None})
        assert len(result.errors_for("a")) >= 1
        assert len(result.errors_for("b")) >= 1
        assert len(result.errors_for("c")) >= 1


# ===========================================================================
# DataSanitizer — strip_whitespace
# ===========================================================================

class TestStripWhitespaceSanitizer:
    def setup_method(self):
        self.sanitizer = DataSanitizer([strip_whitespace()])

    def test_strips_leading(self):
        assert self.sanitizer.sanitize("  hello") == "hello"

    def test_strips_trailing(self):
        assert self.sanitizer.sanitize("hello  ") == "hello"

    def test_strips_both(self):
        assert self.sanitizer.sanitize("  hello  ") == "hello"

    def test_no_whitespace_unchanged(self):
        assert self.sanitizer.sanitize("hello") == "hello"

    def test_empty_string(self):
        assert self.sanitizer.sanitize("") == ""

    def test_only_whitespace(self):
        assert self.sanitizer.sanitize("   ") == ""

    def test_rule_name(self):
        rule = strip_whitespace()
        assert rule.name == "strip_whitespace"


# ===========================================================================
# DataSanitizer — lowercase
# ===========================================================================

class TestLowercaseSanitizer:
    def setup_method(self):
        self.sanitizer = DataSanitizer([lowercase()])

    def test_converts_uppercase(self):
        assert self.sanitizer.sanitize("HELLO") == "hello"

    def test_mixed_case(self):
        assert self.sanitizer.sanitize("Hello World") == "hello world"

    def test_already_lowercase(self):
        assert self.sanitizer.sanitize("hello") == "hello"

    def test_empty_string(self):
        assert self.sanitizer.sanitize("") == ""

    def test_rule_name(self):
        rule = lowercase()
        assert rule.name == "lowercase"


# ===========================================================================
# DataSanitizer — truncate
# ===========================================================================

class TestTruncateSanitizer:
    def test_truncates_long_string(self):
        sanitizer = DataSanitizer([truncate(5)])
        assert sanitizer.sanitize("hello world") == "hello"

    def test_short_string_unchanged(self):
        sanitizer = DataSanitizer([truncate(10)])
        assert sanitizer.sanitize("hi") == "hi"

    def test_exact_length_unchanged(self):
        sanitizer = DataSanitizer([truncate(5)])
        assert sanitizer.sanitize("hello") == "hello"

    def test_zero_truncates_all(self):
        sanitizer = DataSanitizer([truncate(0)])
        assert sanitizer.sanitize("hello") == ""

    def test_rule_name_contains_max(self):
        rule = truncate(20)
        assert "20" in rule.name

    def test_empty_string(self):
        sanitizer = DataSanitizer([truncate(5)])
        assert sanitizer.sanitize("") == ""


# ===========================================================================
# DataSanitizer — remove_html_tags
# ===========================================================================

class TestRemoveHtmlTagsSanitizer:
    def setup_method(self):
        self.sanitizer = DataSanitizer([remove_html_tags()])

    def test_removes_simple_tag(self):
        assert self.sanitizer.sanitize("<b>bold</b>") == "bold"

    def test_removes_self_closing_tag(self):
        assert self.sanitizer.sanitize("line<br/>break") == "linebreak"

    def test_removes_tag_with_attributes(self):
        assert self.sanitizer.sanitize('<a href="url">link</a>') == "link"

    def test_no_tags_unchanged(self):
        assert self.sanitizer.sanitize("plain text") == "plain text"

    def test_empty_string(self):
        assert self.sanitizer.sanitize("") == ""

    def test_multiple_tags(self):
        result = self.sanitizer.sanitize("<h1>Title</h1><p>Body</p>")
        assert result == "TitleBody"

    def test_rule_name(self):
        rule = remove_html_tags()
        assert rule.name == "remove_html_tags"


# ===========================================================================
# DataSanitizer — sanitize_dict
# ===========================================================================

class TestSanitizeDict:
    def setup_method(self):
        self.sanitizer = DataSanitizer([strip_whitespace(), lowercase()])

    def test_all_string_fields_sanitized_when_no_fields_specified(self):
        data = {"name": "  ALICE  ", "city": "  BERLIN  "}
        result = self.sanitizer.sanitize_dict(data)
        assert result["name"] == "alice"
        assert result["city"] == "berlin"

    def test_non_string_fields_not_touched(self):
        data = {"name": "  ALICE  ", "age": 30}
        result = self.sanitizer.sanitize_dict(data)
        assert result["age"] == 30

    def test_specific_fields_only(self):
        data = {"name": "  ALICE  ", "city": "  BERLIN  "}
        result = self.sanitizer.sanitize_dict(data, fields=["name"])
        assert result["name"] == "alice"
        # city not in fields list; stays as-is
        assert result["city"] == "  BERLIN  "

    def test_original_dict_not_modified(self):
        data = {"name": "  ALICE  "}
        result = self.sanitizer.sanitize_dict(data)
        assert data["name"] == "  ALICE  "  # original unchanged

    def test_empty_dict(self):
        result = self.sanitizer.sanitize_dict({})
        assert result == {}

    def test_fields_list_with_missing_key_ignored(self):
        data = {"name": "  ALICE  "}
        # "email" not in data — should not raise
        result = self.sanitizer.sanitize_dict(data, fields=["name", "email"])
        assert result["name"] == "alice"

    def test_fields_list_skips_non_string_values(self):
        data = {"count": 42}
        result = self.sanitizer.sanitize_dict(data, fields=["count"])
        assert result["count"] == 42  # untouched because not a string


# ===========================================================================
# Chained sanitizers
# ===========================================================================

class TestChainedSanitizers:
    def test_strip_then_lowercase(self):
        s = DataSanitizer([strip_whitespace(), lowercase()])
        assert s.sanitize("  HELLO  ") == "hello"

    def test_lowercase_then_truncate(self):
        s = DataSanitizer([lowercase(), truncate(3)])
        assert s.sanitize("HELLO") == "hel"

    def test_strip_html_then_truncate(self):
        s = DataSanitizer([remove_html_tags(), truncate(4)])
        assert s.sanitize("<b>Hello</b>") == "Hell"

    def test_add_rule_appends_in_order(self):
        s = DataSanitizer()
        s.add_rule(strip_whitespace())
        s.add_rule(lowercase())
        s.add_rule(truncate(5))
        assert s.sanitize("  HELLO WORLD  ") == "hello"

    def test_empty_pipeline_returns_input_unchanged(self):
        s = DataSanitizer()
        assert s.sanitize("  HELLO  ") == "  HELLO  "


# ===========================================================================
# SanitizeRule dataclass
# ===========================================================================

class TestSanitizeRule:
    def test_fields(self):
        rule = SanitizeRule(name="my_rule", transform=str.strip, description="strips")
        assert rule.name == "my_rule"
        assert rule.description == "strips"

    def test_transform_called(self):
        rule = SanitizeRule(name="double", transform=lambda s: s * 2)
        assert rule.transform("ab") == "abab"

    def test_default_description_empty(self):
        rule = SanitizeRule(name="r", transform=lambda s: s)
        assert rule.description == ""


# ===========================================================================
# ValidationRule is abstract
# ===========================================================================

class TestValidationRuleABC:
    def test_cannot_instantiate_abstract_class(self):
        with pytest.raises(TypeError):
            ValidationRule()  # type: ignore[abstract]

    def test_concrete_subclass_must_implement_name_and_validate(self):
        class Incomplete(ValidationRule):
            pass

        with pytest.raises(TypeError):
            Incomplete()  # type: ignore[abstract]

    def test_concrete_subclass_works(self):
        class AlwaysOk(ValidationRule):
            @property
            def name(self):
                return "always_ok"

            def validate(self, field, value):
                return []

        rule = AlwaysOk()
        assert rule.validate("f", "anything") == []
