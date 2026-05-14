"""Retention policies and enforcement."""
from dataclasses import dataclass, field
from datetime import datetime, timezone

from docstoolkit.governance.classifier import DataClass


@dataclass
class RetentionRule:
    """Retention rule for a data class."""
    data_class: DataClass
    max_age_days: int        # documents older than this should be reviewed
    auto_archive: bool = False   # if True, mark as archived when expired
    auto_delete: bool = False    # if True, mark for deletion (never actually deletes)


@dataclass
class RetentionPolicy:
    """Collection of retention rules."""
    name: str
    rules: list = field(default_factory=list)  # list[RetentionRule]
    default_max_age_days: int = 365

    def rule_for(self, data_class: DataClass) -> "RetentionRule | None":
        """Return matching rule, or None."""
        for r in self.rules:
            if r.data_class == data_class:
                return r
        return None

    def max_age_for(self, data_class: DataClass) -> int:
        """Return max_age_days for data_class or default."""
        rule = self.rule_for(data_class)
        return rule.max_age_days if rule else self.default_max_age_days


@dataclass
class RetentionViolation:
    doc_id: str
    data_class: DataClass
    age_days: float
    max_age_days: int
    action: str   # "archive" or "delete" or "review"


class RetentionEngine:
    """Checks documents against retention policy."""

    def __init__(self, policy: RetentionPolicy):
        self._policy = policy

    def check(
        self,
        doc_id: str,
        data_class: DataClass,
        last_modified_iso: str,
    ) -> "RetentionViolation | None":
        """Return RetentionViolation if doc exceeds retention, else None.

        age_days = (now - last_modified).days
        If age_days > max_age_for(data_class):
          rule = policy.rule_for(data_class)
          action = "delete" if rule.auto_delete else "archive" if rule.auto_archive else "review"
          return RetentionViolation(...)
        """
        try:
            last_modified = datetime.fromisoformat(last_modified_iso)
        except (ValueError, TypeError):
            return None

        # Make both timezone-aware or both naive for comparison
        now = datetime.now(timezone.utc)
        if last_modified.tzinfo is None:
            last_modified = last_modified.replace(tzinfo=timezone.utc)

        age_days = (now - last_modified).total_seconds() / 86400.0
        max_age = self._policy.max_age_for(data_class)

        if age_days <= max_age:
            return None

        rule = self._policy.rule_for(data_class)
        if rule is not None and rule.auto_delete:
            action = "delete"
        elif rule is not None and rule.auto_archive:
            action = "archive"
        else:
            action = "review"

        return RetentionViolation(
            doc_id=doc_id,
            data_class=data_class,
            age_days=age_days,
            max_age_days=max_age,
            action=action,
        )

    def check_batch(
        self,
        docs: list,   # list of (doc_id, data_class, last_modified_iso)
    ) -> list:
        """Check multiple docs; return list[RetentionViolation]."""
        violations = []
        for doc_id, dc, ts in docs:
            v = self.check(doc_id, dc, ts)
            if v:
                violations.append(v)
        return violations
