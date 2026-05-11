"""Tests for scripts/improve_crossrefs.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_crossrefs")


def test_projects_list_exists():
    assert hasattr(mod, "PROJECTS")
    assert isinstance(mod.PROJECTS, list)
    assert len(mod.PROJECTS) > 0


def test_projects_contains_known():
    assert "Svyazi" in mod.PROJECTS
    assert "AgentFS" in mod.PROJECTS


def test_build_index_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nSvyazi and AgentFS are great projects.", encoding="utf-8")
    result = mod.build_index()
    assert isinstance(result, dict)


def test_build_index_finds_projects(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("Using Svyazi and Yodoca in this project.", encoding="utf-8")
    result = mod.build_index()
    assert "Svyazi" in result or "Yodoca" in result


def test_build_index_case_insensitive(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("svyazi is the main project here.", encoding="utf-8")
    result = mod.build_index()
    assert "Svyazi" in result


def test_build_file_map_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("Using Svyazi and AgentFS together.", encoding="utf-8")
    result = mod.build_file_map()
    assert isinstance(result, dict)


def test_build_file_map_maps_files_to_projects(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("Using Svyazi in this file.", encoding="utf-8")
    result = mod.build_file_map()
    all_projects = []
    for projects in result.values():
        all_projects.extend(projects)
    assert "Svyazi" in all_projects
