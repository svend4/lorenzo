"""text_pipeline — composable text processing pipeline (pure stdlib)."""
from docstoolkit.text_pipeline.pipeline import (
    PipelineResult,
    PipelineStep,
    StepOutput,
    TextPipeline,
)

__all__ = [
    "PipelineStep",
    "StepOutput",
    "PipelineResult",
    "TextPipeline",
]
