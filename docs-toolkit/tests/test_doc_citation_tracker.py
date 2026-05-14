"""Tests for docstoolkit.doc_citation_tracker (E295)."""
import threading

import pytest

from docstoolkit.doc_citation_tracker import (
    Citation,
    CitationStats,
    DocCitationTracker,
    UrlStats,
)


# ---------------------------------------------------------------------------
# Dataclass: Citation
# ---------------------------------------------------------------------------
class TestCitationDataclass:
    def test_required_fields(self):
        c = Citation(citation_id=1, doc_id="doc1", url="https://example.com")
        assert c.citation_id == 1
        assert c.doc_id == "doc1"
        assert c.url == "https://example.com"

    def test_optional_title_default(self):
        c = Citation(citation_id=1, doc_id="d", url="u")
        assert c.title == ""

    def test_optional_added_at_default(self):
        c = Citation(citation_id=1, doc_id="d", url="u")
        assert c.added_at == 0.0

    def test_explicit_optional_fields(self):
        c = Citation(citation_id=5, doc_id="d", url="u", title="My page", added_at=42.0)
        assert c.title == "My page"
        assert c.added_at == 42.0


# ---------------------------------------------------------------------------
# Dataclass: UrlStats
# ---------------------------------------------------------------------------
class TestUrlStatsDataclass:
    def test_fields(self):
        s = UrlStats(url="https://x.com", doc_count=3, citation_count=7)
        assert s.url == "https://x.com"
        assert s.doc_count == 3
        assert s.citation_count == 7


# ---------------------------------------------------------------------------
# Dataclass: CitationStats
# ---------------------------------------------------------------------------
class TestCitationStatsDataclass:
    def test_fields(self):
        s = CitationStats(
            total_citations=10,
            unique_urls=4,
            unique_docs=2,
            top_urls=[("https://a.com", 2)],
        )
        assert s.total_citations == 10
        assert s.unique_urls == 4
        assert s.unique_docs == 2
        assert s.top_urls == [("https://a.com", 2)]

    def test_top_urls_default_independent(self):
        s1 = CitationStats(total_citations=0, unique_urls=0, unique_docs=0, top_urls=[])
        s2 = CitationStats(total_citations=0, unique_urls=0, unique_docs=0, top_urls=[])
        s1.top_urls.append(("u", 1))
        assert s2.top_urls == []


# ---------------------------------------------------------------------------
# add()
# ---------------------------------------------------------------------------
class TestAdd:
    def test_returns_citation(self):
        t = DocCitationTracker()
        c = t.add("doc1", "https://example.com", now=1.0)
        assert isinstance(c, Citation)

    def test_auto_increments_id(self):
        t = DocCitationTracker()
        c1 = t.add("d1", "https://a.com", now=1.0)
        c2 = t.add("d1", "https://b.com", now=2.0)
        assert c2.citation_id == c1.citation_id + 1

    def test_ids_start_at_one(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", now=1.0)
        assert c.citation_id == 1

    def test_stores_doc_id(self):
        t = DocCitationTracker()
        c = t.add("myDoc", "https://x.com", now=1.0)
        assert c.doc_id == "myDoc"

    def test_stores_url(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com/page", now=1.0)
        assert c.url == "https://x.com/page"

    def test_stores_title(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", title="My Title", now=1.0)
        assert c.title == "My Title"

    def test_default_title_empty(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", now=1.0)
        assert c.title == ""

    def test_stores_timestamp(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", now=99.5)
        assert c.added_at == 99.5

    def test_default_timestamp_uses_time(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com")
        assert c.added_at > 0.0

    def test_increments_total_citations(self):
        t = DocCitationTracker()
        t.add("d1", "https://a.com", now=1.0)
        t.add("d2", "https://b.com", now=2.0)
        assert t.total_citations == 2

    def test_same_url_different_docs(self):
        t = DocCitationTracker()
        t.add("doc1", "https://shared.com", now=1.0)
        t.add("doc2", "https://shared.com", now=2.0)
        assert t.total_citations == 2


# ---------------------------------------------------------------------------
# citations_for_doc()
# ---------------------------------------------------------------------------
class TestCitationsForDoc:
    def test_unknown_doc_returns_empty(self):
        t = DocCitationTracker()
        assert t.citations_for_doc("ghost") == []

    def test_single_citation(self):
        t = DocCitationTracker()
        c = t.add("doc1", "https://x.com", now=1.0)
        result = t.citations_for_doc("doc1")
        assert len(result) == 1
        assert result[0].citation_id == c.citation_id

    def test_multiple_citations_insertion_order(self):
        t = DocCitationTracker()
        c1 = t.add("doc1", "https://a.com", now=1.0)
        c2 = t.add("doc1", "https://b.com", now=2.0)
        c3 = t.add("doc1", "https://c.com", now=3.0)
        ids = [c.citation_id for c in t.citations_for_doc("doc1")]
        assert ids == [c1.citation_id, c2.citation_id, c3.citation_id]

    def test_does_not_include_other_docs(self):
        t = DocCitationTracker()
        t.add("doc1", "https://a.com", now=1.0)
        t.add("doc2", "https://b.com", now=2.0)
        result = t.citations_for_doc("doc2")
        assert len(result) == 1
        assert result[0].url == "https://b.com"

    def test_same_url_twice_in_doc(self):
        t = DocCitationTracker()
        t.add("doc1", "https://a.com", now=1.0)
        t.add("doc1", "https://a.com", now=2.0)
        assert len(t.citations_for_doc("doc1")) == 2


# ---------------------------------------------------------------------------
# docs_citing()
# ---------------------------------------------------------------------------
class TestDocsCiting:
    def test_unknown_url_returns_empty(self):
        t = DocCitationTracker()
        assert t.docs_citing("https://nope.com") == []

    def test_single_doc(self):
        t = DocCitationTracker()
        t.add("doc1", "https://x.com", now=1.0)
        assert t.docs_citing("https://x.com") == ["doc1"]

    def test_multiple_docs_sorted(self):
        t = DocCitationTracker()
        t.add("doc_c", "https://x.com", now=1.0)
        t.add("doc_a", "https://x.com", now=2.0)
        t.add("doc_b", "https://x.com", now=3.0)
        assert t.docs_citing("https://x.com") == ["doc_a", "doc_b", "doc_c"]

    def test_duplicate_citation_from_same_doc(self):
        t = DocCitationTracker()
        t.add("doc1", "https://x.com", now=1.0)
        t.add("doc1", "https://x.com", now=2.0)
        # still only one unique doc
        assert t.docs_citing("https://x.com") == ["doc1"]


# ---------------------------------------------------------------------------
# url_stats()
# ---------------------------------------------------------------------------
class TestUrlStats:
    def test_unknown_url_returns_none(self):
        t = DocCitationTracker()
        assert t.url_stats("https://ghost.com") is None

    def test_single_doc_single_citation(self):
        t = DocCitationTracker()
        t.add("doc1", "https://x.com", now=1.0)
        s = t.url_stats("https://x.com")
        assert s is not None
        assert s.doc_count == 1
        assert s.citation_count == 1

    def test_multiple_docs(self):
        t = DocCitationTracker()
        t.add("doc1", "https://x.com", now=1.0)
        t.add("doc2", "https://x.com", now=2.0)
        s = t.url_stats("https://x.com")
        assert s.doc_count == 2
        assert s.citation_count == 2

    def test_citation_count_exceeds_doc_count(self):
        t = DocCitationTracker()
        t.add("doc1", "https://x.com", now=1.0)
        t.add("doc1", "https://x.com", now=2.0)
        t.add("doc2", "https://x.com", now=3.0)
        s = t.url_stats("https://x.com")
        assert s.doc_count == 2
        assert s.citation_count == 3

    def test_url_field_matches(self):
        t = DocCitationTracker()
        t.add("doc1", "https://exact.com/path", now=1.0)
        s = t.url_stats("https://exact.com/path")
        assert s.url == "https://exact.com/path"


# ---------------------------------------------------------------------------
# delete()
# ---------------------------------------------------------------------------
class TestDelete:
    def test_delete_existing_returns_true(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", now=1.0)
        assert t.delete(c.citation_id) is True

    def test_delete_nonexistent_returns_false(self):
        t = DocCitationTracker()
        assert t.delete(9999) is False

    def test_delete_reduces_total(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", now=1.0)
        t.delete(c.citation_id)
        assert t.total_citations == 0

    def test_deleted_citation_not_in_doc(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", now=1.0)
        t.delete(c.citation_id)
        assert t.citations_for_doc("d") == []

    def test_delete_clears_url_index_when_last(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", now=1.0)
        t.delete(c.citation_id)
        assert t.url_stats("https://x.com") is None
        assert t.docs_citing("https://x.com") == []

    def test_delete_partial_leaves_url_index(self):
        t = DocCitationTracker()
        c1 = t.add("d1", "https://x.com", now=1.0)
        t.add("d2", "https://x.com", now=2.0)
        t.delete(c1.citation_id)
        s = t.url_stats("https://x.com")
        assert s is not None
        assert s.doc_count == 1
        assert "d1" not in t.docs_citing("https://x.com")
        assert "d2" in t.docs_citing("https://x.com")

    def test_delete_twice_returns_false(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", now=1.0)
        t.delete(c.citation_id)
        assert t.delete(c.citation_id) is False


# ---------------------------------------------------------------------------
# delete_doc_citations()
# ---------------------------------------------------------------------------
class TestDeleteDocCitations:
    def test_unknown_doc_returns_zero(self):
        t = DocCitationTracker()
        assert t.delete_doc_citations("ghost") == 0

    def test_returns_count_removed(self):
        t = DocCitationTracker()
        t.add("d", "https://a.com", now=1.0)
        t.add("d", "https://b.com", now=2.0)
        assert t.delete_doc_citations("d") == 2

    def test_doc_gone_after_delete(self):
        t = DocCitationTracker()
        t.add("d", "https://a.com", now=1.0)
        t.delete_doc_citations("d")
        assert t.citations_for_doc("d") == []

    def test_url_index_cleaned_up(self):
        t = DocCitationTracker()
        t.add("d", "https://a.com", now=1.0)
        t.delete_doc_citations("d")
        assert t.url_stats("https://a.com") is None

    def test_only_target_doc_removed(self):
        t = DocCitationTracker()
        t.add("d1", "https://shared.com", now=1.0)
        t.add("d2", "https://shared.com", now=2.0)
        t.delete_doc_citations("d1")
        assert t.total_citations == 1
        assert t.docs_citing("https://shared.com") == ["d2"]

    def test_total_citations_updated(self):
        t = DocCitationTracker()
        t.add("d1", "https://a.com", now=1.0)
        t.add("d1", "https://b.com", now=2.0)
        t.add("d2", "https://c.com", now=3.0)
        t.delete_doc_citations("d1")
        assert t.total_citations == 1


# ---------------------------------------------------------------------------
# top_cited_urls()
# ---------------------------------------------------------------------------
class TestTopCitedUrls:
    def test_empty_tracker(self):
        t = DocCitationTracker()
        assert t.top_cited_urls() == []

    def test_default_limit_ten(self):
        t = DocCitationTracker()
        for i in range(15):
            t.add(f"doc{i}", f"https://url{i}.com", now=float(i))
        assert len(t.top_cited_urls()) == 10

    def test_sorted_by_doc_count_desc(self):
        t = DocCitationTracker()
        t.add("d1", "https://popular.com", now=1.0)
        t.add("d2", "https://popular.com", now=2.0)
        t.add("d3", "https://popular.com", now=3.0)
        t.add("d1", "https://rare.com", now=4.0)
        top = t.top_cited_urls(limit=2)
        assert top[0].url == "https://popular.com"
        assert top[0].doc_count == 3

    def test_limit_respected(self):
        t = DocCitationTracker()
        for i in range(5):
            t.add(f"doc{i}", f"https://url{i}.com", now=float(i))
        assert len(t.top_cited_urls(limit=3)) == 3

    def test_returns_urlstats_objects(self):
        t = DocCitationTracker()
        t.add("d1", "https://x.com", now=1.0)
        top = t.top_cited_urls(limit=1)
        assert isinstance(top[0], UrlStats)


# ---------------------------------------------------------------------------
# search_url()
# ---------------------------------------------------------------------------
class TestSearchUrl:
    def test_no_match_returns_empty(self):
        t = DocCitationTracker()
        t.add("d", "https://example.com", now=1.0)
        assert t.search_url("github") == []

    def test_exact_match(self):
        t = DocCitationTracker()
        c = t.add("d", "https://github.com/user/repo", now=1.0)
        result = t.search_url("https://github.com/user/repo")
        assert len(result) == 1
        assert result[0].citation_id == c.citation_id

    def test_partial_match(self):
        t = DocCitationTracker()
        c = t.add("d", "https://github.com/user/repo", now=1.0)
        result = t.search_url("github")
        assert len(result) == 1
        assert result[0].citation_id == c.citation_id

    def test_case_insensitive(self):
        t = DocCitationTracker()
        t.add("d", "https://GitHub.COM/test", now=1.0)
        assert len(t.search_url("github.com")) == 1
        assert len(t.search_url("GITHUB.COM")) == 1

    def test_multiple_matches_sorted_by_id(self):
        t = DocCitationTracker()
        c1 = t.add("d1", "https://python.org/docs", now=1.0)
        c2 = t.add("d2", "https://python.org/tutorial", now=2.0)
        result = t.search_url("python.org")
        assert [c.citation_id for c in result] == [c1.citation_id, c2.citation_id]

    def test_no_false_positives(self):
        t = DocCitationTracker()
        t.add("d", "https://docs.python.org", now=1.0)
        t.add("d", "https://nodejs.org", now=2.0)
        result = t.search_url("python")
        assert all("python" in c.url.lower() for c in result)
        assert len(result) == 1


# ---------------------------------------------------------------------------
# stats()
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty_tracker(self):
        t = DocCitationTracker()
        s = t.stats()
        assert s.total_citations == 0
        assert s.unique_urls == 0
        assert s.unique_docs == 0
        assert s.top_urls == []

    def test_total_citations(self):
        t = DocCitationTracker()
        t.add("d1", "https://a.com", now=1.0)
        t.add("d2", "https://b.com", now=2.0)
        assert t.stats().total_citations == 2

    def test_unique_urls(self):
        t = DocCitationTracker()
        t.add("d1", "https://a.com", now=1.0)
        t.add("d2", "https://a.com", now=2.0)
        t.add("d1", "https://b.com", now=3.0)
        assert t.stats().unique_urls == 2

    def test_unique_docs(self):
        t = DocCitationTracker()
        t.add("d1", "https://a.com", now=1.0)
        t.add("d1", "https://b.com", now=2.0)
        t.add("d2", "https://c.com", now=3.0)
        assert t.stats().unique_docs == 2

    def test_top_urls_max_five(self):
        t = DocCitationTracker()
        for i in range(7):
            t.add(f"doc{i}", f"https://url{i}.com", now=float(i))
        s = t.stats()
        assert len(s.top_urls) == 5

    def test_top_urls_format(self):
        t = DocCitationTracker()
        t.add("d1", "https://popular.com", now=1.0)
        t.add("d2", "https://popular.com", now=2.0)
        s = t.stats()
        assert s.top_urls[0] == ("https://popular.com", 2)

    def test_returns_citation_stats_type(self):
        t = DocCitationTracker()
        assert isinstance(t.stats(), CitationStats)


# ---------------------------------------------------------------------------
# total_citations property
# ---------------------------------------------------------------------------
class TestTotalCitationsProperty:
    def test_zero_initially(self):
        t = DocCitationTracker()
        assert t.total_citations == 0

    def test_increments_on_add(self):
        t = DocCitationTracker()
        t.add("d", "https://x.com", now=1.0)
        assert t.total_citations == 1

    def test_decrements_on_delete(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", now=1.0)
        t.delete(c.citation_id)
        assert t.total_citations == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_adds(self):
        t = DocCitationTracker()

        def worker(doc_id: str):
            for i in range(50):
                t.add(doc_id, f"https://url{i}.com", now=float(i))

        threads = [threading.Thread(target=worker, args=(f"doc{j}",)) for j in range(4)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        assert t.total_citations == 200

    def test_concurrent_deletes(self):
        t = DocCitationTracker()
        citations = [t.add("d", f"https://url{i}.com", now=float(i)) for i in range(100)]
        results = []

        def deleter(cid: int):
            results.append(t.delete(cid))

        threads = [threading.Thread(target=deleter, args=(c.citation_id,)) for c in citations]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        assert t.total_citations == 0
        assert results.count(True) == 100

    def test_concurrent_add_and_query(self):
        t = DocCitationTracker()
        errors = []

        def adder():
            for i in range(100):
                t.add("d", f"https://url{i}.com", now=float(i))

        def reader():
            for _ in range(100):
                try:
                    t.stats()
                    t.top_cited_urls()
                except Exception as exc:
                    errors.append(exc)

        threads = (
            [threading.Thread(target=adder) for _ in range(2)]
            + [threading.Thread(target=reader) for _ in range(2)]
        )
        for th in threads:
            th.start()
        for th in threads:
            th.join()
        assert errors == []


# ---------------------------------------------------------------------------
# Edge cases / integration
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_empty_doc_id_allowed(self):
        t = DocCitationTracker()
        c = t.add("", "https://x.com", now=1.0)
        assert c.doc_id == ""
        assert len(t.citations_for_doc("")) == 1

    def test_empty_url_allowed(self):
        t = DocCitationTracker()
        c = t.add("d", "", now=1.0)
        assert c.url == ""

    def test_citation_ids_unique_across_instances(self):
        # Each instance has its own counter starting at 1
        t1 = DocCitationTracker()
        t2 = DocCitationTracker()
        c1 = t1.add("d", "https://a.com", now=1.0)
        c2 = t2.add("d", "https://a.com", now=1.0)
        assert c1.citation_id == 1
        assert c2.citation_id == 1

    def test_search_url_empty_fragment_matches_all(self):
        t = DocCitationTracker()
        t.add("d1", "https://a.com", now=1.0)
        t.add("d2", "https://b.com", now=2.0)
        result = t.search_url("")
        assert len(result) == 2

    def test_delete_and_re_add_preserves_new_id(self):
        t = DocCitationTracker()
        c1 = t.add("d", "https://x.com", now=1.0)
        t.delete(c1.citation_id)
        c2 = t.add("d", "https://x.com", now=2.0)
        assert c2.citation_id > c1.citation_id

    def test_top_cited_urls_limit_zero(self):
        t = DocCitationTracker()
        t.add("d", "https://x.com", now=1.0)
        assert t.top_cited_urls(limit=0) == []

    def test_delete_doc_then_url_stats_gone(self):
        t = DocCitationTracker()
        t.add("d", "https://x.com", now=1.0)
        t.delete_doc_citations("d")
        assert t.url_stats("https://x.com") is None

    def test_stats_reflects_deletes(self):
        t = DocCitationTracker()
        c = t.add("d", "https://x.com", now=1.0)
        t.delete(c.citation_id)
        s = t.stats()
        assert s.total_citations == 0
        assert s.unique_urls == 0
        assert s.unique_docs == 0
