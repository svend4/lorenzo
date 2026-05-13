"""URL pattern matching and routing with named parameters.

Pattern syntax:
- Static parts: ``/users`` matches exactly ``/users``.
- Named parameters: ``/users/{id}`` captures ``id``.
- Typed parameters: ``/users/{id:int}`` requires integer characters
  (value still stored as ``str``).
- Wildcard tail: ``/files/*path`` captures the remainder of the path.

Trailing slashes are matched leniently — ``/users`` and ``/users/`` are
considered equivalent for the purposes of matching.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Pattern, Tuple


# Tokens inside a pattern:
#   {name}         → named parameter
#   {name:type}    → typed named parameter
#   *name          → wildcard tail
_PARAM_RE = re.compile(r"\{(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?::(?P<type>[A-Za-z_]+))?\}")
_WILDCARD_RE = re.compile(r"\*(?P<name>[A-Za-z_][A-Za-z0-9_]*)")

# Mapping of named types → regex fragments.
_TYPE_PATTERNS = {
    "int": r"\d+",
    "str": r"[^/]+",
    "slug": r"[A-Za-z0-9_\-]+",
}


@dataclass
class Route:
    """A single registered route."""

    pattern: str
    handler: Callable
    methods: List[str] = field(default_factory=lambda: ["GET"])
    name: Optional[str] = None
    priority: int = 0
    # Filled by ``__post_init__``.
    regex: Pattern = field(init=False, repr=False, compare=False)
    param_names: List[str] = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        # Normalize methods to upper-case for case-insensitive matching.
        self.methods = [m.upper() for m in self.methods]
        self.regex, self.param_names = _compile_pattern(self.pattern)

    def matches_method(self, method: str) -> bool:
        return method.upper() in self.methods

    def match_path(self, path: str) -> Optional[Dict[str, str]]:
        """Return captured params if ``path`` matches, else ``None``."""
        normalized = _normalize_path(path)
        m = self.regex.match(normalized)
        if m is None:
            return None
        return dict(m.groupdict())


@dataclass
class RouteMatch:
    """Result of matching a path against a route."""

    route: Route
    params: Dict[str, str]
    method: str
    path: str


# ---------------------------------------------------------------------------
# Pattern compilation
# ---------------------------------------------------------------------------


def _normalize_path(path: str) -> str:
    """Strip a single trailing slash unless the path is exactly ``/``."""
    if len(path) > 1 and path.endswith("/"):
        return path[:-1]
    return path


def _compile_pattern(pattern: str) -> Tuple[Pattern, List[str]]:
    """Compile a pattern string into a regex plus an ordered param list."""
    # Walk through the pattern building a regex piece by piece. Anything that
    # isn't a parameter or wildcard token is treated as a literal.
    normalized = _normalize_path(pattern)
    result: List[str] = []
    param_names: List[str] = []
    i = 0
    while i < len(normalized):
        ch = normalized[i]
        if ch == "{":
            m = _PARAM_RE.match(normalized, i)
            if not m:
                raise ValueError(f"Invalid parameter in pattern: {pattern!r}")
            name = m.group("name")
            typ = m.group("type") or "str"
            if name in param_names:
                raise ValueError(f"Duplicate parameter name {name!r} in pattern {pattern!r}")
            type_re = _TYPE_PATTERNS.get(typ, r"[^/]+")
            result.append(f"(?P<{name}>{type_re})")
            param_names.append(name)
            i = m.end()
        elif ch == "*":
            m = _WILDCARD_RE.match(normalized, i)
            if not m:
                raise ValueError(f"Invalid wildcard in pattern: {pattern!r}")
            name = m.group("name")
            if name in param_names:
                raise ValueError(f"Duplicate parameter name {name!r} in pattern {pattern!r}")
            result.append(f"(?P<{name}>.+)")
            param_names.append(name)
            i = m.end()
        else:
            # Escape a single literal character so regex metacharacters in the
            # pattern (``.``, ``+``, ``?`` …) do not change meaning.
            result.append(re.escape(ch))
            i += 1

    regex = re.compile("^" + "".join(result) + "$")
    return regex, param_names


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------


class UrlRouter:
    """A simple URL router with named parameters and reverse routing."""

    def __init__(self) -> None:
        self._routes: List[Route] = []

    # ------------------------------------------------------------------ add
    def add_route(
        self,
        pattern: str,
        handler: Callable,
        methods: Optional[List[str]] = None,
        name: Optional[str] = None,
        priority: int = 0,
    ) -> Route:
        if methods is None:
            methods = ["GET"]
        route = Route(
            pattern=pattern,
            handler=handler,
            methods=list(methods),
            name=name,
            priority=priority,
        )
        self._routes.append(route)
        # Sort by priority desc so iteration order matches match precedence.
        self._routes.sort(key=lambda r: r.priority, reverse=True)
        return route

    def get(self, pattern: str, handler: Callable, name: Optional[str] = None) -> Route:
        return self.add_route(pattern, handler, methods=["GET"], name=name)

    def post(self, pattern: str, handler: Callable, name: Optional[str] = None) -> Route:
        return self.add_route(pattern, handler, methods=["POST"], name=name)

    def put(self, pattern: str, handler: Callable, name: Optional[str] = None) -> Route:
        return self.add_route(pattern, handler, methods=["PUT"], name=name)

    def delete(self, pattern: str, handler: Callable, name: Optional[str] = None) -> Route:
        return self.add_route(pattern, handler, methods=["DELETE"], name=name)

    # ----------------------------------------------------------------- match
    def match(self, path: str, method: str = "GET") -> Optional[RouteMatch]:
        method_u = method.upper()
        for route in self._routes:
            if not route.matches_method(method_u):
                continue
            params = route.match_path(path)
            if params is not None:
                return RouteMatch(route=route, params=params, method=method_u, path=path)
        return None

    def match_all(self, path: str) -> List[RouteMatch]:
        matches: List[RouteMatch] = []
        for route in self._routes:
            params = route.match_path(path)
            if params is not None:
                # Use the first method as a representative entry per route.
                method = route.methods[0] if route.methods else "GET"
                matches.append(RouteMatch(route=route, params=params, method=method, path=path))
        return matches

    # -------------------------------------------------------------- dispatch
    def dispatch(self, path: str, method: str = "GET", **extra: Any) -> Any:
        m = self.match(path, method)
        if m is None:
            raise LookupError(f"No route matches {method} {path}")
        kwargs = dict(m.params)
        kwargs.update(extra)
        return m.route.handler(**kwargs)

    # --------------------------------------------------------------- url_for
    def url_for(self, name: str, **params: Any) -> str:
        for route in self._routes:
            if route.name == name:
                return _fill_pattern(route.pattern, params)
        raise KeyError(f"No route named {name!r}")

    # --------------------------------------------------------------- manage
    def remove_route(self, pattern: str) -> bool:
        for i, route in enumerate(self._routes):
            if route.pattern == pattern:
                del self._routes[i]
                return True
        return False

    @property
    def route_count(self) -> int:
        return len(self._routes)

    def clear(self) -> None:
        self._routes.clear()

    def list_routes(self) -> List[Route]:
        return sorted(self._routes, key=lambda r: r.priority, reverse=True)


def _fill_pattern(pattern: str, params: Dict[str, Any]) -> str:
    """Substitute ``{name}`` / ``{name:type}`` / ``*name`` tokens with values."""
    used: set = set()

    def repl_param(m: re.Match) -> str:
        name = m.group("name")
        if name not in params:
            raise KeyError(f"Missing parameter {name!r} for url_for")
        used.add(name)
        return str(params[name])

    def repl_wild(m: re.Match) -> str:
        name = m.group("name")
        if name not in params:
            raise KeyError(f"Missing parameter {name!r} for url_for")
        used.add(name)
        return str(params[name])

    result = _PARAM_RE.sub(repl_param, pattern)
    result = _WILDCARD_RE.sub(repl_wild, result)
    return result
