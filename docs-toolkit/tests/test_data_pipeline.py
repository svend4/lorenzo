"""Tests for E50 Data Pipeline module — 65+ test cases."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.data_pipeline import (
    StageResult,
    PipelineStage,
    FilterStage,
    TransformStage,
    AggregateStage,
    PipelineConfig,
    PipelineRun,
    DataPipeline,
)


# ---------------------------------------------------------------------------
# StageResult
# ---------------------------------------------------------------------------

class TestStageResult:
    def test_basic_fields(self):
        sr = StageResult("s1", 100, 80, 500.0)
        assert sr.stage_name == "s1"
        assert sr.records_in == 100
        assert sr.records_out == 80
        assert sr.duration_ms == 500.0
        assert sr.errors == []

    def test_errors_default_empty_list(self):
        sr = StageResult("s", 10, 10, 1.0)
        assert isinstance(sr.errors, list)
        assert len(sr.errors) == 0

    def test_errors_field(self):
        sr = StageResult("s", 10, 8, 1.0, errors=["oops"])
        assert sr.errors == ["oops"]

    def test_throughput_basic(self):
        # 1000 records in 1000 ms → ~1000 rec/s
        sr = StageResult("s", 100, 1000, 1000.0)
        assert abs(sr.throughput() - 1000.0) < 1.0

    def test_throughput_zero_duration(self):
        # duration_ms = 0 → should not raise, throughput very high
        sr = StageResult("s", 100, 50, 0.0)
        assert sr.throughput() > 1e6

    def test_throughput_zero_records_out(self):
        sr = StageResult("s", 100, 0, 100.0)
        assert sr.throughput() == 0.0

    def test_error_rate_no_errors(self):
        sr = StageResult("s", 100, 100, 10.0)
        assert sr.error_rate() == pytest.approx(0.0, abs=1e-9)

    def test_error_rate_some_errors(self):
        sr = StageResult("s", 100, 95, 10.0, errors=["e1", "e2"])
        # 2 / (100 + 1e-10) ≈ 0.02
        assert sr.error_rate() == pytest.approx(0.02, rel=1e-5)

    def test_error_rate_zero_records_in(self):
        sr = StageResult("s", 0, 0, 1.0, errors=["e"])
        # 1 / (0 + 1e-10) → very large but should not raise
        assert sr.error_rate() > 1e8

    def test_throughput_returns_float(self):
        sr = StageResult("s", 10, 10, 200.0)
        assert isinstance(sr.throughput(), float)

    def test_error_rate_returns_float(self):
        sr = StageResult("s", 10, 10, 200.0)
        assert isinstance(sr.error_rate(), float)

    def test_multiple_errors_counted(self):
        errors = ["e1", "e2", "e3"]
        sr = StageResult("s", 50, 47, 10.0, errors=errors)
        assert sr.error_rate() == pytest.approx(3 / (50 + 1e-10), rel=1e-5)


# ---------------------------------------------------------------------------
# PipelineStage ABC
# ---------------------------------------------------------------------------

class TestPipelineStageABC:
    def test_cannot_instantiate_abc(self):
        with pytest.raises(TypeError):
            PipelineStage()

    def test_concrete_subclass_must_implement_both_methods(self):
        class Incomplete(PipelineStage):
            def name(self):
                return "incomplete"
            # missing process()
        with pytest.raises(TypeError):
            Incomplete()

    def test_concrete_subclass_works(self):
        class Identity(PipelineStage):
            def name(self):
                return "identity"
            def process(self, records):
                return records
        stage = Identity()
        assert stage.name() == "identity"
        data = [{"a": 1}]
        assert stage.process(data) == data


# ---------------------------------------------------------------------------
# FilterStage
# ---------------------------------------------------------------------------

class TestFilterStage:
    def test_name(self):
        s = FilterStage("my-filter", lambda r: True)
        assert s.name() == "my-filter"

    def test_keeps_all_matching(self):
        s = FilterStage("all", lambda r: True)
        records = [{"x": 1}, {"x": 2}]
        assert s.process(records) == records

    def test_drops_all_non_matching(self):
        s = FilterStage("none", lambda r: False)
        records = [{"x": 1}, {"x": 2}]
        assert s.process(records) == []

    def test_partial_filter(self):
        s = FilterStage("even", lambda r: r["n"] % 2 == 0)
        records = [{"n": i} for i in range(5)]
        out = s.process(records)
        assert [r["n"] for r in out] == [0, 2, 4]

    def test_empty_input(self):
        s = FilterStage("f", lambda r: True)
        assert s.process([]) == []

    def test_predicate_on_missing_key_drops_record(self):
        # predicate raises KeyError → record excluded silently
        s = FilterStage("key-check", lambda r: r["missing_key"] == "x")
        records = [{"a": 1}, {"a": 2}]
        assert s.process(records) == []

    def test_predicate_exception_skips_record(self):
        def bad_pred(r):
            if r.get("fail"):
                raise RuntimeError("boom")
            return True
        s = FilterStage("safe", bad_pred)
        records = [{"fail": True}, {"ok": True}]
        out = s.process(records)
        assert len(out) == 1
        assert out[0] == {"ok": True}

    def test_returns_new_list(self):
        records = [{"a": 1}]
        s = FilterStage("f", lambda r: True)
        out = s.process(records)
        assert out is not records

    def test_filter_on_string_field(self):
        s = FilterStage("name-filter", lambda r: r.get("name", "").startswith("A"))
        records = [{"name": "Alice"}, {"name": "Bob"}, {"name": "Anna"}]
        out = s.process(records)
        assert len(out) == 2
        assert all(r["name"].startswith("A") for r in out)

    def test_filter_preserves_record_content(self):
        s = FilterStage("f", lambda r: r["keep"])
        record = {"keep": True, "data": "hello", "num": 42}
        out = s.process([record])
        assert out[0] == record


# ---------------------------------------------------------------------------
# TransformStage
# ---------------------------------------------------------------------------

class TestTransformStage:
    def test_name(self):
        s = TransformStage("my-transform", lambda r: r)
        assert s.name() == "my-transform"

    def test_identity_transform(self):
        s = TransformStage("id", lambda r: r)
        records = [{"a": 1}, {"b": 2}]
        assert s.process(records) == records

    def test_adds_field(self):
        s = TransformStage("add", lambda r: {**r, "new": "val"})
        records = [{"x": 1}]
        out = s.process(records)
        assert out[0] == {"x": 1, "new": "val"}

    def test_modifies_field(self):
        s = TransformStage("upper", lambda r: {**r, "name": r["name"].upper()})
        records = [{"name": "hello"}]
        out = s.process(records)
        assert out[0]["name"] == "HELLO"

    def test_removes_field(self):
        s = TransformStage("drop", lambda r: {k: v for k, v in r.items() if k != "secret"})
        records = [{"public": "data", "secret": "hidden"}]
        out = s.process(records)
        assert "secret" not in out[0]
        assert "public" in out[0]

    def test_empty_input(self):
        s = TransformStage("t", lambda r: r)
        assert s.process([]) == []

    def test_exception_skips_record(self):
        def bad_transform(r):
            if r.get("fail"):
                raise ValueError("transform error")
            return r
        s = TransformStage("safe", bad_transform)
        records = [{"fail": True}, {"ok": True}]
        out = s.process(records)
        assert len(out) == 1
        assert out[0] == {"ok": True}

    def test_all_exceptions_returns_empty(self):
        s = TransformStage("bad", lambda r: 1 / 0)
        records = [{"a": 1}, {"b": 2}]
        out = s.process(records)
        assert out == []

    def test_multiple_records_all_transformed(self):
        s = TransformStage("double", lambda r: {**r, "v": r["v"] * 2})
        records = [{"v": i} for i in range(5)]
        out = s.process(records)
        assert [r["v"] for r in out] == [0, 2, 4, 6, 8]

    def test_transform_returns_new_dict(self):
        original = {"a": 1}
        s = TransformStage("copy", lambda r: dict(r))
        out = s.process([original])
        assert out[0] == original
        assert out[0] is not original


# ---------------------------------------------------------------------------
# AggregateStage
# ---------------------------------------------------------------------------

class TestAggregateStage:
    def test_name(self):
        s = AggregateStage("agg", "key", "val")
        assert s.name() == "agg"

    def test_sum(self):
        s = AggregateStage("s", "category", "amount", "sum")
        records = [
            {"category": "A", "amount": 10},
            {"category": "A", "amount": 20},
            {"category": "B", "amount": 5},
        ]
        out = s.process(records)
        result = {r["category"]: r["amount"] for r in out}
        assert result["A"] == 30
        assert result["B"] == 5

    def test_count(self):
        s = AggregateStage("c", "group", "val", "count")
        records = [
            {"group": "X", "val": 1},
            {"group": "X", "val": 2},
            {"group": "Y", "val": 3},
        ]
        out = s.process(records)
        result = {r["group"]: r["val"] for r in out}
        assert result["X"] == 2
        assert result["Y"] == 1

    def test_avg(self):
        s = AggregateStage("a", "cat", "score", "avg")
        records = [
            {"cat": "A", "score": 10},
            {"cat": "A", "score": 20},
            {"cat": "B", "score": 15},
        ]
        out = s.process(records)
        result = {r["cat"]: r["score"] for r in out}
        assert result["A"] == pytest.approx(15.0)
        assert result["B"] == pytest.approx(15.0)

    def test_max(self):
        s = AggregateStage("m", "grp", "v", "max")
        records = [
            {"grp": "G", "v": 3},
            {"grp": "G", "v": 7},
            {"grp": "G", "v": 1},
        ]
        out = s.process(records)
        assert out[0]["v"] == 7

    def test_min(self):
        s = AggregateStage("m", "grp", "v", "min")
        records = [
            {"grp": "G", "v": 3},
            {"grp": "G", "v": 7},
            {"grp": "G", "v": 1},
        ]
        out = s.process(records)
        assert out[0]["v"] == 1

    def test_default_agg_func_is_sum(self):
        s = AggregateStage("d", "k", "n")
        records = [{"k": "x", "n": 4}, {"k": "x", "n": 6}]
        out = s.process(records)
        assert out[0]["n"] == 10

    def test_invalid_agg_func_raises(self):
        with pytest.raises(ValueError):
            AggregateStage("bad", "k", "v", "median")

    def test_empty_input(self):
        s = AggregateStage("e", "k", "v", "sum")
        assert s.process([]) == []

    def test_single_record_per_group(self):
        s = AggregateStage("s", "id", "val", "sum")
        records = [{"id": 1, "val": 99}]
        out = s.process(records)
        assert len(out) == 1
        assert out[0]["val"] == 99

    def test_output_has_key_and_agg_fields(self):
        s = AggregateStage("s", "dept", "salary", "sum")
        records = [{"dept": "eng", "salary": 100}]
        out = s.process(records)
        assert "dept" in out[0]
        assert "salary" in out[0]

    def test_groups_correctly(self):
        s = AggregateStage("s", "cat", "n", "count")
        records = [
            {"cat": "A", "n": 1},
            {"cat": "B", "n": 2},
            {"cat": "A", "n": 3},
            {"cat": "C", "n": 4},
            {"cat": "B", "n": 5},
        ]
        out = s.process(records)
        result = {r["cat"]: r["n"] for r in out}
        assert result == {"A": 2, "B": 2, "C": 1}

    def test_missing_agg_field_handled(self):
        # Records without agg_field → None values excluded from aggregation
        s = AggregateStage("s", "k", "v", "sum")
        records = [{"k": "x"}, {"k": "x", "v": 5}]
        out = s.process(records)
        assert out[0]["v"] == 5


# ---------------------------------------------------------------------------
# PipelineConfig
# ---------------------------------------------------------------------------

class TestPipelineConfig:
    def test_defaults(self):
        cfg = PipelineConfig()
        assert cfg.stop_on_error is False
        assert cfg.max_errors == 100

    def test_custom_values(self):
        cfg = PipelineConfig(stop_on_error=True, max_errors=5)
        assert cfg.stop_on_error is True
        assert cfg.max_errors == 5


# ---------------------------------------------------------------------------
# DataPipeline and PipelineRun
# ---------------------------------------------------------------------------

class TestDataPipeline:
    def _make_pipeline(self, name="test"):
        return DataPipeline(name)

    def test_empty_pipeline_runs(self):
        p = self._make_pipeline()
        records = [{"a": 1}]
        run = p.run(records)
        assert run.total_records_in == 1
        assert run.total_records_out == 1
        assert run.stage_results == []

    def test_stage_count_zero_initially(self):
        p = self._make_pipeline()
        assert p.stage_count() == 0

    def test_add_stage_increments_count(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("f", lambda r: True))
        assert p.stage_count() == 1
        p.add_stage(TransformStage("t", lambda r: r))
        assert p.stage_count() == 2

    def test_single_filter_stage(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("positive", lambda r: r["v"] > 0))
        records = [{"v": -1}, {"v": 0}, {"v": 1}, {"v": 2}]
        run = p.run(records)
        assert run.total_records_in == 4
        assert run.total_records_out == 2

    def test_single_transform_stage(self):
        p = self._make_pipeline()
        p.add_stage(TransformStage("double", lambda r: {**r, "v": r["v"] * 2}))
        records = [{"v": 1}, {"v": 2}, {"v": 3}]
        run = p.run(records)
        assert run.total_records_out == 3
        assert run.total_records_in == 3

    def test_sequential_stages(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("pos", lambda r: r["n"] > 0))
        p.add_stage(TransformStage("double", lambda r: {**r, "n": r["n"] * 2}))
        records = [{"n": -1}, {"n": 2}, {"n": 3}]
        run = p.run(records)
        assert run.total_records_in == 3
        assert run.total_records_out == 2

    def test_pipeline_run_has_stage_results(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("f", lambda r: True))
        p.add_stage(TransformStage("t", lambda r: r))
        run = p.run([{"x": 1}])
        assert len(run.stage_results) == 2

    def test_stage_result_names_match(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("alpha", lambda r: True))
        p.add_stage(TransformStage("beta", lambda r: r))
        run = p.run([{"x": 1}])
        names = [sr.stage_name for sr in run.stage_results]
        assert names == ["alpha", "beta"]

    def test_pipeline_run_success_no_errors(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("f", lambda r: True))
        run = p.run([{"x": 1}])
        assert run.success() is True

    def test_pipeline_run_pipeline_name(self):
        p = DataPipeline("my-pipeline")
        run = p.run([])
        assert run.pipeline_name == "my-pipeline"

    def test_pipeline_run_total_duration(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("f", lambda r: True))
        run = p.run([{"x": i} for i in range(100)])
        assert run.total_duration_ms >= 0.0

    def test_bottleneck_single_stage(self):
        p = self._make_pipeline()
        p.add_stage(TransformStage("only", lambda r: r))
        run = p.run([{"x": 1}])
        assert run.bottleneck() == "only"

    def test_bottleneck_none_on_empty_stages(self):
        p = self._make_pipeline()
        run = p.run([{"x": 1}])
        assert run.bottleneck() is None

    def test_pipeline_run_records_in_out(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("half", lambda r: r["n"] % 2 == 0))
        records = [{"n": i} for i in range(10)]
        run = p.run(records)
        assert run.total_records_in == 10
        assert run.total_records_out == 5

    def test_aggregate_stage_in_pipeline(self):
        p = self._make_pipeline()
        p.add_stage(AggregateStage("sum", "dept", "salary", "sum"))
        records = [
            {"dept": "eng", "salary": 100},
            {"dept": "eng", "salary": 200},
            {"dept": "hr", "salary": 50},
        ]
        run = p.run(records)
        assert run.total_records_in == 3
        assert run.total_records_out == 2

    def test_pipeline_config_default(self):
        p = DataPipeline("p")
        assert p._config.stop_on_error is False

    def test_pipeline_config_custom(self):
        cfg = PipelineConfig(stop_on_error=True, max_errors=5)
        p = DataPipeline("p", config=cfg)
        assert p._config.stop_on_error is True

    def test_stage_result_records_in_out_correct(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("filter", lambda r: r["v"] > 3))
        records = [{"v": i} for i in range(6)]
        run = p.run(records)
        sr = run.stage_results[0]
        assert sr.records_in == 6
        assert sr.records_out == 2

    def test_multiple_stages_record_counts(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("f1", lambda r: r["v"] > 1))
        p.add_stage(FilterStage("f2", lambda r: r["v"] > 3))
        records = [{"v": i} for i in range(6)]
        run = p.run(records)
        assert run.stage_results[0].records_in == 6
        assert run.stage_results[0].records_out == 4
        assert run.stage_results[1].records_in == 4
        assert run.stage_results[1].records_out == 2

    def test_run_returns_pipeline_run_type(self):
        p = self._make_pipeline()
        run = p.run([])
        assert isinstance(run, PipelineRun)

    def test_empty_records_through_pipeline(self):
        p = self._make_pipeline()
        p.add_stage(FilterStage("f", lambda r: True))
        p.add_stage(TransformStage("t", lambda r: r))
        run = p.run([])
        assert run.total_records_in == 0
        assert run.total_records_out == 0


# ---------------------------------------------------------------------------
# PipelineRun bottleneck logic
# ---------------------------------------------------------------------------

class TestPipelineRunBottleneck:
    def test_bottleneck_returns_slowest_stage(self):
        # Manually construct a PipelineRun with known throughputs
        # stage A: 10 records in 100ms → ~100 rec/s
        # stage B: 10 records in 1000ms → ~10 rec/s  ← bottleneck
        sr_a = StageResult("fast", 10, 10, 100.0)
        sr_b = StageResult("slow", 10, 10, 1000.0)
        run = PipelineRun("p", [sr_a, sr_b], 10, 10, 1100.0)
        assert run.bottleneck() == "slow"

    def test_bottleneck_with_zero_output(self):
        # stage that produces 0 records → throughput 0 → bottleneck
        sr_a = StageResult("normal", 10, 10, 10.0)
        sr_b = StageResult("zero_out", 10, 0, 1.0)
        run = PipelineRun("p", [sr_a, sr_b], 10, 0, 11.0)
        assert run.bottleneck() == "zero_out"

    def test_success_true_when_no_errors(self):
        sr = StageResult("s", 5, 5, 10.0)
        run = PipelineRun("p", [sr], 5, 5, 10.0)
        assert run.success() is True

    def test_success_false_when_errors_present(self):
        sr = StageResult("s", 5, 4, 10.0, errors=["err"])
        run = PipelineRun("p", [sr], 5, 4, 10.0)
        assert run.success() is False

    def test_success_true_empty_stage_list(self):
        run = PipelineRun("p", [], 0, 0, 0.0)
        assert run.success() is True
