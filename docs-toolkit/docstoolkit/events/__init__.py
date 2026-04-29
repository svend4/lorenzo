"""Event bus + webhook system для docs-toolkit.

Используется внутри пакета (file_changed, ingest_done, rag_completed, etc.)
и наружу (Slack/Discord/HTTP webhooks).

Использование:
    from docstoolkit.events import EventBus, Event, WebhookSink

    bus = EventBus()
    bus.subscribe("ingest.done", lambda e: print(e.payload))
    bus.add_sink(WebhookSink("https://hooks.slack.com/...", events=["error"]))

    bus.emit(Event("ingest.done", {"path": "x.md", "size": 1024}))
"""
from docstoolkit.events.bus import EventBus, Event, get_default_bus
from docstoolkit.events.sinks import (
    WebhookSink, SlackSink, DiscordSink, JsonlSink, ConsoleSink,
)

__all__ = [
    "EventBus", "Event", "get_default_bus",
    "WebhookSink", "SlackSink", "DiscordSink", "JsonlSink", "ConsoleSink",
]
