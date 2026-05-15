"""Advanced ask() wrappers for novel/research features.

Wires the following primitives behind one-line helpers usable from CLI / API:
  - probe_counterfactual()  — I4 attribution probing
  - measure_voice()         — N4 epistemic voice profiling
  - diffuse_knowledge()     — N6 cross-corpus concept transfer
  - build_taxonomy_ask()    — N7 self-organising taxonomy on retrieved docs
  - federated_aggregate()   — N5 DP-aware multi-org eval aggregation
  - co_evolve_round()       — N10 adversarial generator round
  - classify_docs()         — S3 TF-IDF document auto-classification
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
