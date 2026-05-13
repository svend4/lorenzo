"""Tests for docstoolkit.doc_link_graph."""
from __future__ import annotations

import pytest

from docstoolkit.doc_link_graph import (
    DocLink,
    DocLinkGraph,
    LinkStats,
    LinkType,
)


# ---------- LinkType ----------

class TestLinkType:
    def test_all_members_present(self):
        names = {m.name for m in LinkType}
        assert {"REFERENCE", "CITATION", "EMBED", "MENTION", "FOLLOWUP"} <= names

    def test_values_are_strings(self):
        for m in LinkType:
            assert isinstance(m.value, str)

    def test_distinct_values(self):
        values = [m.value for m in LinkType]
        assert len(values) == len(set(values))

    def test_can_compare(self):
        assert LinkType.REFERENCE == LinkType.REFERENCE
        assert LinkType.CITATION != LinkType.MENTION


# ---------- DocLink ----------

class TestDocLink:
    def test_create_basic(self):
        link = DocLink(source="a", target="b", link_type=LinkType.REFERENCE)
        assert link.source == "a"
        assert link.target == "b"
        assert link.link_type == LinkType.REFERENCE
        assert link.weight == 1.0
        assert link.metadata == {}
        assert link.created_at == 0.0

    def test_weight_custom(self):
        link = DocLink(source="a", target="b", link_type=LinkType.CITATION, weight=2.5)
        assert link.weight == 2.5

    def test_metadata_independent(self):
        a = DocLink(source="a", target="b", link_type=LinkType.MENTION)
        b = DocLink(source="c", target="d", link_type=LinkType.MENTION)
        a.metadata["x"] = 1
        assert b.metadata == {}

    def test_created_at(self):
        link = DocLink(source="a", target="b", link_type=LinkType.EMBED, created_at=12.5)
        assert link.created_at == 12.5


# ---------- LinkStats ----------

class TestLinkStats:
    def test_create(self):
        stats = LinkStats(
            total_docs=3,
            total_links=2,
            most_linked_to=[("a", 1)],
            most_linking=[("b", 1)],
            orphan_count=0,
        )
        assert stats.total_docs == 3
        assert stats.total_links == 2
        assert stats.orphan_count == 0


# ---------- AddDoc ----------

class TestAddDoc:
    def test_add_one(self):
        g = DocLinkGraph()
        g.add_doc("a")
        assert "a" in g.all_docs()

    def test_add_many(self):
        g = DocLinkGraph()
        for d in ("a", "b", "c"):
            g.add_doc(d)
        assert g.doc_count == 3

    def test_add_duplicate(self):
        g = DocLinkGraph()
        g.add_doc("a")
        g.add_doc("a")
        assert g.doc_count == 1


# ---------- RemoveDoc ----------

class TestRemoveDoc:
    def test_remove_existing(self):
        g = DocLinkGraph()
        g.add_doc("a")
        assert g.remove_doc("a") is True
        assert g.doc_count == 0

    def test_remove_missing(self):
        g = DocLinkGraph()
        assert g.remove_doc("missing") is False

    def test_removes_outgoing_links(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_doc("a")
        assert g.in_degree("b") == 0
        assert g.link_count == 0

    def test_removes_incoming_links(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_doc("b")
        assert g.out_degree("a") == 0
        assert g.link_count == 0

    def test_cascades_complex(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        g.add_link("c", "b")
        g.remove_doc("b")
        assert g.link_count == 0
        assert g.doc_count == 2  # a, c remain


# ---------- AddLink ----------

class TestAddLink:
    def test_basic(self):
        g = DocLinkGraph()
        link = g.add_link("a", "b")
        assert isinstance(link, DocLink)
        assert link.source == "a"
        assert link.target == "b"
        assert link.link_type == LinkType.REFERENCE

    def test_creates_docs_implicitly(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        assert "a" in g.all_docs()
        assert "b" in g.all_docs()

    def test_custom_link_type(self):
        g = DocLinkGraph()
        link = g.add_link("a", "b", link_type=LinkType.CITATION)
        assert link.link_type == LinkType.CITATION

    def test_weight(self):
        g = DocLinkGraph()
        link = g.add_link("a", "b", weight=3.5)
        assert link.weight == 3.5

    def test_metadata(self):
        g = DocLinkGraph()
        link = g.add_link("a", "b", metadata={"k": "v"})
        assert link.metadata == {"k": "v"}

    def test_now(self):
        g = DocLinkGraph()
        link = g.add_link("a", "b", now=100.0)
        assert link.created_at == 100.0

    def test_replacing_existing(self):
        g = DocLinkGraph()
        g.add_link("a", "b", weight=1.0)
        g.add_link("a", "b", weight=5.0)
        assert g.link_count == 1
        assert g.forward_links("a")[0].weight == 5.0

    def test_metadata_default_empty(self):
        g = DocLinkGraph()
        link = g.add_link("a", "b")
        assert link.metadata == {}


# ---------- RemoveLink ----------

class TestRemoveLink:
    def test_existing(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        assert g.remove_link("a", "b") is True
        assert g.link_count == 0

    def test_missing(self):
        g = DocLinkGraph()
        g.add_doc("a")
        assert g.remove_link("a", "b") is False

    def test_unknown_source(self):
        g = DocLinkGraph()
        assert g.remove_link("nope", "b") is False

    def test_keeps_docs(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_link("a", "b")
        assert g.doc_count == 2

    def test_removes_from_backlinks(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_link("a", "b")
        assert g.backlinks("b") == []


# ---------- UpdateLink ----------

class TestUpdateLink:
    def test_weight(self):
        g = DocLinkGraph()
        g.add_link("a", "b", weight=1.0)
        assert g.update_link("a", "b", weight=2.0) is True
        assert g.forward_links("a")[0].weight == 2.0

    def test_metadata_merges(self):
        g = DocLinkGraph()
        g.add_link("a", "b", metadata={"x": 1})
        g.update_link("a", "b", metadata={"y": 2})
        link = g.forward_links("a")[0]
        assert link.metadata == {"x": 1, "y": 2}

    def test_missing(self):
        g = DocLinkGraph()
        assert g.update_link("a", "b", weight=2.0) is False

    def test_no_changes(self):
        g = DocLinkGraph()
        g.add_link("a", "b", weight=1.0)
        assert g.update_link("a", "b") is True
        assert g.forward_links("a")[0].weight == 1.0


# ---------- ForwardLinks ----------

class TestForwardLinks:
    def test_basic(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("a", "c")
        assert len(g.forward_links("a")) == 2

    def test_unknown_doc(self):
        g = DocLinkGraph()
        assert g.forward_links("nope") == []

    def test_returns_copy(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        result = g.forward_links("a")
        result.clear()
        assert len(g.forward_links("a")) == 1


# ---------- Backlinks ----------

class TestBacklinks:
    def test_basic(self):
        g = DocLinkGraph()
        g.add_link("a", "z")
        g.add_link("b", "z")
        assert len(g.backlinks("z")) == 2

    def test_unknown_doc(self):
        g = DocLinkGraph()
        assert g.backlinks("nope") == []

    def test_no_incoming(self):
        g = DocLinkGraph()
        g.add_doc("a")
        assert g.backlinks("a") == []


# ---------- LinksByType ----------

class TestLinksByType:
    def test_basic(self):
        g = DocLinkGraph()
        g.add_link("a", "b", link_type=LinkType.CITATION)
        g.add_link("a", "c", link_type=LinkType.MENTION)
        g.add_link("b", "c", link_type=LinkType.CITATION)
        cites = g.links_by_type(LinkType.CITATION)
        assert len(cites) == 2

    def test_none_of_type(self):
        g = DocLinkGraph()
        g.add_link("a", "b", link_type=LinkType.CITATION)
        assert g.links_by_type(LinkType.EMBED) == []

    def test_empty(self):
        g = DocLinkGraph()
        assert g.links_by_type(LinkType.REFERENCE) == []


# ---------- IsLinked ----------

class TestIsLinked:
    def test_true(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        assert g.is_linked("a", "b") is True

    def test_false(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        assert g.is_linked("b", "a") is False

    def test_unknown(self):
        g = DocLinkGraph()
        assert g.is_linked("x", "y") is False


# ---------- Path ----------

class TestPath:
    def test_direct(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        assert g.path("a", "b") == ["a", "b"]

    def test_two_hops(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        assert g.path("a", "c") == ["a", "b", "c"]

    def test_shortest_preferred(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        g.add_link("c", "d")
        g.add_link("a", "d")
        result = g.path("a", "d")
        assert result == ["a", "d"]

    def test_no_path(self):
        g = DocLinkGraph()
        g.add_doc("a")
        g.add_doc("b")
        assert g.path("a", "b") is None

    def test_unknown_source(self):
        g = DocLinkGraph()
        g.add_doc("b")
        assert g.path("nope", "b") is None

    def test_self(self):
        g = DocLinkGraph()
        g.add_doc("a")
        assert g.path("a", "a") == ["a"]

    def test_max_depth_blocks(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        g.add_link("c", "d")
        assert g.path("a", "d", max_depth=2) is None


# ---------- Descendants ----------

class TestDescendants:
    def test_one_hop(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("a", "c")
        assert g.descendants("a", depth=1) == {"b", "c"}

    def test_two_hops(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        assert g.descendants("a", depth=2) == {"b", "c"}

    def test_depth_limits(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        assert g.descendants("a", depth=1) == {"b"}

    def test_unknown(self):
        g = DocLinkGraph()
        assert g.descendants("nope") == set()

    def test_no_children(self):
        g = DocLinkGraph()
        g.add_doc("a")
        assert g.descendants("a") == set()


# ---------- Ancestors ----------

class TestAncestors:
    def test_one_hop(self):
        g = DocLinkGraph()
        g.add_link("a", "z")
        g.add_link("b", "z")
        assert g.ancestors("z", depth=1) == {"a", "b"}

    def test_two_hops(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        assert g.ancestors("c", depth=2) == {"a", "b"}

    def test_depth_limits(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        assert g.ancestors("c", depth=1) == {"b"}

    def test_unknown(self):
        g = DocLinkGraph()
        assert g.ancestors("nope") == set()


# ---------- Clusters ----------

class TestClusters:
    def test_one_cluster(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        clusters = g.clusters()
        assert len(clusters) == 1
        assert clusters[0] == {"a", "b", "c"}

    def test_two_clusters(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("c", "d")
        clusters = g.clusters()
        assert len(clusters) == 2

    def test_singleton(self):
        g = DocLinkGraph()
        g.add_doc("a")
        clusters = g.clusters()
        assert clusters == [{"a"}]

    def test_empty(self):
        g = DocLinkGraph()
        assert g.clusters() == []

    def test_undirected_link_grouping(self):
        # Reverse link still groups
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("c", "b")
        clusters = g.clusters()
        assert len(clusters) == 1
        assert clusters[0] == {"a", "b", "c"}


# ---------- CircularRefs ----------

class TestCircularRefs:
    def test_simple_cycle(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "a")
        cycles = g.circular_refs()
        assert len(cycles) == 1

    def test_no_cycle(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        assert g.circular_refs() == []

    def test_triangle(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        g.add_link("c", "a")
        cycles = g.circular_refs()
        assert len(cycles) >= 1
        # Cycle contains a, b, c
        cycle_nodes = set(cycles[0])
        assert {"a", "b", "c"} <= cycle_nodes

    def test_self_loop(self):
        g = DocLinkGraph()
        g.add_link("a", "a")
        cycles = g.circular_refs()
        assert len(cycles) >= 1

    def test_empty(self):
        g = DocLinkGraph()
        assert g.circular_refs() == []


# ---------- Pagerank ----------

class TestPagerank:
    def test_empty(self):
        g = DocLinkGraph()
        assert g.pagerank() == {}

    def test_sums_to_one(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        g.add_link("c", "a")
        ranks = g.pagerank()
        assert abs(sum(ranks.values()) - 1.0) < 0.01

    def test_popular_has_higher_rank(self):
        g = DocLinkGraph()
        # b gets many incoming
        g.add_link("a", "b")
        g.add_link("c", "b")
        g.add_link("d", "b")
        g.add_link("e", "b")
        ranks = g.pagerank()
        assert ranks["b"] > ranks["a"]

    def test_singleton(self):
        g = DocLinkGraph()
        g.add_doc("a")
        ranks = g.pagerank()
        assert "a" in ranks
        assert abs(ranks["a"] - 1.0) < 0.01

    def test_returns_all_docs(self):
        g = DocLinkGraph()
        for d in ("a", "b", "c"):
            g.add_doc(d)
        g.add_link("a", "b")
        ranks = g.pagerank()
        assert set(ranks) == {"a", "b", "c"}


# ---------- OutDegreeInDegree ----------

class TestOutDegreeInDegree:
    def test_out(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("a", "c")
        assert g.out_degree("a") == 2

    def test_in(self):
        g = DocLinkGraph()
        g.add_link("a", "z")
        g.add_link("b", "z")
        assert g.in_degree("z") == 2

    def test_unknown(self):
        g = DocLinkGraph()
        assert g.out_degree("nope") == 0
        assert g.in_degree("nope") == 0


# ---------- TotalDegree ----------

class TestTotalDegree:
    def test_both(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("c", "b")
        assert g.total_degree("b") == 2  # 1 in + 0 out... wait
        # b has 1 incoming from a, 1 incoming from c, 0 outgoing
        # Actually total_degree should be 2

    def test_mixed(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        assert g.total_degree("b") == 2  # 1 in (a), 1 out (c)

    def test_unknown(self):
        g = DocLinkGraph()
        assert g.total_degree("nope") == 0


# ---------- Orphans ----------

class TestOrphans:
    def test_no_orphans(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        assert g.orphans() == []

    def test_some_orphans(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_doc("z")
        assert g.orphans() == ["z"]

    def test_all_orphans(self):
        g = DocLinkGraph()
        g.add_doc("a")
        g.add_doc("b")
        assert sorted(g.orphans()) == ["a", "b"]

    def test_empty(self):
        g = DocLinkGraph()
        assert g.orphans() == []


# ---------- Stats ----------

class TestStats:
    def test_empty(self):
        g = DocLinkGraph()
        stats = g.stats()
        assert stats.total_docs == 0
        assert stats.total_links == 0
        assert stats.orphan_count == 0

    def test_basic(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("c", "b")
        stats = g.stats()
        assert stats.total_docs == 3
        assert stats.total_links == 2

    def test_most_linked_to(self):
        g = DocLinkGraph()
        g.add_link("a", "z")
        g.add_link("b", "z")
        g.add_link("c", "z")
        stats = g.stats()
        assert stats.most_linked_to[0] == ("z", 3)

    def test_most_linking(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("a", "c")
        g.add_link("a", "d")
        stats = g.stats()
        assert stats.most_linking[0] == ("a", 3)

    def test_orphan_count(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_doc("z")
        stats = g.stats()
        assert stats.orphan_count == 1

    def test_top_10_cap(self):
        g = DocLinkGraph()
        for i in range(15):
            g.add_link(f"src{i}", "target")
        stats = g.stats()
        # target is most linked, exists in top 10
        names = [n for n, _ in stats.most_linked_to]
        assert "target" in names


# ---------- AllDocs ----------

class TestAllDocs:
    def test_empty(self):
        g = DocLinkGraph()
        assert g.all_docs() == []

    def test_some(self):
        g = DocLinkGraph()
        g.add_doc("b")
        g.add_doc("a")
        assert g.all_docs() == ["a", "b"]

    def test_from_links(self):
        g = DocLinkGraph()
        g.add_link("x", "y")
        assert sorted(g.all_docs()) == ["x", "y"]


# ---------- CountProps ----------

class TestCountProps:
    def test_doc_count(self):
        g = DocLinkGraph()
        assert g.doc_count == 0
        g.add_doc("a")
        assert g.doc_count == 1

    def test_link_count(self):
        g = DocLinkGraph()
        assert g.link_count == 0
        g.add_link("a", "b")
        assert g.link_count == 1
        g.add_link("a", "c")
        assert g.link_count == 2


# ---------- Clear ----------

class TestClear:
    def test_clears_docs(self):
        g = DocLinkGraph()
        g.add_doc("a")
        g.add_link("b", "c")
        g.clear()
        assert g.doc_count == 0

    def test_clears_links(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.clear()
        assert g.link_count == 0

    def test_can_reuse_after_clear(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.clear()
        g.add_link("x", "y")
        assert g.doc_count == 2
        assert g.link_count == 1


# ---------- EdgeCases ----------

class TestEdgeCases:
    def test_self_loop_link(self):
        g = DocLinkGraph()
        g.add_link("a", "a")
        assert g.is_linked("a", "a") is True
        assert g.out_degree("a") == 1
        assert g.in_degree("a") == 1

    def test_path_with_self_loop(self):
        g = DocLinkGraph()
        g.add_link("a", "a")
        g.add_link("a", "b")
        assert g.path("a", "b") == ["a", "b"]

    def test_path_unknown_target(self):
        g = DocLinkGraph()
        g.add_doc("a")
        assert g.path("a", "unknown") is None

    def test_disconnected_no_path(self):
        g = DocLinkGraph()
        g.add_doc("a")
        g.add_doc("b")
        assert g.path("a", "b") is None

    def test_descendants_with_cycle(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "a")
        descs = g.descendants("a", depth=5)
        assert "b" in descs

    def test_pagerank_dangling(self):
        g = DocLinkGraph()
        # b is a dangling node (no outgoing)
        g.add_link("a", "b")
        ranks = g.pagerank()
        assert abs(sum(ranks.values()) - 1.0) < 0.05

    def test_remove_doc_with_self_loop(self):
        g = DocLinkGraph()
        g.add_link("a", "a")
        g.remove_doc("a")
        assert g.doc_count == 0
        assert g.link_count == 0

    def test_multiple_link_types_same_pair(self):
        g = DocLinkGraph()
        g.add_link("a", "b", link_type=LinkType.CITATION)
        # adding another with different type replaces
        g.add_link("a", "b", link_type=LinkType.MENTION)
        assert g.link_count == 1
        assert g.forward_links("a")[0].link_type == LinkType.MENTION
