"""AgentLoop — основной исполнитель."""
import json
import re
import time
from datetime import datetime

from docstoolkit.agent.types import Tool, ToolCall, AgentStep, AgentResult


# ---------------------------------------------------------------------------
# Echo planner (без LLM): простые правила для тестов
# ---------------------------------------------------------------------------

def _echo_plan(task: str, tools: list[Tool],
               history: list[AgentStep]) -> tuple[str, list[ToolCall], bool]:
    """Mock-планировщик. Если task содержит имя tool — вызывает его.
    После 1-2 tool calls завершает."""
    task_lower = task.lower()
    iteration = len(history) + 1

    # Финальное завершение если уже использовали tool
    if iteration >= 2 and history and history[-1].tool_calls:
        last_outputs = "\n".join(
            tc.output[:200] for s in history for tc in s.tool_calls
        )
        return ("Завершаю",
                [],
                True)  # is_final

    # Выбираем tool по имени в task
    chosen: Tool | None = None
    for t in tools:
        if t.name in task_lower or t.name.replace("_", " ") in task_lower:
            chosen = t
            break

    if not chosen:
        # Default: search если есть
        chosen = next((t for t in tools if t.name == "search"), None)

    if not chosen:
        return ("Нет подходящего инструмента", [], True)

    # Простой arg extraction: первое слово после имени tool
    inputs = {"query": task}  # default
    if chosen.input_schema and "properties" in chosen.input_schema:
        first_prop = next(iter(chosen.input_schema["properties"]), None)
        if first_prop:
            inputs = {first_prop: task}

    return (f"Использую {chosen.name}",
            [ToolCall(name=chosen.name, inputs=inputs)],
            False)


# ---------------------------------------------------------------------------
# Anthropic LLM planner
# ---------------------------------------------------------------------------

def _anthropic_plan(task: str, tools: list[Tool],
                     history: list[AgentStep],
                     model: str = "claude-haiku-4-5-20251001",
                     api_key: str | None = None) -> tuple[str, list[ToolCall], bool, int, float]:
    """Anthropic с tool use. Возвращает (thought, tool_calls, is_final, tokens, cost)."""
    try:
        import anthropic
        import os
    except ImportError:
        raise ImportError("Для Anthropic agent: pip install anthropic")

    client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

    # Convert tools to Anthropic format
    anthropic_tools = [
        {
            "name": t.name,
            "description": t.description,
            "input_schema": t.input_schema,
        }
        for t in tools
    ]

    # Build messages from history
    messages = [{"role": "user", "content": task}]
    for step in history:
        if step.tool_calls:
            tool_use_blocks = [
                {"type": "tool_use", "id": f"tu_{i}", "name": tc.name, "input": tc.inputs}
                for i, tc in enumerate(step.tool_calls)
            ]
            messages.append({"role": "assistant", "content": tool_use_blocks})
            tool_result_blocks = [
                {"type": "tool_result", "tool_use_id": f"tu_{i}", "content": tc.output}
                for i, tc in enumerate(step.tool_calls)
            ]
            messages.append({"role": "user", "content": tool_result_blocks})

    resp = client.messages.create(
        model=model,
        max_tokens=2000,
        tools=anthropic_tools,
        messages=messages,
    )

    # Extract thought + tool_calls + answer
    thought = ""
    tool_calls = []
    answer = ""
    for block in resp.content:
        if block.type == "text":
            if resp.stop_reason == "tool_use":
                thought = block.text
            else:
                answer = block.text
        elif block.type == "tool_use":
            tool_calls.append(ToolCall(name=block.name, inputs=block.input or {}))

    is_final = resp.stop_reason != "tool_use"

    # Pricing (Haiku 4.5)
    in_tok = resp.usage.input_tokens
    out_tok = resp.usage.output_tokens
    pricing = {"input": 1.0, "output": 5.0}  # USD per 1M tokens
    cost = (in_tok * pricing["input"] + out_tok * pricing["output"]) / 1_000_000

    if is_final:
        return (thought or answer, [], True, in_tok + out_tok, cost)
    return (thought, tool_calls, False, in_tok + out_tok, cost)


# ---------------------------------------------------------------------------
# AgentLoop
# ---------------------------------------------------------------------------

class AgentLoop:
    """Цикл выполнения задачи через инструменты."""

    def __init__(self, tools: list[Tool], llm: str = "echo",
                 model: str = "claude-haiku-4-5-20251001",
                 max_iterations: int = 10,
                 budget_usd: float = 0.10):
        self.tools = tools
        self.tools_by_name = {t.name: t for t in tools}
        self.llm = llm
        self.model = model
        self.max_iterations = max_iterations
        self.budget_usd = budget_usd

    def run(self, task: str) -> AgentResult:
        t0 = time.time()
        steps: list[AgentStep] = []
        total_tokens = 0
        total_cost = 0.0
        halted_reason = "max_iter"

        for iteration in range(1, self.max_iterations + 1):
            # Plan
            try:
                if self.llm == "anthropic":
                    thought, tool_calls, is_final, tokens, cost = _anthropic_plan(
                        task, self.tools, steps, self.model
                    )
                    total_tokens += tokens
                    total_cost += cost
                    if total_cost > self.budget_usd:
                        halted_reason = f"budget_exceeded ${total_cost:.4f} > ${self.budget_usd}"
                        break
                else:
                    thought, tool_calls, is_final = _echo_plan(task, self.tools, steps)
            except Exception as e:
                halted_reason = f"planner_error: {e}"
                break

            step = AgentStep(
                iteration=iteration,
                thought=thought,
                tool_calls=tool_calls,
                is_final=is_final,
            )

            # Execute tool calls
            for tc in tool_calls:
                tool = self.tools_by_name.get(tc.name)
                if not tool:
                    tc.error = f"Unknown tool: {tc.name}"
                    tc.output = tc.error
                    continue
                ts0 = time.time()
                try:
                    tc.output = tool.call(**tc.inputs)
                except Exception as e:
                    tc.error = str(e)
                    tc.output = f"Error: {e}"
                tc.duration_ms = int((time.time() - ts0) * 1000)

            steps.append(step)

            if is_final:
                halted_reason = "done"
                # Финальный answer — из thought (echo) или последнего блока
                final_answer = thought
                step.answer = final_answer
                break

        duration_ms = int((time.time() - t0) * 1000)
        final_answer = steps[-1].answer if steps and steps[-1].is_final else ""
        if not final_answer and steps:
            # Fallback: возьмём output последнего tool
            for s in reversed(steps):
                if s.tool_calls and s.tool_calls[-1].output:
                    final_answer = f"[no final from LLM]\nLast tool output:\n{s.tool_calls[-1].output[:500]}"
                    break

        return AgentResult(
            task=task,
            answer=final_answer,
            steps=steps,
            total_iterations=len(steps),
            total_tool_calls=sum(len(s.tool_calls) for s in steps),
            total_tokens=total_tokens,
            total_cost=total_cost,
            duration_ms=duration_ms,
            halted_reason=halted_reason,
        )
