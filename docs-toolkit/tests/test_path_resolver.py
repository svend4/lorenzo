"""Tests for docstoolkit.path_resolver."""
from __future__ import annotations

import pytest

from docstoolkit.path_resolver import PathResolver, PathType, ResolvedPath


# ---------------------------------------------------------------------------
# PathType
# ---------------------------------------------------------------------------

class TestPathType:
    def test_members(self):
        assert PathType.ABSOLUTE.value == "absolute"
        assert PathType.RELATIVE.value == "relative"
        assert PathType.ANCHOR.value == "anchor"
        assert PathType.EXTERNAL.value == "external"
        assert PathType.INVALID.value == "invalid"

    def test_distinct(self):
        members = {p for p in PathType}
        assert len(members) == 5


# ---------------------------------------------------------------------------
# ResolvedPath
# ---------------------------------------------------------------------------

class TestResolvedPath:
    def test_fields(self):
        rp = ResolvedPath(
            original="a/b.md",
            resolved="a/b.md",
            path_type=PathType.RELATIVE,
            is_resolved=True,
            error=None,
        )
        assert rp.original == "a/b.md"
        assert rp.resolved == "a/b.md"
        assert rp.path_type == PathType.RELATIVE
        assert rp.is_resolved is True
        assert rp.error is None

    def test_default_is_resolved_false(self):
        rp = ResolvedPath(original="x", resolved="x", path_type=PathType.INVALID)
        assert rp.is_resolved is False
        assert rp.error is None

    def test_error_field(self):
        rp = ResolvedPath(
            original="",
            resolved="",
            path_type=PathType.INVALID,
            is_resolved=False,
            error="empty path",
        )
        assert rp.error == "empty path"


# ---------------------------------------------------------------------------
# is_absolute / is_external / is_anchor
# ---------------------------------------------------------------------------

class TestIsAbsolute:
    def setup_method(self):
        self.r = PathResolver()

    def test_absolute_path(self):
        assert self.r.is_absolute("/foo/bar.md") is True

    def test_relative_path(self):
        assert self.r.is_absolute("foo/bar.md") is False

    def test_dot_path(self):
        assert self.r.is_absolute("./foo.md") is False

    def test_empty(self):
        assert self.r.is_absolute("") is False


class TestIsExternal:
    def setup_method(self):
        self.r = PathResolver()

    def test_http(self):
        assert self.r.is_external("http://example.com") is True

    def test_https(self):
        assert self.r.is_external("https://example.com") is True

    def test_ftp(self):
        assert self.r.is_external("ftp://files.example.com") is True

    def test_mailto(self):
        assert self.r.is_external("mailto:user@example.com") is True

    def test_relative_not_external(self):
        assert self.r.is_external("foo/bar.md") is False

    def test_empty_not_external(self):
        assert self.r.is_external("") is False

    def test_case_insensitive(self):
        assert self.r.is_external("HTTPS://example.com") is True


class TestIsAnchor:
    def setup_method(self):
        self.r = PathResolver()

    def test_anchor(self):
        assert self.r.is_anchor("#section") is True

    def test_path_with_anchor(self):
        # path containing # but not starting → not anchor-only
        assert self.r.is_anchor("file.md#section") is False

    def test_empty(self):
        assert self.r.is_anchor("") is False


# ---------------------------------------------------------------------------
# resolve — absolute
# ---------------------------------------------------------------------------

class TestResolveAbsolute:
    def setup_method(self):
        self.r = PathResolver(base_dir="/project")

    def test_absolute(self):
        rp = self.r.resolve("/docs/file.md")
        assert rp.path_type == PathType.ABSOLUTE
        assert rp.is_resolved is True
        assert rp.resolved == "/docs/file.md"

    def test_absolute_with_dotdot(self):
        rp = self.r.resolve("/a/b/../c/file.md")
        assert rp.path_type == PathType.ABSOLUTE
        assert rp.resolved == "/a/c/file.md"

    def test_absolute_with_anchor(self):
        rp = self.r.resolve("/docs/file.md#section")
        assert rp.path_type == PathType.ABSOLUTE
        assert rp.resolved == "/docs/file.md#section"


# ---------------------------------------------------------------------------
# resolve — relative
# ---------------------------------------------------------------------------

class TestResolveRelative:
    def setup_method(self):
        self.r = PathResolver(base_dir=".")

    def test_simple_relative_no_from(self):
        rp = self.r.resolve("foo/bar.md")
        assert rp.path_type == PathType.RELATIVE
        assert rp.is_resolved is True
        assert rp.resolved == "foo/bar.md"

    def test_dot_prefix(self):
        rp = self.r.resolve("./foo.md")
        assert rp.path_type == PathType.RELATIVE
        assert rp.resolved == "foo.md"

    def test_dotdot_relative(self):
        rp = self.r.resolve("../foo.md", from_file="dir/source.md")
        assert rp.path_type == PathType.RELATIVE
        assert rp.resolved == "foo.md"

    def test_relative_from_file(self):
        rp = self.r.resolve("sibling.md", from_file="docs/source.md")
        assert rp.path_type == PathType.RELATIVE
        assert rp.resolved == "docs/sibling.md"

    def test_relative_with_anchor(self):
        rp = self.r.resolve("other.md#sec", from_file="docs/source.md")
        assert rp.path_type == PathType.RELATIVE
        assert rp.resolved == "docs/other.md#sec"

    def test_nested_relative(self):
        rp = self.r.resolve("sub/deep.md", from_file="a/b/c.md")
        assert rp.path_type == PathType.RELATIVE
        assert rp.resolved == "a/b/sub/deep.md"

    def test_dotdot_dotdot(self):
        rp = self.r.resolve("../../top.md", from_file="a/b/c.md")
        assert rp.path_type == PathType.RELATIVE
        assert rp.resolved == "top.md"

    def test_relative_uses_base_dir(self):
        r = PathResolver(base_dir="root/docs")
        rp = r.resolve("file.md")
        assert rp.path_type == PathType.RELATIVE
        assert rp.resolved == "root/docs/file.md"


# ---------------------------------------------------------------------------
# resolve — external
# ---------------------------------------------------------------------------

class TestResolveExternal:
    def setup_method(self):
        self.r = PathResolver()

    def test_http_unchanged(self):
        rp = self.r.resolve("http://example.com/path")
        assert rp.path_type == PathType.EXTERNAL
        assert rp.is_resolved is True
        assert rp.resolved == "http://example.com/path"

    def test_https_unchanged(self):
        rp = self.r.resolve("https://example.com/")
        assert rp.path_type == PathType.EXTERNAL
        assert rp.resolved == "https://example.com/"

    def test_mailto_unchanged(self):
        rp = self.r.resolve("mailto:foo@bar.com")
        assert rp.path_type == PathType.EXTERNAL
        assert rp.resolved == "mailto:foo@bar.com"

    def test_ftp_unchanged(self):
        rp = self.r.resolve("ftp://files.example.com/x")
        assert rp.path_type == PathType.EXTERNAL
        assert rp.resolved == "ftp://files.example.com/x"


# ---------------------------------------------------------------------------
# resolve — anchor
# ---------------------------------------------------------------------------

class TestResolveAnchor:
    def setup_method(self):
        self.r = PathResolver()

    def test_anchor_no_from(self):
        rp = self.r.resolve("#section")
        assert rp.path_type == PathType.ANCHOR
        assert rp.is_resolved is True
        assert rp.resolved == "#section"

    def test_anchor_with_from_file(self):
        rp = self.r.resolve("#section", from_file="docs/index.md")
        assert rp.path_type == PathType.ANCHOR
        assert rp.resolved == "docs/index.md#section"

    def test_empty_anchor(self):
        rp = self.r.resolve("#")
        assert rp.path_type == PathType.ANCHOR
        assert rp.resolved == "#"


# ---------------------------------------------------------------------------
# resolve_all
# ---------------------------------------------------------------------------

class TestResolveAll:
    def setup_method(self):
        self.r = PathResolver()

    def test_resolve_all_mixed(self):
        results = self.r.resolve_all(
            ["http://x.com", "#sec", "/abs.md", "rel.md"],
            from_file="src.md",
        )
        assert len(results) == 4
        assert results[0].path_type == PathType.EXTERNAL
        assert results[1].path_type == PathType.ANCHOR
        assert results[2].path_type == PathType.ABSOLUTE
        assert results[3].path_type == PathType.RELATIVE

    def test_resolve_all_empty_list(self):
        assert self.r.resolve_all([]) == []

    def test_resolve_all_preserves_order(self):
        paths = ["a.md", "b.md", "c.md"]
        results = self.r.resolve_all(paths)
        assert [r.original for r in results] == paths


# ---------------------------------------------------------------------------
# relative_to
# ---------------------------------------------------------------------------

class TestRelativeTo:
    def setup_method(self):
        self.r = PathResolver()

    def test_sibling(self):
        rel = self.r.relative_to("docs/b.md", "docs/a.md")
        assert rel == "b.md"

    def test_up_one(self):
        rel = self.r.relative_to("top.md", "sub/a.md")
        assert rel == "../top.md"

    def test_down_one(self):
        rel = self.r.relative_to("a/sub/x.md", "a/b.md")
        assert rel == "sub/x.md"

    def test_same_dir_different_subtree(self):
        rel = self.r.relative_to("x/c.md", "y/a.md")
        assert rel == "../x/c.md"

    def test_self(self):
        rel = self.r.relative_to("a/b.md", "a/b.md")
        # relpath of same file against its own dir → "b.md"
        assert rel == "b.md"


# ---------------------------------------------------------------------------
# normalize
# ---------------------------------------------------------------------------

class TestNormalize:
    def setup_method(self):
        self.r = PathResolver()

    def test_dotdot(self):
        assert self.r.normalize("a/b/../c") == "a/c"

    def test_dot(self):
        assert self.r.normalize("a/./b") == "a/b"

    def test_double_slashes(self):
        assert self.r.normalize("a//b") == "a/b"

    def test_empty(self):
        assert self.r.normalize("") == ""

    def test_backslashes(self):
        assert self.r.normalize("a\\b\\c") == "a/b/c"

    def test_absolute_preserved(self):
        assert self.r.normalize("/a/b") == "/a/b"


# ---------------------------------------------------------------------------
# join
# ---------------------------------------------------------------------------

class TestJoin:
    def setup_method(self):
        self.r = PathResolver()

    def test_simple(self):
        assert self.r.join("a", "b", "c.md") == "a/b/c.md"

    def test_with_trailing_slash(self):
        assert self.r.join("a/", "b.md") == "a/b.md"

    def test_absolute_resets(self):
        # posix join: absolute part resets — that's expected behavior
        assert self.r.join("a", "/b", "c") == "/b/c"

    def test_empty_parts(self):
        assert self.r.join() == ""


# ---------------------------------------------------------------------------
# parent_dir
# ---------------------------------------------------------------------------

class TestParentDir:
    def setup_method(self):
        self.r = PathResolver()

    def test_nested(self):
        assert self.r.parent_dir("a/b/c.md") == "a/b"

    def test_top(self):
        assert self.r.parent_dir("file.md") == ""

    def test_absolute(self):
        assert self.r.parent_dir("/a/b.md") == "/a"

    def test_empty(self):
        assert self.r.parent_dir("") == ""


# ---------------------------------------------------------------------------
# with_suffix
# ---------------------------------------------------------------------------

class TestWithSuffix:
    def setup_method(self):
        self.r = PathResolver()

    def test_change_extension(self):
        assert self.r.with_suffix("a/b/c.md", ".html") == "a/b/c.html"

    def test_change_extension_no_dot(self):
        assert self.r.with_suffix("a/b/c.md", "html") == "a/b/c.html"

    def test_no_existing_extension(self):
        assert self.r.with_suffix("README", ".md") == "README.md"

    def test_strip_extension(self):
        assert self.r.with_suffix("a/b/c.md", "") == "a/b/c"

    def test_root_file(self):
        assert self.r.with_suffix("file.txt", ".md") == "file.md"


# ---------------------------------------------------------------------------
# extract_anchor
# ---------------------------------------------------------------------------

class TestExtractAnchor:
    def setup_method(self):
        self.r = PathResolver()

    def test_with_anchor(self):
        assert self.r.extract_anchor("file.md#section") == ("file.md", "section")

    def test_without_anchor(self):
        assert self.r.extract_anchor("file.md") == ("file.md", None)

    def test_only_anchor(self):
        assert self.r.extract_anchor("#section") == ("", "section")

    def test_empty(self):
        assert self.r.extract_anchor("") == ("", None)

    def test_anchor_with_dashes(self):
        assert self.r.extract_anchor("doc.md#sub-section-1") == (
            "doc.md",
            "sub-section-1",
        )

    def test_empty_anchor(self):
        path, anchor = self.r.extract_anchor("file.md#")
        assert path == "file.md"
        assert anchor == ""


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def setup_method(self):
        self.r = PathResolver()

    def test_resolve_empty_path(self):
        rp = self.r.resolve("")
        assert rp.path_type == PathType.INVALID
        assert rp.is_resolved is False
        assert rp.error is not None

    def test_resolve_none_path(self):
        rp = self.r.resolve(None)
        assert rp.path_type == PathType.INVALID
        assert rp.is_resolved is False

    def test_root_path(self):
        rp = self.r.resolve("/")
        assert rp.path_type == PathType.ABSOLUTE
        assert rp.is_resolved is True

    def test_only_anchor_no_from(self):
        rp = self.r.resolve("#")
        assert rp.path_type == PathType.ANCHOR
        assert rp.resolved == "#"

    def test_base_dir_normalized(self):
        r = PathResolver(base_dir="root/./sub/../docs")
        assert r.base_dir == "root/docs"

    def test_default_base_dir(self):
        r = PathResolver()
        assert r.base_dir == "."

    def test_resolve_external_with_anchor_in_url(self):
        rp = self.r.resolve("https://example.com/page#section")
        # External wins — full URL preserved
        assert rp.path_type == PathType.EXTERNAL
        assert rp.resolved == "https://example.com/page#section"
