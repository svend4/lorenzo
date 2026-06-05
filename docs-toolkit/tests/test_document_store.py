"""~90 tests for docstoolkit.document_store (E116)."""

import os
import tempfile
import threading
import time

import pytest

from docstoolkit.document_store import Document, DocumentStore


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def store():
    s = DocumentStore()
    yield s
    s.close()


@pytest.fixture
def clock():
    """Monotonically increasing virtual clock."""
    t = [0.0]

    def tick():
        t[0] += 1.0
        return t[0]

    return tick


@pytest.fixture
def tstore(clock):
    s = DocumentStore(now_fn=clock)
    yield s
    s.close()


# ── Document dataclass ────────────────────────────────────────────────────────

class TestDocumentDefaults:
    def test_doc_id_generated(self):
        d = Document()
        assert d.doc_id
        assert len(d.doc_id) == 12

    def test_doc_id_hex(self):
        d = Document()
        int(d.doc_id, 16)  # must be valid hex

    def test_default_collection(self):
        d = Document()
        assert d.collection == "default"

    def test_default_data_empty_dict(self):
        d = Document()
        assert d.data == {}

    def test_default_tags_empty_list(self):
        d = Document()
        assert d.tags == []

    def test_default_text_empty(self):
        d = Document()
        assert d.text == ""

    def test_default_timestamps_zero(self):
        d = Document()
        assert d.created_at == 0.0
        assert d.updated_at == 0.0

    def test_two_docs_have_different_ids(self):
        a, b = Document(), Document()
        assert a.doc_id != b.doc_id


# ── insert ────────────────────────────────────────────────────────────────────

class TestInsert:
    def test_returns_document(self, store):
        doc = store.insert("col", {"k": "v"})
        assert isinstance(doc, Document)

    def test_doc_id_is_set(self, store):
        doc = store.insert("col", {})
        assert doc.doc_id

    def test_collection_stored(self, store):
        doc = store.insert("mycol", {})
        assert doc.collection == "mycol"

    def test_data_stored(self, store):
        doc = store.insert("col", {"x": 42})
        assert doc.data == {"x": 42}

    def test_tags_stored(self, store):
        doc = store.insert("col", {}, tags=["a", "b"])
        assert doc.tags == ["a", "b"]

    def test_text_stored(self, store):
        doc = store.insert("col", {}, text="hello world")
        assert doc.text == "hello world"

    def test_created_at_set(self, store):
        doc = store.insert("col", {})
        assert doc.created_at > 0

    def test_updated_at_equals_created_at_on_insert(self, store):
        doc = store.insert("col", {})
        assert doc.updated_at == doc.created_at

    def test_no_tags_defaults_empty_list(self, store):
        doc = store.insert("col", {})
        assert doc.tags == []

    def test_arbitrary_nested_data(self, store):
        data = {"nested": {"list": [1, 2, 3], "flag": True, "score": 3.14}}
        doc = store.insert("col", data)
        assert doc.data == data

    def test_empty_string_collection(self, store):
        doc = store.insert("", {})
        assert doc.collection == ""


# ── get ───────────────────────────────────────────────────────────────────────

class TestGet:
    def test_get_returns_document(self, store):
        doc = store.insert("col", {"a": 1})
        fetched = store.get(doc.doc_id)
        assert isinstance(fetched, Document)

    def test_get_returns_correct_doc_id(self, store):
        doc = store.insert("col", {})
        assert store.get(doc.doc_id).doc_id == doc.doc_id

    def test_get_returns_correct_data(self, store):
        doc = store.insert("col", {"z": 99})
        assert store.get(doc.doc_id).data == {"z": 99}

    def test_get_returns_correct_tags(self, store):
        doc = store.insert("col", {}, tags=["x", "y"])
        assert store.get(doc.doc_id).tags == ["x", "y"]

    def test_get_missing_returns_none(self, store):
        assert store.get("nonexistent_id") is None

    def test_get_returns_none_after_delete(self, store):
        doc = store.insert("col", {})
        store.delete(doc.doc_id)
        assert store.get(doc.doc_id) is None


# ── update ────────────────────────────────────────────────────────────────────

class TestUpdate:
    def test_update_returns_document(self, store):
        doc = store.insert("col", {})
        result = store.update(doc.doc_id, data={"k": "v"})
        assert isinstance(result, Document)

    def test_update_missing_returns_none(self, store):
        assert store.update("ghost", data={"x": 1}) is None

    def test_update_data_only(self, store):
        doc = store.insert("col", {"old": True}, tags=["t"], text="original")
        store.update(doc.doc_id, data={"new": True})
        fetched = store.get(doc.doc_id)
        assert fetched.data == {"new": True}
        assert fetched.tags == ["t"]       # unchanged
        assert fetched.text == "original"  # unchanged

    def test_update_tags_only(self, store):
        doc = store.insert("col", {"k": 1}, tags=["old"], text="txt")
        store.update(doc.doc_id, tags=["new"])
        fetched = store.get(doc.doc_id)
        assert fetched.tags == ["new"]
        assert fetched.data == {"k": 1}    # unchanged
        assert fetched.text == "txt"       # unchanged

    def test_update_text_only(self, store):
        doc = store.insert("col", {"k": 1}, tags=["t"], text="old text")
        store.update(doc.doc_id, text="new text")
        fetched = store.get(doc.doc_id)
        assert fetched.text == "new text"
        assert fetched.data == {"k": 1}    # unchanged
        assert fetched.tags == ["t"]       # unchanged

    def test_update_all_fields(self, store):
        doc = store.insert("col", {"a": 1}, tags=["x"], text="old")
        store.update(doc.doc_id, data={"b": 2}, tags=["y"], text="new")
        fetched = store.get(doc.doc_id)
        assert fetched.data == {"b": 2}
        assert fetched.tags == ["y"]
        assert fetched.text == "new"

    def test_update_bumps_updated_at(self, tstore, clock):
        doc = tstore.insert("col", {})
        created = doc.created_at
        tstore.update(doc.doc_id, data={"x": 1})
        fetched = tstore.get(doc.doc_id)
        assert fetched.updated_at > created

    def test_update_preserves_created_at(self, tstore):
        doc = tstore.insert("col", {})
        original_created = doc.created_at
        tstore.update(doc.doc_id, data={"x": 1})
        fetched = tstore.get(doc.doc_id)
        assert fetched.created_at == original_created

    def test_update_clears_tags_to_empty(self, store):
        doc = store.insert("col", {}, tags=["a", "b"])
        store.update(doc.doc_id, tags=[])
        fetched = store.get(doc.doc_id)
        assert fetched.tags == []


# ── delete ────────────────────────────────────────────────────────────────────

class TestDelete:
    def test_delete_existing_returns_true(self, store):
        doc = store.insert("col", {})
        assert store.delete(doc.doc_id) is True

    def test_delete_missing_returns_false(self, store):
        assert store.delete("no_such_id") is False

    def test_deleted_doc_not_found(self, store):
        doc = store.insert("col", {})
        store.delete(doc.doc_id)
        assert store.get(doc.doc_id) is None

    def test_double_delete_returns_false(self, store):
        doc = store.insert("col", {})
        store.delete(doc.doc_id)
        assert store.delete(doc.doc_id) is False


# ── find – collection filter ──────────────────────────────────────────────────

class TestFindByCollection:
    def test_find_all_returns_all(self, store):
        store.insert("a", {})
        store.insert("b", {})
        assert len(store.find()) == 2

    def test_find_by_collection(self, store):
        store.insert("alpha", {})
        store.insert("beta", {})
        result = store.find(collection="alpha")
        assert len(result) == 1
        assert result[0].collection == "alpha"

    def test_find_wrong_collection_empty(self, store):
        store.insert("col", {})
        assert store.find(collection="other") == []

    def test_find_multiple_same_collection(self, store):
        for i in range(3):
            store.insert("same", {"i": i})
        assert len(store.find(collection="same")) == 3


# ── find – tag filter ─────────────────────────────────────────────────────────

class TestFindByTags:
    def test_find_single_tag(self, store):
        store.insert("col", {}, tags=["python"])
        store.insert("col", {}, tags=["rust"])
        result = store.find(tags=["python"])
        assert len(result) == 1
        assert "python" in result[0].tags

    def test_find_requires_all_tags(self, store):
        store.insert("col", {}, tags=["a", "b", "c"])
        store.insert("col", {}, tags=["a", "b"])
        result = store.find(tags=["a", "b", "c"])
        assert len(result) == 1

    def test_find_empty_tags_no_restriction(self, store):
        store.insert("col", {}, tags=["x"])
        store.insert("col", {}, tags=["y"])
        assert len(store.find(tags=[])) == 2

    def test_find_none_tags_no_restriction(self, store):
        store.insert("col", {}, tags=["x"])
        store.insert("col", {}, tags=["y"])
        assert len(store.find(tags=None)) == 2

    def test_find_nonexistent_tag_empty(self, store):
        store.insert("col", {}, tags=["a"])
        assert store.find(tags=["z"]) == []

    def test_find_tags_and_collection_combined(self, store):
        store.insert("col1", {}, tags=["t"])
        store.insert("col2", {}, tags=["t"])
        result = store.find(collection="col1", tags=["t"])
        assert len(result) == 1
        assert result[0].collection == "col1"


# ── find – text_query ─────────────────────────────────────────────────────────

class TestFindByTextQuery:
    def test_text_query_exact_substring(self, store):
        store.insert("col", {}, text="The quick brown fox")
        store.insert("col", {}, text="Hello world")
        result = store.find(text_query="quick")
        assert len(result) == 1

    def test_text_query_case_insensitive(self, store):
        store.insert("col", {}, text="Hello World")
        assert len(store.find(text_query="hello")) == 1
        assert len(store.find(text_query="WORLD")) == 1
        assert len(store.find(text_query="HeLLo WoRlD")) == 1

    def test_text_query_no_match_returns_empty(self, store):
        store.insert("col", {}, text="Nothing here")
        assert store.find(text_query="xyz") == []

    def test_text_query_combined_with_collection(self, store):
        store.insert("col1", {}, text="python rocks")
        store.insert("col2", {}, text="python rocks")
        result = store.find(collection="col1", text_query="python")
        assert len(result) == 1

    def test_text_query_combined_with_tags(self, store):
        store.insert("col", {}, tags=["go"], text="golang rocks")
        store.insert("col", {}, tags=["py"], text="golang rocks")
        result = store.find(tags=["go"], text_query="rocks")
        assert len(result) == 1

    def test_text_query_none_no_restriction(self, store):
        store.insert("col", {}, text="anything")
        assert len(store.find(text_query=None)) == 1


# ── find – ordering ───────────────────────────────────────────────────────────

class TestFindOrdering:
    def test_results_ordered_by_created_at_desc(self, tstore):
        d1 = tstore.insert("col", {"order": 1})
        d2 = tstore.insert("col", {"order": 2})
        d3 = tstore.insert("col", {"order": 3})
        results = tstore.find()
        ids = [d.doc_id for d in results]
        assert ids == [d3.doc_id, d2.doc_id, d1.doc_id]

    def test_ordering_preserved_with_collection_filter(self, tstore):
        a = tstore.insert("c", {"n": 1})
        b = tstore.insert("c", {"n": 2})
        results = tstore.find(collection="c")
        assert results[0].doc_id == b.doc_id
        assert results[1].doc_id == a.doc_id


# ── find – limit / offset ─────────────────────────────────────────────────────

class TestFindPagination:
    def test_limit_restricts_count(self, store):
        for i in range(10):
            store.insert("col", {"i": i})
        assert len(store.find(limit=3)) == 3

    def test_offset_skips_rows(self, tstore):
        docs = [tstore.insert("col", {"n": i}) for i in range(5)]
        # ordered DESC: docs[4], docs[3], docs[2], docs[1], docs[0]
        page = tstore.find(offset=2)
        assert page[0].data == {"n": 2}

    def test_limit_and_offset_together(self, tstore):
        for i in range(6):
            tstore.insert("col", {"n": i})
        page = tstore.find(limit=2, offset=2)
        assert len(page) == 2

    def test_offset_beyond_results_empty(self, store):
        store.insert("col", {})
        assert store.find(offset=10) == []

    def test_default_limit_100(self, store):
        for _ in range(5):
            store.insert("col", {})
        assert len(store.find()) == 5


# ── count ─────────────────────────────────────────────────────────────────────

class TestCount:
    def test_count_all(self, store):
        store.insert("a", {})
        store.insert("b", {})
        assert store.count() == 2

    def test_count_by_collection(self, store):
        store.insert("x", {})
        store.insert("x", {})
        store.insert("y", {})
        assert store.count(collection="x") == 2

    def test_count_by_tags(self, store):
        store.insert("c", {}, tags=["p"])
        store.insert("c", {}, tags=["p", "q"])
        store.insert("c", {}, tags=["q"])
        assert store.count(tags=["p"]) == 2
        assert store.count(tags=["p", "q"]) == 1

    def test_count_empty_store(self, store):
        assert store.count() == 0

    def test_count_after_delete(self, store):
        doc = store.insert("c", {})
        assert store.count() == 1
        store.delete(doc.doc_id)
        assert store.count() == 0


# ── collections / all_tags ────────────────────────────────────────────────────

class TestAggregation:
    def test_collections_distinct(self, store):
        store.insert("alpha", {})
        store.insert("beta", {})
        store.insert("alpha", {})
        assert sorted(store.collections()) == ["alpha", "beta"]

    def test_collections_empty(self, store):
        assert store.collections() == []

    def test_collections_sorted(self, store):
        store.insert("zzz", {})
        store.insert("aaa", {})
        cols = store.collections()
        assert cols == sorted(cols)

    def test_all_tags_distinct(self, store):
        store.insert("c", {}, tags=["a", "b"])
        store.insert("c", {}, tags=["b", "c"])
        assert store.all_tags() == ["a", "b", "c"]

    def test_all_tags_empty(self, store):
        store.insert("c", {})
        assert store.all_tags() == []

    def test_all_tags_sorted(self, store):
        store.insert("c", {}, tags=["z", "m", "a"])
        tags = store.all_tags()
        assert tags == sorted(tags)

    def test_all_tags_no_documents(self, store):
        assert store.all_tags() == []


# ── Persistence ───────────────────────────────────────────────────────────────

class TestPersistence:
    def test_data_persists_to_file(self, tmp_path):
        db = str(tmp_path / "docs.db")
        s1 = DocumentStore(db_path=db)
        doc = s1.insert("col", {"persistent": True})
        s1.close()

        s2 = DocumentStore(db_path=db)
        fetched = s2.get(doc.doc_id)
        s2.close()

        assert fetched is not None
        assert fetched.data == {"persistent": True}

    def test_delete_persists_to_file(self, tmp_path):
        db = str(tmp_path / "docs.db")
        s1 = DocumentStore(db_path=db)
        doc = s1.insert("col", {})
        s1.delete(doc.doc_id)
        s1.close()

        s2 = DocumentStore(db_path=db)
        assert s2.get(doc.doc_id) is None
        s2.close()


# ── Virtual time via now_fn ───────────────────────────────────────────────────

class TestVirtualTime:
    def test_created_at_uses_now_fn(self, clock):
        s = DocumentStore(now_fn=clock)
        doc = s.insert("col", {})
        assert doc.created_at == 1.0
        s.close()

    def test_updated_at_uses_now_fn(self, clock):
        s = DocumentStore(now_fn=clock)
        doc = s.insert("col", {})
        s.update(doc.doc_id, data={"x": 1})
        fetched = s.get(doc.doc_id)
        assert fetched.updated_at == 2.0
        s.close()

    def test_ordering_reflects_virtual_time(self, clock):
        s = DocumentStore(now_fn=clock)
        d1 = s.insert("col", {"n": 1})
        d2 = s.insert("col", {"n": 2})
        results = s.find()
        assert results[0].doc_id == d2.doc_id
        assert results[1].doc_id == d1.doc_id
        s.close()


# ── Thread safety ─────────────────────────────────────────────────────────────

class TestThreadSafety:
    def test_concurrent_inserts(self):
        s = DocumentStore()
        errors = []

        def worker(n):
            try:
                for i in range(10):
                    s.insert("col", {"thread": n, "i": i})
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Errors during concurrent inserts: {errors}"
        assert s.count() == 50
        s.close()

    def test_concurrent_reads_and_writes(self):
        s = DocumentStore()
        doc = s.insert("col", {"seed": True})
        errors = []

        def reader():
            try:
                for _ in range(20):
                    s.get(doc.doc_id)
            except Exception as exc:
                errors.append(exc)

        def writer():
            try:
                for i in range(5):
                    s.insert("col", {"w": i})
            except Exception as exc:
                errors.append(exc)

        threads = (
            [threading.Thread(target=reader) for _ in range(4)]
            + [threading.Thread(target=writer) for _ in range(2)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Errors during concurrent reads/writes: {errors}"
        s.close()


# ── Data round-trip edge cases ────────────────────────────────────────────────

class TestDataRoundTrip:
    def test_bool_values(self, store):
        doc = store.insert("c", {"flag": True, "off": False})
        fetched = store.get(doc.doc_id)
        assert fetched.data["flag"] is True
        assert fetched.data["off"] is False

    def test_null_value(self, store):
        doc = store.insert("c", {"nothing": None})
        assert store.get(doc.doc_id).data["nothing"] is None

    def test_numeric_types(self, store):
        doc = store.insert("c", {"int": 7, "float": 3.14})
        fetched = store.get(doc.doc_id).data
        assert fetched["int"] == 7
        assert abs(fetched["float"] - 3.14) < 1e-9

    def test_list_in_data(self, store):
        doc = store.insert("c", {"items": [1, "two", None, True]})
        assert store.get(doc.doc_id).data["items"] == [1, "two", None, True]

    def test_deeply_nested(self, store):
        payload = {"a": {"b": {"c": {"d": [1, 2, {"e": "f"}]}}}}
        doc = store.insert("c", payload)
        assert store.get(doc.doc_id).data == payload

    def test_unicode_text(self, store):
        doc = store.insert("c", {}, text="Привет мир 🌍")
        assert store.get(doc.doc_id).text == "Привет мир 🌍"

    def test_empty_data_dict(self, store):
        doc = store.insert("c", {})
        assert store.get(doc.doc_id).data == {}
