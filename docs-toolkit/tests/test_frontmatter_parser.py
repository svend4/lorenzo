"""Tests for docstoolkit.frontmatter_parser — ≥45 test cases."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from docstoolkit.frontmatter_parser import FrontmatterData, FrontmatterParser


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parser() -> FrontmatterParser:
    return FrontmatterParser()


# ---------------------------------------------------------------------------
# TestFrontmatterData
# ---------------------------------------------------------------------------

class TestFrontmatterData:
    def test_defaults(self):
        fd = FrontmatterData()
        assert fd.data == {}
        assert fd.content == ""
        assert fd.has_frontmatter is False
        assert fd.raw_frontmatter == ""

    def test_get_existing_key(self):
        fd = FrontmatterData(data={"title": "Hello"}, has_frontmatter=True)
        assert fd.get("title") == "Hello"

    def test_get_missing_key_returns_default(self):
        fd = FrontmatterData(data={})
        assert fd.get("missing") is None

    def test_get_missing_key_custom_default(self):
        fd = FrontmatterData(data={})
        assert fd.get("missing", 42) == 42

    def test_keys_returns_keys(self):
        fd = FrontmatterData(data={"a": 1, "b": 2})
        assert set(fd.keys()) == {"a", "b"}

    def test_keys_empty(self):
        fd = FrontmatterData(data={})
        assert list(fd.keys()) == []

    def test_has_frontmatter_field(self):
        fd = FrontmatterData(has_frontmatter=True)
        assert fd.has_frontmatter is True

    def test_raw_frontmatter_preserved(self):
        fd = FrontmatterData(raw_frontmatter="title: foo\nauthor: bar")
        assert "title" in fd.raw_frontmatter


# ---------------------------------------------------------------------------
# TestParserNoFrontmatter
# ---------------------------------------------------------------------------

class TestParserNoFrontmatter:
    def test_plain_text(self):
        p = parser()
        fd = p.parse("Just some plain text.")
        assert fd.has_frontmatter is False
        assert fd.content == "Just some plain text."
        assert fd.data == {}

    def test_empty_string(self):
        p = parser()
        fd = p.parse("")
        assert fd.has_frontmatter is False
        assert fd.content == ""

    def test_only_triple_dashes_not_frontmatter(self):
        p = parser()
        fd = p.parse("---\n")
        assert fd.has_frontmatter is False

    def test_frontmatter_not_at_start(self):
        p = parser()
        text = "Some intro\n---\ntitle: foo\n---\nbody"
        fd = p.parse(text)
        assert fd.has_frontmatter is False
        assert fd.content == text

    def test_markdown_with_hr(self):
        p = parser()
        text = "# Heading\n\n---\n\nParagraph"
        fd = p.parse(text)
        assert fd.has_frontmatter is False


# ---------------------------------------------------------------------------
# TestParserBasic
# ---------------------------------------------------------------------------

class TestParserBasic:
    def test_string_value(self):
        p = parser()
        fd = p.parse("---\ntitle: My Document\n---\n")
        assert fd.has_frontmatter is True
        assert fd.data["title"] == "My Document"

    def test_integer_value(self):
        p = parser()
        fd = p.parse("---\ncount: 42\n---\n")
        assert fd.data["count"] == 42
        assert isinstance(fd.data["count"], int)

    def test_negative_integer(self):
        p = parser()
        fd = p.parse("---\noffset: -5\n---\n")
        assert fd.data["offset"] == -5

    def test_float_value(self):
        p = parser()
        fd = p.parse("---\nrate: 3.14\n---\n")
        assert abs(fd.data["rate"] - 3.14) < 1e-9
        assert isinstance(fd.data["rate"], float)

    def test_bool_true(self):
        p = parser()
        fd = p.parse("---\npublished: true\n---\n")
        assert fd.data["published"] is True

    def test_bool_false(self):
        p = parser()
        fd = p.parse("---\ndraft: false\n---\n")
        assert fd.data["draft"] is False

    def test_null_value(self):
        p = parser()
        fd = p.parse("---\nauthor: null\n---\n")
        assert fd.data["author"] is None

    def test_tilde_null(self):
        p = parser()
        fd = p.parse("---\nauthor: ~\n---\n")
        assert fd.data["author"] is None

    def test_multiple_fields(self):
        p = parser()
        fd = p.parse("---\ntitle: Doc\nversion: 2\nactive: true\n---\n")
        assert fd.data["title"] == "Doc"
        assert fd.data["version"] == 2
        assert fd.data["active"] is True

    def test_raw_frontmatter_contains_content(self):
        p = parser()
        fd = p.parse("---\ntitle: Test\n---\n")
        assert fd.raw_frontmatter == "title: Test"


# ---------------------------------------------------------------------------
# TestParserQuotedStrings
# ---------------------------------------------------------------------------

class TestParserQuotedStrings:
    def test_double_quoted_string(self):
        p = parser()
        fd = p.parse('---\nver: "1.0"\n---\n')
        assert fd.data["ver"] == "1.0"

    def test_single_quoted_string(self):
        p = parser()
        fd = p.parse("---\nver: '2.5'\n---\n")
        assert fd.data["ver"] == "2.5"

    def test_quoted_string_with_colon(self):
        p = parser()
        fd = p.parse('---\ndesc: "key: value"\n---\n')
        assert fd.data["desc"] == "key: value"

    def test_quoted_number_stays_string(self):
        p = parser()
        fd = p.parse('---\nzip: "90210"\n---\n')
        assert fd.data["zip"] == "90210"
        assert isinstance(fd.data["zip"], str)

    def test_quoted_bool_stays_string(self):
        p = parser()
        fd = p.parse('---\nflag: "true"\n---\n')
        assert fd.data["flag"] == "true"
        assert isinstance(fd.data["flag"], str)


# ---------------------------------------------------------------------------
# TestParserLists
# ---------------------------------------------------------------------------

class TestParserLists:
    def test_block_list(self):
        p = parser()
        text = "---\ntags:\n  - python\n  - docs\n---\n"
        fd = p.parse(text)
        assert fd.data["tags"] == ["python", "docs"]

    def test_block_list_single_item(self):
        p = parser()
        text = "---\nroles:\n  - admin\n---\n"
        fd = p.parse(text)
        assert fd.data["roles"] == ["admin"]

    def test_inline_list(self):
        p = parser()
        fd = p.parse("---\ntags: [a, b, c]\n---\n")
        assert fd.data["tags"] == ["a", "b", "c"]

    def test_empty_block_list(self):
        p = parser()
        fd = p.parse("---\ntags:\n---\n")
        assert fd.data["tags"] == []

    def test_empty_inline_list(self):
        p = parser()
        fd = p.parse("---\ntags: []\n---\n")
        assert fd.data["tags"] == []

    def test_list_with_integers(self):
        p = parser()
        text = "---\nscores:\n  - 1\n  - 2\n  - 3\n---\n"
        fd = p.parse(text)
        assert fd.data["scores"] == [1, 2, 3]


# ---------------------------------------------------------------------------
# TestParserBodyPreserved
# ---------------------------------------------------------------------------

class TestParserBodyPreserved:
    def test_body_after_frontmatter(self):
        p = parser()
        text = "---\ntitle: T\n---\n# Heading\n\nParagraph."
        fd = p.parse(text)
        assert fd.content == "# Heading\n\nParagraph."

    def test_empty_body(self):
        p = parser()
        text = "---\ntitle: T\n---\n"
        fd = p.parse(text)
        assert fd.content == ""

    def test_body_with_dashes_not_stripped(self):
        p = parser()
        text = "---\ntitle: T\n---\nBody text\n---\nMore"
        fd = p.parse(text)
        assert "---\nMore" in fd.content

    def test_body_newlines_preserved(self):
        p = parser()
        text = "---\ntitle: T\n---\nLine1\nLine2\nLine3"
        fd = p.parse(text)
        assert fd.content == "Line1\nLine2\nLine3"


# ---------------------------------------------------------------------------
# TestDump
# ---------------------------------------------------------------------------

class TestDump:
    def test_dump_simple(self):
        p = parser()
        result = p.dump({"title": "Hello"})
        assert result.startswith("---\n")
        assert "title: Hello" in result

    def test_dump_bool_true(self):
        p = parser()
        result = p.dump({"published": True})
        assert "published: true" in result

    def test_dump_bool_false(self):
        p = parser()
        result = p.dump({"draft": False})
        assert "draft: false" in result

    def test_dump_null(self):
        p = parser()
        result = p.dump({"author": None})
        assert "author: null" in result

    def test_dump_integer(self):
        p = parser()
        result = p.dump({"count": 7})
        assert "count: 7" in result

    def test_dump_list(self):
        p = parser()
        result = p.dump({"tags": ["a", "b"]})
        assert "tags:" in result
        assert "  - a" in result
        assert "  - b" in result

    def test_dump_with_content(self):
        p = parser()
        result = p.dump({"title": "T"}, content="Body here")
        assert result.endswith("Body here")
        assert "---\ntitle: T\n---\nBody here" == result

    def test_round_trip(self):
        p = parser()
        original = "---\ntitle: Round Trip\ncount: 3\nactive: true\n---\nBody text"
        fd = p.parse(original)
        dumped = p.dump(fd.data, fd.content)
        fd2 = p.parse(dumped)
        assert fd2.data == fd.data
        assert fd2.content == fd.content

    def test_dump_empty_list(self):
        p = parser()
        result = p.dump({"tags": []})
        assert "tags:" in result


# ---------------------------------------------------------------------------
# TestUpdate
# ---------------------------------------------------------------------------

class TestUpdate:
    def test_update_existing_key(self):
        p = parser()
        text = "---\ntitle: Old\n---\nBody"
        result = p.update(text, {"title": "New"})
        fd = p.parse(result)
        assert fd.data["title"] == "New"

    def test_update_adds_new_key(self):
        p = parser()
        text = "---\ntitle: T\n---\nBody"
        result = p.update(text, {"author": "Alice"})
        fd = p.parse(result)
        assert fd.data["author"] == "Alice"
        assert fd.data["title"] == "T"

    def test_update_preserves_body(self):
        p = parser()
        text = "---\ntitle: T\n---\nBody text"
        result = p.update(text, {"version": 2})
        fd = p.parse(result)
        assert fd.content == "Body text"

    def test_update_no_frontmatter_creates_one(self):
        p = parser()
        text = "Just a body."
        result = p.update(text, {"title": "New"})
        fd = p.parse(result)
        assert fd.has_frontmatter is True
        assert fd.data["title"] == "New"

    def test_update_multiple_keys(self):
        p = parser()
        text = "---\na: 1\n---\n"
        result = p.update(text, {"b": 2, "c": 3})
        fd = p.parse(result)
        assert fd.data["a"] == 1
        assert fd.data["b"] == 2
        assert fd.data["c"] == 3


# ---------------------------------------------------------------------------
# TestRemove
# ---------------------------------------------------------------------------

class TestRemove:
    def test_remove_frontmatter(self):
        p = parser()
        text = "---\ntitle: T\n---\nBody"
        assert p.remove(text) == "Body"

    def test_remove_no_frontmatter(self):
        p = parser()
        text = "Just body"
        assert p.remove(text) == "Just body"

    def test_remove_empty_body(self):
        p = parser()
        text = "---\ntitle: T\n---\n"
        assert p.remove(text) == ""

    def test_remove_preserves_multiline_body(self):
        p = parser()
        text = "---\ntitle: T\n---\nLine1\nLine2"
        assert p.remove(text) == "Line1\nLine2"


# ---------------------------------------------------------------------------
# TestHasFrontmatter
# ---------------------------------------------------------------------------

class TestHasFrontmatter:
    def test_true_for_valid_frontmatter(self):
        p = parser()
        assert p.has_frontmatter("---\ntitle: T\n---\n") is True

    def test_false_for_plain_text(self):
        p = parser()
        assert p.has_frontmatter("Just text") is False

    def test_false_for_empty_string(self):
        p = parser()
        assert p.has_frontmatter("") is False

    def test_false_when_frontmatter_not_at_start(self):
        p = parser()
        assert p.has_frontmatter("text\n---\ntitle: T\n---\n") is False


# ---------------------------------------------------------------------------
# TestExtractField
# ---------------------------------------------------------------------------

class TestExtractField:
    def test_extract_existing_field(self):
        p = parser()
        text = "---\nauthor: Bob\n---\nContent"
        assert p.extract_field(text, "author") == "Bob"

    def test_extract_missing_field_returns_none(self):
        p = parser()
        text = "---\ntitle: T\n---\n"
        assert p.extract_field(text, "missing") is None

    def test_extract_missing_field_custom_default(self):
        p = parser()
        text = "---\ntitle: T\n---\n"
        assert p.extract_field(text, "missing", "default_val") == "default_val"

    def test_extract_from_no_frontmatter(self):
        p = parser()
        assert p.extract_field("plain text", "title") is None

    def test_extract_int_field(self):
        p = parser()
        text = "---\nversion: 3\n---\n"
        assert p.extract_field(text, "version") == 3


# ---------------------------------------------------------------------------
# TestEdgeCases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_frontmatter_block(self):
        p = parser()
        fd = p.parse("---\n\n---\n")
        assert fd.has_frontmatter is True
        assert fd.data == {}

    def test_frontmatter_with_comments(self):
        p = parser()
        text = "---\n# This is a comment\ntitle: T\n---\n"
        fd = p.parse(text)
        assert fd.data.get("title") == "T"

    def test_frontmatter_trailing_spaces_on_delimiter(self):
        p = parser()
        text = "---  \ntitle: T\n---  \nBody"
        fd = p.parse(text)
        assert fd.has_frontmatter is True
        assert fd.data["title"] == "T"

    def test_body_with_only_newlines(self):
        p = parser()
        text = "---\ntitle: T\n---\n\n\n"
        fd = p.parse(text)
        assert fd.has_frontmatter is True
        assert fd.content == "\n\n"

    def test_dump_no_content_ends_with_newline(self):
        p = parser()
        result = p.dump({"k": "v"})
        assert result.endswith("\n")

    def test_bool_case_insensitive_true(self):
        p = parser()
        fd = p.parse("---\nflag: True\n---\n")
        assert fd.data["flag"] is True

    def test_bool_case_insensitive_false(self):
        p = parser()
        fd = p.parse("---\nflag: FALSE\n---\n")
        assert fd.data["flag"] is False

    def test_negative_float(self):
        p = parser()
        fd = p.parse("---\ntemp: -1.5\n---\n")
        assert abs(fd.data["temp"] - (-1.5)) < 1e-9

    def test_hyphenated_key(self):
        p = parser()
        fd = p.parse("---\nbuild-id: 99\n---\n")
        assert fd.data["build-id"] == 99
