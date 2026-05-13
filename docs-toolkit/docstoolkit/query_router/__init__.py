"""Query router: rule-based routing, middleware pipeline, pure stdlib.

Usage::

    from docstoolkit.query_router import (
        RouteCondition, RouteAction, RouteRule,
        RouteResult, QueryRouter,
        QueryMiddleware, NormalizationMiddleware, TruncationMiddleware,
        MiddlewarePipeline,
    )

    # Build a router
    router = QueryRouter()
    router.add_rule(RouteRule(
        name="reject-empty",
        condition=RouteCondition.LENGTH_THRESHOLD,
        action=RouteAction.REJECT,
        priority=100,
        max_length=0,
    ))
    result = router.route("hello world")

    # Build a middleware pipeline
    pipeline = MiddlewarePipeline([
        NormalizationMiddleware(),
        TruncationMiddleware(max_length=200),
    ])
    clean = pipeline.run("  Hello World  ")
"""
from docstoolkit.query_router.route import (
    RouteCondition,
    RouteAction,
    RouteRule,
)
from docstoolkit.query_router.router import (
    RouteResult,
    QueryRouter,
)
from docstoolkit.query_router.middleware import (
    QueryMiddleware,
    NormalizationMiddleware,
    TruncationMiddleware,
    MiddlewarePipeline,
)

__all__ = [
    # Enums / dataclasses from route.py
    "RouteCondition",
    "RouteAction",
    "RouteRule",
    # Router
    "RouteResult",
    "QueryRouter",
    # Middleware
    "QueryMiddleware",
    "NormalizationMiddleware",
    "TruncationMiddleware",
    "MiddlewarePipeline",
]
