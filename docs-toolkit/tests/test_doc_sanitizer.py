"""Tests for the doc_sanitizer module (E141)."""

from __future__ import annotations

import pytest

from docstoolkit.doc_sanitizer import (
    DocSanitizer,
    SanitizationResult,
    SanitizationRule,
    SanitizerConfig,
)


# ---------------------------------------------------------------------------
# SanitizationRule
# ---------------------------------------------------------------------------


class TestSanitizationRule:
    def test_has_all_required_members(self) -> None:
        names = {member.name for member in SanitizationRule}
        assert names == {
            "STRIP_HTML",
            "ESCAPE_HTML",
            "REMOVE_SCRIPTS",
            "REMOVE_STYLE",
            "NORMALIZE_LINKS",
            "STRIP_IMAGES",
            "REMOVE_COMMENTS",
        }

    def test_members_are_unique(self) -> None:
        values = [member.value for member in SanitizationRule]
        assert len(values) == len(set(values))

    def test_member_access_by_name(self) -> None:
        assert SanitizationRule["STRIP_HTML"] is SanitizationRule.STRIP_HTML


# ---------------------------------------------------------------------------
# SanitizerConfig
# ---------------------------------------------------------------------------


class TestSanitizerConfig:
    def test_default_rules(self) -> None:
        cfg = SanitizerConfig()
        assert SanitizationRule.REMOVE_SCRIPTS in cfg.rules
        assert SanitizationRule.REMOVE_STYLE in cfg.rules
        assert SanitizationRule.REMOVE_COMMENTS in cfg.rules

    def test_default_allowed_protocols(self) -> None:
        cfg = SanitizerConfig()
        assert cfg.allowed_protocols == {"http", "https", "mailto"}

    def test_default_allowed_html_tags_empty(self) -> None:
        cfg = SanitizerConfig()
        assert cfg.allowed_html_tags == set()

    def test_strip_data_urls_default_true(self) -> None:
        cfg = SanitizerConfig()
        assert cfg.strip_data_urls is True

    def test_custom_rules(self) -> None:
        cfg = SanitizerConfig(rules=[SanitizationRule.STRIP_HTML])
        assert cfg.rules == [SanitizationRule.STRIP_HTML]

    def test_custom_protocols(self) -> None:
        cfg = SanitizerConfig(allowed_protocols={"ftp"})
        assert cfg.allowed_protocols == {"ftp"}

    def test_custom_allowed_tags(self) -> None:
        cfg = SanitizerConfig(allowed_html_tags={"b", "i"})
        assert cfg.allowed_html_tags == {"b", "i"}

    def test_defaults_are_independent(self) -> None:
        cfg1 = SanitizerConfig()
        cfg2 = SanitizerConfig()
        cfg1.rules.append(SanitizationRule.STRIP_HTML)
        assert SanitizationRule.STRIP_HTML not in cfg2.rules


# ---------------------------------------------------------------------------
# SanitizationResult
# ---------------------------------------------------------------------------


class TestSanitizationResult:
    def test_changed_true_when_different(self) -> None:
        result = SanitizationResult(original="a", sanitized="b")
        assert result.changed is True

    def test_changed_false_when_equal(self) -> None:
        result = SanitizationResult(original="same", sanitized="same")
        assert result.changed is False

    def test_removed_items_defaults_empty(self) -> None:
        result = SanitizationResult(original="x", sanitized="x")
        assert result.removed_items == []

    def test_removed_items_assignable(self) -> None:
        result = SanitizationResult(
            original="x", sanitized="y", removed_items=["scripts"]
        )
        assert result.removed_items == ["scripts"]


# ---------------------------------------------------------------------------
# strip_html
# ---------------------------------------------------------------------------


class TestStripHtml:
    def setup_method(self) -> None:
        self.s = DocSanitizer()

    def test_removes_simple_tag(self) -> None:
        assert self.s.strip_html("<p>Hello</p>") == "Hello"

    def test_removes_attributes(self) -> None:
        assert self.s.strip_html('<a href="x">link</a>') == "link"

    def test_removes_multiple_tags(self) -> None:
        assert self.s.strip_html("<b>a</b><i>b</i>") == "ab"

    def test_no_tags_unchanged(self) -> None:
        assert self.s.strip_html("plain text") == "plain text"

    def test_empty(self) -> None:
        assert self.s.strip_html("") == ""


# ---------------------------------------------------------------------------
# strip_html_keep_allowed
# ---------------------------------------------------------------------------


class TestStripHtmlKeepAllowed:
    def setup_method(self) -> None:
        self.s = DocSanitizer()

    def test_keeps_allowed(self) -> None:
        result = self.s.strip_html_keep_allowed(
            "<b>bold</b><span>x</span>", {"b"}
        )
        assert result == "<b>bold</b>x"

    def test_keeps_closing_tags(self) -> None:
        result = self.s.strip_html_keep_allowed(
            "<i>italic</i>", {"i"}
        )
        assert result == "<i>italic</i>"

    def test_keeps_multiple(self) -> None:
        result = self.s.strip_html_keep_allowed(
            "<b>x</b><i>y</i><p>z</p>", {"b", "i"}
        )
        assert result == "<b>x</b><i>y</i>z"

    def test_case_insensitive(self) -> None:
        result = self.s.strip_html_keep_allowed("<B>x</B>", {"b"})
        assert result == "<B>x</B>"

    def test_empty_allowed_strips_all(self) -> None:
        result = self.s.strip_html_keep_allowed("<b>x</b>", set())
        assert result == "x"


# ---------------------------------------------------------------------------
# escape_html
# ---------------------------------------------------------------------------


class TestEscapeHtml:
    def setup_method(self) -> None:
        self.s = DocSanitizer()

    def test_escapes_lt_gt(self) -> None:
        assert self.s.escape_html("<p>") == "&lt;p&gt;"

    def test_escapes_amp(self) -> None:
        assert self.s.escape_html("a & b") == "a &amp; b"

    def test_escapes_quotes(self) -> None:
        out = self.s.escape_html('"x"')
        assert "&quot;" in out

    def test_plain_text_unchanged(self) -> None:
        assert self.s.escape_html("hello") == "hello"


# ---------------------------------------------------------------------------
# remove_scripts
# ---------------------------------------------------------------------------


class TestRemoveScripts:
    def setup_method(self) -> None:
        self.s = DocSanitizer()

    def test_removes_script_block(self) -> None:
        out = self.s.remove_scripts("a<script>alert(1)</script>b")
        assert out == "ab"

    def test_removes_with_attributes(self) -> None:
        out = self.s.remove_scripts(
            'x<script type="text/javascript">evil()</script>y'
        )
        assert out == "xy"

    def test_case_insensitive(self) -> None:
        out = self.s.remove_scripts("a<SCRIPT>x</SCRIPT>b")
        assert out == "ab"

    def test_multiline_script(self) -> None:
        out = self.s.remove_scripts("a<script>\nlots\nof\ncode\n</script>b")
        assert out == "ab"

    def test_no_script_unchanged(self) -> None:
        assert self.s.remove_scripts("plain") == "plain"


# ---------------------------------------------------------------------------
# remove_style
# ---------------------------------------------------------------------------


class TestRemoveStyle:
    def setup_method(self) -> None:
        self.s = DocSanitizer()

    def test_removes_style_block(self) -> None:
        out = self.s.remove_style("a<style>body{color:red}</style>b")
        assert out == "ab"

    def test_case_insensitive(self) -> None:
        out = self.s.remove_style("a<STYLE>x</STYLE>b")
        assert out == "ab"

    def test_multiline(self) -> None:
        out = self.s.remove_style("a<style>\nbody{\ncolor:red\n}\n</style>b")
        assert out == "ab"

    def test_no_style_unchanged(self) -> None:
        assert self.s.remove_style("plain") == "plain"


# ---------------------------------------------------------------------------
# remove_comments
# ---------------------------------------------------------------------------


class TestRemoveComments:
    def setup_method(self) -> None:
        self.s = DocSanitizer()

    def test_removes_simple_comment(self) -> None:
        assert self.s.remove_comments("a<!-- c -->b") == "ab"

    def test_removes_multiline_comment(self) -> None:
        out = self.s.remove_comments("a<!--\nmulti\nline\n-->b")
        assert out == "ab"

    def test_removes_multiple_comments(self) -> None:
        out = self.s.remove_comments("a<!-- x -->b<!-- y -->c")
        assert out == "abc"

    def test_no_comment_unchanged(self) -> None:
        assert self.s.remove_comments("plain") == "plain"


# ---------------------------------------------------------------------------
# normalize_links
# ---------------------------------------------------------------------------


class TestNormalizeLinks:
    def setup_method(self) -> None:
        self.s = DocSanitizer()
        self.allowed = {"http", "https", "mailto"}

    def test_keeps_https_link(self) -> None:
        text = "[ok](https://example.com)"
        assert self.s.normalize_links(text, self.allowed) == text

    def test_keeps_http_link(self) -> None:
        text = "[ok](http://example.com)"
        assert self.s.normalize_links(text, self.allowed) == text

    def test_keeps_mailto(self) -> None:
        text = "[ok](mailto:x@y.com)"
        assert self.s.normalize_links(text, self.allowed) == text

    def test_replaces_javascript_link(self) -> None:
        out = self.s.normalize_links(
            "[click](javascript:evil)", self.allowed
        )
        assert out == "[click](#)"

    def test_replaces_data_link(self) -> None:
        out = self.s.normalize_links(
            "[click](data:text/html,xx)", self.allowed
        )
        assert out == "[click](#)"

    def test_keeps_relative(self) -> None:
        text = "[doc](./file.md)"
        assert self.s.normalize_links(text, self.allowed) == text

    def test_keeps_anchor(self) -> None:
        text = "[a](#section)"
        assert self.s.normalize_links(text, self.allowed) == text


# ---------------------------------------------------------------------------
# strip_images
# ---------------------------------------------------------------------------


class TestStripImages:
    def setup_method(self) -> None:
        self.s = DocSanitizer()

    def test_strips_image(self) -> None:
        assert self.s.strip_images("a![alt](src.png)b") == "ab"

    def test_strips_image_with_empty_alt(self) -> None:
        assert self.s.strip_images("![](x.png)") == ""

    def test_keeps_regular_link(self) -> None:
        assert self.s.strip_images("[link](x)") == "[link](x)"

    def test_strips_multiple(self) -> None:
        out = self.s.strip_images("![a](1)![b](2)")
        assert out == ""

    def test_no_image_unchanged(self) -> None:
        assert self.s.strip_images("plain") == "plain"


# ---------------------------------------------------------------------------
# is_safe_url
# ---------------------------------------------------------------------------


class TestIsSafeUrl:
    def setup_method(self) -> None:
        self.s = DocSanitizer()
        self.allowed = {"http", "https", "mailto"}

    def test_http_safe(self) -> None:
        assert self.s.is_safe_url("http://x.com", self.allowed) is True

    def test_https_safe(self) -> None:
        assert self.s.is_safe_url("https://x.com", self.allowed) is True

    def test_mailto_safe(self) -> None:
        assert self.s.is_safe_url("mailto:x@y.com", self.allowed) is True

    def test_javascript_unsafe(self) -> None:
        assert self.s.is_safe_url("javascript:alert(1)", self.allowed) is False

    def test_ftp_unsafe_when_not_allowed(self) -> None:
        assert self.s.is_safe_url("ftp://x.com", self.allowed) is False

    def test_relative_safe(self) -> None:
        assert self.s.is_safe_url("./path", self.allowed) is True

    def test_anchor_safe(self) -> None:
        assert self.s.is_safe_url("#section", self.allowed) is True

    def test_empty_safe(self) -> None:
        assert self.s.is_safe_url("", self.allowed) is True

    def test_data_url_unsafe_default(self) -> None:
        s = DocSanitizer()  # strip_data_urls=True default
        assert s.is_safe_url("data:text/html,x", self.allowed) is False

    def test_data_url_safe_when_allowed(self) -> None:
        cfg = SanitizerConfig(strip_data_urls=False, allowed_protocols={"data"})
        s = DocSanitizer(cfg)
        assert s.is_safe_url("data:text/html,x", {"data"}) is True

    def test_case_insensitive_protocol(self) -> None:
        assert self.s.is_safe_url("HTTPS://x.com", self.allowed) is True


# ---------------------------------------------------------------------------
# Integration pipeline
# ---------------------------------------------------------------------------


class TestSanitizeIntegration:
    def test_default_removes_scripts_style_comments(self) -> None:
        s = DocSanitizer()
        text = "a<script>x</script>b<style>y</style>c<!-- d -->e"
        result = s.sanitize(text)
        assert result.sanitized == "abce"
        assert result.changed is True

    def test_returns_result_object(self) -> None:
        s = DocSanitizer()
        result = s.sanitize("hello")
        assert isinstance(result, SanitizationResult)
        assert result.original == "hello"

    def test_unchanged_when_no_match(self) -> None:
        s = DocSanitizer()
        result = s.sanitize("plain text")
        assert result.changed is False
        assert result.removed_items == []

    def test_records_removed_items(self) -> None:
        s = DocSanitizer()
        result = s.sanitize("<script>x</script>")
        assert "scripts" in result.removed_items

    def test_full_pipeline_all_rules(self) -> None:
        cfg = SanitizerConfig(
            rules=[
                SanitizationRule.REMOVE_SCRIPTS,
                SanitizationRule.REMOVE_STYLE,
                SanitizationRule.REMOVE_COMMENTS,
                SanitizationRule.STRIP_IMAGES,
                SanitizationRule.NORMALIZE_LINKS,
                SanitizationRule.STRIP_HTML,
            ]
        )
        s = DocSanitizer(cfg)
        text = (
            "<script>x</script>"
            "<style>y</style>"
            "<!-- comment -->"
            "![img](src.png)"
            "[bad](javascript:alert(1))"
            "<b>bold</b>"
        )
        result = s.sanitize(text)
        assert "<script>" not in result.sanitized
        assert "<style>" not in result.sanitized
        assert "<!--" not in result.sanitized
        assert "![" not in result.sanitized
        assert "javascript:" not in result.sanitized
        assert "<b>" not in result.sanitized

    def test_strip_html_keeps_allowed_in_pipeline(self) -> None:
        cfg = SanitizerConfig(
            rules=[SanitizationRule.STRIP_HTML],
            allowed_html_tags={"b"},
        )
        s = DocSanitizer(cfg)
        result = s.sanitize("<b>x</b><span>y</span>")
        assert result.sanitized == "<b>x</b>y"


# ---------------------------------------------------------------------------
# Batch
# ---------------------------------------------------------------------------


class TestSanitizeBatch:
    def test_batch_returns_list(self) -> None:
        s = DocSanitizer()
        out = s.sanitize_batch(["a", "b"])
        assert isinstance(out, list)
        assert len(out) == 2

    def test_batch_preserves_order(self) -> None:
        s = DocSanitizer()
        out = s.sanitize_batch(["x", "y", "z"])
        assert [r.original for r in out] == ["x", "y", "z"]

    def test_batch_empty(self) -> None:
        s = DocSanitizer()
        assert s.sanitize_batch([]) == []

    def test_batch_sanitizes_each(self) -> None:
        s = DocSanitizer()
        out = s.sanitize_batch(
            ["<script>x</script>", "<!-- c -->"]
        )
        assert all(r.changed for r in out)


# ---------------------------------------------------------------------------
# Selective rules
# ---------------------------------------------------------------------------


class TestSelectiveRules:
    def test_only_remove_scripts(self) -> None:
        cfg = SanitizerConfig(rules=[SanitizationRule.REMOVE_SCRIPTS])
        s = DocSanitizer(cfg)
        result = s.sanitize("<script>x</script><style>y</style>")
        assert "<script>" not in result.sanitized
        assert "<style>" in result.sanitized

    def test_only_escape_html(self) -> None:
        cfg = SanitizerConfig(rules=[SanitizationRule.ESCAPE_HTML])
        s = DocSanitizer(cfg)
        result = s.sanitize("<p>a</p>")
        assert "&lt;" in result.sanitized
        assert "&gt;" in result.sanitized

    def test_only_strip_images(self) -> None:
        cfg = SanitizerConfig(rules=[SanitizationRule.STRIP_IMAGES])
        s = DocSanitizer(cfg)
        result = s.sanitize("![alt](src)![b](c)")
        assert result.sanitized == ""

    def test_empty_rules_no_change(self) -> None:
        cfg = SanitizerConfig(rules=[])
        s = DocSanitizer(cfg)
        result = s.sanitize("<script>x</script>")
        assert result.changed is False

    def test_normalize_links_only(self) -> None:
        cfg = SanitizerConfig(rules=[SanitizationRule.NORMALIZE_LINKS])
        s = DocSanitizer(cfg)
        result = s.sanitize("[a](javascript:x)")
        assert result.sanitized == "[a](#)"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def setup_method(self) -> None:
        self.s = DocSanitizer()

    def test_empty_string(self) -> None:
        result = self.s.sanitize("")
        assert result.sanitized == ""
        assert result.changed is False

    def test_no_html_no_change(self) -> None:
        result = self.s.sanitize("just plain text")
        assert result.sanitized == "just plain text"
        assert result.changed is False

    def test_malformed_unclosed_tag(self) -> None:
        # Unclosed `<script>` without closing tag: pattern needs closing
        # so it should NOT be removed by remove_scripts.
        text = "<script>never closed"
        result = self.s.remove_scripts(text)
        # remains because pattern requires </script>
        assert result == text

    def test_unicode_preserved(self) -> None:
        text = "Привет <script>x</script> мир"
        result = self.s.sanitize(text)
        assert "Привет" in result.sanitized
        assert "мир" in result.sanitized
        assert "<script>" not in result.sanitized

    def test_nested_html_strip(self) -> None:
        assert self.s.strip_html("<div><p>x</p></div>") == "x"

    def test_long_text(self) -> None:
        text = "a" * 10_000 + "<script>x</script>" + "b" * 10_000
        result = self.s.sanitize(text)
        assert "<script>" not in result.sanitized
        assert len(result.sanitized) == 20_000

    def test_config_passed_through(self) -> None:
        cfg = SanitizerConfig(allowed_protocols={"http"})
        s = DocSanitizer(cfg)
        assert s.config.allowed_protocols == {"http"}

    def test_default_config_when_none(self) -> None:
        s = DocSanitizer(None)
        assert isinstance(s.config, SanitizerConfig)


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
