"""Tests for E211 doc_ai_assist."""
from __future__ import annotations

import pytest

from docstoolkit.doc_ai_assist import (
    AssistAction,
    AssistRequest,
    AssistResult,
    DocAiAssist,
    StubProvider,
)


# ---------------------------------------------------------------------------
class TestAssistAction:
    def test_has_all_eight_actions(self):
        names = {a.name for a in AssistAction}
        assert names == {
            "SUMMARIZE",
            "REWRITE",
            "EXPLAIN",
            "TRANSLATE",
            "EXPAND",
            "SHORTEN",
            "FORMALIZE",
            "SIMPLIFY",
        }

    def test_actions_are_strings(self):
        assert AssistAction.SUMMARIZE.value == "summarize"
        assert AssistAction.REWRITE.value == "rewrite"

    def test_action_equality(self):
        assert AssistAction.EXPLAIN == AssistAction.EXPLAIN
        assert AssistAction.EXPLAIN != AssistAction.SUMMARIZE


# ---------------------------------------------------------------------------
class TestAssistRequest:
    def test_minimal_request(self):
        req = AssistRequest(text="hello", action=AssistAction.SUMMARIZE)
        assert req.text == "hello"
        assert req.action is AssistAction.SUMMARIZE
        assert req.params == {}

    def test_request_with_params(self):
        req = AssistRequest(
            text="hi", action=AssistAction.TRANSLATE, params={"target_language": "ru"}
        )
        assert req.params == {"target_language": "ru"}

    def test_default_params_independent(self):
        r1 = AssistRequest(text="a", action=AssistAction.EXPLAIN)
        r2 = AssistRequest(text="b", action=AssistAction.EXPLAIN)
        r1.params["x"] = 1
        assert r2.params == {}


# ---------------------------------------------------------------------------
class TestAssistResult:
    def test_success_when_no_error(self):
        r = AssistResult(input="x", output="y", action=AssistAction.EXPLAIN)
        assert r.success is True

    def test_failure_when_error_set(self):
        r = AssistResult(input="x", output="", action=AssistAction.EXPLAIN, error="boom")
        assert r.success is False

    def test_defaults(self):
        r = AssistResult(input="x", output="y", action=AssistAction.EXPLAIN)
        assert r.tokens_used == 0
        assert r.latency_ms == 0.0
        assert r.error is None


# ---------------------------------------------------------------------------
class TestStubProviderSummarize:
    def setup_method(self):
        self.provider = StubProvider()

    def test_first_sentence_returned(self):
        req = AssistRequest(
            text="Hello world. Second sentence here.", action=AssistAction.SUMMARIZE
        )
        r = self.provider(req)
        assert r.output == "Hello world."

    def test_summarize_no_punctuation(self):
        req = AssistRequest(text="just one fragment", action=AssistAction.SUMMARIZE)
        r = self.provider(req)
        assert r.output == "just one fragment"

    def test_summarize_empty(self):
        req = AssistRequest(text="", action=AssistAction.SUMMARIZE)
        r = self.provider(req)
        assert r.output == ""
        assert r.success


# ---------------------------------------------------------------------------
class TestStubProviderRewrite:
    def setup_method(self):
        self.provider = StubProvider()

    def test_reverses_words(self):
        req = AssistRequest(text="one two three", action=AssistAction.REWRITE)
        r = self.provider(req)
        assert r.output == "three two one"

    def test_single_word(self):
        req = AssistRequest(text="alone", action=AssistAction.REWRITE)
        r = self.provider(req)
        assert r.output == "alone"


# ---------------------------------------------------------------------------
class TestStubProviderExplain:
    def setup_method(self):
        self.provider = StubProvider()

    def test_prefixes_with_explain(self):
        req = AssistRequest(text="foo", action=AssistAction.EXPLAIN)
        r = self.provider(req)
        assert r.output == "EXPLAIN: foo"

    def test_explain_empty_text(self):
        req = AssistRequest(text="", action=AssistAction.EXPLAIN)
        r = self.provider(req)
        assert r.output == "EXPLAIN: "


# ---------------------------------------------------------------------------
class TestStubProviderTranslate:
    def setup_method(self):
        self.provider = StubProvider()

    def test_uppercases(self):
        req = AssistRequest(text="hello world", action=AssistAction.TRANSLATE)
        r = self.provider(req)
        assert r.output == "HELLO WORLD"

    def test_already_upper(self):
        req = AssistRequest(text="ABC", action=AssistAction.TRANSLATE)
        r = self.provider(req)
        assert r.output == "ABC"


# ---------------------------------------------------------------------------
class TestStubProviderExpand:
    def setup_method(self):
        self.provider = StubProvider()

    def test_default_doubles_text(self):
        req = AssistRequest(text="hey", action=AssistAction.EXPAND)
        r = self.provider(req)
        assert r.output == "hey hey"

    def test_factor_three(self):
        req = AssistRequest(text="x", action=AssistAction.EXPAND, params={"factor": 3})
        r = self.provider(req)
        assert r.output == "x x x"

    def test_factor_invalid_falls_back_to_two(self):
        req = AssistRequest(text="z", action=AssistAction.EXPAND, params={"factor": "oops"})
        r = self.provider(req)
        assert r.output == "z z"


# ---------------------------------------------------------------------------
class TestStubProviderShorten:
    def setup_method(self):
        self.provider = StubProvider()

    def test_truncates_to_max_chars(self):
        req = AssistRequest(
            text="abcdefghij", action=AssistAction.SHORTEN, params={"max_chars": 4}
        )
        r = self.provider(req)
        assert r.output == "abcd"

    def test_shorter_than_limit_unchanged(self):
        req = AssistRequest(text="hi", action=AssistAction.SHORTEN, params={"max_chars": 10})
        r = self.provider(req)
        assert r.output == "hi"

    def test_default_max_chars(self):
        text = "x" * 500
        req = AssistRequest(text=text, action=AssistAction.SHORTEN)
        r = self.provider(req)
        assert len(r.output) == 200


# ---------------------------------------------------------------------------
class TestStubProviderFormalize:
    def setup_method(self):
        self.provider = StubProvider()

    def test_dont_expanded(self):
        req = AssistRequest(text="I don't know", action=AssistAction.FORMALIZE)
        r = self.provider(req)
        assert r.output == "I do not know"

    def test_wont_expanded(self):
        req = AssistRequest(text="he won't go", action=AssistAction.FORMALIZE)
        r = self.provider(req)
        assert r.output == "he will not go"

    def test_multiple_contractions(self):
        req = AssistRequest(text="don't and won't", action=AssistAction.FORMALIZE)
        r = self.provider(req)
        assert "do not" in r.output and "will not" in r.output


# ---------------------------------------------------------------------------
class TestStubProviderSimplify:
    def setup_method(self):
        self.provider = StubProvider()

    def test_longest_words_replaced(self):
        text = "extraordinary creativity demonstrates value"
        req = AssistRequest(text=text, action=AssistAction.SIMPLIFY)
        r = self.provider(req)
        # "extraordinary" (13), "demonstrates" (12), "creativity" (10) replaced
        assert "<word>" in r.output
        assert "extraordinary" not in r.output
        assert "demonstrates" not in r.output
        assert "creativity" not in r.output
        assert "value" in r.output

    def test_short_words_kept(self):
        req = AssistRequest(text="a b c", action=AssistAction.SIMPLIFY)
        r = self.provider(req)
        assert r.output == "a b c"


# ---------------------------------------------------------------------------
class TestSummarize:
    def test_summarize_uses_summarize_action(self):
        d = DocAiAssist()
        r = d.summarize("First. Second.")
        assert r.action is AssistAction.SUMMARIZE
        assert r.output == "First."

    def test_summarize_records_call(self):
        d = DocAiAssist()
        d.summarize("hi.")
        assert d.total_calls == 1


# ---------------------------------------------------------------------------
class TestRewrite:
    def test_rewrite_reverses(self):
        d = DocAiAssist()
        r = d.rewrite("a b c")
        assert r.output == "c b a"
        assert r.action is AssistAction.REWRITE

    def test_style_param_passed(self):
        captured = {}

        def prov(req: AssistRequest) -> AssistResult:
            captured.update(req.params)
            return AssistResult(input=req.text, output=req.text, action=req.action)

        d = DocAiAssist(provider=prov)
        d.rewrite("x", style="formal")
        assert captured == {"style": "formal"}


# ---------------------------------------------------------------------------
class TestExplain:
    def test_explain_prefix(self):
        d = DocAiAssist()
        r = d.explain("topic")
        assert r.output == "EXPLAIN: topic"

    def test_explain_action(self):
        d = DocAiAssist()
        r = d.explain("topic")
        assert r.action is AssistAction.EXPLAIN


# ---------------------------------------------------------------------------
class TestTranslate:
    def test_translate_uppercase(self):
        d = DocAiAssist()
        r = d.translate("hello")
        assert r.output == "HELLO"

    def test_target_language_param(self):
        captured = {}

        def prov(req: AssistRequest) -> AssistResult:
            captured.update(req.params)
            return AssistResult(input=req.text, output="", action=req.action)

        d = DocAiAssist(provider=prov)
        d.translate("hi", target_language="ru")
        assert captured == {"target_language": "ru"}


# ---------------------------------------------------------------------------
class TestExpand:
    def test_expand_doubles_by_default(self):
        d = DocAiAssist()
        r = d.expand("hi")
        assert r.output == "hi hi"

    def test_expand_factor(self):
        d = DocAiAssist()
        r = d.expand("k", factor=4)
        assert r.output == "k k k k"


# ---------------------------------------------------------------------------
class TestShorten:
    def test_shorten_default(self):
        d = DocAiAssist()
        r = d.shorten("x" * 300)
        assert len(r.output) == 200

    def test_shorten_custom(self):
        d = DocAiAssist()
        r = d.shorten("abcdef", max_chars=3)
        assert r.output == "abc"


# ---------------------------------------------------------------------------
class TestFormalize:
    def test_formalize_dont(self):
        d = DocAiAssist()
        r = d.formalize("don't worry")
        assert r.output == "do not worry"

    def test_formalize_action(self):
        d = DocAiAssist()
        r = d.formalize("won't")
        assert r.action is AssistAction.FORMALIZE


# ---------------------------------------------------------------------------
class TestSimplify:
    def test_simplify_replaces_long(self):
        d = DocAiAssist()
        r = d.simplify("complicated terminology baffles readers")
        assert "<word>" in r.output

    def test_simplify_action(self):
        d = DocAiAssist()
        r = d.simplify("xyzzy abc def")
        assert r.action is AssistAction.SIMPLIFY


# ---------------------------------------------------------------------------
class TestProcess:
    def test_process_dispatches_to_provider(self):
        d = DocAiAssist()
        req = AssistRequest(text="hi", action=AssistAction.EXPLAIN)
        r = d.process(req)
        assert r.output == "EXPLAIN: hi"

    def test_process_increments_calls(self):
        d = DocAiAssist()
        d.process(AssistRequest(text="x", action=AssistAction.EXPLAIN))
        d.process(AssistRequest(text="y", action=AssistAction.EXPLAIN))
        assert d.total_calls == 2

    def test_process_returns_assist_result(self):
        d = DocAiAssist()
        r = d.process(AssistRequest(text="z", action=AssistAction.SUMMARIZE))
        assert isinstance(r, AssistResult)


# ---------------------------------------------------------------------------
class TestBatch:
    def test_batch_returns_parallel_list(self):
        d = DocAiAssist()
        reqs = [
            AssistRequest(text="a b", action=AssistAction.REWRITE),
            AssistRequest(text="c", action=AssistAction.EXPLAIN),
            AssistRequest(text="HI", action=AssistAction.TRANSLATE),
        ]
        results = d.batch(reqs)
        assert len(results) == 3
        assert results[0].output == "b a"
        assert results[1].output == "EXPLAIN: c"
        assert results[2].output == "HI"

    def test_batch_empty(self):
        d = DocAiAssist()
        assert d.batch([]) == []

    def test_batch_updates_total_calls(self):
        d = DocAiAssist()
        d.batch(
            [
                AssistRequest(text="x", action=AssistAction.EXPLAIN),
                AssistRequest(text="y", action=AssistAction.EXPLAIN),
            ]
        )
        assert d.total_calls == 2


# ---------------------------------------------------------------------------
class TestTotalCalls:
    def test_starts_at_zero(self):
        assert DocAiAssist().total_calls == 0

    def test_increments_with_every_method(self):
        d = DocAiAssist()
        d.summarize("a.")
        d.rewrite("a b")
        d.explain("a")
        d.translate("a")
        d.expand("a")
        d.shorten("a")
        d.formalize("a")
        d.simplify("alpha beta gamma")
        assert d.total_calls == 8


# ---------------------------------------------------------------------------
class TestTotalTokens:
    def test_starts_at_zero(self):
        assert DocAiAssist().total_tokens == 0

    def test_sums_tokens_used(self):
        d = DocAiAssist()
        d.explain("one two three")  # 3 tokens
        d.explain("four five")  # 2 tokens
        assert d.total_tokens == 5

    def test_empty_text_zero_tokens(self):
        d = DocAiAssist()
        d.explain("")
        assert d.total_tokens == 0


# ---------------------------------------------------------------------------
class TestCustomProvider:
    def test_custom_callable_used(self):
        def prov(req: AssistRequest) -> AssistResult:
            return AssistResult(
                input=req.text,
                output="custom:" + req.text,
                action=req.action,
                tokens_used=42,
            )

        d = DocAiAssist(provider=prov)
        r = d.explain("hi")
        assert r.output == "custom:hi"
        assert r.tokens_used == 42

    def test_custom_provider_tokens_accumulate(self):
        def prov(req: AssistRequest) -> AssistResult:
            return AssistResult(input=req.text, output="", action=req.action, tokens_used=10)

        d = DocAiAssist(provider=prov)
        d.explain("x")
        d.explain("y")
        assert d.total_tokens == 20

    def test_provider_returning_error(self):
        def prov(req: AssistRequest) -> AssistResult:
            return AssistResult(
                input=req.text, output="", action=req.action, error="provider failed"
            )

        d = DocAiAssist(provider=prov)
        r = d.summarize("hi.")
        assert not r.success
        assert r.error == "provider failed"


# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_default_provider_is_stub(self):
        d = DocAiAssist()
        assert isinstance(d.provider, StubProvider)

    def test_tokens_used_matches_word_count(self):
        provider = StubProvider()
        r = provider(AssistRequest(text="a b c d e", action=AssistAction.EXPLAIN))
        assert r.tokens_used == 5

    def test_latency_recorded(self):
        provider = StubProvider()
        r = provider(AssistRequest(text="hi", action=AssistAction.EXPLAIN))
        assert r.latency_ms >= 0.0

    def test_result_input_preserved(self):
        provider = StubProvider()
        r = provider(AssistRequest(text="preserve me", action=AssistAction.TRANSLATE))
        assert r.input == "preserve me"

    def test_unicode_handled(self):
        d = DocAiAssist()
        r = d.translate("привет мир")
        assert r.output == "ПРИВЕТ МИР"

    def test_process_with_extra_params_ignored_by_stub(self):
        d = DocAiAssist()
        req = AssistRequest(
            text="hi", action=AssistAction.EXPLAIN, params={"unused": "value"}
        )
        r = d.process(req)
        assert r.success

    def test_request_dataclass_equality(self):
        r1 = AssistRequest(text="x", action=AssistAction.EXPLAIN)
        r2 = AssistRequest(text="x", action=AssistAction.EXPLAIN)
        assert r1 == r2


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
