"""Tests for the citation_parser module — ≥45 tests covering all spec requirements."""
from __future__ import annotations

import dataclasses
from enum import Enum

import pytest

from docstoolkit.citation_parser import (
    Citation,
    CitationParser,
    CitationStats,
    CitationType,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parser() -> CitationParser:
    return CitationParser()


def _make_citation(
    raw: str = "[text](https://example.com)",
    citation_type: CitationType = CitationType.URL,
    url: str | None = "https://example.com",
    title: str | None = "text",
    line_num: int = 1,
    identifier: str | None = None,
) -> Citation:
    return Citation(
        raw=raw,
        citation_type=citation_type,
        url=url,
        title=title,
        line_num=line_num,
        identifier=identifier,
    )


# ===========================================================================
# 1. TestCitationType
# ===========================================================================

class TestCitationType:
    def test_is_enum(self):
        assert issubclass(CitationType, Enum)

    def test_members_exist(self):
        for name in ("URL", "DOI", "ARXIV", "GITHUB", "FOOTNOTE", "INLINE_REF", "BARE_URL"):
            assert hasattr(CitationType, name), f"Missing member: {name}"

    def test_values_are_strings(self):
        for member in CitationType:
            assert isinstance(member.value, str)

    def test_distinct_values(self):
        values = [m.value for m in CitationType]
        assert len(values) == len(set(values))

    def test_total_member_count(self):
        assert len(CitationType) == 7


# ===========================================================================
# 2. TestCitationDataclass
# ===========================================================================

class TestCitationDataclass:
    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(Citation)

    def test_required_fields(self):
        c = Citation(raw="[link](https://x.com)", citation_type=CitationType.URL)
        assert c.raw == "[link](https://x.com)"
        assert c.citation_type == CitationType.URL

    def test_optional_fields_default_none(self):
        c = Citation(raw="x", citation_type=CitationType.BARE_URL)
        assert c.url is None
        assert c.title is None
        assert c.identifier is None

    def test_line_num_default_one(self):
        c = Citation(raw="x", citation_type=CitationType.BARE_URL)
        assert c.line_num == 1

    def test_all_fields_settable(self):
        c = Citation(
            raw="raw",
            citation_type=CitationType.DOI,
            url="https://doi.org/10.1234/test",
            title="My Paper",
            line_num=5,
            identifier="10.1234/test",
        )
        assert c.url == "https://doi.org/10.1234/test"
        assert c.title == "My Paper"
        assert c.line_num == 5
        assert c.identifier == "10.1234/test"

    def test_is_valid_url_valid(self):
        c = Citation(raw="r", citation_type=CitationType.URL, url="https://example.com")
        assert c.is_valid is True

    def test_is_valid_url_missing_scheme(self):
        c = Citation(raw="r", citation_type=CitationType.URL, url="example.com")
        assert c.is_valid is False

    def test_is_valid_url_none(self):
        c = Citation(raw="r", citation_type=CitationType.URL, url=None)
        assert c.is_valid is False

    def test_is_valid_doi_with_identifier(self):
        c = Citation(raw="r", citation_type=CitationType.DOI, identifier="10.1234/test")
        assert c.is_valid is True

    def test_is_valid_doi_bad_identifier(self):
        c = Citation(raw="r", citation_type=CitationType.DOI, identifier="not-a-doi")
        assert c.is_valid is False

    def test_is_valid_arxiv_valid_id(self):
        c = Citation(raw="r", citation_type=CitationType.ARXIV, identifier="2301.12345")
        assert c.is_valid is True

    def test_is_valid_arxiv_short_id(self):
        c = Citation(raw="r", citation_type=CitationType.ARXIV, identifier="2301.1234")
        assert c.is_valid is True

    def test_is_valid_arxiv_bad_id(self):
        c = Citation(raw="r", citation_type=CitationType.ARXIV, identifier="bad-id")
        assert c.is_valid is False

    def test_is_valid_github(self):
        c = Citation(raw="r", citation_type=CitationType.GITHUB, url="https://github.com/user/repo")
        assert c.is_valid is True

    def test_is_valid_footnote_always_true_with_raw(self):
        c = Citation(raw="[^1]", citation_type=CitationType.FOOTNOTE)
        assert c.is_valid is True

    def test_is_valid_inline_ref_true(self):
        c = Citation(raw="[text][ref]", citation_type=CitationType.INLINE_REF)
        assert c.is_valid is True


# ===========================================================================
# 3. TestCitationStatsDataclass
# ===========================================================================

class TestCitationStatsDataclass:
    def test_is_dataclass(self):
        assert dataclasses.is_dataclass(CitationStats)

    def test_default_values(self):
        s = CitationStats()
        assert s.total == 0
        assert s.by_type == {}
        assert s.unique_urls == set()

    def test_domains_empty_when_no_urls(self):
        s = CitationStats()
        assert s.domains == set()

    def test_domains_single_url(self):
        s = CitationStats(unique_urls={"https://example.com/page"})
        assert "example.com" in s.domains

    def test_domains_multiple_urls_same_domain(self):
        s = CitationStats(unique_urls={"https://example.com/a", "https://example.com/b"})
        assert s.domains == {"example.com"}

    def test_domains_multiple_different_domains(self):
        s = CitationStats(unique_urls={"https://a.com/x", "https://b.org/y"})
        assert "a.com" in s.domains
        assert "b.org" in s.domains
        assert len(s.domains) == 2

    def test_domains_strips_path_and_query(self):
        s = CitationStats(unique_urls={"https://doi.org/10.1234/test?q=1"})
        assert "doi.org" in s.domains

    def test_total_field(self):
        s = CitationStats(total=42)
        assert s.total == 42

    def test_by_type_field(self):
        s = CitationStats(by_type={"url": 3, "doi": 1})
        assert s.by_type["url"] == 3
        assert s.by_type["doi"] == 1


# ===========================================================================
# 4. TestParseMarkdownLinks
# ===========================================================================

class TestParseMarkdownLinks:
    def setup_method(self):
        self.p = _parser()

    def test_simple_markdown_link(self):
        text = "See [Google](https://google.com) for info."
        results = self.p.parse(text)
        assert any(c.url == "https://google.com" for c in results)

    def test_title_captured(self):
        text = "[My Title](https://example.com)"
        results = self.p.parse(text)
        assert results[0].title == "My Title"

    def test_markdown_link_type_url(self):
        text = "[link](https://example.com)"
        results = self.p.parse(text)
        assert results[0].citation_type == CitationType.URL

    def test_markdown_link_github_type(self):
        text = "[repo](https://github.com/user/project)"
        results = self.p.parse(text)
        assert results[0].citation_type == CitationType.GITHUB

    def test_markdown_link_arxiv_type(self):
        text = "[paper](https://arxiv.org/abs/2301.12345)"
        results = self.p.parse(text)
        assert results[0].citation_type == CitationType.ARXIV

    def test_markdown_link_doi_type(self):
        text = "[doi](https://doi.org/10.1234/something)"
        results = self.p.parse(text)
        assert results[0].citation_type == CitationType.DOI

    def test_markdown_link_line_number(self):
        text = "Line one\n[link](https://example.com)"
        results = self.p.parse(text)
        url_citations = [c for c in results if c.url == "https://example.com"]
        assert url_citations[0].line_num == 2

    def test_multiple_markdown_links(self):
        text = "[A](https://a.com) and [B](https://b.com)"
        results = self.p.parse(text)
        urls = {c.url for c in results if c.url}
        assert "https://a.com" in urls
        assert "https://b.com" in urls


# ===========================================================================
# 5. TestParseBareUrls
# ===========================================================================

class TestParseBareUrls:
    def setup_method(self):
        self.p = _parser()

    def test_bare_https_url(self):
        text = "Visit https://example.com for details."
        results = self.p.parse(text)
        bare = [c for c in results if c.citation_type == CitationType.BARE_URL]
        assert len(bare) >= 1

    def test_bare_http_url(self):
        text = "See http://old-site.com here."
        results = self.p.parse(text)
        bare = [c for c in results if c.citation_type == CitationType.BARE_URL]
        assert len(bare) >= 1

    def test_bare_url_not_inside_markdown_link(self):
        text = "[click](https://example.com)"
        results = self.p.parse(text)
        # The URL inside a markdown link should be URL type, not BARE_URL
        bare = [c for c in results if c.citation_type == CitationType.BARE_URL]
        assert len(bare) == 0

    def test_parse_urls_includes_bare(self):
        text = "See https://example.com here."
        results = self.p.parse_urls(text)
        assert len(results) >= 1

    def test_bare_url_line_number(self):
        text = "First line\nhttps://example.com\nThird line"
        results = self.p.parse(text)
        url_hits = [c for c in results if c.url == "https://example.com"]
        assert url_hits[0].line_num == 2


# ===========================================================================
# 6. TestParseDois
# ===========================================================================

class TestParseDois:
    def setup_method(self):
        self.p = _parser()

    def test_doi_url_pattern(self):
        text = "Reference: https://doi.org/10.1038/nature12345"
        results = self.p.parse_dois(text)
        assert len(results) >= 1
        assert results[0].citation_type == CitationType.DOI

    def test_doi_prefix_pattern(self):
        text = "See doi:10.1234/abcde for details."
        results = self.p.parse_dois(text)
        assert len(results) >= 1

    def test_doi_identifier_extracted(self):
        text = "https://doi.org/10.1038/nature12345"
        results = self.p.parse_dois(text)
        assert results[0].identifier == "10.1038/nature12345"

    def test_doi_url_constructed_from_prefix(self):
        text = "doi:10.1234/test-paper"
        results = self.p.parse_dois(text)
        assert results[0].url == "https://doi.org/10.1234/test-paper"

    def test_doi_is_valid(self):
        text = "doi:10.1234/test"
        results = self.p.parse_dois(text)
        assert results[0].is_valid is True

    def test_doi_in_markdown_link(self):
        text = "[paper](https://doi.org/10.1234/test)"
        results = self.p.parse_dois(text)
        assert len(results) >= 1
        assert results[0].citation_type == CitationType.DOI


# ===========================================================================
# 7. TestParseArxiv
# ===========================================================================

class TestParseArxiv:
    def setup_method(self):
        self.p = _parser()

    def test_arxiv_label_pattern(self):
        text = "See arXiv:2301.12345 for the paper."
        results = self.p.parse_arxiv(text)
        assert len(results) >= 1
        assert results[0].citation_type == CitationType.ARXIV

    def test_arxiv_url_pattern(self):
        text = "Paper at https://arxiv.org/abs/2301.12345"
        results = self.p.parse_arxiv(text)
        assert len(results) >= 1

    def test_arxiv_identifier_extracted_from_label(self):
        text = "arXiv:2301.12345"
        results = self.p.parse_arxiv(text)
        assert results[0].identifier == "2301.12345"

    def test_arxiv_identifier_extracted_from_url(self):
        text = "https://arxiv.org/abs/2301.12345"
        results = self.p.parse_arxiv(text)
        assert results[0].identifier == "2301.12345"

    def test_arxiv_url_constructed_from_label(self):
        text = "arXiv:2301.12345"
        results = self.p.parse_arxiv(text)
        assert results[0].url == "https://arxiv.org/abs/2301.12345"

    def test_arxiv_case_insensitive(self):
        text = "arxiv:2301.12345"
        results = self.p.parse_arxiv(text)
        assert len(results) >= 1

    def test_arxiv_is_valid(self):
        text = "arXiv:2301.12345"
        results = self.p.parse_arxiv(text)
        assert results[0].is_valid is True

    def test_arxiv_four_digit_id(self):
        text = "arXiv:2301.1234"
        results = self.p.parse_arxiv(text)
        assert len(results) >= 1
        assert results[0].identifier == "2301.1234"


# ===========================================================================
# 8. TestParseGithub
# ===========================================================================

class TestParseGithub:
    def setup_method(self):
        self.p = _parser()

    def test_github_bare_url(self):
        text = "Project at https://github.com/user/repo"
        results = self.p.parse(text)
        github = [c for c in results if c.citation_type == CitationType.GITHUB]
        assert len(github) >= 1

    def test_github_in_markdown_link(self):
        text = "[project](https://github.com/user/repo)"
        results = self.p.parse(text)
        assert results[0].citation_type == CitationType.GITHUB

    def test_github_url_preserved(self):
        text = "https://github.com/user/my-repo"
        results = self.p.parse(text)
        github = [c for c in results if c.citation_type == CitationType.GITHUB]
        assert github[0].url == "https://github.com/user/my-repo"

    def test_github_is_valid(self):
        text = "https://github.com/user/repo"
        results = self.p.parse(text)
        github = [c for c in results if c.citation_type == CitationType.GITHUB]
        assert github[0].is_valid is True

    def test_parse_urls_includes_github(self):
        text = "https://github.com/user/repo"
        results = self.p.parse_urls(text)
        assert len(results) >= 1
        assert results[0].citation_type == CitationType.GITHUB


# ===========================================================================
# 9. TestParseFootnotes
# ===========================================================================

class TestParseFootnotes:
    def setup_method(self):
        self.p = _parser()

    def test_footnote_definition_detected(self):
        text = "[^1]: https://example.com"
        results = self.p.parse(text)
        footnotes = [c for c in results if c.citation_type == CitationType.FOOTNOTE]
        assert len(footnotes) >= 1

    def test_footnote_usage_detected(self):
        text = "Some text[^note] with a footnote."
        results = self.p.parse(text)
        footnotes = [c for c in results if c.citation_type == CitationType.FOOTNOTE]
        assert len(footnotes) >= 1

    def test_footnote_identifier_captured(self):
        text = "Text[^myref] here.\n\n[^myref]: https://example.com"
        results = self.p.parse(text)
        ids = {c.identifier for c in results if c.citation_type == CitationType.FOOTNOTE}
        assert "myref" in ids

    def test_footnote_def_url_captured(self):
        text = "[^1]: https://example.com"
        results = self.p.parse(text)
        footnotes = [c for c in results if c.citation_type == CitationType.FOOTNOTE]
        urls = {c.url for c in footnotes if c.url}
        assert "https://example.com" in urls

    def test_inline_ref_detected(self):
        text = "See [this][ref1] for details.\n\n[ref1]: https://example.com"
        results = self.p.parse(text)
        inline = [c for c in results if c.citation_type == CitationType.INLINE_REF]
        assert len(inline) >= 1

    def test_inline_ref_title_captured(self):
        text = "[My Label][someref]"
        results = self.p.parse(text)
        inline = [c for c in results if c.citation_type == CitationType.INLINE_REF]
        assert inline[0].title == "My Label"

    def test_inline_ref_identifier_captured(self):
        text = "[label][mykey]"
        results = self.p.parse(text)
        inline = [c for c in results if c.citation_type == CitationType.INLINE_REF]
        assert inline[0].identifier == "mykey"


# ===========================================================================
# 10. TestParseAll
# ===========================================================================

class TestParseAll:
    def setup_method(self):
        self.p = _parser()

    def test_parse_returns_list(self):
        assert isinstance(self.p.parse(""), list)

    def test_parse_finds_multiple_types(self):
        text = (
            "[paper](https://arxiv.org/abs/2301.12345)\n"
            "[gh](https://github.com/user/repo)\n"
            "doi:10.1234/test\n"
            "[^1]: https://example.com\n"
        )
        results = self.p.parse(text)
        types = {c.citation_type for c in results}
        assert CitationType.ARXIV in types
        assert CitationType.GITHUB in types
        assert CitationType.DOI in types

    def test_line_numbers_accurate(self):
        text = "Line 1\nLine 2\nhttps://example.com\nLine 4"
        results = self.p.parse(text)
        bare = [c for c in results if c.url == "https://example.com"]
        assert bare[0].line_num == 3

    def test_order_preserved(self):
        text = "[A](https://a.com) then [B](https://b.com)"
        results = self.p.parse(text)
        urls = [c.url for c in results if c.url]
        assert urls.index("https://a.com") < urls.index("https://b.com")

    def test_parse_urls_returns_only_url_types(self):
        text = "https://example.com doi:10.1234/test arXiv:2301.12345"
        results = self.p.parse_urls(text)
        url_types = {CitationType.URL, CitationType.BARE_URL, CitationType.GITHUB}
        assert all(c.citation_type in url_types for c in results)

    def test_parse_dois_returns_only_doi(self):
        text = "doi:10.1234/test and https://example.com"
        results = self.p.parse_dois(text)
        assert all(c.citation_type == CitationType.DOI for c in results)

    def test_parse_arxiv_returns_only_arxiv(self):
        text = "arXiv:2301.12345 and https://example.com"
        results = self.p.parse_arxiv(text)
        assert all(c.citation_type == CitationType.ARXIV for c in results)


# ===========================================================================
# 11. TestStats
# ===========================================================================

class TestStats:
    def setup_method(self):
        self.p = _parser()

    def test_stats_returns_citation_stats(self):
        result = self.p.stats("")
        assert isinstance(result, CitationStats)

    def test_stats_empty_text(self):
        s = self.p.stats("")
        assert s.total == 0
        assert s.by_type == {}
        assert s.unique_urls == set()

    def test_stats_total_count(self):
        text = "[A](https://a.com) [B](https://b.com)"
        s = self.p.stats(text)
        assert s.total == 2

    def test_stats_by_type(self):
        text = "[A](https://a.com) doi:10.1234/test"
        s = self.p.stats(text)
        assert "url" in s.by_type or "github" in s.by_type or "doi" in s.by_type

    def test_stats_unique_urls(self):
        text = "[A](https://a.com) [B](https://a.com)"  # same URL twice
        s = self.p.stats(text)
        assert "https://a.com" in s.unique_urls
        assert len(s.unique_urls) == 1

    def test_stats_domains(self):
        text = "[A](https://github.com/u/r) [B](https://arxiv.org/abs/2301.12345)"
        s = self.p.stats(text)
        assert len(s.domains) >= 1

    def test_stats_by_type_counts_doi(self):
        text = "doi:10.1234/a doi:10.1234/b"
        s = self.p.stats(text)
        assert s.by_type.get("doi", 0) == 2


# ===========================================================================
# 12. TestDeduplicate
# ===========================================================================

class TestDeduplicate:
    def setup_method(self):
        self.p = _parser()

    def test_deduplicate_returns_list(self):
        result = self.p.deduplicate([])
        assert isinstance(result, list)

    def test_deduplicate_empty(self):
        assert self.p.deduplicate([]) == []

    def test_deduplicate_removes_same_url(self):
        c1 = _make_citation(url="https://example.com")
        c2 = _make_citation(url="https://example.com")
        result = self.p.deduplicate([c1, c2])
        assert len(result) == 1

    def test_deduplicate_keeps_different_urls(self):
        c1 = _make_citation(url="https://a.com")
        c2 = _make_citation(url="https://b.com")
        result = self.p.deduplicate([c1, c2])
        assert len(result) == 2

    def test_deduplicate_by_identifier_when_no_url(self):
        c1 = Citation(raw="[^1]", citation_type=CitationType.FOOTNOTE, identifier="note1")
        c2 = Citation(raw="[^1]", citation_type=CitationType.FOOTNOTE, identifier="note1")
        result = self.p.deduplicate([c1, c2])
        assert len(result) == 1

    def test_deduplicate_keeps_first(self):
        c1 = _make_citation(raw="first", url="https://example.com")
        c2 = _make_citation(raw="second", url="https://example.com")
        result = self.p.deduplicate([c1, c2])
        assert result[0].raw == "first"

    def test_deduplicate_via_parse_same_url(self):
        text = "[A](https://example.com) and [B](https://example.com)"
        citations = self.p.parse(text)
        deduped = self.p.deduplicate(citations)
        urls = [c.url for c in deduped if c.url == "https://example.com"]
        assert len(urls) == 1


# ===========================================================================
# 13. TestEdgeCases
# ===========================================================================

class TestEdgeCases:
    def setup_method(self):
        self.p = _parser()

    def test_empty_text_returns_empty_list(self):
        assert self.p.parse("") == []

    def test_plain_text_no_citations(self):
        assert self.p.parse("Just some plain text with no links.") == []

    def test_image_not_parsed_as_citation(self):
        text = "![alt text](https://example.com/image.png)"
        results = self.p.parse(text)
        # Images (![...](url)) should not be picked up by the markdown link pattern
        md_links = [c for c in results if c.title == "alt text"]
        assert len(md_links) == 0

    def test_same_url_multiple_times_stats(self):
        text = "[A](https://example.com)\n[B](https://example.com)"
        s = self.p.stats(text)
        assert s.total == 2
        assert len(s.unique_urls) == 1  # unique urls

    def test_arxiv_label_and_url_not_double_counted(self):
        # When both label and URL appear, they should each be their own citation
        text = "arXiv:2301.12345 and https://arxiv.org/abs/2301.12345"
        results = self.p.parse_arxiv(text)
        assert len(results) == 2

    def test_github_url_with_path(self):
        text = "https://github.com/user/repo/blob/main/README.md"
        results = self.p.parse(text)
        github = [c for c in results if c.citation_type == CitationType.GITHUB]
        assert len(github) >= 1

    def test_parse_returns_correct_raw_text(self):
        text = "[click here](https://example.com)"
        results = self.p.parse(text)
        assert results[0].raw == "[click here](https://example.com)"

    def test_multiline_document(self):
        text = (
            "# Title\n\n"
            "See [this paper](https://arxiv.org/abs/2301.12345) for details.\n\n"
            "Also doi:10.1038/nature12345 is relevant.\n\n"
            "GitHub: https://github.com/user/repo\n\n"
            "[^1]: https://example.com\n"
        )
        results = self.p.parse(text)
        types = {c.citation_type for c in results}
        assert CitationType.ARXIV in types
        assert CitationType.DOI in types
        assert CitationType.GITHUB in types

    def test_doi_bare_ten_prefix(self):
        text = "Citation: 10.1038/nature12345 is widely used."
        results = self.p.parse_dois(text)
        assert len(results) >= 1
        assert results[0].identifier == "10.1038/nature12345"
