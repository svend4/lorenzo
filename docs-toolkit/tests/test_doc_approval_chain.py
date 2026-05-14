"""Tests for E320 DocApprovalChain — multi-step document approval workflow."""
from __future__ import annotations

import threading
import time
from dataclasses import fields

import pytest

from docstoolkit.doc_approval_chain import (
    ApprovalChain,
    ApprovalStep,
    ChainStats,
    DocApprovalChain,
)


# ---------------------------------------------------------------------------
# Dataclass shape tests
# ---------------------------------------------------------------------------


class TestApprovalStepDataclass:
    def test_required_fields(self):
        step = ApprovalStep(
            step_id="s1",
            chain_id="c1",
            approver="alice",
            order=0,
        )
        assert step.step_id == "s1"
        assert step.chain_id == "c1"
        assert step.approver == "alice"
        assert step.order == 0

    def test_default_status(self):
        step = ApprovalStep(step_id="s", chain_id="c", approver="a", order=0)
        assert step.status == "pending"

    def test_default_decided_at_none(self):
        step = ApprovalStep(step_id="s", chain_id="c", approver="a", order=0)
        assert step.decided_at is None

    def test_default_comment_empty(self):
        step = ApprovalStep(step_id="s", chain_id="c", approver="a", order=0)
        assert step.comment == ""

    def test_custom_values(self):
        step = ApprovalStep(
            step_id="x",
            chain_id="y",
            approver="bob",
            order=3,
            status="approved",
            decided_at=1000.0,
            comment="LGTM",
        )
        assert step.status == "approved"
        assert step.decided_at == 1000.0
        assert step.comment == "LGTM"


class TestApprovalChainDataclass:
    def test_required_fields(self):
        chain = ApprovalChain(chain_id="c1", doc_id="d1", created_by="alice")
        assert chain.chain_id == "c1"
        assert chain.doc_id == "d1"
        assert chain.created_by == "alice"

    def test_default_created_at(self):
        chain = ApprovalChain(chain_id="c", doc_id="d", created_by="u")
        assert chain.created_at == 0.0

    def test_default_status(self):
        chain = ApprovalChain(chain_id="c", doc_id="d", created_by="u")
        assert chain.status == "pending"

    def test_default_current_step(self):
        chain = ApprovalChain(chain_id="c", doc_id="d", created_by="u")
        assert chain.current_step == 0

    def test_custom_values(self):
        chain = ApprovalChain(
            chain_id="c2",
            doc_id="d2",
            created_by="bob",
            created_at=500.0,
            status="approved",
            current_step=2,
        )
        assert chain.status == "approved"
        assert chain.current_step == 2
        assert chain.created_at == 500.0


class TestChainStatsDataclass:
    def test_all_fields(self):
        s = ChainStats(
            total_chains=10,
            pending=1,
            in_progress=2,
            approved=3,
            rejected=2,
            cancelled=2,
        )
        assert s.total_chains == 10
        assert s.pending == 1
        assert s.in_progress == 2
        assert s.approved == 3
        assert s.rejected == 2
        assert s.cancelled == 2


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_creates_instance(self):
        dac = DocApprovalChain()
        assert dac is not None

    def test_empty_stats_on_start(self):
        dac = DocApprovalChain()
        s = dac.stats()
        assert s.total_chains == 0
        assert s.pending == 0
        assert s.in_progress == 0
        assert s.approved == 0
        assert s.rejected == 0
        assert s.cancelled == 0


# ---------------------------------------------------------------------------
# create_chain
# ---------------------------------------------------------------------------


class TestCreateChain:
    def test_returns_approval_chain(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob", "carol"])
        assert isinstance(chain, ApprovalChain)

    def test_chain_id_is_uuid_hex(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob"])
        assert len(chain.chain_id) == 32
        assert chain.chain_id.isalnum()

    def test_chain_ids_are_unique(self):
        dac = DocApprovalChain()
        c1 = dac.create_chain("doc1", "alice", ["bob"])
        c2 = dac.create_chain("doc1", "alice", ["bob"])
        assert c1.chain_id != c2.chain_id

    def test_status_in_progress_with_approvers(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob", "carol"])
        assert chain.status == "in_progress"

    def test_status_pending_without_approvers(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", [])
        assert chain.status == "pending"

    def test_steps_created_in_order(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob", "carol", "dave"])
        steps = dac.get_steps(chain.chain_id)
        assert [s.approver for s in steps] == ["bob", "carol", "dave"]
        assert [s.order for s in steps] == [0, 1, 2]

    def test_step_ids_are_unique(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob", "carol"])
        steps = dac.get_steps(chain.chain_id)
        ids = [s.step_id for s in steps]
        assert len(ids) == len(set(ids))

    def test_created_at_uses_now_param(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob"], now=1234.0)
        assert chain.created_at == 1234.0

    def test_doc_id_and_created_by(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("mydoc", "creator", ["approver"])
        assert chain.doc_id == "mydoc"
        assert chain.created_by == "creator"


# ---------------------------------------------------------------------------
# get_chain
# ---------------------------------------------------------------------------


class TestGetChain:
    def test_found(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob"])
        result = dac.get_chain(chain.chain_id)
        assert result is not None
        assert result.chain_id == chain.chain_id

    def test_not_found(self):
        dac = DocApprovalChain()
        assert dac.get_chain("nonexistent") is None


# ---------------------------------------------------------------------------
# get_steps
# ---------------------------------------------------------------------------


class TestGetSteps:
    def test_sorted_by_order(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["c", "b", "a"])
        steps = dac.get_steps(chain.chain_id)
        orders = [s.order for s in steps]
        assert orders == sorted(orders)

    def test_empty_for_unknown_chain(self):
        dac = DocApprovalChain()
        assert dac.get_steps("unknown") == []

    def test_all_steps_pending_initially(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob", "carol"])
        steps = dac.get_steps(chain.chain_id)
        assert all(s.status == "pending" for s in steps)


# ---------------------------------------------------------------------------
# current_step
# ---------------------------------------------------------------------------


class TestCurrentStep:
    def test_returns_first_step_initially(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob", "carol"])
        step = dac.current_step(chain.chain_id)
        assert step is not None
        assert step.order == 0
        assert step.approver == "bob"

    def test_none_when_no_steps(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", [])
        assert dac.current_step(chain.chain_id) is None

    def test_none_for_unknown_chain(self):
        dac = DocApprovalChain()
        assert dac.current_step("unknown") is None

    def test_advances_after_approve(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob", "carol"])
        dac.approve_step(chain.chain_id, "bob", now=1.0)
        step = dac.current_step(chain.chain_id)
        assert step is not None
        assert step.order == 1
        assert step.approver == "carol"

    def test_none_when_all_steps_complete(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob"])
        dac.approve_step(chain.chain_id, "bob", now=1.0)
        assert dac.current_step(chain.chain_id) is None


# ---------------------------------------------------------------------------
# approve_step
# ---------------------------------------------------------------------------


class TestApproveStep:
    def test_returns_approved_step(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob"])
        step = dac.approve_step(chain.chain_id, "bob", comment="OK", now=10.0)
        assert step is not None
        assert step.status == "approved"
        assert step.comment == "OK"
        assert step.decided_at == 10.0

    def test_advances_current_step_index(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob", "carol"])
        dac.approve_step(chain.chain_id, "bob", now=1.0)
        refreshed = dac.get_chain(chain.chain_id)
        assert refreshed.current_step == 1

    def test_last_approval_sets_chain_approved(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob"])
        dac.approve_step(chain.chain_id, "bob", now=1.0)
        refreshed = dac.get_chain(chain.chain_id)
        assert refreshed.status == "approved"

    def test_intermediate_approval_keeps_in_progress(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob", "carol"])
        dac.approve_step(chain.chain_id, "bob", now=1.0)
        refreshed = dac.get_chain(chain.chain_id)
        assert refreshed.status == "in_progress"

    def test_none_for_missing_chain(self):
        dac = DocApprovalChain()
        assert dac.approve_step("nonexistent", "bob") is None

    def test_none_when_no_pending_step(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob"])
        dac.approve_step(chain.chain_id, "bob", now=1.0)
        # Chain is approved now, no pending step
        result = dac.approve_step(chain.chain_id, "carol", now=2.0)
        assert result is None


# ---------------------------------------------------------------------------
# reject_step
# ---------------------------------------------------------------------------


class TestRejectStep:
    def test_returns_rejected_step(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob", "carol"])
        step = dac.reject_step(chain.chain_id, "bob", comment="No", now=5.0)
        assert step is not None
        assert step.status == "rejected"
        assert step.comment == "No"
        assert step.decided_at == 5.0

    def test_sets_chain_rejected(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob"])
        dac.reject_step(chain.chain_id, "bob", now=1.0)
        refreshed = dac.get_chain(chain.chain_id)
        assert refreshed.status == "rejected"

    def test_none_for_missing_chain(self):
        dac = DocApprovalChain()
        assert dac.reject_step("nonexistent", "bob") is None

    def test_none_when_no_pending_step(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", [])
        # No steps → no pending step
        assert dac.reject_step(chain.chain_id, "bob") is None


# ---------------------------------------------------------------------------
# cancel_chain
# ---------------------------------------------------------------------------


class TestCancelChain:
    def test_cancel_returns_true(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob"])
        assert dac.cancel_chain(chain.chain_id) is True

    def test_cancel_sets_status(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc1", "alice", ["bob"])
        dac.cancel_chain(chain.chain_id)
        refreshed = dac.get_chain(chain.chain_id)
        assert refreshed.status == "cancelled"

    def test_cancel_unknown_returns_false(self):
        dac = DocApprovalChain()
        assert dac.cancel_chain("unknown") is False


# ---------------------------------------------------------------------------
# chains_for_doc
# ---------------------------------------------------------------------------


class TestChainsForDoc:
    def test_returns_chains_for_doc(self):
        dac = DocApprovalChain()
        c1 = dac.create_chain("doc1", "alice", ["bob"], now=1.0)
        c2 = dac.create_chain("doc1", "alice", ["carol"], now=2.0)
        dac.create_chain("doc2", "alice", ["dave"], now=3.0)
        chains = dac.chains_for_doc("doc1")
        assert len(chains) == 2
        assert {c.chain_id for c in chains} == {c1.chain_id, c2.chain_id}

    def test_sorted_by_created_at(self):
        dac = DocApprovalChain()
        c2 = dac.create_chain("docX", "alice", [], now=2.0)
        c1 = dac.create_chain("docX", "alice", [], now=1.0)
        chains = dac.chains_for_doc("docX")
        assert chains[0].chain_id == c1.chain_id
        assert chains[1].chain_id == c2.chain_id

    def test_empty_for_unknown_doc(self):
        dac = DocApprovalChain()
        assert dac.chains_for_doc("nosuchdoc") == []


# ---------------------------------------------------------------------------
# chains_by_status
# ---------------------------------------------------------------------------


class TestChainsByStatus:
    def test_filters_by_status(self):
        dac = DocApprovalChain()
        c1 = dac.create_chain("d1", "alice", [], now=1.0)      # pending
        c2 = dac.create_chain("d2", "alice", ["bob"], now=2.0)  # in_progress
        c3 = dac.create_chain("d3", "alice", [], now=3.0)      # pending

        pending = dac.chains_by_status("pending")
        assert len(pending) == 2
        assert {c.chain_id for c in pending} == {c1.chain_id, c3.chain_id}

        in_progress = dac.chains_by_status("in_progress")
        assert len(in_progress) == 1
        assert in_progress[0].chain_id == c2.chain_id

    def test_sorted_by_created_at(self):
        dac = DocApprovalChain()
        c2 = dac.create_chain("d1", "alice", [], now=2.0)
        c1 = dac.create_chain("d2", "alice", [], now=1.0)
        result = dac.chains_by_status("pending")
        assert result[0].chain_id == c1.chain_id
        assert result[1].chain_id == c2.chain_id

    def test_empty_for_nonexistent_status(self):
        dac = DocApprovalChain()
        dac.create_chain("d1", "alice", [], now=1.0)
        assert dac.chains_by_status("approved") == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_counts_all_statuses(self):
        dac = DocApprovalChain()
        # pending (no approvers)
        dac.create_chain("d1", "u", [], now=1.0)
        # in_progress
        c2 = dac.create_chain("d2", "u", ["a"], now=2.0)
        # approved
        c3 = dac.create_chain("d3", "u", ["a"], now=3.0)
        dac.approve_step(c3.chain_id, "a", now=4.0)
        # rejected
        c4 = dac.create_chain("d4", "u", ["a"], now=5.0)
        dac.reject_step(c4.chain_id, "a", now=6.0)
        # cancelled
        c5 = dac.create_chain("d5", "u", ["a"], now=7.0)
        dac.cancel_chain(c5.chain_id)

        s = dac.stats()
        assert s.total_chains == 5
        assert s.pending == 1
        assert s.in_progress == 1
        assert s.approved == 1
        assert s.rejected == 1
        assert s.cancelled == 1

    def test_empty_stats(self):
        dac = DocApprovalChain()
        s = dac.stats()
        assert s.total_chains == 0


# ---------------------------------------------------------------------------
# Full workflow
# ---------------------------------------------------------------------------


class TestFullWorkflow:
    def test_create_approve_all_steps(self):
        dac = DocApprovalChain()
        approvers = ["alice", "bob", "carol"]
        chain = dac.create_chain("doc42", "owner", approvers, now=0.0)

        assert chain.status == "in_progress"

        for idx, approver in enumerate(approvers):
            step = dac.current_step(chain.chain_id)
            assert step is not None
            assert step.approver == approver
            assert step.order == idx

            result = dac.approve_step(chain.chain_id, approver, comment=f"OK by {approver}", now=float(idx + 1))
            assert result is not None
            assert result.status == "approved"

        final_chain = dac.get_chain(chain.chain_id)
        assert final_chain.status == "approved"
        assert dac.current_step(chain.chain_id) is None

        steps = dac.get_steps(chain.chain_id)
        assert all(s.status == "approved" for s in steps)

    def test_reject_mid_workflow(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc99", "owner", ["alice", "bob"], now=0.0)
        dac.approve_step(chain.chain_id, "alice", now=1.0)
        dac.reject_step(chain.chain_id, "bob", comment="Rejected", now=2.0)

        final = dac.get_chain(chain.chain_id)
        assert final.status == "rejected"

        steps = dac.get_steps(chain.chain_id)
        statuses = {s.approver: s.status for s in steps}
        assert statuses["alice"] == "approved"
        assert statuses["bob"] == "rejected"

    def test_cancel_workflow(self):
        dac = DocApprovalChain()
        chain = dac.create_chain("doc77", "owner", ["alice", "bob"], now=0.0)
        dac.cancel_chain(chain.chain_id)
        final = dac.get_chain(chain.chain_id)
        assert final.status == "cancelled"


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_create_chain(self):
        dac = DocApprovalChain()
        results: list[ApprovalChain] = []
        errors: list[Exception] = []
        lock = threading.Lock()

        def worker():
            try:
                chain = dac.create_chain("shared_doc", "user", ["approver"])
                with lock:
                    results.append(chain)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Errors in threads: {errors}"
        assert len(results) == 20
        chain_ids = [c.chain_id for c in results]
        assert len(chain_ids) == len(set(chain_ids)), "Duplicate chain IDs detected"

    def test_concurrent_approve(self):
        """Concurrent approvals on separate chains should not interfere."""
        dac = DocApprovalChain()
        chains = [dac.create_chain(f"doc{i}", "owner", ["alice"], now=float(i)) for i in range(10)]
        errors: list[Exception] = []
        lock = threading.Lock()

        def approve(chain_id: str):
            try:
                dac.approve_step(chain_id, "alice", now=99.0)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=approve, args=(c.chain_id,)) for c in chains]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        for c in chains:
            refreshed = dac.get_chain(c.chain_id)
            assert refreshed.status == "approved"
