"""Tests for the E31 multi-modal metadata module."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.multimodal_meta import (
    AssetMetadata,
    AssetPattern,
    AssetType,
    MetadataExtractor,
    MultiModalIndex,
)


# ---------------------------------------------------------------------------
# AssetType
# ---------------------------------------------------------------------------

class TestAssetType:
    def test_all_members_exist(self):
        expected = {"TEXT", "IMAGE", "TABLE", "CODE", "DIAGRAM", "AUDIO", "VIDEO", "UNKNOWN"}
        assert {m.name for m in AssetType} == expected

    def test_values_are_lowercase_strings(self):
        for member in AssetType:
            assert isinstance(member.value, str)
            assert member.value == member.value.lower()

    def test_lookup_by_value(self):
        assert AssetType("image") is AssetType.IMAGE
        assert AssetType("video") is AssetType.VIDEO


# ---------------------------------------------------------------------------
# AssetMetadata — basic construction
# ---------------------------------------------------------------------------

class TestAssetMetadataConstruction:
    def test_required_fields(self):
        a = AssetMetadata(source_doc="doc.md", asset_type=AssetType.TEXT)
        assert a.source_doc == "doc.md"
        assert a.asset_type == AssetType.TEXT

    def test_auto_asset_id_generated(self):
        a = AssetMetadata(source_doc="x.md", asset_type=AssetType.IMAGE)
        assert isinstance(a.asset_id, str)
        assert len(a.asset_id) == 8

    def test_auto_asset_id_unique(self):
        ids = {AssetMetadata(source_doc="x", asset_type=AssetType.TEXT).asset_id for _ in range(50)}
        assert len(ids) == 50

    def test_created_ts_auto(self):
        before = time.time()
        a = AssetMetadata(source_doc="x", asset_type=AssetType.CODE)
        after = time.time()
        assert before <= a.created_ts <= after

    def test_defaults(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.UNKNOWN)
        assert a.mime_type == ""
        assert a.width == 0
        assert a.height == 0
        assert a.duration_sec == 0.0
        assert a.language == ""
        assert a.alt_text == ""
        assert a.caption == ""
        assert a.tags == []

    def test_tags_independent_instances(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.TEXT)
        b = AssetMetadata(source_doc="d", asset_type=AssetType.TEXT)
        a.tags.append("foo")
        assert b.tags == []

    def test_explicit_values(self):
        a = AssetMetadata(
            source_doc="report.md",
            asset_type=AssetType.VIDEO,
            mime_type="video/mp4",
            width=1920,
            height=1080,
            duration_sec=120.5,
            alt_text="Demo video",
            caption="Figure 1",
            tags=["demo", "intro"],
        )
        assert a.mime_type == "video/mp4"
        assert a.width == 1920
        assert a.height == 1080
        assert a.duration_sec == 120.5
        assert a.alt_text == "Demo video"
        assert a.caption == "Figure 1"
        assert a.tags == ["demo", "intro"]


# ---------------------------------------------------------------------------
# AssetMetadata — is_visual
# ---------------------------------------------------------------------------

class TestIsVisual:
    def test_image_is_visual(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE)
        assert a.is_visual() is True

    def test_diagram_is_visual(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.DIAGRAM)
        assert a.is_visual() is True

    def test_text_not_visual(self):
        assert AssetMetadata(source_doc="d", asset_type=AssetType.TEXT).is_visual() is False

    def test_audio_not_visual(self):
        assert AssetMetadata(source_doc="d", asset_type=AssetType.AUDIO).is_visual() is False

    def test_video_not_visual(self):
        assert AssetMetadata(source_doc="d", asset_type=AssetType.VIDEO).is_visual() is False

    def test_table_not_visual(self):
        assert AssetMetadata(source_doc="d", asset_type=AssetType.TABLE).is_visual() is False

    def test_code_not_visual(self):
        assert AssetMetadata(source_doc="d", asset_type=AssetType.CODE).is_visual() is False


# ---------------------------------------------------------------------------
# AssetMetadata — is_temporal
# ---------------------------------------------------------------------------

class TestIsTemporal:
    def test_audio_is_temporal(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.AUDIO)
        assert a.is_temporal() is True

    def test_video_is_temporal(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.VIDEO)
        assert a.is_temporal() is True

    def test_image_not_temporal(self):
        assert AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE).is_temporal() is False

    def test_text_not_temporal(self):
        assert AssetMetadata(source_doc="d", asset_type=AssetType.TEXT).is_temporal() is False

    def test_diagram_not_temporal(self):
        assert AssetMetadata(source_doc="d", asset_type=AssetType.DIAGRAM).is_temporal() is False


# ---------------------------------------------------------------------------
# AssetMetadata — word_count
# ---------------------------------------------------------------------------

class TestWordCount:
    def test_empty_returns_zero(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE)
        assert a.word_count() == 0

    def test_alt_only(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE, alt_text="a photo of a cat")
        assert a.word_count() == 5

    def test_caption_only(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE, caption="Figure 1: results")
        assert a.word_count() == 3

    def test_both_combined(self):
        a = AssetMetadata(
            source_doc="d",
            asset_type=AssetType.IMAGE,
            alt_text="screenshot",
            caption="main result",
        )
        assert a.word_count() == 3  # 1 + 2

    def test_whitespace_only_not_counted(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE, alt_text="  ", caption="  ")
        assert a.word_count() == 0

    def test_single_word_each(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE, alt_text="logo", caption="caption")
        assert a.word_count() == 2


# ---------------------------------------------------------------------------
# AssetPattern
# ---------------------------------------------------------------------------

class TestAssetPattern:
    def test_construction(self):
        p = AssetPattern(
            pattern=r"!\[([^\]]*)\]\(([^)]+)\)",
            asset_type=AssetType.IMAGE,
            mime_type="image/png",
        )
        assert p.pattern.startswith("!")
        assert p.asset_type is AssetType.IMAGE
        assert p.mime_type == "image/png"


# ---------------------------------------------------------------------------
# MetadataExtractor — Markdown images
# ---------------------------------------------------------------------------

class TestExtractMarkdownImages:
    def setup_method(self):
        self.ext = MetadataExtractor()

    def test_single_png_image(self):
        text = "![A cat](images/cat.png)"
        assets = self.ext.extract(text, "doc.md")
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert len(imgs) == 1
        assert imgs[0].alt_text == "A cat"
        assert imgs[0].mime_type == "image/png"
        assert imgs[0].source_doc == "doc.md"

    def test_jpg_image(self):
        text = "![Photo](photo.jpg)"
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert imgs[0].mime_type == "image/jpeg"

    def test_jpeg_image(self):
        text = "![Photo](photo.jpeg)"
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert imgs[0].mime_type == "image/jpeg"

    def test_gif_image(self):
        text = "![Animation](anim.gif)"
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert imgs[0].mime_type == "image/gif"

    def test_svg_image(self):
        text = "![Diagram](fig.svg)"
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert imgs[0].mime_type == "image/svg+xml"

    def test_unknown_extension(self):
        text = "![Doc](file.bmp)"
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert len(imgs) == 1  # still detected as image
        # mime may be empty or something, not strictly checked

    def test_empty_alt_text(self):
        text = "![](logo.png)"
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert len(imgs) == 1
        assert imgs[0].alt_text == ""

    def test_multiple_images(self):
        text = "![A](a.png) some text ![B](b.jpg)"
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert len(imgs) == 2

    def test_no_images_returns_empty_list_for_images(self):
        text = "Just plain text with no images."
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert imgs == []


# ---------------------------------------------------------------------------
# MetadataExtractor — code blocks
# ---------------------------------------------------------------------------

class TestExtractCodeBlocks:
    def setup_method(self):
        self.ext = MetadataExtractor()

    def test_python_code_block(self):
        text = "```python\nprint('hi')\n```"
        assets = self.ext.extract(text)
        code = [a for a in assets if a.asset_type == AssetType.CODE]
        assert len(code) == 1
        assert code[0].language == "python"

    def test_plain_code_block_no_lang(self):
        text = "```\nsome code\n```"
        assets = self.ext.extract(text)
        code = [a for a in assets if a.asset_type == AssetType.CODE]
        assert len(code) == 1
        assert code[0].language == ""

    def test_javascript_code_block(self):
        text = "```javascript\nconsole.log('x');\n```"
        assets = self.ext.extract(text)
        code = [a for a in assets if a.asset_type == AssetType.CODE]
        assert code[0].language == "javascript"

    def test_tilde_fence(self):
        text = "~~~bash\necho hi\n~~~"
        assets = self.ext.extract(text)
        code = [a for a in assets if a.asset_type == AssetType.CODE]
        assert len(code) == 1
        assert code[0].language == "bash"

    def test_multiple_code_blocks(self):
        text = "```python\nx=1\n```\ntext\n```js\ny=2\n```"
        assets = self.ext.extract(text)
        code = [a for a in assets if a.asset_type == AssetType.CODE]
        assert len(code) == 2

    def test_code_block_source_doc(self):
        text = "```go\nfmt.Println()\n```"
        assets = self.ext.extract(text, "readme.md")
        code = [a for a in assets if a.asset_type == AssetType.CODE]
        assert code[0].source_doc == "readme.md"


# ---------------------------------------------------------------------------
# MetadataExtractor — HTML tags
# ---------------------------------------------------------------------------

class TestExtractHTMLTags:
    def setup_method(self):
        self.ext = MetadataExtractor()

    def test_html_img_tag(self):
        text = '<img src="photo.jpg" alt="A photo">'
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert len(imgs) == 1
        assert imgs[0].alt_text == "A photo"

    def test_html_img_no_alt(self):
        text = '<img src="photo.jpg">'
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        assert len(imgs) == 1
        assert imgs[0].alt_text == ""

    def test_html_table_tag(self):
        text = "<table>\n<tr><td>data</td></tr>\n</table>"
        assets = self.ext.extract(text)
        tables = [a for a in assets if a.asset_type == AssetType.TABLE]
        assert len(tables) == 1

    def test_html_video_tag(self):
        text = '<video src="clip.mp4" controls>'
        assets = self.ext.extract(text)
        videos = [a for a in assets if a.asset_type == AssetType.VIDEO]
        assert len(videos) == 1

    def test_html_audio_tag(self):
        text = '<audio src="song.mp3" controls>'
        assets = self.ext.extract(text)
        audios = [a for a in assets if a.asset_type == AssetType.AUDIO]
        assert len(audios) == 1

    def test_mixed_html_and_markdown(self):
        text = '![alt](pic.png)\n<img src="x.jpg" alt="y">\n<table><tr><td>z</td></tr></table>'
        assets = self.ext.extract(text)
        imgs = [a for a in assets if a.asset_type == AssetType.IMAGE]
        tables = [a for a in assets if a.asset_type == AssetType.TABLE]
        assert len(imgs) == 2
        assert len(tables) == 1

    def test_case_insensitive_html(self):
        text = "<IMG SRC='x.png'><TABLE><VIDEO><AUDIO>"
        assets = self.ext.extract(text)
        types = {a.asset_type for a in assets}
        assert AssetType.IMAGE in types
        assert AssetType.TABLE in types
        assert AssetType.VIDEO in types
        assert AssetType.AUDIO in types


# ---------------------------------------------------------------------------
# MetadataExtractor — detect_tables
# ---------------------------------------------------------------------------

class TestDetectTables:
    def setup_method(self):
        self.ext = MetadataExtractor()

    def test_simple_markdown_table(self):
        text = (
            "| Name | Age |\n"
            "| ---- | --- |\n"
            "| Alice | 30 |\n"
        )
        tables = self.ext.detect_tables(text, "doc.md")
        assert len(tables) == 1
        assert tables[0].asset_type == AssetType.TABLE
        assert tables[0].mime_type == "text/markdown"
        assert tables[0].source_doc == "doc.md"

    def test_table_with_colon_separator(self):
        text = (
            "| Left | Center | Right |\n"
            "| :--- | :----: | ---: |\n"
            "| a    |   b    |    c |\n"
        )
        tables = self.ext.detect_tables(text)
        assert len(tables) == 1

    def test_multiple_tables(self):
        text = (
            "| A | B |\n"
            "| - | - |\n"
            "| 1 | 2 |\n"
            "\n"
            "Some text in between.\n"
            "\n"
            "| X | Y |\n"
            "| - | - |\n"
            "| 3 | 4 |\n"
        )
        tables = self.ext.detect_tables(text)
        assert len(tables) == 2

    def test_no_table(self):
        text = "Just regular text\nwithout any pipes.\n"
        tables = self.ext.detect_tables(text)
        assert tables == []

    def test_single_pipe_not_a_table(self):
        text = "Here is one | pipe character\nand another | one here\n"
        tables = self.ext.detect_tables(text)
        # Without a separator line this should not be detected as a table
        assert tables == []

    def test_empty_text(self):
        tables = self.ext.detect_tables("")
        assert tables == []


# ---------------------------------------------------------------------------
# MultiModalIndex — add / get
# ---------------------------------------------------------------------------

class TestIndexAddGet:
    def setup_method(self):
        self.idx = MultiModalIndex()

    def test_add_and_get(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE)
        self.idx.add(a)
        assert self.idx.get(a.asset_id) is a

    def test_get_missing_returns_none(self):
        assert self.idx.get("nonexistent") is None

    def test_overwrite_same_id(self):
        a = AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE)
        orig_id = a.asset_id
        self.idx.add(a)
        b = AssetMetadata(source_doc="other", asset_type=AssetType.CODE)
        # Force same id for overwrite test
        b.asset_id = orig_id  # type: ignore[misc]
        self.idx.add(b)
        assert self.idx.get(orig_id) is b

    def test_asset_count_zero(self):
        assert self.idx.asset_count() == 0

    def test_asset_count_increments(self):
        for _ in range(5):
            self.idx.add(AssetMetadata(source_doc="d", asset_type=AssetType.TEXT))
        assert self.idx.asset_count() == 5


# ---------------------------------------------------------------------------
# MultiModalIndex — by_type / by_doc
# ---------------------------------------------------------------------------

class TestIndexFilters:
    def setup_method(self):
        self.idx = MultiModalIndex()
        for t in (AssetType.IMAGE, AssetType.IMAGE, AssetType.CODE, AssetType.TABLE):
            self.idx.add(AssetMetadata(source_doc="doc_a.md", asset_type=t))
        self.idx.add(AssetMetadata(source_doc="doc_b.md", asset_type=AssetType.VIDEO))

    def test_by_type_image(self):
        results = self.idx.by_type(AssetType.IMAGE)
        assert len(results) == 2
        assert all(a.asset_type == AssetType.IMAGE for a in results)

    def test_by_type_no_match(self):
        assert self.idx.by_type(AssetType.AUDIO) == []

    def test_by_doc_a(self):
        results = self.idx.by_doc("doc_a.md")
        assert len(results) == 4

    def test_by_doc_b(self):
        results = self.idx.by_doc("doc_b.md")
        assert len(results) == 1
        assert results[0].asset_type == AssetType.VIDEO

    def test_by_doc_missing(self):
        assert self.idx.by_doc("unknown.md") == []


# ---------------------------------------------------------------------------
# MultiModalIndex — search_by_tag
# ---------------------------------------------------------------------------

class TestIndexSearchByTag:
    def setup_method(self):
        self.idx = MultiModalIndex()
        a = AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE, tags=["Python", "Tutorial"])
        b = AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE, tags=["python", "intro"])
        c = AssetMetadata(source_doc="d", asset_type=AssetType.CODE, tags=["Rust"])
        self.idx.add(a)
        self.idx.add(b)
        self.idx.add(c)

    def test_case_insensitive_match(self):
        results = self.idx.search_by_tag("python")
        assert len(results) == 2

    def test_case_insensitive_upper(self):
        results = self.idx.search_by_tag("PYTHON")
        assert len(results) == 2

    def test_exact_tag_match(self):
        results = self.idx.search_by_tag("Rust")
        assert len(results) == 1

    def test_no_match(self):
        results = self.idx.search_by_tag("golang")
        assert results == []

    def test_partial_tag_no_match(self):
        # "py" should not match "python"
        results = self.idx.search_by_tag("py")
        assert results == []


# ---------------------------------------------------------------------------
# MultiModalIndex — search_by_text
# ---------------------------------------------------------------------------

class TestIndexSearchByText:
    def setup_method(self):
        self.idx = MultiModalIndex()
        self.idx.add(AssetMetadata(
            source_doc="d", asset_type=AssetType.IMAGE,
            alt_text="a beautiful sunset over the ocean",
            caption="Figure 1: coastal scenery",
        ))
        self.idx.add(AssetMetadata(
            source_doc="d", asset_type=AssetType.IMAGE,
            alt_text="mountain landscape",
            caption="Figure 2: alpine meadow",
        ))
        self.idx.add(AssetMetadata(
            source_doc="d", asset_type=AssetType.CODE,
            language="python",
        ))

    def test_single_token_match(self):
        results = self.idx.search_by_text("sunset")
        assert len(results) == 1
        assert results[0].alt_text == "a beautiful sunset over the ocean"

    def test_multi_token_match(self):
        results = self.idx.search_by_text("Figure alpine")
        assert len(results) == 1
        assert "mountain" in results[0].alt_text

    def test_case_insensitive(self):
        results = self.idx.search_by_text("SUNSET")
        assert len(results) == 1

    def test_no_match(self):
        results = self.idx.search_by_text("desert")
        assert results == []

    def test_empty_query_returns_all(self):
        results = self.idx.search_by_text("")
        assert len(results) == 3

    def test_partial_word_not_required(self):
        # "ocean" is in alt_text; "scenic" is not → no match
        results = self.idx.search_by_text("ocean scenic")
        assert len(results) == 0


# ---------------------------------------------------------------------------
# MultiModalIndex — stats
# ---------------------------------------------------------------------------

class TestIndexStats:
    def test_empty_stats(self):
        idx = MultiModalIndex()
        s = idx.stats()
        assert s["total"] == 0
        assert s["by_type"] == {}

    def test_stats_counts(self):
        idx = MultiModalIndex()
        for _ in range(3):
            idx.add(AssetMetadata(source_doc="d", asset_type=AssetType.IMAGE))
        for _ in range(2):
            idx.add(AssetMetadata(source_doc="d", asset_type=AssetType.CODE))
        s = idx.stats()
        assert s["total"] == 5
        assert s["by_type"]["image"] == 3
        assert s["by_type"]["code"] == 2
        assert "table" not in s["by_type"]

    def test_stats_keys(self):
        idx = MultiModalIndex()
        idx.add(AssetMetadata(source_doc="d", asset_type=AssetType.AUDIO))
        s = idx.stats()
        assert "total" in s
        assert "by_type" in s


# ---------------------------------------------------------------------------
# Integration: extractor + index
# ---------------------------------------------------------------------------

class TestIntegration:
    def test_extract_and_index_pipeline(self):
        text = (
            "# My Document\n\n"
            "![Logo](logo.png)\n\n"
            "```python\nprint('hello')\n```\n\n"
            "| Col1 | Col2 |\n"
            "| ---- | ---- |\n"
            "| a    | b    |\n\n"
            "<audio src='bg.mp3'>\n"
        )
        ext = MetadataExtractor()
        idx = MultiModalIndex()

        assets = ext.extract(text, "guide.md")
        tables = ext.detect_tables(text, "guide.md")
        for a in assets + tables:
            idx.add(a)

        assert idx.asset_count() >= 3  # image + code + audio (+ markdown table from detect_tables)
        assert len(idx.by_type(AssetType.IMAGE)) >= 1
        assert len(idx.by_type(AssetType.CODE)) >= 1
        assert len(idx.by_type(AssetType.AUDIO)) >= 1
        # The markdown table is found via detect_tables
        assert len(idx.by_type(AssetType.TABLE)) >= 1

    def test_doc_id_propagated(self):
        text = "![img](x.png)\n```py\npass\n```"
        ext = MetadataExtractor()
        assets = ext.extract(text, "specific_doc.md")
        assert all(a.source_doc == "specific_doc.md" for a in assets)
