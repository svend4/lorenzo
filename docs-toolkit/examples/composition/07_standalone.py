"""Standalone helpers: bandit A/B, voice profile, taxonomy, bulk diff,
counterfactual probe, asset search, knowledge diffusion.

These don't live inside ask() — they're separate one-line entry points
in docstoolkit.rag.*.
"""
from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

from docstoolkit.bandit import BanditExperiment
from docstoolkit.rag.advanced import (
    diffuse_knowledge,
    measure_voice,
    probe_counterfactual,
)
from docstoolkit.rag.bandit_ask import ask_with_bandit, evaluate_record
from docstoolkit.rag.bulk_diff import diff_corpus_dirs
from docstoolkit.rag.types import Passage


class _Retriever:
    def search(self, query, top_k):
        return [Passage(text="content", doc_id="d", title="D", score=0.7)]


class _Answerer:
    def answer(self, system, user, model=""):
        return "ok", 0, 0.0


def main() -> None:
    print("=" * 60)
    print("I7 — Bandit A/B retrieval-variant selection")
    print("=" * 60)
    exp = BanditExperiment("rag-AB", ["bm25", "hybrid", "semantic"])
    variants = {
        "bm25": {"method": "bm25"},
        "hybrid": {"method": "hybrid"},
        "semantic": {"method": "semantic"},
    }
    with patch("docstoolkit.rag.pipeline.Retriever",
               lambda **kw: _Retriever()), \
         patch("docstoolkit.rag.pipeline.get_answerer",
               lambda name, **kw: _Answerer()):
        for _ in range(5):
            result, picked = ask_with_bandit("query", exp, variants)
            evaluate_record(exp, picked, result, success_threshold=0.5)
    print(f"  After 5 rounds, bandit picks: {exp.choose()}")

    print("\n" + "=" * 60)
    print("N4 — Epistemic voice profiling")
    print("=" * 60)
    texts = {
        "claim-heavy": "Python is great. RAG is the future. AI wins.",
        "hedge-heavy": "It may be that some agents perhaps benefit "
                       "from possibly using memory in certain cases.",
    }
    for label, t in texts.items():
        v = measure_voice(t)
        print(f"  [{label}] claim={v['claim_ratio']:.2f} "
              f"hedge={v['hedge_ratio']:.2f}")

    print("\n" + "=" * 60)
    print("I4 — Counterfactual probing")
    print("=" * 60)
    corpus = {
        "a": "Python and RAG together solve grounding.",
        "b": "Docker provides reproducible deployment.",
        "c": "Python is also used for scripts and DevOps.",
    }
    res = probe_counterfactual("How is Python used?", corpus, "a")
    print(f"  Removing 'a' affected: {res['affected']}, "
          f"severity={res['severity']}")

    print("\n" + "=" * 60)
    print("S5 — Bulk diff between two corpus snapshots")
    print("=" * 60)
    with tempfile.TemporaryDirectory() as tmp:
        a = Path(tmp) / "a"
        b = Path(tmp) / "b"
        a.mkdir()
        b.mkdir()
        (a / "old.md").write_text("v1 content", encoding="utf-8")
        (a / "common.md").write_text("same", encoding="utf-8")
        (b / "new.md").write_text("brand new", encoding="utf-8")
        (b / "common.md").write_text("same", encoding="utf-8")
        diff = diff_corpus_dirs(a, b)
        print(f"  added: {diff.added}")
        print(f"  removed: {diff.removed}")
        print(f"  modified: {diff.modified}")

    print("\n" + "=" * 60)
    print("N6 — Knowledge diffusion between corpora")
    print("=" * 60)
    src = {"s1": "Python and RAG together solve grounding."}
    tgt = {"t1": "Python tutorials and beginner guides for newcomers."}
    diffs = diffuse_knowledge(src, tgt, threshold=0.05)
    print(f"  Found {len(diffs)} candidate concept alignments")
    for d in diffs[:3]:
        print(f"    - {d}")


if __name__ == "__main__":
    main()
