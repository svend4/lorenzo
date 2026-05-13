"""E237 Document Field Validator.

Declarative field validation rules for arbitrary document data — types,
ranges, patterns, dependencies. Pure stdlib (uses only ``re``).

Different from ``config_validator`` (E101): this one is designed for free-form
document payloads where you build up the schema imperatively by adding fields
and rules.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class FieldType(Enum):
    """Supported logical field types."""

    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    LIST = "list"
    DICT = "dict"
    EMAIL = "email"
    URL = "url"
    DATE = "date"


class Severity(Enum):
    """Validation issue severity."""

    ERROR = "error"
    WARNING = "warning"


_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
_URL_RE = re.compile(r"https?://\S+")
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


@dataclass
class ValidationRule:
    """A single declarative validation rule."""

    rule_type: str
    value: Any = None
    message: Optional[str] = None
    severity: Severity = Severity.ERROR


@dataclass
class FieldSchema:
    """Schema describing one field of a document."""

    name: str
    field_type: Optional[FieldType] = None
    rules: list[ValidationRule] = field(default_factory=list)
    required: bool = False
    default: Any = None


@dataclass
class ValidationError:
    """Single validation issue (error or warning)."""

    field: str
    rule: str
    message: str
    severity: Severity = Severity.ERROR


@dataclass
class ValidationResult:
    """Outcome of validating a document."""

    valid: bool
    errors: list[ValidationError]
    warnings: list[ValidationError]

    @property
    def total_issues(self) -> int:
        return len(self.errors) + len(self.warnings)


def _matches_type(value: Any, field_type: FieldType) -> bool:
    if field_type is FieldType.STRING:
        return isinstance(value, str)
    if field_type is FieldType.INT:
        return isinstance(value, int) and not isinstance(value, bool)
    if field_type is FieldType.FLOAT:
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if field_type is FieldType.BOOL:
        return isinstance(value, bool)
    if field_type is FieldType.LIST:
        return isinstance(value, list)
    if field_type is FieldType.DICT:
        return isinstance(value, dict)
    if field_type is FieldType.EMAIL:
        return isinstance(value, str) and bool(_EMAIL_RE.search(value))
    if field_type is FieldType.URL:
        return isinstance(value, str) and bool(_URL_RE.search(value))
    if field_type is FieldType.DATE:
        return isinstance(value, str) and bool(_DATE_RE.search(value))
    return False


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str) and value == "":
        return True
    return False


class DocFieldValidator:
    """Declarative document field validator."""

    def __init__(self) -> None:
        self._schemas: dict[str, FieldSchema] = {}

    # ------------------------------------------------------------------
    # Schema management
    # ------------------------------------------------------------------
    def add_schema(self, schema: FieldSchema) -> bool:
        if not isinstance(schema, FieldSchema):
            return False
        if not schema.name:
            return False
        if schema.name in self._schemas:
            return False
        self._schemas[schema.name] = schema
        return True

    def add_field(
        self,
        name: str,
        field_type: Optional[FieldType] = None,
        required: bool = False,
        default: Any = None,
    ) -> FieldSchema:
        schema = FieldSchema(
            name=name,
            field_type=field_type,
            required=required,
            default=default,
        )
        self._schemas[name] = schema
        return schema

    def add_rule(
        self,
        field_name: str,
        rule_type: str,
        value: Any = None,
        message: Optional[str] = None,
        severity: Severity = Severity.ERROR,
    ) -> bool:
        schema = self._schemas.get(field_name)
        if schema is None:
            return False
        rule = ValidationRule(
            rule_type=rule_type,
            value=value,
            message=message,
            severity=severity,
        )
        schema.rules.append(rule)
        if rule_type == "required":
            schema.required = True
        return True

    def remove_field(self, name: str) -> bool:
        if name not in self._schemas:
            return False
        del self._schemas[name]
        return True

    def schemas(self) -> list[FieldSchema]:
        return list(self._schemas.values())

    def get_schema(self, name: str) -> Optional[FieldSchema]:
        return self._schemas.get(name)

    @property
    def field_count(self) -> int:
        return len(self._schemas)

    def clear(self) -> None:
        self._schemas.clear()

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate(self, data: dict, strict: bool = False) -> ValidationResult:
        errors: list[ValidationError] = []
        warnings: list[ValidationError] = []

        if not isinstance(data, dict):
            err = ValidationError(
                field="<root>",
                rule="type",
                message="data must be a dict",
                severity=Severity.ERROR,
            )
            return ValidationResult(valid=False, errors=[err], warnings=[])

        for name, schema in self._schemas.items():
            present = name in data
            value = data.get(name)

            # required check (either via .required flag or rule)
            if schema.required and (not present or _is_empty(value)):
                errors.append(
                    ValidationError(
                        field=name,
                        rule="required",
                        message=f"Field '{name}' is required",
                        severity=Severity.ERROR,
                    )
                )
                # If absent and required, skip remaining rules for this field
                if not present:
                    continue

            if not present:
                continue

            issues = self._run_field_rules(name, schema, value, data)
            for issue in issues:
                if issue.severity is Severity.ERROR:
                    errors.append(issue)
                else:
                    warnings.append(issue)

        # strict: report unknown fields
        if strict:
            for key in data:
                if key not in self._schemas:
                    errors.append(
                        ValidationError(
                            field=key,
                            rule="extra",
                            message=f"Unknown field '{key}'",
                            severity=Severity.ERROR,
                        )
                    )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

    def validate_field(self, field_name: str, value: Any) -> list[ValidationError]:
        schema = self._schemas.get(field_name)
        if schema is None:
            return []
        issues: list[ValidationError] = []
        if schema.required and _is_empty(value):
            issues.append(
                ValidationError(
                    field=field_name,
                    rule="required",
                    message=f"Field '{field_name}' is required",
                    severity=Severity.ERROR,
                )
            )
            if value is None:
                return issues
        issues.extend(self._run_field_rules(field_name, schema, value, {field_name: value}))
        return issues

    def _run_field_rules(
        self,
        name: str,
        schema: FieldSchema,
        value: Any,
        data: dict,
    ) -> list[ValidationError]:
        issues: list[ValidationError] = []

        # Implicit field_type check
        if schema.field_type is not None and not _matches_type(value, schema.field_type):
            issues.append(
                ValidationError(
                    field=name,
                    rule="type",
                    message=(
                        f"Field '{name}' must be of type "
                        f"{schema.field_type.value}"
                    ),
                    severity=Severity.ERROR,
                )
            )

        for rule in schema.rules:
            issue = self._check_rule(name, schema, rule, value, data)
            if issue is not None:
                issues.append(issue)
        return issues

    def _check_rule(
        self,
        name: str,
        schema: FieldSchema,
        rule: ValidationRule,
        value: Any,
        data: dict,
    ) -> Optional[ValidationError]:
        rt = rule.rule_type
        ok = True
        default_msg = ""

        if rt == "required":
            ok = not _is_empty(value)
            default_msg = f"Field '{name}' is required"
        elif rt == "type":
            target = rule.value
            if isinstance(target, FieldType):
                ok = _matches_type(value, target)
                default_msg = (
                    f"Field '{name}' must be of type {target.value}"
                )
            else:
                ok = isinstance(value, target) if isinstance(target, type) else False
                default_msg = f"Field '{name}' has wrong type"
        elif rt == "min_length":
            try:
                ok = len(value) >= rule.value
            except TypeError:
                ok = False
            default_msg = (
                f"Field '{name}' must have length >= {rule.value}"
            )
        elif rt == "max_length":
            try:
                ok = len(value) <= rule.value
            except TypeError:
                ok = False
            default_msg = (
                f"Field '{name}' must have length <= {rule.value}"
            )
        elif rt == "min":
            try:
                ok = value >= rule.value
            except TypeError:
                ok = False
            default_msg = f"Field '{name}' must be >= {rule.value}"
        elif rt == "max":
            try:
                ok = value <= rule.value
            except TypeError:
                ok = False
            default_msg = f"Field '{name}' must be <= {rule.value}"
        elif rt == "pattern":
            pattern = rule.value
            if isinstance(value, str) and isinstance(pattern, str):
                ok = re.search(pattern, value) is not None
            else:
                ok = False
            default_msg = (
                f"Field '{name}' must match pattern {rule.value!r}"
            )
        elif rt == "in":
            try:
                ok = value in rule.value
            except TypeError:
                ok = False
            default_msg = f"Field '{name}' must be one of {rule.value}"
        elif rt == "not_in":
            try:
                ok = value not in rule.value
            except TypeError:
                ok = True
            default_msg = (
                f"Field '{name}' must not be one of {rule.value}"
            )
        elif rt == "depends_on":
            # rule.value: {"field": <other_field>, "values": [...]}
            spec = rule.value or {}
            dep_field = spec.get("field") if isinstance(spec, dict) else None
            dep_values = spec.get("values") if isinstance(spec, dict) else None
            if dep_field is None or dep_values is None:
                ok = False
                default_msg = (
                    f"Field '{name}' has malformed depends_on rule"
                )
            else:
                dep_value = data.get(dep_field)
                ok = dep_value in dep_values
                default_msg = (
                    f"Field '{name}' requires '{dep_field}' to be one of "
                    f"{dep_values}"
                )
        else:
            # Unknown rule -> warning, not error
            return ValidationError(
                field=name,
                rule=rt,
                message=rule.message or f"Unknown rule type '{rt}'",
                severity=Severity.WARNING,
            )

        if ok:
            return None

        return ValidationError(
            field=name,
            rule=rt,
            message=rule.message or default_msg,
            severity=rule.severity,
        )

    # ------------------------------------------------------------------
    # Defaults & coercion
    # ------------------------------------------------------------------
    def apply_defaults(self, data: dict) -> dict:
        result = dict(data) if isinstance(data, dict) else {}
        for name, schema in self._schemas.items():
            if name not in result and schema.default is not None:
                result[name] = schema.default
        return result

    def coerce(self, data: dict) -> dict:
        result = dict(data) if isinstance(data, dict) else {}
        for name, schema in self._schemas.items():
            if name not in result:
                continue
            value = result[name]
            ft = schema.field_type
            if ft is None:
                continue
            if _matches_type(value, ft):
                continue
            coerced = self._coerce_value(value, ft)
            if coerced is not None:
                result[name] = coerced
        return result

    @staticmethod
    def _coerce_value(value: Any, field_type: FieldType) -> Any:
        try:
            if field_type is FieldType.STRING:
                if isinstance(value, bool):
                    return "true" if value else "false"
                return str(value)
            if field_type is FieldType.INT:
                if isinstance(value, bool):
                    return int(value)
                if isinstance(value, (int, float)):
                    return int(value)
                if isinstance(value, str):
                    return int(value.strip())
            if field_type is FieldType.FLOAT:
                if isinstance(value, bool):
                    return float(value)
                if isinstance(value, (int, float)):
                    return float(value)
                if isinstance(value, str):
                    return float(value.strip())
            if field_type is FieldType.BOOL:
                if isinstance(value, str):
                    v = value.strip().lower()
                    if v in ("true", "1", "yes", "y", "on"):
                        return True
                    if v in ("false", "0", "no", "n", "off"):
                        return False
                if isinstance(value, (int, float)):
                    return bool(value)
            if field_type is FieldType.LIST:
                if isinstance(value, tuple):
                    return list(value)
                if isinstance(value, set):
                    return list(value)
            if field_type is FieldType.DICT:
                # nothing reasonable to coerce
                return None
        except (ValueError, TypeError):
            return None
        return None
