"""Layout templates for documents with slot fill, inheritance, and rendering."""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Optional, Union


# Regex for placeholders
# Multi-slot block: {{#name}}...{{/name}}
_MULTI_RE = re.compile(r"\{\{#(\w+)\}\}(.*?)\{\{/\1\}\}", re.DOTALL)
# Single slot {{name}} or {{name | default}}
_SLOT_RE = re.compile(r"\{\{\s*(\w+)\s*(?:\|\s*([^}]*?))?\s*\}\}")


@dataclass
class LayoutSlot:
    name: str
    default: str = ""
    required: bool = False
    multi: bool = False


@dataclass
class Layout:
    name: str
    template: str
    slots: list[LayoutSlot] = field(default_factory=list)
    extends: Optional[str] = None


@dataclass
class RenderError:
    slot_name: str
    error: str


@dataclass
class RenderOutput:
    text: str
    errors: list[RenderError] = field(default_factory=list)
    success: bool = True
    unfilled_slots: list[str] = field(default_factory=list)


class DocLayout:
    """Registry and renderer for layout templates."""

    def __init__(self) -> None:
        self._layouts: dict[str, Layout] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    def register_layout(
        self,
        name: str,
        template: str,
        slots: Optional[list[LayoutSlot]] = None,
        extends: Optional[str] = None,
    ) -> Layout:
        with self._lock:
            layout = Layout(
                name=name,
                template=template,
                slots=list(slots) if slots else [],
                extends=extends,
            )
            self._layouts[name] = layout
            return layout

    def unregister_layout(self, name: str) -> bool:
        with self._lock:
            if name in self._layouts:
                del self._layouts[name]
                return True
            return False

    def get_layout(self, name: str) -> Optional[Layout]:
        with self._lock:
            return self._layouts.get(name)

    def list_layouts(self) -> list[Layout]:
        with self._lock:
            return list(self._layouts.values())

    def layouts_extending(self, parent_name: str) -> list[Layout]:
        with self._lock:
            return [layout for layout in self._layouts.values() if layout.extends == parent_name]

    @property
    def total_layouts(self) -> int:
        with self._lock:
            return len(self._layouts)

    def clear(self) -> None:
        with self._lock:
            self._layouts.clear()

    # ------------------------------------------------------------------
    # Template inspection
    # ------------------------------------------------------------------
    def extract_slots(self, template: str) -> list[str]:
        """Return ordered, de-duplicated list of slot names in the template."""
        names: list[str] = []
        seen: set[str] = set()

        for match in _MULTI_RE.finditer(template):
            slot_name = match.group(1)
            if slot_name not in seen:
                seen.add(slot_name)
                names.append(slot_name)

        # Strip multi-blocks before scanning single slots so inner placeholders
        # aren't double counted.
        stripped = _MULTI_RE.sub("", template)
        for match in _SLOT_RE.finditer(stripped):
            slot_name = match.group(1)
            if slot_name not in seen:
                seen.add(slot_name)
                names.append(slot_name)

        return names

    def validate_layout(self, layout: Layout) -> tuple[bool, list[str]]:
        """Validate a layout. Returns (ok, errors)."""
        errors: list[str] = []

        if not layout.name:
            errors.append("layout name is empty")
        if not isinstance(layout.template, str):
            errors.append("template must be a string")

        slot_names: set[str] = set()
        for slot in layout.slots:
            if not slot.name:
                errors.append("slot with empty name")
                continue
            if slot.name in slot_names:
                errors.append(f"duplicate slot: {slot.name}")
            slot_names.add(slot.name)

        # Check for unclosed multi blocks
        opens = re.findall(r"\{\{#(\w+)\}\}", layout.template)
        closes = re.findall(r"\{\{/(\w+)\}\}", layout.template)
        if sorted(opens) != sorted(closes):
            errors.append("unbalanced multi-slot blocks")

        # Required slots with defaults can still be required; check sanity
        for slot in layout.slots:
            if slot.required and slot.multi and slot.default:
                # default for a multi slot doesn't quite make sense but allow it
                pass

        return (len(errors) == 0, errors)

    # ------------------------------------------------------------------
    # Inheritance
    # ------------------------------------------------------------------
    def resolve_inheritance(self, name: str) -> Optional[Layout]:
        """Return a merged layout walking up the extends chain.

        Child overrides parent. Detects cycles."""
        with self._lock:
            current = self._layouts.get(name)
            if current is None:
                return None

            chain: list[Layout] = []
            visited: set[str] = set()
            cursor: Optional[Layout] = current
            while cursor is not None:
                if cursor.name in visited:
                    # Cycle: stop here
                    break
                visited.add(cursor.name)
                chain.append(cursor)
                if cursor.extends is None:
                    break
                cursor = self._layouts.get(cursor.extends)

        # Walk from root → child, accumulating
        merged_template = ""
        merged_slots: dict[str, LayoutSlot] = {}
        # chain[0] is current (most specific), chain[-1] is root
        for layout in reversed(chain):
            if layout.template:
                merged_template = layout.template
            for slot in layout.slots:
                merged_slots[slot.name] = slot

        # The most-specific layout's template wins if it set one
        # (already handled by overwriting in the loop above)

        return Layout(
            name=current.name,
            template=merged_template,
            slots=list(merged_slots.values()),
            extends=current.extends,
        )

    # ------------------------------------------------------------------
    # Slot mutation
    # ------------------------------------------------------------------
    def set_default_slot(self, layout_name: str, slot_name: str, default: str) -> bool:
        with self._lock:
            layout = self._layouts.get(layout_name)
            if layout is None:
                return False
            for slot in layout.slots:
                if slot.name == slot_name:
                    slot.default = default
                    return True
            # Slot not declared: add it
            layout.slots.append(LayoutSlot(name=slot_name, default=default))
            return True

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def render(
        self,
        layout_name: str,
        slot_content: Optional[dict[str, Union[str, list]]] = None,
        strict: bool = False,
    ) -> RenderOutput:
        slot_content = slot_content or {}

        resolved = self.resolve_inheritance(layout_name)
        if resolved is None:
            return RenderOutput(
                text="",
                errors=[RenderError(slot_name="", error=f"layout not found: {layout_name}")],
                success=False,
                unfilled_slots=[],
            )

        slot_defs: dict[str, LayoutSlot] = {slot.name: slot for slot in resolved.slots}

        errors: list[RenderError] = []
        unfilled: list[str] = []

        # 1. Render multi-slot blocks first
        def _multi_replacer(match: re.Match[str]) -> str:
            slot_name = match.group(1)
            block = match.group(2)
            value = slot_content.get(slot_name)
            if value is None:
                # Check default in slot definition
                slot_def = slot_defs.get(slot_name)
                if slot_def is not None and slot_def.required and strict:
                    errors.append(
                        RenderError(
                            slot_name=slot_name,
                            error=f"required multi-slot '{slot_name}' is missing",
                        )
                    )
                if slot_name not in unfilled:
                    unfilled.append(slot_name)
                return ""
            if not isinstance(value, list):
                value = [value]
            parts: list[str] = []
            for item in value:
                rendered_block = block
                if isinstance(item, dict):
                    for k, v in item.items():
                        rendered_block = rendered_block.replace(f"{{{{{k}}}}}", str(v))
                else:
                    rendered_block = rendered_block.replace("{{.}}", str(item))
                    rendered_block = rendered_block.replace("{{item}}", str(item))
                parts.append(rendered_block)
            return "".join(parts)

        text = _MULTI_RE.sub(_multi_replacer, resolved.template)

        # 2. Render single slots
        def _slot_replacer(match: re.Match[str]) -> str:
            slot_name = match.group(1)
            inline_default = match.group(2)
            value = slot_content.get(slot_name)
            if value is not None:
                if isinstance(value, list):
                    return "".join(str(x) for x in value)
                return str(value)

            # Fall back to inline default
            if inline_default is not None:
                return inline_default

            # Fall back to slot definition default
            slot_def = slot_defs.get(slot_name)
            if slot_def is not None and slot_def.default:
                return slot_def.default

            # Required check
            if slot_def is not None and slot_def.required:
                err_msg = f"required slot '{slot_name}' is missing"
                errors.append(RenderError(slot_name=slot_name, error=err_msg))
            if slot_name not in unfilled:
                unfilled.append(slot_name)
            return ""

        text = _SLOT_RE.sub(_slot_replacer, text)

        success = len(errors) == 0
        if strict and unfilled:
            # In strict mode, any unfilled slot without a default is a failure
            for slot_name in unfilled:
                if not any(err.slot_name == slot_name for err in errors):
                    errors.append(
                        RenderError(
                            slot_name=slot_name,
                            error=f"unfilled slot '{slot_name}' in strict mode",
                        )
                    )
            success = False

        return RenderOutput(
            text=text,
            errors=errors,
            success=success,
            unfilled_slots=unfilled,
        )
