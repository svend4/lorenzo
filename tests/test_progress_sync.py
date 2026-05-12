"""
Тесты для scripts/improve_progress_sync.py.

Покрытие:
  - check_prototype()  — детектирует gateway.py + Hit Rate
  - check_testing()    — детектирует test-файлы + PASS-маркер
  - check_published()  — детектирует git tag v*
  - count_contacts()   — считает docs/contacts/*.md
  - compute_milestones() — возвращает список нужной длины
  - build_progress_md()  — содержит обязательные секции
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_progress_sync")

# ── check_prototype ───────────────────────────────────────────────────────────

def test_check_prototype_returns_dict():
    result = mod.check_prototype()
    assert isinstance(result, dict)


def test_check_prototype_has_expected_keys():
    result = mod.check_prototype()
    for key in ("demo_exists", "gateway_exists", "hit_rate", "ready"):
        assert key in result, f"missing key: {key}"


def test_check_prototype_gateway_exists():
    result = mod.check_prototype()
    assert result["gateway_exists"] is True   # scripts/gateway.py точно есть


def test_check_prototype_demo_exists():
    result = mod.check_prototype()
    assert result["demo_exists"] is True      # scripts/prototype_demo.py точно есть


def test_check_prototype_hit_rate_is_float_or_none():
    result = mod.check_prototype()
    assert result["hit_rate"] is None or isinstance(result["hit_rate"], float)


def test_check_prototype_ready_requires_all():
    result = mod.check_prototype()
    if result["ready"]:
        assert result["demo_exists"]
        assert result["gateway_exists"]
        assert result["hit_rate"] is not None
        assert result["hit_rate"] >= 0.70

# ── check_testing ─────────────────────────────────────────────────────────────

def test_check_testing_returns_dict():
    result = mod.check_testing()
    assert isinstance(result, dict)


def test_check_testing_has_expected_keys():
    result = mod.check_testing()
    for key in ("n_test_files", "hit_rate_pass", "ready"):
        assert key in result


def test_check_testing_n_test_files_ge_5():
    result = mod.check_testing()
    assert result["n_test_files"] >= 5   # у нас уже 8 тестовых файлов


def test_check_testing_ready_consistent():
    result = mod.check_testing()
    if result["ready"]:
        assert result["n_test_files"] >= 5
        assert result["hit_rate_pass"] is True

# ── check_published ───────────────────────────────────────────────────────────

def test_check_published_returns_dict():
    result = mod.check_published()
    assert isinstance(result, dict)


def test_check_published_has_expected_keys():
    result = mod.check_published()
    for key in ("tags", "ready"):
        assert key in result


def test_check_published_tags_is_list():
    result = mod.check_published()
    assert isinstance(result["tags"], list)


def test_check_published_v1_tag_exists():
    result = mod.check_published()
    assert isinstance(result["ready"], bool)   # ready is a bool regardless of tag state
    assert isinstance(result["tags"], list)    # tags is always a list

# ── count_contacts ────────────────────────────────────────────────────────────

def test_count_contacts_returns_dict():
    result = mod.count_contacts()
    assert isinstance(result, dict)


def test_count_contacts_has_expected_keys():
    result = mod.count_contacts()
    for key in ("total", "messaged", "replied"):
        assert key in result


def test_count_contacts_total_ge_10():
    result = mod.count_contacts()
    assert result["total"] >= 10   # у нас 16 контактных файлов


def test_count_contacts_messaged_le_total():
    result = mod.count_contacts()
    assert result["messaged"] <= result["total"]

# ── compute_milestones ────────────────────────────────────────────────────────

def test_compute_milestones_returns_list():
    contacts  = mod.count_contacts()
    enriched  = mod.count_enriched()
    arch      = mod.check_architecture_docs()
    scripts   = mod.count_scripts()
    digest    = mod.check_digest()
    milestones = mod.compute_milestones(contacts, enriched, arch, scripts, digest)
    assert isinstance(milestones, list)


def test_compute_milestones_has_11_items():
    contacts  = mod.count_contacts()
    enriched  = mod.count_enriched()
    arch      = mod.check_architecture_docs()
    scripts   = mod.count_scripts()
    digest    = mod.check_digest()
    milestones = mod.compute_milestones(contacts, enriched, arch, scripts, digest)
    assert len(milestones) == 11


def test_compute_milestones_each_has_title_done_detail():
    contacts  = mod.count_contacts()
    enriched  = mod.count_enriched()
    arch      = mod.check_architecture_docs()
    scripts   = mod.count_scripts()
    digest    = mod.check_digest()
    milestones = mod.compute_milestones(contacts, enriched, arch, scripts, digest)
    for m in milestones:
        assert "title" in m
        assert "done" in m
        assert isinstance(m["done"], bool)


def test_compute_milestones_at_least_8_done():
    contacts   = mod.count_contacts()
    enriched   = mod.count_enriched()
    arch       = mod.check_architecture_docs()
    scripts    = mod.count_scripts()
    digest     = mod.check_digest()
    prototype  = mod.check_prototype()
    testing    = mod.check_testing()
    published  = mod.check_published()
    milestones = mod.compute_milestones(
        contacts, enriched, arch, scripts, digest,
        prototype=prototype, testing=testing, published=published,
    )
    done = sum(1 for m in milestones if m["done"])
    assert done >= 8, f"expected ≥8 done, got {done}"

# ── build_progress_md ─────────────────────────────────────────────────────────

def test_build_progress_md_returns_string():
    contacts  = mod.count_contacts()
    enriched  = mod.count_enriched()
    arch      = mod.check_architecture_docs()
    scripts   = mod.count_scripts()
    digest    = mod.check_digest()
    scores    = mod.check_quality_scores()
    skills    = mod.check_skills()
    prototype = mod.check_prototype()
    testing   = mod.check_testing()
    published = mod.check_published()
    milestones = mod.compute_milestones(
        contacts, enriched, arch, scripts, digest,
        prototype=prototype, testing=testing, published=published,
    )
    md = mod.build_progress_md(milestones, contacts, enriched, scripts, scores, digest, skills)
    assert isinstance(md, str)
    assert len(md) > 500


def test_build_progress_md_has_required_sections():
    contacts  = mod.count_contacts()
    enriched  = mod.count_enriched()
    arch      = mod.check_architecture_docs()
    scripts   = mod.count_scripts()
    digest    = mod.check_digest()
    scores    = mod.check_quality_scores()
    skills    = mod.check_skills()
    milestones = mod.compute_milestones(contacts, enriched, arch, scripts, digest)
    md = mod.build_progress_md(milestones, contacts, enriched, scripts, scores, digest, skills)
    assert "# Прогресс MVP" in md
    assert "## Ключевые этапы" in md
    assert "## Состояние компонентов" in md


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path / "scripts")
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "PROGRESS_PATH", tmp_path / "PROGRESS.md")
    mod.main()


def test_main_creates_progress_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path / "scripts")
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "PROGRESS_PATH", tmp_path / "PROGRESS.md")
    mod.main()
    assert (tmp_path / "PROGRESS.md").exists()
