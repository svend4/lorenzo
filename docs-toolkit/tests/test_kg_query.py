"""Phase V.3 — KG query DSL tests."""
from __future__ import annotations

import pytest

from docstoolkit.knowledge_graph import (
    Entity, EntityType,
    Triple, TripleStore,
    QueryParseError, parse_query, run_query,
)


@pytest.fixture
def populated_store():
    s = TripleStore(":memory:")
    for eid, name in [("py", "Python"), ("rag", "RAG"), ("llm", "LLM"),
                      ("alice", "Alice"), ("bob", "Bob")]:
        s.add_entity(Entity(entity_id=eid, name=name,
                            entity_type=EntityType.CONCEPT))
    s.add_triple(Triple(subject="py", predicate="uses", object="rag"))
    s.add_triple(Triple(subject="py", predicate="uses", object="llm"))
    s.add_triple(Triple(subject="rag", predicate="mentions", object="alice"))
    s.add_triple(Triple(subject="rag", predicate="mentions", object="bob"))
    s.add_triple(Triple(subject="llm", predicate="mentions", object="alice"))
    yield s
    s.close()


# ---------- Parser ----------

def test_parse_single_pattern():
    pats = parse_query('"Python" uses ?topic')
    assert len(pats) == 1
    assert pats[0].subject == "Python"
    assert pats[0].predicate == "uses"
    assert pats[0].object == "?topic"


def test_parse_multiple_patterns():
    text = '''
        "Python" uses     ?topic
        ?topic   mentions ?author
    '''
    pats = parse_query(text)
    assert len(pats) == 2
    assert pats[1].object == "?author"


def test_parse_skips_blank_lines_and_comments():
    text = '''
        # this is a comment

        "py" uses "rag"
    '''
    pats = parse_query(text)
    assert len(pats) == 1


def test_parse_rejects_empty_query():
    with pytest.raises(QueryParseError):
        parse_query("")


def test_parse_rejects_malformed_line():
    with pytest.raises(QueryParseError) as excinfo:
        parse_query('this is nonsense')
    assert "line 1" in str(excinfo.value)


# ---------- Runner ----------

def test_run_simple_literal_subject(populated_store):
    res = run_query(populated_store, '"py" uses ?topic')
    topics = {b["topic"] for b in res}
    assert topics == {"rag", "llm"}


def test_run_simple_literal_object(populated_store):
    res = run_query(populated_store, '?subj mentions "alice"')
    subjs = {b["subj"] for b in res}
    assert subjs == {"rag", "llm"}


def test_run_two_pattern_join(populated_store):
    """Topics used by `py` that mention an author."""
    res = run_query(populated_store, '''
        "py"   uses     ?topic
        ?topic mentions ?author
    ''')
    pairs = sorted((b["topic"], b["author"]) for b in res)
    assert pairs == [("llm", "alice"), ("rag", "alice"), ("rag", "bob")]


def test_run_three_pattern_chain(populated_store):
    populated_store.add_triple(
        Triple(subject="alice", predicate="works_at", object="acme")
    )
    res = run_query(populated_store, '''
        "py"     uses      ?topic
        ?topic   mentions  ?author
        ?author  works_at  ?org
    ''')
    triples = sorted((b["topic"], b["author"], b["org"]) for b in res)
    # Only `rag mentions alice works_at acme` and `llm mentions alice works_at acme`
    assert triples == [
        ("llm", "alice", "acme"),
        ("rag", "alice", "acme"),
    ]


def test_run_no_match_returns_empty(populated_store):
    res = run_query(populated_store, '"py" uses "nonexistent"')
    assert res == []


def test_run_no_match_short_circuits(populated_store):
    # First pattern matches; second has no matches → empty.
    res = run_query(populated_store, '''
        "py"     uses     ?topic
        ?topic   imaginary_predicate ?x
    ''')
    assert res == []


def test_run_pattern_with_only_variables(populated_store):
    res = run_query(populated_store, '?s mentions ?o')
    # rag→alice, rag→bob, llm→alice  = 3 bindings
    assert len(res) == 3
