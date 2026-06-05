"""PageRank-boosted retrieval: цитатный авторитет влияет на ранжирование.

Sprint 56 / S4 — Citation graph + PageRank boost.

Использование:
    from docstoolkit.citations.boost import PageRankBoostedRetriever

    base = Retriever(method="hybrid")
    boosted = PageRankBoostedRetriever(base, corpus_dir=Path("docs"),
                                       alpha=0.3, cap=0.4)
    results = boosted.search("query", top_k=5)
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Iterable

from docstoolkit.citations.graph import build_citation_graph, pagerank
from docstoolkit.rag.types import Passage


@dataclass
class PageRankBoostedRetriever:
    """Wrap a base retriever; multiply scores by `(1 + alpha * min(pr, cap))`.

    Cap prevents one highly-cited document from dominating every query.
    PageRank scores are computed once (lazy) and cached in-instance.
    """

    base: object
    corpus_dir: Path | None = None
    alpha: float = 0.3
    cap: float = 0.4
    pr_scores: dict[str, float] | None = None
    _max_pr: float = field(default=0.0, init=False, repr=False)

    def _ensure_pr(self) -> None:
        if self.pr_scores is not None:
            self._max_pr = max(self.pr_scores.values(), default=0.0)
            return
        if self.corpus_dir is None:
            self.pr_scores = {}
            return
        graph = build_citation_graph(Path(self.corpus_dir))
        self.pr_scores = pagerank(graph)
        self._max_pr = max(self.pr_scores.values(), default=0.0)

    def _normalize(self, pr: float) -> float:
        """Scale to [0, 1] using observed max, then clip by cap."""
        if self._max_pr <= 0:
            return 0.0
        norm = pr / self._max_pr
        return min(norm, self.cap)

    def search(self, query: str, top_k: int = 5) -> list[Passage]:
        self._ensure_pr()
        # Pull a wider window so re-ranking is meaningful.
        candidates: list[Passage] = self.base.search(query, top_k=top_k * 2)
        scored: list[Passage] = []
        for p in candidates:
            pr = self.pr_scores.get(p.doc_id, 0.0)
            boost = 1.0 + self.alpha * self._normalize(pr)
            new_score = p.score * boost
            try:
                scored.append(replace(p, score=new_score))
            except TypeError:
                scored.append(Passage(
                    text=p.text, doc_id=p.doc_id,
                    title=p.title, score=new_score,
                    snippet_start=getattr(p, "snippet_start", 0),
                ))
        scored.sort(key=lambda x: -x.score)
        return scored[:top_k]


def build_pr_lookup(corpus_dir: Path) -> dict[str, float]:
    """Convenience: compute PageRank for `corpus_dir` and return the dict."""
    graph = build_citation_graph(Path(corpus_dir))
    return pagerank(graph)


def boost_scores(
    passages: Iterable[Passage],
    pr_scores: dict[str, float],
    alpha: float = 0.3,
    cap: float = 0.4,
) -> list[Passage]:
    """Apply PageRank boost to a sequence of passages without re-ordering callers.

    Returns NEW Passage instances (no mutation). Sorting is the caller's choice.
    """
    if not pr_scores:
        return list(passages)
    max_pr = max(pr_scores.values())
    if max_pr <= 0:
        return list(passages)
    out: list[Passage] = []
    for p in passages:
        pr = pr_scores.get(p.doc_id, 0.0)
        norm = min(pr / max_pr, cap)
        boost = 1.0 + alpha * norm
        try:
            out.append(replace(p, score=p.score * boost))
        except TypeError:
            out.append(Passage(
                text=p.text, doc_id=p.doc_id, title=p.title,
                score=p.score * boost,
                snippet_start=getattr(p, "snippet_start", 0),
            ))
    return out
