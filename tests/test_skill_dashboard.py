"""Tests for scripts/improve_skill_dashboard.py."""

import importlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_skill_dashboard")


def test_log_path_attribute():
    assert hasattr(mod, "LOG_PATH")


def test_skills_dir_attribute():
    assert hasattr(mod, "SKILLS_DIR")


def test_out_path_attribute():
    assert hasattr(mod, "OUT")


def test_out_path_is_md_file():
    assert str(mod.OUT).endswith(".md")


def test_main_creates_file_no_log(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    (skills_dir / "analyze-project.md").write_text("# Analyze", encoding="utf-8")
    out = tmp_path / "docs" / "SKILL_DASHBOARD.md"
    (tmp_path / "docs").mkdir()
    monkeypatch.setattr(mod, "LOG_PATH", tmp_path / "missing.jsonl")
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "OUT", out)
    mod.main()
    assert out.exists()


def test_main_output_contains_header(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    out = tmp_path / "docs" / "SKILL_DASHBOARD.md"
    (tmp_path / "docs").mkdir()
    monkeypatch.setattr(mod, "LOG_PATH", tmp_path / "missing.jsonl")
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "OUT", out)
    mod.main()
    content = out.read_text(encoding="utf-8")
    assert "Skill Dashboard" in content


def test_main_with_log(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    skills_dir = tmp_path / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    (skills_dir / "analyze.md").write_text("# Analyze", encoding="utf-8")
    log_path = tmp_path / "skill_metrics.jsonl"
    now = datetime.now().isoformat()
    entries = [
        {"skill": "analyze", "ts": now, "helpful": 4, "complete": 5},
        {"skill": "analyze", "ts": now, "helpful": 3, "complete": 4},
    ]
    log_path.write_text("\n".join(json.dumps(e) for e in entries), encoding="utf-8")
    out = tmp_path / "docs" / "SKILL_DASHBOARD.md"
    (tmp_path / "docs").mkdir()
    monkeypatch.setattr(mod, "LOG_PATH", log_path)
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "OUT", out)
    mod.main()
    assert out.exists()
    content = out.read_text(encoding="utf-8")
    assert "analyze" in content


def test_main_without_skills_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    out = tmp_path / "docs" / "SKILL_DASHBOARD.md"
    (tmp_path / "docs").mkdir()
    monkeypatch.setattr(mod, "LOG_PATH", tmp_path / "missing.jsonl")
    monkeypatch.setattr(mod, "SKILLS_DIR", tmp_path / "nonexistent")
    monkeypatch.setattr(mod, "OUT", out)
    mod.main()
    assert out.exists()
