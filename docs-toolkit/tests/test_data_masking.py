"""Tests for the E103 Data Masking module (docstoolkit.data_masking).

Covers:
  - Each strategy on string values
  - PARTIAL edge cases (short string, partial_show=0, partial_show=1, exact boundary)
  - HASH is deterministic
  - NULLIFY returns None
  - Non-string value masking (int, float, None, bool)
  - Field pattern matching (exact, regex like ".*_token", "password|secret")
  - First matching rule wins (rule priority)
  - Nested dict masking (recursive=True)
  - recursive=False doesn't descend
  - mask_keys=True also masks field names
  - should_mask / matched_rule
  - mask_value returns unchanged if no match
  - Original dict not modified
  - Empty data
  - No rules → no masking
  - List values in dict (treat as non-dict, apply strategy to the list itself)
"""
import hashlib
import pytest

from docstoolkit.data_masking import DataMasker, MaskConfig, MaskRule, MaskStrategy


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _sha256_16(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()[:16]


def _masker(*rules: MaskRule, recursive: bool = True, mask_keys: bool = False) -> DataMasker:
    return DataMasker(MaskConfig(rules=list(rules), recursive=recursive, mask_keys=mask_keys))


# ===========================================================================
# MaskStrategy enum
# ===========================================================================

class TestMaskStrategy:
    def test_redact_value(self):
        assert MaskStrategy.REDACT.value == "redact"

    def test_partial_value(self):
        assert MaskStrategy.PARTIAL.value == "partial"

    def test_hash_value(self):
        assert MaskStrategy.HASH.value == "hash"

    def test_nullify_value(self):
        assert MaskStrategy.NULLIFY.value == "nullify"

    def test_fixed_value(self):
        assert MaskStrategy.FIXED.value == "fixed"

    def test_is_str_subclass(self):
        assert isinstance(MaskStrategy.REDACT, str)


# ===========================================================================
# mask_string — REDACT
# ===========================================================================

class TestMaskStringRedact:
    def setup_method(self):
        self.m = _masker()

    def test_redact_returns_three_stars(self):
        assert self.m.mask_string("secret", MaskStrategy.REDACT) == "***"

    def test_redact_empty_string(self):
        assert self.m.mask_string("", MaskStrategy.REDACT) == "***"

    def test_redact_long_string(self):
        assert self.m.mask_string("a" * 100, MaskStrategy.REDACT) == "***"

    def test_redact_single_char(self):
        assert self.m.mask_string("x", MaskStrategy.REDACT) == "***"


# ===========================================================================
# mask_string — PARTIAL
# ===========================================================================

class TestMaskStringPartial:
    def setup_method(self):
        self.m = _masker()

    def test_partial_normal(self):
        # "abcdefgh", partial_show=2 → "ab****gh"
        result = self.m.mask_string("abcdefgh", MaskStrategy.PARTIAL, partial_show=2)
        assert result == "ab****gh"

    def test_partial_show_1(self):
        # "abcde", partial_show=1 → "a***e"
        result = self.m.mask_string("abcde", MaskStrategy.PARTIAL, partial_show=1)
        assert result == "a***e"

    def test_partial_show_0_returns_all_stars(self):
        result = self.m.mask_string("hello", MaskStrategy.PARTIAL, partial_show=0)
        assert result == "*****"

    def test_partial_short_string_exact_boundary(self):
        # length == 2*partial_show → all stars
        result = self.m.mask_string("abcd", MaskStrategy.PARTIAL, partial_show=2)
        assert result == "****"

    def test_partial_short_string_below_boundary(self):
        # length < 2*partial_show → all stars
        result = self.m.mask_string("ab", MaskStrategy.PARTIAL, partial_show=3)
        assert result == "**"

    def test_partial_preserves_length(self):
        s = "hello_world"
        result = self.m.mask_string(s, MaskStrategy.PARTIAL, partial_show=2)
        assert len(result) == len(s)

    def test_partial_default_partial_show_2(self):
        # default partial_show is 2
        result = self.m.mask_string("abcdefgh", MaskStrategy.PARTIAL)
        assert result == "ab****gh"

    def test_partial_single_char(self):
        result = self.m.mask_string("x", MaskStrategy.PARTIAL, partial_show=2)
        assert result == "*"

    def test_partial_empty_string(self):
        result = self.m.mask_string("", MaskStrategy.PARTIAL, partial_show=2)
        assert result == ""

    def test_partial_exactly_one_middle_char(self):
        # "abcde", partial_show=2 → "ab*de"
        result = self.m.mask_string("abcde", MaskStrategy.PARTIAL, partial_show=2)
        assert result == "ab*de"


# ===========================================================================
# mask_string — HASH
# ===========================================================================

class TestMaskStringHash:
    def setup_method(self):
        self.m = _masker()

    def test_hash_length_is_16(self):
        result = self.m.mask_string("secret", MaskStrategy.HASH)
        assert len(result) == 16

    def test_hash_is_deterministic(self):
        r1 = self.m.mask_string("secret", MaskStrategy.HASH)
        r2 = self.m.mask_string("secret", MaskStrategy.HASH)
        assert r1 == r2

    def test_hash_different_values_differ(self):
        r1 = self.m.mask_string("secret1", MaskStrategy.HASH)
        r2 = self.m.mask_string("secret2", MaskStrategy.HASH)
        assert r1 != r2

    def test_hash_matches_expected(self):
        expected = _sha256_16("mypassword")
        assert self.m.mask_string("mypassword", MaskStrategy.HASH) == expected

    def test_hash_empty_string(self):
        result = self.m.mask_string("", MaskStrategy.HASH)
        assert result == _sha256_16("")


# ===========================================================================
# mask_string — NULLIFY
# ===========================================================================

class TestMaskStringNullify:
    def setup_method(self):
        self.m = _masker()

    def test_nullify_returns_none_string(self):
        # mask_string always returns a string; use mask_value for actual None
        result = self.m.mask_string("anything", MaskStrategy.NULLIFY)
        assert result == "None"


# ===========================================================================
# mask_string — FIXED
# ===========================================================================

class TestMaskStringFixed:
    def setup_method(self):
        self.m = _masker()

    def test_fixed_default_value(self):
        result = self.m.mask_string("secret", MaskStrategy.FIXED)
        assert result == "REDACTED"

    def test_fixed_custom_value(self):
        result = self.m.mask_string("secret", MaskStrategy.FIXED, fixed_value="<hidden>")
        assert result == "<hidden>"

    def test_fixed_empty_fixed_value(self):
        result = self.m.mask_string("secret", MaskStrategy.FIXED, fixed_value="")
        assert result == ""


# ===========================================================================
# Non-string value masking
# ===========================================================================

class TestNonStringMasking:
    def test_redact_int(self):
        m = _masker(MaskRule("field", MaskStrategy.REDACT))
        assert m.mask_value("field", 42) == "***"

    def test_redact_float(self):
        m = _masker(MaskRule("field", MaskStrategy.REDACT))
        assert m.mask_value("field", 3.14) == "***"

    def test_redact_none(self):
        m = _masker(MaskRule("field", MaskStrategy.REDACT))
        assert m.mask_value("field", None) == "***"

    def test_redact_bool(self):
        m = _masker(MaskRule("field", MaskStrategy.REDACT))
        assert m.mask_value("field", True) == "***"

    def test_nullify_int(self):
        m = _masker(MaskRule("field", MaskStrategy.NULLIFY))
        assert m.mask_value("field", 99) is None

    def test_nullify_none(self):
        m = _masker(MaskRule("field", MaskStrategy.NULLIFY))
        assert m.mask_value("field", None) is None

    def test_hash_int(self):
        m = _masker(MaskRule("field", MaskStrategy.HASH))
        result = m.mask_value("field", 42)
        assert result == _sha256_16("42")

    def test_hash_bool(self):
        m = _masker(MaskRule("field", MaskStrategy.HASH))
        result = m.mask_value("field", True)
        assert result == _sha256_16("True")

    def test_partial_int(self):
        # int → convert to string first, then PARTIAL
        m = _masker(MaskRule("field", MaskStrategy.PARTIAL, partial_show=1))
        result = m.mask_value("field", 12345)
        # "12345" → "1***5"
        assert result == "1***5"

    def test_fixed_float(self):
        m = _masker(MaskRule("field", MaskStrategy.FIXED, fixed_value="[MASKED]"))
        assert m.mask_value("field", 1.5) == "[MASKED]"

    def test_fixed_none(self):
        m = _masker(MaskRule("field", MaskStrategy.FIXED))
        assert m.mask_value("field", None) == "REDACTED"


# ===========================================================================
# Field pattern matching
# ===========================================================================

class TestFieldPatternMatching:
    def test_exact_match(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT))
        assert m.should_mask("password") is True
        assert m.should_mask("username") is False

    def test_wildcard_suffix_pattern(self):
        m = _masker(MaskRule(".*_token", MaskStrategy.HASH))
        assert m.should_mask("auth_token") is True
        assert m.should_mask("refresh_token") is True
        assert m.should_mask("token_auth") is False

    def test_alternation_pattern(self):
        m = _masker(MaskRule("password|secret", MaskStrategy.REDACT))
        assert m.should_mask("password") is True
        assert m.should_mask("secret") is True
        assert m.should_mask("token") is False

    def test_prefix_pattern(self):
        m = _masker(MaskRule("api_.*", MaskStrategy.REDACT))
        assert m.should_mask("api_key") is True
        assert m.should_mask("api_secret") is True
        assert m.should_mask("token") is False

    def test_case_sensitive_by_default(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT))
        assert m.should_mask("Password") is False

    def test_partial_match_not_accepted(self):
        # "pass" should NOT match a field named "password" with pattern "pass"
        m = _masker(MaskRule("pass", MaskStrategy.REDACT))
        assert m.should_mask("password") is False


# ===========================================================================
# Rule priority (first matching rule wins)
# ===========================================================================

class TestRulePriority:
    def test_first_rule_wins_over_second(self):
        m = _masker(
            MaskRule("password", MaskStrategy.REDACT),
            MaskRule("password", MaskStrategy.HASH),
        )
        result = m.mask_value("password", "secret")
        assert result == "***"  # REDACT wins

    def test_general_pattern_after_specific_not_applied(self):
        m = _masker(
            MaskRule("api_key", MaskStrategy.FIXED, fixed_value="KEY"),
            MaskRule("api_.*", MaskStrategy.REDACT),
        )
        result = m.mask_value("api_key", "xyz")
        assert result == "KEY"

    def test_second_rule_applied_when_first_no_match(self):
        m = _masker(
            MaskRule("other_field", MaskStrategy.REDACT),
            MaskRule("password", MaskStrategy.HASH),
        )
        result = m.mask_value("password", "secret")
        assert result == _sha256_16("secret")

    def test_matched_rule_returns_first(self):
        rule1 = MaskRule("field", MaskStrategy.REDACT)
        rule2 = MaskRule("field", MaskStrategy.HASH)
        m = _masker(rule1, rule2)
        assert m.matched_rule("field") is rule1


# ===========================================================================
# should_mask / matched_rule
# ===========================================================================

class TestShouldMaskAndMatchedRule:
    def test_should_mask_true(self):
        m = _masker(MaskRule("secret", MaskStrategy.REDACT))
        assert m.should_mask("secret") is True

    def test_should_mask_false(self):
        m = _masker(MaskRule("secret", MaskStrategy.REDACT))
        assert m.should_mask("public_info") is False

    def test_matched_rule_returns_none_when_no_match(self):
        m = _masker(MaskRule("secret", MaskStrategy.REDACT))
        assert m.matched_rule("public_info") is None

    def test_matched_rule_returns_correct_rule(self):
        rule = MaskRule("api_key", MaskStrategy.HASH)
        m = _masker(rule)
        assert m.matched_rule("api_key") is rule

    def test_no_rules_should_mask_false(self):
        m = _masker()
        assert m.should_mask("anything") is False

    def test_no_rules_matched_rule_none(self):
        m = _masker()
        assert m.matched_rule("anything") is None


# ===========================================================================
# mask_value — unchanged when no match
# ===========================================================================

class TestMaskValueNoMatch:
    def test_string_unchanged(self):
        m = _masker(MaskRule("secret", MaskStrategy.REDACT))
        assert m.mask_value("username", "alice") == "alice"

    def test_int_unchanged(self):
        m = _masker(MaskRule("secret", MaskStrategy.REDACT))
        assert m.mask_value("count", 5) == 5

    def test_none_unchanged(self):
        m = _masker(MaskRule("secret", MaskStrategy.REDACT))
        assert m.mask_value("value", None) is None

    def test_dict_unchanged(self):
        m = _masker(MaskRule("secret", MaskStrategy.REDACT))
        d = {"a": 1}
        assert m.mask_value("data", d) == {"a": 1}


# ===========================================================================
# mask() — full dict masking
# ===========================================================================

class TestMaskDict:
    def test_basic_masking(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT))
        result = m.mask({"username": "alice", "password": "s3cr3t"})
        assert result == {"username": "alice", "password": "***"}

    def test_unmatched_fields_pass_through(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT))
        result = m.mask({"name": "Bob", "age": 30})
        assert result == {"name": "Bob", "age": 30}

    def test_original_dict_not_modified(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT))
        original = {"username": "alice", "password": "s3cr3t"}
        original_copy = dict(original)
        m.mask(original)
        assert original == original_copy

    def test_empty_dict(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT))
        assert m.mask({}) == {}

    def test_no_rules_no_masking(self):
        m = _masker()
        data = {"password": "secret", "token": "abc"}
        assert m.mask(data) == data

    def test_multiple_rules_applied(self):
        m = _masker(
            MaskRule("password", MaskStrategy.REDACT),
            MaskRule("email", MaskStrategy.PARTIAL, partial_show=2),
        )
        result = m.mask({"password": "s3cr3t", "email": "alice@example.com", "name": "Alice"})
        assert result["password"] == "***"
        assert result["email"] != "alice@example.com"
        assert result["name"] == "Alice"

    def test_hash_strategy_in_mask(self):
        m = _masker(MaskRule("token", MaskStrategy.HASH))
        result = m.mask({"token": "mytoken"})
        assert result["token"] == _sha256_16("mytoken")

    def test_nullify_in_mask(self):
        m = _masker(MaskRule("ssn", MaskStrategy.NULLIFY))
        result = m.mask({"ssn": "123-45-6789", "name": "John"})
        assert result["ssn"] is None
        assert result["name"] == "John"

    def test_fixed_in_mask(self):
        m = _masker(MaskRule("api_key", MaskStrategy.FIXED, fixed_value="<redacted>"))
        result = m.mask({"api_key": "live_abc123"})
        assert result["api_key"] == "<redacted>"


# ===========================================================================
# Nested dict masking (recursive)
# ===========================================================================

class TestRecursiveMasking:
    def test_recursive_true_descends(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT), recursive=True)
        data = {"user": {"password": "secret", "name": "Alice"}}
        result = m.mask(data)
        assert result["user"]["password"] == "***"
        assert result["user"]["name"] == "Alice"

    def test_recursive_false_does_not_descend(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT), recursive=False)
        data = {"user": {"password": "secret", "name": "Alice"}}
        result = m.mask(data)
        # nested dict is returned as-is
        assert result["user"] == {"password": "secret", "name": "Alice"}

    def test_recursive_deep_nesting(self):
        m = _masker(MaskRule("token", MaskStrategy.REDACT), recursive=True)
        data = {"a": {"b": {"token": "abc"}}}
        result = m.mask(data)
        assert result["a"]["b"]["token"] == "***"

    def test_recursive_does_not_modify_original_nested(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT), recursive=True)
        inner = {"password": "secret"}
        outer = {"user": inner}
        m.mask(outer)
        assert inner["password"] == "secret"

    def test_top_level_and_nested_both_masked(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT), recursive=True)
        data = {"password": "top", "user": {"password": "nested"}}
        result = m.mask(data)
        assert result["password"] == "***"
        assert result["user"]["password"] == "***"

    def test_recursive_partial_on_nested_string(self):
        m = _masker(MaskRule("email", MaskStrategy.PARTIAL, partial_show=2), recursive=True)
        data = {"contact": {"email": "ab@cd.ef"}}
        result = m.mask(data)
        assert result["contact"]["email"] != "ab@cd.ef"
        assert len(result["contact"]["email"]) == len("ab@cd.ef")


# ===========================================================================
# mask_keys=True
# ===========================================================================

class TestMaskKeys:
    def test_mask_keys_true_redact(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT), mask_keys=True)
        result = m.mask({"password": "secret", "username": "alice"})
        assert "***" in result
        assert result["***"] == "***"
        assert result["username"] == "alice"

    def test_mask_keys_false_key_unchanged(self):
        m = _masker(MaskRule("password", MaskStrategy.REDACT), mask_keys=False)
        result = m.mask({"password": "secret"})
        assert "password" in result
        assert result["password"] == "***"

    def test_mask_keys_fixed_strategy(self):
        m = _masker(
            MaskRule("secret_key", MaskStrategy.FIXED, fixed_value="HIDDEN"),
            mask_keys=True,
        )
        result = m.mask({"secret_key": "value"})
        assert "HIDDEN" in result
        assert result["HIDDEN"] == "HIDDEN"

    def test_mask_keys_hash_strategy(self):
        m = _masker(MaskRule("password", MaskStrategy.HASH), mask_keys=True)
        result = m.mask({"password": "abc"})
        masked_key = _sha256_16("password")
        assert masked_key in result

    def test_mask_keys_nullify_strategy(self):
        m = _masker(MaskRule("ssn", MaskStrategy.NULLIFY), mask_keys=True)
        result = m.mask({"ssn": "123"})
        assert "None" in result
        assert result["None"] is None


# ===========================================================================
# List values in dict
# ===========================================================================

class TestListValues:
    def test_list_value_redact(self):
        m = _masker(MaskRule("tags", MaskStrategy.REDACT))
        result = m.mask({"tags": ["a", "b", "c"]})
        assert result["tags"] == "***"

    def test_list_value_fixed(self):
        m = _masker(MaskRule("tags", MaskStrategy.FIXED, fixed_value="[masked]"))
        result = m.mask({"tags": [1, 2, 3]})
        assert result["tags"] == "[masked]"

    def test_list_value_nullify(self):
        m = _masker(MaskRule("items", MaskStrategy.NULLIFY))
        result = m.mask({"items": [1, 2, 3]})
        assert result["items"] is None

    def test_list_value_not_recursed_into(self):
        # Lists are not dicts, so recursive=True should NOT descend into them
        m = _masker(MaskRule("password", MaskStrategy.REDACT), recursive=True)
        data = {"passwords": [{"password": "secret"}]}
        result = m.mask(data)
        # "passwords" key does not match "password" pattern
        assert result["passwords"] == [{"password": "secret"}]
