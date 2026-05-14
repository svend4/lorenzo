"""Tests for the changelog_builder module."""

import pytest

from docstoolkit.changelog_builder import (
    ChangeEntry,
    ChangeType,
    Changelog,
    ChangelogBuilder,
    Release,
)


class TestChangeType:
    def test_added_value(self):
        assert ChangeType.ADDED.value == "Added"

    def test_changed_value(self):
        assert ChangeType.CHANGED.value == "Changed"

    def test_deprecated_value(self):
        assert ChangeType.DEPRECATED.value == "Deprecated"

    def test_removed_value(self):
        assert ChangeType.REMOVED.value == "Removed"

    def test_fixed_value(self):
        assert ChangeType.FIXED.value == "Fixed"

    def test_security_value(self):
        assert ChangeType.SECURITY.value == "Security"

    def test_other_value(self):
        assert ChangeType.OTHER.value == "Other"

    def test_all_members_present(self):
        names = {ct.name for ct in ChangeType}
        assert names == {
            "ADDED",
            "CHANGED",
            "DEPRECATED",
            "REMOVED",
            "FIXED",
            "SECURITY",
            "OTHER",
        }


class TestChangeEntry:
    def test_minimal_construction(self):
        entry = ChangeEntry(change_type=ChangeType.ADDED, description="new thing")
        assert entry.change_type == ChangeType.ADDED
        assert entry.description == "new thing"
        assert entry.scope is None
        assert entry.author is None
        assert entry.date is None
        assert entry.pr_number is None

    def test_full_construction(self):
        entry = ChangeEntry(
            change_type=ChangeType.FIXED,
            description="bug",
            scope="api",
            author="alice",
            date="2024-01-15",
            pr_number=42,
        )
        assert entry.scope == "api"
        assert entry.author == "alice"
        assert entry.date == "2024-01-15"
        assert entry.pr_number == 42

    def test_entry_equality(self):
        a = ChangeEntry(change_type=ChangeType.ADDED, description="x")
        b = ChangeEntry(change_type=ChangeType.ADDED, description="x")
        assert a == b

    def test_entry_inequality(self):
        a = ChangeEntry(change_type=ChangeType.ADDED, description="x")
        b = ChangeEntry(change_type=ChangeType.FIXED, description="x")
        assert a != b


class TestReleaseProperties:
    def test_by_type_empty(self):
        r = Release(version="1.0.0", date="2024-01-01")
        assert r.by_type == {}

    def test_by_type_groups_entries(self):
        r = Release(version="1.0.0", date="2024-01-01")
        r.entries.append(ChangeEntry(ChangeType.ADDED, "a"))
        r.entries.append(ChangeEntry(ChangeType.ADDED, "b"))
        r.entries.append(ChangeEntry(ChangeType.FIXED, "c"))
        grouped = r.by_type
        assert len(grouped[ChangeType.ADDED]) == 2
        assert len(grouped[ChangeType.FIXED]) == 1

    def test_by_type_preserves_order(self):
        r = Release(version="1.0.0", date="2024-01-01")
        r.entries.append(ChangeEntry(ChangeType.ADDED, "first"))
        r.entries.append(ChangeEntry(ChangeType.ADDED, "second"))
        assert [e.description for e in r.by_type[ChangeType.ADDED]] == ["first", "second"]

    def test_entry_count_zero(self):
        assert Release(version="1.0.0", date="2024-01-01").entry_count == 0

    def test_entry_count_multiple(self):
        r = Release(version="1.0.0", date="2024-01-01")
        r.entries.extend(
            [
                ChangeEntry(ChangeType.ADDED, "a"),
                ChangeEntry(ChangeType.FIXED, "b"),
                ChangeEntry(ChangeType.OTHER, "c"),
            ]
        )
        assert r.entry_count == 3

    def test_is_breaking_false_when_empty(self):
        assert Release(version="1.0.0", date="2024-01-01").is_breaking is False

    def test_is_breaking_false_when_no_breaking(self):
        r = Release(version="1.0.0", date="2024-01-01")
        r.entries.append(ChangeEntry(ChangeType.ADDED, "x"))
        r.entries.append(ChangeEntry(ChangeType.FIXED, "y"))
        assert r.is_breaking is False

    def test_is_breaking_true_with_removed(self):
        r = Release(version="1.0.0", date="2024-01-01")
        r.entries.append(ChangeEntry(ChangeType.REMOVED, "old api"))
        assert r.is_breaking is True

    def test_is_breaking_true_with_breaking_prefix(self):
        r = Release(version="1.0.0", date="2024-01-01")
        r.entries.append(ChangeEntry(ChangeType.CHANGED, "BREAKING: redesign"))
        assert r.is_breaking is True


class TestChangelogProperties:
    def test_find_release_existing(self):
        cl = Changelog(releases=[Release(version="1.0.0", date="2024-01-01")])
        assert cl.find_release("1.0.0").version == "1.0.0"

    def test_find_release_missing(self):
        cl = Changelog(releases=[Release(version="1.0.0", date="2024-01-01")])
        assert cl.find_release("2.0.0") is None

    def test_find_release_empty(self):
        assert Changelog().find_release("1.0.0") is None

    def test_latest_none_when_empty(self):
        assert Changelog().latest is None

    def test_latest_skips_unreleased(self):
        cl = Changelog(
            releases=[
                Release(version="Unreleased", date=""),
                Release(version="1.0.0", date="2024-01-01"),
            ]
        )
        assert cl.latest.version == "1.0.0"

    def test_latest_only_release(self):
        cl = Changelog(releases=[Release(version="2.0.0", date="2024-05-01")])
        assert cl.latest.version == "2.0.0"

    def test_unreleased_present(self):
        cl = Changelog(
            releases=[
                Release(version="Unreleased", date=""),
                Release(version="1.0.0", date="2024-01-01"),
            ]
        )
        assert cl.unreleased.version == "Unreleased"

    def test_unreleased_case_insensitive(self):
        cl = Changelog(releases=[Release(version="unreleased", date="")])
        assert cl.unreleased is not None

    def test_unreleased_absent(self):
        cl = Changelog(releases=[Release(version="1.0.0", date="2024-01-01")])
        assert cl.unreleased is None


class TestAddRelease:
    def test_add_release_returns_release(self):
        b = ChangelogBuilder()
        r = b.add_release("1.0.0", "2024-01-01")
        assert isinstance(r, Release)
        assert r.version == "1.0.0"
        assert r.date == "2024-01-01"

    def test_add_release_appends_to_changelog(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-01")
        cl = b.build()
        assert len(cl.releases) == 1

    def test_add_release_default_date(self):
        b = ChangelogBuilder()
        r = b.add_release("1.0.0")
        # Default date is today (ISO format)
        assert len(r.date) == 10
        assert r.date[4] == "-"
        assert r.date[7] == "-"

    def test_add_release_dedup_returns_existing(self):
        b = ChangelogBuilder()
        r1 = b.add_release("1.0.0", "2024-01-01")
        r2 = b.add_release("1.0.0", "2024-02-02")
        assert r1 is r2
        # Original date preserved
        assert r1.date == "2024-01-01"

    def test_add_multiple_releases(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-01")
        b.add_release("1.1.0", "2024-02-01")
        b.add_release("2.0.0", "2024-03-01")
        assert len(b.build().releases) == 3


class TestAddEntry:
    def test_add_entry_to_existing_release(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-01")
        b.add_entry("1.0.0", ChangeType.ADDED, "feature x")
        cl = b.build()
        assert cl.releases[0].entries[0].description == "feature x"

    def test_add_entry_creates_release_implicitly(self):
        b = ChangelogBuilder()
        b.add_entry("0.1.0", ChangeType.FIXED, "bug")
        cl = b.build()
        assert cl.releases[0].version == "0.1.0"
        assert cl.releases[0].entries[0].change_type == ChangeType.FIXED

    def test_add_entry_with_kwargs(self):
        b = ChangelogBuilder()
        b.add_entry(
            "1.0.0",
            ChangeType.FIXED,
            "fix bug",
            scope="api",
            author="alice",
            pr_number=7,
            date="2024-01-01",
        )
        entry = b.build().releases[0].entries[0]
        assert entry.scope == "api"
        assert entry.author == "alice"
        assert entry.pr_number == 7
        assert entry.date == "2024-01-01"

    def test_add_multiple_entries(self):
        b = ChangelogBuilder()
        b.add_entry("1.0.0", ChangeType.ADDED, "a")
        b.add_entry("1.0.0", ChangeType.ADDED, "b")
        b.add_entry("1.0.0", ChangeType.FIXED, "c")
        cl = b.build()
        assert len(cl.releases[0].entries) == 3


class TestParseConventionalFeat:
    def test_feat_basic(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("feat: add login")
        assert entry.change_type == ChangeType.ADDED
        assert entry.description == "add login"
        assert entry.scope is None

    def test_feat_uppercase_type_normalized(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("FEAT: hello")
        assert entry.change_type == ChangeType.ADDED

    def test_feat_with_extra_spaces(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("feat:    spaced description")
        assert entry.description == "spaced description"


class TestParseConventionalFix:
    def test_fix_basic(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("fix: resolve crash")
        assert entry.change_type == ChangeType.FIXED
        assert entry.description == "resolve crash"

    def test_refactor_to_changed(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("refactor: simplify loop")
        assert entry.change_type == ChangeType.CHANGED

    def test_perf_to_changed(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("perf: faster index")
        assert entry.change_type == ChangeType.CHANGED

    def test_revert_to_removed(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("revert: undo feature")
        assert entry.change_type == ChangeType.REMOVED

    def test_docs_to_other(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("docs: update readme")
        assert entry.change_type == ChangeType.OTHER

    def test_chore_to_other(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("chore: bump deps")
        assert entry.change_type == ChangeType.OTHER

    def test_style_to_other(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("style: format code")
        assert entry.change_type == ChangeType.OTHER

    def test_test_to_other(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("test: add unit tests")
        assert entry.change_type == ChangeType.OTHER


class TestParseConventionalWithScope:
    def test_feat_with_scope(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("feat(api): add endpoint")
        assert entry.change_type == ChangeType.ADDED
        assert entry.scope == "api"
        assert entry.description == "add endpoint"

    def test_fix_with_scope(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("fix(ui): button hover")
        assert entry.scope == "ui"
        assert entry.change_type == ChangeType.FIXED

    def test_breaking_marker_bang(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("feat!: breaking redesign")
        assert entry.description.startswith("BREAKING")

    def test_breaking_marker_in_body(self):
        b = ChangelogBuilder()
        msg = "feat: redesign\n\nBREAKING CHANGE: drop old API"
        entry = b.parse_conventional(msg)
        assert entry.description.startswith("BREAKING")

    def test_breaking_with_scope(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("feat(api)!: revamp")
        assert entry.scope == "api"
        assert entry.description.startswith("BREAKING")


class TestParseConventionalUnknown:
    def test_non_conventional_returns_none(self):
        b = ChangelogBuilder()
        assert b.parse_conventional("just a random message") is None

    def test_empty_returns_none(self):
        b = ChangelogBuilder()
        assert b.parse_conventional("") is None

    def test_unknown_type_falls_back_to_other(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("wibble: something weird")
        assert entry is not None
        assert entry.change_type == ChangeType.OTHER

    def test_missing_colon_returns_none(self):
        b = ChangelogBuilder()
        assert b.parse_conventional("feat add login") is None

    def test_only_type_returns_none(self):
        b = ChangelogBuilder()
        # Header "feat:" with no description should not match the description group
        assert b.parse_conventional("feat:") is None


class TestParseCommits:
    def test_parse_commits_creates_release(self):
        b = ChangelogBuilder()
        rel = b.parse_commits(
            ["feat: a", "fix: b"],
            version="1.0.0",
        )
        assert rel.version == "1.0.0"
        assert rel.entry_count == 2

    def test_parse_commits_default_version_unreleased(self):
        b = ChangelogBuilder()
        rel = b.parse_commits(["feat: a"])
        assert rel.version == "Unreleased"

    def test_parse_commits_skips_invalid(self):
        b = ChangelogBuilder()
        rel = b.parse_commits(["feat: ok", "not conventional", "fix: also ok"])
        assert rel.entry_count == 2

    def test_parse_commits_preserves_types(self):
        b = ChangelogBuilder()
        rel = b.parse_commits(["feat: a", "fix: b", "refactor: c"])
        types = [e.change_type for e in rel.entries]
        assert types == [ChangeType.ADDED, ChangeType.FIXED, ChangeType.CHANGED]

    def test_parse_commits_with_scope(self):
        b = ChangelogBuilder()
        rel = b.parse_commits(["feat(api): hello", "fix(ui): there"])
        assert rel.entries[0].scope == "api"
        assert rel.entries[1].scope == "ui"

    def test_parse_commits_empty_list(self):
        b = ChangelogBuilder()
        rel = b.parse_commits([])
        assert rel.entry_count == 0
        assert rel.version == "Unreleased"


class TestToMarkdown:
    def test_to_markdown_empty(self):
        b = ChangelogBuilder()
        md = b.to_markdown(Changelog())
        assert md.startswith("# Changelog")

    def test_to_markdown_single_release(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-15")
        b.add_entry("1.0.0", ChangeType.ADDED, "New feature")
        b.add_entry("1.0.0", ChangeType.FIXED, "Bug fix")
        md = b.to_markdown(b.build())
        assert "## [1.0.0] - 2024-01-15" in md
        assert "### Added" in md
        assert "- New feature" in md
        assert "### Fixed" in md
        assert "- Bug fix" in md

    def test_to_markdown_section_order(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-15")
        b.add_entry("1.0.0", ChangeType.FIXED, "fixme")
        b.add_entry("1.0.0", ChangeType.ADDED, "added")
        md = b.to_markdown(b.build())
        # Added comes before Fixed in Keep-a-Changelog order
        assert md.index("### Added") < md.index("### Fixed")

    def test_to_markdown_scope_rendered(self):
        b = ChangelogBuilder()
        b.add_entry("1.0.0", ChangeType.ADDED, "endpoint", scope="api")
        md = b.to_markdown(b.build())
        assert "**api**" in md
        assert "endpoint" in md

    def test_to_markdown_pr_number(self):
        b = ChangelogBuilder()
        b.add_entry("1.0.0", ChangeType.ADDED, "thing", pr_number=42)
        md = b.to_markdown(b.build())
        assert "(#42)" in md

    def test_to_markdown_author(self):
        b = ChangelogBuilder()
        b.add_entry("1.0.0", ChangeType.ADDED, "thing", author="alice")
        md = b.to_markdown(b.build())
        assert "@alice" in md

    def test_to_markdown_multiple_releases(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-15")
        b.add_entry("1.0.0", ChangeType.ADDED, "a")
        b.add_release("2.0.0", "2024-06-01")
        b.add_entry("2.0.0", ChangeType.REMOVED, "old api")
        md = b.to_markdown(b.build())
        assert "## [1.0.0]" in md
        assert "## [2.0.0]" in md
        assert "### Removed" in md

    def test_to_markdown_unreleased(self):
        b = ChangelogBuilder()
        b.add_release("Unreleased", "")
        b.add_entry("Unreleased", ChangeType.ADDED, "wip feature")
        md = b.to_markdown(b.build())
        assert "## [Unreleased]" in md


class TestFromMarkdown:
    def test_from_markdown_basic(self):
        text = """# Changelog

## [1.0.0] - 2024-01-15

### Added
- New feature

### Fixed
- Bug fix
"""
        b = ChangelogBuilder()
        cl = b.from_markdown(text)
        assert len(cl.releases) == 1
        rel = cl.releases[0]
        assert rel.version == "1.0.0"
        assert rel.date == "2024-01-15"
        assert rel.entry_count == 2

    def test_from_markdown_multiple_releases(self):
        text = """# Changelog

## [2.0.0] - 2024-06-01

### Removed
- old api

## [1.0.0] - 2024-01-15

### Added
- first feature
"""
        cl = ChangelogBuilder().from_markdown(text)
        assert len(cl.releases) == 2
        assert cl.releases[0].version == "2.0.0"
        assert cl.releases[1].version == "1.0.0"

    def test_from_markdown_scope_parsed(self):
        text = """# Changelog

## [1.0.0] - 2024-01-15

### Added
- **api**: new endpoint
"""
        cl = ChangelogBuilder().from_markdown(text)
        entry = cl.releases[0].entries[0]
        assert entry.scope == "api"
        assert entry.description == "new endpoint"

    def test_from_markdown_pr_number_parsed(self):
        text = """# Changelog

## [1.0.0] - 2024-01-15

### Added
- something (#42)
"""
        cl = ChangelogBuilder().from_markdown(text)
        assert cl.releases[0].entries[0].pr_number == 42

    def test_from_markdown_author_parsed(self):
        text = """# Changelog

## [1.0.0] - 2024-01-15

### Added
- a feature @alice
"""
        cl = ChangelogBuilder().from_markdown(text)
        entry = cl.releases[0].entries[0]
        assert entry.author == "alice"

    def test_from_markdown_unreleased(self):
        text = """# Changelog

## [Unreleased]

### Added
- wip
"""
        cl = ChangelogBuilder().from_markdown(text)
        assert cl.unreleased is not None
        assert cl.unreleased.entry_count == 1

    def test_from_markdown_no_releases(self):
        cl = ChangelogBuilder().from_markdown("# Changelog\n\nNothing here yet.\n")
        assert cl.releases == []

    def test_from_markdown_unknown_section_to_other(self):
        text = """# Changelog

## [1.0.0] - 2024-01-15

### Mystery
- something
"""
        cl = ChangelogBuilder().from_markdown(text)
        assert cl.releases[0].entries[0].change_type == ChangeType.OTHER


class TestRoundTrip:
    def test_round_trip_simple(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-15")
        b.add_entry("1.0.0", ChangeType.ADDED, "feature x")
        b.add_entry("1.0.0", ChangeType.FIXED, "bug y")
        md = b.to_markdown(b.build())
        cl = ChangelogBuilder().from_markdown(md)
        assert len(cl.releases) == 1
        rel = cl.releases[0]
        assert rel.version == "1.0.0"
        assert rel.date == "2024-01-15"
        assert rel.entry_count == 2

    def test_round_trip_preserves_scope(self):
        b = ChangelogBuilder()
        b.add_entry("1.0.0", ChangeType.ADDED, "endpoint", scope="api")
        md = b.to_markdown(b.build())
        cl = ChangelogBuilder().from_markdown(md)
        entry = cl.releases[0].entries[0]
        assert entry.scope == "api"
        assert entry.description == "endpoint"

    def test_round_trip_preserves_pr_and_author(self):
        b = ChangelogBuilder()
        b.add_entry(
            "1.0.0",
            ChangeType.FIXED,
            "fix",
            pr_number=7,
            author="bob",
        )
        md = b.to_markdown(b.build())
        cl = ChangelogBuilder().from_markdown(md)
        entry = cl.releases[0].entries[0]
        assert entry.pr_number == 7
        assert entry.author == "bob"

    def test_round_trip_multiple_releases(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-15")
        b.add_entry("1.0.0", ChangeType.ADDED, "a")
        b.add_release("2.0.0", "2024-06-01")
        b.add_entry("2.0.0", ChangeType.REMOVED, "old")
        md1 = b.to_markdown(b.build())
        cl = ChangelogBuilder().from_markdown(md1)
        # Re-render and confirm equivalence
        md2 = ChangelogBuilder().to_markdown(cl)
        assert md1 == md2


class TestEdgeCases:
    def test_build_empty(self):
        cl = ChangelogBuilder().build()
        assert cl.releases == []
        assert cl.latest is None
        assert cl.unreleased is None

    def test_release_with_no_entries_in_markdown(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-15")
        md = b.to_markdown(b.build())
        assert "## [1.0.0] - 2024-01-15" in md

    def test_entry_count_after_many_releases(self):
        b = ChangelogBuilder()
        b.add_entry("1.0.0", ChangeType.ADDED, "a")
        b.add_entry("1.0.0", ChangeType.ADDED, "b")
        b.add_entry("2.0.0", ChangeType.FIXED, "c")
        cl = b.build()
        assert cl.find_release("1.0.0").entry_count == 2
        assert cl.find_release("2.0.0").entry_count == 1

    def test_unreleased_then_release(self):
        b = ChangelogBuilder()
        b.add_release("Unreleased")
        b.add_entry("Unreleased", ChangeType.ADDED, "wip")
        b.add_release("1.0.0", "2024-01-15")
        b.add_entry("1.0.0", ChangeType.ADDED, "shipped")
        cl = b.build()
        assert cl.unreleased.entry_count == 1
        assert cl.latest.version == "1.0.0"

    def test_find_release_returns_same_instance(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-15")
        cl = b.build()
        assert cl.find_release("1.0.0") is cl.releases[0]

    def test_build_returns_fresh_release_list(self):
        b = ChangelogBuilder()
        b.add_release("1.0.0", "2024-01-15")
        cl1 = b.build()
        b.add_release("2.0.0", "2024-06-01")
        # cl1 should not have been mutated
        assert len(cl1.releases) == 1

    def test_parse_conventional_with_trailing_whitespace(self):
        b = ChangelogBuilder()
        entry = b.parse_conventional("feat: trailing   ")
        assert entry.description == "trailing"

    def test_markdown_round_trip_breaking(self):
        b = ChangelogBuilder()
        b.add_entry("1.0.0", ChangeType.CHANGED, "BREAKING: redesign API")
        md = b.to_markdown(b.build())
        cl = ChangelogBuilder().from_markdown(md)
        assert cl.releases[0].is_breaking is True
