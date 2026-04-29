"""EventBus core."""
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable


# Стандартные типы событий
EVENT_TYPES = {
    "ingest.start": "Старт ingest",
    "ingest.done": "Файл успешно ingested",
    "ingest.error": "Ошибка ingest",
    "rag.start": "RAG-запрос",
    "rag.done": "RAG ответ получен",
    "search.done": "Поиск завершён",
    "agent.step": "Шаг agent loop",
    "agent.done": "Agent завершил задачу",
    "job.queued": "Job добавлен в очередь",
    "job.started": "Worker подобрал job",
    "job.done": "Job завершён",
    "job.failed": "Job упал",
    "validation.error": "Документ не прошёл валидацию",
    "file.changed": "Файл изменился (watch)",
    "error": "Любая ошибка",
}


@dataclass
class Event:
    type: str
    payload: dict = field(default_factory=dict)
    ts: str = field(default_factory=lambda: datetime.now().isoformat(timespec='seconds'))
    source: str = ""             # «agent», «ingest», etc.

    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "payload": self.payload,
            "ts": self.ts,
            "source": self.source,
        }


class EventBus:
    """Простой event bus: emit() → handlers + sinks.

    handlers вызываются синхронно. sinks могут быть async (через ThreadPool).
    """

    def __init__(self):
        self._handlers: dict[str, list[Callable]] = defaultdict(list)
        self._sinks: list = []
        self._wildcard_handlers: list[Callable] = []

    def subscribe(self, event_type: str, handler: Callable):
        """Подписаться на конкретный тип event'а. '*' для всех."""
        if event_type == "*":
            self._wildcard_handlers.append(handler)
        else:
            self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable):
        if event_type == "*" and handler in self._wildcard_handlers:
            self._wildcard_handlers.remove(handler)
        elif handler in self._handlers.get(event_type, []):
            self._handlers[event_type].remove(handler)

    def add_sink(self, sink):
        """Добавить sink (Webhook/Jsonl/etc.)."""
        self._sinks.append(sink)

    def emit(self, event: Event):
        """Эмит event'а: вызывает handlers + sinks."""
        # Synchronous handlers
        for h in self._handlers.get(event.type, []):
            try:
                h(event)
            except Exception:
                pass
        for h in self._wildcard_handlers:
            try:
                h(event)
            except Exception:
                pass
        # Sinks
        for sink in self._sinks:
            if sink.should_emit(event):
                try:
                    sink.send(event)
                except Exception:
                    pass


_default_bus: EventBus | None = None


def get_default_bus() -> EventBus:
    global _default_bus
    if _default_bus is None:
        _default_bus = EventBus()
    return _default_bus
