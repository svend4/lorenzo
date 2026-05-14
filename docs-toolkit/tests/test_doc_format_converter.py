"""Tests for E373 DocFormatConverter."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_format_converter import (
    ConversionPath,
    ConversionResult,
    ConverterStats,
    DocFormatConverter,
)


# --------------------------------------------------------------- dataclasses


class TestConversionPathDataclass:
    def test_minimum_fields(self):
        p = ConversionPath(from_format="md", to_format="html")
        assert p.from_format == "md"
        assert p.to_format == "html"
        assert p.converter is None
        assert p.description == ""

    def test_all_fields(self):
        fn = lambda s: s.upper()
        p = ConversionPath(
            from_format="md",
            to_format="html",
            converter=fn,
            description="Markdown to HTML",
        )
        assert p.converter is fn
        assert p.description == "Markdown to HTML"

    def test_callable_attached(self):
        p = ConversionPath(
            from_format="a", to_format="b", converter=lambda s: s + "!"
        )
        assert p.converter("hello") == "hello!"


class TestConversionResultDataclass:
    def test_default_success_result(self):
        r = ConversionResult(from_format="md", to_format="html")
        assert r.from_format == "md"
        assert r.to_format == "html"
        assert r.content == ""
        assert r.success is True
        assert r.error == ""
        assert r.chain == []

    def test_with_chain(self):
        r = ConversionResult(
            from_format="md",
            to_format="pdf",
            content="bytes",
            chain=["md", "html", "pdf"],
        )
        assert r.chain == ["md", "html", "pdf"]
        assert r.content == "bytes"

    def test_failure_result(self):
        r = ConversionResult(
            from_format="md",
            to_format="exe",
            success=False,
            error="no path",
        )
        assert r.success is False
        assert r.error == "no path"

    def test_chain_default_is_independent(self):
        r1 = ConversionResult(from_format="a", to_format="b")
        r2 = ConversionResult(from_format="a", to_format="b")
        r1.chain.append("x")
        assert r2.chain == []


class TestConverterStatsDataclass:
    def test_fields(self):
        s = ConverterStats(
            total_paths=3,
            total_conversions=10,
            success_count=8,
            failure_count=2,
        )
        assert s.total_paths == 3
        assert s.total_conversions == 10
        assert s.success_count == 8
        assert s.failure_count == 2


# ------------------------------------------------------------------- main


class TestConstruction:
    def test_empty(self):
        c = DocFormatConverter()
        assert c.list_paths() == []
        st = c.stats()
        assert st.total_paths == 0
        assert st.total_conversions == 0
        assert st.success_count == 0
        assert st.failure_count == 0

    def test_independent_instances(self):
        a = DocFormatConverter()
        b = DocFormatConverter()
        a.register_path(ConversionPath(from_format="md", to_format="html"))
        assert len(b.list_paths()) == 0


class TestRegisterPath:
    def test_register_new(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        assert c.stats().total_paths == 1

    def test_register_multiple(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        c.register_path(ConversionPath(from_format="html", to_format="pdf"))
        assert c.stats().total_paths == 2

    def test_replace_existing(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(from_format="md", to_format="html", description="v1")
        )
        c.register_path(
            ConversionPath(from_format="md", to_format="html", description="v2")
        )
        assert c.stats().total_paths == 1
        p = c.get_path("md", "html")
        assert p is not None
        assert p.description == "v2"


class TestUnregisterPath:
    def test_unregister_existing(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        assert c.unregister_path("md", "html") is True
        assert c.stats().total_paths == 0

    def test_unregister_missing(self):
        c = DocFormatConverter()
        assert c.unregister_path("md", "html") is False

    def test_unregister_one_keeps_other(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        c.register_path(ConversionPath(from_format="html", to_format="pdf"))
        assert c.unregister_path("md", "html") is True
        assert c.get_path("html", "pdf") is not None


class TestGetPath:
    def test_get_found(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(
                from_format="md", to_format="html", description="markdown"
            )
        )
        p = c.get_path("md", "html")
        assert p is not None
        assert p.description == "markdown"

    def test_get_missing(self):
        c = DocFormatConverter()
        assert c.get_path("md", "html") is None

    def test_get_wrong_direction(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        assert c.get_path("html", "md") is None


class TestListPaths:
    def test_empty(self):
        assert DocFormatConverter().list_paths() == []

    def test_sorted(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="z", to_format="a"))
        c.register_path(ConversionPath(from_format="a", to_format="z"))
        c.register_path(ConversionPath(from_format="a", to_format="b"))
        keys = [(p.from_format, p.to_format) for p in c.list_paths()]
        assert keys == [("a", "b"), ("a", "z"), ("z", "a")]

    def test_returns_path_objects(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        items = c.list_paths()
        assert len(items) == 1
        assert isinstance(items[0], ConversionPath)


class TestConvert:
    def test_convert_success_direct(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(
                from_format="md",
                to_format="html",
                converter=lambda s: f"<p>{s}</p>",
            )
        )
        r = c.convert("hi", "md", "html")
        assert r.success is True
        assert r.content == "<p>hi</p>"
        assert r.chain == ["md", "html"]
        assert r.error == ""

    def test_convert_no_path(self):
        c = DocFormatConverter()
        r = c.convert("x", "md", "pdf")
        assert r.success is False
        assert r.content == ""
        assert "no conversion path" in r.error
        assert r.chain == []

    def test_convert_identity_when_same_format(self):
        c = DocFormatConverter()
        r = c.convert("hello", "md", "md")
        assert r.success is True
        assert r.content == "hello"
        assert r.chain == ["md"]

    def test_convert_passthrough_when_no_callable(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        r = c.convert("raw", "md", "html")
        assert r.success is True
        assert r.content == "raw"

    def test_convert_handles_converter_exception(self):
        def boom(_s):
            raise ValueError("boom")

        c = DocFormatConverter()
        c.register_path(
            ConversionPath(from_format="md", to_format="html", converter=boom)
        )
        r = c.convert("x", "md", "html")
        assert r.success is False
        assert "boom" in r.error
        assert r.content == ""

    def test_convert_increments_counters_success(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(
                from_format="md", to_format="html", converter=lambda s: s
            )
        )
        c.convert("x", "md", "html")
        st = c.stats()
        assert st.total_conversions == 1
        assert st.success_count == 1
        assert st.failure_count == 0

    def test_convert_increments_counters_failure(self):
        c = DocFormatConverter()
        c.convert("x", "md", "pdf")
        st = c.stats()
        assert st.total_conversions == 1
        assert st.success_count == 0
        assert st.failure_count == 1


class TestConvertChain:
    def test_two_hop(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(
                from_format="md",
                to_format="html",
                converter=lambda s: s + "[html]",
            )
        )
        c.register_path(
            ConversionPath(
                from_format="html",
                to_format="pdf",
                converter=lambda s: s + "[pdf]",
            )
        )
        r = c.convert("hi", "md", "pdf")
        assert r.success is True
        assert r.content == "hi[html][pdf]"
        assert r.chain == ["md", "html", "pdf"]

    def test_three_hop(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(from_format="a", to_format="b", converter=lambda s: s + "B")
        )
        c.register_path(
            ConversionPath(from_format="b", to_format="c", converter=lambda s: s + "C")
        )
        c.register_path(
            ConversionPath(from_format="c", to_format="d", converter=lambda s: s + "D")
        )
        r = c.convert("X", "a", "d")
        assert r.success is True
        assert r.content == "XBCD"
        assert r.chain == ["a", "b", "c", "d"]

    def test_chain_prefers_direct(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(from_format="a", to_format="b", converter=lambda s: s + "B")
        )
        c.register_path(
            ConversionPath(from_format="b", to_format="c", converter=lambda s: s + "C")
        )
        c.register_path(
            ConversionPath(from_format="a", to_format="c", converter=lambda s: s + "AC")
        )
        r = c.convert("X", "a", "c")
        assert r.success is True
        # Direct path used.
        assert r.chain == ["a", "c"]
        assert r.content == "XAC"

    def test_chain_exceeds_hop_limit(self):
        c = DocFormatConverter()
        # Build a 6-hop chain: f0 -> f1 -> ... -> f6 (6 hops > 5 max).
        for i in range(6):
            c.register_path(
                ConversionPath(
                    from_format=f"f{i}",
                    to_format=f"f{i + 1}",
                    converter=lambda s: s,
                )
            )
        r = c.convert("X", "f0", "f6")
        assert r.success is False
        assert r.chain == []

    def test_chain_within_hop_limit(self):
        c = DocFormatConverter()
        # 5-hop chain.
        for i in range(5):
            c.register_path(
                ConversionPath(
                    from_format=f"f{i}",
                    to_format=f"f{i + 1}",
                    converter=lambda s: s + str(i),
                )
            )
        r = c.convert("X", "f0", "f5")
        assert r.success is True
        assert r.chain == ["f0", "f1", "f2", "f3", "f4", "f5"]

    def test_chain_with_passthrough_step(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(from_format="a", to_format="b")
        )  # passthrough
        c.register_path(
            ConversionPath(from_format="b", to_format="c", converter=lambda s: s + "!")
        )
        r = c.convert("hi", "a", "c")
        assert r.success is True
        assert r.content == "hi!"


class TestAvailableTargets:
    def test_empty(self):
        c = DocFormatConverter()
        assert c.available_targets("md") == []

    def test_direct_only_sorted(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="pdf"))
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        c.register_path(ConversionPath(from_format="md", to_format="txt"))
        assert c.available_targets("md") == ["html", "pdf", "txt"]

    def test_does_not_include_indirect(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        c.register_path(ConversionPath(from_format="html", to_format="pdf"))
        # pdf is reachable but not direct from md.
        assert c.available_targets("md") == ["html"]

    def test_unknown_source(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        assert c.available_targets("unknown") == []


class TestAvailableSources:
    def test_empty(self):
        c = DocFormatConverter()
        assert c.available_sources("html") == []

    def test_direct_only_sorted(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="rst", to_format="html"))
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        c.register_path(ConversionPath(from_format="txt", to_format="html"))
        assert c.available_sources("html") == ["md", "rst", "txt"]

    def test_unknown_target(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        assert c.available_sources("unknown") == []


class TestCanConvert:
    def test_direct(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        assert c.can_convert("md", "html") is True

    def test_chain(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        c.register_path(ConversionPath(from_format="html", to_format="pdf"))
        assert c.can_convert("md", "pdf") is True

    def test_unreachable(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        assert c.can_convert("md", "epub") is False

    def test_same_format(self):
        c = DocFormatConverter()
        assert c.can_convert("md", "md") is True

    def test_chain_exceeds_limit(self):
        c = DocFormatConverter()
        for i in range(6):
            c.register_path(
                ConversionPath(from_format=f"f{i}", to_format=f"f{i + 1}")
            )
        assert c.can_convert("f0", "f6") is False


class TestFindChain:
    def test_direct(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        assert c.find_chain("md", "html") == ["md", "html"]

    def test_shortest_chain(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="a", to_format="b"))
        c.register_path(ConversionPath(from_format="b", to_format="c"))
        c.register_path(ConversionPath(from_format="c", to_format="d"))
        c.register_path(ConversionPath(from_format="a", to_format="d"))
        chain = c.find_chain("a", "d")
        assert chain == ["a", "d"]

    def test_no_chain(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        assert c.find_chain("md", "epub") is None

    def test_same_format(self):
        c = DocFormatConverter()
        assert c.find_chain("md", "md") == ["md"]

    def test_two_hop_chain(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        c.register_path(ConversionPath(from_format="html", to_format="pdf"))
        assert c.find_chain("md", "pdf") == ["md", "html", "pdf"]

    def test_chain_with_branches_picks_shortest(self):
        c = DocFormatConverter()
        # Long way: a -> b -> c -> d
        c.register_path(ConversionPath(from_format="a", to_format="b"))
        c.register_path(ConversionPath(from_format="b", to_format="c"))
        c.register_path(ConversionPath(from_format="c", to_format="d"))
        # Shorter way: a -> x -> d
        c.register_path(ConversionPath(from_format="a", to_format="x"))
        c.register_path(ConversionPath(from_format="x", to_format="d"))
        chain = c.find_chain("a", "d")
        assert chain is not None
        assert len(chain) == 3
        assert chain[0] == "a"
        assert chain[-1] == "d"


class TestClear:
    def test_clear_empty(self):
        assert DocFormatConverter().clear() == 0

    def test_clear_with_paths(self):
        c = DocFormatConverter()
        c.register_path(ConversionPath(from_format="md", to_format="html"))
        c.register_path(ConversionPath(from_format="html", to_format="pdf"))
        assert c.clear() == 2
        assert c.list_paths() == []

    def test_clear_does_not_reset_counters(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(
                from_format="md", to_format="html", converter=lambda s: s
            )
        )
        c.convert("x", "md", "html")
        c.clear()
        st = c.stats()
        assert st.total_conversions == 1
        assert st.success_count == 1


class TestStats:
    def test_initial(self):
        st = DocFormatConverter().stats()
        assert st.total_paths == 0
        assert st.total_conversions == 0
        assert st.success_count == 0
        assert st.failure_count == 0

    def test_after_mixed_operations(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(
                from_format="md", to_format="html", converter=lambda s: s
            )
        )
        c.register_path(
            ConversionPath(
                from_format="html", to_format="pdf", converter=lambda s: s
            )
        )
        c.convert("x", "md", "html")  # success
        c.convert("x", "md", "pdf")  # success (chain)
        c.convert("x", "md", "epub")  # failure
        st = c.stats()
        assert st.total_paths == 2
        assert st.total_conversions == 3
        assert st.success_count == 2
        assert st.failure_count == 1

    def test_returns_stats_object(self):
        st = DocFormatConverter().stats()
        assert isinstance(st, ConverterStats)


# --------------------------------------------------------------- thread safety


class TestThreadSafety:
    def test_concurrent_register(self):
        c = DocFormatConverter()

        def worker(start: int) -> None:
            for i in range(50):
                c.register_path(
                    ConversionPath(
                        from_format=f"f{start}_{i}", to_format="out"
                    )
                )

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert c.stats().total_paths == 8 * 50

    def test_concurrent_convert(self):
        c = DocFormatConverter()
        c.register_path(
            ConversionPath(
                from_format="md", to_format="html", converter=lambda s: s
            )
        )

        def worker() -> None:
            for _ in range(20):
                c.convert("x", "md", "html")

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        st = c.stats()
        assert st.total_conversions == 8 * 20
        assert st.success_count == 8 * 20

    def test_concurrent_register_and_unregister(self):
        c = DocFormatConverter()

        def reg() -> None:
            for i in range(50):
                c.register_path(
                    ConversionPath(from_format=f"a{i}", to_format=f"b{i}")
                )

        def unreg() -> None:
            for i in range(50):
                c.unregister_path(f"a{i}", f"b{i}")

        t1 = threading.Thread(target=reg)
        t2 = threading.Thread(target=unreg)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # No crash, internal state consistent.
        assert isinstance(c.stats(), ConverterStats)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
