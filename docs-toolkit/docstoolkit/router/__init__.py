"""Model router: declarative chain providers с failover, retry, cost-aware routing.

Использование:
    from docstoolkit.router import ModelRouter, ModelChain, ModelHop

    chain = ModelChain(name="haiku-then-echo", hops=[
        ModelHop(answerer="anthropic", model="claude-haiku-4-5-20251001"),
        ModelHop(answerer="echo"),  # fallback
    ])
    r = ModelRouter()
    result = r.invoke(chain, system="...", user="...")
    # result: RouteResult(answer, tokens, cost, hop_used, hops_tried, errors)

Built-in chains: "cheap", "fast", "balanced", "high-quality".
"""
from docstoolkit.router.chain import (
    ModelRouter, ModelChain, ModelHop, RouteResult,
    BUILTIN_CHAINS,
)

__all__ = [
    "ModelRouter", "ModelChain", "ModelHop", "RouteResult",
    "BUILTIN_CHAINS",
]
