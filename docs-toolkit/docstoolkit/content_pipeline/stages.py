"""Concrete stage implementations for the E65 Content Pipeline module."""
import time

from docstoolkit.content_pipeline.stage import ContentStage, StageResult, StageType


class FilterStage(ContentStage):
    """Keep only items for which ``predicate(item)`` is True."""

    def __init__(self, name: str, predicate):
        self._name = name
        self._predicate = predicate

    @property
    def name(self) -> str:
        return self._name

    @property
    def stage_type(self) -> StageType:
        return StageType.PROCESSING

    def process(self, items: list) -> tuple[list, StageResult]:
        start = time.monotonic()
        kept = []
        for item in items:
            try:
                if self._predicate(item):
                    kept.append(item)
            except Exception:
                pass  # predicate errors silently drop the item
        duration_ms = (time.monotonic() - start) * 1000.0
        result = StageResult(
            stage_name=self._name,
            stage_type=self.stage_type,
            input_count=len(items),
            output_count=len(kept),
            duration_ms=duration_ms,
        )
        return kept, result


class TransformStage(ContentStage):
    """Apply ``transform(item)`` to each item; skip items where transform raises."""

    def __init__(self, name: str, transform):
        self._name = name
        self._transform = transform

    @property
    def name(self) -> str:
        return self._name

    @property
    def stage_type(self) -> StageType:
        return StageType.PROCESSING

    def process(self, items: list) -> tuple[list, StageResult]:
        start = time.monotonic()
        output = []
        errors = []
        for item in items:
            try:
                output.append(self._transform(item))
            except Exception as exc:
                errors.append(f"{type(exc).__name__}: {exc}")
        duration_ms = (time.monotonic() - start) * 1000.0
        result = StageResult(
            stage_name=self._name,
            stage_type=self.stage_type,
            input_count=len(items),
            output_count=len(output),
            errors=errors,
            duration_ms=duration_ms,
        )
        return output, result


class DeduplicationStage(ContentStage):
    """Remove duplicate items.

    Uniqueness is determined by ``key_fn(item)`` when provided, otherwise by
    ``str(item)``.  First occurrence of each key is kept; subsequent ones are
    dropped.
    """

    def __init__(self, name: str, key_fn=None):
        self._name = name
        self._key_fn = key_fn if key_fn is not None else str

    @property
    def name(self) -> str:
        return self._name

    @property
    def stage_type(self) -> StageType:
        return StageType.PROCESSING

    def process(self, items: list) -> tuple[list, StageResult]:
        start = time.monotonic()
        seen = set()
        output = []
        for item in items:
            try:
                key = self._key_fn(item)
            except Exception:
                key = id(item)  # fallback: treat as unique
            if key not in seen:
                seen.add(key)
                output.append(item)
        duration_ms = (time.monotonic() - start) * 1000.0
        result = StageResult(
            stage_name=self._name,
            stage_type=self.stage_type,
            input_count=len(items),
            output_count=len(output),
            duration_ms=duration_ms,
        )
        return output, result


class ValidationStage(ContentStage):
    """Keep valid items; collect error messages for invalid ones.

    ``validator(item)`` should return ``True`` for valid items or raise /
    return ``False`` for invalid ones.  When it raises, the exception message
    is recorded as the error.  When it returns a falsy value the item is
    rejected with a generic message.
    """

    def __init__(self, name: str, validator):
        self._name = name
        self._validator = validator

    @property
    def name(self) -> str:
        return self._name

    @property
    def stage_type(self) -> StageType:
        return StageType.VALIDATION

    def process(self, items: list) -> tuple[list, StageResult]:
        start = time.monotonic()
        output = []
        errors = []
        for item in items:
            try:
                valid = self._validator(item)
                if valid:
                    output.append(item)
                else:
                    errors.append(f"Validation failed for item: {item!r}")
            except Exception as exc:
                errors.append(f"{type(exc).__name__}: {exc}")
        duration_ms = (time.monotonic() - start) * 1000.0
        result = StageResult(
            stage_name=self._name,
            stage_type=self.stage_type,
            input_count=len(items),
            output_count=len(output),
            errors=errors,
            duration_ms=duration_ms,
        )
        return output, result


class EnrichmentStage(ContentStage):
    """Apply ``enricher(item)`` to each item; keep the original on exception."""

    def __init__(self, name: str, enricher):
        self._name = name
        self._enricher = enricher

    @property
    def name(self) -> str:
        return self._name

    @property
    def stage_type(self) -> StageType:
        return StageType.ENRICHMENT

    def process(self, items: list) -> tuple[list, StageResult]:
        start = time.monotonic()
        output = []
        errors = []
        for item in items:
            try:
                output.append(self._enricher(item))
            except Exception as exc:
                errors.append(f"{type(exc).__name__}: {exc}")
                output.append(item)  # keep original on failure
        duration_ms = (time.monotonic() - start) * 1000.0
        result = StageResult(
            stage_name=self._name,
            stage_type=self.stage_type,
            input_count=len(items),
            output_count=len(output),
            errors=errors,
            duration_ms=duration_ms,
        )
        return output, result
