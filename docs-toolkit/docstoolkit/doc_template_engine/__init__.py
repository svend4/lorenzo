"""doc_template_engine — simple {{variable}} string template engine (E290).

Pure stdlib, thread-safe.
"""
from docstoolkit.doc_template_engine.engine import (
    DocTemplateEngine,
    RenderResult,
    Template,
)

__all__ = [
    "DocTemplateEngine",
    "RenderResult",
    "Template",
]
