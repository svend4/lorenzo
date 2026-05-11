"""Tests for scripts/improve_watch.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_watch")


def test_snapshot_returns_dict(tmp_path):
    result = mod._snapshot(tmp_path)
    assert isinstance(result, dict)


def test_snapshot_empty_dir(tmp_path):
    result = mod._snapshot(tmp_path)
    assert result == {}


def test_snapshot_finds_md_files(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Hello", encoding="utf-8")
    result = mod._snapshot(tmp_path)
    assert f in result


def test_snapshot_ignores_non_md(tmp_path):
    py = tmp_path / "script.py"
    py.write_text("print('hello')", encoding="utf-8")
    result = mod._snapshot(tmp_path)
    assert py not in result


def test_snapshot_finds_nested_md(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    f = sub / "nested.md"
    f.write_text("# Nested", encoding="utf-8")
    result = mod._snapshot(tmp_path)
    assert f in result


def test_snapshot_values_are_floats(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Hello", encoding="utf-8")
    result = mod._snapshot(tmp_path)
    assert isinstance(result[f], float)


def test_changed_files_empty():
    result = mod._changed_files({}, {})
    assert result == []


def test_changed_files_new_file(tmp_path):
    f = tmp_path / "doc.md"
    old = {}
    new = {f: 1234567890.0}
    result = mod._changed_files(old, new)
    assert f in result


def test_changed_files_deleted_file(tmp_path):
    f = tmp_path / "doc.md"
    old = {f: 1234567890.0}
    new = {}
    result = mod._changed_files(old, new)
    assert f in result


def test_changed_files_modified_file(tmp_path):
    f = tmp_path / "doc.md"
    old = {f: 1000.0}
    new = {f: 2000.0}
    result = mod._changed_files(old, new)
    assert f in result


def test_changed_files_unchanged_file(tmp_path):
    f = tmp_path / "doc.md"
    mtime = 1234567890.0
    old = {f: mtime}
    new = {f: mtime}
    result = mod._changed_files(old, new)
    assert f not in result


def test_changed_files_returns_list(tmp_path):
    result = mod._changed_files({}, {})
    assert isinstance(result, list)


def test_interval_constant():
    assert hasattr(mod, "INTERVAL")
    assert isinstance(mod.INTERVAL, int)
    assert mod.INTERVAL > 0


def test_docs_path_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)
