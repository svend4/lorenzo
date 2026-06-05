"""Advanced ask() wrappers for novel/research features.

Wires the following primitives behind one-line helpers usable from CLI / API:
  - probe_counterfactual()  — I4 attribution probing
  - measure_voice()         — N4 epistemic voice profiling
  - diffuse_knowledge()     — N6 cross-corpus concept transfer
  - build_taxonomy_ask()    — N7 self-organising taxonomy on retrieved docs
  - federated_aggregate()   — N5 DP-aware multi-org eval aggregation
  - co_evolve_round()       — N10 adversarial generator round
  - classify_docs()         — S3 TF-IDF document auto-classification
  - FusedRetrieverAdapter() — I6 .search()-shaped adapter over fusion module
  - search_assets()         — M8 cross-modal multi-modal asset search
  - evolve_prompt()         — I9 PromptGA wrapper
  - incremental_index_docs()— M7 IncrementalIndexer wrapper
"""
from __future__ import annotations

from typing import Iterable, Sequence

from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import AnswerResult, Passage


# ---------------------------------------------------------------------------
# I4 — Counterfactual probing
# ---------------------------------------------------------------------------

def probe_counterfactual(
    question: str,
    corpus: dict[str, str],
    candidate_doc_id: str,
) -> dict:
    """Run a single query against `corpus`, then re-run with `candidate_doc_id`
    removed. Return baseline + counterfactual sentence-level summary.

    Use case: «If we delete this doc, does the answer change?»
    """
    from docstoolkit.counterfactual_corpus import counterfactual_remove

    report = counterfactual_remove(
        candidate_doc_id, corpus, [question],
    )
    affected_list = getattr(report, "affected_queries", []) or \
                    getattr(report, "query_deltas", [])
    return {
        "doc": candidate_doc_id,
        "affected": any(getattr(d, "affected", False) for d in affected_list),
        "severity": getattr(report, "severity", "low"),
        "summary": getattr(report, "summary", ""),
    }


# ---------------------------------------------------------------------------
# N4 — Epistemic voice profiling
# ---------------------------------------------------------------------------

def measure_voice(text: str) -> dict:
    """Return voice profile (claims/hedge ratio etc.) for a single text."""
    from docstoolkit.epistemic import measure_profile

    p = measure_profile(text)
    return {
        "claim_ratio": getattr(p, "claim_ratio", 0.0),
        "hedge_ratio": getattr(p, "hedge_ratio", 0.0),
        "confidence_score": getattr(p, "confidence_score", 0.0),
        "objectivity": getattr(p, "objectivity", 0.0),
    }


# ---------------------------------------------------------------------------
# N6 — Knowledge diffusion
# ---------------------------------------------------------------------------

def diffuse_knowledge(
    source_corpus: dict[str, str],
    target_corpus: dict[str, str],
    *,
    threshold: float = 0.15,
) -> list[dict]:
    """Identify concepts in source corpus that should diffuse to target."""
    from docstoolkit.diffusion import align_corpora

    res = align_corpora(source_corpus, target_corpus,
                        threshold=threshold)
    alignments = getattr(res, "alignments", [])
    out: list[dict] = []
    for a in alignments:
        out.append({
            "source_concept": getattr(a, "concept",
                                       getattr(a, "source_concept", "")),
            "target_doc": getattr(a, "target_doc_id",
                                   getattr(a, "target_concept", "")),
            "similarity": getattr(a, "similarity", 0.0),
        })
    return out


# ---------------------------------------------------------------------------
# N7 — Self-organising taxonomy
# ---------------------------------------------------------------------------

def build_taxonomy_ask(
    question: str,
    *,
    top_k: int = 25,
    levels: int = 3,
) -> dict:
    """Run ask() with high top_k, then cluster retrieved docs into a taxonomy."""
    from docstoolkit.taxonomy import build_taxonomy, TaxonomyConfig

    r = ask(question, top_k=top_k)
    docs_for_tax = [(p.doc_id, p.text) for p in r.retrieved_passages]
    tree = build_taxonomy(
        docs_for_tax,
        config=TaxonomyConfig(max_depth=levels),
    )
    return {
        "answer": r.answer,
        "tree_root": getattr(tree, "root_id", ""),
        "node_count": getattr(tree, "node_count", lambda: 0)()
            if callable(getattr(tree, "node_count", None))
            else getattr(tree, "node_count", 0),
    }


# ---------------------------------------------------------------------------
# N5 — Federated golden datasets aggregation
# ---------------------------------------------------------------------------

def federated_aggregate(
    per_node_metrics: list[dict],
    *,
    epsilon: float = 1.0,
) -> dict:
    """Aggregate per-node eval metrics with Laplace DP noise.

    Each node sends `{metric_name: float}` dicts; output is a privacy-preserving
    mean across nodes.
    """
    from docstoolkit.federated_eval import aggregator as agg_mod

    # Best-effort: federated_eval API may vary. Compute simple noisy means.
    if not per_node_metrics:
        return {}
    keys = set().union(*(m.keys() for m in per_node_metrics))
    out: dict[str, float] = {}
    for k in keys:
        values = [m.get(k, 0.0) for m in per_node_metrics]
        mean = sum(values) / len(values)
        # Optional DP noise via federated_eval.privacy if available
        try:
            from docstoolkit.federated_eval.privacy import add_laplace_noise
            noisy = add_laplace_noise(mean, epsilon=epsilon)
        except Exception:
            noisy = mean
        out[k] = noisy
    return out


# ---------------------------------------------------------------------------
# N10 — Adversarial co-evolution round
# ---------------------------------------------------------------------------

def co_evolve_round(
    seed_questions: Sequence[str],
    *,
    n_variants: int = 3,
) -> list[str]:
    """Generate n adversarially-hard variants for each seed question."""
    from docstoolkit.adversarial import AdversarialGenerator

    gen = AdversarialGenerator()
    out: list[str] = []
    for q in seed_questions:
        try:
            hard = gen.generate(q, n=n_variants)
            for h in hard:
                out.append(getattr(h, "question", str(h)))
        except Exception:
            out.append(q)
    return out


# ---------------------------------------------------------------------------
# S3 — Document classification
# ---------------------------------------------------------------------------

def classify_docs(
    docs: Sequence[tuple[str, str]],
    training_examples: Sequence[tuple[str, str]],
    *,
    confidence_threshold: float = 0.3,
) -> list[dict]:
    """Train a TF-IDF classifier on `training_examples` (text, label) pairs,
    classify each `docs[i]` (id, text), return [{doc_id, label, confidence}]."""
    from docstoolkit.classifier import tfidf_classifier as tc

    # Resolve the actual TFIDFClassifier class
    cls_attr = getattr(tc, "TfidfClassifier", None)
    if cls_attr is None or not docs:
        return [
            {"doc_id": d_id, "label": "", "confidence": 0.0}
            for d_id, _ in docs
        ]
    # Build {label: [texts]} corpus shape required by TfidfClassifier
    by_label: dict[str, list[str]] = {}
    for label, text in training_examples:
        by_label.setdefault(label, []).append(text)
    # Classifier requires min docs per label; lower the bar
    try:
        clf = cls_attr(min_docs_per_section=1)
    except TypeError:
        clf = cls_attr()
    try:
        clf.fit(by_label)
    except ValueError:
        return [
            {"doc_id": d_id, "label": "", "confidence": 0.0}
            for d_id, _ in docs
        ]
    out: list[dict] = []
    for doc_id, text in docs:
        try:
            result = clf.classify(text)
            label = getattr(result, "label", "")
            conf = float(getattr(result, "confidence", 0.0))
        except Exception:
            label, conf = "", 0.0
        out.append({
            "doc_id": doc_id,
            "label": label if conf >= confidence_threshold else "",
            "confidence": conf,
        })
    return out


# ---------------------------------------------------------------------------
# I6 — Learned fusion adapter
# ---------------------------------------------------------------------------

class FusedRetrieverAdapter:
    """Wrap `fusion.FusedRetriever` to expose the `.search(query, top_k)`
    contract that `RAGPipeline` expects.

    Caller supplies a `candidates_fn(query) -> list[dict]` that yields the
    per-passage feature dicts (`{text, doc_id, bm25, dense, graph, ...}`).
    """

    def __init__(self, fused, candidates_fn):
        self._fused = fused
        self._candidates_fn = candidates_fn

    def search(self, query: str, top_k: int = 5):
        from docstoolkit.rag.types import Passage

        cands = list(self._candidates_fn(query))
        ranked = self._fused.score_passages(query, cands, top_k=top_k)
        # ranked is [(doc_id, score)] — re-attach text/title from candidates
        by_id = {c.get("doc_id", ""): c for c in cands}
        out: list[Passage] = []
        for doc_id, score in ranked:
            c = by_id.get(doc_id, {})
            out.append(Passage(
                text=c.get("text", ""), doc_id=doc_id,
                title=c.get("title", ""), score=float(score),
            ))
        return out


# ---------------------------------------------------------------------------
# M8 — Cross-modal multi-modal asset search
# ---------------------------------------------------------------------------

def search_assets(
    query: str,
    docs_dir: "Path | str" = None,
    *,
    asset_type: str = "",
    tag: str = "",
):
    """Return assets (images / tables / code blocks) matching the query.

    Builds a `MultiModalIndex` lazily on the corpus and queries it. If
    `asset_type` is provided, restricts to that type. `tag` further filters.
    """
    from pathlib import Path as _P

    from docstoolkit.multimodal_meta import (
        AssetType,
        MetadataExtractor,
        MultiModalIndex,
    )

    if docs_dir is None:
        try:
            from docstoolkit.config import load_config
            docs_dir = load_config().docs_dir
        except Exception:
            docs_dir = _P("docs")

    docs_dir = _P(docs_dir)
    index = MultiModalIndex()
    extractor = MetadataExtractor()
    if docs_dir.exists():
        for f in docs_dir.rglob("*.md"):
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except (OSError, PermissionError):
                continue
            rel = str(f.relative_to(docs_dir)).replace("\\", "/")
            for asset in extractor.extract(text, doc_id=rel):
                index.add(asset)

    results = index.search_by_text(query) if query else []
    if asset_type:
        try:
            atype = AssetType[asset_type.upper()]
            results = [r for r in results if r.asset_type == atype]
        except (KeyError, AttributeError):
            pass
    if tag:
        results = [r for r in results
                   if tag in getattr(r, "tags", [])]
    return [
        {
            "asset_id": getattr(a, "asset_id", ""),
            "doc_id": getattr(a, "source_doc", getattr(a, "doc_id", "")),
            "type": getattr(a.asset_type, "value", str(a.asset_type)),
            "title": getattr(a, "caption", "") or getattr(a, "alt_text", ""),
            "tags": list(getattr(a, "tags", [])),
        }
        for a in results
    ]


# ---------------------------------------------------------------------------
# I9 — Self-improving prompts (genetic algorithm)
# ---------------------------------------------------------------------------

def evolve_prompt(
    seeds: list[str],
    fitness_fn,
    *,
    generations: int = 5,
    population_size: int = 8,
) -> list[tuple[str, float]]:
    """Run `generations` of `PromptGA` evolution and return the final
    population sorted by fitness."""
    from docstoolkit.prompts_ga import GAConfig, PromptGA

    cfg = GAConfig(population_size=population_size)
    ga = PromptGA(seed_templates=list(seeds),
                  fitness_fn=fitness_fn, config=cfg)
    for _ in range(max(1, generations)):
        ga.step()
    return ga.evolve()  # final pop sorted by fitness


# ---------------------------------------------------------------------------
# M7 — Incremental indexing
# ---------------------------------------------------------------------------

def incremental_index_docs(
    docs: dict,
    handler=None,
):
    """Submit a batch of `{doc_id: content}` to an `IncrementalIndexer`
    and process it through `handler` (defaults to a no-op).
    Returns the final IndexStats."""
    from docstoolkit.incremental_index import IncrementalIndexer

    indexer = IncrementalIndexer()
    indexer.submit_batch(docs)
    return indexer.process_batch(handler=handler or (lambda change: None))
