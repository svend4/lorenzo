"""Document summarization pipeline — pure stdlib, no ML dependencies."""
from docstoolkit.summarization.extractor import SentenceScore, ExtractiveSummarizer
from docstoolkit.summarization.abstractive import TemplateConfig, AbstractiveSummarizer
from docstoolkit.summarization.pipeline import (
    SummaryLevel,
    SummaryConfig,
    SummaryResult,
    SummarizationPipeline,
)

__all__ = [
    # extractor
    "SentenceScore",
    "ExtractiveSummarizer",
    # abstractive
    "TemplateConfig",
    "AbstractiveSummarizer",
    # pipeline
    "SummaryLevel",
    "SummaryConfig",
    "SummaryResult",
    "SummarizationPipeline",
]
