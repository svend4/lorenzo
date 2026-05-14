"""DataPipeline orchestrator for the E50 Data Pipeline module."""
import time
from dataclasses import dataclass, field

from docstoolkit.data_pipeline.stage import PipelineStage, StageResult


@dataclass
class PipelineConfig:
    """Configuration for DataPipeline execution."""
    stop_on_error: bool = False
    max_errors: int = 100


@dataclass
class PipelineRun:
    """Summary of a complete pipeline execution."""
    pipeline_name: str
    stage_results: list
    total_records_in: int
    total_records_out: int
    total_duration_ms: float

    def success(self) -> bool:
        """True when no stage accumulated any errors."""
        return all(len(sr.errors) == 0 for sr in self.stage_results)

    def bottleneck(self):
        """Return the name of the stage with the lowest throughput, or None."""
        if not self.stage_results:
            return None
        slowest = min(self.stage_results, key=lambda sr: sr.throughput())
        return slowest.stage_name


class DataPipeline:
    """Sequential data pipeline that passes records through ordered stages."""

    def __init__(self, name: str, config: PipelineConfig = None):
        self._name = name
        self._config = config or PipelineConfig()
        self._stages: list = []

    def add_stage(self, stage: PipelineStage) -> None:
        """Append a stage to the pipeline."""
        self._stages.append(stage)

    def stage_count(self) -> int:
        """Return the number of registered stages."""
        return len(self._stages)

    def run(self, records: list) -> PipelineRun:
        """Execute all stages sequentially and return a PipelineRun summary."""
        total_start = time.monotonic()
        stage_results = []
        current_records = list(records)
        total_records_in = len(current_records)

        for stage in self._stages:
            records_in = len(current_records)
            stage_errors: list = []
            stage_start = time.monotonic()

            try:
                output_records = stage.process(current_records)
            except Exception as exc:
                output_records = []
                stage_errors.append(f"{type(exc).__name__}: {exc}")

            stage_duration_ms = (time.monotonic() - stage_start) * 1000.0
            result = StageResult(
                stage_name=stage.name(),
                records_in=records_in,
                records_out=len(output_records),
                duration_ms=stage_duration_ms,
                errors=stage_errors,
            )
            stage_results.append(result)

            if stage_errors and self._config.stop_on_error:
                break

            total_errors = sum(len(sr.errors) for sr in stage_results)
            if total_errors >= self._config.max_errors:
                break

            current_records = output_records

        total_duration_ms = (time.monotonic() - total_start) * 1000.0
        return PipelineRun(
            pipeline_name=self._name,
            stage_results=stage_results,
            total_records_in=total_records_in,
            total_records_out=len(current_records),
            total_duration_ms=total_duration_ms,
        )
