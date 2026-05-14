"""Tests for E77 state_machine module — target: 78+ tests."""
from __future__ import annotations

import pytest

from docstoolkit.state_machine import (
    State,
    Transition,
    TransitionError,
    StateMachine,
    StateMachineConfig,
    StateMachineBuilder,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _simple_machine(allow_self: bool = False) -> StateMachine:
    """idle -> running -> done (terminal)."""
    cfg = StateMachineConfig(initial_state="idle", allow_self_transitions=allow_self)
    sm = StateMachine(cfg)
    sm.add_state(State("idle", description="waiting"))
    sm.add_state(State("running", description="active"))
    sm.add_state(State("done", is_terminal=True))
    sm.add_transition(Transition("idle", "start", "running"))
    sm.add_transition(Transition("running", "finish", "done"))
    return sm


def _builder_machine(allow_self: bool = False) -> StateMachine:
    return (
        StateMachineBuilder("idle", allow_self_transitions=allow_self)
        .state("idle", description="waiting")
        .state("running", description="active")
        .state("done", is_terminal=True)
        .transition("idle", "start", "running")
        .transition("running", "finish", "done")
        .build()
    )


# ===========================================================================
# State dataclass
# ===========================================================================

class TestStateDataclass:
    def test_name_required(self):
        s = State(name="s1")
        assert s.name == "s1"

    def test_description_default_empty(self):
        s = State(name="s1")
        assert s.description == ""

    def test_description_set(self):
        s = State(name="s1", description="hello")
        assert s.description == "hello"

    def test_is_terminal_default_false(self):
        s = State(name="s1")
        assert s.is_terminal is False

    def test_is_terminal_set_true(self):
        s = State(name="s1", is_terminal=True)
        assert s.is_terminal is True

    def test_on_enter_default_none(self):
        s = State(name="s1")
        assert s.on_enter is None

    def test_on_exit_default_none(self):
        s = State(name="s1")
        assert s.on_exit is None

    def test_on_enter_set(self):
        cb = lambda ctx: None
        s = State(name="s1", on_enter=cb)
        assert s.on_enter is cb

    def test_on_exit_set(self):
        cb = lambda ctx: None
        s = State(name="s1", on_exit=cb)
        assert s.on_exit is cb

    def test_equality_by_name(self):
        assert State("a") == State("a", description="different")

    def test_inequality_by_name(self):
        assert State("a") != State("b")

    def test_hash_by_name(self):
        assert hash(State("x")) == hash(State("x"))

    def test_hash_different_names(self):
        assert hash(State("a")) != hash(State("b"))

    def test_state_in_set(self):
        states = {State("a"), State("b"), State("a", description="dup")}
        assert len(states) == 2


# ===========================================================================
# Transition dataclass
# ===========================================================================

class TestTransitionDataclass:
    def test_basic_fields(self):
        t = Transition("a", "go", "b")
        assert t.from_state == "a"
        assert t.event == "go"
        assert t.to_state == "b"

    def test_guard_default_none(self):
        t = Transition("a", "go", "b")
        assert t.guard is None

    def test_action_default_none(self):
        t = Transition("a", "go", "b")
        assert t.action is None

    def test_guard_set(self):
        g = lambda ctx: True
        t = Transition("a", "go", "b", guard=g)
        assert t.guard is g

    def test_action_set(self):
        a = lambda ctx: None
        t = Transition("a", "go", "b", action=a)
        assert t.action is a


# ===========================================================================
# StateMachineConfig
# ===========================================================================

class TestStateMachineConfig:
    def test_initial_state_required(self):
        cfg = StateMachineConfig(initial_state="start")
        assert cfg.initial_state == "start"

    def test_allow_self_transitions_default_false(self):
        cfg = StateMachineConfig(initial_state="s")
        assert cfg.allow_self_transitions is False

    def test_allow_self_transitions_set(self):
        cfg = StateMachineConfig(initial_state="s", allow_self_transitions=True)
        assert cfg.allow_self_transitions is True


# ===========================================================================
# StateMachine — add_state / add_transition
# ===========================================================================

class TestStateMachineRegistration:
    def test_add_state(self):
        cfg = StateMachineConfig(initial_state="s1")
        sm = StateMachine(cfg)
        sm.add_state(State("s1"))
        assert sm.current_state == "s1"

    def test_add_duplicate_state_raises(self):
        cfg = StateMachineConfig(initial_state="s1")
        sm = StateMachine(cfg)
        sm.add_state(State("s1"))
        with pytest.raises(ValueError, match="already registered"):
            sm.add_state(State("s1"))

    def test_add_transition_unknown_from_raises(self):
        cfg = StateMachineConfig(initial_state="s1")
        sm = StateMachine(cfg)
        sm.add_state(State("s1"))
        sm.add_state(State("s2"))
        with pytest.raises(ValueError, match="Unknown from_state"):
            sm.add_transition(Transition("ghost", "go", "s2"))

    def test_add_transition_unknown_to_raises(self):
        cfg = StateMachineConfig(initial_state="s1")
        sm = StateMachine(cfg)
        sm.add_state(State("s1"))
        with pytest.raises(ValueError, match="Unknown to_state"):
            sm.add_transition(Transition("s1", "go", "ghost"))

    def test_add_self_transition_disallowed_raises(self):
        cfg = StateMachineConfig(initial_state="s1", allow_self_transitions=False)
        sm = StateMachine(cfg)
        sm.add_state(State("s1"))
        with pytest.raises(ValueError, match="Self-transition"):
            sm.add_transition(Transition("s1", "ping", "s1"))

    def test_add_self_transition_allowed(self):
        cfg = StateMachineConfig(initial_state="s1", allow_self_transitions=True)
        sm = StateMachine(cfg)
        sm.add_state(State("s1"))
        sm.add_transition(Transition("s1", "ping", "s1"))  # should not raise


# ===========================================================================
# StateMachine — trigger (happy path)
# ===========================================================================

class TestStateMachineTrigger:
    def test_trigger_changes_state(self):
        sm = _simple_machine()
        sm.trigger("start")
        assert sm.current_state == "running"

    def test_trigger_returns_new_state(self):
        sm = _simple_machine()
        result = sm.trigger("start")
        assert result == "running"

    def test_trigger_sequence(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.trigger("finish")
        assert sm.current_state == "done"

    def test_trigger_unknown_event_raises(self):
        sm = _simple_machine()
        with pytest.raises(TransitionError):
            sm.trigger("unknown_event")

    def test_trigger_wrong_state_raises(self):
        sm = _simple_machine()
        # "finish" is only valid from "running", not "idle"
        with pytest.raises(TransitionError):
            sm.trigger("finish")

    def test_trigger_from_terminal_raises(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.trigger("finish")
        with pytest.raises(TransitionError):
            sm.trigger("start")

    def test_trigger_with_none_context(self):
        sm = _simple_machine()
        sm.trigger("start", context=None)
        assert sm.current_state == "running"

    def test_trigger_with_empty_context(self):
        sm = _simple_machine()
        sm.trigger("start", context={})
        assert sm.current_state == "running"

    def test_trigger_default_context(self):
        sm = _simple_machine()
        sm.trigger("start")  # no context kwarg
        assert sm.current_state == "running"


# ===========================================================================
# StateMachine — guards
# ===========================================================================

class TestStateMachineGuards:
    def test_guard_allows_transition(self):
        sm = _simple_machine()
        cfg = StateMachineConfig(initial_state="idle")
        sm2 = StateMachine(cfg)
        sm2.add_state(State("idle"))
        sm2.add_state(State("running"))
        sm2.add_transition(
            Transition("idle", "start", "running", guard=lambda ctx: ctx.get("ok"))
        )
        sm2.trigger("start", context={"ok": True})
        assert sm2.current_state == "running"

    def test_guard_blocks_transition(self):
        cfg = StateMachineConfig(initial_state="idle")
        sm = StateMachine(cfg)
        sm.add_state(State("idle"))
        sm.add_state(State("running"))
        sm.add_transition(
            Transition("idle", "start", "running", guard=lambda ctx: ctx.get("ok"))
        )
        with pytest.raises(TransitionError):
            sm.trigger("start", context={"ok": False})

    def test_guard_receives_context(self):
        received = {}
        def guard(ctx):
            received.update(ctx)
            return True
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_transition(Transition("a", "go", "b", guard=guard))
        sm.trigger("go", context={"key": "value"})
        assert received.get("key") == "value"

    def test_guard_none_always_allows(self):
        sm = _simple_machine()
        sm.trigger("start")  # guard is None
        assert sm.current_state == "running"

    def test_multiple_transitions_same_event_first_matching_guard(self):
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_state(State("c"))
        # first transition: guard fails, second: guard passes
        sm.add_transition(
            Transition("a", "go", "b", guard=lambda ctx: False)
        )
        sm.add_transition(
            Transition("a", "go", "c", guard=lambda ctx: True)
        )
        sm.trigger("go")
        assert sm.current_state == "c"


# ===========================================================================
# StateMachine — actions
# ===========================================================================

class TestStateMachineActions:
    def test_action_called_on_transition(self):
        calls = []
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_transition(
            Transition("a", "go", "b", action=lambda ctx: calls.append("action"))
        )
        sm.trigger("go")
        assert calls == ["action"]

    def test_action_receives_context(self):
        received = {}
        def action(ctx):
            received.update(ctx)
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_transition(Transition("a", "go", "b", action=action))
        sm.trigger("go", context={"payload": 42})
        assert received.get("payload") == 42

    def test_action_not_called_when_guard_blocks(self):
        calls = []
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_transition(
            Transition(
                "a", "go", "b",
                guard=lambda ctx: False,
                action=lambda ctx: calls.append("x"),
            )
        )
        with pytest.raises(TransitionError):
            sm.trigger("go")
        assert calls == []

    def test_action_none_no_error(self):
        sm = _simple_machine()
        sm.trigger("start")  # action is None
        assert sm.current_state == "running"


# ===========================================================================
# StateMachine — on_enter / on_exit
# ===========================================================================

class TestLifecycleHooks:
    def test_on_exit_called_on_departure(self):
        calls = []
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a", on_exit=lambda ctx: calls.append("exit_a")))
        sm.add_state(State("b"))
        sm.add_transition(Transition("a", "go", "b"))
        sm.trigger("go")
        assert "exit_a" in calls

    def test_on_enter_called_on_arrival(self):
        calls = []
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b", on_enter=lambda ctx: calls.append("enter_b")))
        sm.add_transition(Transition("a", "go", "b"))
        sm.trigger("go")
        assert "enter_b" in calls

    def test_hook_order_exit_action_enter(self):
        order = []
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a", on_exit=lambda ctx: order.append("exit")))
        sm.add_state(State("b", on_enter=lambda ctx: order.append("enter")))
        sm.add_transition(
            Transition("a", "go", "b", action=lambda ctx: order.append("action"))
        )
        sm.trigger("go")
        assert order == ["exit", "action", "enter"]

    def test_on_exit_receives_context(self):
        received = {}
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a", on_exit=lambda ctx: received.update(ctx)))
        sm.add_state(State("b"))
        sm.add_transition(Transition("a", "go", "b"))
        sm.trigger("go", context={"x": 1})
        assert received.get("x") == 1

    def test_on_enter_receives_context(self):
        received = {}
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b", on_enter=lambda ctx: received.update(ctx)))
        sm.add_transition(Transition("a", "go", "b"))
        sm.trigger("go", context={"y": 2})
        assert received.get("y") == 2

    def test_hooks_not_called_on_guard_block(self):
        calls = []
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a", on_exit=lambda ctx: calls.append("exit")))
        sm.add_state(State("b", on_enter=lambda ctx: calls.append("enter")))
        sm.add_transition(
            Transition("a", "go", "b", guard=lambda ctx: False)
        )
        with pytest.raises(TransitionError):
            sm.trigger("go")
        assert calls == []


# ===========================================================================
# StateMachine — history
# ===========================================================================

class TestStateMachineHistory:
    def test_history_empty_initially(self):
        sm = _simple_machine()
        assert sm.history == []

    def test_history_records_transition(self):
        sm = _simple_machine()
        sm.trigger("start")
        assert sm.history == [("idle", "start", "running")]

    def test_history_accumulates(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.trigger("finish")
        assert sm.history == [
            ("idle", "start", "running"),
            ("running", "finish", "done"),
        ]

    def test_history_is_copy(self):
        sm = _simple_machine()
        sm.trigger("start")
        h = sm.history
        h.append(("fake", "fake", "fake"))
        assert len(sm.history) == 1  # original unmodified

    def test_history_cleared_on_reset(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.reset()
        assert sm.history == []


# ===========================================================================
# StateMachine — can_trigger
# ===========================================================================

class TestCanTrigger:
    def test_can_trigger_valid_event(self):
        sm = _simple_machine()
        assert sm.can_trigger("start") is True

    def test_cannot_trigger_invalid_event(self):
        sm = _simple_machine()
        assert sm.can_trigger("finish") is False

    def test_cannot_trigger_on_terminal(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.trigger("finish")
        assert sm.can_trigger("start") is False

    def test_cannot_trigger_when_guard_blocks(self):
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_transition(
            Transition("a", "go", "b", guard=lambda ctx: ctx.get("ok"))
        )
        assert sm.can_trigger("go", context={"ok": False}) is False

    def test_can_trigger_when_guard_passes(self):
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_transition(
            Transition("a", "go", "b", guard=lambda ctx: ctx.get("ok"))
        )
        assert sm.can_trigger("go", context={"ok": True}) is True

    def test_can_trigger_default_context(self):
        sm = _simple_machine()
        assert sm.can_trigger("start") is True


# ===========================================================================
# StateMachine — available_events
# ===========================================================================

class TestAvailableEvents:
    def test_available_events_non_empty(self):
        sm = _simple_machine()
        assert "start" in sm.available_events()

    def test_available_events_empty_on_terminal(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.trigger("finish")
        assert sm.available_events() == []

    def test_available_events_after_transition(self):
        sm = _simple_machine()
        sm.trigger("start")
        events = sm.available_events()
        assert "finish" in events
        assert "start" not in events

    def test_available_events_excludes_guard_blocked(self):
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_transition(
            Transition("a", "go", "b", guard=lambda ctx: ctx.get("ok"))
        )
        events = sm.available_events(context={"ok": False})
        assert "go" not in events

    def test_available_events_includes_guard_passing(self):
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_transition(
            Transition("a", "go", "b", guard=lambda ctx: ctx.get("ok"))
        )
        events = sm.available_events(context={"ok": True})
        assert "go" in events

    def test_available_events_no_duplicates(self):
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_state(State("c"))
        sm.add_transition(Transition("a", "go", "b"))
        sm.add_transition(Transition("a", "go", "c"))
        events = sm.available_events()
        assert events.count("go") == 1

    def test_available_events_default_context(self):
        sm = _simple_machine()
        events = sm.available_events()  # no context kwarg
        assert isinstance(events, list)


# ===========================================================================
# StateMachine — reset
# ===========================================================================

class TestStateMachineReset:
    def test_reset_returns_to_initial(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.reset()
        assert sm.current_state == "idle"

    def test_reset_clears_history(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.reset()
        assert sm.history == []

    def test_reset_allows_retrigger(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.trigger("finish")
        sm.reset()
        sm.trigger("start")
        assert sm.current_state == "running"

    def test_reset_multiple_times(self):
        sm = _simple_machine()
        sm.reset()
        sm.reset()
        assert sm.current_state == "idle"
        assert sm.history == []


# ===========================================================================
# StateMachine — is_terminal
# ===========================================================================

class TestIsTerminal:
    def test_initial_state_not_terminal(self):
        sm = _simple_machine()
        assert sm.is_terminal() is False

    def test_non_terminal_state_after_transition(self):
        sm = _simple_machine()
        sm.trigger("start")
        assert sm.is_terminal() is False

    def test_terminal_state_detected(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.trigger("finish")
        assert sm.is_terminal() is True

    def test_terminal_state_blocks_trigger(self):
        sm = _simple_machine()
        sm.trigger("start")
        sm.trigger("finish")
        with pytest.raises(TransitionError):
            sm.trigger("start")


# ===========================================================================
# Self-transitions
# ===========================================================================

class TestSelfTransitions:
    def test_self_transition_allowed(self):
        cfg = StateMachineConfig(initial_state="idle", allow_self_transitions=True)
        sm = StateMachine(cfg)
        sm.add_state(State("idle"))
        sm.add_transition(Transition("idle", "ping", "idle"))
        sm.trigger("ping")
        assert sm.current_state == "idle"

    def test_self_transition_recorded_in_history(self):
        cfg = StateMachineConfig(initial_state="idle", allow_self_transitions=True)
        sm = StateMachine(cfg)
        sm.add_state(State("idle"))
        sm.add_transition(Transition("idle", "ping", "idle"))
        sm.trigger("ping")
        assert sm.history == [("idle", "ping", "idle")]

    def test_self_transition_disallowed_at_add(self):
        cfg = StateMachineConfig(initial_state="idle", allow_self_transitions=False)
        sm = StateMachine(cfg)
        sm.add_state(State("idle"))
        with pytest.raises(ValueError, match="Self-transition"):
            sm.add_transition(Transition("idle", "ping", "idle"))

    def test_self_transition_hooks_called(self):
        calls = []
        cfg = StateMachineConfig(initial_state="idle", allow_self_transitions=True)
        sm = StateMachine(cfg)
        sm.add_state(
            State(
                "idle",
                on_exit=lambda ctx: calls.append("exit"),
                on_enter=lambda ctx: calls.append("enter"),
            )
        )
        sm.add_transition(Transition("idle", "ping", "idle"))
        sm.trigger("ping")
        assert calls == ["exit", "enter"]


# ===========================================================================
# TransitionError
# ===========================================================================

class TestTransitionError:
    def test_is_exception_subclass(self):
        assert issubclass(TransitionError, Exception)

    def test_can_raise_and_catch(self):
        with pytest.raises(TransitionError):
            raise TransitionError("test error")

    def test_message_preserved(self):
        try:
            raise TransitionError("msg")
        except TransitionError as exc:
            assert "msg" in str(exc)


# ===========================================================================
# StateMachineBuilder
# ===========================================================================

class TestStateMachineBuilder:
    def test_build_returns_state_machine(self):
        sm = _builder_machine()
        assert isinstance(sm, StateMachine)

    def test_build_initial_state(self):
        sm = _builder_machine()
        assert sm.current_state == "idle"

    def test_build_trigger_works(self):
        sm = _builder_machine()
        sm.trigger("start")
        assert sm.current_state == "running"

    def test_build_full_sequence(self):
        sm = _builder_machine()
        sm.trigger("start")
        sm.trigger("finish")
        assert sm.is_terminal()

    def test_fluent_chaining_returns_builder(self):
        builder = StateMachineBuilder("a")
        result = builder.state("a").state("b").transition("a", "go", "b")
        assert isinstance(result, StateMachineBuilder)

    def test_builder_with_on_enter(self):
        calls = []
        sm = (
            StateMachineBuilder("a")
            .state("a")
            .state("b", on_enter=lambda ctx: calls.append("enter_b"))
            .transition("a", "go", "b")
            .build()
        )
        sm.trigger("go")
        assert "enter_b" in calls

    def test_builder_with_on_exit(self):
        calls = []
        sm = (
            StateMachineBuilder("a")
            .state("a", on_exit=lambda ctx: calls.append("exit_a"))
            .state("b")
            .transition("a", "go", "b")
            .build()
        )
        sm.trigger("go")
        assert "exit_a" in calls

    def test_builder_with_guard(self):
        sm = (
            StateMachineBuilder("a")
            .state("a")
            .state("b")
            .transition("a", "go", "b", guard=lambda ctx: ctx.get("ok"))
            .build()
        )
        with pytest.raises(TransitionError):
            sm.trigger("go", context={"ok": False})

    def test_builder_with_action(self):
        calls = []
        sm = (
            StateMachineBuilder("a")
            .state("a")
            .state("b")
            .transition("a", "go", "b", action=lambda ctx: calls.append("act"))
            .build()
        )
        sm.trigger("go")
        assert calls == ["act"]

    def test_builder_allow_self_transitions(self):
        sm = (
            StateMachineBuilder("a", allow_self_transitions=True)
            .state("a")
            .transition("a", "ping", "a")
            .build()
        )
        sm.trigger("ping")
        assert sm.current_state == "a"

    def test_builder_allow_self_transitions_method(self):
        sm = (
            StateMachineBuilder("a")
            .allow_self_transitions(True)
            .state("a")
            .transition("a", "ping", "a")
            .build()
        )
        sm.trigger("ping")
        assert sm.current_state == "a"

    def test_builder_terminal_state(self):
        sm = (
            StateMachineBuilder("a")
            .state("a")
            .state("done", is_terminal=True)
            .transition("a", "end", "done")
            .build()
        )
        sm.trigger("end")
        assert sm.is_terminal()

    def test_builder_multiple_transitions_from_same_state(self):
        sm = (
            StateMachineBuilder("idle")
            .state("idle")
            .state("running")
            .state("paused")
            .transition("idle", "start", "running")
            .transition("idle", "pause", "paused")
            .build()
        )
        assert "start" in sm.available_events()
        assert "pause" in sm.available_events()

    def test_builder_description_passed(self):
        sm = (
            StateMachineBuilder("a")
            .state("a", description="first state")
            .state("b")
            .transition("a", "go", "b")
            .build()
        )
        # Just verify it builds without error; description stored in State object
        sm.trigger("go")
        assert sm.current_state == "b"


# ===========================================================================
# Context passing edge cases
# ===========================================================================

class TestContextEdgeCases:
    def test_context_mutated_by_action_visible_to_on_enter(self):
        """Action can mutate context; on_enter sees the mutation."""
        log = []
        def action(ctx):
            ctx["mutated"] = True
        def on_enter(ctx):
            log.append(ctx.get("mutated"))
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b", on_enter=on_enter))
        sm.add_transition(Transition("a", "go", "b", action=action))
        sm.trigger("go", context={})
        assert log == [True]

    def test_guard_and_action_share_context(self):
        log = []
        def guard(ctx):
            log.append(f"guard:{ctx.get('v')}")
            return True
        def action(ctx):
            log.append(f"action:{ctx.get('v')}")
        cfg = StateMachineConfig(initial_state="a")
        sm = StateMachine(cfg)
        sm.add_state(State("a"))
        sm.add_state(State("b"))
        sm.add_transition(Transition("a", "go", "b", guard=guard, action=action))
        sm.trigger("go", context={"v": 99})
        assert log == ["guard:99", "action:99"]


# ===========================================================================
# Public API surface (__init__ exports)
# ===========================================================================

class TestPublicAPI:
    def test_state_importable(self):
        from docstoolkit.state_machine import State as S
        assert S is State

    def test_transition_importable(self):
        from docstoolkit.state_machine import Transition as T
        assert T is Transition

    def test_transition_error_importable(self):
        from docstoolkit.state_machine import TransitionError as TE
        assert TE is TransitionError

    def test_state_machine_importable(self):
        from docstoolkit.state_machine import StateMachine as SM
        assert SM is StateMachine

    def test_state_machine_config_importable(self):
        from docstoolkit.state_machine import StateMachineConfig as SMC
        assert SMC is StateMachineConfig

    def test_state_machine_builder_importable(self):
        from docstoolkit.state_machine import StateMachineBuilder as SMB
        assert SMB is StateMachineBuilder
