"""Tests for docstoolkit.doc_transformer (E153)."""

from __future__ import annotations

import pytest

from docstoolkit.doc_transformer import (
    DocTransformer,
    Transform,
    TransformOp,
    TransformResult,
)


# ---------------------------------------------------------------------------
# Enum / dataclass basics
# ---------------------------------------------------------------------------


class TestTransformOp:
    def test_members_exist(self):
        names = {
            "UPPERCASE",
            "LOWERCASE",
            "TITLE_CASE",
            "SENTENCE_CASE",
            "REVERSE",
            "REDACT",
            "REPLACE",
            "EXTRACT",
            "PREFIX",
            "SUFFIX",
            "STRIP",
            "WRAP",
            "INDENT",
            "DEDENT",
        }
        assert names.issubset({m.name for m in TransformOp})

    def test_values_are_strings(self):
        for m in TransformOp:
            assert isinstance(m.value, str)

    def test_uppercase_value(self):
        assert TransformOp.UPPERCASE.value == "uppercase"


class TestTransform:
    def test_default_params_empty(self):
        t = Transform(op=TransformOp.UPPERCASE)
        assert t.params == {}

    def test_default_condition_none(self):
        t = Transform(op=TransformOp.UPPERCASE)
        assert t.condition is None

    def test_custom_params(self):
        t = Transform(op=TransformOp.REPLACE, params={"old": "a", "new": "b"})
        assert t.params == {"old": "a", "new": "b"}

    def test_custom_condition(self):
        t = Transform(op=TransformOp.UPPERCASE, condition=r"^hello")
        assert t.condition == r"^hello"


class TestTransformResult:
    def test_changed_true(self):
        r = TransformResult(original="a", transformed="b", applied=[])
        assert r.changed is True

    def test_changed_false(self):
        r = TransformResult(original="a", transformed="a", applied=[])
        assert r.changed is False

    def test_applied_default(self):
        r = TransformResult(original="a", transformed="a")
        assert r.applied == []


# ---------------------------------------------------------------------------
# Individual operations
# ---------------------------------------------------------------------------


@pytest.fixture
def t():
    return DocTransformer()


class TestUppercase:
    def test_basic(self, t):
        assert t.uppercase("hello") == "HELLO"

    def test_mixed(self, t):
        assert t.uppercase("Hello World") == "HELLO WORLD"

    def test_empty(self, t):
        assert t.uppercase("") == ""


class TestLowercase:
    def test_basic(self, t):
        assert t.lowercase("HELLO") == "hello"

    def test_mixed(self, t):
        assert t.lowercase("Hello World") == "hello world"

    def test_empty(self, t):
        assert t.lowercase("") == ""


class TestTitleCase:
    def test_basic(self, t):
        assert t.title_case("hello world") == "Hello World"

    def test_all_caps(self, t):
        assert t.title_case("HELLO WORLD") == "Hello World"


class TestSentenceCase:
    def test_basic(self, t):
        assert t.sentence_case("hello world") == "Hello world"

    def test_multiple_sentences(self, t):
        out = t.sentence_case("hello. world. foo")
        assert out.startswith("Hello.")
        assert "World." in out
        assert out.endswith("Foo")

    def test_empty(self, t):
        assert t.sentence_case("") == ""

    def test_question_mark(self, t):
        out = t.sentence_case("what? yes!")
        assert out.startswith("What?")
        assert "Yes!" in out


class TestReverse:
    def test_basic(self, t):
        assert t.reverse("abc") == "cba"

    def test_palindrome(self, t):
        assert t.reverse("aba") == "aba"

    def test_empty(self, t):
        assert t.reverse("") == ""


class TestRedact:
    def test_basic(self, t):
        out = t.redact("email me at a@b.com", r"\S+@\S+")
        assert out == "email me at [REDACTED]"

    def test_custom_replacement(self, t):
        out = t.redact("number 12345", r"\d+", "***")
        assert out == "number ***"

    def test_no_match(self, t):
        out = t.redact("hello", r"\d+")
        assert out == "hello"


class TestReplace:
    def test_plain(self, t):
        assert t.replace("hello world", "world", "there") == "hello there"

    def test_no_match(self, t):
        assert t.replace("hello", "xyz", "abc") == "hello"

    def test_regex(self, t):
        assert t.replace("a1b2c3", r"\d", "_", regex=True) == "a_b_c_"

    def test_regex_groups(self, t):
        # Plain mode treats backslashes literally.
        assert t.replace("foo bar", "bar", "baz") == "foo baz"


class TestExtract:
    def test_basic(self, t):
        nums = t.extract("a1 b22 c333", r"\d+")
        assert nums == ["1", "22", "333"]

    def test_no_match(self, t):
        assert t.extract("hello", r"\d+") == []

    def test_empty(self, t):
        assert t.extract("", r"\w+") == []


class TestPrefix:
    def test_single_line(self, t):
        assert t.prefix("hello", ">>> ") == ">>> hello"

    def test_multi_line(self, t):
        out = t.prefix("a\nb\nc", "- ")
        assert out == "- a\n- b\n- c"

    def test_empty(self, t):
        assert t.prefix("", "X") == ""


class TestSuffix:
    def test_single_line(self, t):
        assert t.suffix("hello", "!") == "hello!"

    def test_multi_line(self, t):
        out = t.suffix("a\nb", ";")
        assert out == "a;\nb;"

    def test_empty(self, t):
        assert t.suffix("", "!") == ""


class TestStrip:
    def test_basic(self, t):
        assert t.strip("  hello  ") == "hello"

    def test_multi_line(self, t):
        assert t.strip("  a  \n  b  ") == "a\nb"

    def test_empty(self, t):
        assert t.strip("") == ""


class TestWrap:
    def test_basic(self, t):
        assert t.wrap("hello", "<<", ">>") == "<<hello>>"

    def test_empty_text(self, t):
        assert t.wrap("", "[", "]") == "[]"


class TestIndent:
    def test_default(self, t):
        assert t.indent("hello") == "  hello"

    def test_custom_spaces(self, t):
        assert t.indent("hello", 4) == "    hello"

    def test_multi_line(self, t):
        assert t.indent("a\nb", 2) == "  a\n  b"

    def test_empty(self, t):
        assert t.indent("") == ""


class TestDedent:
    def test_basic(self, t):
        text = "    a\n    b"
        assert t.dedent(text) == "a\nb"

    def test_no_common(self, t):
        text = "a\n  b"
        assert t.dedent(text) == "a\n  b"

    def test_empty(self, t):
        assert t.dedent("") == ""


# ---------------------------------------------------------------------------
# Dispatch via apply()
# ---------------------------------------------------------------------------


class TestApply:
    def test_apply_uppercase(self, t):
        result = t.apply("hello", Transform(op=TransformOp.UPPERCASE))
        assert result == "HELLO"

    def test_apply_replace(self, t):
        tr = Transform(op=TransformOp.REPLACE, params={"old": "a", "new": "X"})
        assert t.apply("banana", tr) == "bXnXnX"

    def test_apply_redact(self, t):
        tr = Transform(
            op=TransformOp.REDACT,
            params={"pattern": r"\d+", "replacement": "#"},
        )
        assert t.apply("a1 b22", tr) == "a# b#"

    def test_apply_wrap(self, t):
        tr = Transform(
            op=TransformOp.WRAP, params={"before": "[", "after": "]"}
        )
        assert t.apply("hi", tr) == "[hi]"

    def test_apply_indent(self, t):
        tr = Transform(op=TransformOp.INDENT, params={"spaces": 3})
        assert t.apply("x", tr) == "   x"


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------


class TestApplyPipeline:
    def test_single(self, t):
        r = t.apply_pipeline("hello", [Transform(op=TransformOp.UPPERCASE)])
        assert r.transformed == "HELLO"
        assert r.applied == [TransformOp.UPPERCASE]

    def test_sequence(self, t):
        pipe = [
            Transform(op=TransformOp.STRIP),
            Transform(op=TransformOp.UPPERCASE),
            Transform(op=TransformOp.WRAP, params={"before": "<", "after": ">"}),
        ]
        r = t.apply_pipeline("  hello  ", pipe)
        assert r.transformed == "<HELLO>"
        assert len(r.applied) == 3

    def test_empty_pipeline(self, t):
        r = t.apply_pipeline("hello", [])
        assert r.transformed == "hello"
        assert r.applied == []
        assert r.changed is False

    def test_result_original_preserved(self, t):
        r = t.apply_pipeline(
            "abc", [Transform(op=TransformOp.UPPERCASE)]
        )
        assert r.original == "abc"

    def test_pipeline_changed_property(self, t):
        r = t.apply_pipeline("abc", [Transform(op=TransformOp.UPPERCASE)])
        assert r.changed is True


class TestApplyCondition:
    def test_condition_matches(self, t):
        tr = Transform(op=TransformOp.UPPERCASE, condition=r"^hello")
        r = t.apply_pipeline("hello world", [tr])
        assert r.transformed == "HELLO WORLD"
        assert r.applied == [TransformOp.UPPERCASE]

    def test_condition_no_match(self, t):
        tr = Transform(op=TransformOp.UPPERCASE, condition=r"^xyz")
        r = t.apply_pipeline("hello world", [tr])
        assert r.transformed == "hello world"
        assert r.applied == []

    def test_mixed_pipeline_conditions(self, t):
        pipe = [
            Transform(op=TransformOp.UPPERCASE, condition=r"hello"),
            Transform(op=TransformOp.REVERSE, condition=r"NOMATCH"),
        ]
        r = t.apply_pipeline("hello", pipe)
        assert r.transformed == "HELLO"
        assert r.applied == [TransformOp.UPPERCASE]


class TestApplyBatch:
    def test_basic(self, t):
        out = t.apply_batch(
            ["abc", "def"], [Transform(op=TransformOp.UPPERCASE)]
        )
        assert len(out) == 2
        assert all(isinstance(r, TransformResult) for r in out)
        assert out[0].transformed == "ABC"
        assert out[1].transformed == "DEF"

    def test_empty_list(self, t):
        out = t.apply_batch([], [Transform(op=TransformOp.UPPERCASE)])
        assert out == []

    def test_empty_pipeline(self, t):
        out = t.apply_batch(["a", "b"], [])
        assert [r.transformed for r in out] == ["a", "b"]


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_text_pipeline(self, t):
        r = t.apply_pipeline(
            "",
            [
                Transform(op=TransformOp.UPPERCASE),
                Transform(op=TransformOp.STRIP),
            ],
        )
        assert r.transformed == ""
        assert r.changed is False

    def test_unknown_op_raises(self, t):
        bogus = Transform.__new__(Transform)
        bogus.op = "NOT_A_REAL_OP"  # type: ignore[assignment]
        bogus.params = {}
        bogus.condition = None
        with pytest.raises(ValueError):
            t.apply("x", bogus)

    def test_extract_via_apply_joins_with_newline(self, t):
        tr = Transform(op=TransformOp.EXTRACT, params={"pattern": r"\d+"})
        out = t.apply("a1 b22", tr)
        assert out == "1\n22"

    def test_dedent_via_apply(self, t):
        out = t.apply("    a\n    b", Transform(op=TransformOp.DEDENT))
        assert out == "a\nb"

    def test_sentence_case_via_apply(self, t):
        out = t.apply("hello world", Transform(op=TransformOp.SENTENCE_CASE))
        assert out == "Hello world"

    def test_reverse_via_apply(self, t):
        out = t.apply("abc", Transform(op=TransformOp.REVERSE))
        assert out == "cba"

    def test_prefix_via_apply(self, t):
        out = t.apply(
            "x", Transform(op=TransformOp.PREFIX, params={"prefix": "> "})
        )
        assert out == "> x"

    def test_suffix_via_apply(self, t):
        out = t.apply(
            "x", Transform(op=TransformOp.SUFFIX, params={"suffix": "!"})
        )
        assert out == "x!"
