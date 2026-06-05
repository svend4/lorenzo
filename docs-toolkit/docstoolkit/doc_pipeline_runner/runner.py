"""DocPipelineRunner — execute named pipelines on document batches with progress tracking."""
from __future__ import annotations

import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional


class StepResult(Enum):
    """Result of a single step execution."""

    SUCCESS = "success"
    FAILURE = "failure"
    SKIPPED = "skipped"


@dataclass
class PipelineStep:
    """A single step in a pipeline."""

    step_id: str
    name: str
    processor: Callable[[dict], dict]
    enabled: bool = True
    optional: bool = False


@dataclass
class Pipeline:
    """A named pipeline composed of steps."""

    pipeline_id: str
    name: str
    steps: list[PipelineStep] = field(default_factory=list)
    description: str = ""


@dataclass
class StepExecution:
    """Outcome of executing a single step."""

    step_id: str
    step_name: str
    result: StepResult
    duration_ms: float = 0.0
    error: Optional[str] = None
    output: Any = None


@dataclass
class PipelineExecution:
    """Record of executing a pipeline on a single document."""

    pipeline_id: str
    doc_id: str
    steps_executed: list[StepExecution] = field(default_factory=list)
    success: bool = False
    started_at: float = 0.0
    completed_at: float = 0.0

    @property
    def total_duration_ms(self) -> float:
        if self.completed_at <= 0 or self.started_at <= 0:
            return sum(s.duration_ms for s in self.steps_executed)
        return max(0.0, (self.completed_at - self.started_at) * 1000.0)


@dataclass
class BatchExecution:
    """Record of executing a pipeline across a batch of documents."""

    pipeline_id: str
    total_docs: int
    executions: list[PipelineExecution] = field(default_factory=list)
    success_count: int = 0
    failure_count: int = 0


class DocPipelineRunner:
    """Runner for registered document pipelines."""

    def __init__(self) -> None:
        self._pipelines: dict[str, Pipeline] = {}
        self._executions: list[PipelineExecution] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Pipeline registration
    # ------------------------------------------------------------------
    def register_pipeline(
        self,
        name: str,
        steps: list[PipelineStep] = None,
        description: str = "",
    ) -> Pipeline:
        pipeline_id = f"pipe_{uuid.uuid4().hex[:12]}"
        pipeline = Pipeline(
            pipeline_id=pipeline_id,
            name=name,
            steps=list(steps) if steps else [],
            description=description,
        )
        with self._lock:
            self._pipelines[pipeline_id] = pipeline
        return pipeline

    def add_step(
        self,
        pipeline_id: str,
        name: str,
        processor: Callable,
        optional: bool = False,
    ) -> Optional[PipelineStep]:
        with self._lock:
            pipeline = self._pipelines.get(pipeline_id)
            if pipeline is None:
                return None
            step = PipelineStep(
                step_id=f"step_{uuid.uuid4().hex[:10]}",
                name=name,
                processor=processor,
                enabled=True,
                optional=optional,
            )
            pipeline.steps.append(step)
            return step

    def remove_step(self, pipeline_id: str, step_id: str) -> bool:
        with self._lock:
            pipeline = self._pipelines.get(pipeline_id)
            if pipeline is None:
                return False
            for idx, step in enumerate(pipeline.steps):
                if step.step_id == step_id:
                    pipeline.steps.pop(idx)
                    return True
            return False

    def enable_step(self, pipeline_id: str, step_id: str) -> bool:
        return self._set_step_enabled(pipeline_id, step_id, True)

    def disable_step(self, pipeline_id: str, step_id: str) -> bool:
        return self._set_step_enabled(pipeline_id, step_id, False)

    def _set_step_enabled(self, pipeline_id: str, step_id: str, enabled: bool) -> bool:
        with self._lock:
            pipeline = self._pipelines.get(pipeline_id)
            if pipeline is None:
                return False
            for step in pipeline.steps:
                if step.step_id == step_id:
                    step.enabled = enabled
                    return True
            return False

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------
    def execute(
        self,
        pipeline_id: str,
        doc: dict,
        doc_id: str = "doc",
        now: Optional[float] = None,
    ) -> Optional[PipelineExecution]:
        with self._lock:
            pipeline = self._pipelines.get(pipeline_id)
            if pipeline is None:
                return None
            steps_snapshot = list(pipeline.steps)

        started = now if now is not None else time.time()
        execution = PipelineExecution(
            pipeline_id=pipeline_id,
            doc_id=doc_id,
            started_at=started,
        )

        current = doc
        success = True
        for step in steps_snapshot:
            if not step.enabled:
                execution.steps_executed.append(
                    StepExecution(
                        step_id=step.step_id,
                        step_name=step.name,
                        result=StepResult.SKIPPED,
                        duration_ms=0.0,
                    )
                )
                continue

            step_start = time.time()
            try:
                output = step.processor(current)
                duration = (time.time() - step_start) * 1000.0
                execution.steps_executed.append(
                    StepExecution(
                        step_id=step.step_id,
                        step_name=step.name,
                        result=StepResult.SUCCESS,
                        duration_ms=duration,
                        output=output,
                    )
                )
                if isinstance(output, dict):
                    current = output
            except Exception as exc:  # pragma: no cover - tested
                duration = (time.time() - step_start) * 1000.0
                execution.steps_executed.append(
                    StepExecution(
                        step_id=step.step_id,
                        step_name=step.name,
                        result=StepResult.FAILURE,
                        duration_ms=duration,
                        error=str(exc),
                    )
                )
                if not step.optional:
                    success = False
                    break

        execution.success = success
        execution.completed_at = time.time()

        with self._lock:
            self._executions.append(execution)
        return execution

    def execute_batch(
        self,
        pipeline_id: str,
        docs: list[dict],
        parallel: bool = False,
        max_workers: int = 4,
        now: Optional[float] = None,
    ) -> BatchExecution:
        batch = BatchExecution(
            pipeline_id=pipeline_id,
            total_docs=len(docs),
        )

        with self._lock:
            pipeline_exists = pipeline_id in self._pipelines
        if not pipeline_exists:
            return batch

        def _run(idx_doc):
            idx, doc = idx_doc
            doc_id = str(doc.get("id", f"doc_{idx}")) if isinstance(doc, dict) else f"doc_{idx}"
            return self.execute(pipeline_id, doc, doc_id=doc_id, now=now)

        items = list(enumerate(docs))

        if parallel and len(items) > 1:
            with ThreadPoolExecutor(max_workers=max(1, max_workers)) as pool:
                results = list(pool.map(_run, items))
        else:
            results = [_run(item) for item in items]

        for execution in results:
            if execution is None:
                continue
            batch.executions.append(execution)
            if execution.success:
                batch.success_count += 1
            else:
                batch.failure_count += 1

        return batch

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def get_pipeline(self, pipeline_id: str) -> Optional[Pipeline]:
        with self._lock:
            return self._pipelines.get(pipeline_id)

    def pipelines(self) -> list[Pipeline]:
        with self._lock:
            return list(self._pipelines.values())

    def delete_pipeline(self, pipeline_id: str) -> bool:
        with self._lock:
            if pipeline_id not in self._pipelines:
                return False
            del self._pipelines[pipeline_id]
            return True

    def recent_executions(self, limit: int = 10) -> list[PipelineExecution]:
        with self._lock:
            if limit is None or limit <= 0:
                return list(reversed(self._executions))
            return list(reversed(self._executions[-limit:]))

    def executions_for_pipeline(
        self, pipeline_id: str, limit: int = None
    ) -> list[PipelineExecution]:
        with self._lock:
            matched = [e for e in self._executions if e.pipeline_id == pipeline_id]
        if limit is not None and limit > 0:
            return matched[-limit:]
        return matched

    @property
    def total_pipelines(self) -> int:
        with self._lock:
            return len(self._pipelines)

    @property
    def total_executions(self) -> int:
        with self._lock:
            return len(self._executions)

    def clear(self) -> None:
        with self._lock:
            self._pipelines.clear()
            self._executions.clear()
