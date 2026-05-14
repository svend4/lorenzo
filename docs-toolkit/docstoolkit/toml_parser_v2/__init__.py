"""toml_parser_v2 — minimal TOML 1.0 subset parser/serializer (stdlib-only)."""
from docstoolkit.toml_parser_v2.parser import (
    ParseError,
    TomlParser,
)

__all__ = [
    "ParseError",
    "TomlParser",
]
