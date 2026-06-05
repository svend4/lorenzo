"""Tests for E334 DocSessionStore."""

from __future__ import annotations

import threading
import uuid

import pytest

from docstoolkit.doc_session_store import DocSessionStore, Session, SessionStats


# --------------------------------------------------------------------------- #
# Dataclasses                                                                 #
# --------------------------------------------------------------------------- #
class TestSessionDataclass:
    def test_session_minimal_construction(self):
        s = Session(session_id="sid", user_id="u", doc_id="d")
        assert s.session_id == "sid"
        assert s.user_id == "u"
        assert s.doc_id == "d"

    def test_session_defaults(self):
        s = Session(session_id="sid", user_id="u", doc_id="d")
        assert s.started_at == 0.0
        assert s.last_activity_at == 0.0
        assert s.ended_at is None
        assert s.active is True
        assert s.metadata == {}

    def test_session_metadata_is_independent(self):
        a = Session(session_id="a", user_id="u", doc_id="d")
        b = Session(session_id="b", user_id="u", doc_id="d")
        a.metadata["k"] = "v"
        assert b.metadata == {}

    def test_session_explicit_values(self):
        s = Session(
            session_id="sid",
            user_id="u",
            doc_id="d",
            started_at=10.0,
            last_activity_at=11.0,
            ended_at=12.0,
            active=False,
            metadata={"x": 1},
        )
        assert s.started_at == 10.0
        assert s.last_activity_at == 11.0
        assert s.ended_at == 12.0
        assert s.active is False
        assert s.metadata == {"x": 1}


class TestSessionStatsDataclass:
    def test_stats_construction(self):
        st = SessionStats(
            total_sessions=5, active_sessions=3, unique_users=2, unique_docs=4
        )
        assert st.total_sessions == 5
        assert st.active_sessions == 3
        assert st.unique_users == 2
        assert st.unique_docs == 4

    def test_stats_equality(self):
        a = SessionStats(1, 1, 1, 1)
        b = SessionStats(1, 1, 1, 1)
        assert a == b

    def test_stats_inequality(self):
        a = SessionStats(1, 1, 1, 1)
        b = SessionStats(2, 1, 1, 1)
        assert a != b


# --------------------------------------------------------------------------- #
# Construction                                                                #
# --------------------------------------------------------------------------- #
class TestConstruction:
    def test_empty_store(self):
        st = DocSessionStore()
        assert st.stats().total_sessions == 0

    def test_all_doc_ids_empty(self):
        st = DocSessionStore()
        assert st.all_doc_ids() == []

    def test_get_missing(self):
        st = DocSessionStore()
        assert st.get("missing") is None


# --------------------------------------------------------------------------- #
# start                                                                       #
# --------------------------------------------------------------------------- #
class TestStart:
    def test_start_creates_session(self):
        st = DocSessionStore()
        s = st.start("u1", "d1", now=100.0)
        assert s.user_id == "u1"
        assert s.doc_id == "d1"

    def test_start_session_id_is_uuid(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        uuid.UUID(s.session_id)  # raises on invalid

    def test_start_active_true(self):
        st = DocSessionStore()
        s = st.start("u1", "d1", now=100.0)
        assert s.active is True
        assert s.ended_at is None

    def test_start_timestamps_equal(self):
        st = DocSessionStore()
        s = st.start("u1", "d1", now=100.0)
        assert s.started_at == 100.0
        assert s.last_activity_at == 100.0

    def test_start_metadata_stored(self):
        st = DocSessionStore()
        s = st.start("u1", "d1", metadata={"client": "web"})
        assert s.metadata == {"client": "web"}

    def test_start_metadata_default_empty(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        assert s.metadata == {}

    def test_start_metadata_copied(self):
        st = DocSessionStore()
        meta = {"k": 1}
        s = st.start("u1", "d1", metadata=meta)
        meta["k"] = 2
        assert s.metadata["k"] == 1

    def test_start_indexed_by_user(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        assert st.sessions_for_user("u1")[0].session_id == s.session_id

    def test_start_indexed_by_doc(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        assert st.sessions_for_doc("d1")[0].session_id == s.session_id

    def test_start_multiple_unique_ids(self):
        st = DocSessionStore()
        a = st.start("u1", "d1")
        b = st.start("u1", "d1")
        assert a.session_id != b.session_id


# --------------------------------------------------------------------------- #
# touch                                                                       #
# --------------------------------------------------------------------------- #
class TestTouch:
    def test_touch_updates_last_activity(self):
        st = DocSessionStore()
        s = st.start("u1", "d1", now=100.0)
        st.touch(s.session_id, now=200.0)
        assert st.get(s.session_id).last_activity_at == 200.0

    def test_touch_returns_true_when_active(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        assert st.touch(s.session_id, now=50.0) is True

    def test_touch_returns_false_when_missing(self):
        st = DocSessionStore()
        assert st.touch("missing", now=10.0) is False

    def test_touch_returns_false_on_inactive(self):
        st = DocSessionStore()
        s = st.start("u1", "d1", now=10.0)
        st.end(s.session_id, now=20.0)
        assert st.touch(s.session_id, now=30.0) is False

    def test_touch_inactive_does_not_update(self):
        st = DocSessionStore()
        s = st.start("u1", "d1", now=10.0)
        st.end(s.session_id, now=20.0)
        st.touch(s.session_id, now=999.0)
        assert st.get(s.session_id).last_activity_at == 10.0


# --------------------------------------------------------------------------- #
# end                                                                         #
# --------------------------------------------------------------------------- #
class TestEnd:
    def test_end_marks_inactive(self):
        st = DocSessionStore()
        s = st.start("u1", "d1", now=10.0)
        st.end(s.session_id, now=20.0)
        assert st.get(s.session_id).active is False

    def test_end_sets_ended_at(self):
        st = DocSessionStore()
        s = st.start("u1", "d1", now=10.0)
        st.end(s.session_id, now=20.0)
        assert st.get(s.session_id).ended_at == 20.0

    def test_end_returns_true(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        assert st.end(s.session_id, now=100.0) is True

    def test_end_returns_false_when_missing(self):
        st = DocSessionStore()
        assert st.end("missing") is False

    def test_end_returns_false_when_already_ended(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        st.end(s.session_id, now=10.0)
        assert st.end(s.session_id, now=20.0) is False


# --------------------------------------------------------------------------- #
# get                                                                         #
# --------------------------------------------------------------------------- #
class TestGet:
    def test_get_found(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        assert st.get(s.session_id) is not None

    def test_get_not_found(self):
        st = DocSessionStore()
        assert st.get("nope") is None

    def test_get_returns_same_session(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        got = st.get(s.session_id)
        assert got.user_id == "u1"
        assert got.doc_id == "d1"


# --------------------------------------------------------------------------- #
# active_sessions_for_user                                                    #
# --------------------------------------------------------------------------- #
class TestActiveSessionsForUser:
    def test_only_active(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=10.0)
        b = st.start("u1", "d2", now=20.0)
        st.end(b.session_id, now=30.0)
        result = st.active_sessions_for_user("u1")
        assert [s.session_id for s in result] == [a.session_id]

    def test_sorted_by_started_at(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=30.0)
        b = st.start("u1", "d2", now=10.0)
        c = st.start("u1", "d3", now=20.0)
        result = st.active_sessions_for_user("u1")
        assert [s.session_id for s in result] == [b.session_id, c.session_id, a.session_id]

    def test_empty_for_unknown_user(self):
        st = DocSessionStore()
        assert st.active_sessions_for_user("ghost") == []


# --------------------------------------------------------------------------- #
# active_sessions_for_doc                                                     #
# --------------------------------------------------------------------------- #
class TestActiveSessionsForDoc:
    def test_only_active(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=10.0)
        b = st.start("u2", "d1", now=20.0)
        st.end(b.session_id, now=30.0)
        result = st.active_sessions_for_doc("d1")
        assert [s.session_id for s in result] == [a.session_id]

    def test_sorted_by_started_at(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=30.0)
        b = st.start("u2", "d1", now=10.0)
        c = st.start("u3", "d1", now=20.0)
        result = st.active_sessions_for_doc("d1")
        assert [s.session_id for s in result] == [b.session_id, c.session_id, a.session_id]

    def test_empty_for_unknown_doc(self):
        st = DocSessionStore()
        assert st.active_sessions_for_doc("ghost") == []


# --------------------------------------------------------------------------- #
# sessions_for_user                                                           #
# --------------------------------------------------------------------------- #
class TestSessionsForUser:
    def test_all_sessions_by_default(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=10.0)
        b = st.start("u1", "d2", now=20.0)
        st.end(b.session_id, now=25.0)
        result = st.sessions_for_user("u1")
        assert {s.session_id for s in result} == {a.session_id, b.session_id}

    def test_active_only_flag(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=10.0)
        b = st.start("u1", "d2", now=20.0)
        st.end(b.session_id, now=25.0)
        result = st.sessions_for_user("u1", active_only=True)
        assert [s.session_id for s in result] == [a.session_id]

    def test_sorted_by_started_at(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=20.0)
        b = st.start("u1", "d2", now=10.0)
        result = st.sessions_for_user("u1")
        assert [s.session_id for s in result] == [b.session_id, a.session_id]


# --------------------------------------------------------------------------- #
# sessions_for_doc                                                            #
# --------------------------------------------------------------------------- #
class TestSessionsForDoc:
    def test_all_sessions_by_default(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=10.0)
        b = st.start("u2", "d1", now=20.0)
        st.end(b.session_id, now=25.0)
        result = st.sessions_for_doc("d1")
        assert {s.session_id for s in result} == {a.session_id, b.session_id}

    def test_active_only_flag(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=10.0)
        b = st.start("u2", "d1", now=20.0)
        st.end(b.session_id, now=25.0)
        result = st.sessions_for_doc("d1", active_only=True)
        assert [s.session_id for s in result] == [a.session_id]

    def test_sorted_by_started_at(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=30.0)
        b = st.start("u2", "d1", now=10.0)
        result = st.sessions_for_doc("d1")
        assert [s.session_id for s in result] == [b.session_id, a.session_id]


# --------------------------------------------------------------------------- #
# expire_idle                                                                 #
# --------------------------------------------------------------------------- #
class TestExpireIdle:
    def test_expires_idle(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=10.0)
        b = st.start("u2", "d2", now=10.0)
        st.touch(b.session_id, now=95.0)
        count = st.expire_idle(timeout_seconds=30.0, now=100.0)
        assert count == 1
        assert st.get(a.session_id).active is False
        assert st.get(b.session_id).active is True

    def test_returns_zero_when_nothing_expired(self):
        st = DocSessionStore()
        st.start("u1", "d1", now=100.0)
        count = st.expire_idle(timeout_seconds=60.0, now=110.0)
        assert count == 0

    def test_sets_ended_at_for_expired(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=10.0)
        st.expire_idle(timeout_seconds=5.0, now=100.0)
        assert st.get(a.session_id).ended_at == 100.0

    def test_does_not_re_expire_already_ended(self):
        st = DocSessionStore()
        a = st.start("u1", "d1", now=10.0)
        st.end(a.session_id, now=20.0)
        count = st.expire_idle(timeout_seconds=1.0, now=100.0)
        assert count == 0
        assert st.get(a.session_id).ended_at == 20.0

    def test_boundary_not_expired(self):
        st = DocSessionStore()
        st.start("u1", "d1", now=10.0)
        # delta == timeout: not strictly greater, must remain active
        count = st.expire_idle(timeout_seconds=10.0, now=20.0)
        assert count == 0


# --------------------------------------------------------------------------- #
# concurrent_editors                                                          #
# --------------------------------------------------------------------------- #
class TestConcurrentEditors:
    def test_unique_users(self):
        st = DocSessionStore()
        st.start("u1", "d1")
        st.start("u1", "d1")  # same user, two sessions
        st.start("u2", "d1")
        assert st.concurrent_editors("d1") == ["u1", "u2"]

    def test_only_active_users(self):
        st = DocSessionStore()
        s1 = st.start("u1", "d1")
        st.start("u2", "d1")
        st.end(s1.session_id)
        assert st.concurrent_editors("d1") == ["u2"]

    def test_sorted(self):
        st = DocSessionStore()
        st.start("zeta", "d1")
        st.start("alpha", "d1")
        st.start("mu", "d1")
        assert st.concurrent_editors("d1") == ["alpha", "mu", "zeta"]

    def test_empty_for_unknown_doc(self):
        st = DocSessionStore()
        assert st.concurrent_editors("ghost") == []


# --------------------------------------------------------------------------- #
# delete_session                                                              #
# --------------------------------------------------------------------------- #
class TestDeleteSession:
    def test_returns_true_when_deleted(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        assert st.delete_session(s.session_id) is True
        assert st.get(s.session_id) is None

    def test_returns_false_when_missing(self):
        st = DocSessionStore()
        assert st.delete_session("nope") is False

    def test_removes_from_user_index(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        st.delete_session(s.session_id)
        assert st.sessions_for_user("u1") == []

    def test_removes_from_doc_index(self):
        st = DocSessionStore()
        s = st.start("u1", "d1")
        st.delete_session(s.session_id)
        assert st.sessions_for_doc("d1") == []


# --------------------------------------------------------------------------- #
# clear_user                                                                  #
# --------------------------------------------------------------------------- #
class TestClearUser:
    def test_returns_count(self):
        st = DocSessionStore()
        st.start("u1", "d1")
        st.start("u1", "d2")
        st.start("u1", "d3")
        assert st.clear_user("u1") == 3

    def test_does_not_affect_other_users(self):
        st = DocSessionStore()
        st.start("u1", "d1")
        s = st.start("u2", "d1")
        st.clear_user("u1")
        assert st.get(s.session_id) is not None

    def test_returns_zero_for_unknown_user(self):
        st = DocSessionStore()
        assert st.clear_user("ghost") == 0


# --------------------------------------------------------------------------- #
# all_doc_ids                                                                 #
# --------------------------------------------------------------------------- #
class TestAllDocIds:
    def test_sorted_unique(self):
        st = DocSessionStore()
        st.start("u1", "doc-z")
        st.start("u1", "doc-a")
        st.start("u2", "doc-a")
        st.start("u1", "doc-m")
        assert st.all_doc_ids() == ["doc-a", "doc-m", "doc-z"]

    def test_empty(self):
        st = DocSessionStore()
        assert st.all_doc_ids() == []


# --------------------------------------------------------------------------- #
# stats                                                                       #
# --------------------------------------------------------------------------- #
class TestStats:
    def test_empty_stats(self):
        st = DocSessionStore()
        s = st.stats()
        assert s == SessionStats(0, 0, 0, 0)

    def test_totals(self):
        st = DocSessionStore()
        a = st.start("u1", "d1")
        st.start("u2", "d1")
        st.start("u2", "d2")
        st.end(a.session_id)
        s = st.stats()
        assert s.total_sessions == 3
        assert s.active_sessions == 2
        assert s.unique_users == 2
        assert s.unique_docs == 2

    def test_after_delete(self):
        st = DocSessionStore()
        a = st.start("u1", "d1")
        st.delete_session(a.session_id)
        assert st.stats() == SessionStats(0, 0, 0, 0)


# --------------------------------------------------------------------------- #
# Thread safety                                                               #
# --------------------------------------------------------------------------- #
class TestThreadSafety:
    def test_concurrent_starts(self):
        st = DocSessionStore()
        threads = []
        results: list[str] = []
        lock = threading.Lock()

        def worker(i: int) -> None:
            s = st.start(f"u{i % 5}", f"d{i % 7}", now=float(i))
            with lock:
                results.append(s.session_id)

        for i in range(200):
            t = threading.Thread(target=worker, args=(i,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 200
        assert len(set(results)) == 200
        assert st.stats().total_sessions == 200
        assert st.stats().active_sessions == 200

    def test_concurrent_touch_and_end(self):
        st = DocSessionStore()
        sessions = [st.start(f"u{i}", "d1", now=float(i)) for i in range(50)]
        threads = []

        def touch_worker(sid: str) -> None:
            for _ in range(20):
                st.touch(sid, now=1000.0)

        def end_worker(sid: str) -> None:
            st.end(sid, now=2000.0)

        for s in sessions:
            threads.append(threading.Thread(target=touch_worker, args=(s.session_id,)))
            threads.append(threading.Thread(target=end_worker, args=(s.session_id,)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All ended after dust settles
        for s in sessions:
            assert st.get(s.session_id).active is False


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
