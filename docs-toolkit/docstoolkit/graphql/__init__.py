"""GraphQL-lite: a pure-stdlib schema definition and query execution layer.

Provides a lightweight GraphQL-inspired API without the ``graphql-core``
dependency.  Supports:

* Type system (scalars, objects, lists, non-null)
* Schema definition via Python decorators
* Query parsing (field selection, arguments, aliases)
* Resolver execution with context propagation
* Error collection (partial results)

Not a full GraphQL implementation — subscriptions and directives are out
of scope for the stdlib-only target.

Usage::

    from docstoolkit.graphql import Schema, field, ObjectType

    @ObjectType
    class Query:
        @field(description="Ask a question")
        def ask(root, info, query: str, top_k: int = 5):
            return {"answer": "...", "sources": []}

    schema = Schema(query=Query)
    result = schema.execute("{ ask(query: \\"hello\\") { answer } }")
"""
from docstoolkit.graphql.types import (
    ScalarType, ObjectType, ListType, NonNull,
    FieldDefinition, field,
    GraphQLString, GraphQLInt, GraphQLFloat, GraphQLBoolean,
)
from docstoolkit.graphql.schema import Schema
from docstoolkit.graphql.executor import ExecutionResult

__all__ = [
    "ScalarType", "ObjectType", "ListType", "NonNull",
    "FieldDefinition", "field",
    "GraphQLString", "GraphQLInt", "GraphQLFloat", "GraphQLBoolean",
    "Schema",
    "ExecutionResult",
]
