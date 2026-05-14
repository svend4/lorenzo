"""Data classification by content patterns."""
import re
from dataclasses import dataclass, field
from enum import Enum


class DataClass(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"


@dataclass
class ClassificationRule:
    """Pattern-based classification rule."""
    name: str
    pattern: str          # regex pattern to match in content
    data_class: DataClass
    priority: int = 0     # higher = applied first


@dataclass
class DataClassifier:
    """Classifies documents by content patterns."""
    rules: list = field(default_factory=list)   # list[ClassificationRule]
    default_class: DataClass = DataClass.INTERNAL

    def add_rule(self, rule: ClassificationRule) -> None:
        """Add rule; keep sorted by priority desc."""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: -r.priority)

    def classify(self, content: str) -> DataClass:
        """Apply rules in priority order; return first match or default."""
        for rule in self.rules:
            if re.search(rule.pattern, content, re.IGNORECASE):
                return rule.data_class
        return self.default_class

    def explain(self, content: str) -> tuple:
        """Return (DataClass, rule_name_or_'default')."""
        for rule in self.rules:
            if re.search(rule.pattern, content, re.IGNORECASE):
                return (rule.data_class, rule.name)
        return (self.default_class, "default")


def classify_document(
    content: str,
    rules: list | None = None,    # list[ClassificationRule]
) -> DataClass:
    """Convenience: classify with optional rule list, else sensible defaults.

    Default rules (in priority order):
    - SECRET: pattern r'\\b(password|secret|private.?key|api.?key|token)\\b'  priority=100
    - CONFIDENTIAL: pattern r'\\b(confidential|internal.?only|do.?not.?share)\\b'  priority=50
    - PUBLIC: pattern r'\\b(public|open.?source|cc.?by|mit.?license)\\b'  priority=10
    """
    classifier = DataClassifier()
    default_rules = rules or [
        ClassificationRule(
            "secret_data",
            r'\b(password|secret|private.?key|api.?key|token)\b',
            DataClass.SECRET,
            priority=100,
        ),
        ClassificationRule(
            "confidential_data",
            r'\b(confidential|internal.?only|do.?not.?share)\b',
            DataClass.CONFIDENTIAL,
            priority=50,
        ),
        ClassificationRule(
            "public_data",
            r'\b(public|open.?source|cc.?by|mit.?license)\b',
            DataClass.PUBLIC,
            priority=10,
        ),
    ]
    for r in default_rules:
        classifier.add_rule(r)
    return classifier.classify(content)
