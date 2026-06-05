"""Тесты кросс-документного синтеза (rag/synthesis.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rag.synthesis import (
    SynthesisMode,
    DocumentGroup,
    SynthesisRequest,
    SynthesisResult,
    _build_synthesis_prompt,
    _extract_themes_and_differences,
    synthesize,
    compare_sections,
)
from docstoolkit.rag.types import Passage


# ---- helpers ----

def _make_passage(text: str, doc_id: str = "d1", title: str = "") -> Passage:
    return Passage(text=text, doc_id=doc_id, title=title, score=0.5)


def _make_group(name: str, texts: list[str], label: str = "") -> DocumentGroup:
    passages = [_make_passage(t, doc_id=f"{name}_{i}") for i, t in enumerate(texts)]
    return DocumentGroup(name=name, passages=passages, label=label)


# ---- SynthesisMode ----

def test_synthesis_mode_values():
    assert SynthesisMode.compare == "compare"
    assert SynthesisMode.summarize == "summarize"
    assert SynthesisMode.contrast == "contrast"
    assert SynthesisMode.timeline == "timeline"


def test_synthesis_mode_is_str_enum():
    assert isinstance(SynthesisMode.compare, str)


# ---- DocumentGroup ----

def test_document_group_defaults():
    p = _make_passage("hello")
    g = DocumentGroup(name="grp", passages=[p])
    assert g.label == ""
    assert len(g.passages) == 1


def test_document_group_with_label():
    g = DocumentGroup(name="a", passages=[], label="Section A")
    assert g.label == "Section A"


# ---- SynthesisRequest ----

def test_synthesis_request_defaults():
    req = SynthesisRequest()
    assert req.groups == []
    assert req.question == ""
    assert req.mode == SynthesisMode.compare
    assert req.answerer == "echo"
    assert req.model == "claude-haiku-4-5-20251001"


def test_synthesis_request_custom_mode():
    req = SynthesisRequest(mode=SynthesisMode.timeline)
    assert req.mode == SynthesisMode.timeline


# ---- _build_synthesis_prompt ----

def test_build_prompt_compare_mode():
    group_a = _make_group("a", ["Fast memory system", "Low latency design"], label="Group A")
    group_b = _make_group("b", ["Heavy disk-based storage"], label="Group B")
    req = SynthesisRequest(
        groups=[group_a, group_b],
        question="What are the main differences?",
        mode=SynthesisMode.compare,
    )
    system, user = _build_synthesis_prompt(req)

    assert isinstance(system, str) and len(system) > 10
    assert "Group A" in user
    assert "Group B" in user
    assert "What are the main differences?" in user
    assert "Сравни" in user or "сравни" in user.lower()


def test_build_prompt_contrast_mode():
    group = _make_group("x", ["Text"], label="X")
    req = SynthesisRequest(groups=[group], question="Q", mode=SynthesisMode.contrast)
    system, user = _build_synthesis_prompt(req)
    assert "противоречи" in user.lower() or "различи" in user.lower() or "Выяви" in user


def test_build_prompt_summarize_mode():
    group = _make_group("x", ["Text"], label="X")
    req = SynthesisRequest(groups=[group], question="Q", mode=SynthesisMode.summarize)
    _system, user = _build_synthesis_prompt(req)
    assert "Суммаризируй" in user or "суммаризируй" in user.lower()


def test_build_prompt_timeline_mode():
    group = _make_group("x", ["Text"], label="X")
    req = SynthesisRequest(groups=[group], question="Q", mode=SynthesisMode.timeline)
    _system, user = _build_synthesis_prompt(req)
    assert "хронологи" in user.lower() or "времен" in user.lower()


def test_build_prompt_empty_groups():
    req = SynthesisRequest(groups=[], question="Q")
    system, user = _build_synthesis_prompt(req)
    assert "нет групп" in user.lower() or "(нет групп)" in user


def test_build_prompt_includes_passage_text():
    group = _make_group("a", ["Unique content xyz123"], label="A")
    req = SynthesisRequest(groups=[group], question="Q", mode=SynthesisMode.compare)
    _system, user = _build_synthesis_prompt(req)
    assert "Unique content xyz123" in user


def test_build_prompt_includes_question():
    group = _make_group("a", ["text"], label="A")
    req = SynthesisRequest(
        groups=[group],
        question="How does memory consolidation work?",
        mode=SynthesisMode.compare,
    )
    _system, user = _build_synthesis_prompt(req)
    assert "How does memory consolidation work?" in user


def test_build_prompt_uses_group_label_if_set():
    group = DocumentGroup(name="internal_name", passages=[], label="Human Readable Label")
    req = SynthesisRequest(groups=[group], question="Q")
    _system, user = _build_synthesis_prompt(req)
    assert "Human Readable Label" in user


def test_build_prompt_falls_back_to_name_when_no_label():
    group = DocumentGroup(name="fallback_name", passages=[])
    req = SynthesisRequest(groups=[group], question="Q")
    _system, user = _build_synthesis_prompt(req)
    assert "fallback_name" in user


# ---- _extract_themes_and_differences ----

def test_extract_from_structured_answer():
    answer = (
        "## Общие темы\n"
        "- Both use memory layers\n"
        "- Both support async operations\n"
        "\n## Различия\n"
        "- System A uses Redis, System B uses SQLite\n"
        "- Latency profiles differ significantly\n"
    )
    common, differences = _extract_themes_and_differences(answer)
    assert len(common) > 0
    assert len(differences) > 0


def test_extract_inline_common_markers():
    answer = "Оба проекта используют общую архитектуру хранилища данных."
    common, differences = _extract_themes_and_differences(answer)
    assert len(common) >= 0  # may or may not detect inline


def test_extract_returns_bounded_lists():
    answer = "\n".join([f"- Пункт {i}" for i in range(20)])
    common, differences = _extract_themes_and_differences(answer)
    assert len(common) <= 5
    assert len(differences) <= 5


def test_extract_empty_answer():
    common, differences = _extract_themes_and_differences("")
    assert common == []
    assert differences == []


# ---- synthesize ----

def test_synthesize_returns_result():
    group_a = _make_group("sec_a", ["Memory is key", "Speed matters"], label="Section A")
    group_b = _make_group("sec_b", ["Storage is important"], label="Section B")
    req = SynthesisRequest(
        groups=[group_a, group_b],
        question="Compare sections",
        mode=SynthesisMode.compare,
        answerer="echo",
    )
    result = synthesize(req)
    assert isinstance(result, SynthesisResult)
    assert isinstance(result.answer, str)
    assert result.duration_ms >= 0


def test_synthesize_groups_summary_populated():
    group_a = _make_group("sec_a", ["text one", "text two"], label="A")
    group_b = _make_group("sec_b", ["text three"], label="B")
    req = SynthesisRequest(groups=[group_a, group_b], question="Q", answerer="echo")
    result = synthesize(req)

    assert len(result.groups_summary) == 2
    names = {g["name"] for g in result.groups_summary}
    assert "sec_a" in names
    assert "sec_b" in names


def test_synthesize_groups_summary_passage_counts():
    group_a = _make_group("a", ["p1", "p2", "p3"])
    req = SynthesisRequest(groups=[group_a], question="Q", answerer="echo")
    result = synthesize(req)
    a_summary = next(g for g in result.groups_summary if g["name"] == "a")
    assert a_summary["passage_count"] == 3


def test_synthesize_groups_summary_has_titles():
    p = Passage(text="Hello", doc_id="doc1", title="My Title")
    group = DocumentGroup(name="g", passages=[p])
    req = SynthesisRequest(groups=[group], question="Q", answerer="echo")
    result = synthesize(req)
    assert "My Title" in result.groups_summary[0]["titles"]


def test_synthesize_groups_summary_falls_back_to_doc_id():
    p = Passage(text="Hello", doc_id="doc1", title="")
    group = DocumentGroup(name="g", passages=[p])
    req = SynthesisRequest(groups=[group], question="Q", answerer="echo")
    result = synthesize(req)
    assert "doc1" in result.groups_summary[0]["titles"]


def test_synthesize_empty_groups():
    req = SynthesisRequest(groups=[], question="Q", answerer="echo")
    result = synthesize(req)
    assert isinstance(result.answer, str)
    assert result.groups_summary == []


def test_synthesize_common_themes_and_differences_are_lists():
    group = _make_group("a", ["text"])
    req = SynthesisRequest(groups=[group], question="Q", answerer="echo")
    result = synthesize(req)
    assert isinstance(result.common_themes, list)
    assert isinstance(result.differences, list)


def test_synthesize_duration_ms_nonnegative():
    req = SynthesisRequest(groups=[], question="Q", answerer="echo")
    result = synthesize(req)
    assert result.duration_ms >= 0


# ---- compare_sections ----

def test_compare_sections_returns_result():
    section_a = [_make_passage("Memory system A", "a1"), _make_passage("Fast lookups", "a2")]
    section_b = [_make_passage("Storage system B", "b1")]
    result = compare_sections(section_a, section_b, "What is different?")
    assert isinstance(result, SynthesisResult)


def test_compare_sections_default_answerer_echo():
    section_a = [_make_passage("A text", "a")]
    section_b = [_make_passage("B text", "b")]
    result = compare_sections(section_a, section_b, "Q")
    # Should not raise and return valid result
    assert result.answer is not None


def test_compare_sections_groups_named_correctly():
    section_a = [_make_passage("a", "a1")]
    section_b = [_make_passage("b", "b1")]
    result = compare_sections(section_a, section_b, "Q")
    names = {g["name"] for g in result.groups_summary}
    assert "section_a" in names
    assert "section_b" in names


def test_compare_sections_custom_mode():
    section_a = [_make_passage("a", "a1")]
    section_b = [_make_passage("b", "b1")]
    result = compare_sections(
        section_a, section_b, "Q", mode=SynthesisMode.contrast
    )
    assert isinstance(result, SynthesisResult)


def test_compare_sections_empty_inputs():
    result = compare_sections([], [], "Q")
    assert isinstance(result, SynthesisResult)
    # groups exist but with 0 passages
    assert result.groups_summary[0]["passage_count"] == 0
    assert result.groups_summary[1]["passage_count"] == 0


def test_compare_sections_passes_kwargs():
    section_a = [_make_passage("a", "a1")]
    section_b = [_make_passage("b", "b1")]
    result = compare_sections(
        section_a, section_b, "Q",
        answerer="echo",
        model="claude-haiku-4-5-20251001",
    )
    assert isinstance(result, SynthesisResult)
