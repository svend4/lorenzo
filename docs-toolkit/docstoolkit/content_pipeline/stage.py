"""Stage primitives for the E65 Content Pipeline module."""
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class StageType(Enum):
    """Logical stage category within a content pipeline."""
    INGESTION = "ingestion"
    PROCESSING = "processing"
    ENRICHMENT = "enrichment"
    VALIDATION = "validation"
    OUTPUT = "output"


@dataclass
class StageResult:
    """Result metadata for a single content pipeline stage execution."""
    stage_name: str
    stage_type: StageType
    input_count: int
    output_count: int
    errors: list[str] = field(default_factory=list)
    duration_ms: float = 0.0
    metadata: dict = field(default_factory=dict)

    def success_rate(self) -> float:
        """Fraction of input items that were successfully passed through.

        Returns 1.0 when input_count is 0 (nothing to process = full success).
        """
        if self.input_count == 0:
            return 1.0
        return self.output_count / self.input_count

    def has_errors(self) -> bool:
        """True when at least one error was recorded."""
        return bool(self.errors)


class ContentStage(ABC):
    """Abstract base class for all content pipeline stages."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable stage name."""

    @property
    @abstractmethod
    def stage_type(self) -> StageType:
        """Logical stage category."""

    @abstractmethod
    def process(self, items: list) -> tuple[list, StageResult]:
        """Process *items* and return (output_items, StageResult)."""
