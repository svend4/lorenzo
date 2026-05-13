"""Stage primitives for the E50 Data Pipeline module."""
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class StageResult:
    """Result metadata for a single pipeline stage execution."""
    stage_name: str
    records_in: int
    records_out: int
    duration_ms: float
    errors: list = field(default_factory=list)

    def throughput(self) -> float:
        """Records per second produced by this stage."""
        return self.records_out / (self.duration_ms / 1000.0 + 1e-9)

    def error_rate(self) -> float:
        """Fraction of input records that caused errors."""
        return len(self.errors) / (self.records_in + 1e-10)


class PipelineStage(ABC):
    """Abstract base class for all pipeline stages."""

    @abstractmethod
    def process(self, records: list) -> list:
        """Process a list of record dicts and return transformed records."""

    @abstractmethod
    def name(self) -> str:
        """Return the stage name."""


class FilterStage(PipelineStage):
    """Keep only records for which predicate(record) is True."""

    def __init__(self, name: str, predicate):
        self._name = name
        self._predicate = predicate

    def name(self) -> str:
        return self._name

    def process(self, records: list) -> list:
        result = []
        for record in records:
            try:
                if self._predicate(record):
                    result.append(record)
            except Exception:
                # Predicate errors: exclude the record silently
                pass
        return result


class TransformStage(PipelineStage):
    """Apply transform(record) -> dict to each record."""

    def __init__(self, name: str, transform):
        self._name = name
        self._transform = transform

    def name(self) -> str:
        return self._name

    def process(self, records: list) -> list:
        result = []
        for record in records:
            try:
                transformed = self._transform(record)
                result.append(transformed)
            except Exception:
                # Transform errors: skip the record
                pass
        return result


class AggregateStage(PipelineStage):
    """Group by key_field, aggregate agg_field with agg_func.

    Supported agg_func values: "sum", "count", "avg", "max", "min".
    Output records: one per group with {key_field: key, agg_field: value}.
    """

    SUPPORTED = {"sum", "count", "avg", "max", "min"}

    def __init__(self, name: str, key_field: str, agg_field: str, agg_func: str = "sum"):
        if agg_func not in self.SUPPORTED:
            raise ValueError(f"agg_func must be one of {self.SUPPORTED}, got {agg_func!r}")
        self._name = name
        self._key_field = key_field
        self._agg_field = agg_field
        self._agg_func = agg_func

    def name(self) -> str:
        return self._name

    def process(self, records: list) -> list:
        # Group records by key_field
        groups: dict = {}
        for record in records:
            key = record.get(self._key_field)
            groups.setdefault(key, []).append(record)

        result = []
        for key, group_records in groups.items():
            value = self._aggregate(group_records)
            result.append({self._key_field: key, self._agg_field: value})
        return result

    def _aggregate(self, records: list):
        func = self._agg_func
        values = []
        for r in records:
            v = r.get(self._agg_field)
            if v is not None:
                values.append(v)

        if func == "count":
            return len(records)

        if not values:
            return None

        if func == "sum":
            return sum(values)
        if func == "avg":
            return sum(values) / len(values)
        if func == "max":
            return max(values)
        if func == "min":
            return min(values)
