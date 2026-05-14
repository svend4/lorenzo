"""Unified governance policy engine."""
from dataclasses import dataclass, field

from docstoolkit.governance.classifier import DataClass, DataClassifier
from docstoolkit.governance.retention import (
    RetentionEngine,
    RetentionPolicy,
    RetentionViolation,
)

_RETENTION_SEVERITY = {
    DataClass.SECRET: "critical",
    DataClass.CONFIDENTIAL: "high",
    DataClass.INTERNAL: "medium",
    DataClass.PUBLIC: "low",
}


@dataclass
class PolicyViolation:
    """A governance policy violation."""
    doc_id: str
    violation_type: str    # "classification" | "retention" | "access"
    detail: str
    severity: str          # "low" | "medium" | "high" | "critical"
    data_class: DataClass = DataClass.INTERNAL

    def is_critical(self) -> bool:
        return self.severity == "critical"


@dataclass
class PolicyReport:
    """Report from a policy engine run."""
    violations: list = field(default_factory=list)   # list[PolicyViolation]
    docs_checked: int = 0
    clean_docs: int = 0

    def violation_count(self) -> int:
        return len(self.violations)

    def critical_count(self) -> int:
        return sum(1 for v in self.violations if v.is_critical())

    def by_type(self, vtype: str) -> list:
        return [v for v in self.violations if v.violation_type == vtype]

    def summary(self) -> str:
        return (
            f"docs={self.docs_checked} clean={self.clean_docs} "
            f"violations={self.violation_count()} critical={self.critical_count()}"
        )


class PolicyEngine:
    """Unified governance engine: classify + retention check."""

    def __init__(
        self,
        classifier: DataClassifier,
        retention_engine: RetentionEngine | None = None,
    ):
        self._classifier = classifier
        self._retention = retention_engine

    def audit(
        self,
        docs: list,   # list of (doc_id, content, last_modified_iso)
    ) -> PolicyReport:
        """Run full governance audit.

        For each doc:
        1. Classify content → DataClass
        2. If classification is SECRET: add PolicyViolation severity="critical"
        3. If retention_engine: check retention → if violation: add PolicyViolation
        4. Track docs_checked and clean_docs

        Return PolicyReport.

        Violation severity mapping (retention):
        - DataClass.SECRET + retention violation → "critical"
        - DataClass.CONFIDENTIAL + retention violation → "high"
        - DataClass.INTERNAL + retention violation → "medium"
        - DataClass.PUBLIC + retention violation → "low"
        """
        report = PolicyReport(docs_checked=len(docs))
        doc_violations: dict[str, list] = {}

        for doc_id, content, last_modified_iso in docs:
            data_class = self._classifier.classify(content)
            violations_for_doc = []

            # Classification check: SECRET content triggers a violation
            if data_class == DataClass.SECRET:
                violations_for_doc.append(PolicyViolation(
                    doc_id=doc_id,
                    violation_type="classification",
                    detail=f"Document classified as SECRET",
                    severity="critical",
                    data_class=data_class,
                ))

            # Retention check
            if self._retention is not None:
                rv = self._retention.check(doc_id, data_class, last_modified_iso)
                if rv is not None:
                    severity = _RETENTION_SEVERITY.get(data_class, "medium")
                    violations_for_doc.append(PolicyViolation(
                        doc_id=doc_id,
                        violation_type="retention",
                        detail=(
                            f"Document age {rv.age_days:.1f}d exceeds "
                            f"max {rv.max_age_days}d; action={rv.action}"
                        ),
                        severity=severity,
                        data_class=data_class,
                    ))

            report.violations.extend(violations_for_doc)
            if not violations_for_doc:
                report.clean_docs += 1

        return report
