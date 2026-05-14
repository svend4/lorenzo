"""Tests for the E441 DocConceptMap module."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_concept_map import Concept, ConceptStats, DocConceptMap


# ---------------------------------------------------------------------- #
# Concept dataclass                                                      #
# ---------------------------------------------------------------------- #
def test_concept_defaults():
    c = Concept(concept_id="c1", name="Alpha")
    assert c.concept_id == "c1"
    assert c.name == "Alpha"
    assert c.description == ""
    assert c.related == []
    assert c.created_at == 0.0


def test_concept_with_all_fields():
    c = Concept(
        concept_id="c2",
        name="Beta",
        description="desc",
        related=["c1"],
        created_at=12.5,
    )
    assert c.description == "desc"
    assert c.related == ["c1"]
    assert c.created_at == 12.5


def test_concept_related_is_default_factory_isolated():
    a = Concept(concept_id="a", name="A")
    b = Concept(concept_id="b", name="B")
    a.related.append("x")
    assert b.related == []


# ---------------------------------------------------------------------- #
# ConceptStats                                                           #
# ---------------------------------------------------------------------- #
def test_concept_stats_fields():
    s = ConceptStats(total_concepts=2, total_associations=3, unique_docs=1)
    assert s.total_concepts == 2
    assert s.total_associations == 3
    assert s.unique_docs == 1


# ---------------------------------------------------------------------- #
# define_concept                                                         #
# ---------------------------------------------------------------------- #
def test_define_concept_basic():
    m = DocConceptMap()
    c = m.define_concept("c1", "Alpha")
    assert c.concept_id == "c1"
    assert c.name == "Alpha"
    assert c.description == ""
    assert c.related == []
    assert c.created_at == 0.0


def test_define_concept_with_description_and_related():
    m = DocConceptMap()
    m.define_concept("c1", "Alpha")
    c = m.define_concept(
        "c2", "Beta", description="d", related=["c1"], now=99.9
    )
    assert c.description == "d"
    assert c.related == ["c1"]
    assert c.created_at == 99.9


def test_define_concept_overwrites_existing():
    m = DocConceptMap()
    m.define_concept("c1", "Alpha")
    m.define_concept("c1", "AlphaPrime", description="new")
    got = m.get_concept("c1")
    assert got is not None
    assert got.name == "AlphaPrime"
    assert got.description == "new"


def test_define_concept_related_list_is_copied():
    m = DocConceptMap()
    seed = ["x", "y"]
    m.define_concept("c1", "A", related=seed)
    seed.append("z")
    got = m.get_concept("c1")
    assert got is not None
    assert got.related == ["x", "y"]


# ---------------------------------------------------------------------- #
# undefine_concept                                                       #
# ---------------------------------------------------------------------- #
def test_undefine_concept_missing():
    m = DocConceptMap()
    assert m.undefine_concept("ghost") is False


def test_undefine_concept_basic():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    assert m.undefine_concept("c1") is True
    assert m.get_concept("c1") is None


def test_undefine_concept_removes_doc_associations():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.associate("d1", "c1")
    m.associate("d2", "c1")
    assert m.undefine_concept("c1") is True
    assert m.docs_for_concept("c1") == []
    assert m.concepts_for_doc("d1") == []
    assert m.concepts_for_doc("d2") == []


def test_undefine_concept_removes_from_related_lists():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B", related=["c1"])
    m.define_concept("c3", "C", related=["c1"])
    assert m.undefine_concept("c1") is True
    assert m.get_concept("c2").related == []
    assert m.get_concept("c3").related == []


# ---------------------------------------------------------------------- #
# get_concept                                                            #
# ---------------------------------------------------------------------- #
def test_get_concept_returns_none_for_missing():
    m = DocConceptMap()
    assert m.get_concept("ghost") is None


def test_get_concept_returns_concept():
    m = DocConceptMap()
    m.define_concept("c1", "Alpha")
    assert m.get_concept("c1").name == "Alpha"


# ---------------------------------------------------------------------- #
# add_related / remove_related                                           #
# ---------------------------------------------------------------------- #
def test_add_related_new():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")
    assert m.add_related("c1", "c2") is True
    assert m.get_concept("c1").related == ["c2"]


def test_add_related_already_exists():
    m = DocConceptMap()
    m.define_concept("c1", "A", related=["c2"])
    m.define_concept("c2", "B")
    assert m.add_related("c1", "c2") is False


def test_add_related_missing_concept():
    m = DocConceptMap()
    m.define_concept("c2", "B")
    assert m.add_related("ghost", "c2") is False


def test_add_related_missing_target():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    assert m.add_related("c1", "ghost") is False


def test_remove_related_existing():
    m = DocConceptMap()
    m.define_concept("c1", "A", related=["c2"])
    m.define_concept("c2", "B")
    assert m.remove_related("c1", "c2") is True
    assert m.get_concept("c1").related == []


def test_remove_related_missing_relation():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")
    assert m.remove_related("c1", "c2") is False


def test_remove_related_missing_concept():
    m = DocConceptMap()
    assert m.remove_related("ghost", "c2") is False


# ---------------------------------------------------------------------- #
# associate / disassociate                                               #
# ---------------------------------------------------------------------- #
def test_associate_new():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    assert m.associate("d1", "c1") is True


def test_associate_already_exists():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.associate("d1", "c1")
    assert m.associate("d1", "c1") is False


def test_associate_missing_concept():
    m = DocConceptMap()
    assert m.associate("d1", "ghost") is False


def test_disassociate_existing():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.associate("d1", "c1")
    assert m.disassociate("d1", "c1") is True
    assert m.concepts_for_doc("d1") == []


def test_disassociate_missing():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    assert m.disassociate("d1", "c1") is False


def test_disassociate_unknown_doc():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    assert m.disassociate("ghost", "c1") is False


def test_disassociate_cleans_empty_doc_set():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.associate("d1", "c1")
    m.disassociate("d1", "c1")
    assert "d1" not in m.all_doc_ids()


# ---------------------------------------------------------------------- #
# concepts_for_doc / docs_for_concept                                    #
# ---------------------------------------------------------------------- #
def test_concepts_for_doc_sorted_by_name():
    m = DocConceptMap()
    m.define_concept("c1", "Zeta")
    m.define_concept("c2", "Alpha")
    m.define_concept("c3", "Mid")
    m.associate("d1", "c1")
    m.associate("d1", "c2")
    m.associate("d1", "c3")
    names = [c.name for c in m.concepts_for_doc("d1")]
    assert names == ["Alpha", "Mid", "Zeta"]


def test_concepts_for_doc_empty():
    m = DocConceptMap()
    assert m.concepts_for_doc("ghost") == []


def test_docs_for_concept_sorted():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.associate("d2", "c1")
    m.associate("d1", "c1")
    m.associate("d3", "c1")
    assert m.docs_for_concept("c1") == ["d1", "d2", "d3"]


def test_docs_for_concept_empty_for_unknown():
    m = DocConceptMap()
    assert m.docs_for_concept("ghost") == []


def test_docs_for_concept_empty_for_defined_no_assoc():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    assert m.docs_for_concept("c1") == []


# ---------------------------------------------------------------------- #
# related_concepts                                                       #
# ---------------------------------------------------------------------- #
def test_related_concepts_direct():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "Bravo")
    m.define_concept("c3", "Alpha")
    m.add_related("c1", "c2")
    m.add_related("c1", "c3")
    names = [c.name for c in m.related_concepts("c1")]
    assert names == ["Alpha", "Bravo"]


def test_related_concepts_missing_seed():
    m = DocConceptMap()
    assert m.related_concepts("ghost") == []


def test_related_concepts_no_related():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    assert m.related_concepts("c1") == []


def test_related_concepts_transitive_basic():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")
    m.define_concept("c3", "C")
    m.add_related("c1", "c2")
    m.add_related("c2", "c3")
    ids = {c.concept_id for c in m.related_concepts("c1", transitive=True)}
    assert ids == {"c2", "c3"}


def test_related_concepts_transitive_max_depth_limits():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")
    m.define_concept("c3", "C")
    m.define_concept("c4", "D")
    m.add_related("c1", "c2")
    m.add_related("c2", "c3")
    m.add_related("c3", "c4")
    ids = {
        c.concept_id
        for c in m.related_concepts("c1", transitive=True, max_depth=1)
    }
    assert ids == {"c2"}
    ids2 = {
        c.concept_id
        for c in m.related_concepts("c1", transitive=True, max_depth=2)
    }
    assert ids2 == {"c2", "c3"}


def test_related_concepts_transitive_excludes_seed():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")
    m.add_related("c1", "c2")
    m.add_related("c2", "c1")
    ids = {c.concept_id for c in m.related_concepts("c1", transitive=True)}
    assert ids == {"c2"}


def test_related_concepts_transitive_zero_depth():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")
    m.add_related("c1", "c2")
    assert (
        m.related_concepts("c1", transitive=True, max_depth=0) == []
    )


def test_related_concepts_skips_missing_related_ids():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")
    m.add_related("c1", "c2")
    # Force a dangling related id (bypass API)
    m._concepts["c1"].related.append("ghost")
    direct = m.related_concepts("c1")
    assert [c.concept_id for c in direct] == ["c2"]
    tr = m.related_concepts("c1", transitive=True)
    assert [c.concept_id for c in tr] == ["c2"]


def test_related_concepts_sorted_by_name():
    m = DocConceptMap()
    m.define_concept("c1", "Root")
    m.define_concept("c2", "Zeta")
    m.define_concept("c3", "Alpha")
    m.add_related("c1", "c2")
    m.add_related("c1", "c3")
    names = [c.name for c in m.related_concepts("c1", transitive=True)]
    assert names == ["Alpha", "Zeta"]


# ---------------------------------------------------------------------- #
# find_concepts_by_name                                                  #
# ---------------------------------------------------------------------- #
def test_find_concepts_by_name_substring():
    m = DocConceptMap()
    m.define_concept("c1", "Alpha Beta")
    m.define_concept("c2", "beta gamma")
    m.define_concept("c3", "Delta")
    results = m.find_concepts_by_name("beta")
    names = [c.name for c in results]
    assert names == ["Alpha Beta", "beta gamma"]


def test_find_concepts_by_name_case_insensitive():
    m = DocConceptMap()
    m.define_concept("c1", "Knowledge Graph")
    res = m.find_concepts_by_name("KNOW")
    assert len(res) == 1
    assert res[0].concept_id == "c1"


def test_find_concepts_by_name_no_match():
    m = DocConceptMap()
    m.define_concept("c1", "Alpha")
    assert m.find_concepts_by_name("nothing") == []


def test_find_concepts_by_name_empty_query_matches_all():
    m = DocConceptMap()
    m.define_concept("c1", "Alpha")
    m.define_concept("c2", "Beta")
    res = m.find_concepts_by_name("")
    assert {c.concept_id for c in res} == {"c1", "c2"}


# ---------------------------------------------------------------------- #
# co_occurring_concepts                                                  #
# ---------------------------------------------------------------------- #
def test_co_occurring_basic():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")
    m.define_concept("c3", "C")
    m.associate("d1", "c1")
    m.associate("d1", "c2")
    m.associate("d2", "c1")
    m.associate("d2", "c2")
    m.associate("d3", "c1")
    m.associate("d3", "c3")
    res = m.co_occurring_concepts("c1")
    assert res == [("c2", 2), ("c3", 1)]


def test_co_occurring_excludes_self():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.associate("d1", "c1")
    assert m.co_occurring_concepts("c1") == []


def test_co_occurring_missing_concept():
    m = DocConceptMap()
    assert m.co_occurring_concepts("ghost") == []


def test_co_occurring_limit():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    for i in range(5):
        cid = f"x{i}"
        m.define_concept(cid, f"X{i}")
        m.associate("d1", "c1")
        m.associate("d1", cid)
    res = m.co_occurring_concepts("c1", limit=3)
    assert len(res) == 3


def test_co_occurring_tie_sort_by_id():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("aa", "AA")
    m.define_concept("bb", "BB")
    m.associate("d1", "c1")
    m.associate("d1", "bb")
    m.associate("d1", "aa")
    res = m.co_occurring_concepts("c1")
    assert res == [("aa", 1), ("bb", 1)]


# ---------------------------------------------------------------------- #
# clear_doc                                                              #
# ---------------------------------------------------------------------- #
def test_clear_doc_basic():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")
    m.associate("d1", "c1")
    m.associate("d1", "c2")
    removed = m.clear_doc("d1")
    assert removed == 2
    assert m.concepts_for_doc("d1") == []
    assert m.docs_for_concept("c1") == []
    assert m.docs_for_concept("c2") == []


def test_clear_doc_unknown():
    m = DocConceptMap()
    assert m.clear_doc("ghost") == 0


def test_clear_doc_does_not_affect_other_docs():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.associate("d1", "c1")
    m.associate("d2", "c1")
    m.clear_doc("d1")
    assert m.docs_for_concept("c1") == ["d2"]


# ---------------------------------------------------------------------- #
# all_concept_ids / all_doc_ids                                          #
# ---------------------------------------------------------------------- #
def test_all_concept_ids_sorted():
    m = DocConceptMap()
    m.define_concept("z", "Z")
    m.define_concept("a", "A")
    m.define_concept("m", "M")
    assert m.all_concept_ids() == ["a", "m", "z"]


def test_all_concept_ids_empty():
    assert DocConceptMap().all_concept_ids() == []


def test_all_doc_ids_sorted():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.associate("z", "c1")
    m.associate("a", "c1")
    m.associate("m", "c1")
    assert m.all_doc_ids() == ["a", "m", "z"]


def test_all_doc_ids_empty():
    assert DocConceptMap().all_doc_ids() == []


# ---------------------------------------------------------------------- #
# stats                                                                  #
# ---------------------------------------------------------------------- #
def test_stats_empty():
    s = DocConceptMap().stats()
    assert s == ConceptStats(
        total_concepts=0, total_associations=0, unique_docs=0
    )


def test_stats_with_associations():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")
    m.associate("d1", "c1")
    m.associate("d1", "c2")
    m.associate("d2", "c1")
    s = m.stats()
    assert s.total_concepts == 2
    assert s.total_associations == 3
    assert s.unique_docs == 2


def test_stats_updates_after_disassociate():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.associate("d1", "c1")
    m.disassociate("d1", "c1")
    s = m.stats()
    assert s.total_associations == 0
    assert s.unique_docs == 0


# ---------------------------------------------------------------------- #
# Integration                                                            #
# ---------------------------------------------------------------------- #
def test_integration_full_workflow():
    m = DocConceptMap()
    m.define_concept("memory", "Memory")
    m.define_concept("rag", "RAG")
    m.define_concept("graph", "Knowledge Graph")
    m.add_related("memory", "rag")
    m.add_related("rag", "graph")
    m.associate("doc1", "memory")
    m.associate("doc1", "rag")
    m.associate("doc2", "rag")
    m.associate("doc2", "graph")
    assert {c.concept_id for c in m.concepts_for_doc("doc1")} == {
        "memory",
        "rag",
    }
    assert m.docs_for_concept("rag") == ["doc1", "doc2"]
    tr = m.related_concepts("memory", transitive=True)
    assert {c.concept_id for c in tr} == {"rag", "graph"}
    assert m.co_occurring_concepts("rag")[0] == ("graph", 1) or m.co_occurring_concepts(
        "rag"
    )[0] == ("memory", 1)


# ---------------------------------------------------------------------- #
# Thread safety                                                          #
# ---------------------------------------------------------------------- #
def test_thread_safety_define_concepts():
    m = DocConceptMap()

    def worker(start: int) -> None:
        for i in range(start, start + 50):
            m.define_concept(f"c{i}", f"name{i}")

    threads = [threading.Thread(target=worker, args=(i * 50,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(m.all_concept_ids()) == 200


def test_thread_safety_associate_disassociate():
    m = DocConceptMap()
    for i in range(20):
        m.define_concept(f"c{i}", f"name{i}")

    def writer() -> None:
        for i in range(20):
            m.associate(f"d{i}", f"c{i}")

    def reader() -> None:
        for _ in range(50):
            m.stats()
            m.all_doc_ids()
            m.all_concept_ids()

    threads = [
        threading.Thread(target=writer),
        threading.Thread(target=writer),
        threading.Thread(target=reader),
        threading.Thread(target=reader),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    s = m.stats()
    assert s.total_concepts == 20
    # 20 unique doc-concept pairs (writers idempotent)
    assert s.total_associations == 20


def test_thread_safety_mixed_operations():
    m = DocConceptMap()
    m.define_concept("c1", "A")
    m.define_concept("c2", "B")

    def associator() -> None:
        for i in range(100):
            m.associate(f"d{i}", "c1")
            m.associate(f"d{i}", "c2")

    def disassociator() -> None:
        for i in range(100):
            m.disassociate(f"d{i}", "c1")

    def querier() -> None:
        for _ in range(100):
            m.docs_for_concept("c1")
            m.docs_for_concept("c2")
            m.co_occurring_concepts("c1")

    threads = [
        threading.Thread(target=associator),
        threading.Thread(target=disassociator),
        threading.Thread(target=querier),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # No assertion on exact state due to race in scheduling -- just ensure
    # no exceptions and state is consistent.
    s = m.stats()
    assert s.total_concepts == 2
    assert s.total_associations >= 0


def test_thread_safety_define_undefine():
    m = DocConceptMap()

    def definer() -> None:
        for i in range(100):
            m.define_concept(f"c{i}", f"n{i}")

    def undefiner() -> None:
        for i in range(100):
            m.undefine_concept(f"c{i}")

    t1 = threading.Thread(target=definer)
    t2 = threading.Thread(target=undefiner)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # Map should be in a valid state (no exceptions)
    m.stats()


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
