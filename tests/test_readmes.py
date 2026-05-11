"""Tests for scripts/improve_readmes.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_readmes")


def test_folder_titles_is_dict():
    assert hasattr(mod, "FOLDER_TITLES")
    assert isinstance(mod.FOLDER_TITLES, dict)


def test_folder_titles_has_svyazi():
    assert "01-svyazi" in mod.FOLDER_TITLES


def test_folder_titles_has_habr():
    assert "05-habr-projects" in mod.FOLDER_TITLES


def test_first_description_returns_string(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nThis is the first paragraph content.\n", encoding="utf-8")
    result = mod.first_description(f)
    assert isinstance(result, str)


def test_first_description_skips_heading(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nFirst paragraph content.\n", encoding="utf-8")
    result = mod.first_description(f)
    assert "Title" not in result or "First" in result


def test_first_description_returns_first_paragraph(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# Title\n\nFirst good paragraph.\n\nSecond paragraph.\n", encoding="utf-8")
    result = mod.first_description(f)
    assert "First good paragraph" in result


def test_first_description_truncates(tmp_path):
    f = tmp_path / "test.md"
    long_text = "A " * 100
    f.write_text(f"# Title\n\n{long_text}\n", encoding="utf-8")
    result = mod.first_description(f)
    assert len(result) <= 123  # 120 + "…"


def test_first_description_empty_file(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# Title\n\n", encoding="utf-8")
    result = mod.first_description(f)
    assert result == ""


def test_make_readme_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    folder = tmp_path / "01-test"
    folder.mkdir()
    (folder / "doc1.md").write_text("# Doc 1\n\nFirst document content.\n", encoding="utf-8")
    (folder / "doc2.md").write_text("# Doc 2\n\nSecond document content.\n", encoding="utf-8")
    mod.make_readme(folder)
    assert (folder / "README.md").exists()


def test_make_readme_skips_empty_folder(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    folder = tmp_path / "empty"
    folder.mkdir()
    mod.make_readme(folder)
    assert not (folder / "README.md").exists()


def test_make_readme_respects_handcrafted(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    folder = tmp_path / "01-test"
    folder.mkdir()
    (folder / "doc.md").write_text("# Doc\n\nContent.\n", encoding="utf-8")
    # Create a handcrafted README
    readme = folder / "README.md"
    readme.write_text("<!-- handcrafted -->\n# Manual README\n\nHand-written content.\n", encoding="utf-8")
    mod.make_readme(folder)
    # Should not overwrite handcrafted README
    assert "Manual README" in readme.read_text(encoding="utf-8")


def test_make_readme_content_includes_filenames(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    folder = tmp_path / "section"
    folder.mkdir()
    (folder / "doc1.md").write_text("# Doc 1\n\nContent.\n", encoding="utf-8")
    mod.make_readme(folder)
    content = (folder / "README.md").read_text(encoding="utf-8")
    assert "doc1.md" in content
