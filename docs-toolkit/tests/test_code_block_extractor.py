"""Tests for docstoolkit.code_block_extractor — ≥45 tests."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.code_block_extractor import CodeBlock, CodeBlockExtractor, ExtractionStats


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_extractor() -> CodeBlockExtractor:
    return CodeBlockExtractor()


# ===========================================================================
# TestCodeBlockDataclass
# ===========================================================================

class TestCodeBlockDataclass:
    def test_fields_stored_correctly(self):
        b = CodeBlock(language="python", code="x = 1", line_start=2,
                      line_end=4, fence_char="`", fence_width=3)
        assert b.language == "python"
        assert b.code == "x = 1"
        assert b.line_start == 2
        assert b.line_end == 4
        assert b.fence_char == "`"
        assert b.fence_width == 3

    def test_line_count_single_line(self):
        b = CodeBlock(language="", code="hello", line_start=1,
                      line_end=3, fence_char="`", fence_width=3)
        assert b.line_count == 1

    def test_line_count_multi_line(self):
        b = CodeBlock(language="", code="a\nb\nc", line_start=1,
                      line_end=5, fence_char="`", fence_width=3)
        assert b.line_count == 3

    def test_line_count_empty_code(self):
        b = CodeBlock(language="", code="", line_start=1,
                      line_end=2, fence_char="`", fence_width=3)
        assert b.line_count == 0

    def test_is_empty_true_for_empty_code(self):
        b = CodeBlock(language="", code="", line_start=1,
                      line_end=2, fence_char="`", fence_width=3)
        assert b.is_empty is True

    def test_is_empty_true_for_whitespace_only(self):
        b = CodeBlock(language="", code="   \n  \n", line_start=1,
                      line_end=4, fence_char="`", fence_width=3)
        assert b.is_empty is True

    def test_is_empty_false_for_non_empty(self):
        b = CodeBlock(language="bash", code="echo hi", line_start=1,
                      line_end=3, fence_char="`", fence_width=3)
        assert b.is_empty is False

    def test_fence_width_stored(self):
        b = CodeBlock(language="", code="", line_start=1,
                      line_end=2, fence_char="`", fence_width=5)
        assert b.fence_width == 5


# ===========================================================================
# TestExtractionStatsDataclass
# ===========================================================================

class TestExtractionStatsDataclass:
    def test_most_common_language_single(self):
        s = ExtractionStats(total_blocks=1, by_language={"python": 1}, total_lines=5)
        assert s.most_common_language == "python"

    def test_most_common_language_multiple(self):
        s = ExtractionStats(total_blocks=5,
                            by_language={"python": 3, "bash": 2},
                            total_lines=20)
        assert s.most_common_language == "python"

    def test_most_common_language_empty(self):
        s = ExtractionStats(total_blocks=0, by_language={}, total_lines=0)
        assert s.most_common_language == ""

    def test_unique_languages(self):
        s = ExtractionStats(total_blocks=3,
                            by_language={"python": 2, "js": 1},
                            total_lines=10)
        assert s.unique_languages == {"python", "js"}

    def test_unique_languages_empty(self):
        s = ExtractionStats(total_blocks=0, by_language={}, total_lines=0)
        assert s.unique_languages == set()

    def test_most_common_language_no_lang_key(self):
        """Empty-string key represents unlabelled blocks."""
        s = ExtractionStats(total_blocks=2, by_language={"": 2}, total_lines=4)
        assert s.most_common_language == ""


# ===========================================================================
# TestExtractBasic
# ===========================================================================

class TestExtractBasic:
    def test_single_block_returns_one(self):
        text = "```python\nprint('hi')\n```\n"
        blocks = make_extractor().extract(text)
        assert len(blocks) == 1

    def test_single_block_language(self):
        text = "```python\nprint('hi')\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.language == "python"

    def test_single_block_code(self):
        text = "```python\nprint('hi')\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.code == "print('hi')"

    def test_no_language_tag(self):
        text = "```\nsome code\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.language == ""

    def test_fence_char_backtick(self):
        text = "```python\nx\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.fence_char == "`"

    def test_fence_width_three(self):
        text = "```python\nx\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.fence_width == 3

    def test_block_with_surrounding_prose(self):
        text = "Before\n```python\nx = 1\n```\nAfter\n"
        blocks = make_extractor().extract(text)
        assert len(blocks) == 1
        assert blocks[0].code == "x = 1"


# ===========================================================================
# TestExtractMultiple
# ===========================================================================

class TestExtractMultiple:
    def test_two_blocks_count(self):
        text = "```python\na\n```\n\n```bash\nb\n```\n"
        blocks = make_extractor().extract(text)
        assert len(blocks) == 2

    def test_two_blocks_languages(self):
        text = "```python\na\n```\n\n```bash\nb\n```\n"
        blocks = make_extractor().extract(text)
        assert blocks[0].language == "python"
        assert blocks[1].language == "bash"

    def test_three_blocks_order(self):
        text = "```a\n1\n```\n```b\n2\n```\n```c\n3\n```\n"
        blocks = make_extractor().extract(text)
        assert [b.language for b in blocks] == ["a", "b", "c"]

    def test_different_languages_mixed(self):
        text = "```python\nfoo\n```\n\n```javascript\nbar\n```\n"
        blocks = make_extractor().extract(text)
        assert blocks[0].code == "foo"
        assert blocks[1].code == "bar"


# ===========================================================================
# TestExtractTildes
# ===========================================================================

class TestExtractTildes:
    def test_tilde_fence_detected(self):
        text = "~~~python\nprint(1)\n~~~\n"
        blocks = make_extractor().extract(text)
        assert len(blocks) == 1

    def test_tilde_fence_char(self):
        text = "~~~python\nprint(1)\n~~~\n"
        block = make_extractor().extract(text)[0]
        assert block.fence_char == "~"

    def test_tilde_fence_language(self):
        text = "~~~bash\necho hi\n~~~\n"
        block = make_extractor().extract(text)[0]
        assert block.language == "bash"

    def test_tilde_fence_code(self):
        text = "~~~\nhello world\n~~~\n"
        block = make_extractor().extract(text)[0]
        assert block.code == "hello world"


# ===========================================================================
# TestExtractNoBlocks
# ===========================================================================

class TestExtractNoBlocks:
    def test_plain_text_returns_empty(self):
        assert make_extractor().extract("just plain text") == []

    def test_empty_string_returns_empty(self):
        assert make_extractor().extract("") == []

    def test_inline_code_not_matched(self):
        text = "Use `print()` for output."
        assert make_extractor().extract(text) == []

    def test_double_backtick_not_a_fence(self):
        text = "``not a fence``"
        assert make_extractor().extract(text) == []

    def test_unclosed_fence_not_returned(self):
        text = "```python\nno closing fence\n"
        assert make_extractor().extract(text) == []


# ===========================================================================
# TestExtractByLanguage
# ===========================================================================

class TestExtractByLanguage:
    def test_filter_returns_matching(self):
        text = "```python\na\n```\n```bash\nb\n```\n"
        blocks = make_extractor().extract_by_language(text, "python")
        assert len(blocks) == 1
        assert blocks[0].language == "python"

    def test_filter_returns_empty_for_missing_lang(self):
        text = "```python\na\n```\n"
        blocks = make_extractor().extract_by_language(text, "ruby")
        assert blocks == []

    def test_filter_empty_language(self):
        text = "```\nx\n```\n```python\ny\n```\n"
        blocks = make_extractor().extract_by_language(text, "")
        assert len(blocks) == 1
        assert blocks[0].code == "x"

    def test_filter_multiple_same_language(self):
        text = "```python\na\n```\n```python\nb\n```\n"
        blocks = make_extractor().extract_by_language(text, "python")
        assert len(blocks) == 2


# ===========================================================================
# TestStats
# ===========================================================================

class TestStats:
    def test_total_blocks_zero(self):
        s = make_extractor().stats("no blocks here")
        assert s.total_blocks == 0

    def test_total_blocks_two(self):
        text = "```python\na\n```\n```bash\nb\n```\n"
        s = make_extractor().stats(text)
        assert s.total_blocks == 2

    def test_by_language_counts(self):
        text = "```python\na\n```\n```python\nb\n```\n```bash\nc\n```\n"
        s = make_extractor().stats(text)
        assert s.by_language["python"] == 2
        assert s.by_language["bash"] == 1

    def test_total_lines(self):
        text = "```python\nline1\nline2\n```\n```bash\nline3\n```\n"
        s = make_extractor().stats(text)
        assert s.total_lines == 3

    def test_most_common_language_via_stats(self):
        text = "```python\na\n```\n```python\nb\n```\n```bash\nc\n```\n"
        s = make_extractor().stats(text)
        assert s.most_common_language == "python"


# ===========================================================================
# TestStripCodeBlocks
# ===========================================================================

class TestStripCodeBlocks:
    def test_strip_removes_block(self):
        text = "Before\n```python\ncode\n```\nAfter\n"
        result = make_extractor().strip_code_blocks(text)
        assert "```" not in result
        assert "code" not in result

    def test_strip_keeps_prose(self):
        text = "Before\n```python\ncode\n```\nAfter\n"
        result = make_extractor().strip_code_blocks(text)
        assert "Before" in result
        assert "After" in result

    def test_strip_no_blocks_unchanged(self):
        text = "just prose\nno blocks\n"
        result = make_extractor().strip_code_blocks(text)
        assert result == text

    def test_strip_multiple_blocks(self):
        text = "A\n```\nblock1\n```\nB\n```\nblock2\n```\nC\n"
        result = make_extractor().strip_code_blocks(text)
        assert "block1" not in result
        assert "block2" not in result
        assert "A" in result
        assert "B" in result
        assert "C" in result


# ===========================================================================
# TestReplaceCodeBlock
# ===========================================================================

class TestReplaceCodeBlock:
    def test_replace_changes_code(self):
        text = "```python\nold code\n```\n"
        extractor = make_extractor()
        block = extractor.extract(text)[0]
        result = extractor.replace_code_block(text, block, "new code")
        assert "new code" in result
        assert "old code" not in result

    def test_replace_preserves_opening_fence(self):
        text = "```python\nold\n```\n"
        extractor = make_extractor()
        block = extractor.extract(text)[0]
        result = extractor.replace_code_block(text, block, "new")
        assert "```python" in result

    def test_replace_preserves_closing_fence(self):
        text = "```python\nold\n```\n"
        extractor = make_extractor()
        block = extractor.extract(text)[0]
        result = extractor.replace_code_block(text, block, "new")
        assert result.count("```") >= 2

    def test_replace_preserves_surrounding_text(self):
        text = "Before\n```python\nold\n```\nAfter\n"
        extractor = make_extractor()
        block = extractor.extract(text)[0]
        result = extractor.replace_code_block(text, block, "new")
        assert "Before" in result
        assert "After" in result

    def test_replace_empty_new_code(self):
        text = "```python\nsome code\n```\n"
        extractor = make_extractor()
        block = extractor.extract(text)[0]
        result = extractor.replace_code_block(text, block, "")
        assert "some code" not in result
        # Fences still present
        assert "```python" in result


# ===========================================================================
# TestLineNumbers
# ===========================================================================

class TestLineNumbers:
    def test_line_start_first_line(self):
        text = "```python\ncode\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.line_start == 1

    def test_line_end_third_line(self):
        text = "```python\ncode\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.line_end == 3

    def test_line_start_after_prose(self):
        text = "line1\nline2\n```bash\ncmd\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.line_start == 3

    def test_line_end_after_prose(self):
        text = "line1\nline2\n```bash\ncmd\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.line_end == 5

    def test_two_blocks_line_numbers(self):
        text = "```a\nx\n```\n```b\ny\n```\n"
        blocks = make_extractor().extract(text)
        assert blocks[0].line_start == 1
        assert blocks[0].line_end == 3
        assert blocks[1].line_start == 4
        assert blocks[1].line_end == 6


# ===========================================================================
# TestEdgeCases
# ===========================================================================

class TestEdgeCases:
    def test_empty_block(self):
        text = "```python\n```\n"
        blocks = make_extractor().extract(text)
        assert len(blocks) == 1
        assert blocks[0].is_empty is True

    def test_four_backtick_fence(self):
        text = "````python\ncode\n````\n"
        blocks = make_extractor().extract(text)
        assert len(blocks) == 1
        assert blocks[0].fence_width == 4

    def test_four_backtick_not_closed_by_three(self):
        """A 4-backtick fence must be closed by 4+ backticks."""
        text = "````python\ncode\n```\nmore\n````\n"
        blocks = make_extractor().extract(text)
        assert len(blocks) == 1
        # The code body should include the 3-backtick line because it does not close
        assert "```" in blocks[0].code

    def test_backtick_fence_contains_tilde_sequence(self):
        """Tilde sequences inside a backtick fence do not close it."""
        text = "```python\n~~~\nstill inside\n~~~\n```\n"
        blocks = make_extractor().extract(text)
        assert len(blocks) == 1
        assert "~~~" in blocks[0].code

    def test_tilde_fence_contains_backtick_sequence(self):
        """Backtick sequences inside a tilde fence do not close it."""
        text = "~~~python\n```\nstill inside\n```\n~~~\n"
        blocks = make_extractor().extract(text)
        assert len(blocks) == 1
        assert "```" in blocks[0].code

    def test_language_with_extra_info_takes_first_word(self):
        text = "```python extra-info\ncode\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.language == "python"

    def test_multiline_code_preserved(self):
        text = "```python\nline1\nline2\nline3\n```\n"
        block = make_extractor().extract(text)[0]
        assert block.code == "line1\nline2\nline3"
        assert block.line_count == 3

    def test_tilde_four_width(self):
        text = "~~~~bash\ncmd\n~~~~\n"
        block = make_extractor().extract(text)[0]
        assert block.fence_width == 4
        assert block.fence_char == "~"
