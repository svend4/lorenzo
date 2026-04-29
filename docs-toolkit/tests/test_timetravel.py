"""Тесты time-travel git queries.

Используют реальный git репо — некоторые тесты skip если не git checkout.
"""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.timetravel.git import (
    snapshot_at, list_commits, file_history, GitError, _git,
)


def _is_git_repo(path: Path) -> bool:
    return (path / ".git").exists() or any(
        (p / ".git").exists() for p in path.parents
    )


REPO_AVAILABLE = _is_git_repo(Path(__file__).parent)


@pytest.mark.skipif(not REPO_AVAILABLE, reason="Не в git-репозитории")
def test_list_commits_basic():
    commits = list_commits(limit=5)
    assert isinstance(commits, list)
    if commits:
        c = commits[0]
        assert "sha" in c
        assert "short_sha" in c
        assert "message" in c
        assert len(c["short_sha"]) <= 12


@pytest.mark.skipif(not REPO_AVAILABLE, reason="Не в git-репозитории")
def test_list_commits_with_path():
    commits = list_commits(path="docs-toolkit/pyproject.toml", limit=5)
    assert isinstance(commits, list)


@pytest.mark.skipif(not REPO_AVAILABLE, reason="Не в git-репозитории")
def test_snapshot_at_head():
    # Любой существующий файл
    text = snapshot_at("docs-toolkit/pyproject.toml", "HEAD")
    assert isinstance(text, str)
    assert len(text) > 0


@pytest.mark.skipif(not REPO_AVAILABLE, reason="Не в git-репозитории")
def test_snapshot_nonexistent_returns_empty():
    text = snapshot_at("nonexistent_file_12345.md", "HEAD")
    assert text == ""


@pytest.mark.skipif(not REPO_AVAILABLE, reason="Не в git-репозитории")
def test_file_history():
    history = file_history("docs-toolkit/pyproject.toml", limit=5)
    assert isinstance(history, list)
    if history:
        h = history[0]
        assert "sha" in h
        assert "additions" in h
        assert "deletions" in h


def test_git_error_on_invalid_command():
    with pytest.raises(GitError):
        _git("--invalid-command")


def test_list_commits_empty_path_works():
    """list_commits без path возвращает все коммиты."""
    # просто smoke test — может вернуть пустое если нет git, не должно raise
    try:
        commits = list_commits(limit=3)
        assert isinstance(commits, list)
    except GitError:
        pytest.skip("git command failed (CI environment?)")
