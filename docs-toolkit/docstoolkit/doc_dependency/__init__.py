"""Document dependency declaration and resolution with cycle detection."""
from docstoolkit.doc_dependency.dependency import (
    Dependency,
    DependencyGraph,
    DependencyType,
    DocDependency,
    ResolveResult,
)

__all__ = [
    "Dependency",
    "DependencyGraph",
    "DependencyType",
    "DocDependency",
    "ResolveResult",
]
