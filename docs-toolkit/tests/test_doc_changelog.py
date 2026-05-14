"""Tests for docstoolkit.doc_changelog."""
import threading

import pytest

from docstoolkit.doc_changelog import (
    ChangelogConfig,
    ChangeType,
    DocChangeEntry,
    DocChangelog,
    Release,
)


# ---------------------------------------------------------------------------
class TestChangeType:
    def test_all_members_present(self):
        names = {c.name for c in ChangeType}
        assert names == {"ADDED", "MODIFIED", "REMOVED", "RENAMED", "MOVED"}

    def test_values_are_strings(self):
        for c in ChangeType:
            assert isinstance(c.value, str)

    def test_added_value(self):
        assert ChangeType.ADDED.value == "Added"

    def test_modified_value(self):
        assert ChangeType.MODIFIED.value == "Modified"


# ---------------------------------------------------------------------------
class TestDocChangeEntry:
    def test_minimal_construct(self):
        e = DocChangeEntry(doc_id="d1", change_type=ChangeType.ADDED, description="hi")
        assert e.doc_id == "d1"
        assert e.change_type is ChangeType.ADDED
        assert e.description == "hi"
        assert e.timestamp == 0.0
        assert e.author is None
        assert e.tags == []

    def test_with_author_and_tags(self):
        e = DocChangeEntry(
            doc_id="d2",
            change_type=ChangeType.MODIFIED,
            description="x",
            author="alice",
            tags=["t1", "t2"],
        )
        assert e.author == "alice"
        assert e.tags == ["t1", "t2"]

    def test_tags_default_independent(self):
        a = DocChangeEntry(doc_id="x", change_type=ChangeType.ADDED, description="a")
        b = DocChangeEntry(doc_id="y", change_type=ChangeType.ADDED, description="b")
        a.tags.append("t")
        assert b.tags == []


# ---------------------------------------------------------------------------
class TestReleaseDataclass:
    def test_minimal(self):
        r = Release(version="1.0.0", released_at=1234.0)
        assert r.version == "1.0.0"
        assert r.released_at == 1234.0
        assert r.entries == []
        assert r.notes is None

    def test_with_entries(self):
        e = DocChangeEntry(doc_id="d", change_type=ChangeType.ADDED, description="x")
        r = Release(version="2.0", released_at=1.0, entries=[e], notes="hi")
        assert r.entries == [e]
        assert r.notes == "hi"


# ---------------------------------------------------------------------------
class TestChangelogConfig:
    def test_defaults(self):
        c = ChangelogConfig()
        assert c.group_by_type is True
        assert c.include_authors is False
        assert c.date_format == "%Y-%m-%d"
        assert c.unreleased_label == "Unreleased"

    def test_overrides(self):
        c = ChangelogConfig(group_by_type=False, include_authors=True,
                            date_format="%d/%m/%Y", unreleased_label="Pending")
        assert c.group_by_type is False
        assert c.include_authors is True
        assert c.date_format == "%d/%m/%Y"
        assert c.unreleased_label == "Pending"


# ---------------------------------------------------------------------------
class TestRecord:
    def test_record_returns_entry(self):
        cl = DocChangelog()
        e = cl.record("doc1", ChangeType.ADDED, "added doc1", now=100.0)
        assert isinstance(e, DocChangeEntry)
        assert e.doc_id == "doc1"
        assert e.change_type is ChangeType.ADDED
        assert e.description == "added doc1"
        assert e.timestamp == 100.0

    def test_record_appends_to_unreleased(self):
        cl = DocChangelog()
        cl.record("doc1", ChangeType.ADDED, "x", now=1.0)
        cl.record("doc2", ChangeType.MODIFIED, "y", now=2.0)
        assert cl.unreleased_count() == 2

    def test_record_default_timestamp_uses_time(self):
        cl = DocChangelog()
        e = cl.record("d", ChangeType.ADDED, "x")
        assert e.timestamp > 0

    def test_record_author(self):
        cl = DocChangelog()
        e = cl.record("d", ChangeType.ADDED, "x", author="alice", now=1.0)
        assert e.author == "alice"

    def test_record_tags(self):
        cl = DocChangelog()
        e = cl.record("d", ChangeType.ADDED, "x", tags=["a", "b"], now=1.0)
        assert e.tags == ["a", "b"]

    def test_record_thread_safe(self):
        cl = DocChangelog()

        def worker():
            for i in range(50):
                cl.record(f"d{i}", ChangeType.ADDED, "x", now=1.0)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert cl.unreleased_count() == 200


# ---------------------------------------------------------------------------
class TestTagRelease:
    def test_tag_release_with_pending(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        rel = cl.tag_release("1.0.0", now=100.0)
        assert rel is not None
        assert rel.version == "1.0.0"
        assert rel.released_at == 100.0
        assert len(rel.entries) == 1

    def test_tag_release_clears_unreleased(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=2.0)
        assert cl.unreleased_count() == 0

    def test_tag_release_no_pending_returns_none(self):
        cl = DocChangelog()
        assert cl.tag_release("1.0.0", now=1.0) is None

    def test_tag_release_duplicate_version(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=2.0)
        cl.record("d2", ChangeType.MODIFIED, "b", now=3.0)
        assert cl.tag_release("1.0.0", now=4.0) is None

    def test_tag_release_with_notes(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        rel = cl.tag_release("1.0.0", now=2.0, notes="Big release")
        assert rel.notes == "Big release"

    def test_tag_release_default_timestamp(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        rel = cl.tag_release("1.0.0")
        assert rel.released_at > 0


# ---------------------------------------------------------------------------
class TestReleases:
    def test_empty(self):
        cl = DocChangelog()
        assert cl.releases() == []

    def test_only_unreleased(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "x", now=1.0)
        rels = cl.releases()
        assert len(rels) == 1
        assert rels[0].version == "Unreleased"

    def test_newest_first(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=10.0)
        cl.record("d2", ChangeType.ADDED, "b", now=20.0)
        cl.tag_release("2.0.0", now=30.0)
        rels = cl.releases()
        assert [r.version for r in rels] == ["2.0.0", "1.0.0"]

    def test_unreleased_at_top(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=10.0)
        cl.record("d2", ChangeType.ADDED, "b", now=20.0)
        rels = cl.releases()
        assert rels[0].version == "Unreleased"
        assert rels[1].version == "1.0.0"


# ---------------------------------------------------------------------------
class TestReleaseLookup:
    def test_find_by_version(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=2.0)
        rel = cl.release("1.0.0")
        assert rel is not None
        assert rel.version == "1.0.0"

    def test_find_unreleased(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        rel = cl.release("Unreleased")
        assert rel is not None
        assert rel.version == "Unreleased"

    def test_unknown_returns_none(self):
        cl = DocChangelog()
        assert cl.release("nope") is None

    def test_unreleased_when_empty_none(self):
        cl = DocChangelog()
        assert cl.release("Unreleased") is None


# ---------------------------------------------------------------------------
class TestLatestRelease:
    def test_empty(self):
        cl = DocChangelog()
        assert cl.latest_release() is None

    def test_returns_last_tagged(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=10.0)
        cl.record("d2", ChangeType.ADDED, "b", now=20.0)
        cl.tag_release("2.0.0", now=30.0)
        assert cl.latest_release().version == "2.0.0"

    def test_ignores_unreleased(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=10.0)
        cl.record("d2", ChangeType.ADDED, "b", now=20.0)
        assert cl.latest_release().version == "1.0.0"


# ---------------------------------------------------------------------------
class TestEntriesForDoc:
    def test_empty(self):
        cl = DocChangelog()
        assert cl.entries_for_doc("d") == []

    def test_across_releases(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.record("d2", ChangeType.ADDED, "b", now=2.0)
        cl.tag_release("1.0.0", now=10.0)
        cl.record("d1", ChangeType.MODIFIED, "c", now=20.0)
        entries = cl.entries_for_doc("d1")
        assert len(entries) == 2
        assert entries[0].description == "a"
        assert entries[1].description == "c"

    def test_unknown_doc(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        assert cl.entries_for_doc("nope") == []


# ---------------------------------------------------------------------------
class TestEntriesForRelease:
    def test_empty(self):
        cl = DocChangelog()
        assert cl.entries_for_release("1.0") == []

    def test_known(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=2.0)
        entries = cl.entries_for_release("1.0.0")
        assert len(entries) == 1

    def test_unreleased(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        entries = cl.entries_for_release("Unreleased")
        assert len(entries) == 1


# ---------------------------------------------------------------------------
class TestEntriesSince:
    def test_unknown_version(self):
        cl = DocChangelog()
        assert cl.entries_since("9.9") == []

    def test_since_first(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=10.0)
        cl.record("d2", ChangeType.ADDED, "b", now=20.0)
        cl.tag_release("2.0.0", now=30.0)
        cl.record("d3", ChangeType.ADDED, "c", now=40.0)
        result = cl.entries_since("1.0.0")
        descriptions = [e.description for e in result]
        assert descriptions == ["b", "c"]

    def test_since_latest_only_unreleased(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=2.0)
        cl.record("d2", ChangeType.ADDED, "b", now=3.0)
        result = cl.entries_since("1.0.0")
        assert [e.description for e in result] == ["b"]


# ---------------------------------------------------------------------------
class TestToMarkdown:
    def test_empty(self):
        cl = DocChangelog()
        md = cl.to_markdown()
        assert "# Changelog" in md

    def test_with_release(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "added d1", now=1.0)
        cl.tag_release("1.0.0", now=1_700_000_000.0)
        md = cl.to_markdown()
        assert "# Changelog" in md
        assert "[1.0.0]" in md
        assert "### Added" in md
        assert "added d1" in md
        assert "(d1)" in md

    def test_includes_unreleased(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "added d1", now=1.0)
        md = cl.to_markdown()
        assert "[Unreleased]" in md

    def test_groups_by_type(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.record("d2", ChangeType.MODIFIED, "b", now=2.0)
        cl.record("d3", ChangeType.REMOVED, "c", now=3.0)
        md = cl.to_markdown()
        assert "### Added" in md
        assert "### Modified" in md
        assert "### Removed" in md

    def test_no_grouping(self):
        cl = DocChangelog(ChangelogConfig(group_by_type=False))
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.record("d2", ChangeType.MODIFIED, "b", now=2.0)
        md = cl.to_markdown()
        assert "### Added" not in md
        assert "- a (d1)" in md
        assert "- b (d2)" in md

    def test_newest_release_first(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=10.0)
        cl.record("d2", ChangeType.ADDED, "b", now=20.0)
        cl.tag_release("2.0.0", now=30.0)
        md = cl.to_markdown()
        assert md.index("[2.0.0]") < md.index("[1.0.0]")

    def test_includes_release_notes(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=2.0, notes="Hello world notes")
        md = cl.to_markdown()
        assert "Hello world notes" in md


# ---------------------------------------------------------------------------
class TestToMarkdownSingleVersion:
    def test_known_version(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=2.0)
        md = cl.to_markdown(version="1.0.0")
        assert "[1.0.0]" in md
        assert "# Changelog" not in md

    def test_unknown_version(self):
        cl = DocChangelog()
        assert cl.to_markdown(version="x") == ""

    def test_single_version_unreleased(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        md = cl.to_markdown(version="Unreleased")
        assert "[Unreleased]" in md
        assert "a" in md


# ---------------------------------------------------------------------------
class TestAddReleaseNotes:
    def test_known_release(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=2.0)
        assert cl.add_release_notes("1.0.0", "Some notes") is True
        assert cl.release("1.0.0").notes == "Some notes"

    def test_unknown_release(self):
        cl = DocChangelog()
        assert cl.add_release_notes("nope", "notes") is False

    def test_replaces_existing(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=2.0, notes="old")
        cl.add_release_notes("1.0.0", "new")
        assert cl.release("1.0.0").notes == "new"


# ---------------------------------------------------------------------------
class TestEntryCount:
    def test_empty(self):
        assert DocChangelog().entry_count == 0

    def test_counts_unreleased(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.record("d2", ChangeType.ADDED, "b", now=2.0)
        assert cl.entry_count == 2

    def test_counts_released_and_unreleased(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0", now=2.0)
        cl.record("d2", ChangeType.ADDED, "b", now=3.0)
        assert cl.entry_count == 2


# ---------------------------------------------------------------------------
class TestReleaseCount:
    def test_empty(self):
        assert DocChangelog().release_count == 0

    def test_after_tags(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0.0", now=2.0)
        cl.record("d2", ChangeType.ADDED, "b", now=3.0)
        cl.tag_release("2.0.0", now=4.0)
        assert cl.release_count == 2

    def test_excludes_unreleased(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        assert cl.release_count == 0


# ---------------------------------------------------------------------------
class TestUnreleasedCount:
    def test_empty(self):
        assert DocChangelog().unreleased_count() == 0

    def test_after_record(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        assert cl.unreleased_count() == 1

    def test_after_release(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0", now=2.0)
        assert cl.unreleased_count() == 0


# ---------------------------------------------------------------------------
class TestClear:
    def test_clears_all(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0", now=2.0)
        cl.record("d2", ChangeType.ADDED, "b", now=3.0)
        cl.clear()
        assert cl.entry_count == 0
        assert cl.release_count == 0
        assert cl.unreleased_count() == 0


# ---------------------------------------------------------------------------
class TestGroupByType:
    def test_order_added_then_modified_then_removed(self):
        cl = DocChangelog()
        cl.record("d1", ChangeType.REMOVED, "rm", now=1.0)
        cl.record("d2", ChangeType.MODIFIED, "mod", now=2.0)
        cl.record("d3", ChangeType.ADDED, "ad", now=3.0)
        md = cl.to_markdown()
        ia = md.index("### Added")
        im = md.index("### Modified")
        ir = md.index("### Removed")
        assert ia < im < ir

    def test_disabled_lists_flat(self):
        cl = DocChangelog(ChangelogConfig(group_by_type=False))
        cl.record("d1", ChangeType.ADDED, "a", now=1.0)
        cl.record("d2", ChangeType.MODIFIED, "b", now=2.0)
        md = cl.to_markdown()
        assert "### Added" not in md
        assert "### Modified" not in md
        assert "- a (d1)" in md
        assert "- b (d2)" in md


# ---------------------------------------------------------------------------
class TestIncludeAuthors:
    def test_includes_author_when_enabled(self):
        cl = DocChangelog(ChangelogConfig(include_authors=True))
        cl.record("d", ChangeType.ADDED, "a", author="alice", now=1.0)
        md = cl.to_markdown()
        assert "alice" in md

    def test_excludes_author_when_disabled(self):
        cl = DocChangelog(ChangelogConfig(include_authors=False))
        cl.record("d", ChangeType.ADDED, "a", author="alice", now=1.0)
        md = cl.to_markdown()
        assert "alice" not in md

    def test_no_author_no_decoration(self):
        cl = DocChangelog(ChangelogConfig(include_authors=True))
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        md = cl.to_markdown()
        # description line should still be rendered without "@"
        assert "@" not in md


# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_custom_unreleased_label(self):
        cl = DocChangelog(ChangelogConfig(unreleased_label="Pending"))
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        md = cl.to_markdown()
        assert "[Pending]" in md
        assert cl.release("Pending") is not None

    def test_custom_date_format(self):
        cl = DocChangelog(ChangelogConfig(date_format="%Y/%m/%d"))
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.tag_release("1.0", now=1_700_000_000.0)
        md = cl.to_markdown()
        # 2023-11-14 in UTC -> contains slashes
        assert "/" in md

    def test_release_dataclass_kept_after_tag(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        rel = cl.tag_release("1.0", now=2.0)
        # mutating returned reference should not vanish from internal state
        rel.notes = "external mutation"
        # but a fresh fetch should reflect since they are the same object
        assert cl.release("1.0").notes == "external mutation"

    def test_many_change_types(self):
        cl = DocChangelog()
        cl.record("d", ChangeType.ADDED, "a", now=1.0)
        cl.record("d", ChangeType.MODIFIED, "b", now=2.0)
        cl.record("d", ChangeType.REMOVED, "c", now=3.0)
        cl.record("d", ChangeType.RENAMED, "d", now=4.0)
        cl.record("d", ChangeType.MOVED, "e", now=5.0)
        md = cl.to_markdown()
        for label in ["Added", "Modified", "Removed", "Renamed", "Moved"]:
            assert f"### {label}" in md

    def test_threadsafe_tag_release(self):
        cl = DocChangelog()
        for i in range(10):
            cl.record(f"d{i}", ChangeType.ADDED, "x", now=float(i))

        results = []

        def worker():
            r = cl.tag_release("1.0.0", now=100.0)
            results.append(r)

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # Exactly one should have succeeded
        successful = [r for r in results if r is not None]
        assert len(successful) == 1
        assert cl.release_count == 1
