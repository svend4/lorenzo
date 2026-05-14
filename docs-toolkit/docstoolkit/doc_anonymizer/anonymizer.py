"""Document PII anonymizer implementation.

Pattern-based detection and masking of personally identifiable information in
unstructured document text. Stdlib only (``re``, ``hashlib``).
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class PiiType(Enum):
    """Supported PII categories."""

    EMAIL = "email"
    PHONE = "phone"
    SSN = "ssn"
    IP_ADDRESS = "ip_address"
    CREDIT_CARD = "credit_card"
    URL = "url"
    DATE = "date"
    IBAN = "iban"
    FULL_NAME = "full_name"
    CUSTOM = "custom"


class MaskingMode(Enum):
    """Available masking strategies."""

    REDACT = "redact"
    PARTIAL = "partial"
    HASH = "hash"
    FAKE = "fake"
    TOKENIZE = "tokenize"


@dataclass
class PiiMatch:
    """A single detected PII span and its replacement."""

    pii_type: PiiType
    original: str
    replacement: str
    start: int
    end: int


@dataclass
class AnonymizeResult:
    """Outcome of anonymizing one text."""

    original: str
    anonymized: str
    matches: List[PiiMatch] = field(default_factory=list)
    mapping: Dict[str, str] = field(default_factory=dict)

    @property
    def match_count(self) -> int:
        return len(self.matches)

    @property
    def types_found(self) -> Set[PiiType]:
        return {m.pii_type for m in self.matches}


@dataclass
class AnonymizerConfig:
    """Configuration for :class:`DocAnonymizer`."""

    enabled_types: Set[PiiType] = field(
        default_factory=lambda: {
            PiiType.EMAIL,
            PiiType.PHONE,
            PiiType.SSN,
            PiiType.IP_ADDRESS,
            PiiType.CREDIT_CARD,
            PiiType.URL,
        }
    )
    mode: MaskingMode = MaskingMode.REDACT
    redact_template: str = "[REDACTED]"
    partial_keep: int = 4
    custom_patterns: List[Tuple[str, str]] = field(default_factory=list)
    salt: str = ""


# Compiled regular expressions for PII detection.
_EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE_RE = re.compile(
    r"\+?\d{1,3}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{3,4}[\s\-]?\d{3,4}"
)
_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_IP_RE = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")
_CC_RE = re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b")
_URL_RE = re.compile(r"https?://\S+")


def _matches(pattern: re.Pattern, text: str) -> List[Tuple[str, int, int]]:
    return [(m.group(0), m.start(), m.end()) for m in pattern.finditer(text)]


class DocAnonymizer:
    """Detect and anonymize PII in document text."""

    def __init__(self, config: Optional[AnonymizerConfig] = None) -> None:
        self.config = config if config is not None else AnonymizerConfig()
        self._total_anonymized = 0
        self._token_counter = 0

    # ------------------------------------------------------------------
    # Detection helpers
    # ------------------------------------------------------------------
    def detect_emails(self, text: str) -> List[Tuple[str, int, int]]:
        return _matches(_EMAIL_RE, text)

    def detect_phones(self, text: str) -> List[Tuple[str, int, int]]:
        return _matches(_PHONE_RE, text)

    def detect_ssns(self, text: str) -> List[Tuple[str, int, int]]:
        return _matches(_SSN_RE, text)

    def detect_ips(self, text: str) -> List[Tuple[str, int, int]]:
        return _matches(_IP_RE, text)

    def detect_credit_cards(self, text: str) -> List[Tuple[str, int, int]]:
        return _matches(_CC_RE, text)

    def detect_urls(self, text: str) -> List[Tuple[str, int, int]]:
        return _matches(_URL_RE, text)

    def detect_custom(
        self, text: str, pattern: str
    ) -> List[Tuple[str, int, int]]:
        compiled = re.compile(pattern)
        return _matches(compiled, text)

    # ------------------------------------------------------------------
    # Combined detection
    # ------------------------------------------------------------------
    def find_pii(self, text: str) -> List[PiiMatch]:
        """Return all matches for enabled PII types in *text*.

        Overlapping spans are resolved greedily: the earliest match wins, and
        if two start at the same offset the longer one is kept.
        """
        raw: List[Tuple[int, int, PiiType, str]] = []
        enabled = self.config.enabled_types

        detectors: List[Tuple[PiiType, callable]] = [
            (PiiType.URL, self.detect_urls),  # before EMAIL/IP to win ties
            (PiiType.EMAIL, self.detect_emails),
            (PiiType.SSN, self.detect_ssns),
            (PiiType.CREDIT_CARD, self.detect_credit_cards),
            (PiiType.IP_ADDRESS, self.detect_ips),
            (PiiType.PHONE, self.detect_phones),
        ]
        for pii_type, fn in detectors:
            if pii_type in enabled:
                for value, start, end in fn(text):
                    raw.append((start, end, pii_type, value))

        # Custom patterns
        if PiiType.CUSTOM in enabled or self.config.custom_patterns:
            for pattern, _label in self.config.custom_patterns:
                for value, start, end in self.detect_custom(text, pattern):
                    raw.append((start, end, PiiType.CUSTOM, value))

        # Sort by (start asc, length desc) and drop overlaps.
        raw.sort(key=lambda t: (t[0], -(t[1] - t[0])))
        chosen: List[Tuple[int, int, PiiType, str]] = []
        last_end = -1
        for start, end, pii_type, value in raw:
            if start < last_end:
                continue
            chosen.append((start, end, pii_type, value))
            last_end = end

        results: List[PiiMatch] = []
        for start, end, pii_type, value in chosen:
            replacement = self.mask_value(value, pii_type)
            results.append(
                PiiMatch(
                    pii_type=pii_type,
                    original=value,
                    replacement=replacement,
                    start=start,
                    end=end,
                )
            )
        return results

    # ------------------------------------------------------------------
    # Masking
    # ------------------------------------------------------------------
    def mask_value(
        self,
        value: str,
        pii_type: PiiType,
        mode: Optional[MaskingMode] = None,
    ) -> str:
        active = mode if mode is not None else self.config.mode
        if active is MaskingMode.REDACT:
            return self.config.redact_template
        if active is MaskingMode.PARTIAL:
            keep = max(0, self.config.partial_keep)
            if keep >= len(value):
                return value
            hidden_len = len(value) - keep
            return ("*" * hidden_len) + value[-keep:] if keep else "*" * len(value)
        if active is MaskingMode.HASH:
            digest = hashlib.sha256(
                (value + self.config.salt).encode("utf-8")
            ).hexdigest()
            return digest[:8]
        if active is MaskingMode.FAKE:
            return _fake_for(pii_type)
        if active is MaskingMode.TOKENIZE:
            self._token_counter += 1
            return f"<PII_{self._token_counter}>"
        raise ValueError(f"Unknown masking mode: {active!r}")

    # ------------------------------------------------------------------
    # Anonymization
    # ------------------------------------------------------------------
    def anonymize(self, text: str) -> AnonymizeResult:
        # Reset tokens per-call so token IDs are stable per input.
        self._token_counter = 0
        matches = self.find_pii(text)

        out_parts: List[str] = []
        cursor = 0
        mapping: Dict[str, str] = {}
        for m in matches:
            out_parts.append(text[cursor:m.start])
            out_parts.append(m.replacement)
            cursor = m.end
            if self.config.mode is MaskingMode.TOKENIZE:
                mapping[m.replacement] = m.original
        out_parts.append(text[cursor:])

        anonymized = "".join(out_parts)
        self._total_anonymized += len(matches)
        return AnonymizeResult(
            original=text,
            anonymized=anonymized,
            matches=matches,
            mapping=mapping,
        )

    def restore(self, anonymized: str, mapping: Dict[str, str]) -> str:
        """Reverse a TOKENIZE result using its mapping."""
        # Replace longer tokens first to avoid partial collisions
        out = anonymized
        for token in sorted(mapping.keys(), key=len, reverse=True):
            out = out.replace(token, mapping[token])
        return out

    def anonymize_batch(self, texts: List[str]) -> List[AnonymizeResult]:
        return [self.anonymize(t) for t in texts]

    @property
    def total_anonymized(self) -> int:
        return self._total_anonymized


def _fake_for(pii_type: PiiType) -> str:
    """Return a deterministic placeholder for ``FAKE`` mode."""
    table = {
        PiiType.EMAIL: "user@example.com",
        PiiType.PHONE: "+1-555-0100",
        PiiType.SSN: "000-00-0000",
        PiiType.IP_ADDRESS: "0.0.0.0",
        PiiType.CREDIT_CARD: "0000-0000-0000-0000",
        PiiType.URL: "https://example.com",
        PiiType.DATE: "1970-01-01",
        PiiType.IBAN: "XX00 0000 0000 0000",
        PiiType.FULL_NAME: "John Doe",
        PiiType.CUSTOM: "<FAKE>",
    }
    return table.get(pii_type, "<FAKE>")
