"""Tests for docstoolkit.doc_image_meta (E221)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_image_meta import (
    DocImageMeta,
    ImageRef,
    ImageReport,
    ImageUsage,
)


@pytest.fixture
def dim() -> DocImageMeta:
    return DocImageMeta()


# ---------------------------------------------------------------------------
class TestImageRef:
    def test_defaults(self):
        r = ImageRef(url="img.png")
        assert r.url == "img.png"
        assert r.alt_text == ""
        assert r.title == ""
        assert r.is_remote is False
        assert r.line_num == 0

    def test_all_fields(self):
        r = ImageRef(
            url="https://example.com/a.png",
            alt_text="alt",
            title="t",
            is_remote=True,
            line_num=12,
        )
        assert r.url == "https://example.com/a.png"
        assert r.alt_text == "alt"
        assert r.title == "t"
        assert r.is_remote is True
        assert r.line_num == 12


# ---------------------------------------------------------------------------
class TestImageReport:
    def _report(self) -> ImageReport:
        return ImageReport(
            doc_id="d1",
            images=[
                ImageRef(url="a.png", alt_text="A", is_remote=False),
                ImageRef(url="b.png", alt_text="", is_remote=False),
                ImageRef(url="https://x/c.png", alt_text="C", is_remote=True),
                ImageRef(url="a.png", alt_text="A2", is_remote=False),
            ],
        )

    def test_image_count(self):
        assert self._report().image_count == 4

    def test_missing_alt_count(self):
        assert self._report().missing_alt_count == 1

    def test_remote_count(self):
        assert self._report().remote_count == 1

    def test_local_count(self):
        assert self._report().local_count == 3

    def test_unique_urls(self):
        assert self._report().unique_urls == {"a.png", "b.png", "https://x/c.png"}

    def test_empty_report(self):
        r = ImageReport(doc_id="x")
        assert r.image_count == 0
        assert r.missing_alt_count == 0
        assert r.remote_count == 0
        assert r.local_count == 0
        assert r.unique_urls == set()


# ---------------------------------------------------------------------------
class TestImageUsage:
    def test_defaults(self):
        u = ImageUsage(url="a.png")
        assert u.url == "a.png"
        assert u.doc_ids == set()
        assert u.usage_count == 0

    def test_with_values(self):
        u = ImageUsage(url="a.png", doc_ids={"d1", "d2"}, usage_count=3)
        assert u.doc_ids == {"d1", "d2"}
        assert u.usage_count == 3


# ---------------------------------------------------------------------------
class TestScan:
    def test_scan_returns_report(self, dim):
        rep = dim.scan("d1", "![a](one.png) and ![b](two.png)")
        assert isinstance(rep, ImageReport)
        assert rep.doc_id == "d1"
        assert rep.image_count == 2

    def test_scan_updates_usage_index(self, dim):
        dim.scan("d1", "![a](one.png)")
        u = dim.usage("one.png")
        assert u is not None
        assert u.usage_count == 1
        assert "d1" in u.doc_ids

    def test_scan_replaces_previous_for_doc(self, dim):
        dim.scan("d1", "![a](one.png) ![b](two.png)")
        dim.scan("d1", "![a](one.png)")  # only one now
        assert dim.usage("two.png") is None
        u = dim.usage("one.png")
        assert u.usage_count == 1

    def test_scan_empty_content(self, dim):
        rep = dim.scan("d1", "")
        assert rep.image_count == 0

    def test_scan_no_images(self, dim):
        rep = dim.scan("d1", "Just some text [a link](http://x).")
        assert rep.image_count == 0


# ---------------------------------------------------------------------------
class TestScanBatch:
    def test_scan_batch_basic(self, dim):
        docs = {
            "d1": "![a](one.png)",
            "d2": "![b](two.png) ![c](one.png)",
        }
        reports = dim.scan_batch(docs)
        assert len(reports) == 2
        ids = {r.doc_id for r in reports}
        assert ids == {"d1", "d2"}

    def test_scan_batch_empty(self, dim):
        assert dim.scan_batch({}) == []

    def test_scan_batch_aggregates_usage(self, dim):
        dim.scan_batch({
            "d1": "![](shared.png)",
            "d2": "![](shared.png)",
        })
        u = dim.usage("shared.png")
        assert u.usage_count == 2
        assert u.doc_ids == {"d1", "d2"}


# ---------------------------------------------------------------------------
class TestExtractImages:
    def test_simple(self, dim):
        refs = dim.extract_images("![alt](x.png)")
        assert len(refs) == 1
        assert refs[0].url == "x.png"
        assert refs[0].alt_text == "alt"
        assert refs[0].title == ""
        assert refs[0].is_remote is False

    def test_with_title(self, dim):
        refs = dim.extract_images('![alt](x.png "the title")')
        assert refs[0].title == "the title"

    def test_remote_http(self, dim):
        refs = dim.extract_images("![](http://x/y.png)")
        assert refs[0].is_remote is True

    def test_remote_https(self, dim):
        refs = dim.extract_images("![](https://x/y.png)")
        assert refs[0].is_remote is True

    def test_local(self, dim):
        refs = dim.extract_images("![](./local/path.png)")
        assert refs[0].is_remote is False

    def test_line_numbers(self, dim):
        content = "line1\nline2 ![a](one.png)\nline3\n![b](two.png)"
        refs = dim.extract_images(content)
        assert refs[0].line_num == 2
        assert refs[1].line_num == 4

    def test_empty_alt(self, dim):
        refs = dim.extract_images("![](x.png)")
        assert refs[0].alt_text == ""

    def test_no_images(self, dim):
        assert dim.extract_images("plain text [link](u)") == []

    def test_empty_content(self, dim):
        assert dim.extract_images("") == []

    def test_multiple_in_one_line(self, dim):
        refs = dim.extract_images("![a](1.png) text ![b](2.png) ![c](3.png)")
        assert [r.url for r in refs] == ["1.png", "2.png", "3.png"]


# ---------------------------------------------------------------------------
class TestUsage:
    def test_known_url(self, dim):
        dim.scan("d1", "![a](one.png)")
        u = dim.usage("one.png")
        assert u is not None
        assert u.url == "one.png"

    def test_unknown_url(self, dim):
        assert dim.usage("nope.png") is None

    def test_usage_returns_copy(self, dim):
        dim.scan("d1", "![a](one.png)")
        u = dim.usage("one.png")
        u.doc_ids.add("hacker")
        # internal state not affected
        u2 = dim.usage("one.png")
        assert "hacker" not in u2.doc_ids


# ---------------------------------------------------------------------------
class TestAllUsage:
    def test_empty(self, dim):
        assert dim.all_usage() == []

    def test_returns_all(self, dim):
        dim.scan("d1", "![](a.png) ![](b.png)")
        dim.scan("d2", "![](b.png)")
        usages = dim.all_usage()
        urls = {u.url for u in usages}
        assert urls == {"a.png", "b.png"}

    def test_usage_count_correct(self, dim):
        dim.scan("d1", "![](a.png) ![](a.png)")
        dim.scan("d2", "![](a.png)")
        u = dim.usage("a.png")
        assert u.usage_count == 3
        assert u.doc_ids == {"d1", "d2"}


# ---------------------------------------------------------------------------
class TestUnusedImages:
    def test_finds_unused(self, dim):
        dim.scan("d1", "![](a.png) ![](b.png) ![](c.png)")
        unused = dim.unused_images(used_urls={"a.png"})
        assert set(unused) == {"b.png", "c.png"}

    def test_none_unused(self, dim):
        dim.scan("d1", "![](a.png)")
        assert dim.unused_images({"a.png"}) == []

    def test_all_unused_when_empty_used(self, dim):
        dim.scan("d1", "![](a.png) ![](b.png)")
        assert set(dim.unused_images(set())) == {"a.png", "b.png"}


# ---------------------------------------------------------------------------
class TestDocsUsing:
    def test_multiple_docs(self, dim):
        dim.scan("d1", "![](a.png)")
        dim.scan("d2", "![](a.png)")
        assert sorted(dim.docs_using("a.png")) == ["d1", "d2"]

    def test_unknown_url(self, dim):
        assert dim.docs_using("nope.png") == []

    def test_single_doc(self, dim):
        dim.scan("d1", "![](a.png)")
        assert dim.docs_using("a.png") == ["d1"]


# ---------------------------------------------------------------------------
class TestValidateAlt:
    def test_finds_empty_alt(self, dim):
        rep = dim.scan("d1", "![](a.png) ![alt](b.png) ![](c.png)")
        bad = dim.validate_alt(rep)
        assert {r.url for r in bad} == {"a.png", "c.png"}

    def test_no_missing(self, dim):
        rep = dim.scan("d1", "![ok](a.png)")
        assert dim.validate_alt(rep) == []

    def test_empty_report(self, dim):
        rep = ImageReport(doc_id="x")
        assert dim.validate_alt(rep) == []


# ---------------------------------------------------------------------------
class TestTopUsed:
    def test_orders_by_count(self, dim):
        dim.scan("d1", "![](a.png) ![](a.png) ![](b.png)")
        dim.scan("d2", "![](a.png) ![](c.png)")
        top = dim.top_used(top_k=10)
        # a.png used 3 times, b.png used 1, c.png used 1
        assert top[0].url == "a.png"
        assert top[0].usage_count == 3

    def test_respects_top_k(self, dim):
        dim.scan("d1", "![](a.png) ![](b.png) ![](c.png)")
        assert len(dim.top_used(top_k=2)) == 2

    def test_zero_top_k(self, dim):
        dim.scan("d1", "![](a.png)")
        assert dim.top_used(top_k=0) == []

    def test_empty_index(self, dim):
        assert dim.top_used() == []


# ---------------------------------------------------------------------------
class TestRemoveDoc:
    def test_removes_refs(self, dim):
        dim.scan("d1", "![](a.png) ![](b.png)")
        removed = dim.remove_doc("d1")
        assert removed == 2
        assert dim.usage("a.png") is None
        assert dim.usage("b.png") is None

    def test_only_decrements_when_shared(self, dim):
        dim.scan("d1", "![](shared.png)")
        dim.scan("d2", "![](shared.png)")
        dim.remove_doc("d1")
        u = dim.usage("shared.png")
        assert u is not None
        assert u.usage_count == 1
        assert u.doc_ids == {"d2"}

    def test_unknown_doc(self, dim):
        assert dim.remove_doc("nope") == 0

    def test_doc_no_longer_listed(self, dim):
        dim.scan("d1", "![](a.png)")
        dim.remove_doc("d1")
        assert dim.docs_using("a.png") == []


# ---------------------------------------------------------------------------
class TestTotalUniqueUrls:
    def test_empty(self, dim):
        assert dim.total_unique_urls() == 0

    def test_counts_unique(self, dim):
        dim.scan("d1", "![](a.png) ![](a.png) ![](b.png)")
        assert dim.total_unique_urls() == 2


# ---------------------------------------------------------------------------
class TestTotalDocImageRefs:
    def test_empty(self, dim):
        assert dim.total_doc_image_refs() == 0

    def test_counts_all_refs(self, dim):
        dim.scan("d1", "![](a.png) ![](a.png)")
        dim.scan("d2", "![](a.png) ![](b.png)")
        assert dim.total_doc_image_refs() == 4


# ---------------------------------------------------------------------------
class TestClear:
    def test_clears_everything(self, dim):
        dim.scan("d1", "![](a.png) ![](b.png)")
        dim.clear()
        assert dim.total_unique_urls() == 0
        assert dim.total_doc_image_refs() == 0
        assert dim.all_usage() == []

    def test_clear_when_empty(self, dim):
        dim.clear()
        assert dim.total_unique_urls() == 0


# ---------------------------------------------------------------------------
class TestImageStats:
    def test_empty(self, dim):
        s = dim.image_stats()
        assert s["total"] == 0
        assert s["remote"] == 0
        assert s["local"] == 0
        assert s["missing_alt"] == 0

    def test_full(self, dim):
        dim.scan("d1", "![alt](a.png) ![](b.png) ![alt](https://x/c.png)")
        s = dim.image_stats()
        assert s["total"] == 3
        assert s["remote"] == 1
        assert s["local"] == 2
        assert s["missing_alt"] == 1


# ---------------------------------------------------------------------------
class TestIsRemoteDetection:
    def test_http(self, dim):
        refs = dim.extract_images("![](http://x.com/a.png)")
        assert refs[0].is_remote is True

    def test_https(self, dim):
        refs = dim.extract_images("![](https://x.com/a.png)")
        assert refs[0].is_remote is True

    def test_relative(self, dim):
        refs = dim.extract_images("![](./a.png)")
        assert refs[0].is_remote is False

    def test_absolute_local(self, dim):
        refs = dim.extract_images("![](/abs/a.png)")
        assert refs[0].is_remote is False

    def test_ftp_not_remote_per_spec(self, dim):
        # Per spec is_remote is http/https only.
        refs = dim.extract_images("![](ftp://x/a.png)")
        assert refs[0].is_remote is False


# ---------------------------------------------------------------------------
class TestAltText:
    def test_captured(self, dim):
        refs = dim.extract_images("![hello world](a.png)")
        assert refs[0].alt_text == "hello world"

    def test_empty(self, dim):
        refs = dim.extract_images("![](a.png)")
        assert refs[0].alt_text == ""

    def test_with_spaces(self, dim):
        refs = dim.extract_images("![  spaced  ](a.png)")
        assert refs[0].alt_text == "  spaced  "


# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_thread_safety(self, dim):
        def worker(i):
            dim.scan(f"d{i}", f"![]({i}.png) ![](shared.png)")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        u = dim.usage("shared.png")
        assert u is not None
        assert u.usage_count == 20
        assert len(u.doc_ids) == 20

    def test_rescan_same_doc_does_not_double_count(self, dim):
        dim.scan("d1", "![](a.png)")
        dim.scan("d1", "![](a.png)")
        u = dim.usage("a.png")
        assert u.usage_count == 1

    def test_duplicate_images_same_doc(self, dim):
        dim.scan("d1", "![](a.png) ![](a.png) ![](a.png)")
        u = dim.usage("a.png")
        assert u.usage_count == 3
        assert u.doc_ids == {"d1"}

    def test_image_with_title_and_alt(self, dim):
        refs = dim.extract_images('![alt text](a.png "the title")')
        assert refs[0].alt_text == "alt text"
        assert refs[0].title == "the title"
        assert refs[0].url == "a.png"

    def test_mixed_remote_local(self, dim):
        dim.scan("d1", "![](https://x/a.png) ![](./b.png)")
        s = dim.image_stats()
        assert s["remote"] == 1
        assert s["local"] == 1

    def test_not_an_image_just_link(self, dim):
        # No leading "!" — should not match.
        refs = dim.extract_images("[not an image](x.png)")
        assert refs == []

    def test_image_at_start_of_file(self, dim):
        refs = dim.extract_images("![first](a.png) more text")
        assert refs[0].line_num == 1
