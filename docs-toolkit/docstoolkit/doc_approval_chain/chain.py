"""E320 DocApprovalChain — multi-step document approval workflow.

Thread-safe, stdlib-only, dataclass-based approval chain for document workflows.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ApprovalStep:
    """A single step in an approval chain."""

    step_id: str
    chain_id: str
    approver: str
    order: int  # 0-based step order
    status: str = "pending"  # "pending", "approved", "rejected", "skipped"
    decided_at: Optional[float] = None
    comment: str = ""


@dataclass
class ApprovalChain:
    """A complete approval workflow for a document."""

    chain_id: str
    doc_id: str
    created_by: str
    created_at: float = 0.0
    status: str = "pending"  # "pending", "in_progress", "approved", "rejected", "cancelled"
    current_step: int = 0


@dataclass
class ChainStats:
    """Aggregate statistics across all approval chains."""

    total_chains: int
    pending: int
    in_progress: int
    approved: int
    rejected: int
    cancelled: int


class DocApprovalChain:
    """In-memory, thread-safe multi-step document approval chain manager."""

    def __init__(self) -> None:
        self._chains: dict[str, ApprovalChain] = {}
        self._steps: dict[str, list[ApprovalStep]] = {}
        self._by_doc: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------ create_chain
    def create_chain(
        self,
        doc_id: str,
        created_by: str,
        approvers: list[str],
        now: Optional[float] = None,
    ) -> ApprovalChain:
        """Create a new approval chain with one step per approver.

        Status is ``"pending"`` when *approvers* is empty, otherwise
        ``"in_progress"``.  Returns the newly created :class:`ApprovalChain`.
        """
        if now is None:
            now = time.time()

        chain_id = uuid.uuid4().hex
        status = "in_progress" if approvers else "pending"

        chain = ApprovalChain(
            chain_id=chain_id,
            doc_id=doc_id,
            created_by=created_by,
            created_at=now,
            status=status,
            current_step=0,
        )

        steps: list[ApprovalStep] = [
            ApprovalStep(
                step_id=uuid.uuid4().hex,
                chain_id=chain_id,
                approver=approver,
                order=idx,
            )
            for idx, approver in enumerate(approvers)
        ]

        with self._lock:
            self._chains[chain_id] = chain
            self._steps[chain_id] = steps
            self._by_doc.setdefault(doc_id, []).append(chain_id)

        return chain

    # ------------------------------------------------------------- get_chain
    def get_chain(self, chain_id: str) -> Optional[ApprovalChain]:
        """Return the :class:`ApprovalChain` for *chain_id*, or ``None``."""
        with self._lock:
            return self._chains.get(chain_id)

    # ------------------------------------------------------------- get_steps
    def get_steps(self, chain_id: str) -> list[ApprovalStep]:
        """Return all steps for *chain_id* sorted by order."""
        with self._lock:
            steps = list(self._steps.get(chain_id, []))
        steps.sort(key=lambda s: s.order)
        return steps

    # ----------------------------------------------------------- current_step
    def current_step(self, chain_id: str) -> Optional[ApprovalStep]:
        """Return the step at the chain's ``current_step`` index, or ``None``.

        Returns ``None`` when the chain is not found or all steps are complete.
        """
        with self._lock:
            chain = self._chains.get(chain_id)
            if chain is None:
                return None
            steps = self._steps.get(chain_id, [])
            sorted_steps = sorted(steps, key=lambda s: s.order)
            if chain.current_step >= len(sorted_steps):
                return None
            return sorted_steps[chain.current_step]

    # ----------------------------------------------------------- approve_step
    def approve_step(
        self,
        chain_id: str,
        approver: str,
        comment: str = "",
        now: Optional[float] = None,
    ) -> Optional[ApprovalStep]:
        """Approve the current pending step.

        Advances ``chain.current_step``.  When all steps are approved the
        chain status is set to ``"approved"``.

        Returns ``None`` if the chain is not found or there is no pending step.
        """
        if now is None:
            now = time.time()

        with self._lock:
            chain = self._chains.get(chain_id)
            if chain is None:
                return None

            steps = sorted(self._steps.get(chain_id, []), key=lambda s: s.order)
            if chain.current_step >= len(steps):
                return None

            step = steps[chain.current_step]
            if step.status != "pending":
                return None

            step.status = "approved"
            step.decided_at = now
            step.comment = comment

            chain.current_step += 1

            # If all steps are now approved, mark chain approved
            if chain.current_step >= len(steps):
                chain.status = "approved"

        return step

    # ------------------------------------------------------------ reject_step
    def reject_step(
        self,
        chain_id: str,
        approver: str,
        comment: str = "",
        now: Optional[float] = None,
    ) -> Optional[ApprovalStep]:
        """Reject the current pending step and set the chain to ``"rejected"``.

        Returns ``None`` if the chain is not found or there is no pending step.
        """
        if now is None:
            now = time.time()

        with self._lock:
            chain = self._chains.get(chain_id)
            if chain is None:
                return None

            steps = sorted(self._steps.get(chain_id, []), key=lambda s: s.order)
            if chain.current_step >= len(steps):
                return None

            step = steps[chain.current_step]
            if step.status != "pending":
                return None

            step.status = "rejected"
            step.decided_at = now
            step.comment = comment

            chain.status = "rejected"

        return step

    # ----------------------------------------------------------- cancel_chain
    def cancel_chain(self, chain_id: str) -> bool:
        """Set chain status to ``"cancelled"``.

        Returns ``True`` if the chain was found, ``False`` otherwise.
        """
        with self._lock:
            chain = self._chains.get(chain_id)
            if chain is None:
                return False
            chain.status = "cancelled"
            return True

    # -------------------------------------------------------- chains_for_doc
    def chains_for_doc(self, doc_id: str) -> list[ApprovalChain]:
        """Return all chains for *doc_id* sorted by ``created_at``."""
        with self._lock:
            chain_ids = list(self._by_doc.get(doc_id, []))
            chains = [self._chains[cid] for cid in chain_ids if cid in self._chains]
        chains.sort(key=lambda c: c.created_at)
        return chains

    # ------------------------------------------------------- chains_by_status
    def chains_by_status(self, status: str) -> list[ApprovalChain]:
        """Return all chains with *status* sorted by ``created_at``."""
        with self._lock:
            chains = [c for c in self._chains.values() if c.status == status]
        chains.sort(key=lambda c: c.created_at)
        return chains

    # --------------------------------------------------------------- stats
    def stats(self) -> ChainStats:
        """Return aggregate counts across all chains by status."""
        with self._lock:
            pending = 0
            in_progress = 0
            approved = 0
            rejected = 0
            cancelled = 0
            for chain in self._chains.values():
                if chain.status == "pending":
                    pending += 1
                elif chain.status == "in_progress":
                    in_progress += 1
                elif chain.status == "approved":
                    approved += 1
                elif chain.status == "rejected":
                    rejected += 1
                elif chain.status == "cancelled":
                    cancelled += 1
            total = len(self._chains)
        return ChainStats(
            total_chains=total,
            pending=pending,
            in_progress=in_progress,
            approved=approved,
            rejected=rejected,
            cancelled=cancelled,
        )
