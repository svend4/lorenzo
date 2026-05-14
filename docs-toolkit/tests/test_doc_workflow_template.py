"""Tests for E350 doc_workflow_template."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_workflow_template import (
    DocWorkflowTemplate,
    TemplateStats,
    WorkflowStep,
    WorkflowTemplate,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestWorkflowStepDataclass:
    def test_create_minimal(self):
        step = WorkflowStep(step_id="s1", name="Draft")
        assert step.step_id == "s1"
        assert step.name == "Draft"

    def test_defaults(self):
        step = WorkflowStep(step_id="s1", name="Draft")
        assert step.description == ""
        assert step.required is True
        assert step.order == 0

    def test_create_full(self):
        step = WorkflowStep(
            step_id="s1",
            name="Draft",
            description="Write initial draft",
            required=False,
            order=5,
        )
        assert step.description == "Write initial draft"
        assert step.required is False
        assert step.order == 5

    def test_equality(self):
        a = WorkflowStep(step_id="s1", name="Draft")
        b = WorkflowStep(step_id="s1", name="Draft")
        assert a == b


class TestWorkflowTemplateDataclass:
    def test_create_minimal(self):
        tpl = WorkflowTemplate(template_id="t1", name="Article")
        assert tpl.template_id == "t1"
        assert tpl.name == "Article"

    def test_defaults(self):
        tpl = WorkflowTemplate(template_id="t1", name="Article")
        assert tpl.description == ""
        assert tpl.steps == []
        assert tpl.created_at == 0.0
        assert tpl.version == 1

    def test_steps_default_factory_independent(self):
        a = WorkflowTemplate(template_id="t1", name="A")
        b = WorkflowTemplate(template_id="t2", name="B")
        a.steps.append(WorkflowStep(step_id="s", name="x"))
        assert b.steps == []

    def test_create_with_steps(self):
        steps = [WorkflowStep(step_id="s1", name="Draft")]
        tpl = WorkflowTemplate(
            template_id="t1",
            name="Article",
            description="desc",
            steps=steps,
            created_at=123.0,
            version=2,
        )
        assert tpl.steps == steps
        assert tpl.created_at == 123.0
        assert tpl.version == 2
        assert tpl.description == "desc"


class TestTemplateStatsDataclass:
    def test_create(self):
        s = TemplateStats(total_templates=3, total_steps=9, avg_steps_per_template=3.0)
        assert s.total_templates == 3
        assert s.total_steps == 9
        assert s.avg_steps_per_template == 3.0

    def test_equality(self):
        a = TemplateStats(total_templates=1, total_steps=2, avg_steps_per_template=2.0)
        b = TemplateStats(total_templates=1, total_steps=2, avg_steps_per_template=2.0)
        assert a == b


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_create_empty(self):
        dwt = DocWorkflowTemplate()
        assert dwt.list_templates() == []

    def test_initial_stats(self):
        dwt = DocWorkflowTemplate()
        s = dwt.stats()
        assert s.total_templates == 0
        assert s.total_steps == 0
        assert s.avg_steps_per_template == 0.0

    def test_no_doc_assignments(self):
        dwt = DocWorkflowTemplate()
        assert dwt.template_for_doc("doc1") is None


# ---------------------------------------------------------------------------
# create_template
# ---------------------------------------------------------------------------


class TestCreateTemplate:
    def test_returns_template(self):
        dwt = DocWorkflowTemplate()
        tpl = dwt.create_template("t1", "Article", [], now=100.0)
        assert isinstance(tpl, WorkflowTemplate)
        assert tpl.template_id == "t1"

    def test_fields_set(self):
        dwt = DocWorkflowTemplate()
        tpl = dwt.create_template(
            "t1", "Article", [], description="desc", now=100.0
        )
        assert tpl.name == "Article"
        assert tpl.description == "desc"
        assert tpl.created_at == 100.0

    def test_version_is_one(self):
        dwt = DocWorkflowTemplate()
        tpl = dwt.create_template("t1", "Article", [], now=100.0)
        assert tpl.version == 1

    def test_with_steps(self):
        dwt = DocWorkflowTemplate()
        steps = [
            WorkflowStep(step_id="s1", name="Draft", order=1),
            WorkflowStep(step_id="s2", name="Review", order=2),
        ]
        tpl = dwt.create_template("t1", "Article", steps, now=100.0)
        assert len(tpl.steps) == 2

    def test_now_defaults_to_time(self):
        dwt = DocWorkflowTemplate()
        tpl = dwt.create_template("t1", "Article", [])
        assert tpl.created_at > 0.0

    def test_retrievable(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Article", [], now=100.0)
        assert dwt.get_template("t1") is not None

    def test_steps_are_copied(self):
        dwt = DocWorkflowTemplate()
        external = [WorkflowStep(step_id="s1", name="Draft")]
        dwt.create_template("t1", "Article", external, now=100.0)
        external.append(WorkflowStep(step_id="s2", name="Review"))
        tpl = dwt.get_template("t1")
        assert len(tpl.steps) == 1


# ---------------------------------------------------------------------------
# update_template
# ---------------------------------------------------------------------------


class TestUpdateTemplate:
    def test_update_name(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Old", [], now=100.0)
        tpl = dwt.update_template("t1", name="New")
        assert tpl is not None
        assert tpl.name == "New"

    def test_update_description(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        tpl = dwt.update_template("t1", description="d")
        assert tpl.description == "d"

    def test_update_steps(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        steps = [WorkflowStep(step_id="s1", name="x")]
        tpl = dwt.update_template("t1", steps=steps)
        assert len(tpl.steps) == 1

    def test_partial_update_preserves_others(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], description="orig", now=100.0)
        tpl = dwt.update_template("t1", name="New")
        assert tpl.description == "orig"

    def test_version_increments(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        tpl = dwt.update_template("t1", name="New")
        assert tpl.version == 2

    def test_version_increments_on_steps_change(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        tpl = dwt.update_template("t1", steps=[WorkflowStep(step_id="s", name="x")])
        assert tpl.version == 2

    def test_version_not_incremented_when_no_change(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], description="d", now=100.0)
        tpl = dwt.update_template("t1", name="Name", description="d")
        assert tpl.version == 1

    def test_multiple_updates_increment(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "A", [], now=100.0)
        dwt.update_template("t1", name="B")
        tpl = dwt.update_template("t1", name="C")
        assert tpl.version == 3

    def test_missing_returns_none(self):
        dwt = DocWorkflowTemplate()
        assert dwt.update_template("missing", name="x") is None


# ---------------------------------------------------------------------------
# delete_template
# ---------------------------------------------------------------------------


class TestDeleteTemplate:
    def test_existing_returns_true(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        assert dwt.delete_template("t1") is True

    def test_missing_returns_false(self):
        dwt = DocWorkflowTemplate()
        assert dwt.delete_template("missing") is False

    def test_removed_from_storage(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.delete_template("t1")
        assert dwt.get_template("t1") is None

    def test_clears_doc_assignments(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.apply_template("doc1", "t1")
        dwt.apply_template("doc2", "t1")
        dwt.delete_template("t1")
        assert dwt.template_for_doc("doc1") is None
        assert dwt.template_for_doc("doc2") is None

    def test_does_not_affect_other_assignments(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "A", [], now=100.0)
        dwt.create_template("t2", "B", [], now=100.0)
        dwt.apply_template("doc1", "t1")
        dwt.apply_template("doc2", "t2")
        dwt.delete_template("t1")
        assert dwt.template_for_doc("doc2") is not None
        assert dwt.template_for_doc("doc2").template_id == "t2"


# ---------------------------------------------------------------------------
# get_template
# ---------------------------------------------------------------------------


class TestGetTemplate:
    def test_found(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        tpl = dwt.get_template("t1")
        assert tpl is not None
        assert tpl.template_id == "t1"

    def test_not_found(self):
        dwt = DocWorkflowTemplate()
        assert dwt.get_template("missing") is None


# ---------------------------------------------------------------------------
# list_templates
# ---------------------------------------------------------------------------


class TestListTemplates:
    def test_empty(self):
        dwt = DocWorkflowTemplate()
        assert dwt.list_templates() == []

    def test_sorted_by_name(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Charlie", [], now=100.0)
        dwt.create_template("t2", "Alpha", [], now=100.0)
        dwt.create_template("t3", "Bravo", [], now=100.0)
        names = [t.name for t in dwt.list_templates()]
        assert names == ["Alpha", "Bravo", "Charlie"]

    def test_all_returned(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "A", [], now=100.0)
        dwt.create_template("t2", "B", [], now=100.0)
        assert len(dwt.list_templates()) == 2


# ---------------------------------------------------------------------------
# add_step
# ---------------------------------------------------------------------------


class TestAddStep:
    def test_returns_true_when_template_exists(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        step = WorkflowStep(step_id="s1", name="Draft")
        assert dwt.add_step("t1", step) is True

    def test_returns_false_when_missing(self):
        dwt = DocWorkflowTemplate()
        step = WorkflowStep(step_id="s1", name="Draft")
        assert dwt.add_step("missing", step) is False

    def test_step_appended(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.add_step("t1", WorkflowStep(step_id="s1", name="Draft"))
        tpl = dwt.get_template("t1")
        assert len(tpl.steps) == 1
        assert tpl.steps[0].step_id == "s1"

    def test_version_increments(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.add_step("t1", WorkflowStep(step_id="s1", name="Draft"))
        tpl = dwt.get_template("t1")
        assert tpl.version == 2

    def test_multiple_adds(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.add_step("t1", WorkflowStep(step_id="s1", name="Draft"))
        dwt.add_step("t1", WorkflowStep(step_id="s2", name="Review"))
        tpl = dwt.get_template("t1")
        assert len(tpl.steps) == 2
        assert tpl.version == 3


# ---------------------------------------------------------------------------
# remove_step
# ---------------------------------------------------------------------------


class TestRemoveStep:
    def test_returns_true_when_existing(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template(
            "t1",
            "Name",
            [WorkflowStep(step_id="s1", name="Draft")],
            now=100.0,
        )
        assert dwt.remove_step("t1", "s1") is True

    def test_returns_false_when_template_missing(self):
        dwt = DocWorkflowTemplate()
        assert dwt.remove_step("missing", "s1") is False

    def test_returns_false_when_step_missing(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        assert dwt.remove_step("t1", "missing") is False

    def test_step_removed(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template(
            "t1",
            "Name",
            [
                WorkflowStep(step_id="s1", name="Draft"),
                WorkflowStep(step_id="s2", name="Review"),
            ],
            now=100.0,
        )
        dwt.remove_step("t1", "s1")
        tpl = dwt.get_template("t1")
        ids = [s.step_id for s in tpl.steps]
        assert "s1" not in ids
        assert "s2" in ids

    def test_version_increments(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template(
            "t1",
            "Name",
            [WorkflowStep(step_id="s1", name="Draft")],
            now=100.0,
        )
        dwt.remove_step("t1", "s1")
        tpl = dwt.get_template("t1")
        assert tpl.version == 2

    def test_version_not_incremented_on_missing_step(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.remove_step("t1", "missing")
        tpl = dwt.get_template("t1")
        assert tpl.version == 1


# ---------------------------------------------------------------------------
# apply_template
# ---------------------------------------------------------------------------


class TestApplyTemplate:
    def test_returns_true_when_exists(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        assert dwt.apply_template("doc1", "t1") is True

    def test_returns_false_when_missing(self):
        dwt = DocWorkflowTemplate()
        assert dwt.apply_template("doc1", "missing") is False

    def test_assignment_stored(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.apply_template("doc1", "t1")
        tpl = dwt.template_for_doc("doc1")
        assert tpl is not None
        assert tpl.template_id == "t1"

    def test_reassignment_replaces(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "A", [], now=100.0)
        dwt.create_template("t2", "B", [], now=100.0)
        dwt.apply_template("doc1", "t1")
        dwt.apply_template("doc1", "t2")
        tpl = dwt.template_for_doc("doc1")
        assert tpl.template_id == "t2"


# ---------------------------------------------------------------------------
# template_for_doc
# ---------------------------------------------------------------------------


class TestTemplateForDoc:
    def test_found(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.apply_template("doc1", "t1")
        tpl = dwt.template_for_doc("doc1")
        assert tpl is not None
        assert tpl.template_id == "t1"

    def test_not_found(self):
        dwt = DocWorkflowTemplate()
        assert dwt.template_for_doc("doc1") is None


# ---------------------------------------------------------------------------
# docs_using
# ---------------------------------------------------------------------------


class TestDocsUsing:
    def test_empty(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        assert dwt.docs_using("t1") == []

    def test_sorted(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.apply_template("doc_c", "t1")
        dwt.apply_template("doc_a", "t1")
        dwt.apply_template("doc_b", "t1")
        assert dwt.docs_using("t1") == ["doc_a", "doc_b", "doc_c"]

    def test_only_for_specified(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "A", [], now=100.0)
        dwt.create_template("t2", "B", [], now=100.0)
        dwt.apply_template("doc1", "t1")
        dwt.apply_template("doc2", "t2")
        assert dwt.docs_using("t1") == ["doc1"]
        assert dwt.docs_using("t2") == ["doc2"]

    def test_missing_template(self):
        dwt = DocWorkflowTemplate()
        assert dwt.docs_using("missing") == []


# ---------------------------------------------------------------------------
# steps_of
# ---------------------------------------------------------------------------


class TestStepsOf:
    def test_empty(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        assert dwt.steps_of("t1") == []

    def test_missing_returns_empty(self):
        dwt = DocWorkflowTemplate()
        assert dwt.steps_of("missing") == []

    def test_sorted_by_order(self):
        dwt = DocWorkflowTemplate()
        steps = [
            WorkflowStep(step_id="s3", name="Third", order=30),
            WorkflowStep(step_id="s1", name="First", order=10),
            WorkflowStep(step_id="s2", name="Second", order=20),
        ]
        dwt.create_template("t1", "Name", steps, now=100.0)
        result = dwt.steps_of("t1")
        assert [s.step_id for s in result] == ["s1", "s2", "s3"]

    def test_zero_order_default(self):
        dwt = DocWorkflowTemplate()
        steps = [
            WorkflowStep(step_id="a", name="A"),
            WorkflowStep(step_id="b", name="B"),
        ]
        dwt.create_template("t1", "Name", steps, now=100.0)
        # Stable sort preserves insertion when order equal.
        result = dwt.steps_of("t1")
        assert len(result) == 2


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------


class TestClearDoc:
    def test_existing_returns_true(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.apply_template("doc1", "t1")
        assert dwt.clear_doc("doc1") is True

    def test_missing_returns_false(self):
        dwt = DocWorkflowTemplate()
        assert dwt.clear_doc("doc1") is False

    def test_assignment_removed(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.apply_template("doc1", "t1")
        dwt.clear_doc("doc1")
        assert dwt.template_for_doc("doc1") is None

    def test_double_clear(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "Name", [], now=100.0)
        dwt.apply_template("doc1", "t1")
        dwt.clear_doc("doc1")
        assert dwt.clear_doc("doc1") is False


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        dwt = DocWorkflowTemplate()
        s = dwt.stats()
        assert s.total_templates == 0
        assert s.total_steps == 0
        assert s.avg_steps_per_template == 0.0

    def test_counts(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template(
            "t1",
            "A",
            [
                WorkflowStep(step_id="s1", name="x"),
                WorkflowStep(step_id="s2", name="y"),
            ],
            now=100.0,
        )
        dwt.create_template(
            "t2",
            "B",
            [WorkflowStep(step_id="s1", name="x")],
            now=100.0,
        )
        s = dwt.stats()
        assert s.total_templates == 2
        assert s.total_steps == 3

    def test_avg(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template(
            "t1",
            "A",
            [
                WorkflowStep(step_id="s1", name="x"),
                WorkflowStep(step_id="s2", name="y"),
                WorkflowStep(step_id="s3", name="z"),
            ],
            now=100.0,
        )
        dwt.create_template(
            "t2",
            "B",
            [WorkflowStep(step_id="s1", name="x")],
            now=100.0,
        )
        s = dwt.stats()
        assert s.avg_steps_per_template == pytest.approx(2.0)

    def test_avg_with_no_steps(self):
        dwt = DocWorkflowTemplate()
        dwt.create_template("t1", "A", [], now=100.0)
        dwt.create_template("t2", "B", [], now=100.0)
        s = dwt.stats()
        assert s.total_templates == 2
        assert s.total_steps == 0
        assert s.avg_steps_per_template == 0.0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_create_template(self):
        dwt = DocWorkflowTemplate()
        n_threads = 20
        per_thread = 10

        def worker(tid_prefix: str):
            for i in range(per_thread):
                dwt.create_template(
                    f"{tid_prefix}-{i}",
                    f"Name-{tid_prefix}-{i}",
                    [WorkflowStep(step_id=f"s{i}", name="x")],
                    now=100.0,
                )

        threads = [
            threading.Thread(target=worker, args=(f"t{idx}",))
            for idx in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        all_templates = dwt.list_templates()
        assert len(all_templates) == n_threads * per_thread

    def test_concurrent_create_and_delete(self):
        dwt = DocWorkflowTemplate()

        def creator():
            for i in range(50):
                dwt.create_template(
                    f"c-{i}", f"name-{i}", [], now=100.0
                )

        def deleter():
            for i in range(50):
                dwt.delete_template(f"c-{i}")

        t1 = threading.Thread(target=creator)
        t2 = threading.Thread(target=deleter)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # Should not raise; state is consistent
        dwt.stats()
