"""Adaptive multi-hop retrieval: iterative refinement пока не достигнут порог уверенности.

Pattern (Self-RAG / FLARE-вдохновлённый):
  1. Initial query → retrieve top-k passages
  2. Score confidence of result set (overlap, score distribution)
  3. If confidence ниже threshold → reformulate query → retrieve more
  4. Stop когда confidence high OR max_hops reached
  5. Return объединённый ranked set + trace всех hops
"""
import re
import time
from dataclasses import dataclass, field

from docstoolkit.rag.retriever import Retriever
from docstoolkit.rag.types import Passage


@dataclass
class HopResult:
    """Один retrieval hop."""
    hop: int
    query: str
    passages: list[Passage] = field(default_factory=list)
    confidence: float = 0.0          # 0-1
    reason: str = ""                 # why hop ended (high_conf | reformulated | max_hops)
    duration_ms: int = 0


@dataclass
class AdaptiveResult:
    """Итог adaptive retrieval."""
    original_query: str
    hops: list[HopResult] = field(default_factory=list)
    final_passages: list[Passage] = field(default_factory=list)
    final_confidence: float = 0.0
    halted_reason: str = ""
    duration_ms: int = 0

    @property
    def total_hops(self) -> int:
        return len(self.hops)

    def to_markdown(self) -> str:
        lines = [f"# Adaptive retrieval: {self.original_query}\n"]
        lines.append(f"**Hops:** {self.total_hops}")
        lines.append(f"**Confidence:** {self.final_confidence:.2f}")
        lines.append(f"**Halted:** {self.halted_reason}")
        lines.append(f"**Duration:** {self.duration_ms}ms\n")
        lines.append("## Trace\n")
        lines.append("| Hop | Query | Passages | Conf | Reason |")
        lines.append("|----:|-------|---------:|-----:|--------|")
        for h in self.hops:
            q = h.query[:50] + ("…" if len(h.query) > 50 else "")
            lines.append(f"| {h.hop} | {q} | {len(h.passages)} | "
                         f"{h.confidence:.2f} | {h.reason} |")
        if self.final_passages:
            lines.append("\n## Final passages (top-5)\n")
            for i, p in enumerate(self.final_passages[:5], 1):
                lines.append(f"{i}. **{p.title or p.doc_id}** (score={p.score:.3f})")
        return "\n".join(lines)


def confidence_from_passages(passages: list[Passage]) -> float:
    """Heuristic 0-1 confidence:
       - 0 если 0 passages
       - higher если top score >> next scores (concentrated relevance)
       - higher если many passages with score>0
    """
    if not passages:
        return 0.0
    n = len(passages)
    scores = [p.score for p in passages if p.score > 0]
    if not scores:
        return 0.0
    top = scores[0]
    # mass at top: top / sum
    mass = top / (sum(scores) or 1.0)
    # coverage: число passages с осмысленным score (>=0.1*top)
    cov = sum(1 for s in scores if s >= 0.1 * top) / max(n, 1)
    # combine: 0.6 mass concentration + 0.4 coverage, но не выше 1
    return min(1.0, 0.6 * mass + 0.4 * cov)


def reformulate_query(original: str, passages: list[Passage],
                       hop: int) -> str:
    """Heuristic query reformulation без LLM:
       - extract salient terms из top passage title/text
       - комбинирует с оригиналом
    """
    if not passages:
        # Просто перефразируем — добавим контекст-trigger
        return f"{original} (context background)"

    top = passages[0]
    text_snippet = (top.title or "") + " " + (top.text[:300] or "")
    # tokens > 3 letters not in original
    orig_words = set(re.findall(r'\w+', original.lower()))
    candidates = [
        w for w in re.findall(r'[А-Яа-яA-Za-z]{4,}', text_snippet)
        if w.lower() not in orig_words
    ]
    # Take first 3 unique
    seen = set()
    pick = []
    for w in candidates:
        wl = w.lower()
        if wl not in seen:
            seen.add(wl)
            pick.append(w)
        if len(pick) >= 3:
            break

    if not pick:
        return f"{original} {hop}"
    return f"{original} {' '.join(pick)}"


def adaptive_search(query: str, *, retriever: Retriever | None = None,
                     top_k: int = 5, max_hops: int = 3,
                     confidence_threshold: float = 0.65,
                     reformulator=None,
                     confidence_fn=None,
                     method: str = "hybrid") -> AdaptiveResult:
    """Многохоповый поиск с reformulation."""
    t0 = time.time()
    result = AdaptiveResult(original_query=query)

    if retriever is None:
        retriever = Retriever(method=method)
    refn = reformulator or reformulate_query
    confn = confidence_fn or confidence_from_passages

    cur_query = query
    seen_doc_ids: set[str] = set()
    accumulated: list[Passage] = []

    for hop_idx in range(1, max_hops + 1):
        h_t0 = time.time()
        hop = HopResult(hop=hop_idx, query=cur_query)
        try:
            passages = retriever.search(cur_query, top_k=top_k)
        except Exception as e:
            hop.reason = f"error: {e}"
            hop.duration_ms = int((time.time() - h_t0) * 1000)
            result.hops.append(hop)
            result.halted_reason = f"hop {hop_idx} error: {e}"
            break

        hop.passages = passages
        hop.confidence = confn(passages)

        # Aggregate dedup
        for p in passages:
            if p.doc_id not in seen_doc_ids:
                seen_doc_ids.add(p.doc_id)
                accumulated.append(p)

        if hop.confidence >= confidence_threshold:
            hop.reason = f"high_confidence (≥{confidence_threshold:.2f})"
            hop.duration_ms = int((time.time() - h_t0) * 1000)
            result.hops.append(hop)
            result.halted_reason = "confidence_reached"
            break

        if hop_idx == max_hops:
            hop.reason = "max_hops"
            hop.duration_ms = int((time.time() - h_t0) * 1000)
            result.hops.append(hop)
            result.halted_reason = "max_hops"
            break

        # Reformulate for next hop
        new_query = refn(query, passages, hop_idx)
        hop.reason = f"reformulated → {new_query[:50]}"
        hop.duration_ms = int((time.time() - h_t0) * 1000)
        result.hops.append(hop)
        cur_query = new_query

    # Final ranking: re-sort accumulated by score desc, dedup keeping highest score
    accumulated.sort(key=lambda p: p.score, reverse=True)
    result.final_passages = accumulated[:top_k]
    result.final_confidence = confn(result.final_passages)
    result.duration_ms = int((time.time() - t0) * 1000)
    return result
