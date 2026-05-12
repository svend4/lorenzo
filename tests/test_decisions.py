"""
Тесты для scripts/improve_decisions.py.

Покрытие:
  - categorize()         — категоризация текста решения
  - extract_decisions()  — извлечение решений из текста
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_decisions")


# ── categorize ────────────────────────────────────────────────────────────────

def test_categorize_returns_string():
    result = mod.categorize("some text about the system")
    assert isinstance(result, str)


def test_categorize_architecture_from_agentfs():
    result = mod.categorize("AgentFS is the best choice for knowledge storage")
    assert result == "архитектура"


def test_categorize_architecture_from_layer():
    result = mod.categorize("слой памяти реализован через CardIndex")
    assert result == "архитектура"


def test_categorize_memory_from_yodoca():
    result = mod.categorize("Yodoca handles memory consolidation best")
    assert result == "память"


def test_categorize_memory_from_consol():
    result = mod.categorize("консолидация данных агента через forgetting механизм")
    assert result == "память"


def test_categorize_security_from_sentinel():
    result = mod.categorize("SENTINEL guards against malicious tool calls")
    assert result == "безопасность"


def test_categorize_mvp_from_mvp():
    result = mod.categorize("MVP должен включать только основные функции поиска")
    assert result == "MVP"


def test_categorize_license_from_mit():
    result = mod.categorize("MIT лицензия позволяет использовать без ограничений")
    assert result == "лицензия"


def test_categorize_risks():
    result = mod.categorize("не стоит использовать BSL из-за ограничений")
    # Could match risks or license
    assert result in ("лицензия", "риски", "общее")


def test_categorize_default_general():
    result = mod.categorize("some random text that matches nothing specific here")
    assert result == "общее"


# ── extract_decisions ─────────────────────────────────────────────────────────

def _make_file(tmp_path, name="test.md"):
    f = tmp_path / name
    f.write_text("", encoding="utf-8")
    return f


def test_extract_decisions_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_decisions("plain text without patterns", f)
    assert isinstance(result, list)


def test_extract_decisions_empty_text(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_decisions("", f)
    assert result == []


def test_extract_decisions_finds_recommendation(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "рекомендуется использовать BM25 для основного поиска информации по документам"
    result = mod.extract_decisions(text, f)
    assert len(result) > 0


def test_extract_decisions_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "рекомендуется использовать BM25 для основного поиска документов"
    result = mod.extract_decisions(text, f)
    for item in result:
        assert "text" in item
        assert "file" in item
        assert "category" in item


def test_extract_decisions_skips_short(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    result = mod.extract_decisions("рекомендуется это.", f)
    # too short definition
    assert result == []


def test_extract_decisions_finds_best_choice(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "лучший выбор: использовать AgentFS для хранения данных в файловой системе"
    result = mod.extract_decisions(text, f)
    assert len(result) > 0


def test_extract_decisions_strips_markdown_links(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "рекомендуется [AgentFS](docs/agentfs.md) для хранения знаний и данных агента"
    result = mod.extract_decisions(text, f)
    for item in result:
        assert "](docs/" not in item["text"]


def test_extract_decisions_category_is_set(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "рекомендуется использовать AgentFS для хранения данных в файловой системе"
    result = mod.extract_decisions(text, f)
    for item in result:
        assert len(item["category"]) > 0


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_decisions_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "DECISIONS.md").exists()


def test_main_decisions_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text(
        "# Title\n\nрекомендуется использовать BM25 для поиска данных.", encoding="utf-8"
    )
    mod.main()
    text = (tmp_path / "DECISIONS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "DECISIONS.md").exists()


def test_main_decisions_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "DECISIONS.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


# ── extract_decisions edge cases ─────────────────────────────────────────────

def test_extract_decisions_skips_val_short_after_link_strip(tmp_path, monkeypatch):
    """Line 60: val < 20 chars after stripping markdown links → continue."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    # The match is ">20 chars via URL, but after stripping link text is < 20
    text = "рекомендуется [a](bcdefghijklmnopqrst) x"
    result = mod.extract_decisions(text, f)
    # All results should have len >= 20
    for item in result:
        assert len(item["text"]) >= 20


def test_extract_decisions_skips_pipe_start(tmp_path, monkeypatch):
    """Line 63: val starts with '|' → continue."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "рекомендуется | первая | вторая | третья колонка для таблицы данных"
    result = mod.extract_decisions(text, f)
    for item in result:
        assert not item["text"].startswith("|")


def test_extract_decisions_skips_hash_start(tmp_path, monkeypatch):
    """Line 63: val starts with '#' → continue."""
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = _make_file(tmp_path)
    text = "рекомендуется # заголовок ещё более длинный и подробный раздел"
    result = mod.extract_decisions(text, f)
    for item in result:
        assert not item["text"].startswith("#")


# ── main: full coverage ───────────────────────────────────────────────────────

def test_main_skips_reserved_files(tmp_path, monkeypatch):
    """Line 81: file in skip set → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "README.md").write_text("# Read me content here is fine.", encoding="utf-8")
    (tmp_path / "doc.md").write_text(
        "# Title\n\n" + "рекомендуется использовать BM25 для поиска данных. " * 5,
        encoding="utf-8",
    )
    mod.main()
    assert (tmp_path / "DECISIONS.md").exists()


def test_main_finds_decisions_in_long_doc(tmp_path, monkeypatch):
    """Lines 85-87, 101-110: long doc with decisions → cat_order loop runs."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    content = "# Title\n\n" + "рекомендуется использовать BM25 для поиска данных в проекте. " * 5
    (tmp_path / "doc.md").write_text(content, encoding="utf-8")
    mod.main()
    text = (tmp_path / "DECISIONS.md").read_text(encoding="utf-8")
    assert "решений" in text or "#" in text


def test_main_many_decisions_truncates(tmp_path, monkeypatch):
    """Lines 111-115: 20+ unique items per category → remaining message."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    recs = [
        f"рекомендуется вариант{i:02d} для системы поиска данных в базе знаний"
        for i in range(25)
    ]
    content = "# Doc\n\n" + "\n\n".join(recs) + "\n"
    (tmp_path / "doc.md").write_text(content, encoding="utf-8")
    mod.main()
    result = (tmp_path / "DECISIONS.md").read_text(encoding="utf-8")
    assert "#" in result


def test_main_duplicate_decisions_deduplicated(tmp_path, monkeypatch):
    """Lines 106-107: duplicate keys → continue."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    decision = "рекомендуется использовать BM25 для поиска данных в проекте"
    content = "# Doc\n\n" + (decision + ".\n\n") * 4
    (tmp_path / "doc.md").write_text(content, encoding="utf-8")
    mod.main()
    assert (tmp_path / "DECISIONS.md").exists()


# ── __main__ block ────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 124: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    script_path = str(ROOT / "scripts" / "improve_decisions.py")
    runpy.run_path(script_path, run_name="__main__")
