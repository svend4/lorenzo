"""E65 Content Pipeline module for docs-toolkit.

Provides a composable, stdlib-only content pipeline framework with:
  - StageType / StageResult / ContentStage (ABC)
  - FilterStage / TransformStage / DeduplicationStage / ValidationStage / EnrichmentStage
  - PipelineConfig / PipelineRun / ContentPipeline

Usage::

    from docstoolkit.content_pipeline import (
        ContentPipeline, FilterStage, TransformStage,
        DeduplicationStage, ValidationStage, EnrichmentStage,
    )

    pipeline = ContentPipeline("my-pipe")
    pipeline.add_stage(FilterStage("drop-empty", lambda x: bool(x.get("text"))))
    pipeline.add_stage(TransformStage("upper", lambda x: {**x, "text": x["text"].upper()}))
    items, run = pipeline.run([{"text": "hello"}, {"text": ""}])
"""
from docstoolkit.content_pipeline.stage import (
    StageType,
    StageResult,
    ContentStage,
)
from docstoolkit.content_pipeline.stages import (
    FilterStage,
    TransformStage,
    DeduplicationStage,
    ValidationStage,
    EnrichmentStage,
)
from docstoolkit.content_pipeline.pipeline import (
    PipelineConfig,
    PipelineRun,
    ContentPipeline,
)

__all__ = [
    "StageType",
    "StageResult",
    "ContentStage",
    "FilterStage",
    "TransformStage",
    "DeduplicationStage",
    "ValidationStage",
    "EnrichmentStage",
    "PipelineConfig",
    "PipelineRun",
    "ContentPipeline",
]
