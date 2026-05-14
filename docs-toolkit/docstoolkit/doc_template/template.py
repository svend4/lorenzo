"""doc_template.template — document-style templates with sections and includes.

Simple variable-based document templates supporting:
- Variables: ${variable_name}
- Defaults: ${variable_name:default_value}
- Section markers: {{section: section_name}}
- Comments: {{# this is a comment }}

Pure stdlib.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# ${name} or ${name:default}
_VAR_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)(?::([^}]*))?\}")

# {{section: name}}
_SECTION_RE = re.compile(r"\{\{\s*section:\s*([A-Za-z_][A-Za-z0-9_\-]*)\s*\}\}")

# {{# comment }} (non-greedy)
_COMMENT_RE = re.compile(r"\{\{#.*?\}\}", re.DOTALL)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class TemplateSection:
    """A named section of a document template."""

    name: str
    content: str
    is_required: bool = False


@dataclass
class TemplateDefinition:
    """A named document template made up of sections plus a list of required variables."""

    name: str
    sections: list[TemplateSection] = field(default_factory=list)
    variables: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class RenderResult:
    """The result of rendering a template."""

    output: str
    missing_variables: list[str] = field(default_factory=list)
    missing_sections: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return not self.missing_variables and not self.missing_sections


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class TemplateRegistry:
    """In-memory registry of named templates."""

    def __init__(self) -> None:
        self._templates: dict[str, TemplateDefinition] = {}

    def register(self, template: TemplateDefinition) -> None:
        if not isinstance(template, TemplateDefinition):
            raise TypeError("template must be a TemplateDefinition")
        if not template.name:
            raise ValueError("template.name must be a non-empty string")
        self._templates[template.name] = template

    def get(self, name: str) -> Optional[TemplateDefinition]:
        return self._templates.get(name)

    def list_names(self) -> list[str]:
        return sorted(self._templates.keys())

    def remove(self, name: str) -> bool:
        if name in self._templates:
            del self._templates[name]
            return True
        return False

    @property
    def count(self) -> int:
        return len(self._templates)


# ---------------------------------------------------------------------------
# DocTemplate (engine)
# ---------------------------------------------------------------------------


class DocTemplate:
    """Document template engine: render, parse, validate, extract."""

    def __init__(self, registry: Optional[TemplateRegistry] = None) -> None:
        self.registry = registry if registry is not None else TemplateRegistry()

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render_string(
        self,
        template: str,
        variables: dict,
    ) -> str:
        """Render an arbitrary template string with variable substitution.

        Substitutes ${var} or ${var:default}. Comments are stripped.
        Missing variables (without defaults) are left as-is.
        """
        if template is None:
            return ""
        # Strip comments first.
        text = _COMMENT_RE.sub("", template)

        def _sub(match: re.Match[str]) -> str:
            name = match.group(1)
            default = match.group(2)
            if name in variables:
                return str(variables[name])
            if default is not None:
                return default
            return match.group(0)  # leave placeholder

        return _VAR_RE.sub(_sub, text)

    def render_section(self, section: str, variables: dict) -> str:
        """Render a single section string with variables (alias for render_string)."""
        return self.render_string(section, variables)

    def render(
        self,
        template_name: str,
        variables: dict,
        sections: Optional[dict] = None,
    ) -> RenderResult:
        """Render a template registered under ``template_name``.

        Sections are joined in declaration order. Optional override content for
        sections may be passed via the ``sections`` dict (keyed by section name).
        Section markers ``{{section: name}}`` inside section content are also
        expanded using the override dict.
        """
        sections = sections or {}
        template = self.registry.get(template_name)
        if template is None:
            return RenderResult(
                output="",
                missing_variables=[],
                missing_sections=[f"template:{template_name}"],
            )

        # Validate required pieces first.
        ok, missing = self.validate(template, variables, sections)
        missing_vars = [m[4:] for m in missing if m.startswith("var:")]
        missing_secs = [m[8:] for m in missing if m.startswith("section:")]

        rendered_parts: list[str] = []
        for sec in template.sections:
            # Section content can be overridden by the sections dict.
            raw = sections.get(sec.name, sec.content)
            # Expand inline section markers in content.
            raw = self._expand_section_markers(raw, sections)
            rendered_parts.append(self.render_string(raw, variables))

        output = "\n".join(rendered_parts)

        return RenderResult(
            output=output,
            missing_variables=missing_vars,
            missing_sections=missing_secs,
        )

    def _expand_section_markers(self, text: str, sections: dict) -> str:
        """Replace ``{{section: name}}`` markers with sections[name] if present."""

        def _sub(match: re.Match[str]) -> str:
            name = match.group(1)
            if name in sections:
                return str(sections[name])
            return match.group(0)

        return _SECTION_RE.sub(_sub, text)

    # ------------------------------------------------------------------
    # Extraction
    # ------------------------------------------------------------------

    def extract_variables(self, text: str) -> list[str]:
        """Return the ordered list of unique variable names referenced in ``text``."""
        if not text:
            return []
        seen: list[str] = []
        for match in _VAR_RE.finditer(text):
            name = match.group(1)
            if name not in seen:
                seen.append(name)
        return seen

    def extract_sections(self, text: str) -> list[str]:
        """Return the ordered list of unique section markers referenced in ``text``."""
        if not text:
            return []
        seen: list[str] = []
        for match in _SECTION_RE.finditer(text):
            name = match.group(1)
            if name not in seen:
                seen.append(name)
        return seen

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    def parse(self, text: str) -> TemplateDefinition:
        """Parse a template document with optional YAML-like frontmatter.

        Frontmatter is a block of ``key: value`` pairs delimited by ``---`` lines.
        Recognised keys: ``name``, ``description``, ``variables`` (list-formatted
        as ``[a, b, c]``).

        Body is split into sections by ``{{section: name}}`` markers; if none are
        present a single section named ``body`` is produced.
        """
        if text is None:
            text = ""

        meta_name = "untitled"
        description = ""
        variables: list[str] = []

        body = text
        if text.lstrip().startswith("---"):
            stripped = text.lstrip("\n")
            # Find end of frontmatter (second `---` line).
            lines = stripped.split("\n")
            # First line must be ---
            if lines and lines[0].strip() == "---":
                end_idx = -1
                for i in range(1, len(lines)):
                    if lines[i].strip() == "---":
                        end_idx = i
                        break
                if end_idx > 0:
                    fm_lines = lines[1:end_idx]
                    body = "\n".join(lines[end_idx + 1 :])
                    # Strip a single leading newline from body for tidiness.
                    if body.startswith("\n"):
                        body = body[1:]
                    for fm_line in fm_lines:
                        if ":" not in fm_line:
                            continue
                        key, _, value = fm_line.partition(":")
                        key = key.strip()
                        value = value.strip()
                        if key == "name":
                            meta_name = value or meta_name
                        elif key == "description":
                            description = value
                        elif key == "variables":
                            # Format: [a, b, c]
                            if value.startswith("[") and value.endswith("]"):
                                inner = value[1:-1]
                                variables = [
                                    v.strip().strip("\"'")
                                    for v in inner.split(",")
                                    if v.strip()
                                ]
                            elif value:
                                variables = [
                                    v.strip().strip("\"'")
                                    for v in value.split(",")
                                    if v.strip()
                                ]

        # Build sections from body. Sections are split on {{section: name}} lines.
        sections = self._split_sections(body)

        # If no variables specified in frontmatter, auto-extract.
        if not variables:
            variables = self.extract_variables(body)

        return TemplateDefinition(
            name=meta_name,
            sections=sections,
            variables=variables,
            description=description,
        )

    def _split_sections(self, body: str) -> list[TemplateSection]:
        """Split body into a list of TemplateSection.

        A ``{{section: name}}`` marker starts a new named section. Any content
        before the first marker forms a section named ``body``.
        """
        if not body:
            return [TemplateSection(name="body", content="")]

        markers = list(_SECTION_RE.finditer(body))
        if not markers:
            return [TemplateSection(name="body", content=body)]

        sections: list[TemplateSection] = []
        # Prefix content before first marker becomes "body" (if non-empty).
        first = markers[0]
        prefix = body[: first.start()]
        if prefix.strip():
            sections.append(TemplateSection(name="body", content=prefix))

        for i, marker in enumerate(markers):
            name = marker.group(1)
            start = marker.end()
            end = markers[i + 1].start() if i + 1 < len(markers) else len(body)
            content = body[start:end]
            # Trim a single leading newline for tidiness.
            if content.startswith("\n"):
                content = content[1:]
            sections.append(TemplateSection(name=name, content=content))

        return sections

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
        template: TemplateDefinition,
        variables: dict,
        sections: Optional[dict] = None,
    ) -> tuple[bool, list[str]]:
        """Validate that all required variables and required sections are provided.

        Returns a tuple ``(ok, missing)`` where missing items are prefixed with
        either ``var:`` or ``section:`` to indicate kind.
        """
        sections = sections or {}
        missing: list[str] = []

        for var in template.variables:
            if var not in variables:
                missing.append(f"var:{var}")

        for sec in template.sections:
            if sec.is_required:
                # Required if either content non-empty in definition or provided.
                provided = sec.name in sections
                has_default = bool((sec.content or "").strip())
                if not provided and not has_default:
                    missing.append(f"section:{sec.name}")

        return (not missing, missing)


__all__ = [
    "DocTemplate",
    "RenderResult",
    "TemplateDefinition",
    "TemplateRegistry",
    "TemplateSection",
]
