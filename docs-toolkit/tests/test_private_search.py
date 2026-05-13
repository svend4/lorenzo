"""Tests for the E38 Privacy-preserving search module.

Coverage:
    - QueryAnonymizer: email, phone, IP, credit-card redaction; is_sensitive;
      custom rules; multiple matches in a single query.
    - QueryGeneralizer: levels 1-3; token frequency; history tracking.
    - KAnonymizer: batch generalization; group_count; k enforcement.
    - PrivateSearcher: search results; privacy_applied list; flags;
      index_documents; noise_queries; k_anonymity integration.
"""
import pytest

from docstoolkit.private_search import (
    AnonymizationRule,
    KAnonymityConfig,
    KAnonymizer,
    PrivateSearchConfig,
    PrivateSearchResult,
    PrivateSearcher,
    QueryAnonymizer,
    QueryGeneralizer,
)


# ===========================================================================
# QueryAnonymizer
# ===========================================================================

class TestQueryAnonymizerEmail:
    def test_email_redacted(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("contact user@example.com please")
        assert "[EMAIL]" in result
        assert "user@example.com" not in result

    def test_email_label_in_list(self):
        a = QueryAnonymizer()
        _, labels = a.anonymize("send to foo@bar.org")
        assert "EMAIL" in labels

    def test_email_no_false_positive_plain_text(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("no sensitive data here")
        assert result == "no sensitive data here"
        assert labels == []

    def test_email_multiple_addresses(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("a@b.com and c@d.net")
        assert result.count("[EMAIL]") == 2
        assert "EMAIL" in labels

    def test_email_subdomain(self):
        a = QueryAnonymizer()
        result, _ = a.anonymize("user@mail.example.co.uk")
        assert "[EMAIL]" in result

    def test_email_plus_addressing(self):
        a = QueryAnonymizer()
        result, _ = a.anonymize("user+tag@example.com")
        assert "[EMAIL]" in result


class TestQueryAnonymizerPhone:
    def test_phone_dash_format(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("call 123-456-7890 now")
        assert "[PHONE]" in result
        assert "PHONE" in labels

    def test_phone_dot_format(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("123.456.7890")
        assert "[PHONE]" in result

    def test_phone_space_format(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("123 456 7890")
        assert "[PHONE]" in result

    def test_phone_not_triggered_by_short_numbers(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("code 123-45 is fine")
        assert "PHONE" not in labels


class TestQueryAnonymizerIP:
    def test_ip_redacted(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("server at 192.168.1.1 failed")
        assert "[IP]" in result
        assert "IP" in labels

    def test_ip_all_zeros(self):
        a = QueryAnonymizer()
        result, _ = a.anonymize("0.0.0.0")
        assert "[IP]" in result

    def test_ip_max_values(self):
        a = QueryAnonymizer()
        result, _ = a.anonymize("255.255.255.255")
        assert "[IP]" in result

    def test_ip_multiple(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("from 10.0.0.1 to 10.0.0.2")
        assert result.count("[IP]") == 2


class TestQueryAnonymizerCard:
    def test_card_dash_format(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("card 1234-5678-9012-3456")
        assert "[CARD]" in result
        assert "CARD" in labels

    def test_card_space_format(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("1234 5678 9012 3456")
        assert "[CARD]" in result
        assert "CARD" in labels

    def test_card_not_triggered_short(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("1234-5678")
        assert "CARD" not in labels


class TestQueryAnonymizerMixed:
    def test_multiple_pii_types(self):
        a = QueryAnonymizer()
        query = "email user@x.com ip 10.0.0.1 phone 555-123-4567"
        result, labels = a.anonymize(query)
        assert "[EMAIL]" in result
        assert "[IP]" in result
        assert "[PHONE]" in result
        assert "EMAIL" in labels
        assert "IP" in labels
        assert "PHONE" in labels

    def test_label_deduplication(self):
        """Same label should appear only once even with multiple matches."""
        a = QueryAnonymizer()
        _, labels = a.anonymize("a@b.com and c@d.net")
        assert labels.count("EMAIL") == 1

    def test_clean_query_unchanged(self):
        a = QueryAnonymizer()
        result, labels = a.anonymize("what is machine learning")
        assert result == "what is machine learning"
        assert labels == []


class TestQueryAnonymizerIsSensitive:
    def test_sensitive_email(self):
        a = QueryAnonymizer()
        assert a.is_sensitive("user@example.com") is True

    def test_sensitive_phone(self):
        a = QueryAnonymizer()
        assert a.is_sensitive("555-123-4567") is True

    def test_sensitive_ip(self):
        a = QueryAnonymizer()
        assert a.is_sensitive("192.168.0.1") is True

    def test_not_sensitive(self):
        a = QueryAnonymizer()
        assert a.is_sensitive("hello world") is False

    def test_sensitive_card(self):
        a = QueryAnonymizer()
        assert a.is_sensitive("1234-5678-9012-3456") is True


class TestQueryAnonymizerCustomRule:
    def test_custom_rule_applied(self):
        a = QueryAnonymizer()
        rule = AnonymizationRule(pattern=r'\bSSN-\d{9}\b', replacement='[SSN]', label='SSN')
        a.add_rule(rule)
        result, labels = a.anonymize("id SSN-123456789 here")
        assert "[SSN]" in result
        assert "SSN" in labels

    def test_custom_rule_is_sensitive(self):
        a = QueryAnonymizer()
        rule = AnonymizationRule(pattern=r'SECRET', replacement='[REDACTED]', label='SECRET')
        a.add_rule(rule)
        assert a.is_sensitive("this is SECRET") is True
        assert a.is_sensitive("this is fine") is False

    def test_multiple_custom_rules(self):
        a = QueryAnonymizer()
        a.add_rule(AnonymizationRule(pattern=r'\bPIN:\d{4}\b', replacement='[PIN]', label='PIN'))
        a.add_rule(AnonymizationRule(pattern=r'\bDOB:\d{8}\b', replacement='[DOB]', label='DOB'))
        result, labels = a.anonymize("PIN:1234 and DOB:19900101")
        assert "[PIN]" in result
        assert "[DOB]" in result
        assert "PIN" in labels
        assert "DOB" in labels


# ===========================================================================
# QueryGeneralizer
# ===========================================================================

class TestQueryGeneralizerTokenFrequency:
    def test_empty_history(self):
        g = QueryGeneralizer()
        assert g.token_frequency("unknown") == 0

    def test_frequency_after_add(self):
        g = QueryGeneralizer()
        g.add_to_history("machine learning is great")
        g.add_to_history("machine translation works")
        assert g.token_frequency("machine") == 2

    def test_case_insensitive_frequency(self):
        g = QueryGeneralizer()
        g.add_to_history("Python python PYTHON")
        assert g.token_frequency("python") == 3

    def test_single_occurrence(self):
        g = QueryGeneralizer()
        g.add_to_history("unique term here")
        assert g.token_frequency("unique") == 1


class TestQueryGeneralizerLevel1:
    def test_rare_tokens_removed(self):
        g = QueryGeneralizer()
        g.add_to_history("machine learning")
        g.add_to_history("machine vision")
        # "machine" appears twice, "rare" never
        result = g.generalize("machine rare term", level=1)
        assert "machine" in result
        assert "rare" not in result

    def test_all_rare_returns_original(self):
        g = QueryGeneralizer()
        # No history → all tokens are rare → return original
        result = g.generalize("unique query text", level=1)
        assert result == "unique query text"

    def test_common_tokens_kept(self):
        g = QueryGeneralizer()
        for _ in range(3):
            g.add_to_history("search query")
        result = g.generalize("search query fast", level=1)
        assert "search" in result
        assert "query" in result


class TestQueryGeneralizerLevel2:
    def test_numbers_replaced(self):
        g = QueryGeneralizer()
        g.add_to_history("order 12345 status")
        g.add_to_history("order 67890 status")
        result = g.generalize("order 12345 status", level=2)
        assert "[NUM]" in result
        assert "12345" not in result

    def test_title_case_replaced(self):
        g = QueryGeneralizer()
        g.add_to_history("John Smith query")
        g.add_to_history("John Doe query")
        result = g.generalize("John Smith query", level=2)
        assert "[NAME]" in result

    def test_lowercase_not_replaced(self):
        g = QueryGeneralizer()
        g.add_to_history("machine learning query")
        g.add_to_history("machine vision query")
        result = g.generalize("machine learning query", level=2)
        # All-lowercase words should not be replaced with [NAME]
        assert "[NAME]" not in result


class TestQueryGeneralizerLevel3:
    def test_top3_by_length(self):
        g = QueryGeneralizer()
        result = g.generalize("a bb ccc dddd eeeee", level=3)
        tokens = result.split()
        assert len(tokens) <= 3
        # Longest tokens should be present
        assert "eeeee" in tokens
        assert "dddd" in tokens

    def test_empty_query(self):
        g = QueryGeneralizer()
        result = g.generalize("", level=3)
        assert result == ""

    def test_single_token(self):
        g = QueryGeneralizer()
        result = g.generalize("hello", level=3)
        assert "hello" in result

    def test_level3_ignores_history(self):
        g = QueryGeneralizer()
        # Even without history, level 3 just picks longest tokens
        result = g.generalize("one two three four five", level=3)
        tokens = result.split()
        assert len(tokens) <= 3


# ===========================================================================
# KAnonymizer
# ===========================================================================

class TestKAnonymizer:
    def _make_k_queries(self, base: str, k: int) -> list[str]:
        """Create k identical queries."""
        return [base] * k

    def test_group_count_identical_queries(self):
        ka = KAnonymizer(KAnonymityConfig(k=3))
        queries = self._make_k_queries("machine learning", 5)
        counts = ka.group_count(queries)
        # All should map to the same group of size 5
        assert all(v >= 3 for v in counts.values())

    def test_anonymize_batch_returns_same_length(self):
        ka = KAnonymizer(KAnonymityConfig(k=2))
        queries = ["hello world", "hello world", "foo bar", "foo bar"]
        result = ka.anonymize_batch(queries)
        assert len(result) == len(queries)

    def test_anonymize_batch_empty(self):
        ka = KAnonymizer()
        assert ka.anonymize_batch([]) == []

    def test_group_count_returns_dict(self):
        ka = KAnonymizer(KAnonymityConfig(k=2))
        queries = ["a b", "a b", "c d", "c d"]
        counts = ka.group_count(queries)
        assert isinstance(counts, dict)
        assert len(counts) > 0

    def test_k_anonymity_enforced_with_generalization(self):
        """If queries are too diverse, generalization should merge groups."""
        # We have 6 queries split into pairs — k=3 forces further generalization
        queries = (
            ["apple mango fruit"] * 3
            + ["banana grape fruit"] * 3
        )
        ka = KAnonymizer(KAnonymityConfig(k=3))
        generalized = ka.anonymize_batch(queries)
        counts = dict()
        for g in generalized:
            counts[g] = counts.get(g, 0) + 1
        # Every group should have size >= 3
        for v in counts.values():
            assert v >= 3

    def test_default_config(self):
        ka = KAnonymizer()
        assert ka._config.k == 5

    def test_custom_config(self):
        config = KAnonymityConfig(k=10, generalization_level=2)
        ka = KAnonymizer(config)
        assert ka._config.k == 10
        assert ka._config.generalization_level == 2

    def test_group_count_values_are_ints(self):
        ka = KAnonymizer(KAnonymityConfig(k=2))
        queries = ["test query"] * 4
        counts = ka.group_count(queries)
        for v in counts.values():
            assert isinstance(v, int)


# ===========================================================================
# PrivateSearcher
# ===========================================================================

_DOCS = {
    "doc_python": "Python programming language tutorial basics",
    "doc_ml": "machine learning deep learning neural networks",
    "doc_web": "web development HTML CSS JavaScript frameworks",
    "doc_privacy": "privacy anonymity data protection GDPR compliance",
    "doc_search": "search engine indexing BM25 ranking algorithms",
}


class TestPrivateSearcherBasic:
    def test_search_returns_result_object(self):
        ps = PrivateSearcher(documents=_DOCS)
        result = ps.search("machine learning")
        assert isinstance(result, PrivateSearchResult)

    def test_result_has_all_fields(self):
        ps = PrivateSearcher(documents=_DOCS)
        result = ps.search("python tutorial")
        assert hasattr(result, "query")
        assert hasattr(result, "anonymized_query")
        assert hasattr(result, "results")
        assert hasattr(result, "privacy_applied")

    def test_original_query_preserved(self):
        ps = PrivateSearcher(documents=_DOCS)
        result = ps.search("python tutorial")
        assert result.query == "python tutorial"

    def test_results_is_list(self):
        ps = PrivateSearcher(documents=_DOCS)
        result = ps.search("machine learning")
        assert isinstance(result.results, list)

    def test_relevant_doc_returned(self):
        ps = PrivateSearcher(documents=_DOCS)
        result = ps.search("machine learning neural")
        assert "doc_ml" in result.results

    def test_privacy_applied_is_list(self):
        ps = PrivateSearcher(documents=_DOCS)
        result = ps.search("query")
        assert isinstance(result.privacy_applied, list)

    def test_no_docs_returns_empty_results(self):
        ps = PrivateSearcher()
        result = ps.search("anything")
        assert result.results == []

    def test_empty_query_returns_empty_results(self):
        ps = PrivateSearcher(documents=_DOCS)
        result = ps.search("")
        assert result.results == []


class TestPrivateSearcherAnonymizeFlag:
    def test_anonymize_queries_true_applies_technique(self):
        config = PrivateSearchConfig(anonymize_queries=True)
        ps = PrivateSearcher(config=config, documents=_DOCS)
        result = ps.search("python tutorial")
        assert "anonymize_queries" in result.privacy_applied

    def test_anonymize_queries_false_skips_technique(self):
        config = PrivateSearchConfig(anonymize_queries=False)
        ps = PrivateSearcher(config=config, documents=_DOCS)
        result = ps.search("python tutorial")
        assert "anonymize_queries" not in result.privacy_applied

    def test_pii_in_query_is_redacted(self):
        config = PrivateSearchConfig(anonymize_queries=True)
        ps = PrivateSearcher(config=config, documents=_DOCS)
        result = ps.search("find user@example.com about privacy")
        assert "[EMAIL]" in result.anonymized_query
        assert "user@example.com" not in result.anonymized_query

    def test_pii_label_in_privacy_applied(self):
        config = PrivateSearchConfig(anonymize_queries=True)
        ps = PrivateSearcher(config=config, documents=_DOCS)
        result = ps.search("server at 10.0.0.1 search")
        assert "IP" in result.privacy_applied

    def test_anonymize_off_preserves_query(self):
        config = PrivateSearchConfig(anonymize_queries=False)
        ps = PrivateSearcher(config=config, documents=_DOCS)
        result = ps.search("user@example.com search")
        assert result.anonymized_query == "user@example.com search"


class TestPrivateSearcherKAnonymity:
    def test_k_anonymity_flag_applies_technique(self):
        config = PrivateSearchConfig(k_anonymity=True, k=2)
        ps = PrivateSearcher(config=config, documents=_DOCS)
        result = ps.search("machine learning")
        assert "k_anonymity" in result.privacy_applied

    def test_k_anonymity_false_skips_technique(self):
        config = PrivateSearchConfig(k_anonymity=False)
        ps = PrivateSearcher(config=config, documents=_DOCS)
        result = ps.search("machine learning")
        assert "k_anonymity" not in result.privacy_applied

    def test_k_anonymity_still_returns_results(self):
        config = PrivateSearchConfig(k_anonymity=True, k=2)
        ps = PrivateSearcher(config=config, documents=_DOCS)
        result = ps.search("search indexing")
        assert isinstance(result.results, list)


class TestPrivateSearcherNoiseQueries:
    def test_noise_queries_in_privacy_applied(self):
        config = PrivateSearchConfig(noise_queries=3)
        ps = PrivateSearcher(config=config, documents=_DOCS)
        result = ps.search("python")
        assert "noise_queries" in result.privacy_applied

    def test_noise_queries_zero_not_in_privacy_applied(self):
        config = PrivateSearchConfig(noise_queries=0)
        ps = PrivateSearcher(config=config, documents=_DOCS)
        result = ps.search("python")
        assert "noise_queries" not in result.privacy_applied

    def test_noise_does_not_affect_real_results(self):
        config_noise = PrivateSearchConfig(noise_queries=5, anonymize_queries=False)
        config_clean = PrivateSearchConfig(noise_queries=0, anonymize_queries=False)
        ps_noise = PrivateSearcher(config=config_noise, documents=_DOCS)
        ps_clean = PrivateSearcher(config=config_clean, documents=_DOCS)
        r_noise = ps_noise.search("machine learning")
        r_clean = ps_clean.search("machine learning")
        assert r_noise.results == r_clean.results


class TestPrivateSearcherIndexDocuments:
    def test_index_documents_adds_to_search(self):
        ps = PrivateSearcher()
        ps.index_documents({"new_doc": "unique xylophone content here"})
        result = ps.search("xylophone")
        assert "new_doc" in result.results

    def test_index_documents_merges_with_existing(self):
        ps = PrivateSearcher(documents={"d1": "hello world"})
        ps.index_documents({"d2": "hello python"})
        result = ps.search("hello python")
        assert "d2" in result.results

    def test_search_ranks_relevant_docs_higher(self):
        ps = PrivateSearcher(documents={
            "relevant": "BM25 search ranking algorithm relevance scoring",
            "irrelevant": "cat dog bird animal pet",
        })
        result = ps.search("BM25 ranking")
        assert result.results[0] == "relevant"

    def test_all_matching_docs_in_results(self):
        docs = {
            "a": "python is great",
            "b": "python tutorial",
            "c": "java tutorial",
        }
        ps = PrivateSearcher(documents=docs)
        result = ps.search("python")
        assert "a" in result.results
        assert "b" in result.results


class TestPrivateSearcherDefaultConfig:
    def test_default_config_anonymizes(self):
        ps = PrivateSearcher(documents=_DOCS)
        result = ps.search("query about user@test.com")
        assert "anonymize_queries" in result.privacy_applied

    def test_default_config_no_k_anonymity(self):
        ps = PrivateSearcher(documents=_DOCS)
        result = ps.search("query")
        assert "k_anonymity" not in result.privacy_applied

    def test_default_config_no_noise(self):
        ps = PrivateSearcher(documents=_DOCS)
        result = ps.search("query")
        assert "noise_queries" not in result.privacy_applied
