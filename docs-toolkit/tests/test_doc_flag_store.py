"""Tests for E311 DocFlagStore."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_flag_store import (
    DocFlagStore,
    Flag,
    FlagOverride,
    FlagStats,
)


# ---------------------------------------------------------------------------
# TestFlagDataclass
# ---------------------------------------------------------------------------


class TestFlagDataclass:
    def test_default_enabled_false(self):
        f = Flag(name="my_flag")
        assert f.enabled is False

    def test_custom_enabled_true(self):
        f = Flag(name="my_flag", enabled=True)
        assert f.enabled is True

    def test_default_description_empty(self):
        f = Flag(name="my_flag")
        assert f.description == ""

    def test_custom_description(self):
        f = Flag(name="my_flag", description="some desc")
        assert f.description == "some desc"

    def test_default_rollout_pct(self):
        f = Flag(name="my_flag")
        assert f.rollout_pct == 100.0

    def test_custom_rollout_pct(self):
        f = Flag(name="my_flag", rollout_pct=25.0)
        assert f.rollout_pct == 25.0

    def test_name_stored(self):
        f = Flag(name="alpha")
        assert f.name == "alpha"


# ---------------------------------------------------------------------------
# TestFlagOverrideDataclass
# ---------------------------------------------------------------------------


class TestFlagOverrideDataclass:
    def test_fields_stored(self):
        ov = FlagOverride(doc_id="d1", flag_name="flag_a", enabled=True)
        assert ov.doc_id == "d1"
        assert ov.flag_name == "flag_a"
        assert ov.enabled is True

    def test_default_set_at_zero(self):
        ov = FlagOverride(doc_id="d1", flag_name="flag_a", enabled=False)
        assert ov.set_at == 0.0

    def test_custom_set_at(self):
        ts = 1_700_000_000.0
        ov = FlagOverride(doc_id="d1", flag_name="flag_a", enabled=True, set_at=ts)
        assert ov.set_at == ts


# ---------------------------------------------------------------------------
# TestFlagStatsDataclass
# ---------------------------------------------------------------------------


class TestFlagStatsDataclass:
    def test_all_fields(self):
        s = FlagStats(
            total_flags=5,
            enabled_flags=2,
            total_overrides=10,
            docs_with_overrides=3,
        )
        assert s.total_flags == 5
        assert s.enabled_flags == 2
        assert s.total_overrides == 10
        assert s.docs_with_overrides == 3


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_store(self):
        store = DocFlagStore()
        assert store.list_flags() == []

    def test_empty_stats(self):
        store = DocFlagStore()
        s = store.stats()
        assert s.total_flags == 0
        assert s.enabled_flags == 0
        assert s.total_overrides == 0
        assert s.docs_with_overrides == 0


# ---------------------------------------------------------------------------
# TestDefineFlag
# ---------------------------------------------------------------------------


class TestDefineFlag:
    def test_define_new_flag(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="alpha"))
        assert store.get_flag("alpha") is not None

    def test_define_flag_defaults(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="alpha"))
        f = store.get_flag("alpha")
        assert f.enabled is False
        assert f.description == ""
        assert f.rollout_pct == 100.0

    def test_define_flag_with_values(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="beta", enabled=True, description="desc", rollout_pct=50.0))
        f = store.get_flag("beta")
        assert f.enabled is True
        assert f.description == "desc"
        assert f.rollout_pct == 50.0

    def test_replace_flag(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="gamma", enabled=False))
        store.define_flag(Flag(name="gamma", enabled=True, description="updated"))
        f = store.get_flag("gamma")
        assert f.enabled is True
        assert f.description == "updated"

    def test_define_multiple_flags(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="a"))
        store.define_flag(Flag(name="b"))
        store.define_flag(Flag(name="c"))
        assert len(store.list_flags()) == 3


# ---------------------------------------------------------------------------
# TestUndefineFlag
# ---------------------------------------------------------------------------


class TestUndefineFlag:
    def test_undefine_existing_flag_returns_true(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="x"))
        assert store.undefine_flag("x") is True

    def test_undefine_removes_flag(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="x"))
        store.undefine_flag("x")
        assert store.get_flag("x") is None

    def test_undefine_unknown_flag_returns_false(self):
        store = DocFlagStore()
        assert store.undefine_flag("nonexistent") is False

    def test_undefine_removes_associated_overrides(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="feature_x"))
        store.set_override("doc1", "feature_x", True)
        store.set_override("doc2", "feature_x", False)
        store.undefine_flag("feature_x")
        assert store.get_override("doc1", "feature_x") is None
        assert store.get_override("doc2", "feature_x") is None

    def test_undefine_leaves_other_flags_intact(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="keep"))
        store.define_flag(Flag(name="remove"))
        store.undefine_flag("remove")
        assert store.get_flag("keep") is not None

    def test_undefine_leaves_other_overrides_intact(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="flag_a"))
        store.define_flag(Flag(name="flag_b"))
        store.set_override("doc1", "flag_a", True)
        store.set_override("doc1", "flag_b", True)
        store.undefine_flag("flag_a")
        assert store.get_override("doc1", "flag_b") is not None


# ---------------------------------------------------------------------------
# TestGetFlag
# ---------------------------------------------------------------------------


class TestGetFlag:
    def test_get_existing_flag(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="z", enabled=True))
        f = store.get_flag("z")
        assert f is not None
        assert f.name == "z"

    def test_get_nonexistent_flag_returns_none(self):
        store = DocFlagStore()
        assert store.get_flag("missing") is None


# ---------------------------------------------------------------------------
# TestSetEnabled
# ---------------------------------------------------------------------------


class TestSetEnabled:
    def test_set_enabled_true(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="feat", enabled=False))
        result = store.set_enabled("feat", True)
        assert result is True
        assert store.get_flag("feat").enabled is True

    def test_set_enabled_false(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="feat", enabled=True))
        result = store.set_enabled("feat", False)
        assert result is True
        assert store.get_flag("feat").enabled is False

    def test_set_enabled_unknown_flag_returns_false(self):
        store = DocFlagStore()
        result = store.set_enabled("no_such_flag", True)
        assert result is False

    def test_set_enabled_preserves_other_fields(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="feat", enabled=False, description="d", rollout_pct=42.0))
        store.set_enabled("feat", True)
        f = store.get_flag("feat")
        assert f.description == "d"
        assert f.rollout_pct == 42.0


# ---------------------------------------------------------------------------
# TestListFlags
# ---------------------------------------------------------------------------


class TestListFlags:
    def test_list_empty(self):
        store = DocFlagStore()
        assert store.list_flags() == []

    def test_list_sorted_by_name(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="charlie"))
        store.define_flag(Flag(name="alpha"))
        store.define_flag(Flag(name="bravo"))
        names = [f.name for f in store.list_flags()]
        assert names == ["alpha", "bravo", "charlie"]

    def test_list_returns_flag_objects(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="f1", enabled=True))
        flags = store.list_flags()
        assert len(flags) == 1
        assert isinstance(flags[0], Flag)


# ---------------------------------------------------------------------------
# TestSetOverride
# ---------------------------------------------------------------------------


class TestSetOverride:
    def test_set_override_creates_entry(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="f"))
        ov = store.set_override("doc1", "f", True)
        assert ov.doc_id == "doc1"
        assert ov.flag_name == "f"
        assert ov.enabled is True

    def test_set_override_timestamp_set(self):
        store = DocFlagStore()
        before = time.time()
        ov = store.set_override("doc1", "f", True)
        after = time.time()
        assert before <= ov.set_at <= after

    def test_set_override_custom_timestamp(self):
        store = DocFlagStore()
        ts = 9_000.0
        ov = store.set_override("doc1", "f", True, now=ts)
        assert ov.set_at == ts

    def test_set_override_replace(self):
        store = DocFlagStore()
        store.set_override("doc1", "f", True, now=1.0)
        ov2 = store.set_override("doc1", "f", False, now=2.0)
        assert ov2.enabled is False
        assert ov2.set_at == 2.0

    def test_set_override_returns_flag_override(self):
        store = DocFlagStore()
        ov = store.set_override("d", "flag", False)
        assert isinstance(ov, FlagOverride)


# ---------------------------------------------------------------------------
# TestRemoveOverride
# ---------------------------------------------------------------------------


class TestRemoveOverride:
    def test_remove_existing_override_returns_true(self):
        store = DocFlagStore()
        store.set_override("doc1", "f", True)
        assert store.remove_override("doc1", "f") is True

    def test_remove_override_actually_removes(self):
        store = DocFlagStore()
        store.set_override("doc1", "f", True)
        store.remove_override("doc1", "f")
        assert store.get_override("doc1", "f") is None

    def test_remove_nonexistent_override_returns_false(self):
        store = DocFlagStore()
        assert store.remove_override("doc1", "no_flag") is False


# ---------------------------------------------------------------------------
# TestGetOverride
# ---------------------------------------------------------------------------


class TestGetOverride:
    def test_get_existing_override(self):
        store = DocFlagStore()
        store.set_override("doc1", "flag_a", True)
        ov = store.get_override("doc1", "flag_a")
        assert ov is not None
        assert ov.enabled is True

    def test_get_nonexistent_override_returns_none(self):
        store = DocFlagStore()
        assert store.get_override("doc_missing", "flag_missing") is None


# ---------------------------------------------------------------------------
# TestIsEnabled
# ---------------------------------------------------------------------------


class TestIsEnabled:
    def test_override_true_wins(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="f", enabled=False))
        store.set_override("doc1", "f", True)
        assert store.is_enabled("doc1", "f") is True

    def test_override_false_wins(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="f", enabled=True))
        store.set_override("doc1", "f", False)
        assert store.is_enabled("doc1", "f") is False

    def test_falls_back_to_global_when_no_override(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="f", enabled=True))
        assert store.is_enabled("doc_no_override", "f") is True

    def test_falls_back_to_global_false(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="f", enabled=False))
        assert store.is_enabled("any_doc", "f") is False

    def test_unknown_flag_returns_false(self):
        store = DocFlagStore()
        assert store.is_enabled("doc1", "undefined_flag") is False

    def test_override_for_other_doc_does_not_affect_this_doc(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="f", enabled=False))
        store.set_override("doc_other", "f", True)
        assert store.is_enabled("doc_me", "f") is False


# ---------------------------------------------------------------------------
# TestOverridesForDoc
# ---------------------------------------------------------------------------


class TestOverridesForDoc:
    def test_returns_overrides_for_doc(self):
        store = DocFlagStore()
        store.set_override("doc1", "flag_b", True)
        store.set_override("doc1", "flag_a", False)
        ovs = store.overrides_for_doc("doc1")
        assert len(ovs) == 2

    def test_sorted_by_flag_name(self):
        store = DocFlagStore()
        store.set_override("doc1", "zz_flag", True)
        store.set_override("doc1", "aa_flag", False)
        ovs = store.overrides_for_doc("doc1")
        assert [ov.flag_name for ov in ovs] == ["aa_flag", "zz_flag"]

    def test_only_matching_doc(self):
        store = DocFlagStore()
        store.set_override("doc1", "f", True)
        store.set_override("doc2", "f", False)
        ovs = store.overrides_for_doc("doc1")
        assert all(ov.doc_id == "doc1" for ov in ovs)

    def test_empty_for_unknown_doc(self):
        store = DocFlagStore()
        assert store.overrides_for_doc("ghost_doc") == []


# ---------------------------------------------------------------------------
# TestOverridesForFlag
# ---------------------------------------------------------------------------


class TestOverridesForFlag:
    def test_returns_overrides_for_flag(self):
        store = DocFlagStore()
        store.set_override("doc_b", "flag_x", True)
        store.set_override("doc_a", "flag_x", False)
        ovs = store.overrides_for_flag("flag_x")
        assert len(ovs) == 2

    def test_sorted_by_doc_id(self):
        store = DocFlagStore()
        store.set_override("doc_z", "flag_x", True)
        store.set_override("doc_a", "flag_x", True)
        ovs = store.overrides_for_flag("flag_x")
        assert [ov.doc_id for ov in ovs] == ["doc_a", "doc_z"]

    def test_only_matching_flag(self):
        store = DocFlagStore()
        store.set_override("doc1", "flag_x", True)
        store.set_override("doc1", "flag_y", False)
        ovs = store.overrides_for_flag("flag_x")
        assert all(ov.flag_name == "flag_x" for ov in ovs)

    def test_empty_for_unknown_flag(self):
        store = DocFlagStore()
        assert store.overrides_for_flag("ghost_flag") == []


# ---------------------------------------------------------------------------
# TestDocsWithFlagEnabled
# ---------------------------------------------------------------------------


class TestDocsWithFlagEnabled:
    def test_returns_docs_with_enabled_override(self):
        store = DocFlagStore()
        store.set_override("doc_a", "feat", True)
        store.set_override("doc_b", "feat", True)
        store.set_override("doc_c", "feat", False)
        docs = store.docs_with_flag_enabled("feat")
        assert set(docs) == {"doc_a", "doc_b"}

    def test_excludes_disabled_overrides(self):
        store = DocFlagStore()
        store.set_override("doc1", "feat", False)
        assert store.docs_with_flag_enabled("feat") == []

    def test_sorted_result(self):
        store = DocFlagStore()
        store.set_override("doc_z", "feat", True)
        store.set_override("doc_a", "feat", True)
        docs = store.docs_with_flag_enabled("feat")
        assert docs == ["doc_a", "doc_z"]

    def test_empty_for_unknown_flag(self):
        store = DocFlagStore()
        assert store.docs_with_flag_enabled("no_such_flag") == []

    def test_does_not_include_docs_without_override(self):
        # Even if the global flag is enabled, only overrides are scanned
        store = DocFlagStore()
        store.define_flag(Flag(name="feat", enabled=True))
        # No override set for any doc
        assert store.docs_with_flag_enabled("feat") == []


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty_store_stats(self):
        store = DocFlagStore()
        s = store.stats()
        assert s.total_flags == 0
        assert s.enabled_flags == 0
        assert s.total_overrides == 0
        assert s.docs_with_overrides == 0

    def test_total_flags_count(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="a"))
        store.define_flag(Flag(name="b"))
        assert store.stats().total_flags == 2

    def test_enabled_flags_count(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="on", enabled=True))
        store.define_flag(Flag(name="off", enabled=False))
        assert store.stats().enabled_flags == 1

    def test_total_overrides_count(self):
        store = DocFlagStore()
        store.set_override("d1", "f1", True)
        store.set_override("d1", "f2", False)
        store.set_override("d2", "f1", True)
        assert store.stats().total_overrides == 3

    def test_docs_with_overrides_count(self):
        store = DocFlagStore()
        store.set_override("d1", "f1", True)
        store.set_override("d1", "f2", False)
        store.set_override("d2", "f1", True)
        assert store.stats().docs_with_overrides == 2

    def test_stats_after_remove(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="f", enabled=True))
        store.set_override("d1", "f", False)
        store.remove_override("d1", "f")
        s = store.stats()
        assert s.total_overrides == 0
        assert s.docs_with_overrides == 0

    def test_stats_after_undefine_flag(self):
        store = DocFlagStore()
        store.define_flag(Flag(name="f"))
        store.set_override("d1", "f", True)
        store.undefine_flag("f")
        s = store.stats()
        assert s.total_flags == 0
        assert s.total_overrides == 0


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_set_override(self):
        """Multiple threads setting overrides must not lose entries."""
        store = DocFlagStore()
        store.define_flag(Flag(name="flag"))
        errors: list[Exception] = []

        def worker(doc_id: str) -> None:
            try:
                store.set_override(doc_id, "flag", True)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = [
            threading.Thread(target=worker, args=(f"doc_{i}",))
            for i in range(50)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
        assert store.stats().total_overrides == 50

    def test_concurrent_define_and_read(self):
        """Concurrent define_flag and list_flags must not raise."""
        store = DocFlagStore()
        errors: list[Exception] = []

        def writer(i: int) -> None:
            try:
                store.define_flag(Flag(name=f"flag_{i}"))
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def reader() -> None:
            try:
                store.list_flags()
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = (
            [threading.Thread(target=writer, args=(i,)) for i in range(30)]
            + [threading.Thread(target=reader) for _ in range(20)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
