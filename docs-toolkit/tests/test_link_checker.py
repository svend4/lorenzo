"""Tests for the link_checker module — ≥45 tests covering all spec requirements."""
from __future__ import annotations

import dataclasses

import pytest

from docstoolkit.link_checker import (
    CheckResult,
    Link,
    LinkChecker,
    LinkExtractor,
    LinkStatus,
    LinkType,
    LinkValidator,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_link(
    url: str = "http://example.com",
    text: str = "label",
    line_num: int = 1,
    link_type: LinkType = LinkType.EXTERNAL,
    status: LinkStatus = LinkStatus.UNKNOWN,
) -> Link:
    return Link(url=url, text=text, line_num=line_num,
                link_type=link_type, status=status)


def _result_with(*links: Link) -> CheckResult:
    return CheckResult(links=list(links))


# ===========================================================================
# 1. TestLinkType
# ===========================================================================

class TestLinkType:
    def test_members_exist(self):
        for name in ("INTERNAL", "EXTERNAL", "ANCHOR", "IMAGE", "FOOTNOTE"):
            assert hasattr(LinkType, name)

    def test_values_are_strings(self):
        for member in LinkType:
            assert isinstance(member.value, str)

    def test_distinct_values(self):
        values = [m.value for m in LinkType]
        assert len(values) == len(set(values))

    def test_is_enum(self):
        from enum import Enum
        assert issubclass(LinkType, Enum)


# ===========================================================================
# 2. TestLinkStatus
# ===========================================================================

class TestLinkStatus:
    def test_members_exist(self):
        for name in ("UNKNOWN", "VALID", "BROKEN", "SKIPPED"):
            assert hasattr(LinkStatus, name)

    def test_values_are_strings(self):
        for member in LinkStatus:
            assert isinstance(member.value, str)

    def test_distinct_values(self):
        values = [m.value for m in LinkStatus]
        assert len(values) == len(set(values))

    def test_is_enum(self):
        from enum import Enum
        assert issubclass(LinkStatus, Enum)


# ===========================================================================
# 3. TestLinkDataclass
# ===========================================================================

class TestLinkDataclass:
    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(Link)

    def test_required_fields(self):
        lnk = Link(url="http://x.com", text="X", line_num=1, link_type=LinkType.EXTERNAL)
        assert lnk.url == "http://x.com"
        assert lnk.text == "X"
        assert lnk.line_num == 1
        assert lnk.link_type == LinkType.EXTERNAL

    def test_default_status_unknown(self):
        lnk = Link(url="a.md", text="A", line_num=3, link_type=LinkType.INTERNAL)
        assert lnk.status == LinkStatus.UNKNOWN

    def test_status_can_be_set(self):
        lnk = Link(url="a.md", text="A", line_num=3, link_type=LinkType.INTERNAL,
                   status=LinkStatus.VALID)
        assert lnk.status == LinkStatus.VALID

    def test_fields_mutable(self):
        lnk = Link(url="x", text="y", line_num=1, link_type=LinkType.ANCHOR)
        lnk.status = LinkStatus.BROKEN
        assert lnk.status == LinkStatus.BROKEN


# ===========================================================================
# 4. TestCheckResultProperties
# ===========================================================================

class TestCheckResultProperties:
    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(CheckResult)

    def test_empty_result(self):
        r = CheckResult()
        assert r.links == []
        assert r.valid_count == 0
        assert r.broken_count == 0
        assert r.unknown_count == 0
        assert r.skipped_count == 0

    def test_counts_correct(self):
        links = [
            _make_link(status=LinkStatus.VALID),
            _make_link(status=LinkStatus.VALID),
            _make_link(status=LinkStatus.BROKEN),
            _make_link(status=LinkStatus.UNKNOWN),
            _make_link(status=LinkStatus.SKIPPED),
        ]
        r = CheckResult(links=links)
        assert r.valid_count == 2
        assert r.broken_count == 1
        assert r.unknown_count == 1
        assert r.skipped_count == 1

    def test_by_type_returns_correct_subset(self):
        ext = _make_link(link_type=LinkType.EXTERNAL)
        internal = _make_link(link_type=LinkType.INTERNAL)
        anchor = _make_link(link_type=LinkType.ANCHOR)
        r = CheckResult(links=[ext, internal, anchor])
        assert r.by_type(LinkType.EXTERNAL) == [ext]
        assert r.by_type(LinkType.INTERNAL) == [internal]
        assert r.by_type(LinkType.ANCHOR) == [anchor]

    def test_external_links_property(self):
        ext1 = _make_link(link_type=LinkType.EXTERNAL)
        ext2 = _make_link(link_type=LinkType.EXTERNAL)
        internal = _make_link(link_type=LinkType.INTERNAL)
        r = CheckResult(links=[ext1, internal, ext2])
        assert r.external_links == [ext1, ext2]

    def test_internal_links_property(self):
        ext = _make_link(link_type=LinkType.EXTERNAL)
        internal = _make_link(link_type=LinkType.INTERNAL)
        r = CheckResult(links=[ext, internal])
        assert r.internal_links == [internal]

    def test_by_type_empty_if_none(self):
        r = CheckResult(links=[_make_link(link_type=LinkType.EXTERNAL)])
        assert r.by_type(LinkType.IMAGE) == []


# ===========================================================================
# 5. TestLinkExtractorBasic
# ===========================================================================

class TestLinkExtractorBasic:
    def setup_method(self):
        self.ex = LinkExtractor()

    def test_extract_external_link(self):
        text = "See [Google](https://google.com) for details."
        links = self.ex.extract(text)
        assert len(links) == 1
        lnk = links[0]
        assert lnk.url == "https://google.com"
        assert lnk.text == "Google"
        assert lnk.link_type == LinkType.EXTERNAL

    def test_extract_http_link(self):
        text = "[Page](http://example.com)"
        links = self.ex.extract(text)
        assert links[0].link_type == LinkType.EXTERNAL

    def test_extract_internal_link(self):
        text = "Read [this doc](docs/intro.md) first."
        links = self.ex.extract(text)
        assert len(links) == 1
        assert links[0].link_type == LinkType.INTERNAL
        assert links[0].url == "docs/intro.md"

    def test_extract_anchor_link(self):
        text = "Jump to [section](#installation)."
        links = self.ex.extract(text)
        assert len(links) == 1
        assert links[0].link_type == LinkType.ANCHOR
        assert links[0].url == "#installation"

    def test_extract_external_method(self):
        text = "[A](http://a.com) and [B](b.md) and [C](#top)"
        ext = self.ex.extract_external(text)
        assert len(ext) == 1
        assert ext[0].url == "http://a.com"

    def test_extract_internal_method(self):
        text = "[A](http://a.com) and [B](b.md) and [C](#top)"
        internal = self.ex.extract_internal(text)
        assert len(internal) == 1
        assert internal[0].url == "b.md"

    def test_empty_text(self):
        links = self.ex.extract("")
        assert links == []

    def test_no_links(self):
        text = "This is plain text with no links at all."
        links = self.ex.extract(text)
        assert links == []


# ===========================================================================
# 6. TestLinkExtractorImages
# ===========================================================================

class TestLinkExtractorImages:
    def setup_method(self):
        self.ex = LinkExtractor()

    def test_image_detected(self):
        text = "Here is ![logo](images/logo.png) inline."
        links = self.ex.extract(text)
        assert len(links) == 1
        lnk = links[0]
        assert lnk.link_type == LinkType.IMAGE
        assert lnk.url == "images/logo.png"
        assert lnk.text == "logo"

    def test_image_not_counted_as_link(self):
        text = "![alt](img.png)"
        ext = self.ex.extract_external(text)
        assert ext == []

    def test_image_with_external_url(self):
        text = "![pic](https://cdn.example.com/pic.jpg)"
        links = self.ex.extract(text)
        assert len(links) == 1
        assert links[0].link_type == LinkType.IMAGE

    def test_image_alongside_link(self):
        text = "![pic](img.png) and [link](http://x.com)"
        links = self.ex.extract(text)
        types = {lnk.link_type for lnk in links}
        assert LinkType.IMAGE in types
        assert LinkType.EXTERNAL in types

    def test_empty_alt_text(self):
        text = "![](image.png)"
        links = self.ex.extract(text)
        assert len(links) == 1
        assert links[0].link_type == LinkType.IMAGE
        assert links[0].text == ""


# ===========================================================================
# 7. TestLinkExtractorFootnotes
# ===========================================================================

class TestLinkExtractorFootnotes:
    def setup_method(self):
        self.ex = LinkExtractor()

    def test_reference_link_usage_detected(self):
        text = "Check [this][ref1] out.\n\n[ref1]: http://example.com"
        links = self.ex.extract(text)
        footnote_links = [lnk for lnk in links if lnk.link_type == LinkType.FOOTNOTE]
        assert len(footnote_links) >= 1

    def test_reference_definition_detected(self):
        text = "[ref1]: http://example.com"
        links = self.ex.extract(text)
        assert len(links) >= 1
        assert any(lnk.link_type == LinkType.FOOTNOTE for lnk in links)

    def test_footnote_text_captured(self):
        text = "See [my link][myref].\n\n[myref]: http://x.com"
        links = self.ex.extract(text)
        footnotes = [lnk for lnk in links if lnk.link_type == LinkType.FOOTNOTE
                     and lnk.text == "my link"]
        assert len(footnotes) >= 1

    def test_footnote_url_resolved_from_definition(self):
        text = "See [label][key].\n\n[key]: http://resolved.com"
        links = self.ex.extract(text)
        urls = {lnk.url for lnk in links if lnk.link_type == LinkType.FOOTNOTE}
        assert "http://resolved.com" in urls


# ===========================================================================
# 8. TestLinkExtractorLineNumbers
# ===========================================================================

class TestLinkExtractorLineNumbers:
    def setup_method(self):
        self.ex = LinkExtractor()

    def test_link_on_first_line(self):
        text = "[Home](index.md)\nsome other text"
        links = self.ex.extract(text)
        assert links[0].line_num == 1

    def test_link_on_second_line(self):
        text = "First line\n[Page](page.md)"
        links = self.ex.extract(text)
        assert links[0].line_num == 2

    def test_link_on_third_line(self):
        text = "Line 1\nLine 2\n[Link](http://x.com)"
        links = self.ex.extract(text)
        assert links[0].line_num == 3

    def test_multiple_links_correct_lines(self):
        text = "[A](a.md)\n\n[B](http://b.com)\n[C](#c)"
        links = self.ex.extract(text)
        by_url = {lnk.url: lnk.line_num for lnk in links}
        assert by_url["a.md"] == 1
        assert by_url["http://b.com"] == 3
        assert by_url["#c"] == 4

    def test_image_line_number(self):
        text = "intro\n![logo](logo.png)"
        links = self.ex.extract(text)
        assert links[0].line_num == 2


# ===========================================================================
# 9. TestLinkExtractorMultiple
# ===========================================================================

class TestLinkExtractorMultiple:
    def setup_method(self):
        self.ex = LinkExtractor()

    def test_multiple_links_same_line(self):
        text = "[A](a.md) and [B](http://b.com)"
        links = self.ex.extract(text)
        assert len(links) == 2

    def test_mixed_types_all_extracted(self):
        text = (
            "See [External](https://x.com) and [Internal](doc.md) "
            "and [Anchor](#top) and ![Image](img.png)"
        )
        links = self.ex.extract(text)
        types = {lnk.link_type for lnk in links}
        assert LinkType.EXTERNAL in types
        assert LinkType.INTERNAL in types
        assert LinkType.ANCHOR in types
        assert LinkType.IMAGE in types

    def test_order_preserved(self):
        text = "[first](a.md) then [second](http://b.com) then [third](#c)"
        links = self.ex.extract(text)
        assert links[0].url == "a.md"
        assert links[1].url == "http://b.com"
        assert links[2].url == "#c"

    def test_count_matches_expectation(self):
        text = "\n".join(f"[link{i}](http://x.com/{i})" for i in range(5))
        links = self.ex.extract(text)
        assert len(links) == 5


# ===========================================================================
# 10. TestLinkValidatorInternal
# ===========================================================================

class TestLinkValidatorInternal:
    def setup_method(self):
        self.val = LinkValidator()

    def test_valid_when_file_exists(self):
        lnk = _make_link(url="docs/intro.md", link_type=LinkType.INTERNAL,
                         status=LinkStatus.UNKNOWN)
        result = self.val.validate_internal([lnk], existing_files=["docs/intro.md"])
        assert result[0].status == LinkStatus.VALID

    def test_broken_when_file_missing(self):
        lnk = _make_link(url="docs/missing.md", link_type=LinkType.INTERNAL,
                         status=LinkStatus.UNKNOWN)
        result = self.val.validate_internal([lnk], existing_files=["docs/intro.md"])
        assert result[0].status == LinkStatus.BROKEN

    def test_non_internal_links_untouched(self):
        ext = _make_link(url="http://x.com", link_type=LinkType.EXTERNAL,
                         status=LinkStatus.UNKNOWN)
        result = self.val.validate_internal([ext], existing_files=[])
        assert result[0].status == LinkStatus.UNKNOWN

    def test_multiple_links_mixed(self):
        links = [
            _make_link(url="a.md", link_type=LinkType.INTERNAL),
            _make_link(url="b.md", link_type=LinkType.INTERNAL),
        ]
        result = self.val.validate_internal(links, existing_files=["a.md"])
        statuses = {lnk.url: lnk.status for lnk in result}
        assert statuses["a.md"] == LinkStatus.VALID
        assert statuses["b.md"] == LinkStatus.BROKEN

    def test_empty_existing_files_all_broken(self):
        links = [_make_link(url="x.md", link_type=LinkType.INTERNAL)]
        result = self.val.validate_internal(links, existing_files=[])
        assert result[0].status == LinkStatus.BROKEN


# ===========================================================================
# 11. TestLinkValidatorAnchor
# ===========================================================================

class TestLinkValidatorAnchor:
    def setup_method(self):
        self.val = LinkValidator()

    def test_valid_when_heading_exists(self):
        text = "# Installation\n\nSome text."
        lnk = _make_link(url="#installation", link_type=LinkType.ANCHOR)
        result = self.val.validate_anchors([lnk], text)
        assert result[0].status == LinkStatus.VALID

    def test_broken_when_heading_absent(self):
        text = "# Overview\n\nSome text."
        lnk = _make_link(url="#installation", link_type=LinkType.ANCHOR)
        result = self.val.validate_anchors([lnk], text)
        assert result[0].status == LinkStatus.BROKEN

    def test_heading_case_insensitive(self):
        text = "## Getting Started\n"
        lnk = _make_link(url="#getting-started", link_type=LinkType.ANCHOR)
        result = self.val.validate_anchors([lnk], text)
        assert result[0].status == LinkStatus.VALID

    def test_non_anchor_links_untouched(self):
        text = "# Overview"
        lnk = _make_link(url="http://x.com", link_type=LinkType.EXTERNAL)
        result = self.val.validate_anchors([lnk], text)
        assert result[0].status == LinkStatus.UNKNOWN

    def test_h2_heading_valid(self):
        text = "## My Section\nContent."
        lnk = _make_link(url="#my-section", link_type=LinkType.ANCHOR)
        result = self.val.validate_anchors([lnk], text)
        assert result[0].status == LinkStatus.VALID


# ===========================================================================
# 12. TestLinkValidatorSkipExternal
# ===========================================================================

class TestLinkValidatorSkipExternal:
    def setup_method(self):
        self.val = LinkValidator()

    def test_external_marked_skipped(self):
        lnk = _make_link(url="http://example.com", link_type=LinkType.EXTERNAL)
        result = self.val.skip_external([lnk])
        assert result[0].status == LinkStatus.SKIPPED

    def test_non_external_untouched(self):
        internal = _make_link(url="doc.md", link_type=LinkType.INTERNAL)
        anchor = _make_link(url="#sec", link_type=LinkType.ANCHOR)
        result = self.val.skip_external([internal, anchor])
        assert result[0].status == LinkStatus.UNKNOWN
        assert result[1].status == LinkStatus.UNKNOWN

    def test_multiple_external_all_skipped(self):
        links = [
            _make_link(url="http://a.com", link_type=LinkType.EXTERNAL),
            _make_link(url="https://b.com", link_type=LinkType.EXTERNAL),
        ]
        result = self.val.skip_external(links)
        assert all(lnk.status == LinkStatus.SKIPPED for lnk in result)

    def test_empty_list(self):
        result = self.val.skip_external([])
        assert result == []


# ===========================================================================
# 13. TestLinkCheckerIntegration
# ===========================================================================

class TestLinkCheckerIntegration:
    def setup_method(self):
        self.checker = LinkChecker()

    def test_check_returns_check_result(self):
        result = self.checker.check("")
        assert isinstance(result, CheckResult)

    def test_check_external_skipped(self):
        text = "[Google](https://google.com)"
        result = self.checker.check(text)
        assert result.skipped_count == 1
        assert result.external_links[0].status == LinkStatus.SKIPPED

    def test_check_internal_valid(self):
        text = "[Doc](docs/readme.md)"
        result = self.checker.check(text, existing_files=["docs/readme.md"])
        assert result.valid_count == 1

    def test_check_internal_broken(self):
        text = "[Missing](docs/missing.md)"
        result = self.checker.check(text, existing_files=["docs/readme.md"])
        assert result.broken_count == 1

    def test_check_anchor_valid(self):
        text = "# Overview\n\nSee [here](#overview)."
        result = self.checker.check(text)
        assert result.valid_count == 1

    def test_check_anchor_broken(self):
        text = "# Overview\n\nSee [bad](#nonexistent)."
        result = self.checker.check(text)
        assert result.broken_count == 1

    def test_check_batch_returns_list(self):
        texts = ["[A](http://a.com)", "[B](b.md)"]
        results = self.checker.check_batch(texts)
        assert isinstance(results, list)
        assert len(results) == 2
        assert all(isinstance(r, CheckResult) for r in results)

    def test_check_batch_independent_results(self):
        texts = [
            "[A](http://a.com)",
            "[B](b.md) [C](https://c.com)",
        ]
        results = self.checker.check_batch(texts)
        assert len(results[0].links) == 1
        assert len(results[1].links) == 2

    def test_check_no_existing_files_internals_unknown(self):
        text = "[Doc](doc.md)"
        result = self.checker.check(text)  # no existing_files passed
        internals = result.internal_links
        assert len(internals) == 1
        assert internals[0].status == LinkStatus.UNKNOWN

    def test_check_mixed_document(self):
        text = (
            "# Setup\n\n"
            "See [External](https://x.com), [Internal](guide.md), "
            "[Anchor](#setup), and ![Image](logo.png)."
        )
        result = self.checker.check(text, existing_files=["guide.md"])
        assert result.skipped_count >= 1      # external
        assert result.valid_count >= 2        # internal + anchor
        assert result.by_type(LinkType.IMAGE) != []


# ===========================================================================
# 14. TestEdgeCases
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.ex = LinkExtractor()
        self.checker = LinkChecker()

    def test_empty_string(self):
        result = self.checker.check("")
        assert result.links == []

    def test_text_with_no_links(self):
        result = self.checker.check("Just plain text, no links here.")
        assert result.links == []

    def test_malformed_link_no_closing_paren(self):
        # Incomplete markdown link — should not crash, just not extracted.
        text = "[broken](http://x.com"
        links = self.ex.extract(text)
        assert isinstance(links, list)

    def test_link_with_spaces_in_url(self):
        # Real-world: sometimes URLs have leading/trailing spaces — should be stripped.
        text = "[Page]( docs/page.md )"
        links = self.ex.extract(text)
        if links:
            assert links[0].url == "docs/page.md"

    def test_adjacent_links_all_found(self):
        text = "[A](a.md)[B](b.md)[C](c.md)"
        links = self.ex.extract(text)
        assert len(links) == 3

    def test_check_result_links_list_default_empty(self):
        r = CheckResult()
        assert isinstance(r.links, list)
        assert len(r.links) == 0

    def test_link_validator_default_base_path(self):
        val = LinkValidator()
        assert val.base_path == "."

    def test_link_validator_custom_base_path(self):
        val = LinkValidator(base_path="/some/path")
        assert val.base_path == "/some/path"

    def test_check_batch_empty_list(self):
        results = self.checker.check_batch([])
        assert results == []

    def test_image_not_in_internal_or_external(self):
        text = "![alt](image.png)"
        links = self.ex.extract(text)
        assert self.ex.extract_internal(text) == []
        assert self.ex.extract_external(text) == []
