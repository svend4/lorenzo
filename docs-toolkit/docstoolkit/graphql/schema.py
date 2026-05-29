"""Schema entry point for docstoolkit GraphQL-lite.

Binds a query type (and optional mutation type) to an executor and provides
the top-level ``execute()`` method.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

from typing import Any, Optional

from docstoolkit.graphql.executor import ExecutionResult, Executor
from docstoolkit.graphql.parser import ParseError, parse_query


class Schema:
    """A GraphQL-lite schema with an optional context factory.

    Parameters
    ----------
    query:
        An :class:`~docstoolkit.graphql.types.ObjectType` subclass (or class)
        whose ``@field``-decorated methods are the root query resolvers.
    context:
        Static context object passed to every resolver.  For dynamic context
        (per-request), pass ``None`` here and supply it via
        ``execute(context=...)``.
    """

    def __init__(self, query, context: Any = None) -> None:
        self.query_type = query
        self._default_context = context

    def execute(
        self,
        query: str,
        context: Any = None,
    ) -> ExecutionResult:
        """Parse and execute a GraphQL query string.

        Parameters
        ----------
        query:
            GraphQL query source, e.g. ``'{ hello(name: "world") }'``.
        context:
            Per-call context object.  If provided, overrides the default
            context set in the :class:`Schema` constructor.

        Returns
        -------
        :class:`~docstoolkit.graphql.executor.ExecutionResult`
        """
        ctx = context if context is not None else self._default_context
        try:
            document = parse_query(query)
        except ParseError as exc:
            from docstoolkit.graphql.executor import GraphQLError
            return ExecutionResult(
                data=None,
                errors=[GraphQLError(message=f"Parse error: {exc}")],
            )

        executor = Executor(schema=self, context=ctx)
        return executor.execute(document)

    def to_sdl(self) -> str:
        """Return a minimal Schema Definition Language representation."""
        lines = ["type Query {"]
        for name, fd in getattr(self.query_type, "_gql_fields", {}).items():
            arg_parts = []
            for arg_name, default in fd.args.items():
                if default is None:
                    arg_parts.append(f"{arg_name}: String")
                elif isinstance(default, bool):
                    arg_parts.append(f"{arg_name}: Boolean = {str(default).lower()}")
                elif isinstance(default, int):
                    arg_parts.append(f"{arg_name}: Int = {default}")
                elif isinstance(default, float):
                    arg_parts.append(f"{arg_name}: Float = {default}")
                else:
                    arg_parts.append(f"{arg_name}: String = \"{default}\"")

            args_str = f"({', '.join(arg_parts)})" if arg_parts else ""
            return_type = fd.return_type or "String"
            if hasattr(return_type, "name"):
                return_type = return_type.name
            desc = f"  # {fd.description}" if fd.description else ""
            lines.append(f"  {name}{args_str}: {return_type}{desc}")
        lines.append("}")
        return "\n".join(lines)
