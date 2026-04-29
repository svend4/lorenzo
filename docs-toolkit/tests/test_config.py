"""Тесты docstoolkit.config"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.config import deep_merge, load_config, find_config, DEFAULT_CONFIG


def test_deep_merge_simple():
    base = {'a': 1, 'b': {'c': 2}}
    override = {'b': {'d': 3}, 'e': 4}
    result = deep_merge(base, override)
    assert result == {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}


def test_deep_merge_override_value():
    base = {'a': 1, 'b': 2}
    override = {'a': 10}
    result = deep_merge(base, override)
    assert result == {'a': 10, 'b': 2}


def test_find_config_not_present(tmp_path):
    """Если config не найден — возвращает None."""
    deep_dir = tmp_path / "deep" / "nested"
    deep_dir.mkdir(parents=True)
    assert find_config(deep_dir) is None


def test_find_config_present(tmp_path):
    config = tmp_path / "docstoolkit.toml"
    config.write_text("")
    deep = tmp_path / "deep"
    deep.mkdir()
    found = find_config(deep)
    assert found == config


def test_load_config_with_defaults(tmp_path):
    cfg = load_config(tmp_path)
    assert cfg.paths['docs'] == 'docs'
    assert cfg.validation['strict'] is False
    assert cfg.language['primary'] in ('en', 'ru')


def test_load_config_with_user_overrides(tmp_path):
    config = tmp_path / "docstoolkit.toml"
    config.write_text(
        '[paths]\ndocs = "documents"\n[language]\nprimary = "ru"\n'
    )
    cfg = load_config(tmp_path)
    assert cfg.paths['docs'] == 'documents'
    assert cfg.language['primary'] == 'ru'


def test_config_docs_dir_property(tmp_path):
    config = tmp_path / "docstoolkit.toml"
    config.write_text("")
    cfg = load_config(tmp_path)
    assert cfg.docs_dir == tmp_path / 'docs'
    assert cfg.templates_dir == tmp_path / 'docs/templates'
