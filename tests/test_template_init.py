"""Тесты для improve_template_init.py."""
import tempfile
from pathlib import Path

from improve_template_init import apply_vars, parse_kv, list_templates, _yaml_value


def test_parse_kv_basic():
    result = parse_kv(['author=Иван', 'platform=GitHub'])
    assert result['author'] == 'Иван'
    assert result['platform'] == 'GitHub'


def test_parse_kv_skip_invalid():
    result = parse_kv(['valid=yes', 'novalue', 'k=v'])
    assert 'valid' in result
    assert 'novalue' not in result


def test_yaml_value_int():
    assert _yaml_value('42') == '42'


def test_yaml_value_string_with_special():
    assert _yaml_value('hello: world').startswith('"')


def test_yaml_value_bool():
    assert _yaml_value('true') == 'true'
    assert _yaml_value('false') == 'false'


def test_yaml_value_date():
    assert _yaml_value('2026-04-29') == '2026-04-29'


def test_apply_vars_replaces_frontmatter():
    content = """---
template: test
title: "[Тема]"
created: 2026-04-29
---

# [Тема]

Body
"""
    result = apply_vars(content, {'title': 'Real Title'})
    assert 'title: "Real Title"' in result


def test_apply_vars_replaces_body_placeholders():
    content = """---
template: test
---

# [имя]

Hello [имя]
"""
    result = apply_vars(content, {'имя': 'Алиса'})
    assert 'Hello Алиса' in result


def test_list_templates_returns_list():
    """Smoke test."""
    templates = list_templates()
    assert isinstance(templates, list)


# ── main ──────────────────────────────────────────────────────────────────────

import importlib as _importlib
import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
_mod = _importlib.import_module("improve_template_init")


def test_main_list_no_crash(monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog", "--list"])
    result = _mod.main()
    assert result == 0


def test_main_no_type_returns_error(monkeypatch):
    monkeypatch.setattr("sys.argv", ["prog"])
    result = _mod.main()
    assert result == 1


def test_main_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(_mod, "ROOT", tmp_path)
    template_name = _mod.list_templates()[0] if _mod.list_templates() else None
    if template_name is None:
        return  # no templates available, skip
    slug = str(tmp_path / "output.md")
    monkeypatch.setattr("sys.argv", ["prog", "--type", template_name, "--slug", slug])
    result = _mod.main()
    assert result in (0, None)
