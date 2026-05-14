"""template_engine.engine — simple string template engine (pure stdlib)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


class TemplateError(Exception):
    """Raised for syntax errors or missing variables."""


@dataclass
class Template:
    name: str
    source: str


# ---------------------------------------------------------------------------
# Regex patterns for template tags
# ---------------------------------------------------------------------------
_VAR_RE = re.compile(r"\{\{\s*(.+?)\s*\}\}")
_TAG_RE = re.compile(r"\{%\s*(.+?)\s*%\}")
_COMMENT_RE = re.compile(r"\{#.*?#\}", re.DOTALL)


def _resolve(name: str, context: dict, strict: bool) -> Any:
    """Resolve a potentially dot-notation name against *context*."""
    parts = name.split(".")
    value: Any = context
    for part in parts:
        if isinstance(value, dict):
            if part not in value:
                if strict:
                    raise TemplateError(f"Undefined variable: {name!r}")
                return ""
            value = value[part]
        else:
            if strict:
                raise TemplateError(f"Undefined variable: {name!r}")
            return ""
    return value


def _substitute_vars(text: str, context: dict, strict: bool) -> str:
    """Replace all {{ var }} occurrences in *text* using *context*."""
    def replacer(m: re.Match) -> str:
        val = _resolve(m.group(1).strip(), context, strict)
        return str(val)

    return _VAR_RE.sub(replacer, text)


# ---------------------------------------------------------------------------
# Line-oriented AST node types
# ---------------------------------------------------------------------------
# We represent the template as a flat list of *lines* and then build a tree
# using a recursive-descent parser over that list.

class _TextNode:
    __slots__ = ("text",)

    def __init__(self, text: str) -> None:
        self.text = text

    def render(self, context: dict, strict: bool) -> str:
        return _substitute_vars(self.text, context, strict)


class _IfNode:
    __slots__ = ("condition", "true_nodes", "false_nodes")

    def __init__(
        self,
        condition: str,
        true_nodes: list,
        false_nodes: list,
    ) -> None:
        self.condition = condition
        self.true_nodes = true_nodes
        self.false_nodes = false_nodes

    def render(self, context: dict, strict: bool) -> str:
        value = _resolve(self.condition, context, strict)
        nodes = self.true_nodes if value else self.false_nodes
        return _render_nodes(nodes, context, strict)


class _ForNode:
    __slots__ = ("loop_var", "iterable", "body_nodes")

    def __init__(self, loop_var: str, iterable: str, body_nodes: list) -> None:
        self.loop_var = loop_var
        self.iterable = iterable
        self.body_nodes = body_nodes

    def render(self, context: dict, strict: bool) -> str:
        items = _resolve(self.iterable, context, strict)
        if not items:
            return ""
        parts: list[str] = []
        for item in items:
            child_ctx = {**context, self.loop_var: item}
            parts.append(_render_nodes(self.body_nodes, child_ctx, strict))
        return "".join(parts)


def _render_nodes(nodes: list, context: dict, strict: bool) -> str:
    return "".join(node.render(context, strict) for node in nodes)


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class _Parser:
    """Parse a list of raw lines into a tree of AST nodes."""

    def __init__(self, lines: list[str], strict: bool) -> None:
        self._lines = lines
        self._pos = 0
        self._strict = strict

    def _peek(self) -> str | None:
        if self._pos < len(self._lines):
            return self._lines[self._pos]
        return None

    def _consume(self) -> str:
        line = self._lines[self._pos]
        self._pos += 1
        return line

    def _tag_of(self, line: str) -> str | None:
        """Return the stripped tag keyword if *line* is a pure tag line."""
        m = _TAG_RE.fullmatch(line.strip())
        if m:
            return m.group(1).strip()
        return None

    def parse(self) -> list:
        return self._parse_nodes(stop_tags=frozenset())

    def _parse_nodes(self, stop_tags: frozenset[str]) -> list:
        nodes: list = []
        while self._pos < len(self._lines):
            line = self._peek()
            assert line is not None
            tag = self._tag_of(line)
            if tag is not None and _is_stop_tag(tag, stop_tags):
                break
            self._consume()
            if tag is None:
                # Plain text (possibly containing {{ }} but no block tags)
                nodes.append(_TextNode(line))
            elif tag.startswith("if "):
                condition = tag[3:].strip()
                nodes.append(self._parse_if(condition))
            elif tag.startswith("for "):
                nodes.append(self._parse_for(tag))
            elif tag.startswith("else") and "else" in stop_tags:
                # Handled by caller — push back so caller sees it
                self._pos -= 1
                break
            else:
                # Unknown tag — treat as text (preserves whitespace-only lines)
                nodes.append(_TextNode(line))
        return nodes

    def _parse_if(self, condition: str) -> _IfNode:
        true_nodes = self._parse_nodes(stop_tags=frozenset({"else", "endif"}))
        # peek at what stopped us
        stop_line = self._peek()
        if stop_line is None:
            raise TemplateError("Unclosed {% if %} block")
        stop_tag = self._tag_of(stop_line)
        false_nodes: list = []
        if stop_tag is not None and stop_tag.startswith("else"):
            self._consume()  # consume {% else %}
            false_nodes = self._parse_nodes(stop_tags=frozenset({"endif"}))
            stop_line = self._peek()
            if stop_line is None:
                raise TemplateError("Unclosed {% if %} / {% else %} block")
        # consume {% endif %}
        self._consume()
        return _IfNode(condition, true_nodes, false_nodes)

    def _parse_for(self, tag: str) -> _ForNode:
        # tag looks like: "for item in items"
        m = re.fullmatch(r"for\s+(\w+)\s+in\s+(\S+)", tag)
        if not m:
            raise TemplateError(f"Invalid for tag: {{% {tag} %}}")
        loop_var = m.group(1)
        iterable = m.group(2)
        body_nodes = self._parse_nodes(stop_tags=frozenset({"endfor"}))
        stop_line = self._peek()
        if stop_line is None:
            raise TemplateError("Unclosed {% for %} block")
        self._consume()  # consume {% endfor %}
        return _ForNode(loop_var, iterable, body_nodes)


def _is_stop_tag(tag: str, stop_tags: frozenset[str]) -> bool:
    return any(tag == s or tag.startswith(s) for s in stop_tags)


# ---------------------------------------------------------------------------
# Pre-processing: strip comments, split into lines, handle tag-only lines
# ---------------------------------------------------------------------------

def _preprocess(source: str) -> list[str]:
    """Remove comments, split into *render lines*.

    Lines that contain only a block tag ({% %}) are stripped of their
    trailing newline so they don't produce a blank line in output.
    """
    # Remove comments first
    source = _COMMENT_RE.sub("", source)

    raw_lines = source.split("\n")
    result: list[str] = []
    for i, raw in enumerate(raw_lines):
        is_last = i == len(raw_lines) - 1
        # A line is a "tag-only" line if, after stripping whitespace, it
        # matches exactly one {% %} tag and nothing else.
        stripped = raw.strip()
        if _TAG_RE.fullmatch(stripped):
            # Tag-only line: yield without the trailing newline
            result.append(raw)
        else:
            # Normal line: append newline to all lines except the very last
            result.append(raw if is_last else raw + "\n")
    return result


def _compile(source: str, strict: bool) -> list:
    lines = _preprocess(source)
    parser = _Parser(lines, strict)
    return parser.parse()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

class TemplateEngine:
    """Simple string template engine — pure stdlib, no external deps."""

    def __init__(self, strict: bool = True) -> None:
        self._strict = strict
        self._templates: dict[str, Template] = {}

    def register(self, template: Template) -> None:
        """Register a template by name."""
        self._templates[template.name] = template

    def render(self, name: str, context: dict) -> str:
        """Render a registered template with context variables."""
        if name not in self._templates:
            raise TemplateError(f"Template not registered: {name!r}")
        return self.render_string(self._templates[name].source, context)

    def render_string(self, source: str, context: dict) -> str:
        """Render a template source string directly."""
        nodes = _compile(source, self._strict)
        return _render_nodes(nodes, context, self._strict)

    def registered(self) -> list[str]:
        """Return names of all registered templates."""
        return list(self._templates)
