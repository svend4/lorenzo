"""Тесты model router (chain + failover)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.router import (
    ModelRouter, ModelChain, ModelHop, RouteResult, BUILTIN_CHAINS,
)
from docstoolkit.router.chain import get_chain


def test_model_hop_defaults():
    h = ModelHop()
    assert h.answerer == "echo"
    assert h.max_retries == 0


def test_model_chain_dataclass():
    c = ModelChain(name="x", hops=[ModelHop(answerer="echo")])
    assert c.name == "x"
    assert len(c.hops) == 1


def test_route_result_ok_property():
    r = RouteResult(hop_used=0)
    assert r.ok
    r2 = RouteResult(hop_used=-1)
    assert not r2.ok


def test_invoke_echo_chain_succeeds():
    """echo-only chain всегда работает."""
    r = ModelRouter()
    chain = BUILTIN_CHAINS["echo-only"]
    result = r.invoke(chain, system="S", user="Q\n[1] **T**\nИсточник: `d.md`\n\nText.")
    assert result.ok
    assert result.hop_used == 0
    assert result.hop_answerer == "echo"
    assert result.hops_tried == 1
    assert result.answer
    assert result.duration_ms >= 0


def test_invoke_calls_hop_callback():
    calls = []
    r = ModelRouter(on_hop_attempt=lambda c, i, h: calls.append((c, i, h.answerer)))
    r.invoke(BUILTIN_CHAINS["echo-only"], system="S", user="Q")
    assert len(calls) == 1
    assert calls[0] == ("echo-only", 0, "echo")


def test_invoke_failover_chain_uses_first_working_hop():
    """Цепочка с несколькими hops — первый рабочий побеждает."""
    chain = ModelChain(name="multi", hops=[
        ModelHop(answerer="echo"),  # immediately works
        ModelHop(answerer="anthropic", model="x"),  # never reached
    ])
    r = ModelRouter()
    result = r.invoke(chain, system="S", user="Q")
    assert result.hop_used == 0
    assert result.hops_tried == 1


def test_invoke_skips_when_budget_check_false():
    """budget_check возвращает False → hop пропускается."""
    chain = ModelChain(name="m", hops=[
        ModelHop(answerer="echo"),
        ModelHop(answerer="echo"),  # backup
    ])
    counter = {"n": 0}
    def deny(scope):
        counter["n"] += 1
        return False
    r = ModelRouter(budget_check=deny)
    result = r.invoke(chain, system="S", user="Q", budget_scope="user:x")
    # Все hops отвергнуты budget'ом
    assert result.hop_used == -1
    assert not result.ok
    assert len(result.errors) == 2
    assert all("budget" in e for e in result.errors)


def test_get_chain_known():
    c = get_chain("cheap")
    assert c is not None
    assert c.name == "cheap"


def test_get_chain_unknown():
    assert get_chain("nonexistent-chain-name") is None


def test_builtin_chains_have_required_fields():
    for name, chain in BUILTIN_CHAINS.items():
        assert chain.name == name
        assert len(chain.hops) >= 1
        # Last hop is echo (always-works fallback) for all built-ins
        assert chain.hops[-1].answerer == "echo"


def test_invoke_with_failing_callback_does_not_break():
    """Callback бросает — invoke всё равно работает."""
    def bad_cb(c, i, h):
        raise RuntimeError("cb broken")
    r = ModelRouter(on_hop_attempt=bad_cb)
    result = r.invoke(BUILTIN_CHAINS["echo-only"], system="S", user="Q")
    assert result.ok
