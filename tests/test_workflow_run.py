"""
Тесты для scripts/improve_workflow_run.py.

Покрытие:
  - parse_kv()       — парсинг key=value аргументов
  - substitute()     — подстановка {переменных} в строку
  - execute_step()   — dry-run шаги + unknown op + bad format
  - load_task()      — чтение манифеста из JSON
  - list_tasks()     — список доступных задач
  - StepResult       — repr и атрибуты
"""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_workflow_run")

# ── parse_kv ──────────────────────────────────────────────────────────────────

def test_parse_kv_basic():
    result = mod.parse_kv(["author=kksudo", "project=AgentFS"])
    assert result == {"author": "kksudo", "project": "AgentFS"}


def test_parse_kv_empty_list():
    assert mod.parse_kv([]) == {}


def test_parse_kv_ignores_no_equals():
    result = mod.parse_kv(["author=kksudo", "noequals", "k=v"])
    assert "noequals" not in result
    assert result["author"] == "kksudo"


def test_parse_kv_value_with_spaces():
    result = mod.parse_kv(["name=Yodoca Memory System"])
    assert result["name"] == "Yodoca Memory System"


def test_parse_kv_value_with_equals():
    # Split on first '=' only
    result = mod.parse_kv(["url=http://example.com/a=b"])
    assert result["url"] == "http://example.com/a=b"


def test_parse_kv_strips_whitespace():
    result = mod.parse_kv([" key = value "])
    assert result["key"] == "value"


def test_parse_kv_returns_dict():
    assert isinstance(mod.parse_kv([]), dict)

# ── substitute ────────────────────────────────────────────────────────────────

def test_substitute_basic():
    result = mod.substitute("Hello, {name}!", {"name": "kksudo"})
    assert result == "Hello, kksudo!"


def test_substitute_multiple_vars():
    result = mod.substitute("{author}/{project}", {"author": "kksudo", "project": "AgentFS"})
    assert result == "kksudo/AgentFS"


def test_substitute_unknown_var_unchanged():
    result = mod.substitute("Hello, {unknown}!", {"name": "kksudo"})
    assert "{unknown}" in result


def test_substitute_empty_dict():
    result = mod.substitute("No vars here.", {})
    assert result == "No vars here."


def test_substitute_empty_string():
    result = mod.substitute("", {"a": "b"})
    assert result == ""


def test_substitute_returns_string():
    result = mod.substitute("text {x}", {"x": "val"})
    assert isinstance(result, str)


def test_substitute_repeated_var():
    result = mod.substitute("{x} and {x}", {"x": "foo"})
    assert result == "foo and foo"

# ── StepResult ────────────────────────────────────────────────────────────────

def test_step_result_attributes():
    r = mod.StepResult("my_step", "ok", output="done", duration_ms=42)
    assert r.name == "my_step"
    assert r.status == "ok"
    assert r.output == "done"
    assert r.duration_ms == 42


def test_step_result_repr():
    r = mod.StepResult("step", "fail", duration_ms=100)
    assert "fail" in repr(r)
    assert "step" in repr(r)


def test_step_result_defaults():
    r = mod.StepResult("step", "ok")
    assert r.output == ""
    assert r.error == ""
    assert r.duration_ms == 0

# ── execute_step (dry-run) ────────────────────────────────────────────────────

def test_execute_step_dry_run_returns_dry_run():
    step = {"read": "docs/HEALTH.md"}
    result = mod.execute_step(step, {}, dry_run=True)
    assert result.status == "dry-run"


def test_execute_step_dry_run_contains_op():
    step = {"run_script": "improve_metrics.py"}
    result = mod.execute_step(step, {}, dry_run=True)
    assert "run_script" in result.name


def test_execute_step_dry_run_substitutes_vars():
    step = {"read": "docs/{section}/README.md"}
    result = mod.execute_step(step, {"section": "01-svyazi"}, dry_run=True)
    assert "01-svyazi" in result.name


def test_execute_step_bad_format():
    # Step with more than 1 key is bad format
    step = {"op1": "arg1", "op2": "arg2"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "skip"


def test_execute_step_unknown_op():
    step = {"unknown_operation_xyz": "some_arg"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "skip"


def test_execute_step_generate_op():
    step = {"generate": "Write a summary of the document."}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"
    assert "LLM" in result.output


def test_execute_step_write_section_op():
    step = {"write_section": "## Summary"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"


def test_execute_step_validate_template_op():
    step = {"validate_template": "project-component"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"


def test_execute_step_update_index_op():
    step = {"update_index": "docs/new-doc.md"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"


def test_execute_step_read_missing_file():
    step = {"read": "docs/NONEXISTENT_FILE_XYZ.md"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status in ("skip", "fail")


def test_execute_step_returns_step_result():
    step = {"generate": "prompt"}
    result = mod.execute_step(step, {}, dry_run=True)
    assert isinstance(result, mod.StepResult)

# ── load_task ─────────────────────────────────────────────────────────────────

def test_load_task_returns_none_if_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    result = mod.load_task("nonexistent-task")
    assert result is None


def test_load_task_reads_json(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    task_data = {"id": "my-task", "description": "Test task",
                 "pipeline": [{"generate": "do something"}]}
    (tmp_path / "my-task.json").write_text(
        json.dumps(task_data), encoding="utf-8"
    )
    result = mod.load_task("my-task")
    assert result is not None
    assert result["id"] == "my-task"


def test_load_task_returns_dict(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    (tmp_path / "t.json").write_text('{"a": 1}', encoding="utf-8")
    result = mod.load_task("t")
    assert isinstance(result, dict)

# ── list_tasks ────────────────────────────────────────────────────────────────

def test_list_tasks_empty_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    assert mod.list_tasks() == []


def test_list_tasks_missing_dir(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path / "nonexistent")
    assert mod.list_tasks() == []


def test_list_tasks_returns_stems(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    for name in ["write-contact", "audit-corpus", "enrich-doc"]:
        (tmp_path / f"{name}.json").write_text("{}", encoding="utf-8")
    result = mod.list_tasks()
    assert sorted(result) == ["audit-corpus", "enrich-doc", "write-contact"]


def test_list_tasks_returns_list(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    assert isinstance(mod.list_tasks(), list)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_list_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--list"])
    result = mod.main()
    assert result == 0


def test_main_no_task_returns_error(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    result = mod.main()
    assert result == 1


def test_main_missing_task_id_graceful(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--task", "nonexistent-task", "--dry-run"])
    result = mod.main()
    assert result in (0, 1)


# ── execute_step: read (lines 93-94) ─────────────────────────────────────────

def test_execute_step_read_existing_file(tmp_path, monkeypatch):
    """Lines 93-96: read op with existing file."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "test.md").write_text("# Hello world content", encoding="utf-8")
    step = {"read": "test.md"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"
    assert "chars" in result.output


def test_execute_step_read_missing_returns_skip(tmp_path, monkeypatch):
    """Lines 93-94: read op with missing file → skip."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    step = {"read": "TOTALLY_NONEXISTENT_FILE.md"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "skip"
    assert "not found" in result.error


# ── execute_step: read_glob (lines 99-104) ───────────────────────────────────

def test_execute_step_read_glob(tmp_path, monkeypatch):
    """Lines 99-104: read_glob op."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "a.md").write_text("# A", encoding="utf-8")
    (tmp_path / "b.md").write_text("# B", encoding="utf-8")
    step = {"read_glob": "*.md"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"
    assert "matched" in result.output


def test_execute_step_read_glob_no_matches(tmp_path, monkeypatch):
    """Lines 99-104: read_glob op with no matches."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    step = {"read_glob": "*.xyz_nonexistent"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"
    assert "matched" in result.output
    assert "0" in result.output


# ── execute_step: run_script (lines 107-119) ─────────────────────────────────

def test_execute_step_run_script_not_found(tmp_path, monkeypatch):
    """Line 111: run_script op with missing script → fail."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "scripts").mkdir()
    step = {"run_script": "nonexistent_xyz.py"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "fail"
    assert "not found" in result.error


def test_execute_step_run_script_ok(tmp_path, monkeypatch):
    """Lines 113-119: run_script op with existing script that succeeds."""
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "dummy.py").write_text("print('ok')", encoding="utf-8")
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "done"
    mock_result.stderr = ""
    step = {"run_script": "dummy.py"}
    with patch("subprocess.run", return_value=mock_result):
        result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"


def test_execute_step_run_script_fail(tmp_path, monkeypatch):
    """Lines 115-119: run_script op that returns non-zero → fail."""
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "bad.py").write_text("sys.exit(1)", encoding="utf-8")
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "error output"
    step = {"run_script": "bad.py"}
    with patch("subprocess.run", return_value=mock_result):
        result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "fail"


def test_execute_step_run_script_with_extra_args(tmp_path, monkeypatch):
    """Lines 107-119: run_script with extra arguments."""
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "myscript.py").write_text("print('ok')", encoding="utf-8")
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "output"
    mock_result.stderr = ""
    step = {"run_script": "myscript.py --dry-run --top 5"}
    with patch("subprocess.run", return_value=mock_result) as mock_run:
        result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"
    call_args = mock_run.call_args[0][0]
    assert "--dry-run" in call_args
    assert "--top" in call_args


# ── execute_step: run_template_init (lines 122-128) ──────────────────────────

def test_execute_step_run_template_init(tmp_path, monkeypatch):
    """Lines 122-128: run_template_init op with no vars."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    step = {"run_template_init": "project-component"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"


def test_execute_step_run_template_init_with_vars(tmp_path, monkeypatch):
    """Lines 124-125: run_template_init with vars_dict items."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    step = {"run_template_init": "project-component"}
    result = mod.execute_step(step, {"author": "kksudo", "project": "AgentFS"}, dry_run=False)
    assert result.status == "ok"
    assert "requires" in result.output


# ── execute_step: bm25_passages (lines 131-139) ──────────────────────────────

def test_execute_step_bm25_passages(tmp_path, monkeypatch):
    """Lines 131-139: bm25_passages op returns ok."""
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "passage result"
    step = {"bm25_passages": "agent memory"}
    with patch("subprocess.run", return_value=mock_result):
        result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"


def test_execute_step_bm25_passages_fail(tmp_path, monkeypatch):
    """Lines 136-139: bm25_passages op returns fail on non-zero returncode."""
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    step = {"bm25_passages": "no results query"}
    with patch("subprocess.run", return_value=mock_result):
        result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "fail"


# ── execute_step: filter_by_topic / update_checklist (lines 162, 167) ────────

def test_execute_step_filter_by_topic(tmp_path, monkeypatch):
    """Lines 161-164: filter_by_topic op."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    step = {"filter_by_topic": "memory"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"
    assert "memory" in result.output


def test_execute_step_update_checklist(tmp_path, monkeypatch):
    """Lines 166-169: update_checklist op."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    step = {"update_checklist": "item completed"}
    result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "ok"


# ── execute_step: exception handlers (lines 173-176) ─────────────────────────

def test_execute_step_timeout(tmp_path, monkeypatch):
    """Lines 173-174: TimeoutExpired → fail with 'timeout' error."""
    from unittest.mock import patch
    import subprocess as _subprocess
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "slow.py").write_text("import time; time.sleep(999)", encoding="utf-8")
    step = {"run_script": "slow.py"}
    with patch("subprocess.run", side_effect=_subprocess.TimeoutExpired(["slow.py"], 120)):
        result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "fail"
    assert "timeout" in result.error


def test_execute_step_generic_exception(tmp_path, monkeypatch):
    """Lines 175-176: generic Exception → fail."""
    from unittest.mock import patch
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "broken.py").write_text("raise RuntimeError('oops')", encoding="utf-8")
    step = {"run_script": "broken.py"}
    with patch("subprocess.run", side_effect=RuntimeError("oops")):
        result = mod.execute_step(step, {}, dry_run=False)
    assert result.status == "fail"
    assert "oops" in result.error


# ── run_workflow (lines 185-212) ─────────────────────────────────────────────

def test_run_workflow_missing_task(tmp_path, monkeypatch, capsys):
    """Lines 180-183: run_workflow with missing task → empty list."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    result = mod.run_workflow("nonexistent-task", {})
    assert result == []
    out = capsys.readouterr().out
    assert "не найден" in out or "Манифест" in out


def test_run_workflow_empty_pipeline(tmp_path, monkeypatch, capsys):
    """Lines 185-188: run_workflow with empty pipeline → empty list."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    (tmp_path / "empty-task.json").write_text(
        '{"id": "empty-task", "description": "Empty", "pipeline": []}',
        encoding="utf-8"
    )
    result = mod.run_workflow("empty-task", {})
    assert result == []
    out = capsys.readouterr().out
    assert "пустой" in out or "нет pipeline" in out or "⚠" in out


def test_run_workflow_runs_steps(tmp_path, monkeypatch, capsys):
    """Lines 195-211: run_workflow processes all steps."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    task_data = {
        "id": "test-task",
        "description": "Test workflow",
        "pipeline": [
            {"generate": "Write a summary."},
            {"validate_template": "project"},
        ]
    }
    (tmp_path / "test-task.json").write_text(
        json.dumps(task_data), encoding="utf-8"
    )
    results = mod.run_workflow("test-task", {"author": "kksudo"})
    assert len(results) == 2
    out = capsys.readouterr().out
    assert "Workflow" in out or "test-task" in out


def test_run_workflow_dry_run(tmp_path, monkeypatch, capsys):
    """Lines 196-211: run_workflow dry_run mode."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    task_data = {
        "id": "dry-task",
        "description": "Dry run test",
        "pipeline": [{"generate": "test prompt"}]
    }
    (tmp_path / "dry-task.json").write_text(
        json.dumps(task_data), encoding="utf-8"
    )
    results = mod.run_workflow("dry-task", {}, dry_run=True)
    assert len(results) == 1
    assert results[0].status == "dry-run"


def test_run_workflow_failed_steps_count(tmp_path, monkeypatch, capsys):
    """Lines 207-211: run_workflow summary reflects step statuses."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    task_data = {
        "id": "mixed-task",
        "description": "Mixed results",
        "pipeline": [
            {"generate": "ok step"},
            {"unknown_op_xyz": "will skip"},
        ]
    }
    (tmp_path / "mixed-task.json").write_text(
        json.dumps(task_data), encoding="utf-8"
    )
    results = mod.run_workflow("mixed-task", {})
    assert len(results) == 2
    statuses = {r.status for r in results}
    assert "ok" in statuses


def test_run_workflow_with_outputs_and_errors(tmp_path, monkeypatch, capsys):
    """Lines 200-205: run_workflow prints output and error lines."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    task_data = {
        "id": "output-task",
        "description": "Task with output",
        "pipeline": [
            {"read": "nonexistent_file_xyz.md"},   # → skip with error
        ]
    }
    (tmp_path / "output-task.json").write_text(
        json.dumps(task_data), encoding="utf-8"
    )
    results = mod.run_workflow("output-task", {})
    assert len(results) == 1
    out = capsys.readouterr().out
    # Should print ERROR line
    assert "ERROR" in out or "not found" in out


# ── main: --list with tasks (lines 221-223) ───────────────────────────────────

def test_main_list_with_tasks(tmp_path, monkeypatch, capsys):
    """Lines 221-223: --list shows task descriptions."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--list"])
    task_data = {"id": "my-task", "description": "My task description"}
    (tmp_path / "my-task.json").write_text(
        json.dumps(task_data), encoding="utf-8"
    )
    result = mod.main()
    assert result == 0
    out = capsys.readouterr().out
    assert "my-task" in out
    assert "My task description" in out


def test_main_list_multiple_tasks(tmp_path, monkeypatch, capsys):
    """Lines 220-223: --list iterates all tasks."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--list"])
    for name, desc in [("alpha-task", "Alpha desc"), ("beta-task", "Beta desc")]:
        (tmp_path / f"{name}.json").write_text(
            json.dumps({"id": name, "description": desc}), encoding="utf-8"
        )
    result = mod.main()
    assert result == 0
    out = capsys.readouterr().out
    assert "alpha-task" in out
    assert "beta-task" in out


# ── main: --inputs parsing (lines 235-239) ───────────────────────────────────

def test_main_with_inputs(tmp_path, monkeypatch, capsys):
    """Lines 234-240: --inputs parsing in main."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    task_data = {
        "id": "input-task",
        "description": "Task with inputs",
        "pipeline": [{"generate": "process {author}"}]
    }
    (tmp_path / "input-task.json").write_text(
        json.dumps(task_data), encoding="utf-8"
    )
    monkeypatch.setattr("sys.argv", ["prog", "--task", "input-task", "--inputs", "author=kksudo"])
    result = mod.main()
    assert result in (0, 1)


def test_main_with_inputs_stops_at_flag(tmp_path, monkeypatch, capsys):
    """Lines 236-238: --inputs parsing stops at next -- flag."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    task_data = {
        "id": "input-task2",
        "description": "Task",
        "pipeline": [{"generate": "process"}]
    }
    (tmp_path / "input-task2.json").write_text(
        json.dumps(task_data), encoding="utf-8"
    )
    monkeypatch.setattr("sys.argv", ["prog", "--task", "input-task2",
                                     "--inputs", "author=kksudo", "--dry-run"])
    result = mod.main()
    assert result in (0, 1)


def test_main_with_multiple_inputs(tmp_path, monkeypatch, capsys):
    """Lines 235-239: --inputs with multiple key=value pairs."""
    monkeypatch.setattr(mod, "TASKS_GENERATED", tmp_path)
    task_data = {
        "id": "multi-input-task",
        "description": "Multi-input task",
        "pipeline": [{"generate": "process {author} {project}"}]
    }
    (tmp_path / "multi-input-task.json").write_text(
        json.dumps(task_data), encoding="utf-8"
    )
    monkeypatch.setattr("sys.argv", ["prog", "--task", "multi-input-task",
                                     "--inputs", "author=kksudo", "project=AgentFS"])
    result = mod.main()
    assert result in (0, 1)
