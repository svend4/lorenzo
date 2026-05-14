"""Document composition module: assemble docs from fragments with includes/inheritance."""

from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class FragmentType(Enum):
    HEADER = "header"
    BODY = "body"
    FOOTER = "footer"
    SIDEBAR = "sidebar"
    NAV = "nav"
    ASIDE = "aside"
    OTHER = "other"


@dataclass
class Fragment:
    fragment_id: str
    fragment_type: FragmentType
    content: str
    name: Optional[str] = None
    variables: dict = field(default_factory=dict)
    created_at: float = 0.0


@dataclass
class Composition:
    composition_id: str
    fragments: list = field(default_factory=list)
    variables: dict = field(default_factory=dict)
    parent: Optional[str] = None


@dataclass
class RenderResult:
    content: str
    applied_fragments: list = field(default_factory=list)
    missing_vars: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    success: bool = True


# Regex patterns
# Match ${var} or ${var | default}; exclude include:... by negative lookahead
_VAR_PATTERN = re.compile(r"\$\{(?!include:)([^{}|]+?)(?:\s*\|\s*([^{}]*?))?\}")
_INCLUDE_PATTERN = re.compile(r"\$\{include:([^{}]+?)\}")


class DocCompose:
    """Compose documents from fragments with inheritance, includes, and variable expansion."""

    def __init__(self):
        self._lock = threading.Lock()
        self._fragments: dict = {}
        self._compositions: dict = {}

    # ---------- Fragment management ----------
    def register_fragment(
        self,
        fragment_id: str,
        fragment_type: FragmentType,
        content: str,
        name: Optional[str] = None,
        variables: Optional[dict] = None,
        now: float = 0.0,
    ) -> Fragment:
        with self._lock:
            frag = Fragment(
                fragment_id=fragment_id,
                fragment_type=fragment_type,
                content=content,
                name=name,
                variables=dict(variables) if variables else {},
                created_at=now,
            )
            self._fragments[fragment_id] = frag
            return frag

    def unregister_fragment(self, fragment_id: str) -> bool:
        with self._lock:
            if fragment_id in self._fragments:
                del self._fragments[fragment_id]
                return True
            return False

    def get_fragment(self, fragment_id: str) -> Optional[Fragment]:
        with self._lock:
            return self._fragments.get(fragment_id)

    def fragments_by_type(self, fragment_type: FragmentType) -> list:
        with self._lock:
            return [f for f in self._fragments.values() if f.fragment_type == fragment_type]

    def find_fragment_by_name(self, name: str) -> Optional[Fragment]:
        with self._lock:
            for f in self._fragments.values():
                if f.name == name:
                    return f
            return None

    # ---------- Composition management ----------
    def register_composition(
        self,
        composition_id: str,
        fragments: list,
        variables: Optional[dict] = None,
        parent: Optional[str] = None,
    ) -> Composition:
        with self._lock:
            comp = Composition(
                composition_id=composition_id,
                fragments=list(fragments) if fragments else [],
                variables=dict(variables) if variables else {},
                parent=parent,
            )
            self._compositions[composition_id] = comp
            return comp

    def unregister_composition(self, composition_id: str) -> bool:
        with self._lock:
            if composition_id in self._compositions:
                del self._compositions[composition_id]
                return True
            return False

    def get_composition(self, composition_id: str) -> Optional[Composition]:
        with self._lock:
            return self._compositions.get(composition_id)

    # ---------- Variable expansion ----------
    def extract_variables(self, content: str) -> list:
        """Find all ${var} placeholders. Returns unique variable names."""
        seen = []
        for m in _VAR_PATTERN.finditer(content):
            name = m.group(1).strip()
            if name and name not in seen:
                seen.append(name)
        return seen

    def expand_variables(self, content: str, variables: dict) -> tuple:
        """Expand ${var} and ${var|default}. Returns (expanded, missing_list)."""
        variables = variables or {}
        missing: list = []

        def replace(match):
            var_name = match.group(1).strip()
            default = match.group(2)
            if var_name in variables:
                return str(variables[var_name])
            if default is not None:
                return default.strip()
            if var_name not in missing:
                missing.append(var_name)
            return match.group(0)  # leave unchanged

        expanded = _VAR_PATTERN.sub(replace, content)
        return expanded, missing

    # ---------- Includes ----------
    def process_includes(self, content: str, max_depth: int = 5) -> str:
        """Replace ${include:ID_or_name} with the fragment content, recursive."""
        if max_depth <= 0:
            return content

        def replace(match):
            key = match.group(1).strip()
            with self._lock:
                frag = self._fragments.get(key)
                if frag is None:
                    # search by name
                    for f in self._fragments.values():
                        if f.name == key:
                            frag = f
                            break
            if frag is None:
                return match.group(0)
            # recurse
            return self.process_includes(frag.content, max_depth - 1)

        # If no includes, return as-is
        if "${include:" not in content:
            return content
        return _INCLUDE_PATTERN.sub(replace, content)

    # ---------- Inheritance ----------
    def resolve_inheritance(self, composition_id: str) -> Optional[Composition]:
        """Merge composition with its parent chain. Detects cycles."""
        with self._lock:
            comp = self._compositions.get(composition_id)
            if comp is None:
                return None
            # collect parent chain (root-first)
            chain = []
            visited = set()
            current = comp
            while current is not None:
                if current.composition_id in visited:
                    # cycle detected — stop
                    break
                visited.add(current.composition_id)
                chain.append(current)
                if current.parent is None:
                    break
                current = self._compositions.get(current.parent)

        # Build merged composition: parents first → child last
        merged_fragments: list = []
        merged_variables: dict = {}
        for node in reversed(chain):
            for fid in node.fragments:
                merged_fragments.append(fid)
            merged_variables.update(node.variables)

        return Composition(
            composition_id=composition_id,
            fragments=merged_fragments,
            variables=merged_variables,
            parent=comp.parent,
        )

    # ---------- Rendering ----------
    def render_fragment(self, fragment_id: str, variables: Optional[dict] = None) -> str:
        """Render a single fragment: includes + variable expansion."""
        frag = self.get_fragment(fragment_id)
        if frag is None:
            return ""
        # Merge fragment defaults with given variables (given overrides)
        merged_vars = dict(frag.variables)
        if variables:
            merged_vars.update(variables)
        # Process includes first, then expand vars
        content = self.process_includes(frag.content)
        expanded, _missing = self.expand_variables(content, merged_vars)
        return expanded

    def render(self, composition_id: str, variables: Optional[dict] = None) -> RenderResult:
        """Render a composition: resolve inheritance, expand all fragments."""
        resolved = self.resolve_inheritance(composition_id)
        if resolved is None:
            return RenderResult(
                content="",
                applied_fragments=[],
                missing_vars=[],
                errors=[f"composition not found: {composition_id}"],
                success=False,
            )

        # Build variable scope: composition vars, overridden by call-time vars
        scope_vars = dict(resolved.variables)
        if variables:
            scope_vars.update(variables)

        parts: list = []
        applied: list = []
        all_missing: list = []
        errors: list = []

        for fid in resolved.fragments:
            frag = self.get_fragment(fid)
            if frag is None:
                errors.append(f"fragment not found: {fid}")
                continue
            # Per-fragment variable scope: fragment defaults < composition scope
            frag_vars = dict(frag.variables)
            frag_vars.update(scope_vars)
            # Process includes then expand
            content = self.process_includes(frag.content)
            expanded, missing = self.expand_variables(content, frag_vars)
            parts.append(expanded)
            applied.append(fid)
            for m in missing:
                if m not in all_missing:
                    all_missing.append(m)

        joined = "\n".join(parts)
        return RenderResult(
            content=joined,
            applied_fragments=applied,
            missing_vars=all_missing,
            errors=errors,
            success=len(errors) == 0,
        )

    # ---------- Properties / utilities ----------
    @property
    def total_fragments(self) -> int:
        with self._lock:
            return len(self._fragments)

    @property
    def total_compositions(self) -> int:
        with self._lock:
            return len(self._compositions)

    def clear(self) -> None:
        with self._lock:
            self._fragments.clear()
            self._compositions.clear()
