"""Tests for E434 DocTokenBalance."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_token_balance import (
    Balance,
    DocTokenBalance,
    TokenBalanceStats,
    Transaction,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestBalanceDataclass:
    def test_construct_basic(self):
        b = Balance(account="alice", current=100)
        assert b.account == "alice"
        assert b.current == 100
        assert b.total_credited == 0
        assert b.total_debited == 0

    def test_construct_full(self):
        b = Balance(account="a", current=10, total_credited=20, total_debited=10)
        assert b.total_credited == 20
        assert b.total_debited == 10

    def test_mutable(self):
        b = Balance(account="a", current=0)
        b.current = 5
        assert b.current == 5

    def test_equality(self):
        b1 = Balance(account="a", current=1)
        b2 = Balance(account="a", current=1)
        assert b1 == b2


class TestTransactionDataclass:
    def test_construct_default(self):
        t = Transaction()
        assert t.tx_id == 0
        assert t.account == ""
        assert t.amount == 0
        assert t.reason == ""
        assert t.timestamp == 0.0
        assert t.balance_after == 0

    def test_construct_full(self):
        t = Transaction(
            tx_id=1,
            account="a",
            amount=5,
            reason="topup",
            timestamp=10.0,
            balance_after=5,
        )
        assert t.tx_id == 1
        assert t.amount == 5
        assert t.reason == "topup"
        assert t.timestamp == 10.0
        assert t.balance_after == 5

    def test_negative_amount_means_debit(self):
        t = Transaction(tx_id=2, account="a", amount=-3)
        assert t.amount == -3


class TestTokenBalanceStatsDataclass:
    def test_construct(self):
        s = TokenBalanceStats(
            total_accounts=1,
            total_balance=10,
            total_credited_lifetime=20,
            total_debited_lifetime=10,
            total_transactions=3,
        )
        assert s.total_accounts == 1
        assert s.total_balance == 10
        assert s.total_credited_lifetime == 20
        assert s.total_debited_lifetime == 10
        assert s.total_transactions == 3


# ---------------------------------------------------------------------------
# credit()
# ---------------------------------------------------------------------------


class TestCredit:
    def test_credit_new_account(self):
        ledger = DocTokenBalance()
        tx = ledger.credit("alice", 100)
        assert tx.amount == 100
        assert tx.balance_after == 100
        assert tx.account == "alice"

    def test_credit_increments_balance(self):
        ledger = DocTokenBalance()
        ledger.credit("alice", 50)
        ledger.credit("alice", 25)
        assert ledger.balance_of("alice") == 75

    def test_credit_zero_raises(self):
        ledger = DocTokenBalance()
        with pytest.raises(ValueError):
            ledger.credit("a", 0)

    def test_credit_negative_raises(self):
        ledger = DocTokenBalance()
        with pytest.raises(ValueError):
            ledger.credit("a", -5)

    def test_credit_records_reason(self):
        ledger = DocTokenBalance()
        tx = ledger.credit("a", 1, reason="signup-bonus")
        assert tx.reason == "signup-bonus"

    def test_credit_uses_provided_now(self):
        ledger = DocTokenBalance()
        tx = ledger.credit("a", 1, now=42.0)
        assert tx.timestamp == 42.0

    def test_credit_tx_ids_increment(self):
        ledger = DocTokenBalance()
        t1 = ledger.credit("a", 1)
        t2 = ledger.credit("b", 1)
        assert t1.tx_id == 1
        assert t2.tx_id == 2

    def test_credit_updates_total_credited(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 10)
        ledger.credit("a", 5)
        bal = ledger.get_balance("a")
        assert bal.total_credited == 15
        assert bal.total_debited == 0


# ---------------------------------------------------------------------------
# debit()
# ---------------------------------------------------------------------------


class TestDebit:
    def test_debit_basic(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 100)
        tx = ledger.debit("a", 30)
        assert tx is not None
        assert tx.amount == -30
        assert tx.balance_after == 70

    def test_debit_insufficient_returns_none(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 5)
        assert ledger.debit("a", 10) is None
        assert ledger.balance_of("a") == 5

    def test_debit_allow_negative(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 5)
        tx = ledger.debit("a", 10, allow_negative=True)
        assert tx is not None
        assert tx.balance_after == -5

    def test_debit_unknown_account_returns_none(self):
        ledger = DocTokenBalance()
        assert ledger.debit("ghost", 1) is None

    def test_debit_unknown_account_allow_negative(self):
        ledger = DocTokenBalance()
        tx = ledger.debit("ghost", 5, allow_negative=True)
        assert tx is not None
        assert ledger.balance_of("ghost") == -5

    def test_debit_zero_raises(self):
        ledger = DocTokenBalance()
        with pytest.raises(ValueError):
            ledger.debit("a", 0)

    def test_debit_negative_raises(self):
        ledger = DocTokenBalance()
        with pytest.raises(ValueError):
            ledger.debit("a", -1)

    def test_debit_updates_total_debited(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 100)
        ledger.debit("a", 10)
        ledger.debit("a", 5)
        bal = ledger.get_balance("a")
        assert bal.total_debited == 15
        assert bal.current == 85

    def test_debit_uses_provided_now(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 10, now=1.0)
        tx = ledger.debit("a", 1, now=99.0)
        assert tx.timestamp == 99.0


# ---------------------------------------------------------------------------
# balance_of / get_balance
# ---------------------------------------------------------------------------


class TestBalanceQueries:
    def test_balance_of_missing(self):
        ledger = DocTokenBalance()
        assert ledger.balance_of("nope") == 0

    def test_balance_of_known(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 42)
        assert ledger.balance_of("a") == 42

    def test_get_balance_missing(self):
        ledger = DocTokenBalance()
        assert ledger.get_balance("nope") is None

    def test_get_balance_returns_object(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 5)
        bal = ledger.get_balance("a")
        assert isinstance(bal, Balance)
        assert bal.account == "a"
        assert bal.current == 5


# ---------------------------------------------------------------------------
# transactions_for
# ---------------------------------------------------------------------------


class TestTransactionsFor:
    def test_empty_for_unknown(self):
        ledger = DocTokenBalance()
        assert ledger.transactions_for("ghost") == []

    def test_most_recent_first(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 1, now=1.0)
        ledger.credit("a", 2, now=2.0)
        ledger.credit("a", 3, now=3.0)
        txs = ledger.transactions_for("a")
        assert [t.amount for t in txs] == [3, 2, 1]

    def test_limit(self):
        ledger = DocTokenBalance()
        for i in range(5):
            ledger.credit("a", i + 1)
        txs = ledger.transactions_for("a", limit=2)
        assert len(txs) == 2
        assert txs[0].amount == 5
        assert txs[1].amount == 4

    def test_only_for_that_account(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 1)
        ledger.credit("b", 2)
        txs = ledger.transactions_for("a")
        assert len(txs) == 1
        assert txs[0].account == "a"


# ---------------------------------------------------------------------------
# transactions_in_range
# ---------------------------------------------------------------------------


class TestTransactionsInRange:
    def test_empty(self):
        ledger = DocTokenBalance()
        assert ledger.transactions_in_range(0, 100) == []

    def test_inclusive_endpoints(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 1, now=10.0)
        ledger.credit("a", 2, now=20.0)
        txs = ledger.transactions_in_range(10.0, 20.0)
        assert len(txs) == 2

    def test_excludes_outside(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 1, now=5.0)
        ledger.credit("a", 2, now=15.0)
        ledger.credit("a", 3, now=25.0)
        txs = ledger.transactions_in_range(10.0, 20.0)
        assert len(txs) == 1
        assert txs[0].amount == 2

    def test_sorted_ascending(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 1, now=30.0)
        ledger.credit("a", 2, now=10.0)
        ledger.credit("a", 3, now=20.0)
        txs = ledger.transactions_in_range(0, 100)
        assert [t.timestamp for t in txs] == [10.0, 20.0, 30.0]


# ---------------------------------------------------------------------------
# top_accounts_by_balance
# ---------------------------------------------------------------------------


class TestTopAccounts:
    def test_empty(self):
        ledger = DocTokenBalance()
        assert ledger.top_accounts_by_balance() == []

    def test_sorted_desc(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 5)
        ledger.credit("b", 10)
        ledger.credit("c", 1)
        top = ledger.top_accounts_by_balance()
        assert top == [("b", 10), ("a", 5), ("c", 1)]

    def test_limit(self):
        ledger = DocTokenBalance()
        for i, name in enumerate(["a", "b", "c", "d"]):
            ledger.credit(name, (i + 1) * 10)
        top = ledger.top_accounts_by_balance(limit=2)
        assert len(top) == 2
        assert top[0] == ("d", 40)
        assert top[1] == ("c", 30)


# ---------------------------------------------------------------------------
# transfer
# ---------------------------------------------------------------------------


class TestTransfer:
    def test_transfer_basic(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 100)
        result = ledger.transfer("a", "b", 30)
        assert result is not None
        debit_tx, credit_tx = result
        assert debit_tx.amount == -30
        assert credit_tx.amount == 30
        assert ledger.balance_of("a") == 70
        assert ledger.balance_of("b") == 30

    def test_transfer_insufficient_returns_none(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 5)
        assert ledger.transfer("a", "b", 10) is None
        assert ledger.balance_of("a") == 5
        assert ledger.balance_of("b") == 0

    def test_transfer_from_unknown(self):
        ledger = DocTokenBalance()
        assert ledger.transfer("ghost", "b", 1) is None

    def test_transfer_to_self_raises(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 10)
        with pytest.raises(ValueError):
            ledger.transfer("a", "a", 1)

    def test_transfer_zero_raises(self):
        ledger = DocTokenBalance()
        with pytest.raises(ValueError):
            ledger.transfer("a", "b", 0)

    def test_transfer_negative_raises(self):
        ledger = DocTokenBalance()
        with pytest.raises(ValueError):
            ledger.transfer("a", "b", -5)

    def test_transfer_records_reason(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 100)
        d, c = ledger.transfer("a", "b", 10, reason="refund")
        assert d.reason == "refund"
        assert c.reason == "refund"

    def test_transfer_uses_now(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 100, now=1.0)
        d, c = ledger.transfer("a", "b", 10, now=42.0)
        assert d.timestamp == 42.0
        assert c.timestamp == 42.0


# ---------------------------------------------------------------------------
# set_balance
# ---------------------------------------------------------------------------


class TestSetBalance:
    def test_set_balance_new_account(self):
        ledger = DocTokenBalance()
        tx = ledger.set_balance("a", 50)
        assert tx.amount == 50
        assert tx.balance_after == 50
        assert ledger.balance_of("a") == 50

    def test_set_balance_up(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 10)
        tx = ledger.set_balance("a", 30)
        assert tx.amount == 20
        assert ledger.balance_of("a") == 30
        bal = ledger.get_balance("a")
        assert bal.total_credited == 30  # 10 initial + 20 adjust

    def test_set_balance_down(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 50)
        tx = ledger.set_balance("a", 20)
        assert tx.amount == -30
        assert ledger.balance_of("a") == 20
        bal = ledger.get_balance("a")
        assert bal.total_debited == 30

    def test_set_balance_no_change(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 5)
        tx = ledger.set_balance("a", 5)
        assert tx.amount == 0
        assert tx.balance_after == 5

    def test_set_balance_default_reason(self):
        ledger = DocTokenBalance()
        tx = ledger.set_balance("a", 10)
        assert tx.reason == "adjustment"

    def test_set_balance_custom_reason(self):
        ledger = DocTokenBalance()
        tx = ledger.set_balance("a", 10, reason="manual-correction")
        assert tx.reason == "manual-correction"


# ---------------------------------------------------------------------------
# all_accounts
# ---------------------------------------------------------------------------


class TestAllAccounts:
    def test_empty(self):
        ledger = DocTokenBalance()
        assert ledger.all_accounts() == []

    def test_sorted(self):
        ledger = DocTokenBalance()
        ledger.credit("zeta", 1)
        ledger.credit("alpha", 1)
        ledger.credit("mu", 1)
        assert ledger.all_accounts() == ["alpha", "mu", "zeta"]


# ---------------------------------------------------------------------------
# clear_account
# ---------------------------------------------------------------------------


class TestClearAccount:
    def test_clear_unknown(self):
        ledger = DocTokenBalance()
        assert ledger.clear_account("ghost") is False

    def test_clear_existing_returns_true(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 10)
        assert ledger.clear_account("a") is True

    def test_clear_removes_balance(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 10)
        ledger.clear_account("a")
        assert ledger.balance_of("a") == 0
        assert ledger.get_balance("a") is None
        assert "a" not in ledger.all_accounts()

    def test_clear_removes_transactions(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 10)
        ledger.debit("a", 3)
        ledger.clear_account("a")
        assert ledger.transactions_for("a") == []

    def test_clear_preserves_other_accounts(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 10)
        ledger.credit("b", 20)
        ledger.debit("b", 5)
        ledger.clear_account("a")
        assert ledger.balance_of("b") == 15
        b_txs = ledger.transactions_for("b")
        assert len(b_txs) == 2
        # Order: most-recent first; latest is the -5 debit.
        assert b_txs[0].amount == -5
        assert b_txs[1].amount == 20

    def test_clear_then_recreate(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 10)
        ledger.clear_account("a")
        ledger.credit("a", 7)
        assert ledger.balance_of("a") == 7


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_stats_empty(self):
        ledger = DocTokenBalance()
        s = ledger.stats()
        assert s.total_accounts == 0
        assert s.total_balance == 0
        assert s.total_credited_lifetime == 0
        assert s.total_debited_lifetime == 0
        assert s.total_transactions == 0

    def test_stats_with_activity(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 100)
        ledger.credit("b", 50)
        ledger.debit("a", 30)
        s = ledger.stats()
        assert s.total_accounts == 2
        assert s.total_balance == 120  # 70 + 50
        assert s.total_credited_lifetime == 150
        assert s.total_debited_lifetime == 30
        assert s.total_transactions == 3

    def test_stats_after_transfer(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 100)
        ledger.transfer("a", "b", 40)
        s = ledger.stats()
        # transfer counts as 1 debit + 1 credit, plus original credit.
        assert s.total_transactions == 3
        assert s.total_balance == 100  # 60 + 40


# ---------------------------------------------------------------------------
# Thread-safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_credits(self):
        ledger = DocTokenBalance()
        n_threads = 10
        per_thread = 100

        def worker():
            for _ in range(per_thread):
                ledger.credit("shared", 1)

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert ledger.balance_of("shared") == n_threads * per_thread
        assert ledger.stats().total_transactions == n_threads * per_thread

    def test_concurrent_debits_no_overdraft(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 100)
        results = []

        def worker():
            r = ledger.debit("a", 1)
            results.append(r)

        threads = [threading.Thread(target=worker) for _ in range(200)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Exactly 100 successes, 100 failures, never negative.
        successes = [r for r in results if r is not None]
        failures = [r for r in results if r is None]
        assert len(successes) == 100
        assert len(failures) == 100
        assert ledger.balance_of("a") == 0

    def test_concurrent_transfers_contention(self):
        """Many threads transferring between two accounts must never overdraft."""
        ledger = DocTokenBalance()
        ledger.credit("a", 500)
        ledger.credit("b", 500)

        outcomes = {"ok": 0, "fail": 0}
        lock = threading.Lock()

        def worker(direction: str):
            for _ in range(50):
                if direction == "ab":
                    r = ledger.transfer("a", "b", 1)
                else:
                    r = ledger.transfer("b", "a", 1)
                with lock:
                    if r is None:
                        outcomes["fail"] += 1
                    else:
                        outcomes["ok"] += 1

        threads = []
        for _ in range(10):
            threads.append(threading.Thread(target=worker, args=("ab",)))
            threads.append(threading.Thread(target=worker, args=("ba",)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Total tokens are conserved.
        assert ledger.balance_of("a") + ledger.balance_of("b") == 1000
        # Both accounts must remain non-negative.
        assert ledger.balance_of("a") >= 0
        assert ledger.balance_of("b") >= 0
        # Total ok + fail equals total attempts.
        assert outcomes["ok"] + outcomes["fail"] == 20 * 50

    def test_concurrent_mixed_operations(self):
        ledger = DocTokenBalance()
        ledger.credit("a", 1000)

        def credit_worker():
            for _ in range(50):
                ledger.credit("a", 2)

        def debit_worker():
            for _ in range(50):
                ledger.debit("a", 1)

        threads = [
            threading.Thread(target=credit_worker),
            threading.Thread(target=credit_worker),
            threading.Thread(target=debit_worker),
            threading.Thread(target=debit_worker),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Started 1000, credited +200, debited -100 → 1100
        assert ledger.balance_of("a") == 1100
