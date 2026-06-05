"""Notification template definitions."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class TemplateFormat(Enum):
    """Output format for a rendered notification template."""

    TEXT = "text"
    HTML = "html"
    MARKDOWN = "markdown"
    JSON = "json"


@dataclass
class TemplateVariable:
    """Declares a single variable used in a template."""

    name: str
    required: bool = True
    default_value: str = ""
    description: str = ""


@dataclass
class NotifTemplate:
    """A notification template with subject/body placeholders."""

    name: str
    body: str
    template_id: str = field(default_factory=lambda: uuid4().hex[:8])
    subject: str = ""
    format: TemplateFormat = TemplateFormat.TEXT
    variables: list[TemplateVariable] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def required_variables(self) -> list[str]:
        """Return names of required variables."""
        return [v.name for v in self.variables if v.required]

    def optional_variables(self) -> list[str]:
        """Return names of optional variables (not required)."""
        return [v.name for v in self.variables if not v.required]
