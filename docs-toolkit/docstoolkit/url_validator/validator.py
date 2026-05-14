"""URL validation and analysis (stdlib only — no HTTP requests)."""
from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from urllib.parse import parse_qs, urlparse, urlunparse, urlencode


class UrlScheme(Enum):
    HTTP = "http"
    HTTPS = "https"
    FTP = "ftp"
    MAILTO = "mailto"
    FILE = "file"
    SSH = "ssh"
    OTHER = "other"

    @classmethod
    def from_string(cls, scheme: str) -> "UrlScheme":
        scheme = (scheme or "").lower()
        for s in cls:
            if s.value == scheme:
                return s
        return cls.OTHER


class ValidationCheck(Enum):
    SCHEME = "scheme"
    HOST = "host"
    TLD = "tld"
    FORMAT = "format"
    RESERVED = "reserved"


@dataclass
class ValidationError:
    check: ValidationCheck
    message: str


@dataclass
class UrlInfo:
    url: str
    scheme: UrlScheme
    host: str
    port: Optional[int]
    path: str
    query: dict = field(default_factory=dict)
    fragment: str = ""
    is_valid: bool = False
    is_secure: bool = False
    tld: str = ""

    @property
    def is_ip(self) -> bool:
        if not self.host:
            return False
        host = self.host.strip("[]")  # IPv6 brackets
        try:
            ipaddress.ip_address(host)
            return True
        except ValueError:
            return False


_ALLOWED_SCHEMES = {"http", "https", "ftp", "mailto", "file", "ssh"}
_SECURE_SCHEMES = {"https", "sftp", "ssh"}
_LOCALHOST_HOSTS = {"localhost", "127.0.0.1", "::1", "0.0.0.0"}

_URL_EXTRACT_RE = re.compile(
    r'https?://[^\s<>"\'\)\]]+|ftp://[^\s<>"\']+|mailto:[^\s<>"\'\)\]]+'
)


class UrlValidator:
    """Parse, validate, and analyze URLs."""

    def parse(self, url: str) -> UrlInfo:
        """Parse URL into a UrlInfo struct."""
        if url is None:
            url = ""
        try:
            parsed = urlparse(url)
        except Exception:
            return UrlInfo(
                url=url,
                scheme=UrlScheme.OTHER,
                host="",
                port=None,
                path="",
                query={},
                fragment="",
                is_valid=False,
                is_secure=False,
                tld="",
            )

        scheme_str = (parsed.scheme or "").lower()
        scheme = UrlScheme.from_string(scheme_str)

        # Host extraction — hostname strips port and userinfo
        host = ""
        port: Optional[int] = None
        try:
            host = parsed.hostname or ""
            port = parsed.port
        except (ValueError, TypeError):
            host = ""
            port = None

        # mailto: hosts live in the path
        if scheme == UrlScheme.MAILTO:
            host = ""

        path = parsed.path or ""
        fragment = parsed.fragment or ""

        # Parse query into dict
        query: dict = {}
        if parsed.query:
            query = parse_qs(parsed.query, keep_blank_values=True)

        # TLD
        tld = ""
        if host and "." in host:
            tld = host.rsplit(".", 1)[-1]

        is_secure = scheme_str in _SECURE_SCHEMES

        info = UrlInfo(
            url=url,
            scheme=scheme,
            host=host,
            port=port,
            path=path,
            query=query,
            fragment=fragment,
            is_valid=False,
            is_secure=is_secure,
            tld=tld,
        )
        info.is_valid = self.is_valid(url)
        return info

    def validate(self, url: str) -> tuple:
        """Validate URL; return (is_valid, [errors])."""
        errors: list = []

        if url is None or not isinstance(url, str) or not url.strip():
            errors.append(ValidationError(ValidationCheck.FORMAT, "empty URL"))
            return False, errors

        # No whitespace allowed inside URL
        if any(c.isspace() for c in url):
            errors.append(
                ValidationError(ValidationCheck.FORMAT, "URL contains whitespace")
            )

        try:
            parsed = urlparse(url)
        except Exception as exc:
            errors.append(
                ValidationError(ValidationCheck.FORMAT, f"parse error: {exc}")
            )
            return False, errors

        scheme_str = (parsed.scheme or "").lower()
        if scheme_str not in _ALLOWED_SCHEMES:
            errors.append(
                ValidationError(
                    ValidationCheck.SCHEME,
                    f"scheme '{scheme_str}' not in allowed set",
                )
            )

        # Host check
        try:
            host = parsed.hostname or ""
        except (ValueError, TypeError):
            host = ""

        if scheme_str == "mailto":
            # mailto uses path; ensure path looks like an email
            mail_target = parsed.path or ""
            if "@" not in mail_target or not mail_target.split("@", 1)[0]:
                errors.append(
                    ValidationError(
                        ValidationCheck.HOST, "mailto missing/invalid address"
                    )
                )
        elif scheme_str == "file":
            # file: host may be empty (file:///path)
            pass
        else:
            if not host:
                errors.append(ValidationError(ValidationCheck.HOST, "empty host"))

        # TLD check — host must contain '.' unless it's an IP or localhost
        if host and scheme_str not in ("mailto", "file"):
            if host not in _LOCALHOST_HOSTS:
                is_ip = False
                try:
                    ipaddress.ip_address(host.strip("[]"))
                    is_ip = True
                except ValueError:
                    is_ip = False
                if not is_ip and "." not in host:
                    errors.append(
                        ValidationError(
                            ValidationCheck.TLD, f"host '{host}' has no TLD"
                        )
                    )

        # Reserved/traversal in path
        path = parsed.path or ""
        if ".." in path.split("/"):
            errors.append(
                ValidationError(
                    ValidationCheck.RESERVED, "path contains '..' traversal"
                )
            )

        return (len(errors) == 0), errors

    def is_valid(self, url: str) -> bool:
        ok, _ = self.validate(url)
        return ok

    def normalize(self, url: str) -> str:
        """Normalize URL: lowercase scheme/host, sort query params, strip trailing slash on root."""
        if not url:
            return url
        try:
            parsed = urlparse(url)
        except Exception:
            return url

        scheme = (parsed.scheme or "").lower()

        # Lowercase host portion of netloc but preserve userinfo/port
        netloc = parsed.netloc
        if netloc:
            userinfo = ""
            hostport = netloc
            if "@" in netloc:
                userinfo, hostport = netloc.split("@", 1)
                userinfo = userinfo + "@"
            # Split port off
            port_part = ""
            if hostport.startswith("["):
                # IPv6 — split after closing ]
                if "]" in hostport:
                    end = hostport.index("]")
                    host_only = hostport[: end + 1]
                    rest = hostport[end + 1 :]
                    if rest.startswith(":"):
                        port_part = rest
                    hostport = host_only + port_part
                hostport_lower = hostport.lower()
            else:
                if ":" in hostport:
                    h, p = hostport.rsplit(":", 1)
                    hostport_lower = h.lower() + ":" + p
                else:
                    hostport_lower = hostport.lower()
            netloc = userinfo + hostport_lower

        path = parsed.path or ""
        # Strip trailing slash from root (i.e. when path is exactly "/")
        if path == "/":
            path = ""

        # Sort query params alphabetically
        query = parsed.query
        if query:
            parsed_q = parse_qs(query, keep_blank_values=True)
            pairs = []
            for key in sorted(parsed_q.keys()):
                for value in parsed_q[key]:
                    pairs.append((key, value))
            query = urlencode(pairs)

        return urlunparse(
            (scheme, netloc, path, parsed.params, query, parsed.fragment)
        )

    def extract_urls(self, text: str) -> list:
        """Find URLs in text."""
        if not text:
            return []
        results = []
        for match in _URL_EXTRACT_RE.finditer(text):
            url = match.group(0)
            # Trim trailing punctuation that's commonly not part of URLs
            url = url.rstrip(".,;:!?")
            results.append(url)
        return results

    def domain_of(self, url: str) -> str:
        """Return host without subdomain prefix.

        Returns last two labels for typical 'sub.example.com' -> 'example.com'.
        For IPs or single-label hosts, returns the host as-is.
        """
        info = self.parse(url)
        host = info.host
        if not host:
            return ""
        if info.is_ip:
            return host
        labels = host.split(".")
        if len(labels) <= 2:
            return host
        return ".".join(labels[-2:])

    def same_domain(self, url1: str, url2: str) -> bool:
        """True if two URLs share the same registrable domain (last 2 labels)."""
        d1 = self.domain_of(url1)
        d2 = self.domain_of(url2)
        if not d1 or not d2:
            return False
        return d1.lower() == d2.lower()

    def is_localhost(self, url: str) -> bool:
        """True if URL points at localhost."""
        info = self.parse(url)
        host = (info.host or "").lower()
        return host in _LOCALHOST_HOSTS
