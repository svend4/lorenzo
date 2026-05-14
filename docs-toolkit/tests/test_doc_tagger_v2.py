"""Tests for E208 doc_tagger_v2."""
from __future__ import annotations

import pytest

from docstoolkit.doc_tagger_v2 import (
    DocTaggerV2,
    TagDefinition,
    TaggingFeedback,
    TagSuggestion,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestTagDefinition:
    def test_minimal(self):
        d = TagDefinition(tag="ai")
        assert d.tag == "ai"
        assert d.parent is None
        assert d.aliases == []
        assert d.keywords == []
        assert d.description == ""
        assert d.usage_count == 0

    def test_with_parent(self):
        d = TagDefinition(tag="ml", parent="ai")
        assert d.parent == "ai"

    def test_with_aliases_and_keywords(self):
        d = TagDefinition(
            tag="ai",
            aliases=["artificial-intelligence"],
            keywords=["agent", "model"],
        )
        assert d.aliases == ["artificial-intelligence"]
        assert d.keywords == ["agent", "model"]

    def test_independent_default_lists(self):
        d1 = TagDefinition(tag="a")
        d2 = TagDefinition(tag="b")
        d1.aliases.append("x")
        assert d2.aliases == []


class TestTagSuggestion:
    def test_basic(self):
        s = TagSuggestion(tag="ai", confidence=0.8, source="keyword")
        assert s.tag == "ai"
        assert s.confidence == 0.8
        assert s.source == "keyword"

    def test_ancestor_source(self):
        s = TagSuggestion(tag="root", confidence=0.4, source="ancestor")
        assert s.source == "ancestor"


class TestTaggingFeedback:
    def test_basic(self):
        fb = TaggingFeedback(doc_id="d1", tag="ai", accepted=True, timestamp=1.0)
        assert fb.doc_id == "d1"
        assert fb.tag == "ai"
        assert fb.accepted is True
        assert fb.timestamp == 1.0

    def test_rejected(self):
        fb = TaggingFeedback(doc_id="d", tag="t", accepted=False, timestamp=0.0)
        assert fb.accepted is False


# ---------------------------------------------------------------------------
# define_tag
# ---------------------------------------------------------------------------


class TestDefineTag:
    def test_creates_tag(self):
        t = DocTaggerV2()
        d = t.define_tag("ai", keywords=["agent"])
        assert d.tag == "ai"
        assert "agent" in d.keywords
        assert t.total_tags == 1

    def test_empty_raises(self):
        t = DocTaggerV2()
        with pytest.raises(ValueError):
            t.define_tag("")

    def test_whitespace_raises(self):
        t = DocTaggerV2()
        with pytest.raises(ValueError):
            t.define_tag("   ")

    def test_with_parent(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        d = t.define_tag("ml", parent="ai")
        assert d.parent == "ai"

    def test_parent_missing_silent(self):
        t = DocTaggerV2()
        d = t.define_tag("ml", parent="ai")
        assert d.parent is None  # parent not registered

    def test_with_aliases(self):
        t = DocTaggerV2()
        d = t.define_tag("ai", aliases=["artificial-intelligence", "AI"])
        assert "artificial-intelligence" in d.aliases

    def test_update_existing(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent"])
        t.define_tag("ai", keywords=["model"], description="d")
        d = t.tag_definition("ai")
        assert "agent" in d.keywords
        assert "model" in d.keywords
        assert d.description == "d"


# ---------------------------------------------------------------------------
# remove_tag
# ---------------------------------------------------------------------------


class TestRemoveTag:
    def test_removes(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        assert t.remove_tag("ai") is True
        assert t.total_tags == 0

    def test_missing(self):
        t = DocTaggerV2()
        assert t.remove_tag("nope") is False

    def test_detaches_children(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        t.define_tag("ml", parent="ai")
        t.remove_tag("ai")
        assert t.tag_definition("ml").parent is None

    def test_removes_aliases(self):
        t = DocTaggerV2()
        t.define_tag("ai", aliases=["AI"])
        t.remove_tag("ai")
        assert t.resolve_alias("AI") is None


# ---------------------------------------------------------------------------
# add_keyword
# ---------------------------------------------------------------------------


class TestAddKeyword:
    def test_adds(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        assert t.add_keyword("ai", "agent") is True
        assert "agent" in t.tag_definition("ai").keywords

    def test_unknown_tag(self):
        t = DocTaggerV2()
        assert t.add_keyword("nope", "x") is False

    def test_duplicate(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent"])
        assert t.add_keyword("ai", "agent") is False

    def test_empty(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        assert t.add_keyword("ai", "") is False


# ---------------------------------------------------------------------------
# add_alias
# ---------------------------------------------------------------------------


class TestAddAlias:
    def test_adds(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        assert t.add_alias("ai", "artificial-intelligence") is True
        assert t.resolve_alias("artificial-intelligence") == "ai"

    def test_unknown_tag(self):
        t = DocTaggerV2()
        assert t.add_alias("nope", "x") is False

    def test_duplicate(self):
        t = DocTaggerV2()
        t.define_tag("ai", aliases=["AI"])
        assert t.add_alias("ai", "AI") is False

    def test_collision(self):
        t = DocTaggerV2()
        t.define_tag("ai", aliases=["smart"])
        t.define_tag("ml")
        # alias already taken by another tag
        assert t.add_alias("ml", "smart") is False

    def test_case_insensitive_lookup(self):
        t = DocTaggerV2()
        t.define_tag("ai", aliases=["Artificial-Intelligence"])
        assert t.resolve_alias("artificial-intelligence") == "ai"


# ---------------------------------------------------------------------------
# set_parent
# ---------------------------------------------------------------------------


class TestSetParent:
    def test_sets(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        t.define_tag("ml")
        assert t.set_parent("ml", "ai") is True
        assert t.tag_definition("ml").parent == "ai"

    def test_clears(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        t.define_tag("ml", parent="ai")
        assert t.set_parent("ml", None) is True
        assert t.tag_definition("ml").parent is None

    def test_missing_parent(self):
        t = DocTaggerV2()
        t.define_tag("ml")
        assert t.set_parent("ml", "nope") is False

    def test_missing_tag(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        assert t.set_parent("nope", "ai") is False

    def test_self_parent(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        assert t.set_parent("ai", "ai") is False

    def test_cycle_detection(self):
        t = DocTaggerV2()
        t.define_tag("a")
        t.define_tag("b", parent="a")
        t.define_tag("c", parent="b")
        # making a's parent c would create a cycle
        assert t.set_parent("a", "c") is False


# ---------------------------------------------------------------------------
# tag_text
# ---------------------------------------------------------------------------


class TestTagText:
    def test_basic_match(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent", "model"])
        result = t.tag_text("the agent uses a model", min_confidence=0.0)
        assert any(s.tag == "ai" for s in result)

    def test_confidence_full(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent", "model"])
        result = t.tag_text("agent model")
        s = next(x for x in result if x.tag == "ai")
        assert s.confidence == pytest.approx(1.0)

    def test_confidence_partial(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent", "model", "robot"])
        result = t.tag_text("agent only", min_confidence=0.0)
        s = next(x for x in result if x.tag == "ai")
        assert s.confidence == pytest.approx(1 / 3)

    def test_min_confidence_filter(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent", "model", "robot"])
        # only 1/3 confidence
        result = t.tag_text("agent only", min_confidence=0.5)
        assert all(s.tag != "ai" for s in result)

    def test_max_tags(self):
        t = DocTaggerV2()
        for i, kw in enumerate(["a", "b", "c"]):
            t.define_tag(f"t{i}", keywords=[kw])
        result = t.tag_text("a b c", max_tags=2, min_confidence=0.0)
        assert len(result) == 2

    def test_whole_word(self):
        t = DocTaggerV2()
        t.define_tag("cat", keywords=["cat"])
        result = t.tag_text("scattered concatenation", min_confidence=0.0)
        assert all(s.tag != "cat" for s in result)

    def test_case_insensitive(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["Agent"])
        result = t.tag_text("the AGENT runs", min_confidence=0.0)
        assert any(s.tag == "ai" for s in result)

    def test_empty_text(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent"])
        assert t.tag_text("") == []

    def test_source_is_keyword(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent"])
        result = t.tag_text("agent")
        assert result[0].source == "keyword"

    def test_increments_usage(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent"])
        t.tag_text("agent")
        assert t.tag_definition("ai").usage_count == 1


# ---------------------------------------------------------------------------
# tag_text_with_ancestors
# ---------------------------------------------------------------------------


class TestTagTextWithAncestors:
    def test_includes_ancestors(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        t.define_tag("ml", parent="ai", keywords=["neural"])
        result = t.tag_text_with_ancestors("neural network", min_confidence=0.0)
        tags = {s.tag for s in result}
        assert "ml" in tags
        assert "ai" in tags

    def test_ancestor_source_label(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        t.define_tag("ml", parent="ai", keywords=["neural"])
        result = t.tag_text_with_ancestors("neural network", min_confidence=0.0)
        anc = next(s for s in result if s.tag == "ai")
        assert anc.source == "ancestor"

    def test_no_ancestor_if_no_match(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        t.define_tag("ml", parent="ai", keywords=["neural"])
        result = t.tag_text_with_ancestors("nothing related", min_confidence=0.0)
        assert all(s.tag != "ai" for s in result)

    def test_max_tags_respected(self):
        t = DocTaggerV2()
        t.define_tag("root")
        t.define_tag("mid", parent="root")
        t.define_tag("leaf", parent="mid", keywords=["x"])
        result = t.tag_text_with_ancestors("x", max_tags=2, min_confidence=0.0)
        assert len(result) == 2


# ---------------------------------------------------------------------------
# record_feedback
# ---------------------------------------------------------------------------


class TestRecordFeedback:
    def test_returns_record(self):
        t = DocTaggerV2()
        fb = t.record_feedback("d1", "ai", True, now=10.0)
        assert isinstance(fb, TaggingFeedback)
        assert fb.doc_id == "d1"
        assert fb.tag == "ai"
        assert fb.accepted is True
        assert fb.timestamp == 10.0

    def test_multiple(self):
        t = DocTaggerV2()
        t.record_feedback("d1", "ai", True)
        t.record_feedback("d2", "ai", False)
        # acceptance rate
        assert t.acceptance_rate("ai") == 0.5


# ---------------------------------------------------------------------------
# suggested_tags
# ---------------------------------------------------------------------------


class TestSuggestedTags:
    def test_returns_strings(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent"])
        out = t.suggested_tags("the agent runs")
        assert out == ["ai"]

    def test_empty(self):
        t = DocTaggerV2()
        assert t.suggested_tags("text") == []


# ---------------------------------------------------------------------------
# resolve_alias
# ---------------------------------------------------------------------------


class TestResolveAlias:
    def test_canonical(self):
        t = DocTaggerV2()
        t.define_tag("ai", aliases=["AI"])
        assert t.resolve_alias("ai") == "ai"

    def test_alias(self):
        t = DocTaggerV2()
        t.define_tag("ai", aliases=["AI", "artificial-intelligence"])
        assert t.resolve_alias("AI") == "ai"
        assert t.resolve_alias("artificial-intelligence") == "ai"

    def test_unknown(self):
        t = DocTaggerV2()
        assert t.resolve_alias("nope") is None

    def test_empty(self):
        t = DocTaggerV2()
        assert t.resolve_alias("") is None


# ---------------------------------------------------------------------------
# ancestors
# ---------------------------------------------------------------------------


class TestAncestors:
    def test_chain(self):
        t = DocTaggerV2()
        t.define_tag("root")
        t.define_tag("mid", parent="root")
        t.define_tag("leaf", parent="mid")
        assert t.ancestors("leaf") == ["mid", "root"]

    def test_no_parent(self):
        t = DocTaggerV2()
        t.define_tag("root")
        assert t.ancestors("root") == []

    def test_unknown(self):
        t = DocTaggerV2()
        assert t.ancestors("nope") == []


# ---------------------------------------------------------------------------
# descendants
# ---------------------------------------------------------------------------


class TestDescendants:
    def test_tree(self):
        t = DocTaggerV2()
        t.define_tag("root")
        t.define_tag("a", parent="root")
        t.define_tag("b", parent="root")
        t.define_tag("a1", parent="a")
        result = t.descendants("root")
        assert set(result) == {"a", "b", "a1"}

    def test_leaf(self):
        t = DocTaggerV2()
        t.define_tag("root")
        assert t.descendants("root") == []

    def test_unknown(self):
        t = DocTaggerV2()
        assert t.descendants("nope") == []


# ---------------------------------------------------------------------------
# siblings
# ---------------------------------------------------------------------------


class TestSiblings:
    def test_basic(self):
        t = DocTaggerV2()
        t.define_tag("root")
        t.define_tag("a", parent="root")
        t.define_tag("b", parent="root")
        t.define_tag("c", parent="root")
        assert t.siblings("a") == ["b", "c"]

    def test_no_parent_siblings(self):
        t = DocTaggerV2()
        t.define_tag("a")
        t.define_tag("b")
        # both have parent None — siblings
        assert t.siblings("a") == ["b"]

    def test_unknown(self):
        t = DocTaggerV2()
        assert t.siblings("nope") == []


# ---------------------------------------------------------------------------
# co_occurring
# ---------------------------------------------------------------------------


class TestCoOccurring:
    def test_basic(self):
        t = DocTaggerV2()
        t.record_doc_tags("d1", ["ai", "ml", "nlp"])
        t.record_doc_tags("d2", ["ai", "ml"])
        result = t.co_occurring("ai")
        d = dict(result)
        assert d.get("ml") == 2
        assert d.get("nlp") == 1

    def test_top_k(self):
        t = DocTaggerV2()
        t.record_doc_tags("d1", ["ai", "a", "b", "c"])
        assert len(t.co_occurring("ai", top_k=2)) == 2

    def test_empty(self):
        t = DocTaggerV2()
        assert t.co_occurring("ai") == []


# ---------------------------------------------------------------------------
# record_doc_tags
# ---------------------------------------------------------------------------


class TestRecordDocTags:
    def test_increments_pairs(self):
        t = DocTaggerV2()
        t.record_doc_tags("d1", ["x", "y"])
        result = t.co_occurring("x")
        assert ("y", 1) in result

    def test_dedupes_within_doc(self):
        t = DocTaggerV2()
        t.record_doc_tags("d1", ["x", "y", "x"])
        result = dict(t.co_occurring("x"))
        # y should only count once
        assert result.get("y") == 1

    def test_empty_tags(self):
        t = DocTaggerV2()
        t.record_doc_tags("d1", [])
        assert t.co_occurring("anything") == []


# ---------------------------------------------------------------------------
# acceptance_rate
# ---------------------------------------------------------------------------


class TestAcceptanceRate:
    def test_no_feedback(self):
        t = DocTaggerV2()
        assert t.acceptance_rate("ai") == 0.0

    def test_all_accepted(self):
        t = DocTaggerV2()
        t.record_feedback("d1", "ai", True)
        t.record_feedback("d2", "ai", True)
        assert t.acceptance_rate("ai") == 1.0

    def test_mixed(self):
        t = DocTaggerV2()
        t.record_feedback("d1", "ai", True)
        t.record_feedback("d2", "ai", False)
        t.record_feedback("d3", "ai", False)
        assert t.acceptance_rate("ai") == pytest.approx(1 / 3)


# ---------------------------------------------------------------------------
# total_tags
# ---------------------------------------------------------------------------


class TestTotalTags:
    def test_zero(self):
        t = DocTaggerV2()
        assert t.total_tags == 0

    def test_grows(self):
        t = DocTaggerV2()
        t.define_tag("a")
        t.define_tag("b")
        assert t.total_tags == 2


# ---------------------------------------------------------------------------
# tag_definition lookup
# ---------------------------------------------------------------------------


class TestTagDefinitionLookup:
    def test_known(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        assert t.tag_definition("ai").tag == "ai"

    def test_unknown(self):
        t = DocTaggerV2()
        assert t.tag_definition("nope") is None


# ---------------------------------------------------------------------------
# all_tags
# ---------------------------------------------------------------------------


class TestAllTags:
    def test_sorted(self):
        t = DocTaggerV2()
        t.define_tag("b")
        t.define_tag("a")
        t.define_tag("c")
        assert t.all_tags() == ["a", "b", "c"]

    def test_empty(self):
        t = DocTaggerV2()
        assert t.all_tags() == []


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_removes_everything(self):
        t = DocTaggerV2()
        t.define_tag("ai", keywords=["agent"], aliases=["AI"])
        t.record_doc_tags("d1", ["ai", "ml"])
        t.record_feedback("d1", "ai", True)
        t.clear()
        assert t.total_tags == 0
        assert t.resolve_alias("AI") is None
        assert t.acceptance_rate("ai") == 0.0
        assert t.co_occurring("ai") == []


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_cycle_in_existing_chain_returns_false(self):
        t = DocTaggerV2()
        t.define_tag("a")
        t.define_tag("b", parent="a")
        # b's parent is a; trying to set a's parent to b would cycle
        assert t.set_parent("a", "b") is False

    def test_long_chain_ancestors(self):
        t = DocTaggerV2()
        t.define_tag("t0")
        for i in range(1, 5):
            t.define_tag(f"t{i}", parent=f"t{i-1}")
        anc = t.ancestors("t4")
        assert anc == ["t3", "t2", "t1", "t0"]

    def test_remove_tag_clears_cooccurrence(self):
        t = DocTaggerV2()
        t.record_doc_tags("d1", ["a", "b"])
        t.define_tag("a")
        t.define_tag("b")
        t.remove_tag("a")
        # b should no longer co-occur with a
        assert all(other != "a" for other, _ in t.co_occurring("b"))

    def test_alias_resolves_to_canonical_when_input_is_canonical(self):
        t = DocTaggerV2()
        t.define_tag("ai")
        assert t.resolve_alias("ai") == "ai"

    def test_descendants_with_cycle_safe(self):
        # We can't actually create a cycle through set_parent,
        # so this just tests the BFS terminates on a normal tree.
        t = DocTaggerV2()
        t.define_tag("a")
        t.define_tag("b", parent="a")
        t.define_tag("c", parent="b")
        assert set(t.descendants("a")) == {"b", "c"}

    def test_missing_tag_in_feedback(self):
        # Recording feedback for an unregistered tag still works.
        t = DocTaggerV2()
        fb = t.record_feedback("d", "ghost", True)
        assert fb.tag == "ghost"
        assert t.acceptance_rate("ghost") == 1.0

    def test_define_tag_with_parent_creates_link(self):
        t = DocTaggerV2()
        t.define_tag("root")
        t.define_tag("child", parent="root")
        assert "child" in t.descendants("root")
