"""Workflow DAG: топологическая сортировка + параллельное выполнение."""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Step:
    """Один узел DAG.

    inputs: dict[arg_name -> ref], где ref:
      - "$.X" → context[X]
      - "$.STEP.output" → output другого шага
      - любая константа (str без $.) → передаётся как есть
    """
    name: str
    fn: Callable
    inputs: dict[str, Any] = field(default_factory=dict)
    on_error: str = "fail"          # fail | skip | retry
    max_retries: int = 0
    retry_backoff_s: float = 0.5


@dataclass
class StepResult:
    """Результат одного шага."""
    name: str
    output: Any = None
    error: str = ""
    started_ts: float = 0.0
    duration_ms: int = 0
    skipped: bool = False
    retries: int = 0

    @property
    def ok(self) -> bool:
        return not self.error and not self.skipped


@dataclass
class Workflow:
    """Описание DAG'а: список Step'ов."""
    name: str
    steps: list[Step] = field(default_factory=list)
    description: str = ""


@dataclass
class WorkflowResult:
    """Результат прогона DAG'а."""
    workflow: str
    steps: list[StepResult] = field(default_factory=list)
    outputs: dict[str, Any] = field(default_factory=dict)
    duration_ms: int = 0
    failed: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failed

    def step(self, name: str) -> StepResult | None:
        for s in self.steps:
            if s.name == name:
                return s
        return None

    def report(self) -> str:
        """Markdown отчёт."""
        lines = [f"# Workflow: {self.workflow}\n"]
        lines.append(f"**Duration:** {self.duration_ms}ms")
        lines.append(f"**Steps:** {len(self.steps)} "
                     f"({len(self.failed)} failed)\n")
        lines.append("| Step | Status | Duration | Detail |")
        lines.append("|------|--------|---------:|--------|")
        for s in self.steps:
            if s.skipped:
                status = "skipped"
            elif s.error:
                status = "ERROR"
            else:
                status = "ok"
            detail = s.error[:60] if s.error else (
                f"{type(s.output).__name__}" if s.output is not None else "—"
            )
            if s.retries:
                detail += f" (retries={s.retries})"
            lines.append(f"| `{s.name}` | {status} | {s.duration_ms}ms | {detail} |")
        return "\n".join(lines)


# ---- runner ----

def run(wf: Workflow, context: dict | None = None) -> WorkflowResult:
    """Синхронный запуск с топологической сортировкой.
    Шаги без взаимных зависимостей выполняются последовательно
    (для true-parallel — run_async)."""
    context = dict(context or {})
    result = WorkflowResult(workflow=wf.name)
    t0 = time.time()

    order = _topo_sort(wf.steps)
    if order is None:
        result.failed.append("__cycle__")
        return result

    step_outputs: dict[str, Any] = {}
    for step in order:
        sr = _execute_step(step, context, step_outputs)
        result.steps.append(sr)
        if sr.error and step.on_error == "fail":
            result.failed.append(step.name)
            # Skip остальные
            for remaining in order[order.index(step) + 1:]:
                result.steps.append(StepResult(
                    name=remaining.name, skipped=True,
                    error="upstream failure",
                ))
            break
        elif sr.error and step.on_error == "skip":
            result.failed.append(step.name)
        else:
            step_outputs[step.name] = sr.output
            result.outputs[step.name] = sr.output

    result.duration_ms = int((time.time() - t0) * 1000)
    return result


def run_async(wf: Workflow, context: dict | None = None,
              max_workers: int = 4) -> WorkflowResult:
    """Параллельное выполнение шагов одного level'а через ThreadPoolExecutor."""
    context = dict(context or {})
    result = WorkflowResult(workflow=wf.name)
    t0 = time.time()

    levels = _level_sort(wf.steps)
    if levels is None:
        result.failed.append("__cycle__")
        return result

    step_outputs: dict[str, Any] = {}
    aborted = False
    for level in levels:
        if aborted:
            for s in level:
                result.steps.append(StepResult(name=s.name, skipped=True,
                                                error="upstream failure"))
            continue

        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {ex.submit(_execute_step, s, context, step_outputs): s
                       for s in level}
            level_results = []
            for fut in as_completed(futures):
                level_results.append(fut.result())

        # Сохраняем в порядке level
        name_to_sr = {sr.name: sr for sr in level_results}
        for s in level:
            sr = name_to_sr[s.name]
            result.steps.append(sr)
            if sr.error and s.on_error == "fail":
                result.failed.append(s.name)
                aborted = True
            elif sr.error and s.on_error == "skip":
                result.failed.append(s.name)
            else:
                step_outputs[s.name] = sr.output
                result.outputs[s.name] = sr.output

    result.duration_ms = int((time.time() - t0) * 1000)
    return result


# ---- internals ----

def _execute_step(step: Step, context: dict,
                   step_outputs: dict[str, Any]) -> StepResult:
    sr = StepResult(name=step.name, started_ts=time.time())
    t0 = time.time()
    try:
        kwargs = _resolve_inputs(step.inputs, context, step_outputs)
    except Exception as e:
        sr.error = f"input resolution: {e}"
        sr.duration_ms = int((time.time() - t0) * 1000)
        return sr

    attempts = 0
    while True:
        attempts += 1
        try:
            sr.output = step.fn(**kwargs)
            sr.duration_ms = int((time.time() - t0) * 1000)
            sr.retries = attempts - 1
            return sr
        except Exception as e:
            if step.on_error == "retry" and attempts <= step.max_retries:
                time.sleep(step.retry_backoff_s * attempts)
                continue
            if attempts <= step.max_retries:
                time.sleep(step.retry_backoff_s * attempts)
                continue
            sr.error = f"{type(e).__name__}: {str(e)[:200]}"
            sr.duration_ms = int((time.time() - t0) * 1000)
            sr.retries = attempts - 1
            return sr


def _resolve_inputs(spec: dict[str, Any], context: dict,
                     outputs: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for arg, ref in spec.items():
        if isinstance(ref, str) and ref.startswith("$."):
            path = ref[2:]
            parts = path.split(".")
            if len(parts) == 1:
                out[arg] = context[parts[0]]
            elif len(parts) == 2 and parts[1] == "output":
                out[arg] = outputs[parts[0]]
            else:
                # $.STEP.output.field — не поддерживаем deep nav, оставляем
                out[arg] = ref
        else:
            out[arg] = ref
    return out


def _step_deps(step: Step) -> set[str]:
    """Имена шагов от которых зависит данный шаг."""
    deps = set()
    for ref in step.inputs.values():
        if isinstance(ref, str) and ref.startswith("$."):
            parts = ref[2:].split(".")
            if len(parts) >= 2 and parts[1] == "output":
                deps.add(parts[0])
    return deps


def _topo_sort(steps: list[Step]) -> list[Step] | None:
    """Топологическая сортировка. Возвращает None если есть цикл."""
    by_name = {s.name: s for s in steps}
    in_deg = {s.name: 0 for s in steps}
    edges: dict[str, list[str]] = {s.name: [] for s in steps}

    for s in steps:
        for d in _step_deps(s):
            if d in by_name:
                edges[d].append(s.name)
                in_deg[s.name] += 1

    queue = [n for n, deg in in_deg.items() if deg == 0]
    order = []
    while queue:
        # стабильный порядок по имени для детерминизма
        queue.sort()
        n = queue.pop(0)
        order.append(by_name[n])
        for nxt in edges[n]:
            in_deg[nxt] -= 1
            if in_deg[nxt] == 0:
                queue.append(nxt)

    if len(order) != len(steps):
        return None  # cycle
    return order


def _level_sort(steps: list[Step]) -> list[list[Step]] | None:
    """Группирует шаги по level'ам (одинаковая глубина зависимостей)."""
    by_name = {s.name: s for s in steps}
    in_deg = {s.name: 0 for s in steps}
    edges: dict[str, list[str]] = {s.name: [] for s in steps}

    for s in steps:
        for d in _step_deps(s):
            if d in by_name:
                edges[d].append(s.name)
                in_deg[s.name] += 1

    levels: list[list[Step]] = []
    remaining = set(in_deg.keys())
    while remaining:
        current = [n for n in remaining if in_deg[n] == 0]
        if not current:
            return None  # cycle
        current.sort()
        levels.append([by_name[n] for n in current])
        for n in current:
            remaining.discard(n)
            for nxt in edges[n]:
                in_deg[nxt] -= 1
    return levels
