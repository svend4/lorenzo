"""E122 Document formatter — markdown cleanup, whitespace normalization, heading normalization.

Public API
----------
:class:`FormatRule`      — enum of available formatting rules
:class:`FormatConfig`    — configuration for DocFormatter
:class:`FormatterResult` — result of a single format() call
:class:`DocFormatter`    — main formatter class
"""
from .formatter import DocFormatter, FormatConfig, FormatRule, FormatterResult

__all__ = [
    "DocFormatter",
    "FormatConfig",
    "FormatRule",
    "FormatterResult",
]
