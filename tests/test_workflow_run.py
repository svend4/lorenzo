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
