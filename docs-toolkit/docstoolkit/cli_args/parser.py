"""Minimal CLI argument parser (alternative to argparse, with simpler API)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ArgType(Enum):
    """Argument types supported by the parser."""

    STRING = "string"
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    LIST_STRING = "list_string"
    LIST_INT = "list_int"


class ParseError(Exception):
    """Raised by parse_strict when an error occurs during parsing."""


@dataclass
class Argument:
    """Description of one named argument."""

    name: str
    arg_type: ArgType = ArgType.STRING
    required: bool = False
    default: Any = None
    short: Optional[str] = None
    help: str = ""
    choices: Optional[list] = None

    @property
    def is_list(self) -> bool:
        return self.arg_type in (ArgType.LIST_STRING, ArgType.LIST_INT)

    @property
    def is_bool(self) -> bool:
        return self.arg_type == ArgType.BOOL


@dataclass
class ParseResult:
    """Result of CliParser.parse — values, positionals, errors."""

    values: dict = field(default_factory=dict)
    positional: list = field(default_factory=list)
    errors: list = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors

    def get(self, name: str, default: Any = None) -> Any:
        return self.values.get(name, default)


def _coerce_scalar(raw: str, arg_type: ArgType) -> Any:
    """Convert a string into the requested scalar type. Raises ValueError."""
    if arg_type == ArgType.STRING:
        return raw
    if arg_type == ArgType.INT:
        return int(raw)
    if arg_type == ArgType.FLOAT:
        return float(raw)
    if arg_type == ArgType.BOOL:
        low = raw.lower()
        if low in ("true", "1", "yes", "on"):
            return True
        if low in ("false", "0", "no", "off"):
            return False
        raise ValueError(f"invalid bool value: {raw!r}")
    raise ValueError(f"not a scalar type: {arg_type}")


def _coerce_list_item(raw: str, arg_type: ArgType) -> Any:
    if arg_type == ArgType.LIST_INT:
        return int(raw)
    return raw  # LIST_STRING


class CliParser:
    """Simple CLI parser with no auto-exit behavior."""

    def __init__(self, program_name: str = "cli", description: str = "") -> None:
        self.program_name = program_name
        self.description = description
        self._arguments: list[Argument] = []
        self._by_name: dict[str, Argument] = {}
        self._by_short: dict[str, Argument] = {}
        self._positional: list[Argument] = []

    # ------------------------------------------------------------------ setup

    @property
    def argument_count(self) -> int:
        return len(self._arguments) + len(self._positional)

    def add_argument(
        self,
        name: str,
        arg_type: ArgType = ArgType.STRING,
        **kwargs: Any,
    ) -> Argument:
        """Register a named (optional) argument."""
        if not name:
            raise ValueError("argument name must be non-empty")
        if name in self._by_name:
            raise ValueError(f"duplicate argument name: {name}")
        arg = Argument(name=name, arg_type=arg_type, **kwargs)
        if arg.short is not None:
            if arg.short in self._by_short:
                raise ValueError(f"duplicate short option: -{arg.short}")
            self._by_short[arg.short] = arg
        self._arguments.append(arg)
        self._by_name[name] = arg
        return arg

    def add_flag(
        self,
        name: str,
        short: Optional[str] = None,
        help: str = "",
    ) -> Argument:
        """Convenience for adding a boolean flag (default False)."""
        return self.add_argument(
            name,
            arg_type=ArgType.BOOL,
            default=False,
            short=short,
            help=help,
        )

    def add_positional(
        self,
        name: str,
        arg_type: ArgType = ArgType.STRING,
        help: str = "",
    ) -> None:
        """Register a positional argument (consumed in registration order)."""
        if not name:
            raise ValueError("positional name must be non-empty")
        if any(p.name == name for p in self._positional):
            raise ValueError(f"duplicate positional name: {name}")
        if name in self._by_name:
            raise ValueError(f"name collides with named argument: {name}")
        self._positional.append(
            Argument(name=name, arg_type=arg_type, help=help)
        )

    # ------------------------------------------------------------------ parse

    def parse(self, argv: list) -> ParseResult:
        """Parse argv into a ParseResult. Does not raise on errors."""
        result = ParseResult()

        # Seed defaults
        for arg in self._arguments:
            if arg.is_list:
                result.values[arg.name] = list(arg.default) if arg.default else []
            else:
                result.values[arg.name] = arg.default

        seen: set[str] = set()
        extra_positional: list[str] = []

        i = 0
        end_of_opts = False
        while i < len(argv):
            tok = argv[i]

            if end_of_opts:
                extra_positional.append(tok)
                i += 1
                continue

            if tok == "--":
                end_of_opts = True
                i += 1
                continue

            if tok.startswith("--") and len(tok) > 2:
                i = self._handle_long(tok, argv, i, result, seen)
                continue

            if tok.startswith("-") and len(tok) > 1 and tok != "-":
                i = self._handle_short(tok, argv, i, result, seen)
                continue

            extra_positional.append(tok)
            i += 1

        # Assign positionals
        for idx, parg in enumerate(self._positional):
            if idx >= len(extra_positional):
                result.errors.append(f"missing positional argument: {parg.name}")
                continue
            raw = extra_positional[idx]
            try:
                if parg.is_list:
                    result.values[parg.name] = [
                        _coerce_list_item(p, parg.arg_type)
                        for p in raw.split(",")
                        if p != ""
                    ]
                else:
                    result.values[parg.name] = _coerce_scalar(raw, parg.arg_type)
            except ValueError as exc:
                result.errors.append(
                    f"invalid value for positional {parg.name!r}: {exc}"
                )

        # Anything beyond declared positionals goes to result.positional
        if len(extra_positional) > len(self._positional):
            result.positional = extra_positional[len(self._positional):]
        else:
            result.positional = []

        # Validate required + choices
        for arg in self._arguments:
            if arg.required and arg.name not in seen:
                result.errors.append(f"missing required argument: --{arg.name}")
            if arg.choices is not None and arg.name in seen:
                val = result.values[arg.name]
                vals = val if arg.is_list else [val]
                for v in vals:
                    if v not in arg.choices:
                        result.errors.append(
                            f"invalid choice for --{arg.name}: {v!r} "
                            f"(choose from {arg.choices})"
                        )

        return result

    def parse_strict(self, argv: list) -> dict:
        """Parse argv and raise ParseError on any error; return values dict."""
        result = self.parse(argv)
        if not result.is_valid:
            raise ParseError("; ".join(result.errors))
        return result.values

    # ------------------------------------------------- internal token handling

    def _handle_long(
        self,
        tok: str,
        argv: list,
        i: int,
        result: ParseResult,
        seen: set,
    ) -> int:
        body = tok[2:]
        if "=" in body:
            name, _, value = body.partition("=")
            has_value = True
        else:
            name = body
            value = None
            has_value = False

        # Handle --no-<name> negation for bool args
        if not has_value and name.startswith("no-"):
            base = name[3:]
            if base in self._by_name and self._by_name[base].is_bool:
                arg = self._by_name[base]
                result.values[arg.name] = False
                seen.add(arg.name)
                return i + 1

        if name not in self._by_name:
            result.errors.append(f"unknown option: --{name}")
            return i + 1

        arg = self._by_name[name]

        if arg.is_bool:
            if has_value:
                try:
                    result.values[arg.name] = _coerce_scalar(value, ArgType.BOOL)
                except ValueError as exc:
                    result.errors.append(
                        f"invalid value for --{arg.name}: {exc}"
                    )
            else:
                result.values[arg.name] = True
            seen.add(arg.name)
            return i + 1

        # Non-bool needs a value
        if not has_value:
            if i + 1 >= len(argv):
                result.errors.append(f"option --{arg.name} requires a value")
                return i + 1
            value = argv[i + 1]
            consumed = 2
        else:
            consumed = 1

        self._store_value(arg, value, result)
        seen.add(arg.name)
        return i + consumed

    def _handle_short(
        self,
        tok: str,
        argv: list,
        i: int,
        result: ParseResult,
        seen: set,
    ) -> int:
        body = tok[1:]  # strip leading '-'

        # Single short option, possibly followed by a value
        first = body[0]
        rest = body[1:]

        if first not in self._by_short:
            result.errors.append(f"unknown short option: -{first}")
            return i + 1

        arg = self._by_short[first]

        if arg.is_bool:
            # Combined flags only for bool: -abc => -a -b -c (all bool)
            if rest == "":
                result.values[arg.name] = True
                seen.add(arg.name)
                return i + 1
            # All characters must be bool short options
            chars = [first] + list(rest)
            all_bool = True
            for ch in chars:
                if ch not in self._by_short or not self._by_short[ch].is_bool:
                    all_bool = False
                    break
            if all_bool:
                for ch in chars:
                    a = self._by_short[ch]
                    result.values[a.name] = True
                    seen.add(a.name)
                return i + 1
            # Not combinable — treat rest as value? Bool with rest: error.
            result.errors.append(
                f"short option -{first} is a flag and cannot take inline value"
            )
            return i + 1

        # Non-bool: value may be glued (-nVALUE) or next token (-n VALUE)
        if rest:
            value = rest
            consumed = 1
        else:
            if i + 1 >= len(argv):
                result.errors.append(f"option -{first} requires a value")
                return i + 1
            value = argv[i + 1]
            consumed = 2

        self._store_value(arg, value, result)
        seen.add(arg.name)
        return i + consumed

    def _store_value(self, arg: Argument, raw: str, result: ParseResult) -> None:
        if arg.is_list:
            parts = [p for p in raw.split(",") if p != ""]
            try:
                coerced = [_coerce_list_item(p, arg.arg_type) for p in parts]
            except ValueError as exc:
                result.errors.append(
                    f"invalid value for --{arg.name}: {exc}"
                )
                return
            # Append to existing list (supports --items a --items b)
            existing = result.values.get(arg.name) or []
            if not isinstance(existing, list):
                existing = []
            existing.extend(coerced)
            result.values[arg.name] = existing
            return

        try:
            result.values[arg.name] = _coerce_scalar(raw, arg.arg_type)
        except ValueError as exc:
            result.errors.append(f"invalid value for --{arg.name}: {exc}")

    # ------------------------------------------------------------------ help

    def format_usage(self) -> str:
        parts = [f"usage: {self.program_name}"]
        for arg in self._arguments:
            stub = f"--{arg.name}"
            if not arg.is_bool:
                stub += f" <{arg.arg_type.value}>"
            parts.append(f"[{stub}]" if not arg.required else stub)
        for parg in self._positional:
            parts.append(f"<{parg.name}>")
        return " ".join(parts)

    def format_help(self) -> str:
        lines = [self.format_usage()]
        if self.description:
            lines.append("")
            lines.append(self.description)
        if self._arguments:
            lines.append("")
            lines.append("options:")
            for arg in self._arguments:
                short = f"-{arg.short}, " if arg.short else ""
                name = f"--{arg.name}"
                ty = "" if arg.is_bool else f" <{arg.arg_type.value}>"
                req = " (required)" if arg.required else ""
                dflt = (
                    f" [default: {arg.default}]"
                    if arg.default is not None and not arg.required
                    else ""
                )
                ch = f" choices={arg.choices}" if arg.choices else ""
                help_text = f"  {help_pad(short + name + ty)}{arg.help}{req}{dflt}{ch}"
                lines.append(help_text)
        if self._positional:
            lines.append("")
            lines.append("positional:")
            for parg in self._positional:
                lines.append(
                    f"  {help_pad(parg.name)}{parg.help} <{parg.arg_type.value}>"
                )
        return "\n".join(lines)


def help_pad(s: str, width: int = 28) -> str:
    if len(s) >= width:
        return s + "  "
    return s + " " * (width - len(s))
