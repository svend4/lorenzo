"""Type system for docstoolkit GraphQL-lite.

Defines scalar types, object types, list wrappers and non-null markers — the
minimal set needed to describe a schema and validate resolver return types.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Type


# ---------------------------------------------------------------------------
# Scalars
# ---------------------------------------------------------------------------

class ScalarType:
    """A leaf value type (String, Int, Float, Boolean, ID)."""

    def __init__(self, name: str, serialize=None, parse=None) -> None:
        self.name = name
        self._serialize = serialize or (lambda v: v)
        self._parse = parse or (lambda v: v)

    def serialize(self, value: Any) -> Any:
        return self._serialize(value)

    def parse(self, value: Any) -> Any:
        return self._parse(value)

    def __repr__(self) -> str:
        return f"ScalarType({self.name!r})"


GraphQLString = ScalarType("String", serialize=str, parse=str)
GraphQLInt = ScalarType("Int", serialize=int, parse=int)
GraphQLFloat = ScalarType("Float", serialize=float, parse=float)
GraphQLBoolean = ScalarType("Boolean", serialize=bool, parse=bool)
GraphQLID = ScalarType("ID", serialize=str, parse=str)


# ---------------------------------------------------------------------------
# Wrappers
# ---------------------------------------------------------------------------

class ListType:
    """Wrapper: [T]"""
    def __init__(self, of_type) -> None:
        self.of_type = of_type

    def __repr__(self) -> str:
        return f"[{self.of_type!r}]"


class NonNull:
    """Wrapper: T!"""
    def __init__(self, of_type) -> None:
        self.of_type = of_type

    def __repr__(self) -> str:
        return f"{self.of_type!r}!"


# ---------------------------------------------------------------------------
# Field definition
# ---------------------------------------------------------------------------

@dataclass
class FieldDefinition:
    """Metadata + resolver for a single field on an object type."""
    name: str
    resolver: Callable
    return_type: Any = None
    description: str = ""
    args: Dict[str, Any] = field(default_factory=dict)   # name → default value

    def resolve(self, root: Any, info: "ResolveInfo", **kwargs) -> Any:
        return self.resolver(root, info, **kwargs)


def field(
    return_type: Any = None,
    description: str = "",
    **arg_defaults,
) -> Callable:
    """Decorator that marks a method as a GraphQL field resolver.

    Usage::

        @ObjectType
        class Query:
            @field(return_type=GraphQLString, description="greeting")
            def hello(root, info, name: str = "world"):
                return f"Hello, {name}!"
    """
    def decorator(fn: Callable) -> Callable:
        fn._gql_field = True
        fn._gql_return_type = return_type
        fn._gql_description = description
        return fn
    return decorator


# ---------------------------------------------------------------------------
# ObjectType
# ---------------------------------------------------------------------------

class _ObjectTypeMeta(type):
    """Metaclass that scans a class for @field-decorated methods."""

    def __new__(mcs, name: str, bases: tuple, namespace: dict):
        fields: Dict[str, FieldDefinition] = {}
        for attr_name, obj in namespace.items():
            if callable(obj) and getattr(obj, "_gql_field", False):
                sig = inspect.signature(obj)
                args = {}
                params = list(sig.parameters.values())
                # Skip 'root' and 'info' positional args
                for p in params[2:]:
                    args[p.name] = (
                        p.default if p.default is not inspect.Parameter.empty else None
                    )
                fields[attr_name] = FieldDefinition(
                    name=attr_name,
                    resolver=obj,
                    return_type=getattr(obj, "_gql_return_type", None),
                    description=getattr(obj, "_gql_description", ""),
                    args=args,
                )
        cls = super().__new__(mcs, name, bases, namespace)
        cls._gql_fields = fields
        return cls


class ObjectType(metaclass=_ObjectTypeMeta):
    """Base class for GraphQL-lite object types.

    Subclass and decorate methods with :func:`field`::

        class Query(ObjectType):
            @field(return_type=GraphQLString)
            def hello(root, info, name: str = "world"):
                return f"Hello, {name}!"
    """


# ---------------------------------------------------------------------------
# ResolveInfo (context object passed to resolvers)
# ---------------------------------------------------------------------------

@dataclass
class ResolveInfo:
    """Context passed to every resolver during execution."""
    field_name: str
    schema: Any          # back-reference to Schema
    context: Any = None  # request-level context (e.g. user, db)
