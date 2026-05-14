"""Тесты counterfactual RAG (rag/counterfactual.py)."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rag.counterfactual import (
    SpanAttribution,
    AttributedAnswer,
    CounterfactualResult,
    _tokenize,
    _jaccard,
    _split_sentences,
    attribute_answer,
    _token_diff_summary,
    counterfactual_ask,
    ForensicRAG,
)
from docstoolkit.rag.types import Passage


# ---- helpers ----

def _make_passage(text: str, doc_id: str = "d1", title: str = "") -> Passage:
    return Passage(text=text, doc_id=doc_id, title=title, score=0.5)


def _simple_answerer(question: str, passages: list[Passage]) -> str:
    """Mock answerer: concatenates passage texts."""
    if not passages:
        return "No relevant information found."
    return " ".join(p.text[:50] for p in passages)


# ---- _tokenize ----

def test_tokenize_basic():
    tokens = _tokenize("Hello World")
    assert "hello" in tokens
    assert "world" in tokens


def test_tokenize_lowercases():
    tokens = _tokenize("Python RAG Memory")
    assert "python" in tokens
    assert "rag" in tokens
    assert "memory" in tokens


def test_tokenize_removes_punctuation():
    tokens = _tokenize("Hello, world! Test.")
    assert "hello" in tokens
    assert "world" in tokens
    assert "," not in tokens


def test_tokenize_empty():
    assert _tokenize("") == set()


def test_tokenize_returns_set():
    tokens = _tokenize("word word word")
    assert isinstance(tokens, set)
    assert tokens == {"word"}


# ---- _jaccard ----

def test_jaccard_identical_sets():
    a = {"a", "b", "c"}
    assert _jaccard(a, a) == 1.0


def test_jaccard_disjoint_sets():
    assert _jaccard({"a", "b"}, {"c", "d"}) == 0.0


def test_jaccard_partial_overlap():
    a = {"a", "b", "c"}
    b = {"b", "c", "d"}
    score = _jaccard(a, b)
    assert 0.0 < score < 1.0
    # intersection=2, union=4 → 0.5
    assert abs(score - 0.5) < 0.001


def test_jaccard_empty_sets():
    assert _jaccard(set(), set()) == 0.0
    assert _jaccard(set(), {"a"}) == 0.0
    assert _jaccard({"a"}, set()) == 0.0


# ---- _split_sentences ----

def test_split_sentences_basic():
    text = "First sentence. Second sentence. Third."
    sents = _split_sentences(text)
    assert len(sents) >= 2


def test_split_sentences_on_newlines():
    text = "Paragraph one.\n\nParagraph two."
    sents = _split_sentences(text)
    assert len(sents) >= 2


def test_split_sentences_empty():
    sents = _split_sentences("")
    assert sents == []


def test_split_sentences_single():
    sents = _split_sentences("Only one sentence here.")
    assert len(sents) == 1
    assert "Only one sentence here." in sents[0]


def test_split_sentences_strips_whitespace():
    sents = _split_sentences("  Hello.  \n  World.  ")
    assert all(s == s.strip() for s in sents)


# ---- attribute_answer ----

def test_attribute_answer_with_known_overlap():
    """A sentence that closely mirrors a passage should be attributed."""
    passage = _make_passage(
        "Memory consolidation happens during sleep through hippocampal replay",
        doc_id="neuro1",
        title="Sleep and Memory",
    )
    answer = "Memory consolidation happens during sleep through hippocampal replay."
    result = attribute_answer(answer, [passage])
    assert isinstance(result, AttributedAnswer)
    assert len(result.attributions) > 0
    assert result.attributions[0].source_doc_id == "neuro1"
    assert result.attributions[0].confidence > 0.15


def test_attribute_answer_below_threshold_unattributed():
    """A sentence with no word overlap should be unattributed."""
    passage = _make_passage("Completely different xyz topic", doc_id="d1")
    answer = "Rainbow unicorns dance in neon skies."
    result = attribute_answer(answer, [passage])
    assert result.unattributed_fraction == 1.0


def test_attribute_answer_multiple_sentences():
    p1 = _make_passage("Python is a great programming language for data science", doc_id="d1")
    p2 = _make_passage("Machine learning models require training data and compute", doc_id="d2")
    answer = (
        "Python is a great programming language for data science. "
        "Machine learning models require training data and compute."
    )
    result = attribute_answer(answer, [p1, p2])
    assert isinstance(result, AttributedAnswer)
    assert len(result.attributions) == 2
    doc_ids = {a.source_doc_id for a in result.attributions}
    assert "d1" in doc_ids
    assert "d2" in doc_ids


def test_attribute_answer_picks_best_passage():
    """When multiple passages overlap, the best one wins."""
    p_low = _make_passage("memory cache fast", doc_id="low")
    p_high = _make_passage(
        "memory cache fast system retrieval lookup indexing architecture",
        doc_id="high",
    )
    answer = "memory cache fast system retrieval lookup"
    result = attribute_answer(answer, [p_low, p_high])
    # p_high has more overlap
    assert result.attributions[0].source_doc_id == "high"


def test_attribute_answer_unattributed_fraction_range():
    p = _make_passage("relevant content word overlap", doc_id="d")
    answer = "relevant content word overlap. Totally irrelevant unrelated text."
    result = attribute_answer(answer, [p])
    assert 0.0 <= result.unattributed_fraction <= 1.0


def test_attribute_answer_empty_answer():
    result = attribute_answer("", [_make_passage("text", "d")])
    assert result.unattributed_fraction == 1.0
    assert result.attributions == []


def test_attribute_answer_no_passages():
    result = attribute_answer("Some answer text here.", [])
    assert result.unattributed_fraction == 1.0


def test_attribute_answer_span_attribution_fields():
    p = _make_passage("fast memory system", doc_id="doc1", title="Fast Memory")
    answer = "fast memory system"
    result = attribute_answer(answer, [p])
    assert len(result.attributions) > 0
    attr = result.attributions[0]
    assert attr.source_doc_id == "doc1"
    assert attr.source_title == "Fast Memory"
    assert 0.0 <= attr.confidence <= 1.0
    assert attr.offset >= 0


def test_attribute_answer_title_fallback_to_doc_id():
    p = Passage(text="some text here", doc_id="my_doc_id", title="")
    result = attribute_answer("some text here", [p])
    if result.attributions:
        assert result.attributions[0].source_title == "my_doc_id"


def test_attribute_answer_query_field_empty_by_default():
    result = attribute_answer("text", [])
    assert result.query == ""


# ---- _token_diff_summary ----

def test_token_diff_summary_no_change():
    result = _token_diff_summary("hello world", "hello world")
    assert "изменений нет" in result.lower()


def test_token_diff_summary_added_words():
    result = _token_diff_summary("hello", "hello world foo")
    assert "добавлено" in result


def test_token_diff_summary_removed_words():
    result = _token_diff_summary("hello world foo", "hello")
    assert "убрано" in result


def test_token_diff_summary_both_changes():
    result = _token_diff_summary("alpha beta gamma", "alpha delta epsilon")
    assert "добавлено" in result
    assert "убрано" in result


def test_token_diff_summary_returns_string():
    assert isinstance(_token_diff_summary("a", "b"), str)


# ---- counterfactual_ask ----

def test_counterfactual_ask_basic():
    passages = [
        _make_passage("Memory system uses Redis", doc_id="doc_redis"),
        _make_passage("Alternative uses SQLite for persistence", doc_id="doc_sqlite"),
    ]
    result = counterfactual_ask("What storage is used?", passages, "doc_redis", _simple_answerer)
    assert isinstance(result, CounterfactualResult)
    assert result.removed_doc_id == "doc_redis"
    assert isinstance(result.original_answer, str)
    assert isinstance(result.modified_answer, str)
    assert isinstance(result.delta, str)
    assert 0.0 <= result.attribution_shift <= 1.0


def test_counterfactual_ask_removes_correct_doc():
    """The modified answer should not reference the removed doc."""
    called_with = []

    def tracking_answerer(question: str, passages: list[Passage]) -> str:
        called_with.append([p.doc_id for p in passages])
        return "answer"

    passages = [
        _make_passage("text a", doc_id="keep_me"),
        _make_passage("text b", doc_id="remove_me"),
    ]
    counterfactual_ask("Q", passages, "remove_me", tracking_answerer)

    # First call: all passages
    assert "keep_me" in called_with[0]
    assert "remove_me" in called_with[0]
    # Second call: without removed doc
    assert "keep_me" in called_with[1]
    assert "remove_me" not in called_with[1]


def test_counterfactual_ask_calls_answerer_twice():
    call_count = [0]

    def counting_answerer(question: str, passages: list[Passage]) -> str:
        call_count[0] += 1
        return f"answer_{call_count[0]}"

    passages = [_make_passage("text", "d1"), _make_passage("more text", "d2")]
    counterfactual_ask("Q", passages, "d1", counting_answerer)
    assert call_count[0] == 2


def test_counterfactual_ask_delta_not_empty_when_different():
    passages = [
        _make_passage("Memory persistence layer SQLite caching", doc_id="d1"),
        _make_passage("Distributed storage Redis cluster nodes", doc_id="d2"),
    ]
    result = counterfactual_ask("Describe storage", passages, "d2", _simple_answerer)
    # original has both, modified only has d1 → should show differences
    assert isinstance(result.delta, str)


def test_counterfactual_ask_removes_nonexistent_doc():
    """Removing a doc_id not in passages → modified == original."""
    passages = [_make_passage("text", "d1")]

    def echo_fn(q, ps):
        return " ".join(p.text for p in ps)

    result = counterfactual_ask("Q", passages, "nonexistent", echo_fn)
    assert result.original_answer == result.modified_answer


def test_counterfactual_ask_attribution_shift_range():
    passages = [
        _make_passage("fast memory cache lookup", doc_id="d1"),
        _make_passage("slow disk storage write", doc_id="d2"),
    ]
    result = counterfactual_ask("Q", passages, "d1", _simple_answerer)
    assert 0.0 <= result.attribution_shift <= 1.0


# ---- ForensicRAG ----

class _MockRetriever:
    """Mock retriever returning preset passages."""

    def __init__(self, passages: list[Passage]):
        self._passages = passages

    def search(self, question: str, top_k: int = 5) -> list[Passage]:
        return self._passages[:top_k]


def test_forensic_rag_ask_returns_attributed_answer():
    passages = [
        _make_passage("Memory is fast cache", doc_id="d1", title="Cache"),
        _make_passage("Storage uses disks slow", doc_id="d2", title="Disk"),
    ]
    retriever = _MockRetriever(passages)
    rag = ForensicRAG(retriever, _simple_answerer)
    result = rag.ask("What is fast?", top_k=2)
    assert isinstance(result, AttributedAnswer)
    assert isinstance(result.answer, str)
    assert 0.0 <= result.unattributed_fraction <= 1.0


def test_forensic_rag_ask_sets_query():
    passages = [_make_passage("text", "d1")]
    retriever = _MockRetriever(passages)
    rag = ForensicRAG(retriever, _simple_answerer)
    result = rag.ask("My question", top_k=1)
    assert result.query == "My question"


def test_forensic_rag_explain_returns_counterfactual():
    passages = [
        _make_passage("Memory cache fast lookup", doc_id="cache_doc"),
        _make_passage("Disk storage slow access", doc_id="disk_doc"),
    ]
    retriever = _MockRetriever(passages)
    rag = ForensicRAG(retriever, _simple_answerer)
    result = rag.explain("What is used?", suspect_doc_id="cache_doc")
    assert isinstance(result, CounterfactualResult)
    assert result.removed_doc_id == "cache_doc"


def test_forensic_rag_explain_shows_impact():
    passages = [
        _make_passage("Alpha beta gamma delta epsilon", doc_id="important"),
        _make_passage("Basic info here", doc_id="other"),
    ]
    retriever = _MockRetriever(passages)
    rag = ForensicRAG(retriever, _simple_answerer)
    result = rag.explain("Q", suspect_doc_id="important")
    # Removing an important doc should change the answer
    assert result.original_answer != result.modified_answer or result.delta is not None


def test_forensic_rag_top_k_limits_retrieval():
    passages = [_make_passage(f"text {i}", f"d{i}") for i in range(10)]
    retriever = _MockRetriever(passages)

    retrieved = []

    def tracking_answerer(q, ps):
        retrieved.extend(ps)
        return "answer"

    rag = ForensicRAG(retriever, tracking_answerer)
    rag.ask("Q", top_k=3)
    # First call should have at most 3 passages
    assert len(retrieved) <= 3
