"""Template renderer: fills placeholders and records missing variables."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.notif_templates.template import NotifTemplate, TemplateFormat


@dataclass
class RenderResult:
    """Result of rendering a single template against a context."""

    subject: str
    body: str
    format: TemplateFormat
    missing_vars: list[str] = field(default_factory=list)

    def is_complete(self) -> bool:
        """Return True when no required variables were missing."""
        return len(self.missing_vars) == 0


class _SafeFormatMap(dict):
    """dict subclass used with str.format_map.

    Behaviour:
    - Returns the context value if the key is present.
    - Falls back to the declared ``default_value`` for optional variables.
    - Records required variables that are absent (without raising KeyError).
    - Leaves unknown placeholders unchanged so they surface in missing_vars.
    """

    def __init__(self, context: dict, template: NotifTemplate, missing: list[str]) -> None:
        super().__init__(context)
        self._template = template
        self._missing = missing
        # Build lookup maps from variable declarations
        self._defaults: dict[str, str] = {
            v.name: v.default_value for v in template.variables if not v.required
        }
        self._required_names: set[str] = {
            v.name for v in template.variables if v.required
        }

    def __missing__(self, key: str) -> str:  # type: ignore[override]
        if key in self._defaults:
            return self._defaults[key]
        # Required variable or undeclared placeholder: record as missing
        if key not in self._missing:
            self._missing.append(key)
        # Return a sentinel so the placeholder is visible in the rendered output
        return f"{{{key}}}"


class TemplateRenderer:
    """Renders :class:`NotifTemplate` instances against variable contexts."""

    def render(self, template: NotifTemplate, context: dict) -> RenderResult:
        """Render *template* with *context*, recording any missing required vars."""
        missing: list[str] = []
        fmt_map = _SafeFormatMap(context, template, missing)

        rendered_subject = template.subject.format_map(fmt_map)
        rendered_body = template.body.format_map(fmt_map)

        return RenderResult(
            subject=rendered_subject,
            body=rendered_body,
            format=template.format,
            missing_vars=missing,
        )

    def render_batch(
        self, template: NotifTemplate, contexts: list[dict]
    ) -> list[RenderResult]:
        """Render *template* for each context dict in *contexts*."""
        return [self.render(template, ctx) for ctx in contexts]

    def validate(self, template: NotifTemplate, context: dict) -> list[str]:
        """Return names of required variables absent from *context*."""
        required = set(template.required_variables())
        provided = set(context.keys())
        return sorted(required - provided)
