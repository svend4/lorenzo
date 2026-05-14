"""Tests for E355 doc_relation_graph."""
from __future__ import annotations

import threading
import uuid

import pytest

from docstoolkit.doc_relation_graph import (
    DocRelationGraph,
    Relation,
    RelationStats,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestRelationDataclass:
    def test_basic_fields(self):
        rel = Relation(
            relation_id="r1",
            from_doc="a",
            to_doc="b",
            relation_type="references",
        )
        assert rel.relation_id == "r1"
        assert rel.from_doc == "a"
        assert rel.to_doc == "b"
        assert rel.relation_type == "references"

    def test_default_weight(self):
        rel = Relation("r1", "a", "b", "t")
        assert rel.weight == 1.0

    def test_custom_weight(self):
        rel = Relation("r1", "a", "b", "t", weight=2.5)
        assert rel.weight == 2.5

    def test_default_created_at(self):
        rel = Relation("r1", "a", "b", "t")
        assert rel.created_at == 0.0

    def test_default_metadata_is_dict(self):
        rel = Relation("r1", "a", "b", "t")
        assert rel.metadata == {}

    def test_metadata_independent_instances(self):
        r1 = Relation("r1", "a", "b", "t")
        r2 = Relation("r2", "c", "d", "t")
        r1.metadata["k"] = "v"
        assert r2.metadata == {}


class TestRelationStatsDataclass:
    def test_basic_fields(self):
        s = RelationStats(
            total_relations=3,
            unique_docs=2,
            unique_types=1,
            type_counts={"references": 3},
        )
        assert s.total_relations == 3
        assert s.unique_docs == 2
        assert s.unique_types == 1
        assert s.type_counts == {"references": 3}

    def test_default_type_counts(self):
        s = RelationStats(total_relations=0, unique_docs=0, unique_types=0)
        assert s.type_counts == {}


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_graph(self):
        g = DocRelationGraph()
        assert g.stats().total_relations == 0

    def test_no_relation_types(self):
        g = DocRelationGraph()
        assert g.all_relation_types() == []

    def test_no_top_referenced(self):
        g = DocRelationGraph()
        assert g.top_referenced_docs() == []

    def test_two_independent_graphs(self):
        g1 = DocRelationGraph()
        g2 = DocRelationGraph()
        g1.add_relation("a", "b", "references")
        assert g1.stats().total_relations == 1
        assert g2.stats().total_relations == 0


# ---------------------------------------------------------------------------
# add_relation
# ---------------------------------------------------------------------------


class TestAddRelation:
    def test_returns_relation_instance(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "references")
        assert isinstance(rel, Relation)

    def test_assigns_uuid(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "references")
        # Must be a valid UUID
        uuid.UUID(rel.relation_id)

    def test_unique_uuids(self):
        g = DocRelationGraph()
        ids = {g.add_relation("a", "b", "t").relation_id for _ in range(50)}
        assert len(ids) == 50

    def test_fields_set_correctly(self):
        g = DocRelationGraph()
        rel = g.add_relation(
            "a",
            "b",
            "supersedes",
            weight=2.0,
            metadata={"k": "v"},
            now=1234.5,
        )
        assert rel.from_doc == "a"
        assert rel.to_doc == "b"
        assert rel.relation_type == "supersedes"
        assert rel.weight == 2.0
        assert rel.metadata == {"k": "v"}
        assert rel.created_at == 1234.5

    def test_default_weight(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        assert rel.weight == 1.0

    def test_default_created_at(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        assert rel.created_at == 0.0

    def test_metadata_copied(self):
        g = DocRelationGraph()
        meta = {"k": "v"}
        rel = g.add_relation("a", "b", "t", metadata=meta)
        meta["k"] = "changed"
        assert rel.metadata == {"k": "v"}

    def test_metadata_none_yields_empty_dict(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        assert rel.metadata == {}

    def test_stats_after_add(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "t")
        assert g.stats().total_relations == 1


# ---------------------------------------------------------------------------
# remove_relation
# ---------------------------------------------------------------------------


class TestRemoveRelation:
    def test_returns_true_when_existed(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        assert g.remove_relation(rel.relation_id) is True

    def test_returns_false_when_missing(self):
        g = DocRelationGraph()
        assert g.remove_relation("nope") is False

    def test_removed_from_get(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        g.remove_relation(rel.relation_id)
        assert g.get_relation(rel.relation_id) is None

    def test_removed_from_outgoing(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        g.remove_relation(rel.relation_id)
        assert g.outgoing("a") == []

    def test_removed_from_incoming(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        g.remove_relation(rel.relation_id)
        assert g.incoming("b") == []

    def test_removed_from_type_index(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        g.remove_relation(rel.relation_id)
        assert g.relations_of_type("t") == []
        assert "t" not in g.all_relation_types()


# ---------------------------------------------------------------------------
# get_relation
# ---------------------------------------------------------------------------


class TestGetRelation:
    def test_found(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        got = g.get_relation(rel.relation_id)
        assert got is rel or (got is not None and got.relation_id == rel.relation_id)

    def test_not_found(self):
        g = DocRelationGraph()
        assert g.get_relation("nope") is None

    def test_returns_relation_type(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        assert isinstance(g.get_relation(rel.relation_id), Relation)


# ---------------------------------------------------------------------------
# outgoing
# ---------------------------------------------------------------------------


class TestOutgoing:
    def test_empty(self):
        g = DocRelationGraph()
        assert g.outgoing("a") == []

    def test_single(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t", now=1.0)
        out = g.outgoing("a")
        assert len(out) == 1
        assert out[0].relation_id == rel.relation_id

    def test_sorted_by_created_at(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "t", now=3.0)
        g.add_relation("a", "c", "t", now=1.0)
        g.add_relation("a", "d", "t", now=2.0)
        out = g.outgoing("a")
        assert [r.to_doc for r in out] == ["c", "d", "b"]

    def test_filter_by_type(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "references", now=1.0)
        g.add_relation("a", "c", "supersedes", now=2.0)
        g.add_relation("a", "d", "references", now=3.0)
        out = g.outgoing("a", relation_type="references")
        assert [r.to_doc for r in out] == ["b", "d"]

    def test_filter_by_type_empty(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "references")
        assert g.outgoing("a", relation_type="depends_on") == []

    def test_only_outgoing(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "t")
        g.add_relation("b", "a", "t")
        out = g.outgoing("a")
        assert len(out) == 1
        assert out[0].to_doc == "b"


# ---------------------------------------------------------------------------
# incoming
# ---------------------------------------------------------------------------


class TestIncoming:
    def test_empty(self):
        g = DocRelationGraph()
        assert g.incoming("a") == []

    def test_single(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t", now=1.0)
        inc = g.incoming("b")
        assert len(inc) == 1
        assert inc[0].relation_id == rel.relation_id

    def test_sorted_by_created_at(self):
        g = DocRelationGraph()
        g.add_relation("a", "z", "t", now=3.0)
        g.add_relation("b", "z", "t", now=1.0)
        g.add_relation("c", "z", "t", now=2.0)
        inc = g.incoming("z")
        assert [r.from_doc for r in inc] == ["b", "c", "a"]

    def test_filter_by_type(self):
        g = DocRelationGraph()
        g.add_relation("a", "z", "references", now=1.0)
        g.add_relation("b", "z", "supersedes", now=2.0)
        g.add_relation("c", "z", "references", now=3.0)
        inc = g.incoming("z", relation_type="references")
        assert [r.from_doc for r in inc] == ["a", "c"]

    def test_filter_by_type_empty(self):
        g = DocRelationGraph()
        g.add_relation("a", "z", "references")
        assert g.incoming("z", relation_type="depends_on") == []


# ---------------------------------------------------------------------------
# between
# ---------------------------------------------------------------------------


class TestBetween:
    def test_empty(self):
        g = DocRelationGraph()
        assert g.between("a", "b") == []

    def test_single(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t", now=1.0)
        result = g.between("a", "b")
        assert len(result) == 1
        assert result[0].relation_id == rel.relation_id

    def test_multiple_sorted(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "references", now=3.0)
        g.add_relation("a", "b", "depends_on", now=1.0)
        g.add_relation("a", "b", "supersedes", now=2.0)
        result = g.between("a", "b")
        assert [r.relation_type for r in result] == [
            "depends_on",
            "supersedes",
            "references",
        ]

    def test_excludes_reverse(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "t")
        g.add_relation("b", "a", "t")
        result = g.between("a", "b")
        assert len(result) == 1
        assert result[0].from_doc == "a"


# ---------------------------------------------------------------------------
# relations_of_type
# ---------------------------------------------------------------------------


class TestRelationsOfType:
    def test_empty(self):
        g = DocRelationGraph()
        assert g.relations_of_type("references") == []

    def test_single_type(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "references", now=2.0)
        g.add_relation("c", "d", "references", now=1.0)
        g.add_relation("a", "c", "supersedes", now=3.0)
        result = g.relations_of_type("references")
        assert len(result) == 2
        assert [r.created_at for r in result] == [1.0, 2.0]

    def test_unknown_type(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "references")
        assert g.relations_of_type("nope") == []


# ---------------------------------------------------------------------------
# related_docs
# ---------------------------------------------------------------------------


class TestRelatedDocs:
    def test_empty(self):
        g = DocRelationGraph()
        assert g.related_docs("a") == []

    def test_out_only(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "t")
        g.add_relation("a", "c", "t")
        g.add_relation("d", "a", "t")
        assert g.related_docs("a", direction="out") == ["b", "c"]

    def test_in_only(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "t")
        g.add_relation("c", "a", "t")
        g.add_relation("d", "a", "t")
        assert g.related_docs("a", direction="in") == ["c", "d"]

    def test_both(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "t")
        g.add_relation("c", "a", "t")
        assert g.related_docs("a", direction="both") == ["b", "c"]

    def test_default_is_both(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "t")
        g.add_relation("c", "a", "t")
        assert g.related_docs("a") == ["b", "c"]

    def test_dedup(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "references")
        g.add_relation("a", "b", "supersedes")
        g.add_relation("b", "a", "depends_on")
        assert g.related_docs("a", direction="both") == ["b"]

    def test_sorted(self):
        g = DocRelationGraph()
        g.add_relation("a", "z", "t")
        g.add_relation("a", "m", "t")
        g.add_relation("a", "b", "t")
        assert g.related_docs("a", direction="out") == ["b", "m", "z"]

    def test_invalid_direction(self):
        g = DocRelationGraph()
        with pytest.raises(ValueError):
            g.related_docs("a", direction="weird")

    def test_excludes_self_when_self_loop(self):
        g = DocRelationGraph()
        g.add_relation("a", "a", "t")
        g.add_relation("a", "b", "t")
        # "a" pointing to itself should not appear in related docs
        assert "a" not in g.related_docs("a", direction="both")


# ---------------------------------------------------------------------------
# all_relation_types
# ---------------------------------------------------------------------------


class TestAllRelationTypes:
    def test_empty(self):
        g = DocRelationGraph()
        assert g.all_relation_types() == []

    def test_sorted_unique(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "supersedes")
        g.add_relation("a", "c", "references")
        g.add_relation("a", "d", "references")
        g.add_relation("a", "e", "depends_on")
        assert g.all_relation_types() == [
            "depends_on",
            "references",
            "supersedes",
        ]

    def test_removed_type_disappears(self):
        g = DocRelationGraph()
        r = g.add_relation("a", "b", "references")
        g.add_relation("a", "c", "depends_on")
        g.remove_relation(r.relation_id)
        assert g.all_relation_types() == ["depends_on"]


# ---------------------------------------------------------------------------
# update_weight
# ---------------------------------------------------------------------------


class TestUpdateWeight:
    def test_true_when_found(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t")
        assert g.update_weight(rel.relation_id, 3.5) is True

    def test_false_when_missing(self):
        g = DocRelationGraph()
        assert g.update_weight("nope", 3.5) is False

    def test_weight_actually_updated(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t", weight=1.0)
        g.update_weight(rel.relation_id, 9.0)
        assert g.get_relation(rel.relation_id).weight == 9.0

    def test_zero_weight(self):
        g = DocRelationGraph()
        rel = g.add_relation("a", "b", "t", weight=1.0)
        g.update_weight(rel.relation_id, 0.0)
        assert g.get_relation(rel.relation_id).weight == 0.0


# ---------------------------------------------------------------------------
# top_referenced_docs
# ---------------------------------------------------------------------------


class TestTopReferencedDocs:
    def test_empty(self):
        g = DocRelationGraph()
        assert g.top_referenced_docs() == []

    def test_sorted_by_count_desc(self):
        g = DocRelationGraph()
        g.add_relation("a", "z", "t")
        g.add_relation("b", "z", "t")
        g.add_relation("c", "z", "t")
        g.add_relation("a", "y", "t")
        result = g.top_referenced_docs()
        assert result[0] == ("z", 3)
        assert ("y", 1) in result

    def test_tiebreak_by_doc_id_asc(self):
        g = DocRelationGraph()
        g.add_relation("a", "z", "t")
        g.add_relation("b", "y", "t")
        g.add_relation("c", "x", "t")
        # Counts all 1 — sorted by doc_id ascending
        result = g.top_referenced_docs()
        assert result == [("x", 1), ("y", 1), ("z", 1)]

    def test_limit(self):
        g = DocRelationGraph()
        for src in ("a", "b", "c"):
            g.add_relation(src, "z", "t")
        g.add_relation("a", "y", "t")
        g.add_relation("a", "x", "t")
        result = g.top_referenced_docs(limit=2)
        assert len(result) == 2
        assert result[0] == ("z", 3)

    def test_limit_zero_returns_all(self):
        g = DocRelationGraph()
        g.add_relation("a", "z", "t")
        g.add_relation("a", "y", "t")
        result = g.top_referenced_docs(limit=0)
        assert len(result) == 2

    def test_only_docs_with_incoming(self):
        g = DocRelationGraph()
        g.add_relation("a", "z", "t")
        # "a" has no incoming — should not appear
        targets = [doc for doc, _ in g.top_referenced_docs()]
        assert "a" not in targets
        assert "z" in targets


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        g = DocRelationGraph()
        s = g.stats()
        assert s.total_relations == 0
        assert s.unique_docs == 0
        assert s.unique_types == 0
        assert s.type_counts == {}

    def test_totals(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "references")
        g.add_relation("a", "c", "references")
        g.add_relation("b", "c", "supersedes")
        s = g.stats()
        assert s.total_relations == 3
        # unique docs: a, b, c
        assert s.unique_docs == 3
        assert s.unique_types == 2

    def test_type_counts(self):
        g = DocRelationGraph()
        g.add_relation("a", "b", "references")
        g.add_relation("a", "c", "references")
        g.add_relation("b", "c", "supersedes")
        s = g.stats()
        assert s.type_counts == {"references": 2, "supersedes": 1}

    def test_stats_after_remove(self):
        g = DocRelationGraph()
        r = g.add_relation("a", "b", "references")
        g.add_relation("a", "c", "supersedes")
        g.remove_relation(r.relation_id)
        s = g.stats()
        assert s.total_relations == 1
        assert s.type_counts == {"supersedes": 1}
        assert s.unique_types == 1


# ---------------------------------------------------------------------------
# Thread-safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_add_relation(self):
        g = DocRelationGraph()
        threads = []
        per_thread = 50
        num_threads = 8

        def worker(idx: int):
            for j in range(per_thread):
                g.add_relation(f"doc-{idx}", f"target-{j}", "references")

        for i in range(num_threads):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        s = g.stats()
        assert s.total_relations == per_thread * num_threads
        assert s.type_counts == {"references": per_thread * num_threads}

    def test_concurrent_unique_uuids(self):
        g = DocRelationGraph()
        results: list = []
        lock = threading.Lock()

        def worker():
            for _ in range(25):
                rel = g.add_relation("a", "b", "t")
                with lock:
                    results.append(rel.relation_id)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 100
        assert len(set(results)) == 100

    def test_concurrent_add_and_remove(self):
        g = DocRelationGraph()
        added_ids: list = []
        lock = threading.Lock()

        def adder():
            for _ in range(50):
                rel = g.add_relation("a", "b", "t")
                with lock:
                    added_ids.append(rel.relation_id)

        threads = [threading.Thread(target=adder) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(added_ids) == 200
        # Now remove half concurrently
        to_remove = added_ids[:100]

        def remover(chunk):
            for rid in chunk:
                g.remove_relation(rid)

        threads = []
        for i in range(4):
            chunk = to_remove[i * 25:(i + 1) * 25]
            t = threading.Thread(target=remover, args=(chunk,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        assert g.stats().total_relations == 100
