"""Tests for docstoolkit.graphql — GraphQL-lite query layer."""
from __future__ import annotations

import pytest

from docstoolkit.graphql import (
    Schema, ExecutionResult, ObjectType,
    field, GraphQLString, GraphQLInt, GraphQLBoolean,
)
from docstoolkit.graphql.parser import parse_query, ParseError, FieldNode, QueryDocument
from docstoolkit.graphql.types import ListType, NonNull, ScalarType


# ===========================================================================
# Type system
# ===========================================================================

class TestScalarType:
    def test_name(self):
        assert GraphQLString.name == "String"

    def test_serialize_string(self):
        assert GraphQLString.serialize(42) == "42"

    def test_parse_int(self):
        assert GraphQLInt.parse("5") == 5

    def test_parse_bool(self):
        assert GraphQLBoolean.parse(1) is True

    def test_repr(self):
        assert "String" in repr(GraphQLString)


class TestListType:
    def test_of_type(self):
        lt = ListType(GraphQLString)
        assert lt.of_type is GraphQLString

    def test_repr(self):
        lt = ListType(GraphQLString)
        assert "String" in repr(lt)


class TestNonNull:
    def test_of_type(self):
        nn = NonNull(GraphQLInt)
        assert nn.of_type is GraphQLInt


# ===========================================================================
# Parser
# ===========================================================================

class TestParser:
    def test_simple_field(self):
        doc = parse_query("{ hello }")
        assert len(doc.selections) == 1
        assert doc.selections[0].name == "hello"

    def test_multiple_fields(self):
        doc = parse_query("{ hello goodbye }")
        assert len(doc.selections) == 2

    def test_string_argument(self):
        doc = parse_query('{ greet(name: "Alice") }')
        assert doc.selections[0].arguments["name"] == "Alice"

    def test_int_argument(self):
        doc = parse_query("{ search(top_k: 5) }")
        assert doc.selections[0].arguments["top_k"] == 5

    def test_float_argument(self):
        doc = parse_query("{ filter(threshold: 0.85) }")
        assert doc.selections[0].arguments["threshold"] == pytest.approx(0.85)

    def test_bool_argument_true(self):
        doc = parse_query("{ search(verbose: true) }")
        assert doc.selections[0].arguments["verbose"] is True

    def test_bool_argument_false(self):
        doc = parse_query("{ search(strict: false) }")
        assert doc.selections[0].arguments["strict"] is False

    def test_null_argument(self):
        doc = parse_query("{ search(cursor: null) }")
        assert doc.selections[0].arguments["cursor"] is None

    def test_nested_selection(self):
        doc = parse_query("{ ask { answer sources } }")
        sel = doc.selections[0]
        assert sel.name == "ask"
        sub_names = [s.name for s in sel.selections]
        assert "answer" in sub_names
        assert "sources" in sub_names

    def test_deeply_nested(self):
        doc = parse_query("{ ask { sources { doc_id score } } }")
        ask = doc.selections[0]
        sources = ask.selections[0]
        assert sources.name == "sources"
        sub = [s.name for s in sources.selections]
        assert "doc_id" in sub

    def test_alias(self):
        doc = parse_query("{ myAlias: hello }")
        sel = doc.selections[0]
        assert sel.alias == "myAlias"
        assert sel.name == "hello"
        assert sel.response_name == "myAlias"

    def test_multiple_arguments(self):
        doc = parse_query('{ search(query: "agent", top_k: 3) }')
        args = doc.selections[0].arguments
        assert args["query"] == "agent"
        assert args["top_k"] == 3

    def test_parse_error_missing_brace(self):
        with pytest.raises(ParseError):
            parse_query("{ hello")

    def test_parse_empty_selection(self):
        doc = parse_query("{}")
        assert doc.selections == []

    def test_returns_query_document(self):
        doc = parse_query("{ hello }")
        assert isinstance(doc, QueryDocument)


# ===========================================================================
# Schema + Executor
# ===========================================================================

class TestSchemaBasic:
    def _make_schema(self):
        class Query(ObjectType):
            @field(return_type=GraphQLString, description="Say hello")
            def hello(root, info, name: str = "world"):
                return f"Hello, {name}!"

            @field(return_type=GraphQLInt)
            def add(root, info, a: int = 0, b: int = 0):
                return a + b

        return Schema(query=Query)

    def test_simple_field_resolved(self):
        schema = self._make_schema()
        result = schema.execute("{ hello }")
        assert result.ok
        assert result.data["hello"] == "Hello, world!"

    def test_argument_passed(self):
        schema = self._make_schema()
        result = schema.execute('{ hello(name: "Alice") }')
        assert result.data["hello"] == "Hello, Alice!"

    def test_int_resolver(self):
        schema = self._make_schema()
        result = schema.execute("{ add(a: 3, b: 4) }")
        assert result.data["add"] == 7

    def test_unknown_field_returns_error(self):
        schema = self._make_schema()
        result = schema.execute("{ nonexistent }")
        assert not result.ok
        assert result.data.get("nonexistent") is None

    def test_execution_result_to_dict(self):
        schema = self._make_schema()
        result = schema.execute("{ hello }")
        d = result.to_dict()
        assert "data" in d
        assert d["data"]["hello"] == "Hello, world!"


class TestSchemaErrors:
    def test_parse_error_captured(self):
        class Query(ObjectType):
            @field()
            def hello(root, info):
                return "hi"

        schema = Schema(query=Query)
        result = schema.execute("{ hello")   # missing }
        assert not result.ok
        assert any("Parse error" in e.message for e in result.errors)

    def test_resolver_exception_captured(self):
        class Query(ObjectType):
            @field()
            def boom(root, info):
                raise ValueError("intentional failure")

        schema = Schema(query=Query)
        result = schema.execute("{ boom }")
        assert not result.ok
        assert result.data.get("boom") is None
        assert any("intentional failure" in e.message for e in result.errors)


class TestSchemaNestedObjects:
    def _make_schema(self):
        class Query(ObjectType):
            @field()
            def doc(root, info, id: str = "1"):
                return {"id": id, "title": "My Doc", "score": 0.9}

            @field()
            def docs(root, info, section: str = ""):
                return [
                    {"id": "a", "title": "Alpha"},
                    {"id": "b", "title": "Beta"},
                ]

        return Schema(query=Query)

    def test_nested_selection_on_dict(self):
        schema = self._make_schema()
        result = schema.execute('{ doc(id: "1") { id title } }')
        assert result.ok
        assert result.data["doc"]["id"] == "1"
        assert result.data["doc"]["title"] == "My Doc"

    def test_unrequested_field_not_returned(self):
        schema = self._make_schema()
        result = schema.execute('{ doc(id: "1") { title } }')
        assert "id" not in result.data["doc"]

    def test_list_field_selection(self):
        schema = self._make_schema()
        result = schema.execute('{ docs { id title } }')
        assert result.ok
        items = result.data["docs"]
        assert len(items) == 2
        assert items[0]["id"] == "a"

    def test_alias_in_result(self):
        schema = self._make_schema()
        result = schema.execute('{ myDoc: doc(id: "42") { id } }')
        assert result.ok
        assert "myDoc" in result.data
        assert result.data["myDoc"]["id"] == "42"


class TestSchemaContext:
    def test_context_passed_to_resolver(self):
        class Query(ObjectType):
            @field()
            def whoami(root, info):
                return info.context.get("user", "anonymous")

        schema = Schema(query=Query)
        result = schema.execute("{ whoami }", context={"user": "alice"})
        assert result.data["whoami"] == "alice"

    def test_default_context(self):
        class Query(ObjectType):
            @field()
            def mode(root, info):
                return info.context or "none"

        schema = Schema(query=Query, context="production")
        result = schema.execute("{ mode }")
        assert result.data["mode"] == "production"


class TestSchemaSDL:
    def test_to_sdl_contains_type_query(self):
        class Query(ObjectType):
            @field(return_type=GraphQLString, description="greeting")
            def hello(root, info, name: str = "world"):
                return "hi"

        schema = Schema(query=Query)
        sdl = schema.to_sdl()
        assert "type Query" in sdl
        assert "hello" in sdl

    def test_to_sdl_includes_args(self):
        class Query(ObjectType):
            @field()
            def search(root, info, query: str = "", top_k: int = 5):
                return []

        schema = Schema(query=Query)
        sdl = schema.to_sdl()
        assert "query" in sdl
        assert "top_k" in sdl


class TestMultipleFields:
    def test_two_fields_in_one_query(self):
        class Query(ObjectType):
            @field()
            def hello(root, info):
                return "hello"

            @field()
            def goodbye(root, info):
                return "goodbye"

        schema = Schema(query=Query)
        result = schema.execute("{ hello goodbye }")
        assert result.ok
        assert result.data["hello"] == "hello"
        assert result.data["goodbye"] == "goodbye"


# ===========================================================================
# ExecutionResult
# ===========================================================================

class TestExecutionResult:
    def test_ok_no_errors(self):
        r = ExecutionResult(data={"x": 1}, errors=[])
        assert r.ok is True

    def test_not_ok_with_errors(self):
        from docstoolkit.graphql.executor import GraphQLError
        r = ExecutionResult(data={}, errors=[GraphQLError(message="oops")])
        assert r.ok is False

    def test_to_dict_no_errors(self):
        r = ExecutionResult(data={"x": 1})
        d = r.to_dict()
        assert "data" in d
        assert "errors" not in d

    def test_to_dict_with_errors(self):
        from docstoolkit.graphql.executor import GraphQLError
        r = ExecutionResult(data={}, errors=[GraphQLError(message="fail", path=["q"])])
        d = r.to_dict()
        assert "errors" in d
        assert d["errors"][0]["message"] == "fail"
