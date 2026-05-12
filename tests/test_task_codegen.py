"""Тесты для improve_task_codegen.py — YAML парсер и валидация."""
from improve_task_codegen import parse_yaml, validate_manifest


def test_parse_yaml_simple():
    text = """
id: hello
version: 1.0
description: test task
"""
    result = parse_yaml(text)
    assert result['id'] == 'hello'
    assert result['version'] == 1.0
    assert result['description'] == 'test task'


def test_parse_yaml_list():
    text = """
trigger_phrases:
  - "first"
  - "second"
"""
    result = parse_yaml(text)
    assert result['trigger_phrases'] == ['first', 'second']


def test_parse_yaml_nested_dict():
    text = """
inputs:
  author:
    type: string
    required: true
"""
    result = parse_yaml(text)
    assert isinstance(result.get('inputs'), dict)
    assert result['inputs']['author']['type'] == 'string'
    assert result['inputs']['author']['required'] is True


def test_validate_manifest_required():
    errs = validate_manifest({'id': 'foo'}, None)
    assert any('version' in e for e in errs)
    assert any('description' in e for e in errs)


def test_validate_manifest_id_format():
    errs = validate_manifest({
        'id': 'BadID',
        'version': 1.0,
        'description': 'test',
    }, None)
    assert any('kebab-case' in e for e in errs)


def test_validate_manifest_mcp_server():
    errs = validate_manifest({
        'id': 'foo',
        'version': 1.0,
        'description': 'test',
        'mcp_server': 'unknown-server',
    }, None)
    assert any('mcp_server' in e for e in errs)


def test_validate_manifest_clean():
    errs = validate_manifest({
        'id': 'my-task',
        'version': 1.0,
        'description': 'test',
        'mcp_server': 'lorenzo-search',
        'trigger_phrases': ['hello'],
    }, None)
    assert errs == []


# ── main ──────────────────────────────────────────────────────────────────────

import importlib as _importlib
import sys as _sys
_sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent / "scripts"))
_mod = _importlib.import_module("improve_task_codegen")


def test_main_no_tasks_dir_returns_error(tmp_path, monkeypatch):
    monkeypatch.setattr(_mod, "TASKS", tmp_path / "nonexistent-tasks")
    monkeypatch.setattr("sys.argv", ["prog"])
    result = _mod.main()
    assert result == 1


def test_main_list_no_tasks_no_crash(tmp_path, monkeypatch):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    monkeypatch.setattr(_mod, "TASKS", tasks_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--list"])
    result = _mod.main()
    assert result == 0


def test_main_validate_no_tasks_no_crash(tmp_path, monkeypatch):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    monkeypatch.setattr(_mod, "TASKS", tasks_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--validate"])
    result = _mod.main()
    assert result == 0


def _make_task_file(tasks_dir, name="my-task"):
    f = tasks_dir / f"{name}.task.yaml"
    f.write_text(
        f"id: {name}\nversion: 1.0\ndescription: Test task\ntrigger_phrases:\n  - hello\nmcp_server: lorenzo-search\n",
        encoding="utf-8"
    )
    return f


def test_main_dry_run_with_manifest(tmp_path, monkeypatch):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    _make_task_file(tasks_dir)
    monkeypatch.setattr(_mod, "TASKS", tasks_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr(_mod, "SKILLS", skills_dir)
    monkeypatch.setattr(_mod, "GENERATED", tasks_dir / "_generated")
    monkeypatch.setattr("sys.argv", ["prog", "--dry-run"])
    result = _mod.main()
    assert result == 0


def test_main_run_with_manifest(tmp_path, monkeypatch):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    _make_task_file(tasks_dir)
    monkeypatch.setattr(_mod, "TASKS", tasks_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr(_mod, "SKILLS", skills_dir)
    monkeypatch.setattr(_mod, "GENERATED", tasks_dir / "_generated")
    monkeypatch.setattr("sys.argv", ["prog"])
    result = _mod.main()
    assert result == 0


def test_main_task_filter_existing(tmp_path, monkeypatch):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    _make_task_file(tasks_dir, "my-task")
    monkeypatch.setattr(_mod, "TASKS", tasks_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr(_mod, "SKILLS", skills_dir)
    monkeypatch.setattr(_mod, "GENERATED", tasks_dir / "_generated")
    monkeypatch.setattr("sys.argv", ["prog", "--task", "my-task"])
    result = _mod.main()
    assert result == 0


def test_main_task_filter_not_found(tmp_path, monkeypatch):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    _make_task_file(tasks_dir, "my-task")
    monkeypatch.setattr(_mod, "TASKS", tasks_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr(_mod, "SKILLS", tmp_path / "skills")
    monkeypatch.setattr(_mod, "GENERATED", tasks_dir / "_generated")
    monkeypatch.setattr("sys.argv", ["prog", "--task", "nonexistent"])
    result = _mod.main()
    assert result == 1


def test_main_validate_with_errors(tmp_path, monkeypatch, capsys):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    bad = tasks_dir / "bad.task.yaml"
    bad.write_text("id: BAD_ID\n", encoding="utf-8")
    monkeypatch.setattr(_mod, "TASKS", tasks_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--validate"])
    result = _mod.main()
    assert result == 1


def test_gen_skill_skeleton_returns_string():
    manifest = {
        "id": "test-skill",
        "description": "A test skill",
        "trigger_phrases": ["test phrase"],
        "related": {"skills": ["other-skill"]},
    }
    result = _mod.gen_skill_skeleton(manifest)
    assert isinstance(result, str)
    assert "test-skill" in result
    assert "test phrase" in result


def test_gen_index_returns_string():
    manifests = [
        {"id": "task-a", "description": "Task A", "mcp_server": "lorenzo-search",
         "trigger_phrases": ["phrase"], "mcp_tool": "search"},
    ]
    result = _mod.gen_index(manifests)
    assert isinstance(result, str)
    assert "task-a" in result
    assert "TASKS_INDEX" in result


def test_parse_yaml_coerce_types():
    text = """
count: 42
flag: true
ratio: 3.14
nothing: null
"""
    result = parse_yaml(text)
    assert result["count"] == 42
    assert result["flag"] is True
    assert result["ratio"] == 3.14
    assert result["nothing"] is None


def test_parse_yaml_inline_list():
    text = 'tags: [alpha, beta, gamma]\n'
    result = parse_yaml(text)
    assert result["tags"] == ["alpha", "beta", "gamma"]


def test_parse_yaml_quoted_strings():
    text = 'name: "quoted value"\n'
    result = parse_yaml(text)
    assert result["name"] == "quoted value"


def test_parse_yaml_comment_line():
    text = "# This is a comment\nid: test\n"
    result = parse_yaml(text)
    assert result["id"] == "test"


def test_parse_yaml_list_with_nested():
    text = """
pipeline:
  - name: step1
    op: run
"""
    result = parse_yaml(text)
    assert isinstance(result.get("pipeline"), list)
    assert result["pipeline"][0]["name"] == "step1"


def test_load_manifest_from_file(tmp_path):
    f = tmp_path / "test.task.yaml"
    f.write_text("id: my-test\nversion: 1.0\ndescription: hello\n", encoding="utf-8")
    result = _mod.load_manifest(f)
    assert result["id"] == "my-test"


def test_validate_manifest_empty_trigger_phrases():
    errs = validate_manifest({
        "id": "my-task", "version": 1.0, "description": "test",
        "trigger_phrases": []
    }, None)
    assert any("trigger_phrases" in e for e in errs)


def test_validate_manifest_invalid_input_type():
    errs = validate_manifest({
        "id": "my-task", "version": 1.0, "description": "test",
        "inputs": {"q": {"type": "invalid_type"}}
    }, None)
    assert any("inputs" in e for e in errs)


def test_main_skill_already_exists(tmp_path, monkeypatch):
    tasks_dir = tmp_path / "tasks"
    tasks_dir.mkdir()
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    _make_task_file(tasks_dir, "my-task")
    existing_skill = skills_dir / "my-task.md"
    existing_skill.write_text("# Existing skill\n", encoding="utf-8")
    monkeypatch.setattr(_mod, "TASKS", tasks_dir)
    monkeypatch.setattr(_mod, "DOCS", tmp_path)
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    monkeypatch.setattr(_mod, "SKILLS", skills_dir)
    monkeypatch.setattr(_mod, "GENERATED", tasks_dir / "_generated")
    monkeypatch.setattr("sys.argv", ["prog"])
    result = _mod.main()
    assert result == 0
    assert existing_skill.read_text(encoding="utf-8") == "# Existing skill\n"
