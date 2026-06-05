"""Tests for E279 DocPipelineRunner."""
import threading
from docstoolkit.doc_pipeline_runner import (
    BatchExecution,
    DocPipelineRunner,
    Pipeline,
    PipelineExecution,
    PipelineStep,
    StepExecution,
    StepResult,
)

T0 = 1_700_000_000.0


def _runner() -> DocPipelineRunner:
    return DocPipelineRunner()


def _identity(doc: dict) -> dict:
    return doc


def _upper_title(doc: dict) -> dict:
    return {**doc, "title": doc.get("title", "").upper()}


def _add_tag(doc: dict) -> dict:
    tags = list(doc.get("tags", []))
    tags.append("processed")
    return {**doc, "tags": tags}


def _always_fail(doc: dict) -> dict:
    raise RuntimeError("forced failure")


# ---------------------------------------------------------------------------
# Pipeline registration
# ---------------------------------------------------------------------------


def test_register_pipeline_returns_pipeline():
    r = _runner()
    p = r.register_pipeline("my-pipe")
    assert isinstance(p, Pipeline)


def test_register_pipeline_has_name():
    r = _runner()
    p = r.register_pipeline("my-pipe")
    assert p.name == "my-pipe"


def test_register_pipeline_gets_id():
    r = _runner()
    p = r.register_pipeline("p")
    assert p.pipeline_id.startswith("pipe_")


def test_register_pipeline_two_different_ids():
    r = _runner()
    p1 = r.register_pipeline("a")
    p2 = r.register_pipeline("b")
    assert p1.pipeline_id != p2.pipeline_id


def test_pipelines_list():
    r = _runner()
    r.register_pipeline("a")
    r.register_pipeline("b")
    assert len(r.pipelines()) == 2


def test_total_pipelines_property():
    r = _runner()
    r.register_pipeline("a")
    assert r.total_pipelines == 1


def test_get_pipeline_returns_pipeline():
    r = _runner()
    p = r.register_pipeline("p")
    got = r.get_pipeline(p.pipeline_id)
    assert got is p


def test_get_pipeline_missing_returns_none():
    r = _runner()
    assert r.get_pipeline("no-such") is None


def test_delete_pipeline_returns_true():
    r = _runner()
    p = r.register_pipeline("p")
    assert r.delete_pipeline(p.pipeline_id) is True
    assert r.total_pipelines == 0


def test_delete_pipeline_missing_returns_false():
    r = _runner()
    assert r.delete_pipeline("no-such") is False


# ---------------------------------------------------------------------------
# Step management
# ---------------------------------------------------------------------------


def test_add_step_returns_pipeline_step():
    r = _runner()
    p = r.register_pipeline("p")
    step = r.add_step(p.pipeline_id, "upper", _upper_title)
    assert isinstance(step, PipelineStep)


def test_add_step_name_stored():
    r = _runner()
    p = r.register_pipeline("p")
    step = r.add_step(p.pipeline_id, "tag", _add_tag)
    assert step.name == "tag"


def test_add_step_missing_pipeline_returns_none():
    r = _runner()
    assert r.add_step("no-such", "s", _identity) is None


def test_remove_step_returns_true():
    r = _runner()
    p = r.register_pipeline("p")
    step = r.add_step(p.pipeline_id, "s", _identity)
    assert r.remove_step(p.pipeline_id, step.step_id) is True


def test_remove_step_reduces_count():
    r = _runner()
    p = r.register_pipeline("p")
    step = r.add_step(p.pipeline_id, "s", _identity)
    r.remove_step(p.pipeline_id, step.step_id)
    assert len(r.get_pipeline(p.pipeline_id).steps) == 0


def test_remove_step_missing_returns_false():
    r = _runner()
    p = r.register_pipeline("p")
    assert r.remove_step(p.pipeline_id, "no-step") is False


def test_disable_step_marks_disabled():
    r = _runner()
    p = r.register_pipeline("p")
    step = r.add_step(p.pipeline_id, "s", _identity)
    r.disable_step(p.pipeline_id, step.step_id)
    assert not r.get_pipeline(p.pipeline_id).steps[0].enabled


def test_enable_step_marks_enabled():
    r = _runner()
    p = r.register_pipeline("p")
    step = r.add_step(p.pipeline_id, "s", _identity)
    r.disable_step(p.pipeline_id, step.step_id)
    r.enable_step(p.pipeline_id, step.step_id)
    assert r.get_pipeline(p.pipeline_id).steps[0].enabled


# ---------------------------------------------------------------------------
# execute
# ---------------------------------------------------------------------------


def test_execute_returns_pipeline_execution():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "id", _identity)
    exec_ = r.execute(p.pipeline_id, {"id": "d1"}, doc_id="d1", now=T0)
    assert isinstance(exec_, PipelineExecution)


def test_execute_missing_pipeline_returns_none():
    r = _runner()
    assert r.execute("no-such", {}) is None


def test_execute_success_flag_true():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "id", _identity)
    exec_ = r.execute(p.pipeline_id, {"id": "d1"})
    assert exec_.success is True


def test_execute_steps_executed_list():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "upper", _upper_title)
    r.add_step(p.pipeline_id, "tag", _add_tag)
    exec_ = r.execute(p.pipeline_id, {"title": "hello"})
    assert len(exec_.steps_executed) == 2


def test_execute_step_result_success():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "id", _identity)
    exec_ = r.execute(p.pipeline_id, {})
    assert exec_.steps_executed[0].result == StepResult.SUCCESS


def test_execute_disabled_step_skipped():
    r = _runner()
    p = r.register_pipeline("p")
    step = r.add_step(p.pipeline_id, "s", _identity)
    r.disable_step(p.pipeline_id, step.step_id)
    exec_ = r.execute(p.pipeline_id, {})
    assert exec_.steps_executed[0].result == StepResult.SKIPPED


def test_execute_failing_required_step_marks_failure():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "fail", _always_fail, optional=False)
    exec_ = r.execute(p.pipeline_id, {})
    assert exec_.success is False


def test_execute_failing_optional_step_continues():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "fail", _always_fail, optional=True)
    r.add_step(p.pipeline_id, "id", _identity)
    exec_ = r.execute(p.pipeline_id, {})
    assert exec_.success is True
    assert len(exec_.steps_executed) == 2


def test_execute_failing_step_error_stored():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "fail", _always_fail, optional=True)
    exec_ = r.execute(p.pipeline_id, {})
    se = exec_.steps_executed[0]
    assert se.result == StepResult.FAILURE
    assert "forced failure" in se.error


def test_execute_doc_id_stored():
    r = _runner()
    p = r.register_pipeline("p")
    exec_ = r.execute(p.pipeline_id, {}, doc_id="myDoc")
    assert exec_.doc_id == "myDoc"


def test_execute_increments_total_executions():
    r = _runner()
    p = r.register_pipeline("p")
    r.execute(p.pipeline_id, {})
    r.execute(p.pipeline_id, {})
    assert r.total_executions == 2


def test_execute_total_duration_ms_non_negative():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "id", _identity)
    exec_ = r.execute(p.pipeline_id, {})
    assert exec_.total_duration_ms >= 0.0


def test_execute_pipeline_id_stored():
    r = _runner()
    p = r.register_pipeline("p")
    exec_ = r.execute(p.pipeline_id, {})
    assert exec_.pipeline_id == p.pipeline_id


def test_execute_transforms_doc_through_steps():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "upper", _upper_title)
    r.add_step(p.pipeline_id, "tag", _add_tag)
    exec_ = r.execute(p.pipeline_id, {"title": "hello"})
    last_output = exec_.steps_executed[-1].output
    assert last_output is not None
    # title should have been uppercased by step 1, tags appended by step 2
    assert "HELLO" in str(last_output.get("title", ""))
    assert "processed" in last_output.get("tags", [])


# ---------------------------------------------------------------------------
# execute_batch
# ---------------------------------------------------------------------------


def test_execute_batch_returns_batch_execution():
    r = _runner()
    p = r.register_pipeline("p")
    batch = r.execute_batch(p.pipeline_id, [{"id": "d1"}, {"id": "d2"}])
    assert isinstance(batch, BatchExecution)


def test_execute_batch_total_docs():
    r = _runner()
    p = r.register_pipeline("p")
    batch = r.execute_batch(p.pipeline_id, [{"id": "d1"}, {"id": "d2"}])
    assert batch.total_docs == 2


def test_execute_batch_success_count():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "id", _identity)
    batch = r.execute_batch(p.pipeline_id, [{"id": "d1"}, {"id": "d2"}])
    assert batch.success_count == 2
    assert batch.failure_count == 0


def test_execute_batch_failure_counted():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "fail", _always_fail, optional=False)
    batch = r.execute_batch(p.pipeline_id, [{"id": "d1"}])
    assert batch.failure_count == 1


def test_execute_batch_empty():
    r = _runner()
    p = r.register_pipeline("p")
    batch = r.execute_batch(p.pipeline_id, [])
    assert batch.success_count == 0
    assert batch.total_docs == 0


def test_execute_batch_missing_pipeline():
    r = _runner()
    batch = r.execute_batch("no-such", [{"id": "d"}])
    assert batch.total_docs == 1
    assert batch.success_count == 0


def test_execute_batch_parallel():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "id", _identity)
    docs = [{"id": f"d{i}"} for i in range(6)]
    batch = r.execute_batch(p.pipeline_id, docs, parallel=True, max_workers=3)
    assert batch.success_count == 6


def test_execute_batch_doc_id_from_dict():
    r = _runner()
    p = r.register_pipeline("p")
    batch = r.execute_batch(p.pipeline_id, [{"id": "myDoc"}])
    assert batch.executions[0].doc_id == "myDoc"


# ---------------------------------------------------------------------------
# recent_executions / executions_for_pipeline
# ---------------------------------------------------------------------------


def test_recent_executions_returns_latest():
    r = _runner()
    p = r.register_pipeline("p")
    for _ in range(5):
        r.execute(p.pipeline_id, {})
    result = r.recent_executions(3)
    assert len(result) == 3


def test_recent_executions_newest_first():
    r = _runner()
    p = r.register_pipeline("p")
    e1 = r.execute(p.pipeline_id, {}, doc_id="first")
    e2 = r.execute(p.pipeline_id, {}, doc_id="second")
    result = r.recent_executions(2)
    assert result[0].doc_id == e2.doc_id
    assert result[1].doc_id == e1.doc_id


def test_executions_for_pipeline_filters():
    r = _runner()
    p1 = r.register_pipeline("p1")
    p2 = r.register_pipeline("p2")
    r.execute(p1.pipeline_id, {})
    r.execute(p2.pipeline_id, {})
    r.execute(p1.pipeline_id, {})
    result = r.executions_for_pipeline(p1.pipeline_id)
    assert len(result) == 2
    assert all(e.pipeline_id == p1.pipeline_id for e in result)


def test_executions_for_pipeline_with_limit():
    r = _runner()
    p = r.register_pipeline("p")
    for _ in range(5):
        r.execute(p.pipeline_id, {})
    result = r.executions_for_pipeline(p.pipeline_id, limit=2)
    assert len(result) == 2


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


def test_clear_removes_pipelines_and_executions():
    r = _runner()
    p = r.register_pipeline("p")
    r.execute(p.pipeline_id, {})
    r.clear()
    assert r.total_pipelines == 0
    assert r.total_executions == 0


# ---------------------------------------------------------------------------
# Register pipeline with initial steps
# ---------------------------------------------------------------------------


def test_register_pipeline_with_steps():
    r = _runner()
    step = PipelineStep(
        step_id="s1",
        name="upper",
        processor=_upper_title,
    )
    p = r.register_pipeline("p", steps=[step])
    assert len(r.get_pipeline(p.pipeline_id).steps) == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_concurrent_execute():
    r = _runner()
    p = r.register_pipeline("p")
    r.add_step(p.pipeline_id, "id", _identity)
    errors = []

    def worker():
        try:
            for i in range(10):
                r.execute(p.pipeline_id, {"n": i})
        except Exception as exc:
            errors.append(exc)

    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert r.total_executions == 50
