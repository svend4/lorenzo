"""Tests for scripts/improve_epub.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_epub")


def test_check_pandoc_returns_bool():
    result = mod._check_pandoc()
    assert isinstance(result, bool)


def test_clean_for_epub_removes_html_comments():
    text = "Before <!-- comment --> After"
    result = mod._clean_for_epub(text)
    assert "comment" not in result
    assert "Before" in result
    assert "After" in result


def test_clean_for_epub_removes_multiline_comments():
    text = "Start\n<!-- \nmulti\nline\ncomment\n-->\nEnd"
    result = mod._clean_for_epub(text)
    assert "multi" not in result
    assert "Start" in result
    assert "End" in result


def test_clean_for_epub_removes_shields():
    text = "See ![badge](https://img.shields.io/badge/test-pass-green) for status."
    result = mod._clean_for_epub(text)
    assert "shields.io" not in result
    assert "status" in result


def test_clean_for_epub_preserves_regular_links():
    text = "[GitHub](https://github.com/user/repo)"
    result = mod._clean_for_epub(text)
    assert "GitHub" in result


def test_clean_for_epub_returns_string():
    result = mod._clean_for_epub("# Title\n\nContent.")
    assert isinstance(result, str)


def test_skip_files_constant():
    assert hasattr(mod, "SKIP_FILES")
    assert isinstance(mod.SKIP_FILES, set)
    assert "SEARCH.md" in mod.SKIP_FILES


def test_docs_path_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)


def test_today_attribute():
    assert hasattr(mod, "TODAY")
    assert isinstance(mod.TODAY, str)
    assert len(mod.TODAY) == 10  # YYYY-MM-DD


def test_title_attribute():
    assert hasattr(mod, "TITLE")
    assert isinstance(mod.TITLE, str)
    assert len(mod.TITLE) > 0


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_check_only_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_ONLY", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    mod.main()


def test_main_no_pandoc_check_returns(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_ONLY", True)
    monkeypatch.setattr(mod, "_check_pandoc", lambda: False)
    mod.main()


def test_main_pandoc_found_check_returns(tmp_path, monkeypatch, capsys):
    import subprocess as _sp
    from unittest.mock import MagicMock, patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_ONLY", True)
    monkeypatch.setattr(mod, "_check_pandoc", lambda: True)
    fake_result = MagicMock()
    fake_result.stdout = "pandoc 3.0\n"
    with patch("subprocess.run", return_value=fake_result):
        mod.main()


def test_build_epub_success(tmp_path, monkeypatch):
    from unittest.mock import MagicMock, patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent.", encoding="utf-8")
    out = tmp_path / "test.epub"
    fake_result = MagicMock()
    fake_result.returncode = 0
    with patch("subprocess.run", return_value=fake_result):
        result = mod.build_epub([f], out, "Test Title")
    assert result is True


def test_build_epub_failure(tmp_path, monkeypatch):
    from unittest.mock import MagicMock, patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent.", encoding="utf-8")
    out = tmp_path / "test.epub"
    fake_result = MagicMock()
    fake_result.returncode = 1
    fake_result.stderr = "pandoc error"
    with patch("subprocess.run", return_value=fake_result):
        result = mod.build_epub([f], out, "Test Title")
    assert result is False


def test_build_epub_empty_files(tmp_path, monkeypatch):
    from unittest.mock import MagicMock, patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    out = tmp_path / "test.epub"
    fake_result = MagicMock()
    fake_result.returncode = 0
    with patch("subprocess.run", return_value=fake_result):
        result = mod.build_epub([], out, "Test Title")
    assert result is True


def test_main_no_pandoc_exits(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_ONLY", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "_check_pandoc", lambda: False)
    with pytest.raises(SystemExit):
        mod.main()


def test_main_no_files_returns(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_ONLY", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUTPUT", None)
    monkeypatch.setattr(mod, "_check_pandoc", lambda: True)
    mod.main()
    out = capsys.readouterr().out
    assert "Нет" in out or "no" in out.lower()


def test_main_build_epub_success(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_ONLY", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUTPUT", None)
    monkeypatch.setattr(mod, "TITLE", "Test Title")
    monkeypatch.setattr(mod, "_check_pandoc", lambda: True)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent word " * 5, encoding="utf-8")

    def fake_build_epub(files, output, title):
        output.write_bytes(b"fake epub content")
        return True

    monkeypatch.setattr(mod, "build_epub", fake_build_epub)
    mod.main()


def test_main_build_epub_failure_exits(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CHECK_ONLY", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUTPUT", None)
    monkeypatch.setattr(mod, "TITLE", "Test")
    monkeypatch.setattr(mod, "_check_pandoc", lambda: True)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nContent.", encoding="utf-8")
    monkeypatch.setattr(mod, "build_epub", lambda files, output, title: False)
    with pytest.raises(SystemExit):
        mod.main()
