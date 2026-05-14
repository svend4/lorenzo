"""Tests for docstoolkit.metadata_extractor — E64."""
from __future__ import annotations

import pytest

from docstoolkit.metadata_extractor import (
    DocumentMetadata,
    DocumentMetadataExtractor,
    ExtractionSchema,
    ExtractedField,
    FieldType,
    MetadataExtractor,
)


# ===========================================================================
# Fixtures
# ===========================================================================

@pytest.fixture()
def extractor() -> MetadataExtractor:
    return MetadataExtractor()


@pytest.fixture()
def doc_extractor() -> DocumentMetadataExtractor:
    return DocumentMetadataExtractor()


# ===========================================================================
# FieldType enum
# ===========================================================================

class TestFieldType:
    def test_enum_members_exist(self):
        members = {ft.name for ft in FieldType}
        assert members == {"TEXT", "DATE", "NUMBER", "EMAIL", "URL", "PHONE", "BOOLEAN"}

    def test_enum_values(self):
        assert FieldType.TEXT.value == "text"
        assert FieldType.DATE.value == "date"
        assert FieldType.NUMBER.value == "number"
        assert FieldType.EMAIL.value == "email"
        assert FieldType.URL.value == "url"
        assert FieldType.PHONE.value == "phone"
        assert FieldType.BOOLEAN.value == "boolean"

    def test_enum_count(self):
        assert len(FieldType) == 7

    def test_enum_identity(self):
        assert FieldType["EMAIL"] is FieldType.EMAIL


# ===========================================================================
# ExtractedField dataclass
# ===========================================================================

class TestExtractedField:
    def test_required_fields(self):
        ef = ExtractedField(name="email", value="a@b.com", field_type=FieldType.EMAIL)
        assert ef.name == "email"
        assert ef.value == "a@b.com"
        assert ef.field_type is FieldType.EMAIL

    def test_default_confidence(self):
        ef = ExtractedField(name="x", value=1, field_type=FieldType.NUMBER)
        assert ef.confidence == 1.0

    def test_default_source_span(self):
        ef = ExtractedField(name="x", value=1, field_type=FieldType.NUMBER)
        assert ef.source_span == (0, 0)

    def test_custom_confidence(self):
        ef = ExtractedField(name="x", value="y", field_type=FieldType.TEXT, confidence=0.75)
        assert ef.confidence == 0.75

    def test_custom_source_span(self):
        ef = ExtractedField(name="x", value="y", field_type=FieldType.TEXT, source_span=(5, 12))
        assert ef.source_span == (5, 12)

    def test_equality(self):
        ef1 = ExtractedField(name="n", value="v", field_type=FieldType.TEXT, source_span=(0, 1))
        ef2 = ExtractedField(name="n", value="v", field_type=FieldType.TEXT, source_span=(0, 1))
        assert ef1 == ef2

    def test_inequality_on_value(self):
        ef1 = ExtractedField(name="n", value="a", field_type=FieldType.TEXT)
        ef2 = ExtractedField(name="n", value="b", field_type=FieldType.TEXT)
        assert ef1 != ef2


# ===========================================================================
# ExtractionSchema dataclass
# ===========================================================================

class TestExtractionSchema:
    def test_default_empty_fields(self):
        schema = ExtractionSchema()
        assert schema.fields == []

    def test_fields_set(self):
        schema = ExtractionSchema(fields=["email", "date"])
        assert schema.fields == ["email", "date"]

    def test_independent_defaults(self):
        s1 = ExtractionSchema()
        s2 = ExtractionSchema()
        s1.fields.append("email")
        assert s2.fields == []


# ===========================================================================
# MetadataExtractor — extract_emails
# ===========================================================================

class TestExtractEmails:
    def test_single_email(self, extractor):
        results = extractor.extract_emails("Contact us: hello@example.com today")
        assert len(results) == 1
        assert results[0].value == "hello@example.com"

    def test_email_field_type(self, extractor):
        results = extractor.extract_emails("user@domain.org")
        assert results[0].field_type is FieldType.EMAIL

    def test_email_name(self, extractor):
        results = extractor.extract_emails("user@domain.org")
        assert results[0].name == "email"

    def test_email_span_correct(self, extractor):
        text = "abc user@test.com xyz"
        results = extractor.extract_emails(text)
        start, end = results[0].source_span
        assert text[start:end] == "user@test.com"

    def test_multiple_emails(self, extractor):
        text = "a@b.com and c@d.org and e@f.io"
        results = extractor.extract_emails(text)
        assert len(results) == 3
        assert {r.value for r in results} == {"a@b.com", "c@d.org", "e@f.io"}

    def test_no_email_returns_empty(self, extractor):
        assert extractor.extract_emails("no emails here") == []

    def test_email_with_plus(self, extractor):
        results = extractor.extract_emails("user+tag@example.com")
        assert results[0].value == "user+tag@example.com"

    def test_email_with_subdomain(self, extractor):
        results = extractor.extract_emails("a@mail.sub.example.com")
        assert len(results) == 1

    def test_empty_text_returns_empty(self, extractor):
        assert extractor.extract_emails("") == []


# ===========================================================================
# MetadataExtractor — extract_urls
# ===========================================================================

class TestExtractUrls:
    def test_http_url(self, extractor):
        results = extractor.extract_urls("Visit http://example.com now")
        assert len(results) == 1
        assert results[0].value == "http://example.com"

    def test_https_url(self, extractor):
        results = extractor.extract_urls("See https://secure.example.com/path?q=1")
        assert results[0].value == "https://secure.example.com/path?q=1"

    def test_url_field_type(self, extractor):
        results = extractor.extract_urls("https://x.com")
        assert results[0].field_type is FieldType.URL

    def test_url_name(self, extractor):
        results = extractor.extract_urls("https://x.com")
        assert results[0].name == "url"

    def test_multiple_urls(self, extractor):
        text = "a https://one.com b https://two.org c"
        results = extractor.extract_urls(text)
        assert len(results) == 2

    def test_no_url_returns_empty(self, extractor):
        assert extractor.extract_urls("no url here") == []

    def test_url_span(self, extractor):
        text = "go to https://example.com/page now"
        results = extractor.extract_urls(text)
        start, end = results[0].source_span
        assert text[start:end] == "https://example.com/page"

    def test_empty_text_returns_empty(self, extractor):
        assert extractor.extract_urls("") == []


# ===========================================================================
# MetadataExtractor — extract_dates
# ===========================================================================

class TestExtractDates:
    def test_iso_date(self, extractor):
        dates = extractor.extract_dates("Created on 2024-03-15.")
        assert "2024-03-15" in dates

    def test_eu_date(self, extractor):
        dates = extractor.extract_dates("Datum: 15.03.2024")
        assert "15.03.2024" in dates

    def test_us_date(self, extractor):
        dates = extractor.extract_dates("Date: 3/15/2024")
        assert "3/15/2024" in dates

    def test_multiple_formats_in_one_text(self, extractor):
        text = "ISO 2024-01-01 EU 1.1.2024 US 1/1/2024"
        dates = extractor.extract_dates(text)
        assert len(dates) >= 3

    def test_no_date_returns_empty(self, extractor):
        assert extractor.extract_dates("no dates here") == []

    def test_returns_strings(self, extractor):
        dates = extractor.extract_dates("2024-07-04")
        assert all(isinstance(d, str) for d in dates)

    def test_empty_text_returns_empty(self, extractor):
        assert extractor.extract_dates("") == []

    def test_eu_date_single_digit(self, extractor):
        dates = extractor.extract_dates("5.9.2023 is today")
        assert "5.9.2023" in dates


# ===========================================================================
# MetadataExtractor — extract_numbers
# ===========================================================================

class TestExtractNumbers:
    def test_integer(self, extractor):
        nums = extractor.extract_numbers("value is 42")
        assert 42.0 in nums

    def test_float(self, extractor):
        nums = extractor.extract_numbers("pi is 3.14")
        assert 3.14 in nums

    def test_negative(self, extractor):
        nums = extractor.extract_numbers("temperature -5 degrees")
        assert -5.0 in nums

    def test_multiple_numbers(self, extractor):
        nums = extractor.extract_numbers("1 2 3 4 5")
        assert nums == [1.0, 2.0, 3.0, 4.0, 5.0]

    def test_returns_floats(self, extractor):
        nums = extractor.extract_numbers("100")
        assert all(isinstance(n, float) for n in nums)

    def test_no_numbers_returns_empty(self, extractor):
        nums = extractor.extract_numbers("no numbers here")
        assert nums == []

    def test_empty_text_returns_empty(self, extractor):
        assert extractor.extract_numbers("") == []

    def test_mixed_text_and_numbers(self, extractor):
        nums = extractor.extract_numbers("abc 7 def 8.5 ghi")
        assert 7.0 in nums
        assert 8.5 in nums


# ===========================================================================
# MetadataExtractor — extract (sorted by position)
# ===========================================================================

class TestExtract:
    def test_returns_list(self, extractor):
        result = extractor.extract("hello@world.com https://example.com")
        assert isinstance(result, list)

    def test_sorted_by_position(self, extractor):
        text = "https://example.com then hello@world.com"
        result = extractor.extract(text)
        positions = [r.source_span[0] for r in result]
        assert positions == sorted(positions)

    def test_sorted_reverse_order_in_text(self, extractor):
        text = "email first user@test.com then url https://test.com"
        result = extractor.extract(text)
        positions = [r.source_span[0] for r in result]
        assert positions == sorted(positions)

    def test_multiple_types_found(self, extractor):
        text = "Email: user@test.com URL: https://test.com Date: 2024-01-01"
        result = extractor.extract(text)
        types_found = {r.field_type for r in result}
        assert FieldType.EMAIL in types_found
        assert FieldType.URL in types_found
        assert FieldType.DATE in types_found

    def test_empty_text_returns_empty(self, extractor):
        assert extractor.extract("") == []

    def test_no_matches_returns_empty(self, extractor):
        # Text with no emails, URLs, dates, phones; avoid "no"/"yes"/"true"/"false"
        assert extractor.extract("just plain words here patterns") == []

    def test_boolean_true_found(self, extractor):
        result = extractor.extract("flag is true")
        booleans = [r for r in result if r.field_type is FieldType.BOOLEAN]
        assert any(r.value is True for r in booleans)

    def test_boolean_false_found(self, extractor):
        result = extractor.extract("enabled: false")
        booleans = [r for r in result if r.field_type is FieldType.BOOLEAN]
        assert any(r.value is False for r in booleans)

    def test_boolean_yes(self, extractor):
        result = extractor.extract("answer: yes")
        booleans = [r for r in result if r.field_type is FieldType.BOOLEAN]
        assert any(r.value is True for r in booleans)

    def test_boolean_no(self, extractor):
        result = extractor.extract("answer: no")
        booleans = [r for r in result if r.field_type is FieldType.BOOLEAN]
        assert any(r.value is False for r in booleans)


# ===========================================================================
# MetadataExtractor — extract_to_dict
# ===========================================================================

class TestExtractToDict:
    def test_returns_dict_with_all_field_types(self, extractor):
        result = extractor.extract_to_dict("test")
        assert set(result.keys()) == {ft.name for ft in FieldType}

    def test_email_grouped_correctly(self, extractor):
        result = extractor.extract_to_dict("Contact: user@example.com")
        assert "user@example.com" in result["EMAIL"]

    def test_url_grouped_correctly(self, extractor):
        result = extractor.extract_to_dict("Visit https://example.com")
        assert "https://example.com" in result["URL"]

    def test_date_grouped_correctly(self, extractor):
        result = extractor.extract_to_dict("Created: 2024-01-01")
        assert "2024-01-01" in result["DATE"]

    def test_number_grouped_correctly(self, extractor):
        result = extractor.extract_to_dict("Count: 42")
        assert 42.0 in result["NUMBER"]

    def test_empty_lists_for_unmatched_types(self, extractor):
        result = extractor.extract_to_dict("just words here")
        assert result["EMAIL"] == []
        assert result["URL"] == []

    def test_empty_text_all_empty_lists(self, extractor):
        result = extractor.extract_to_dict("")
        for key in result:
            assert result[key] == []

    def test_multiple_emails_in_dict(self, extractor):
        result = extractor.extract_to_dict("a@b.com and c@d.com")
        assert len(result["EMAIL"]) == 2


# ===========================================================================
# DocumentMetadata dataclass
# ===========================================================================

class TestDocumentMetadata:
    def test_required_doc_id(self):
        dm = DocumentMetadata(doc_id="doc1")
        assert dm.doc_id == "doc1"

    def test_default_values(self):
        dm = DocumentMetadata(doc_id="doc1")
        assert dm.title == ""
        assert dm.author == ""
        assert dm.created_at == 0.0
        assert dm.word_count == 0
        assert dm.char_count == 0
        assert dm.language == "unknown"
        assert dm.tags == []
        assert dm.custom == {}

    def test_independent_tags_default(self):
        dm1 = DocumentMetadata(doc_id="a")
        dm2 = DocumentMetadata(doc_id="b")
        dm1.tags.append("TAG")
        assert dm2.tags == []

    def test_independent_custom_default(self):
        dm1 = DocumentMetadata(doc_id="a")
        dm2 = DocumentMetadata(doc_id="b")
        dm1.custom["k"] = "v"
        assert dm2.custom == {}


# ===========================================================================
# DocumentMetadataExtractor — word_count / char_count
# ===========================================================================

class TestDocumentCounts:
    def test_word_count(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "one two three four five")
        assert meta.word_count == 5

    def test_char_count(self, doc_extractor):
        text = "hello world"
        meta = doc_extractor.extract("doc1", text)
        assert meta.char_count == len(text)

    def test_empty_text_counts(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "")
        assert meta.word_count == 0
        assert meta.char_count == 0

    def test_single_word(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "word")
        assert meta.word_count == 1

    def test_multiline_word_count(self, doc_extractor):
        text = "line one\nline two\nthree"
        meta = doc_extractor.extract("doc1", text)
        assert meta.word_count == 5


# ===========================================================================
# DocumentMetadataExtractor — language detection
# ===========================================================================

class TestLanguageDetection:
    def test_english_text(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "This is a purely English text with many words.")
        assert meta.language == "en"

    def test_russian_text(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "Это чисто русский текст с большим количеством слов.")
        assert meta.language == "ru"

    def test_no_alpha_returns_unknown(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "123 456 789 !@#")
        assert meta.language == "unknown"

    def test_empty_text_returns_unknown(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "")
        assert meta.language == "unknown"

    def test_mostly_english_is_en(self, doc_extractor):
        # 80 % English letters, only a few Cyrillic
        meta = doc_extractor.extract("doc1", "Hello world это one two three four five six seven")
        assert meta.language == "en"

    def test_mostly_russian_is_ru(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "Привет мир hello один два три четыре пять шесть семь")
        assert meta.language == "ru"

    def test_cyrillic_exactly_above_threshold(self, doc_extractor):
        # Build text with exactly 21 % Cyrillic and rest Latin
        cyrillic_part = "а" * 21   # 21 Cyrillic chars
        latin_part = "b" * 79      # 79 Latin chars
        meta = doc_extractor.extract("doc1", cyrillic_part + latin_part)
        assert meta.language == "ru"

    def test_cyrillic_exactly_at_threshold_is_en(self, doc_extractor):
        # Exactly 20 % should NOT be > 0.20, so it should return "en"
        cyrillic_part = "а" * 20
        latin_part = "b" * 80
        meta = doc_extractor.extract("doc1", cyrillic_part + latin_part)
        assert meta.language == "en"


# ===========================================================================
# DocumentMetadataExtractor — title
# ===========================================================================

class TestTitleExtraction:
    def test_title_from_first_line(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "My Title\nSome body text.")
        assert meta.title == "My Title"

    def test_title_skips_empty_first_lines(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "\n\nActual Title\nbody")
        assert meta.title == "Actual Title"

    def test_title_truncated_to_100(self, doc_extractor):
        long_line = "A" * 200
        meta = doc_extractor.extract("doc1", long_line)
        assert len(meta.title) == 100

    def test_title_empty_for_empty_text(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "")
        assert meta.title == ""

    def test_title_stripped(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "  Padded Title  \nbody")
        assert meta.title == "Padded Title"

    def test_title_only_whitespace_lines(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "   \n   \n")
        assert meta.title == ""


# ===========================================================================
# DocumentMetadataExtractor — author from email
# ===========================================================================

class TestAuthorExtraction:
    def test_author_from_email(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "Author: john@example.com\nContent here.")
        assert meta.author == "john@example.com"

    def test_author_empty_when_no_email(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "No email here at all.")
        assert meta.author == ""

    def test_author_first_email_only(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "first@a.com second@b.com")
        assert meta.author == "first@a.com"

    def test_author_empty_text(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "")
        assert meta.author == ""


# ===========================================================================
# DocumentMetadataExtractor — tags
# ===========================================================================

class TestTagExtraction:
    def test_tags_repeated_caps(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "Use API often. API is great. REST is also here.")
        assert "API" in meta.tags

    def test_tags_requires_two_occurrences(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "ONCE appears only once in this text.")
        assert "ONCE" not in meta.tags

    def test_tags_min_three_chars(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "AB AB AB short. REST REST REST long.")
        # AB is only 2 chars so should not be a tag
        assert "AB" not in meta.tags
        assert "REST" in meta.tags

    def test_tags_sorted(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "REST REST REST API API API XML XML XML")
        assert meta.tags == sorted(meta.tags)

    def test_tags_empty_for_no_caps(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "no caps words here at all")
        assert meta.tags == []

    def test_tags_empty_text(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "")
        assert meta.tags == []

    def test_tags_multiple_unique(self, doc_extractor):
        meta = doc_extractor.extract("doc1", "API API REST REST XML XML SDK SDK")
        assert set(meta.tags) == {"API", "REST", "XML", "SDK"}


# ===========================================================================
# Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_very_long_text_does_not_crash(self, extractor):
        text = ("user@example.com " + "word " * 10_000 + "https://example.com ")
        result = extractor.extract(text)
        assert len(result) >= 2

    def test_overlapping_type_candidates(self, extractor):
        # A phone-like number inside a URL should not crash
        text = "https://example.com/phone/+1234567890/page"
        result = extractor.extract(text)
        assert any(r.field_type is FieldType.URL for r in result)

    def test_only_whitespace_returns_nothing_meaningful(self, extractor):
        result = extractor.extract("     \n\t  ")
        # Numbers might still be empty; no emails/urls/dates
        assert not any(r.field_type in (FieldType.EMAIL, FieldType.URL, FieldType.DATE)
                       for r in result)

    def test_doc_id_preserved(self, doc_extractor):
        meta = doc_extractor.extract("unique-id-42", "some text")
        assert meta.doc_id == "unique-id-42"

    def test_extract_to_dict_boolean_values(self, extractor):
        result = extractor.extract_to_dict("flag true and also false")
        assert True in result["BOOLEAN"]
        assert False in result["BOOLEAN"]

    def test_extract_numbers_negative_float(self, extractor):
        nums = extractor.extract_numbers("delta is -3.14")
        assert -3.14 in nums

    def test_extract_dates_returns_list_of_strings(self, extractor):
        dates = extractor.extract_dates("Born 1990-05-20 died 2050-01-01")
        assert isinstance(dates, list)
        assert all(isinstance(d, str) for d in dates)
