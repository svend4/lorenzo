"""Tests for E415 DocNamespaceStore."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_namespace_store import (
    DocNamespaceStore,
    Namespace,
    NamespaceStats,
)


# --------------------------------------------------------------------------- fixtures


@pytest.fixture()
def store() -> DocNamespaceStore:
    return DocNamespaceStore()


@pytest.fixture()
def populated(store: DocNamespaceStore) -> DocNamespaceStore:
    store.create_namespace("ns1", "Alpha", "first", now=100.0)
    store.create_namespace("ns2", "Beta", "second", now=200.0)
    store.add_doc("ns1", "d1")
    store.add_doc("ns1", "d2")
    store.add_doc("ns2", "d3")
    return store


# --------------------------------------------------------------------------- exports


def test_exports_namespace():
    assert Namespace is not None


def test_exports_namespace_stats():
    assert NamespaceStats is not None


def test_exports_store():
    assert DocNamespaceStore is not None


# --------------------------------------------------------------------------- create_namespace


def test_create_namespace_returns_namespace(store):
    ns = store.create_namespace("a", "Alpha")
    assert isinstance(ns, Namespace)
    assert ns.namespace_id == "a"
    assert ns.name == "Alpha"
    assert ns.description == ""


def test_create_namespace_with_description(store):
    ns = store.create_namespace("a", "Alpha", "desc")
    assert ns.description == "desc"


def test_create_namespace_with_now(store):
    ns = store.create_namespace("a", "Alpha", now=42.0)
    assert ns.created_at == 42.0


def test_create_namespace_auto_timestamp(store):
    ns = store.create_namespace("a", "Alpha")
    assert ns.created_at > 0


def test_create_namespace_duplicate_raises(store):
    store.create_namespace("a", "Alpha")
    with pytest.raises(ValueError):
        store.create_namespace("a", "Alpha2")


def test_create_namespace_empty_id_raises(store):
    with pytest.raises(ValueError):
        store.create_namespace("", "Alpha")


def test_create_namespace_empty_name_raises(store):
    with pytest.raises(ValueError):
        store.create_namespace("a", "")


def test_create_namespace_persists(store):
    store.create_namespace("a", "Alpha")
    assert store.get_namespace("a") is not None


# --------------------------------------------------------------------------- get_namespace


def test_get_namespace_existing(populated):
    ns = populated.get_namespace("ns1")
    assert ns is not None
    assert ns.name == "Alpha"


def test_get_namespace_missing_returns_none(store):
    assert store.get_namespace("nope") is None


def test_get_namespace_after_delete(populated):
    populated.delete_namespace("ns1")
    assert populated.get_namespace("ns1") is None


# --------------------------------------------------------------------------- list_namespaces


def test_list_namespaces_empty(store):
    assert store.list_namespaces() == []


def test_list_namespaces_sorted_by_name(store):
    store.create_namespace("z", "Zeta")
    store.create_namespace("a", "Alpha")
    store.create_namespace("m", "Mu")
    names = [n.name for n in store.list_namespaces()]
    assert names == ["Alpha", "Mu", "Zeta"]


def test_list_namespaces_returns_list(populated):
    assert isinstance(populated.list_namespaces(), list)


def test_list_namespaces_count(populated):
    assert len(populated.list_namespaces()) == 2


# --------------------------------------------------------------------------- delete_namespace


def test_delete_namespace_returns_true(populated):
    assert populated.delete_namespace("ns1") is True


def test_delete_namespace_missing_returns_false(store):
    assert store.delete_namespace("nope") is False


def test_delete_namespace_removes_it(populated):
    populated.delete_namespace("ns1")
    assert populated.get_namespace("ns1") is None


def test_delete_namespace_removes_doc_memberships(populated):
    populated.delete_namespace("ns1")
    assert populated.namespace_of("d1") is None
    assert populated.namespace_of("d2") is None


def test_delete_namespace_keeps_others(populated):
    populated.delete_namespace("ns1")
    assert populated.get_namespace("ns2") is not None
    assert populated.namespace_of("d3") == "ns2"


# --------------------------------------------------------------------------- add_doc


def test_add_doc_new_returns_true(store):
    store.create_namespace("a", "Alpha")
    assert store.add_doc("a", "d1") is True


def test_add_doc_unknown_namespace_raises(store):
    with pytest.raises(KeyError):
        store.add_doc("nope", "d1")


def test_add_doc_persists(store):
    store.create_namespace("a", "Alpha")
    store.add_doc("a", "d1")
    assert "d1" in store.docs_in_namespace("a")


def test_add_doc_same_namespace_returns_false(store):
    store.create_namespace("a", "Alpha")
    store.add_doc("a", "d1")
    assert store.add_doc("a", "d1") is False


def test_add_doc_moves_from_other_namespace(store):
    store.create_namespace("a", "Alpha")
    store.create_namespace("b", "Beta")
    store.add_doc("a", "d1")
    result = store.add_doc("b", "d1")
    assert result is False  # moved, not newly added
    assert store.namespace_of("d1") == "b"
    assert "d1" not in store.docs_in_namespace("a")


def test_add_doc_increments_count(store):
    store.create_namespace("a", "Alpha")
    store.add_doc("a", "d1")
    store.add_doc("a", "d2")
    assert store.doc_count_in("a") == 2


# --------------------------------------------------------------------------- remove_doc


def test_remove_doc_existing(populated):
    assert populated.remove_doc("ns1", "d1") is True


def test_remove_doc_missing_returns_false(populated):
    assert populated.remove_doc("ns1", "nope") is False


def test_remove_doc_unknown_namespace(populated):
    assert populated.remove_doc("nope", "d1") is False


def test_remove_doc_clears_membership(populated):
    populated.remove_doc("ns1", "d1")
    assert populated.namespace_of("d1") is None


def test_remove_doc_wrong_namespace_does_nothing(populated):
    # d1 is in ns1, not ns2
    assert populated.remove_doc("ns2", "d1") is False
    assert populated.namespace_of("d1") == "ns1"


# --------------------------------------------------------------------------- move_doc


def test_move_doc_success(populated):
    assert populated.move_doc("d1", "ns2") is True
    assert populated.namespace_of("d1") == "ns2"


def test_move_doc_unknown_namespace_raises(populated):
    with pytest.raises(KeyError):
        populated.move_doc("d1", "nope")


def test_move_doc_for_unattached_returns_false(populated):
    assert populated.move_doc("unknown_doc", "ns1") is False


def test_move_doc_to_same_namespace_returns_true(populated):
    assert populated.move_doc("d1", "ns1") is True
    assert populated.namespace_of("d1") == "ns1"


def test_move_doc_removes_from_old_namespace(populated):
    populated.move_doc("d1", "ns2")
    assert "d1" not in populated.docs_in_namespace("ns1")
    assert "d1" in populated.docs_in_namespace("ns2")


# --------------------------------------------------------------------------- namespace_of


def test_namespace_of_existing(populated):
    assert populated.namespace_of("d1") == "ns1"
    assert populated.namespace_of("d3") == "ns2"


def test_namespace_of_missing(store):
    assert store.namespace_of("nope") is None


# --------------------------------------------------------------------------- docs_in_namespace


def test_docs_in_namespace_sorted(store):
    store.create_namespace("a", "Alpha")
    store.add_doc("a", "z")
    store.add_doc("a", "a")
    store.add_doc("a", "m")
    assert store.docs_in_namespace("a") == ["a", "m", "z"]


def test_docs_in_namespace_empty(store):
    store.create_namespace("a", "Alpha")
    assert store.docs_in_namespace("a") == []


def test_docs_in_namespace_unknown(store):
    assert store.docs_in_namespace("nope") == []


# --------------------------------------------------------------------------- doc_count_in


def test_doc_count_in(populated):
    assert populated.doc_count_in("ns1") == 2
    assert populated.doc_count_in("ns2") == 1


def test_doc_count_in_empty_namespace(store):
    store.create_namespace("a", "Alpha")
    assert store.doc_count_in("a") == 0


def test_doc_count_in_unknown(store):
    assert store.doc_count_in("nope") == 0


# --------------------------------------------------------------------------- all_doc_ids


def test_all_doc_ids_sorted(populated):
    assert populated.all_doc_ids() == ["d1", "d2", "d3"]


def test_all_doc_ids_empty(store):
    assert store.all_doc_ids() == []


def test_all_doc_ids_after_remove(populated):
    populated.remove_doc("ns1", "d1")
    assert populated.all_doc_ids() == ["d2", "d3"]


# --------------------------------------------------------------------------- clear_namespace


def test_clear_namespace_returns_count(populated):
    assert populated.clear_namespace("ns1") == 2


def test_clear_namespace_empties_bucket(populated):
    populated.clear_namespace("ns1")
    assert populated.docs_in_namespace("ns1") == []


def test_clear_namespace_keeps_namespace(populated):
    populated.clear_namespace("ns1")
    assert populated.get_namespace("ns1") is not None


def test_clear_namespace_removes_doc_attachments(populated):
    populated.clear_namespace("ns1")
    assert populated.namespace_of("d1") is None
    assert populated.namespace_of("d2") is None


def test_clear_namespace_unknown_returns_zero(store):
    assert store.clear_namespace("nope") == 0


# --------------------------------------------------------------------------- stats


def test_stats_empty(store):
    s = store.stats()
    assert s.total_namespaces == 0
    assert s.total_docs == 0
    assert s.avg_docs_per_namespace == 0.0


def test_stats_with_data(populated):
    s = populated.stats()
    assert s.total_namespaces == 2
    assert s.total_docs == 3
    assert s.avg_docs_per_namespace == 1.5


def test_stats_returns_namespace_stats(store):
    assert isinstance(store.stats(), NamespaceStats)


def test_stats_after_clear(populated):
    populated.clear_namespace("ns1")
    s = populated.stats()
    assert s.total_docs == 1
    assert s.total_namespaces == 2


# --------------------------------------------------------------------------- thread safety


def test_thread_safety_add_docs():
    store = DocNamespaceStore()
    store.create_namespace("ns", "NS")

    def worker(start: int):
        for i in range(50):
            store.add_doc("ns", f"d-{start}-{i}")

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert store.doc_count_in("ns") == 50 * 8


def test_thread_safety_create_namespaces():
    store = DocNamespaceStore()
    errors: list[Exception] = []

    def worker(idx: int):
        try:
            store.create_namespace(f"ns-{idx}", f"NS{idx}")
        except Exception as exc:  # pragma: no cover - guard
            errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(32)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors
    assert len(store.list_namespaces()) == 32


def test_thread_safety_move_docs():
    store = DocNamespaceStore()
    store.create_namespace("a", "A")
    store.create_namespace("b", "B")
    for i in range(100):
        store.add_doc("a", f"d{i}")

    def mover():
        for i in range(100):
            store.move_doc(f"d{i}", "b")

    threads = [threading.Thread(target=mover) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert store.doc_count_in("a") == 0
    assert store.doc_count_in("b") == 100


def test_thread_safety_mixed_ops():
    store = DocNamespaceStore()
    store.create_namespace("ns", "NS")

    def adder():
        for i in range(100):
            store.add_doc("ns", f"d{i}")

    def reader():
        for _ in range(100):
            store.list_namespaces()
            store.stats()
            store.docs_in_namespace("ns")

    threads = [threading.Thread(target=adder) for _ in range(3)] + [
        threading.Thread(target=reader) for _ in range(3)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert store.doc_count_in("ns") == 100
