"""Sinks для event bus: куда отправлять события."""
import json
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from pathlib import Path

from docstoolkit.events.bus import Event


class Sink(ABC):
    """Базовый класс sink."""

    def __init__(self, events: list[str] | None = None):
        """events: список типов на которые реагировать ('*' = все)."""
        self.events = events or ["*"]

    def should_emit(self, event: Event) -> bool:
        if "*" in self.events:
            return True
        return event.type in self.events

    @abstractmethod
    def send(self, event: Event):
        ...


class ConsoleSink(Sink):
    """Печатает event'ы в stdout."""

    def send(self, event: Event):
        print(f"[{event.ts}] {event.type:30s} {event.payload}")


class JsonlSink(Sink):
    """Аппендит event'ы в JSONL файл."""

    def __init__(self, path: str | Path, events: list[str] | None = None):
        super().__init__(events)
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def send(self, event: Event):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")


class WebhookSink(Sink):
    """POST event как JSON на URL."""

    def __init__(self, url: str, events: list[str] | None = None,
                 headers: dict | None = None, timeout: int = 5):
        super().__init__(events)
        self.url = url
        self.headers = headers or {}
        self.timeout = timeout

    def send(self, event: Event):
        body = json.dumps(event.to_dict(), ensure_ascii=False).encode("utf-8")
        headers = {"Content-Type": "application/json", **self.headers}
        req = urllib.request.Request(self.url, data=body, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                resp.read()
        except urllib.error.URLError:
            pass  # silent fail — не должны блокировать основной flow


class SlackSink(WebhookSink):
    """Slack-форматированный webhook."""

    def __init__(self, webhook_url: str, events: list[str] | None = None,
                 channel: str = "", username: str = "docs-toolkit"):
        super().__init__(webhook_url, events)
        self.channel = channel
        self.username = username

    def send(self, event: Event):
        emoji = {
            "error": "🔴", "validation.error": "⚠️",
            "ingest.done": "📥", "rag.done": "🤖",
            "agent.done": "✅", "job.done": "✅", "job.failed": "❌",
        }.get(event.type, "ℹ️")

        payload_str = ", ".join(f"{k}={v}" for k, v in event.payload.items())
        message = f"{emoji} *{event.type}*: {payload_str[:200]}"

        slack_payload = {
            "text": message,
            "username": self.username,
        }
        if self.channel:
            slack_payload["channel"] = self.channel

        body = json.dumps(slack_payload).encode("utf-8")
        req = urllib.request.Request(self.url, data=body,
                                      headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                resp.read()
        except urllib.error.URLError:
            pass


class DiscordSink(WebhookSink):
    """Discord webhook (slightly different format)."""

    def send(self, event: Event):
        emoji = {
            "error": "🔴", "ingest.done": "📥",
            "rag.done": "🤖", "agent.done": "✅",
        }.get(event.type, "ℹ️")

        payload_str = ", ".join(f"{k}={v}" for k, v in event.payload.items())
        discord_payload = {
            "content": f"{emoji} **{event.type}**: {payload_str[:1500]}",
            "username": "docs-toolkit",
        }
        body = json.dumps(discord_payload).encode("utf-8")
        req = urllib.request.Request(self.url, data=body,
                                      headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                resp.read()
        except urllib.error.URLError:
            pass
