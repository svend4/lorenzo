"""Saved searches + alerts (Sprint 91 / S1).

Thin convenience layer on top of `docstoolkit.alerts.AlertStore` + `AlertRunner`
to register a `rag.ask()`-style query for periodic monitoring and fire
alerts when the top-K result set changes.

Usage:
    from docstoolkit.rag.saved import save_query, run_due_alerts

    qid = save_query("Yodoca updates",
                     query="Yodoca",
                     owner="alice",
                     interval_minutes=60)

    fired = run_due_alerts()
    for a in fired:
        print(a.query_id, a.reason)
"""
from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterable

from docstoolkit.alerts import (
    AlertRunner,
    AlertStore,
    FiredAlert,
    SavedQuery,
)
from docstoolkit.rag.pipeline import ask
from docstoolkit.rag.types import Passage


def _default_retriever(query: str, top_k: int = 5) -> list[Passage]:
    return ask(query, top_k=top_k).retrieved_passages


def save_query(
    query: str,
    *,
    owner: str = "default",
    schedule: str = "daily",
    top_k: int = 5,
    retriever_method: str = "hybrid",
    store: AlertStore | None = None,
) -> str:
    """Persist a SavedQuery in the AlertStore; return its id."""
    own = False
    if store is None:
        store = AlertStore()
        own = True
    try:
        q = SavedQuery(
            query=query,
            owner=owner,
            schedule=schedule,
            top_k=top_k,
            retriever_method=retriever_method,
        )
        return store.save(q)
    finally:
        if own:
            store.close()


def list_queries(
    owner: str = "",
    store: AlertStore | None = None,
) -> list[SavedQuery]:
    own = False
    if store is None:
        store = AlertStore()
        own = True
    try:
        return store.list_all(owner=owner)
    finally:
        if own:
            store.close()


def run_due_alerts(
    retriever: Callable[[str, int], list[Passage]] | None = None,
    *,
    store: AlertStore | None = None,
) -> list[FiredAlert]:
    """Run AlertRunner.tick() and return fired alerts (changed result sets)."""
    own = False
    if store is None:
        store = AlertStore()
        own = True
    try:
        runner = AlertRunner(
            store, retriever_fn=retriever or _default_retriever,
        )
        return runner.tick()
    finally:
        if own:
            store.close()
