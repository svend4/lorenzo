"""Tests for cross-modal grounding: ImageRef, GroundedImage, ImageIndex."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.ingest.grounding import (
    ImageRef,
    GroundedImage,
    extract_image_refs,
    ground_image,
    ground_document,
    ImageIndex,
)


# ---- extract_image_refs ----

def test_extract_single_image():
    md = "Some text before. ![diagram](images/diagram.png) Some text after."
    refs = extract_image_refs(md, doc_id="doc1")
    assert len(refs) == 1
    ref = refs[0]
    assert ref.path == "images/diagram.png"
    assert ref.alt_text == "diagram"
    assert ref.doc_id == "doc1"


def test_extract_no_images():
    md = "No images here, just text."
    refs = extract_image_refs(md, doc_id="doc1")
    assert refs == []


def test_extract_multiple_images():
    md = "![img1](a.png) text ![img2](b.jpg) more ![img3](c.gif)"
    refs = extract_image_refs(md, doc_id="doc2")
    assert len(refs) == 3
    paths = [r.path for r in refs]
    assert "a.png" in paths
    assert "b.jpg" in paths
    assert "c.gif" in paths


def test_extract_context_before_captured():
    prefix = "A" * 150  # more than 100 chars
    md = f"{prefix}![alt](img.png)"
    refs = extract_image_refs(md, doc_id="d")
    assert len(refs) == 1
    # context_before should be at most 100 chars
    assert len(refs[0].context_before) <= 100
    assert refs[0].context_before == prefix[-100:]


def test_extract_context_after_captured():
    suffix = "B" * 150
    md = f"![alt](img.png){suffix}"
    refs = extract_image_refs(md, doc_id="d")
    assert len(refs) == 1
    assert len(refs[0].context_after) <= 100
    assert refs[0].context_after == suffix[:100]


def test_extract_empty_alt_text():
    md = "![](no_alt.png)"
    refs = extract_image_refs(md, doc_id="d")
    assert len(refs) == 1
    assert refs[0].alt_text == ""


def test_extract_context_at_document_boundaries():
    md = "![first](a.png) middle ![last](b.png)"
    refs = extract_image_refs(md, doc_id="d")
    # First image has no real prefix
    assert refs[0].context_before == ""
    # Last image has no real suffix (only empty or < 100 chars)
    assert len(refs[-1].context_after) <= 100


# ---- ground_image ----

def test_ground_image_synthetic_text_contains_parts():
    ref = ImageRef(
        path="arch.png",
        alt_text="architecture diagram",
        caption="System overview",
        context_before="See the architecture",
        context_after="for more details",
        doc_id="doc1",
    )
    gi = ground_image(ref)
    assert "architecture diagram" in gi.synthetic_text
    assert "System overview" in gi.synthetic_text
    assert "See the architecture" in gi.synthetic_text
    assert "for more details" in gi.synthetic_text


def test_ground_image_keywords_extracted():
    ref = ImageRef(
        path="memory.png",
        alt_text="memory architecture",
        caption="Memory subsystem",
        context_before="The memory module stores",
        context_after="and retrieves data efficiently",
        doc_id="doc1",
    )
    gi = ground_image(ref)
    assert isinstance(gi.keywords, list)
    assert len(gi.keywords) > 0
    kw_lower = [k.lower() for k in gi.keywords]
    assert "memory" in kw_lower or "architecture" in kw_lower


def test_ground_image_empty_fields():
    ref = ImageRef(
        path="empty.png",
        alt_text="",
        caption="",
        context_before="",
        context_after="",
        doc_id="doc1",
    )
    gi = ground_image(ref)
    # Should not raise; synthetic_text may be empty or whitespace
    assert isinstance(gi.synthetic_text, str)
    assert isinstance(gi.keywords, list)


def test_ground_image_keywords_no_stopwords():
    ref = ImageRef(
        path="x.png",
        alt_text="the and or",
        caption="in of with",
        context_before="",
        context_after="",
        doc_id="d",
    )
    gi = ground_image(ref)
    stopwords = {"the", "and", "or", "in", "of", "with"}
    for kw in gi.keywords:
        assert kw.lower() not in stopwords


# ---- ground_document ----

def test_ground_document_returns_grounded_images():
    md = "Intro ![fig1](f1.png) Middle ![fig2](f2.png) End"
    images = ground_document(md, doc_id="doc1")
    assert len(images) == 2
    assert all(isinstance(gi, GroundedImage) for gi in images)


def test_ground_document_empty():
    images = ground_document("No images", doc_id="doc1")
    assert images == []


# ---- ImageIndex ----

@pytest.fixture
def idx_with_data():
    idx = ImageIndex()
    for i, (alt, ctx_b, ctx_a) in enumerate([
        ("memory architecture", "persistent storage", "retrieval system"),
        ("agent workflow", "task scheduling", "execution engine"),
        ("knowledge graph", "concept nodes", "edge weights"),
    ]):
        ref = ImageRef(
            path=f"img{i}.png",
            alt_text=alt,
            caption="",
            context_before=ctx_b,
            context_after=ctx_a,
            doc_id=f"doc{i}",
        )
        gi = ground_image(ref)
        idx.add(gi)
    return idx


def test_image_index_search_returns_results(idx_with_data):
    results = idx_with_data.search("memory storage", top_k=2)
    assert len(results) <= 2
    assert all(isinstance(r, GroundedImage) for r in results)


def test_image_index_search_relevance(idx_with_data):
    results = idx_with_data.search("memory architecture", top_k=3)
    assert len(results) > 0
    # The memory-related image should be first
    assert "memory" in results[0].ref.alt_text.lower()


def test_image_index_search_no_match(idx_with_data):
    results = idx_with_data.search("zzz totally unrelated xyzzy", top_k=5)
    assert results == []


def test_image_index_empty_search():
    idx = ImageIndex()
    results = idx.search("anything", top_k=5)
    assert results == []


def test_image_index_save_load(tmp_path, idx_with_data):
    save_path = tmp_path / "index.json"
    idx_with_data.save(save_path)
    assert save_path.exists()

    idx2 = ImageIndex()
    idx2.load(save_path)
    assert len(idx2._images) == len(idx_with_data._images)

    # Verify data integrity
    orig_paths = {gi.ref.path for gi in idx_with_data._images}
    loaded_paths = {gi.ref.path for gi in idx2._images}
    assert orig_paths == loaded_paths


def test_image_index_save_load_roundtrip_search(tmp_path, idx_with_data):
    save_path = tmp_path / "idx.json"
    idx_with_data.save(save_path)

    idx2 = ImageIndex()
    idx2.load(save_path)
    results = idx2.search("memory", top_k=2)
    assert len(results) > 0


def test_image_index_to_passages(idx_with_data):
    from docstoolkit.rag.types import Passage
    passages = idx_with_data.to_passages()
    assert len(passages) == len(idx_with_data._images)
    for p in passages:
        assert isinstance(p, Passage)
        assert p.title.startswith("[image]")
        assert p.doc_id != ""
