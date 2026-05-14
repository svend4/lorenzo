"""E354 DocValidationEngine — pluggable validation rule engine for documents.

Pure stdlib, thread-safe via ``threading.Lock``, dataclasses throughout.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ValidationRule:
    """A single validation rule.

    ``check`` must be a callable ``check(content: str) -> Optional[str]``
    returning an error message string if the content violates the rule,
    or ``None`` if the content is valid for this rule.
    """

    rule_id: str
    name: str
    description: str = ""
    severity: str = "warning"  # "info", "warning", "error"
    enabled: bool = True
    check: object = field(default=None)


@dataclass
class ValidationIssue:
    """A single found issue."""

    rule_id: str
    severity: str
    message: str


@dataclass
class ValidationResult:
    """Result of validating a document."""

    doc_id: str
    valid: bool
    issues: list = field(default_factory=list)
    validated_at: float = 0.0


@dataclass
class ValidationStats:
    """Aggregate statistics for the engine."""

    total_rules: int
    enabled_rules: int
    total_validations: int
    total_issues_found: int


class DocValidationEngine:
    """Pluggable validation rule engine for documents."""

    def __init__(self) -> None:
        self._rules: dict = {}
        self._total_validations: int = 0
        self._total_issues: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Rule management
    # ------------------------------------------------------------------
    def register_rule(self, rule: ValidationRule) -> None:
        """Register or replace a rule."""
        with self._lock:
            self._rules[rule.rule_id] = rule

    def unregister_rule(self, rule_id: str) -> bool:
        """Remove a rule. Returns True if existed."""
        with self._lock:
            if rule_id in self._rules:
                del self._rules[rule_id]
                return True
            return False

    def enable_rule(self, rule_id: str) -> bool:
        """Enable a rule. Returns True if rule exists."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = True
            return True

    def disable_rule(self, rule_id: str) -> bool:
        """Disable a rule. Returns True if rule exists."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None:
                return False
            rule.enabled = False
            return True

    def get_rule(self, rule_id: str) -> Optional[ValidationRule]:
        """Return rule by id, or None."""
        with self._lock:
            return self._rules.get(rule_id)

    def list_rules(self) -> list:
        """Return all rules sorted by rule_id."""
        with self._lock:
            return sorted(self._rules.values(), key=lambda r: r.rule_id)

    def clear_rules(self) -> int:
        """Remove all rules. Returns the count removed."""
        with self._lock:
            count = len(self._rules)
            self._rules.clear()
            return count

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate(
        self,
        doc_id: str,
        content: str,
        rule_ids: Optional[list] = None,
        now: Optional[float] = None,
    ) -> ValidationResult:
        """Validate ``content`` against enabled rules.

        If ``rule_ids`` is provided, only those rules are considered (and only
        enabled ones among them). Otherwise every enabled rule runs.
        """
        if now is None:
            now = time.time()

        with self._lock:
            if rule_ids is None:
                candidates = list(self._rules.values())
            else:
                candidates = [self._rules[rid] for rid in rule_ids if rid in self._rules]

            issues: list = []
            has_error = False
            for rule in candidates:
                if not rule.enabled:
                    continue
                check_fn = rule.check
                if check_fn is None:
                    continue
                try:
                    msg = check_fn(content)
                except Exception as exc:  # noqa: BLE001
                    msg = f"rule error: {exc}"
                if msg is not None:
                    issues.append(
                        ValidationIssue(
                            rule_id=rule.rule_id,
                            severity=rule.severity,
                            message=msg,
                        )
                    )
                    if rule.severity == "error":
                        has_error = True

            self._total_validations += 1
            self._total_issues += len(issues)

            return ValidationResult(
                doc_id=doc_id,
                valid=not has_error,
                issues=issues,
                validated_at=now,
            )

    def validate_rule(self, rule_id: str, content: str) -> Optional[ValidationIssue]:
        """Apply a single rule. Returns None if rule unknown or no issue."""
        with self._lock:
            rule = self._rules.get(rule_id)
            if rule is None or rule.check is None:
                return None
            try:
                msg = rule.check(content)
            except Exception as exc:  # noqa: BLE001
                msg = f"rule error: {exc}"
            if msg is None:
                return None
            return ValidationIssue(
                rule_id=rule.rule_id,
                severity=rule.severity,
                message=msg,
            )

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------
    def stats(self) -> ValidationStats:
        """Return aggregate statistics."""
        with self._lock:
            enabled = sum(1 for r in self._rules.values() if r.enabled)
            return ValidationStats(
                total_rules=len(self._rules),
                enabled_rules=enabled,
                total_validations=self._total_validations,
                total_issues_found=self._total_issues,
            )
