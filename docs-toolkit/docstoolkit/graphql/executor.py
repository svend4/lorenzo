"""Query executor for docstoolkit GraphQL-lite.

Traverses the parsed :class:`QueryDocument` and calls resolver functions
registered on the :class:`Schema`, collecting results and errors.

Pure stdlib — no external dependencies.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from docstoolkit.graphql.parser import FieldNode, QueryDocument
from docstoolkit.graphql.types import ResolveInfo


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class GraphQLError:
    message: str
    path: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"message": self.message, "path": self.path}


@dataclass
class ExecutionResult:
    """Result of executing a query against a :class:`Schema`."""
    data: Optional[Dict[str, Any]] = None
    errors: List[GraphQLError] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict:
        result: dict = {}
        if self.data is not None:
            result["data"] = self.data
        if self.errors:
            result["errors"] = [e.to_dict() for e in self.errors]
        return result


# ---------------------------------------------------------------------------
# Executor
# ---------------------------------------------------------------------------

class Executor:
    """Executes a :class:`QueryDocument` against resolver definitions.

    Parameters
    ----------
    schema:
        The :class:`~docstoolkit.graphql.schema.Schema` to resolve against.
    context:
        Optional request-level context (user, db connection, etc.) passed to
        every resolver.
    """

    def __init__(self, schema, context: Any = None) -> None:
        self._schema = schema
        self._context = context

    def execute(self, document: QueryDocument) -> ExecutionResult:
        """Execute *document* against the schema and return an :class:`ExecutionResult`."""
        data: Dict[str, Any] = {}
        errors: List[GraphQLError] = []

        for selection in document.selections:
            self._resolve_field(
                selection=selection,
                parent=None,
                type_class=self._schema.query_type,
                result=data,
                errors=errors,
                path=[],
            )

        return ExecutionResult(data=data, errors=errors)

    def _resolve_field(
        self,
        selection: FieldNode,
        parent: Any,
        type_class,
        result: dict,
        errors: List[GraphQLError],
        path: List[str],
    ) -> None:
        field_name = selection.name
        response_key = selection.response_name
        current_path = path + [response_key]

        # Look up field definition on the type
        field_def = getattr(type_class, "_gql_fields", {}).get(field_name)
        if field_def is None:
            errors.append(GraphQLError(
                message=f"Field '{field_name}' does not exist on type '{type_class.__name__}'",
                path=current_path,
            ))
            result[response_key] = None
            return

        info = ResolveInfo(
            field_name=field_name,
            schema=self._schema,
            context=self._context,
        )

        # Merge query arguments with field defaults
        kwargs = dict(field_def.args)
        kwargs.update(selection.arguments)

        # Execute resolver
        try:
            value = field_def.resolve(parent, info, **kwargs)
        except Exception as exc:
            errors.append(GraphQLError(
                message=str(exc),
                path=current_path,
            ))
            result[response_key] = None
            return

        # If sub-selections exist, resolve them recursively
        if selection.selections:
            if value is None:
                result[response_key] = None
            elif isinstance(value, list):
                result[response_key] = [
                    self._resolve_object(item, selection.selections, errors, current_path + [str(i)])
                    for i, item in enumerate(value)
                ]
            elif isinstance(value, dict):
                sub: dict = {}
                self._resolve_dict_selections(value, selection.selections, sub, errors, current_path)
                result[response_key] = sub
            else:
                result[response_key] = value
        else:
            result[response_key] = value

    def _resolve_object(self, obj: Any, selections: list, errors: list, path: list) -> Any:
        if obj is None:
            return None
        sub: dict = {}
        if isinstance(obj, dict):
            self._resolve_dict_selections(obj, selections, sub, errors, path)
        else:
            self._resolve_dict_selections(vars(obj) if hasattr(obj, "__dict__") else {}, selections, sub, errors, path)
        return sub

    def _resolve_dict_selections(self, obj: dict, selections: list, result: dict, errors: list, path: list) -> None:
        for sel in selections:
            key = sel.response_name
            if sel.name in obj:
                value = obj[sel.name]
                if sel.selections:
                    if isinstance(value, list):
                        result[key] = [
                            self._resolve_object(item, sel.selections, errors, path + [key, str(i)])
                            for i, item in enumerate(value)
                        ]
                    elif isinstance(value, dict):
                        sub: dict = {}
                        self._resolve_dict_selections(value, sel.selections, sub, errors, path + [key])
                        result[key] = sub
                    else:
                        result[key] = value
                else:
                    result[key] = value
            else:
                result[key] = None
