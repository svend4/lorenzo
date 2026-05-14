"""Notification template engine — pure stdlib."""
from docstoolkit.notif_templates.template import (
    TemplateFormat,
    TemplateVariable,
    NotifTemplate,
)
from docstoolkit.notif_templates.renderer import (
    RenderResult,
    TemplateRenderer,
)
from docstoolkit.notif_templates.registry import TemplateRegistry

__all__ = [
    "TemplateFormat",
    "TemplateVariable",
    "NotifTemplate",
    "RenderResult",
    "TemplateRenderer",
    "TemplateRegistry",
]
