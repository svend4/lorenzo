"""Tests for E315 docstoolkit.doc_link_graph."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_link_graph import DocLink, DocLinkGraph, LinkGraphStats


# ---------------------------------------------------------------------------
# DocLink dataclass
# ---------------------------------------------------------------------------

class TestDocLinkDataclass:
    def test_required_fields(self):
        lnk = DocLink(from_doc="a", to_doc="b")
        assert lnk.from_doc == "a"
        assert lnk.to_doc == "b"

    def test_defaults(self):
        lnk = DocLink(from_doc="a", to_doc="b")
        assert lnk.anchor == ""
        assert lnk.link_type == "internal"
        assert lnk.added_at == 0.0

    def test_custom_anchor(self):
        lnk = DocLink(from_doc="a", to_doc="b", anchor="click here")
        assert lnk.anchor == "click here"

    def test_custom_link_type(self):
        lnk = DocLink(from_doc="a", to_doc="b", link_type="external")
        assert lnk.link_type == "external"

    def test_citation_link_type(self):
        lnk = DocLink(from_doc="a", to_doc="b", link_type="citation")
        assert lnk.link_type == "citation"

    def test_custom_added_at(self):
        lnk = DocLink(from_doc="a", to_doc="b", added_at=999.9)
        assert lnk.added_at == 999.9

    def test_all_fields(self):
        lnk = DocLink(from_doc="x", to_doc="y", anchor="ref", link_type="citation", added_at=1.0)
        assert lnk.from_doc == "x"
        assert lnk.to_doc == "y"
        assert lnk.anchor == "ref"
        assert lnk.link_type == "citation"
        assert lnk.added_at == 1.0

    def test_mutable_fields(self):
        lnk = DocLink(from_doc="a", to_doc="b")
        lnk.anchor = "new"
        assert lnk.anchor == "new"


# ---------------------------------------------------------------------------
# LinkGraphStats dataclass
# ---------------------------------------------------------------------------

class TestLinkGraphStatsDataclass:
    def test_all_fields(self):
        s = LinkGraphStats(total_links=5, unique_sources=3, unique_targets=4, orphan_count=1)
        assert s.total_links == 5
        assert s.unique_sources == 3
        assert s.unique_targets == 4
        assert s.orphan_count == 1

    def test_zero_values(self):
        s = LinkGraphStats(total_links=0, unique_sources=0, unique_targets=0, orphan_count=0)
        assert s.total_links == 0

    def test_dataclass_equality(self):
        a = LinkGraphStats(total_links=1, unique_sources=1, unique_targets=1, orphan_count=0)
        b = LinkGraphStats(total_links=1, unique_sources=1, unique_targets=1, orphan_count=0)
        assert a == b


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_graph(self):
        g = DocLinkGraph()
        assert g.all_nodes() == []
        assert g.all_links() == []

    def test_stats_empty(self):
        g = DocLinkGraph()
        s = g.stats()
        assert s.total_links == 0
        assert s.unique_sources == 0
        assert s.unique_targets == 0
        assert s.orphan_count == 0

    def test_independent_instances(self):
        g1 = DocLinkGraph()
        g2 = DocLinkGraph()
        g1.add_node("a")
        assert g2.all_nodes() == []


# ---------------------------------------------------------------------------
# add_node
# ---------------------------------------------------------------------------

class TestAddNode:
    def test_registers_node(self):
        g = DocLinkGraph()
        g.add_node("doc1")
        assert "doc1" in g.all_nodes()

    def test_no_duplicate_on_readd(self):
        g = DocLinkGraph()
        g.add_node("doc1")
        g.add_node("doc1")
        assert g.all_nodes().count("doc1") == 1

    def test_multiple_nodes(self):
        g = DocLinkGraph()
        for name in ("c", "a", "b"):
            g.add_node(name)
        assert g.all_nodes() == ["a", "b", "c"]

    def test_node_has_no_links(self):
        g = DocLinkGraph()
        g.add_node("solo")
        assert g.out_degree("solo") == 0
        assert g.in_degree("solo") == 0

    def test_orphan_after_add_node(self):
        g = DocLinkGraph()
        g.add_node("isolated")
        assert g.stats().orphan_count == 1


# ---------------------------------------------------------------------------
# remove_node
# ---------------------------------------------------------------------------

class TestRemoveNode:
    def test_removes_node(self):
        g = DocLinkGraph()
        g.add_node("a")
        g.remove_node("a")
        assert "a" not in g.all_nodes()

    def test_returns_zero_for_unknown(self):
        g = DocLinkGraph()
        assert g.remove_node("ghost") == 0

    def test_returns_count_of_removed_links(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("a", "c")
        removed = g.remove_node("a")
        assert removed == 2

    def test_removes_outgoing_links(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_node("a")
        assert g.in_degree("b") == 0
        assert not g.has_link("a", "b")

    def test_removes_incoming_links(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_node("b")
        assert g.out_degree("a") == 0
        assert not g.has_link("a", "b")

    def test_self_loop_counted_once(self):
        g = DocLinkGraph()
        g.add_link("a", "a")
        removed = g.remove_node("a")
        assert removed == 1
        assert g.all_nodes() == []

    def test_cascades_both_directions(self):
        g = DocLinkGraph()
        g.add_link("x", "y")
        g.add_link("z", "y")
        removed = g.remove_node("y")
        assert removed == 2
        assert g.out_degree("x") == 0
        assert g.out_degree("z") == 0


# ---------------------------------------------------------------------------
# add_link
# ---------------------------------------------------------------------------

class TestAddLink:
    def test_creates_link(self):
        g = DocLinkGraph()
        lnk = g.add_link("a", "b")
        assert isinstance(lnk, DocLink)
        assert lnk.from_doc == "a"
        assert lnk.to_doc == "b"

    def test_registers_both_nodes(self):
        g = DocLinkGraph()
        g.add_link("src", "dst")
        assert "src" in g.all_nodes()
        assert "dst" in g.all_nodes()

    def test_default_link_type(self):
        g = DocLinkGraph()
        lnk = g.add_link("a", "b")
        assert lnk.link_type == "internal"

    def test_custom_link_type(self):
        g = DocLinkGraph()
        lnk = g.add_link("a", "b", link_type="external")
        assert lnk.link_type == "external"

    def test_custom_anchor(self):
        g = DocLinkGraph()
        lnk = g.add_link("a", "b", anchor="See also")
        assert lnk.anchor == "See also"

    def test_custom_now(self):
        g = DocLinkGraph()
        lnk = g.add_link("a", "b", now=42.0)
        assert lnk.added_at == 42.0

    def test_update_anchor_on_readd(self):
        g = DocLinkGraph()
        g.add_link("a", "b", anchor="old")
        lnk2 = g.add_link("a", "b", anchor="new")
        assert lnk2.anchor == "new"
        assert len(g.all_links()) == 1

    def test_update_link_type_on_readd(self):
        g = DocLinkGraph()
        g.add_link("a", "b", link_type="internal")
        lnk2 = g.add_link("a", "b", link_type="citation")
        assert lnk2.link_type == "citation"
        assert len(g.all_links()) == 1

    def test_no_duplicate_in_all_links(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("a", "b")
        assert len(g.all_links()) == 1

    def test_self_link(self):
        g = DocLinkGraph()
        lnk = g.add_link("a", "a")
        assert lnk.from_doc == "a"
        assert lnk.to_doc == "a"


# ---------------------------------------------------------------------------
# remove_link
# ---------------------------------------------------------------------------

class TestRemoveLink:
    def test_returns_true_when_existed(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        assert g.remove_link("a", "b") is True

    def test_returns_false_when_absent(self):
        g = DocLinkGraph()
        g.add_node("a")
        assert g.remove_link("a", "b") is False

    def test_link_gone_after_remove(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_link("a", "b")
        assert not g.has_link("a", "b")

    def test_removed_from_outgoing(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_link("a", "b")
        assert g.outgoing("a") == []

    def test_removed_from_incoming(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_link("a", "b")
        assert g.incoming("b") == []

    def test_nodes_remain_after_remove_link(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_link("a", "b")
        assert "a" in g.all_nodes()
        assert "b" in g.all_nodes()


# ---------------------------------------------------------------------------
# get_link
# ---------------------------------------------------------------------------

class TestGetLink:
    def test_found(self):
        g = DocLinkGraph()
        g.add_link("a", "b", anchor="hello")
        lnk = g.get_link("a", "b")
        assert lnk is not None
        assert lnk.anchor == "hello"

    def test_not_found(self):
        g = DocLinkGraph()
        assert g.get_link("a", "b") is None

    def test_wrong_direction(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        assert g.get_link("b", "a") is None


# ---------------------------------------------------------------------------
# has_link
# ---------------------------------------------------------------------------

class TestHasLink:
    def test_true_when_present(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        assert g.has_link("a", "b") is True

    def test_false_when_absent(self):
        g = DocLinkGraph()
        assert g.has_link("a", "b") is False

    def test_directional(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        assert g.has_link("b", "a") is False


# ---------------------------------------------------------------------------
# outgoing
# ---------------------------------------------------------------------------

class TestOutgoing:
    def test_sorted_by_to_doc(self):
        g = DocLinkGraph()
        g.add_link("a", "c")
        g.add_link("a", "b")
        links = g.outgoing("a")
        assert [lnk.to_doc for lnk in links] == ["b", "c"]

    def test_empty_for_unknown_node(self):
        g = DocLinkGraph()
        assert g.outgoing("ghost") == []

    def test_empty_after_remove(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_link("a", "b")
        assert g.outgoing("a") == []

    def test_returns_doclink_instances(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        links = g.outgoing("a")
        assert all(isinstance(lnk, DocLink) for lnk in links)


# ---------------------------------------------------------------------------
# incoming
# ---------------------------------------------------------------------------

class TestIncoming:
    def test_sorted_by_from_doc(self):
        g = DocLinkGraph()
        g.add_link("c", "z")
        g.add_link("a", "z")
        links = g.incoming("z")
        assert [lnk.from_doc for lnk in links] == ["a", "c"]

    def test_empty_for_unknown_node(self):
        g = DocLinkGraph()
        assert g.incoming("ghost") == []

    def test_empty_after_remove(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_link("a", "b")
        assert g.incoming("b") == []

    def test_returns_doclink_instances(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        links = g.incoming("b")
        assert all(isinstance(lnk, DocLink) for lnk in links)


# ---------------------------------------------------------------------------
# Degrees
# ---------------------------------------------------------------------------

class TestDegrees:
    def test_out_degree(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("a", "c")
        assert g.out_degree("a") == 2

    def test_in_degree(self):
        g = DocLinkGraph()
        g.add_link("x", "z")
        g.add_link("y", "z")
        assert g.in_degree("z") == 2

    def test_out_degree_zero_for_unknown(self):
        g = DocLinkGraph()
        assert g.out_degree("nope") == 0

    def test_in_degree_zero_for_unknown(self):
        g = DocLinkGraph()
        assert g.in_degree("nope") == 0

    def test_degree_after_remove(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.remove_link("a", "b")
        assert g.out_degree("a") == 0
        assert g.in_degree("b") == 0


# ---------------------------------------------------------------------------
# all_links
# ---------------------------------------------------------------------------

class TestAllLinks:
    def test_sorted_by_from_to(self):
        g = DocLinkGraph()
        g.add_link("b", "c")
        g.add_link("a", "z")
        g.add_link("a", "b")
        links = g.all_links()
        keys = [(lnk.from_doc, lnk.to_doc) for lnk in links]
        assert keys == sorted(keys)

    def test_empty(self):
        g = DocLinkGraph()
        assert g.all_links() == []

    def test_count(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("c", "d")
        assert len(g.all_links()) == 2


# ---------------------------------------------------------------------------
# all_nodes
# ---------------------------------------------------------------------------

class TestAllNodes:
    def test_sorted(self):
        g = DocLinkGraph()
        for n in ("z", "a", "m"):
            g.add_node(n)
        assert g.all_nodes() == ["a", "m", "z"]

    def test_includes_isolated_nodes(self):
        g = DocLinkGraph()
        g.add_node("isolated")
        g.add_link("src", "dst")
        nodes = g.all_nodes()
        assert "isolated" in nodes
        assert "src" in nodes
        assert "dst" in nodes

    def test_empty(self):
        g = DocLinkGraph()
        assert g.all_nodes() == []

    def test_implicit_from_add_link(self):
        g = DocLinkGraph()
        g.add_link("from_doc", "to_doc")
        assert "from_doc" in g.all_nodes()
        assert "to_doc" in g.all_nodes()


# ---------------------------------------------------------------------------
# most_linked_to
# ---------------------------------------------------------------------------

class TestMostLinkedTo:
    def test_sorted_by_in_degree_desc(self):
        g = DocLinkGraph()
        g.add_link("a", "hub")
        g.add_link("b", "hub")
        g.add_link("c", "hub")
        g.add_link("a", "spoke")
        result = g.most_linked_to()
        assert result[0][0] == "hub"
        assert result[0][1] == 3

    def test_limit_respected(self):
        g = DocLinkGraph()
        for i in range(20):
            g.add_link(f"src{i}", "popular")
        result = g.most_linked_to(limit=5)
        assert len(result) <= 5

    def test_tie_break_by_doc_id_asc(self):
        g = DocLinkGraph()
        g.add_link("x", "beta")
        g.add_link("x", "alpha")
        result = g.most_linked_to()
        names = [r[0] for r in result]
        # both have in_degree 1; alpha < beta lexicographically
        assert names.index("alpha") < names.index("beta")

    def test_default_limit_10(self):
        g = DocLinkGraph()
        for i in range(15):
            target = f"t{i:02d}"
            g.add_link("src", target)
            # give each different in_degree by adding extra links
            for j in range(i):
                g.add_link(f"extra{i}_{j}", target)
        result = g.most_linked_to()
        assert len(result) <= 10

    def test_only_docs_with_incoming(self):
        g = DocLinkGraph()
        g.add_node("orphan")
        g.add_link("a", "b")
        result = g.most_linked_to()
        names = [r[0] for r in result]
        assert "orphan" not in names
        assert "a" not in names  # a has outgoing but no incoming


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty_graph(self):
        g = DocLinkGraph()
        s = g.stats()
        assert s.total_links == 0
        assert s.unique_sources == 0
        assert s.unique_targets == 0
        assert s.orphan_count == 0

    def test_total_links(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("b", "c")
        assert g.stats().total_links == 2

    def test_unique_sources(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("a", "c")
        g.add_link("d", "e")
        assert g.stats().unique_sources == 2  # a and d

    def test_unique_targets(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_link("c", "b")
        g.add_link("d", "e")
        assert g.stats().unique_targets == 2  # b and e

    def test_orphan_count_isolated_node(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        g.add_node("lonely")
        s = g.stats()
        assert s.orphan_count == 1

    def test_orphan_count_zero_when_all_connected(self):
        g = DocLinkGraph()
        g.add_link("a", "b")
        s = g.stats()
        assert s.orphan_count == 0

    def test_orphan_count_multiple(self):
        g = DocLinkGraph()
        g.add_node("x")
        g.add_node("y")
        g.add_node("z")
        s = g.stats()
        assert s.orphan_count == 3

    def test_source_not_counted_as_target(self):
        g = DocLinkGraph()
        g.add_link("only_out", "dst")
        s = g.stats()
        assert s.unique_sources == 1
        assert s.unique_targets == 1

    def test_returns_linkgraphstats_instance(self):
        g = DocLinkGraph()
        assert isinstance(g.stats(), LinkGraphStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_add_link(self):
        g = DocLinkGraph()
        errors: list[Exception] = []

        def worker(i: int) -> None:
            try:
                for j in range(20):
                    g.add_link(f"src{i}", f"dst{j}")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
        # 10 sources × 20 destinations = 200 links
        assert len(g.all_links()) == 200

    def test_concurrent_add_and_remove(self):
        g = DocLinkGraph()
        errors: list[Exception] = []

        def adder(i: int) -> None:
            try:
                for j in range(10):
                    g.add_link(f"a{i}", f"b{j}")
            except Exception as exc:
                errors.append(exc)

        def remover(i: int) -> None:
            try:
                for j in range(10):
                    g.remove_link(f"a{i}", f"b{j}")
            except Exception as exc:
                errors.append(exc)

        threads = []
        for i in range(5):
            threads.append(threading.Thread(target=adder, args=(i,)))
            threads.append(threading.Thread(target=remover, args=(i,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
