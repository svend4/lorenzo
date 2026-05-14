"""Tests for E436 DocInviteLink."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_invite_link import DocInviteLink, InviteLink, LinkStats


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def reg() -> DocInviteLink:
    return DocInviteLink()


# ---------------------------------------------------------------------------
# Dataclass-level tests
# ---------------------------------------------------------------------------


def test_invite_link_defaults():
    link = InviteLink(link_id="x", doc_id="d", created_by="u")
    assert link.created_at == 0.0
    assert link.expires_at is None
    assert link.max_uses is None
    assert link.use_count == 0
    assert link.revoked is False


def test_invite_link_is_expired_none():
    link = InviteLink(link_id="x", doc_id="d", created_by="u", expires_at=None)
    assert not link.is_expired(now=999.0)


def test_invite_link_is_expired_future():
    link = InviteLink(link_id="x", doc_id="d", created_by="u", expires_at=100.0)
    assert not link.is_expired(now=50.0)


def test_invite_link_is_expired_past():
    link = InviteLink(link_id="x", doc_id="d", created_by="u", expires_at=100.0)
    assert link.is_expired(now=200.0)


def test_invite_link_is_expired_exact_boundary():
    link = InviteLink(link_id="x", doc_id="d", created_by="u", expires_at=100.0)
    assert link.is_expired(now=100.0)


def test_invite_link_is_exhausted_none():
    link = InviteLink(link_id="x", doc_id="d", created_by="u", max_uses=None, use_count=999)
    assert not link.is_exhausted()


def test_invite_link_is_exhausted_under():
    link = InviteLink(link_id="x", doc_id="d", created_by="u", max_uses=3, use_count=1)
    assert not link.is_exhausted()


def test_invite_link_is_exhausted_equal():
    link = InviteLink(link_id="x", doc_id="d", created_by="u", max_uses=3, use_count=3)
    assert link.is_exhausted()


def test_invite_link_is_valid_default():
    link = InviteLink(link_id="x", doc_id="d", created_by="u")
    assert link.is_valid(now=0.0)


def test_invite_link_is_valid_revoked():
    link = InviteLink(link_id="x", doc_id="d", created_by="u", revoked=True)
    assert not link.is_valid(now=0.0)


def test_link_stats_dataclass():
    s = LinkStats(total_links=1, active_links=2, revoked_count=3, total_uses=4)
    assert s.total_links == 1
    assert s.active_links == 2
    assert s.revoked_count == 3
    assert s.total_uses == 4


# ---------------------------------------------------------------------------
# create_link
# ---------------------------------------------------------------------------


def test_create_link_basic(reg):
    link = reg.create_link("doc1", "alice", now=100.0)
    assert isinstance(link, InviteLink)
    assert link.doc_id == "doc1"
    assert link.created_by == "alice"
    assert link.created_at == 100.0
    assert link.expires_at is None
    assert link.max_uses is None
    assert link.use_count == 0
    assert link.revoked is False
    assert link.link_id  # non-empty


def test_create_link_unique_ids(reg):
    link_ids = {reg.create_link("d", "u").link_id for _ in range(50)}
    assert len(link_ids) == 50


def test_create_link_with_expires_at(reg):
    link = reg.create_link("doc1", "alice", expires_at=200.0, now=100.0)
    assert link.expires_at == 200.0


def test_create_link_duration_overrides_expires_at(reg):
    link = reg.create_link(
        "doc1", "alice", expires_at=999.0, duration_seconds=50.0, now=100.0
    )
    assert link.expires_at == 150.0


def test_create_link_with_duration_only(reg):
    link = reg.create_link("doc1", "alice", duration_seconds=30.0, now=100.0)
    assert link.expires_at == 130.0


def test_create_link_with_max_uses(reg):
    link = reg.create_link("doc1", "alice", max_uses=5)
    assert link.max_uses == 5


def test_create_link_max_uses_invalid(reg):
    with pytest.raises(ValueError):
        reg.create_link("doc1", "alice", max_uses=0)


def test_create_link_max_uses_negative(reg):
    with pytest.raises(ValueError):
        reg.create_link("doc1", "alice", max_uses=-3)


def test_create_link_duration_negative(reg):
    with pytest.raises(ValueError):
        reg.create_link("doc1", "alice", duration_seconds=-1.0)


def test_create_link_default_now_uses_clock(reg):
    before = time.time()
    link = reg.create_link("doc1", "alice")
    after = time.time()
    assert before <= link.created_at <= after


def test_create_link_registered_in_by_doc(reg):
    link = reg.create_link("doc1", "alice")
    found = reg.links_for_doc("doc1", include_invalid=True)
    assert link.link_id in [l.link_id for l in found]


def test_create_link_multiple_for_same_doc(reg):
    l1 = reg.create_link("doc1", "alice", now=1.0)
    l2 = reg.create_link("doc1", "bob", now=2.0)
    ids = [l.link_id for l in reg.links_for_doc("doc1", include_invalid=True)]
    assert set(ids) == {l1.link_id, l2.link_id}


# ---------------------------------------------------------------------------
# use_link
# ---------------------------------------------------------------------------


def test_use_link_success(reg):
    link = reg.create_link("doc1", "alice", now=100.0)
    assert reg.use_link(link.link_id, now=110.0) is True
    assert reg.get_link(link.link_id).use_count == 1


def test_use_link_unknown(reg):
    assert reg.use_link("nope") is False


def test_use_link_revoked(reg):
    link = reg.create_link("doc1", "alice")
    reg.revoke(link.link_id)
    assert reg.use_link(link.link_id) is False
    assert reg.get_link(link.link_id).use_count == 0


def test_use_link_expired(reg):
    link = reg.create_link("doc1", "alice", expires_at=200.0, now=100.0)
    assert reg.use_link(link.link_id, now=250.0) is False
    assert reg.get_link(link.link_id).use_count == 0


def test_use_link_max_uses_increments(reg):
    link = reg.create_link("doc1", "alice", max_uses=2)
    assert reg.use_link(link.link_id) is True
    assert reg.use_link(link.link_id) is True
    assert reg.get_link(link.link_id).use_count == 2


def test_use_link_max_uses_exhausted(reg):
    link = reg.create_link("doc1", "alice", max_uses=2)
    reg.use_link(link.link_id)
    reg.use_link(link.link_id)
    assert reg.use_link(link.link_id) is False
    assert reg.get_link(link.link_id).use_count == 2


def test_use_link_unlimited_max_uses(reg):
    link = reg.create_link("doc1", "alice")
    for _ in range(100):
        assert reg.use_link(link.link_id) is True
    assert reg.get_link(link.link_id).use_count == 100


def test_use_link_default_now(reg):
    link = reg.create_link("doc1", "alice")
    assert reg.use_link(link.link_id) is True


# ---------------------------------------------------------------------------
# is_valid
# ---------------------------------------------------------------------------


def test_is_valid_known(reg):
    link = reg.create_link("doc1", "alice")
    assert reg.is_valid(link.link_id) is True


def test_is_valid_unknown(reg):
    assert reg.is_valid("nope") is False


def test_is_valid_revoked(reg):
    link = reg.create_link("doc1", "alice")
    reg.revoke(link.link_id)
    assert reg.is_valid(link.link_id) is False


def test_is_valid_expired(reg):
    link = reg.create_link("doc1", "alice", expires_at=100.0, now=50.0)
    assert reg.is_valid(link.link_id, now=200.0) is False


def test_is_valid_exhausted(reg):
    link = reg.create_link("doc1", "alice", max_uses=1)
    reg.use_link(link.link_id)
    assert reg.is_valid(link.link_id) is False


# ---------------------------------------------------------------------------
# revoke
# ---------------------------------------------------------------------------


def test_revoke_known(reg):
    link = reg.create_link("doc1", "alice")
    assert reg.revoke(link.link_id) is True
    assert reg.get_link(link.link_id).revoked is True


def test_revoke_unknown(reg):
    assert reg.revoke("nope") is False


def test_revoke_idempotent(reg):
    link = reg.create_link("doc1", "alice")
    reg.revoke(link.link_id)
    assert reg.revoke(link.link_id) is False


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------


def test_delete_known(reg):
    link = reg.create_link("doc1", "alice")
    assert reg.delete(link.link_id) is True
    assert reg.get_link(link.link_id) is None


def test_delete_unknown(reg):
    assert reg.delete("nope") is False


def test_delete_removes_from_by_doc(reg):
    link = reg.create_link("doc1", "alice")
    reg.delete(link.link_id)
    assert reg.links_for_doc("doc1", include_invalid=True) == []


def test_delete_keeps_other_links_for_doc(reg):
    l1 = reg.create_link("doc1", "alice", now=1.0)
    l2 = reg.create_link("doc1", "bob", now=2.0)
    reg.delete(l1.link_id)
    remaining = reg.links_for_doc("doc1", include_invalid=True)
    assert [l.link_id for l in remaining] == [l2.link_id]


# ---------------------------------------------------------------------------
# get_link
# ---------------------------------------------------------------------------


def test_get_link_known(reg):
    link = reg.create_link("doc1", "alice")
    assert reg.get_link(link.link_id) is link


def test_get_link_unknown(reg):
    assert reg.get_link("nope") is None


# ---------------------------------------------------------------------------
# links_for_doc
# ---------------------------------------------------------------------------


def test_links_for_doc_empty(reg):
    assert reg.links_for_doc("doc1") == []


def test_links_for_doc_sorted_desc(reg):
    l1 = reg.create_link("doc1", "u", now=1.0)
    l2 = reg.create_link("doc1", "u", now=2.0)
    l3 = reg.create_link("doc1", "u", now=3.0)
    result = reg.links_for_doc("doc1")
    assert [l.link_id for l in result] == [l3.link_id, l2.link_id, l1.link_id]


def test_links_for_doc_excludes_invalid_by_default(reg):
    good = reg.create_link("doc1", "u", now=1.0)
    bad = reg.create_link("doc1", "u", now=2.0)
    reg.revoke(bad.link_id)
    result = reg.links_for_doc("doc1")
    assert [l.link_id for l in result] == [good.link_id]


def test_links_for_doc_includes_invalid_when_asked(reg):
    good = reg.create_link("doc1", "u", now=1.0)
    bad = reg.create_link("doc1", "u", now=2.0)
    reg.revoke(bad.link_id)
    result = reg.links_for_doc("doc1", include_invalid=True)
    assert {l.link_id for l in result} == {good.link_id, bad.link_id}


def test_links_for_doc_isolated_per_doc(reg):
    a = reg.create_link("doc1", "u")
    b = reg.create_link("doc2", "u")
    ids_a = [l.link_id for l in reg.links_for_doc("doc1")]
    ids_b = [l.link_id for l in reg.links_for_doc("doc2")]
    assert ids_a == [a.link_id]
    assert ids_b == [b.link_id]


# ---------------------------------------------------------------------------
# active / expired / exhausted
# ---------------------------------------------------------------------------


def test_active_links_only_valid(reg):
    a = reg.create_link("d1", "u", now=1.0)
    b = reg.create_link("d2", "u", now=2.0)
    c = reg.create_link("d3", "u", expires_at=10.0, now=3.0)
    reg.revoke(b.link_id)
    result = reg.active_links(now=50.0)
    assert [l.link_id for l in result] == [a.link_id]


def test_active_links_sorted_desc(reg):
    l1 = reg.create_link("d", "u", now=1.0)
    l2 = reg.create_link("d", "u", now=2.0)
    result = reg.active_links()
    assert [l.link_id for l in result] == [l2.link_id, l1.link_id]


def test_expired_links(reg):
    a = reg.create_link("d", "u", expires_at=100.0, now=50.0)
    b = reg.create_link("d", "u", now=60.0)
    result = reg.expired_links(now=200.0)
    assert [l.link_id for l in result] == [a.link_id]
    assert b.link_id not in [l.link_id for l in result]


def test_expired_links_sorted_desc(reg):
    a = reg.create_link("d", "u", expires_at=10.0, now=1.0)
    b = reg.create_link("d", "u", expires_at=10.0, now=2.0)
    result = reg.expired_links(now=100.0)
    assert [l.link_id for l in result] == [b.link_id, a.link_id]


def test_exhausted_links(reg):
    a = reg.create_link("d", "u", max_uses=1)
    b = reg.create_link("d", "u", max_uses=5)
    reg.use_link(a.link_id)
    reg.use_link(b.link_id)
    result = reg.exhausted_links()
    assert [l.link_id for l in result] == [a.link_id]


def test_exhausted_links_empty(reg):
    reg.create_link("d", "u")
    assert reg.exhausted_links() == []


# ---------------------------------------------------------------------------
# revoke_all_for_doc
# ---------------------------------------------------------------------------


def test_revoke_all_for_doc_counts(reg):
    a = reg.create_link("doc1", "u")
    b = reg.create_link("doc1", "u")
    c = reg.create_link("doc2", "u")
    count = reg.revoke_all_for_doc("doc1")
    assert count == 2
    assert reg.get_link(a.link_id).revoked is True
    assert reg.get_link(b.link_id).revoked is True
    assert reg.get_link(c.link_id).revoked is False


def test_revoke_all_for_doc_skips_already_revoked(reg):
    a = reg.create_link("doc1", "u")
    b = reg.create_link("doc1", "u")
    reg.revoke(a.link_id)
    count = reg.revoke_all_for_doc("doc1")
    assert count == 1
    assert reg.get_link(b.link_id).revoked is True


def test_revoke_all_for_doc_unknown(reg):
    assert reg.revoke_all_for_doc("nope") == 0


# ---------------------------------------------------------------------------
# purge_invalid
# ---------------------------------------------------------------------------


def test_purge_invalid_removes_revoked(reg):
    a = reg.create_link("d", "u")
    reg.revoke(a.link_id)
    assert reg.purge_invalid() == 1
    assert reg.get_link(a.link_id) is None


def test_purge_invalid_removes_expired(reg):
    a = reg.create_link("d", "u", expires_at=10.0, now=1.0)
    assert reg.purge_invalid(now=100.0) == 1
    assert reg.get_link(a.link_id) is None


def test_purge_invalid_removes_exhausted(reg):
    a = reg.create_link("d", "u", max_uses=1)
    reg.use_link(a.link_id)
    assert reg.purge_invalid() == 1
    assert reg.get_link(a.link_id) is None


def test_purge_invalid_keeps_valid(reg):
    a = reg.create_link("d", "u")
    b = reg.create_link("d", "u")
    reg.revoke(b.link_id)
    assert reg.purge_invalid() == 1
    assert reg.get_link(a.link_id) is not None


def test_purge_invalid_clears_by_doc(reg):
    a = reg.create_link("doc1", "u")
    reg.revoke(a.link_id)
    reg.purge_invalid()
    assert reg.links_for_doc("doc1", include_invalid=True) == []


def test_purge_invalid_returns_zero_when_empty(reg):
    assert reg.purge_invalid() == 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_empty(reg):
    s = reg.stats()
    assert s == LinkStats(total_links=0, active_links=0, revoked_count=0, total_uses=0)


def test_stats_counts(reg):
    a = reg.create_link("d", "u")
    b = reg.create_link("d", "u")
    c = reg.create_link("d", "u", max_uses=1)
    reg.revoke(b.link_id)
    reg.use_link(c.link_id)  # exhausts it
    reg.use_link(a.link_id)  # active still
    s = reg.stats()
    assert s.total_links == 3
    assert s.revoked_count == 1
    assert s.total_uses == 2
    assert s.active_links == 1  # only `a` is valid


def test_stats_expired_not_active(reg):
    reg.create_link("d", "u", expires_at=10.0, now=1.0)
    s = reg.stats(now=100.0)
    assert s.total_links == 1
    assert s.active_links == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_thread_safety_create_link(reg):
    def worker():
        for _ in range(40):
            reg.create_link("doc1", "u")

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert reg.stats().total_links == 8 * 40


def test_thread_safety_use_link(reg):
    link = reg.create_link("doc1", "u", max_uses=100)
    successes = []
    lock = threading.Lock()

    def worker():
        for _ in range(50):
            if reg.use_link(link.link_id):
                with lock:
                    successes.append(1)

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Exactly 100 successful uses regardless of contention.
    assert reg.get_link(link.link_id).use_count == 100
    assert len(successes) == 100


def test_thread_safety_mixed_ops(reg):
    for _ in range(20):
        reg.create_link("doc1", "u")

    def reader():
        for _ in range(50):
            reg.active_links()
            reg.stats()
            reg.links_for_doc("doc1", include_invalid=True)

    def writer():
        for _ in range(20):
            link = reg.create_link("doc1", "u")
            reg.use_link(link.link_id)
            reg.revoke(link.link_id)

    threads = [threading.Thread(target=reader) for _ in range(4)]
    threads += [threading.Thread(target=writer) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = reg.stats()
    # 20 initial + 4 writers * 20 created
    assert s.total_links == 20 + 4 * 20


def test_thread_safety_revoke_all_for_doc(reg):
    for _ in range(50):
        reg.create_link("doc1", "u")

    def worker():
        reg.revoke_all_for_doc("doc1")

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # All revoked once; further calls return 0.
    assert reg.stats().revoked_count == 50


# ---------------------------------------------------------------------------
# Integration
# ---------------------------------------------------------------------------


def test_full_lifecycle(reg):
    link = reg.create_link("doc1", "alice", duration_seconds=100.0, max_uses=3, now=10.0)
    assert reg.is_valid(link.link_id, now=10.0)
    assert reg.use_link(link.link_id, now=20.0)
    assert reg.use_link(link.link_id, now=30.0)
    assert reg.is_valid(link.link_id, now=40.0)
    assert reg.use_link(link.link_id, now=50.0)
    assert not reg.is_valid(link.link_id, now=60.0)  # exhausted
    assert not reg.use_link(link.link_id, now=70.0)


def test_purge_then_stats(reg):
    a = reg.create_link("d", "u")
    b = reg.create_link("d", "u")
    reg.revoke(a.link_id)
    reg.purge_invalid()
    s = reg.stats()
    assert s.total_links == 1
    assert s.active_links == 1
    assert s.revoked_count == 0


def test_create_link_after_purge_reuses_doc_index(reg):
    a = reg.create_link("doc1", "u")
    reg.revoke(a.link_id)
    reg.purge_invalid()
    assert reg.links_for_doc("doc1", include_invalid=True) == []
    b = reg.create_link("doc1", "u")
    result = reg.links_for_doc("doc1")
    assert [l.link_id for l in result] == [b.link_id]
