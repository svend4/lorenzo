"""Tests for docstoolkit.url_router."""
from __future__ import annotations

import pytest

from docstoolkit.url_router import Route, RouteMatch, UrlRouter


# ---------------------------------------------------------------------------
# Route dataclass
# ---------------------------------------------------------------------------


class TestRoute:
    def test_route_basic_fields(self):
        r = Route(pattern="/x", handler=lambda: None, methods=["GET"])
        assert r.pattern == "/x"
        assert callable(r.handler)
        assert r.methods == ["GET"]

    def test_route_default_methods(self):
        r = Route(pattern="/x", handler=lambda: None)
        assert r.methods == ["GET"]

    def test_route_default_name_is_none(self):
        r = Route(pattern="/x", handler=lambda: None)
        assert r.name is None

    def test_route_default_priority_zero(self):
        r = Route(pattern="/x", handler=lambda: None)
        assert r.priority == 0

    def test_route_methods_uppercased(self):
        r = Route(pattern="/x", handler=lambda: None, methods=["get", "post"])
        assert r.methods == ["GET", "POST"]

    def test_route_matches_method_case_insensitive(self):
        r = Route(pattern="/x", handler=lambda: None, methods=["GET"])
        assert r.matches_method("get")
        assert r.matches_method("GET")
        assert not r.matches_method("POST")


# ---------------------------------------------------------------------------
# RouteMatch dataclass
# ---------------------------------------------------------------------------


class TestRouteMatch:
    def test_route_match_fields(self):
        r = Route(pattern="/x", handler=lambda: None)
        m = RouteMatch(route=r, params={"a": "1"}, method="GET", path="/x")
        assert m.route is r
        assert m.params == {"a": "1"}
        assert m.method == "GET"
        assert m.path == "/x"


# ---------------------------------------------------------------------------
# add_route / convenience methods
# ---------------------------------------------------------------------------


class TestAddRoute:
    def test_add_route_returns_route(self):
        r = UrlRouter()
        route = r.add_route("/x", lambda: None)
        assert isinstance(route, Route)

    def test_add_route_default_methods_get(self):
        r = UrlRouter()
        route = r.add_route("/x", lambda: None)
        assert route.methods == ["GET"]

    def test_add_route_custom_methods(self):
        r = UrlRouter()
        route = r.add_route("/x", lambda: None, methods=["GET", "POST"])
        assert route.methods == ["GET", "POST"]

    def test_add_route_with_name(self):
        r = UrlRouter()
        route = r.add_route("/x", lambda: None, name="home")
        assert route.name == "home"

    def test_add_route_with_priority(self):
        r = UrlRouter()
        route = r.add_route("/x", lambda: None, priority=5)
        assert route.priority == 5

    def test_add_route_increments_count(self):
        r = UrlRouter()
        assert r.route_count == 0
        r.add_route("/x", lambda: None)
        assert r.route_count == 1


class TestGet:
    def test_get_sets_methods(self):
        r = UrlRouter()
        route = r.get("/x", lambda: "ok")
        assert route.methods == ["GET"]

    def test_get_returns_route(self):
        r = UrlRouter()
        route = r.get("/x", lambda: "ok")
        assert isinstance(route, Route)

    def test_get_with_name(self):
        r = UrlRouter()
        route = r.get("/x", lambda: "ok", name="x")
        assert route.name == "x"


class TestPost:
    def test_post_sets_methods(self):
        r = UrlRouter()
        route = r.post("/x", lambda: "ok")
        assert route.methods == ["POST"]

    def test_post_matches_post_only(self):
        r = UrlRouter()
        r.post("/x", lambda: "ok")
        assert r.match("/x", "POST") is not None
        assert r.match("/x", "GET") is None


class TestPutDelete:
    def test_put_sets_methods(self):
        r = UrlRouter()
        route = r.put("/x", lambda: None)
        assert route.methods == ["PUT"]

    def test_delete_sets_methods(self):
        r = UrlRouter()
        route = r.delete("/x", lambda: None)
        assert route.methods == ["DELETE"]

    def test_put_matches_put_only(self):
        r = UrlRouter()
        r.put("/x", lambda: None)
        assert r.match("/x", "PUT") is not None
        assert r.match("/x", "GET") is None

    def test_delete_matches_delete_only(self):
        r = UrlRouter()
        r.delete("/x", lambda: None)
        assert r.match("/x", "DELETE") is not None
        assert r.match("/x", "GET") is None


# ---------------------------------------------------------------------------
# Matching: static routes
# ---------------------------------------------------------------------------


class TestMatchStatic:
    def test_static_exact_match(self):
        r = UrlRouter()
        r.get("/users", lambda: "ok")
        m = r.match("/users")
        assert m is not None
        assert m.params == {}

    def test_static_no_match_different_path(self):
        r = UrlRouter()
        r.get("/users", lambda: "ok")
        assert r.match("/posts") is None

    def test_static_trailing_slash_lenient(self):
        r = UrlRouter()
        r.get("/users", lambda: "ok")
        assert r.match("/users/") is not None

    def test_static_no_trailing_slash_lenient(self):
        r = UrlRouter()
        r.get("/users/", lambda: "ok")
        assert r.match("/users") is not None

    def test_static_root_path(self):
        r = UrlRouter()
        r.get("/", lambda: "home")
        assert r.match("/") is not None


# ---------------------------------------------------------------------------
# Matching: single parameter
# ---------------------------------------------------------------------------


class TestMatchParameters:
    def test_single_param_captures_value(self):
        r = UrlRouter()
        r.get("/users/{id}", lambda **kw: kw)
        m = r.match("/users/123")
        assert m is not None
        assert m.params == {"id": "123"}

    def test_param_does_not_cross_slash(self):
        r = UrlRouter()
        r.get("/users/{id}", lambda: None)
        # /users/123/posts should NOT match /users/{id}
        assert r.match("/users/123/posts") is None

    def test_param_with_letters(self):
        r = UrlRouter()
        r.get("/users/{id}", lambda **kw: kw)
        m = r.match("/users/alice")
        assert m.params == {"id": "alice"}

    def test_param_with_hyphen(self):
        r = UrlRouter()
        r.get("/users/{id}", lambda **kw: kw)
        m = r.match("/users/abc-123")
        assert m.params == {"id": "abc-123"}


class TestMatchMultipleParams:
    def test_two_params(self):
        r = UrlRouter()
        r.get("/users/{id}/posts/{post_id}", lambda **kw: kw)
        m = r.match("/users/42/posts/7")
        assert m is not None
        assert m.params == {"id": "42", "post_id": "7"}

    def test_three_params(self):
        r = UrlRouter()
        r.get("/{a}/{b}/{c}", lambda **kw: kw)
        m = r.match("/x/y/z")
        assert m.params == {"a": "x", "b": "y", "c": "z"}

    def test_duplicate_param_name_raises(self):
        r = UrlRouter()
        with pytest.raises(ValueError):
            r.get("/{x}/{x}", lambda **kw: kw)


# ---------------------------------------------------------------------------
# Matching: typed int parameter
# ---------------------------------------------------------------------------


class TestMatchTypedInt:
    def test_int_matches_digits(self):
        r = UrlRouter()
        r.get("/users/{id:int}", lambda **kw: kw)
        m = r.match("/users/123")
        assert m is not None
        assert m.params == {"id": "123"}

    def test_int_rejects_letters(self):
        r = UrlRouter()
        r.get("/users/{id:int}", lambda: None)
        assert r.match("/users/alice") is None

    def test_int_value_stored_as_string(self):
        r = UrlRouter()
        r.get("/items/{n:int}", lambda **kw: kw)
        m = r.match("/items/42")
        assert isinstance(m.params["n"], str)


# ---------------------------------------------------------------------------
# Matching: wildcard
# ---------------------------------------------------------------------------


class TestMatchWildcard:
    def test_wildcard_captures_tail(self):
        r = UrlRouter()
        r.get("/files/*path", lambda **kw: kw)
        m = r.match("/files/a/b/c.txt")
        assert m is not None
        assert m.params == {"path": "a/b/c.txt"}

    def test_wildcard_captures_single_segment(self):
        r = UrlRouter()
        r.get("/files/*path", lambda **kw: kw)
        m = r.match("/files/x")
        assert m.params == {"path": "x"}

    def test_wildcard_requires_at_least_one_char(self):
        r = UrlRouter()
        r.get("/files/*path", lambda: None)
        # No content after the slash → should not match.
        assert r.match("/files/") is None


# ---------------------------------------------------------------------------
# Method routing
# ---------------------------------------------------------------------------


class TestMatchMethod:
    def test_get_vs_post_distinct(self):
        r = UrlRouter()
        r.get("/x", lambda: "get")
        r.post("/x", lambda: "post")
        assert r.match("/x", "GET").route.handler() == "get"
        assert r.match("/x", "POST").route.handler() == "post"

    def test_route_with_multiple_methods(self):
        r = UrlRouter()
        r.add_route("/x", lambda: "ok", methods=["GET", "POST"])
        assert r.match("/x", "GET") is not None
        assert r.match("/x", "POST") is not None
        assert r.match("/x", "DELETE") is None

    def test_method_case_insensitive(self):
        r = UrlRouter()
        r.get("/x", lambda: "ok")
        assert r.match("/x", "get") is not None


# ---------------------------------------------------------------------------
# Match not found
# ---------------------------------------------------------------------------


class TestMatchNotFound:
    def test_empty_router_returns_none(self):
        r = UrlRouter()
        assert r.match("/anything") is None

    def test_path_mismatch_returns_none(self):
        r = UrlRouter()
        r.get("/x", lambda: None)
        assert r.match("/y") is None

    def test_method_mismatch_returns_none(self):
        r = UrlRouter()
        r.get("/x", lambda: None)
        assert r.match("/x", "POST") is None


# ---------------------------------------------------------------------------
# match_all
# ---------------------------------------------------------------------------


class TestMatchAll:
    def test_match_all_returns_all_matches(self):
        r = UrlRouter()
        r.get("/x", lambda: None)
        r.post("/x", lambda: None)
        matches = r.match_all("/x")
        assert len(matches) == 2

    def test_match_all_empty_when_no_match(self):
        r = UrlRouter()
        r.get("/x", lambda: None)
        assert r.match_all("/y") == []

    def test_match_all_includes_params(self):
        r = UrlRouter()
        r.get("/users/{id}", lambda: None)
        r.post("/users/{id}", lambda: None)
        matches = r.match_all("/users/5")
        assert all(m.params == {"id": "5"} for m in matches)


# ---------------------------------------------------------------------------
# dispatch
# ---------------------------------------------------------------------------


class TestDispatch:
    def test_dispatch_calls_handler_with_params(self):
        r = UrlRouter()
        r.get("/users/{id}", lambda id: f"user-{id}")
        assert r.dispatch("/users/42") == "user-42"

    def test_dispatch_no_match_raises(self):
        r = UrlRouter()
        with pytest.raises(LookupError):
            r.dispatch("/missing")

    def test_dispatch_passes_extra_kwargs(self):
        r = UrlRouter()
        r.get("/x", lambda **kw: kw)
        result = r.dispatch("/x", "GET", request="REQ")
        assert result == {"request": "REQ"}

    def test_dispatch_combines_params_and_extras(self):
        r = UrlRouter()
        r.get("/users/{id}", lambda id, ctx: (id, ctx))
        assert r.dispatch("/users/9", "GET", ctx="C") == ("9", "C")


# ---------------------------------------------------------------------------
# url_for (reverse routing)
# ---------------------------------------------------------------------------


class TestUrlFor:
    def test_url_for_static(self):
        r = UrlRouter()
        r.get("/home", lambda: None, name="home")
        assert r.url_for("home") == "/home"

    def test_url_for_with_param(self):
        r = UrlRouter()
        r.get("/users/{id}", lambda: None, name="user")
        assert r.url_for("user", id=42) == "/users/42"

    def test_url_for_with_typed_param(self):
        r = UrlRouter()
        r.get("/items/{n:int}", lambda: None, name="item")
        assert r.url_for("item", n=7) == "/items/7"

    def test_url_for_with_multiple_params(self):
        r = UrlRouter()
        r.get("/users/{id}/posts/{post_id}", lambda: None, name="post")
        assert r.url_for("post", id=1, post_id=2) == "/users/1/posts/2"

    def test_url_for_with_wildcard(self):
        r = UrlRouter()
        r.get("/files/*path", lambda: None, name="file")
        assert r.url_for("file", path="a/b.txt") == "/files/a/b.txt"

    def test_url_for_unknown_name_raises(self):
        r = UrlRouter()
        with pytest.raises(KeyError):
            r.url_for("nope")

    def test_url_for_missing_param_raises(self):
        r = UrlRouter()
        r.get("/users/{id}", lambda: None, name="user")
        with pytest.raises(KeyError):
            r.url_for("user")


# ---------------------------------------------------------------------------
# Priority
# ---------------------------------------------------------------------------


class TestPriority:
    def test_higher_priority_matched_first(self):
        r = UrlRouter()
        r.add_route("/x", lambda: "low", priority=1)
        r.add_route("/x", lambda: "high", priority=10)
        m = r.match("/x")
        assert m.route.handler() == "high"

    def test_default_priority_order_is_insertion(self):
        r = UrlRouter()
        r.add_route("/x", lambda: "first")
        r.add_route("/x", lambda: "second")
        # Both priority=0 — the first inserted wins.
        m = r.match("/x")
        assert m.route.handler() == "first"

    def test_list_routes_sorted_by_priority(self):
        r = UrlRouter()
        r.add_route("/a", lambda: None, priority=1)
        r.add_route("/b", lambda: None, priority=5)
        r.add_route("/c", lambda: None, priority=3)
        priorities = [route.priority for route in r.list_routes()]
        assert priorities == [5, 3, 1]


# ---------------------------------------------------------------------------
# remove_route
# ---------------------------------------------------------------------------


class TestRemoveRoute:
    def test_remove_existing_returns_true(self):
        r = UrlRouter()
        r.get("/x", lambda: None)
        assert r.remove_route("/x") is True

    def test_remove_nonexistent_returns_false(self):
        r = UrlRouter()
        assert r.remove_route("/missing") is False

    def test_remove_decreases_count(self):
        r = UrlRouter()
        r.get("/x", lambda: None)
        r.remove_route("/x")
        assert r.route_count == 0

    def test_remove_makes_route_unmatchable(self):
        r = UrlRouter()
        r.get("/x", lambda: None)
        r.remove_route("/x")
        assert r.match("/x") is None


# ---------------------------------------------------------------------------
# route_count
# ---------------------------------------------------------------------------


class TestRouteCount:
    def test_count_starts_zero(self):
        assert UrlRouter().route_count == 0

    def test_count_after_adding(self):
        r = UrlRouter()
        r.get("/a", lambda: None)
        r.get("/b", lambda: None)
        r.get("/c", lambda: None)
        assert r.route_count == 3


# ---------------------------------------------------------------------------
# list_routes
# ---------------------------------------------------------------------------


class TestListRoutes:
    def test_list_routes_empty(self):
        assert UrlRouter().list_routes() == []

    def test_list_routes_returns_all(self):
        r = UrlRouter()
        r.get("/a", lambda: None)
        r.post("/b", lambda: None)
        routes = r.list_routes()
        assert len(routes) == 2

    def test_list_routes_returns_new_list(self):
        # Modifying the returned list shouldn't affect internal state.
        r = UrlRouter()
        r.get("/a", lambda: None)
        routes = r.list_routes()
        routes.clear()
        assert r.route_count == 1


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_clear_removes_all_routes(self):
        r = UrlRouter()
        r.get("/a", lambda: None)
        r.get("/b", lambda: None)
        r.clear()
        assert r.route_count == 0

    def test_clear_on_empty_router(self):
        r = UrlRouter()
        r.clear()
        assert r.route_count == 0

    def test_match_empty_path(self):
        r = UrlRouter()
        r.get("", lambda: "empty")
        assert r.match("") is not None

    def test_no_routes_match_anything(self):
        r = UrlRouter()
        assert r.match("/x") is None
        assert r.match_all("/x") == []

    def test_pattern_with_regex_metachars_treated_literally(self):
        # The dot in the pattern should match only a literal dot.
        r = UrlRouter()
        r.get("/a.b", lambda: "ok")
        assert r.match("/a.b") is not None
        assert r.match("/axb") is None

    def test_handler_can_be_any_callable(self):
        class Handler:
            def __call__(self, **kw):
                return "called"

        r = UrlRouter()
        r.get("/x", Handler())
        assert r.dispatch("/x") == "called"

    def test_match_returns_routematch_instance(self):
        r = UrlRouter()
        r.get("/x", lambda: None)
        m = r.match("/x")
        assert isinstance(m, RouteMatch)
