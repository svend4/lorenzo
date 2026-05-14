"""Registry for notification templates."""
from __future__ import annotations

from docstoolkit.notif_templates.renderer import RenderResult, TemplateRenderer
from docstoolkit.notif_templates.template import NotifTemplate


class TemplateRegistry:
    """A simple in-memory store for :class:`NotifTemplate` objects."""

    def __init__(self) -> None:
        self._store: dict[str, NotifTemplate] = {}
        self._renderer = TemplateRenderer()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def register(self, template: NotifTemplate) -> None:
        """Register *template*.

        Raises:
            ValueError: if a template with the same ``template_id`` already exists.
        """
        if template.template_id in self._store:
            raise ValueError(
                f"Template with id {template.template_id!r} is already registered."
            )
        self._store[template.template_id] = template

    def unregister(self, template_id: str) -> bool:
        """Remove the template identified by *template_id*.

        Returns:
            ``True`` if the template existed and was removed, ``False`` otherwise.
        """
        if template_id in self._store:
            del self._store[template_id]
            return True
        return False

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get(self, template_id: str) -> NotifTemplate | None:
        """Return the template with *template_id*, or ``None``."""
        return self._store.get(template_id)

    def get_by_name(self, name: str) -> NotifTemplate | None:
        """Return the first template whose ``name`` matches, or ``None``."""
        for tmpl in self._store.values():
            if tmpl.name == name:
                return tmpl
        return None

    def list_all(self) -> list[NotifTemplate]:
        """Return all registered templates (insertion order)."""
        return list(self._store.values())

    def list_by_tag(self, tag: str) -> list[NotifTemplate]:
        """Return all templates that carry *tag*."""
        return [tmpl for tmpl in self._store.values() if tag in tmpl.tags]

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self, template_id: str, context: dict) -> RenderResult:
        """Render the template identified by *template_id* with *context*.

        Raises:
            KeyError: if no template with *template_id* is registered.
        """
        tmpl = self._store.get(template_id)
        if tmpl is None:
            raise KeyError(f"No template registered with id {template_id!r}.")
        return self._renderer.render(tmpl, context)
