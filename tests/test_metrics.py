"""
Тесты для scripts/improve_metrics.py.

Покрытие:
  - link_density()     — ссылок на 1000 слов
  - example_density()  — code-блоков на 1000 слов
  - heading_ratio()    — заголовков на 100 слов
  - has_summary()      — наличие <!-- summary --> блока
  - has_tags()         — наличие <!-- tags: ... --> блока
  - has_toc()          — наличие TOC-маркера
  - has_callout()      — наличие > [! ... ] блока
  - quality_score()    — итоговый балл 0–100
"""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_metrics")

# ── link_density ──────────────────────────────────────────────────────────────

def test_link_density_zero_when_no_links():
    assert mod.link_density("no links here at all") == 0.0


def test_link_density_positive_with_links():
    text = "[AgentFS](docs/agentfs.md) is a filesystem for agents."
    assert mod.link_density(text) > 0


def test_link_density_scales_with_link_count():
    base = "word " * 100
    one_link  = base + "[a](b)"
    two_links = base + "[a](b) [c](d)"
    assert mod.link_density(two_links) > mod.link_density(one_link)


def test_link_density_empty_text():
    # empty text: words=1 (max guard), links=0
    assert mod.link_density("") == 0.0

# ── example_density ───────────────────────────────────────────────────────────

def test_example_density_zero_when_no_code():
    assert mod.example_density("plain text no code") == 0.0


def test_example_density_positive_with_code():
    text = "Example:\n```python\nprint('hello')\n```\nDone."
    assert mod.example_density(text) > 0


def test_example_density_counts_pairs():
    # Два code-блока
    text = "```python\ncode1\n```\n words " * 10 + "```bash\ncode2\n```"
    density_2 = mod.example_density(text)
    # Один code-блок
    text_1 = "words " * 20 + "```python\ncode\n```"
    density_1 = mod.example_density(text_1)
    assert density_2 > 0 and density_1 > 0

# ── heading_ratio ─────────────────────────────────────────────────────────────

def test_heading_ratio_zero_when_no_headings():
    text = "no headings here just plain paragraph text"
    assert mod.heading_ratio(text) == 0.0


def test_heading_ratio_positive_with_headings():
    text = "# Title\n\n## Section\n\nsome words here"
    assert mod.heading_ratio(text) > 0


def test_heading_ratio_increases_with_more_headings():
    base = "word " * 50
    fewer = "# H1\n" + base
    more  = "# H1\n## H2\n### H3\n" + base
    assert mod.heading_ratio(more) > mod.heading_ratio(fewer)

# ── has_summary ───────────────────────────────────────────────────────────────

def test_has_summary_true():
    assert mod.has_summary("<!-- summary -->\n> Key text.") is True


def test_has_summary_false():
    assert mod.has_summary("# Title\n\nNo summary here.") is False

# ── has_tags ──────────────────────────────────────────────────────────────────

def test_has_tags_true():
    assert mod.has_tags("<!-- tags: memory, agent -->") is True


def test_has_tags_false():
    assert mod.has_tags("# Title\n\nNo tags here.") is False

# ── has_toc ───────────────────────────────────────────────────────────────────

def test_has_toc_with_russian_header():
    assert mod.has_toc("## Содержание\n\n- [Раздел](#раздел)") is True


def test_has_toc_with_auto_marker():
    assert mod.has_toc("<!-- toc-auto -->\n## Contents") is True


def test_has_toc_false():
    assert mod.has_toc("# Title\n\nNo table of contents.") is False

# ── has_callout ───────────────────────────────────────────────────────────────

def test_has_callout_true():
    assert mod.has_callout("> [!NOTE]\n> Important note here.") is True


def test_has_callout_warning():
    assert mod.has_callout("> [!WARNING]\n> Be careful.") is True


def test_has_callout_false():
    assert mod.has_callout("# Title\n\n> Regular blockquote.") is False

# ── quality_score ─────────────────────────────────────────────────────────────

def _make_data(**kwargs):
    """Базовый f_data с разумными значениями."""
    defaults = {
        "words": 500,
        "has_h1": True,
        "has_summary": True,
        "has_tags": True,
        "link_density": 2.0,
        "has_toc": True,
        "example_density": 1.0,
        "has_callout": True,
    }
    defaults.update(kwargs)
    return defaults


def test_quality_score_perfect_doc():
    score = mod.quality_score(_make_data())
    assert score == 100.0


def test_quality_score_minimal_doc():
    # words=0 < 300 → ещё +10 за TOC-условие, поэтому минимум = 10
    data = _make_data(words=0, has_h1=False, has_summary=False,
                      has_tags=False, link_density=0, has_toc=False,
                      example_density=0, has_callout=False)
    assert mod.quality_score(data) == 10.0


def test_quality_score_range():
    for _ in range(5):
        data = _make_data(has_summary=False, has_tags=False)
        score = mod.quality_score(data)
        assert 0.0 <= score <= 100.0


def test_quality_score_has_summary_raises():
    without = mod.quality_score(_make_data(has_summary=False))
    with_s   = mod.quality_score(_make_data(has_summary=True))
    assert with_s > without


def test_quality_score_few_words_penalised():
    rich = mod.quality_score(_make_data(words=500))
    poor = mod.quality_score(_make_data(words=10))
    assert rich > poor


def test_quality_score_real_file():
    yodoca = ROOT / "docs" / "05-habr-projects" / "memory" / "yodoca.md"
    if not yodoca.exists():
        import pytest; pytest.skip("yodoca.md not found")
    text = yodoca.read_text(encoding="utf-8")
    words = len(text.split())
    data = {
        "words":           words,
        "has_h1":          "# " in text,
        "has_summary":     mod.has_summary(text),
        "has_tags":        mod.has_tags(text),
        "link_density":    mod.link_density(text),
        "has_toc":         mod.has_toc(text),
        "example_density": mod.example_density(text),
        "has_callout":     mod.has_callout(text),
    }
    score = mod.quality_score(data)
    assert score >= 50, f"yodoca.md quality too low: {score}"


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_metrics_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "METRICS.md").exists()


def test_main_metrics_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# Title\n\nContent here.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "METRICS.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "METRICS.md").exists()


def test_main_metrics_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "METRICS.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
