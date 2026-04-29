"""Тесты event bus + sinks."""
import json
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.events import EventBus, Event, get_default_bus
from docstoolkit.events.sinks import (
    Sink, JsonlSink, ConsoleSink, WebhookSink, SlackSink,
)


def test_event_dataclass():
    e = Event(type="test", payload={"x": 1})
    assert e.type == "test"
    assert e.payload == {"x": 1}
    assert e.ts  # auto-set


def test_event_to_dict():
    e = Event(type="t", payload={"a": "b"})
    d = e.to_dict()
    assert d["type"] == "t"
    assert d["payload"] == {"a": "b"}


def test_bus_subscribe_emit():
    bus = EventBus()
    captured = []
    bus.subscribe("test", lambda e: captured.append(e))
    bus.emit(Event("test", {"x": 1}))
    assert len(captured) == 1
    assert captured[0].payload == {"x": 1}


def test_bus_wildcard_subscribe():
    bus = EventBus()
    captured = []
    bus.subscribe("*", lambda e: captured.append(e))
    bus.emit(Event("type1"))
    bus.emit(Event("type2"))
    assert len(captured) == 2


def test_bus_unsubscribe():
    bus = EventBus()
    h = lambda e: None
    bus.subscribe("x", h)
    bus.unsubscribe("x", h)
    bus.emit(Event("x"))
    # No exception


def test_bus_handler_exception_does_not_block():
    bus = EventBus()
    captured = []
    bus.subscribe("x", lambda e: 1/0)  # raises
    bus.subscribe("x", lambda e: captured.append(e))
    bus.emit(Event("x"))
    assert len(captured) == 1  # second handler still called


def test_jsonl_sink(tmp_path):
    log = tmp_path / "log.jsonl"
    sink = JsonlSink(log)
    sink.send(Event("a", {"v": 1}))
    sink.send(Event("b", {"v": 2}))
    lines = log.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    e = json.loads(lines[0])
    assert e["type"] == "a"


def test_sink_filter():
    sink = ConsoleSink(events=["error"])
    assert sink.should_emit(Event("error"))
    assert not sink.should_emit(Event("ingest.done"))


def test_sink_wildcard_filter():
    sink = ConsoleSink(events=["*"])
    assert sink.should_emit(Event("anything"))


def test_webhook_sink_handles_error():
    """WebhookSink не падает при недоступном URL."""
    sink = WebhookSink("http://nonexistent.invalid.example", timeout=1)
    sink.send(Event("test"))  # должно не падать


def test_default_bus_singleton():
    b1 = get_default_bus()
    b2 = get_default_bus()
    assert b1 is b2
