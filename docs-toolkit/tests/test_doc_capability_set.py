"""Tests for E387 DocCapabilitySet."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_capability_set import (
    Capability,
    CapabilityStats,
    DocCapabilitySet,
)


# ---------------------------------------------------------------------------
# Capability dataclass
# ---------------------------------------------------------------------------
class TestCapabilityDataclass:
    def test_required_name(self):
        c = Capability(name="search")
        assert c.name == "search"

    def test_default_description_empty(self):
        c = Capability(name="x")
        assert c.description == ""

    def test_default_enabled_false(self):
        c = Capability(name="x")
        assert c.default_enabled is False

    def test_custom_description(self):
        c = Capability(name="x", description="hello")
        assert c.description == "hello"

    def test_custom_default_enabled(self):
        c = Capability(name="x", default_enabled=True)
        assert c.default_enabled is True

    def test_equality(self):
        a = Capability(name="x", description="d", default_enabled=True)
        b = Capability(name="x", description="d", default_enabled=True)
        assert a == b

    def test_inequality(self):
        assert Capability(name="x") != Capability(name="y")


# ---------------------------------------------------------------------------
# CapabilityStats dataclass
# ---------------------------------------------------------------------------
class TestCapabilityStatsDataclass:
    def test_fields(self):
        s = CapabilityStats(
            total_capabilities=1, total_docs=2, total_assignments=3
        )
        assert s.total_capabilities == 1
        assert s.total_docs == 2
        assert s.total_assignments == 3

    def test_equality(self):
        a = CapabilityStats(1, 2, 3)
        b = CapabilityStats(1, 2, 3)
        assert a == b

    def test_inequality(self):
        assert CapabilityStats(1, 2, 3) != CapabilityStats(1, 2, 4)


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty_on_init(self):
        s = DocCapabilitySet()
        assert s.list_capabilities() == []
        assert s.all_doc_ids() == []

    def test_stats_empty(self):
        s = DocCapabilitySet()
        assert s.stats() == CapabilityStats(0, 0, 0)


# ---------------------------------------------------------------------------
# define_capability
# ---------------------------------------------------------------------------
class TestDefineCapability:
    def test_define_one(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="search"))
        assert s.get_capability("search").name == "search"

    def test_define_replaces(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x", description="a"))
        s.define_capability(Capability(name="x", description="b"))
        assert s.get_capability("x").description == "b"

    def test_define_multiple(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a"))
        s.define_capability(Capability(name="b"))
        assert {c.name for c in s.list_capabilities()} == {"a", "b"}


# ---------------------------------------------------------------------------
# undefine_capability — cascade
# ---------------------------------------------------------------------------
class TestUndefineCapability:
    def test_undefine_existing_returns_true(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        assert s.undefine_capability("x") is True

    def test_undefine_unknown_returns_false(self):
        s = DocCapabilitySet()
        assert s.undefine_capability("nope") is False

    def test_undefine_removes_definition(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        s.undefine_capability("x")
        assert s.get_capability("x") is None

    def test_cascade_removes_from_docs(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        s.define_capability(Capability(name="y"))
        s.enable("d1", "x")
        s.enable("d1", "y")
        s.undefine_capability("x")
        assert s.capabilities_of("d1") == {"y": True}

    def test_cascade_drops_doc_when_empty(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        s.enable("d1", "x")
        s.undefine_capability("x")
        assert "d1" not in s.all_doc_ids()


# ---------------------------------------------------------------------------
# get_capability
# ---------------------------------------------------------------------------
class TestGetCapability:
    def test_get_existing(self):
        s = DocCapabilitySet()
        c = Capability(name="x", description="d")
        s.define_capability(c)
        got = s.get_capability("x")
        assert got is not None and got.description == "d"

    def test_get_missing(self):
        s = DocCapabilitySet()
        assert s.get_capability("nope") is None


# ---------------------------------------------------------------------------
# list_capabilities
# ---------------------------------------------------------------------------
class TestListCapabilities:
    def test_sorted_by_name(self):
        s = DocCapabilitySet()
        for name in ["c", "a", "b"]:
            s.define_capability(Capability(name=name))
        assert [c.name for c in s.list_capabilities()] == ["a", "b", "c"]

    def test_empty(self):
        assert DocCapabilitySet().list_capabilities() == []


# ---------------------------------------------------------------------------
# set_capability — undefined returns False
# ---------------------------------------------------------------------------
class TestSetCapability:
    def test_undefined_returns_false(self):
        s = DocCapabilitySet()
        assert s.set_capability("d1", "x", True) is False

    def test_defined_returns_true(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        assert s.set_capability("d1", "x", True) is True

    def test_undefined_does_not_record(self):
        s = DocCapabilitySet()
        s.set_capability("d1", "x", True)
        assert s.capabilities_of("d1") == {}

    def test_overwrite(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        s.set_capability("d1", "x", True)
        s.set_capability("d1", "x", False)
        assert s.capabilities_of("d1") == {"x": False}


# ---------------------------------------------------------------------------
# enable / disable
# ---------------------------------------------------------------------------
class TestEnableDisable:
    def test_enable_sets_true(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        s.enable("d1", "x")
        assert s.is_enabled("d1", "x") is True

    def test_disable_sets_false(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x", default_enabled=True))
        s.disable("d1", "x")
        assert s.is_enabled("d1", "x") is False

    def test_enable_undefined_false(self):
        s = DocCapabilitySet()
        assert s.enable("d1", "x") is False

    def test_disable_undefined_false(self):
        s = DocCapabilitySet()
        assert s.disable("d1", "x") is False


# ---------------------------------------------------------------------------
# is_enabled — override + default fallback
# ---------------------------------------------------------------------------
class TestIsEnabled:
    def test_unknown_cap_false(self):
        s = DocCapabilitySet()
        assert s.is_enabled("d1", "x") is False

    def test_default_enabled_true(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x", default_enabled=True))
        assert s.is_enabled("d1", "x") is True

    def test_default_enabled_false(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        assert s.is_enabled("d1", "x") is False

    def test_override_true_beats_default_false(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        s.enable("d1", "x")
        assert s.is_enabled("d1", "x") is True

    def test_override_false_beats_default_true(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x", default_enabled=True))
        s.disable("d1", "x")
        assert s.is_enabled("d1", "x") is False

    def test_override_per_doc(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x", default_enabled=True))
        s.disable("d1", "x")
        assert s.is_enabled("d1", "x") is False
        assert s.is_enabled("d2", "x") is True


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------
class TestClearDoc:
    def test_clear_unknown_zero(self):
        assert DocCapabilitySet().clear_doc("nope") == 0

    def test_clear_returns_count(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a"))
        s.define_capability(Capability(name="b"))
        s.enable("d1", "a")
        s.enable("d1", "b")
        assert s.clear_doc("d1") == 2

    def test_clear_removes_doc(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a"))
        s.enable("d1", "a")
        s.clear_doc("d1")
        assert "d1" not in s.all_doc_ids()
        assert s.capabilities_of("d1") == {}


# ---------------------------------------------------------------------------
# capabilities_of — copy
# ---------------------------------------------------------------------------
class TestCapabilitiesOf:
    def test_returns_explicit_only(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a", default_enabled=True))
        s.define_capability(Capability(name="b"))
        s.enable("d1", "b")
        # 'a' default-on is not explicit
        assert s.capabilities_of("d1") == {"b": True}

    def test_returns_copy(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a"))
        s.enable("d1", "a")
        snap = s.capabilities_of("d1")
        snap["a"] = False
        assert s.is_enabled("d1", "a") is True

    def test_empty_for_unknown_doc(self):
        s = DocCapabilitySet()
        assert s.capabilities_of("nope") == {}


# ---------------------------------------------------------------------------
# enabled_capabilities — sorted, with defaults
# ---------------------------------------------------------------------------
class TestEnabledCapabilities:
    def test_sorted(self):
        s = DocCapabilitySet()
        for name in ["c", "a", "b"]:
            s.define_capability(Capability(name=name))
            s.enable("d1", name)
        assert s.enabled_capabilities("d1") == ["a", "b", "c"]

    def test_includes_defaults_when_no_override(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a", default_enabled=True))
        s.define_capability(Capability(name="b"))
        assert s.enabled_capabilities("d1") == ["a"]

    def test_override_false_excludes_default(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a", default_enabled=True))
        s.disable("d1", "a")
        assert s.enabled_capabilities("d1") == []

    def test_combines_default_and_override(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a", default_enabled=True))
        s.define_capability(Capability(name="b"))
        s.enable("d1", "b")
        assert s.enabled_capabilities("d1") == ["a", "b"]


# ---------------------------------------------------------------------------
# docs_with_capability — enabled filter
# ---------------------------------------------------------------------------
class TestDocsWithCapability:
    def test_explicit_none_returns_set(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        s.enable("d1", "x")
        s.disable("d2", "x")
        assert s.docs_with_capability("x") == ["d1", "d2"]

    def test_enabled_true_only_enabled(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        s.enable("d1", "x")
        s.disable("d2", "x")
        assert s.docs_with_capability("x", enabled=True) == ["d1"]

    def test_enabled_false_only_explicitly_disabled(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x", default_enabled=True))
        s.enable("d1", "x")
        s.disable("d2", "x")
        assert s.docs_with_capability("x", enabled=False) == ["d2"]

    def test_enabled_true_includes_default_on_docs(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a", default_enabled=True))
        s.define_capability(Capability(name="b"))
        # d1 has explicit on 'b', so it has presence in _doc_caps
        s.enable("d1", "b")
        # d2 has explicit disable on a different cap to register in _doc_caps
        s.enable("d2", "b")
        # both should be considered enabled for 'a' via default
        assert s.docs_with_capability("a", enabled=True) == ["d1", "d2"]

    def test_unknown_cap_empty(self):
        s = DocCapabilitySet()
        assert s.docs_with_capability("nope") == []
        assert s.docs_with_capability("nope", enabled=True) == []
        assert s.docs_with_capability("nope", enabled=False) == []

    def test_sorted(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        for d in ["c", "a", "b"]:
            s.enable(d, "x")
        assert s.docs_with_capability("x") == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# all_doc_ids — sorted
# ---------------------------------------------------------------------------
class TestAllDocIds:
    def test_empty(self):
        assert DocCapabilitySet().all_doc_ids() == []

    def test_sorted(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x"))
        for d in ["c", "a", "b"]:
            s.enable(d, "x")
        assert s.all_doc_ids() == ["a", "b", "c"]

    def test_only_explicit(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="x", default_enabled=True))
        # No explicit settings → no docs
        assert s.all_doc_ids() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_counts(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a"))
        s.define_capability(Capability(name="b"))
        s.enable("d1", "a")
        s.enable("d1", "b")
        s.enable("d2", "a")
        st = s.stats()
        assert st.total_capabilities == 2
        assert st.total_docs == 2
        assert st.total_assignments == 3

    def test_after_clear(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a"))
        s.enable("d1", "a")
        s.clear_doc("d1")
        st = s.stats()
        assert st.total_docs == 0
        assert st.total_assignments == 0
        assert st.total_capabilities == 1

    def test_after_undefine(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="a"))
        s.define_capability(Capability(name="b"))
        s.enable("d1", "a")
        s.undefine_capability("a")
        st = s.stats()
        assert st.total_capabilities == 1
        assert st.total_docs == 0
        assert st.total_assignments == 0


# ---------------------------------------------------------------------------
# Thread safety — concurrent set_capability
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_set(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="cap"))
        n_threads = 16
        n_per = 50

        def worker(tid: int):
            for i in range(n_per):
                s.set_capability(f"doc-{tid}-{i}", "cap", bool(i % 2))

        threads = [
            threading.Thread(target=worker, args=(t,))
            for t in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        st = s.stats()
        assert st.total_docs == n_threads * n_per
        assert st.total_assignments == n_threads * n_per

    def test_concurrent_define_and_set(self):
        s = DocCapabilitySet()
        s.define_capability(Capability(name="cap"))

        def setter():
            for i in range(100):
                s.set_capability(f"d{i}", "cap", True)

        def lister():
            for _ in range(100):
                s.list_capabilities()
                s.stats()

        threads = [
            threading.Thread(target=setter),
            threading.Thread(target=setter),
            threading.Thread(target=lister),
            threading.Thread(target=lister),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert s.stats().total_docs == 100

    def test_concurrent_undefine_safe(self):
        s = DocCapabilitySet()
        for i in range(20):
            s.define_capability(Capability(name=f"c{i}"))
            s.enable("d1", f"c{i}")

        def undefiner(names):
            for n in names:
                s.undefine_capability(n)

        half = [f"c{i}" for i in range(0, 10)]
        rest = [f"c{i}" for i in range(10, 20)]
        threads = [
            threading.Thread(target=undefiner, args=(half,)),
            threading.Thread(target=undefiner, args=(rest,)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # All capabilities removed → all overrides cascaded → no docs left
        assert s.list_capabilities() == []
        assert s.all_doc_ids() == []


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
