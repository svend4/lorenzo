"""E373 DocFormatConverter — pluggable format conversion registry.

Public API
----------
:class:`ConversionPath`     — registered conversion route
:class:`ConversionResult`   — outcome of a conversion
:class:`ConverterStats`     — aggregate statistics
:class:`DocFormatConverter` — main interface for format conversion
"""

from .converter import ConversionPath, ConversionResult, ConverterStats, DocFormatConverter

__all__ = ["ConversionPath", "ConversionResult", "ConverterStats", "DocFormatConverter"]
