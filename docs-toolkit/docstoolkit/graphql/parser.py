"""Minimal GraphQL query parser.

Parses a subset of GraphQL query syntax sufficient for field selection and
argument passing:

    {
        ask(query: "hello", top_k: 5) {
            answer
            sources { doc_id score }
        }
        docs(section: "01-svyazi") {
            id
            title
        }
    }

Does NOT support:
* Mutations / subscriptions (use separate endpoints)
* Variables (future extension)
* Directives
* Fragments

Returns a tree of :class:`FieldNode` objects.
Pure stdlib — no external dependencies.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# AST nodes
# ---------------------------------------------------------------------------

@dataclass
class FieldNode:
    """A single selected field in a query."""
    name: str
    alias: Optional[str] = None          # alias: name(...)
    arguments: Dict[str, Any] = field(default_factory=dict)
    selections: List["FieldNode"] = field(default_factory=list)

    @property
    def response_name(self) -> str:
        return self.alias or self.name


@dataclass
class QueryDocument:
    """Top-level parsed query document."""
    selections: List[FieldNode] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

_TOKEN_RE = re.compile(
    r'"(?:[^"\\]|\\.)*"'   # string literal (must come first)
    r'|[{}():,]'           # punctuation
    r'|[A-Za-z_]\w*'      # identifier
    r'|-?\d+(?:\.\d+)?'   # number
    r'|true|false|null',
    re.MULTILINE,
)


def _tokenize(src: str) -> List[str]:
    return _TOKEN_RE.findall(src)


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class ParseError(Exception):
    pass


class _Parser:
    def __init__(self, tokens: List[str]) -> None:
        self._tokens = tokens
        self._pos = 0

    def _peek(self) -> Optional[str]:
        if self._pos < len(self._tokens):
            return self._tokens[self._pos]
        return None

    def _consume(self, expected: Optional[str] = None) -> str:
        tok = self._peek()
        if tok is None:
            raise ParseError("Unexpected end of query")
        if expected is not None and tok != expected:
            raise ParseError(f"Expected {expected!r}, got {tok!r}")
        self._pos += 1
        return tok

    def parse(self) -> QueryDocument:
        self._consume("{")
        selections = self._parse_selection_set_body()
        self._consume("}")
        return QueryDocument(selections=selections)

    def _parse_selection_set_body(self) -> List[FieldNode]:
        nodes = []
        while self._peek() not in (None, "}"):
            nodes.append(self._parse_field())
        return nodes

    def _parse_field(self) -> FieldNode:
        name = self._consume()
        if not re.match(r'[A-Za-z_]\w*', name):
            raise ParseError(f"Expected field name, got {name!r}")

        alias: Optional[str] = None
        # alias: name pattern
        if self._peek() == ":":
            self._consume(":")
            actual_name = self._consume()
            alias, name = name, actual_name

        arguments: Dict[str, Any] = {}
        if self._peek() == "(":
            arguments = self._parse_arguments()

        selections: List[FieldNode] = []
        if self._peek() == "{":
            self._consume("{")
            selections = self._parse_selection_set_body()
            self._consume("}")

        return FieldNode(
            name=name,
            alias=alias,
            arguments=arguments,
            selections=selections,
        )

    def _parse_arguments(self) -> Dict[str, Any]:
        self._consume("(")
        args: Dict[str, Any] = {}
        while self._peek() != ")":
            key = self._consume()
            self._consume(":")
            value = self._parse_value()
            args[key] = value
            if self._peek() == ",":
                self._consume(",")
        self._consume(")")
        return args

    def _parse_value(self) -> Any:
        tok = self._peek()
        if tok is None:
            raise ParseError("Expected value, got end of input")

        if tok == "true":
            self._consume()
            return True
        if tok == "false":
            self._consume()
            return False
        if tok == "null":
            self._consume()
            return None
        if tok.startswith('"'):
            self._consume()
            # Unescape basic escape sequences
            inner = tok[1:-1]
            return inner.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
        if re.match(r'-?\d+\.\d+', tok):
            self._consume()
            return float(tok)
        if re.match(r'-?\d+', tok):
            self._consume()
            return int(tok)
        # identifier (enum value)
        return self._consume()


def parse_query(src: str) -> QueryDocument:
    """Parse a GraphQL query string into a :class:`QueryDocument`.

    Parameters
    ----------
    src:
        GraphQL query source.  Must be wrapped in ``{ ... }``.

    Raises
    ------
    ParseError
        On invalid syntax.
    """
    tokens = _tokenize(src.strip())
    return _Parser(tokens).parse()
