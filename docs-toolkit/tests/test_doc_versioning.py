"""Tests for the doc_versioning module (E18 — Semantic versioning for documents)."""
from __future__ import annotations

import time

import pytest

from docstoolkit.doc_versioning import (
    ChangeDetector,
    ChangeType,
    DocVersion,
    VersionHistory,
    VersionRecord,
)


# ===========================================================================
# DocVersion
# ===========================================================================

class TestDocVersionStr:
    def test_str_zero(self):
        assert str(DocVersion(0, 0, 0)) == "0.0.0"

    def test_str_initial(self):
        assert str(DocVersion(0, 1, 0)) == "0.1.0"

    def test_str_arbitrary(self):
        assert str(DocVersion(3, 14, 159)) == "3.14.159"


class TestDocVersionParse:
    def test_parse_simple(self):
        v = DocVersion.parse("1.2.3")
        assert v == DocVersion(1, 2, 3)

    def test_parse_zeros(self):
        assert DocVersion.parse("0.0.0") == DocVersion(0, 0, 0)

    def test_parse_leading_space(self):
        assert DocVersion.parse("  2.3.4  ") == DocVersion(2, 3, 4)

    def test_parse_invalid_too_few_parts(self):
        with pytest.raises(ValueError):
            DocVersion.parse("1.2")

    def test_parse_invalid_too_many_parts(self):
        with pytest.raises(ValueError):
            DocVersion.parse("1.2.3.4")

    def test_parse_invalid_non_numeric(self):
        with pytest.raises(ValueError):
            DocVersion.parse("a.b.c")

    def test_parse_roundtrip(self):
        v = DocVersion(7, 8, 9)
        assert DocVersion.parse(str(v)) == v


class TestDocVersionInitial:
    def test_initial_value(self):
        v = DocVersion.initial()
        assert v == DocVersion(0, 1, 0)

    def test_initial_str(self):
        assert str(DocVersion.initial()) == "0.1.0"


class TestDocVersionBump:
    def test_bump_major(self):
        v = DocVersion(1, 2, 3)
        assert v.bump(ChangeType.MAJOR) == DocVersion(2, 0, 0)

    def test_bump_major_resets_minor_and_patch(self):
        bumped = DocVersion(0, 5, 7).bump(ChangeType.MAJOR)
        assert bumped.minor == 0
        assert bumped.patch == 0

    def test_bump_minor(self):
        v = DocVersion(1, 2, 3)
        assert v.bump(ChangeType.MINOR) == DocVersion(1, 3, 0)

    def test_bump_minor_resets_patch(self):
        bumped = DocVersion(1, 2, 9).bump(ChangeType.MINOR)
        assert bumped.patch == 0

    def test_bump_patch(self):
        v = DocVersion(1, 2, 3)
        assert v.bump(ChangeType.PATCH) == DocVersion(1, 2, 4)

    def test_bump_none(self):
        v = DocVersion(1, 2, 3)
        assert v.bump(ChangeType.NONE) == DocVersion(1, 2, 3)

    def test_bump_does_not_mutate(self):
        original = DocVersion(1, 2, 3)
        _ = original.bump(ChangeType.MAJOR)
        assert original == DocVersion(1, 2, 3)

    def test_bump_major_from_initial(self):
        assert DocVersion.initial().bump(ChangeType.MAJOR) == DocVersion(1, 0, 0)

    def test_bump_minor_from_initial(self):
        assert DocVersion.initial().bump(ChangeType.MINOR) == DocVersion(0, 2, 0)

    def test_bump_patch_from_initial(self):
        assert DocVersion.initial().bump(ChangeType.PATCH) == DocVersion(0, 1, 1)


class TestDocVersionIsCompatible:
    def test_same_major_compatible(self):
        assert DocVersion(1, 0, 0).is_compatible_with(DocVersion(1, 5, 3))

    def test_different_major_incompatible(self):
        assert not DocVersion(1, 0, 0).is_compatible_with(DocVersion(2, 0, 0))

    def test_zero_major_compatible(self):
        assert DocVersion(0, 1, 0).is_compatible_with(DocVersion(0, 9, 99))

    def test_zero_vs_one_incompatible(self):
        assert not DocVersion(0, 1, 0).is_compatible_with(DocVersion(1, 0, 0))

    def test_same_version_compatible(self):
        v = DocVersion(3, 3, 3)
        assert v.is_compatible_with(v)


class TestDocVersionComparisons:
    def test_equality(self):
        assert DocVersion(1, 2, 3) == DocVersion(1, 2, 3)

    def test_inequality(self):
        assert DocVersion(1, 2, 3) != DocVersion(1, 2, 4)

    def test_hash_consistent(self):
        v = DocVersion(1, 2, 3)
        assert hash(v) == hash(DocVersion(1, 2, 3))

    def test_ordering(self):
        assert DocVersion(0, 1, 0) < DocVersion(1, 0, 0)
        assert DocVersion(1, 1, 0) > DocVersion(1, 0, 9)


# ===========================================================================
# ChangeDetector
# ===========================================================================

class TestChangeDetectorNone:
    def setup_method(self):
        self.cd = ChangeDetector()

    def test_identical_empty(self):
        assert self.cd.detect("", "") is ChangeType.NONE

    def test_identical_text(self):
        text = "Hello, world!\n\nThis is a test."
        assert self.cd.detect(text, text) is ChangeType.NONE

    def test_identical_with_headings(self):
        text = "# Title\n\nContent here."
        assert self.cd.detect(text, text) is ChangeType.NONE


class TestChangeDetectorPatch:
    def setup_method(self):
        self.cd = ChangeDetector()

    def test_extra_whitespace(self):
        old = "Hello world"
        new = "Hello   world"
        assert self.cd.detect(old, new) is ChangeType.PATCH

    def test_trailing_newline(self):
        old = "Hello world"
        new = "Hello world\n"
        assert self.cd.detect(old, new) is ChangeType.PATCH

    def test_extra_spaces_around_words(self):
        old = "word1 word2 word3"
        new = "  word1  word2   word3  "
        assert self.cd.detect(old, new) is ChangeType.PATCH

    def test_punctuation_only_change(self):
        old = "Hello, world!"
        new = "Hello world"
        assert self.cd.detect(old, new) is ChangeType.PATCH


class TestChangeDetectorMinor:
    def setup_method(self):
        self.cd = ChangeDetector()

    def test_word_count_increased_over_10_pct(self):
        old = " ".join(["word"] * 100)
        # 112 words = 12 % increase
        new = " ".join(["word"] * 112)
        assert self.cd.detect(old, new) is ChangeType.MINOR

    def test_new_heading_added(self):
        old = "Some content here without any headings."
        new = "Some content here without any headings.\n\n# New Section\n\nMore text."
        result = self.cd.detect(old, new)
        assert result in (ChangeType.MINOR, ChangeType.MAJOR)

    def test_one_new_heading_is_minor_or_major(self):
        old = "# Intro\n\nContent."
        new = "# Intro\n\nContent.\n\n## Details\n\nMore details here added now."
        result = self.cd.detect(old, new)
        assert result in (ChangeType.MINOR, ChangeType.MAJOR)


class TestChangeDetectorMajor:
    def setup_method(self):
        self.cd = ChangeDetector()

    def test_word_count_changed_over_30_pct(self):
        old = " ".join(["word"] * 100)
        new = " ".join(["word"] * 135)   # 35 % increase
        assert self.cd.detect(old, new) is ChangeType.MAJOR

    def test_word_count_decreased_over_30_pct(self):
        old = " ".join(["word"] * 100)
        new = " ".join(["word"] * 60)    # 40 % decrease
        assert self.cd.detect(old, new) is ChangeType.MAJOR

    def test_heading_count_diff_gt_2(self):
        old = "# H1\n\nContent."
        new = (
            "# H1\n\nContent.\n\n"
            "## H2\n\nMore.\n\n"
            "## H3\n\nEven more.\n\n"
            "## H4\n\nYet more.\n\n"
        )
        assert self.cd.detect(old, new) is ChangeType.MAJOR

    def test_empty_old_nonempty_new(self):
        new = " ".join(["word"] * 50)
        assert self.cd.detect("", new) is ChangeType.MAJOR


class TestChangeDetectorHelpers:
    def setup_method(self):
        self.cd = ChangeDetector()

    def test_word_count_empty(self):
        assert self.cd.word_count("") == 0

    def test_word_count_simple(self):
        assert self.cd.word_count("one two three") == 3

    def test_word_count_extra_spaces(self):
        assert self.cd.word_count("  a   b  ") == 2

    def test_heading_count_empty(self):
        assert self.cd.heading_count("") == 0

    def test_heading_count_no_headings(self):
        assert self.cd.heading_count("Just plain text\nAnother line") == 0

    def test_heading_count_h1(self):
        assert self.cd.heading_count("# Title") == 1

    def test_heading_count_multiple_levels(self):
        text = "# H1\n## H2\n### H3\nNot a heading\n## Another H2"
        assert self.cd.heading_count(text) == 4

    def test_heading_count_not_confused_by_inline_hash(self):
        text = "Some text with #hashtag inline"
        assert self.cd.heading_count(text) == 0


# ===========================================================================
# VersionHistory
# ===========================================================================

class TestVersionHistoryRecord:
    def setup_method(self):
        self.history = VersionHistory()

    def test_first_record_starts_at_initial(self):
        rec = self.history.record("doc1", "content", ChangeType.MINOR)
        assert rec.version == DocVersion.initial()

    def test_first_record_returns_version_record_type(self):
        rec = self.history.record("doc1", "content", ChangeType.MINOR)
        assert isinstance(rec, VersionRecord)

    def test_second_record_bumps_version(self):
        self.history.record("doc1", "v1 content", ChangeType.MINOR)
        rec2 = self.history.record("doc1", "v2 content", ChangeType.MINOR)
        assert rec2.version == DocVersion(0, 2, 0)

    def test_major_bump(self):
        self.history.record("doc1", "v1", ChangeType.MINOR)
        rec2 = self.history.record("doc1", "v2 different", ChangeType.MAJOR)
        assert rec2.version == DocVersion(1, 0, 0)

    def test_patch_bump(self):
        self.history.record("doc1", "v1", ChangeType.MINOR)
        rec2 = self.history.record("doc1", "v2 typo fix", ChangeType.PATCH)
        assert rec2.version == DocVersion(0, 1, 1)

    def test_duplicate_content_skipped(self):
        content = "identical content"
        rec1 = self.history.record("doc1", content, ChangeType.MINOR)
        rec2 = self.history.record("doc1", content, ChangeType.MINOR)
        # Same record returned, no new entry created
        assert rec1.version == rec2.version
        assert len(self.history.list_versions("doc1")) == 1

    def test_content_hash_length(self):
        rec = self.history.record("doc1", "some content", ChangeType.MINOR)
        assert len(rec.content_hash) == 16

    def test_summary_stored(self):
        rec = self.history.record("doc1", "content", ChangeType.MINOR, summary="Added intro")
        assert rec.summary == "Added intro"

    def test_ts_stored(self):
        ts = 1_700_000_000.0
        rec = self.history.record("doc1", "content", ChangeType.MINOR, ts=ts)
        assert rec.ts == ts

    def test_ts_auto_set_when_none(self):
        before = time.time()
        rec = self.history.record("doc1", "content", ChangeType.MINOR)
        after = time.time()
        assert before <= rec.ts <= after

    def test_doc_id_stored(self):
        rec = self.history.record("my-doc", "content", ChangeType.MINOR)
        assert rec.doc_id == "my-doc"

    def test_change_type_stored(self):
        rec = self.history.record("doc1", "content", ChangeType.MAJOR)
        assert rec.change_type is ChangeType.MAJOR


class TestVersionHistoryLatest:
    def setup_method(self):
        self.history = VersionHistory()

    def test_latest_returns_none_for_unknown_doc(self):
        assert self.history.latest("nonexistent") is None

    def test_latest_returns_most_recent(self):
        self.history.record("doc1", "v1", ChangeType.MINOR)
        self.history.record("doc1", "v2 content", ChangeType.MINOR)
        latest = self.history.latest("doc1")
        assert latest is not None
        assert latest.version == DocVersion(0, 2, 0)

    def test_latest_isolated_per_doc(self):
        self.history.record("docA", "content A", ChangeType.MINOR)
        self.history.record("docB", "content B", ChangeType.MAJOR)
        assert self.history.latest("docA").version == DocVersion(0, 1, 0)
        assert self.history.latest("docB").version == DocVersion(0, 1, 0)


class TestVersionHistoryListVersions:
    def setup_method(self):
        self.history = VersionHistory()

    def test_list_empty_for_unknown_doc(self):
        assert self.history.list_versions("ghost") == []

    def test_list_oldest_first(self):
        self.history.record("doc1", "v1 text", ChangeType.MINOR)
        self.history.record("doc1", "v2 text more words here added", ChangeType.MINOR)
        self.history.record("doc1", "v3 even more words added to this document", ChangeType.PATCH)
        versions = [r.version for r in self.history.list_versions("doc1")]
        assert versions == [DocVersion(0, 1, 0), DocVersion(0, 2, 0), DocVersion(0, 2, 1)]

    def test_list_count(self):
        for i in range(5):
            self.history.record("doc1", f"content version {i} unique text here", ChangeType.MINOR)
        assert len(self.history.list_versions("doc1")) == 5


class TestVersionHistoryDiffSummary:
    def setup_method(self):
        self.history = VersionHistory()
        self.history.record("doc1", "initial text", ChangeType.MINOR)
        self.history.record("doc1", "updated text with more words here added", ChangeType.MINOR)
        self.history.record("doc1", "typo fix", ChangeType.PATCH)

    def test_diff_summary_format(self):
        summary = self.history.diff_summary("doc1", "0.1.0", "0.2.0")
        assert summary == "v0.1.0 → v0.2.0: MINOR"

    def test_diff_summary_patch(self):
        summary = self.history.diff_summary("doc1", "0.2.0", "0.2.1")
        assert summary == "v0.2.0 → v0.2.1: PATCH"

    def test_diff_summary_unknown_from_raises(self):
        with pytest.raises(KeyError):
            self.history.diff_summary("doc1", "9.9.9", "0.2.0")

    def test_diff_summary_unknown_to_raises(self):
        with pytest.raises(KeyError):
            self.history.diff_summary("doc1", "0.1.0", "9.9.9")


class TestVersionHistoryAllDocs:
    def setup_method(self):
        self.history = VersionHistory()

    def test_all_docs_empty(self):
        assert self.history.all_docs() == []

    def test_all_docs_sorted(self):
        self.history.record("beta", "b", ChangeType.MINOR)
        self.history.record("alpha", "a", ChangeType.MINOR)
        self.history.record("gamma", "g", ChangeType.MINOR)
        assert self.history.all_docs() == ["alpha", "beta", "gamma"]

    def test_all_docs_no_duplicates(self):
        self.history.record("doc1", "v1", ChangeType.MINOR)
        self.history.record("doc1", "v2 more content here", ChangeType.MINOR)
        assert self.history.all_docs() == ["doc1"]

    def test_all_docs_multiple(self):
        for name in ["x", "y", "z"]:
            self.history.record(name, f"content for {name}", ChangeType.MINOR)
        assert set(self.history.all_docs()) == {"x", "y", "z"}


class TestVersionHistoryIsolation:
    """Ensure separate VersionHistory instances share no state."""

    def test_separate_instances_independent(self):
        h1 = VersionHistory()
        h2 = VersionHistory()
        h1.record("doc1", "content", ChangeType.MINOR)
        assert h2.latest("doc1") is None


class TestVersionHistoryIntegration:
    """End-to-end scenario exercising ChangeDetector + VersionHistory together."""

    def test_full_workflow(self):
        history = VersionHistory()
        detector = ChangeDetector()

        original = "# Introduction\n\nThis is the first version of the document."
        history.record("guide.md", original, ChangeType.MINOR)

        # Typo fix
        v2_text = "# Introduction\n\nThis is the first version of the document"
        ct2 = detector.detect(original, v2_text)
        history.record("guide.md", v2_text, ct2)

        # Large content addition
        v3_text = v2_text + "\n\n" + " ".join(["extra content word"] * 60)
        ct3 = detector.detect(v2_text, v3_text)
        history.record("guide.md", v3_text, ct3)

        versions = history.list_versions("guide.md")
        assert versions[0].version == DocVersion(0, 1, 0)
        assert len(versions) == 3
