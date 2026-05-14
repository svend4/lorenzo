"""Tests for the ``doc_anonymizer`` module."""
from __future__ import annotations

import hashlib

import pytest

from docstoolkit.doc_anonymizer import (
    AnonymizeResult,
    AnonymizerConfig,
    DocAnonymizer,
    MaskingMode,
    PiiMatch,
    PiiType,
)


# ----------------------------------------------------------------------
# Enums and dataclasses
# ----------------------------------------------------------------------
class TestPiiType:
    def test_has_email(self):
        assert PiiType.EMAIL.value == "email"

    def test_has_phone(self):
        assert PiiType.PHONE.value == "phone"

    def test_has_ssn(self):
        assert PiiType.SSN.value == "ssn"

    def test_has_ip(self):
        assert PiiType.IP_ADDRESS.value == "ip_address"

    def test_has_credit_card(self):
        assert PiiType.CREDIT_CARD.value == "credit_card"

    def test_has_url(self):
        assert PiiType.URL.value == "url"

    def test_has_date_iban_fullname_custom(self):
        assert PiiType.DATE.value == "date"
        assert PiiType.IBAN.value == "iban"
        assert PiiType.FULL_NAME.value == "full_name"
        assert PiiType.CUSTOM.value == "custom"


class TestMaskingMode:
    def test_modes_exist(self):
        for name in ("REDACT", "PARTIAL", "HASH", "FAKE", "TOKENIZE"):
            assert hasattr(MaskingMode, name)

    def test_redact_value(self):
        assert MaskingMode.REDACT.value == "redact"


class TestPiiMatch:
    def test_construct(self):
        m = PiiMatch(PiiType.EMAIL, "a@b.com", "[X]", 0, 7)
        assert m.pii_type is PiiType.EMAIL
        assert m.original == "a@b.com"
        assert m.replacement == "[X]"
        assert m.start == 0
        assert m.end == 7

    def test_fields_are_named(self):
        m = PiiMatch(pii_type=PiiType.SSN, original="x", replacement="y", start=1, end=2)
        assert m.end - m.start == 1


class TestAnonymizeResult:
    def test_match_count(self):
        ms = [
            PiiMatch(PiiType.EMAIL, "a@b.c", "[R]", 0, 5),
            PiiMatch(PiiType.SSN, "1-2-3", "[R]", 6, 11),
        ]
        r = AnonymizeResult(original="t", anonymized="t", matches=ms)
        assert r.match_count == 2

    def test_types_found(self):
        ms = [
            PiiMatch(PiiType.EMAIL, "a@b.c", "[R]", 0, 5),
            PiiMatch(PiiType.EMAIL, "x@y.z", "[R]", 6, 11),
            PiiMatch(PiiType.SSN, "1-2-3", "[R]", 12, 17),
        ]
        r = AnonymizeResult(original="t", anonymized="t", matches=ms)
        assert r.types_found == {PiiType.EMAIL, PiiType.SSN}

    def test_empty(self):
        r = AnonymizeResult(original="x", anonymized="x", matches=[])
        assert r.match_count == 0
        assert r.types_found == set()


class TestAnonymizerConfig:
    def test_defaults(self):
        cfg = AnonymizerConfig()
        assert cfg.mode is MaskingMode.REDACT
        assert cfg.redact_template == "[REDACTED]"
        assert cfg.partial_keep == 4
        assert cfg.custom_patterns == []
        assert cfg.salt == ""
        assert PiiType.EMAIL in cfg.enabled_types

    def test_override(self):
        cfg = AnonymizerConfig(
            enabled_types={PiiType.EMAIL},
            mode=MaskingMode.HASH,
            redact_template="<X>",
            partial_keep=2,
            salt="s",
        )
        assert cfg.enabled_types == {PiiType.EMAIL}
        assert cfg.mode is MaskingMode.HASH
        assert cfg.redact_template == "<X>"
        assert cfg.partial_keep == 2
        assert cfg.salt == "s"


# ----------------------------------------------------------------------
# Detection helpers
# ----------------------------------------------------------------------
class TestDetectEmails:
    def test_simple(self):
        a = DocAnonymizer()
        out = a.detect_emails("contact alice@example.com today")
        assert len(out) == 1
        val, start, end = out[0]
        assert val == "alice@example.com"
        assert start == 8 and end == 8 + len(val)

    def test_multiple(self):
        a = DocAnonymizer()
        out = a.detect_emails("a@b.com and c.d+tag@example.co.uk")
        assert len(out) == 2

    def test_none(self):
        a = DocAnonymizer()
        assert a.detect_emails("no pii here") == []


class TestDetectPhones:
    def test_us_style(self):
        a = DocAnonymizer()
        out = a.detect_phones("call +1 (415) 555-0100 please")
        assert len(out) >= 1
        assert "555" in out[0][0]

    def test_intl(self):
        a = DocAnonymizer()
        out = a.detect_phones("phone: +44 20 7946 0958")
        assert len(out) >= 1

    def test_no_match(self):
        a = DocAnonymizer()
        assert a.detect_phones("hello world") == []


class TestDetectSsns:
    def test_basic(self):
        a = DocAnonymizer()
        out = a.detect_ssns("SSN is 123-45-6789 ok")
        assert out and out[0][0] == "123-45-6789"

    def test_no_dashes(self):
        a = DocAnonymizer()
        assert a.detect_ssns("123456789") == []

    def test_multiple(self):
        a = DocAnonymizer()
        text = "111-22-3333 and 444-55-6666"
        assert len(a.detect_ssns(text)) == 2


class TestDetectIps:
    def test_basic(self):
        a = DocAnonymizer()
        out = a.detect_ips("server 192.168.1.1 down")
        assert out and out[0][0] == "192.168.1.1"

    def test_multiple(self):
        a = DocAnonymizer()
        assert len(a.detect_ips("10.0.0.1 and 8.8.8.8")) == 2

    def test_no_match(self):
        a = DocAnonymizer()
        assert a.detect_ips("plain text") == []


class TestDetectCreditCards:
    def test_with_spaces(self):
        a = DocAnonymizer()
        out = a.detect_credit_cards("card 4111 1111 1111 1111 ok")
        assert out and "4111" in out[0][0]

    def test_with_dashes(self):
        a = DocAnonymizer()
        out = a.detect_credit_cards("4111-1111-1111-1111")
        assert out

    def test_no_match(self):
        a = DocAnonymizer()
        assert a.detect_credit_cards("12345") == []


class TestDetectUrls:
    def test_http(self):
        a = DocAnonymizer()
        out = a.detect_urls("visit http://example.com today")
        assert out and out[0][0] == "http://example.com"

    def test_https(self):
        a = DocAnonymizer()
        out = a.detect_urls("https://secure.example.org/path?x=1 end")
        assert out

    def test_no_match(self):
        a = DocAnonymizer()
        assert a.detect_urls("example.com without scheme") == []


class TestDetectCustom:
    def test_pattern(self):
        a = DocAnonymizer()
        out = a.detect_custom("user-A1, user-B2", r"user-[A-Z]\d")
        assert len(out) == 2

    def test_empty(self):
        a = DocAnonymizer()
        assert a.detect_custom("nothing", r"\bZZZ\b") == []


# ----------------------------------------------------------------------
# find_pii
# ----------------------------------------------------------------------
class TestFindPii:
    def test_finds_email_and_phone(self):
        a = DocAnonymizer()
        text = "Email alice@example.com or call +1 (415) 555-0100"
        matches = a.find_pii(text)
        types = {m.pii_type for m in matches}
        assert PiiType.EMAIL in types
        assert PiiType.PHONE in types

    def test_respects_enabled_types(self):
        cfg = AnonymizerConfig(enabled_types={PiiType.EMAIL})
        a = DocAnonymizer(cfg)
        text = "alice@example.com and SSN 123-45-6789"
        matches = a.find_pii(text)
        assert all(m.pii_type is PiiType.EMAIL for m in matches)

    def test_returns_matches_sorted_by_start(self):
        a = DocAnonymizer()
        text = "SSN 111-22-3333 then email a@b.com"
        matches = a.find_pii(text)
        starts = [m.start for m in matches]
        assert starts == sorted(starts)

    def test_overlap_url_wins_over_inner_email(self):
        a = DocAnonymizer()
        text = "go to https://x.com/u@y.com end"
        matches = a.find_pii(text)
        # URL should consume the embedded email-like string
        assert any(m.pii_type is PiiType.URL for m in matches)
        assert not any(
            m.pii_type is PiiType.EMAIL and m.start >= text.index("https")
            for m in matches
        )

    def test_custom_pattern_used(self):
        cfg = AnonymizerConfig(
            enabled_types={PiiType.CUSTOM},
            custom_patterns=[(r"ORD-\d{4}", "order_id")],
        )
        a = DocAnonymizer(cfg)
        matches = a.find_pii("see ORD-1234 and ORD-5678")
        assert len(matches) == 2
        assert all(m.pii_type is PiiType.CUSTOM for m in matches)


# ----------------------------------------------------------------------
# mask_value behaviours
# ----------------------------------------------------------------------
class TestMaskValueRedact:
    def test_default_template(self):
        a = DocAnonymizer()
        assert a.mask_value("alice@x.com", PiiType.EMAIL) == "[REDACTED]"

    def test_custom_template(self):
        a = DocAnonymizer(AnonymizerConfig(redact_template="<X>"))
        assert a.mask_value("x", PiiType.SSN) == "<X>"


class TestMaskValuePartial:
    def test_keeps_last_n(self):
        cfg = AnonymizerConfig(mode=MaskingMode.PARTIAL, partial_keep=4)
        a = DocAnonymizer(cfg)
        out = a.mask_value("4111111111111111", PiiType.CREDIT_CARD)
        assert out.endswith("1111")
        assert out.startswith("*")
        assert len(out) == 16

    def test_short_value_returned_unchanged(self):
        cfg = AnonymizerConfig(mode=MaskingMode.PARTIAL, partial_keep=4)
        a = DocAnonymizer(cfg)
        assert a.mask_value("abc", PiiType.EMAIL) == "abc"

    def test_zero_keep(self):
        cfg = AnonymizerConfig(mode=MaskingMode.PARTIAL, partial_keep=0)
        a = DocAnonymizer(cfg)
        out = a.mask_value("secret", PiiType.EMAIL)
        assert out == "******"


class TestMaskValueHash:
    def test_deterministic(self):
        cfg = AnonymizerConfig(mode=MaskingMode.HASH, salt="pepper")
        a = DocAnonymizer(cfg)
        out1 = a.mask_value("alice@example.com", PiiType.EMAIL)
        out2 = a.mask_value("alice@example.com", PiiType.EMAIL)
        assert out1 == out2
        assert len(out1) == 8

    def test_uses_salt(self):
        a1 = DocAnonymizer(AnonymizerConfig(mode=MaskingMode.HASH, salt="A"))
        a2 = DocAnonymizer(AnonymizerConfig(mode=MaskingMode.HASH, salt="B"))
        assert a1.mask_value("x", PiiType.EMAIL) != a2.mask_value("x", PiiType.EMAIL)

    def test_matches_sha256_prefix(self):
        cfg = AnonymizerConfig(mode=MaskingMode.HASH, salt="s")
        a = DocAnonymizer(cfg)
        expected = hashlib.sha256(b"value" + b"s").hexdigest()[:8]
        assert a.mask_value("value", PiiType.EMAIL) == expected


class TestMaskValueFake:
    def test_email_placeholder(self):
        cfg = AnonymizerConfig(mode=MaskingMode.FAKE)
        a = DocAnonymizer(cfg)
        assert a.mask_value("alice@example.com", PiiType.EMAIL) == "user@example.com"

    def test_phone_placeholder(self):
        cfg = AnonymizerConfig(mode=MaskingMode.FAKE)
        a = DocAnonymizer(cfg)
        assert "555" in a.mask_value("+1 415 555 0100", PiiType.PHONE)

    def test_ssn_placeholder(self):
        cfg = AnonymizerConfig(mode=MaskingMode.FAKE)
        a = DocAnonymizer(cfg)
        assert a.mask_value("123-45-6789", PiiType.SSN) == "000-00-0000"

    def test_ip_placeholder(self):
        cfg = AnonymizerConfig(mode=MaskingMode.FAKE)
        a = DocAnonymizer(cfg)
        assert a.mask_value("1.2.3.4", PiiType.IP_ADDRESS) == "0.0.0.0"


class TestMaskValueTokenize:
    def test_increments(self):
        cfg = AnonymizerConfig(mode=MaskingMode.TOKENIZE)
        a = DocAnonymizer(cfg)
        t1 = a.mask_value("alice@x.com", PiiType.EMAIL)
        t2 = a.mask_value("bob@x.com", PiiType.EMAIL)
        assert t1 == "<PII_1>"
        assert t2 == "<PII_2>"

    def test_format(self):
        cfg = AnonymizerConfig(mode=MaskingMode.TOKENIZE)
        a = DocAnonymizer(cfg)
        out = a.mask_value("x", PiiType.EMAIL)
        assert out.startswith("<PII_") and out.endswith(">")


# ----------------------------------------------------------------------
# anonymize() end-to-end
# ----------------------------------------------------------------------
class TestAnonymize:
    def test_redacts_email(self):
        a = DocAnonymizer()
        r = a.anonymize("ping alice@example.com please")
        assert "alice@example.com" not in r.anonymized
        assert "[REDACTED]" in r.anonymized

    def test_returns_result_dataclass(self):
        a = DocAnonymizer()
        r = a.anonymize("alice@example.com")
        assert isinstance(r, AnonymizeResult)
        assert r.original == "alice@example.com"
        assert r.match_count == 1

    def test_preserves_non_pii(self):
        a = DocAnonymizer()
        r = a.anonymize("hello world")
        assert r.anonymized == "hello world"
        assert r.match_count == 0

    def test_multiple_replacements(self):
        a = DocAnonymizer()
        r = a.anonymize("a@b.com and c@d.com")
        assert r.match_count == 2
        assert r.anonymized.count("[REDACTED]") == 2

    def test_tokenize_mode_records_mapping(self):
        cfg = AnonymizerConfig(mode=MaskingMode.TOKENIZE)
        a = DocAnonymizer(cfg)
        r = a.anonymize("alice@x.com bob@y.com")
        assert "<PII_1>" in r.anonymized
        assert "<PII_2>" in r.anonymized
        assert set(r.mapping.values()) == {"alice@x.com", "bob@y.com"}

    def test_partial_mode_keeps_tail(self):
        cfg = AnonymizerConfig(mode=MaskingMode.PARTIAL, partial_keep=4)
        a = DocAnonymizer(cfg)
        r = a.anonymize("card 4111 1111 1111 1111 end")
        # Some characters preserved at the tail of the match
        assert "1111 end" in r.anonymized or "1111" in r.anonymized

    def test_offsets_are_correct(self):
        a = DocAnonymizer()
        text = "x alice@example.com y"
        r = a.anonymize(text)
        m = r.matches[0]
        assert text[m.start:m.end] == "alice@example.com"


# ----------------------------------------------------------------------
# restore()
# ----------------------------------------------------------------------
class TestRestore:
    def test_round_trip(self):
        cfg = AnonymizerConfig(mode=MaskingMode.TOKENIZE)
        a = DocAnonymizer(cfg)
        text = "alice@x.com talked to bob@y.com"
        r = a.anonymize(text)
        restored = a.restore(r.anonymized, r.mapping)
        assert restored == text

    def test_empty_mapping_is_noop(self):
        a = DocAnonymizer()
        assert a.restore("nothing here", {}) == "nothing here"

    def test_longer_tokens_first(self):
        # Ensure <PII_10> isn't broken by replacing <PII_1> first
        a = DocAnonymizer()
        mapping = {"<PII_1>": "A", "<PII_10>": "B"}
        out = a.restore("<PII_10> and <PII_1>", mapping)
        assert out == "B and A"


# ----------------------------------------------------------------------
# Batch / counters
# ----------------------------------------------------------------------
class TestAnonymizeBatch:
    def test_returns_list(self):
        a = DocAnonymizer()
        results = a.anonymize_batch(["a@b.com", "no pii"])
        assert len(results) == 2
        assert results[0].match_count == 1
        assert results[1].match_count == 0

    def test_total_counter(self):
        a = DocAnonymizer()
        a.anonymize_batch(["a@b.com", "c@d.com", "plain"])
        assert a.total_anonymized == 2

    def test_empty_batch(self):
        a = DocAnonymizer()
        assert a.anonymize_batch([]) == []


# ----------------------------------------------------------------------
# Enabled types behaviour
# ----------------------------------------------------------------------
class TestEnabledTypes:
    def test_disabled_type_not_masked(self):
        cfg = AnonymizerConfig(enabled_types={PiiType.EMAIL})
        a = DocAnonymizer(cfg)
        text = "192.168.1.1 and a@b.com"
        r = a.anonymize(text)
        assert "192.168.1.1" in r.anonymized
        assert "a@b.com" not in r.anonymized

    def test_all_disabled(self):
        cfg = AnonymizerConfig(enabled_types=set())
        a = DocAnonymizer(cfg)
        r = a.anonymize("alice@example.com 1.2.3.4 123-45-6789")
        assert r.anonymized == "alice@example.com 1.2.3.4 123-45-6789"
        assert r.match_count == 0

    def test_only_ssn(self):
        cfg = AnonymizerConfig(enabled_types={PiiType.SSN})
        a = DocAnonymizer(cfg)
        r = a.anonymize("123-45-6789 and a@b.com")
        assert "123-45-6789" not in r.anonymized
        assert "a@b.com" in r.anonymized


# ----------------------------------------------------------------------
# Edge cases
# ----------------------------------------------------------------------
class TestEdgeCases:
    def test_empty_string(self):
        a = DocAnonymizer()
        r = a.anonymize("")
        assert r.anonymized == ""
        assert r.match_count == 0

    def test_no_pii(self):
        a = DocAnonymizer()
        r = a.anonymize("just some plain text")
        assert r.anonymized == "just some plain text"

    def test_unicode_preserved(self):
        a = DocAnonymizer()
        r = a.anonymize("Привет alice@example.com мир")
        assert "Привет" in r.anonymized
        assert "мир" in r.anonymized
        assert "alice@example.com" not in r.anonymized

    def test_unknown_mode_raises(self):
        a = DocAnonymizer()
        with pytest.raises(ValueError):
            a.mask_value("x", PiiType.EMAIL, mode="not-a-mode")  # type: ignore[arg-type]

    def test_default_config_when_none(self):
        a = DocAnonymizer(None)
        assert isinstance(a.config, AnonymizerConfig)

    def test_total_anonymized_starts_zero(self):
        assert DocAnonymizer().total_anonymized == 0

    def test_repeat_anonymize_resets_token_ids(self):
        cfg = AnonymizerConfig(mode=MaskingMode.TOKENIZE)
        a = DocAnonymizer(cfg)
        r1 = a.anonymize("a@b.com")
        r2 = a.anonymize("c@d.com")
        # Tokens should reset per-call so each result is independently restorable
        assert "<PII_1>" in r1.anonymized
        assert "<PII_1>" in r2.anonymized

    def test_mode_override_per_call(self):
        a = DocAnonymizer()  # default REDACT
        out = a.mask_value("alice@example.com", PiiType.EMAIL, mode=MaskingMode.FAKE)
        assert out == "user@example.com"
