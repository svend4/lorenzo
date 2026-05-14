"""Tests for docstoolkit.doc_link_check."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_link_check import (
    CheckReport,
    CheckResult,
    DocLinkCheck,
    LinkRef,
    LinkStatus,
)
from docstoolkit.doc_link_check.checker import stub_checker


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TestLinkStatus:
    def test_has_valid(self):
        assert LinkStatus.VALID.value == "valid"

    def test_has_broken(self):
        assert LinkStatus.BROKEN.value == "broken"

    def test_has_redirect(self):
        assert LinkStatus.REDIRECT.value == "redirect"

    def test_has_unknown(self):
        assert LinkStatus.UNKNOWN.value == "unknown"

    def test_has_skipped(self):
        assert LinkStatus.SKIPPED.value == "skipped"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

class TestLinkRef:
    def test_minimal_construction(self):
        ref = LinkRef(url="https://example.com", source_doc_id="doc1")
        assert ref.url == "https://example.com"
        assert ref.source_doc_id == "doc1"

    def test_default_line_num(self):
        ref = LinkRef(url="u", source_doc_id="d")
        assert ref.line_num == 0

    def test_default_link_text(self):
        ref = LinkRef(url="u", source_doc_id="d")
        assert ref.link_text == ""

    def test_full_construction(self):
        ref = LinkRef(url="u", source_doc_id="d", line_num=5, link_text="hi")
        assert ref.line_num == 5
        assert ref.link_text == "hi"


class TestCheckResult:
    def test_minimal(self):
        r = CheckResult(url="u", status=LinkStatus.VALID)
        assert r.url == "u"
        assert r.status == LinkStatus.VALID

    def test_defaults(self):
        r = CheckResult(url="u", status=LinkStatus.VALID)
        assert r.checked_at == 0.0
        assert r.error is None
        assert r.final_url is None
        assert r.latency_ms == 0.0

    def test_full(self):
        r = CheckResult(
            url="u",
            status=LinkStatus.REDIRECT,
            checked_at=100.0,
            error=None,
            final_url="u2",
            latency_ms=12.5,
        )
        assert r.checked_at == 100.0
        assert r.final_url == "u2"
        assert r.latency_ms == 12.5


class TestCheckReport:
    def test_defaults(self):
        rep = CheckReport()
        assert rep.total_links == 0
        assert rep.valid_count == 0
        assert rep.broken_count == 0
        assert rep.unknown_count == 0
        assert rep.by_doc == {}
        assert rep.broken_links == []

    def test_set_fields(self):
        rep = CheckReport(total_links=5, valid_count=3, broken_count=1, unknown_count=1)
        assert rep.total_links == 5
        assert rep.valid_count == 3


# ---------------------------------------------------------------------------
# register_doc
# ---------------------------------------------------------------------------

class TestRegisterDoc:
    def test_register_returns_count(self):
        c = DocLinkCheck()
        content = "[a](http://a) and [b](http://b)"
        assert c.register_doc("doc1", content) == 2

    def test_register_empty_doc(self):
        c = DocLinkCheck()
        assert c.register_doc("doc1", "no links here") == 0

    def test_register_stores_links(self):
        c = DocLinkCheck()
        c.register_doc("doc1", "[a](http://a)")
        assert c.total_links == 1

    def test_register_overwrites(self):
        c = DocLinkCheck()
        c.register_doc("doc1", "[a](http://a) [b](http://b)")
        c.register_doc("doc1", "[c](http://c)")
        assert c.links_for_doc("doc1")[0].url == "http://c"
        assert len(c.links_for_doc("doc1")) == 1

    def test_register_multiple_docs(self):
        c = DocLinkCheck()
        c.register_doc("a", "[x](u1)")
        c.register_doc("b", "[y](u2)")
        assert c.total_docs == 2


# ---------------------------------------------------------------------------
# unregister_doc
# ---------------------------------------------------------------------------

class TestUnregisterDoc:
    def test_unregister_existing(self):
        c = DocLinkCheck()
        c.register_doc("doc1", "[a](u)")
        assert c.unregister_doc("doc1") is True

    def test_unregister_missing(self):
        c = DocLinkCheck()
        assert c.unregister_doc("missing") is False

    def test_unregister_decreases_total(self):
        c = DocLinkCheck()
        c.register_doc("doc1", "[a](u)")
        c.unregister_doc("doc1")
        assert c.total_docs == 0
        assert c.total_links == 0


# ---------------------------------------------------------------------------
# extract_links
# ---------------------------------------------------------------------------

class TestExtractLinks:
    def test_single_link(self):
        c = DocLinkCheck()
        assert c.extract_links("[t](http://a)") == ["http://a"]

    def test_multiple_links(self):
        c = DocLinkCheck()
        urls = c.extract_links("[a](u1) and [b](u2)")
        assert urls == ["u1", "u2"]

    def test_no_links(self):
        c = DocLinkCheck()
        assert c.extract_links("no links") == []

    def test_ignores_images(self):
        c = DocLinkCheck()
        # Image syntax ![alt](url) should be skipped.
        urls = c.extract_links("![img](pic.png) and [link](u)")
        assert urls == ["u"]

    def test_strips_whitespace(self):
        c = DocLinkCheck()
        urls = c.extract_links("[a]( spaced )")
        assert urls == ["spaced"]

    def test_link_order_preserved(self):
        c = DocLinkCheck()
        urls = c.extract_links("[a](one) [b](two) [c](three)")
        assert urls == ["one", "two", "three"]


# ---------------------------------------------------------------------------
# check_link
# ---------------------------------------------------------------------------

class TestCheckLink:
    def test_valid_link(self):
        c = DocLinkCheck()
        r = c.check_link("http://ok")
        assert r.status == LinkStatus.VALID

    def test_broken_link(self):
        c = DocLinkCheck()
        r = c.check_link("broken:err")
        assert r.status == LinkStatus.BROKEN

    def test_increments_checks_run(self):
        c = DocLinkCheck()
        c.check_link("http://a")
        assert c.total_checks_run == 1

    def test_sets_checked_at(self):
        c = DocLinkCheck()
        r = c.check_link("http://a", now=100.0)
        assert r.checked_at == 100.0

    def test_skipped_url_returns_skipped(self):
        c = DocLinkCheck()
        c.skip_url("http://skip")
        r = c.check_link("http://skip")
        assert r.status == LinkStatus.SKIPPED

    def test_skipped_does_not_call_checker(self):
        calls: list[str] = []

        def checker(u: str) -> CheckResult:
            calls.append(u)
            return CheckResult(url=u, status=LinkStatus.VALID)

        c = DocLinkCheck(checker=checker)
        c.skip_url("http://x")
        c.check_link("http://x")
        assert calls == []


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

class TestCheckLinkCache:
    def test_cached_within_ttl(self):
        calls: list[str] = []

        def checker(u: str) -> CheckResult:
            calls.append(u)
            return CheckResult(url=u, status=LinkStatus.VALID)

        c = DocLinkCheck(checker=checker, cache_ttl=100.0)
        c.check_link("http://a", now=0.0)
        c.check_link("http://a", now=50.0)
        assert len(calls) == 1

    def test_expired_cache_re_checks(self):
        calls: list[str] = []

        def checker(u: str) -> CheckResult:
            calls.append(u)
            return CheckResult(url=u, status=LinkStatus.VALID)

        c = DocLinkCheck(checker=checker, cache_ttl=10.0)
        c.check_link("http://a", now=0.0)
        # cache expires at 10.0 — at now=20.0 cache is expired
        c.check_link("http://a", now=20.0)
        assert len(calls) == 2

    def test_cache_records_separate_urls(self):
        c = DocLinkCheck()
        c.check_link("http://a", now=0.0)
        c.check_link("http://b", now=0.0)
        assert c.total_checks_run == 2

    def test_cache_hit_does_not_increment_checks_run(self):
        c = DocLinkCheck(cache_ttl=100.0)
        c.check_link("http://a", now=0.0)
        c.check_link("http://a", now=10.0)
        assert c.total_checks_run == 1


class TestCheckLinkForce:
    def test_force_bypasses_cache(self):
        calls: list[str] = []

        def checker(u: str) -> CheckResult:
            calls.append(u)
            return CheckResult(url=u, status=LinkStatus.VALID)

        c = DocLinkCheck(checker=checker, cache_ttl=1000.0)
        c.check_link("http://a", now=0.0)
        c.check_link("http://a", now=10.0, force=True)
        assert len(calls) == 2

    def test_force_updates_cache(self):
        # First call returns VALID, then we swap checker to BROKEN and force-recheck.
        c = DocLinkCheck(cache_ttl=1000.0)
        c.check_link("http://a", now=0.0)

        def broken_checker(u: str) -> CheckResult:
            return CheckResult(url=u, status=LinkStatus.BROKEN)

        c.set_checker(broken_checker)
        r = c.check_link("http://a", now=10.0, force=True)
        assert r.status == LinkStatus.BROKEN
        # Cached as broken too.
        assert c.cached_result("http://a", now=10.0).status == LinkStatus.BROKEN


# ---------------------------------------------------------------------------
# check_all_links
# ---------------------------------------------------------------------------

class TestCheckAllLinks:
    def test_empty_returns_empty_report(self):
        c = DocLinkCheck()
        rep = c.check_all_links()
        assert rep.total_links == 0
        assert rep.by_doc == {}

    def test_counts_valid_and_broken(self):
        c = DocLinkCheck()
        c.register_doc("d1", "[a](http://ok) [b](broken:bad)")
        rep = c.check_all_links()
        assert rep.total_links == 2
        assert rep.valid_count == 1
        assert rep.broken_count == 1

    def test_broken_links_listed(self):
        c = DocLinkCheck()
        c.register_doc("d1", "[a](broken:1)")
        rep = c.check_all_links()
        assert len(rep.broken_links) == 1
        assert rep.broken_links[0].url == "broken:1"
        assert rep.broken_links[0].source_doc_id == "d1"

    def test_by_doc_groups(self):
        c = DocLinkCheck()
        c.register_doc("d1", "[a](u1)")
        c.register_doc("d2", "[b](u2)")
        rep = c.check_all_links()
        assert set(rep.by_doc.keys()) == {"d1", "d2"}
        assert len(rep.by_doc["d1"]) == 1
        assert len(rep.by_doc["d2"]) == 1

    def test_skipped_not_counted_as_broken(self):
        c = DocLinkCheck()
        c.skip_url("http://skip")
        c.register_doc("d1", "[a](http://skip)")
        rep = c.check_all_links()
        assert rep.broken_count == 0
        assert rep.valid_count == 0


# ---------------------------------------------------------------------------
# check_doc
# ---------------------------------------------------------------------------

class TestCheckDoc:
    def test_returns_results(self):
        c = DocLinkCheck()
        c.register_doc("d1", "[a](u1) [b](u2)")
        results = c.check_doc("d1")
        assert len(results) == 2
        assert all(isinstance(r, CheckResult) for r in results)

    def test_unknown_doc_returns_empty(self):
        c = DocLinkCheck()
        assert c.check_doc("missing") == []

    def test_uses_cache(self):
        calls: list[str] = []

        def checker(u: str) -> CheckResult:
            calls.append(u)
            return CheckResult(url=u, status=LinkStatus.VALID)

        c = DocLinkCheck(checker=checker, cache_ttl=100.0)
        c.register_doc("d1", "[a](u1)")
        c.check_doc("d1", now=0.0)
        c.check_doc("d1", now=10.0)
        assert len(calls) == 1


# ---------------------------------------------------------------------------
# links_for_doc
# ---------------------------------------------------------------------------

class TestLinksForDoc:
    def test_returns_refs(self):
        c = DocLinkCheck()
        c.register_doc("d1", "[hello](http://h)")
        refs = c.links_for_doc("d1")
        assert len(refs) == 1
        assert refs[0].url == "http://h"
        assert refs[0].link_text == "hello"

    def test_missing_doc_empty(self):
        c = DocLinkCheck()
        assert c.links_for_doc("missing") == []

    def test_returns_copy(self):
        c = DocLinkCheck()
        c.register_doc("d1", "[a](u)")
        refs = c.links_for_doc("d1")
        refs.clear()
        assert len(c.links_for_doc("d1")) == 1

    def test_line_numbers_tracked(self):
        c = DocLinkCheck()
        content = "line1\nline2 [a](u)\nline3"
        c.register_doc("d1", content)
        refs = c.links_for_doc("d1")
        assert refs[0].line_num == 2


# ---------------------------------------------------------------------------
# broken_links_for_doc
# ---------------------------------------------------------------------------

class TestBrokenLinksForDoc:
    def test_empty_without_check(self):
        c = DocLinkCheck()
        c.register_doc("d1", "[a](broken:x)")
        assert c.broken_links_for_doc("d1") == []

    def test_after_check_lists_broken(self):
        c = DocLinkCheck()
        c.register_doc("d1", "[a](broken:x) [b](http://ok)")
        c.check_doc("d1")
        broken = c.broken_links_for_doc("d1")
        assert len(broken) == 1
        assert broken[0].url == "broken:x"

    def test_unknown_doc(self):
        c = DocLinkCheck()
        assert c.broken_links_for_doc("missing") == []


# ---------------------------------------------------------------------------
# cached_result
# ---------------------------------------------------------------------------

class TestCachedResult:
    def test_no_cache_returns_none(self):
        c = DocLinkCheck()
        assert c.cached_result("http://a") is None

    def test_after_check_returns_cached(self):
        c = DocLinkCheck(cache_ttl=100.0)
        c.check_link("http://a", now=0.0)
        r = c.cached_result("http://a", now=10.0)
        assert r is not None
        assert r.status == LinkStatus.VALID

    def test_expired_returns_none(self):
        c = DocLinkCheck(cache_ttl=10.0)
        c.check_link("http://a", now=0.0)
        assert c.cached_result("http://a", now=20.0) is None


# ---------------------------------------------------------------------------
# clear_cache
# ---------------------------------------------------------------------------

class TestClearCache:
    def test_returns_count(self):
        c = DocLinkCheck()
        c.check_link("http://a")
        c.check_link("http://b")
        assert c.clear_cache() == 2

    def test_empties_cache(self):
        c = DocLinkCheck(cache_ttl=100.0)
        c.check_link("http://a", now=0.0)
        c.clear_cache()
        assert c.cached_result("http://a", now=0.0) is None

    def test_clear_empty_cache(self):
        c = DocLinkCheck()
        assert c.clear_cache() == 0


# ---------------------------------------------------------------------------
# set_checker
# ---------------------------------------------------------------------------

class TestSetChecker:
    def test_swaps_checker(self):
        c = DocLinkCheck()

        def new_checker(u: str) -> CheckResult:
            return CheckResult(url=u, status=LinkStatus.UNKNOWN)

        c.set_checker(new_checker)
        r = c.check_link("http://a")
        assert r.status == LinkStatus.UNKNOWN

    def test_new_checker_called(self):
        c = DocLinkCheck()
        calls: list[str] = []

        def new_checker(u: str) -> CheckResult:
            calls.append(u)
            return CheckResult(url=u, status=LinkStatus.VALID)

        c.set_checker(new_checker)
        c.check_link("http://a")
        assert calls == ["http://a"]


# ---------------------------------------------------------------------------
# skip_url
# ---------------------------------------------------------------------------

class TestSkipUrl:
    def test_skip_returns_true_first(self):
        c = DocLinkCheck()
        assert c.skip_url("http://a") is True

    def test_skip_returns_false_if_already(self):
        c = DocLinkCheck()
        c.skip_url("http://a")
        assert c.skip_url("http://a") is False

    def test_skipped_check_returns_skipped(self):
        c = DocLinkCheck()
        c.skip_url("http://a")
        r = c.check_link("http://a")
        assert r.status == LinkStatus.SKIPPED


class TestUnskipUrl:
    def test_unskip_existing(self):
        c = DocLinkCheck()
        c.skip_url("http://a")
        assert c.unskip_url("http://a") is True

    def test_unskip_missing(self):
        c = DocLinkCheck()
        assert c.unskip_url("http://a") is False

    def test_after_unskip_calls_checker(self):
        c = DocLinkCheck()
        c.skip_url("http://a")
        c.unskip_url("http://a")
        r = c.check_link("http://a")
        assert r.status == LinkStatus.VALID


class TestIsSkipped:
    def test_not_skipped_initially(self):
        c = DocLinkCheck()
        assert c.is_skipped("http://a") is False

    def test_after_skip(self):
        c = DocLinkCheck()
        c.skip_url("http://a")
        assert c.is_skipped("http://a") is True

    def test_after_unskip(self):
        c = DocLinkCheck()
        c.skip_url("http://a")
        c.unskip_url("http://a")
        assert c.is_skipped("http://a") is False


# ---------------------------------------------------------------------------
# Stats / lifecycle
# ---------------------------------------------------------------------------

class TestTotalLinks:
    def test_zero_initially(self):
        c = DocLinkCheck()
        assert c.total_links == 0

    def test_counts_links_across_docs(self):
        c = DocLinkCheck()
        c.register_doc("d1", "[a](u1) [b](u2)")
        c.register_doc("d2", "[c](u3)")
        assert c.total_links == 3


class TestTotalDocs:
    def test_zero_initially(self):
        c = DocLinkCheck()
        assert c.total_docs == 0

    def test_grows_with_register(self):
        c = DocLinkCheck()
        c.register_doc("d1", "")
        c.register_doc("d2", "")
        assert c.total_docs == 2


class TestTotalChecksRun:
    def test_zero_initially(self):
        c = DocLinkCheck()
        assert c.total_checks_run == 0

    def test_increments_per_check(self):
        c = DocLinkCheck()
        c.check_link("http://a")
        c.check_link("http://b")
        assert c.total_checks_run == 2

    def test_cache_hit_does_not_increment(self):
        c = DocLinkCheck(cache_ttl=1000.0)
        c.check_link("http://a", now=0.0)
        c.check_link("http://a", now=10.0)
        assert c.total_checks_run == 1


class TestClear:
    def test_clear_resets_docs(self):
        c = DocLinkCheck()
        c.register_doc("d1", "[a](u)")
        c.clear()
        assert c.total_docs == 0
        assert c.total_links == 0

    def test_clear_resets_cache(self):
        c = DocLinkCheck(cache_ttl=100.0)
        c.check_link("http://a", now=0.0)
        c.clear()
        assert c.cached_result("http://a", now=0.0) is None

    def test_clear_resets_skip(self):
        c = DocLinkCheck()
        c.skip_url("http://a")
        c.clear()
        assert c.is_skipped("http://a") is False

    def test_clear_resets_checks_run(self):
        c = DocLinkCheck()
        c.check_link("http://a")
        c.clear()
        assert c.total_checks_run == 0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_default_checker_is_stub(self):
        c = DocLinkCheck()
        assert c.check_link("http://ok").status == LinkStatus.VALID
        assert c.check_link("broken:x").status == LinkStatus.BROKEN

    def test_stub_checker_function(self):
        r = stub_checker("http://x")
        assert r.status == LinkStatus.VALID
        r2 = stub_checker("broken:y")
        assert r2.status == LinkStatus.BROKEN

    def test_empty_content_no_links(self):
        c = DocLinkCheck()
        assert c.register_doc("d1", "") == 0

    def test_thread_safety_register(self):
        c = DocLinkCheck()

        def worker(i: int):
            c.register_doc(f"d{i}", f"[a](u{i})")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert c.total_docs == 20

    def test_thread_safety_check(self):
        c = DocLinkCheck(cache_ttl=1000.0)
        urls = [f"http://u{i}" for i in range(20)]

        def worker(url: str):
            c.check_link(url, now=0.0)

        threads = [threading.Thread(target=worker, args=(u,)) for u in urls]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert c.total_checks_run == 20

    def test_custom_checker_passed_in_ctor(self):
        def checker(u: str) -> CheckResult:
            return CheckResult(url=u, status=LinkStatus.REDIRECT, final_url="x")

        c = DocLinkCheck(checker=checker)
        r = c.check_link("http://a")
        assert r.status == LinkStatus.REDIRECT
        assert r.final_url == "x"

    def test_report_unknown_count(self):
        def checker(u: str) -> CheckResult:
            return CheckResult(url=u, status=LinkStatus.UNKNOWN)

        c = DocLinkCheck(checker=checker)
        c.register_doc("d1", "[a](u1) [b](u2)")
        rep = c.check_all_links()
        assert rep.unknown_count == 2
