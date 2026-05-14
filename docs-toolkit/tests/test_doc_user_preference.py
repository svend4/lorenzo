"""Tests for E372 DocUserPreference."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_user_preference import (
    DocUserPreference,
    Preference,
    PreferenceStats,
)


# ---------------------------------------------------------------------- #
# Dataclasses
# ---------------------------------------------------------------------- #
class TestPreferenceDataclass:
    def test_construct_basic(self):
        p = Preference(user_id="u1", key="theme", value="dark")
        assert p.user_id == "u1"
        assert p.key == "theme"
        assert p.value == "dark"
        assert p.updated_at == 0.0

    def test_construct_with_timestamp(self):
        p = Preference(user_id="u1", key="theme", value="dark", updated_at=42.0)
        assert p.updated_at == 42.0

    def test_value_can_be_any_type_int(self):
        p = Preference(user_id="u1", key="size", value=14)
        assert p.value == 14

    def test_value_can_be_any_type_list(self):
        p = Preference(user_id="u1", key="tags", value=["a", "b"])
        assert p.value == ["a", "b"]

    def test_equality(self):
        a = Preference("u1", "k", "v", 1.0)
        b = Preference("u1", "k", "v", 1.0)
        assert a == b

    def test_inequality(self):
        a = Preference("u1", "k", "v", 1.0)
        b = Preference("u1", "k", "v", 2.0)
        assert a != b


class TestPreferenceStatsDataclass:
    def test_construct(self):
        s = PreferenceStats(
            total_preferences=10,
            unique_users=3,
            unique_keys=4,
            default_count=2,
        )
        assert s.total_preferences == 10
        assert s.unique_users == 3
        assert s.unique_keys == 4
        assert s.default_count == 2

    def test_equality(self):
        a = PreferenceStats(1, 2, 3, 4)
        b = PreferenceStats(1, 2, 3, 4)
        assert a == b

    def test_inequality(self):
        a = PreferenceStats(1, 2, 3, 4)
        b = PreferenceStats(9, 2, 3, 4)
        assert a != b


# ---------------------------------------------------------------------- #
# Construction
# ---------------------------------------------------------------------- #
class TestConstruction:
    def test_empty_on_init(self):
        store = DocUserPreference()
        assert store.defaults() == {}
        assert store.all_keys() == []

    def test_stats_empty(self):
        store = DocUserPreference()
        s = store.stats()
        assert s.total_preferences == 0
        assert s.unique_users == 0
        assert s.unique_keys == 0
        assert s.default_count == 0


# ---------------------------------------------------------------------- #
# Defaults
# ---------------------------------------------------------------------- #
class TestSetDefault:
    def test_new(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        assert store.get_default("theme") == "light"

    def test_replace(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        store.set_default("theme", "dark")
        assert store.get_default("theme") == "dark"

    def test_multiple_keys(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        store.set_default("lang", "en")
        assert store.get_default("theme") == "light"
        assert store.get_default("lang") == "en"


class TestGetDefault:
    def test_found(self):
        store = DocUserPreference()
        store.set_default("theme", "dark")
        assert store.get_default("theme") == "dark"

    def test_none_for_unknown(self):
        store = DocUserPreference()
        assert store.get_default("missing") is None


class TestDefaults:
    def test_copy_returns_all(self):
        store = DocUserPreference()
        store.set_default("a", 1)
        store.set_default("b", 2)
        assert store.defaults() == {"a": 1, "b": 2}

    def test_copy_independent(self):
        store = DocUserPreference()
        store.set_default("a", 1)
        copy = store.defaults()
        copy["a"] = 999
        assert store.get_default("a") == 1

    def test_empty(self):
        store = DocUserPreference()
        assert store.defaults() == {}


class TestRemoveDefault:
    def test_true_when_existed(self):
        store = DocUserPreference()
        store.set_default("a", 1)
        assert store.remove_default("a") is True
        assert store.get_default("a") is None

    def test_false_when_missing(self):
        store = DocUserPreference()
        assert store.remove_default("missing") is False


# ---------------------------------------------------------------------- #
# Preferences
# ---------------------------------------------------------------------- #
class TestSetPreference:
    def test_new(self):
        store = DocUserPreference()
        p = store.set_preference("u1", "theme", "dark")
        assert p.user_id == "u1"
        assert p.key == "theme"
        assert p.value == "dark"

    def test_replace(self):
        store = DocUserPreference()
        store.set_preference("u1", "theme", "dark")
        store.set_preference("u1", "theme", "light")
        assert store.get_preference("u1", "theme") == "light"

    def test_timestamp_default(self):
        store = DocUserPreference()
        before = time.time()
        p = store.set_preference("u1", "theme", "dark")
        after = time.time()
        assert before <= p.updated_at <= after

    def test_timestamp_provided(self):
        store = DocUserPreference()
        p = store.set_preference("u1", "theme", "dark", now=123.0)
        assert p.updated_at == 123.0


class TestGetPreference:
    def test_user_value(self):
        store = DocUserPreference()
        store.set_preference("u1", "theme", "dark")
        assert store.get_preference("u1", "theme") == "dark"

    def test_fallback_to_default(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        assert store.get_preference("u_unknown", "theme") == "light"

    def test_none_if_neither(self):
        store = DocUserPreference()
        assert store.get_preference("u1", "missing") is None

    def test_user_overrides_default(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        store.set_preference("u1", "theme", "dark")
        assert store.get_preference("u1", "theme") == "dark"

    def test_other_user_gets_default(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        store.set_preference("u1", "theme", "dark")
        assert store.get_preference("u2", "theme") == "light"


class TestGetRaw:
    def test_none_if_not_set(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        assert store.get_raw("u1", "theme") is None

    def test_returns_pref(self):
        store = DocUserPreference()
        store.set_preference("u1", "theme", "dark", now=10.0)
        raw = store.get_raw("u1", "theme")
        assert raw is not None
        assert raw.value == "dark"
        assert raw.updated_at == 10.0

    def test_none_unknown_user(self):
        store = DocUserPreference()
        store.set_preference("u1", "theme", "dark")
        assert store.get_raw("u2", "theme") is None


class TestDeletePreference:
    def test_true_when_existed(self):
        store = DocUserPreference()
        store.set_preference("u1", "theme", "dark")
        assert store.delete_preference("u1", "theme") is True
        assert store.get_raw("u1", "theme") is None

    def test_false_when_missing(self):
        store = DocUserPreference()
        assert store.delete_preference("u1", "theme") is False

    def test_user_falls_back_after_delete(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        store.set_preference("u1", "theme", "dark")
        store.delete_preference("u1", "theme")
        assert store.get_preference("u1", "theme") == "light"


class TestPreferencesForUser:
    def test_sorted_by_key(self):
        store = DocUserPreference()
        store.set_preference("u1", "theme", "dark")
        store.set_preference("u1", "lang", "en")
        store.set_preference("u1", "size", 14)
        prefs = store.preferences_for_user("u1")
        assert [p.key for p in prefs] == ["lang", "size", "theme"]

    def test_empty_for_unknown_user(self):
        store = DocUserPreference()
        assert store.preferences_for_user("u_unknown") == []

    def test_only_own_prefs(self):
        store = DocUserPreference()
        store.set_preference("u1", "theme", "dark")
        store.set_preference("u2", "theme", "light")
        prefs = store.preferences_for_user("u1")
        assert len(prefs) == 1
        assert prefs[0].user_id == "u1"


class TestUsersWithPreference:
    def test_sorted(self):
        store = DocUserPreference()
        store.set_preference("zeta", "theme", "dark")
        store.set_preference("alpha", "theme", "light")
        store.set_preference("mid", "theme", "auto")
        assert store.users_with_preference("theme") == ["alpha", "mid", "zeta"]

    def test_empty_for_unknown_key(self):
        store = DocUserPreference()
        assert store.users_with_preference("missing") == []

    def test_ignores_other_keys(self):
        store = DocUserPreference()
        store.set_preference("u1", "theme", "dark")
        store.set_preference("u2", "lang", "en")
        assert store.users_with_preference("theme") == ["u1"]


class TestResetToDefault:
    def test_true_when_existed(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        store.set_preference("u1", "theme", "dark")
        assert store.reset_to_default("u1", "theme") is True
        assert store.get_preference("u1", "theme") == "light"

    def test_false_when_missing(self):
        store = DocUserPreference()
        assert store.reset_to_default("u1", "theme") is False

    def test_idempotent(self):
        store = DocUserPreference()
        store.set_preference("u1", "theme", "dark")
        assert store.reset_to_default("u1", "theme") is True
        assert store.reset_to_default("u1", "theme") is False


class TestClearUser:
    def test_count(self):
        store = DocUserPreference()
        store.set_preference("u1", "a", 1)
        store.set_preference("u1", "b", 2)
        store.set_preference("u1", "c", 3)
        assert store.clear_user("u1") == 3
        assert store.preferences_for_user("u1") == []

    def test_zero_for_unknown(self):
        store = DocUserPreference()
        assert store.clear_user("u_unknown") == 0

    def test_does_not_affect_others(self):
        store = DocUserPreference()
        store.set_preference("u1", "a", 1)
        store.set_preference("u2", "a", 2)
        store.clear_user("u1")
        assert store.get_preference("u2", "a") == 2


class TestAllKeys:
    def test_sorted_union(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        store.set_default("lang", "en")
        store.set_preference("u1", "size", 14)
        store.set_preference("u1", "lang", "de")
        assert store.all_keys() == ["lang", "size", "theme"]

    def test_empty(self):
        store = DocUserPreference()
        assert store.all_keys() == []

    def test_only_defaults(self):
        store = DocUserPreference()
        store.set_default("a", 1)
        store.set_default("b", 2)
        assert store.all_keys() == ["a", "b"]

    def test_only_prefs(self):
        store = DocUserPreference()
        store.set_preference("u1", "x", 1)
        store.set_preference("u2", "y", 2)
        assert store.all_keys() == ["x", "y"]


class TestStats:
    def test_totals(self):
        store = DocUserPreference()
        store.set_default("theme", "light")
        store.set_default("lang", "en")
        store.set_preference("u1", "theme", "dark")
        store.set_preference("u1", "size", 14)
        store.set_preference("u2", "theme", "auto")
        s = store.stats()
        assert s.total_preferences == 3
        assert s.unique_users == 2
        assert s.unique_keys == 2  # theme, size
        assert s.default_count == 2

    def test_stats_after_delete(self):
        store = DocUserPreference()
        store.set_preference("u1", "a", 1)
        store.delete_preference("u1", "a")
        s = store.stats()
        assert s.total_preferences == 0
        assert s.unique_users == 0

    def test_stats_after_clear(self):
        store = DocUserPreference()
        store.set_preference("u1", "a", 1)
        store.set_preference("u1", "b", 2)
        store.clear_user("u1")
        s = store.stats()
        assert s.total_preferences == 0


# ---------------------------------------------------------------------- #
# Thread safety
# ---------------------------------------------------------------------- #
class TestThreadSafety:
    def test_concurrent_set_preference(self):
        store = DocUserPreference()
        N = 50
        threads = []

        def worker(uid: int) -> None:
            for i in range(10):
                store.set_preference(f"u{uid}", f"k{i}", uid * 100 + i)

        for t in range(N):
            th = threading.Thread(target=worker, args=(t,))
            threads.append(th)
            th.start()
        for th in threads:
            th.join()

        s = store.stats()
        assert s.total_preferences == N * 10
        assert s.unique_users == N
        assert s.unique_keys == 10

    def test_concurrent_set_and_delete(self):
        store = DocUserPreference()
        for i in range(20):
            store.set_preference("u1", f"k{i}", i)

        def deleter() -> None:
            for i in range(20):
                store.delete_preference("u1", f"k{i}")

        def setter() -> None:
            for i in range(20):
                store.set_preference("u2", f"k{i}", i)

        t1 = threading.Thread(target=deleter)
        t2 = threading.Thread(target=setter)
        t1.start(); t2.start()
        t1.join(); t2.join()

        # All u1 keys should be gone, all u2 keys should be present.
        assert store.preferences_for_user("u1") == []
        assert len(store.preferences_for_user("u2")) == 20
