"""Tests for docstoolkit.url_shortener."""
from __future__ import annotations

import os
import tempfile

import pytest

from docstoolkit.url_shortener import (
    ShortenerConfig,
    ShortenerStats,
    ShortUrl,
    UrlShortener,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def shortener() -> UrlShortener:
    s = UrlShortener()
    yield s
    s.close()


@pytest.fixture
def tmp_db_path() -> str:
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    try:
        os.remove(path)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

class TestShortUrl:
    def test_minimal_construction(self):
        s = ShortUrl(short_code="abc", original_url="http://x", created_at=1.0)
        assert s.short_code == "abc"
        assert s.original_url == "http://x"
        assert s.created_at == 1.0
        assert s.click_count == 0
        assert s.expires_at is None

    def test_full_construction(self):
        s = ShortUrl(
            short_code="abc",
            original_url="http://x",
            created_at=1.0,
            click_count=5,
            expires_at=100.0,
        )
        assert s.click_count == 5
        assert s.expires_at == 100.0

    def test_equality(self):
        a = ShortUrl("a", "u", 1.0)
        b = ShortUrl("a", "u", 1.0)
        assert a == b


class TestShortenerStats:
    def test_default_values(self):
        s = ShortenerStats(total_urls=0, total_clicks=0)
        assert s.most_clicked == []
        assert s.oldest_at is None

    def test_with_data(self):
        s = ShortenerStats(
            total_urls=3,
            total_clicks=7,
            most_clicked=[("a", 5), ("b", 2)],
            oldest_at=0.0,
        )
        assert s.total_urls == 3
        assert s.total_clicks == 7
        assert s.most_clicked == [("a", 5), ("b", 2)]
        assert s.oldest_at == 0.0


class TestShortenerConfig:
    def test_defaults(self):
        c = ShortenerConfig()
        assert c.code_length == 7
        assert c.db_path == ":memory:"
        assert len(c.alphabet) == 62

    def test_custom_values(self):
        c = ShortenerConfig(code_length=10, db_path="/tmp/x.db", alphabet="ab")
        assert c.code_length == 10
        assert c.db_path == "/tmp/x.db"
        assert c.alphabet == "ab"

    def test_invalid_code_length(self):
        with pytest.raises(ValueError):
            UrlShortener(ShortenerConfig(code_length=0))

    def test_invalid_alphabet(self):
        with pytest.raises(ValueError):
            UrlShortener(ShortenerConfig(alphabet=""))


# ---------------------------------------------------------------------------
# Shorten basic
# ---------------------------------------------------------------------------

class TestShortenBasic:
    def test_returns_short_url(self, shortener: UrlShortener):
        result = shortener.shorten("http://example.com", now=1.0)
        assert isinstance(result, ShortUrl)
        assert result.original_url == "http://example.com"
        assert result.created_at == 1.0
        assert result.click_count == 0
        assert result.expires_at is None

    def test_short_code_length(self, shortener: UrlShortener):
        r = shortener.shorten("http://example.com", now=1.0)
        assert len(r.short_code) == 7

    def test_short_code_uses_alphabet(self, shortener: UrlShortener):
        alphabet = set(ShortenerConfig().alphabet)
        r = shortener.shorten("http://example.com", now=1.0)
        for ch in r.short_code:
            assert ch in alphabet

    def test_increments_count(self, shortener: UrlShortener):
        assert shortener.count == 0
        shortener.shorten("http://a", now=1.0)
        assert shortener.count == 1
        shortener.shorten("http://b", now=2.0)
        assert shortener.count == 2

    def test_same_url_different_codes(self, shortener: UrlShortener):
        a = shortener.shorten("http://x", now=1.0)
        b = shortener.shorten("http://x", now=2.0)
        assert a.short_code != b.short_code

    def test_custom_code_length(self):
        s = UrlShortener(ShortenerConfig(code_length=12))
        r = s.shorten("http://x", now=1.0)
        assert len(r.short_code) == 12
        s.close()

    def test_url_none_raises(self, shortener: UrlShortener):
        with pytest.raises(ValueError):
            shortener.shorten(None, now=1.0)


# ---------------------------------------------------------------------------
# Custom code
# ---------------------------------------------------------------------------

class TestShortenCustomCode:
    def test_uses_custom_code(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", custom_code="mycode", now=1.0)
        assert r.short_code == "mycode"

    def test_custom_code_persisted(self, shortener: UrlShortener):
        shortener.shorten("http://x", custom_code="abc123", now=1.0)
        assert shortener.exists("abc123")

    def test_custom_code_expandable(self, shortener: UrlShortener):
        shortener.shorten("http://x", custom_code="foo", now=1.0)
        result = shortener.expand("foo", now=2.0)
        assert result is not None
        assert result.original_url == "http://x"

    def test_empty_custom_code(self, shortener: UrlShortener):
        with pytest.raises(ValueError):
            shortener.shorten("http://x", custom_code="", now=1.0)

    def test_invalid_char_in_custom_code(self, shortener: UrlShortener):
        with pytest.raises(ValueError):
            shortener.shorten("http://x", custom_code="bad!code", now=1.0)


# ---------------------------------------------------------------------------
# Duplicate custom code
# ---------------------------------------------------------------------------

class TestShortenDuplicateCode:
    def test_duplicate_raises(self, shortener: UrlShortener):
        shortener.shorten("http://a", custom_code="dup", now=1.0)
        with pytest.raises(ValueError):
            shortener.shorten("http://b", custom_code="dup", now=2.0)

    def test_duplicate_does_not_overwrite(self, shortener: UrlShortener):
        shortener.shorten("http://a", custom_code="dup", now=1.0)
        try:
            shortener.shorten("http://b", custom_code="dup", now=2.0)
        except ValueError:
            pass
        result = shortener.expand("dup", now=3.0)
        assert result.original_url == "http://a"


# ---------------------------------------------------------------------------
# Expand
# ---------------------------------------------------------------------------

class TestExpand:
    def test_returns_stored_url(self, shortener: UrlShortener):
        r = shortener.shorten("http://example.com", now=1.0)
        ret = shortener.expand(r.short_code, now=2.0)
        assert ret is not None
        assert ret.original_url == "http://example.com"

    def test_returns_short_url_dataclass(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        ret = shortener.expand(r.short_code, now=2.0)
        assert isinstance(ret, ShortUrl)

    def test_does_not_increment_clicks(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        shortener.expand(r.short_code, now=2.0)
        shortener.expand(r.short_code, now=3.0)
        result = shortener.expand(r.short_code, now=4.0)
        assert result.click_count == 0


class TestExpandExpired:
    def test_returns_none_past_expiry(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", expires_at=10.0, now=1.0)
        assert shortener.expand(r.short_code, now=20.0) is None

    def test_returns_url_before_expiry(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", expires_at=10.0, now=1.0)
        assert shortener.expand(r.short_code, now=5.0) is not None

    def test_returns_none_at_expiry(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", expires_at=10.0, now=1.0)
        assert shortener.expand(r.short_code, now=10.0) is None

    def test_no_expiry_always_works(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        assert shortener.expand(r.short_code, now=10**9) is not None


class TestExpandMissing:
    def test_unknown_code_returns_none(self, shortener: UrlShortener):
        assert shortener.expand("nope") is None

    def test_empty_code_returns_none(self, shortener: UrlShortener):
        assert shortener.expand("") is None


# ---------------------------------------------------------------------------
# Visit
# ---------------------------------------------------------------------------

class TestVisit:
    def test_returns_original_url(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        assert shortener.visit(r.short_code, now=2.0) == "http://x"

    def test_increments_click_count(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        shortener.visit(r.short_code, now=2.0)
        result = shortener.expand(r.short_code, now=3.0)
        assert result.click_count == 1

    def test_multiple_visits(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        for i in range(5):
            shortener.visit(r.short_code, now=2.0 + i)
        assert shortener.expand(r.short_code, now=10.0).click_count == 5

    def test_unknown_returns_none(self, shortener: UrlShortener):
        assert shortener.visit("nope") is None

    def test_expired_returns_none(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", expires_at=10.0, now=1.0)
        assert shortener.visit(r.short_code, now=20.0) is None

    def test_expired_does_not_increment(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", expires_at=10.0, now=1.0)
        shortener.visit(r.short_code, now=20.0)
        # Get the row directly via list_all (no expiry check)
        all_urls = shortener.list_all()
        assert all_urls[0].click_count == 0


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------

class TestDelete:
    def test_delete_returns_true(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        assert shortener.delete(r.short_code) is True

    def test_delete_removes_url(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        shortener.delete(r.short_code)
        assert shortener.expand(r.short_code, now=2.0) is None

    def test_delete_unknown_returns_false(self, shortener: UrlShortener):
        assert shortener.delete("nope") is False

    def test_delete_decrements_count(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        assert shortener.count == 1
        shortener.delete(r.short_code)
        assert shortener.count == 0


# ---------------------------------------------------------------------------
# Exists
# ---------------------------------------------------------------------------

class TestExists:
    def test_exists_true(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        assert shortener.exists(r.short_code) is True

    def test_exists_false(self, shortener: UrlShortener):
        assert shortener.exists("nope") is False

    def test_exists_after_delete(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        shortener.delete(r.short_code)
        assert shortener.exists(r.short_code) is False


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------

class TestListAll:
    def test_empty(self, shortener: UrlShortener):
        assert shortener.list_all() == []

    def test_returns_all(self, shortener: UrlShortener):
        shortener.shorten("http://a", now=1.0)
        shortener.shorten("http://b", now=2.0)
        shortener.shorten("http://c", now=3.0)
        assert len(shortener.list_all()) == 3

    def test_order_newest_first(self, shortener: UrlShortener):
        shortener.shorten("http://a", now=1.0)
        shortener.shorten("http://b", now=2.0)
        shortener.shorten("http://c", now=3.0)
        urls = shortener.list_all()
        assert urls[0].original_url == "http://c"
        assert urls[-1].original_url == "http://a"

    def test_limit(self, shortener: UrlShortener):
        for i in range(10):
            shortener.shorten(f"http://{i}", now=float(i))
        assert len(shortener.list_all(limit=3)) == 3


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty_stats(self, shortener: UrlShortener):
        s = shortener.stats()
        assert s.total_urls == 0
        assert s.total_clicks == 0
        assert s.most_clicked == []
        assert s.oldest_at is None

    def test_total_urls(self, shortener: UrlShortener):
        shortener.shorten("http://a", now=1.0)
        shortener.shorten("http://b", now=2.0)
        assert shortener.stats().total_urls == 2

    def test_total_clicks(self, shortener: UrlShortener):
        r = shortener.shorten("http://x", now=1.0)
        shortener.visit(r.short_code, now=2.0)
        shortener.visit(r.short_code, now=3.0)
        assert shortener.stats().total_clicks == 2

    def test_most_clicked(self, shortener: UrlShortener):
        r1 = shortener.shorten("http://a", now=1.0)
        r2 = shortener.shorten("http://b", now=2.0)
        for _ in range(3):
            shortener.visit(r1.short_code, now=5.0)
        for _ in range(7):
            shortener.visit(r2.short_code, now=5.0)
        most = shortener.stats().most_clicked
        assert most[0] == (r2.short_code, 7)
        assert most[1] == (r1.short_code, 3)

    def test_most_clicked_max_10(self, shortener: UrlShortener):
        codes = []
        for i in range(15):
            r = shortener.shorten(f"http://{i}", now=float(i))
            codes.append(r.short_code)
            for _ in range(i + 1):
                shortener.visit(r.short_code, now=100.0)
        assert len(shortener.stats().most_clicked) == 10

    def test_oldest_at(self, shortener: UrlShortener):
        shortener.shorten("http://a", now=5.0)
        shortener.shorten("http://b", now=2.0)
        shortener.shorten("http://c", now=10.0)
        assert shortener.stats().oldest_at == 2.0


# ---------------------------------------------------------------------------
# Cleanup expired
# ---------------------------------------------------------------------------

class TestCleanupExpired:
    def test_no_expired(self, shortener: UrlShortener):
        shortener.shorten("http://a", now=1.0)
        assert shortener.cleanup_expired(now=100.0) == 0

    def test_removes_expired(self, shortener: UrlShortener):
        shortener.shorten("http://a", expires_at=10.0, now=1.0)
        shortener.shorten("http://b", expires_at=20.0, now=2.0)
        shortener.shorten("http://c", expires_at=30.0, now=3.0)
        removed = shortener.cleanup_expired(now=15.0)
        assert removed == 1
        assert shortener.count == 2

    def test_remove_all_expired(self, shortener: UrlShortener):
        shortener.shorten("http://a", expires_at=10.0, now=1.0)
        shortener.shorten("http://b", expires_at=20.0, now=2.0)
        removed = shortener.cleanup_expired(now=100.0)
        assert removed == 2
        assert shortener.count == 0

    def test_no_expiry_not_removed(self, shortener: UrlShortener):
        shortener.shorten("http://a", now=1.0)
        shortener.shorten("http://b", expires_at=5.0, now=1.0)
        removed = shortener.cleanup_expired(now=100.0)
        assert removed == 1
        assert shortener.count == 1


# ---------------------------------------------------------------------------
# Count property
# ---------------------------------------------------------------------------

class TestCount:
    def test_starts_at_zero(self, shortener: UrlShortener):
        assert shortener.count == 0

    def test_count_increments(self, shortener: UrlShortener):
        for i in range(5):
            shortener.shorten(f"http://{i}", now=float(i))
        assert shortener.count == 5

    def test_count_is_property(self, shortener: UrlShortener):
        # Property — should be accessed without parens
        assert isinstance(shortener.count, int)


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

class TestPersistence:
    def test_file_db_persists(self, tmp_db_path):
        s1 = UrlShortener(ShortenerConfig(db_path=tmp_db_path))
        r = s1.shorten("http://example.com", now=1.0)
        code = r.short_code
        s1.close()

        s2 = UrlShortener(ShortenerConfig(db_path=tmp_db_path))
        result = s2.expand(code, now=2.0)
        assert result is not None
        assert result.original_url == "http://example.com"
        s2.close()

    def test_clicks_persist(self, tmp_db_path):
        s1 = UrlShortener(ShortenerConfig(db_path=tmp_db_path))
        r = s1.shorten("http://x", now=1.0)
        s1.visit(r.short_code, now=2.0)
        s1.visit(r.short_code, now=3.0)
        s1.close()

        s2 = UrlShortener(ShortenerConfig(db_path=tmp_db_path))
        result = s2.expand(r.short_code, now=10.0)
        assert result.click_count == 2
        s2.close()

    def test_count_persists(self, tmp_db_path):
        s1 = UrlShortener(ShortenerConfig(db_path=tmp_db_path))
        for i in range(3):
            s1.shorten(f"http://{i}", now=float(i))
        s1.close()

        s2 = UrlShortener(ShortenerConfig(db_path=tmp_db_path))
        assert s2.count == 3
        s2.close()


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_url(self, shortener: UrlShortener):
        r = shortener.shorten("", now=1.0)
        assert r.original_url == ""
        assert shortener.expand(r.short_code, now=2.0).original_url == ""

    def test_very_long_url(self, shortener: UrlShortener):
        long_url = "http://example.com/" + "a" * 10000
        r = shortener.shorten(long_url, now=1.0)
        assert shortener.expand(r.short_code, now=2.0).original_url == long_url

    def test_special_chars_url(self, shortener: UrlShortener):
        url = "http://example.com/?q=hello world&foo=bar#frag"
        r = shortener.shorten(url, now=1.0)
        assert shortener.expand(r.short_code, now=2.0).original_url == url

    def test_unicode_url(self, shortener: UrlShortener):
        url = "http://пример.рф/путь?q=значение"
        r = shortener.shorten(url, now=1.0)
        assert shortener.expand(r.short_code, now=2.0).original_url == url

    def test_short_alphabet(self):
        s = UrlShortener(ShortenerConfig(alphabet="01", code_length=5))
        r = s.shorten("http://x", now=1.0)
        assert len(r.short_code) == 5
        for ch in r.short_code:
            assert ch in "01"
        s.close()

    def test_close_idempotent(self):
        s = UrlShortener()
        s.close()
        # closing again should raise or be silent depending on sqlite version;
        # we accept either, but no segfault
        try:
            s.close()
        except Exception:
            pass
