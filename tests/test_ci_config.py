"""Tests for scripts/improve_ci_config.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_ci_config")


def test_docs_yml_is_string():
    assert hasattr(mod, "DOCS_YML")
    assert isinstance(mod.DOCS_YML, str)


def test_docs_yml_contains_workflow_name():
    assert "docs-update" in mod.DOCS_YML or "name:" in mod.DOCS_YML


def test_docs_yml_contains_python_setup():
    assert "python" in mod.DOCS_YML.lower() or "setup-python" in mod.DOCS_YML


def test_docs_check_yml_is_string():
    assert hasattr(mod, "DOCS_CHECK_YML")
    assert isinstance(mod.DOCS_CHECK_YML, str)


def test_docs_check_yml_contains_pr_trigger():
    assert "pull_request" in mod.DOCS_CHECK_YML


def test_minimal_yml_is_string():
    assert hasattr(mod, "MINIMAL_YML")
    assert isinstance(mod.MINIMAL_YML, str)


def test_minimal_yml_shorter_than_full():
    assert len(mod.MINIMAL_YML) < len(mod.DOCS_YML)


def test_docs_yml_has_on_section():
    assert "on:" in mod.DOCS_YML


def test_docs_yml_has_jobs_section():
    assert "jobs:" in mod.DOCS_YML


def test_docs_yml_targets_main_branch():
    assert "main" in mod.DOCS_YML


def test_docs_check_yml_has_steps():
    assert "steps:" in mod.DOCS_CHECK_YML


def test_docs_yml_uses_checkout_action():
    assert "actions/checkout" in mod.DOCS_YML


def test_gh_dir_path_is_github_workflows():
    assert ".github" in str(mod.GH_DIR)
    assert "workflows" in str(mod.GH_DIR)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_docs_yml(tmp_path, monkeypatch):
    gh_dir = tmp_path / ".github" / "workflows"
    monkeypatch.setattr(mod, "GH_DIR", gh_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "MINIMAL", False)
    mod.main()
    assert (gh_dir / "docs.yml").exists()


def test_main_creates_docs_check_yml(tmp_path, monkeypatch):
    gh_dir = tmp_path / ".github" / "workflows"
    monkeypatch.setattr(mod, "GH_DIR", gh_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "MINIMAL", False)
    mod.main()
    assert (gh_dir / "docs_check.yml").exists()


def test_main_minimal_creates_minimal_yml(tmp_path, monkeypatch):
    gh_dir = tmp_path / ".github" / "workflows"
    monkeypatch.setattr(mod, "GH_DIR", gh_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "MINIMAL", True)
    mod.main()
    assert (gh_dir / "docs_check_minimal.yml").exists()


def test_main_dry_run_does_not_write(tmp_path, monkeypatch):
    gh_dir = tmp_path / ".github" / "workflows"
    monkeypatch.setattr(mod, "GH_DIR", gh_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "MINIMAL", False)
    mod.main()
    assert not gh_dir.exists()
