"""
Тесты для scripts/improve_complexity.py.

Покрытие:
  - strip_md()         — очистка markdown-разметки
  - avg_sentence_len() — средняя длина предложений
  - term_density()     — доля технических терминов
  - heading_depth()    — максимальный уровень заголовка
  - complexity_score() — итоговый балл 0–5
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_complexity")

# ── strip_md ──────────────────────────────────────────────────────────────────

def test_strip_md_removes_code_blocks():
    text = "Before.\n```python\nprint('hello')\n```\nAfter."
    result = mod.strip_md(text)
    assert "print" not in result
    assert "Before" in result
    assert "After" in result


def test_strip_md_removes_comments():
    text = "Text. <!-- hidden comment --> More text."
    result = mod.strip_md(text)
    assert "hidden comment" not in result
    assert "More text" in result


def test_strip_md_removes_link_brackets():
    text = "See [AgentFS](docs/agentfs.md) for details."
    result = mod.strip_md(text)
    assert "[" not in result
    assert "]" not in result
    assert "AgentFS" in result  # link text preserved


def test_strip_md_removes_headings_hashes():
    text = "# Title\n## Section\nContent here."
    result = mod.strip_md(text)
    assert "#" not in result


def test_strip_md_returns_string():
    assert isinstance(mod.strip_md("text"), str)


def test_strip_md_empty():
    assert mod.strip_md("") == ""


def test_strip_md_removes_bold():
    text = "This is **bold** text and _italic_."
    result = mod.strip_md(text)
    assert "**" not in result
    assert "_" not in result

# ── avg_sentence_len ──────────────────────────────────────────────────────────

def test_avg_sentence_len_basic():
    text = "This is a sentence with exactly eight words here. Another one is also here."
    result = mod.avg_sentence_len(text)
    assert result > 0


def test_avg_sentence_len_empty():
    assert mod.avg_sentence_len("") == 0


def test_avg_sentence_len_short_sentences_filtered():
    # Sentences with < 3 words are filtered out
    text = "Ok. Yes. No. This sentence is long enough to be counted here."
    result = mod.avg_sentence_len(text)
    # Only the long sentence should be counted
    assert result > 5


def test_avg_sentence_len_returns_float():
    result = mod.avg_sentence_len("This is one sentence. This is another sentence.")
    assert isinstance(result, float)


def test_avg_sentence_len_longer_sentences_higher():
    short = "короткое. краткое. маленькое. малое здесь."
    long  = ("Это очень длинное предложение содержит много слов и информации. "
             "Ещё одно длинное предложение тоже присутствует в этом тексте.")
    assert mod.avg_sentence_len(long) > mod.avg_sentence_len(short)

# ── term_density ──────────────────────────────────────────────────────────────

def test_term_density_zero_no_terms():
    text = "обычный текст без технических терминов проекта"
    assert mod.term_density(text) == 0.0


def test_term_density_positive_with_terms():
    text = "mcp api rag llm используются в проекте svyazi"
    result = mod.term_density(text)
    assert result > 0


def test_term_density_returns_float():
    result = mod.term_density("mcp api text")
    assert isinstance(result, float)


def test_term_density_empty_text():
    assert mod.term_density("") == 0


def test_term_density_percentage():
    # 2 terms out of 4 words = 50%
    text = "mcp api word word"
    result = mod.term_density(text)
    assert result == pytest.approx(50.0)


def test_term_density_scales_with_term_count():
    few_terms  = "mcp word word word word word word word"
    many_terms = "mcp api rag llm word word word word"
    assert mod.term_density(many_terms) > mod.term_density(few_terms)

# ── heading_depth ─────────────────────────────────────────────────────────────

def test_heading_depth_no_headings():
    assert mod.heading_depth("Plain text no headings.") == 0


def test_heading_depth_h1_only():
    text = "# Title\n\nContent."
    assert mod.heading_depth(text) == 1


def test_heading_depth_max_level():
    text = "# H1\n## H2\n### H3\n#### H4\n"
    assert mod.heading_depth(text) == 4


def test_heading_depth_h6():
    text = "###### Deep heading\n"
    assert mod.heading_depth(text) == 6


def test_heading_depth_returns_int():
    result = mod.heading_depth("# Title")
    assert isinstance(result, int)

# ── complexity_score ──────────────────────────────────────────────────────────

def test_complexity_score_returns_int():
    result = mod.complexity_score(10.0, 0.5, 2, 500)
    assert isinstance(result, int)


def test_complexity_score_min_zero():
    result = mod.complexity_score(0.0, 0.0, 0, 0)
    assert result == 0


def test_complexity_score_max_five():
    result = mod.complexity_score(30.0, 5.0, 4, 5000)
    assert result == 5


def test_complexity_score_capped_at_five():
    # Even with extreme values, score caps at 5
    result = mod.complexity_score(100.0, 100.0, 6, 100000)
    assert result <= 5


def test_complexity_score_long_sentences_raises():
    low  = mod.complexity_score(10.0, 0.0, 0, 0)
    high = mod.complexity_score(30.0, 0.0, 0, 0)  # > 25 → +2
    assert high > low


def test_complexity_score_high_term_density_raises():
    low  = mod.complexity_score(10.0, 0.5, 0, 0)
    high = mod.complexity_score(10.0, 4.0, 0, 0)  # > 3 → +2
    assert high > low


def test_complexity_score_deep_headings_raises():
    low  = mod.complexity_score(10.0, 0.0, 2, 0)
    high = mod.complexity_score(10.0, 0.0, 4, 0)  # >= 4 → +1
    assert high > low


def test_complexity_score_many_words_raises():
    low  = mod.complexity_score(10.0, 0.0, 0, 500)
    high = mod.complexity_score(10.0, 0.0, 0, 5000)  # > 3000 → +2
    assert high > low


def test_complexity_score_medium_sentence_one_point():
    score = mod.complexity_score(20.0, 0.0, 0, 0)  # > 15 but <= 25 → +1
    assert score == 1
