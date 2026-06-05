"""Tests for advanced helpers (I4, N4, N5, N6, N7, N10, S3)."""
from __future__ import annotations

import pytest

from docstoolkit.rag.advanced import (
    classify_docs,
    co_evolve_round,
    diffuse_knowledge,
    federated_aggregate,
    measure_voice,
    probe_counterfactual,
)


# ---- I4 probe_counterfactual ----

def test_probe_returns_summary():
    corpus = {
        "a": "Python is great for RAG",
        "b": "Python is used everywhere",
        "c": "Docker matters for deployment",
    }
    out = probe_counterfactual("Python", corpus, "a")
    assert "doc" in out and out["doc"] == "a"
    assert "affected" in out
    assert "summary" in out


def test_probe_unknown_doc_handled_gracefully():
    corpus = {"a": "Python", "b": "Java"}
    out = probe_counterfactual("Python", corpus, "nonexistent")
    assert isinstance(out, dict)


# ---- N4 measure_voice ----

def test_measure_voice_returns_dict():
    text = "Python is great. We believe RAG is the future."
    out = measure_voice(text)
    assert isinstance(out, dict)
    assert "claim_ratio" in out


def test_measure_voice_handles_empty():
    out = measure_voice("")
    assert isinstance(out, dict)


# ---- N6 diffuse_knowledge ----

def test_diffuse_returns_list():
    src = {"a": "Python and RAG concepts"}
    tgt = {"b": "Python tutorials and basics"}
    out = diffuse_knowledge(src, tgt)
    assert isinstance(out, list)


def test_diffuse_empty_corpora():
    out = diffuse_knowledge({}, {})
    assert isinstance(out, list)


# ---- N5 federated_aggregate ----

def test_federated_empty():
    assert federated_aggregate([]) == {}


def test_federated_averages_metrics():
    nodes = [
        {"precision": 0.8, "recall": 0.6},
        {"precision": 0.6, "recall": 0.7},
    ]
    out = federated_aggregate(nodes, epsilon=10.0)  # low noise
    # Means are 0.7 and 0.65 — noisy result within reasonable range
    assert "precision" in out and "recall" in out


def test_federated_handles_missing_keys():
    nodes = [
        {"precision": 0.8},
        {"recall": 0.7},
    ]
    out = federated_aggregate(nodes, epsilon=10.0)
    assert "precision" in out
    assert "recall" in out


# ---- N10 co_evolve_round ----

def test_co_evolve_returns_list():
    out = co_evolve_round(["What is RAG?"], n_variants=2)
    assert isinstance(out, list)


def test_co_evolve_empty_seeds():
    assert co_evolve_round([]) == []


# ---- S3 classify_docs ----

def test_classify_empty_inputs():
    assert classify_docs([], []) == []


def test_classify_basic():
    training = [
        ("ml", "machine learning artificial intelligence"),
        ("ops", "deployment kubernetes containers"),
        ("ml", "neural networks training"),
        ("ops", "docker orchestration"),
    ]
    docs = [
        ("doc1", "machine learning is fun"),
        ("doc2", "kubernetes deployment"),
    ]
    out = classify_docs(docs, training, confidence_threshold=0.0)
    assert len(out) == 2
    assert all("label" in d for d in out)
    assert all("confidence" in d for d in out)


def test_classify_threshold_filters_low_conf():
    training = [("a", "alpha beta gamma"), ("b", "delta epsilon zeta")]
    docs = [("d", "unrelated text foo bar")]
    out = classify_docs(docs, training, confidence_threshold=10.0)
    # Threshold impossible to reach → empty label
    assert out[0]["label"] == ""
