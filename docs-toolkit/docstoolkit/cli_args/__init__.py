"""cli_args — minimal CLI argument parser without argparse.

Provides:
- ArgType: enum of supported argument types
- Argument: declarative description of one argument
- ParseResult: outcome of parsing (values, positional, errors)
- ParseError: exception raised by parse_strict
- CliParser: the parser itself
"""

from docstoolkit.cli_args.parser import (
    ArgType,
    Argument,
    CliParser,
    ParseError,
    ParseResult,
)

__all__ = [
    "ArgType",
    "Argument",
    "CliParser",
    "ParseError",
    "ParseResult",
]
