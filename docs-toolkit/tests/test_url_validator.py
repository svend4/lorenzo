"""Tests for url_validator module."""
import pytest

from docstoolkit.url_validator import (
    UrlValidator,
    UrlInfo,
    UrlScheme,
    ValidationCheck,
    ValidationError,
)


@pytest.fixture
def v():
    return UrlValidator()


class TestUrlScheme:
    def test_http(self):
        assert UrlScheme.from_string("http") == UrlScheme.HTTP

    def test_https(self):
        assert UrlScheme.from_string("https") == UrlScheme.HTTPS

    def test_uppercase(self):
        assert UrlScheme.from_string("HTTPS") == UrlScheme.HTTPS

    def test_unknown_scheme_becomes_other(self):
        assert UrlScheme.from_string("gopher") == UrlScheme.OTHER

    def test_empty_scheme_other(self):
        assert UrlScheme.from_string("") == UrlScheme.OTHER

    def test_mailto(self):
        assert UrlScheme.from_string("mailto") == UrlScheme.MAILTO


class TestUrlInfo:
    def test_is_ip_for_ipv4(self, v):
        info = v.parse("http://192.168.1.1/")
        assert info.is_ip is True

    def test_is_ip_false_for_hostname(self, v):
        info = v.parse("http://example.com/")
        assert info.is_ip is False

    def test_is_ip_false_for_empty_host(self, v):
        info = v.parse("mailto:foo@example.com")
        assert info.is_ip is False

    def test_is_secure_https(self, v):
        info = v.parse("https://example.com/")
        assert info.is_secure is True

    def test_is_secure_http_false(self, v):
        info = v.parse("http://example.com/")
        assert info.is_secure is False

    def test_is_secure_ssh(self, v):
        info = v.parse("ssh://example.com/")
        assert info.is_secure is True


class TestParse:
    def test_http_basic(self, v):
        info = v.parse("http://example.com/")
        assert info.scheme == UrlScheme.HTTP
        assert info.host == "example.com"
        assert info.path == "/"

    def test_https(self, v):
        info = v.parse("https://example.com/path")
        assert info.scheme == UrlScheme.HTTPS
        assert info.host == "example.com"
        assert info.path == "/path"

    def test_with_port(self, v):
        info = v.parse("http://example.com:8080/")
        assert info.host == "example.com"
        assert info.port == 8080

    def test_no_port_when_default(self, v):
        info = v.parse("http://example.com/")
        assert info.port is None

    def test_with_query(self, v):
        info = v.parse("http://example.com/?a=1&b=2")
        assert info.query == {"a": ["1"], "b": ["2"]}

    def test_query_repeated_keys(self, v):
        info = v.parse("http://example.com/?a=1&a=2")
        assert info.query == {"a": ["1", "2"]}

    def test_with_fragment(self, v):
        info = v.parse("http://example.com/page#section")
        assert info.fragment == "section"

    def test_no_fragment_default_empty(self, v):
        info = v.parse("http://example.com/")
        assert info.fragment == ""

    def test_tld_extraction(self, v):
        info = v.parse("http://www.example.com/")
        assert info.tld == "com"

    def test_url_field_preserved(self, v):
        url = "http://example.com/path?x=1"
        info = v.parse(url)
        assert info.url == url


class TestParseMailto:
    def test_mailto_scheme(self, v):
        info = v.parse("mailto:user@example.com")
        assert info.scheme == UrlScheme.MAILTO

    def test_mailto_host_empty(self, v):
        info = v.parse("mailto:user@example.com")
        assert info.host == ""

    def test_mailto_is_valid(self, v):
        assert v.is_valid("mailto:user@example.com") is True

    def test_mailto_missing_address_invalid(self, v):
        assert v.is_valid("mailto:") is False

    def test_mailto_no_at_invalid(self, v):
        assert v.is_valid("mailto:nobody") is False


class TestValidate:
    def test_valid_http(self, v):
        ok, errors = v.validate("http://example.com/")
        assert ok is True
        assert errors == []

    def test_valid_https(self, v):
        ok, _ = v.validate("https://example.com/path")
        assert ok is True

    def test_invalid_scheme(self, v):
        ok, errors = v.validate("gopher://example.com/")
        assert ok is False
        assert any(e.check == ValidationCheck.SCHEME for e in errors)

    def test_missing_host(self, v):
        ok, errors = v.validate("http:///path")
        assert ok is False
        assert any(e.check == ValidationCheck.HOST for e in errors)

    def test_missing_tld(self, v):
        ok, errors = v.validate("http://nodotted/")
        assert ok is False
        assert any(e.check == ValidationCheck.TLD for e in errors)

    def test_ip_address_passes_tld(self, v):
        ok, errors = v.validate("http://192.168.1.1/")
        assert ok is True
        assert errors == []

    def test_localhost_passes_tld(self, v):
        ok, errors = v.validate("http://localhost/")
        assert ok is True

    def test_traversal_in_path(self, v):
        ok, errors = v.validate("http://example.com/foo/../etc/passwd")
        assert ok is False
        assert any(e.check == ValidationCheck.RESERVED for e in errors)

    def test_whitespace_in_url(self, v):
        ok, errors = v.validate("http://exa mple.com/")
        assert ok is False
        assert any(e.check == ValidationCheck.FORMAT for e in errors)

    def test_empty_url(self, v):
        ok, errors = v.validate("")
        assert ok is False
        assert any(e.check == ValidationCheck.FORMAT for e in errors)


class TestIsValid:
    def test_valid(self, v):
        assert v.is_valid("https://example.com/") is True

    def test_invalid_scheme(self, v):
        assert v.is_valid("gopher://example.com/") is False

    def test_invalid_no_host(self, v):
        assert v.is_valid("http:///path") is False

    def test_empty(self, v):
        assert v.is_valid("") is False


class TestNormalize:
    def test_lowercase_scheme(self, v):
        assert v.normalize("HTTP://example.com/") == "http://example.com"

    def test_lowercase_host(self, v):
        assert v.normalize("http://EXAMPLE.COM/") == "http://example.com"

    def test_strip_trailing_root_slash(self, v):
        assert v.normalize("http://example.com/") == "http://example.com"

    def test_preserves_non_root_path(self, v):
        assert v.normalize("http://example.com/foo/").endswith("/foo/")

    def test_sort_query_params(self, v):
        result = v.normalize("http://example.com/?b=2&a=1")
        assert "a=1&b=2" in result

    def test_normalize_idempotent(self, v):
        once = v.normalize("HTTP://Example.COM/?b=2&a=1")
        twice = v.normalize(once)
        assert once == twice


class TestExtractUrls:
    def test_single_http(self, v):
        urls = v.extract_urls("see http://example.com here")
        assert "http://example.com" in urls

    def test_multiple(self, v):
        urls = v.extract_urls("a http://a.com and b https://b.org")
        assert len(urls) == 2

    def test_mailto(self, v):
        urls = v.extract_urls("contact mailto:foo@bar.com please")
        assert any(u.startswith("mailto:") for u in urls)

    def test_ftp(self, v):
        urls = v.extract_urls("download ftp://files.example.com/file")
        assert any(u.startswith("ftp://") for u in urls)

    def test_empty_text(self, v):
        assert v.extract_urls("") == []

    def test_no_urls(self, v):
        assert v.extract_urls("just plain text") == []

    def test_trims_trailing_punct(self, v):
        urls = v.extract_urls("visit http://example.com.")
        assert "http://example.com" in urls


class TestDomainOf:
    def test_strip_www(self, v):
        assert v.domain_of("http://www.example.com/") == "example.com"

    def test_strip_deep_subdomain(self, v):
        assert v.domain_of("http://a.b.example.org/") == "example.org"

    def test_already_apex(self, v):
        assert v.domain_of("http://example.com/") == "example.com"

    def test_ip_returned_as_is(self, v):
        assert v.domain_of("http://192.168.1.1/") == "192.168.1.1"

    def test_empty_for_no_host(self, v):
        assert v.domain_of("mailto:foo@example.com") == ""


class TestSameDomain:
    def test_same(self, v):
        assert v.same_domain("http://a.example.com/x", "https://b.example.com/y")

    def test_different(self, v):
        assert not v.same_domain("http://example.com/", "http://other.org/")

    def test_case_insensitive(self, v):
        assert v.same_domain("http://Example.COM/", "http://example.com/")

    def test_empty_returns_false(self, v):
        assert v.same_domain("", "http://example.com/") is False


class TestIsLocalhost:
    def test_localhost_name(self, v):
        assert v.is_localhost("http://localhost/") is True

    def test_loopback_ipv4(self, v):
        assert v.is_localhost("http://127.0.0.1/") is True

    def test_loopback_ipv6(self, v):
        assert v.is_localhost("http://[::1]/") is True

    def test_zero_address(self, v):
        assert v.is_localhost("http://0.0.0.0/") is True

    def test_not_localhost(self, v):
        assert v.is_localhost("http://example.com/") is False


class TestValidationErrors:
    def test_scheme_error_message(self, v):
        _, errors = v.validate("gopher://example.com/")
        scheme_errs = [e for e in errors if e.check == ValidationCheck.SCHEME]
        assert scheme_errs
        assert "gopher" in scheme_errs[0].message.lower() or "scheme" in scheme_errs[0].message.lower()

    def test_host_error_message(self, v):
        _, errors = v.validate("http:///path")
        host_errs = [e for e in errors if e.check == ValidationCheck.HOST]
        assert host_errs
        assert "host" in host_errs[0].message.lower()

    def test_tld_error_message(self, v):
        _, errors = v.validate("http://nodot/")
        tld_errs = [e for e in errors if e.check == ValidationCheck.TLD]
        assert tld_errs

    def test_format_error_for_whitespace(self, v):
        _, errors = v.validate("http://exa mple.com/")
        fmt_errs = [e for e in errors if e.check == ValidationCheck.FORMAT]
        assert fmt_errs

    def test_reserved_error_for_traversal(self, v):
        _, errors = v.validate("http://example.com/a/../b")
        res_errs = [e for e in errors if e.check == ValidationCheck.RESERVED]
        assert res_errs

    def test_validation_error_dataclass(self):
        err = ValidationError(ValidationCheck.SCHEME, "bad scheme")
        assert err.check == ValidationCheck.SCHEME
        assert err.message == "bad scheme"


class TestEdgeCases:
    def test_empty_string_parse(self, v):
        info = v.parse("")
        assert info.is_valid is False

    def test_only_scheme(self, v):
        info = v.parse("http://")
        assert info.is_valid is False

    def test_none_parse_handled(self, v):
        info = v.parse(None)
        assert info.is_valid is False

    def test_malformed_url(self, v):
        assert v.is_valid("not a url at all") is False

    def test_file_scheme_valid(self, v):
        # file:///tmp/x is valid
        assert v.is_valid("file:///tmp/x") is True

    def test_ssh_scheme_valid(self, v):
        assert v.is_valid("ssh://user@example.com") is True

    def test_url_with_userinfo(self, v):
        info = v.parse("http://user:pass@example.com:8080/path")
        assert info.host == "example.com"
        assert info.port == 8080
