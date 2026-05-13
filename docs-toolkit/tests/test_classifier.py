"""Tests for docstoolkit.classifier (TF-IDF centroid-based section classifier)."""
import json
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.classifier import ClassificationResult, TfidfClassifier


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

SPORTS_DOCS = [
    "football soccer players team match goal penalty",
    "basketball court dribble slam dunk players team",
    "tennis racket serve volley court match players",
    "football players team training stadium scoring",
]

COOKING_DOCS = [
    "recipe ingredients flour butter sugar bake oven",
    "pasta sauce tomato garlic cook boil simmer recipe",
    "bread dough yeast flour baking oven temperature",
    "recipe butter eggs sugar cream bake dessert cake",
]

TECH_DOCS = [
    "python programming code function class module library",
    "database sql query table index schema migration",
    "docker container image kubernetes deployment cluster",
    "python code algorithm runtime function recursive",
]

SMALL_CORPUS = {
    "sports": SPORTS_DOCS,
    "cooking": COOKING_DOCS,
    "tech": TECH_DOCS,
}


def make_classifier(min_docs: int = 3) -> TfidfClassifier:
    clf = TfidfClassifier(min_docs_per_section=min_docs)
    clf.fit(SMALL_CORPUS)
    return clf


# ---------------------------------------------------------------------------
# S3-1  Imports
# ---------------------------------------------------------------------------

def test_imports():
    assert TfidfClassifier is not None
    assert ClassificationResult is not None


# ---------------------------------------------------------------------------
# S3-2  ClassificationResult dataclass fields
# ---------------------------------------------------------------------------

def test_classification_result_fields():
    r = ClassificationResult(
        suggested_section="sports",
        confidence=0.9,
        alternatives=[("cooking", 0.1)],
        top_terms=["football", "players"],
    )
    assert r.suggested_section == "sports"
    assert r.confidence == 0.9
    assert r.alternatives == [("cooking", 0.1)]
    assert r.top_terms == ["football", "players"]


def test_classification_result_defaults():
    r = ClassificationResult(suggested_section="x", confidence=0.5)
    assert r.alternatives == []
    assert r.top_terms == []


# ---------------------------------------------------------------------------
# S3-3  fit / basic classification
# ---------------------------------------------------------------------------

def test_fit_succeeds():
    clf = make_classifier()
    assert clf._fitted is True
    assert len(clf._centroids) == 3


def test_fit_skips_small_sections():
    corpus = {
        "big": ["doc one word", "doc two word", "doc three word"],
        "small": ["only one doc here"],  # < min_docs=3 → skipped
    }
    clf = TfidfClassifier(min_docs_per_section=3)
    clf.fit(corpus)
    assert "small" not in clf._centroids
    assert "big" in clf._centroids


def test_fit_raises_if_no_valid_sections():
    with pytest.raises(ValueError):
        TfidfClassifier(min_docs_per_section=10).fit({"x": ["a", "b"]})


# ---------------------------------------------------------------------------
# S3-4  classify returns correct section
# ---------------------------------------------------------------------------

def test_classify_sports():
    clf = make_classifier()
    result = clf.classify("football team players match goal penalty kick")
    assert result.suggested_section == "sports"


def test_classify_cooking():
    clf = make_classifier()
    result = clf.classify("recipe ingredients bake oven butter sugar flour cake")
    assert result.suggested_section == "cooking"


def test_classify_tech():
    clf = make_classifier()
    result = clf.classify("python programming code function class module")
    assert result.suggested_section == "tech"


# ---------------------------------------------------------------------------
# S3-5  confidence
# ---------------------------------------------------------------------------

def test_confidence_range():
    clf = make_classifier()
    result = clf.classify("football team match players penalty goal")
    assert 0.0 <= result.confidence <= 1.0


def test_confidence_higher_for_clear_doc():
    clf = make_classifier()
    clear = clf.classify(
        "football soccer match goal penalty kick players team stadium"
    )
    ambiguous = clf.classify("the quick brown fox")
    assert clear.confidence >= ambiguous.confidence


# ---------------------------------------------------------------------------
# S3-6  alternatives sorted descending
# ---------------------------------------------------------------------------

def test_alternatives_sorted_descending():
    clf = make_classifier()
    result = clf.classify("football players goal penalty kick team match")
    # alternatives should be sorted high → low
    scores = [s for _, s in result.alternatives]
    assert scores == sorted(scores, reverse=True)


def test_alternatives_do_not_include_best():
    clf = make_classifier()
    result = clf.classify("python code function class module library")
    alt_sections = [s for s, _ in result.alternatives]
    assert result.suggested_section not in alt_sections


def test_alternatives_count():
    clf = make_classifier()
    result = clf.classify("something something something")
    # 3 sections total → 2 alternatives
    assert len(result.alternatives) == 2


# ---------------------------------------------------------------------------
# S3-7  top_terms
# ---------------------------------------------------------------------------

def test_top_terms_non_empty_for_matching_doc():
    clf = make_classifier()
    result = clf.classify("football players match goal team penalty")
    assert len(result.top_terms) > 0


def test_top_terms_are_strings():
    clf = make_classifier()
    result = clf.classify("recipe bake oven butter sugar flour cake")
    assert all(isinstance(t, str) for t in result.top_terms)


# ---------------------------------------------------------------------------
# S3-8  explain
# ---------------------------------------------------------------------------

def test_explain_returns_per_section():
    clf = make_classifier()
    explanation = clf.explain("football players match goal team")
    assert set(explanation.keys()) == {"sports", "cooking", "tech"}


def test_explain_top5_per_section():
    clf = make_classifier()
    explanation = clf.explain("football players match goal team")
    for section, terms in explanation.items():
        assert len(terms) <= 5


def test_explain_term_score_pairs():
    clf = make_classifier()
    explanation = clf.explain("python code function class")
    for section, terms in explanation.items():
        for term, score in terms:
            assert isinstance(term, str)
            assert isinstance(score, float)


def test_explain_scores_non_negative():
    clf = make_classifier()
    explanation = clf.explain("recipe flour butter sugar bake")
    for section, terms in explanation.items():
        for _, score in terms:
            assert score >= 0.0


# ---------------------------------------------------------------------------
# S3-9  save / load roundtrip
# ---------------------------------------------------------------------------

def test_save_load_roundtrip(tmp_path):
    clf = make_classifier()
    save_path = tmp_path / "model.json"
    clf.save(save_path)
    assert save_path.exists()

    clf2 = TfidfClassifier()
    clf2.load(save_path)

    result1 = clf.classify("football players match goal team")
    result2 = clf2.classify("football players match goal team")
    assert result1.suggested_section == result2.suggested_section
    assert result1.confidence == pytest.approx(result2.confidence, abs=1e-9)


def test_save_creates_valid_json(tmp_path):
    clf = make_classifier()
    path = tmp_path / "model.json"
    clf.save(path)
    data = json.loads(path.read_text())
    assert "idf" in data
    assert "centroids" in data


def test_load_restores_fitted_flag(tmp_path):
    clf = make_classifier()
    path = tmp_path / "model.json"
    clf.save(path)

    clf2 = TfidfClassifier()
    assert clf2._fitted is False
    clf2.load(path)
    assert clf2._fitted is True


def test_load_preserves_classifications(tmp_path):
    clf = make_classifier()
    path = tmp_path / "model.json"
    clf.save(path)

    clf2 = TfidfClassifier()
    clf2.load(path)

    for text in [
        "recipe bake oven butter",
        "python code function class",
        "football players match goal",
    ]:
        assert clf.classify(text).suggested_section == clf2.classify(text).suggested_section


# ---------------------------------------------------------------------------
# S3-10  fit_from_docs_dir
# ---------------------------------------------------------------------------

def test_fit_from_docs_dir(tmp_path):
    # Create a mini docs directory
    for section in ("section-a", "section-b", "section-c"):
        sec_dir = tmp_path / section
        sec_dir.mkdir()
        for i in range(4):
            content = " ".join([section.replace("-", " ")] * 30 + [f"word{i}"] * 5)
            (sec_dir / f"doc{i}.md").write_text(content)

    clf = TfidfClassifier.fit_from_docs_dir(tmp_path, min_docs_per_section=3)
    assert clf._fitted
    assert len(clf._centroids) == 3


def test_fit_from_docs_dir_skips_root_files(tmp_path):
    # Root-level md files go to __root__ section
    (tmp_path / "root.md").write_text("standalone root document")
    for i in range(4):
        (tmp_path / "sec-a").mkdir(exist_ok=True)
        (tmp_path / "sec-a" / f"doc{i}.md").write_text(f"section alpha text document {i}")

    clf = TfidfClassifier.fit_from_docs_dir(tmp_path, min_docs_per_section=4)
    assert "sec-a" in clf._centroids


# ---------------------------------------------------------------------------
# S3-11  classify raises before fit
# ---------------------------------------------------------------------------

def test_classify_raises_before_fit():
    clf = TfidfClassifier()
    with pytest.raises(RuntimeError):
        clf.classify("anything")


def test_explain_raises_before_fit():
    clf = TfidfClassifier()
    with pytest.raises(RuntimeError):
        clf.explain("anything")
