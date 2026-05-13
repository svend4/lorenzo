"""Tests for scripts/utils_docignore.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("utils_docignore")


def test_load_patterns_returns_list():
    result = mod.load_patterns()
    assert isinstance(result, list)


def test_load_patterns_from_custom_file(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    docignore.write_text("docs/REPORT.md\ndocs/templates/\n# comment\n\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    result = mod.load_patterns()
    assert "docs/REPORT.md" in result
    assert "docs/templates/" in result
    assert "# comment" not in result
    assert "" not in result
    mod.load_patterns.cache_clear()


def test_load_patterns_missing_file(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    result = mod.load_patterns()
    assert result == []
    mod.load_patterns.cache_clear()


def test_is_ignored_exact_match(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    docignore.write_text("docs/REPORT.md\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.load_patterns.cache_clear()
    assert mod.is_ignored("docs/REPORT.md", root=tmp_path) is True
    mod.load_patterns.cache_clear()


def test_is_ignored_no_match(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    docignore.write_text("docs/REPORT.md\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    assert mod.is_ignored("docs/OTHER.md", root=tmp_path) is False
    mod.load_patterns.cache_clear()


def test_is_ignored_folder_pattern(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    docignore.write_text("docs/templates/\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    assert mod.is_ignored("docs/templates/project.md", root=tmp_path) is True
    mod.load_patterns.cache_clear()


def test_is_ignored_glob_pattern(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    docignore.write_text("docs/badges/*.svg\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    assert mod.is_ignored("docs/badges/status.svg", root=tmp_path) is True
    assert mod.is_ignored("docs/badges/status.md", root=tmp_path) is False
    mod.load_patterns.cache_clear()


def test_is_ignored_recursive_glob(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    docignore.write_text("**/README.md\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    assert mod.is_ignored("docs/01-svyazi/README.md", root=tmp_path) is True
    mod.load_patterns.cache_clear()


def test_is_ignored_absolute_path(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    docignore.write_text("docs/REPORT.md\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    abs_path = tmp_path / "docs" / "REPORT.md"
    assert mod.is_ignored(abs_path, root=tmp_path) is True
    mod.load_patterns.cache_clear()


def test_filter_paths_removes_ignored(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    docignore.write_text("docs/REPORT.md\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    paths = ["docs/REPORT.md", "docs/OTHER.md"]
    result = mod.filter_paths(paths)
    assert all("REPORT.md" not in str(p) for p in result)
    mod.load_patterns.cache_clear()


def test_filter_paths_returns_list(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    docignore.write_text("", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    result = mod.filter_paths(["docs/file.md"])
    assert isinstance(result, list)
    mod.load_patterns.cache_clear()


def test_is_ignored_empty_patterns(tmp_path, monkeypatch):
    docignore = tmp_path / ".docignore"
    docignore.write_text("", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    assert mod.is_ignored("docs/anything.md", root=tmp_path) is False
    mod.load_patterns.cache_clear()


def test_is_ignored_absolute_path_outside_root(tmp_path, monkeypatch):
    """Lines 56-57: absolute path not under root → ValueError → False."""
    import tempfile
    other_root = Path(tempfile.mkdtemp())
    docignore = tmp_path / ".docignore"
    docignore.write_text("some/path.md\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    # Absolute path not under tmp_path root → ValueError → returns False
    abs_path = other_root / "some" / "path.md"
    result = mod.is_ignored(abs_path, root=tmp_path)
    assert result is False
    mod.load_patterns.cache_clear()


def test_is_ignored_recursive_glob_nested(tmp_path, monkeypatch):
    """Lines 74-75: recursive glob matches nested paths via second fnmatch check."""
    docignore = tmp_path / ".docignore"
    # Pattern **/subdir/REPORT.md:
    # tail = "subdir/REPORT.md", rel.name = "REPORT.md"
    # First check: fnmatch("REPORT.md", "subdir/REPORT.md") → False
    # Second check: fnmatch("docs/subdir/REPORT.md", "*/subdir/REPORT.md") → True
    docignore.write_text("**/subdir/REPORT.md\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    assert mod.is_ignored("docs/subdir/REPORT.md", root=tmp_path) is True
    mod.load_patterns.cache_clear()


def test_main_block_no_args(tmp_path, monkeypatch):
    """Lines 93-99: __main__ block with no args prints usage."""
    import runpy
    docignore = tmp_path / ".docignore"
    docignore.write_text("docs/REPORT.md\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    monkeypatch.setattr("sys.argv", ["utils_docignore.py"])
    script_path = str(ROOT / "scripts" / "utils_docignore.py")
    try:
        runpy.run_path(script_path, run_name="__main__")
    except SystemExit:
        pass
    mod.load_patterns.cache_clear()


def test_main_block_with_args(tmp_path, monkeypatch):
    """Lines 100-102: __main__ block with path args."""
    import runpy
    docignore = tmp_path / ".docignore"
    docignore.write_text("docs/REPORT.md\n", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCIGNORE", docignore)
    mod.load_patterns.cache_clear()
    monkeypatch.setattr("sys.argv", ["utils_docignore.py", "docs/REPORT.md", "docs/OTHER.md"])
    script_path = str(ROOT / "scripts" / "utils_docignore.py")
    runpy.run_path(script_path, run_name="__main__")
    mod.load_patterns.cache_clear()
