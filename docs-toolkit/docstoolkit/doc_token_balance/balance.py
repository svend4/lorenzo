"""Token balance ledger per user/account.

Pure stdlib implementation, thread-safe via :class:`threading.Lock`.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Balance:
    """Current balance for an account."""

    account: str
    current: int
    total_credited: int = 0
    total_debited: int = 0


@dataclass
class Transaction:
    """A single balance transaction.

    Positive ``amount`` is a credit, negative is a debit.
    """

    tx_id: int = 0
    account: str = ""
    amount: int = 0
    reason: str = ""
    timestamp: float = 0.0
    balance_after: int = 0


@dataclass
class TokenBalanceStats:
    """Aggregate statistics across all accounts."""

    total_accounts: int
    total_balance: int
    total_credited_lifetime: int
    total_debited_lifetime: int
    total_transactions: int


class DocTokenBalance:
    """Token balance ledger keyed by account string."""

    def __init__(self) -> None:
        self._balances: dict[str, Balance] = {}
        self._transactions: list[Transaction] = []
        self._by_account: dict[str, list[int]] = {}
        self._next_tx_id: int = 1
        self._lock = threading.Lock()

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return time.time() if now is None else now

    def _record(
        self,
        account: str,
        amount: int,
        reason: str,
        timestamp: float,
        balance_after: int,
    ) -> Transaction:
        tx = Transaction(
            tx_id=self._next_tx_id,
            account=account,
            amount=amount,
            reason=reason,
            timestamp=timestamp,
            balance_after=balance_after,
        )
        self._next_tx_id += 1
        self._transactions.append(tx)
        idx = len(self._transactions) - 1
        self._by_account.setdefault(account, []).append(idx)
        return tx

    def credit(
        self,
        account: str,
        amount: int,
        reason: str = "",
        now: Optional[float] = None,
    ) -> Transaction:
        """Credit ``amount`` tokens to ``account``. ``amount`` must be > 0."""
        if amount <= 0:
            raise ValueError("credit amount must be positive")
        ts = self._now(now)
        with self._lock:
            bal = self._balances.get(account)
            if bal is None:
                bal = Balance(account=account, current=0)
                self._balances[account] = bal
            bal.current += amount
            bal.total_credited += amount
            return self._record(account, amount, reason, ts, bal.current)

    def debit(
        self,
        account: str,
        amount: int,
        reason: str = "",
        allow_negative: bool = False,
        now: Optional[float] = None,
    ) -> Optional[Transaction]:
        """Debit ``amount`` tokens from ``account``.

        Returns ``None`` if insufficient funds and ``allow_negative`` is False.
        """
        if amount <= 0:
            raise ValueError("debit amount must be positive")
        ts = self._now(now)
        with self._lock:
            bal = self._balances.get(account)
            if bal is None:
                bal = Balance(account=account, current=0)
                self._balances[account] = bal
            if not allow_negative and bal.current < amount:
                return None
            bal.current -= amount
            bal.total_debited += amount
            return self._record(account, -amount, reason, ts, bal.current)

    def balance_of(self, account: str) -> int:
        """Return current balance for ``account`` (0 if not found)."""
        with self._lock:
            bal = self._balances.get(account)
            return bal.current if bal is not None else 0

    def get_balance(self, account: str) -> Optional[Balance]:
        """Return the :class:`Balance` object for ``account`` or ``None``."""
        with self._lock:
            return self._balances.get(account)

    def transactions_for(
        self, account: str, limit: Optional[int] = None
    ) -> list[Transaction]:
        """Return transactions for ``account``, most recent first."""
        with self._lock:
            idxs = self._by_account.get(account, [])
            result = [self._transactions[i] for i in reversed(idxs)]
            if limit is not None:
                result = result[:limit]
            return result

    def transactions_in_range(self, start: float, end: float) -> list[Transaction]:
        """Return transactions in ``[start, end]`` (inclusive), sorted by ts asc."""
        with self._lock:
            txs = [t for t in self._transactions if start <= t.timestamp <= end]
        txs.sort(key=lambda t: t.timestamp)
        return txs

    def top_accounts_by_balance(self, limit: int = 10) -> list[tuple]:
        """Return ``(account, balance)`` pairs sorted by balance desc."""
        with self._lock:
            items = [(a, b.current) for a, b in self._balances.items()]
        items.sort(key=lambda x: x[1], reverse=True)
        return items[:limit]

    def transfer(
        self,
        from_account: str,
        to_account: str,
        amount: int,
        reason: str = "",
        now: Optional[float] = None,
    ) -> Optional[tuple]:
        """Transfer ``amount`` from ``from_account`` to ``to_account``.

        Returns ``(debit_tx, credit_tx)`` or ``None`` if insufficient funds.
        """
        if amount <= 0:
            raise ValueError("transfer amount must be positive")
        if from_account == to_account:
            raise ValueError("cannot transfer to same account")
        ts = self._now(now)
        with self._lock:
            src = self._balances.get(from_account)
            if src is None or src.current < amount:
                return None
            src.current -= amount
            src.total_debited += amount
            debit_tx = self._record(
                from_account, -amount, reason, ts, src.current
            )

            dst = self._balances.get(to_account)
            if dst is None:
                dst = Balance(account=to_account, current=0)
                self._balances[to_account] = dst
            dst.current += amount
            dst.total_credited += amount
            credit_tx = self._record(to_account, amount, reason, ts, dst.current)

            return (debit_tx, credit_tx)

    def set_balance(
        self,
        account: str,
        new_balance: int,
        reason: str = "adjustment",
        now: Optional[float] = None,
    ) -> Transaction:
        """Set ``account`` balance to ``new_balance``, recording an adjustment."""
        ts = self._now(now)
        with self._lock:
            bal = self._balances.get(account)
            if bal is None:
                bal = Balance(account=account, current=0)
                self._balances[account] = bal
            delta = new_balance - bal.current
            bal.current = new_balance
            if delta > 0:
                bal.total_credited += delta
            elif delta < 0:
                bal.total_debited += -delta
            return self._record(account, delta, reason, ts, bal.current)

    def all_accounts(self) -> list[str]:
        """Return sorted list of all account names."""
        with self._lock:
            return sorted(self._balances.keys())

    def clear_account(self, account: str) -> bool:
        """Remove all balance and transactions for ``account``.

        Returns True if the account existed, else False.
        """
        with self._lock:
            existed = account in self._balances or account in self._by_account
            if not existed:
                return False
            self._balances.pop(account, None)
            idxs = self._by_account.pop(account, [])
            # Remove from main transaction list (rebuild indices for remaining).
            if idxs:
                remove_set = set(idxs)
                new_txs: list[Transaction] = []
                old_to_new: dict[int, int] = {}
                for old_idx, tx in enumerate(self._transactions):
                    if old_idx in remove_set:
                        continue
                    old_to_new[old_idx] = len(new_txs)
                    new_txs.append(tx)
                self._transactions = new_txs
                # Rebuild per-account index mappings.
                new_by_account: dict[str, list[int]] = {}
                for acct, acct_idxs in self._by_account.items():
                    mapped = [old_to_new[i] for i in acct_idxs if i in old_to_new]
                    new_by_account[acct] = mapped
                self._by_account = new_by_account
            return True

    def stats(self) -> TokenBalanceStats:
        """Return aggregate :class:`TokenBalanceStats`."""
        with self._lock:
            total_balance = sum(b.current for b in self._balances.values())
            credited = sum(b.total_credited for b in self._balances.values())
            debited = sum(b.total_debited for b in self._balances.values())
            return TokenBalanceStats(
                total_accounts=len(self._balances),
                total_balance=total_balance,
                total_credited_lifetime=credited,
                total_debited_lifetime=debited,
                total_transactions=len(self._transactions),
            )
