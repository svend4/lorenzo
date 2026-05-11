"""
Тесты для scripts/improve_kpi_snapshot.py.

Покрытие:
  - read_metric()    — regex-парсинг числа из файла
  - load_history()   — чтение/инициализация истории
  - save_history()   — запись истории в JSON
  - trend()          — текстовый тренд curr vs prev
"""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_kpi_snapshot")

# ── read_metric ───────────────────────────────────────────────────────────────

def test_read_metric_extracts_number(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "HEALTH.md").write_text("Балл: **87/100**", encoding="utf-8")
    result = mod.read_metric("HEALTH.md", r"(\d+)/100")
    assert result == 87


def test_read_metric_missing_file_returns_default(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.read_metric("NONEXISTENT.md", r"(\d+)", default=42)
    assert result == 42


def test_read_metric_no_match_returns_default(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "DOC.md").write_text("No numbers here.", encoding="utf-8")
    result = mod.read_metric("DOC.md", r"(\d+)%", default=5)
    assert result == 5


def test_read_metric_strips_commas(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "METRICS.md").write_text("Файлов: 2,482", encoding="utf-8")
    result = mod.read_metric("METRICS.md", r"(\d+,\d+)")
    assert result == 2482


def test_read_metric_returns_int(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "F.md").write_text("Score: 96%", encoding="utf-8")
    result = mod.read_metric("F.md", r"(\d+)%")
    assert isinstance(result, int)


def test_read_metric_default_zero(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.read_metric("MISSING.md", r"(\d+)")
    assert result == 0

# ── load_history ──────────────────────────────────────────────────────────────

def test_load_history_returns_list(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "HISTORY_FILE", tmp_path / "kpi_history.json")
    result = mod.load_history()
    assert isinstance(result, list)


def test_load_history_empty_when_no_file(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "HISTORY_FILE", tmp_path / "kpi_history.json")
    assert mod.load_history() == []


def test_load_history_reads_existing(monkeypatch, tmp_path):
    hist_file = tmp_path / "kpi_history.json"
    data = [{"date": "2026-01-01", "docs": 100}, {"date": "2026-02-01", "docs": 150}]
    hist_file.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(mod, "HISTORY_FILE", hist_file)
    result = mod.load_history()
    assert len(result) == 2
    assert result[0]["docs"] == 100


def test_load_history_corrupt_returns_empty(monkeypatch, tmp_path):
    hist_file = tmp_path / "kpi_history.json"
    hist_file.write_text("INVALID JSON {{{{", encoding="utf-8")
    monkeypatch.setattr(mod, "HISTORY_FILE", hist_file)
    result = mod.load_history()
    assert result == []

# ── save_history ──────────────────────────────────────────────────────────────

def test_save_history_creates_file(monkeypatch, tmp_path):
    hist_file = tmp_path / "kpi_history.json"
    monkeypatch.setattr(mod, "HISTORY_FILE", hist_file)
    mod.save_history([{"date": "2026-05-11", "docs": 200}])
    assert hist_file.exists()


def test_save_history_valid_json(monkeypatch, tmp_path):
    hist_file = tmp_path / "kpi_history.json"
    monkeypatch.setattr(mod, "HISTORY_FILE", hist_file)
    data = [{"date": "2026-05-11", "docs": 250, "scripts": 159}]
    mod.save_history(data)
    loaded = json.loads(hist_file.read_text(encoding="utf-8"))
    assert loaded[0]["scripts"] == 159


def test_save_load_roundtrip(monkeypatch, tmp_path):
    hist_file = tmp_path / "kpi_history.json"
    monkeypatch.setattr(mod, "HISTORY_FILE", hist_file)
    original = [{"date": "2026-01-01", "docs": 100, "scoring": 96}]
    mod.save_history(original)
    result = mod.load_history()
    assert result[0]["scoring"] == 96

# ── trend ─────────────────────────────────────────────────────────────────────

def test_trend_up():
    result = mod.trend(150, 100)
    assert "↑" in result
    assert "+50" in result


def test_trend_down():
    result = mod.trend(80, 100)
    assert "↓" in result
    assert "-20" in result or "−20" in result or "20" in result


def test_trend_equal():
    result = mod.trend(100, 100)
    assert "=" in result or "→" in result


def test_trend_prev_zero_returns_arrow():
    result = mod.trend(50, 0)
    assert "→" in result


def test_trend_returns_string():
    assert isinstance(mod.trend(10, 5), str)


def test_trend_large_delta():
    result = mod.trend(1000, 500)
    assert "+500" in result


def test_trend_negative_delta_shows_magnitude():
    result = mod.trend(10, 20)
    assert "10" in result  # delta = -10
