"""E50 Data Pipeline module for docs-toolkit.

Provides a composable, stdlib-only data pipeline framework with:
  - StageResult / PipelineStage / FilterStage / TransformStage / AggregateStage
  - PipelineConfig / PipelineRun / DataPipeline

Usage::

    from docstoolkit.data_pipeline import DataPipeline, FilterStage, TransformStage

    pipeline = DataPipeline("my-pipe")
    pipeline.add_stage(FilterStage("drop-empty", lambda r: bool(r.get("text"))))
    pipeline.add_stage(TransformStage("upper", lambda r: {**r, "text": r["text"].upper()}))
    run = pipeline.run([{"text": "hello"}, {"text": ""}])
"""
from docstoolkit.data_pipeline.stage import (
    StageResult,
    PipelineStage,
    FilterStage,
    TransformStage,
    AggregateStage,
)
from docstoolkit.data_pipeline.pipeline import (
    PipelineConfig,
    PipelineRun,
    DataPipeline,
)

__all__ = [
    "StageResult",
    "PipelineStage",
    "FilterStage",
    "TransformStage",
    "AggregateStage",
    "PipelineConfig",
    "PipelineRun",
    "DataPipeline",
]
