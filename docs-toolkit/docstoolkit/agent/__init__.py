"""Agent loop для autonomous Lorenzo.

Объединяет:
  - RAG (retrieve passages)
  - Skills (knowledge базы инструкций)
  - Tools (callable функции через MCP-style schema)
  - LLM (Anthropic / Echo для тестов)

Цикл:
  user task → LLM выбирает tool → execute → LLM продолжает / завершает

Использование:
    from docstoolkit.agent import AgentLoop, Tool

    tools = [Tool("search", search_fn, "Поиск по корпусу", {...schema})]
    agent = AgentLoop(tools=tools, llm="echo")
    result = agent.run("найди про Yodoca и сделай резюме")
"""
from docstoolkit.agent.types import Tool, ToolCall, AgentStep, AgentResult
from docstoolkit.agent.loop import AgentLoop
from docstoolkit.agent.builtin_tools import default_tools

__all__ = [
    "Tool", "ToolCall", "AgentStep", "AgentResult",
    "AgentLoop", "default_tools",
]
