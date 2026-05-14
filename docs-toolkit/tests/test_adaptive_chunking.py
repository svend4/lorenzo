"""Tests for the adaptive_chunking module (E23)."""
import pytest

from docstoolkit.adaptive_chunking import (
    Chunk,
    ChunkType,
    AdaptiveChunker,
    ChunkConfig,
    ChunkingStrategy,
    StrategySelector,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_chunk(text: str, chunk_type: ChunkType = ChunkType.PARAGRAPH) -> Chunk:
    return Chunk(
        text=text,
        chunk_type=chunk_type,
        doc_id="test-doc",
        start_char=0,
        end_char=len(text),
    )


# ===========================================================================
# Chunk dataclass
# ===========================================================================

class TestChunkBasics:
    def test_chunk_id_is_8_chars(self):
        c = make_chunk("hello world")
        assert len(c.chunk_id) == 8

    def test_chunk_id_is_hex(self):
        c = make_chunk("hello world")
        int(c.chunk_id, 16)  # should not raise

    def test_chunk_ids_are_unique(self):
        ids = {make_chunk("x").chunk_id for _ in range(50)}
        assert len(ids) == 50

    def test_word_count_simple(self):
        c = make_chunk("one two three")
        assert c.word_count() == 3

    def test_word_count_empty(self):
        c = make_chunk("")
        assert c.word_count() == 0

    def test_word_count_extra_spaces(self):
        c = make_chunk("  hello   world  ")
        assert c.word_count() == 2

    def test_char_count(self):
        text = "hello world"
        c = make_chunk(text)
        assert c.char_count() == len(text)

    def test_char_count_empty(self):
        c = make_chunk("")
        assert c.char_count() == 0

    def test_is_empty_false(self):
        c = make_chunk("not empty")
        assert c.is_empty() is False

    def test_is_empty_true_blank(self):
        c = make_chunk("")
        assert c.is_empty() is True

    def test_is_empty_true_whitespace(self):
        c = make_chunk("   \n\t  ")
        assert c.is_empty() is True

    def test_metadata_default_is_empty_dict(self):
        c = make_chunk("text")
        assert c.metadata == {}

    def test_metadata_custom(self):
        c = Chunk(
            text="text",
            chunk_type=ChunkType.FIXED,
            doc_id="d",
            start_char=0,
            end_char=4,
            metadata={"key": "value"},
        )
        assert c.metadata["key"] == "value"

    def test_chunk_type_values(self):
        assert ChunkType.PARAGRAPH.value == "paragraph"
        assert ChunkType.SENTENCE.value == "sentence"
        assert ChunkType.HEADING_SECTION.value == "heading_section"
        assert ChunkType.FIXED.value == "fixed"
        assert ChunkType.SEMANTIC.value == "semantic"


# ===========================================================================
# ChunkConfig
# ===========================================================================

class TestChunkConfig:
    def test_defaults(self):
        cfg = ChunkConfig()
        assert cfg.target_size == 300
        assert cfg.min_size == 50
        assert cfg.max_size == 600
        assert cfg.overlap == 0

    def test_custom_values(self):
        cfg = ChunkConfig(target_size=100, min_size=20, max_size=200, overlap=10)
        assert cfg.target_size == 100
        assert cfg.min_size == 20
        assert cfg.max_size == 200
        assert cfg.overlap == 10


# ===========================================================================
# AdaptiveChunker.chunk_by_paragraphs
# ===========================================================================

class TestChunkByParagraphs:
    def setup_method(self):
        self.chunker = AdaptiveChunker()

    def _cfg(self, **kw):
        return ChunkConfig(target_size=300, min_size=50, max_size=600, **kw)

    def test_empty_text_returns_empty(self):
        result = self.chunker.chunk_by_paragraphs("", "doc1")
        assert result == []

    def test_single_paragraph(self):
        text = "word " * 60  # 60 words, above min_size=50
        result = self.chunker.chunk_by_paragraphs(text, "doc1", ChunkConfig(min_size=50))
        assert len(result) == 1
        assert result[0].chunk_type == ChunkType.PARAGRAPH

    def test_two_paragraphs(self):
        para1 = "word " * 60
        para2 = "thing " * 60
        text = para1 + "\n\n" + para2
        result = self.chunker.chunk_by_paragraphs(text, "doc1", ChunkConfig(min_size=50))
        assert len(result) == 2

    def test_short_paragraph_merged_with_next(self):
        short = "tiny para"  # 2 words < min_size=50
        long_para = "word " * 60
        text = short + "\n\n" + long_para
        cfg = ChunkConfig(min_size=50, max_size=600, target_size=300)
        result = self.chunker.chunk_by_paragraphs(text, "doc1", cfg)
        # short should be merged into one chunk
        assert len(result) == 1
        assert "tiny para" in result[0].text

    def test_oversized_paragraph_split(self):
        # Create a paragraph > max_size=100 words with clear sentence boundaries
        sentences = ["This is sentence number {0}. ".format(i) for i in range(30)]
        text = "".join(sentences)
        cfg = ChunkConfig(target_size=50, min_size=5, max_size=100)
        result = self.chunker.chunk_by_paragraphs(text, "doc1", cfg)
        assert len(result) > 1
        for chunk in result:
            assert chunk.word_count() <= cfg.max_size + 20  # allow small overshoot per sentence

    def test_doc_id_set_correctly(self):
        text = "Some paragraph with enough words " * 5
        result = self.chunker.chunk_by_paragraphs(text, "my-doc")
        assert all(c.doc_id == "my-doc" for c in result)

    def test_char_offsets_within_original(self):
        para1 = "First paragraph with enough words here now."
        para2 = "Second paragraph with enough words here now."
        text = para1 + "\n\n" + para2
        cfg = ChunkConfig(min_size=2, max_size=600)
        result = self.chunker.chunk_by_paragraphs(text, "doc1", cfg)
        for chunk in result:
            assert chunk.start_char >= 0
            assert chunk.end_char <= len(text)
            assert text[chunk.start_char:chunk.end_char] == chunk.text

    def test_whitespace_only_paragraphs_skipped(self):
        text = "Good paragraph here.\n\n   \n\nAnother good paragraph here."
        cfg = ChunkConfig(min_size=1, max_size=600)
        result = self.chunker.chunk_by_paragraphs(text, "doc1", cfg)
        assert all(not c.is_empty() for c in result)


# ===========================================================================
# AdaptiveChunker.chunk_by_headings
# ===========================================================================

class TestChunkByHeadings:
    def setup_method(self):
        self.chunker = AdaptiveChunker()

    def test_empty_text(self):
        assert self.chunker.chunk_by_headings("", "doc") == []

    def test_single_section(self):
        text = "# Introduction\n\nSome introductory content here."
        result = self.chunker.chunk_by_headings(text, "doc")
        assert len(result) == 1
        assert result[0].chunk_type == ChunkType.HEADING_SECTION
        assert "Introduction" in result[0].text

    def test_two_sections(self):
        text = "# Section One\n\nContent one.\n\n# Section Two\n\nContent two."
        result = self.chunker.chunk_by_headings(text, "doc")
        assert len(result) == 2

    def test_three_sections(self):
        text = "# A\n\nContent A.\n\n## B\n\nContent B.\n\n### C\n\nContent C."
        result = self.chunker.chunk_by_headings(text, "doc")
        assert len(result) == 3

    def test_section_includes_heading(self):
        text = "# My Heading\n\nBody text here."
        result = self.chunker.chunk_by_headings(text, "doc")
        assert "# My Heading" in result[0].text

    def test_section_includes_content(self):
        text = "# My Heading\n\nBody text here."
        result = self.chunker.chunk_by_headings(text, "doc")
        assert "Body text here." in result[0].text

    def test_content_before_first_heading(self):
        text = "Preamble text.\n\n# Section\n\nContent."
        result = self.chunker.chunk_by_headings(text, "doc")
        # preamble + section = 2 chunks
        assert len(result) == 2

    def test_no_headings_returns_one_chunk(self):
        text = "Just plain text without any headings at all."
        result = self.chunker.chunk_by_headings(text, "doc")
        assert len(result) == 1

    def test_heading_section_type(self):
        text = "# Title\n\nContent here."
        result = self.chunker.chunk_by_headings(text, "doc")
        assert result[0].chunk_type == ChunkType.HEADING_SECTION

    def test_doc_id_propagated(self):
        text = "# Title\n\nContent."
        result = self.chunker.chunk_by_headings(text, "myid")
        assert result[0].doc_id == "myid"


# ===========================================================================
# AdaptiveChunker.chunk_fixed
# ===========================================================================

class TestChunkFixed:
    def setup_method(self):
        self.chunker = AdaptiveChunker()

    def test_empty_text(self):
        assert self.chunker.chunk_fixed("", "doc") == []

    def test_exact_target(self):
        text = " ".join(f"word{i}" for i in range(10))
        cfg = ChunkConfig(target_size=10, min_size=1, max_size=20)
        result = self.chunker.chunk_fixed(text, "doc", cfg)
        assert len(result) == 1
        assert result[0].word_count() == 10

    def test_two_chunks(self):
        text = " ".join(f"w{i}" for i in range(20))
        cfg = ChunkConfig(target_size=10, min_size=1, max_size=20, overlap=0)
        result = self.chunker.chunk_fixed(text, "doc", cfg)
        assert len(result) == 2

    def test_last_chunk_smaller(self):
        # 25 words, target=10 → chunks of 10, 10, 5
        text = " ".join(f"w{i}" for i in range(25))
        cfg = ChunkConfig(target_size=10, min_size=1, max_size=30, overlap=0)
        result = self.chunker.chunk_fixed(text, "doc", cfg)
        assert result[-1].word_count() == 5

    def test_overlap_increases_chunk_count(self):
        # 20 words, target=10, overlap=5 → step=5 → 3 chunks
        text = " ".join(f"w{i}" for i in range(20))
        cfg = ChunkConfig(target_size=10, min_size=1, max_size=20, overlap=5)
        result = self.chunker.chunk_fixed(text, "doc", cfg)
        assert len(result) >= 3

    def test_overlap_shared_words(self):
        text = " ".join(str(i) for i in range(15))
        cfg = ChunkConfig(target_size=6, min_size=1, max_size=20, overlap=2)
        result = self.chunker.chunk_fixed(text, "doc", cfg)
        # The last words of chunk N should appear at the start of chunk N+1
        words0 = result[0].text.split()
        words1 = result[1].text.split()
        assert words0[-2:] == words1[:2]

    def test_chunk_type_is_fixed(self):
        text = "a b c d e f g h i j"
        cfg = ChunkConfig(target_size=5, min_size=1, max_size=20)
        result = self.chunker.chunk_fixed(text, "doc", cfg)
        assert all(c.chunk_type == ChunkType.FIXED for c in result)

    def test_doc_id(self):
        text = "a b c d e f"
        cfg = ChunkConfig(target_size=3, min_size=1, max_size=10)
        result = self.chunker.chunk_fixed(text, "xyz", cfg)
        assert all(c.doc_id == "xyz" for c in result)

    def test_single_word(self):
        result = self.chunker.chunk_fixed("hello", "doc", ChunkConfig(target_size=5))
        assert len(result) == 1
        assert result[0].text == "hello"


# ===========================================================================
# AdaptiveChunker.chunk_sentences
# ===========================================================================

class TestChunkSentences:
    def setup_method(self):
        self.chunker = AdaptiveChunker()

    def test_empty_text(self):
        assert self.chunker.chunk_sentences("", "doc") == []

    def test_single_sentence(self):
        text = "This is a single sentence."
        result = self.chunker.chunk_sentences(text, "doc", ChunkConfig(target_size=20))
        assert len(result) == 1

    def test_sentences_grouped(self):
        # 10 sentences of ~5 words each = ~50 words total
        sentences = ["This is sentence {0}.".format(i) for i in range(10)]
        text = " ".join(sentences)
        cfg = ChunkConfig(target_size=15, min_size=1, max_size=100)
        result = self.chunker.chunk_sentences(text, "doc", cfg)
        assert len(result) >= 2

    def test_chunk_type_is_sentence(self):
        text = "First sentence. Second sentence. Third sentence."
        cfg = ChunkConfig(target_size=10, min_size=1, max_size=50)
        result = self.chunker.chunk_sentences(text, "doc", cfg)
        assert all(c.chunk_type == ChunkType.SENTENCE for c in result)

    def test_doc_id_propagated(self):
        text = "First sentence. Second sentence."
        result = self.chunker.chunk_sentences(text, "myid", ChunkConfig(target_size=5))
        assert all(c.doc_id == "myid" for c in result)

    def test_exclamation_boundary(self):
        text = "Great! Really great! Wonderful!"
        cfg = ChunkConfig(target_size=2, min_size=1, max_size=10)
        result = self.chunker.chunk_sentences(text, "doc", cfg)
        assert len(result) >= 1

    def test_question_boundary(self):
        text = "What is this? Is it good? Maybe yes?"
        cfg = ChunkConfig(target_size=3, min_size=1, max_size=20)
        result = self.chunker.chunk_sentences(text, "doc", cfg)
        assert len(result) >= 1

    def test_all_text_preserved(self):
        sentences = ["Word{0} sentence number here.".format(i) for i in range(6)]
        text = " ".join(sentences)
        cfg = ChunkConfig(target_size=10, min_size=1, max_size=50)
        result = self.chunker.chunk_sentences(text, "doc", cfg)
        combined = " ".join(c.text for c in result)
        for word in text.split():
            assert word in combined


# ===========================================================================
# StrategySelector
# ===========================================================================

class TestStrategySelector:
    def setup_method(self):
        self.selector = StrategySelector()

    def test_heading_count_zero(self):
        assert self.selector.heading_count("No headings here.") == 0

    def test_heading_count_one(self):
        text = "# Title\n\nContent"
        assert self.selector.heading_count(text) == 1

    def test_heading_count_multiple(self):
        text = "# H1\n## H2\n### H3\nContent"
        assert self.selector.heading_count(text) == 3

    def test_heading_count_non_heading_hash(self):
        text = "This is not a #heading because no space after."
        # Lines starting with # followed by a space are headings
        assert self.selector.heading_count(text) == 0

    def test_avg_paragraph_words_empty(self):
        assert self.selector.avg_paragraph_words("") == 0.0

    def test_avg_paragraph_words_single(self):
        text = "one two three four five"
        assert self.selector.avg_paragraph_words(text) == 5.0

    def test_avg_paragraph_words_two_paragraphs(self):
        text = "one two\n\nthree four five six"
        # paragraph 1: 2 words, paragraph 2: 4 words → avg = 3.0
        assert self.selector.avg_paragraph_words(text) == 3.0

    def test_sentence_count_zero(self):
        assert self.selector.sentence_count("no punctuation") == 0

    def test_sentence_count_basic(self):
        text = "First sentence. Second sentence. Third sentence."
        assert self.selector.sentence_count(text) == 3

    def test_sentence_count_mixed(self):
        text = "Is it? Yes! Sure."
        assert self.selector.sentence_count(text) == 3

    def test_select_heading(self):
        text = "# Title\n\nSome content here."
        assert self.selector.select(text) == ChunkingStrategy.HEADING

    def test_select_fixed_for_long_paragraphs(self):
        # One paragraph with > 200 words, no headings
        text = " ".join(["word"] * 210)
        assert self.selector.select(text) == ChunkingStrategy.FIXED

    def test_select_sentence_for_many_sentences(self):
        # > 20 sentences, no headings, short paragraphs
        sentences = ["Short sentence here." for _ in range(25)]
        text = " ".join(sentences)
        assert self.selector.select(text) == ChunkingStrategy.SENTENCE

    def test_select_paragraph_fallback(self):
        # Short text with few sentences, no headings
        text = "Short para. Another short para."
        assert self.selector.select(text) == ChunkingStrategy.PARAGRAPH

    def test_select_heading_takes_priority_over_long_paragraphs(self):
        # Text has heading AND long paragraphs → HEADING wins
        long_content = " ".join(["word"] * 250)
        text = "# Title\n\n" + long_content
        assert self.selector.select(text) == ChunkingStrategy.HEADING

    def test_select_heading_takes_priority_over_many_sentences(self):
        sentences = ["Sentence here. " for _ in range(25)]
        text = "# Title\n\n" + "".join(sentences)
        assert self.selector.select(text) == ChunkingStrategy.HEADING

    def test_chunking_strategy_values(self):
        assert ChunkingStrategy.AUTO.value == "auto"
        assert ChunkingStrategy.PARAGRAPH.value == "paragraph"
        assert ChunkingStrategy.HEADING.value == "heading"
        assert ChunkingStrategy.FIXED.value == "fixed"
        assert ChunkingStrategy.SENTENCE.value == "sentence"
