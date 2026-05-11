"""Tests for scripts/improve_component_matrix.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_component_matrix")


def test_components_is_list():
    assert hasattr(mod, "COMPONENTS")
    assert isinstance(mod.COMPONENTS, list)
    assert len(mod.COMPONENTS) > 0


def test_components_have_4_elements():
    for item in mod.COMPONENTS:
        assert len(item) == 4, f"Component {item} must have 4 elements (name, license, status, repo)"


def test_features_is_list():
    assert hasattr(mod, "FEATURES")
    assert isinstance(mod.FEATURES, list)
    assert len(mod.FEATURES) > 0


def test_features_have_2_elements():
    for item in mod.FEATURES:
        assert len(item) == 2, f"Feature {item} must have (key, label)"


def test_matrix_is_dict():
    assert hasattr(mod, "MATRIX")
    assert isinstance(mod.MATRIX, dict)


def test_matrix_has_entries():
    assert len(mod.MATRIX) > 0


def test_matrix_cardindex_exists():
    assert "CardIndex" in mod.MATRIX


def test_matrix_agentfs_exists():
    assert "AgentFS" in mod.MATRIX


def test_matrix_rows_match_features_count():
    n_features = len(mod.FEATURES)
    for comp, row in mod.MATRIX.items():
        assert len(row) == n_features, f"Matrix row for {comp} has {len(row)} but expected {n_features}"


def test_status_icon_is_dict():
    assert hasattr(mod, "STATUS_ICON")
    assert isinstance(mod.STATUS_ICON, dict)


def test_status_icon_has_stable():
    assert "stable" in mod.STATUS_ICON


def test_license_color_is_dict():
    assert hasattr(mod, "LICENSE_COLOR")
    assert isinstance(mod.LICENSE_COLOR, dict)


def test_license_color_has_mit():
    assert "MIT" in mod.LICENSE_COLOR


def test_components_include_sentinel():
    names = [c[0] for c in mod.COMPONENTS]
    assert "SENTINEL" in names


def test_matrix_values_are_valid_symbols():
    valid = {"✅", "🟡", "❌"}
    for comp, row in mod.MATRIX.items():
        for val in row:
            assert val in valid, f"Invalid value {val!r} in matrix for {comp}"


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_component_matrix_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "COMPONENT_MATRIX.md").exists()


def test_main_component_matrix_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "COMPONENT_MATRIX.md").read_text(encoding="utf-8")
    assert "Матрица компонентов" in text
    assert "AgentFS" in text
    assert "CardIndex" in text


def test_main_component_matrix_has_features_table(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "COMPONENT_MATRIX.md").read_text(encoding="utf-8")
    assert "Покрытие возможностей" in text


def test_main_component_matrix_has_ensembles(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "COMPONENT_MATRIX.md").read_text(encoding="utf-8")
    assert "Knowledge OS" in text
