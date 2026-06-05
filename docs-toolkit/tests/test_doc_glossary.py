"""Tests for docstoolkit.doc_glossary (E251)."""
from __future__ import annotations

import pytest

from docstoolkit.doc_glossary import DocGlossary, GlossaryStats, Term


# ---------- Fixtures ----------


@pytest.fixture
def g() -> DocGlossary:
    return DocGlossary()


@pytest.fixture
def populated() -> DocGlossary:
    g = DocGlossary()
    g.add_term(
        "RAG",
        "Retrieval-Augmented Generation",
        category="ai",
        examples=["LangChain", "LlamaIndex"],
        synonyms=["retrieval augmented generation"],
        now=1.0,
    )
    g.add_term(
        "LLM",
        "Large Language Model",
        category="ai",
        examples=["GPT-4"],
        synonyms=["large language model"],
        now=2.0,
    )
    g.add_term(
        "API",
        "Application Programming Interface",
        category="web",
        now=3.0,
    )
    return g


# ---------- Term dataclass ----------


class TestTerm:
    def test_minimal(self):
        t = Term(term="x", definition="y")
        assert t.term == "x"
        assert t.definition == "y"
        assert t.category is None
        assert t.examples == []
        assert t.synonyms == []
        assert t.related == []
        assert t.created_at == 0.0
        assert t.updated_at == 0.0

    def test_full(self):
        t = Term(
            term="RAG",
            definition="def",
            category="ai",
            examples=["x"],
            synonyms=["y"],
            related=["LLM"],
            created_at=1.0,
            updated_at=2.0,
        )
        assert t.category == "ai"
        assert t.examples == ["x"]
        assert t.synonyms == ["y"]
        assert t.related == ["LLM"]

    def test_independent_defaults(self):
        a = Term(term="a", definition="b")
        b = Term(term="c", definition="d")
        a.examples.append("x")
        assert b.examples == []


# ---------- GlossaryStats ----------


class TestGlossaryStats:
    def test_default(self):
        s = GlossaryStats()
        assert s.total_terms == 0
        assert s.total_synonyms == 0
        assert s.total_categories == 0
        assert s.terms_by_category == {}
        assert s.terms_with_examples == 0

    def test_custom(self):
        s = GlossaryStats(
            total_terms=3,
            total_synonyms=2,
            total_categories=2,
            terms_by_category={"ai": 2, "web": 1},
            terms_with_examples=1,
        )
        assert s.total_terms == 3
        assert s.terms_by_category["ai"] == 2


# ---------- add_term ----------


class TestAddTerm:
    def test_basic(self, g: DocGlossary):
        t = g.add_term("RAG", "def")
        assert t.term == "RAG"
        assert t.definition == "def"
        assert g.term_count == 1

    def test_with_metadata(self, g: DocGlossary):
        t = g.add_term(
            "RAG",
            "def",
            category="ai",
            examples=["LangChain"],
            synonyms=["retrieval"],
            related=["LLM"],
            now=42.0,
        )
        assert t.category == "ai"
        assert t.examples == ["LangChain"]
        assert t.synonyms == ["retrieval"]
        assert t.related == ["LLM"]
        assert t.created_at == 42.0
        assert t.updated_at == 42.0

    def test_duplicate_raises(self, g: DocGlossary):
        g.add_term("RAG", "def")
        with pytest.raises(ValueError):
            g.add_term("RAG", "other")

    def test_duplicate_case_insensitive(self, g: DocGlossary):
        g.add_term("RAG", "def")
        with pytest.raises(ValueError):
            g.add_term("rag", "other")

    def test_empty_term_raises(self, g: DocGlossary):
        with pytest.raises(ValueError):
            g.add_term("", "def")

    def test_whitespace_only_raises(self, g: DocGlossary):
        with pytest.raises(ValueError):
            g.add_term("   ", "def")

    def test_synonym_registered(self, g: DocGlossary):
        g.add_term("RAG", "def", synonyms=["retrieval"])
        assert g.is_term("retrieval")


# ---------- update_term ----------


class TestUpdateTerm:
    def test_definition(self, populated: DocGlossary):
        t = populated.update_term("RAG", definition="new def", now=5.0)
        assert t is not None
        assert t.definition == "new def"
        assert t.updated_at == 5.0

    def test_category(self, populated: DocGlossary):
        t = populated.update_term("RAG", category="newcat")
        assert t.category == "newcat"

    def test_examples_replaces(self, populated: DocGlossary):
        t = populated.update_term("RAG", examples=["NewEx"])
        assert t.examples == ["NewEx"]

    def test_synonyms_replaces(self, populated: DocGlossary):
        t = populated.update_term("RAG", synonyms=["newsyn"])
        assert t.synonyms == ["newsyn"]
        assert populated.is_term("newsyn")
        # Old synonym removed
        assert not populated.is_term("retrieval augmented generation")

    def test_related(self, populated: DocGlossary):
        t = populated.update_term("RAG", related=["LLM"])
        assert t.related == ["LLM"]

    def test_unknown_returns_none(self, g: DocGlossary):
        assert g.update_term("nope", definition="x") is None

    def test_via_synonym(self, populated: DocGlossary):
        t = populated.update_term("retrieval augmented generation", definition="new")
        assert t is not None
        assert t.term == "RAG"
        assert t.definition == "new"


# ---------- remove_term ----------


class TestRemoveTerm:
    def test_basic(self, populated: DocGlossary):
        assert populated.remove_term("RAG") is True
        assert populated.get_term("RAG") is None
        assert populated.term_count == 2

    def test_unknown(self, g: DocGlossary):
        assert g.remove_term("nope") is False

    def test_clears_synonyms(self, populated: DocGlossary):
        populated.remove_term("RAG")
        assert not populated.is_term("retrieval augmented generation")

    def test_clears_related_refs(self, g: DocGlossary):
        g.add_term("A", "def-a")
        g.add_term("B", "def-b", related=["A"])
        g.remove_term("A")
        b = g.get_term("B")
        assert b.related == []

    def test_via_synonym(self, populated: DocGlossary):
        assert populated.remove_term("retrieval augmented generation") is True
        assert populated.get_term("RAG") is None


# ---------- get_term ----------


class TestGetTerm:
    def test_existing(self, populated: DocGlossary):
        t = populated.get_term("RAG")
        assert t is not None
        assert t.term == "RAG"

    def test_case_insensitive(self, populated: DocGlossary):
        assert populated.get_term("rag") is not None
        assert populated.get_term("Rag") is not None

    def test_missing(self, g: DocGlossary):
        assert g.get_term("nope") is None

    def test_empty(self, g: DocGlossary):
        assert g.get_term("") is None


# ---------- get_term by synonym ----------


class TestGetTermBySynonym:
    def test_lookup(self, populated: DocGlossary):
        t = populated.get_term("retrieval augmented generation")
        assert t is not None
        assert t.term == "RAG"

    def test_case_insensitive(self, populated: DocGlossary):
        t = populated.get_term("RETRIEVAL AUGMENTED GENERATION")
        assert t is not None
        assert t.term == "RAG"


# ---------- add_synonym ----------


class TestAddSynonym:
    def test_basic(self, populated: DocGlossary):
        assert populated.add_synonym("RAG", "rag-style") is True
        assert populated.is_term("rag-style")

    def test_unknown(self, g: DocGlossary):
        assert g.add_synonym("nope", "x") is False

    def test_empty(self, populated: DocGlossary):
        assert populated.add_synonym("RAG", "") is False
        assert populated.add_synonym("RAG", "   ") is False

    def test_idempotent(self, populated: DocGlossary):
        populated.add_synonym("RAG", "alias")
        populated.add_synonym("RAG", "alias")
        t = populated.get_term("RAG")
        assert t.synonyms.count("alias") == 1


# ---------- remove_synonym ----------


class TestRemoveSynonym:
    def test_basic(self, populated: DocGlossary):
        assert (
            populated.remove_synonym("RAG", "retrieval augmented generation")
            is True
        )
        assert not populated.is_term("retrieval augmented generation")

    def test_unknown_term(self, g: DocGlossary):
        assert g.remove_synonym("nope", "x") is False

    def test_unknown_synonym(self, populated: DocGlossary):
        assert populated.remove_synonym("RAG", "nope") is False

    def test_case_insensitive(self, populated: DocGlossary):
        assert (
            populated.remove_synonym("RAG", "RETRIEVAL AUGMENTED GENERATION")
            is True
        )


# ---------- add_related ----------


class TestAddRelated:
    def test_basic(self, populated: DocGlossary):
        assert populated.add_related("RAG", "LLM") is True
        t = populated.get_term("RAG")
        assert "LLM" in t.related

    def test_unknown_term(self, populated: DocGlossary):
        assert populated.add_related("nope", "LLM") is False

    def test_unknown_related(self, populated: DocGlossary):
        assert populated.add_related("RAG", "nope") is False

    def test_self_ref(self, populated: DocGlossary):
        assert populated.add_related("RAG", "RAG") is False

    def test_duplicate(self, populated: DocGlossary):
        populated.add_related("RAG", "LLM")
        assert populated.add_related("RAG", "LLM") is False


# ---------- remove_related ----------


class TestRemoveRelated:
    def test_basic(self, populated: DocGlossary):
        populated.add_related("RAG", "LLM")
        assert populated.remove_related("RAG", "LLM") is True
        t = populated.get_term("RAG")
        assert "LLM" not in t.related

    def test_unknown_term(self, g: DocGlossary):
        assert g.remove_related("nope", "x") is False

    def test_unknown_related(self, populated: DocGlossary):
        assert populated.remove_related("RAG", "nope") is False


# ---------- find_by_category ----------


class TestFindByCategory:
    def test_match(self, populated: DocGlossary):
        results = populated.find_by_category("ai")
        names = {t.term for t in results}
        assert names == {"RAG", "LLM"}

    def test_case_insensitive(self, populated: DocGlossary):
        assert len(populated.find_by_category("AI")) == 2

    def test_no_match(self, populated: DocGlossary):
        assert populated.find_by_category("missing") == []

    def test_empty(self, g: DocGlossary):
        assert g.find_by_category("any") == []


# ---------- find_by_keyword ----------


class TestFindByKeyword:
    def test_match(self, populated: DocGlossary):
        results = populated.find_by_keyword("language")
        assert len(results) == 1
        assert results[0].term == "LLM"

    def test_case_insensitive(self, populated: DocGlossary):
        results = populated.find_by_keyword("LANGUAGE")
        assert len(results) == 1

    def test_no_match(self, populated: DocGlossary):
        assert populated.find_by_keyword("zzz") == []

    def test_empty(self, populated: DocGlossary):
        assert populated.find_by_keyword("") == []


# ---------- search ----------


class TestSearch:
    def test_term_name(self, populated: DocGlossary):
        results = populated.search("RAG")
        assert any(t.term == "RAG" for t in results)

    def test_definition(self, populated: DocGlossary):
        results = populated.search("Retrieval")
        assert any(t.term == "RAG" for t in results)

    def test_examples(self, populated: DocGlossary):
        results = populated.search("LangChain")
        assert any(t.term == "RAG" for t in results)

    def test_synonyms(self, populated: DocGlossary):
        results = populated.search("retrieval augmented generation")
        assert any(t.term == "RAG" for t in results)

    def test_empty(self, populated: DocGlossary):
        assert populated.search("") == []

    def test_no_match(self, populated: DocGlossary):
        assert populated.search("zzz_no_match") == []


# ---------- all_terms ----------


class TestAllTerms:
    def test_sorted(self, populated: DocGlossary):
        names = [t.term for t in populated.all_terms()]
        assert names == ["API", "LLM", "RAG"]

    def test_empty(self, g: DocGlossary):
        assert g.all_terms() == []


# ---------- categories ----------


class TestCategories:
    def test_distinct_sorted(self, populated: DocGlossary):
        assert populated.categories() == ["ai", "web"]

    def test_empty(self, g: DocGlossary):
        assert g.categories() == []

    def test_skips_none(self, g: DocGlossary):
        g.add_term("X", "def")
        assert g.categories() == []


# ---------- auto_link ----------


class TestAutoLink:
    def test_basic(self, populated: DocGlossary):
        out = populated.auto_link("Use RAG with an LLM.")
        assert "[RAG](#rag)" in out
        assert "[LLM](#llm)" in out

    def test_case_insensitive(self, populated: DocGlossary):
        out = populated.auto_link("use rag for retrieval.")
        assert "[rag](#rag)" in out

    def test_whole_word(self, populated: DocGlossary):
        out = populated.auto_link("ragdoll is not a term.")
        assert "ragdoll" in out
        assert "[rag]" not in out.lower() or "ragdoll" in out

    def test_once_per_term(self, populated: DocGlossary):
        out = populated.auto_link("RAG and RAG and RAG.")
        # only first replaced
        assert out.count("[RAG](#rag)") == 1
        assert out.count("RAG") >= 3  # raw occurrences also remain

    def test_avoid_code_block(self, populated: DocGlossary):
        text = "```\nRAG\n```\nThen RAG outside."
        out = populated.auto_link(text)
        # inside code block stays untouched
        assert "```\nRAG\n```" in out
        # outside is linked
        assert "[RAG](#rag)" in out

    def test_avoid_inline_code(self, populated: DocGlossary):
        text = "`RAG` is code; but RAG is a term."
        out = populated.auto_link(text)
        assert "`RAG`" in out
        assert "[RAG](#rag)" in out

    def test_avoid_existing_link(self, populated: DocGlossary):
        text = "See [RAG](https://example.com) and also RAG."
        out = populated.auto_link(text)
        assert "[RAG](https://example.com)" in out
        assert "[RAG](#rag)" in out

    def test_synonym_linking(self, populated: DocGlossary):
        out = populated.auto_link("retrieval augmented generation is great.")
        # The matched text retains its case, linked to canonical slug
        assert "(#rag)" in out

    def test_custom_format(self, populated: DocGlossary):
        out = populated.auto_link("See RAG.", term_format="<{term}|{slug}>")
        assert "<RAG|rag>" in out

    def test_empty(self, populated: DocGlossary):
        assert populated.auto_link("") == ""

    def test_no_terms(self, g: DocGlossary):
        assert g.auto_link("hello world") == "hello world"

    def test_longer_phrase_priority(self, g: DocGlossary):
        g.add_term("machine", "x")
        g.add_term("machine learning", "y")
        out = g.auto_link("machine learning is great")
        assert "[machine learning](#machine-learning)" in out
        assert "[machine](#machine)" not in out


# ---------- extract_mentioned ----------


class TestExtractMentioned:
    def test_basic(self, populated: DocGlossary):
        mentions = populated.extract_mentioned("Use RAG and LLM.")
        assert set(mentions) == {"RAG", "LLM"}

    def test_dedup(self, populated: DocGlossary):
        mentions = populated.extract_mentioned("RAG and RAG and RAG.")
        assert mentions == ["RAG"]

    def test_via_synonym(self, populated: DocGlossary):
        mentions = populated.extract_mentioned(
            "retrieval augmented generation rocks"
        )
        assert "RAG" in mentions

    def test_ignores_code(self, populated: DocGlossary):
        mentions = populated.extract_mentioned("`RAG` is code")
        assert mentions == []

    def test_empty(self, g: DocGlossary):
        assert g.extract_mentioned("") == []


# ---------- to_markdown ----------


class TestToMarkdown:
    def test_empty(self, g: DocGlossary):
        md = g.to_markdown()
        assert "Glossary" in md
        assert "No terms" in md

    def test_renders_terms(self, populated: DocGlossary):
        md = populated.to_markdown()
        assert "# Glossary" in md
        assert "RAG" in md
        assert "Retrieval-Augmented Generation" in md
        assert "LangChain" in md

    def test_groups_by_category(self, populated: DocGlossary):
        md = populated.to_markdown()
        assert "## ai" in md
        assert "## web" in md

    def test_includes_synonyms(self, populated: DocGlossary):
        md = populated.to_markdown()
        assert "Synonyms" in md

    def test_includes_related(self, g: DocGlossary):
        g.add_term("A", "def-a")
        g.add_term("B", "def-b", related=["A"])
        md = g.to_markdown()
        assert "Related" in md


# ---------- to_dict ----------


class TestToDict:
    def test_basic(self, populated: DocGlossary):
        d = populated.to_dict()
        assert isinstance(d, list)
        assert len(d) == 3
        terms = {e["term"] for e in d}
        assert terms == {"RAG", "LLM", "API"}

    def test_fields(self, populated: DocGlossary):
        d = populated.to_dict()
        for entry in d:
            assert "term" in entry
            assert "definition" in entry
            assert "category" in entry
            assert "examples" in entry
            assert "synonyms" in entry
            assert "related" in entry
            assert "created_at" in entry
            assert "updated_at" in entry

    def test_empty(self, g: DocGlossary):
        assert g.to_dict() == []


# ---------- from_dict ----------


class TestFromDict:
    def test_basic(self, g: DocGlossary):
        n = g.from_dict(
            [
                {"term": "A", "definition": "def-a"},
                {"term": "B", "definition": "def-b"},
            ]
        )
        assert n == 2
        assert g.term_count == 2

    def test_with_full_fields(self, g: DocGlossary):
        n = g.from_dict(
            [
                {
                    "term": "RAG",
                    "definition": "def",
                    "category": "ai",
                    "examples": ["x"],
                    "synonyms": ["y"],
                    "related": [],
                    "created_at": 1.0,
                    "updated_at": 2.0,
                }
            ]
        )
        assert n == 1
        t = g.get_term("RAG")
        assert t.examples == ["x"]
        assert t.synonyms == ["y"]
        assert g.is_term("y")

    def test_skips_duplicates(self, populated: DocGlossary):
        n = populated.from_dict([{"term": "RAG", "definition": "different"}])
        assert n == 0
        # Definition unchanged
        assert populated.get_term("RAG").definition == "Retrieval-Augmented Generation"

    def test_skips_missing_term(self, g: DocGlossary):
        n = g.from_dict([{"definition": "no term"}])
        assert n == 0

    def test_empty(self, g: DocGlossary):
        assert g.from_dict([]) == 0

    def test_roundtrip(self, populated: DocGlossary):
        d = populated.to_dict()
        g2 = DocGlossary()
        n = g2.from_dict(d)
        assert n == 3
        assert g2.term_count == 3


# ---------- is_term ----------


class TestIsTerm:
    def test_canonical(self, populated: DocGlossary):
        assert populated.is_term("RAG") is True

    def test_synonym(self, populated: DocGlossary):
        assert populated.is_term("retrieval augmented generation") is True

    def test_case_insensitive(self, populated: DocGlossary):
        assert populated.is_term("rag") is True

    def test_unknown(self, populated: DocGlossary):
        assert populated.is_term("nope") is False

    def test_empty(self, g: DocGlossary):
        assert g.is_term("") is False


# ---------- stats ----------


class TestStats:
    def test_empty(self, g: DocGlossary):
        s = g.stats()
        assert s.total_terms == 0
        assert s.total_synonyms == 0
        assert s.total_categories == 0
        assert s.terms_by_category == {}
        assert s.terms_with_examples == 0

    def test_populated(self, populated: DocGlossary):
        s = populated.stats()
        assert s.total_terms == 3
        assert s.total_synonyms == 2
        assert s.total_categories == 2
        assert s.terms_by_category.get("ai") == 2
        assert s.terms_by_category.get("web") == 1
        assert s.terms_with_examples == 2

    def test_uncategorized(self, g: DocGlossary):
        g.add_term("X", "def")
        s = g.stats()
        assert s.terms_by_category.get("Uncategorized") == 1
        assert s.total_categories == 0


# ---------- term_count ----------


class TestTermCount:
    def test_empty(self, g: DocGlossary):
        assert g.term_count == 0

    def test_after_add(self, g: DocGlossary):
        g.add_term("A", "x")
        g.add_term("B", "y")
        assert g.term_count == 2

    def test_after_remove(self, populated: DocGlossary):
        populated.remove_term("RAG")
        assert populated.term_count == 2


# ---------- clear ----------


class TestClear:
    def test_clears_all(self, populated: DocGlossary):
        populated.clear()
        assert populated.term_count == 0
        assert not populated.is_term("RAG")
        assert not populated.is_term("retrieval augmented generation")

    def test_idempotent(self, g: DocGlossary):
        g.clear()
        g.clear()
        assert g.term_count == 0


# ---------- edge cases ----------


class TestEdgeCases:
    def test_unicode_term(self, g: DocGlossary):
        g.add_term("Связи", "общение")
        assert g.is_term("Связи")
        assert g.get_term("связи").definition == "общение"

    def test_unicode_auto_link(self, g: DocGlossary):
        g.add_term("Связи", "общение")
        out = g.auto_link("Связи это важно")
        # The slugifier strips non-word characters but Cyrillic word chars survive
        assert "Связи" in out
        assert "](#" in out

    def test_terms_with_special_chars(self, g: DocGlossary):
        g.add_term("C++", "language")
        # Whole-word match with special chars: '++' aren't word chars.
        out = g.auto_link("Use C++ here")
        # Verify no crash; the linker tolerates special chars via re.escape
        assert "C++" in out

    def test_long_definition(self, g: DocGlossary):
        defn = "x" * 5000
        g.add_term("Long", defn)
        assert g.get_term("Long").definition == defn

    def test_many_terms(self, g: DocGlossary):
        for i in range(100):
            g.add_term(f"T{i}", f"d{i}")
        assert g.term_count == 100
        assert len(g.all_terms()) == 100

    def test_synonym_collision_with_term(self, g: DocGlossary):
        g.add_term("A", "def-a")
        g.add_term("B", "def-b", synonyms=["A"])
        # Canonical A wins on resolution
        t = g.get_term("A")
        assert t.term == "A"

    def test_update_clears_old_synonyms(self, g: DocGlossary):
        g.add_term("X", "d", synonyms=["alpha", "beta"])
        g.update_term("X", synonyms=["gamma"])
        assert g.is_term("gamma")
        assert not g.is_term("alpha")
        assert not g.is_term("beta")

    def test_search_substring(self, populated: DocGlossary):
        results = populated.search("ret")
        assert any(t.term == "RAG" for t in results)

    def test_to_markdown_anchor(self, populated: DocGlossary):
        md = populated.to_markdown()
        assert 'id="rag"' in md

    def test_extract_mentioned_order_independent(self, populated: DocGlossary):
        mentions = set(populated.extract_mentioned("LLM and RAG and API."))
        assert mentions == {"LLM", "RAG", "API"}
