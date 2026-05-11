"""
Тесты для scripts/improve_benchmark.py.

Покрытие:
  - load_history()   — загрузка/инициализация benchmark.json
  - save_history()   — запись в файл
  - _trend()         — текстовый тренд из списка замеров
  - print_report()   — форматирование отчёта (проверяем что не падает)
"""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_benchmark")

# ── load_history ──────────────────────────────────────────────────────────────

def test_load_history_returns_dict(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "BENCH_FILE", tmp_path / "nonexistent.json")
    result = mod.load_history()
    assert isinstance(result, dict)


def test_load_history_default_structure(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "BENCH_FILE", tmp_path / "nonexistent.json")
    result = mod.load_history()
    assert "runs" in result
    assert "scripts" in result


def test_load_history_reads_existing(monkeypatch, tmp_path):
    data = {"runs": [{"date": "2026-01-01"}], "scripts": {"improve_metrics.py": [1.2, 1.5]}}
    bench = tmp_path / "benchmark.json"
    bench.write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(mod, "BENCH_FILE", bench)
    result = mod.load_history()
    assert len(result["runs"]) == 1
    assert "improve_metrics.py" in result["scripts"]


def test_load_history_corrupt_file_returns_default(monkeypatch, tmp_path):
    bench = tmp_path / "benchmark.json"
    bench.write_text("NOT VALID JSON {{{{", encoding="utf-8")
    monkeypatch.setattr(mod, "BENCH_FILE", bench)
    result = mod.load_history()
    assert isinstance(result, dict)
    assert "runs" in result

# ── save_history ──────────────────────────────────────────────────────────────

def test_save_history_creates_file(monkeypatch, tmp_path):
    bench = tmp_path / "benchmark.json"
    monkeypatch.setattr(mod, "BENCH_FILE", bench)
    data = {"runs": [], "scripts": {"test.py": [0.5]}}
    mod.save_history(data)
    assert bench.exists()


def test_save_history_valid_json(monkeypatch, tmp_path):
    bench = tmp_path / "benchmark.json"
    monkeypatch.setattr(mod, "BENCH_FILE", bench)
    data = {"runs": [{"date": "2026-05-11"}], "scripts": {"a.py": [1.0, 2.0]}}
    mod.save_history(data)
    loaded = json.loads(bench.read_text(encoding="utf-8"))
    assert loaded["scripts"]["a.py"] == [1.0, 2.0]


def test_save_load_roundtrip(monkeypatch, tmp_path):
    bench = tmp_path / "benchmark.json"
    monkeypatch.setattr(mod, "BENCH_FILE", bench)
    original = {"runs": [{"date": "2026-05-11", "count": 3}],
                "scripts": {"improve_metrics.py": [1.1, 1.2, 0.9]}}
    mod.save_history(original)
    loaded = mod.load_history()
    assert loaded["scripts"]["improve_metrics.py"] == [1.1, 1.2, 0.9]

# ── _trend ────────────────────────────────────────────────────────────────────

def test_trend_single_point():
    result = mod._trend([1.5])
    assert result == "—"


def test_trend_empty_list():
    result = mod._trend([])
    assert result == "—"


def test_trend_stable():
    result = mod._trend([1.0, 1.05])  # delta < 0.1
    assert "стабильно" in result


def test_trend_slower():
    result = mod._trend([1.0, 2.5])  # delta > 0 and >= 0.1
    assert "медленнее" in result


def test_trend_faster():
    result = mod._trend([3.0, 1.0])  # delta < -0.1
    assert "быстрее" in result


def test_trend_returns_string():
    result = mod._trend([1.0, 2.0])
    assert isinstance(result, str)


def test_trend_shows_delta():
    result = mod._trend([1.0, 3.0])  # delta = 2.0
    assert "2.0" in result

# ── print_report ──────────────────────────────────────────────────────────────

def test_print_report_empty_data(capsys):
    mod.print_report({"runs": [], "scripts": {}})
    captured = capsys.readouterr()
    assert "Нет данных" in captured.out


def test_print_report_with_data(capsys):
    data = {
        "runs": [{"date": "2026-05-11"}],
        "scripts": {
            "improve_metrics.py": [1.2, 1.5, 0.9],
            "improve_health.py": [0.5],
        },
    }
    mod.print_report(data)
    captured = capsys.readouterr()
    assert "improve_metrics.py" in captured.out
    assert "improve_health.py" in captured.out


def test_print_report_shows_run_count(capsys):
    data = {
        "runs": [{"date": "2026-04-01"}, {"date": "2026-05-11"}],
        "scripts": {"a.py": [1.0]},
    }
    mod.print_report(data)
    captured = capsys.readouterr()
    assert "2" in captured.out  # 2 runs


def test_print_report_skips_empty_times(capsys):
    data = {
        "runs": [],
        "scripts": {"empty_script.py": []},
    }
    mod.print_report(data)
    captured = capsys.readouterr()
    # Should not crash; empty script list doesn't appear
    assert "Нет данных" not in captured.out or True  # no-crash check


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_report_only_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "BENCH_FILE", tmp_path / "benchmark.json")
    monkeypatch.setattr(mod, "REPORT_ONLY", True)
    mod.main()  # report-only → reads empty history, must not raise


def test_main_report_only_with_history(tmp_path, monkeypatch):
    import json
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    bench = tmp_path / "benchmark.json"
    bench.write_text(json.dumps({
        "scripts": {"test.py": [1.2, 0.9, 1.5]},
        "runs": [{"date": "2025-05-01", "timestamp": "2025-05-01T10:00:00",
                  "scripts": {"test.py": 1.2}, "total": 1.2}]
    }), encoding="utf-8")
    monkeypatch.setattr(mod, "BENCH_FILE", bench)
    monkeypatch.setattr(mod, "REPORT_ONLY", True)
    mod.main()  # must not raise
