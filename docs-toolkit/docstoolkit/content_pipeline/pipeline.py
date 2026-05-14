"""ContentPipeline orchestrator for the E65 Content Pipeline module."""
import time
from dataclasses import dataclass, field

from docstoolkit.content_pipeline.stage import ContentStage, StageResult


@dataclass
class PipelineConfig:
    """Configuration for ContentPipeline execution."""
    stop_on_error: bool = False
    min_items: int = 0


@dataclass
class PipelineRun:
    """Summary of a complete content pipeline execution."""
    pipeline_name: str
    started_at: float
    finished_at: float = 0.0
    stage_results: list[StageResult] = field(default_factory=list)
    input_count: int = 0
    output_count: int = 0

    def duration_ms(self) -> float:
        """Wall-clock duration of the run in milliseconds."""
        return (self.finished_at - self.started_at) * 1000.0

    def total_errors(self) -> int:
        """Total number of error messages across all stages."""
        return sum(len(sr.errors) for sr in self.stage_results)

    def bottleneck(self) -> "str | None":
        """Return the name of the stage with the lowest success_rate, or None.

        When multiple stages share the same (minimum) success_rate the first
        one in execution order is returned.
        """
        if not self.stage_results:
            return None
        worst = min(self.stage_results, key=lambda sr: sr.success_rate())
        return worst.stage_name


class ContentPipeline:
    """Sequential content pipeline that passes items through ordered stages."""

    def __init__(self, name: str, config: PipelineConfig = None):
        self._name = name
        self._config = config or PipelineConfig()
        self._stages: list[ContentStage] = []

    def add_stage(self, stage: ContentStage) -> None:
        """Append *stage* to the pipeline."""
        self._stages.append(stage)

    def run(self, items: list) -> tuple[list, PipelineRun]:
        """Execute all stages sequentially.

        Returns ``(output_items, PipelineRun)``.

        Raises ``ValueError`` when the final item count is less than
        ``config.min_items`` (checked after all stages have run, or after
        early-stop).
        """
        started_at = time.monotonic()
        run = PipelineRun(
            pipeline_name=self._name,
            started_at=started_at,
            input_count=len(items),
        )
        current = list(items)

        for stage in self._stages:
            stage_start = time.monotonic()
            output, result = stage.process(current)
            result.duration_ms = (time.monotonic() - stage_start) * 1000.0
            run.stage_results.append(result)

            if result.has_errors() and self._config.stop_on_error:
                current = output
                break

            current = output

        run.finished_at = time.monotonic()
        run.output_count = len(current)

        if len(current) < self._config.min_items:
            raise ValueError(
                f"Pipeline '{self._name}' produced {len(current)} items, "
                f"minimum required is {self._config.min_items}"
            )

        return current, run
