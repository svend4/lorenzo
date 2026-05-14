"""Tests for E65 Content Pipeline module — 75+ test cases."""
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.content_pipeline import (
    StageType,
    StageResult,
    ContentStage,
    FilterStage,
    TransformStage,
    DeduplicationStage,
    ValidationStage,
    EnrichmentStage,
    PipelineConfig,
    PipelineRun,
    ContentPipeline,
)


# ---------------------------------------------------------------------------
# StageType
# ---------------------------------------------------------------------------

class TestStageType:
    def test_all_members_exist(self):
        members = {e.name for e in StageType}
        assert members == {"INGESTION", "PROCESSING", "ENRICHMENT", "VALIDATION", "OUTPUT"}

    def test_values_are_strings(self):
        for member in StageType:
            assert isinstance(member.value, str)


# ---------------------------------------------------------------------------
# StageResult
# ---------------------------------------------------------------------------

class TestStageResult:
    def _make(self, input_count=10, output_count=10, errors=None):
        return StageResult(
            stage_name="s",
            stage_type=StageType.PROCESSING,
            input_count=input_count,
            output_count=output_count,
            errors=errors or [],
        )

    def test_basic_fields(self):
        sr = StageResult("s", StageType.INGESTION, 5, 3)
        assert sr.stage_name == "s"
        assert sr.stage_type == StageType.INGESTION
        assert sr.input_count == 5
        assert sr.output_count == 3

    def test_errors_default_empty(self):
        sr = self._make()
        assert sr.errors == []

    def test_metadata_default_empty(self):
        sr = self._make()
        assert sr.metadata == {}

    def test_duration_ms_default_zero(self):
        sr = self._make()
        assert sr.duration_ms == 0.0

    def test_success_rate_full(self):
        sr = self._make(input_count=10, output_count=10)
        assert sr.success_rate() == pytest.approx(1.0)

    def test_success_rate_partial(self):
        sr = self._make(input_count=10, output_count=5)
        assert sr.success_rate() == pytest.approx(0.5)

    def test_success_rate_zero_output(self):
        sr = self._make(input_count=10, output_count=0)
        assert sr.success_rate() == pytest.approx(0.0)

    def test_success_rate_zero_input_returns_one(self):
        sr = self._make(input_count=0, output_count=0)
        assert sr.success_rate() == pytest.approx(1.0)

    def test_success_rate_returns_float(self):
        sr = self._make(input_count=4, output_count=3)
        assert isinstance(sr.success_rate(), float)

    def test_has_errors_false_when_empty(self):
        sr = self._make()
        assert sr.has_errors() is False

    def test_has_errors_true_when_present(self):
        sr = self._make(errors=["oops"])
        assert sr.has_errors() is True

    def test_has_errors_multiple(self):
        sr = self._make(errors=["e1", "e2", "e3"])
        assert sr.has_errors() is True

    def test_metadata_stored(self):
        sr = StageResult("s", StageType.OUTPUT, 1, 1, metadata={"key": "val"})
        assert sr.metadata["key"] == "val"

    def test_success_rate_over_100_percent_possible(self):
        # enrichment might duplicate items
        sr = self._make(input_count=5, output_count=10)
        assert sr.success_rate() == pytest.approx(2.0)


# ---------------------------------------------------------------------------
# ContentStage ABC
# ---------------------------------------------------------------------------

class TestContentStageABC:
    def test_cannot_instantiate_abstract(self):
        with pytest.raises(TypeError):
            ContentStage()

    def test_concrete_subclass_works(self):
        class MyStage(ContentStage):
            @property
            def name(self):
                return "my"

            @property
            def stage_type(self):
                return StageType.PROCESSING

            def process(self, items):
                result = StageResult("my", StageType.PROCESSING, len(items), len(items))
                return items, result

        stage = MyStage()
        out, sr = stage.process([1, 2, 3])
        assert out == [1, 2, 3]
        assert sr.stage_name == "my"


# ---------------------------------------------------------------------------
# FilterStage
# ---------------------------------------------------------------------------

class TestFilterStage:
    def test_keeps_matching_items(self):
        stage = FilterStage("even", lambda x: x % 2 == 0)
        out, sr = stage.process([1, 2, 3, 4, 5, 6])
        assert out == [2, 4, 6]

    def test_rejects_non_matching(self):
        stage = FilterStage("pos", lambda x: x > 0)
        out, sr = stage.process([-1, 0, 1, 2])
        assert out == [1, 2]

    def test_empty_input(self):
        stage = FilterStage("f", lambda x: True)
        out, sr = stage.process([])
        assert out == []
        assert sr.input_count == 0
        assert sr.output_count == 0

    def test_all_pass(self):
        stage = FilterStage("all", lambda x: True)
        items = [1, 2, 3]
        out, sr = stage.process(items)
        assert out == items
        assert sr.output_count == 3

    def test_none_pass(self):
        stage = FilterStage("none", lambda x: False)
        out, sr = stage.process([1, 2, 3])
        assert out == []
        assert sr.output_count == 0

    def test_stage_result_counts(self):
        stage = FilterStage("f", lambda x: x > 2)
        out, sr = stage.process([1, 2, 3, 4])
        assert sr.input_count == 4
        assert sr.output_count == 2

    def test_stage_type_is_processing(self):
        stage = FilterStage("f", lambda x: True)
        assert stage.stage_type == StageType.PROCESSING

    def test_name_property(self):
        stage = FilterStage("my-filter", lambda x: True)
        assert stage.name == "my-filter"

    def test_predicate_exception_drops_item_silently(self):
        def bad_pred(x):
            if x == 2:
                raise ValueError("boom")
            return True
        stage = FilterStage("safe", bad_pred)
        out, sr = stage.process([1, 2, 3])
        assert 2 not in out
        assert out == [1, 3]

    def test_no_errors_in_result(self):
        stage = FilterStage("f", lambda x: True)
        _, sr = stage.process([1, 2])
        assert not sr.has_errors()

    def test_duration_ms_set(self):
        stage = FilterStage("f", lambda x: True)
        _, sr = stage.process(list(range(100)))
        assert sr.duration_ms >= 0.0


# ---------------------------------------------------------------------------
# TransformStage
# ---------------------------------------------------------------------------

class TestTransformStage:
    def test_applies_transform(self):
        stage = TransformStage("double", lambda x: x * 2)
        out, sr = stage.process([1, 2, 3])
        assert out == [2, 4, 6]

    def test_skips_on_exception(self):
        def bad_transform(x):
            if x == 2:
                raise ValueError("bad")
            return x * 10
        stage = TransformStage("t", bad_transform)
        out, sr = stage.process([1, 2, 3])
        assert out == [10, 30]
        assert sr.output_count == 2

    def test_exception_recorded_in_errors(self):
        def boom(x):
            raise RuntimeError("kaboom")
        stage = TransformStage("t", boom)
        out, sr = stage.process([1])
        assert sr.has_errors()
        assert "RuntimeError" in sr.errors[0]

    def test_empty_input(self):
        stage = TransformStage("t", lambda x: x)
        out, sr = stage.process([])
        assert out == []
        assert sr.input_count == 0
        assert sr.output_count == 0

    def test_stage_type_is_processing(self):
        stage = TransformStage("t", lambda x: x)
        assert stage.stage_type == StageType.PROCESSING

    def test_name_property(self):
        stage = TransformStage("my-transform", lambda x: x)
        assert stage.name == "my-transform"

    def test_all_fail_gives_empty_output(self):
        stage = TransformStage("t", lambda x: 1 / 0)
        out, sr = stage.process([1, 2, 3])
        assert out == []
        assert len(sr.errors) == 3

    def test_transform_to_dict(self):
        stage = TransformStage("wrap", lambda x: {"val": x})
        out, _ = stage.process([1, 2])
        assert out == [{"val": 1}, {"val": 2}]

    def test_duration_ms_set(self):
        stage = TransformStage("t", lambda x: x)
        _, sr = stage.process([1, 2, 3])
        assert sr.duration_ms >= 0.0


# ---------------------------------------------------------------------------
# DeduplicationStage
# ---------------------------------------------------------------------------

class TestDeduplicationStage:
    def test_removes_exact_duplicates(self):
        stage = DeduplicationStage("dedup")
        out, sr = stage.process([1, 2, 2, 3, 1])
        assert out == [1, 2, 3]

    def test_keeps_first_occurrence(self):
        stage = DeduplicationStage("dedup")
        out, _ = stage.process(["a", "b", "a", "c"])
        assert out == ["a", "b", "c"]

    def test_no_duplicates_unchanged(self):
        stage = DeduplicationStage("dedup")
        items = [1, 2, 3]
        out, sr = stage.process(items)
        assert out == items

    def test_empty_input(self):
        stage = DeduplicationStage("dedup")
        out, sr = stage.process([])
        assert out == []
        assert sr.output_count == 0

    def test_all_same(self):
        stage = DeduplicationStage("dedup")
        out, sr = stage.process([5, 5, 5, 5])
        assert out == [5]
        assert sr.output_count == 1

    def test_custom_key_fn(self):
        stage = DeduplicationStage("dedup", key_fn=lambda x: x["id"])
        items = [{"id": 1, "v": "a"}, {"id": 2, "v": "b"}, {"id": 1, "v": "c"}]
        out, _ = stage.process(items)
        assert len(out) == 2
        assert out[0]["id"] == 1
        assert out[1]["id"] == 2

    def test_custom_key_fn_keeps_first(self):
        stage = DeduplicationStage("dedup", key_fn=lambda x: x % 3)
        out, _ = stage.process([0, 1, 2, 3, 4, 5])
        # keys: 0,1,2,0,1,2 → keep first of each: 0,1,2
        assert out == [0, 1, 2]

    def test_stage_type_is_processing(self):
        stage = DeduplicationStage("dedup")
        assert stage.stage_type == StageType.PROCESSING

    def test_name_property(self):
        stage = DeduplicationStage("my-dedup")
        assert stage.name == "my-dedup"

    def test_counts_correct(self):
        stage = DeduplicationStage("dedup")
        _, sr = stage.process([1, 1, 2, 2, 3])
        assert sr.input_count == 5
        assert sr.output_count == 3

    def test_no_errors(self):
        stage = DeduplicationStage("dedup")
        _, sr = stage.process([1, 2, 3])
        assert not sr.has_errors()


# ---------------------------------------------------------------------------
# ValidationStage
# ---------------------------------------------------------------------------

class TestValidationStage:
    def test_valid_items_pass_through(self):
        stage = ValidationStage("val", lambda x: x > 0)
        out, sr = stage.process([1, 2, 3])
        assert out == [1, 2, 3]

    def test_invalid_items_rejected(self):
        stage = ValidationStage("val", lambda x: x > 0)
        out, sr = stage.process([-1, 0, 1, 2])
        assert out == [1, 2]

    def test_invalid_item_error_message_recorded(self):
        stage = ValidationStage("val", lambda x: x > 0)
        _, sr = stage.process([-1])
        assert sr.has_errors()
        assert len(sr.errors) == 1

    def test_validator_exception_recorded_as_error(self):
        def boom(x):
            raise ValueError("invalid!")
        stage = ValidationStage("val", boom)
        out, sr = stage.process([1])
        assert out == []
        assert sr.has_errors()
        assert "ValueError" in sr.errors[0]

    def test_empty_input(self):
        stage = ValidationStage("val", lambda x: True)
        out, sr = stage.process([])
        assert out == []
        assert sr.input_count == 0

    def test_all_valid(self):
        stage = ValidationStage("val", lambda x: True)
        out, sr = stage.process([1, 2, 3])
        assert out == [1, 2, 3]
        assert not sr.has_errors()

    def test_all_invalid(self):
        stage = ValidationStage("val", lambda x: False)
        out, sr = stage.process([1, 2, 3])
        assert out == []
        assert len(sr.errors) == 3

    def test_stage_type_is_validation(self):
        stage = ValidationStage("val", lambda x: True)
        assert stage.stage_type == StageType.VALIDATION

    def test_name_property(self):
        stage = ValidationStage("my-validator", lambda x: True)
        assert stage.name == "my-validator"

    def test_counts_correct(self):
        stage = ValidationStage("val", lambda x: x % 2 == 0)
        _, sr = stage.process([1, 2, 3, 4])
        assert sr.input_count == 4
        assert sr.output_count == 2

    def test_error_message_contains_item_repr(self):
        stage = ValidationStage("val", lambda x: False)
        _, sr = stage.process(["bad_item"])
        assert "bad_item" in sr.errors[0]


# ---------------------------------------------------------------------------
# EnrichmentStage
# ---------------------------------------------------------------------------

class TestEnrichmentStage:
    def test_enriches_items(self):
        stage = EnrichmentStage("enrich", lambda x: {**x, "extra": True})
        out, _ = stage.process([{"a": 1}, {"a": 2}])
        assert all(item["extra"] is True for item in out)

    def test_keeps_original_on_exception(self):
        def bad_enrich(x):
            if x.get("fail"):
                raise RuntimeError("boom")
            return {**x, "ok": True}
        stage = EnrichmentStage("enrich", bad_enrich)
        items = [{"fail": True, "id": 1}, {"id": 2}]
        out, sr = stage.process(items)
        assert len(out) == 2
        assert out[0] == {"fail": True, "id": 1}  # original kept
        assert out[1]["ok"] is True

    def test_error_recorded_on_exception(self):
        stage = EnrichmentStage("enrich", lambda x: 1 / 0)
        _, sr = stage.process([1])
        assert sr.has_errors()
        assert "ZeroDivisionError" in sr.errors[0]

    def test_output_count_equals_input_count(self):
        stage = EnrichmentStage("enrich", lambda x: x)
        _, sr = stage.process([1, 2, 3])
        assert sr.output_count == sr.input_count

    def test_output_count_equals_input_even_on_failure(self):
        stage = EnrichmentStage("enrich", lambda x: 1 / 0)
        out, sr = stage.process([1, 2, 3])
        assert len(out) == 3  # originals kept
        assert sr.output_count == 3

    def test_empty_input(self):
        stage = EnrichmentStage("enrich", lambda x: x)
        out, sr = stage.process([])
        assert out == []
        assert sr.input_count == 0

    def test_stage_type_is_enrichment(self):
        stage = EnrichmentStage("enrich", lambda x: x)
        assert stage.stage_type == StageType.ENRICHMENT

    def test_name_property(self):
        stage = EnrichmentStage("my-enricher", lambda x: x)
        assert stage.name == "my-enricher"

    def test_no_errors_on_clean_run(self):
        stage = EnrichmentStage("enrich", lambda x: x * 2)
        _, sr = stage.process([1, 2, 3])
        assert not sr.has_errors()


# ---------------------------------------------------------------------------
# PipelineConfig
# ---------------------------------------------------------------------------

class TestPipelineConfig:
    def test_defaults(self):
        cfg = PipelineConfig()
        assert cfg.stop_on_error is False
        assert cfg.min_items == 0

    def test_custom_values(self):
        cfg = PipelineConfig(stop_on_error=True, min_items=5)
        assert cfg.stop_on_error is True
        assert cfg.min_items == 5


# ---------------------------------------------------------------------------
# PipelineRun
# ---------------------------------------------------------------------------

class TestPipelineRun:
    def _make_run(self, stage_results=None, started_at=0.0, finished_at=1.0):
        return PipelineRun(
            pipeline_name="test",
            started_at=started_at,
            finished_at=finished_at,
            stage_results=stage_results or [],
            input_count=10,
            output_count=8,
        )

    def test_duration_ms(self):
        run = self._make_run(started_at=0.0, finished_at=1.0)
        assert run.duration_ms() == pytest.approx(1000.0)

    def test_duration_ms_zero(self):
        run = self._make_run(started_at=5.0, finished_at=5.0)
        assert run.duration_ms() == pytest.approx(0.0)

    def test_total_errors_no_stages(self):
        run = self._make_run()
        assert run.total_errors() == 0

    def test_total_errors_across_stages(self):
        sr1 = StageResult("s1", StageType.PROCESSING, 5, 5, errors=["e1"])
        sr2 = StageResult("s2", StageType.VALIDATION, 5, 4, errors=["e2", "e3"])
        run = self._make_run(stage_results=[sr1, sr2])
        assert run.total_errors() == 3

    def test_total_errors_no_errors(self):
        sr1 = StageResult("s1", StageType.PROCESSING, 5, 5)
        run = self._make_run(stage_results=[sr1])
        assert run.total_errors() == 0

    def test_bottleneck_none_when_no_stages(self):
        run = self._make_run()
        assert run.bottleneck() is None

    def test_bottleneck_single_stage(self):
        sr = StageResult("only", StageType.PROCESSING, 10, 5)
        run = self._make_run(stage_results=[sr])
        assert run.bottleneck() == "only"

    def test_bottleneck_returns_lowest_success_rate(self):
        sr1 = StageResult("s1", StageType.PROCESSING, 10, 9)  # 0.9
        sr2 = StageResult("s2", StageType.VALIDATION, 9, 3)   # 0.33
        sr3 = StageResult("s3", StageType.ENRICHMENT, 3, 3)   # 1.0
        run = self._make_run(stage_results=[sr1, sr2, sr3])
        assert run.bottleneck() == "s2"

    def test_bottleneck_first_when_tied(self):
        sr1 = StageResult("s1", StageType.PROCESSING, 10, 5)  # 0.5
        sr2 = StageResult("s2", StageType.VALIDATION, 10, 5)  # 0.5
        run = self._make_run(stage_results=[sr1, sr2])
        assert run.bottleneck() == "s1"

    def test_stage_results_default_empty(self):
        run = PipelineRun("p", started_at=0.0)
        assert run.stage_results == []

    def test_finished_at_default_zero(self):
        run = PipelineRun("p", started_at=0.0)
        assert run.finished_at == 0.0


# ---------------------------------------------------------------------------
# ContentPipeline — integration
# ---------------------------------------------------------------------------

class TestContentPipeline:
    def test_sequential_stages(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(FilterStage("evens", lambda x: x % 2 == 0))
        pipeline.add_stage(TransformStage("double", lambda x: x * 2))
        out, run = pipeline.run([1, 2, 3, 4, 5])
        assert out == [4, 8]  # evens: [2,4], doubled: [4,8]
        assert len(run.stage_results) == 2

    def test_empty_input(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(FilterStage("f", lambda x: True))
        out, run = pipeline.run([])
        assert out == []
        assert run.input_count == 0
        assert run.output_count == 0

    def test_no_stages(self):
        pipeline = ContentPipeline("test")
        items = [1, 2, 3]
        out, run = pipeline.run(items)
        assert out == items
        assert run.stage_results == []

    def test_single_stage(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(TransformStage("sq", lambda x: x ** 2))
        out, _ = pipeline.run([2, 3, 4])
        assert out == [4, 9, 16]

    def test_pipeline_run_counts(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(FilterStage("f", lambda x: x > 2))
        _, run = pipeline.run([1, 2, 3, 4, 5])
        assert run.input_count == 5
        assert run.output_count == 3

    def test_pipeline_run_name(self):
        pipeline = ContentPipeline("my-pipe")
        _, run = pipeline.run([])
        assert run.pipeline_name == "my-pipe"

    def test_duration_ms_positive(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(FilterStage("f", lambda x: True))
        _, run = pipeline.run(list(range(1000)))
        assert run.duration_ms() >= 0.0

    def test_stop_on_error_halts_pipeline(self):
        cfg = PipelineConfig(stop_on_error=True)
        pipeline = ContentPipeline("test", cfg)
        # ValidationStage will fail on items < 0, generating errors
        pipeline.add_stage(ValidationStage("val", lambda x: x >= 0))
        pipeline.add_stage(TransformStage("double", lambda x: x * 2))
        out, run = pipeline.run([-1, 1, 2])
        # After validation with errors and stop_on_error, pipeline stops
        assert len(run.stage_results) == 1
        assert run.stage_results[0].has_errors()

    def test_stop_on_error_false_continues(self):
        cfg = PipelineConfig(stop_on_error=False)
        pipeline = ContentPipeline("test", cfg)
        pipeline.add_stage(ValidationStage("val", lambda x: x >= 0))
        pipeline.add_stage(TransformStage("double", lambda x: x * 2))
        out, run = pipeline.run([-1, 1, 2])
        # Both stages run
        assert len(run.stage_results) == 2
        assert out == [2, 4]

    def test_min_items_raises_when_below(self):
        cfg = PipelineConfig(min_items=5)
        pipeline = ContentPipeline("test", cfg)
        pipeline.add_stage(FilterStage("f", lambda x: False))  # filters everything
        with pytest.raises(ValueError, match="minimum required"):
            pipeline.run([1, 2, 3])

    def test_min_items_does_not_raise_when_met(self):
        cfg = PipelineConfig(min_items=2)
        pipeline = ContentPipeline("test", cfg)
        pipeline.add_stage(FilterStage("f", lambda x: True))
        out, _ = pipeline.run([1, 2, 3])
        assert len(out) == 3

    def test_min_items_zero_never_raises(self):
        cfg = PipelineConfig(min_items=0)
        pipeline = ContentPipeline("test", cfg)
        pipeline.add_stage(FilterStage("f", lambda x: False))
        out, _ = pipeline.run([1, 2, 3])
        assert out == []

    def test_bottleneck_via_pipeline(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(FilterStage("f", lambda x: x > 3))  # drops 3/5
        pipeline.add_stage(TransformStage("t", lambda x: x))   # keeps all
        _, run = pipeline.run([1, 2, 3, 4, 5])
        # filter: 5 in, 2 out (0.4); transform: 2 in, 2 out (1.0)
        assert run.bottleneck() == "f"

    def test_all_filtered_out(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(FilterStage("f", lambda x: False))
        out, run = pipeline.run([1, 2, 3])
        assert out == []
        assert run.output_count == 0

    def test_dedup_in_pipeline(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(DeduplicationStage("dedup"))
        out, _ = pipeline.run([1, 2, 2, 3, 1])
        assert out == [1, 2, 3]

    def test_enrichment_in_pipeline(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(EnrichmentStage("enrich", lambda x: x + 100))
        out, _ = pipeline.run([1, 2, 3])
        assert out == [101, 102, 103]

    def test_total_errors_across_pipeline(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(TransformStage("t", lambda x: 1 / 0))  # all fail
        _, run = pipeline.run([1, 2, 3])
        assert run.total_errors() == 3

    def test_stage_results_length_matches_executed_stages(self):
        pipeline = ContentPipeline("test")
        for i in range(5):
            pipeline.add_stage(TransformStage(f"t{i}", lambda x: x))
        _, run = pipeline.run([1, 2, 3])
        assert len(run.stage_results) == 5

    def test_multiple_dedup_and_filter(self):
        pipeline = ContentPipeline("test")
        pipeline.add_stage(DeduplicationStage("dedup"))
        pipeline.add_stage(FilterStage("pos", lambda x: x > 0))
        out, run = pipeline.run([1, -1, 2, 2, -3, 3])
        assert out == [1, 2, 3]

    def test_config_defaults_used_when_none(self):
        pipeline = ContentPipeline("test")
        # Should not raise even when no items pass filter
        pipeline.add_stage(FilterStage("f", lambda x: False))
        out, _ = pipeline.run([1, 2])
        assert out == []

    def test_pipeline_run_started_at_set(self):
        before = time.monotonic()
        pipeline = ContentPipeline("test")
        _, run = pipeline.run([])
        after = time.monotonic()
        assert before <= run.started_at <= after

    def test_pipeline_run_finished_at_set(self):
        pipeline = ContentPipeline("test")
        _, run = pipeline.run([1, 2, 3])
        assert run.finished_at >= run.started_at
