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
