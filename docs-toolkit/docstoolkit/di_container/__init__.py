"""Dependency injection container for docs-toolkit."""
from docstoolkit.di_container.binding import Binding, BindingScope
from docstoolkit.di_container.container import DIContainer
from docstoolkit.di_container.decorators import inject, injectable, singleton

__all__ = [
    "Binding",
    "BindingScope",
    "DIContainer",
    "inject",
    "injectable",
    "singleton",
]
