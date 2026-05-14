"""E350 DocWorkflowTemplate core implementation.

Reusable workflow templates for documents. Pure stdlib, thread-safe.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class WorkflowStep:
    """A single step in a workflow template."""

    step_id: str
    name: str
    description: str = ""
    required: bool = True
    order: int = 0


@dataclass
class WorkflowTemplate:
    """A named workflow template composed of ordered steps."""

    template_id: str
    name: str
    description: str = ""
    steps: list[WorkflowStep] = field(default_factory=list)
    created_at: float = 0.0
    version: int = 1


@dataclass
class TemplateStats:
    """Aggregate statistics across all workflow templates."""

    total_templates: int
    total_steps: int
    avg_steps_per_template: float


class DocWorkflowTemplate:
    """Manage reusable workflow templates and assign them to documents.

    Internal storage:
        ``_templates``: ``template_id -> WorkflowTemplate``
        ``_doc_templates``: ``doc_id -> template_id`` (current assignment)
    """

    def __init__(self) -> None:
        self._templates: dict[str, WorkflowTemplate] = {}
        self._doc_templates: dict[str, str] = {}
        self._lock = threading.Lock()

    # ---- template CRUD ----------------------------------------------------------

    def create_template(
        self,
        template_id: str,
        name: str,
        steps: list[WorkflowStep],
        description: str = "",
        now: Optional[float] = None,
    ) -> WorkflowTemplate:
        """Create a new template with version=1. Replaces any existing template
        with the same ``template_id``."""
        ts = now if now is not None else time.time()
        with self._lock:
            template = WorkflowTemplate(
                template_id=template_id,
                name=name,
                description=description,
                steps=list(steps),
                created_at=ts,
                version=1,
            )
            self._templates[template_id] = template
            return template

    def update_template(
        self,
        template_id: str,
        name: Optional[str] = None,
        steps: Optional[list[WorkflowStep]] = None,
        description: Optional[str] = None,
    ) -> Optional[WorkflowTemplate]:
        """Partial update of an existing template.

        Increments ``version`` if any change is applied. Returns the updated
        template, or ``None`` if no template with ``template_id`` exists.
        """
        with self._lock:
            template = self._templates.get(template_id)
            if template is None:
                return None
            changed = False
            if name is not None and name != template.name:
                template.name = name
                changed = True
            if description is not None and description != template.description:
                template.description = description
                changed = True
            if steps is not None:
                template.steps = list(steps)
                changed = True
            if changed:
                template.version += 1
            return template

    def delete_template(self, template_id: str) -> bool:
        """Delete a template and any doc assignments referencing it.

        Returns ``True`` if the template existed, otherwise ``False``.
        """
        with self._lock:
            if template_id not in self._templates:
                return False
            del self._templates[template_id]
            # Remove any doc assignments pointing to this template.
            to_remove = [
                doc_id
                for doc_id, tid in self._doc_templates.items()
                if tid == template_id
            ]
            for doc_id in to_remove:
                del self._doc_templates[doc_id]
            return True

    def get_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """Return the template or ``None`` if not found."""
        with self._lock:
            return self._templates.get(template_id)

    def list_templates(self) -> list[WorkflowTemplate]:
        """Return all templates sorted by ``name``."""
        with self._lock:
            return sorted(self._templates.values(), key=lambda t: t.name)

    # ---- step management --------------------------------------------------------

    def add_step(self, template_id: str, step: WorkflowStep) -> bool:
        """Append a step to a template. Returns True if the template existed."""
        with self._lock:
            template = self._templates.get(template_id)
            if template is None:
                return False
            template.steps.append(step)
            template.version += 1
            return True

    def remove_step(self, template_id: str, step_id: str) -> bool:
        """Remove a step by ``step_id``. Returns ``True`` if it existed."""
        with self._lock:
            template = self._templates.get(template_id)
            if template is None:
                return False
            for i, step in enumerate(template.steps):
                if step.step_id == step_id:
                    del template.steps[i]
                    template.version += 1
                    return True
            return False

    def steps_of(self, template_id: str) -> list[WorkflowStep]:
        """Return steps for a template sorted by ``order``.

        Empty list if the template does not exist.
        """
        with self._lock:
            template = self._templates.get(template_id)
            if template is None:
                return []
            return sorted(template.steps, key=lambda s: s.order)

    # ---- doc assignment ---------------------------------------------------------

    def apply_template(self, doc_id: str, template_id: str) -> bool:
        """Assign a template to a document. Returns ``True`` if the template exists."""
        with self._lock:
            if template_id not in self._templates:
                return False
            self._doc_templates[doc_id] = template_id
            return True

    def template_for_doc(self, doc_id: str) -> Optional[WorkflowTemplate]:
        """Return the template currently assigned to a document, or ``None``."""
        with self._lock:
            tid = self._doc_templates.get(doc_id)
            if tid is None:
                return None
            return self._templates.get(tid)

    def docs_using(self, template_id: str) -> list[str]:
        """Return sorted doc_ids using the given template."""
        with self._lock:
            return sorted(
                doc_id
                for doc_id, tid in self._doc_templates.items()
                if tid == template_id
            )

    def clear_doc(self, doc_id: str) -> bool:
        """Remove a doc's template assignment. Returns ``True`` if it existed."""
        with self._lock:
            return self._doc_templates.pop(doc_id, None) is not None

    # ---- statistics -------------------------------------------------------------

    def stats(self) -> TemplateStats:
        """Return aggregate statistics across all templates."""
        with self._lock:
            total_templates = len(self._templates)
            total_steps = sum(len(t.steps) for t in self._templates.values())
            avg = (total_steps / total_templates) if total_templates else 0.0
            return TemplateStats(
                total_templates=total_templates,
                total_steps=total_steps,
                avg_steps_per_template=avg,
            )
