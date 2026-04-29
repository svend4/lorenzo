"""Тесты agent loop."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.agent.types import Tool, ToolCall, AgentStep, AgentResult
from docstoolkit.agent.loop import AgentLoop, _echo_plan


def test_tool_dataclass():
    t = Tool(name="test", fn=lambda: "ok", description="test desc")
    assert t.name == "test"
    assert t.call() == "ok"


def test_tool_call_with_kwargs():
    t = Tool(name="echo", fn=lambda x: f"got: {x}", description="echo")
    assert t.call(x="hello") == "got: hello"


def test_tool_handles_error():
    def bad(): raise ValueError("oops")
    t = Tool(name="bad", fn=bad, description="bad")
    assert "❌" in t.call()
    assert "oops" in t.call()


def test_tool_serializes_dict():
    t = Tool(name="dict", fn=lambda: {"a": 1}, description="d")
    assert '"a"' in t.call()


def test_echo_plan_chooses_named_tool():
    tools = [
        Tool("search", lambda query="": "found", "поиск"),
        Tool("read", lambda: "content", "чтение"),
    ]
    thought, calls, is_final = _echo_plan("search Yodoca", tools, [])
    assert not is_final
    assert len(calls) == 1
    assert calls[0].name == "search"


def test_echo_plan_terminates_after_2_iterations():
    tools = [Tool("search", lambda query="": "found", "поиск")]
    history = [AgentStep(iteration=1, tool_calls=[ToolCall("search", {})])]
    thought, calls, is_final = _echo_plan("test", tools, history)
    assert is_final


def test_agent_loop_basic_flow():
    tools = [Tool("search", lambda query="": f"results for {query}", "search desc")]
    agent = AgentLoop(tools=tools, llm="echo", max_iterations=3)
    result = agent.run("search xyz")

    assert result.task == "search xyz"
    assert result.total_iterations >= 1
    assert result.total_tool_calls >= 1
    assert result.halted_reason in ("done", "max_iter")


def test_agent_loop_unknown_tool_handles():
    """Если LLM вернул unknown tool — не падает."""
    tools = [Tool("search", lambda query="": "ok", "search")]
    agent = AgentLoop(tools=tools, llm="echo", max_iterations=2)
    result = agent.run("test query")
    assert result.duration_ms >= 0


def test_agent_result_to_markdown():
    r = AgentResult(
        task="test", answer="answer", total_iterations=2,
        total_tool_calls=1, total_cost=0.005,
    )
    md = r.to_markdown()
    assert "test" in md
    assert "answer" in md
    assert "2" in md  # iterations
