"""Tests for scripts/improve_passive_voice.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_passive_voice")


def test_clean_returns_string():
    result = mod._clean("some text")
    assert isinstance(result, str)


def test_clean_removes_code():
    result = mod._clean("Before\n```python\ncode here\n```\nAfter")
    assert "code here" not in result


def test_clean_removes_urls():
    result = mod._clean("See https://example.com for more.")
    assert "https" not in result


def test_sentences_returns_list():
    result = mod._sentences("Hello world test. Another sentence here.")
    assert isinstance(result, list)


def test_sentences_filters_short():
    result = mod._sentences("Hi. OK.")
    assert all(len(s.split()) >= 5 for s in result)


def test_sentences_strips_headings():
    text = "# Title heading\n\nThis is a proper sentence with enough words."
    result = mod._sentences(text)
    texts = " ".join(result)
    assert "Title heading" not in texts


def test_count_nominals_returns_int():
    result = mod._count_nominals("использование алгоритмов обработки")
    assert isinstance(result, int)


def test_count_nominals_finds_anie():
    result = mod._count_nominals("использование и построение системы")
    assert result >= 2


def test_count_nominals_finds_ost():
    result = mod._count_nominals("эффективность и надёжность системы")
    assert result >= 2


def test_count_nominals_empty():
    result = mod._count_nominals("")
    assert result == 0


def test_grade_returns_string():
    result = mod._grade(0.05)
    assert isinstance(result, str)


def test_grade_low_passive_active():
    result = mod._grade(0.03)
    assert "Активный" in result


def test_grade_medium_passive():
    result = mod._grade(0.12)
    assert "Умеренный" in result


def test_grade_high_passive():
    result = mod._grade(0.20)
    assert "Много" in result


def test_grade_very_high_passive():
    result = mod._grade(0.35)
    assert "Преимущественно" in result


def test_passive_ru_pattern_matches():
    text = "Система используется для обработки запросов."
    assert mod.PASSIVE_RU.search(text) is not None


def test_passive_en_pattern_matches():
    text = "The data was processed by the agent."
    assert mod.PASSIVE_EN.search(text) is not None


def test_cliche_pattern_matches():
    text = "В рамках данного проекта выполняется анализ."
    assert mod.CLICHE_RU.search(text) is not None


# ── main ──────────────────────────────────────────────────────────────────────

_PASSIVE_DOC = """\
# Title

Система используется для обработки данных агента в режиме реального времени.
Данные реализованы в виде графа знаний системы агентов и документов.
Компоненты разрабатываются командой в рамках данного проекта системы.
Функция выполняется автоматически при поступлении запроса к системе.
Результаты передаются в базу данных для хранения архивных записей.
Модуль применяется для анализа текстовых документов базы знаний агентов.
"""


def _pv_setup(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "VERBOSE", False)
    (tmp_path / "doc.md").write_text(_PASSIVE_DOC, encoding="utf-8")


def test_main_creates_passive_voice_md(tmp_path, monkeypatch):
    _pv_setup(tmp_path, monkeypatch)
    mod.main()
    assert (tmp_path / "PASSIVE_VOICE.md").exists()


def test_main_passive_voice_has_content(tmp_path, monkeypatch):
    _pv_setup(tmp_path, monkeypatch)
    mod.main()
    text = (tmp_path / "PASSIVE_VOICE.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "VERBOSE", False)
    mod.main()  # no files → returns early, must not raise


def test_main_passive_voice_starts_with_heading(tmp_path, monkeypatch):
    _pv_setup(tmp_path, monkeypatch)
    mod.main()
    text = (tmp_path / "PASSIVE_VOICE.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
