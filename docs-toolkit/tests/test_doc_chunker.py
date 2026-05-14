"""Tests for the doc_chunker module (E155)."""
import pytest

from docstoolkit.doc_chunker import (
    Chunk,
    ChunkConfig,
    ChunkStrategy,
    DocChunker,
)


# ===========================================================================
# ChunkStrategy enum
# ===========================================================================

class TestChunkStrategy:
    def test_has_fixed_size(self):
        assert ChunkStrategy.FIXED_SIZE.value == "fixed_size"

    def test_has_by_paragraph(self):
        assert ChunkStrategy.BY_PARAGRAPH.value == "by_paragraph"

    def test_has_by_sentence(self):
        assert ChunkStrategy.BY_SENTENCE.value == "by_sentence"

    def test_has_by_heading(self):
        assert ChunkStrategy.BY_HEADING.value == "by_heading"

    def test_has_by_token_count(self):
        assert ChunkStrategy.BY_TOKEN_COUNT.value == "by_token_count"

    def test_has_sliding_window(self):
        assert ChunkStrategy.SLIDING_WINDOW.value == "sliding_window"

    def test_six_strategies(self):
        assert len(list(ChunkStrategy)) == 6


# ===========================================================================
# Chunk dataclass
# ===========================================================================

class TestChunk:
    def test_basic_creation(self):
        c = Chunk(text="hi", chunk_id=0, start_pos=0, end_pos=2)
        assert c.text == "hi"
        assert c.chunk_id == 0
        assert c.start_pos == 0
        assert c.end_pos == 2

    def test_metadata_default_is_empty_dict(self):
        c = Chunk(text="hi", chunk_id=0, start_pos=0, end_pos=2)
        assert c.metadata == {}

    def test_token_count_default_is_zero(self):
        c = Chunk(text="hi", chunk_id=0, start_pos=0, end_pos=2)
        assert c.token_count == 0

    def test_metadata_is_independent_per_instance(self):
        a = Chunk(text="a", chunk_id=0, start_pos=0, end_pos=1)
        b = Chunk(text="b", chunk_id=1, start_pos=1, end_pos=2)
        a.metadata["x"] = 1
        assert "x" not in b.metadata


# ===========================================================================
# ChunkConfig
# ===========================================================================

class TestChunkConfig:
    def test_defaults(self):
        cfg = ChunkConfig()
        assert cfg.strategy == ChunkStrategy.FIXED_SIZE
        assert cfg.chunk_size == 500
        assert cfg.overlap == 0
        assert cfg.min_chunk_size == 50
        assert cfg.separator == "\n\n"

    def test_override(self):
        cfg = ChunkConfig(strategy=ChunkStrategy.BY_PARAGRAPH, chunk_size=100)
        assert cfg.strategy == ChunkStrategy.BY_PARAGRAPH
        assert cfg.chunk_size == 100


# ===========================================================================
# FIXED_SIZE
# ===========================================================================

class TestFixedSize:
    def test_exact_split_no_overlap(self):
        c = DocChunker()
        text = "a" * 100
        chunks = c.chunk_fixed_size(text, size=25, overlap=0)
        assert len(chunks) == 4
        assert all(ch.text == "a" * 25 for ch in chunks)

    def test_chunk_ids_sequential(self):
        c = DocChunker()
        chunks = c.chunk_fixed_size("x" * 30, size=10, overlap=0)
        assert [ch.chunk_id for ch in chunks] == [0, 1, 2]

    def test_with_overlap(self):
        c = DocChunker()
        text = "x" * 30
        chunks = c.chunk_fixed_size(text, size=10, overlap=2)
        # step = 8 → starts at 0, 8, 16, 24
        assert chunks[0].start_pos == 0
        assert chunks[1].start_pos == 8
        assert chunks[2].start_pos == 16

    def test_short_text_one_chunk(self):
        c = DocChunker()
        chunks = c.chunk_fixed_size("abc", size=10, overlap=0)
        assert len(chunks) == 1
        assert chunks[0].text == "abc"

    def test_break_at_whitespace(self):
        c = DocChunker()
        # 20-char text; size 12 would land mid-word, should break at space
        text = "hello world example here"
        chunks = c.chunk_fixed_size(text, size=12, overlap=0)
        # First chunk should not end in the middle of a word
        assert chunks[0].text.endswith(" ") or chunks[0].text in (
            "hello world ",
            "hello world",
        )

    def test_invalid_size_raises(self):
        c = DocChunker()
        with pytest.raises(ValueError):
            c.chunk_fixed_size("x", size=0)

    def test_overlap_ge_size_raises(self):
        c = DocChunker()
        with pytest.raises(ValueError):
            c.chunk_fixed_size("x" * 20, size=5, overlap=5)

    def test_empty_text(self):
        c = DocChunker()
        assert c.chunk_fixed_size("", size=10) == []


# ===========================================================================
# BY_PARAGRAPH
# ===========================================================================

class TestByParagraph:
    def test_basic_two_paragraphs(self):
        c = DocChunker()
        text = "First paragraph.\n\nSecond paragraph."
        chunks = c.chunk_by_paragraph(text)
        assert len(chunks) == 2
        assert chunks[0].text == "First paragraph."
        assert chunks[1].text == "Second paragraph."

    def test_three_paragraphs(self):
        c = DocChunker()
        text = "A\n\nB\n\nC"
        chunks = c.chunk_by_paragraph(text)
        assert [ch.text for ch in chunks] == ["A", "B", "C"]

    def test_custom_separator(self):
        c = DocChunker()
        text = "a---b---c"
        chunks = c.chunk_by_paragraph(text, separator="---")
        assert [ch.text for ch in chunks] == ["a", "b", "c"]

    def test_paragraph_num_metadata(self):
        c = DocChunker()
        chunks = c.chunk_by_paragraph("p1\n\np2\n\np3")
        assert chunks[0].metadata["paragraph_num"] == 0
        assert chunks[2].metadata["paragraph_num"] == 2

    def test_single_paragraph_no_separator(self):
        c = DocChunker()
        chunks = c.chunk_by_paragraph("single block")
        assert len(chunks) == 1
        assert chunks[0].text == "single block"


# ===========================================================================
# BY_SENTENCE
# ===========================================================================

class TestBySentence:
    def test_three_sentences(self):
        c = DocChunker()
        text = "First. Second! Third?"
        chunks = c.chunk_by_sentence(text)
        assert len(chunks) == 3
        assert chunks[0].text == "First."
        assert chunks[1].text == "Second!"
        assert chunks[2].text == "Third?"

    def test_single_sentence(self):
        c = DocChunker()
        chunks = c.chunk_by_sentence("Only one sentence here.")
        assert len(chunks) == 1

    def test_sentence_num_metadata(self):
        c = DocChunker()
        chunks = c.chunk_by_sentence("A. B. C.")
        assert chunks[0].metadata["sentence_num"] == 0
        assert chunks[2].metadata["sentence_num"] == 2

    def test_no_terminator_one_chunk(self):
        c = DocChunker()
        chunks = c.chunk_by_sentence("no terminator")
        assert len(chunks) == 1
        assert chunks[0].text == "no terminator"


# ===========================================================================
# BY_HEADING
# ===========================================================================

class TestByHeading:
    def test_two_headings(self):
        c = DocChunker()
        text = "# Title\nBody one.\n\n## Sub\nBody two."
        chunks = c.chunk_by_heading(text)
        assert len(chunks) == 2
        assert chunks[0].metadata["heading"] == "Title"
        assert chunks[1].metadata["heading"] == "Sub"

    def test_heading_levels(self):
        c = DocChunker()
        text = "# H1\ntext\n\n### H3\nmore"
        chunks = c.chunk_by_heading(text)
        assert chunks[0].metadata["level"] == 1
        assert chunks[1].metadata["level"] == 3

    def test_chunk_includes_heading_line(self):
        c = DocChunker()
        text = "# Title\nbody."
        chunks = c.chunk_by_heading(text)
        assert chunks[0].text.startswith("# Title")

    def test_preamble_before_first_heading(self):
        c = DocChunker()
        text = "preamble text\n\n# Title\nbody"
        chunks = c.chunk_by_heading(text)
        assert len(chunks) == 2
        assert chunks[0].metadata["heading"] is None
        assert chunks[1].metadata["heading"] == "Title"

    def test_no_headings_returns_one_chunk(self):
        c = DocChunker()
        text = "Just plain text without any markdown headings."
        chunks = c.chunk_by_heading(text)
        assert len(chunks) == 1
        assert chunks[0].metadata["heading"] is None

    def test_chunk_body_until_next_heading(self):
        c = DocChunker()
        text = "# A\nbody A\n\n# B\nbody B"
        chunks = c.chunk_by_heading(text)
        assert "body A" in chunks[0].text
        assert "body B" not in chunks[0].text
        assert "body B" in chunks[1].text


# ===========================================================================
# BY_TOKEN_COUNT
# ===========================================================================

class TestByTokenCount:
    def test_basic_split(self):
        c = DocChunker()
        text = "one two three four five six"
        chunks = c.chunk_by_token_count(text, max_tokens=2)
        assert len(chunks) == 3
        assert chunks[0].token_count == 2

    def test_token_count_matches_split(self):
        c = DocChunker()
        chunks = c.chunk_by_token_count("a b c d e", max_tokens=3)
        assert chunks[0].token_count == 3
        assert chunks[1].token_count == 2

    def test_with_overlap(self):
        c = DocChunker()
        text = "one two three four five six seven eight"
        chunks = c.chunk_by_token_count(text, max_tokens=4, overlap=1)
        # step = 3 → token starts 0, 3, 6
        assert chunks[0].metadata["token_start"] == 0
        assert chunks[1].metadata["token_start"] == 3

    def test_empty_text(self):
        c = DocChunker()
        assert c.chunk_by_token_count("", max_tokens=5) == []

    def test_invalid_max_tokens_raises(self):
        c = DocChunker()
        with pytest.raises(ValueError):
            c.chunk_by_token_count("text", max_tokens=0)


# ===========================================================================
# SLIDING_WINDOW
# ===========================================================================

class TestSlidingWindow:
    def test_basic_window_step(self):
        c = DocChunker()
        text = "abcdefghij"  # 10 chars
        chunks = c.chunk_sliding_window(text, window=4, step=2)
        # windows: [0:4], [2:6], [4:8], [6:10], [8:10]
        assert chunks[0].text == "abcd"
        assert chunks[1].text == "cdef"
        assert chunks[2].text == "efgh"

    def test_step_equals_window_no_overlap(self):
        c = DocChunker()
        text = "abcdefgh"
        chunks = c.chunk_sliding_window(text, window=4, step=4)
        assert [ch.text for ch in chunks] == ["abcd", "efgh"]

    def test_last_chunk_short_ok(self):
        c = DocChunker()
        text = "abcdefg"
        chunks = c.chunk_sliding_window(text, window=4, step=4)
        assert chunks[-1].text == "efg"

    def test_invalid_window_raises(self):
        c = DocChunker()
        with pytest.raises(ValueError):
            c.chunk_sliding_window("text", window=0, step=1)

    def test_invalid_step_raises(self):
        c = DocChunker()
        with pytest.raises(ValueError):
            c.chunk_sliding_window("text", window=2, step=0)


# ===========================================================================
# merge_small_chunks
# ===========================================================================

class TestMergeSmall:
    def test_merges_small_chunk_into_previous(self):
        chunks = [
            Chunk(text="this is a longer chunk", chunk_id=0, start_pos=0, end_pos=22),
            Chunk(text="x", chunk_id=1, start_pos=22, end_pos=23),
            Chunk(text="also a longer chunk", chunk_id=2, start_pos=23, end_pos=42),
        ]
        c = DocChunker()
        merged = c.merge_small_chunks(chunks, min_size=10)
        # The single "x" chunk gets merged
        assert len(merged) == 2

    def test_no_merge_when_all_large(self):
        chunks = [
            Chunk(text="aaaaaaaaaaa", chunk_id=0, start_pos=0, end_pos=11),
            Chunk(text="bbbbbbbbbbb", chunk_id=1, start_pos=11, end_pos=22),
        ]
        c = DocChunker()
        merged = c.merge_small_chunks(chunks, min_size=5)
        assert len(merged) == 2

    def test_empty_list(self):
        c = DocChunker()
        assert c.merge_small_chunks([], min_size=10) == []

    def test_renumbered_after_merge(self):
        chunks = [
            Chunk(text="x", chunk_id=0, start_pos=0, end_pos=1),
            Chunk(text="longer text here", chunk_id=1, start_pos=1, end_pos=17),
            Chunk(text="another long text", chunk_id=2, start_pos=17, end_pos=34),
        ]
        c = DocChunker()
        merged = c.merge_small_chunks(chunks, min_size=10)
        assert [m.chunk_id for m in merged] == list(range(len(merged)))


# ===========================================================================
# start/end positions correctness
# ===========================================================================

class TestStartEndPos:
    def test_fixed_size_offsets_match(self):
        c = DocChunker()
        text = "abcdefghijklmnop"
        chunks = c.chunk_fixed_size(text, size=4, overlap=0)
        for ch in chunks:
            assert text[ch.start_pos:ch.end_pos] == ch.text

    def test_paragraph_offsets_match(self):
        c = DocChunker()
        text = "Para one.\n\nPara two.\n\nPara three."
        chunks = c.chunk_by_paragraph(text)
        for ch in chunks:
            assert text[ch.start_pos:ch.end_pos] == ch.text

    def test_sentence_offsets_match(self):
        c = DocChunker()
        text = "One. Two. Three."
        chunks = c.chunk_by_sentence(text)
        for ch in chunks:
            assert text[ch.start_pos:ch.end_pos] == ch.text

    def test_heading_offsets_match(self):
        c = DocChunker()
        text = "# A\nbody A\n\n# B\nbody B"
        chunks = c.chunk_by_heading(text)
        for ch in chunks:
            assert text[ch.start_pos:ch.end_pos] == ch.text

    def test_sliding_window_offsets_match(self):
        c = DocChunker()
        text = "abcdefghij"
        chunks = c.chunk_sliding_window(text, window=4, step=2)
        for ch in chunks:
            assert text[ch.start_pos:ch.end_pos] == ch.text


# ===========================================================================
# Metadata
# ===========================================================================

class TestMetadata:
    def test_heading_metadata_set(self):
        c = DocChunker()
        chunks = c.chunk_by_heading("# Hello\nworld")
        assert chunks[0].metadata["heading"] == "Hello"

    def test_paragraph_metadata_set(self):
        c = DocChunker()
        chunks = c.chunk_by_paragraph("a\n\nb\n\nc")
        for i, ch in enumerate(chunks):
            assert ch.metadata["paragraph_num"] == i

    def test_strategy_recorded_in_metadata(self):
        c = DocChunker()
        chunks = c.chunk_fixed_size("hello world hello", size=8)
        assert chunks[0].metadata["strategy"] == "fixed_size"

    def test_token_metadata_has_token_indices(self):
        c = DocChunker()
        chunks = c.chunk_by_token_count("a b c d e", max_tokens=2)
        assert "token_start" in chunks[0].metadata
        assert "token_end" in chunks[0].metadata


# ===========================================================================
# chunk_batch
# ===========================================================================

class TestChunkBatch:
    def test_basic_batch(self):
        c = DocChunker(ChunkConfig(strategy=ChunkStrategy.BY_PARAGRAPH,
                                   min_chunk_size=0))
        texts = ["a\n\nb", "x\n\ny\n\nz"]
        result = c.chunk_batch(texts)
        assert len(result) == 2
        assert len(result[0]) == 2
        assert len(result[1]) == 3

    def test_empty_batch(self):
        c = DocChunker()
        assert c.chunk_batch([]) == []

    def test_batch_returns_list_of_lists(self):
        c = DocChunker(ChunkConfig(strategy=ChunkStrategy.BY_PARAGRAPH,
                                   min_chunk_size=0))
        result = c.chunk_batch(["a", "b"])
        assert isinstance(result, list)
        assert all(isinstance(r, list) for r in result)


# ===========================================================================
# min_chunk_size filtering
# ===========================================================================

class TestMinChunkSize:
    def test_small_chunks_dropped(self):
        cfg = ChunkConfig(
            strategy=ChunkStrategy.BY_PARAGRAPH,
            min_chunk_size=5,
        )
        c = DocChunker(cfg)
        text = "abc\n\nlong enough paragraph\n\nde"
        chunks = c.chunk(text)
        for ch in chunks:
            assert len(ch.text) >= 5

    def test_min_size_zero_keeps_all(self):
        cfg = ChunkConfig(
            strategy=ChunkStrategy.BY_PARAGRAPH,
            min_chunk_size=0,
        )
        c = DocChunker(cfg)
        chunks = c.chunk("a\n\nb\n\nlong paragraph here")
        assert len(chunks) == 3

    def test_all_too_small_keeps_original(self):
        cfg = ChunkConfig(
            strategy=ChunkStrategy.BY_PARAGRAPH,
            min_chunk_size=1000,
        )
        c = DocChunker(cfg)
        chunks = c.chunk("short\n\ntiny")
        # Implementation: if all would be filtered, keep original
        assert len(chunks) > 0


# ===========================================================================
# Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_empty_text_returns_empty(self):
        c = DocChunker()
        assert c.chunk("") == []

    def test_single_paragraph_one_chunk(self):
        cfg = ChunkConfig(strategy=ChunkStrategy.BY_PARAGRAPH, min_chunk_size=0)
        c = DocChunker(cfg)
        chunks = c.chunk("Only one paragraph here.")
        assert len(chunks) == 1

    def test_no_headings_returns_one_chunk(self):
        cfg = ChunkConfig(strategy=ChunkStrategy.BY_HEADING, min_chunk_size=0)
        c = DocChunker(cfg)
        chunks = c.chunk("No headings here at all.")
        assert len(chunks) == 1
        assert chunks[0].metadata["heading"] is None

    def test_non_string_input_raises(self):
        c = DocChunker()
        with pytest.raises(TypeError):
            c.chunk(123)  # type: ignore[arg-type]

    def test_dispatch_uses_configured_strategy(self):
        cfg = ChunkConfig(
            strategy=ChunkStrategy.BY_SENTENCE,
            min_chunk_size=0,
        )
        c = DocChunker(cfg)
        chunks = c.chunk("First. Second. Third.")
        assert len(chunks) == 3

    def test_default_config_when_none(self):
        c = DocChunker(None)
        assert c.config.strategy == ChunkStrategy.FIXED_SIZE
