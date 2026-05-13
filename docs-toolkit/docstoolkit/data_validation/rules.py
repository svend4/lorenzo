"""Validation rules for the E71 Data Validation module."""
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class ValidationSeverity(Enum):
    """Severity level for a validation error."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationError:
    """A single validation failure or notice."""
    field: str
    message: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    value: Any = None


class ValidationRule(ABC):
    """Abstract base class for all validation rules."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the rule name."""

    @abstractmethod
    def validate(self, field: str, value: Any) -> list[ValidationError]:
        """Validate *value* for *field*; return a (possibly empty) list of errors."""


# ---------------------------------------------------------------------------
# Built-in rules
# ---------------------------------------------------------------------------

class RequiredRule(ValidationRule):
    """Fail if value is None or an empty string."""

    @property
    def name(self) -> str:
        return "required"

    def validate(self, field: str, value: Any) -> list[ValidationError]:
        if value is None or value == "":
            return [ValidationError(
                field=field,
                message=f"'{field}' is required",
                value=value,
            )]
        return []


class TypeRule(ValidationRule):
    """Fail if value is not an instance of *expected_type*; skip if None."""

    def __init__(self, expected_type: type) -> None:
        self._expected_type = expected_type

    @property
    def name(self) -> str:
        return f"type:{self._expected_type.__name__}"

    def validate(self, field: str, value: Any) -> list[ValidationError]:
        if value is None:
            return []
        if not isinstance(value, self._expected_type):
            return [ValidationError(
                field=field,
                message=(
                    f"'{field}' must be of type {self._expected_type.__name__}, "
                    f"got {type(value).__name__}"
                ),
                value=value,
            )]
        return []


class RangeRule(ValidationRule):
    """Numeric range check; skip if value is None."""

    def __init__(self, min_val=None, max_val=None) -> None:
        self._min = min_val
        self._max = max_val

    @property
    def name(self) -> str:
        return f"range:[{self._min},{self._max}]"

    def validate(self, field: str, value: Any) -> list[ValidationError]:
        if value is None:
            return []
        if not isinstance(value, (int, float)):
            return []
        errors: list[ValidationError] = []
        try:
            if self._min is not None and value < self._min:
                errors.append(ValidationError(
                    field=field,
                    message=f"'{field}' must be >= {self._min}, got {value}",
                    value=value,
                ))
            if self._max is not None and value > self._max:
                errors.append(ValidationError(
                    field=field,
                    message=f"'{field}' must be <= {self._max}, got {value}",
                    value=value,
                ))
        except TypeError:
            errors.append(ValidationError(
                field=field,
                message=(
                    f"'{field}' cannot be compared with range "
                    f"[{self._min}, {self._max}]: incompatible type {type(value).__name__}"
                ),
                value=value,
            ))
        return errors


class LengthRule(ValidationRule):
    """Length check via len(); skip if value is None."""

    def __init__(self, min_len=None, max_len=None) -> None:
        self._min = min_len
        self._max = max_len

    @property
    def name(self) -> str:
        return f"length:[{self._min},{self._max}]"

    def validate(self, field: str, value: Any) -> list[ValidationError]:
        if value is None:
            return []
        length = len(value)
        errors: list[ValidationError] = []
        if self._min is not None and length < self._min:
            errors.append(ValidationError(
                field=field,
                message=f"'{field}' length must be >= {self._min}, got {length}",
                value=value,
            ))
        if self._max is not None and length > self._max:
            errors.append(ValidationError(
                field=field,
                message=f"'{field}' length must be <= {self._max}, got {length}",
                value=value,
            ))
        return errors


class RegexRule(ValidationRule):
    """re.match check against *pattern*; skip if value is None."""

    def __init__(self, pattern: str, flags: int = 0) -> None:
        self._pattern = pattern
        self._flags = flags
        self._compiled = re.compile(pattern, flags)

    @property
    def name(self) -> str:
        return f"regex:{self._pattern}"

    def validate(self, field: str, value: Any) -> list[ValidationError]:
        if value is None:
            return []
        if not self._compiled.match(str(value)):
            return [ValidationError(
                field=field,
                message=f"'{field}' does not match pattern '{self._pattern}'",
                value=value,
            )]
        return []


class ChoiceRule(ValidationRule):
    """Value must be in *choices*; skip if value is None."""

    def __init__(self, choices: list) -> None:
        self._choices = list(choices)

    @property
    def name(self) -> str:
        return f"choice:{self._choices}"

    def validate(self, field: str, value: Any) -> list[ValidationError]:
        if value is None:
            return []
        if value not in self._choices:
            return [ValidationError(
                field=field,
                message=f"'{field}' must be one of {self._choices}, got {value!r}",
                value=value,
            )]
        return []
