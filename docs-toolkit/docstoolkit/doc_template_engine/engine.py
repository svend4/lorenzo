"""doc_template_engine.engine — simple {{variable}} string template engine.

Supports {{var}} placeholders, pure stdlib, thread-safe via threading.Lock.
"""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4

# ---------------------------------------------------------------------------
# Regex
# ---------------------------------------------------------------------------

_VAR_RE = re.compile(r"\{\{(\w+)\}\}")


def _extract_variables(content: str) -> list[str]:
    """Return sorted unique list of {{var}} names found in *content*."""
    return sorted(set(_VAR_RE.findall(content)))


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Template:
    """A registered template with extracted variable names."""

    template_id: str
    name: str
    content: str
    variables: list[str]   # sorted list of variable names found in content
    created_at: float


@dataclass
class RenderResult:
    """Result of rendering a template."""

    template_id: str
    rendered: str
    variables_used: list[str]   # variables that were substituted
    missing_vars: list[str]     # variables in template not provided


# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------


class DocTemplateEngine:
    """Simple {{variable}} template engine. Pure stdlib, thread-safe."""

    def __init__(self) -> None:
        self._templates: dict[str, Template] = {}   # keyed by template_id
        self._by_name: dict[str, str] = {}          # name -> template_id
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(
        self,
        name: str,
        content: str,
        now: Optional[float] = None,
    ) -> Template:
        """Register a new template.

        Extracts ``{{var}}`` placeholders into ``variables``.
        ``template_id`` is generated as ``tmpl_<10 hex chars>``.
        """
        import time as _time

        template_id = f"tmpl_{uuid4().hex[:10]}"
        variables = _extract_variables(content)
        created_at = now if now is not None else _time.time()
        tmpl = Template(
            template_id=template_id,
            name=name,
            content=content,
            variables=variables,
            created_at=created_at,
        )
        with self._lock:
            self._templates[template_id] = tmpl
            self._by_name[name] = template_id
        return tmpl

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def get(self, template_id: str) -> Optional[Template]:
        """Return a template by its ID, or None if not found."""
        with self._lock:
            return self._templates.get(template_id)

    def get_by_name(self, name: str) -> Optional[Template]:
        """Return a template by its name, or None if not found."""
        with self._lock:
            tid = self._by_name.get(name)
            if tid is None:
                return None
            return self._templates.get(tid)

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def update(self, template_id: str, content: str) -> Optional[Template]:
        """Update template content and re-extract variables.

        Returns None if *template_id* is not registered.
        """
        with self._lock:
            tmpl = self._templates.get(template_id)
            if tmpl is None:
                return None
            updated = Template(
                template_id=tmpl.template_id,
                name=tmpl.name,
                content=content,
                variables=_extract_variables(content),
                created_at=tmpl.created_at,
            )
            self._templates[template_id] = updated
            self._by_name[updated.name] = template_id
            return updated

    def delete(self, template_id: str) -> bool:
        """Delete a template. Returns True if it existed, False otherwise."""
        with self._lock:
            tmpl = self._templates.pop(template_id, None)
            if tmpl is None:
                return False
            self._by_name.pop(tmpl.name, None)
            return True

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(
        self,
        template_id: str,
        variables: dict,
        strict: bool = False,
    ) -> Optional[RenderResult]:
        """Render a registered template with *variables*.

        - Replaces ``{{var}}`` with ``str(variables[var])`` when present.
        - If *strict* is True and any placeholder variable is missing,
          raises ``ValueError`` listing missing variable names.
        - If *strict* is False, leaves unresolved ``{{var}}`` unchanged.
        - Returns None if *template_id* is not found.
        """
        with self._lock:
            tmpl = self._templates.get(template_id)
        if tmpl is None:
            return None
        return self._do_render(tmpl.template_id, tmpl.content, tmpl.variables, variables, strict)

    def render_string(
        self,
        content: str,
        variables: dict,
        strict: bool = False,
    ) -> RenderResult:
        """Render an ad-hoc template string without registering it."""
        tmpl_vars = _extract_variables(content)
        return self._do_render("", content, tmpl_vars, variables, strict)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def templates(self) -> list[Template]:
        """Return all registered templates sorted by name."""
        with self._lock:
            return sorted(self._templates.values(), key=lambda t: t.name)

    def find_templates_using(self, variable_name: str) -> list[Template]:
        """Return templates whose variable list includes *variable_name*."""
        with self._lock:
            return [
                t for t in self._templates.values()
                if variable_name in t.variables
            ]

    @property
    def total_templates(self) -> int:
        """Total number of registered templates."""
        with self._lock:
            return len(self._templates)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _do_render(
        template_id: str,
        content: str,
        tmpl_vars: list[str],
        variables: dict,
        strict: bool,
    ) -> RenderResult:
        """Core rendering logic shared by render() and render_string()."""
        missing_vars = [v for v in tmpl_vars if v not in variables]
        if strict and missing_vars:
            raise ValueError(
                f"Missing template variables: {', '.join(sorted(missing_vars))}"
            )

        variables_used: list[str] = []

        def _replacer(match: re.Match) -> str:
            var = match.group(1)
            if var in variables:
                variables_used.append(var)
                return str(variables[var])
            return match.group(0)  # leave placeholder intact

        rendered = _VAR_RE.sub(_replacer, content)

        return RenderResult(
            template_id=template_id,
            rendered=rendered,
            variables_used=sorted(set(variables_used)),
            missing_vars=missing_vars,
        )


__all__ = [
    "DocTemplateEngine",
    "RenderResult",
    "Template",
]
