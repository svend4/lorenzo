"""Phase V.3 — Mini DSL for querying a TripleStore.

The DSL parses a tiny pattern grammar and resolves it against a
`TripleStore` (or any object with a `find_triples(...)` method matching
the same signature). Designed for ad-hoc graph exploration without
hauling in a full SPARQL implementation.

Grammar (one triple-pattern per line; variables prefixed with `?`):

    pattern  := term predicate term
    term     := variable | "literal"
    variable := "?" [a-zA-Z_][a-zA-Z0-9_]*
    predicate := IDENT

Multiple lines are AND-joined. Each pattern can be:

    "Python"  uses  ?topic        # subject literal, object var
    ?x        uses  "RAG"         # subject var, object literal
    ?x        uses  ?y            # all uses-triples

Example::

    store = TripleStore(":memory:")
    # ... populate ...

    results = run_query(store, '''
        "Python"  uses     ?topic
        ?topic    mentions ?author
    ''')

    # results = [{"topic": "rag", "author": "alice"}, ...]

The implementation is intentionally minimal: linear pass per pattern,
hash-join on the bound variables. Good enough for graphs up to ~10^5
triples; for larger, swap in a real triple-pattern engine.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class TriplePattern:
    """One parsed line from the DSL."""
    subject: str          # either a variable like "?x" or a literal like "Python"
    predicate: str        # always a literal predicate
    object: str


_PATTERN_RE = re.compile(
    r'^\s*'
    r'(?P<s>"[^"]+"|\?[a-zA-Z_][a-zA-Z0-9_]*)'
    r'\s+'
    r'(?P<p>[a-zA-Z_][a-zA-Z0-9_]*)'
    r'\s+'
    r'(?P<o>"[^"]+"|\?[a-zA-Z_][a-zA-Z0-9_]*)'
    r'\s*$'
)


class QueryParseError(ValueError):
    """Raised when the query string is malformed."""


def parse_query(text: str) -> list[TriplePattern]:
    """Parse a multi-line query string into a list of TriplePattern.

    Empty lines and `#` comments are ignored. Raises QueryParseError on
    any malformed line so the caller learns about typos at parse time.
    """
    patterns: list[TriplePattern] = []
    for line_no, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _PATTERN_RE.match(line)
        if not m:
            raise QueryParseError(
                f"line {line_no}: malformed pattern {raw!r}"
            )
        patterns.append(TriplePattern(
            subject=_strip_quotes(m.group("s")),
            predicate=m.group("p"),
            object=_strip_quotes(m.group("o")),
        ))
    if not patterns:
        raise QueryParseError("query has no patterns")
    return patterns


def _strip_quotes(t: str) -> str:
    """Keep `?x` as-is, strip the wrapping quotes from `"literal"`."""
    if t.startswith('"') and t.endswith('"'):
        return t[1:-1]
    return t


def _is_var(t: str) -> bool:
    return t.startswith("?")


def run_query(store, query_text: str,
              *, limit: int = 1000) -> list[dict[str, str]]:
    """Resolve every variable in the query against `store`.

    Returns a list of bindings dicts: each dict maps variable-name
    (without the leading `?`) to the entity_id it bound to. Empty list
    if no bindings satisfy all patterns.

    Algorithm: greedy hash-join — start with one pattern, get all matching
    triples, then for each subsequent pattern intersect bindings on shared
    variables. Complexity O(N · k) where k is the average matching set size.
    """
    patterns = parse_query(query_text)
    bindings: list[dict[str, str]] = [{}]

    for pat in patterns:
        new_bindings: list[dict[str, str]] = []
        for b in bindings:
            # Bind any already-known variable in the pattern.
            s_filter = _resolve(pat.subject, b)
            o_filter = _resolve(pat.object, b)
            triples = store.find_triples(
                subject=s_filter if not _is_var(pat.subject) else None,
                predicate=pat.predicate,
                object=o_filter if not _is_var(pat.object) else None,
                limit=limit,
            )
            for t in triples:
                # When the subject *is* a variable already bound in b, filter:
                if _is_var(pat.subject):
                    s_var = pat.subject[1:]
                    if s_var in b and b[s_var] != t.subject:
                        continue
                if _is_var(pat.object):
                    o_var = pat.object[1:]
                    if o_var in b and b[o_var] != t.object:
                        continue
                # Build a candidate new binding.
                nb = dict(b)
                if _is_var(pat.subject):
                    nb[pat.subject[1:]] = t.subject
                if _is_var(pat.object):
                    nb[pat.object[1:]] = t.object
                new_bindings.append(nb)
        bindings = new_bindings
        if not bindings:
            break
    return bindings


def _resolve(term: str, binding: dict[str, str]) -> str:
    """If term is a bound variable, return its value; else the term itself."""
    if _is_var(term):
        return binding.get(term[1:], term)
    return term


__all__ = ["TriplePattern", "QueryParseError", "parse_query", "run_query"]
