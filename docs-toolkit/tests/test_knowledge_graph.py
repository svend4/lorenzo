"""Tests for the knowledge_graph module (E26).

65+ tests covering entity, relation, graph and extractor functionality.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.knowledge_graph.entity import Entity, EntityType
from docstoolkit.knowledge_graph.relation import Relation, RelationType
from docstoolkit.knowledge_graph.graph import KnowledgeGraph
from docstoolkit.knowledge_graph.extractor import KGExtractor, ExtractionConfig
from docstoolkit.knowledge_graph import (
    Entity as KGEntity,
    EntityType as KGEntityType,
    Relation as KGRelation,
    RelationType as KGRelationType,
    KnowledgeGraph as KG,
    KGExtractor as KGExt,
    ExtractionConfig as KGConfig,
)


# ===========================================================================
# Helpers
# ===========================================================================

def make_entity(name="Test", entity_type=EntityType.CONCEPT, **kwargs) -> Entity:
    return Entity(name=name, entity_type=entity_type, **kwargs)


def make_relation(source_id, target_id, relation_type=RelationType.RELATED_TO) -> Relation:
    return Relation(source_id=source_id, target_id=target_id, relation_type=relation_type)


# ===========================================================================
# EntityType enum
# ===========================================================================

class TestEntityType:
    def test_all_values_present(self):
        values = {e.value for e in EntityType}
        assert "person" in values
        assert "organization" in values
        assert "technology" in values
        assert "concept" in values
        assert "location" in values
        assert "date" in values
        assert "unknown" in values

    def test_enum_has_seven_members(self):
        assert len(EntityType) == 7

    def test_enum_members_accessible(self):
        assert EntityType.PERSON
        assert EntityType.ORGANIZATION
        assert EntityType.TECHNOLOGY
        assert EntityType.CONCEPT
        assert EntityType.LOCATION
        assert EntityType.DATE
        assert EntityType.UNKNOWN


# ===========================================================================
# Entity dataclass
# ===========================================================================

class TestEntity:
    def test_auto_id_generated(self):
        e = make_entity()
        assert e.entity_id
        assert len(e.entity_id) == 8

    def test_ids_unique(self):
        ids = {make_entity().entity_id for _ in range(50)}
        assert len(ids) == 50

    def test_name_stored(self):
        e = make_entity(name="Python")
        assert e.name == "Python"

    def test_entity_type_stored(self):
        e = make_entity(entity_type=EntityType.TECHNOLOGY)
        assert e.entity_type == EntityType.TECHNOLOGY

    def test_aliases_default_empty(self):
        e = make_entity()
        assert e.aliases == []

    def test_metadata_default_empty(self):
        e = make_entity()
        assert e.metadata == {}

    def test_aliases_stored(self):
        e = Entity(name="Python", entity_type=EntityType.TECHNOLOGY, aliases=["py", "python3"])
        assert "py" in e.aliases
        assert "python3" in e.aliases

    def test_metadata_stored(self):
        e = Entity(name="Python", entity_type=EntityType.TECHNOLOGY, metadata={"version": "3.11"})
        assert e.metadata["version"] == "3.11"

    # matches()

    def test_matches_name_exact(self):
        e = make_entity(name="Python")
        assert e.matches("I use Python daily")

    def test_matches_name_case_insensitive(self):
        e = make_entity(name="Python")
        assert e.matches("python is great")
        assert e.matches("PYTHON")

    def test_matches_alias(self):
        e = Entity(name="Python", entity_type=EntityType.TECHNOLOGY, aliases=["py"])
        assert e.matches("use py for scripting")

    def test_matches_alias_case_insensitive(self):
        e = Entity(name="Python", entity_type=EntityType.TECHNOLOGY, aliases=["Py"])
        assert e.matches("use PY for scripting")

    def test_not_matches_unrelated(self):
        e = make_entity(name="Python")
        assert not e.matches("Java is a language")

    def test_not_matches_empty_text(self):
        e = make_entity(name="Python")
        assert not e.matches("")

    def test_matches_no_aliases(self):
        e = make_entity(name="Rust")
        assert not e.matches("Go is fast")

    # canonical_name()

    def test_canonical_name_strips_whitespace(self):
        e = Entity(name="  Python  ", entity_type=EntityType.TECHNOLOGY)
        assert e.canonical_name() == "Python"

    def test_canonical_name_no_whitespace(self):
        e = make_entity(name="Python")
        assert e.canonical_name() == "Python"

    def test_canonical_name_preserves_internal_spaces(self):
        e = Entity(name="  Large Language Model  ", entity_type=EntityType.CONCEPT)
        assert e.canonical_name() == "Large Language Model"


# ===========================================================================
# RelationType enum
# ===========================================================================

class TestRelationType:
    def test_all_values_present(self):
        values = {r.value for r in RelationType}
        assert "uses" in values
        assert "part_of" in values
        assert "related_to" in values
        assert "mentions" in values
        assert "authored_by" in values
        assert "located_in" in values
        assert "depends_on" in values

    def test_enum_has_seven_members(self):
        assert len(RelationType) == 7


# ===========================================================================
# Relation dataclass
# ===========================================================================

class TestRelation:
    def test_auto_id_generated(self):
        r = make_relation("a", "b")
        assert r.relation_id
        assert len(r.relation_id) == 8

    def test_ids_unique(self):
        ids = {make_relation("a", "b").relation_id for _ in range(50)}
        assert len(ids) == 50

    def test_source_target_stored(self):
        r = make_relation("src", "tgt")
        assert r.source_id == "src"
        assert r.target_id == "tgt"

    def test_default_weight(self):
        r = make_relation("a", "b")
        assert r.weight == 1.0

    def test_custom_weight(self):
        r = Relation(source_id="a", target_id="b",
                     relation_type=RelationType.USES, weight=2.5)
        assert r.weight == 2.5

    def test_default_evidence_empty(self):
        r = make_relation("a", "b")
        assert r.evidence == ""

    def test_custom_evidence(self):
        r = Relation(source_id="a", target_id="b",
                     relation_type=RelationType.MENTIONS,
                     evidence="Python is used in this project")
        assert "Python" in r.evidence

    def test_relation_type_stored(self):
        r = make_relation("a", "b", RelationType.DEPENDS_ON)
        assert r.relation_type == RelationType.DEPENDS_ON


# ===========================================================================
# KnowledgeGraph
# ===========================================================================

class TestKnowledgeGraph:
    def setup_method(self):
        self.g = KnowledgeGraph()

    # add_entity / get_entity

    def test_add_and_get_entity(self):
        e = make_entity(name="Python")
        self.g.add_entity(e)
        assert self.g.get_entity(e.entity_id) is e

    def test_get_entity_not_found(self):
        assert self.g.get_entity("nonexistent") is None

    def test_entity_count_empty(self):
        assert self.g.entity_count() == 0

    def test_entity_count_after_add(self):
        self.g.add_entity(make_entity(name="A"))
        self.g.add_entity(make_entity(name="B"))
        assert self.g.entity_count() == 2

    def test_add_entity_overwrites(self):
        e = make_entity(name="Python")
        self.g.add_entity(e)
        e2 = Entity(name="Python updated", entity_type=EntityType.TECHNOLOGY,
                    entity_id=e.entity_id)
        self.g.add_entity(e2)
        assert self.g.get_entity(e.entity_id).name == "Python updated"
        assert self.g.entity_count() == 1

    # find_entity

    def test_find_entity_by_name(self):
        e = make_entity(name="Python")
        self.g.add_entity(e)
        found = self.g.find_entity("Python")
        assert found is e

    def test_find_entity_case_insensitive(self):
        e = make_entity(name="Python")
        self.g.add_entity(e)
        assert self.g.find_entity("python") is e
        assert self.g.find_entity("PYTHON") is e

    def test_find_entity_by_alias(self):
        e = Entity(name="Python", entity_type=EntityType.TECHNOLOGY, aliases=["py"])
        self.g.add_entity(e)
        assert self.g.find_entity("py") is e

    def test_find_entity_alias_case_insensitive(self):
        e = Entity(name="Python", entity_type=EntityType.TECHNOLOGY, aliases=["Py"])
        self.g.add_entity(e)
        assert self.g.find_entity("PY") is e

    def test_find_entity_not_found(self):
        self.g.add_entity(make_entity(name="Python"))
        assert self.g.find_entity("Ruby") is None

    # add_relation / relations_for

    def test_add_and_relations_for(self):
        e1 = make_entity(name="A")
        e2 = make_entity(name="B")
        self.g.add_entity(e1)
        self.g.add_entity(e2)
        r = make_relation(e1.entity_id, e2.entity_id)
        self.g.add_relation(r)
        rels = self.g.relations_for(e1.entity_id)
        assert r in rels

    def test_relations_for_target(self):
        e1 = make_entity(name="A")
        e2 = make_entity(name="B")
        self.g.add_entity(e1)
        self.g.add_entity(e2)
        r = make_relation(e1.entity_id, e2.entity_id)
        self.g.add_relation(r)
        # Should appear in target's relations too
        assert r in self.g.relations_for(e2.entity_id)

    def test_relations_for_empty(self):
        e = make_entity(name="Isolated")
        self.g.add_entity(e)
        assert self.g.relations_for(e.entity_id) == []

    def test_relation_count_empty(self):
        assert self.g.relation_count() == 0

    def test_relation_count_after_add(self):
        e1 = make_entity(name="A")
        e2 = make_entity(name="B")
        self.g.add_entity(e1)
        self.g.add_entity(e2)
        self.g.add_relation(make_relation(e1.entity_id, e2.entity_id))
        self.g.add_relation(make_relation(e2.entity_id, e1.entity_id))
        assert self.g.relation_count() == 2

    # neighbors

    def test_neighbors_returns_connected(self):
        e1 = make_entity(name="A")
        e2 = make_entity(name="B")
        e3 = make_entity(name="C")
        self.g.add_entity(e1)
        self.g.add_entity(e2)
        self.g.add_entity(e3)
        self.g.add_relation(make_relation(e1.entity_id, e2.entity_id))
        self.g.add_relation(make_relation(e1.entity_id, e3.entity_id))
        nbrs = self.g.neighbors(e1.entity_id)
        ids = {n.entity_id for n in nbrs}
        assert e2.entity_id in ids
        assert e3.entity_id in ids

    def test_neighbors_excludes_self(self):
        e = make_entity(name="Lonely")
        self.g.add_entity(e)
        assert self.g.neighbors(e.entity_id) == []

    def test_neighbors_no_duplicates(self):
        e1 = make_entity(name="A")
        e2 = make_entity(name="B")
        self.g.add_entity(e1)
        self.g.add_entity(e2)
        # Two relations between same pair
        self.g.add_relation(make_relation(e1.entity_id, e2.entity_id))
        self.g.add_relation(make_relation(e2.entity_id, e1.entity_id))
        nbrs = self.g.neighbors(e1.entity_id)
        ids = [n.entity_id for n in nbrs]
        assert ids.count(e2.entity_id) == 1

    def test_disconnected_graph_neighbors_empty(self):
        e1 = make_entity(name="A")
        e2 = make_entity(name="B")
        self.g.add_entity(e1)
        self.g.add_entity(e2)
        # No relation added
        assert self.g.neighbors(e1.entity_id) == []

    # subgraph

    def test_subgraph_includes_only_specified_entities(self):
        e1 = make_entity(name="A")
        e2 = make_entity(name="B")
        e3 = make_entity(name="C")
        self.g.add_entity(e1)
        self.g.add_entity(e2)
        self.g.add_entity(e3)
        sub = self.g.subgraph([e1.entity_id, e2.entity_id])
        assert sub.get_entity(e1.entity_id) is not None
        assert sub.get_entity(e2.entity_id) is not None
        assert sub.get_entity(e3.entity_id) is None

    def test_subgraph_includes_inter_relations(self):
        e1 = make_entity(name="A")
        e2 = make_entity(name="B")
        e3 = make_entity(name="C")
        self.g.add_entity(e1)
        self.g.add_entity(e2)
        self.g.add_entity(e3)
        r12 = make_relation(e1.entity_id, e2.entity_id)
        r13 = make_relation(e1.entity_id, e3.entity_id)
        self.g.add_relation(r12)
        self.g.add_relation(r13)
        sub = self.g.subgraph([e1.entity_id, e2.entity_id])
        # r12 is between both included entities → present
        assert sub.relation_count() == 1

    def test_subgraph_excludes_cross_relations(self):
        e1 = make_entity(name="A")
        e2 = make_entity(name="B")
        e3 = make_entity(name="C")
        self.g.add_entity(e1)
        self.g.add_entity(e2)
        self.g.add_entity(e3)
        # Only relation between e1 and e3 (e3 excluded from subgraph)
        self.g.add_relation(make_relation(e1.entity_id, e3.entity_id))
        sub = self.g.subgraph([e1.entity_id, e2.entity_id])
        assert sub.relation_count() == 0

    def test_subgraph_empty_ids(self):
        self.g.add_entity(make_entity(name="A"))
        sub = self.g.subgraph([])
        assert sub.entity_count() == 0
        assert sub.relation_count() == 0

    def test_subgraph_unknown_id_ignored(self):
        e = make_entity(name="A")
        self.g.add_entity(e)
        sub = self.g.subgraph([e.entity_id, "does_not_exist"])
        assert sub.entity_count() == 1

    # to_dict

    def test_to_dict_structure(self):
        e = make_entity(name="Python", entity_type=EntityType.TECHNOLOGY)
        self.g.add_entity(e)
        d = self.g.to_dict()
        assert "entities" in d
        assert "relations" in d
        assert isinstance(d["entities"], list)
        assert isinstance(d["relations"], list)

    def test_to_dict_entity_fields(self):
        e = Entity(name="Python", entity_type=EntityType.TECHNOLOGY,
                   aliases=["py"], metadata={"version": "3"})
        self.g.add_entity(e)
        d = self.g.to_dict()
        entry = d["entities"][0]
        assert entry["name"] == "Python"
        assert entry["entity_type"] == "technology"
        assert "py" in entry["aliases"]
        assert entry["metadata"]["version"] == "3"

    def test_to_dict_relation_fields(self):
        e1 = make_entity(name="A")
        e2 = make_entity(name="B")
        self.g.add_entity(e1)
        self.g.add_entity(e2)
        r = Relation(source_id=e1.entity_id, target_id=e2.entity_id,
                     relation_type=RelationType.USES, weight=3.0, evidence="A uses B")
        self.g.add_relation(r)
        d = self.g.to_dict()
        entry = d["relations"][0]
        assert entry["relation_type"] == "uses"
        assert entry["weight"] == 3.0
        assert entry["evidence"] == "A uses B"

    def test_to_dict_empty_graph(self):
        d = self.g.to_dict()
        assert d["entities"] == []
        assert d["relations"] == []


# ===========================================================================
# KGExtractor
# ===========================================================================

class TestKGExtractor:
    def setup_method(self):
        self.extractor = KGExtractor()

    # empty / trivial

    def test_extract_empty_string(self):
        entities, relations = self.extractor.extract("")
        assert entities == []
        assert relations == []

    def test_extract_whitespace_only(self):
        entities, relations = self.extractor.extract("   \n\t  ")
        assert entities == []
        assert relations == []

    # entity extraction

    def test_extract_single_title_case(self):
        entities, _ = self.extractor.extract("Python is popular")
        names = [e.name for e in entities]
        assert "Python" in names

    def test_extract_multi_word_title_case(self):
        entities, _ = self.extractor.extract(
            "Large Language Model is transformative technology"
        )
        names = [e.name for e in entities]
        assert any("Large" in n for n in names)

    def test_extract_tech_keyword_classified_technology(self):
        entities, _ = self.extractor.extract("Python API integration")
        tech = [e for e in entities if e.entity_type == EntityType.TECHNOLOGY]
        assert len(tech) >= 1

    def test_extract_allcaps_classified_organization(self):
        entities, _ = self.extractor.extract("NASA launched a satellite. NASA confirmed.")
        orgs = [e for e in entities if e.entity_type == EntityType.ORGANIZATION]
        names = [e.name for e in orgs]
        assert "NASA" in names

    def test_extract_concept_type(self):
        entities, _ = self.extractor.extract("Microservice architecture")
        concepts = [e for e in entities if e.entity_type == EntityType.CONCEPT]
        assert len(concepts) >= 1

    def test_extract_deduplication(self):
        text = "Python Python Python"
        entities, _ = self.extractor.extract(text)
        names = [e.name for e in entities]
        assert names.count("Python") == 1

    def test_extract_min_entity_len_respected(self):
        config = ExtractionConfig(min_entity_len=6)
        extractor = KGExtractor(config)
        entities, _ = extractor.extract("Go runs fast. Javascript is verbose.")
        names = [e.name for e in entities]
        assert "Go" not in names  # too short

    def test_extract_returns_entities_list(self):
        entities, relations = self.extractor.extract("Python and RAG are great tools")
        assert isinstance(entities, list)
        assert isinstance(relations, list)

    # relation extraction

    def test_extract_relation_within_window(self):
        text = "Python RAG pipeline"
        entities, relations = self.extractor.extract(text)
        assert len(entities) >= 2
        assert len(relations) >= 1

    def test_extract_relation_type_related_to(self):
        text = "Python RAG pipeline"
        _, relations = self.extractor.extract(text)
        for r in relations:
            assert r.relation_type == RelationType.RELATED_TO

    def test_extract_relation_evidence_nonempty(self):
        text = "Python RAG pipeline"
        entities, relations = self.extractor.extract(text)
        if relations:
            assert relations[0].evidence != ""

    def test_extract_no_relation_outside_window(self):
        config = ExtractionConfig(relation_window=5)
        extractor = KGExtractor(config)
        # Far-apart entities
        text = "Python" + " " * 200 + "RAG"
        _, relations = extractor.extract(text)
        assert len(relations) == 0

    def test_extract_single_entity_no_relations(self):
        _, relations = self.extractor.extract("Python is a language")
        # Only Python is Title Case here; no two distinct entities → no relation
        assert len(relations) == 0

    # enrich

    def test_enrich_adds_to_existing_graph(self):
        g = KnowledgeGraph()
        self.extractor.enrich(g, "Python RAG integration")
        assert g.entity_count() >= 1

    def test_enrich_no_duplicate_entities(self):
        g = KnowledgeGraph()
        self.extractor.enrich(g, "Python RAG pipeline")
        count_after_first = g.entity_count()
        self.extractor.enrich(g, "Python RAG pipeline")
        assert g.entity_count() == count_after_first

    def test_enrich_adds_relations(self):
        g = KnowledgeGraph()
        self.extractor.enrich(g, "Python RAG pipeline")
        assert g.relation_count() >= 1

    def test_enrich_accumulates_from_multiple_texts(self):
        g = KnowledgeGraph()
        self.extractor.enrich(g, "Python API integration")
        count1 = g.entity_count()
        self.extractor.enrich(g, "Docker Kubernetes deployment")
        count2 = g.entity_count()
        assert count2 >= count1

    # ExtractionConfig

    def test_default_config_values(self):
        config = ExtractionConfig()
        assert config.min_entity_len == 3
        assert config.relation_window == 100

    def test_custom_config_stored(self):
        config = ExtractionConfig(min_entity_len=5, relation_window=50)
        assert config.min_entity_len == 5
        assert config.relation_window == 50

    # package-level re-exports

    def test_package_imports(self):
        assert KGEntity is Entity
        assert KGEntityType is EntityType
        assert KGRelation is Relation
        assert KGRelationType is RelationType
        assert KG is KnowledgeGraph
        assert KGExt is KGExtractor
        assert KGConfig is ExtractionConfig
