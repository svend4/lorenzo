"""
Тесты для scripts/improve_digest.py.

Покрытие:
  - git_log()          — парсинг вывода git log (H|date|msg)
  - files_in_commit()  — список .md файлов из git diff-tree
  - git_stats_since()  — извлечение статистики (files/insertions/deletions)
  - new_files_since()  — файлы со статусом A (added) из diff
  - count_scripts()    — количество improve_*.py
"""

import importlib
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_digest")

# ── git_log ───────────────────────────────────────────────────────────────────

def _mock_run(stdout):
    result = MagicMock()
    result.stdout = stdout
    result.returncode = 0
    return result


def test_git_log_returns_list():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.git_log()
    assert isinstance(result, list)


def test_git_log_parses_single_commit():
    output = "abc12345|2025-05-01|feat: add new feature"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.git_log()
    assert len(result) == 1
    assert result[0]["hash"] == "abc12345"
    assert result[0]["date"] == "2025-05-01"
    assert "new feature" in result[0]["msg"]


def test_git_log_parses_multiple_commits():
    output = "aaa11111|2025-05-01|feat: alpha\nbbb22222|2025-05-02|fix: beta"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.git_log(2)
    assert len(result) == 2


def test_git_log_empty_output():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.git_log()
    assert result == []


def test_git_log_skips_malformed_lines():
    output = "bad line\nabc12345|2025-05-01|good commit"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.git_log()
    assert len(result) == 1


def test_git_log_hash_truncated_to_8():
    output = "abcdef1234567890|2025-05-01|feat: test"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.git_log()
    assert len(result[0]["hash"]) == 8


# ── files_in_commit ───────────────────────────────────────────────────────────

def test_files_in_commit_returns_list():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.files_in_commit("abc123")
    assert isinstance(result, list)


def test_files_in_commit_includes_md_files():
    output = "docs/README.md\ndocs/HEALTH.md\nscripts/foo.py"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.files_in_commit("abc123")
    assert "docs/README.md" in result
    assert "docs/HEALTH.md" in result


def test_files_in_commit_excludes_non_md():
    output = "scripts/foo.py\ndocs/README.md"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.files_in_commit("abc123")
    assert all(f.endswith(".md") for f in result)


def test_files_in_commit_empty_output():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.files_in_commit("abc123")
    assert result == []


# ── git_stats_since ───────────────────────────────────────────────────────────

def test_git_stats_since_returns_dict():
    with patch("subprocess.run", return_value=_mock_run("5 files changed, 100 insertions(+), 20 deletions(-)")):
        result = mod.git_stats_since()
    assert isinstance(result, dict)


def test_git_stats_since_extracts_files():
    output = "5 files changed, 100 insertions(+), 20 deletions(-)"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.git_stats_since()
    assert result["files"] == 5


def test_git_stats_since_extracts_insertions():
    output = "5 files changed, 100 insertions(+), 20 deletions(-)"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.git_stats_since()
    assert result["insertions"] == 100


def test_git_stats_since_extracts_deletions():
    output = "5 files changed, 100 insertions(+), 20 deletions(-)"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.git_stats_since()
    assert result["deletions"] == 20


def test_git_stats_since_zero_on_empty():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.git_stats_since()
    assert result == {"files": 0, "insertions": 0, "deletions": 0}


def test_git_stats_since_has_required_keys():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.git_stats_since()
    assert "files" in result
    assert "insertions" in result
    assert "deletions" in result


# ── new_files_since ───────────────────────────────────────────────────────────

def test_new_files_since_returns_list():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.new_files_since()
    assert isinstance(result, list)


def test_new_files_since_finds_added_md():
    output = "A\tdocs/new-doc.md\nM\tdocs/existing.md\nA\tscripts/foo.py"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.new_files_since()
    assert "docs/new-doc.md" in result


def test_new_files_since_excludes_non_md():
    output = "A\tdocs/new.md\nA\tscripts/tool.py"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.new_files_since()
    assert all(f.endswith(".md") for f in result)


def test_new_files_since_excludes_modified():
    output = "M\tdocs/existing.md"
    with patch("subprocess.run", return_value=_mock_run(output)):
        result = mod.new_files_since()
    assert result == []


def test_new_files_since_empty_output():
    with patch("subprocess.run", return_value=_mock_run("")):
        result = mod.new_files_since()
    assert result == []


# ── count_scripts ─────────────────────────────────────────────────────────────

def test_count_scripts_returns_int():
    result = mod.count_scripts()
    assert isinstance(result, int)


def test_count_scripts_positive():
    result = mod.count_scripts()
    assert result > 0


def test_count_scripts_uses_scripts_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "improve_alpha.py").write_text("", encoding="utf-8")
    (scripts / "improve_beta.py").write_text("", encoding="utf-8")
    (scripts / "other.py").write_text("", encoding="utf-8")
    result = mod.count_scripts()
    assert result == 2


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_digest_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "DIGEST.md").exists()


def test_main_digest_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "DIGEST.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "DIGEST.md").exists()


def test_main_digest_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "DIGEST.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
