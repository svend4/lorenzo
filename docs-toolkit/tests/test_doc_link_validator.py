"""Tests for E363 DocLinkValidator."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_link_validator import (
    DocLinkValidator,
    LinkCheck,
    ValidatorStats,
)


# ----------------------------------------------------------------------
# Dataclass tests
# ----------------------------------------------------------------------


class TestLinkCheckDataclass:
    def test_defaults(self):
        c = LinkCheck(url="https://x", doc_id="d1")
        assert c.url == "https://x"
        assert c.doc_id == "d1"
        assert c.checked_at == 0.0
        assert c.valid is True
        assert c.error == ""
        assert c.link_type == "external"

    def test_explicit_fields(self):
        c = LinkCheck(
            url="https://y",
            doc_id="d2",
            checked_at=1.5,
            valid=False,
            error="404",
            link_type="internal",
        )
        assert c.checked_at == 1.5
        assert c.valid is False
        assert c.error == "404"
        assert c.link_type == "internal"

    def test_equality(self):
        a = LinkCheck(url="u", doc_id="d", checked_at=1.0)
        b = LinkCheck(url="u", doc_id="d", checked_at=1.0)
        assert a == b

    def test_inequality(self):
        a = LinkCheck(url="u", doc_id="d", checked_at=1.0)
        b = LinkCheck(url="u", doc_id="d", checked_at=2.0)
        assert a != b


class TestValidatorStatsDataclass:
    def test_fields(self):
        s = ValidatorStats(total_checks=5, valid_count=3, invalid_count=2, unique_urls=4)
        assert s.total_checks == 5
        assert s.valid_count == 3
        assert s.invalid_count == 2
        assert s.unique_urls == 4

    def test_equality(self):
        a = ValidatorStats(1, 1, 0, 1)
        b = ValidatorStats(1, 1, 0, 1)
        assert a == b


# ----------------------------------------------------------------------
# Construction
# ----------------------------------------------------------------------


class TestConstruction:
    def test_empty_construction(self):
        v = DocLinkValidator()
        assert v.unique_urls() == []
        assert v.invalid_links() == []
        assert v.valid_links() == []

    def test_initial_stats_zero(self):
        v = DocLinkValidator()
        s = v.stats()
        assert s.total_checks == 0
        assert s.valid_count == 0
        assert s.invalid_count == 0
        assert s.unique_urls == 0

    def test_initial_latest_for_url_none(self):
        v = DocLinkValidator()
        assert v.latest_for_url("https://nope") is None


# ----------------------------------------------------------------------
# classify_link
# ----------------------------------------------------------------------


class TestClassifyLink:
    def test_external_https(self):
        v = DocLinkValidator()
        assert v.classify_link("https://example.com/path") == "external"

    def test_external_http(self):
        v = DocLinkValidator()
        assert v.classify_link("http://example.com") == "external"

    def test_external_ftp(self):
        v = DocLinkValidator()
        assert v.classify_link("ftp://files.example.com/x") == "external"

    def test_mailto(self):
        v = DocLinkValidator()
        assert v.classify_link("mailto:foo@bar.com") == "mailto"

    def test_anchor(self):
        v = DocLinkValidator()
        assert v.classify_link("#section-1") == "anchor"

    def test_internal_leading_slash(self):
        v = DocLinkValidator()
        assert v.classify_link("/docs/page.html") == "internal"

    def test_internal_relative(self):
        v = DocLinkValidator()
        assert v.classify_link("page.html") == "internal"

    def test_internal_relative_dotted(self):
        v = DocLinkValidator()
        assert v.classify_link("../other/page.md") == "internal"


# ----------------------------------------------------------------------
# record_check
# ----------------------------------------------------------------------


class TestRecordCheck:
    def test_returns_link_check(self):
        v = DocLinkValidator()
        c = v.record_check("https://x", "d1", True, now=1.0)
        assert isinstance(c, LinkCheck)

    def test_fields_propagated(self):
        v = DocLinkValidator()
        c = v.record_check("https://x", "d1", True, error="", now=2.5)
        assert c.url == "https://x"
        assert c.doc_id == "d1"
        assert c.checked_at == 2.5
        assert c.valid is True
        assert c.error == ""

    def test_error_propagated(self):
        v = DocLinkValidator()
        c = v.record_check("https://x", "d1", False, error="timeout", now=1.0)
        assert c.valid is False
        assert c.error == "timeout"

    def test_link_type_external(self):
        v = DocLinkValidator()
        c = v.record_check("https://x.com", "d", True, now=1.0)
        assert c.link_type == "external"

    def test_link_type_mailto(self):
        v = DocLinkValidator()
        c = v.record_check("mailto:a@b", "d", True, now=1.0)
        assert c.link_type == "mailto"

    def test_link_type_anchor(self):
        v = DocLinkValidator()
        c = v.record_check("#top", "d", True, now=1.0)
        assert c.link_type == "anchor"

    def test_link_type_internal(self):
        v = DocLinkValidator()
        c = v.record_check("/about", "d", True, now=1.0)
        assert c.link_type == "internal"

    def test_now_defaults_to_time(self):
        v = DocLinkValidator()
        c = v.record_check("https://x", "d1", True)
        assert c.checked_at > 0

    def test_stored_in_internal_list(self):
        v = DocLinkValidator()
        v.record_check("https://x", "d", True, now=1.0)
        v.record_check("https://y", "d", True, now=2.0)
        assert v.stats().total_checks == 2


# ----------------------------------------------------------------------
# checks_for_url
# ----------------------------------------------------------------------


class TestChecksForUrl:
    def test_empty_for_unknown(self):
        v = DocLinkValidator()
        assert v.checks_for_url("https://nope") == []

    def test_returns_all_checks(self):
        v = DocLinkValidator()
        v.record_check("https://x", "d1", True, now=1.0)
        v.record_check("https://x", "d2", False, error="500", now=2.0)
        assert len(v.checks_for_url("https://x")) == 2

    def test_sorted_desc(self):
        v = DocLinkValidator()
        v.record_check("https://x", "d1", True, now=1.0)
        v.record_check("https://x", "d2", True, now=3.0)
        v.record_check("https://x", "d3", True, now=2.0)
        ts = [c.checked_at for c in v.checks_for_url("https://x")]
        assert ts == [3.0, 2.0, 1.0]

    def test_isolated_per_url(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", True, now=1.0)
        v.record_check("https://b", "d", True, now=2.0)
        assert len(v.checks_for_url("https://a")) == 1
        assert len(v.checks_for_url("https://b")) == 1


# ----------------------------------------------------------------------
# checks_for_doc
# ----------------------------------------------------------------------


class TestChecksForDoc:
    def test_empty_for_unknown(self):
        v = DocLinkValidator()
        assert v.checks_for_doc("missing") == []

    def test_returns_all_checks(self):
        v = DocLinkValidator()
        v.record_check("https://x", "d1", True, now=1.0)
        v.record_check("https://y", "d1", False, error="dns", now=2.0)
        v.record_check("https://x", "d2", True, now=3.0)
        assert len(v.checks_for_doc("d1")) == 2

    def test_sorted_desc(self):
        v = DocLinkValidator()
        v.record_check("https://x", "d1", True, now=1.0)
        v.record_check("https://y", "d1", True, now=5.0)
        v.record_check("https://z", "d1", True, now=3.0)
        ts = [c.checked_at for c in v.checks_for_doc("d1")]
        assert ts == [5.0, 3.0, 1.0]

    def test_doc_isolation(self):
        v = DocLinkValidator()
        v.record_check("https://x", "d1", True, now=1.0)
        v.record_check("https://x", "d2", True, now=2.0)
        assert len(v.checks_for_doc("d1")) == 1
        assert len(v.checks_for_doc("d2")) == 1


# ----------------------------------------------------------------------
# latest_for_url
# ----------------------------------------------------------------------


class TestLatestForUrl:
    def test_returns_most_recent(self):
        v = DocLinkValidator()
        v.record_check("https://x", "d", True, now=1.0)
        v.record_check("https://x", "d", False, error="oops", now=5.0)
        v.record_check("https://x", "d", True, now=3.0)
        latest = v.latest_for_url("https://x")
        assert latest is not None
        assert latest.checked_at == 5.0
        assert latest.valid is False
        assert latest.error == "oops"

    def test_none_for_unknown(self):
        v = DocLinkValidator()
        v.record_check("https://x", "d", True, now=1.0)
        assert v.latest_for_url("https://other") is None

    def test_single_entry(self):
        v = DocLinkValidator()
        v.record_check("https://x", "d", True, now=7.0)
        latest = v.latest_for_url("https://x")
        assert latest is not None
        assert latest.checked_at == 7.0


# ----------------------------------------------------------------------
# invalid_links
# ----------------------------------------------------------------------


class TestInvalidLinks:
    def test_empty(self):
        v = DocLinkValidator()
        assert v.invalid_links() == []

    def test_only_invalid_latest(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", False, error="500", now=1.0)
        v.record_check("https://b", "d", True, now=1.0)
        result = v.invalid_links()
        assert len(result) == 1
        assert result[0].url == "https://a"

    def test_latest_per_url_overrides_old_invalid(self):
        v = DocLinkValidator()
        # First invalid, then valid → not in invalid_links
        v.record_check("https://a", "d", False, error="x", now=1.0)
        v.record_check("https://a", "d", True, now=2.0)
        assert v.invalid_links() == []

    def test_latest_per_url_overrides_old_valid(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", True, now=1.0)
        v.record_check("https://a", "d", False, error="x", now=2.0)
        result = v.invalid_links()
        assert len(result) == 1
        assert result[0].url == "https://a"

    def test_sorted_by_url(self):
        v = DocLinkValidator()
        v.record_check("https://c", "d", False, error="x", now=1.0)
        v.record_check("https://a", "d", False, error="x", now=1.0)
        v.record_check("https://b", "d", False, error="x", now=1.0)
        urls = [c.url for c in v.invalid_links()]
        assert urls == ["https://a", "https://b", "https://c"]


# ----------------------------------------------------------------------
# valid_links
# ----------------------------------------------------------------------


class TestValidLinks:
    def test_empty(self):
        v = DocLinkValidator()
        assert v.valid_links() == []

    def test_only_valid_latest(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", True, now=1.0)
        v.record_check("https://b", "d", False, error="x", now=1.0)
        result = v.valid_links()
        assert len(result) == 1
        assert result[0].url == "https://a"

    def test_latest_per_url(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", True, now=1.0)
        v.record_check("https://a", "d", False, error="x", now=2.0)
        assert v.valid_links() == []

    def test_latest_per_url_recovers(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", False, error="x", now=1.0)
        v.record_check("https://a", "d", True, now=2.0)
        result = v.valid_links()
        assert len(result) == 1

    def test_sorted_by_url(self):
        v = DocLinkValidator()
        v.record_check("https://z", "d", True, now=1.0)
        v.record_check("https://a", "d", True, now=1.0)
        v.record_check("https://m", "d", True, now=1.0)
        urls = [c.url for c in v.valid_links()]
        assert urls == ["https://a", "https://m", "https://z"]


# ----------------------------------------------------------------------
# unique_urls
# ----------------------------------------------------------------------


class TestUniqueUrls:
    def test_empty(self):
        v = DocLinkValidator()
        assert v.unique_urls() == []

    def test_deduplicates(self):
        v = DocLinkValidator()
        v.record_check("https://x", "d1", True, now=1.0)
        v.record_check("https://x", "d2", True, now=2.0)
        v.record_check("https://x", "d3", False, error="x", now=3.0)
        assert v.unique_urls() == ["https://x"]

    def test_sorted(self):
        v = DocLinkValidator()
        v.record_check("https://c", "d", True, now=1.0)
        v.record_check("https://a", "d", True, now=1.0)
        v.record_check("https://b", "d", True, now=1.0)
        assert v.unique_urls() == ["https://a", "https://b", "https://c"]


# ----------------------------------------------------------------------
# broken_urls
# ----------------------------------------------------------------------


class TestBrokenUrls:
    def test_empty(self):
        v = DocLinkValidator()
        assert v.broken_urls() == []

    def test_currently_broken_only(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", False, error="500", now=1.0)
        v.record_check("https://b", "d", True, now=1.0)
        assert v.broken_urls() == ["https://a"]

    def test_recovered_excluded(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", False, error="500", now=1.0)
        v.record_check("https://a", "d", True, now=2.0)
        assert v.broken_urls() == []

    def test_newly_broken_included(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", True, now=1.0)
        v.record_check("https://a", "d", False, error="x", now=2.0)
        assert v.broken_urls() == ["https://a"]

    def test_sorted(self):
        v = DocLinkValidator()
        v.record_check("https://m", "d", False, error="x", now=1.0)
        v.record_check("https://a", "d", False, error="x", now=1.0)
        v.record_check("https://z", "d", False, error="x", now=1.0)
        assert v.broken_urls() == ["https://a", "https://m", "https://z"]


# ----------------------------------------------------------------------
# clear_checks_for_doc
# ----------------------------------------------------------------------


class TestClearChecksForDoc:
    def test_returns_zero_for_unknown(self):
        v = DocLinkValidator()
        assert v.clear_checks_for_doc("missing") == 0

    def test_returns_count(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d1", True, now=1.0)
        v.record_check("https://b", "d1", True, now=2.0)
        v.record_check("https://c", "d2", True, now=3.0)
        assert v.clear_checks_for_doc("d1") == 2

    def test_removes_from_doc_index(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d1", True, now=1.0)
        v.clear_checks_for_doc("d1")
        assert v.checks_for_doc("d1") == []

    def test_keeps_other_docs(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d1", True, now=1.0)
        v.record_check("https://b", "d2", True, now=2.0)
        v.clear_checks_for_doc("d1")
        assert len(v.checks_for_doc("d2")) == 1

    def test_updates_url_index(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d1", True, now=1.0)
        v.record_check("https://a", "d2", False, error="x", now=2.0)
        v.clear_checks_for_doc("d1")
        # Only d2's check survives.
        remaining = v.checks_for_url("https://a")
        assert len(remaining) == 1
        assert remaining[0].doc_id == "d2"

    def test_url_disappears_when_all_doc_checks_cleared(self):
        v = DocLinkValidator()
        v.record_check("https://only", "d1", True, now=1.0)
        v.clear_checks_for_doc("d1")
        assert v.unique_urls() == []

    def test_stats_decrease(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d1", True, now=1.0)
        v.record_check("https://b", "d2", True, now=2.0)
        v.clear_checks_for_doc("d1")
        assert v.stats().total_checks == 1


# ----------------------------------------------------------------------
# clear_all
# ----------------------------------------------------------------------


class TestClearAll:
    def test_returns_zero_when_empty(self):
        v = DocLinkValidator()
        assert v.clear_all() == 0

    def test_returns_count(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", True, now=1.0)
        v.record_check("https://b", "d", True, now=2.0)
        v.record_check("https://c", "d", True, now=3.0)
        assert v.clear_all() == 3

    def test_clears_everything(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d1", True, now=1.0)
        v.record_check("https://b", "d2", False, error="x", now=2.0)
        v.clear_all()
        assert v.unique_urls() == []
        assert v.invalid_links() == []
        assert v.valid_links() == []
        assert v.checks_for_doc("d1") == []
        assert v.checks_for_doc("d2") == []
        s = v.stats()
        assert s.total_checks == 0
        assert s.unique_urls == 0


# ----------------------------------------------------------------------
# stats
# ----------------------------------------------------------------------


class TestStats:
    def test_totals(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", True, now=1.0)
        v.record_check("https://b", "d", False, error="x", now=2.0)
        v.record_check("https://b", "d", True, now=3.0)
        s = v.stats()
        assert s.total_checks == 3
        # Counts are over raw checks (not latest-per-url):
        assert s.valid_count == 2
        assert s.invalid_count == 1
        assert s.unique_urls == 2

    def test_unique_urls_count(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", True, now=1.0)
        v.record_check("https://a", "d", True, now=2.0)
        v.record_check("https://b", "d", True, now=3.0)
        assert v.stats().unique_urls == 2

    def test_all_invalid(self):
        v = DocLinkValidator()
        v.record_check("https://a", "d", False, error="e", now=1.0)
        v.record_check("https://b", "d", False, error="e", now=2.0)
        s = v.stats()
        assert s.valid_count == 0
        assert s.invalid_count == 2


# ----------------------------------------------------------------------
# Thread safety
# ----------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_record_check(self):
        v = DocLinkValidator()
        n_threads = 8
        per_thread = 50

        def worker(tid: int) -> None:
            for i in range(per_thread):
                url = f"https://host{tid}/p{i}"
                v.record_check(url, f"doc{tid}", True, now=float(i + 1))

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = v.stats()
        assert s.total_checks == n_threads * per_thread
        assert s.unique_urls == n_threads * per_thread
        assert s.valid_count == n_threads * per_thread
        assert s.invalid_count == 0

    def test_concurrent_record_same_url(self):
        v = DocLinkValidator()
        n_threads = 6
        per_thread = 40

        def worker(tid: int) -> None:
            for i in range(per_thread):
                v.record_check(
                    "https://shared",
                    f"doc{tid}",
                    valid=(i % 2 == 0),
                    error="" if i % 2 == 0 else "fail",
                    now=float(tid * 1000 + i + 1),
                )

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert v.stats().total_checks == n_threads * per_thread
        assert v.unique_urls() == ["https://shared"]
        # Every check was recorded.
        assert len(v.checks_for_url("https://shared")) == n_threads * per_thread

    def test_concurrent_clear_and_record(self):
        v = DocLinkValidator()

        def writer() -> None:
            for i in range(100):
                v.record_check(f"https://x/{i}", f"doc{i % 4}", True, now=float(i + 1))

        def cleaner() -> None:
            for _ in range(20):
                v.clear_checks_for_doc("doc0")

        threads = [
            threading.Thread(target=writer),
            threading.Thread(target=writer),
            threading.Thread(target=cleaner),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # No exception is the main assertion; stats must remain self-consistent.
        s = v.stats()
        assert s.total_checks >= 0
        assert s.valid_count + s.invalid_count == s.total_checks
        assert s.unique_urls == len(v.unique_urls())


if __name__ == "__main__":
    pytest.main([__file__, "-q"])
