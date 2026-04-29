"""Plan-and-execute: разбивает сложную задачу на subtasks, выполняет по очереди.

Pattern:
  1. Planner: LLM (или heuristic) → ordered list[Subtask]
  2. Executor: каждый subtask → AgentLoop.run() → SubtaskResult
  3. Replanner (опц.): on subtask failure → перепланировать остаток

Не дублирует AgentLoop, а оркестрирует его.
"""
import re
import time
from dataclasses import dataclass, field
from datetime import datetime

from docstoolkit.agent.types import AgentResult


@dataclass
class Subtask:
    """Один подзадач."""
    id: int
    description: str
    depends_on: list[int] = field(default_factory=list)
    completed: bool = False
    output: str = ""


@dataclass
class SubtaskResult:
    """Результат выполнения одного subtask'а."""
    subtask_id: int
    description: str
    output: str = ""
    error: str = ""
    duration_ms: int = 0
    iterations: int = 0
    tool_calls: int = 0
    tokens: int = 0
    cost: float = 0.0
    agent_result: AgentResult | None = None

    @property
    def ok(self) -> bool:
        return not self.error


@dataclass
class Plan:
    """Список subtasks."""
    task: str
    subtasks: list[Subtask] = field(default_factory=list)
    rationale: str = ""

    def to_markdown(self) -> str:
        lines = [f"# Plan: {self.task}\n"]
        if self.rationale:
            lines.append(f"_{self.rationale}_\n")
        for s in self.subtasks:
            deps = (f" (depends: {s.depends_on})" if s.depends_on else "")
            lines.append(f"{s.id}. {s.description}{deps}")
        return "\n".join(lines)


@dataclass
class PlanExecuteResult:
    """Итог plan-and-execute сессии."""
    task: str
    plan: Plan
    subtask_results: list[SubtaskResult] = field(default_factory=list)
    final_answer: str = ""
    duration_ms: int = 0
    halted_reason: str = ""
    replans: int = 0
    ts: str = field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))

    @property
    def ok(self) -> bool:
        return all(sr.ok for sr in self.subtask_results)

    def to_markdown(self) -> str:
        lines = [f"# Plan-and-execute: {self.task}\n"]
        lines.append(f"**Status:** {'✓' if self.ok else '✗'} "
                     f"({self.halted_reason or 'completed'})")
        lines.append(f"**Duration:** {self.duration_ms}ms")
        lines.append(f"**Subtasks:** {len(self.subtask_results)}/{len(self.plan.subtasks)}")
        if self.replans:
            lines.append(f"**Replans:** {self.replans}")
        lines.append("")
        lines.append("## Plan\n")
        lines.append(self.plan.to_markdown())
        lines.append("\n## Execution trace\n")
        lines.append("| # | Subtask | Status | Iter | Tools | Duration |")
        lines.append("|--:|---------|--------|-----:|------:|---------:|")
        for sr in self.subtask_results:
            status = "✓" if sr.ok else f"ERR: {sr.error[:30]}"
            desc = sr.description[:40] + ("…" if len(sr.description) > 40 else "")
            lines.append(f"| {sr.subtask_id} | {desc} | {status} | "
                         f"{sr.iterations} | {sr.tool_calls} | {sr.duration_ms}ms |")
        if self.final_answer:
            lines.append("\n## Final answer\n")
            lines.append(self.final_answer)
        return "\n".join(lines)


# ---- planner ----

def heuristic_planner(task: str) -> Plan:
    """Heuristic-планировщик без LLM: разбивает по числовым маркерам / союзам.

    Правила:
      - "1) X 2) Y 3) Z" → 3 subtask
      - "X, и Y, потом Z" → 3 subtask
      - "X и Y" → 2 subtask
      - один глагол → 1 subtask
    """
    # Try numbered lists first: "1) ... 2) ... 3) ..."
    numbered = re.findall(r'\d[\).]\s*([^\d\n]{5,200}?)(?=\d[\).]|$)',
                           task + " 9)")
    if len(numbered) >= 2:
        subtasks = [Subtask(id=i + 1, description=p.strip(", и.;"))
                    for i, p in enumerate(numbered)]
        return Plan(task=task, subtasks=subtasks,
                    rationale="Numbered list detected")

    # Split on connectors
    parts = re.split(r'(?:\s+(?:потом|затем|после|then|и затем|а затем)\s+|;\s+)',
                      task, flags=re.IGNORECASE)
    if len(parts) >= 2:
        subtasks = [Subtask(id=i + 1, description=p.strip(", и.;"))
                    for i, p in enumerate(parts) if p.strip()]
        return Plan(task=task, subtasks=subtasks,
                    rationale="Sequential connector split")

    # And-split (only for short tasks)
    if " и " in task.lower() and len(task) < 200:
        parts = re.split(r'\s+и\s+', task, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) == 2 and all(len(p.strip()) > 5 for p in parts):
            return Plan(
                task=task,
                subtasks=[
                    Subtask(id=1, description=parts[0].strip(", .")),
                    Subtask(id=2, description=parts[1].strip(", ."),
                            depends_on=[1]),
                ],
                rationale="And-split",
            )

    return Plan(task=task,
                subtasks=[Subtask(id=1, description=task)],
                rationale="Single task")


# ---- executor ----

def execute_plan(plan: Plan, *, agent=None, on_subtask=None,
                  max_replans: int = 0,
                  replanner=None) -> PlanExecuteResult:
    """Выполняет plan через agent (AgentLoop) или напрямую (echo).

    agent: instance с .run(task, context_messages=[...]) → AgentResult
           Если None — fallback на «эхо-executor» (для тестов).
    on_subtask(subtask, sr) — callback после каждого subtask'а.
    max_replans: при failure subtask'а — replan до N раз.
    """
    result = PlanExecuteResult(task=plan.task, plan=plan)
    t0 = time.time()

    completed_outputs: dict[int, str] = {}
    i = 0
    while i < len(plan.subtasks):
        st = plan.subtasks[i]
        # build prefix из dependencies — добавляется в task description
        prefix_parts = []
        for dep_id in st.depends_on:
            if dep_id in completed_outputs:
                prefix_parts.append(
                    f"[Из subtask {dep_id}]: {completed_outputs[dep_id][:500]}"
                )
        prefix = ("\n".join(prefix_parts) + "\n\n") if prefix_parts else ""
        sr = _run_subtask(st, agent, prefix=prefix)
        result.subtask_results.append(sr)

        if on_subtask:
            try:
                on_subtask(st, sr)
            except Exception:
                pass

        if not sr.ok:
            if result.replans < max_replans and replanner:
                # Replan: новый план для оставшихся subtasks
                remaining_task = (
                    f"Замени неудавшийся подзадач '{st.description}'. "
                    f"Ошибка: {sr.error}. "
                    f"Продолжи цель: {plan.task}"
                )
                try:
                    new_plan = replanner(remaining_task)
                    # Объединяем: оставляем уже сделанные, заменяем хвост
                    next_id = max(s.id for s in plan.subtasks) + 1
                    for ns in new_plan.subtasks:
                        ns.id = next_id
                        next_id += 1
                    plan.subtasks = plan.subtasks[:i + 1] + new_plan.subtasks
                    result.replans += 1
                    i += 1
                    continue
                except Exception:
                    pass
            # No replan — abort
            result.halted_reason = f"subtask {st.id} failed"
            break

        st.completed = True
        st.output = sr.output
        completed_outputs[st.id] = sr.output
        i += 1

    # Final answer = output последнего subtask'а
    if result.subtask_results and result.subtask_results[-1].ok:
        result.final_answer = result.subtask_results[-1].output
    if not result.halted_reason:
        result.halted_reason = "completed"
    result.duration_ms = int((time.time() - t0) * 1000)
    return result


def _run_subtask(st: Subtask, agent, prefix: str = "") -> SubtaskResult:
    sr = SubtaskResult(subtask_id=st.id, description=st.description)
    t0 = time.time()
    try:
        full_task = (prefix + st.description) if prefix else st.description
        if agent is not None:
            ar = agent.run(full_task)
            sr.agent_result = ar
            sr.output = ar.answer
            sr.iterations = ar.total_iterations
            sr.tool_calls = ar.total_tool_calls
            sr.tokens = ar.total_tokens
            sr.cost = ar.total_cost
        else:
            # Fallback echo: просто описание subtask'а
            sr.output = f"[echo-executor] {st.description}"
    except Exception as e:
        sr.error = f"{type(e).__name__}: {str(e)[:200]}"
    sr.duration_ms = int((time.time() - t0) * 1000)
    return sr


def plan_and_execute(task: str, *, agent=None, planner=None,
                      on_subtask=None, max_replans: int = 0) -> PlanExecuteResult:
    """Удобный wrapper: planner(task) → execute_plan."""
    p = (planner or heuristic_planner)(task)
    return execute_plan(p, agent=agent, on_subtask=on_subtask,
                         max_replans=max_replans, replanner=planner)
