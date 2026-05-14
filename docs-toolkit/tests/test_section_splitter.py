"""Tests for docstoolkit.section_splitter."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.section_splitter import Section, SectionSplitter, SplitConfig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _splitter(**kwargs) -> SectionSplitter:
    return SectionSplitter(SplitConfig(**kwargs))


# ---------------------------------------------------------------------------
# TestSectionDataclass
# ---------------------------------------------------------------------------

class TestSectionDataclass:
    def test_heading_field(self):
        s = Section(heading="My Heading", level=1, content="body", line_start=1, line_end=2)
        assert s.heading == "My Heading"

    def test_level_field(self):
        s = Section(heading="", level=2, content="body", line_start=1, line_end=2)
        assert s.level == 2

    def test_content_field(self):
        s = Section(heading="H", level=1, content="hello world", line_start=1, line_end=2)
        assert s.content == "hello world"

    def test_word_count_basic(self):
        s = Section(heading="H", level=1, content="one two three", line_start=1, line_end=2)
        assert s.word_count == 3

    def test_word_count_empty_content(self):
        s = Section(heading="H", level=1, content="", line_start=1, line_end=2)
        assert s.word_count == 0

    def test_word_count_whitespace_only(self):
        s = Section(heading="H", level=1, content="   \n  \t  ", line_start=1, line_end=2)
        assert s.word_count == 0

    def test_is_empty_true(self):
        s = Section(heading="H", level=1, content="", line_start=1, line_end=1)
        assert s.is_empty is True

    def test_is_empty_whitespace(self):
        s = Section(heading="H", level=1, content="  \n  ", line_start=1, line_end=2)
        assert s.is_empty is True

    def test_is_empty_false(self):
        s = Section(heading="H", level=1, content="hello", line_start=1, line_end=2)
        assert s.is_empty is False

    def test_subsections_default_empty(self):
        s = Section(heading="H", level=1, content="body", line_start=1, line_end=2)
        assert s.subsections == []

    def test_subsections_mutable(self):
        child = Section(heading="Child", level=2, content="c", line_start=3, line_end=4)
        parent = Section(heading="Parent", level=1, content="p", line_start=1, line_end=4, subsections=[child])
        assert len(parent.subsections) == 1
        assert parent.subsections[0].heading == "Child"


# ---------------------------------------------------------------------------
# TestSplitConfig
# ---------------------------------------------------------------------------

class TestSplitConfig:
    def test_defaults(self):
        cfg = SplitConfig()
        assert cfg.max_level == 6
        assert cfg.include_preamble is True
        assert cfg.min_words == 0

    def test_custom_max_level(self):
        cfg = SplitConfig(max_level=2)
        assert cfg.max_level == 2

    def test_custom_include_preamble(self):
        cfg = SplitConfig(include_preamble=False)
        assert cfg.include_preamble is False

    def test_custom_min_words(self):
        cfg = SplitConfig(min_words=10)
        assert cfg.min_words == 10


# ---------------------------------------------------------------------------
# TestSplitBasic
# ---------------------------------------------------------------------------

class TestSplitBasic:
    def test_single_h1(self):
        text = "# Hello\nsome body text"
        sp = SectionSplitter()
        sections = sp.split(text)
        # preamble (empty) + h1
        headings = [s.heading for s in sections]
        assert "Hello" in headings

    def test_preamble_included(self):
        text = "intro line\n\n# Section One\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        assert sections[0].level == 0
        assert sections[0].heading == ""
        assert "intro line" in sections[0].content

    def test_preamble_level_zero(self):
        text = "preamble\n# H1\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        assert sections[0].level == 0

    def test_section_heading_text(self):
        text = "# Alpha\nbody\n## Beta\nbody2"
        sp = SectionSplitter()
        sections = sp.split(text)
        headings = [s.heading for s in sections]
        assert "Alpha" in headings
        assert "Beta" in headings

    def test_section_content_correct(self):
        text = "# First\nfirst body\n# Second\nsecond body"
        sp = SectionSplitter()
        sections = sp.split(text)
        first = next(s for s in sections if s.heading == "First")
        assert "first body" in first.content

    def test_section_count(self):
        text = "preamble\n# A\ntext\n# B\ntext"
        sp = SectionSplitter()
        sections = sp.split(text)
        # preamble + A + B = 3
        assert len(sections) == 3

    def test_multiple_levels(self):
        text = "# H1\n## H2\n### H3\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        levels = [s.level for s in sections]
        assert 1 in levels
        assert 2 in levels
        assert 3 in levels


# ---------------------------------------------------------------------------
# TestSplitNoPreamble
# ---------------------------------------------------------------------------

class TestSplitNoPreamble:
    def test_preamble_excluded(self):
        text = "intro\n# Section\nbody"
        sp = _splitter(include_preamble=False)
        sections = sp.split(text)
        assert all(s.level != 0 for s in sections)

    def test_no_preamble_content_in_first_heading(self):
        text = "# First\nbody"
        sp = _splitter(include_preamble=False)
        sections = sp.split(text)
        assert sections[0].heading == "First"

    def test_no_preamble_count(self):
        text = "ignored\n# A\ntext\n# B\ntext"
        sp = _splitter(include_preamble=False)
        sections = sp.split(text)
        assert len(sections) == 2


# ---------------------------------------------------------------------------
# TestSplitMaxLevel
# ---------------------------------------------------------------------------

class TestSplitMaxLevel:
    def test_max_level_2_skips_h3(self):
        text = "# H1\n## H2\n### H3 ignored\nbody"
        sp = _splitter(max_level=2)
        sections = sp.split(text)
        levels = [s.level for s in sections]
        assert 3 not in levels

    def test_max_level_1_only_h1(self):
        text = "# H1\n## H2 goes to body\nbody"
        sp = _splitter(max_level=1)
        sections = sp.split(text)
        levels = [s.level for s in sections if s.level > 0]
        assert all(l == 1 for l in levels)

    def test_max_level_2_h2_included(self):
        text = "# H1\n## H2\nbody"
        sp = _splitter(max_level=2)
        sections = sp.split(text)
        levels = [s.level for s in sections]
        assert 2 in levels

    def test_max_level_content_includes_skipped_headings(self):
        text = "# H1\n### H3 skipped\nbody"
        sp = _splitter(max_level=1)
        sections = sp.split(text)
        h1 = next(s for s in sections if s.level == 1)
        assert "H3 skipped" in h1.content


# ---------------------------------------------------------------------------
# TestSplitMinWords
# ---------------------------------------------------------------------------

class TestSplitMinWords:
    def test_min_words_skips_short_section(self):
        text = "# Short\nhi\n# Long enough section here\nthis section has many words in the body"
        sp = _splitter(min_words=5)
        sections = sp.split(text)
        headings = [s.heading for s in sections]
        assert "Short" not in headings

    def test_min_words_keeps_long_section(self):
        text = "# Long enough section here\nthis section has enough words in the body text"
        sp = _splitter(min_words=5)
        sections = sp.split(text)
        assert any(s.heading == "Long enough section here" for s in sections)

    def test_min_words_zero_keeps_all(self):
        text = "# A\nhi\n# B\nbye"
        sp = _splitter(min_words=0)
        sections = sp.split(text)
        headings = [s.heading for s in sections if s.level > 0]
        assert "A" in headings
        assert "B" in headings


# ---------------------------------------------------------------------------
# TestSplitByLevel
# ---------------------------------------------------------------------------

class TestSplitByLevel:
    def test_split_by_level_2_only(self):
        text = "# H1 ignored\n## Section A\nbody\n## Section B\nbody2"
        sp = SectionSplitter()
        sections = sp.split_by_level(text, level=2)
        levels = [s.level for s in sections if s.level > 0]
        assert all(l == 2 for l in levels)

    def test_split_by_level_2_headings(self):
        text = "# H1\n## Alpha\ncontent\n## Beta\ncontent"
        sp = SectionSplitter()
        sections = sp.split_by_level(text, level=2)
        headings = [s.heading for s in sections if s.level > 0]
        assert "Alpha" in headings
        assert "Beta" in headings

    def test_split_by_level_h1_not_in_result(self):
        text = "# H1\n## Alpha\ncontent"
        sp = SectionSplitter()
        sections = sp.split_by_level(text, level=2)
        headings = [s.heading for s in sections if s.level > 0]
        assert "H1" not in headings

    def test_split_by_level_h3_in_content(self):
        text = "## Top\n### Sub\ncontent"
        sp = SectionSplitter()
        sections = sp.split_by_level(text, level=2)
        assert len([s for s in sections if s.level > 0]) == 1
        body = sections[-1].content if sections[-1].level > 0 else sections[0].content
        assert "Sub" in body

    def test_split_by_level_preamble_included(self):
        text = "preamble text here\n## Section\nbody"
        sp = SectionSplitter()
        sections = sp.split_by_level(text, level=2)
        # preamble should be first
        assert sections[0].level == 0


# ---------------------------------------------------------------------------
# TestSplitHierarchical
# ---------------------------------------------------------------------------

class TestSplitHierarchical:
    def test_h2_is_child_of_h1(self):
        text = "# Parent\n## Child\nbody"
        sp = SectionSplitter()
        result = sp.split_hierarchical(text)
        h1_sections = [s for s in result if s.level == 1]
        assert len(h1_sections) == 1
        assert len(h1_sections[0].subsections) == 1
        assert h1_sections[0].subsections[0].heading == "Child"

    def test_h3_is_child_of_h2(self):
        text = "# H1\n## H2\n### H3\nbody"
        sp = SectionSplitter()
        result = sp.split_hierarchical(text)
        h1 = next(s for s in result if s.level == 1)
        h2 = h1.subsections[0]
        assert h2.level == 2
        assert h2.subsections[0].level == 3

    def test_sibling_h2_not_nested(self):
        text = "# H1\n## A\nbody\n## B\nbody"
        sp = SectionSplitter()
        result = sp.split_hierarchical(text)
        h1 = next(s for s in result if s.level == 1)
        assert len(h1.subsections) == 2

    def test_top_level_only_in_result(self):
        text = "# H1\n## H2\n### H3"
        sp = SectionSplitter()
        result = sp.split_hierarchical(text)
        # Only h1 (and maybe preamble) at top level
        top_levels = [s for s in result if s.level > 0]
        assert len(top_levels) == 1


# ---------------------------------------------------------------------------
# TestSplitHierarchicalSubsections
# ---------------------------------------------------------------------------

class TestSplitHierarchicalSubsections:
    def test_subsections_populated(self):
        text = "# A\n## A1\n## A2\nbody"
        sp = SectionSplitter()
        result = sp.split_hierarchical(text)
        h1 = next(s for s in result if s.level == 1)
        assert len(h1.subsections) == 2

    def test_deep_nesting(self):
        text = "# L1\n## L2\n### L3\n#### L4\nbody"
        sp = SectionSplitter()
        result = sp.split_hierarchical(text)
        l1 = next(s for s in result if s.level == 1)
        l2 = l1.subsections[0]
        l3 = l2.subsections[0]
        assert l3.level == 3
        assert l3.subsections[0].level == 4

    def test_preamble_not_in_subsections(self):
        text = "pre\n# H1\n## H2\nbody"
        sp = SectionSplitter()
        result = sp.split_hierarchical(text)
        preamble = next((s for s in result if s.level == 0), None)
        assert preamble is not None
        assert preamble.subsections == []

    def test_multiple_h1_each_with_own_children(self):
        text = "# A\n## A1\n# B\n## B1\nbody"
        sp = SectionSplitter()
        result = sp.split_hierarchical(text)
        h1s = [s for s in result if s.level == 1]
        assert len(h1s) == 2
        assert h1s[0].subsections[0].heading == "A1"
        assert h1s[1].subsections[0].heading == "B1"


# ---------------------------------------------------------------------------
# TestFlatten
# ---------------------------------------------------------------------------

class TestFlatten:
    def test_flatten_nested(self):
        text = "# H1\n## H2\n### H3\nbody"
        sp = SectionSplitter()
        hierarchical = sp.split_hierarchical(text)
        flat = sp.flatten(hierarchical)
        levels = [s.level for s in flat if s.level > 0]
        assert levels == [1, 2, 3]

    def test_flatten_depth_first(self):
        text = "# A\n## A1\n## A2\n# B\nbody"
        sp = SectionSplitter()
        hierarchical = sp.split_hierarchical(text)
        flat = sp.flatten(hierarchical)
        headings = [s.heading for s in flat if s.level > 0]
        assert headings == ["A", "A1", "A2", "B"]

    def test_flatten_no_subsections(self):
        text = "# A\n# B\n# C"
        sp = SectionSplitter()
        hierarchical = sp.split_hierarchical(text)
        flat = sp.flatten(hierarchical)
        headings = [s.heading for s in flat if s.level > 0]
        assert headings == ["A", "B", "C"]

    def test_flatten_returns_list(self):
        text = "# H1\nbody"
        sp = SectionSplitter()
        hierarchical = sp.split_hierarchical(text)
        flat = sp.flatten(hierarchical)
        assert isinstance(flat, list)


# ---------------------------------------------------------------------------
# TestFindSection
# ---------------------------------------------------------------------------

class TestFindSection:
    def test_find_existing(self):
        text = "# Alpha\nbody\n# Beta\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        result = sp.find_section(sections, "Alpha")
        assert result is not None
        assert result.heading == "Alpha"

    def test_find_case_insensitive(self):
        text = "# Alpha\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        result = sp.find_section(sections, "alpha")
        assert result is not None

    def test_find_case_insensitive_upper(self):
        text = "# alpha\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        result = sp.find_section(sections, "ALPHA")
        assert result is not None

    def test_find_not_existing_returns_none(self):
        text = "# Alpha\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        result = sp.find_section(sections, "Nonexistent")
        assert result is None

    def test_find_nested(self):
        text = "# Parent\n## Nested Child\nbody"
        sp = SectionSplitter()
        hierarchical = sp.split_hierarchical(text)
        result = sp.find_section(hierarchical, "Nested Child")
        assert result is not None
        assert result.level == 2

    def test_find_empty_sections_list(self):
        sp = SectionSplitter()
        result = sp.find_section([], "any")
        assert result is None


# ---------------------------------------------------------------------------
# TestToDict
# ---------------------------------------------------------------------------

class TestToDict:
    def test_to_dict_keys(self):
        s = Section(heading="H", level=1, content="body text", line_start=1, line_end=2)
        sp = SectionSplitter()
        d = sp.to_dict(s)
        assert set(d.keys()) == {"heading", "level", "content", "word_count"}

    def test_to_dict_values(self):
        s = Section(heading="My Title", level=2, content="one two three", line_start=5, line_end=10)
        sp = SectionSplitter()
        d = sp.to_dict(s)
        assert d["heading"] == "My Title"
        assert d["level"] == 2
        assert d["content"] == "one two three"
        assert d["word_count"] == 3

    def test_to_dict_no_subsections_key(self):
        s = Section(heading="H", level=1, content="body", line_start=1, line_end=2)
        sp = SectionSplitter()
        d = sp.to_dict(s)
        assert "subsections" not in d

    def test_to_dict_serializable(self):
        import json
        s = Section(heading="H", level=1, content="body text here", line_start=1, line_end=3)
        sp = SectionSplitter()
        d = sp.to_dict(s)
        # Should not raise
        json.dumps(d)


# ---------------------------------------------------------------------------
# TestLineNumbers
# ---------------------------------------------------------------------------

class TestLineNumbers:
    def test_preamble_line_start_is_1(self):
        text = "pre\n# H1\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        preamble = sections[0]
        assert preamble.line_start == 1

    def test_h1_line_start(self):
        text = "pre\n# H1\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        h1 = next(s for s in sections if s.level == 1)
        assert h1.line_start == 2

    def test_h1_line_end(self):
        text = "# H1\nline1\nline2"
        sp = SectionSplitter()
        sections = sp.split(text)
        h1 = next(s for s in sections if s.level == 1)
        assert h1.line_end == 3

    def test_preamble_line_end(self):
        text = "line1\nline2\n# H1\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        preamble = sections[0]
        # preamble ends just before the heading on line 3
        assert preamble.line_end == 2

    def test_multiple_sections_line_numbers(self):
        text = "# A\nbody A\n# B\nbody B"
        sp = SectionSplitter()
        sections = sp.split(text)
        a = next(s for s in sections if s.heading == "A")
        b = next(s for s in sections if s.heading == "B")
        assert a.line_start == 1
        assert b.line_start == 3

    def test_last_section_line_end(self):
        text = "# First\nbody\n# Last\nfinal line"
        sp = SectionSplitter()
        sections = sp.split(text)
        last = next(s for s in sections if s.heading == "Last")
        assert last.line_end == 4


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_text(self):
        sp = SectionSplitter()
        sections = sp.split("")
        # Either empty list or a single empty preamble
        for s in sections:
            assert s.is_empty

    def test_no_headings(self):
        text = "just some plain text\nno headings here"
        sp = SectionSplitter()
        sections = sp.split(text)
        assert len(sections) == 1
        assert sections[0].level == 0
        assert "plain text" in sections[0].content

    def test_no_headings_no_preamble(self):
        text = "just plain text"
        sp = _splitter(include_preamble=False)
        sections = sp.split(text)
        assert sections == []

    def test_only_headings_no_body(self):
        text = "# H1\n## H2\n### H3"
        sp = SectionSplitter()
        sections = sp.split(text)
        assert all(s.is_empty for s in sections if s.level > 0)

    def test_heading_with_trailing_spaces(self):
        text = "# Heading with spaces   \nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        h = next(s for s in sections if s.level > 0)
        # heading text should be stripped
        assert h.heading == "Heading with spaces"

    def test_h6_heading(self):
        text = "###### Deep heading\nbody"
        sp = SectionSplitter()
        sections = sp.split(text)
        h = next(s for s in sections if s.level > 0)
        assert h.level == 6

    def test_hierarchical_empty_text(self):
        sp = SectionSplitter()
        result = sp.split_hierarchical("")
        assert isinstance(result, list)

    def test_split_by_level_no_matching_headings(self):
        text = "# H1\nbody"
        sp = SectionSplitter()
        sections = sp.split_by_level(text, level=2)
        # Only preamble (containing the H1 line as body)
        heading_sections = [s for s in sections if s.level == 2]
        assert heading_sections == []
