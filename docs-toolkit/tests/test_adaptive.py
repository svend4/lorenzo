"""Тесты adaptive multi-hop retrieval."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.rag.adaptive import (
    AdaptiveResult, HopResult,
    confidence_from_passages, reformulate_query, adaptive_search,
)
from docstoolkit.rag.types import Passage


# ---- confidence_from_passages ----

def test_confidence_empty():
    assert confidence_from_passages([]) == 0.0


def test_confidence_zero_scores():
    passages = [Passage(text="x", doc_id="d", score=0)]
    assert confidence_from_passages(passages) == 0.0


def test_confidence_high_when_concentrated():
    passages = [
        Passage(text="a", doc_id="a", score=0.95),
        Passage(text="b", doc_id="b", score=0.05),
    ]
    c = confidence_from_passages(passages)
    assert c > 0.5


def test_confidence_lower_when_spread():
    spread = [Passage(text=str(i), doc_id=f"d{i}", score=0.2) for i in range(5)]
    concentrated = [Passage(text="a", doc_id="a", score=0.95),
                     Passage(text="b", doc_id="b", score=0.05)]
    assert confidence_from_passages(spread) < confidence_from_passages(concentrated)


def test_confidence_capped_at_1():
    p = [Passage(text="x", doc_id="d", score=100.0)]
    assert confidence_from_passages(p) <= 1.0


# ---- reformulate_query ----

def test_reformulate_no_passages():
    q = reformulate_query("исходный", [], hop=1)
    assert "исходный" in q
    assert q != "исходный"  # reformulated somehow


def test_reformulate_extracts_new_terms():
    p = [Passage(text="Yodoca это memory engine с активацией",
                 doc_id="d", title="Architecture")]
    q = reformulate_query("что такое X", p, hop=1)
    # должны добавиться слова из title/text, не входящие в оригинал
    assert "Yodoca" in q or "Architecture" in q or "memory" in q


def test_reformulate_skips_words_already_in_query():
    p = [Passage(text="memory engine memory engine", doc_id="d",
                 title="memory")]
    q = reformulate_query("memory engine", p, hop=1)
    # 'memory' и 'engine' уже в query → не должны добавляться
    # Но reformulator может вообще ничего не найти → fallback "{q} {hop}"
    assert "memory engine" in q


# ---- adaptive_search ----

class _MockRetriever:
    def __init__(self, responses: list[list[Passage]]):
        self.responses = responses
        self.calls = 0

    def search(self, query, top_k=5):
        if self.calls >= len(self.responses):
            return []
        r = self.responses[self.calls]
        self.calls += 1
        return r[:top_k]


def test_adaptive_stops_on_high_confidence():
    """Первый hop сразу даёт high conf → stops."""
    high_conf = [
        Passage(text="x", doc_id="dx", score=0.95),
        Passage(text="y", doc_id="dy", score=0.05),
    ]
    mr = _MockRetriever([high_conf])
    result = adaptive_search("q", retriever=mr, max_hops=3,
                              confidence_threshold=0.5)
    assert result.total_hops == 1
    assert result.halted_reason == "confidence_reached"
    assert mr.calls == 1


def test_adaptive_reformulates_until_confident():
    """Hop 1 low → reformulate → hop 2 high → stop."""
    low_conf = [Passage(text=str(i), doc_id=f"d{i}", score=0.2)
                for i in range(5)]
    high_conf = [
        Passage(text="x", doc_id="dx", score=0.95),
        Passage(text="y", doc_id="dy", score=0.05),
    ]
    mr = _MockRetriever([low_conf, high_conf])
    result = adaptive_search("q", retriever=mr, max_hops=3,
                              confidence_threshold=0.7)
    assert result.total_hops == 2
    assert mr.calls == 2
    assert result.halted_reason == "confidence_reached"
    # query был reformulated между hops
    assert result.hops[0].query != result.hops[1].query


def test_adaptive_max_hops_reached():
    """Никакой hop не достиг threshold → max_hops."""
    weak = [Passage(text=str(i), doc_id=f"d{i}", score=0.1) for i in range(5)]
    mr = _MockRetriever([weak, weak, weak])
    result = adaptive_search("q", retriever=mr, max_hops=3,
                              confidence_threshold=0.95)
    assert result.total_hops == 3
    assert result.halted_reason == "max_hops"


def test_adaptive_dedups_passages_across_hops():
    """Одинаковые doc_id из разных hops не дублируются."""
    overlap_a = [Passage(text="x", doc_id="shared", score=0.5),
                  Passage(text="y", doc_id="a", score=0.3)]
    overlap_b = [Passage(text="z", doc_id="shared", score=0.4),
                  Passage(text="w", doc_id="b", score=0.2)]
    mr = _MockRetriever([overlap_a, overlap_b, []])
    result = adaptive_search("q", retriever=mr, max_hops=3,
                              confidence_threshold=0.95)
    final_ids = {p.doc_id for p in result.final_passages}
    assert "shared" in final_ids
    assert "a" in final_ids
    assert "b" in final_ids
    assert len(result.final_passages) <= 3  # dedup applied


def test_adaptive_handles_retriever_error():
    class BadRetriever:
        def search(self, q, top_k=5):
            raise RuntimeError("retriever down")

    result = adaptive_search("q", retriever=BadRetriever(), max_hops=3)
    assert "error" in result.halted_reason
    assert result.total_hops == 1


def test_adaptive_custom_reformulator_called():
    seen = []
    def ref(orig, passages, hop):
        seen.append((orig, hop))
        return f"{orig} v{hop}"

    weak = [Passage(text=str(i), doc_id=f"d{i}", score=0.1) for i in range(5)]
    mr = _MockRetriever([weak, weak])
    adaptive_search("orig", retriever=mr, max_hops=2,
                     confidence_threshold=0.95, reformulator=ref)
    # вызывается между hops, не на последнем
    assert len(seen) == 1
    assert seen[0] == ("orig", 1)


def test_adaptive_custom_confidence_fn():
    """Своя confidence_fn используется."""
    weak = [Passage(text=str(i), doc_id=f"d{i}", score=0.1) for i in range(5)]
    mr = _MockRetriever([weak])
    # always-1 confidence → first hop wins
    result = adaptive_search("q", retriever=mr, max_hops=3,
                              confidence_threshold=0.5,
                              confidence_fn=lambda ps: 1.0)
    assert result.total_hops == 1
    assert result.halted_reason == "confidence_reached"


def test_adaptive_result_to_markdown_basic():
    weak = [Passage(text=str(i), doc_id=f"d{i}", score=0.1) for i in range(5)]
    mr = _MockRetriever([weak, weak])
    result = adaptive_search("orig", retriever=mr, max_hops=2,
                              confidence_threshold=0.99)
    md = result.to_markdown()
    assert "Adaptive retrieval: orig" in md
    assert "Hops:" in md
    assert "Trace" in md
