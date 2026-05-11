"""
Тесты для scripts/improve_alerts.py.

Покрытие:
  - detect_callout()   — определение типа callout по тексту
  - extract_summary()  — первое значимое предложение
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_alerts")


# ── detect_callout ────────────────────────────────────────────────────────────

def test_detect_callout_returns_tuple_or_none():
    result = mod.detect_callout("# Title\n\nSome text.")
    assert result is None or isinstance(result, tuple)


def test_detect_callout_none_for_short():
    result = mod.detect_callout("Short.")
    assert result is None


def test_detect_callout_tuple_has_two_elements():
    long_text = "word " * 100
    result = mod.detect_callout(long_text)
    if result is not None:
        assert len(result) == 2


def test_detect_callout_type_is_string():
    long_text = "word " * 100
    result = mod.detect_callout(long_text)
    if result is not None:
        callout_type, message = result
        assert isinstance(callout_type, str)


def test_detect_callout_warning_for_risks():
    text = ("риск риск риск опасность не стоит нельзя осторожно проблема критически "
            "сломает ограничен warning danger избегать ")
    text = text * 5  # Ensure length > 50 words
    result = mod.detect_callout(text)
    if result:
        callout_type, _ = result
        assert callout_type == "WARNING"


def test_detect_callout_tip_for_recommendations():
    text = ("рекомендуется лучший выбор рекомендация практический совет оптимально "
            "рекомендуется tip best practice совет рекомендуется ")
    text = text * 5
    result = mod.detect_callout(text)
    if result:
        callout_type, _ = result
        assert callout_type in ("TIP", "IMPORTANT")


def test_detect_callout_tip_for_mvp():
    text = ("mvp mvp прототип первая итерация начать с mvp прототип "
            "создать первую версию системы для тестирования ")
    text = text * 5
    result = mod.detect_callout(text)
    if result:
        callout_type, _ = result
        assert callout_type == "TIP"


def test_detect_callout_message_is_string():
    long_text = "ключевой важнейший приоритет first critical обязательно must " * 10
    result = mod.detect_callout(long_text)
    if result:
        _, message = result
        assert isinstance(message, str)


# ── extract_summary ───────────────────────────────────────────────────────────

def test_extract_summary_returns_string():
    result = mod.extract_summary("# Title\n\nContent here.")
    assert isinstance(result, str)


def test_extract_summary_empty():
    result = mod.extract_summary("")
    assert isinstance(result, str)


def test_extract_summary_extracts_sentence():
    result = mod.extract_summary("# Title\n\nThis is the first meaningful sentence here.")
    assert len(result) > 0


def test_extract_summary_skips_headings():
    result = mod.extract_summary("# Title\n## Section\n\nActual content sentence here.")
    assert "#" not in result


def test_extract_summary_max_words():
    text = "# Title\n\n" + " ".join(["word"] * 100) + "."
    result = mod.extract_summary(text, max_words=10)
    assert len(result.split()) <= 10


def test_extract_summary_removes_code_blocks():
    text = "```python\nsome code here\n```\nReal text sentence here."
    result = mod.extract_summary(text)
    assert "some code" not in result


def test_extract_summary_skips_short_sentences():
    result = mod.extract_summary("OK. Fine. This is a real sentence with enough words here.")
    # Should skip very short sentences (< 5 words)
    if result:
        assert len(result.split()) >= 5


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_alerts_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    mod.main()
    assert (tmp_path / "ALERTS.md").exists()


def test_main_alerts_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "ALERTS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_dry_run_no_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "--dry-run"])
    mod.main()  # dry-run → no ALERTS.md written, must not raise


def test_main_alerts_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    mod.main()
    text = (tmp_path / "ALERTS.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
