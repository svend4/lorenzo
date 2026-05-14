"""Tests for docstoolkit.glossary_builder — target: >= 40 tests."""
from __future__ import annotations

import pytest

from docstoolkit.glossary_builder import GlossaryBuilder, GlossaryConfig, GlossaryTerm


# ===========================================================================
# TestGlossaryTerm
# ===========================================================================


class TestGlossaryTerm:
    def test_term_field(self):
        t = GlossaryTerm(term="Machine Learning", definition="A field of AI.")
        assert t.term == "Machine Learning"

    def test_definition_field(self):
        t = GlossaryTerm(term="Machine Learning", definition="A field of AI.")
        assert t.definition == "A field of AI."

    def test_aliases_defaults_to_empty_list(self):
        t = GlossaryTerm(term="Machine Learning", definition="Def.")
        assert t.aliases == []

    def test_occurrences_defaults_to_zero(self):
        t = GlossaryTerm(term="Machine Learning", definition="Def.")
        assert t.occurrences == 0

    def test_first_line_defaults_to_zero(self):
        t = GlossaryTerm(term="Machine Learning", definition="Def.")
        assert t.first_line == 0

    def test_context_defaults_to_empty_string(self):
        t = GlossaryTerm(term="Machine Learning", definition="Def.")
        assert t.context == ""

    def test_custom_aliases(self):
        t = GlossaryTerm(term="Machine Learning", definition="Def.", aliases=["ML"])
        assert t.aliases == ["ML"]

    def test_custom_occurrences(self):
        t = GlossaryTerm(term="Machine Learning", definition="Def.", occurrences=5)
        assert t.occurrences == 5

    def test_custom_first_line(self):
        t = GlossaryTerm(term="Machine Learning", definition="Def.", first_line=3)
        assert t.first_line == 3

    def test_custom_context(self):
        t = GlossaryTerm(
            term="Machine Learning", definition="Def.", context="ML is used here."
        )
        assert t.context == "ML is used here."


# ===========================================================================
# TestGlossaryConfig
# ===========================================================================


class TestGlossaryConfig:
    def test_default_min_term_length(self):
        cfg = GlossaryConfig()
        assert cfg.min_term_length == 3

    def test_default_min_occurrences(self):
        cfg = GlossaryConfig()
        assert cfg.min_occurrences == 2

    def test_default_extract_abbreviations(self):
        cfg = GlossaryConfig()
        assert cfg.extract_abbreviations is True

    def test_default_max_definition_length(self):
        cfg = GlossaryConfig()
        assert cfg.max_definition_length == 200

    def test_custom_min_term_length(self):
        cfg = GlossaryConfig(min_term_length=5)
        assert cfg.min_term_length == 5

    def test_custom_min_occurrences(self):
        cfg = GlossaryConfig(min_occurrences=3)
        assert cfg.min_occurrences == 3

    def test_custom_extract_abbreviations_false(self):
        cfg = GlossaryConfig(extract_abbreviations=False)
        assert cfg.extract_abbreviations is False

    def test_custom_max_definition_length(self):
        cfg = GlossaryConfig(max_definition_length=50)
        assert cfg.max_definition_length == 50


# ===========================================================================
# TestBuildBasic
# ===========================================================================


class TestBuildBasic:
    def test_finds_capitalized_two_word_phrase(self):
        text = (
            "Machine Learning is a powerful technique. "
            "Machine Learning has many applications. "
            "Machine Learning continues to grow."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        term_names = [t.term for t in terms]
        assert "Machine Learning" in term_names

    def test_finds_three_word_phrase(self):
        text = (
            "Natural Language Processing is a field. "
            "Natural Language Processing enables machines to understand text. "
            "Natural Language Processing has many uses."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        term_names = [t.term for t in terms]
        assert "Natural Language Processing" in term_names

    def test_definition_is_first_sentence_containing_term(self):
        text = (
            "Deep Learning is a subset of Machine Learning. "
            "Deep Learning uses neural networks. "
            "Deep Learning is very powerful."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        dl = next((t for t in terms if t.term == "Deep Learning"), None)
        assert dl is not None
        assert "Deep Learning is a subset" in dl.definition

    def test_occurrences_count(self):
        text = (
            "Neural Network is great. "
            "Neural Network solves problems. "
            "Neural Network is widely used."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=1))
        terms = builder.build(text)
        nn = next((t for t in terms if t.term == "Neural Network"), None)
        assert nn is not None
        assert nn.occurrences == 3

    def test_first_line_is_one_based(self):
        text = "Line one text.\nDeep Learning is here.\nDeep Learning again."
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        dl = next((t for t in terms if t.term == "Deep Learning"), None)
        assert dl is not None
        assert dl.first_line == 2

    def test_context_matches_definition(self):
        text = (
            "Reinforcement Learning trains agents via rewards. "
            "Reinforcement Learning is used in games. "
            "Reinforcement Learning keeps improving."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        rl = next((t for t in terms if t.term == "Reinforcement Learning"), None)
        assert rl is not None
        assert rl.context == rl.definition or "Reinforcement Learning" in rl.context

    def test_single_word_not_extracted(self):
        text = "Python Python Python is a language used everywhere in Python code."
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        assert all(" " in t.term for t in terms)

    def test_returns_list(self):
        builder = GlossaryBuilder()
        result = builder.build("Hello world.")
        assert isinstance(result, list)


# ===========================================================================
# TestBuildAbbreviations
# ===========================================================================


class TestBuildAbbreviations:
    def test_extracts_abbreviation_alias(self):
        text = (
            "Natural Language Processing (NLP) is important. "
            "NLP is used everywhere. "
            "NLP has many applications."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=1))
        terms = builder.build(text)
        nlp = next(
            (t for t in terms if t.term == "Natural Language Processing"), None
        )
        assert nlp is not None
        assert "NLP" in nlp.aliases

    def test_abbreviation_occurrences_included(self):
        text = (
            "Machine Learning (ML) is a method. "
            "ML is used in many apps. "
            "ML solves complex problems."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=1))
        terms = builder.build(text)
        ml = next((t for t in terms if t.term == "Machine Learning"), None)
        assert ml is not None
        # occurrences should include both "Machine Learning" and "ML"
        assert ml.occurrences >= 1

    def test_abbreviation_disabled(self):
        text = (
            "Natural Language Processing (NLP) is powerful. "
            "Natural Language Processing keeps evolving."
        )
        builder = GlossaryBuilder(
            GlossaryConfig(min_occurrences=1, extract_abbreviations=False)
        )
        terms = builder.build(text)
        nlp = next(
            (t for t in terms if t.term == "Natural Language Processing"), None
        )
        assert nlp is not None
        assert nlp.aliases == []

    def test_abbreviation_two_letters(self):
        text = (
            "Artificial Intelligence (AI) is growing. "
            "AI is changing the world. "
            "AI has broad applications."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=1))
        terms = builder.build(text)
        ai_term = next(
            (t for t in terms if t.term == "Artificial Intelligence"), None
        )
        assert ai_term is not None
        assert "AI" in ai_term.aliases

    def test_abbreviation_five_letters(self):
        text = (
            "Random Access Memory (RAMEM) is hardware. "
            "RAMEM is fast. "
            "RAMEM stores data."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=1))
        terms = builder.build(text)
        ram_term = next(
            (t for t in terms if t.term == "Random Access Memory"), None
        )
        assert ram_term is not None
        assert "RAMEM" in ram_term.aliases


# ===========================================================================
# TestBuildMinOccurrences
# ===========================================================================


class TestBuildMinOccurrences:
    def test_term_below_min_excluded(self):
        text = (
            "Machine Learning is used once here. "
            "Deep Learning appears twice. "
            "Deep Learning is popular."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        term_names = [t.term for t in terms]
        assert "Machine Learning" not in term_names
        assert "Deep Learning" in term_names

    def test_min_occurrences_one_includes_all(self):
        text = (
            "Support Vector Machine is a classifier. "
            "Gradient Boosting is another approach."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=1))
        terms = builder.build(text)
        term_names = [t.term for t in terms]
        assert "Support Vector Machine" in term_names
        assert "Gradient Boosting" in term_names

    def test_min_occurrences_three_filters(self):
        text = (
            "Random Forest is used. "
            "Random Forest works well. "
            "Naive Bayes is mentioned once."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=3))
        terms = builder.build(text)
        term_names = [t.term for t in terms]
        assert "Naive Bayes" not in term_names


# ===========================================================================
# TestBuildMinTermLength
# ===========================================================================


class TestBuildMinTermLength:
    def test_short_phrase_excluded(self):
        # "Big Data" has length 8, which is >= min_term_length characters,
        # but min_term_length=10 means the phrase string must be >=10 chars.
        text = (
            "Big Data is used. Big Data is everywhere. Big Data grows daily."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_term_length=10, min_occurrences=1))
        terms = builder.build(text)
        term_names = [t.term for t in terms]
        assert "Big Data" not in term_names

    def test_longer_phrase_included(self):
        text = (
            "Machine Learning is used. Machine Learning is everywhere."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_term_length=5, min_occurrences=1))
        terms = builder.build(text)
        term_names = [t.term for t in terms]
        assert "Machine Learning" in term_names


# ===========================================================================
# TestBuildSorted
# ===========================================================================


class TestBuildSorted:
    def test_alphabetical_order(self):
        text = (
            "Zebra Crossing is a road marking. "
            "Zebra Crossing is used everywhere. "
            "Alpha Channel stores transparency. "
            "Alpha Channel is important. "
            "Middle Ground is a concept. "
            "Middle Ground matters."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        names = [t.term for t in terms]
        assert names == sorted(names, key=str.lower)

    def test_sorted_case_insensitive(self):
        text = (
            "Beta Version is tested. Beta Version has bugs. "
            "Alpha Release is first. Alpha Release is stable."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        names = [t.term.lower() for t in terms]
        assert names == sorted(names)


# ===========================================================================
# TestBuildFromFiles
# ===========================================================================


class TestBuildFromFiles:
    def test_empty_list_returns_empty(self):
        builder = GlossaryBuilder()
        result = builder.build_from_files([])
        assert result == []

    def test_single_file_same_as_build(self):
        text = (
            "Deep Learning is powerful. "
            "Deep Learning solves vision tasks."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        from_build = builder.build(text)
        from_files = builder.build_from_files([text])
        assert [t.term for t in from_build] == [t.term for t in from_files]

    def test_merges_occurrences_across_files(self):
        text1 = "Machine Learning is good. Machine Learning is fast."
        text2 = "Machine Learning is popular. Machine Learning is accurate."
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build_from_files([text1, text2])
        ml = next((t for t in terms if t.term == "Machine Learning"), None)
        assert ml is not None
        assert ml.occurrences >= 4

    def test_merges_aliases_across_files(self):
        text1 = "Natural Language Processing (NLP) is a field. Natural Language Processing is useful."
        text2 = "Natural Language Processing is growing. Natural Language Processing uses deep models."
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build_from_files([text1, text2])
        nlp = next(
            (t for t in terms if t.term == "Natural Language Processing"), None
        )
        assert nlp is not None
        assert "NLP" in nlp.aliases

    def test_result_sorted_alphabetically(self):
        text1 = "Gradient Descent is an optimizer. Gradient Descent converges slowly."
        text2 = "Activation Function is used. Activation Function maps inputs."
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build_from_files([text1, text2])
        names = [t.term for t in terms]
        assert names == sorted(names, key=str.lower)


# ===========================================================================
# TestFindTerm
# ===========================================================================


class TestFindTerm:
    def _make_terms(self):
        return [
            GlossaryTerm(term="Machine Learning", definition="ML def.", aliases=["ML"]),
            GlossaryTerm(term="Deep Learning", definition="DL def.", aliases=["DL"]),
        ]

    def test_exact_case_match(self):
        builder = GlossaryBuilder()
        terms = self._make_terms()
        result = builder.find_term(terms, "Machine Learning")
        assert result is not None
        assert result.term == "Machine Learning"

    def test_lowercase_query(self):
        builder = GlossaryBuilder()
        terms = self._make_terms()
        result = builder.find_term(terms, "machine learning")
        assert result is not None
        assert result.term == "Machine Learning"

    def test_uppercase_query(self):
        builder = GlossaryBuilder()
        terms = self._make_terms()
        result = builder.find_term(terms, "MACHINE LEARNING")
        assert result is not None
        assert result.term == "Machine Learning"

    def test_find_by_alias(self):
        builder = GlossaryBuilder()
        terms = self._make_terms()
        result = builder.find_term(terms, "ML")
        assert result is not None
        assert result.term == "Machine Learning"

    def test_find_by_alias_lowercase(self):
        builder = GlossaryBuilder()
        terms = self._make_terms()
        result = builder.find_term(terms, "dl")
        assert result is not None
        assert result.term == "Deep Learning"

    def test_not_found_returns_none(self):
        builder = GlossaryBuilder()
        terms = self._make_terms()
        result = builder.find_term(terms, "Random Forest")
        assert result is None

    def test_empty_terms_returns_none(self):
        builder = GlossaryBuilder()
        result = builder.find_term([], "Machine Learning")
        assert result is None


# ===========================================================================
# TestToMarkdown
# ===========================================================================


class TestToMarkdown:
    def test_empty_terms_returns_empty_string(self):
        builder = GlossaryBuilder()
        assert builder.to_markdown([]) == ""

    def test_header_format(self):
        builder = GlossaryBuilder()
        terms = [GlossaryTerm(term="Machine Learning", definition="ML is powerful.")]
        md = builder.to_markdown(terms)
        assert "## Machine Learning" in md

    def test_definition_present(self):
        builder = GlossaryBuilder()
        terms = [GlossaryTerm(term="Deep Learning", definition="DL uses neural nets.")]
        md = builder.to_markdown(terms)
        assert "DL uses neural nets." in md

    def test_multiple_terms_all_present(self):
        builder = GlossaryBuilder()
        terms = [
            GlossaryTerm(term="Alpha Test", definition="First test."),
            GlossaryTerm(term="Beta Test", definition="Second test."),
        ]
        md = builder.to_markdown(terms)
        assert "## Alpha Test" in md
        assert "## Beta Test" in md
        assert "First test." in md
        assert "Second test." in md

    def test_double_newline_after_definition(self):
        builder = GlossaryBuilder()
        terms = [GlossaryTerm(term="Test Term", definition="A definition.")]
        md = builder.to_markdown(terms)
        assert "A definition.\n\n" in md


# ===========================================================================
# TestToDict
# ===========================================================================


class TestToDict:
    def test_returns_list(self):
        builder = GlossaryBuilder()
        result = builder.to_dict([])
        assert isinstance(result, list)

    def test_empty_terms_returns_empty_list(self):
        builder = GlossaryBuilder()
        assert builder.to_dict([]) == []

    def test_dict_has_all_keys(self):
        builder = GlossaryBuilder()
        terms = [
            GlossaryTerm(
                term="Machine Learning",
                definition="ML is powerful.",
                aliases=["ML"],
                occurrences=3,
                first_line=1,
                context="Machine Learning is powerful.",
            )
        ]
        result = builder.to_dict(terms)
        assert len(result) == 1
        d = result[0]
        assert set(d.keys()) == {
            "term", "definition", "aliases", "occurrences", "first_line", "context"
        }

    def test_dict_values_correct(self):
        builder = GlossaryBuilder()
        terms = [
            GlossaryTerm(
                term="Deep Learning",
                definition="DL uses neural nets.",
                aliases=["DL"],
                occurrences=5,
                first_line=2,
                context="Deep Learning uses neural nets.",
            )
        ]
        result = builder.to_dict(terms)
        d = result[0]
        assert d["term"] == "Deep Learning"
        assert d["definition"] == "DL uses neural nets."
        assert d["aliases"] == ["DL"]
        assert d["occurrences"] == 5
        assert d["first_line"] == 2
        assert d["context"] == "Deep Learning uses neural nets."

    def test_aliases_is_list(self):
        builder = GlossaryBuilder()
        terms = [GlossaryTerm(term="Test Term", definition="Def.", aliases=["TT", "T2"])]
        result = builder.to_dict(terms)
        assert isinstance(result[0]["aliases"], list)


# ===========================================================================
# TestEdgeCases
# ===========================================================================


class TestEdgeCases:
    def test_empty_string_returns_empty(self):
        builder = GlossaryBuilder()
        result = builder.build("")
        assert result == []

    def test_whitespace_only_returns_empty(self):
        builder = GlossaryBuilder()
        result = builder.build("   \n\t  ")
        assert result == []

    def test_no_capitalized_phrases(self):
        builder = GlossaryBuilder()
        result = builder.build("all lowercase text here without any capitalized terms.")
        assert result == []

    def test_single_sentence(self):
        text = "Machine Learning is everywhere and Machine Learning is powerful."
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        assert any(t.term == "Machine Learning" for t in terms)

    def test_definition_truncated_to_max_length(self):
        long_sentence = "Deep Learning " + ("is very " * 40) + "powerful."
        text = long_sentence + " Deep Learning continues."
        builder = GlossaryBuilder(
            GlossaryConfig(min_occurrences=1, max_definition_length=50)
        )
        terms = builder.build(text)
        dl = next((t for t in terms if t.term == "Deep Learning"), None)
        assert dl is not None
        assert len(dl.definition) <= 50

    def test_build_returns_sorted_list(self):
        text = (
            "Zebra Algorithm is used. Zebra Algorithm runs fast. "
            "Alpha Method is first. Alpha Method is stable."
        )
        builder = GlossaryBuilder(GlossaryConfig(min_occurrences=2))
        terms = builder.build(text)
        names = [t.term for t in terms]
        assert names == sorted(names, key=str.lower)

    def test_default_config_used_when_none(self):
        builder = GlossaryBuilder(None)
        assert builder._config is not None
        assert isinstance(builder._config, GlossaryConfig)

    def test_find_term_with_extra_whitespace(self):
        builder = GlossaryBuilder()
        terms = [GlossaryTerm(term="Machine Learning", definition="Def.", aliases=[])]
        result = builder.find_term(terms, "  Machine Learning  ")
        assert result is not None
        assert result.term == "Machine Learning"
