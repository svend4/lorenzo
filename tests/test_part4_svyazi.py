"""Tests for scripts/part4_svyazi.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("part4_svyazi")


# ── REPORT maps ───────────────────────────────────────────────────────────────

def test_report1_map_is_dict():
    assert isinstance(mod.REPORT1_MAP, dict)
    assert len(mod.REPORT1_MAP) > 0


def test_report1_map_values_are_md():
    for key, val in mod.REPORT1_MAP.items():
        assert val.endswith(".md"), f"{key!r} → {val!r} should be .md"


def test_report1_map_has_executive_summary():
    assert any("executive" in k.lower() or "summary" in k.lower()
               for k in mod.REPORT1_MAP)


def test_report3_map_is_dict():
    assert isinstance(mod.REPORT3_MAP, dict)
    assert len(mod.REPORT3_MAP) > 0


def test_report3_map_values_are_md():
    for key, val in mod.REPORT3_MAP.items():
        assert val.endswith(".md"), f"{key!r} → {val!r} should be .md"


def test_report3_map_has_roadmap():
    assert any("roadmap" in v.lower() or "дорог" in k.lower()
               for k, v in mod.REPORT3_MAP.items())


def test_report_maps_no_key_overlap():
    keys1 = set(mod.REPORT1_MAP.keys())
    keys3 = set(mod.REPORT3_MAP.keys())
    assert not (keys1 & keys3), "REPORT1_MAP and REPORT3_MAP share keys"


# ── process_report ────────────────────────────────────────────────────────────

def test_process_report_writes_matched_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    # monkeypatch write_doc's ROOT reference via part1_utils
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)

    md = tmp_path / "report.md"
    md.write_text("# Title\n\n## Executive summary\n\nSome content here.", encoding="utf-8")

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    section_map = {"Executive summary": "01-executive-summary.md"}
    mod.process_report(md, section_map, out_dir)

    assert (out_dir / "01-executive-summary.md").exists()


def test_process_report_skips_unmatched(tmp_path, monkeypatch):
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)

    md = tmp_path / "report.md"
    # No preamble — start with ## so no empty-heading section (empty "" matches every key)
    md.write_text("## Unmatched Section\n\nContent.", encoding="utf-8")

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    section_map = {"Executive summary": "01-executive-summary.md"}
    mod.process_report(md, section_map, out_dir)

    # Nothing should be written since no match
    assert not (out_dir / "01-executive-summary.md").exists()


def test_process_report_skips_existing(tmp_path, monkeypatch):
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)

    md = tmp_path / "report.md"
    md.write_text("# Title\n\n## Executive summary\n\nNew content.", encoding="utf-8")

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    existing = out_dir / "01-executive-summary.md"
    existing.write_text("# Original content\n", encoding="utf-8")

    section_map = {"Executive summary": "01-executive-summary.md"}
    mod.process_report(md, section_map, out_dir)

    # Should not overwrite
    assert existing.read_text(encoding="utf-8") == "# Original content\n"


def test_process_report_partial_key_match(tmp_path, monkeypatch):
    import part1_utils
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)

    md = tmp_path / "report.md"
    md.write_text("# Title\n\n## Executive summary and analysis\n\nContent.", encoding="utf-8")

    out_dir = tmp_path / "out"
    out_dir.mkdir()

    section_map = {"Executive summary": "01-executive-summary.md"}
    mod.process_report(md, section_map, out_dir)

    assert (out_dir / "01-executive-summary.md").exists()


# ── run ───────────────────────────────────────────────────────────────────────

def test_run_calls_process_report(tmp_path, monkeypatch):
    """Lines 55-64: run() calls process_report for both reports."""
    import part1_utils
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)

    # Create the out dir
    out_dir = tmp_path / "01-svyazi"
    out_dir.mkdir()

    # Create fake report files
    r1 = tmp_path / "deep-research-report (1).md"
    r3 = tmp_path / "deep-research-report (3).md"
    r1.write_text("# Report 1\n\n## Executive Summary\n\nContent.", encoding="utf-8")
    r3.write_text("# Report 3\n\n## Roadmap\n\nContent.", encoding="utf-8")

    called = []
    monkeypatch.setattr(mod, "process_report",
                        lambda md, mapping, out: called.append(md.name))
    mod.run()
    assert "deep-research-report (1).md" in called
    assert "deep-research-report (3).md" in called


def test_run_no_crash_missing_files(tmp_path, monkeypatch):
    """run() should not crash when source files don't exist."""
    import part1_utils
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(part1_utils, "ROOT", tmp_path)
    (tmp_path / "01-svyazi").mkdir()
    # No report files — process_report will just skip silently
    monkeypatch.setattr(mod, "process_report", lambda md, mapping, out: None)
    mod.run()  # Should not raise
